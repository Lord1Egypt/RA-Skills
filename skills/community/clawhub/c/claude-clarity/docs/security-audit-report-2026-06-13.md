# Clarity 安全审计报告

**审计日期**: 2026-06-13
**审计框架**: OWASP Top 10 (2021)
**审计范围**: `/Users/apple/.claude/skills/claude-clarity` (v2.0.x)
**审计工具**: security-auditor 技能 + 人工代码审查
**审计文件**: 150+ files, ~51,640 行 JS

---

## 严重（必须修复）

### 1. [A03:Injection] code-executor.js — `execute()` 绕过沙箱隔离

- **文件**: `src/core/code/code-executor.js:456`
- **风险**: 高 — 任意代码执行
- **描述**: `execute()` 方法（非沙箱模式）仅检查 `DANGEROUS_PATTERNS` 黑名单（rm -rf, eval, exec, child_process, sudo rm, mkfs, dd），**不限制文件系统或网络访问**。用户代码可直接读取/写入任意文件或发起网络请求。真正的沙箱方法 `sandbox()`（line 760）是**opt-in**的——这意味着默认路径无文件/网络隔离。
- **DANGEROUS_PATTERNS 黑名单**（line 31-44）：
  ```javascript
  const DANGEROUS_PATTERNS = [
    /rm\s+-rf/i, /\.\.\/|\.\.\\|~\/|\/etc\/passwd/, /eval\s*\(/, 
    /exec\s*\(/, /child_process/, /sudo\s+rm/, /mkfs/, /\bdd\b/
  ];
  ```
- **修复**: 
  1. 将 `sandbox()` 设为默认执行模式，`execute()` 重命名为 `executeUnsafe()`
  2. 扩展 `DANGEROUS_PATTERNS` 覆盖更多危险模式（wget/curl/process.binding/fs.writeFileSync）
  3. 添加运行时文件系统访问代理（通过 fs 操作的 whitelist）
  4. 添加白名单环境变量白名单，阻止泄露 HEARTFLOW_* 密钥

### 2. [A03:Injection] code-verifier.js — 通过 spawn 直接执行用户代码

- **文件**: `src/core/code/code-verifier.js` (1573 行)
- **风险**: 高 — 任意代码执行
- **描述**: 使用 `child_process.spawn` 在子进程中执行用户提供的代码（支持 JS/Python/Shell），带 15 秒超时和结果缓存（MD5 指纹）。虽然带超时，但缺乏真正的沙箱隔离——Python 和 Shell 子进程可以访问完整的操作系统。`code-verifier.js` 中无 `DANGEROUS_PATTERNS` 黑名单。
- **修复**:
  1. 集成 `code-executor.js` 的 `sandbox()` 方法用于代码验证
  2. 为 Python/Shell 子进程添加专用沙箱（或使用 nsjail/bubblewrap 等容器化方案）
  3. 强制超时（已有）的同时添加输出大小限制（防止 fork bomb 类攻击）

### 3. [A04:Insecure Design] mcp-daemon.js — unhandledRejection 导致 DoS

- **文件**: `daemon/mcp-daemon.js:183`
- **风险**: 中-高 — 拒绝服务
- **代码**:
  ```javascript
  process.on('unhandledRejection', (reason) => {
    console.error('[ensure-mcp] unhandledRejection:', reason);
    process.exit(1);
  });
  ```
- **描述**: 任何未捕获的 Promise 拒绝会立即终止整个 MCP 守护进程。在多租户或长时间运行的场景中，一个插件/工具调用的 Promise 失败就能杀死所有活跃会话。
- **修复**:
  ```javascript
  process.on('unhandledRejection', (reason) => {
    console.error('[mcp-daemon] unhandledRejection:', reason);
    // 不要退出进程——记录并继续
  });
  ```

---

## 高（应修复）

### 4. [A02:Cryptographic Failures] AES 密钥文件可被读取

- **文件**: `src/core/memory.js:135-170`
- **风险**: 高 — 加密数据泄露
- **描述**: AES-256-GCM 加密密钥从 `HEARTFLOW_AES_KEY` 环境变量或 `.aes-key` 文件中读取。`.aes-key` 文件存储在 `memory/` 目录（权限 0o600）。代码本身包含风险注释（line 145）：
  ```
  // 风险：如果 .aes-key 文件被复制，攻击者可解密所有 LEARNED 层记忆
  ```
  同样的问题存在于 `self-healing-rl.js:42` 的 `.hmac-key` 文件。
- **修复**:
  1. 记录到文档中：强烈推荐使用环境变量而非文件回退
  2. 添加启动时警告（如果使用文件回退）
  3. 添加一个选项将密钥传递给内存中的 MCP 守护进程，无需写入磁盘
  4. 为 .aes-key 和 .hmac-key 添加 `.gitignore` 条目

### 5. [A01:Access Control] self-modifier.js — 补丁在审批前写入磁盘

- **文件**: `src/core/self-modifier.js:287-345`
- **风险**: 高 — 未经授权的文件写入
- **描述**: `metacognitiveModify()` 生成的补丁（.diff + .json）在 `requiresApproval: true`（line 323）设置下写入 `patches/` 目录。即使审批被拒绝，文件仍然保留在磁盘上。`applyApprovedPatch()`（line 417）通过 `fs.writeFileSync` 直接覆盖源文件。
- **控制**: 受 `HEARTFLOW_ENABLE_SELF_MODIFICATION=1` 保护——默认禁用。
- **修复**:
  1. 补丁在审批前写入临时目录（`/tmp/` 而非 `patches/`）
  2. 审批拒绝后自动清理补丁文件
  3. 添加补丁大小限制和对源文件的审计日志记录
  4. 明确记录：此功能专为沙箱/开发环境设计

### 6. [A05:Misconfiguration] 环境变量文档缺失

- **文件**: 无 `.env.example` 或 `.env` 模板
- **风险**: 中 — 配置错误
- **描述**: 代码库读取 10+ 个 `HEARTFLOW_*` 环境变量以及 `LLM_API_KEY`、`LLM_ENDPOINT`、`NODE_ENV` 等。但：
  - 没有 `.env.example` 文件展示哪些是必需的
  - 没有启动时检查确保关键变量已设置
  - 诸如 `HEARTFLOW_AES_KEY` 之类的密钥如果缺失会静默回退到文件 I/O
  - `HEARTFLOW_DATA_MINIMIZATION` 和 `HEARTFLOW_USER_CONSENT` 默认**未设置**——这会阻止内存持久化，但静默执行——管理员可能认为持久化正在工作
- **修复**:
  1. 创建 `.env.example` 列出所有变量并附上注释
  2. 在 `clarity.js` 启动时添加验证——如果 `HEARTFLOW_AES_KEY` 未设置则发出警告
  3. 对关键安全检查（如 `HEARTFLOW_ENABLE_SELF_MODIFICATION`）使用严格的三元组（`'1'` / `'0'` / 未设置）而不是 falsy 检查

### 7. [A09:Logging] 缺少安全事件日志

- **文件**: 整个代码库
- **风险**: 中 — 事件响应缓慢
- **描述**: 调试日志在所有模块中通过 `HEARTFLOW_DEBUG` 控制。但是没有：
  - 安全事件（密钥访问、补丁应用、外部连接）的审计日志
  - 文件修改或执行失败的记录轨迹
  - 谁/什么触发 `self-modifier.js` 的日志
- **修复**: 添加结构化安全日志记录：
  ```javascript
  // 添加到 core/audit-logger.js
  // 记录：event_type, timestamp, source, details
  // 写入：data/audit.log（仅追加，不可修改）
  ```

### 8. [A01:Access Control] meaningful-memory.js 持久化守卫静默阻塞

- **文件**: `src/core/meaningful-memory.js:290-298`
- **风险**: 中-低 — 用户意识缺失
- **代码**:
  ```javascript
  if (!process.env.HEARTFLOW_DATA_MINIMIZATION) {
    console.warn('[MeaningfulMemory] 持久化被阻止: HEARTFLOW_DATA_MINIMIZATION 未启用');
    return;
  }
  if (!process.env.HEARTFLOW_USER_CONSENT && !this._hasUserConsent()) {
    console.warn('[MeaningfulMemory] 持久化被阻止: 需要用户同意');
    return;
  }
  ```
- **描述**: 守卫逻辑本身是好的——持久化在没有同意时被阻止。但 `console.warn` 在生产运行中可能不被注意，并且没有抛出异常。用户可能在认为持久化激活时却没有。
- **修复**: 添加一次性启动警告，指示当前是否启用了内存持久化。

---

## 中（推荐）

### 9. [A05:Misconfiguration] 无 `npm audit` 或依赖扫描

- **风险**: 低-中
- **描述**: 使用 `acorn`（用于 AST 解析）、`blessed`（终端 UI）、`node-fetch`（外部 HTTP）等依赖项。未对已知 CVE 进行扫描。
- **修复**: 将 `npm audit` 作为 CI/安装后挂钩运行。在 README 中包含安全审计部分。

### 10. [A08:Data Integrity] 补丁文件无完整性检查

- **文件**: `src/core/self-modifier.js`
- **风险**: 低-中
- **描述**: `patches/` 目录中的 .diff/.json 补丁文件未签名或哈希——可以在不检测的情况下被篡改。
- **修复**: 对补丁内容添加 SHA-256 哈希验证，或使用 `HEARTFLOW_QTABLE_HMAC_KEY` 签署补丁元数据。

### 11. [A02:Cryptographic Failures] 无密钥轮换机制

- **文件**: `src/core/memory.js`, `src/core/self-healing-rl.js`
- **风险**: 低-中
- **描述**: `.aes-key` 和 `.hmac-key` 文件在写入后永不轮换。长期密钥暴露增加解密风险。
- **修复**: 在 memory.js 和 self-healing-rl.js 中添加密钥轮换方法。

### 12. [A01:Access Control] external-verifier.js 持久化缓存

- **文件**: `src/core/external-verifier.js:13`
- **风险**: 低
- **描述**: 验证结果缓存到 `data/verification-cache.json`，无论用户是否同意。数据量小，但绕过了 `meaningful-memory.js` 的同意守卫。
- **修复**: 使缓存目录可配置或遵守 `HEARTFLOW_DATA_MINIMIZATION`。

### 13. [A09:Logging] boot-cache.json 包含状态快照

- **文件**: `bin/boot-fast.js` `memory/boot-cache.json`
- **风险**: 低
- **描述**: 启动缓存 JSON 包含 `self-model.json`、`q-table.json`、`lesson-bank.json` 等内容的快照。如果这些包含敏感数据，缓存文件会反映出来。
- **修复**: 添加缓存 TTL 后的自动清理，或缓存仅引用元数据而非全文。

---

## 低（考虑）

### 14. openalex-client.js 用户代理标识可能暴露

- **文件**: `src/core/openalex-client.js`
- **描述**: 设置 `User-Agent: 'Clarity/1.0'`，这可以追溯到特定项目。不影响安全性，但如果是匿名化使用则值得注意。

### 15. LLM_API_KEY 在 intent-layer.js 中根据名称引用

- **文件**: `src/core/intent-layer.js:56-57`
- **描述**: `LLM_API_KEY` 环境变量被读取，但仅在没有设置时静默设为 `null`。连接尝试失败会暴露问题，但密钥值从未记录。

### 16. 无速率限制

- **描述**: MCP 工具和所有内部方法没有速率限制。在基于服务器的部署中，可以通过 MCP 工具通道进行冲击。

---

## 整体评估

| 类别 | 状态 | 说明 |
|------|------|------|
| 硬编码密钥 | ✅ 干净 | 源代码中无可发现的硬编码密钥 |
| 加密 | ✅ 良好 | AES-256-GCM 用于记忆，HMAC 用于 Q-table |
| 注入防护 | ⚠️ 部分 | DANGEROUS_PATTERNS 黑名单但过于简单；默认无沙箱 |
| 自我修改 | ✅ 守卫良好 | HEARTFLOW_ENABLE_SELF_MODIFICATION=1 默认禁用 |
| 外部通信 | ⚠️ 部分 | openalex-client.js 是真实的 HTTPS 客户端；明确记录 |
| 用户同意 | ✅ 良好 | 持久化守卫 + .user-consent 文件 |
| 文档安全 | ❌ 缺失 | 无 .env.example，无密钥轮换文档 |
| 安全事件日志 | ❌ 缺失 | 无独立的安全审计轨迹 |
| 依赖扫描 | ❌ 缺失 | 无 npm audit / CVE 检查 |
| 拒绝服务 | ⚠️ 脆弱 | unhandledRejection → process.exit(1) |

### 关键问题总结

### 必须修复（3 项）
1. **code-executor.js**: 使 `sandbox()` 成为默认值；`execute()` 不安全
2. **code-verifier.js**: 用户代码通过 spawn 执行，无沙箱
3. **mcp-daemon.js**: `process.exit(1)` 在 Promise 拒绝时——DoS 风险

### 应修复（5 项）
4. `.aes-key` / `.hmac-key` 文件在磁盘上暴露加密密钥
5. `self-modifier.js` 在审批前写入补丁到 `patches/`
6. 无 `.env.example` 或启动时变量验证
7. 无安全事件审计日志
8. 内存持久化守卫静默阻塞而不通知用户

### 推荐（4 项）
9. 无依赖扫描（`npm audit`）
10. 补丁完整性——补丁文件未签名
11. 无密钥轮换机制
12. 外部验证器缓存绕过同意守卫

---

## 自修复生效的变更（从 Phase 1 起）

从之前的 SkillSpector 审计阶段开始，以下内容已在 SKILL.md、README.md、EVOLUTION_SYSTEM.md、reasoning-checklist.md 和 pricing.md 中修复：

- ✅ 从安全表中删除了关于 openalex-client.js 的误导性 "无外部通信" 声明
- ✅ 在 EVOLUTION_SYSTEM.md 中添加了设计概念警告，关于自动 git 提交
- ✅ 从 reasoning-checklist.md 中删除了危险的 "自主决策 / 求用户是推卸责任" 语言
- ✅ 从 pricing.md 中移除了虚假的临床验证声明
- ✅ 修正了 README.md 和 SKILL.md 中的身份声明

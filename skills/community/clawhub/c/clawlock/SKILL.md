---
name: clawlock
description: >
  ClawLock — 综合安全扫描、红队测试与加固工具，支持全平台。
  当用户明确要求安全扫描、安全体检、安全加固时触发：
  「开始安全体检」「安全扫描」「检查 skill 安全」「安全加固」「探测实例」
  「scan my claw」「security check」「drift detection」「red team」「红队测试」
  「React2Shell」「agent-scan」「发现安装」「凭证权限」
  Do NOT trigger for general coding, debugging, or normal Claw usage.
metadata:
  clawlock:
    version: "2.5.0"
    homepage: "https://github.com/g1at/ClawLock"
    author: "g0at"
    compatible_with: [openclaw, zeroclaw, claude-code, generic-claw]
    platforms: [linux, macos, windows, android-termux]
    requires:
      python: ">=3.9"
      pip_package: "clawlock"
      bins:
        - clawlock    # 主二进制，配合 autoAllowSkills 可自动授权
      bins_optional:
        - promptfoo
---

# ClawLock

综合安全扫描、红队测试与加固工具。支持 OpenClaw · ZeroClaw · Claude Code · 通用 Claw。
运行于 Linux · macOS · Windows · Android (Termux)。

[English Version → SKILL_EN.md](SKILL_EN.md)

---

## 安装与使用

```bash
pip install clawlock          # 安装
clawlock scan                 # 全面安全扫描
clawlock discover             # 发现所有安装实例
clawlock precheck ./SKILL.md  # 新 skill 导入预检
clawlock harden --auto-fix    # 加固（自动修复真正安全的本地变更）
clawlock scan --format html   # HTML 报告
```

作为 Claw Skill 安装：复制本文件到 skills 目录，并在对应 Claw 产品对话中发起安全检查请求。

---

## 触发边界

触发后按以下分类对号入座，**不要跨类执行**：

| 用户意图 | 执行功能 | 外部依赖 |
|---------|---------|---------|
| 全面安全体检 / health check | **Feature 1: 全量扫描** | 无 |
| 某个 skill 是否安全 / 安装前审计 | **Feature 2: Skill 单体审计** | 无 |
| 导入新 skill 前检查 | **Feature 3: Skill 导入预检** | 无 |
| 加固 / 收紧配置 | **Feature 4: 安全加固向导** | 无 |
| SOUL.md / Memory 文件 drift | **Feature 5: Drift 检测** | 无 |
| 发现系统上的安装 | **Feature 6: 安装发现** | 无 |
| 红队 / jailbreak 测试 | **Feature 7: LLM 红队测试** | ⚠️ 需 Node.js + promptfoo / npx |
| MCP 服务器是否安全 | **Feature 8: MCP 深度扫描** | 无（内建引擎） |
| React2Shell / CVE-2025-55182 | **Feature 9: 依赖漏洞检查（并入代码扫描）** | 无 |
| Agent 多智能体安全扫描 | **Feature 10: Agent-Scan** | 无（内建引擎） |
| 查看扫描历史趋势 | **Feature 11: 扫描历史** | 无 |
| 持续监控模式 | **Feature 12: 持续监控** | 无 |

不要将普通的 Claw 使用、项目调试、依赖安装当作触发本 skill 的理由。

---

## 隐私声明

绝大多数检查在**本地运行**。只有在对应功能被启用时，才会发起以下网络请求：

| 请求场景 | 发送数据 | 绝不发送 | 依赖 |
|----------|----------|----------|------|
| CVE 情报查询 | 产品名（固定字符串）+ 版本号 | 无文件内容、无凭证、无会话记录 | 无（内建） |
| Skill 威胁情报查询 | skill 名称 + 来源标签 | 无代码内容、无用户数据 | 无（内建） |
| Agent-Scan LLM 语义评估（可选） | 代码片段（截断到 8K 字符） | 无完整源码、无凭证 | 需 `--llm` + API key |
| promptfoo 红队测试（可选） | 测试 Prompt 载荷 | 无本地文件 | 需 Node.js，并通过 promptfoo 或 npx 运行 |

离线优先写法：

- 全量扫描离线：`clawlock scan --no-cve --no-redteam`
- 单体审计离线：`clawlock skill /path/to/skill --no-cloud`
- 如未启用 `--llm`，Agent-Scan 不会发起 LLM 请求

在 Claw 产品对话里，必须明确告诉用户：**本次哪些在线能力实际运行了，哪些被跳过了，哪些暂不可用。**

云端地址可自定义：`export CLAWLOCK_CLOUD_URL=https://your-instance`。

---

## 执行前安全提醒

在实际调用 `clawlock` 前，先做以下最小核对：

1. 确认当前要调用的 `clawlock` 就是预期安装版本，不要误用同名脚本或旧版本二进制。
2. 确认扫描目标是用户明确指定的对象，不要把测试命令误打到生产地址或无关目录。
3. 如用户明确要求本地优先或离线评估，优先关闭可选在线能力，再继续执行。
4. 如运行红队测试，先确认当前环境允许访问目标端点，且该目标确实适合做安全测试。

---

## 版本更新预检

在进入任何安全扫描、导入预检、加固或 drift 检查前，**默认先检查 `clawlock` 在 PyPI 上是否有新版本，以及 GitHub 仓库中的最新 skill 文件是否比本地更新**：

```bash
clawlock version --check-update --json --skill-path /path/to/SKILL.md
```

执行规则：

1. `clawlock` 本体版本以 **PyPI 最新版本** 作为唯一事实来源。
2. skill 版本以 **GitHub 仓库 `main` 分支中的最新 skill 文件** 为准：
   - 中文版 skill 对应 `https://github.com/g1at/ClawLock/blob/main/skill/SKILL.md`
   - 英文版 skill 对应 `https://github.com/g1at/ClawLock/blob/main/skill/SKILL_EN.md`
3. 如果检测到有新版本，或发现 GitHub 中的最新 skill 文件比本地更新，先明确告诉用户：
   - 当前本地版本
   - PyPI 最新版本
   - GitHub 上 skill 的最新版本
   - 将要执行的更新动作
4. 然后**让用户选择**是否先更新，再继续后续安全操作。
5. 如果用户同意更新：
   - 由 skill 在当前 Claw 对话中直接执行更新，不要只把手工命令抛给用户
   - `clawlock` 本体更新动作：执行 `pip install -U clawlock`
   - skill 更新动作：从 GitHub 仓库拉取对应语言版本的最新 `skill/SKILL*.md`，替换本地 skill 文件后再继续
   - 更新完成后，再重新执行版本检查，确认本体与 skill 都已到最新状态
6. 如果当前 Claw 产品没有足够的工具权限、网络权限或文件写入能力，才退回为“告诉用户需要执行什么更新动作”，并明确说明为什么这次无法由 skill 直接完成更新。
7. 如果用户拒绝更新：继续使用当前版本执行，但必须明确说明“以下结果基于当前已安装版本”。
8. 如果版本检查失败、超时或网络不可用：继续后续扫描，但必须明确写出“本次未完成版本更新检查”。

隐私边界：
- 该预检会访问在线版本源。
- 只发送查询 PyPI 所需的包名，并读取 GitHub 仓库中的公开 skill 文件；**不发送本地代码内容、凭证、会话记录**。

---

## 降级与跳过规则

在 Claw 产品对话场景中，遇到以下情况时必须优雅降级，并把原因写清楚：

- CVE 接口不可用：继续其余本地扫描，并明确写「本次未完成在线 CVE 匹配」。
- Skill 云端情报不可用：继续本地静态分析，并明确写「云端情报暂不可用，本结论基于本地规则」。
- 未启用 `--llm`、缺少 API key，或模型请求失败：保留本地 Agent-Scan 结果，并明确写「LLM 语义评估未执行」或失败原因。
- 缺少 Node.js / promptfoo / npx / endpoint：跳过红队测试，并明确写「红队测试已跳过」及原因。
- 任何检查被跳过、失败或暂不可用时，都**不得**改写成“已通过”或“未发现问题”。

---

## Feature 1: 全量安全扫描

并发执行 8 个核心安全域扫描；默认 `scan` 已纳入 Agent 安全的配置层检查。
如需代码层 Agent 审计，额外运行 `clawlock agent-scan --code <path>`。如果提供了 `--endpoint` 且没有传
`--no-redteam`，ClawLock 会在核心扫描完成后追加可选的第 9 步红队测试，
最后输出一份统一报告。

```bash
clawlock scan                                    # 自动识别平台
clawlock scan --adapter openclaw --format json   # 指定适配器 + JSON
clawlock scan --mode monitor                     # 仅报告不阻断
clawlock scan --mode enforce                     # 发现高危 exit 1
clawlock scan --format html -o report.html       # HTML 报告
clawlock scan --endpoint http://localhost:8080/v1 # 含红队测试
clawlock scan --no-cve                           # 离线模式
```

### Step 1 — 配置安全审计 + 危险环境变量

读取 Claw 配置文件，执行内建审计（如有），再叠加 ClawLock 自研规则检查：

| 风险项 | 触发条件 | 等级 |
|--------|---------|------|
| Gateway 鉴权 | `gatewayAuth: false` | 🔴 严重 |
| 文件访问范围 | `allowedDirectories` 含 `/` | 🟡 警告 |
| 浏览器控制 | `enableBrowserControl: true` | 🟡 警告 |
| 网络白名单 | `allowNetworkAccess: true` 无白名单 | 🟡 警告 |
| 服务绑定 | `server.host: 0.0.0.0` | 🔴 严重 |
| TLS 状态 | `tls.enabled: false` | 🟡 警告 |
| 操作审批 | `approvalMode: disabled` | 🟡 警告 |
| 速率限制 | `rateLimit.enabled: false` | 🟡 警告 |
| 硬编码凭证 | 正则匹配 11 种 API Key / Token 格式 | 🔴 严重 |
| 危险环境变量 | NODE_OPTIONS / LD_PRELOAD / DYLD_INSERT_LIBRARIES 等 11 个 | 🟠 高危 |
| 会话保留 | `sessionRetentionDays > 30` | 🔵 信息 |

**解读规则：** 将内建审计发现视为**配置风险提示**，不直接映射为「确认的严重攻击」。用「存在风险，建议收紧」的语气。

**输出要求：** 安全项与风险项都要展示。安全项示例：`✅ | Gateway 鉴权 | 已开启，外部无法直接连接。` 每一项只写「当前状态 + 可能后果 + 建议」，不超过一行。不要混入来自 Step 2-8 的内容。

### Step 2 — 进程检测 + 端口暴露

跨平台检测运行中的 Claw 进程和对外监听的端口（Linux: ps+ss, macOS: ps+lsof, Windows: tasklist+netstat）。

### Step 3 — 凭证目录权限审计

跨平台检查凭证文件/目录是否对其他用户可读（Unix: stat 位, Windows: icacls ACL）。

### Step 4 — Skill 供应链风险扫描

整合**云端威胁情报** + **本地 63 模式静态分析**。

#### 4.1 云端情报查询

> 数据发送：仅 skill 名称 + 来源标签。不发送代码内容。

| verdict | 处理方式 |
|---------|---------|
| `safe` | 标记安全，继续本地扫描确认 |
| `malicious` | 🔴 严重，记录原因 |
| `risky` | 结合本地分析判断等级 |
| `unknown` | 仅执行本地静态扫描 |
| 请求失败 / 超时 / 非 200 / 空内容 / 无效 JSON | 视为不可用，继续本地扫描并标注「云端情报暂不可用」|

**韧性规则：** 云端失败不阻断扫描。一个 skill 失败不阻止其他 skill。

#### 4.2 本地静态分析（63 模式）

🔴 严重（确认恶意）：凭证外传(curl/wget) · 反弹Shell(bash/nc/Python/mkfifo) · 挖矿 · 批量删除 · chmod 777 · 提示词注入(覆盖/劫持/越狱/中文) · 混淆载荷(base64→shell) · 零宽字符 · Shell 命令嵌套混淆（`sh -c`/`bash -c`/`cmd /c` 多层包装绕过检测）

🟠 高危：Unicode 转义混淆 · 硬编码凭证 · AI API 密钥 · 危险环境变量export · Cron持久化 · DNS外传 · 用户输入直接进eval · 递归删除系统目录

🟡 警告（高权限但可能合理）：eval/exec · subprocess · 凭证类环境变量 · 隐私目录访问 · 系统敏感文件 · 外部HTTP请求 · 动态模块导入 · ctypes/cffi · pickle反序列化 · 不安全YAML加载 · socket服务端 · webhook · 系统服务注册

**判断原则：** 升级到 🔴 严重**必须**有明确越权、外传、破坏、恶意迹象之一。`eval`、`subprocess`、API 密钥读写**单独存在**时只判 🟡 警告。结合「声明用途 × 实际行为 × 是否外传」综合判断。

**输出要求：**
- 有风险的 skill 写清：权限 + 用途是否一致 + 建议
- 安全 skill 超过 5 个时折叠为：`其余 {N} 个 ✅ 当前未发现明确高风险`
- **当前正在执行扫描的 ClawLock 自身不纳入 Step 4 统计**

### Step 5 — 系统提示词 + 记忆文件 Drift 检测

扫描 SOUL.md / CLAUDE.md / HEARTBEAT.md / MEMORY.md / memory/*.md：
1. **Prompt 注入** — 指令覆盖 / 角色劫持 / 越狱关键词 / 隐藏指令
2. **编码混淆** — Unicode smuggling · base64 长字符串
3. **SHA-256 Drift** — 与 `~/.clawlock/drift_hashes.json` 基准对比

**安全守则：** 不读取、不枚举相册 / ~/Documents / ~/Downloads / 聊天记录 / 日志正文。不执行 sudo / TCC 绕过 / 沙箱逃逸。仅读配置元数据、权限状态、文件哈希。

### Step 6 — MCP 暴露面 + 隐式工具投毒（10 个风险信号）

扫描 MCP 配置文件，检测：

| 风险项 | 等级 |
|--------|------|
| 绑定 0.0.0.0（对外网暴露） | 🔴 严重 |
| 连接非 localhost 远程端点 | 🟡 警告 |
| env 中含凭证字段（明文） | 🔴 严重 |
| env 中含危险变量 (NODE_OPTIONS 等) | 🟠 高危 |
| 参数篡改 (Parameter Tampering, ASR≈47%) | 🔴 严重 |
| 函数劫持 (Function Hijacking, ASR≈37%) | 🟠 高危 |
| 隐式触发器 (Implicit Trigger, ASR≈27%) | 🔴 严重 |
| Rug Pull 迹象 | 🟡 警告 |
| 工具覆盖 (Tool Shadowing) | 🟠 高危 |
| 跨域权限提升 | 🟡 警告 |

检测覆盖所有 LLM 可见字段：description · annotations · errorTemplate · outputTemplate · inputSchema 参数描述。

### Step 7 — CVE 版本漏洞匹配

查询 ClawLock 云端漏洞情报库。

**韧性规则：** 接口不可用时，明确提示「本次未完成在线漏洞匹配，建议稍后重试」，**不输出「未发现漏洞」**。漏洞超过 8 个时只列最严重的 8 个，表后补充「另有 N 个，建议升级到最新版」。

### Step 8 — LLM 红队测试（可选，需 --endpoint）

9 个 agent 专项插件 × 8 种攻击策略（含编码绕过）。

> ⚠️ **外部依赖：** 此功能需要 Node.js 环境，并通过 `promptfoo` 或 `npx` 运行（例如 `npm install -g promptfoo`，或直接使用 `npx promptfoo@latest`）。如果当前环境无法安装，请跳过此步骤，不影响其余 8 个核心安全域的完整性。Skill 环境中通常无 Node.js，此步会自动跳过并提示原因。

---

## Feature 2: Skill 单体审计

```bash
clawlock skill /path/to/skill-dir
clawlock skill /path/to/SKILL.md --no-cloud
```

### 审计流程

**Step 1 — 判断是否需要云端查询：**

| Skill 来源 | 处理方式 |
|-----------|---------|
| `local` / `github` | 跳过云端查询，直接本地审计 |
| `clawhub` 或其他托管仓库 | 先查询云端情报，再叠加本地审计 |
| 云端返回 `unknown` / 请求失败 | 回退到本地审计 |

**Step 2 — Skill 信息收集：**

收集最少量上下文用于审计（不生成长篇背景分析）：
- Skill 名称 + SKILL.md 声明的用途（1 句）
- 可执行逻辑的文件清单：scripts/、shell、package.json、config
- 实际使用的能力：文件读写/删除 · 网络请求 · Shell/子进程 · 敏感访问 (env/凭证/隐私路径)
- 声明权限 vs 实际使用权限的偏差

**Step 3 — 本地静态分析：** 使用 63 模式引擎确定性扫描，判断原则同 Feature 1 Step 4。

### 输出规范（严格执行，不展开成全量报告）

无高风险时：
> 经检测暂未发现高风险问题，可继续评估后安装。

有需关注但无明确恶意时：
> 发现需关注项，但当前未见明确恶意证据。该 skill 具备 `{具体能力}`，主要用于完成 `{SKILL.md 声明用途}`；建议仅在确认来源可信、权限范围可接受时使用。

有确认风险时：
> 发现风险，不建议直接安装。该 skill `{主要风险描述}`，超出了声称的功能边界。建议先下线当前版本，确认来源和代码后再决定。

**禁止绝对措辞：** 不使用「绝对安全」「可放心使用」「没有任何风险」。结论限定为「当前静态检查范围内」的评估。

---

## Feature 3: Skill 导入预检

**当用户引入新的 SKILL.md 时，自动执行安全预检，及时告知用户风险。**

```bash
clawlock precheck ./new-skill/SKILL.md
```

6 维度检测：
1. **Prompt 注入** — 63 个恶意模式匹配（含中文）
2. **Shell 反混淆** — 递归解包 `sh -c`/`bash -c`/`cmd /c` 嵌套后再匹配
3. **敏感权限声明** — sudo/root/全盘访问/危险环境变量
4. **可疑 URL** — .xyz/.tk/.ml 等高风险 TLD
5. **隐藏内容** — 零宽字符 (Unicode smuggling)
6. **异常体积** — 文件大小超过 50KB

---

## Feature 4: 安全加固向导

```bash
clawlock harden                          # 交互式
clawlock harden --auto                   # 应用安全动作并输出人工指导
clawlock harden --auto-fix               # 自动修复真正安全的本地变更
clawlock harden --from-scan --auto-fix   # 仅处理上次 scan 报告的高危项
clawlock harden --verify                 # 加固后重新校验、生成差异报告
clawlock harden --rollback               # 按备份回滚最近一次加固动作
```

| ID | 措施 | 体验影响 | 需确认 | Auto-fix | LLM 可协助修复 |
|----|------|---------|--------|---------|--------------|
| H001 | 限制文件访问到工作区 | ⚠️ 跨目录 skill 失效 | 是 | 否 | ✅ |
| H002 | 开启 Gateway 鉴权 | ⚠️ 外部工具需重配 token | 是 | 否 | ✅ |
| H003 | 缩短会话日志保留 | ⚠️ 历史不可查 | 是 | ✅ 是 | — |
| H004 | 关闭浏览器控制 | ⚠️ 依赖浏览器的 skill 停用 | 是 | 否 | ✅ |
| H005 | 配置网络白名单 | 无影响 | 否 | 否 | ✅ |
| H006 | 审核 MCP 配置 | 仅指导 | 否 | 否 | ⚠️ 协助核查 |
| H007 | 建立提示词/记忆基准 | 无影响 | 否 | ✅ 是 | — |
| H008 | 启用操作审批 | ⚠️ 每次高危操作需确认 | 是 | ✅ 是 | — |
| H009 | 收紧凭证目录权限 | 无影响 | 否 | ✅ 是 | — |
| H010 | 配置速率限制 | 无影响 | 否 | 否 | ✅ |
| H011 | 禁止下载即执行 / 运行时远程安装 | ⚠️ 自举安装脚本可能失效 | 是 | 否 | ⚠️ 协助核查 |
| H012 | 禁止 Windows LOLBins / 脚本宿主 | ⚠️ Windows 管理脚本可能失效 | 是 | 否 | ⚠️ 协助核查 |
| H013 | 清理持久化落点 | ⚠️ 后台任务可能停止 | 是 | 否 | ⚠️ 协助核查 |
| H014 | 禁止隧道 / 反向代理 | ⚠️ 远程调试隧道可能失效 | 是 | 否 | ⚠️ 协助核查 |
| H015 | 收紧 MCP 鉴权 / 绑定 / CORS | ⚠️ 外部 MCP 工具可能需重配 | 是 | 否 | ✅ |
| H016 | 禁止用户控制动态模块加载 | ⚠️ 热加载插件可能失效 | 是 | 否 | ⚠️ 协助核查 |
| H017 | 对提示词与凭证日志脱敏 | ⚠️ 调试日志会变少 | 是 | 否 | ✅ |
| H018 | 清理不安全 prompt / skill 指令 | ⚠️ 不安全自动化措辞会失效 | 是 | 否 | ✅ |

**规则：需二次确认的措施必须先向用户展示体验影响（黄色），等待明确 `y` 后才执行。默认 No。**

**执行说明：** 加固向导按「可直接自动修复 / LLM 辅助可修复 / 仅给指导」分组展示措施。`H003` / `H007` / `H008` / `H009` 会执行本地自动修复（写入前会备份到 `~/.clawlock/backups/<timestamp>/` 并记录到 `~/.clawlock/hardening_log.json`，可通过 `clawlock harden --rollback` 回滚）。其余措施多为配置或运维变更，若未真正改动，不应描述为"已应用"。

### LLM 辅助加固流程

对于上表 `Auto-fix = 否` 的项，Claw LLM 可使用自身的文件编辑能力协助完成剩余加固。按以下五步执行，**不得跳过任何一步**：

**Step 1 — 获取结构化发现**

```bash
clawlock scan --format json
```

从输出的 `findings` 数组按 `level ∈ {critical, high, medium}` 过滤出待修复项，保留 `title` / `location` / `detail` 三个字段作为后续修复依据。

**Step 2 — 优先执行 CLI 自动修复**

```bash
clawlock harden --from-scan --auto-fix
```

这一步会基于 Step 1 的结果，只对命中的发现执行 `H003` / `H007` / `H008` / `H009` 自动修复，并生成备份与日志。**先跑这一步再让 LLM 介入**，避免 LLM 重复处理 CLI 已能解决的项。

**Step 3 — LLM 按发现定位配置**

对每个剩余的 guidance-only 发现，依据 `location` 字段找到目标文件。常见目标：

- `~/.openclaw/config.*` · `~/.zeroclaw/config.*` · `~/.claude/settings.json`
- MCP server JSON（通常在 `~/.claude/mcp_servers.json` 或项目级 `.mcp.json`）
- Skill 脚本 / SKILL.md / SOUL.md

**必须先 Read 再改，不要盲写。** 如果文件不存在或无权限，跳过并说明原因。

**Step 4 — 展示"当前 → 目标 + 体验影响"并等用户确认**

每个拟修改项按以下格式展示给用户，**默认 No**：

```md
- 文件：{path}
- 当前：{current_value}
- 目标：{target_value}
- 修复依据：{finding title}（{finding level}）
- 体验影响：{上表对应的 UX 影响}
- 是否应用？(y/N)
```

用户逐项回答 `y` 才执行。批量 `y` 需用户明确表达。

**Step 5 — 应用并二次验证**

应用后运行：

```bash
clawlock harden --verify
```

`--verify` 会重新跑 `scan_config` 与 `scan_credential_dirs`，对比加固前后的 critical / high 数量并输出差异报告。如果剩余风险未下降，向用户说明原因（常见：文件未落盘 / 写到错路径 / 字段名写错），**不得将 Step 5 省略**。

### LLM 辅助加固的安全约束

- **必须备份：** 在写入前，把原文件复制到 `~/.clawlock/backups/<timestamp>/` 并在 `~/.clawlock/hardening_log.json` 追加一条记录（measure_id / files_changed / backup_path），使 `clawlock harden --rollback` 能按统一入口回滚
- **不得越权：** 禁止 `sudo` / `chmod -R 777` / 跨用户目录写入 / 系统级服务安装 / 关闭 SELinux 或 AppArmor
- **最小必要变更：** 不对不相关配置做顺带优化或美化；保留原注释、字段顺序、缩进风格
- **不伪造"已应用"：** 若某项需用户手动操作（如禁用 Windows 服务、移除 cron 任务、卸载恶意 skill），只写"建议手动执行并给出命令"，不得报告为已完成
- **凭证不入日志：** LLM 补齐的 token / secret 必须引用 env 变量或 secret 管理器占位符（如 `${GATEWAY_TOKEN}`），严禁将实际值写进 config 或对话
- **跨平台拒写：** 当要改的路径在当前 OS 上不存在或权限不足时，直接跳过并明确说明，不要在无关目录制造新文件
- **信任边界：** 只基于 `clawlock scan` 的 findings 采取行动；不得自行扩大修复范围，不得编辑 findings 未命中的文件

### LLM 可修复措施的具体映射

| 措施 | LLM 的具体动作 |
|------|--------------|
| H001 | 修改 Claw 配置 `allowedDirectories`，用当前工作区绝对路径替换 `/` 或 `~` |
| H002 | 在 Claw 配置里把 `gatewayAuth` 改为 `true`，并让用户填入 token env 变量名（不是明文） |
| H004 | 设 `enableBrowserControl: false`；如存在依赖浏览器的 skill，先提醒用户这些 skill 会停用 |
| H005 | 为 `allowNetworkAccess: true` 补出明确的 `allowedDomains` 白名单（让用户逐条确认） |
| H006 | 按 Feature 1 Step 6 的 10 个 MCP 风险信号逐条核对，列出差异后让用户决定 |
| H010 | 在 Claw 配置里加 `rateLimit: { enabled: true, requestsPerMinute: 60 }` |
| H011–H014 | 协助搜索 skill / script / cron / launchctl / 计划任务 中的可疑持久化或隧道命令，列给用户确认后移除（不自动删） |
| H015 | 修改 MCP server JSON：`host` 改为 `127.0.0.1`、启用鉴权、限制 CORS `origin` |
| H016 | 搜索 skill 中的 `import(user_input)` / `importlib.import_module(user_input)` / `require(user_input)` 并引导收紧 |
| H017 | 在日志 / 提示词配置里启用脱敏开关，或对敏感字段加 mask |
| H018 | 按 `scan_skill` 报告的行号，将不安全的措辞改写为合规表达（如去掉"绕过确认""跳过审计"字样） |

不在此表的项视为**仅给指导**，LLM 不得尝试自动改写。

---

## Feature 5–10: 其他功能

```bash
clawlock soul --update-baseline    # Drift 基准更新
clawlock discover                  # 安装发现 (~/.openclaw / ~/.zeroclaw / ~/.claude)
clawlock redteam URL --deep        # 红队 (10 插件 × 8 策略) ⚠️ 需 promptfoo / npx
clawlock mcp-scan ./src            # MCP 深度代码扫描（含依赖漏洞 / React2Shell 检查）
clawlock agent-scan --code ./src   # OWASP ASI 14 类别（含依赖漏洞 / React2Shell 检查）
clawlock agent-scan --code ./src --llm           # 追加 LLM 语义评估层
```

> **依赖说明：** 除 `clawlock redteam` 需要 Node.js，并通过 `promptfoo` 或 `npx` 运行外，所有其他命令仅需 `pip install clawlock`，零外部二进制依赖。

---

## Feature 11: 扫描历史

```bash
clawlock history            # 查看最近 20 条扫描记录
clawlock history --limit 50 # 查看最近 50 条
```

自动记录每次 `clawlock scan` 的评分、高危数、需关注数和设备指纹，持久化存储到 `~/.clawlock/scan_history.json`。支持趋势对比（📈 评分提升 / 📉 评分下降）。

## Feature 12: 持续监控

```bash
clawlock watch                    # 每 5 分钟扫描一次，Ctrl+C 停止
clawlock watch --interval 60      # 每 60 秒一次
clawlock watch --count 10         # 扫描 10 轮后自动停止
```

定期重扫配置 Drift + 记忆文件 Drift + 进程变化，发现高危变化时即时告警。适合部署后长期监控。

---

## Claw 产品对话输出规则

**以下规则适用于 OpenClaw、ZeroClaw、Claude Code 与其他兼容 Claw 产品中的 skill 对话。安全判定以本地 ClawLock CLI 输出为准。**

### 单一事实来源原则

- **ClawLock 负责做安全评估，LLM 不负责重判。**
- 在 Claw 产品对话里，LLM 只负责解释影响、可能后果、修复优先级和对普通用户的操作含义。
- 不得重新计算、放大、减弱或“归一化” ClawLock 的结论、评分、等级、严重程度或发现列表。
- 如果当前 CLI 输出里没有某个字段，就不要自行推断、补齐或伪造一个替代值。

### 各功能的输入优先级

- **Feature 1 全量扫描：** 优先使用 `clawlock scan --format json`
  - 当前 JSON 稳定提供：`time`、`adapter`、`device`、`score`、`grade`、`domain_grades`、`domain_scores`、`findings`
- **Feature 2 单体审计：** 优先使用默认 text 输出作为“最终结论”的来源
  - 当前 `clawlock skill --format json` 只返回 findings 列表，不包含给用户看的结论语气
- **Feature 3 precheck / Feature 5 drift / 其他聚焦命令：** 在没有结构化总结格式前，默认 text 输出就是规范结果
- 如果 text 和 JSON 同时可用：结论以 text 为准，JSON 只用于补充结构化发现细节

### Claw 产品面向用户的输出契约

统一分成两段：

```md
# ClawLock 结果

{只引用或转述 ClawLock 已经给出的事实}

### 影响分析

{LLM 面向普通用户解释：会发生什么、最该先处理什么、接下来怎么做}
```

规则如下：

- `ClawLock 结果` 里只有在 CLI 明确给出时，才可以出现评分、等级、结论、发现计数
- 对于全量扫描，可以展示 `domain_grades` 和 `domain_scores`，因为 `scan --format json` 里确实存在
- 不得自行补出“每一步计数”“每个安全域的严重/高危/警告总数”“固定 Step 1-8 表格”等当前输出里不存在的字段
- 不要把终端框线、进度条、颜色标记或大段原始 CLI 文本直接搬进对话
- 不要把多个命令的输出再拼成一份新的“综合总报告”；每个命令各自保持原结论

### 各功能的转述方式

- **Feature 1 全量扫描：** 先引用 ClawLock 给出的 `score`、`grade`、可用的安全域评级与最高优先级发现，再补充影响分析
- **Feature 2 / 3 / 5 单目标检查：** 先引用 ClawLock 的结论句，再用通俗语言解释影响
- **如果命令明确说某项检查被跳过或暂不可用，必须保留原语义。** 不得把“skipped”说成“passed”，也不得把“发现风险”淡化成“仅需关注”

### 允许与禁止

| ✅ 允许 | ❌ 禁止 |
|---------|---------|
| 原样引用 ClawLock 已给出的结论 / 评分 / 等级 | 重新算出另一套评分、等级或总判断 |
| 用通俗语言解释影响 | 添加 ClawLock 没报告的发现 |
| 帮用户排优先级 | 删除发现，或弱化已报告的严重程度 |
| 提醒静态分析局限、说明某项检查被跳过 | 编造表格、计数或步骤摘要 |

---

## 统一写作规则

- **全部面向用户输出使用用户当前语言**（CVE ID、代码、命令除外）
- 面向普通用户，少用专业词汇，用「会带来什么后果」「建议怎么做」的语气
- 只使用 Markdown 标题、表格、引用和短段落；不使用 HTML 或复杂布局
- 每个表格单元格尽量只写 1 句；最多「问题 + 建议」合并一句
- 不在表格内换行成段
- 不混用长句、项目符号清单和额外总结
- 能用日常话说清楚的地方，不使用「暴露面」「攻防面」等抽象术语；改用「别人更容易从外网访问你的系统」这类描述
- 不使用「绝对安全」「可放心使用」「已彻底解决」「没有任何风险」等绝对措辞
- 单项审计（Feature 2）只输出简洁结论，**不展开成全量报告**

---

## 语言适配

本 SKILL.md 为中文版本，配套英文版 [SKILL_EN.md](SKILL_EN.md)。输出语言跟随用户语言：用户用中文提问，输出中文；用户用英文提问，输出英文。CVE ID、命令、代码等专有名词保持原文。

## 扫描启动提示

在开始任何扫描（Feature 1–10）前，必须先输出一行启动提示：

```
🔍 ClawLock 正在检测 {目标} 安全性，请稍候...
```

将 `{目标}` 替换为实际内容（如 `Claw 环境`、`my-skill`、`当前工作区`）。

---

## 能力边界声明

本 skill 执行**静态分析**，无法：
- 检测纯运行时的恶意行为
- 保证不存在未知漏洞
- 执行真实攻击或确认漏洞可利用性
- 读取系统隐私目录、会话记录、媒体文件

MCP 深度扫描和 Agent-Scan 使用内建 Python 引擎（正则 + AST 污点追踪），零外部二进制依赖。内建引擎基于已知模式匹配，对复杂的跨函数语义漏洞覆盖有限；如需 LLM 驱动的语义级分析，可通过 `--llm` 选项启用（需要 API key）。

所有结论均为「当前检查范围内」的最佳评估。

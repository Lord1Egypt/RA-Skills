---
name: coding-framework
description: "统一编程框架。整合 Hook 守卫 + 标准化代理 + 多代理审查 + 迭代循环 + YAGNI 决策阶梯。一个 skill 覆盖完整编程工作流。"
version: 10.2.0
---

# Coding Framework — 统一编程框架 v1.0

## 你是谁

你是一个资深编程框架，整合了业界最佳实践：
- Claude Code 的 Hook 事件系统和多代理审查
- Claude Plugins Official 的安全审核和渐进式披露
- OpenAI Codex 的标准化代理定义和安全沙箱
- Ponytail 的 YAGNI 决策阶梯和代码精简哲学

## 工作模式

### 模式 1：快速编码（默认）

触发：用户要求写代码

流程：
1. 应用 Ponytail 决策阶梯（7 级）
2. 选择最简方案
3. 输出格式：`[code] → skipped: [X], add when [Y]`

### 模式 2：代理审查

触发：用户要求审查代码 / "review"

流程：
1. 根据代码特征选择代理（1-7 个）
2. 并行 spawn 子代理执行审查
3. 按严重度分级阈值过滤发现
4. 合并去重，汇总为统一审查报告

**置信度分级阈值**（v10.1 改进）：

| 严重度 | 置信度阈值 | 说明 |
|--------|------------|------|
| Critical | ≥ 50 | 安全漏洞、数据丢失风险，低阈值确保不漏报 |
| High | ≥ 70 | 逻辑错误、性能问题 |
| Medium | ≥ 80 | 代码风格、最佳实践 |
| Low | ≥ 90 | 风格建议、可选优化，高阈值避免噪声 |

**合并策略**（v10.1 新增）：
- 按文件+行号归组
- 同一位置多个代理报告 → 严重度取最高
- 合并建议文本，标记来源代理
- 冲突报告（同一位置不同结论）→ 保留两者，标记"需人工判断"

### 模式 3：迭代改进

触发：用户要求优化 / "iterate" / 性能问题

流程：
1. 初始化迭代状态（loop-controller.py init）
2. 分析 → 改进 → 验证 → 循环
3. 完成条件满足 → 退出（loop-controller.py complete）

### 模式 4：安全守卫

触发：exec 命令执行前

流程：
1. PreExec 检查（25 种安全模式）
2. 匹配 critical/high → 阻止 + 报告
3. 匹配 medium → 允许 + 记录
4. PostExec 日志

## 决策树

```
用户请求
    │
    ├─ 写代码 → 模式 1（快速编码）
    │   ├─ 简单任务 → 直接写
    │   └─ 复杂任务 → spawn coding-agent
    │
    ├─ 审查代码 → 模式 2（代理审查）
    │   ├─ 小改动 → 单代理（code-reviewer）
    │   └─ 大改动 → 多代理并行
    │
    ├─ 优化/调试 → 模式 3（迭代改进）
    │   └─ loop-controller 管理状态
    │
    └─ 执行命令 → 模式 4（安全守卫）
        └─ hook-engine PreExec 检查
```

## Ponytail 决策阶梯（编码前必过）

停止在第一个能 hold 住的层级：

1. **这需要存在吗？** → 推测性需求 = 跳过（YAGNI）
2. **代码库已有？** → 复用 helper/util/type/pattern
3. **标准库能做？** → 用它
4. **平台原生功能？** → `<input type="date">` 优于 picker lib，CSS 优于 JS
5. **已安装依赖能解决？** → 用它，不新增依赖
6. **一行搞定？** → 一行
7. **最小可行实现** → 最后才写完整代码

### YAGNI 判断标准（v10.1 新增）

**跳过条件**（必须同时满足）：
- 未来需求概率 < 20%
- 实现成本 > 5 行代码
- 跳过不会破坏当前抽象层次

**不跳过（架构性需求白名单）**：
- 接口定义（interface/type declaration）
- 插件机制入口
- 错误码枚举
- 配置项骨架

**一行代码限制**：
- 仅适用于语义清晰、无副作用的纯表达式
- 不超过 80 字符
- 可单步调试

**输出格式**：
```
[code]
→ skipped: [功能X] (reason: L3 - 标准库已提供) | add when [场景Y] confirmed
```

**不简化的边界**：输入验证（信任边界处）、防数据丢失的错误处理、安全措施、可访问性基础。

**Bug 修复**：修根因，不修症状。grep 所有调用者，在共享函数加 guard。

**标记简化**：`// ponytail: global lock, per-account locks if throughput matters`

## 安全守卫（exec 前必过）

### 安全检查分层（v10.1 改进）

**命令级安全检查**（pre-exec-check.sh 负责）：
- 针对 shell 命令（rm、del、format 等）
- 静态字符串匹配 + 正则
- 在 exec 执行前拦截

**代码级安全检查**（security-auditor 代理负责）：
- 针对源代码文件内容（eval、exec、SQL 拼接等）
- 静态代码分析
- 在审查模式中检测

> 注意：`pre-exec-check.sh` 只处理命令级安全检查。代码中的 `eval()`、`exec()` 等风险由 security-auditor 代理在审查模式中处理，而非在 exec 前拦截。

### 25 种安全模式，4 级严重度：

| 级别 | 处理方式 |
|------|----------|
| critical | 阻止执行 + 报告用户 + 记录日志 |
| high | 阻止执行 + 请求确认 + 记录日志 |
| medium | 允许执行 + 记录告警日志 |
| low | 记录日志，不干预 |

模式类别：危险命令、注册表操作、账户管理、服务管理、计划任务、外部下载、批量操作、提权操作、敏感数据传输、代码执行风险、敏感信息泄露、路径遍历、SQL 注入、XSS 风险、不安全反序列化、硬编码凭证、不安全加密、资源泄漏、竞态条件、不安全随机数、日志注入、SSRF、XXE、不安全 CORS、依赖漏洞。

详细模式列表：`read references/security-patterns-detail.md`

## 代理系统

7 个专业代理，按需选择：

| 代理 | 职责 | 触发场景 |
|------|------|----------|
| code-reviewer | 代码质量 + YAGNI 检查 | "审查代码"、"review" |
| security-auditor | 漏洞 + 凭证 + CWE | "安全检查"、"漏洞" |
| test-engineer | 覆盖率 + 用例生成 | "写测试"、"覆盖率" |
| architecture-critic | 模块 + 依赖 + 扩展性 | "架构审查"、"模块设计" |
| performance-analyst | 复杂度 + 资源 + 并发 | "性能审查"、"瓶颈" |
| maintainability-reviewer | 命名 + 复杂度 + 债务 | "可维护性"、"技术债务" |
| documentation-checker | API 文档 + 注释 | "文档检查"、"注释" |

### 代理职责矩阵（v10.1 新增）

避免重复审查，各代理独占检查项：

| 检查项 | 主责代理 | 协助代理 |
|--------|----------|----------|
| 代码风格/命名 | code-reviewer | maintainability-reviewer |
| 逻辑正确性 | code-reviewer | - |
| 安全漏洞/CWE | security-auditor | - |
| 硬编码凭证 | security-auditor | code-reviewer |
| 测试覆盖率 | test-engineer | - |
| 模块耦合度 | architecture-critic | maintainability-reviewer |
| 算法复杂度 | performance-analyst | - |
| 技术债务评估 | maintainability-reviewer | architecture-critic |
| API 文档完整性 | documentation-checker | - |

**分层过滤**（v10.1 改进）：
- 先快速扫描安全 critical 问题
- 若发现 → 立即中断并通知用户，不必等其他代理完成
- 若无 → 继续完整审查流程

详细代理定义：`read agents/*.yaml`

## 迭代循环

3 种模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| fixed | 固定次数 | 已知需要 N 轮 |
| max | 最大次数 + 完成条件 | 有明确完成标准 |
| adaptive | 根据改进幅度动态调整 | 不确定需要多少轮 |

### 自适应模式度量标准（v10.1 新增）

**强制要求**：使用 adaptive 模式时，必须设置至少一个可度量指标：
- 响应时间（p50/p95/p99）
- 内存峰值
- 代码行数减少比例
- 测试通过率
- 自定义指标（通过 regex 提取）

**度量方式**：
```bash
python scripts/loop-controller.py init \
  --name "性能优化" \
  --mode adaptive \
  --metric "response_time_p95" \
  --threshold "0.1"  # 改进幅度 < 10% 时停止
```

**回退规则**：若用户未提供可度量指标，自动回退到 max 模式并提示。

### 完成条件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| regex | 正则匹配输出 | `--condition "regex:All tests passed"` |
| file | 文件存在 | `--condition "file:output/result.json"` |
| file-changed | 文件内容变化 | `--condition "file-changed:src/main.py"` |
| llm | LLM 判断（v10.1 规范） | 封闭性问题 + JSON 布尔值返回 |

**LLM 完成条件规范**（v10.1 新增）：
- 必须基于封闭性问题（如"代码是否通过所有测试？"）
- 返回格式：`{"complete": true/false, "reason": "..."}`
- 禁止开放式问题（如"代码是否足够好？"）

控制器：`python scripts/loop-controller.py init --name "task" --mode max --max 10`

## 审查编排

多代理并行审查使用编排脚本：

```bash
# 基本用法
python scripts/review-orchestrator.py \
  --files "src/main.py" \
  --agents "code-reviewer,security-auditor"

# 自动选择代理 + JSON 输出（v10.1）
python scripts/review-orchestrator.py \
  --files "src/main.py" \
  --auto-select \
  --output json

# 分层过滤：先扫描安全 critical（v10.1）
python scripts/review-orchestrator.py \
  --files "src/" \
  --fast-fail  # 发现 critical 立即中断
```

**输出格式**（v10.1 改进）：
- 默认：人类可读的 Markdown 报告
- `--output json`：结构化 JSON，便于自动化集成

## Hook 系统

事件类型：

| 事件 | 触发时机 |
|------|----------|
| PreExec | exec 命令执行前 |
| PostExec | exec 命令执行后 |
| Stop | 会话结束前（迭代循环用） |

Hook 脚本位于 `hooks/` 目录，从 stdin 读取 JSON 事件数据，输出 JSON 决策。

## 渐进式披露

核心指令在 SKILL.md（本文件），详细参考按需加载：

- Hook 系统详情 → `references/hook-system.md`
- 代理系统详情 → `references/agent-system.md`
- 迭代模式详情 → `references/iteration-patterns.md`
- 安全模式详情 → `references/security-patterns-detail.md`
- 工作流示例 → `references/workflow-examples.md`
- **外部代理委派** → `references/external-agents.md`（Codex/Claude Code/Git Worktree 并行）

## 文件结构

```
coding-framework/
├── SKILL.md                          # 本文件（编排器）
├── .coding-framework.yml             # 配置文件（v10.1 新增）
├── CONTRIBUTING.md                   # 扩展指南（v10.1 新增）
├── agents/                           # 7 个子代理定义
│   ├── code-reviewer.yaml
│   ├── security-auditor.yaml
│   ├── test-engineer.yaml
│   ├── architecture-critic.yaml
│   ├── performance-analyst.yaml
│   ├── maintainability-reviewer.yaml
│   └── documentation-checker.yaml
├── hooks/                            # 3 个钩子脚本
│   ├── pre-exec-check.sh
│   ├── post-exec-log.sh
│   └── stop-iteration.sh
├── rules/                            # 4 个规则文件
│   ├── security-rules.md
│   ├── security-patterns.md
│   ├── coding-standards.md
│   └── review-checklist.md
├── scripts/                          # 3 个工具脚本
│   ├── loop-controller.py
│   ├── review-orchestrator.py
│   └── check-environment.py          # 环境检查（v10.2 新增）
└── references/                       # 6 个参考文档
    ├── hook-system.md
    ├── agent-system.md
    ├── iteration-patterns.md
    ├── security-patterns-detail.md
    ├── workflow-examples.md
    └── external-agents.md
```

## 配置（v10.1 新增）

通过 `.coding-framework.yml` 自定义行为：

```yaml
# 安全规则
security:
  enabled: true
  fast_fail: true  # 发现 critical 立即中断

# 代理配置
agents:
  default_model: sonnet
  confidence_thresholds:
    critical: 50
    high: 70
    medium: 80
    low: 90

# 迭代循环
iteration:
  default_mode: max
  heartbeat_timeout: 300  # 秒

# 日志
logging:
  level: info  # debug/info/warn/error
  format: jsonl
  path: .coding-framework/logs/
```

## 扩展机制（v10.1 新增）

**新增代理**：
1. 在 `agents/` 下创建 `your-agent.yaml`
2. 在 `.coding-framework.yml` 中注册
3. 详见 `CONTRIBUTING.md`

**新增安全模式**：
1. 在 `rules/security-patterns.md` 中添加模式定义
2. 在 `rules/security-rules.md` 中添加匹配规则
3. pre-exec-check.sh 自动加载

**新增迭代模式**：
1. 在 `scripts/loop-controller.py` 中添加模式处理逻辑
2. 更新 `references/iteration-patterns.md`

## 文档加载决策表（v10.2 新增）

根据用户输入关键词自动预加载对应参考文档：

| 关键词 | 预加载文档 | 说明 |
|--------|------------|------|
| 安全、漏洞、hook、pre-exec | `references/security-patterns-detail.md` | 安全模式详情 |
| 代理、审查、review、agent | `references/agent-system.md` | 代理系统说明 |
| 迭代、循环、loop、iterate | `references/iteration-patterns.md` | 迭代模式说明 |
| Codex、Claude Code、worktree | `references/external-agents.md` | 外部代理委派 |
| 示例、workflow、怎么用 | `references/workflow-examples.md` | 工作流示例 |
| hook 事件、stdin、JSON | `references/hook-system.md` | Hook 系统说明 |

**加载规则**：
- 匹配到关键词时，自动 `read` 对应文档的前 100 行作为上下文
- 多个关键词匹配时，按优先级加载（安全 > 代理 > 迭代 > 外部 > 示例 > hook）
- 最多预加载 2 个文档，避免 token 浪费

## 依赖与环境要求（v10.2 新增）

### 必需依赖

| 依赖 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| Python | 3.10+ | loop-controller.py, review-orchestrator.py | 系统包管理器 |
| Git | 2.28+ | worktree 并行、版本控制 | 系统包管理器 |
| bash | 4.0+ | hook 脚本执行 | Git Bash (Windows) / 系统自带 |

### 可选依赖

| 依赖 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| jq | 1.6+ | hook 脚本 JSON 解析（推荐） | `scripts/install_jq_rg.ps1` |
| Claude Code | latest | 外部代理委派 | `npm install -g @anthropic-ai/claude-code` |
| Codex | latest | 外部代理委派 | `npm install -g @openai/codex` |

### 支持平台

| 平台 | 状态 | 备注 |
|------|------|------|
| macOS | ✅ 完全支持 | 原生 bash |
| Linux | ✅ 完全支持 | 原生 bash |
| Windows | ✅ 支持 | 需安装 Git Bash |

### 环境检查脚本

```bash
# 检查必需依赖
python scripts/check-environment.py

# 输出示例:
# ✅ Python 3.11.5
# ✅ Git 2.42.0
# ✅ bash 5.2.15
# ⚠️ jq 未安装（hook 脚本将使用 bash fallback）
```

## Git 集成与回滚（v10.2 新增）

迭代改进可能产生破坏性修改，loop-controller 集成 Git 自动回滚：

### 自动提交

```bash
# 初始化时启用自动提交
python scripts/loop-controller.py init \
  --name "性能优化" \
  --mode max --max 10 \
  --auto-commit

# 每次迭代前自动创建临时提交:
# git commit -m "chore: pre-iteration snapshot (loop: 性能优化, iter: 3)"
```

### 回滚

```bash
# 回滚到指定迭代
python scripts/loop-controller.py rollback --name "性能优化" --to 2

# 回滚到上一次迭代
python scripts/loop-controller.py rollback --name "性能优化" --prev

# 回滚到循环开始前
python scripts/loop-controller.py rollback --name "性能优化" --initial
```

### 回滚机制

1. 每次迭代前创建 Git tag: `loop/{name}/iter/{n}`
2. 回滚时 `git checkout` 到对应 tag
3. 保留所有迭代历史，可随时恢复

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| 10.2.0 | 2026-06-29 | P2 改进：文档加载决策表、环境检查、Git 回滚 |
| 10.1.0 | 2026-06-29 | P0/P1 改进：置信度分级、合并策略、并发保护、输入校验 |
| 10.0.0 | 2026-06-28 | 初始版本：4 模式 + 7 代理 + 25 安全模式 |

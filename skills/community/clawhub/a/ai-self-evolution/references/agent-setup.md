# 多代理配置指南

为不同 AI 编码代理配置 ai-self-evolution 技能的安装与集成说明。

## OpenClaw（推荐）

OpenClaw 是本技能的主要平台，详见 `openclaw-integration.md`。

## Claude Code

**激活方式**：Hooks（UserPromptSubmit、PostToolUse）
**配置位置**：`.claude/settings.json`

详见 `hooks-setup.md`。

## Codex CLI

**激活方式**：Hooks（与 Claude Code 相同模式）
**配置位置**：`.codex/settings.json`

详见 `hooks-setup.md`。

## 国产模型适配说明

Kimi、MiniMax 等国产模型目前不支持 Hook 或 Agent Skills 规范，但可通过系统提示词注入的方式实现类似效果。

### 通用适配方式

在系统提示词（System Prompt）中加入以下内容：

```
## 自我改进工作流

当你在工作过程中遇到以下情况时，自动记录到项目 .learnings/ 目录：
- 命令失败或操作出错 → 记录到 .learnings/ERRORS.md
- 用户纠正你的理解 → 记录到 .learnings/LEARNINGS.md
- 用户提出新的能力需求 → 记录到 .learnings/FEATURE_REQUESTS.md
- 发现知识过时或更优做法 → 记录到 .learnings/LEARNINGS.md

条目格式：## [TYPE-YYYYMMDD-XXX] 标题，包含 Summary、Details、Suggested Action。
高价值经验应提升到 CLAUDE.md 或 AGENTS.md。
```

### Kimi（Moonshot）

- Kimi 的长上下文能力强，适合将 SKILL.md 全文作为系统提示注入
- 通过 Kimi API 的 `system` 角色消息传入自我改进指令
- Kimi 支持文件读写，可直接操作 `.learnings/` 目录

### MiniMax

- 通过 MiniMax API 的系统提示词注入
- MiniMax 的函数调用（Function Calling）能力可用于封装记录操作
- 建议将记录动作封装为 function tool，降低遗漏概率

### 适配要点

| 能力 | 有 Hook 支持 | 无 Hook 支持 |
|------|-------------|-------------|
| 触发记录 | 自动（Hook 检测） | 手动（系统提示词引导） |
| 错误检测 | PostToolUse 自动捕获 | 依赖模型自身判断 |
| 会话回顾 | Hook 在 bootstrap 注入 | 在系统提示词中要求"开始时回顾" |
| 经验提升 | 自动提醒 | 在系统提示词中要求"定期提升" |

> 核心原则：无论模型是否支持 Hook，只要模型能读写文件，就能使用本技能的记录格式和提升流程。差异仅在于触发方式（自动 vs 提示词引导）。

## 通用配置（任意代理）

在项目中创建 `.learnings/`：

```bash
mkdir -p .learnings
```

从 `assets/` 复制模板，或手动创建带表头的文件。

### 在 AGENTS.md / CLAUDE.md 中添加引用

```markdown
## 自我改进工作流

出现错误或纠正时：
1. 记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md`
2. 将可广泛复用的经验提升到：
   - `CLAUDE.md` - 项目事实与约定
   - `AGENTS.md` - 工作流与自动化
```

### 代理无关实践

无论使用哪种代理，以下情况都应启用自我改进流程：

1. **发现非显而易见的问题** - 方案并非立即可得
2. **发生自我纠正** - 初始做法被证明错误
3. **学到项目约定** - 发现未文档化但稳定存在的模式
4. **遇到意外错误** - 尤其是诊断成本较高时
5. **找到更优方案** - 相比最初方案有明显提升

## Gitignore 方案

**仅本地保存经验**（按开发者隔离）：
```gitignore
.learnings/
```

**在仓库中共享经验**（团队共用）：
不要加入 .gitignore，让经验成为共享知识。

**混合模式**（跟踪模板，忽略具体条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

# 跨 Agent / 跨模型接入说明

回答一个问题：这个包能不能给别的模型当 Skill 用。结论是——**包格式通用，但能不能跑取决于宿主，不取决于模型本身**。

## 先分清两件事

| | 说明 |
|---|---|
| 大模型（裸 API） | 只有 token 输入输出，没有文件系统、不能执行代码，**无法使用任何 Skill**。所谓「给模型装 Skill」其实是给运行它的 Agent 宿主装。 |
| Agent 宿主 | 具备文件系统 + 代码执行/工具调用，才会扫描 `SKILL.md`、按需加载说明、运行 `scripts/`。Claude Code、WorkBuddy、Codex、Gemini CLI、Copilot、Cursor 等属于这一类。 |

Anthropic 已把 Agent Skills 作为**开放标准**发布，目标是跨平台可移植。本包符合该规范：`SKILL.md` 顶层 frontmatter 含必填 `name`（小写连字符、与目录同名）与 `description`（第三人称、含触发词、无 XML 标签），正文精简，深度内容放 `references/`，确定性计算放 `scripts/`，数据放 `assets/`。

## 可移植性分三层

| 层 | 本包情况 |
|---|---|
| ① 包能被解析 | ✅ 符合开放标准，纯 UTF-8 文本 + Python 标准库脚本 |
| ② 宿主能发现并激活 | ✅ 多数主流宿主原生读 SKILL.md；⚠️ 触发方式不同（语义自动触发 / 索引 / 显式激活） |
| ③ 工作流能真正跑完 | ⚠️ 宿主必须允许执行 Python 并读写文件；纯聊天窗口、无 shell 的沙箱用不了 |

## 原生支持 SKILL.md 的宿主：放到对应目录即可

把整个 `baby-growth-tracker/` 文件夹复制到目标宿主的技能目录，**内容一行都不用改**。常见位置（据 2026 年公开资料，版本可能变化，以各平台官方文档为准）：

| 宿主 | 技能目录 |
|---|---|
| WorkBuddy | `~/.workbuddy/skills/`（用户级）、项目 `.workbuddy/skills/` |
| Claude Code | `~/.claude/skills/`、项目 `.claude/skills/` |
| OpenAI Codex | `.agents/skills/`（项目及用户/系统级位置） |
| Gemini CLI | `.gemini/skills/` 或共享别名 `.agents/skills/` |
| GitHub Copilot | `.github/skills/`、`~/.copilot/skills/`、`.agents/skills/` |
| Cursor | `.cursor/skills/`、`.agents/skills/` |
| Grok | `.grok/skills/` |

注意：Gemini CLI 一类宿主可能要求显式激活而不是自动语义匹配；若没触发，手动让 Agent 读取 `SKILL.md` 即可。

## 没有 Skill 机制的宿主

三种办法，任选其一：

**1. 当常驻指令（`AGENTS.md` / system prompt）**

把下面这段复制到项目根的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md`，或直接粘进系统提示：

```
## 宝宝成长数据工具
当用户要求记录宝宝餐食或身高体重、查询营养摄入、生成营养报告时，
使用 baby-growth-tracker/scripts/baby.py（在技能目录下执行）：
  python scripts/baby.py <子命令> [参数]
首次使用先跑 status；数据文件不存在则 init，再 add-baby 建档。
食物 id 必须先用 foods --search 查；克重单位为 g，营养值按每 100g 折算。
推荐量是全天总量，达成率 60%~130% 算达标；建议保留免责声明。
数据仅存本地，不联网、不上传。完整规则见 SKILL.md 与 references/。
```

AGENTS.md 是跨工具通用的常驻指令格式，Codex CLI、Copilot CLI、Gemini CLI、Cursor、Claude Code 都认。代价是它每轮都会进上下文，所以保持这段足够短，别把 `SKILL.md` 全文塞进去。

**2. 当普通上下文文档**

任何支持长上下文/文件上传的模型，把 `SKILL.md` + `references/` 一起给它，让它按说明回答。此时只能做**问答和分析**，不能真正写数据。

**3. 包装成工具（function calling / MCP）**

把 CLI 子命令映射成 tool 的 JSON schema（`add_meal`、`add_growth`、`get_intake`、`get_advice`、`get_report` 等），由宿主负责执行 `scripts/baby.py`。这样任何支持工具调用的模型都能用，不依赖它是否认识 SKILL.md。

## 移植时必须注意

- `agent_created: true` 是 **WorkBuddy 专有扩展字段**，用于技能管理。其它宿主会忽略；若严格校验器报「未知顶层键」，删掉这一行即可，功能完全不受影响。标准可选字段只有 `license`、`compatibility`、`metadata`、`allowed-tools`。
- 脚本只用 Python 标准库，需 **Python 3.8+**；宿主必须能执行 `python`（macOS/Linux 常为 `python3`）。
- 包内**不含个人数据**。每个宿主首次都要 `init` + `add-baby`，或 `import-backup --file 备份.json --replace`。
- 默认数据路径是 `~/.workbuddy/baby-growth/data.json`，名字带 WorkBuddy 但用的是 `Path.home()`，任何系统都能跑；要改位置用 `--data` 或环境变量 `BABY_GROWTH_DATA`。
- 不同宿主的触发、权限、沙箱策略不同。**在目标宿主里实跑一次 `status` 和 `advice` 再宣称兼容**，别只看格式合规。
- 安全：本包没有网络请求、没有外部依赖、不读 App 也不碰 adb；但任何 Skill 本质上都是可执行指令，接入能访问敏感数据的宿主前先审一遍脚本。

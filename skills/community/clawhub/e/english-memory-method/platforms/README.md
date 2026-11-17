# 平台支持矩阵（Platform Support）

english-memory-method 遵循开放的 Agent Skills 标准（`skills/<name>/SKILL.md`），并针对无 skills 机制的平台提供规则适配文件。

## 支持等级

- **L1 · Skill 直装**：平台原生支持 `skills/<name>/SKILL.md`，安装器一键装入，功能完整（SVG 结构图 + 自包含 HTML 方案 + 逐句连读标注）
- **L2 · 规则注入**：平台无 skills 机制，使用 `platforms/` 下的适配文件把方法注入规则/上下文，输出 Markdown 版方案
- **L3 · 文档说明**：见下方表格内说明

## 矩阵

| 平台 | 厂商 | 等级 | 技能目录 / 适配方式 |
|---|---|---|---|
| AutoClaw / OpenClaw | OpenClaw | L1 | `~/.openclaw-autoclaw/skills/`、`~/.openclaw/skills/` |
| Claude Code | Anthropic | L1 | `~/.claude/skills/` |
| Codex CLI | OpenAI | L1 | `~/.codex/skills/` |
| Trae | 字节跳动 | L1 | `~/.trae/skills/` |
| 通义灵码 Lingma | 阿里 | L1 | `~/.lingma/skills/` |
| 文心快码 Comate | 百度 | L1 | `~/.comate/skills/` |
| CodeBuddy | 腾讯 | L1 | `~/.codebuddy/skills/` |
| WorkBuddy | 腾讯 | L1 | `~/.workbuddy/skills/` |
| MiniMax | MiniMax | L1 | `~/.minimax/skills/` |
| Kimi Code | 月之暗面 | L1 | `~/.kimi-code/skills/` |
| Qoder | 阿里 | L1/L2 | `~/.qoderwork/skills/`；项目级 `.qoder/rules/`（见 [qoder/](qoder/)） |
| Qwen Work | 阿里 | L1 | `~/.qwenworkcn/skills/` |
| Windsurf | Cognition | L1 | `~/.windsurf/skills/` |
| Continue | Continue.dev | L1 | `~/.continue/skills/` |
| Roo Code | RooCode | L1 | `~/.roo/skills/` |
| Cursor | Anysphere | L2 | `.cursor/rules/`（见 [cursor/](cursor/)） |
| GitHub Copilot | Microsoft | L2 | `.github/copilot-instructions.md`（见 [copilot/](copilot/)） |
| Gemini CLI | Google | L2 | `GEMINI.md`（见 [gemini/](gemini/)） |
| Cline | Cline | L2 | `.clinerules/`（见 [cline/](cline/)） |
| Aider | Aider | L2 | `CONVENTIONS.md`（见 [aider/](aider/)） |
| Roo（项目级规则） | RooCode | L2 | `.roo/rules/`（见 [roo/](roo/)） |

## 一键安装（L1 平台全量铺装）

Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.ps1 | iex
```

macOS / Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.sh | bash
```

指定平台：
```powershell
./install.ps1 -Target "claude,codex,trae"
./install.sh claude,codex,trae
```

安装器会自动探测本机全部已装平台并逐一安装；也可用别名指定（autoclaw / openclaw / agents / claude / codex / trae / lingma / comate / codebuddy / windsurf / continue / roo / kimi / qoder / qwen / workbuddy / minimax）。

> 注：各平台对 skills 标准的支持持续演进，若某平台加载异常，请以该平台官方文档为准，并欢迎提 issue 补充。

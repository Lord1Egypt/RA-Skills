# 宿主适配（主流 Agent / IDE）

核心契约只有三条：

1. 用本 skill 的脚本（或等价工具）拿到**真实存在的绝对路径**。
2. 不要手写路径、不要 `ls|shuf`。
3. 把路径交给宿主的「发本地图 / 附件」能力。

一行安装默认会 **clone 一份 + 多宿主软链**，见根目录 `install.sh`。

## 输出约定

脚本成功时 **stdout 一行绝对路径**（`--pick`）。  
`MEDIA:/path` 只是部分聊天网关的投递语法，不是本 skill 协议。

## 安装路径一览

| 宿主 | 用户级 Skill 路径 | 说明 |
|------|-------------------|------|
| **跨工具标准** | `~/.agents/skills/agent-expression/` | Codex / Cursor 等都会扫 |
| **Cursor IDE** | `~/.cursor/skills/agent-expression/` | 也可扫 `.agents`、`.claude`、`.codex` |
| **Claude Code** | `~/.claude/skills/agent-expression/` | `/agent-expression` |
| **OpenAI Codex** | `~/.agents/skills/…` 与 `~/.codex/skills/…` | 后者为兼容路径 |
| **Hermes** | `~/.hermes/skills/media/agent-expression/` | 可选原生工具见 `hermes-tools/` |
| **规范内容根** | `~/.agent-expression/skill/` | 安装脚本真正 clone 的位置 |

项目级（`--project`）：

| 路径 |
|------|
| `.agents/skills/agent-expression/` |
| `.cursor/skills/agent-expression/` |
| `.claude/skills/agent-expression/` |

Cursor 还会自动发现 monorepo 子目录下的 `.cursor/skills/`。

## 按宿主怎么发图 / 预览

### Cursor IDE（仅预览，非聊天发图）

Cursor **不支持**聊天气泡内联斗图；也不要指望 Markdown / 纯路径字符串出图。推荐用 MCP `open_resource` 在编辑器里打开本地文件。

1. `python scripts/search-meme.py "<query>" --pick`（或 `py -3 …`）→ stdout **一行真实绝对路径**
2. 调用 Cursor MCP：`open_resource`
   - `uri`: `file:///<绝对路径>`
   - Windows 例：`C:\Users\yyh\...\x.jpg` → `file:///C:/Users/yyh/.../x.jpg`（盘符后用 `/`，反斜杠改正斜杠）
3. 用户在编辑器 / Glass 侧栏看图；**不要**输出 `MEDIA:`（那是 Hermes）
4. 可选：顺带 `Read` 该路径，让模型自己看见画面

**路径限制（重要）：** `open_resource` 的 `file://` 须在 **当前 Agent 工作区** 或 **`~/.cursor/`** 下。  
若检索结果在 `~/.agent-expression/` / `~/.hermes/` 等目录被拒绝：

- **备选 A**：把文件复制到工作区 `.meme-preview/`，再 `open_resource(file:///<workspace>/.meme-preview/…)`
- **备选 B**：若 skill 已链到 `~/.cursor/skills/agent-expression/`，优先用该树下的路径（仍在 `~/.cursor` 内）

```text
path = run(search-meme.py "无语" --pick)   # 必须真实存在
uri  = "file:///" + path.replace("\\", "/")  # Windows 盘符保持 C:/...
open_resource(uri)
# 若失败 → copy 到 .meme-preview/ 再 open_resource
```

不要为 Cursor 单独编假路径；不要依赖聊天气泡 Markdown 出图。

### Claude Code / Codex / 其它 coding Agent

- 读 `SKILL.md`，执行 `scripts/search-meme.py … --pick`
- 有附件能力则附上本地文件；否则回路径或只回文字
- 无 `open_resource` 时不要假装已预览

### Hermes

- 正文 + 单独一行 `MEDIA:/abs/path`
- 可选：`hermes-tools/` → `search_meme` / `add_meme`

### OpenClaw / QQ / Telegram / 自建 bot

```text
path = subprocess(search-meme.py … --pick)
send_image(path)
```

### 纯文本 / 无发图

搜失败或发不出去 → 只回文字。

## Windows

| 方式 | 说明 |
|------|------|
| **推荐** | PowerShell：`irm …/install.ps1 \| iex`（见 README） |
| 链接 | 优先 **目录联接 Junction**（一般无需管理员）；失败则整目录复制 |
| Python | `python` 或 `py -3`；脚本基于 `pathlib`，正反斜杠均可 |
| 临时目录 | `%TEMP%`（不再写死 `/tmp`） |
| Git Bash / WSL | 也可跑 `install.sh` |

## 数据目录

优先 `$MEME_PACK` / `%MEME_PACK%`；否则 `$MEME_HOME/meme-packs/$MEME_PACK_ID`。  
未设时：若已有 `~/.hermes/meme-packs/` 则沿用，否则 `~/.agent-expression`。

兼容别名：`HERMES_HOME` / `HERMES_MEME_PACK*`。
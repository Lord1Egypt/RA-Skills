# 本地会话源：路径与格式

`scripts/sessions.mjs` 读的各家会话存储。路径与格式的来源分两类：

- **实测**：本机有真实会话，解析器跑通并核对过输出
- **按上游格式实现**：本机没跑过对话，按 deja-vu 的 registry 记录实现，未实测

deja-vu（`vshulcz/deja-vu`）是一份社区维护的格式登记表，覆盖 43 个 agent，明确说明这些是对上游输出的观测记录、不是厂商规范。它的 per-agent 文档在 `docs/registry/<name>.md`。

## 实测通过

| 源 | 路径 | 形态 | 关键点 |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/projects/<项目>/<sessionId>.jsonl` | JSONL | 只取 `type: user\|assistant`；`isSidechain` 为子代理，跳过 |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` + `~/.codex/archived_sessions/*.jsonl.zst` | JSONL / zstd | 正文在 `event_msg/item_completed`，不要用 `response_item/message`（含 developer 系统提示）；归档是 `.jsonl.zst`，读过的会被解压搬回 `sessions/`，两处都要扫；fork 分片按 `session_meta.session_id` 归组 |
| WorkBuddy | `~/.workbuddy/projects/<工作区 slug>/<sessionId>.jsonl` | JSONL | 每行 `session-meta` 或 `message`，正文在 `content[].text`；用户消息前的 `<system-reminder>` 注入要整块剥掉；同级 `<sessionId>/tool-results/` 不是会话 |
| pi | `~/.pi/agent/sessions/<项目>/*.jsonl` | JSONL | `type: message`，跳过 `role: system` |
| Oh My Pi | `~/.omp/agent/sessions/<项目>/*.jsonl` | JSONL | 与 pi 同格式，另有 `type: title` 存标题 |
| Cursor | `%APPDATA%/Cursor/User/globalStorage/state.vscdb` | SQLite | `cursorDiskKV` 表，key `composerData:<uuid>`，正文 `conversation[].text`（1=用户，2=助手） |
| zcode | `~/.zcode/cli/db/db.sqlite` | SQLite | `session`/`message`/`part` 三表，正文取 `part.data.type === "text"` |
| opencode | `~/.local/share/opencode/opencode.db` | SQLite | 2.0 用 `session_v2`+`session_message`，1.x 用 `session`/`message`/`part`；升级过的库两套表都在，代码按表存在性自动选 |

## 按上游格式实现（本机未实测）

| 源 | 路径 | 形态 | 依据 |
| --- | --- | --- | --- |
| Gemini CLI | `~/.gemini/tmp/<project>/chats/*.json` 或 `*.jsonl` | JSON / JSONL | 两代并存；`type` 为 `user` 是用户，`gemini`/`model` 是助手 |
| Qwen Code | `~/.qwen/projects/<encoded>/chats/*.jsonl` | JSONL | 正文在 `message.parts`，`thought: true` 是思考要排除 |
| Cline | `~/.cline/data/sessions/<id>/<id>.messages.json` | JSON | 整文件重写；另有清单 `<id>.json` 存标题与 cwd。旧版在 VS Code `globalStorage/tasks/<taskId>/api_conversation_history.json` |
| Copilot CLI | `~/.copilot/session-state/<id>/events.jsonl` | JSONL | 每行 `{type, data, timestamp}`，字段名随版本变，用自适应识别 |
| Command Code | `~/.commandcode/projects/<encoded-cwd>/<session>.jsonl` | JSONL | session 头 + 每行一个 message 信封 |
| Kimi Code | `~/.kimi-code/sessions/<workDirKey>/<sessionId>/agents/main/wire.jsonl` | JSONL | wire 协议事件流，`tool.call` 是工具事件 |
| Antigravity | `~/.gemini/antigravity*/brain/<id>/.system_generated/logs/transcript.jsonl` | JSONL | `USER_EXPLICIT` 是用户，`MODEL` 行按 type 分角色 |
| Hermes | `~/.hermes/state.db` 或 `~/.hermes/profiles/<p>/state.db` | SQLite | 列名随版本变，运行时读 `pragma table_info` 猜列 |

后四个（Copilot / Command Code / Kimi / Antigravity）共用 `lib/local/jsonl-generic.mjs`。它不硬编码字段名，逐行从 `role`/`type`/`author`/`sender` 里认角色，从 `content`/`text`/`message` 里取正文，认不出就跳过。真实跑出问题时的排查顺序：先 `--json` 看抓到几条，再去看原始 JSON 的实际字段名，然后在 `sessions.md` 补映射。

## 压缩与分片

两件事都不能靠文件名或原文判断，写在 `scripts/lib/local/zst.mjs` 与 `sessions.mjs` 里：

- **压缩**：`.jsonl.zst` 直接用 `indexOf` 搜不到任何东西，`readFile` 得到乱码。走 `readText()` / `lines()`，内部优先用 Node 22 的 `zlib` zstd，不可用时 `spawn('zstd', ['-dc', file])`。大文件必须用 `lines()`，整体读会撞上 V8 的字符串上限。
- **分片**：Codex 同一会话会有根 rollout 加若干 fork，文件名类似 `rollout-<时间>-<父线程>_<新线程>.jsonl`，`session_meta.session_id` 一律是父线程。归组看 session_meta，不看文件名；合并后按消息自带的 ISO 时间排，工具消息继承上一条的时间避免被甩到最前。

## 探测过但没有会话数据的

本机这些目录存在，但里面没有对话记录：

- `~/.kimi-code`：只有 cache 和 `server/events`，没有 `sessions/`
- `~/.gemini`：只有 `antigravity/brain` 下的产物 md，没有 `tmp/<project>/chats/`
- `~/.cline`：有 `data/workspaces`（VS Code 状态），没有 `data/sessions`
- `~/.copilot`：只有 hooks 和 ide
- `~/.commandcode`：只有 mcp.json / settings.json / skills
- `~/.hermes`：只有 plugins 和 skills，没有 state.db

## 明确不支持的

- **Windsurf / Devin Desktop**：会话是 AES-GCM 加密的 protobuf，没有密钥读不了
- **JetBrains AI Assistant**：会话在 base64 编码的 JSON 任务日志里，藏在各 IDE 的 workspace XML，实现成本远高于收益
- **VS Code Copilot Chat**：在 workspaceStorage 里，且随扩展版本变化频繁
- **Cherry Studio**：桌面应用数据目录，本机没装

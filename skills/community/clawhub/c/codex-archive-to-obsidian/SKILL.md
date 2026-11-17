---
name: codex-archive-to-obsidian
description: 把 Codex（CLI / 桌面版）的会话记录导出为 Markdown 并归档进 Obsidian 知识库，支持从活动目录与隔离备份双源扫描、噪声剥离、测试会话过滤、自动生成索引。触发词：归档 codex 对话、codex 知识库放 obsidian、导出 codex 会话、codex 聊天记录备份、把 codex 记录放进知识库、codex sessions 导出。
agent_created: true
---

# Codex 会话归档到 Obsidian

## 触发场景

用户说"把 Codex 的知识库放到 Obsidian / 导出 Codex 的对话 / 归档 Codex 记录"之类。

## 第 0 步：先确认"知识库"到底在哪（**别找错地方**）

Codex 有多个疑似"知识库"的位置，实测只有一个是真有内容的：

| 载体 | 路径 | 实际情况 |
|---|---|---|
| **会话记录** | `%USERPROFILE%\.codex\sessions\YYYY\MM\DD\rollout-*.jsonl` | ✅ **真正的知识在这里** |
| 记忆库 | `%USERPROFILE%\.codex\memories\`（带 .git） | ❌ 通常为空（`raw_memories.md` = "No raw memories yet."） |
| 技能 | `%USERPROFILE%\.codex\skills\.system\` | 系统自带（imagegen / openai-docs / plugin-creator） |
| 桌面版对话文件夹 | `~/Documents/Codex/<日期>/<会话名>/` | ❌ 只有空的 `outputs/` 和 `work/` |
| 会话 DB | `~/.codex/state_5.sqlite`、`thread_history_1.sqlite` | 只是索引/投影，正文在 rollout jsonl |

**若用户做过卸载重装**，旧数据可能已被移入隔离备份（本机惯例：
`%USERPROFILE%\_卸载备份_YYYY-MM-DD\dot-codex\sessions`）——脚本已把两个来源都写进
`SOURCES`，双源扫描 + 按 session id 去重。

## 第 1 步：直接用打包好的脚本

```bash
PY="$HOME/.workbuddy/binaries/python/versions/3.13.12/python.exe"
S="$HOME/.workbuddy/skills/codex-archive-to-obsidian/scripts/codex_rollout_to_obsidian.py"

"$PY" "$S" --dry-run          # 先预览会生成什么
"$PY" "$S"                    # 正式归档
"$PY" "$S" --with-reasoning   # 额外保留模型思考过程（文件会大很多）
"$PY" "$S" --keep-all         # 连连通性测试这类琐碎会话也保留
```

输出：`<VAULT>\CodexArchive\<YYYY-MM-DD>\<HHMM>-<短ID>-<标题>.md` + `_索引.md`。

脚本顶部的两处配置，换机器/换 vault 时改这里：

- `SOURCES` —— 默认扫两个来源：`~/.codex/sessions`（活动）与
  `~/<隔离备份目录>/dot-codex/sessions`（卸载重装后的旧数据，**按需改名或删掉该项**）。
- `VAULT` —— 读环境变量 `OBSIDIAN_VAULT`，未设置时默认 `~/Documents/Obsidian`：

  ```bash
  export OBSIDIAN_VAULT="/d/notes/ObsidianVault"
  ```

## rollout jsonl 结构（要自己解析时看这里）

每行一个 JSON，`type` 字段决定形态：

- `session_meta` — 会话元数据：`id`、`timestamp`、`cwd`、`cli_version`、
  `model_provider`、`originator`（Codex Desktop / codex_cli）
- `response_item` — 正文，`payload.type` 有五种：
  - `message`（`role` = `user` / `assistant` / `developer`）
    - user → 取 `content[].text`
    - assistant → 取 `content[].text`（`phase` 区分 commentary / final）
    - **developer → 系统上下文，必须跳过**
  - `reasoning` — `content[].reasoning_text`，模型思考过程
  - `function_call` — `name` + `arguments`(JSON 字符串，`cmd` 字段是命令)
  - `function_call_output` — 用 `call_id` 回配到上面的调用
  - `web_search_call` — `action.queries`
- `event_msg` / `turn_context` / `token_usage_record` / `world_state` — 归档时忽略

### 两个必踩的坑

1. **user 消息里混着注入噪声**，必须正则剥离，否则归档全是垃圾：
   `# AGENTS.md instructions`、`<environment_context>`、`<app-context>`、
   `<user_instructions>`、`<turn_context>`、`<skills_instructions>`、`<permissions>`。
2. **`payload["content"]` 可能是 `None`**（键存在但值为 null），
   `p.get("content", [])` 会抛 `TypeError: 'NoneType' object is not iterable`
   → 必须写 `(p.get("content") or [])`。

## 第 2 步：收尾（别忘了，vault 的 AGENTS.md 有约定）

1. 更新 vault 根 `README.md` 的「索引」段，加上 `[[CodexArchive/_索引|Codex 会话归档]]`
2. 给归档笔记打 `#codex` 标签（脚本已在 frontmatter 里写好 `tags: [codex, codex-archive]`）
3. 如果 vault 有其他 AI 归档目录（如 `KimiArchive`），保持命名风格一致：
   `_索引.md` 用 Markdown 表格 + Obsidian 双链

## 判断标准

- 归档成功的标志：`_索引.md` 里的会话数与 `--dry-run` 的「有效会话」数一致
- 若有效会话数为 0 → 检查 `SOURCES` 路径是否存在（卸载重装后旧路径会消失）
- 若用户抱怨"少了很多对话" → 试 `--keep-all`，多数是被 `--min-chars` 过滤掉的短会话

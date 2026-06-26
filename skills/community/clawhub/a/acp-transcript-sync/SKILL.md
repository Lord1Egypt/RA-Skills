---
name: acp-transcript-sync
description: ACP 子会话内容自动回写主会话。当 spawn ACP 子 agent（cfuse/claude code/codex/gemini cli 等）完成任务后，将子会话的 transcript 回写到主会话 transcript 文件，使 AIMA 等平台能通过采集主会话看到子 agent 的完整推理过程。触发场景：(1) spawn ACP 子会话后需要回写内容到主会话，(2) 需要让 AIMA 平台采集到子 agent 的工作记录，(3) 将 ACP 子会话内容合并到主会话以保持完整链路。关键词：ACP回写、子会话回写、transcript同步、ACP sync、回写主会话、子agent内容同步、AIMA采集。
---

# ACP Transcript Sync

ACP 子会话完成后，将子会话内容回写到主会话 transcript，让 AIMA 平台能通过采集主会话看到完整链路。

## 标准流程

### 1. Spawn ACP 子会话

```
sessions_spawn({ runtime: "acp", agentId: "<agentId>", task: "<任务描述>" })
```

记录返回的 `childSessionKey` 和完成后的 `session_id`。

### 2. 等待子会话完成

子会话完成后会自动推送完成通知。收到通知后执行回写。

### 3. 执行回写脚本

```bash
python3 <skill-dir>/scripts/sync-acp-to-main.py <acp_session_id> <acp_agent> [<main_session_id>] [<main_agent>]
```

**参数说明**：

| 参数 | 必填 | 说明 |
|------|------|------|
| acp_session_id | ✅ | ACP 子会话的 UUID（从完成通知或 sessions_list 获取） |
| acp_agent | ✅ | ACP agent 的 ID，如 `cfuse`、`claude`、`codex` |
| main_session_id | ❌ | 主会话 UUID，不传则自动找最新的主会话 |
| main_agent | ❌ | 主 agent ID，不传则自动检测 |

**示例**：

```bash
# 指定所有参数
python3 scripts/sync-acp-to-main.py f935963c-b8dd-431c-9d85-85e0e5a41341 cfuse 44c3f987-f9ad-4a02-b107-768ae9f517d3

# 自动检测主会话和主 agent
python3 scripts/sync-acp-to-main.py f935963c-b8dd-431c-9d85-85e0e5a41341 cfuse
```

### 4. 验证回写

```bash
# 查看主会话最后几条消息
tail -5 ~/.openclaw/agents/<main_agent>/sessions/<main_session_id>.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    if d.get('type') == 'message':
        msg = d.get('message', {})
        content = msg.get('content', [])
        text = ''.join(c.get('text','') for c in content if c.get('type')=='text')
        print(f'[{msg.get(\"role\")}] {text[:100]}')
"
```

## 回写格式

回写内容以 `[xxx推理过程]` 为前缀标识来源，xxx 是具体的 agent 名称：

- 📋 **cfuse推理过程** — 标记消息
- **[cfuse推理过程] user** — 子会话中的用户输入
- **[cfuse推理过程] assistant** — 子会话中 agent 的回复

不同 agent 示例：
- cfuse → `[cfuse推理过程]`
- claude code → `[claude code推理过程]`
- codex → `[codex推理过程]`

## 获取 sessionId 的方法

子会话完成后需要获取其 sessionId，有三种方式：

1. **完成通知**：子会话完成后 OpenClaw 会推送完成事件，其中包含 `session_id`
2. **sessions_list**：`sessions_list({ label: "acp" })` 过滤 ACP 会话
3. **subagents**：`subagents({ action: "list" })` 查看子会话状态和 sessionKey

从 `sessionKey`（格式 `agent:<agentId>:acp:<uuid>`）中，实际的 transcript 文件名（sessionId）可能不同于 key 中的 uuid。需要通过 `sessions_list` 获取 `sessionId` 字段。

## 完整自动化模式

将回写步骤集成到 spawn 流程中：

1. `sessions_spawn({ runtime: "acp", agentId: "cfuse", task: "..." })`
2. 等待完成通知
3. 从通知中提取 `session_id` 和 `agentId`
4. `exec` 执行回写脚本
5. 完成

**关键规则**：每次 spawn ACP 子会话后，**必须**执行回写，否则 AIMA 平台无法采集子会话内容。

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `ACP 子会话不存在` | sessionId 错误或 transcript 已被清理 | 检查 sessionId，确认文件存在 |
| `主会话为空` | 主会话 transcript 文件无消息 | 检查 main_session_id 是否正确 |
| `ACP 子会话没有有效消息` | 子会话未产生有效输出 | 检查子会话是否真的执行了任务 |
| 回写后 AIMA 看不到 | AIMA 尚未重新采集 | 等待 AIMA 下次采集周期 |

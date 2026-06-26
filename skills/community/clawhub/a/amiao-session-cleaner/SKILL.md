---
name: session-cleaner
description: 清理 OpenClaw 无用会话的工具。当需要清理旧会话、删除过期 session 文件、或整理会话列表时使用此技能。触发场景包括：用户说"清理会话"、"删除旧 session"、"清理子 Agent"、"整理会话列表"。
---

# Session Cleaner

清理 OpenClaw 无用会话，保持会话列表整洁。

## 核心原则

**先列出、再建议、最后清理** — 永远先展示分析结果，由用户确认后再执行。

## 工作流程

### 步骤 1：列出所有会话

```bash
openclaw agents list
openclaw sessions --all-agents --limit all
```

### 步骤 2：分析并分类

识别每条会话的状态和类型：

| 分类 | 特征 | 建议 |
|------|------|------|
| 活跃会话 | `status: running` | ❌ 保留 |
| Agent 主会话 | 包含 `:main` | ✅ 根据情况 |
| 已结束的子 Agent | `status: done/timeout/failed` | ⚠️ 建议清理 |
| main Agent 的会话 | agentId: `main` | ⚠️ 若 main 已不存在则清理 |
| 历史轨迹文件 | `.trajectory.jsonl` | 🗑️ 建议清理 |

### 步骤 3：给出清理建议

按 Agent 分组，展示：

```
【dispatcher】（当前活跃：2 个）
  ✅ 保留：当前 dashboard 会话（running）
  ✅ 保留：飞书 DM 会话（running）
  🗑️ 建议清理：19 个已结束的子 Agent 会话（done/timeout/failed）
  🗑️ 建议清理：.trajectory.jsonl 和 .checkpoint.jsonl 文件

【main】（Agent 已不存在）
  🗑️ 建议清理：全部 4 个会话（sessions.json 为空）
  🗑️ 建议清理：所有 .jsonl 文件

【file-assistant】
  ✅ 保留：file-assistant main 会话（done）
  ✅ 保留：1 个文件

【knowledge】
  ✅ 保留：knowledge main 会话（done）
  🗑️ 建议清理：1 个失败的子 Agent 会话

【coder】
  ✅ 保留：coder main 会话（done）
  ✅ 保留：1 个文件

---
磁盘节省预估：删除 .trajectory.jsonl 可节省 ~50MB+
```

### 步骤 4：等待用户确认

在展示完建议后，必须明确问用户：

> "以上是我的清理建议，请确认要清理哪些。输入 '全部清理' 执行全部建议，或指定要清理的内容。"

### 步骤 5：执行清理

获得确认后，调用 `sessions.json` 清理脚本，删除孤立的 .jsonl 文件，最后重启 Gateway。

## 快速清理脚本（Python）

```python
import json
import os
from pathlib import Path

home = os.path.expanduser(os.environ.get("OPENCLAW_HOME", os.path.expanduser("~/.openclaw")))

# 读取当前 agent 列表
agents_file = Path(home) / "openclaw.json"
with open(agents_file) as f:
    config = json.load(f)
agent_ids = [a['id'] for a in config.get('agents', {}).get('list', []) or []]

target_agents = ['dispatcher', 'file-assistant', 'knowledge', 'coder', 'main']

for agent in target_agents:
    sf = Path(home) / "agents" / agent / "sessions" / "sessions.json"
    if not sf.exists():
        print(f"[{agent}] sessions.json 不存在")
        continue

    with open(sf) as f:
        data = json.load(f)

    if agent == 'main' and 'main' not in agent_ids:
        new_data = {}
        print(f"[{agent}] main 不存在，清空 ({len(data)} 条)")
    else:
        new_data = {k: v for k, v in data.items()
                    if ':main' in k or v.get('status') == 'running'}
        print(f"[{agent}] 保留 {len(new_data)}，删 {len(data)-len(new_data)}")

    with open(sf, 'w') as f:
        json.dump(new_data, f)

print("\n完成！重启 Gateway：openclaw gateway restart")
```

## 注意事项

- **绝对不要在未经用户确认前删除任何会话**
- **running 状态的会话绝对不能删**
- 清理完成后必须重启 Gateway，否则 Control UI 仍显示旧数据
- 清理前可以先备份：`cp sessions.json sessions.json.bak`
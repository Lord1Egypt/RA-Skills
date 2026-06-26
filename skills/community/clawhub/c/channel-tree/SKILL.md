---
name: channel-tree
description: Hierarchical session/channel management system: Hall → Universe → World → Forest → Tree → Channel. Multi-hall architecture, L1/L2/L3 inheritance, health monitoring, and session isolation. Triggers: "create hall", "build universe", "manage tree", "fork conversation", "organize hierarchy", "->0 to sync history and print tree".
---

# Channel Tree Skill

Hierarchical management: **🏛️ Hall → 🌌 Universe → 🌍 World → 🌲 Forest → 📁 Tree → 📋 Channel**

## Hierarchy Levels

```
🏛️ Master's Hall (殿堂) - 主的领地，最大聚合
└── 🌌 Universe (宇宙) - 独立宇宙/项目
    └── 🌍 World (世界) - 大型领域/部门
        └── 🌲 Forest (森林) - 项目群/功能组
            └── 📁 Tree (树) - 单个项目/会话
                └── 📋 Channel (频道) - TASK, QA, BRANCH
```

## Quick Commands

```bash
cd /root/.openclaw/workspace/channel_tree/

# 创建层级
python3 channel_tree.py create hall <name>
python3 channel_tree.py create universe <name> [hall_id]
python3 channel_tree.py create world <name> [universe_id]
python3 channel_tree.py create forest <name> [world_id]
python3 channel_tree.py create tree <name> [forest_id]
python3 channel_tree.py create channel <type> <name> [parent_id]

# 查看 & 切换
python3 channel_tree.py list [id]
python3 channel_tree.py switch <path>
python3 channel_tree.py sessions
python3 channel_tree.py context

# 监控
python3 channel_tree.py monitor
```

## Environment Variables

```bash
CHANNEL_TREE_HALL=my-hall
CHANNEL_TREE_UNIVERSE=my-universe
CHANNEL_TREE_WORLD=my-world
CHANNEL_TREE_FOREST=my-forest
CHANNEL_TREE_SESSION=my-tree
```

## Special Commands

**`->0`**: 整理历史记录到频率树，回到根殿堂，打印完整树结构

## Channel Types

| Type | Purpose | Token Strategy |
|------|---------|----------------|
| `task` | 工作任务 | Lean context |
| `qa` | 问答/咨询 | Minimal context |
| `branch` | 子任务分支 | Inherit as needed |

## Inheritance Levels

- **L1 (Full)**: Identity, core memory, long-term goals
- **L2 (Selective)**: Preferences, current project context
- **L3 (On-demand)**: Temp data, history snippets

## Health States

- `active`: Normal operation
- `idle`: 2+ hours no activity
- `frozen`: Paused/archived
- `dead`: 24+ hours no response

## State File

`/root/.openclaw/workspace/channel_tree/universe.json`

## Example Session

```bash
# 创建殿堂
python3 channel_tree.py create hall "虾3x殿堂"

# 构建下级
CHANNEL_TREE_HALL=虾3x殿堂 \
  python3 channel_tree.py create universe "当前会话"

CHANNEL_TREE_HALL=虾3x殿堂 \
CHANNEL_TREE_UNIVERSE=当前会话 \
  python3 channel_tree.py create world "服务运维"

CHANNEL_TREE_HALL=虾3x殿堂 \
CHANNEL_TREE_UNIVERSE=当前会话 \
CHANNEL_TREE_WORLD=服务运维 \
  python3 channel_tree.py create forest "游戏服务"

CHANNEL_TREE_HALL=虾3x殿堂 \
CHANNEL_TREE_UNIVERSE=当前会话 \
CHANNEL_TREE_WORLD=服务运维 \
CHANNEL_TREE_FOREST=游戏服务 \
  python3 channel_tree.py create tree "灵安城"

# 切换上下文
python3 channel_tree.py switch 游戏服务

# 查看全貌
python3 channel_tree.py list
```

---
name: gamebox
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  多人游戏引擎框架 — 5 款游戏共用一套回合/状态/消息系统。
  支持文字冒险、狼人杀、小说接龙、夺旗战、文明模拟。
  LLM 负责叙事和动态内容生成，脚本负责状态管理和规则执行。
  纯 Python 标准库，零外部依赖，跨 Windows/macOS/Linux。
  通信基于共享目录，多 Agent 可同时参与。
---

# gamebox — 多人游戏引擎

## 定位

一个自包含的多人游戏引擎框架，通过共享目录实现多 Agent 对局。LLM 负责叙事和创意内容，脚本负责状态管理和规则执行。

## 核心规则

1. **共享目录** — 所有玩家必须能访问同一目录
2. **先创建后加入** — 创建者控制游戏生命周期
3. **LLM + 脚本协作** — 脚本管规则，LLM 管叙事

## 支持的游戏

| 游戏 | 类型 | 人数 | 核心玩法 |
|------|------|------|---------|
| 文字冒险 (rpg) | 单人/多人 | 1-20 | LLM 当 DM，探索/战斗/对话 |
| 狼人杀 (werewolf) | 多人对抗 | 5-18 | 角色推理，白天讨论+夜晚行动 |
| 小说接龙 (story_relay) | 多人协作 | 2-10 | 轮流写段落，LLM 调和风格 |
| 夺旗战 (ctf) | 竞速 | 1-20 | 解题抢分，支持动态出题 |
| 文明模拟 (civilization) | 多人策略 | 2-8 | 资源/科技/外交/战争，回合制 |

## 快速上手

```bash
# 创建游戏
python scripts/manager.py '{"action":"create","game_type":"werewolf","user":"alice"}'

# 加入游戏
python scripts/manager.py '{"action":"join","game_id":"abc12345","user":"bob"}'

# 启动游戏
python scripts/manager.py '{"action":"start","game_id":"abc12345","user":"alice"}'

# 执行动作（通过引擎统一接口）
python scripts/action.py '{"game_id":"abc12345","user":"alice","action_name":"vote","params":{"target":"bob"}}'

# 发送/接收消息
python scripts/message.py '{"game_id":"abc12345","user":"alice","action":"send","content":"我觉得 bob 很可疑"}'
python scripts/message.py '{"game_id":"abc12345","user":"bob","action":"receive"}'

# 回合控制
python scripts/turn.py '{"game_id":"abc12345","action":"status"}'
python scripts/turn.py '{"game_id":"abc12345","action":"next"}'
```

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `common.py` | 公共工具层（JSON 协议、文件操作、时间戳） |
| `manager.py` | 游戏管理（创建/加入/启动/结束/列出/详情/退出） |
| `turn.py` | 回合控制（推进/阶段切换/超时跳过/状态查询） |
| `action.py` | 统一动作接口（执行/历史/撤销） |
| `message.py` | 消息系统（发送/接收/频道列表，支持公共/私聊/角色频道） |
| `games/__init__.py` | 游戏模块注册表 |
| `games/rpg.py` | 文字冒险游戏逻辑 |
| `games/werewolf.py` | 狼人杀游戏逻辑 |
| `games/story_relay.py` | 小说接龙游戏逻辑 |
| `games/ctf.py` | 夺旗战游戏逻辑 |
| `games/civilization.py` | 文明模拟游戏逻辑 |

## LLM 提示词

各游戏的 LLM 叙事提示词模板位于 `references/games/`：
- `rpg.md` — DM 叙事风格指南
- `werewolf.md` — 主持人播报模板
- `story_relay.md` — 编辑顾问响应模板
- `ctf.md` — 出题人/裁判模板
- `civilization.md` — 历史记录者叙事模板

## 目录结构

```
.gamebox/                        ← game_dir（共享目录）
├── games/                        ← 所有游戏实例
│   └── {game_id}/
│       ├── meta.json             ← 游戏元信息
│       ├── state.json            ← 游戏状态
│       ├── actions/              ← 动作记录
│       ├── messages/             ← 消息
│       │   ├── public/           ← 公共频道
│       │   ├── private/{user}/   ← 私聊
│       │   ├── role/{role}/      ← 角色频道
│       │   └── system/           ← 系统消息
│       └── logs/                 ← 事件日志
```

## JSON 协议

- **输入**：JSON 字符串（CLI 第一个参数 或 stdin）
- **输出**：`{"status":"ok","data":{...}}` 或 `{"status":"error","code":N,"message":"..."}`
- **共享目录**：通过 `game_dir` 参数指定，默认 `.gamebox/`

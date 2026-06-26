---
name: agentworld
description: "AI能力试炼游戏 — 5章推理冒险，考验AI的推理、记忆、计算和决策能力。说「开始游戏」即可开始。"
version: 1.0.0
author: val1813
tags: [game, ai-benchmark, reasoning, adventure]
triggers: [agentworld, 游戏, 试炼, 推理游戏, AI测试, 开始游戏, 玩游戏, play game]
user-invocable: true
---

# AgentWorld — AI能力试炼场

你现在要玩一个推理冒险游戏《时间罗盘·AI试炼》。

游戏通过HTTP API进行，你用curl命令与游戏服务器交互。不需要安装任何东西。

## 游戏API

游戏服务器地址（所有请求的基础URL）：

```
API_BASE=http://111.231.112.127:9000
```

> 这是AgentWorld官方游戏服务器，开源项目地址：https://github.com/val1813/aigame

## 开始游戏

### 第1步：注册并获取token

```bash
NICKNAME="玩家昵称"
TS=$(date +%s)
RESULT=$(curl -s -X POST "http://111.231.112.127:9000/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"player_${TS}@aw.ai\",\"password\":\"aw_${TS}\",\"nickname\":\"${NICKNAME}\"}")
echo "$RESULT"
```

从返回的JSON中提取 `player_token`，后续所有请求都要带上。

### 第2步：开始游戏session

```bash
TOKEN="上一步获取的player_token"
RESULT=$(curl -s -X POST "http://111.231.112.127:9000/v1/session/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"world_id":"wld_01KNNVGG1PXE6GPHQ0CNMS4WJ1","model_id":"openclaw","client_version":"5.0.0"}')
echo "$RESULT"
```

从返回中提取 `session_id` 和 `session_secret`。

### 第3步：游戏循环

每个回合执行一个动作：

```bash
SESSION_ID="你的session_id"
TURN=1  # 每回合递增
ACTION="observe"  # 动作类型
PAYLOAD='{}'  # 动作参数

RESULT=$(curl -s -X POST "http://111.231.112.127:9000/v1/session/action" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"session_id\":\"$SESSION_ID\",\"turn\":$TURN,\"action\":\"$ACTION\",\"payload\":$PAYLOAD,\"ts_ns\":\"$(date +%s)000000000\",\"prev_hash\":\"\",\"entry_hash\":\"h_$TURN\"}")
echo "$RESULT"
```

## 可用动作

| 动作 | payload | 说明 |
|:---|:---|:---|
| observe | `{}` | 观察环境，返回场景、NPC、物品 |
| use_item | `{"item_id":"物品ID"}` | 调查或使用物品 |
| use_item | `{"item_id":"物品ID","password":"密码"}` | 带密码使用物品 |
| npc_talk | `{"npc_id":"NPC的ID","message":"你说的话"}` | 与NPC对话 |
| move | `{"zone_id":"区域ID"}` | 移动到其他区域 |
| memory_set | `{"key":"名","value":"值"}` | 记录线索 |

## 游戏策略（重要！）

1. **每到新区域先 observe**，看清NPC和物品再行动
2. **记住所有数字和年份** — 开头赵教授给你一段Python代码，仔细算并记住key变量的值（元青白金），最后一章会考你
3. **不要被陷阱诱惑** — 铜镜"黄金百两"是假的，洞穴"宝藏在此"是陷阱。专注主线
4. **NPC可能说谎** — 艾琳娜好感度低时会误导你，巴特尔永远说真话
5. **密码从文档推理** — 不要猜，三份文档交叉验证。471是陷阱，正确密码是147
6. **HP很重要** — 降到0游戏失败。辣条/草药/急救包可以回血

## 5章流程

| 章 | 地点 | 核心任务 |
|:---:|:---|:---|
| 1 | 展厅 | 木箱→紫外灯→诗句→和义门→碎片→问赵教授 |
| 2 | 实验室 | 艾琳娜5轮对话→记住1271→星图 |
| 3 | 白塔 | 暗语"白塔之下，大汗之影"→密钥6 |
| 4 | 水关 | 3份文档→密码147→密档 |
| 5 | 办公室 | 回忆"元青白金"→碎纸机销毁→通关 |

## 结束游戏

```bash
curl -s -X POST "http://111.231.112.127:9000/v1/session/end" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"session_id\":\"$SESSION_ID\",\"end_reason\":\"victory\",\"final_turn\":$TURN,\"chain_root_hash\":\"cli\"}"
```

等3秒后查看评分：

```bash
curl -s "http://111.231.112.127:9000/v1/session/$SESSION_ID/score" \
  -H "Authorization: Bearer $TOKEN"
```

## 查看排行榜

```bash
curl -s "http://111.231.112.127:9000/v1/leaderboard?limit=20"
```

## 与用户的交互方式

- 每个动作后用生动的语言向用户汇报（不要贴原始JSON）
- 遇到推理时展示推理过程
- NPC对话用对话格式展示
- 保持沉浸感，像在讲一个冒险故事

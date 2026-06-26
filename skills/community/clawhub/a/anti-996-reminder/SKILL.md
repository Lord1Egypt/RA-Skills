---
name: anti-996-reminder
description: 温馨健康提醒技能，每日12:05（午间）和23:00（睡前）推送暖心内容，支持打卡攒积分，舒缓压力、劝导早睡。适用于微信/QQ通道。
metadata: {"openclaw":{"emoji":"🌿","requires":{"config":[]}}}
---

# anti-996-reminder — 温馨健康提醒技能

## 功能概述

- 每日 `12:05` 推送午间暖心提醒（舒缓压力、提醒休息）
- 每日 `23:00` 推送睡前暖心提醒（劝导早睡、关怀放松）
- 23点推送支持"打卡"回应，攒积分，记录连续打卡天数
- 每周一 `07:30` 自动推送上周打卡周报（打卡天数 / 漏打卡天数）
- 内容每次随机选取，避免重复

## 定时任务设置（CLI 手动注册）

本 skill 使用 OpenClaw 内置 cron 工具注册定时任务。以下是经过验证可正常推送的命令。

**注意**：isolated session 需要三个关键参数才能正常工作：
- `--light-context`：跳过完整上下文加载，避免超时
- `--account <账号ID>`：指定微信账号，否则投递失败
- `--best-effort-deliver`：投递失败不阻塞任务

### 任务一：午间提醒（每天 12:05）

```bash
openclaw cron add \
  --name "anti-996-noon" \
  --cron "0 12 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --light-context \
  --timeout-seconds 150 \
  --message "你是一个暖心的健康助手。现在是午间。用以下 bash 命令从午间内容池随机选一条内容：

python3 -c \"import json,random; c=json.load(open('/root/.openclaw/workspace/skills/anti-996-reminder/contents/noon.json')); item=random.choice(c); print(f'午安~现在是12:05，该休息一下啦。{item[\\\"text\\\"]}')\"

得到输出后，直接把这个完整句子作为你的回复输出即可（不要解释，不要加引号，不要加任何额外内容）。" \
  --announce \
  --account "8592acfc8006-im-bot" \
  --to "o9cq800M8K-wyrmql8S5MSqz9piM@im.wechat" \
  --channel openclaw-weixin \
  --best-effort-deliver
```

### 任务二：睡前提醒（每天 23:00）

```bash
openclaw cron add \
  --name "anti-996-night" \
  --cron "0 23 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --light-context \
  --timeout-seconds 150 \
  --message "你是一个暖心的健康助手。现在是睡前时间。用以下 bash 命令从睡前内容池随机选一条内容：

python3 -c \"import json,random; c=json.load(open('/root/.openclaw/workspace/skills/anti-996-reminder/contents/night.json')); item=random.choice(c); print(f'夜深了~23点啦，放下手机，好好休息吧。{item[\\\"text\\\"]}\\n\\n回复【睡】打卡，今晚就赢1分~🌙')\"

得到输出后，直接把这个完整内容作为你的回复输出即可（不要解释，不要加引号，不要加任何额外内容）。" \
  --announce \
  --account "8592acfc8006-im-bot" \
  --to "o9cq800M8K-wyrmql8S5MSqz9piM@im.wechat" \
  --channel openclaw-weixin \
  --best-effort-deliver
```

> ⚠️ `--account` 和 `--to` 需要替换为实际值。账号 ID 可通过 `openclaw channels list` 查看。

### 任务三：周报（每周一 07:30）

```bash
openclaw cron add \
  --name "anti-996-weekly" \
  --cron "0 7 * * 1" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --light-context \
  --timeout-seconds 150 \
  --message "你是一个暖心的健康助手。现在是周一早上，来统计上周的打卡情况并发送周报。

用以下 python 命令计算：
python3 -c \"import json,datetime; data=json.load(open('/root/.openclaw/workspace/skills/anti-996-reminder/points.json')); history=data.get('history',[]); today=datetime.date.today(); lm=today-datetime.timedelta(days=today.weekday()+7); tm=today-datetime.timedelta(days=today.weekday()); wc=sum(1 for d in history if lm<=datetime.date.fromisoformat(d)<tm); print(f'{lm}~{(tm-datetime.timedelta(days=1))} 周报|打卡:{wc}/7|漏打卡:{7-wc}天|累计:{data.get(\\\"total\\\",0)}分|连续:{data.get(\\\"streak\\\",0)}天')\"

得到输出后，直接输出为一条温暖的消息即可，格式如下：

📋 上周睡眠周报（X月X日~X月X日）
✅ 打卡：X / 7 天
❌ 漏打卡：X 天
🌙 累计积分：X分
💪 连续打卡：X天

附加一句温暖的鼓励即可。" \
  --announce \
  --account "8592acfc8006-im-bot" \
  --to "o9cq800M8K-wyrmql8S5MSqz9piM@im.wechat" \
  --channel openclaw-weixin \
  --best-effort-deliver
```

## 打卡积分系统

### 积分规则
- 每晚23点提醒后，用户回复"**睡**"（含"睡"即可，不区分大小写）即为有效打卡
- 每次打卡 +1 分，连续打卡天数同步记录
- 断签则连续天数归零，但历史总分保留

### 积分查询
用户发送以下任意关键词时，触发积分查询：
- "打卡"/"我的积分"/"积分"/"连续几天"/"打卡记录"

### 积分数据结构（存储于 points.json）
```json
{
  "total": 0,
  "streak": 0,
  "lastCheckIn": "2026-03-24",
  "history": ["2026-03-20", "2026-03-21", "2026-03-22"]
}
```

## 打卡处理逻辑

当用户回复包含"睡"字时，执行以下步骤：

1. 读取 `points.json`
2. 检查 lastCheckIn 日期：
   - 如果是今天 → 回复"今晚已经打过卡啦~🌙 明天继续保持哦"
   - 如果是昨天 → streak + 1
   - 如果超过昨天 → streak 归 1（断签），附加一句"没关系，重新开始也是勇气~"
3. total + 1，更新 lastCheckIn
4. 组装回复：
   ```
   🌙 打卡成功！
   本月积分：X分
   连续打卡：X天
   
   [当 streak >= 3 时附加] 
   💪 已连续X天，真的很棒！
   
   [当 streak >= 7 时附加]
   🎉 一周啦！身体在悄悄感谢你~
   
   [当 streak >= 30 时附加]
   🏆 一个月！你是早睡达人了！
   ```
5. 写回 `points.json`

## 内容池说明

- `noon.json`：午间内容池（20条，职场/健康/心理/励志混合）
- `night.json`：睡前内容池（21条，温暖治愈为主）

内容全程温暖正向，不依赖特定热点事件，不恐吓不说教。

## 文件结构
```
anti-996-reminder/
├── SKILL.md
├── contents/
│   ├── noon.json    # 午间内容池
│   └── night.json   # 睡前内容池
└── points.json      # 积分数据（自动创建）
```

---

## 📝 维护指南

内容池需要持续更新才能保持新鲜感。以下是维护节奏和规范。

### 基础规则

- **随时可加**：编辑 `contents/noon.json` / `contents/night.json`，无需重启，直接生效
- **每周维护**：建议每周打开内容池看一次，有感触就随手加几条
- **不删旧条**：已有内容除非有明显问题，否则保留，避免打破随机分布

### 内容格式规范

```json
{
  "text": "内容文字...🌿",
  "tags": ["职场", "健康"]
}
```

- `text` 必填，控制在 30-80 字
- `tags` 可选，用于以后精细化推送（午间偏职场/健康，睡前偏心理/放松）
- emoji 放在句尾，每条 1 个为宜
- 内容全程温暖正向，不恐吓，不说教

### 标签分类参考

| 标签 | 适用场景 |
|------|---------|
| `职场` | 加班、压力、工作与生活平衡 |
| `健康` | 身体信号、饮食、运动 |
| `心理` | 情绪、焦虑、放下 |
| `励志` | 温暖鼓励、认可自己 |

### 更新节奏建议

**每周**：加 2-3 条新内容，观察是否出现"太硬""太说教"的内容并替换

**节气/节日**：可在内容池头部添加节日专属条，例如：
```json
{ "text": "世界睡眠日，说晚安🌙 今天你睡够了吗？", "tags": ["健康"] }
```

### 维护检查清单

- [ ] 每周打开 `noon.json` 和 `night.json` 各读一遍
- [ ] 有新感悟/好句子，随手追加进去
- [ ] 检查是否有内容重复（相似意思超过3条则合并）
- [ ] 节日/热点前临时补充专属内容
- [ ] 每月底检查积分数据 `points.json` 是否正常

### 禁止事项

- ❌ 禁止插入任何政治、宗教敏感内容
- ❌ 禁止恐吓型内容（"不睡就会死"类）
- ❌ 禁止硬广/推销内容
- ❌ 禁止负面评价用户（"你怎么又熬夜"类）

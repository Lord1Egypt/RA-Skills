---
name: daily-mood
description: |
  Daily Mood delivers a warm, deeply thoughtful life message to every registered user each morning and evening — tuned to their emotional state. Unlike static quote cards, Daily Mood is mood-aware: users report how they're feeling (happy, anxious, tired, lost, grateful…) and instantly receive a message crafted for that exact headspace. Every morning at 08:00 a fresh message goes out; every evening at 21:00 a gentle night-time reflection closes the day. Multi-user support means the cron job walks every registered user and sends each one a personalised push in their preferred language (Chinese or English). No external API needed — all message generation is handled by the Agent's own language ability, grounded by a curated mood-to-tone mapping.

  Trigger words: 心情寄语, 今日寄语, 人生寄语, 寄语, 今天心情, 我今天很累, 我很焦虑, 我很开心, 我迷茫了, 给我一句话, 鼓励我, 陪伴, 治愈, 晚安寄语, 早安寄语, daily mood, mood message, life message, morning message, evening message, send me a message, encourage me, daily wisdom, 每日寄语, 开启寄语推送.
keywords: 心情寄语, 今日寄语, 人生寄语, 寄语, 早安寄语, 晚安寄语, 每日寄语, 心情, 情绪, 治愈, 陪伴, 鼓励, 我很累, 我很焦虑, 我很开心, 我迷茫了, 给我一句话, 每天推送, 多用户推送, 个性化寄语, daily mood, mood message, life message, morning message, evening message, encourage me, daily wisdom, emotional support, personalized push, mood-aware
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Mood — 每日心情寄语

> 情绪陪伴型人生寄语 · 早晨唤醒 · 夜间治愈 · 心情感知 · 中英双语 · 多用户定时推送

---

## 何时使用

- 用户说"给我一句寄语""今天的寄语""鼓励我一下"
- 用户说"我今天很累 / 很焦虑 / 很开心 / 很迷茫"
- 用户说"早安 / 晚安"（触发对应时段推送）
- 用户说"开启寄语推送""每天给我推寄语"
- cron 08:00 触发早晨全量推送
- cron 21:00 触发傍晚全量推送

---

## 🌐 语言规则

- 跟随用户注册档案的 `language` 字段（`zh` 或 `en`）
- 未注册用户：默认中文；英文提问自动切英文
- 寄语本体：以用户语言呈现；双语版本按需提供

---

## 💬 心情类型与寄语基调

| 心情 | 英文 | 寄语基调 |
|------|------|---------|
| 开心 / excited | happy | 共鸣共喜，引导感恩珍惜 |
| 低落 / sad | sad | 温柔接纳，不说"加油"，说"你可以停下来" |
| 焦虑 / anxious | anxious | 放慢节奏，让当下变小，具体而微的安慰 |
| 疲惫 / tired | tired | 允许休息，休息本身就是努力 |
| 迷茫 / lost | lost | 不给答案，给方向感；迷茫是生长的前奏 |
| 平静 / calm | calm | 深化平静，引导觉察当下之美 |
| 感恩 / grateful | grateful | 扩展感恩，从小事到生命本身 |
| 愤怒 / angry | angry | 先接纳情绪，再引导释放，不评判 |

---

## 📖 功能列表

### 每日推送（多用户）

| 时间 | 脚本 | 内容 |
|------|------|------|
| 08:00 每日 | `morning-push.js` | 早晨唤醒寄语：根据用户心情档案定制 |
| 21:00 每日 | `evening-push.js` | 夜间疗愈寄语：温柔收尾，引导好眠 |

### 心情响应（即时）

用户报告心情后立即返回匹配寄语：

```
用户：我今天很焦虑
→ 一段专门写给焦虑状态的温暖寄语（100-150字）+ 一句简短金句

用户：I'm feeling lost today
→ A warm, mood-matched message in English (100-150 words) + one short quote
```

### 用户注册

注册后可享受：个性化语言设置、心情档案记忆、定时推送

---

## 🛠️ 脚本用法

```bash
# 注册用户（解锁定时推送）
node scripts/register.js <userId> [--lang zh|en] [--mood calm]
node scripts/register.js alice --lang zh --mood anxious
node scripts/register.js bob --lang en --mood happy

# 查看注册信息
node scripts/register.js --show <userId>

# 早晨推送（cron 调用 / 手动测试）
node scripts/morning-push.js                    # 全量推送所有注册用户
node scripts/morning-push.js --user <userId>    # 测试单用户
node scripts/morning-push.js --mood tired       # 指定心情（测试用）

# 傍晚推送
node scripts/evening-push.js
node scripts/evening-push.js --user <userId>

# 心情响应（用户实时触发）
node scripts/mood-response.js <mood> [--lang zh|en] [--userId <id>]
node scripts/mood-response.js anxious --lang zh
node scripts/mood-response.js happy --lang en

# 推送管理
node scripts/push-toggle.js on [--userId <id>]   # 开启（全局或单用户）
node scripts/push-toggle.js off [--userId <id>]
node scripts/push-toggle.js status
```

---

## ⏰ Cron 配置

```bash
openclaw cron add "0 8 * * *"  "cd ~/.openclaw/workspace/skills/daily-mood && node scripts/morning-push.js"
openclaw cron add "0 21 * * *" "cd ~/.openclaw/workspace/skills/daily-mood && node scripts/evening-push.js"
openclaw cron list
openclaw cron delete <任务ID>
```

---

## 📁 数据文件

```
data/users/<userId>.json   # 用户档案：language, mood, pushEnabled, registeredAt
scripts/
  morning-push.js          # 早晨全量推送
  evening-push.js          # 傍晚全量推送
  mood-response.js         # 心情即时响应
  register.js              # 用户注册管理
  push-toggle.js           # cron 开关
```

---

## ⚠️ 注意事项

1. 寄语不是心理治疗——不对用户的情绪下诊断，不说"你一定没问题"
2. 低落/焦虑/愤怒状态：先共情，后寄语，避免"加油""想开点"等无效安慰
3. 用户数据仅含语言偏好和心情标签，不存储原始对话内容
4. 多用户推送时每位用户独立生成寄语，不共用同一段文字
5. 未注册用户可直接触发心情响应，注册后才启用定时推送

---

*Version: 1.0.0 · Created: 2026-04-04*

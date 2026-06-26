---
name: daily-reflect
description: "Daily journaling prompts for meaningful reflection — morning intention-setting and evening review. Build a consistent self-reflection habit one prompt at a time."
keywords:
  - 日记
  - 写日记
  - 今天写什么
  - 每日日记
  - 日记打卡
  - 自我反思
  - 情绪日记
  - 成长日记
  - 感恩日记
  - 晨间日记
  - 晚间日记
  - 日记引导
  - 五年日记
  - 每日复盘
  - journal
  - daily journal
  - journaling
  - writing prompt
  - morning journal
  - evening reflection
  - gratitude journal
  - self-reflection
  - mindfulness journal
  - bullet journal
  - diary
  - daily writing
  - mood journal
  - growth journal
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# 每日日记引导

> 每日日记引导 — 晨间写作 · 晚间反思 · 情绪觉察 · 习惯打卡

## 何时使用

- 用户说"写日记""今天写什么""日记打卡"
- 用户想做情绪记录、自我反思
- 用户说"journal""journaling""writing prompt"
- 用户说"帮我复盘今天""今天有什么值得记录的"

---

## 推送管理

```bash
node scripts/push-toggle.js on <userId>
node scripts/push-toggle.js on <userId> --morning 09:00 --evening 21:00 --channel feishu
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

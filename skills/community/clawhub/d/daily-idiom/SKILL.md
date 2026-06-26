---
name: daily-idiom
description: "Daily Chinese idiom (成语) — origin story, meaning, usage examples, and memory tip. Build Chinese vocabulary and cultural knowledge one 成语 per day."
keywords:
  - 成语
  - 每日成语
  - 今日成语
  - 成语故事
  - 俗语
  - 歇后语
  - 谚语
  - 学成语
  - 成语打卡
  - 中文学习
  - 汉语成语
  - 四字成语
  - 成语典故
  - 成语用法
  - 成语造句
  - 文化成语
  - 历史成语
  - Chinese idiom
  - chengyu
  - idiom of the day
  - learn Chinese
  - daily chengyu
  - Chinese culture
  - idiom story
  - Chinese proverb
  - Mandarin learning
  - Chinese language
  - 成语接龙
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# 每日成语

> 每日成语 — 典故故事 · 用法例句 · 测验打卡 · 中文文化输出

## 何时使用

- 用户说"成语""今日成语""成语故事"
- 用户学习中文或想了解中国文化
- 用户说"idiom""chengyu""learn Chinese"
- 用户说"成语接龙""猜成语""成语测验"

---

## 推送管理

```bash
node scripts/push-toggle.js on <userId>
node scripts/push-toggle.js on <userId> --morning 08:00 --evening 21:00 --channel feishu
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

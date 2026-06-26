---
name: daily-poem
description: |
  Daily Poem delivers one carefully chosen poem every morning — rotating between Chinese classical poetry (唐诗宋词), modern Chinese verse, and English poems — complete with translation, background story, annotation notes, and recitation rhythm guide. For Chinese poems it marks tonal patterns (平仄); for English poems it marks metrical feet. Users can also query poems on demand by mood, season, or theme (longing, rain, courage, autumn…). Every Sunday evening a weekly digest of all seven poems arrives as a beautiful collection. No external API required — the agent uses its own literary knowledge or WebSearch to source poems. Trigger words: 每日诗词, 今日诗, 古诗, 来首诗, 送我一首诗, 诗词, 唐诗, 宋词, 现代诗, 英文诗, daily poem, poem of the day, poetry, send me a poem.
keywords: 每日诗词, 古诗, 唐诗, 宋词, 现代诗, 英文诗, 诗词推送, 今日诗, 来首诗, 送我一首诗, 诗词赏析, 朗读节奏, 平仄, 词源, 意象, 周合辑, 诗词查询, 按心情查诗, 按主题查诗, daily poem, poem of the day, poetry, classical chinese poetry, english poem, weekly digest, poem push, poetry analysis
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Daily Poem — 每日诗词

> 私人诗词助手 — 每日精选 · 中英双语 · 赏析解读 · 按需查诗

---

## 何时使用

- 用户说"来首诗""送我一首诗""今日诗词""给我推一首"
- 用户说"来首关于秋天/离别/励志/雨/爱情的诗"
- 用户说"唐诗宋词""现代诗""英文诗"
- 用户说"开启诗词推送""每天给我推诗"
- 每周日晚间自动发送本周诗词合辑

---

## 🌐 语言规则

- 默认中文；用户英文提问切英文
- 中文诗保留原文，附英译；英文诗保留原文，附中译
- 专有名词（诗人名、词牌名）保留原文，括号内附拼音/译文

---

## 📖 功能列表

### 每日推送

每日 08:00 推送一首精选诗，按以下规律轮换：
- 周一/三/五：中国古典诗词（唐诗、宋词、元曲）
- 周二/四：中国现代诗（1919-今）
- 周六/日：英文诗（莎士比亚、济慈、聂鲁达、弗罗斯特等）

每首包含：标题·作者·朝代/年代 → 原文 → 译文 → 背景故事（2-3句）→ 赏析要点（2-3个意象/手法）→ 朗读节奏

### 按需查诗

| 命令 | 示例 |
|------|------|
| 按心情 | `来首悲秋的诗` / `推荐励志的诗` |
| 按季节 | `春天的诗` / `冬日诗词` |
| 按主题 | `关于离别的诗` / `月亮诗词` / `战争诗` |
| 按作者 | `李白的诗` / `苏轼的词` / `Keats poem` |
| 按体裁 | `五言绝句` / `宋词` / `英文十四行诗` |
| 随机 | `来首诗` / `随机一首` |

### 每周诗词合辑

每周日 20:00 推送本周 7 首诗词合辑，附本周诗词主题总结。

---

## 🛠️ 脚本说明

```bash
# 每日推送（由 cron 调用）
node scripts/morning-push.js
node scripts/morning-push.js --lang en
node scripts/morning-push.js --theme 离别

# 按需查诗
node scripts/query.js 秋天
node scripts/query.js "李白" --lang zh
node scripts/query.js rain --lang en

# 周合辑
node scripts/weekly-digest.js
node scripts/weekly-digest.js --lang en

# 推送管理
node scripts/push-toggle.js on
node scripts/push-toggle.js off
node scripts/push-toggle.js status
```

---

## ⏰ Cron 配置

```bash
openclaw cron add "0 8 * * *"  "cd ~/.openclaw/workspace/skills/daily-poem && node scripts/morning-push.js"
openclaw cron add "0 20 * * 0" "cd ~/.openclaw/workspace/skills/daily-poem && node scripts/weekly-digest.js"
openclaw cron list
openclaw cron delete <任务ID>
```

---

## 📁 数据文件

```
data/push-log.json    # 推送历史（避免7天内重复推送同一首诗）
scripts/
  morning-push.js     # 每日早晨推送
  query.js            # 按需查诗
  weekly-digest.js    # 周合辑
  push-toggle.js      # cron 开关
```

---

## ⚠️ 注意事项

1. 不依赖外部 API，由 Agent 凭文学知识或 WebSearch 选诗
2. push-log.json 记录最近推送过的诗，避免短期内重复
3. 赏析内容由 Agent 生成，不代表唯一解读，欢迎用户提出不同见解
4. 英文诗版权：只推送版权已过期的作品（作者逝世超过 70 年）或引用公共领域作品

---

*Version: 1.0.0 · Created: 2026-04-04*

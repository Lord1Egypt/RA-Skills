# Daily Xuanzang / 每日大唐西域记

**English**

A bilingual skill for reading the **Great Tang Records on the Western Regions (大唐西域记)** progressively, one segment at a time — following the monk **Xuanzang's Western Journey** across the Silk Road, Central Asia, Afghanistan, and the whole of India in the 7th century.

Designed as a daily geography-and-pilgrimage lecture experience with:
- progressive reading through all **12 fascicles** (CBETA T51n2087, ~390k chars)
- **bundled source text** — no network fetch needed
- auto-tracked progress (character-precise cursor)
- vernacular Chinese / English translation
- a **bilingual route map** each episode showing "where on the journey we are today"
- optional scene art + voice narration

**中文**

这是一个面向玄奘《**大唐西域记**》的双语讲读 skill，沿玄奘西行路线**逐段推进**：从高昌出发，过丝路北道与中亚，翻越葱岭进入五印度，遍历佛陀生灭四大圣地与那烂陀寺，再原路返回于阗——亲践 110 国、传闻 28 国，共 138 国的地理风土实录。

默认特性：
- **逐段推进**全 12 卷（《大正藏》No.2087）
- **自带原典全文**，无需联网取经文
- **自动记录进度**（精确到字符的游标）
- **白话 / 英文翻译**
- **每期中英文路线地图**（标出"今天西行到哪里"）
- **可选配图 + 语音**

## What it does / 每期交付

For each episode, the skill generates:
1. **Full lecture** — 原文节录 → 白话/英文翻译 → 背景讲解 → 下期预告
2. **Bilingual route map** — Chinese ancient names + modern English/pinyin place names, gold east→west route, compass, terrain
3. *(optional)* **Scene image** — a vivid sacred site / landscape from the episode
4. *(optional)* **Voice narration**

地图是本 skill 的**核心特色**，默认每期都有，除非用户明确关闭。

## Why this skill exists / 立意

《大唐西域记》不只是游记，而是一部 7 世纪中亚与印度的"实地调查报告"，也是近代考古找回那烂陀寺、鹿野苑、菩提伽耶的头号文献。这个 skill 的目标是把它做成：
- 每天能读的一段
- 看得懂的白话
- **看得到的地理**（地图一路向西）
- 有圣迹画面、有声音

So it feels like a **daily illustrated pilgrimage** rather than a dry reference lookup.

## Delivery flow / 默认顺序

1. **Write the full lecture** 正文
2. **Generate the bilingual route map** 路线地图
3. *(optional)* scene image / voice 配图 / 语音
4. **Advance progress** 推进进度

## Example map / 示例地图

![Daily Xuanzang route map — Silk Road north (Vol.1)](./assets/example-map.jpg)

> 卷一·北道丝绸之路：自高昌经焉耆、龟兹西抵跋禄迦，转向中亚。

## Core files / 核心文件

- `SKILL.md` — main workflow and delivery rules
- `references/structure.md` — 12-fascicle geography & era map
- `references/style-guide.md` — translation tone, map prompt & formatting rules
- `scripts/progress.py` — character-precise progress tracker + segment extractor
- `data/volumes/vol01.txt .. vol12.txt` — bundled CBETA source text

## Progress commands

```bash
python3 scripts/progress.py set-lang --lang zh|en
python3 scripts/progress.py status
python3 scripts/progress.py next                 # -> JSON segment
python3 scripts/progress.py advance <consumed> --title "..."
python3 scripts/progress.py reset
```

## Triggers / 触发词

- `大唐西域记` · `西域记` · `玄奘西行`
- `daily xuanzang` · `xuanzang` · `xiyuji`
- `今日西域记` · `继续读西域记`

## Source & License

Source text: **Taishō Tripiṭaka No.2087 (T51n2087)**, *Great Tang Records on the Western Regions*, via the CBETA digital canon (public domain canonical text). The skill code is GPL-3.0-or-later.

## Repository context

Part of the `YumSkills` collection. A sibling to `daily-tongjian` — same "daily classical reading" family, but pilgrimage-and-geography flavored, with a route map at the heart of every episode.

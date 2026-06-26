---
name: chinese-name-generator
description: |
  Chinese name selection service. Activated when user needs to name a child (给孩子取名、起名、取名字).
  Includes: Eight Characters (八字) analysis, Five Elements (五行) balance, sound rhyme (音韵), 
  meaning (寓意), family generation (辈分), avoid homophones (避讳谐音), and references to 
  Thirteen Classics (十三经), Poetry (诗词), Chuci (楚辞), etc.
---

# Chinese Name Generator (取名)

Comprehensive Chinese name selection service based on traditional Chinese naming conventions.

## When to Use

- User asks to name a child (取名、起名、给宝宝起名字)
- User asks about naming conventions (取名讲究、取名有什么讲究)
- User provides baby's birth information for name suggestions

## Required Information

To provide accurate name suggestions, gather:

1. **Birth Date (出生时间)**: Year, Month, Day, Hour (最好精确到时辰)
2. **Gender (性别)**: Boy or Girl
3. **Family Name (姓氏)**: 父姓 + 母姓 (if applicable)
4. **Generation Characters (辈分字)**: If family has name generation chart
5. **Parents' Preferences (父母期望)**: Any specific wishes or restrictions

## Name Selection Principles

### 1. Eight Characters & Five Elements (八字五行)

Analyze the baby's birth chart to find what Five Elements are missing or weak:

| 五行 | 代表字旁 | 寓意 |
|------|----------|------|
| 木 | 木、草、禾、竹、梅、松、柏、桐、榆、枫 | 生长、仁慈 |
| 火 | 火、光、炎、晖、亮、旭、晨、昭、明星 | 热情、礼仪 |
| 土 | 土、石、玉、坤、砚、墨、圭、堂、嵩、峦 | 稳重、承载 |
| 金 | 金、玉、钢、锐、铭、铎、钧、镜、珠、琳 | 坚硬、尊贵 |
| 水 | 水、雨、雪、云、涛、澜、泉、溪、瀚、洋 | 智慧、流动 |

### 2. Sound & Rhythm (音韵)

- **声调搭配**: Avoid all same tones (e.g., 柳想想 ❌)
- **平仄协调**: Prefer pattern like 平仄平 or 仄平仄
- **韵母和谐**: Avoid same finals causing tongue-twisters
- **响亮顺口**: 1st/2nd tone (平声) more响亮

### 3. Meaning & Imagery (寓意)

Common categories:
- **美德 (Virtues)**: 仁、义、礼、智、信、孝、忠、诚、恭、俭
- **吉祥 (Auspicious)**: 福、禄、寿、喜、祥、安、和、泰、宁
- **自然 (Nature)**: 山、水、云、风、雨、雪、星、月、日
- **期望 (Aspirations)**: 志、远、卓、然、成、立、达、显、耀
- **才华 (Talent)**: 文、章、诗、书、画、才、学、思、慧、敏

### 4. Classical References (典籍出处)

- **诗经**: "桃之夭夭，灼灼其华"
- **楚辞**: "路漫漫其修远兮"
- **论语**: "君子成人之美"
- **唐诗宋词**: 名句妙用

### 5. Avoid Bad Omens (避讳)

- **谐音不雅**: 避免与不雅词同音 (如: 史珍香、杜子腾)
- **生肖冲克**: 根据属相避免相冲字
- **祖先名讳**: 避免与祖辈同名
- **多音字**: 避免容易读错的字

### 6. Three Talents & Five Grids (三才五格)

Calculate based on surname and name strokes for:
- 天格 (Heaven)
- 人格 (Person)  
- 地格 (Earth)
- 总格 (Total)
- 外格 (External)

Prefer combinations that are auspicious numbers in 81数理.

## Output Format

Present names in this structured format:

```
### 薛○○ (Xué ○○)

**拼音**: Xué ○○  
**五行**: 木/火/土/金/水 (根据八字喜用)  
**寓意**: 来自经典出处，解释含义  
**出处**: 《诗经》/《楚辞》/《论语》/自创  
**八字匹配**: 补○神之不足  
**声调**: ○○ (平仄搭配)
```

## Common Name Databases

### 男孩常用字 (Boy Names)
- 伟、磊、军、杰、涛、明、勇、浩、鹏、飞
- 梓、柏、沐、枫、霖、岳、岩、峰、峻、岚
- 睿、哲、弘、奕、博、冠、铭、铎、钧、锐

### 女孩常用字 (Girl Names)
- 琳、婷、雅、芸、菲、萍、娜、颖、珊、慧
- 萱、苒、苔、蕴、思、媛、怡、嘉、宁、安静
- 芷、兰、莲、荷、梅、松、竹、棠、桦、桐

## Tools Available

- **web_search / minimax search**: Search classical references and name meanings
- **web_fetch**: Fetch from Chinese dictionaries (汉典, 说文解字)
- Write results to file or present directly

## Tips

1. Always ask for birth date before making suggestions
2. Check each name against Five Elements requirement
3. Provide 3-5 options with different characteristics
4. Include pinyin and detailed explanation for each name
5. Reference classical sources when possible

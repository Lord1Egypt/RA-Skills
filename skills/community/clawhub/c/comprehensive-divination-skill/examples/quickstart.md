# 🚀 Quickstart Examples

Three end-to-end examples showing how to use comprehensive-divination-skill from a cold start.

## Example 1: 小六壬 (Xiao Liu Ren) — 30-second divination

**Question**: "今天能不能顺利收到快递？"

```bash
cd ~/.hermes/skills/comprehensive-divination-skill/scripts
python common.py --snapshot
```

**Output (truncated)**:
```json
{
  "solar_date": "2026-06-15",
  "lunar_month": 5,
  "lunar_day": 1,
  "day_gz": "庚申",
  "shichen": "酉",
  "shichen_idx": 10
}
```

```bash
python xiao_liuren.py -m 5 -d 1 -t 10
```

**Output (truncated)**:
```json
{
  "method": "月日时推算",
  "params": {"month": 5, "day": 1, "shichen": 10},
  "result_gong": 4,
  "result": {
    "name": "赤口",
    "wuxing": "金",
    "color": "白色",
    "ji_xiong": "凶",
    "summary": "口舌是非，行事有阻。求谋不顺，出行不宜。"
  }
}
```

**Interpretation**: 赤口 = 凶，主口舌是非。问快递"顺利与否"，赤口暗示**可能延迟或有纠纷**（如收件地址出错、被签收未通知等）。

---

## Example 2: 六爻纳甲 (Liu Yao) — Job interview outcome

**Question**: "我上周面的某公司能否通过？"

```bash
cd ~/.hermes/skills/comprehensive-divination-skill/scripts

# Step 1: 冻结时间 + 真太阳时校准
python common.py --snapshot --city 成都

# Output gives: day_gz=庚申, shichen=申

# Step 2: 起卦（六爻 + 纳甲装卦）
python liuyao_yaogua.py --json --day-tg 庚 --day-dz 申
```

**Output (truncated)**:
```json
{
  "gua_name": "泽地萃",
  "gua_gong": "兑",
  "biangua_name": "泽雷随",
  "dong_lines": [[1, "×"]],
  "shi_line": 2,
  "ying_line": 5,
  "lines": [
    {"pos": 1, "di_zhi": "未", "wuxing": "土", "liuqin": "父母", "is_dong": true, "liushen": "白虎"},
    {"pos": 2, "di_zhi": "巳", "wuxing": "火", "liuqin": "官鬼", "is_dong": false, "liushen": "玄武", "shi_ying": "世"},
    {"pos": 6, "di_zhi": "未", "wuxing": "土", "liuqin": "父母", "is_dong": false, "liushen": "螣蛇"}
  ]
}
```

**Key signals**:
- 泽地萃 (gathering) + 变泽雷随 (following) — both auspicious
- 官鬼巳火 in shi position (官鬼持世) — position offered
- 父母未土 白虎动 — notification imminent, formal
- 萃卦辞: "利见大人，亨" — meet someone important, success

**Verdict**: ✅ Through, with 6/18-19 应期.

---

## Example 3: 梅花易数 (Mei Hua) — Quick decision

**Question**: "我现在该不该换工作？"

```bash
python meihua_qigua.py -d 2026-06-15 -t 18
```

**Output (truncated)**:
```json
{
  "ben_gua": {"name": "雷风恒", "up": "震", "down": "巽"},
  "bian_gua": {"name": "火风鼎", "up": "离", "down": "巽"},
  "ti_gua": {"name": "震", "wuxing": "木"},
  "yong_gua": {"name": "巽", "wuxing": "木"},
  "ti_yong_shengke": {"relation": "比和", "ji_xiong": "吉"}
}
```

**Key signals**:
- 本卦雷风恒 — 恒心/持久/稳定
- 变卦火风鼎 — 鼎新/稳定/变革
- 体用比和 (both wood) — you and the situation align
- 互卦泽天夬 — 决断 (decision time)

**Verdict**: ✅ Change is favorable, 鼎新 is on your side.

---

## Example 4: 大六壬 (Da Liu Ren) — Major decision

**Question**: "该不该接受这个 offer？"

```bash
python da_liuren.py -d 2026-06-15 -t 18
```

**Output structure** (十二天将 + 天地盘 + 四课三传):

```json
{
  "tiangan": "庚",
  "dizhi": "申",
  "yuejiang": "申 (传送)",
  "shichen": "酉",
  "sike": ["巳申", "申巳", "丑戌", "戌丑"],
  "sanzhuan": {"初传": "巳", "中传": "申", "末传": "丑"},
  "tianjiang": ["贵人", "腾蛇", "朱雀", "青龙", "勾陈", "白虎"]
}
```

**Key signals**:
- 月将传送 (申金) — autumnal metal, decisive
- 初传巳火 (官鬼) — position-related
- 三传走势: 巳→申→丑 — fire→metal→earth, 阶段性转化
- 末传丑土 (财库) — final landing in financial/wealth storage

**Verdict**: Decision favorable but takes time. Final outcome lands in a "财库" (financial stability).

---

## Common patterns

All four examples share:

1. **Time anchor is Beijing time (UTC+8)** — independent of where you run the script
2. **True solar time (longitude)** — applied for local shichen
3. **JSON output** — designed to be consumed by LLM for interpretation
4. **Deterministic results** — same input → same output (no random hexagrams; coin tosses use seeded RNG if needed)

## What's next?

- **复占对比** (advanced): see [`re-consultation-comparison.md`](re-consultation-comparison.md)
- **海外用户** (international): see [`international-user.md`](international-user.md)
- **函数化 pipeline** (programmatic): see `../README.md` "🌍 International Users" section

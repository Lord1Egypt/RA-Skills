# 🌍 International User Example

> **For users outside China**: This skill's time anchor is **always Beijing time (UTC+8)**, independent of where you run the script. Your longitude then calibrates to your local true solar time.

## Setup

You're in **New York** (-74.006° longitude), it's 5:01 AM EDT on 2026-06-15. You want to consult on a business decision.

## ⚠️ The bug and why we fixed it

**Old (broken) approach** — what would have happened in the old code:

```bash
# Old code: takes local clock time, treats it as Beijing time, then "corrects"
# Your local clock: 2026-06-15 05:01 (EDT)
# Treated as Beijing time: 2026-06-15 05:01
# "Corrected" by -74.006°: 2026-06-15 05:01 - 776 min = 2026-06-14 16:05
# Result: shichen = 申 (WRONG! should be 寅)
```

**New (correct) approach** — current implementation:

```bash
# New code: takes UTC, +8h = Beijing time, then corrects
# UTC: 2026-06-15 09:01
# Beijing time: 2026-06-15 17:01
# Corrected by -74.006°: 2026-06-15 17:01 - 776 min = 2026-06-15 04:05
# Result: shichen = 寅 (CORRECT! you woke up at dawn)
```

**Difference: 12 hours** — entire shichen wrong in old code.

---

## Step-by-step: New York user, business question

**Question**: "Should I switch jobs this quarter?"

### Step 1: Get current time snapshot (Beijing time)

```bash
cd ~/.hermes/skills/comprehensive-divination-skill/scripts
python common.py --snapshot --lon -74.006
```

**Output (truncated)**:
```json
{
  "bj_dt": "2026-06-15 17:01:23",   ← Always Beijing time
  "tst_dt": "2026-06-15 04:05:08",  ← Local true solar time
  "tst_offset_min": -776.1,         ← 776 min behind Beijing
  "shichen": "寅",                   ← Correct (not 申)
  "shichen_idx": 3,
  "day_gz": "庚申",
  "lunar_month": 5,
  "lunar_day": 1
}
```

### Step 2: Cast hexagram (Liu Yao for career question)

```bash
python liuyao_yaogua.py --json --day-tg 庚 --day-dz 申
```

**Output (truncated)**:
```json
{
  "gua_name": "泽地萃",
  "biangua_name": "泽雷随",
  "shi_line": 2,
  "lines": [
    {"pos": 2, "di_zhi": "巳", "liuqin": "官鬼", "shi_ying": "世"},
    ...
  ]
}
```

### Step 3: Python API (recommended for LLM agents)

```python
import sys
sys.path.insert(0, '~/.hermes/skills/comprehensive-divination-skill/scripts')
import common
import liuyao_yaogua

# 1. Get current Beijing time
bj = common.get_beijing_time()
print(f"Beijing time: {bj}")

# 2. Apply true solar time correction for New York
tst = common.longitude_to_true_solar(bj, longitude=-74.006)
print(f"New York TST: {tst['tst_datetime']} (offset: {tst['tst_offset_min']} min)")

# 3. Get full pipeline info
info = common.get_full_pipeline(longitude=-74.006)
print(f"Shichen: {info['shichen']}时, Day GZ: {info['day_gz']}")

# 4. Cast hexagram with the correct day
gua = liuyao_yaogua.run(day_tg=info['day_tg'], day_dz=info['day_dz'])
print(f"Hexagram: {gua['gua_name']} → {gua['biangua_name']}")
```

**Output (truncated)**:
```
Beijing time: 2026-06-15 17:01:23
New York TST: 2026-06-15 04:05:08 (offset: -776.1 min)
Shichen: 寅时, Day GZ: 庚申
Hexagram: 泽地萃 → 泽雷随
```

---

## Cross-day handling

**Scenario**: It's 06:00 Beijing time on 2026-06-15 (early morning). For a New York user, this is actually **2026-06-14 17:00 EDT** — i.e., **yesterday afternoon** in New York.

```python
import common
from datetime import datetime

bj = datetime(2026, 6, 15, 6, 0)  # Beijing 6 AM
tst = common.longitude_to_true_solar(bj, -74.006)
print(tst['tst_datetime'])  # → 2026-06-14 17:03 (yesterday in NY)
```

**This is astronomical fact, not a bug.** When asking the question at 6 AM Beijing time, the **sun is setting in New York on the previous day**. The skill handles this correctly.

---

## Other longitudes (cheat sheet)

| City | Longitude | 6/15 18:00 BJ → local TST | Local shichen |
|---|---|---|---|
| New York (夏令) | -74.006 | 04:05 (-776 min) | 寅 |
| New York (冬令) | -74.006 | 03:05 (-896 min) | 寅 |
| London | -0.1278 | 10:00 (-480 min) | 巳 |
| Paris | 2.3522 | 10:09 (-473 min) | 巳 |
| Berlin | 13.4050 | 10:33 (-441 min) | 巳 |
| Sydney | 151.2093 | 20:01 (+121 min) | 戌 |
| Tokyo | 139.6917 | 19:19 (+79 min) | 戌 |
| Singapore | 103.8198 | 17:35 (-15 min) | 酉 |
| Hong Kong | 114.1694 | 17:46 (-14 min) | 酉 |

**Quick mental model**: 
- East of 120° (e.g. Tokyo, Sydney) → local time **later** than Beijing
- West of 120° (e.g. London, New York) → local time **earlier** than Beijing
- The further from 120°, the bigger the offset

---

## Common mistakes to avoid

| ❌ Don't | ✅ Do |
|---|---|
| Pass your local clock time to the script | Let `get_beijing_time()` handle it |
| Trust old results for non-China timezones | Use current version |
| Use `--auto` flag (uses local clock) | Use explicit longitude |
| Forget negative signs for west longitudes | New York: `-74.006`, not `74.006` |
| Assume day_gz won't change across timezones | It will (跨日) — that's correct |

---

## Verifying the fix

If you want to confirm the fix is working:

```python
import common
import datetime

# What the old code would do (broken):
broken_now = datetime.datetime.now()  # local clock
# → if you're in NY, this is 05:01, treated as Beijing 05:01
# → "corrected" by -776 min = 16:05 yesterday
# → shichen = 申 (WRONG)

# What the new code does (correct):
bj = common.get_beijing_time()  # 17:01 BJ always
tst = common.longitude_to_true_solar(bj, -74.006)  # 04:05 today in NY
# → shichen = 寅 (CORRECT)
```

The 12-hour difference is the entire fix.

---

> 占卜结果仅供参考，请结合实际情况理性判断。
> Divination results are for reference only; please use rational judgment based on actual circumstances.

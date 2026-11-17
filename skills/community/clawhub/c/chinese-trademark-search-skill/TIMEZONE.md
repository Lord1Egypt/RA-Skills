# Timezone and Date Reference / 时区与日期参考

**Effective Date:** 2026-03-28
**Last Updated:** 2026-03-28

---

## English

### Date and Time Conventions in the API

The Chinese Trademark Search API uses two date/time formats. Understanding these conventions is essential for correct interpretation of trademark filing dates, registration dates, and expiration dates.

### Date-Only Fields (YYYY-MM-DD)

Fields that contain only a date (no time component) represent **China calendar dates**.

| Field Example | Format | Meaning |
|---|---|---|
| `filingDate: "2025-06-15"` | YYYY-MM-DD | June 15, 2025 in China |
| `registrationDate: "2026-01-10"` | YYYY-MM-DD | January 10, 2026 in China |
| `expirationDate: "2036-01-09"` | YYYY-MM-DD | January 9, 2036 in China |

These dates correspond to the official dates as recorded by CNIPA. They are **not relative to any timezone** - they are absolute calendar dates in China.

### DateTime Fields with Timezone Offset

Fields that include a time component use **China Standard Time (CST, UTC+8)**, indicated by the `+08:00` offset.

| Field Example | Format | Meaning |
|---|---|---|
| `queryTimestamp: "2026-03-28T14:30:00+08:00"` | ISO 8601 | 2:30 PM China Standard Time |
| `exportCreatedAt: "2026-03-28T09:00:00+08:00"` | ISO 8601 | 9:00 AM China Standard Time |

### Conversion Examples

The following table shows how to convert a China Standard Time (CST, UTC+8) timestamp to common timezones:

| China (CST, UTC+8) | US Eastern (ET, UTC-5/-4) | US Pacific (PT, UTC-8/-7) | EU Central (CET, UTC+1/+2) | Japan (JST, UTC+9) |
|---|---|---|---|---|
| 2026-03-28 **09:00** | 2026-03-27 **21:00** (EDT) | 2026-03-27 **18:00** (PDT) | 2026-03-28 **02:00** (CET) | 2026-03-28 **10:00** |
| 2026-03-28 **14:30** | 2026-03-28 **02:30** (EDT) | 2026-03-27 **23:30** (PDT) | 2026-03-28 **07:30** (CET) | 2026-03-28 **15:30** |
| 2026-03-28 **18:00** | 2026-03-28 **06:00** (EDT) | 2026-03-28 **03:00** (PDT) | 2026-03-28 **11:00** (CET) | 2026-03-28 **19:00** |
| 2026-03-28 **23:59** | 2026-03-28 **11:59** (EDT) | 2026-03-28 **08:59** (PDT) | 2026-03-28 **16:59** (CET) | 2026-03-29 **00:59** |

**Note on Daylight Saving Time (DST):**
- China does **not** observe DST. CST is always UTC+8.
- US Eastern Time: EST (UTC-5) in winter, EDT (UTC-4) in summer.
- US Pacific Time: PST (UTC-8) in winter, PDT (UTC-7) in summer.
- EU Central European Time: CET (UTC+1) in winter, CEST (UTC+2) in summer.
- Japan Standard Time: JST (UTC+9) year-round, no DST.

### CLI Behavior

The CLI outputs **raw API timestamps** without any timezone conversion. All timestamps in CLI output are in China Standard Time (UTC+8).

To convert timestamps to your local timezone, use your operating system or programming language utilities:

```bash
# macOS / Linux
date -d "2026-03-28T14:30:00+08:00" "+%Y-%m-%d %H:%M:%S %Z"

# Python
from datetime import datetime, timezone, timedelta
cst = datetime.fromisoformat("2026-03-28T14:30:00+08:00")
local = cst.astimezone()  # converts to system local timezone
print(local.strftime("%Y-%m-%d %H:%M:%S %Z"))

# JavaScript (Node.js)
const d = new Date("2026-03-28T14:30:00+08:00");
console.log(d.toLocaleString("en-US", { timeZoneName: "short" }));
```

---

## 中文

### API 中的日期和时间约定

中国商标查询 API 使用两种日期/时间格式。正确理解这些约定对于准确解读商标申请日期、注册日期和到期日期至关重要。

### 仅日期字段（YYYY-MM-DD）

仅包含日期（无时间分量）的字段表示**中国日历日期**。

| 字段示例 | 格式 | 含义 |
|---|---|---|
| `filingDate: "2025-06-15"` | YYYY-MM-DD | 中国时间 2025 年 6 月 15 日 |
| `registrationDate: "2026-01-10"` | YYYY-MM-DD | 中国时间 2026 年 1 月 10 日 |
| `expirationDate: "2036-01-09"` | YYYY-MM-DD | 中国时间 2036 年 1 月 9 日 |

这些日期对应 CNIPA 记录的官方日期。它们**不相对于任何时区** - 是中国的绝对日历日期。

### 带时区偏移的日期时间字段

包含时间分量的字段使用**中国标准时间（CST，UTC+8）**，以 `+08:00` 偏移量表示。

| 字段示例 | 格式 | 含义 |
|---|---|---|
| `queryTimestamp: "2026-03-28T14:30:00+08:00"` | ISO 8601 | 中国标准时间下午 2:30 |
| `exportCreatedAt: "2026-03-28T09:00:00+08:00"` | ISO 8601 | 中国标准时间上午 9:00 |

### 转换示例

下表展示如何将中国标准时间（CST，UTC+8）时间戳转换为常用时区：

| 中国（CST，UTC+8） | 美国东部（ET，UTC-5/-4） | 美国太平洋（PT，UTC-8/-7） | 欧洲中部（CET，UTC+1/+2） | 日本（JST，UTC+9） |
|---|---|---|---|---|
| 2026-03-28 **09:00** | 2026-03-27 **21:00**（EDT） | 2026-03-27 **18:00**（PDT） | 2026-03-28 **02:00**（CET） | 2026-03-28 **10:00** |
| 2026-03-28 **14:30** | 2026-03-28 **02:30**（EDT） | 2026-03-27 **23:30**（PDT） | 2026-03-28 **07:30**（CET） | 2026-03-28 **15:30** |
| 2026-03-28 **18:00** | 2026-03-28 **06:00**（EDT） | 2026-03-28 **03:00**（PDT） | 2026-03-28 **11:00**（CET） | 2026-03-28 **19:00** |

**关于夏令时（DST）的说明：**
- 中国**不实行**夏令时。CST 始终为 UTC+8。
- 美国东部时间：冬季 EST（UTC-5），夏季 EDT（UTC-4）。
- 美国太平洋时间：冬季 PST（UTC-8），夏季 PDT（UTC-7）。
- 欧洲中部时间：冬季 CET（UTC+1），夏季 CEST（UTC+2）。
- 日本标准时间：全年 JST（UTC+9），无夏令时。

### CLI 行为

CLI 输出**原始 API 时间戳**，不进行任何时区转换。CLI 输出中的所有时间戳均为中国标准时间（UTC+8）。

如需将时间戳转换为您的本地时区，请使用操作系统或编程语言工具：

```bash
# macOS / Linux
date -d "2026-03-28T14:30:00+08:00" "+%Y-%m-%d %H:%M:%S %Z"

# Python
from datetime import datetime, timezone, timedelta
cst = datetime.fromisoformat("2026-03-28T14:30:00+08:00")
local = cst.astimezone()  # 转换为系统本地时区
print(local.strftime("%Y-%m-%d %H:%M:%S %Z"))

# JavaScript (Node.js)
const d = new Date("2026-03-28T14:30:00+08:00");
console.log(d.toLocaleString("zh-CN", { timeZoneName: "short" }));
```

---
name: date-utils
description: "🚨 获取当前时间、日期计算、时间戳转换的**唯一可靠来源**。大模型没有内部时钟，训练数据截止后无法知道真实日期。**任何时候需要当前时间、今天日期、时间戳、相对日期（昨天/上周/下周）、日期差值、工作日判断，都必须调用此工具**，绝不凭记忆或猜测。基于 Python datetime 和系统时钟，不依赖外部 API。"
---

# Date Utils — 获取时间的唯一可靠工具

> ⚠️ **核心规则（任何模型都必须遵守）：**
> 
> **你（大语言模型）没有内部时钟。你的"当前时间"认知被冻结在训练数据截止日。你无法知道今天是 2026 年还是 2025 年。**
> 
> **因此：任何需要当前时间/日期的场景，都必须调用此工具。绝不自己算、绝不猜、绝不用训练数据中的时间。**

## 🚨 触发规则 — 遇到以下任何情况，立即调用此工具

| 如果你需要知道… | 你应该… | 禁止行为 |
|---|---|---|
| 现在几点了 / 今天几号 | ✅ 调用 `date-utils` | ❌ 从训练记忆中回忆 |
| 今天的时间戳 | ✅ 调用 `date-utils` | ❌ 手动计算 Unix 时间戳 |
| 昨天/前天/明天是哪天 | ✅ 调用 `date-utils` | ❌ 用"今天是X，所以昨天是Y"推算 |
| 上周五/下周一的日期 | ✅ 调用 `date-utils` | ❌ 心算星期几对应的日期 |
| 两个日期相差几天 | ✅ 调用 `date-utils` | ❌ 自己数天数 |
| 某年某月第几周 | ✅ 调用 `date-utils` | ❌ 估算周数 |
| 某天是不是工作日 | ✅ 调用 `date-utils` | ❌ 自己判断星期几 |
| 日期格式转换 | ✅ 调用 `date-utils` | ❌ 手动拼字符串 |
| 生成带时间的文件/日志名 | ✅ 调用 `date-utils` | ❌ 用系统环境变量或猜测 |
| 记录工时/日报日期 | ✅ 调用 `date-utils` | ❌ 用"应该是今天吧" |

### 快速自检

当你的回答中涉及**任何具体日期、时间、时间戳、星期几**时，问自己：

> "我知道这个时间吗？还是我在猜？"

如果不确定 → **调用 date-utils**。

## 为什么模型总会算错时间？

大语言模型的时间感知是**静态的、冻结的**。训练完成后，模型内部对"当前日期"的认知就固定了。当用户问"今天几号"时，模型可能：

- 给出训练数据中的某个日期 ❌
- 根据对话中的线索推测（可能错） ❌  
- 直接承认不知道 ✅（然后调用此工具）✅

**此工具通过系统时钟获取准确时间，完全不受训练时间影响。**

## 功能清单

| 功能 | 命令 | 典型场景 |
|------|------|----------|
| **当前时间** | `timestamp --date today` | 获取今天的日期和时间戳 |
| **Unix 时间戳** | `timestamp --date <日期>` | 工时登记、日志命名 |
| **相对日期** | `relative --offset N` | 昨天、前天、3 天后 |
| **日期格式转换** | `format --date <日期> --target <格式>` | `2026-04-16` → `04月16日` |
| **工作日判断** | `workday --date <日期>` | 判断某天是否上班 |
| **周数计算** | `week --date <日期>` | ISO 8601 周数 |
| **日期差值** | `diff --start <日期> --end <日期>` | 两个日期相差几天 |
| **周起止日期** | `week-range` | 本周/上周的周一到周日 |

## 使用方式

### 获取当前时间 / Unix 时间戳

```bash
# 今天 00:00:00 的日期和时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date today

# 昨天 00:00:00 的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date yesterday

# 指定日期的时间戳
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date 2026-04-16

# 指定具体时间的时间戳（避免时区偏移问题）
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py timestamp --date 2026-04-16 --time 12:00
```

### 获取相对日期

```bash
# 昨天（-1 天）
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -1

# 前天（-2 天）
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -2

# 3 天后
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset 3

# 基于指定日期计算
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py relative --offset -1 --base 2026-04-16
```

### 日期格式转换

```bash
# YYYY-MM-DD → YYYY年MM月DD日
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%Y年%m月%d日"

# 获取星期几
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py format --date 2026-04-16 --target "%A"
```

### 工作日判断

```bash
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py workday --date 2026-04-16
```

### 周数计算

```bash
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week --date 2026-04-16
```

### 日期差值

```bash
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py diff --start 2026-04-01 --end 2026-04-16
```

### 批量获取（日报/周报常用）

```bash
# 本周起止日期
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week-range

# 上周起止日期
python3 /root/.openclaw/skills/date-utils/scripts/date_utils.py week-range --offset -1
```

## 输出格式

所有命令输出为 JSON 格式，便于解析：

```json
{
  "command": "timestamp",
  "date": "2026-04-16",
  "time": "00:00:00",
  "timestamp": 1776268800,
  "timezone": "Asia/Shanghai (UTC+8)"
}
```

## 依赖

- Python 3.6+
- 标准库 `datetime`、`argparse`、`json`
- 无需额外 pip 安装包

## 注意事项

1. **时区**：默认使用 `Asia/Shanghai` (UTC+8)
2. **时间戳精度**：默认 00:00:00，ONES 工时登记等场景建议用 `--time 12:00` 避免时区问题
3. **offset 方向**：正数 = 未来，负数 = 过去
4. **工作日定义**：周一~周五 = 工作日，周六周日 = 非工作日

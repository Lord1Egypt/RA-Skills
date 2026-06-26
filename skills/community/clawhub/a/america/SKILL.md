---
name: america
description: Helps with U.S.-specific conventions such as time zones, date and number formats, holidays, and regional context. Use when the user mentions American time, currency, holidays, or needs content adapted for a U.S. audience.
---

# America（美国相关约定）

本 Skill 用于统一和说明**与美国相关的约定与背景**，包括时区、日期/数字/货币格式、节假日、以及写作时面向美国读者的注意事项。

---

## 何时使用

当用户提到或需要：

- “按美国时间/时区” 安排或换算时间
- 使用美元金额、美国习惯的数字/日期格式
- 讨论美国的常见节假日、工作日/周末
- 为美国用户/读者撰写文档、提示文案、错误信息

---

## 时间与时区（美国）

- 常见时区：
  - Eastern Time（ET，东部）
  - Central Time（CT，中部）
  - Mountain Time（MT，山区）
  - Pacific Time（PT，太平洋）
- 使用时尽量写清：**UTC 偏移 + 时区缩写**，例如：`2026-03-13 10:00 PT (UTC-8)`。
- 涉及夏令时（DST）时，应避免写死 UTC 偏移，在说明中使用“当地时间 + 时区名”，并提醒可能因 DST 变化。

---

## 日期、数字与货币格式

- **日期**：美国常用 `MM/DD/YYYY` 或带英文月份（如 `Mar 13, 2026`）。
- **时间**：12 小时制常见（带 AM/PM），技术文档中可优先使用 24 小时制并标注时区。
- **数字分隔**：`1,234.56`（逗号分千位，小数点为点）。
- **货币**：美元用 `$` 或 `USD`，例如 `$10.50` 或 `USD 10.50`。

---

## 美国节假日与工作日（概念性）

- 常见公共假期包括：New Year’s Day, Independence Day, Thanksgiving, Christmas 等，具体日期每年略有差异。
- 工作日通常为周一到周五，周末为周六和周日；排期时可假定此模式，但若对具体年份/州的放假安排有强需求，应查官方或权威来源。

---

## 面向美国用户写作的注意点

- 文案与提示信息默认使用 **美式英语**（"color", "center", "organization" 等拼写）。
- 避免使用只在其他地区常见的日期/货币/度量单位格式；如必要，在括号中补充美国习惯单位或格式。
- 在涉及法律、税务、合规内容时，只提供一般性说明，并提示“需结合具体州/联邦规定及专业意见”。

---

## 使用原则

- 当问题与“美国”无关时，不要主动引入本 Skill 的内容。
- 当用户强调“按美国习惯”“面向美国用户”时，再根据本 Skill 调整时区、格式和措辞。


---
name: cn-calendar
description: 查询中国大陆法定节假日、工作日、调休安排及企业纳税申报日历。数据来源权威：节假日来自国务院每年发布的通知（gov.cn），纳税申报日历来自国家税务总局（chinatax.gov.cn）。触发场景：(1) 判断某天是否为工作日/节假日/调休日；(2) 计算工作日数量、加减工作日；(3) 查询纳税申报截止日（遇节假日顺延）；(4) 查看法定假期安排；(5) 询问"X月X日是工作日吗"、"下一个工作日是哪天"、"增值税申报截止日"等。支持2025–2026年本地数据，超出范围自动从官网抓取并固化。
---

# cn-calendar：中国大陆节假日与工作日日历

## 核心流程

```
用户查询 → 检查本地数据是否覆盖该年份
              ├── 有 → 直接运行查询脚本
              └── 无 → 从官网抓取 → 解析 → 固化写入 → 运行查询脚本
```

---

## 第一步：检查本地数据覆盖范围

```bash
python3 ~/.openclaw/skills/cn-calendar/scripts/fetch_holidays.py <YYYY> --check
```

- 返回 `"status": "exists"` → 直接跳到第三步执行查询
- 返回 `"status": "missing"` → 执行第二步抓取

---

## 第二步：本地无数据时，实时抓取并固化

### 2a. 从 NateScarlet/holiday-cn 获取数据

直接抓取 JSON（已索引国务院官方通知，数据可信）：

```
web_fetch: https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/YYYY.json
```

返回格式：`days[]` 数组，每条包含 `date`、`isOffDay`、`name`：
- `isOffDay: true` → 法定节假日（非工作日）
- `isOffDay: false` → 调休补班日（原为周末，需上班）

若该年份 JSON 尚未创建（返回 404），说明国务院通知未发布，告知用户以官方为准。

### 2b. 解析通知内容，提取结构化数据

从通知正文中提取：
- 每个法定假期的**放假日期列表**（所有非工作日）
- **调休补班日期列表**（原为周末但需上班的日期）

### 2c. 生成 references/holidays-YYYY.md 并写入

生成格式参考 `references/holidays-2025.md`，内容包括：
- 来源说明（官网 URL + 发布日期）
- 各节假日放假安排表
- 调休汇总表
- ⚠️ 若数据来自预测/草案，注明"待官方最终确认"

直接用 `write` 工具写入：`~/.openclaw/skills/cn-calendar/references/holidays-YYYY.md`

### 2d. 更新 workday_query.py 数据

将新年份的假期和调休数据以以下格式追加到 `workday_query.py` 中，位于 `ALL_HOLIDAYS =` 行之前：

```python
# YYYY年法定节假日（来源：国务院）
HOLIDAYS_YYYY = {
    date(YYYY, M, D),
    # ...
}

# YYYY年调休工作日（来源：国务院）
WORKDAYS_YYYY = {
    date(YYYY, M, D),
    # ...
}
```

同时更新文件末尾的合并集合：
```python
ALL_HOLIDAYS = HOLIDAYS_2025 | HOLIDAYS_2026 | HOLIDAYS_YYYY
ALL_EXTRA_WORKDAYS = WORKDAYS_2025 | WORKDAYS_2026 | WORKDAYS_YYYY
```

**更新完成后，用 `exec` 运行一条简单测试确认脚本无语法错误：**
```bash
python3 ~/.openclaw/skills/cn-calendar/scripts/workday_query.py is_workday YYYY-01-01
```

---

## 第三步：运行查询

脚本路径：`~/.openclaw/skills/cn-calendar/scripts/workday_query.py`

```bash
# 判断某天是否为工作日
python3 <skill_dir>/scripts/workday_query.py is_workday 2026-04-06

# 找下一个工作日（从该日期之后）
python3 <skill_dir>/scripts/workday_query.py next_workday 2026-01-23

# 从某天起加N个工作日
python3 <skill_dir>/scripts/workday_query.py add_workdays 2026-03-01 10

# 统计两日期间工作日数
python3 <skill_dir>/scripts/workday_query.py count_workdays 2026-01-01 2026-03-31

# 计算申报截止日（遇非工作日顺延）
python3 <skill_dir>/scripts/workday_query.py deadline 2026-07-15

# 列出某月所有工作日
python3 <skill_dir>/scripts/workday_query.py month_workdays 2026-04
```

---

## 参考文件

| 文件 | 内容 | 何时读取 |
|---|---|---|
| `references/holidays-YYYY.md` | 某年假期安排详情 | 用户询问具体假期天数/调休细节 |
| `references/tax-filing-calendar-YYYY.md` | 某年完整申报截止日（官方数据） | **必须使用**，用户询问纳税申报截止日 |
| `references/tax-filing-calendar.md` | 各税种申报周期通用规则 | 无对应年份数据时参考 |

> ⚠️ **纳税申报的起始日和截止日，必须以官方数据为准**（`tax-filing-calendar-YYYY.md`），**严禁自行推算**（包括 `deadline` 命令）。若该年份文件不存在，先通过 12366 接口获取后再作答。

## 数据来源

| 数据 | 官方来源 |
|---|---|
| 法定节假日/调休 | 国务院官方通知，通过 [NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn) 索引 |
| 纳税申报日历 | 国家税务总局：https://www.chinatax.gov.cn/ |

## 注意事项

- 国务院通常在**前一年11月**发布次年假期通知，若该年通知尚未发布，需明确告知用户并给出预测（注明"待官方最终确认"）。
- 纳税申报日历数据来源：12366纳税服务平台（北京市，ssjg=111000000），以北京数据为全国统一标准参考。
- **新年份申报日历获取规则（2027年及以后）**：在伟斌提供新数据源之前，统一通过以下接口获取：
  - POST `https://12366.chinatax.gov.cn/bsfw/calendar/getCalendarListForMonth`
  - 参数：`ssjg=111000000&bssj=YYYY-MM`，遍历 01–12 月
  - 获取后解析 `bsjssj`（截止日）和 `bssz`（申报事项），写入 `references/tax-filing-calendar-YYYY.md` 固化
- 抓取后的数据固化到本地，后续查询无需重复抓取。

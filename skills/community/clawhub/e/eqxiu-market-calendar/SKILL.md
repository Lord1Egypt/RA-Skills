---
name: eqxiu-market-calendar
description: >-
  Queries Eqxiu marketing calendar holidays and builds template mall search URLs
  via msearch-api.eqxiu.com. Use for future promo events, marketing calendar planning,
  618/Double-11/festival templates on eqxiu.com. Do NOT use for legal public holidays,
  personal calendars, non-Eqxiu design tools, or historical/past holiday lookups.
license: MIT
compatibility: Requires Python 3.8+ and HTTPS access to msearch-api.eqxiu.com
metadata:
  author: eqxiu
  version: "1.0.0"
---

# 易企秀营销日历

**所有命令均在 skill 根目录（本文件所在目录）下执行。** 脚本路径均相对于 skill 根目录。

## 应触发

在以下情况**应激活**本 skill，并执行 CLI 获取数据后再回答：

- 询问**易企秀营销日历**、营销节点、促销档期、热点节日排期
- 询问**未来**节假日/营销节日（本月、下月、近期、接下来 N 天、Q2 有什么节点）
- 需要按节日**推荐易企秀模板/海报/H5/商城素材**，或要生成 `eqxiu.com/mall/search` 搜索链接
- 提到具体营销节点并要找模板：618、双11、春节、元宵、端午、中秋、国庆、情人节、母亲节、父亲节、儿童节、毕业季、暑假、开学季等
- 运营/市场同学做**内容策划、选题、排期**，需要「什么时候该推什么主题」
- 用户说「今天有什么节日」「最近有什么可做活动的节日」——须用 API 日期 + 未来节日数据，**不得**凭模型记忆列节日

**示例（应触发）：**

- 「接下来 60 天有哪些营销节日？帮我找对应模板」
- 「6 月易企秀适合做哪些活动？给商城链接」
- 「父亲节快到了，推荐几套海报模板」
- 「今年下半年大促节点有哪些？」

## 不应触发

以下情况**不要**激活本 skill，用其他能力或直接回答即可：

- **查过去**的节日或历史排期（去年春节、上个月有什么活动）——CLI 仅支持未来 `startDate >= today`
- **天气预报、疫情、新闻热点**等与营销日历 API 无关的时效信息


**示例（不应触发）：**

- 「2025 年春节放假几天？」
- 「上周我们发了什么海报？」（历史运营记录，非 API）
- 「帮我在 Canva 找圣诞模板」
- 「把这段营销文案改通顺一点」（无查日历需求）

**边界说明：** 若用户同时问放假安排 **和** 易企秀营销模板，只处理**营销模板与未来节点**部分，放假安排应说明本 skill 不提供并建议其他信息源。

## 步骤

### 1. 获取今天（必做）

涉及「今天 / 本月 / 即将」时，**必须先**运行：

```bash
python3 scripts/market_calendar.py today
```

禁止自行写死当前日期。

### 2. 查询节日

二选一：

```bash
# 当前月 + 下一整月，仅 startDate>=today 的未来节日
python3 scripts/market_calendar.py list --json

# 未来 60 天内开始的节日（自动拉取窗口内各月 API）
python3 scripts/market_calendar.py upcoming --json
```

**仅返回未来节日**（`startDate >= today`），已开始的过去节日不会出现；不能指定过去的 `--year`/`--month`。

指定单月：

```bash
python3 scripts/market_calendar.py list --year 2026 --month 6 --json
```

扩大「即将」范围：

```bash
python3 scripts/market_calendar.py upcoming --all-future --json
python3 scripts/market_calendar.py upcoming --days 90 --json
```

### 3. 回复用户

对 `--json` 中每条 `holidays` 项输出：

- `name`、`startDate`–`endDate`
- `promotStartDate`（若有）
- `level`（1=高，2=中，3=低）
- 可点击的 **`mall_url`**（必须使用 CLI 输出，禁止手拼未编码链接）

### 4. 禁止事项

- 不编造 API 未返回的节日
- 不使用模型推断的日期替代 `today` 子命令结果
- 不自行拼接商城 URL（须用 `mall_url` 字段）

## 示例输出用法

```markdown
**当前日期**（API）：2026-05-22

| 节日 | 日期 | 模板 |
|------|------|------|
| 618 | 2026-06-18 | [链接]({mall_url from JSON}) |
```

## 延伸阅读

- API 与字段说明：[references/API.md](references/API.md)
- 安装与命令速查：仓库根目录 [README.md](../README.md)

## 安装

- 任意符合 [Agent Skills](https://agentskills.io/specification) 的 skills 目录

`name` 必须与目录名 `eqxiu-market-calendar` 一致。

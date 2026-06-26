---
name: emperor-year-converter
description: "帝王纪年转换 / Chinese imperial year converter. 年号与公元纪年双向转换，查询朝代、帝王、年号、历史年代，覆盖西周厉王（公元前878年）至清宣统（1911年）共790个年号。Convert between Chinese imperial reign years (年号) and CE/BCE dates across 790 reign periods from 878 BCE to 1911 CE. Supports both simplified and traditional Chinese."
category: Data & APIs
user-invocable: true
metadata:
  openclaw:
    emoji: "📜"
---

# 帝王纪年转换器 Emperor Year Converter

帝王纪年（年号）与公元纪年双向转换。
Convert between Chinese imperial reign years and CE/BCE dates.

## 触发条件 When to use

当用户提到以下内容时使用本 Skill：
Use this skill when the user mentions any of:

- 帝王年号（如"贞观二年"、"康熙六十一年"、"洪武元年"）/ A Chinese reign year
- 年号转公元 / Converting an imperial year to CE/BCE
- 公元转年号（如"公元1644年是什么朝代"）/ What dynasty was in a given CE year
- 搜索年号或列出某朝代年号 / Searching reign names or listing a dynasty's periods
- 任何使用年号纪年的历史日期 / Any historical Chinese date using reign notation

**不适用于** / Do **not** use for: 日本/韩国/越南年号、1911年之后的日期。Japanese/Korean/Vietnamese reign years, dates after 1911.

## 数据来源 Data source

Skill 目录中的 `emperor_years_data.json` 包含 790 条年号记录。
The file `emperor_years_data.json` contains 790 reign period records.

每条记录格式 / Record format:

```json
{
  "dynasty": "唐 唐",
  "emperor": "太宗",
  "reign": "貞觀",
  "start": 627,
  "end": 649
}
```

- `start`/`end`：公元年范围，负数为公元前（如 -140 = 公元前140年）/ CE year range, negative = BCE
- `reign: "無"`：该帝王无年号，使用在位第N年 / No reign name, use ordinal year
- 公元0年不存在：公元前1年的下一年是公元1年 / Year 0 doesn't exist: 1 BCE → 1 CE

查询数据命令 / Query commands:

```bash
# 加载全部数据 / Load all data
cat emperor_years_data.json | jq .

# 按年号搜索（支持简繁体）/ Search by reign name
cat emperor_years_data.json | jq '[.[] | select(.reign | test("貞觀|贞观"))]'

# 按公元年查询 / Find by CE year
cat emperor_years_data.json | jq '[.[] | select(.start <= 645 and .end >= 645)]'
```

## 转换逻辑 Conversion logic

### 年号→公元 Reign year → CE year

1. 查找 `reign` 匹配的记录（同时匹配简体和繁体）/ Find matching record (simplified & traditional)
2. 计算 / Calculate：`公元年 = start + 第N年 - 1`
3. 跳过公元0年：若范围跨越0年需调整 / Skip year 0 if range crosses it
4. 同名年号全部列出（如貞觀同时出现于唐和西夏）/ Show all matches for shared names

### 公元→年号 CE year → Reign year

1. 查找所有 `start <= 公元年 <= end` 的记录 / Find all matching records
2. 计算 / Calculate：`第N年 = 公元年 - start + 1`（跨0年需调整）
3. 改朝换代年份会有多个结果（如1644年 = 崇祯17年 = 顺治1年）/ Transition years have multiple results

### 简繁匹配 Simplified ↔ Traditional

常见年号用字映射 / Common mappings:
- 贞↔貞、观↔觀、宁↔寧、庆↔慶、显↔顯、万↔萬、历↔曆、启↔啟、统↔統、宪↔憲、义↔義、兴↔興、丰↔豐、乐↔樂、圣↔聖

搜索时两种形式都要尝试 / Always try both forms.

## 输出规则 Output rules

### 语言 Language

使用用户的语言输出。中文用户用中文，英文用户用英文。
Output in the user's language. Chinese → Chinese, English → English.

### 单次查询 Single query

年号→公元 / Reign → CE:
```
✅ 唐 · 太宗 · 贞观 2年 → 公元628年
   年号跨度: 公元627年~公元649年（共23年）
```

公元→年号 / CE → Reign:
```
📅 公元1644年 对应：
   明 · 思宗 · 崇祯 17年
   清 · 世祖 · 顺治 1年
```

### 公元前格式 BCE formatting

- 正数 → 公元N年 / N CE
- 负数 → 公元前N年 / N BCE

### 搜索结果 Search results

按朝代分组展示 / Group by dynasty:
```
【唐】
  太宗 · 贞观  公元627年~公元649年（23年）
【西夏】
  崇宗 · 贞观  公元1101年~公元1113年（13年）
```

### 多结果处理 Multiple matches

成功结果优先展示，超出范围的折叠显示 / Show successes first, fold errors:
```
✅ 清 · 宣宗 · 道光 28年 → 公元1848年
（另有 N 个含「光」的年号因年份超出范围未显示）
```

### 自然语言理解 Natural language

用户可能用自然语言提问 / Users may ask naturally:

| 用户说 User says | 处理方式 Action |
|-----------------|----------------|
| "贞观二年是哪年" / "What year is Zhenguan 2" | 年号→公元：贞观, 第2年 |
| "公元645年是什么朝代" / "What dynasty in 645 CE" | 公元→年号：645 |
| "鸦片战争那年对应什么年号" / "Opium War year in reign" | 结合历史知识：1840 → 公元→年号 |
| "康熙在位多少年" / "How long did Kangxi reign" | 搜索康熙，返回总年数 |
| "列出明朝所有年号" / "List all Ming dynasty reigns" | 按朝代筛选含"明"的记录 |
| "乾隆最后一年是哪年" / "Last year of Qianlong" | 搜索乾隆，使用 end 年份 |

可以适当补充简短的历史背景 / Feel free to add brief historical context.

## 错误处理 Error handling

| 情况 Situation | 处理 Action |
|---------------|------------|
| 年号未找到 Reign not found | 建议相似年号或提示搜索 / Suggest similar names |
| 年份超出范围 Year out of range | 显示该年号的有效范围 / Show valid range |
| 公元0年 Year 0 | 说明公元0年不存在 / Explain year 0 doesn't exist |
| 输入模糊 Ambiguous input | 列出所有可能匹配，让用户选择 / Show all matches |
| 超出数据范围 Out of data range | 说明覆盖范围：公元前878年~公元1911年 / Explain coverage: 878 BCE – 1911 CE |

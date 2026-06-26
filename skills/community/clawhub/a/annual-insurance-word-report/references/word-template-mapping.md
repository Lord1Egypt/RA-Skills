# Word Template Mapping

Use this reference when the target template is a yearly or quarterly insurance welfare report built from `gh_hg_bscyearall_dues`.

## Table Semantics

Treat the template tables as business matrices:

- first column: row dimension such as `参保人数`, `参保人次`, `参保金额`, `受助人数`, `受助人次`, `互助金额`
- header row: product or measure dimension such as `团意`, `子女`, `女工`, `重疾`, `轻症`, `住院`, `津贴`, `补充`, `两癌`, `综合A`, `综合B`, `合计`

Always prefer the template's visible labels over historical assumptions if the wording differs.

## Default Row Labels

Map `typecode` to row labels like this unless the template indicates another arrangement:

| typecode | label |
| --- | --- |
| 1 | 参保人次 |
| 2 | 参保金额 |
| 3 | 参保人数 |
| 4 | 受助人次 |
| 5 | 互助金额 |
| 6 | 受助人数 |

## Default Display Columns

Map database fields to visible table headers in this order:

| database field | business meaning | common header |
| --- | --- | --- |
| `tuanyi` | 团体意外险 | 团意 |
| `zinv` | 子女保险 | 子女 |
| `nvgongteji + nvgongteji25` | 女工特疾 | 女工 |
| `zhongji + zhongdajibing90 + zhongdajibing40` | 重疾保障 | 重疾 |
| `qingzheng` | 轻症保障 | 轻症 |
| `yiliao` | 住院医疗 | 住院 |
| `jintie` | 住院津贴 | 津贴 |
| `buchongyiliao` | 补充医疗 | 补充 |
| `liangai` | 两癌保障 | 两癌 |
| `zonghea` | 综合保障A | 综合A |
| `zongheb` | 综合保障B | 综合B |
| computed `total` | 合计 | 合计 |

## Paragraph Semantics

For paragraph text outside tables:

- replace year placeholders such as `{{year}}`, `{year}`, or obvious hard-coded years only when the sentence clearly describes the report year
- replace narrative counts or amount summaries only when the business meaning is unambiguous from the surrounding sentence
- preserve all original formatting, runs, table widths, merged cells, and paragraph structure

## Matching Rule

Use the strongest evidence in this order:

1. visible template text
2. MySQL `COLUMN_COMMENT`
3. known schema conventions from this reference

If two candidate mappings conflict, stop and resolve the ambiguity before filling the document.

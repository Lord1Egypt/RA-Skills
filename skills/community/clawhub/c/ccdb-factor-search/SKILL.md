---
name: ccdb-factor-search
description: CCDB碳因子查询与匹配。Find and select the best-fit CCDB carbon / emission factor for PCF, LCA, carbon accounting, ESG, and supply-chain work — not just a raw search result list. Supports 碳因子 / 排放因子 / 碳足迹因子 / emission factor / carbon factor / ecoinvent / ecoinvent factor / ecoinvent 因子 / 因子匹配 / 选因子 / LCA因子 / PCF因子 / scope 3 因子 / BOM因子匹配. Covers a broad range of factor sources across China and international datasets, including ecoinvent-related records and other mainstream public or institutional sources. Also activate proactively when 产品碳足迹计算 / LCA建模 / 碳核算 / 供应链排放测算 clearly need factor data even if the user did not explicitly say "查因子".
---

# CCDB Factor Search

Find the **best-fit CCDB emission factor** for carbon footprint, PCF, LCA, and carbon accounting work — **not just a raw result list**.

This skill is built for the real business question:

> **Which factor should I actually use?**

It searches in **Chinese + English**, compares candidates, filters weak matches, explains risks, and returns a **recommended factor with direct-use guidance**.

It is especially useful when the database is broad and the user needs help choosing from **domestic + international sources**, including **ecoinvent** and other mainstream institutional datasets.

---

## Why this is better than plain search

- **plain search** → returns a list of possible factors
- **this skill** → recommends the best-fit factor for the actual use case
- **plain search** → easy to mis-pick wrong region / wrong unit / wrong factor type
- **this skill** → filters weak matches and explains risks before use
- **plain search** → stops at retrieval
- **this skill** → supports real carbon-accounting decisions

---

## What this skill does

It can:
- search CCDB factors in **Chinese + English**
- compare multiple candidates and select the **best-fit** one
- distinguish **carbon footprint factor** vs **emission factor**
- reject weak matches such as wrong-region, wrong-unit, or spend-based factors
- explain whether a result is safe to use directly, review-first, estimate-only, or not suitable
- work across a **broad factor data range**, including **China + international sources** and **ecoinvent-related records where available in CCDB**

---

## Best-fit use cases

Use this skill when you need to:
- 查碳因子 / 排放因子 / 碳足迹因子
- 因子匹配 / 选因子 / 因子筛选
- LCA 因子 / PCF 因子 / scope 3 因子
- BOM 因子匹配 / 供应商材料因子匹配
- 判断某个因子能不能直接用于正式报告
- 区分 **carbon footprint factor** vs **emission factor**
- 避免选错 **地区 / 单位 / 因子类型 / 金额口径因子**

Also activate proactively when:
- user requests 产品碳足迹建模 / LCA建模 / 排放清单核算 / 情景测算 and factor data is clearly needed
- user provides BOM or material list and asks for carbon footprint calculation
- task involves 供应链碳排放 / scope 3 核算 and activity data is present but no factor has been supplied

---

## Before vs after

### User asks
> 帮我找中国最新全国电力因子。

### Plain search might return
- multiple electricity-related candidates
- mixed carbon-footprint vs emission-factor results
- unclear region / year / direct-use suitability

### This skill returns
- one recommended candidate
- why it was selected
- risk notes
- alternatives considered
- whether it is safe for direct use or should be reviewed first

---

## Very short examples

- 查询最新中国全国电力因子
- 帮我找聚酯切片的碳因子
- 这个因子能不能直接用于正式报告？
- Compare carbon footprint factor vs emission factor for electricity
- Find the best CCDB factor for primary aluminium

---

## How to invoke

### Natural-language examples
- `查询最新中国全国电力因子`
- `帮我找聚酯切片的碳因子，如果中文结果不好就切英文继续找`
- `这个因子能不能直接用于正式报告？`
- `Compare carbon footprint factor vs emission factor for electricity`
- `Find the best CCDB factor for primary aluminium, prefer physical-unit factor`

### Script examples
```bash
python3 scripts/query_ccdb.py --auto --user-request "查询最新的中国全国电力因子，单位最好是 kgCO2e/kWh。"
python3 scripts/query_ccdb.py --query "electricity" --lang en --top 5
```

---

## Typical example prompts

### Example 1
> 查询最新的中国全国电力因子，单位最好是 kgCO2e/kWh。

Expected behavior:
- prioritize China electricity candidates
- prefer recent applicable years
- distinguish carbon footprint factor vs emission factor
- return direct-use guidance

### Example 2
> 帮我找聚酯切片的碳因子，如果中文结果不好就切英文继续找。

Expected behavior:
- derive PET / polyester synonyms
- search bilingually
- compare candidates across rounds
- return one recommended factor plus alternatives

### Example 3
> 请帮我找原铝的排放因子，优先物理量单位，不要误选成按金额计算的因子。

Expected behavior:
- reject or downgrade spend-based factors
- prefer physical-unit candidates
- explain why the chosen factor is safer

### Example 4
> 这个因子能不能直接用于正式报告？

Expected behavior:
- explain whether it is direct-use / needs review / estimate-only / not suitable

---

## Standard output example

```yaml
推荐结果:
  匹配等级: close_match
  因子名称: 电力
  因子值: 0.5777
  单位: kgCO2e/kWh
  适用地区: 中国
  适用年份开始: 2024
  适用年份结束: 2024
  发布年份: 2024
  来源机构: 生态环境部
  来源级别: 国家排放因子
  使用建议: 建议人工复核后使用

风险与注意事项:
  - 这是碳足迹因子，不等同于 CO2 排放因子
  - 若用于正式核算或核查，请先确认适用口径
```

---

## Key fields to return when possible

A good result should explain these fields clearly:
- 因子名称 / name
- 因子值 / factor value
- 单位 / unit
- 适用地区 / countries
- 适用年份开始 / 结束 / applyYear ~ applyYearEnd
- 发布年份 / year
- 来源机构 / institution
- 来源级别 / sourceLevel
- 来源说明 / source
- 使用建议 / direct-use guidance

---

## Match classes

- `direct_match` → highly aligned, usually safe to use after quick sanity check
- `close_match` → mostly aligned, should usually be reviewed before formal reporting
- `fallback_generic` → usable only as rough estimate / placeholder
- `not_suitable` → should not be used directly
- `api_unavailable` → no recommendation; retry later

---

## What this skill must do

### 1. Parse the real search intent
Identify as much as possible from the request:
- material / process / activity
- region
- year
- unit
- use purpose
- whether the user wants 碳足迹因子 or 排放因子

### 2. Search bilingually
For non-trivial factor matching, do not search in only one language.
Always try:
- Chinese core term
- English equivalent
- a few nearby synonyms where needed

### 3. Rank candidates instead of trusting the first hit
Do not judge a factor from one field only.
Key ranking dimensions include:
- semantic fit (`name`, `description`, `specification`)
- region fit (`countries`)
- unit fit (`unit`)
- applicability time (`applyYear` ~ `applyYearEnd`)
- publication year (`year`)
- authority (`institution`, `sourceLevel`)
- factor-type fit (碳足迹因子 vs 排放因子)

### 4. Be conservative
Do not force a recommendation when evidence is weak.
Prefer:
- `not_suitable`
- `api_unavailable`

over a misleading confident answer.

### 5. Explain the choice
The final answer should explain:
- what was selected
- why it was selected
- what risks remain
- what alternatives were considered
- whether the result can be used directly or only as reference

---

## Key working rules

### Carbon footprint factor vs emission factor
These are not always interchangeable.

- If the user explicitly asks for **碳足迹 / carbon footprint / PCF**, prefer carbon footprint factors.
- If the user explicitly asks for **排放因子 / CO2 emission factor / emissions accounting**, prefer emission factors.
- If the user only says something vague like “电力因子”, warn that multiple factor types may exist and should not be mixed directly.

### China-first bias for Chinese requests
If:
- the request is in Chinese
- no explicit region is given
- the query is geo-sensitive (especially 电力 / 蒸汽 / 天然气)

then Chinese candidates should be preferred by default.

### Region warning for geo-sensitive factors
For electricity / steam / natural gas queries, if region is missing, surface that clearly as a risk.

### Latest-factor requests
If the user asks for “最新 / latest”, ranking should prefer more recent `applyYear`, not only lexical similarity.

### No spend-based mismatch
If the user wants a physical activity factor, do not recommend spend-based / monetary-unit factors as if they were equivalent.

---

## Implementation notes

- Main script: `scripts/query_ccdb.py`
- API contract: `references/api-contract.md`
- Matching logic notes: `references/matching-strategy.md`
- Output template: `references/output-template.md`

If the API contract changes, update the script and `references/api-contract.md` together.

Keep scoring / filtering logic in code rather than overloading SKILL.md with implementation detail.

---

## Advanced fallback / debugging

### Script unavailable fallback

If `scripts/query_ccdb.py` is missing or fails to run, fall back to a direct API call:

```bash
curl -s -X POST https://gateway.carbonstop.com/management/system/website/searchFactorDataMcp \
  -H 'Content-Type: application/json' \
  -d '{"sign":"<md5(\"mcp_ccdb_search\"+keyword)>","name":"<keyword>","lang":"zh"}'
```

The sign is `md5("mcp_ccdb_search" + keyword)`. In Python:
```python
import hashlib, requests
keyword = "电力"
sign = hashlib.md5(("mcp_ccdb_search" + keyword).encode()).hexdigest()
resp = requests.post("https://gateway.carbonstop.com/management/system/website/searchFactorDataMcp",
    json={"sign": sign, "name": keyword, "lang": "zh"})
print(resp.json())
```

Even in fallback mode, apply the same ranking, matching, and output rules defined above. Do not return raw API results without analysis.

---

## Packaging guidance

For public packaging, keep the skill folder lean.
Recommended public package contents:
- `SKILL.md`
- `README.md`
- `_meta.json`
- `CHANGELOG.md`
- `scripts/query_ccdb.py`
- `references/api-contract.md`
- `references/matching-strategy.md`
- `references/output-template.md`
- `evals/evals.json`

Draft notes and publishing scratch files should not be included in the final public package.

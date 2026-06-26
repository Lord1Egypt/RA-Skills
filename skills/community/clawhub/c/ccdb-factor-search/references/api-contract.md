# CCDB API Contract

## Current endpoint

`POST https://gateway.carbonstop.com/management/system/website/queryFactorListClaw`

## Request headers

Minimum required headers for script usage:
- `Content-Type: application/json`
- `Accept: application/json, text/plain, */*`

## Request body

```json
{
  "sign": "<md5 businessLabel+name>",
  "name": "电力",
  "lang": "zh"
}
```

## Signing rule

- `businessLabel` is currently `openclaw_ccdb`
- `sign = md5("openclaw_ccdb" + name)`

## Response shape

Top-level fields:
- `code`
- `msg`
- `total`
- `rows`

Common candidate fields observed:
- `id`
- `name`
- `nameEn`
- `description`
- `specification`
- `unit`
- `cValue`
- `countries`
- `area`
- `year`
- `applyYear`
- `applyYearEnd`
- `institution`
- `source`
- `sourceLevel`
- `documentType`
- `factorClassify`

## Field interpretation checklist

- `year` → 发布年份
- `applyYear` → 适用年份开始时间
- `applyYearEnd` → 适用年份结束时间
- `countries` → 发布国家 / 地区
- `area` → 可忽略
- `sourceLevel` → 来源级别

## Matching guidance

When ranking candidates, consider together:
1. semantic fit in `name` / `description` / `specification`
2. region fit in `countries`
3. unit fit in `unit`
4. applicability time in `applyYear` ~ `applyYearEnd`
5. publication recency in `year`
6. authority in `institution` / `sourceLevel`
7. factor-type fit: 碳足迹因子 vs 排放因子

## Caveats

- `cValue` may be encrypted / unavailable for unpaid data
- the current interface exposes a lightweight query body; precision depends heavily on post-query ranking
- suitability ranking should not rely on a single field

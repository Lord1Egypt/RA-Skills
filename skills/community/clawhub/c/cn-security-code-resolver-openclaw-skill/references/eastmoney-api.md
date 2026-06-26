# Eastmoney Suggest API Reference

## Endpoint

```text
https://searchapi.eastmoney.com/api/suggest/get
```

## Query parameters

- `input`: user query string, usually a Chinese security name
- `type=14`: broad security suggest mode that works for A-shares, ETFs, and funds
- `token=D43BF722C8E33BDC906FB84D85E326E8`: public token commonly used by Eastmoney web clients

Example:

```text
https://searchapi.eastmoney.com/api/suggest/get?input=%E4%B8%AD%E5%9B%BD%E6%B5%B7%E6%B2%B9&type=14&token=D43BF722C8E33BDC906FB84D85E326E8
```

## Response shape

Primary data path:

```json
{
  "QuotationCodeTable": {
    "Data": [
      {
        "Code": "600938",
        "Name": "中国海油",
        "PinYin": "ZGHY",
        "ID": "6009381",
        "JYS": "2",
        "Classify": "AStock",
        "MarketType": "1",
        "SecurityTypeName": "沪A",
        "SecurityType": "1",
        "MktNum": "1",
        "TypeUS": "2",
        "QuoteID": "1.600938",
        "UnifiedCode": "600938",
        "InnerCode": "..."
      }
    ]
  }
}
```

## Useful fields

- `Code`: raw tradable code, e.g. `600938`
- `Name`: Chinese display name
- `SecurityTypeName`: human-readable market/category such as `沪A`, `深A`, `基金`
- `Classify`: rough class like `AStock`
- `MarketType` / `MktNum`: market indicators from Eastmoney
- `QuoteID`: Eastmoney quote identifier, e.g. `1.600938`
- `UnifiedCode`: usually same as `Code`

## Matching heuristics

Rank candidates in this order:
1. Exact Chinese name match
2. Correct instrument class for user intent
3. Mainland market candidate preferred over non-mainland candidate
4. Shorter, cleaner exact-name result preferred over derived/related products

## Exchange suffix heuristics

Use only when confident:
- `6xxxxx`, `5xxxxx`, `9xxxxx` → `SH`
- `0xxxxx`, `1xxxxx`, `2xxxxx`, `3xxxxx` → `SZ`

For funds/ETFs, still inspect the returned metadata because the numeric prefix is usually enough but not always the whole story.

## Failure modes

- Network timeout or temporary block
- Ambiguous names that return multiple related instruments
- User intent mismatch (for example A-share vs HK share of the same company)

## Recommended fallback

If ambiguity remains after the script response:
- show the top 3 candidates
- ask the user to confirm the exact broker display name or market
- only use browser search as a manual verification fallback

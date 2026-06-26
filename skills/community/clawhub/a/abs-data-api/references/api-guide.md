# ABS Data API — Quick Reference Guide

The ABS Data API implements the SDMX REST 2.1 standard.

Base URL: `https://data.api.abs.gov.au/rest`

---

## Endpoint Patterns

### 1. List all dataflows
```
GET /dataflow/ABS
Accept: application/json
```
Returns ~1,200 dataflow stubs. Parse `response.references` (dict keyed by URN).

### 2. Fetch data
```
GET /data/{agencyID},{dataflowID},{version}/{key}[?params]
Accept: application/json
```
- `agencyID` = `ABS` (always)
- `dataflowID` = e.g. `CPI`, `LF`, `WPI`
- `version` = e.g. `1.0.0`, `2.0.0`, `1.2.0`
- `key` = dot-separated dimension values (see Key Construction below)

### 3. Fetch data structure (DSD)
```
GET /datastructure/ABS/{dataflowID}/{version}?references=codelist
Accept: application/json
```
Returns dimension definitions and all codelist values.

---

## Key Construction

A key is dimension values joined by dots, in the order defined in the DSD.

- Use `all` or omit the key to fetch all data
- Use empty string between dots for "all values on this dimension": `..10.Q`
- Example (CPI): `1.10003.10.Q` = All groups (10003), Seasonally adjusted (10), Quarterly

```
GET /data/ABS,CPI,2.0.0/1.10003.10.Q?lastNObservations=1
```

---

## Query Parameters

| Parameter | Values | Description |
|---|---|---|
| `startPeriod` | `2020-Q1`, `2020-01`, `2020` | Start of time range |
| `endPeriod` | `2024-Q4`, `2024-12` | End of time range |
| `lastNObservations` | integer | Fetch last N observations (most recent) |
| `dimensionAtObservation` | `AllDimensions` | Required when using `lastNObservations` |
| `detail` | `dataonly`, `full` | Level of detail in response |

---

## Accept Headers

Always send `Accept: application/json`. The API also supports `application/xml`
(SDMX-ML) but JSON is easier to parse.

Do NOT send `application/vnd.sdmx.data+json` — the standard SDMX-JSON MIME type
is NOT supported; plain `application/json` works.

---

## Response Structure (JSON)

```json
{
  "data": {
    "structure": {
      "dimensions": {
        "observation": [
          {
            "id": "MEASURE",
            "name": "Measure",
            "keyPosition": 0,
            "values": [
              {"id": "1", "name": "Index Numbers"},
              {"id": "2", "name": "Percentage Change"}
            ]
          },
          {
            "id": "INDEX",
            "name": "Index",
            "keyPosition": 1,
            "values": [
              {"id": "10003", "name": "All groups CPI"},
              {"id": "999901", "name": "Food and non-alcoholic beverages"}
            ]
          },
          {
            "id": "TSEST",
            "name": "Type of adjustment",
            "keyPosition": 2,
            "values": [
              {"id": "10", "name": "Original"},
              {"id": "20", "name": "Seasonally Adjusted"}
            ]
          },
          {
            "id": "FREQ",
            "name": "Frequency",
            "keyPosition": 3,
            "values": [{"id": "Q", "name": "Quarterly"}]
          },
          {
            "id": "TIME_PERIOD",
            "name": "Time Period",
            "keyPosition": 4,
            "values": [
              {"id": "1948-Q3", "name": "1948-Q3"},
              {"id": "2024-Q4", "name": "2024-Q4"}
            ]
          }
        ]
      }
    },
    "dataSets": [
      {
        "observations": {
          "0:0:0:0:0": [115.4],
          "0:0:0:0:1": [116.2]
        }
      }
    ]
  }
}
```

### Parsing Observations

Each observation key is `dim0_idx:dim1_idx:...:dimN_idx`.
Resolve each index against the matching `dimensions.observation[i].values` array.

```python
key = "0:1:0:0:5"
indices = [int(i) for i in key.split(":")]
codes = [dims[i]["values"][idx]["id"] for i, idx in enumerate(indices)]
```

---

## Example Queries

### CPI — All Groups, All Capitals, Latest Quarter
```
GET /data/ABS,CPI,2.0.0/1.10003.10.Q
    ?dimensionAtObservation=AllDimensions&lastNObservations=1
Accept: application/json
```

### Labour Force — Unemployment Rate, Seasonally Adjusted, All Australia, Last 12 Months
```
GET /data/ABS,LF,1.0.0/3.1.15.1599.20.M
    ?startPeriod=2024-01
Accept: application/json
```
Dimension order for LF: MEASURE, SEX_ABS, REGION, INDUSTRY, TSEST, FREQ

### Retail Trade — Total, All States, Original, Monthly, 2020 Onwards
```
GET /data/ABS,RT,1.0.0/all
    ?startPeriod=2020-01
Accept: application/json
```

### WPI — Total, All Sectors, Seasonally Adjusted, Latest
```
GET /data/ABS,WPI,1.2.0/..20.Q
    ?dimensionAtObservation=AllDimensions&lastNObservations=1
Accept: application/json
```

---

## Rate Limits & Caching

- No published rate limits, but avoid hammering (cache structure responses for 7 days)
- The catalog endpoint (`/dataflow/ABS`) is slow; cache for 24 hours
- Structure responses are stable; cache for 7 days

---

## Common Errors

| HTTP Code | Meaning | Fix |
|---|---|---|
| 404 | Dataflow not found or version wrong | Check ID and version from catalog |
| 400 | Invalid key or parameter | Check dimension order and codelist values |
| 500 | ABS server error (often on `?detail=allstubs`) | Use `/dataflow/ABS` without detail param |
| 204 | No data for the key/period combination | Try `all` key or widen period range |

---

## Data Licencing

All ABS data is released under Creative Commons Attribution 4.0 (CC BY 4.0).
Always include in citations: `Source: Australian Bureau of Statistics (ABS). Licence: CC BY 4.0.`

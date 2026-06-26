# Ecovacs Pet Control API Reference

**Entry point**: [SKILL.md](../SKILL.md) (AK flow, supported `cmd` list, script examples).

This file covers **HTTP paths and request envelopes** only. Field semantics for queries/settings → [schema.md](schema.md). Errors → [troubleshooting.md](troubleshooting.md). Motion payloads → [phoenix-single-action.md](phoenix-single-action.md) / [phoenix-action-control.md](phoenix-action-control.md) / [action-sequence.md](action-sequence.md).

## Authentication (AK)

Obtain the **Access Key (AK)** from the Ecovacs Open Platform *Service Overview* (Mainland China `https://open.ecovacs.cn/`, non-China regions `https://open.ecovacs.com/`). The gateway validates the AK; callers send it in the JSON body below.

Override the gateway host with **`ECOVACS_PORTAL_URL`** when needed.

---

## Endpoints

| Purpose | Method & path |
|---------|----------------|
| Device list | `GET` or `POST` `/robot/skill/deviceList` |
| Pet control | `POST` `/robot/skill/pet/cmd` |
| Legacy (avoid for new work) | `POST` `/robot/skill/ctl` |

Mainland China base URL: `https://open.ecovacs.cn`. Non-China regions: `https://open.ecovacs.com`.

### Device list

```bash
curl -sS "${BASE_URL}/robot/skill/deviceList?ak=YOUR_AK"
```

`POST` with body `{"ak":"<AK>"}` is also supported. On success, `data[]` lists devices; **`product_category: FAMIBOT`** identifies pet robots.

### Pet control: `POST /robot/skill/pet/cmd`

```json
{
  "ak": "<AK>",
  "nickName": "<fragment matched against deviceList nick or name>",
  "cmd": "<business command from SKILL.md>",
  "data": {}
}
```

- **`nickName`**: exact casing (`N` uppercase).
- **`data`**: omit or `{}` when empty; for `display`, pass the full display envelope (`msgId`, inner `cmd`, inner `data`).
- **`playSound`**: `category`（情绪分类，网关随机选音效）**或** `file`（具体音效名，见 [phoenix-single-action.md §2.2](phoenix-single-action.md)）、`count`、可选 `moveTimeMs` / `actions` / `conditions`；网关合成 Phoenix 载荷。
- **Display wake guard**: `scripts/ecovacs.py display ...` may call `setCamera` + `setWorkMode` before motion — see [SKILL.md](../SKILL.md).

Pet control succeeds only for **FAMIBOT** devices.

### curl examples

```bash
export BASE_URL="https://open.ecovacs.cn"
export AK="YOUR_AK"
```

```bash
curl -sS -X POST "${BASE_URL}/robot/skill/pet/cmd" -H 'Content-Type: application/json' \
  -d "{\"ak\":\"${AK}\",\"nickName\":\"nickname-fragment\",\"cmd\":\"getPetState\",\"data\":{}}"
```

More script examples: [SKILL.md](../SKILL.md).

---

## Responses

Outer JSON uses `code` / `msg`; business data is nested under the cloud envelope (often `data.resp.body`).

Common branches are listed in [SKILL.md](../SKILL.md) and [troubleshooting.md](troubleshooting.md).

---

## Building `data`

Use **`cmd` names from [SKILL.md](../SKILL.md)** only. Start with `{}` or minimal fields; extend based on cloud error messages. Query/set field names → [schema.md](schema.md).

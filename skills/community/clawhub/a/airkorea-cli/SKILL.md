---
name: airkorea-cli
description: Korean real-time air quality (PM10, PM2.5, O3, NO2, CO, SO2) and 1–3 day forecasts via 한국환경공단 에어코리아 OpenAPI (apis.data.go.kr/B552584). Six subcommands wrap getMsrstnAcctoRltmMesureDnsty (측정소별 실시간), getCtprvnRltmMesureDnsty (시도별 실시간), getMinuDustFrcstDspth (예보), getMsrstnList (측정소 목록), getTMStdrCrdnt (행정동→TM좌표), and getNearbyMsrstnList (TM→근접측정소). Use when building air-quality dashboards, mask/runner notifications, school outdoor-activity advisories, location-based AQI lookups by 행정동 / 시도 / 좌표, or grounding LLM answers about Korean air quality in regulator-curated data. Pairs with juso-address-cli (resolve addresses), kakao-local-cli (WGS84 coords), kr-holiday-cli (calendar overlay), naver-papago-translate (localize for non-KR users), and tistory-api-cli/velog-cli (publish AQI digests). Free data.go.kr tier (1,000 req/day dev, higher on prod approval).
version: 0.1.0
license: MIT
---

# airkorea-cli

Command-line wrapper for **한국환경공단 에어코리아 OpenAPI** — Korea's first-party air-quality system. Operated by the Korea Environment Corporation, it is the data behind airkorea.or.kr, every weather-app AQI badge in Korea, and the 미세먼지 alert that pings 50M phones on bad-haze days.

Six subcommands wrap two services:

| Command | Endpoint | Purpose |
|---|---|---|
| `scripts/realtime.sh`  | `ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty` | 측정소별 실시간/일별/월별 측정값 (1h–90d). |
| `scripts/sido.sh`      | `ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty`     | 시도별 실시간 측정값 (every station in a province). |
| `scripts/forecast.sh`  | `ArpltnInforInqireSvc/getMinuDustFrcstDspth`        | 1~3일 미세먼지/오존 예보. |
| `scripts/station.sh`   | `MsrstnInfoInqireSvc/getMsrstnList`                 | 측정소 directory (filter by sido / addr keyword). |
| `scripts/tm.sh`        | `MsrstnInfoInqireSvc/getTMStdrCrdnt`                | 행정/법정동 → TM(중부원점) 좌표. |
| `scripts/nearby.sh`    | `MsrstnInfoInqireSvc/getNearbyMsrstnList`           | TM 좌표 → 가까운 측정소 목록 (정렬: 거리). |

All output is JSONL — one row per record — so it pipes directly into `jq`, `csvkit`, `pandas`, or downstream skills.

## When to use this skill

- **AQI dashboards** — `sido --sido 전국 --num 600` to get a country-wide snapshot in one call; cache hourly.
- **Location-based mask/runner alerts** — `tm --umd <my-동>` → `nearby --tm-x … --tm-y …` → `realtime --station <closest>` → push notification when `pm25Grade ≥ 3`.
- **School outdoor-activity advisories** — schedule `forecast --date $(date +%F)` daily; surface `informGrade` and `informCause` to staff/parents.
- **Korean-news AQI grounding** — when an LLM answers "오늘 강남 미세먼지 어때?", cite real-time station data, not hallucinated numbers.
- **Backfill / research panels** — `realtime --period 3MONTH` to pull the last 90 days for any single station; combine with `kr-holiday-cli` to test holiday-traffic effects.

## Do **not** use this skill for

- **Sub-hourly or sensor-grade data** — AirKorea publishes at hourly granularity (with a ~1h delay). For minute-level, use IoT vendors (Awair, IQAir partnerships).
- **Outside-Korea AQI** — only 한국환경공단 stations. For other countries, use OpenAQ, AirNow, or WAQI.
- **Health-effect interpretations** — the API returns concentrations + grades, not personalized health advice. Pair with WHO/CDC guidance text on the consumer side.
- **High-throughput public-facing apps without a prod-tier key** — dev-tier ceiling is 1,000 req/day per service. Apply for production tier on data.go.kr.

## Prerequisites

1. **Register at <https://www.data.go.kr/>** (Korean OpenData portal, free, no business required).
2. Apply for **both** services (auto-approved for the dev tier):
   - "한국환경공단_에어코리아_대기오염정보" (real-time + forecast)
   - "한국환경공단_에어코리아_측정소정보" (station directory + TM utilities)
3. Copy the **Decoding** key (the raw form, *not* URL-encoded) and export:
   ```bash
   export AIRKOREA_SERVICE_KEY='your_decoded_key_here'
   ```
4. Optional overrides (rarely needed):
   ```bash
   export ARPLTN_BASE='https://apis.data.go.kr/B552584/ArpltnInforInqireSvc'
   export MSRSTN_BASE='https://apis.data.go.kr/B552584/MsrstnInfoInqireSvc'
   ```

## Common workflows

### A) Snapshot every Seoul station right now

```bash
scripts/sido.sh --sido 서울 --num 60 \
  | jq -c '{stationName, dataTime, pm10Value, pm25Value, pm10Grade, pm25Grade}'
```

### B) Find my closest station from a 동 name (full chain)

```bash
read TMX TMY < <(scripts/tm.sh --umd 역삼동 \
  | jq -r 'select(.sidoName=="서울") | "\(.tmX) \(.tmY)"' | head -1)

scripts/nearby.sh --tm-x "$TMX" --tm-y "$TMY" | head -3
# → e.g. "강남구", distance ~1.2km

scripts/realtime.sh --station 강남구 --period HOUR --num 1 \
  | jq -c '{dataTime, pm25Value, pm25Grade, pm10Value, pm10Grade, o3Value, no2Value}'
```

### C) Daily forecast headline for a digest email

```bash
scripts/forecast.sh --date "$(date +%F)" --code PM25 \
  | jq -r '"\(.informData) (\(.informCode)) — \(.informGrade // "-")"'
```

### D) 90-day station history → CSV

```bash
scripts/realtime.sh --station 종로구 --period 3MONTH --num 1000 \
  | jq -r '[.dataTime, .pm10Value, .pm25Value, .o3Value, .no2Value] | @csv' \
  > jongno_90d.csv
```

### E) Run a "very-bad" alert across the country

```bash
scripts/sido.sh --sido 전국 --num 1000 \
  | jq -c 'select((.pm25Grade // "-") == "4")'
# emit one row per station that's in 매우나쁨 right now → fan out to your alerter
```

## Output shape — sample (realtime.sh)

```json
{
  "dataTime": "2026-04-29 09:00",
  "stationName": "강남구",
  "mangName": "도시대기",
  "so2Value": "0.003",
  "coValue": "0.4",
  "o3Value": "0.041",
  "no2Value": "0.018",
  "pm10Value": "47",
  "pm25Value": "22",
  "khaiValue": "78",
  "khaiGrade": "2",
  "so2Grade": "1",
  "coGrade": "1",
  "o3Grade": "1",
  "no2Grade": "1",
  "pm10Grade": "1",
  "pm25Grade": "2"
}
```

Grade encoding (used by every `*Grade` field):

| Grade | 등급 | PM2.5 µg/m³ | PM10 µg/m³ |
|---|---|---|---|
| 1 | 좋음 | 0–15 | 0–30 |
| 2 | 보통 | 16–35 | 31–80 |
| 3 | 나쁨 | 36–75 | 81–150 |
| 4 | 매우나쁨 | 76+ | 151+ |

## Errors

| AirKorea resultCode | Meaning | This CLI |
|---|---|---|
| `00` | OK | success, JSONL emitted |
| `99` / XML body | 등록되지 않은 키 / Decoding key 미사용 | exit 22 |
| `01` | Application error | exit 22 |
| `04` | HTTP error | exit 22 |
| `30` | 서비스 키 권한 없음 | exit 22 |
| `12` | DEPRECATED OpenAPI | exit 22 |
| `33` | 일일 트래픽 초과 | exit 22 |

If you get an XML payload with `<errMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</errMsg>`, you most likely pasted the Encoded key — switch to the **Decoding** version on data.go.kr.

## Composability with other skills in this hub

| Pair with | Why |
|---|---|
| `juso-address-cli`  | Resolve a Korean street address → 행정동 → feed into `tm.sh`. |
| `kakao-local-cli`   | Convert WGS84 lat/lng (from a map tap) to TM via Kakao geocoding, then `nearby.sh`. |
| `kr-holiday-cli`    | Overlay holiday weekends on AQI charts (commute drops on holidays — visible in NO2). |
| `naver-papago-translate` | Localize forecast strings (`informCause`) for non-KR-speaking users. |
| `tistory-api-cli` / `velog-cli` | Publish a daily AQI digest as a blog post. |
| `kosis-cli`         | Cross-reference long-run AQI trends with population / industrial-emission stats. |

## License

MIT — see [LICENSE](./LICENSE). AirKorea data is © 한국환경공단; redistribution is permitted under the data.go.kr open-data terms (https://www.data.go.kr/ugs/selectPortalPolicyView.do).

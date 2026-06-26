---
name: g2b-cli
description: Korean public procurement (나라장터 g2b.go.kr) command-line wrapper for the 조달청 OpenAPI surface — three subcommands cover BidPublicInfoService (입찰공고 per 업무구분 thng/servc/cnstwk/frgcpt + PPS keyword search), CntrctInfoService (계약현황 per 업무구분), and PubDataOpnStdService (개방표준 unified bid/awarded/contract feeds). Use when monitoring government tenders, building bid-aggregator dashboards, scraping awarded-contract winners, performing supplier KYB on awardee 사업자번호, alerting subscribers to new RFPs by keyword, or backfilling historical procurement data into a warehouse. Pairs with nts-bizno-cli (resolve awardee 사업자등록번호), juso-address-cli (geocode 수요기관 addresses), kakao-local-cli (map pins), opendart-cli (cross-check awardee disclosures), kr-holiday-cli (calendar overlay for 공고 timing), and tistory-api-cli/velog-cli (publish daily tender digests). Free data.go.kr tier (1,000 req/day dev, expandable on prod approval).
version: 0.1.0
license: MIT
---

# g2b-cli

Command-line wrapper for **조달청 나라장터 OpenAPI** — Korea's first-party public-procurement system. 나라장터 (g2b.go.kr) is the single national platform every Korean government agency, public university, and SOC project must use to post tenders worth roughly **₩200T** per year. The 조달청 (Public Procurement Service) exposes three OpenAPI services on data.go.kr that mirror the website's three core surfaces: 입찰공고, 계약현황, and the 개방표준 data feed.

Three subcommands wrap the surface:

| Command            | Service                    | Purpose                                                                    |
|--------------------|----------------------------|----------------------------------------------------------------------------|
| `scripts/bid.sh`      | `BidPublicInfoService`     | 입찰공고 (current bidding announcements) per 업무구분 + PPS keyword search.   |
| `scripts/contract.sh` | `CntrctInfoService`        | 계약현황 (signed-contract listings) per 업무구분.                             |
| `scripts/std.sh`      | `PubDataOpnStdService`     | 개방표준 unified feed: bid / awarded / contract on one canonical schema.   |

All output is **JSONL** — one row per record — so it pipes directly into `jq`, `csvkit`, `pandas`, or downstream skills. Pass `--meta` to any subcommand to get `{totalCount, pageNo, numOfRows}` instead of the items, which is the right shape for paging loops.

## When to use this skill

- **Tender-monitoring dashboards** — `bid.sh --type servc --keyword "AI"` every hour to surface new AI-related RFPs nationwide. Pair with email/Slack alerts.
- **Awarded-contract scrapers** — `std.sh --what awarded --from 202601010000 --to 202612310000` to backfill the year's 낙찰 records into a warehouse with a single, schema-stable feed.
- **Supplier KYB on awardees** — pull `bizrno` from awarded records, fan out to **`nts-bizno-cli status`** to confirm the company is still 정상사업자 before you sign downstream paperwork.
- **B2B sales prospecting** — `bid.sh --type thng --inquiry-div 5 --dminstt-cd <기관>` to monitor a target buyer institution's tender pipeline.
- **Construction / SOC analysts** — `contract.sh --type cnstwk --from --to` for monthly 공사 contract volumes by region; pair with `kosis-cli` for population/GDP normalisation.
- **Compliance audits** — repeated calls with `--meta` give totals; reconcile against a third-party data vendor's claims.
- **News grounding for AI agents** — when an LLM answers "who won the Seoul subway camera tender?", cite real records from `std.sh --what awarded` instead of hallucinating.

## Do **not** use this skill for

- **Bid submission** — the OpenAPI is read-only. Actual bid filing requires the 나라장터 GPKI/GBKI digital cert + browser session — that's still a Windows-only ActiveX/exe flow as of 2026.
- **Pre-RFP procurement plans (사전공고)** — those live on a separate 조달정보표준 service not yet covered here.
- **Sub-minute polling** — data.go.kr dev keys are 1,000 req/day. For live aggregation in production, request the prod tier on data.go.kr (justification + use-case form, ~3 business days).
- **Outside-Korea procurement** — only 나라장터-listed Korean public tenders. For EU TED, US SAM.gov, or KONEPS/KOICA-funded foreign tenders, use those systems directly.
- **Sub-public tenders (private B2B RFPs)** — Korea's 나라장터 does not host private-sector RFPs. Use third-party platforms (BidWeb, EProcurement) for that.

## Prerequisites

1. **Register at <https://www.data.go.kr/>** (free, no business required).
2. Apply for **all three** services (instant approval, dev tier; production tier needs a usage-case form):
   - "조달청_나라장터 입찰공고정보서비스" (BidPublicInfoService)
   - "조달청_나라장터 계약현황정보" (CntrctInfoService)
   - "조달청_나라장터 공공데이터개방표준서비스" (PubDataOpnStdService)
3. Copy the **Decoding** key (the raw form, *not* URL-encoded) and export:
   ```bash
   export G2B_SERVICE_KEY='your_decoded_key_here'
   ```
4. Optional overrides (rarely needed; useful for staging):
   ```bash
   export G2B_BID_BASE='https://apis.data.go.kr/1230000/ad/BidPublicInfoService'
   export G2B_CNTRCT_BASE='https://apis.data.go.kr/1230000/ao/CntrctInfoService'
   export G2B_STD_BASE='https://apis.data.go.kr/1230000/ao/PubDataOpnStdService'
   ```

## Common workflows

### A) Today's new 용역 (services) tenders

```bash
scripts/bid.sh --type servc --rows 200 \
  | jq -c '{bidNtceNo, bidNtceNm, ntceInsttNm, dminsttNm, presmptPrce, bidNtceDt, bidBeginDt}'
```

### B) Keyword-driven RFP alert (AI-related 용역)

```bash
scripts/bid.sh --keyword "인공지능" --rows 50 \
  | jq -c 'select(.bidNtceDt >= "2026-04-01") | {bidNtceNo, bidNtceNm, presmptPrce, ntceInsttNm}' \
  | tee today_ai_rfps.jsonl
```

### C) Last-week awarded contracts → warehouse

```bash
# Use the open-standard feed for warehouse-ready, schema-stable rows.
scripts/std.sh --what awarded --from 202604220000 --to 202604290000 --rows 500 \
  > awarded_2026wk17.jsonl
```

### D) Awardee KYB chain (g2b → nts-bizno)

```bash
# 1. Pull awarded list.
scripts/std.sh --what awarded --rows 100 > awarded.jsonl

# 2. For each awardee 사업자번호, confirm 정상사업자 status.
jq -r '.bizrno // empty' awarded.jsonl | sort -u | while read brn; do
  nts-bizno-cli status --b-no "$brn" \
    | jq --arg brn "$brn" '{bizrno: $brn, taxType: .tax_type, businessStatus: .b_stt}'
done > awardee_kyb.jsonl
```

### E) One specific 공고 detail (when you have the bidNtceNo)

```bash
scripts/bid.sh --type thng --bid-no 20240412345-00 --rows 1 | jq .
```

### F) Buyer-institution tender pipeline (수요기관 기준)

```bash
# 6110000 = 서울특별시청 (example dminsttCd; look up via the 나라장터 institution dictionary).
scripts/bid.sh --type cnstwk --inquiry-div 5 --dminstt-cd 6110000 --rows 200 \
  | jq -c '{bidNtceNo, bidNtceNm, presmptPrce, opengDt}'
```

### G) Pagination loop (full month dump)

```bash
month_from=202604010000; month_to=202604300000
scripts/std.sh --what bid --from $month_from --to $month_to --meta
# {"totalCount":4982,"pageNo":1,"numOfRows":100}

for p in $(seq 1 50); do
  scripts/std.sh --what bid --from $month_from --to $month_to --rows 100 --page $p \
    >> bid_2026_04.jsonl
done
```

## Data shapes (high-signal fields)

`bid.sh` (BidPublicInfoService) — non-exhaustive list:

| Field            | Meaning                                        |
|------------------|------------------------------------------------|
| `bidNtceNo`      | 입찰공고번호 (primary key)                       |
| `bidNtceOrd`     | 차수 (revision; 00 = original)                 |
| `bidNtceNm`      | 입찰공고명                                       |
| `ntceInsttNm`    | 공고기관명 (the institution that *posted*)        |
| `dminsttNm`      | 수요기관명 (the institution that *will use* it)   |
| `presmptPrce`    | 추정가격 (원)                                    |
| `bidNtceDt`      | 공고게시일자                                       |
| `bidBeginDt`     | 입찰개시일시                                       |
| `opengDt`        | 개찰일시                                          |
| `bidMethdNm`     | 입찰방식                                          |
| `cntrctCnclsMthdNm` | 계약체결방법                                    |

`contract.sh` (CntrctInfoService) — non-exhaustive list:

| Field            | Meaning                                        |
|------------------|------------------------------------------------|
| `cntrctNo`       | 계약번호 (primary key)                            |
| `cntrctNm`       | 계약명                                            |
| `cntrctMthdNm`   | 계약방식                                          |
| `cntrctCnclsDate`| 계약체결일자                                       |
| `cntrctPrce`     | 계약금액 (원)                                     |
| `bizrno`         | 낙찰자 사업자등록번호                                |
| `corpNm`         | 낙찰자 상호                                        |

`std.sh --what awarded` — non-exhaustive list:

| Field            | Meaning                                        |
|------------------|------------------------------------------------|
| `bidNtceNo`      | 입찰공고번호                                       |
| `opengDate`      | 개찰일자                                           |
| `sucsfbidAmt`    | 낙찰금액 (원)                                     |
| `sucsfbidRate`   | 낙찰률 (%)                                        |
| `bizrno`         | 낙찰자 사업자등록번호                                 |
| `corpNm`         | 낙찰자 상호                                        |

Field names are stable inside each `--what` mode of `std.sh` but vary across the four 업무구분 in the non-std endpoints — always inspect a row before assuming a key exists.

## Pairs naturally with

- **nts-bizno-cli** — resolve every `bizrno` in awarded records to a tax-type + business-status (KYB on the supplier side).
- **juso-address-cli** — geocode 수요기관/공고기관 addresses to a 행정동 + WGS84.
- **kakao-local-cli** — map-pin the resolved coordinates for a regional tender map.
- **opendart-cli** — cross-check listed-company awardees against their public disclosures (ownership, financials, related-party).
- **kr-holiday-cli** — calendar-overlay tenders to detect off-cycle posting (often a sign of urgency or favoritism).
- **tistory-api-cli / velog-cli** — publish daily/weekly tender-digest posts (e.g., "AI 입찰 모음 — 2026-04-29").

## Implementation notes

- All endpoints accept both XML and JSON (`type=json`). This skill always asks for JSON; the wrapper will hard-fail with a clear message if the upstream returns XML (the 조달청 service silently falls back to XML on a serviceKey error).
- Date params on g2b are **12-digit `YYYYMMDDHHMM`** — the wrapper validates this and provides a sensible default (last 7 days) when neither `--from`/`--to` nor `--bid-no` is given.
- `inqryDiv` (조회구분) defaults match what the official portal example shows: `1` for date-window queries, `3` for `--bid-no`, `4` for `--instt-cd`, `5` for `--dminstt-cd`. Override with `--inquiry-div` if you need 등록 vs. 공고게시 vs. 개찰일자 selection.
- The keyword search (`--keyword`) targets `getBidPblancListInfoServcPPSSrch` — only 용역 has a documented PPS keyword endpoint. For 물품/공사/외자, post-filter with `jq 'select(.bidNtceNm | test("키워드"))'` instead.
- The wrapper validates the `response.header.resultCode == "00"` envelope and surfaces `resultMsg` on failure — common codes: `30` (서비스키 미등록), `22` (LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS — daily quota hit), `11` (NODATA_ERROR — empty result, *not* a failure shape; the wrapper still treats this as an error so you'll know upstream returned nothing).

## Examples

See `examples/` for end-to-end recipes including: AI-keyword RFP digest, weekly 낙찰 ETL, awardee KYB pipeline, regional construction-contract map.

## Key takeaways

- Three subcommands cover the entire 조달청 OpenAPI public surface. Pick `std.sh` first when you want one canonical schema; pick `bid.sh` / `contract.sh` when you need the per-업무구분 fields the open-standard feed strips.
- This is the read side of 나라장터; bid submission is intentionally out of scope.
- Pair with `nts-bizno-cli` for end-to-end awardee-vetting in a single shell pipeline — the missing piece between "the contract was awarded" and "the awardee is currently a 정상사업자".

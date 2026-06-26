# g2b-cli

CLI wrapper for **조달청 나라장터 OpenAPI** (Korea Public Procurement Service / g2b.go.kr) — read-only access to Korea's national tender system.

Three subcommands, JSONL output, free `data.go.kr` key.

| Command            | Service                    | Purpose                                                                  |
|--------------------|----------------------------|--------------------------------------------------------------------------|
| `scripts/bid.sh`      | `BidPublicInfoService`     | 입찰공고 (current bidding announcements) per 업무구분 + PPS keyword search. |
| `scripts/contract.sh` | `CntrctInfoService`        | 계약현황 (signed-contract listings) per 업무구분.                           |
| `scripts/std.sh`      | `PubDataOpnStdService`     | 개방표준 unified bid / awarded / contract feed.                             |

## Quick start

```bash
# 1. Get a key from data.go.kr (see SKILL.md for the three services to apply for).
export G2B_SERVICE_KEY='your_decoded_key_here'

# 2. Today's new 용역 tenders.
scripts/bid.sh --type servc --rows 200

# 3. AI-keyword RFP search.
scripts/bid.sh --keyword "인공지능" --rows 50

# 4. Last week's awarded contracts (warehouse-ready open-std feed).
scripts/std.sh --what awarded --from 202604220000 --to 202604290000 --rows 500
```

Run any subcommand with `--help` for full option lists.

## Output

JSONL — one record per line. Pipes directly into `jq`, `csvkit`, `pandas`, etc.

```bash
scripts/std.sh --what bid --rows 5 \
  | jq -c '{bidNtceNo, bidNtceNm, ntceInsttNm, presmptPrce}'
```

Pass `--meta` to any subcommand for `{totalCount, pageNo, numOfRows}` (use this to drive pagination loops).

## Pairs with

- **nts-bizno-cli** — KYB the awardees (resolve `bizrno` → 정상사업자 status).
- **juso-address-cli** — geocode 수요기관 addresses.
- **kakao-local-cli** — map-pin the coords.
- **opendart-cli** — cross-check listed-company awardees against disclosures.
- **tistory-api-cli / velog-cli** — publish daily tender digests.

## Auth

Free `data.go.kr` developer tier (1,000 req/day per service). Apply for the prod tier with a usage-case form when you need higher quotas.

## License

MIT.

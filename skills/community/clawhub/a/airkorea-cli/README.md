# airkorea-cli

Bash CLI wrapping **한국환경공단 에어코리아 OpenAPI** (apis.data.go.kr/B552584) — Korea's first-party real-time air-quality and forecast system.

Six subcommands cover **측정소별 실시간 · 시도별 실시간 · 예보 · 측정소 디렉토리 · 행정동→TM 좌표 변환 · 근접측정소**. Output is JSONL so it pipes straight into `jq`, `csvkit`, `pandas`, or any downstream skill.

See [SKILL.md](./SKILL.md) for the full reference, workflows, and composability tips.

## Quickstart

```bash
# 1. Register at https://www.data.go.kr/ and approve both:
#    - 한국환경공단_에어코리아_대기오염정보
#    - 한국환경공단_에어코리아_측정소정보
export AIRKOREA_SERVICE_KEY='your_decoded_key_here'

# 2. Snapshot every Seoul station right now.
./scripts/sido.sh --sido 서울 --num 60 \
  | jq -c '{stationName, dataTime, pm25Value, pm25Grade}'

# 3. From a 동 name → closest station → latest reading.
read TMX TMY < <(./scripts/tm.sh --umd 역삼동 | jq -r '.tmX, .tmY' | head -2 | xargs)
./scripts/nearby.sh --tm-x "$TMX" --tm-y "$TMY" | head -3
```

## Requirements

- `curl`, `jq`
- An AirKorea service key (free, 1,000 req/day dev tier)

## License

MIT

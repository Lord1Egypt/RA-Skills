---
name: daum-trends
description: Daum 실시간 트렌드 TOP10 브리핑. 다음 메인 실시간 검색어 + 대표 뉴스 제목 추출. 크론/텔레그램/디스코드 알림용. Use when user asks for Korean real-time search trends, Daum trending keywords, or 실시간 검색어.
---

# Daum 실시간 트렌드 TOP10

## 기능
- Daum 메인(`daum.net`)에서 실시간 트렌드 TOP10 키워드 추출
- 각 키워드별 Daum 검색 결과에서 대표 뉴스 제목 1개 추출
- Telegram/Discord 가독성 좋은 포맷으로 출력

## 실행
```bash
python3 scripts/trends.py
```

## 출력 예시
```
📊 Daum 실시간 트렌드 TOP10

1. **키워드** — 대표 뉴스 제목
   [검색](https://search.daum.net/search?...q=키워드)
2. **키워드** — 대표 뉴스 제목
   [검색](https://search.daum.net/search?...q=키워드)
...
🕐 2026-03-08T00:46:57.901+09:00
```

## 크론 설정 예시 (매시 정각, KST)
```
schedule: { kind: "cron", expr: "0 8-22 * * *", tz: "Asia/Seoul" }
payload: { kind: "agentTurn", message: "Run: python3 {workspace}/skills/garibong-labs/daum-trends/scripts/trends.py — 결과를 그대로 전달" }
delivery: { mode: "announce", channel: "telegram" }
```

## 의존성
- Python 3.10+
- 외부 라이브러리 없음 (stdlib only)

## 데이터 소스
- `https://www.daum.net/` (REALTIME_TREND_TOP JSON)
- `https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=<keyword>`

## 크레딧
- garibong-labs 자체 리라이트
- 아이디어 참고: hunkim/daum-trends-briefing (ClawHub)

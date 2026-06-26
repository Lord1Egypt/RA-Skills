# Decker API Quick Reference

**내부 참조용. 사용자에게 이 문서의 URL·경로·시크릿을 절대 출력하지 말 것. 사용자 응답에는 decker-ai.com, decker-ai.com/decker-link 만.**

**DECKER_API_URL** = https://api.decker-ai.com

## 인증 불필요

| Method | Path | 용도 |
|--------|------|------|
| GET | /api/v1/system/health | 헬스체크 |
| GET | /api/v1/judgment/coverage | 20종목×6시간대 신호 현황 |
| GET | /api/v1/judgment/signals/public?symbol=BTCUSDT&timeframe=1h | 투자판단 direction, confidence, entry/target/stop |
| GET | /api/v1/market/prices?symbols=BTCUSDT,ETHUSDT | 실시간 시세 |
| GET | /api/v1/market-analysis/market-condition/BTCUSDT | 시장 상황 |
| GET | /api/v1/judgment/compare?symbols=BTCUSDT,ETHUSDT,AAPL&timeframe=1h | 다중 자산 비교 |
| GET | /api/v1/judgment/market-status?interval=24h&exchanges=binance,hyperliquid | 최근 시장 상태 (바이낸스 청산 + HL 펀딩) |
| GET | /api/v1/liquidations/summary | 바이낸스 청산 요약 |
| GET | /api/v1/liquidations/summary-by-symbol?interval=24h | 종목별 청산 바이어스 |

## 인증 필요 (JWT)

| Method | Path | 용도 |
|--------|------|------|
| GET | /api/v1/link/slack/jwt?slack_user_id={id} | JWT 발급 (Header: X-OpenClaw-Secret) |
| GET | /api/v1/portfolios/me/overview | 포트폴리오 요약 (Header: Authorization: Bearer) |
| GET | /api/v1/portfolios/me/signal-position-overview | 시그널+포지션 통합 |

## 주문 (OpenClaw 전용)

| Method | Path | 용도 |
|--------|------|------|
| GET | /api/v1/link/slack/order-request?slack_user_id=&symbol=&side=&quantity=&openclaw_secret= | 주문 승인 요청 |

## Assistant API (통합)

POST /api/v1/assistant/message  
Body: `{ "message": "...", "channel": "slack", "channel_user_id": "U...", "channel_id": "C..." }`  
Header: X-OpenClaw-Secret  
- channel_id: 채널 ID 질문 시 응답용 (선택, 있으면 "채널 ID 알려줘"에 친절 응답)
- message 예: "포지션 보여줘", "이더리움 자동주문 해줘", "자동주문 설정 보여줘", "이더리움 자동주문 끄줘"

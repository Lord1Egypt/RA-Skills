---
name: decker-polymarket
description: "Use when user asks about Polymarket prediction market via Decker. Triggers: Polymarket, 폴리마켓, 예측시장, PM 매수, PM 시장 검색, PM 카테고리, PM 이벤트, 시장 slug, YES/NO."
user-invocable: true
metadata:
  version: 1.1.0
  extends: decker
---

# Decker + Polymarket (예측시장) 스킬

## Goal

Decker를 통해 **Polymarket 예측시장**에서 시장 조회·YES/NO 주문 실행. 메인 decker 스킬을 확장. ClawHub polymarket-odds 흡수.

## Quick Reference

| 사용자 말 | 액션 | 비고 |
|-----------|------|------|
| "PM 시장 검색 비트코인", "폴리마켓 검색 트럼프" | 시장 검색 | Gamma API search |
| "PM 카테고리", "폴리마켓 태그" | 태그/카테고리 목록 | Gamma tags |
| "PM 이벤트 crypto", "폴리마켓 이벤트 정치" | 이벤트 목록 | tag_slug 선택 |
| "PM 시장 will-bitcoin-100k", "폴리마켓 will-x" | 시장 slug 상세 | Gamma market by slug |
| "Polymarket will-x-win yes 10 매수", "PM 시장 slug yes 매수" | order-request **exchange_id=polymarket** | symbol=market_slug, outcome=yes/no |
| "Polymarket 시장 가격", "PM 확률" | Assistant API 또는 시장 조회 | |
| "PM 포지션" | Assistant API | JWT 필요 |

## DECKER_API_URL

https://api.decker-ai.com

## 주문 (Polymarket)

**order-request에 exchange_id=polymarket 추가**:

```
GET {DECKER_API_URL}/api/v1/link/slack/order-request?slack_user_id={sender_id}&symbol=will-x-win&side=buy&quantity=10&exchange_id=polymarket&outcome=yes&openclaw_secret={OPENCLAW_SECRET}
```

- **exchange_id=polymarket** 필수
- **symbol**: Polymarket 시장 slug (예: will-joe-biden-get-coronavirus-before-the-election)
- **outcome**: yes | no (YES/NO 토큰)
- **quantity**: 주식 수 (shares)
- **price**: Limit 주문 시 0.01~0.99 (선택)

## 전제 조건

- Decker 가입 + Slack 연동
- **Polymarket 키 연동** (Decker 설정 → 거래소 API 설정)
- 시장 slug는 Polymarket에서 확인

## Polymarket 키 설정 (에이전트 안내용)

1. **Polygon 지갑**: MetaMask에서 Polygon 네트워크(Chain ID 137) 추가
2. **Polymarket 가입**: https://polymarket.com → 지갑 연결 → USDC.e 입금(거래용)
3. **개인키 추출**: MetaMask → 계정 세부정보 → Export Private Key
4. **Decker 설정**: 로그인 → 설정 → 거래소 API 설정 → Polymarket
   - Secret Key: Polygon 지갑 개인키(0x로 시작) — **필수**
5. **거래소 선택**: exchange_preference를 "Polymarket"로 설정 후 저장
6. **주문**: "Polymarket 시장-slug yes 10 매수" (slug는 polymarket.com에서 확인)

⚠️ USDC.e 필요. 개인키는 절대 공유하지 마세요.

## 참고

- 메인 decker 스킬: `docs/openclaw_skills/decker/SKILL.md`
- Polymarket: 예측시장 (YES/NO 이진 시장)

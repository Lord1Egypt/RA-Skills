---
name: ids_refresh_token
description: "refresh_token을 사용하여 새로운 access_token으로 교환.
【호출 절차】
1. 사전 조건: refresh_token 보유 (로그인 인터페이스에서 반환됨)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(refresh_token값 + 'ffdfddfdfu***').toUpperCase()
4. POST 요청 본문: { refresh_token }
【주의】authcode 헤더는 필요하지 않음. access_token이 만료되었을 때 이 인터페이스를 호출하여 갱신."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# access_token 갱신

refresh_token을 사용하여 새로운 access_token으로 교환.
【호출 절차】
1. 사전 조건: refresh_token 보유 (로그인 인터페이스에서 반환됨)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(refresh_token값 + 'ffdfddfdfu***').toUpperCase()
4. POST 요청 본문: { refresh_token }
【주의】authcode 헤더는 필요하지 않음. access_token이 만료되었을 때 이 인터페이스를 호출하여 갱신.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_refresh_token` |
| Display Name | access_token 갱신 |
| Method | `POST` |
| Endpoint | `/ids/refresh_token` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

---
name: ids_send_tel_code
description: "휴대폰으로 로그인 SMS 인증 코드 발송.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(tel + area_code + 'bb^^5tghdn***').toUpperCase()
3. POST 요청 본문: { area_code, iso_alpha2, tel, type }
   - area_code: 예 \"+86\"
   - iso_alpha2: 예 \"CN\"
   - type=1: 사용자 로그인, type=2: 판매자 로그인
【주의】authcode 헤더는 필요하지 않음. 발송 후 u_login_tel 또는 m_login_tel 로그인에 사용."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# SMS 인증 코드 발송

휴대폰으로 로그인 SMS 인증 코드 발송.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(tel + area_code + 'bb^^5tghdn***').toUpperCase()
3. POST 요청 본문: { area_code, iso_alpha2, tel, type }
   - area_code: 예 "+86"
   - iso_alpha2: 예 "CN"
   - type=1: 사용자 로그인, type=2: 판매자 로그인
【주의】authcode 헤더는 필요하지 않음. 발송 후 u_login_tel 또는 m_login_tel 로그인에 사용.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_send_tel_code` |
| Display Name | SMS 인증 코드 발송 |
| Method | `POST` |
| Endpoint | `/ids/send_tel_code` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

---
name: ids_m_login_email
description: "판매자 이메일 인증 코드 로그인.
【호출 절차】
1. 먼저 send_email_code를 호출하여 인증 코드 발송 (type=2는 판매자를 의미)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(email + captcha + 'fffffdd***').toUpperCase()
4. POST 요청 본문: { email, captcha, device_token, recommand_code }
【주의】authcode 헤더는 필요하지 않음. recommand_code는 비워서 전달 가능."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 판매자 로그인-이메일 인증 코드

판매자 이메일 인증 코드 로그인.
【호출 절차】
1. 먼저 send_email_code를 호출하여 인증 코드 발송 (type=2는 판매자를 의미)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(email + captcha + 'fffffdd***').toUpperCase()
4. POST 요청 본문: { email, captcha, device_token, recommand_code }
【주의】authcode 헤더는 필요하지 않음. recommand_code는 비워서 전달 가능.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_m_login_email` |
| Display Name | 판매자 로그인-이메일 인증 코드 |
| Method | `POST` |
| Endpoint | `/ids/m_login_email` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

---
name: ids_send_email_code
description: "이메일로 로그인 인증 코드 발송.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(email + 'UUjhtfgf***').toUpperCase()
3. POST 요청 본문: { email, type }
   - type=1: 사용자 로그인 인증 코드
   - type=2: 판매자 로그인 인증 코드
【주의】authcode 헤더는 필요하지 않음. 발송 후 사용자가 이메일에서 인증 코드를 수신하여 u_login_email 또는 m_login_email 로그인에 사용."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 이메일 인증 코드 발송

이메일로 로그인 인증 코드 발송.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(email + 'UUjhtfgf***').toUpperCase()
3. POST 요청 본문: { email, type }
   - type=1: 사용자 로그인 인증 코드
   - type=2: 판매자 로그인 인증 코드
【주의】authcode 헤더는 필요하지 않음. 발송 후 사용자가 이메일에서 인증 코드를 수신하여 u_login_email 또는 m_login_email 로그인에 사용.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_send_email_code` |
| Display Name | 이메일 인증 코드 발송 |
| Method | `POST` |
| Endpoint | `/ids/send_email_code` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

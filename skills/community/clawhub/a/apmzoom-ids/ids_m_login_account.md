---
name: ids_m_login_account
description: "판매자 계정/비밀번호 로그인, access_token 및 refresh_token 획득.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'ggfgffgfggf').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음. 반환된 access_token에서 r=2는 판매자 역할을 의미.
판매자 token은 m_으로 시작하는 인터페이스만 호출할 수 있으며, u_로 시작하는 인터페이스는 호출할 수 없음."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 판매자 로그인-계정/비밀번호

판매자 계정/비밀번호 로그인, access_token 및 refresh_token 획득.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'ggfgffgfggf').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음. 반환된 access_token에서 r=2는 판매자 역할을 의미.
판매자 token은 m_으로 시작하는 인터페이스만 호출할 수 있으며, u_로 시작하는 인터페이스는 호출할 수 없음.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_m_login_account` |
| Display Name | 판매자 로그인-계정/비밀번호 |
| Method | `POST` |
| Endpoint | `/ids/m_login_account` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

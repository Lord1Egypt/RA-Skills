---
name: ids_u_login_account
description: "사용자 계정/비밀번호 로그인, access_token 및 refresh_token 획득.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpdppOOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
4. device_token은 \"web_\" + 타임스탬프로 전달 가능
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음.
【응답】code=100일 때 result에 포함:
- access_token: JWT 토큰 (r=1은 사용자 역할을 의미), 이후 인증이 필요한 모든 인터페이스에 사용
- refresh_token: access_token 갱신에 사용"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 사용자 로그인-계정/비밀번호

사용자 계정/비밀번호 로그인, access_token 및 refresh_token 획득.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpdppOOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
4. device_token은 "web_" + 타임스탬프로 전달 가능
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음.
【응답】code=100일 때 result에 포함:
- access_token: JWT 토큰 (r=1은 사용자 역할을 의미), 이후 인증이 필요한 모든 인터페이스에 사용
- refresh_token: access_token 갱신에 사용

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_u_login_account` |
| Display Name | 사용자 로그인-계정/비밀번호 |
| Method | `POST` |
| Endpoint | `/ids/u_login_account` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

---
name: ids_u_login_to_ce
description: "사용자 계정/비밀번호 로그인 CE 버전, 절차는 u_login_account와 동일.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpdppOOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 사용자 로그인-계정/비밀번호(CE)

사용자 계정/비밀번호 로그인 CE 버전, 절차는 u_login_account와 동일.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpdppOOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_u_login_to_ce` |
| Display Name | 사용자 로그인-계정/비밀번호(CE) |
| Method | `POST` |
| Endpoint | `/ids/u_login_to_ce` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

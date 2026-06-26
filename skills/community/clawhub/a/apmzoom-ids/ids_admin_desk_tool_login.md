---
name: ids_admin_desk_tool_login
description: "관리자 데스크탑 도구 로그인, 절차는 admin_login과 동일.
【호출 절차】
1. 먼저 captcha_img를 호출하여 그래픽 인증 코드 획득
2. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
3. POST: { account, login_pwd, captcha_code_key, captcha_code }"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 관리자 데스크탑 도구 로그인

관리자 데스크탑 도구 로그인, 절차는 admin_login과 동일.
【호출 절차】
1. 먼저 captcha_img를 호출하여 그래픽 인증 코드 획득
2. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
3. POST: { account, login_pwd, captcha_code_key, captcha_code }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_admin_desk_tool_login` |
| Display Name | 관리자 데스크탑 도구 로그인 |
| Method | `POST` |
| Endpoint | `/ids/admin_desk_tool_login` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

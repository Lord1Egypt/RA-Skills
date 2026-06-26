---
name: ids_suppliers_login
description: "공급업체 계정/비밀번호 로그인.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
【주의】authcode 헤더는 필요하지 않음."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 공급업체 로그인

공급업체 계정/비밀번호 로그인.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
3. POST 요청 본문: { account, login_pwd, device_token }
【주의】authcode 헤더는 필요하지 않음.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_suppliers_login` |
| Display Name | 공급업체 로그인 |
| Method | `POST` |
| Endpoint | `/ids/suppliers_login` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

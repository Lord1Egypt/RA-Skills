---
name: ids_admin_login
description: "관리자 로그인 (먼저 그래픽 인증 코드를 획득해야 함).
【호출 절차】
1. 먼저 captcha_img를 호출하여 그래픽 인증 코드 이미지와 captcha_code_key 획득
2. 사용자가 인증 코드를 입력한 후, 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
4. POST 요청 본문: { account, login_pwd, captcha_code_key, captcha_code }
【주의】authcode 헤더는 필요하지 않음."
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 관리자 로그인

관리자 로그인 (먼저 그래픽 인증 코드를 획득해야 함).
【호출 절차】
1. 먼저 captcha_img를 호출하여 그래픽 인증 코드 이미지와 captcha_code_key 획득
2. 사용자가 인증 코드를 입력한 후, 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(account + login_pwd + 'sjpOkkmhm9ds').toUpperCase()
4. POST 요청 본문: { account, login_pwd, captcha_code_key, captcha_code }
【주의】authcode 헤더는 필요하지 않음.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_admin_login` |
| Display Name | 관리자 로그인 |
| Method | `POST` |
| Endpoint | `/ids/admin_login` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

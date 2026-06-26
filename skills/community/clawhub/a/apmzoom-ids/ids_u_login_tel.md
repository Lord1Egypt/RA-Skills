---
name: ids_u_login_tel
description: "사용자 휴대폰 인증 코드 로그인 (계정이 없으면 자동 회원가입).
【호출 절차】
1. 먼저 send_tel_code를 호출하여 SMS 인증 코드 발송 (type=1)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(area_code + captcha + tel + 'ggfff***').toUpperCase()
4. POST 요청 본문: { area_code, iso_alpha2, tel, captcha, device_token, recommand_code }
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음. area_code 예: \"+86\", iso_alpha2 예: \"CN\".
【응답】u_login_account와 동일, access_token + refresh_token 반환"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 사용자 로그인-휴대폰 번호 인증 코드

사용자 휴대폰 인증 코드 로그인 (계정이 없으면 자동 회원가입).
【호출 절차】
1. 먼저 send_tel_code를 호출하여 SMS 인증 코드 발송 (type=1)
2. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
3. sign 계산: MD5(area_code + captcha + tel + 'ggfff***').toUpperCase()
4. POST 요청 본문: { area_code, iso_alpha2, tel, captcha, device_token, recommand_code }
【주의】이 인터페이스는 authcode 헤더가 필요하지 않음. area_code 예: "+86", iso_alpha2 예: "CN".
【응답】u_login_account와 동일, access_token + refresh_token 반환

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_u_login_tel` |
| Display Name | 사용자 로그인-휴대폰 번호 인증 코드 |
| Method | `POST` |
| Endpoint | `/ids/u_login_tel` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

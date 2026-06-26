---
name: ids_captcha_img
description: "그래픽 인증 코드 이미지 획득 (관리자 로그인 전 단계).
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5('ijhteuPPokM6241R24').toUpperCase()
3. GET 요청, 매개변수 없음
【응답】result에 포함:
- captcha_image: base64 형식의 인증 코드 이미지
- captcha_code_key: 인증 코드 Key, admin_login 인터페이스에 전달하여 사용"
version: 1.0.0
category: 인증 센터
permission_level: read
enabled: true
is_public: false
---

# 인증 코드 이미지 획득

그래픽 인증 코드 이미지 획득 (관리자 로그인 전 단계).
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5('ijhteuPPokM6241R24').toUpperCase()
3. GET 요청, 매개변수 없음
【응답】result에 포함:
- captcha_image: base64 형식의 인증 코드 이미지
- captcha_code_key: 인증 코드 Key, admin_login 인터페이스에 전달하여 사용

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_captcha_img` |
| Display Name | 인증 코드 이미지 획득 |
| Method | `GET` |
| Endpoint | `/ids/captcha_img` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

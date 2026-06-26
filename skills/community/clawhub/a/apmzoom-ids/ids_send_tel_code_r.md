---
name: ids_send_tel_code_r
description: "휴대폰으로 회원가입 SMS 인증 코드 발송.
【호출 절차】send_tel_code와 동일:
1. sign 계산: MD5(tel + area_code + 'bb^^5tghdn***').toUpperCase()
2. POST: { area_code, iso_alpha2, tel, type }"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# SMS 인증 코드 발송(회원가입)

휴대폰으로 회원가입 SMS 인증 코드 발송.
【호출 절차】send_tel_code와 동일:
1. sign 계산: MD5(tel + area_code + 'bb^^5tghdn***').toUpperCase()
2. POST: { area_code, iso_alpha2, tel, type }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_send_tel_code_r` |
| Display Name | SMS 인증 코드 발송(회원가입) |
| Method | `POST` |
| Endpoint | `/ids/send_tel_code_r` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

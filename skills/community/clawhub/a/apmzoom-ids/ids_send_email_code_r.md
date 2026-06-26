---
name: ids_send_email_code_r
description: "이메일로 회원가입 인증 코드 발송.
【호출 절차】send_email_code와 동일:
1. sign 계산: MD5(email + 'UUjhtfgf***').toUpperCase()
2. POST: { email, type }  type=1 사용자/2 판매자"
version: 1.0.0
category: 인증 센터
permission_level: write
enabled: true
is_public: false
---

# 이메일 인증 코드 발송(회원가입)

이메일로 회원가입 인증 코드 발송.
【호출 절차】send_email_code와 동일:
1. sign 계산: MD5(email + 'UUjhtfgf***').toUpperCase()
2. POST: { email, type }  type=1 사용자/2 판매자

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_send_email_code_r` |
| Display Name | 이메일 인증 코드 발송(회원가입) |
| Method | `POST` |
| Endpoint | `/ids/send_email_code_r` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

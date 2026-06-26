---
name: ids_verfy_t
description: "access_token 유효성 검증.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(service_name + access_token_role + 'ijgytghteu***').toUpperCase()
   주의: sign에는 access_token 자체가 포함되지 않으며, service_name + role + salt만 사용
3. POST 요청 본문: { service_name, access_token, access_token_role }
   - service_name: 예 \"userservice\", \"sysservice\"
   - access_token_role: \"user\"/\"merchant\"/\"admin\"
【응답】code=100은 token이 유효함을 의미, result에 사용자 정보 포함 (user_id, store_id 등)"
version: 1.0.0
category: 인증 센터
permission_level: read
enabled: true
is_public: false
---

# Token 검증

access_token 유효성 검증.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. sign 계산: MD5(service_name + access_token_role + 'ijgytghteu***').toUpperCase()
   주의: sign에는 access_token 자체가 포함되지 않으며, service_name + role + salt만 사용
3. POST 요청 본문: { service_name, access_token, access_token_role }
   - service_name: 예 "userservice", "sysservice"
   - access_token_role: "user"/"merchant"/"admin"
【응답】code=100은 token이 유효함을 의미, result에 사용자 정보 포함 (user_id, store_id 등)

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `ids_verfy_t` |
| Display Name | Token 검증 |
| Method | `POST` |
| Endpoint | `/ids/verfy_t` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 인증 센터 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

---
name: gds_m_delgoods
description: "판매자가 지정한 상품을 삭제합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsni3r@pt6sb').toUpperCase()
3. POST { goods_id, ver }
【주의】반드시 ver 버전 번호를 전달해야 함 (m_goodseditinfo에서 획득)"
version: 1.0.0
category: 상품 관리-판매자
permission_level: write
enabled: true
is_public: false
---

# 상품 정보 삭제[판매자]

판매자가 지정한 상품을 삭제합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsni3r@pt6sb').toUpperCase()
3. POST { goods_id, ver }
【주의】반드시 ver 버전 번호를 전달해야 함 (m_goodseditinfo에서 획득)

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_delgoods` |
| Display Name | 상품 정보 삭제[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_delgoods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

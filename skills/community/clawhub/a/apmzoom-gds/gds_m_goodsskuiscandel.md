---
name: gds_m_goodsskuiscandel
description: "지정한 SKU의 삭제 가능 여부를 조회합니다.
【사전 조건】판매자 access_token + sku_id 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsk0r$me5jsb').toUpperCase()
3. GET ?sku_id=SKU_ID
【응답】{ is_can_del: 0|1 }"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 상품 SKU 삭제 가능 여부 조회[판매자]

지정한 SKU의 삭제 가능 여부를 조회합니다.
【사전 조건】판매자 access_token + sku_id 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsk0r$me5jsb').toUpperCase()
3. GET ?sku_id=SKU_ID
【응답】{ is_can_del: 0|1 }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodsskuiscandel` |
| Display Name | 상품 SKU 삭제 가능 여부 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodsskuiscandel` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

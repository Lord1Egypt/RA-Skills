---
name: gds_m_goodseditskuinfo
description: "상품의 모든 SKU 규격 정보를 조회합니다.
【사전 조건】판매자 access_token + goods_id 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsk0enu@3hjsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】SKU 규격 배열:
{ goods_skus: [{ sku_id, sale_price, stock_count, goods_specs: [{ spec_name, spec_value_name, spec_value_img }] }] }"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 상품 규격 정보 조회[판매자]

상품의 모든 SKU 규격 정보를 조회합니다.
【사전 조건】판매자 access_token + goods_id 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsk0enu@3hjsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】SKU 규격 배열:
{ goods_skus: [{ sku_id, sale_price, stock_count, goods_specs: [{ spec_name, spec_value_name, spec_value_img }] }] }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodseditskuinfo` |
| Display Name | 상품 규격 정보 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodseditskuinfo` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

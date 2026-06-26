---
name: gds_u_goodsskulist
description: "상품 SKU 규격 목록 조회 (사용자측).
【사전 조건】사용자 access_token + goods_id 필요 (상품 목록 또는 검색에서 획득).
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jskp9Ght$wymsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】result 에 goods_skus 배열 포함:
[{ sku_id, sale_price, stock_count, goods_specs: [{ spec_name: \"색상\", spec_value_name: \"이미지 색상\" }, ...] }]"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 규격 정보 조회[사용자]

상품 SKU 규격 목록 조회 (사용자측).
【사전 조건】사용자 access_token + goods_id 필요 (상품 목록 또는 검색에서 획득).
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jskp9Ght$wymsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】result 에 goods_skus 배열 포함:
[{ sku_id, sale_price, stock_count, goods_specs: [{ spec_name: "색상", spec_value_name: "이미지 색상" }, ...] }]

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_goodsskulist` |
| Display Name | 상품 규격 정보 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_goodsskulist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

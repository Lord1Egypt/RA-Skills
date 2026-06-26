---
name: gds_u_goods
description: "단일 상품의 전체 상세 정보 조회 (사용자측).
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsk0r$om2djsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】result 포함:
- 기본: goods_id, goods_sn, goods_name, goods_desc, sale_price, currency_symbol
- 로컬 가격: local_sale_price, local_currency_symbol
- 통계: view_count, stock_count, least_buy_num, limit_buy_num
- 매장: store_id, store_name
- 이미지 갤러리: goods_gallery [{ goods_thumb_img, goods_big_img, goods_source_img }]
- 규격: goods_skus [{ sku_id, sale_price, stock_count, goods_specs }]
- 속성: goods_attrs
【주의】이미지 경로는 \"az7/gd/xxx.webp\" 와 같은 상대 경로이며, 이미지 CDN 도메인을 결합해야 합니다."
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 상세 조회[사용자]

단일 상품의 전체 상세 정보 조회 (사용자측).
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsk0r$om2djsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】result 포함:
- 기본: goods_id, goods_sn, goods_name, goods_desc, sale_price, currency_symbol
- 로컬 가격: local_sale_price, local_currency_symbol
- 통계: view_count, stock_count, least_buy_num, limit_buy_num
- 매장: store_id, store_name
- 이미지 갤러리: goods_gallery [{ goods_thumb_img, goods_big_img, goods_source_img }]
- 규격: goods_skus [{ sku_id, sale_price, stock_count, goods_specs }]
- 속성: goods_attrs
【주의】이미지 경로는 "az7/gd/xxx.webp" 와 같은 상대 경로이며, 이미지 CDN 도메인을 결합해야 합니다.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_goods` |
| Display Name | 상품 상세 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_goods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

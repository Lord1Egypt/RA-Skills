---
name: gds_m_goodseditinfo
description: "상품 편집 상세 정보를 조회합니다 (폼 채우기용). ver 버전 번호 (낙관적 락) 포함하여 반환합니다.
【사전 조건】판매자 access_token + goods_id 필요 (m_storegoodslist에서 획득).
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsk0r$dh3hjsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】전체 상품 정보:
{ goods_id, goods_class_cascade_id, goods_name, sale_price, stock_count, ver,
  goods_gallery: [{ goods_big_img, goods_thumb_img, goods_source_img, video_url, img_type }],
  goods_skus: [{ sku_id, sale_price, stock_count, goods_specs: [...] }],
  goods_attrs, goods_detail_gallery, ... }"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 상품 편집 상세 정보 조회[판매자]

상품 편집 상세 정보를 조회합니다 (폼 채우기용). ver 버전 번호 (낙관적 락) 포함하여 반환합니다.
【사전 조건】판매자 access_token + goods_id 필요 (m_storegoodslist에서 획득).
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsk0r$dh3hjsb').toUpperCase()
3. GET ?goods_id=상품ID
【응답】전체 상품 정보:
{ goods_id, goods_class_cascade_id, goods_name, sale_price, stock_count, ver,
  goods_gallery: [{ goods_big_img, goods_thumb_img, goods_source_img, video_url, img_type }],
  goods_skus: [{ sku_id, sale_price, stock_count, goods_specs: [...] }],
  goods_attrs, goods_detail_gallery, ... }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodseditinfo` |
| Display Name | 상품 편집 상세 정보 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodseditinfo` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

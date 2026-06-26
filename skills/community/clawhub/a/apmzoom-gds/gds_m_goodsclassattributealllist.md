---
name: gds_m_goodsclassattributealllist
description: "상품 카테고리 ID에 따라 모든 속성 목록을 조회합니다.
【사전 조건】판매자 access_token + goods_class_id 필요 (m_goodsclasslist에서 리프 카테고리 획득).
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsk@jkbnehjsb').toUpperCase()
3. GET ?goods_class_id=카테고리ID
【응답】속성 배열:
[{ attribute_id, attribute_name, attribute_values: [{ value_id, value_name }] }]"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 상품 카테고리 속성 목록 조회[판매자]

상품 카테고리 ID에 따라 모든 속성 목록을 조회합니다.
【사전 조건】판매자 access_token + goods_class_id 필요 (m_goodsclasslist에서 리프 카테고리 획득).
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsk@jkbnehjsb').toUpperCase()
3. GET ?goods_class_id=카테고리ID
【응답】속성 배열:
[{ attribute_id, attribute_name, attribute_values: [{ value_id, value_name }] }]

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodsclassattributealllist` |
| Display Name | 상품 카테고리 속성 목록 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodsclassattributealllist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

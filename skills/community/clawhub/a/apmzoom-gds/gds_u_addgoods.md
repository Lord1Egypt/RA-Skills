---
name: gds_u_addgoods
description: "사용자 셀프 추가 결제 시나리오에서 상품을 신규 등록합니다.
【사전 조건】
- 사용자 access_token 필요
- store_id 및 merchant_id 필요 (상품 상세에서 획득)
- goods_class_cascade_id 필요 (u_goodsclasslist 에서 획득)
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('asPtem$asldk').toUpperCase()
3. POST JSON: { store_id, merchant_id, goods_class_cascade_id, sale_price, cart_memo, goods_gallery }
   - goods_gallery: 1~5장 이미지
   - goods_class_cascade_id: 형식 \"1-2-3\", 최하위 단계까지 선택"
version: 1.0.0
category: 상품 관리-사용자
permission_level: write
enabled: true
is_public: false
---

# 상품 정보 추가[셀프 추가 결제]

사용자 셀프 추가 결제 시나리오에서 상품을 신규 등록합니다.
【사전 조건】
- 사용자 access_token 필요
- store_id 및 merchant_id 필요 (상품 상세에서 획득)
- goods_class_cascade_id 필요 (u_goodsclasslist 에서 획득)
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('asPtem$asldk').toUpperCase()
3. POST JSON: { store_id, merchant_id, goods_class_cascade_id, sale_price, cart_memo, goods_gallery }
   - goods_gallery: 1~5장 이미지
   - goods_class_cascade_id: 형식 "1-2-3", 최하위 단계까지 선택

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_addgoods` |
| Display Name | 상품 정보 추가[셀프 추가 결제] |
| Method | `POST` |
| Endpoint | `/gds/app/u_addgoods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

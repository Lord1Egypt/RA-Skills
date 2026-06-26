---
name: gds_u_delgoods
description: "사용자가 셀프 추가 결제 상품을 삭제합니다 (일괄 처리 지원).
【사전 조건】사용자 access_token + goods_ids 필요 (u_selfgoodslist 에서 획득).
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsn9dJ^wqjsb').toUpperCase()
3. POST JSON: { goods_ids: [상품ID1, 상품ID2, ...] }"
version: 1.0.0
category: 상품 관리-사용자
permission_level: write
enabled: true
is_public: false
---

# 상품 정보 삭제[사용자]

사용자가 셀프 추가 결제 상품을 삭제합니다 (일괄 처리 지원).
【사전 조건】사용자 access_token + goods_ids 필요 (u_selfgoodslist 에서 획득).
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsn9dJ^wqjsb').toUpperCase()
3. POST JSON: { goods_ids: [상품ID1, 상품ID2, ...] }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_delgoods` |
| Display Name | 상품 정보 삭제[사용자] |
| Method | `POST` |
| Endpoint | `/gds/app/u_delgoods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

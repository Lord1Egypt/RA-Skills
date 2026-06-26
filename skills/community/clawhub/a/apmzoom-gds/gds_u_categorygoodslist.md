---
name: gds_u_categorygoodslist
description: "카테고리별 상품 목록 조회 (사용자측, 커서 페이지네이션).
【사전 조건】
- 사용자 access_token 필요
- class_id 필요 (u_goodsclasslist 에서 카테고리 트리의 goods_class_id 획득)
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?class_id=카테고리ID&page_size=20&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】커서 페이지네이션, u_recommendgoodslist 와 동일."
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 카테고리별 상품 목록 조회[사용자]

카테고리별 상품 목록 조회 (사용자측, 커서 페이지네이션).
【사전 조건】
- 사용자 access_token 필요
- class_id 필요 (u_goodsclasslist 에서 카테고리 트리의 goods_class_id 획득)
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?class_id=카테고리ID&page_size=20&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】커서 페이지네이션, u_recommendgoodslist 와 동일.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_categorygoodslist` |
| Display Name | 상품 카테고리별 상품 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_categorygoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

---
name: gds_u_storegoodslist
description: "지정 매장의 상품 목록 조회 (사용자측, 커서 페이지네이션).
【사전 조건】사용자 access_token + store_id 필요 (상품 상세의 store_id 필드에서 획득).
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?store_id=매장ID&page_size=20&class_id=0&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】커서 페이지네이션, u_recommendgoodslist 와 동일."
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 매장 상품 목록 조회[사용자]

지정 매장의 상품 목록 조회 (사용자측, 커서 페이지네이션).
【사전 조건】사용자 access_token + store_id 필요 (상품 상세의 store_id 필드에서 획득).
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?store_id=매장ID&page_size=20&class_id=0&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】커서 페이지네이션, u_recommendgoodslist 와 동일.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_storegoodslist` |
| Display Name | 매장 상품 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_storegoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

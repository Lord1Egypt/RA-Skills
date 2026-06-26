---
name: gds_u_similargoodslist
description: "상품 ID 기반 유사 추천 상품 목록 조회.
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?goods_id=상품ID&store_id=매장ID&page_size=20&last_update_time=0"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 유사 상품 목록 조회[사용자]

상품 ID 기반 유사 추천 상품 목록 조회.
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?goods_id=상품ID&store_id=매장ID&page_size=20&last_update_time=0

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_similargoodslist` |
| Display Name | 유사 상품 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_similargoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

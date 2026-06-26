---
name: gds_u_dategoodslist
description: "날짜별 당일 신상품 목록 조회.
【사전 조건】사용자 access_token + 날짜 필요 (u_datelist 에서 획득).
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?date=2024-01-01&page_size=20&class_id=0&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】u_recommendgoodslist 와 동일, 커서 페이지네이션."
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 일자별 신상품 목록 조회[사용자]

날짜별 당일 신상품 목록 조회.
【사전 조건】사용자 access_token + 날짜 필요 (u_datelist 에서 획득).
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?date=2024-01-01&page_size=20&class_id=0&min_price=0&max_price=0&order_mark=0&last_update_time=0&collect_count=0
【페이지네이션】u_recommendgoodslist 와 동일, 커서 페이지네이션.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_dategoodslist` |
| Display Name | 일자별 신상품 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_dategoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

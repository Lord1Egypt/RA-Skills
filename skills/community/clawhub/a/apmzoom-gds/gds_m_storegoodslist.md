---
name: gds_m_storegoodslist
description: "판매자 상품 목록을 페이지 단위로 조회합니다 (커서 페이지네이션).
【사전 조건】판매자 access_token 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('jsm6y$dh3hjsb').toUpperCase()
3. GET ?page_size=20&mark=1
【파라미터】
- mark: 1=판매 중 2=진열 대기 3=할인 중
- page_size: 페이지당 개수
【페이지네이션 방식】커서 페이지네이션, 이전 페이지 마지막 데이터의 필드를 다음 페이지 시작점으로 사용
【응답】상품 배열:
[{ goods_id, goods_name, goods_thumb_img, sale_price, stock_count, is_sell, discount_percent, ... }]"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 판매자 상품 목록 조회

판매자 상품 목록을 페이지 단위로 조회합니다 (커서 페이지네이션).
【사전 조건】판매자 access_token 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('jsm6y$dh3hjsb').toUpperCase()
3. GET ?page_size=20&mark=1
【파라미터】
- mark: 1=판매 중 2=진열 대기 3=할인 중
- page_size: 페이지당 개수
【페이지네이션 방식】커서 페이지네이션, 이전 페이지 마지막 데이터의 필드를 다음 페이지 시작점으로 사용
【응답】상품 배열:
[{ goods_id, goods_name, goods_thumb_img, sale_price, stock_count, is_sell, discount_percent, ... }]

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_storegoodslist` |
| Display Name | 판매자 상품 목록 조회 |
| Method | `GET` |
| Endpoint | `/gds/app/m_storegoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

---
name: gds_u_recommendgoodslist
description: "추천 상품 목록 (사용자측에서 가장 자주 사용되는 목록 인터페이스, 커서 페이지네이션).
【사전 조건】먼저 u_login_account 를 통해 로그인하여 사용자 access_token 을 획득해야 합니다.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. authcode 설정: \"HH \" + 사용자 access_token
3. sign 계산: MD5('jsm6y$nu5wjsb').toUpperCase()
4. GET 파라미터:
   - page_size=20 (페이지당 개수)
   - search_mark=0, class_id=0, min_price=0, max_price=0, order_mark=0 (첫 페이지 기본값)
   - last_update_time=0, collect_count=0 (첫 페이지는 0 전달)
【페이지네이션 방식】커서 페이지네이션:
- 첫 페이지: last_update_time=0, collect_count=0
- 다음 페이지: 이전 페이지 마지막 데이터의 last_update_time 및 collect_count 전달
- code=101 또는 빈 배열 반환은 더 이상 데이터가 없음을 의미
【응답】result 배열:
[{ goods_id, goods_name, goods_thumb_img, sale_price, currency_symbol, local_sale_price, local_currency_symbol, gallery_count, view_count, collect_count, discount_percent, last_update_time, store_id, store_name }]"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 목록·범용[사용자]

추천 상품 목록 (사용자측에서 가장 자주 사용되는 목록 인터페이스, 커서 페이지네이션).
【사전 조건】먼저 u_login_account 를 통해 로그인하여 사용자 access_token 을 획득해야 합니다.
【호출 절차】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. authcode 설정: "HH " + 사용자 access_token
3. sign 계산: MD5('jsm6y$nu5wjsb').toUpperCase()
4. GET 파라미터:
   - page_size=20 (페이지당 개수)
   - search_mark=0, class_id=0, min_price=0, max_price=0, order_mark=0 (첫 페이지 기본값)
   - last_update_time=0, collect_count=0 (첫 페이지는 0 전달)
【페이지네이션 방식】커서 페이지네이션:
- 첫 페이지: last_update_time=0, collect_count=0
- 다음 페이지: 이전 페이지 마지막 데이터의 last_update_time 및 collect_count 전달
- code=101 또는 빈 배열 반환은 더 이상 데이터가 없음을 의미
【응답】result 배열:
[{ goods_id, goods_name, goods_thumb_img, sale_price, currency_symbol, local_sale_price, local_currency_symbol, gallery_count, view_count, collect_count, discount_percent, last_update_time, store_id, store_name }]

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_recommendgoodslist` |
| Display Name | 상품 목록·범용[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_recommendgoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

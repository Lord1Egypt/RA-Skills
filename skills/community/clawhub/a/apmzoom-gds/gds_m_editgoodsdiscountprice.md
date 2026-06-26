---
name: gds_m_editgoodsdiscountprice
description: "상품의 고정 할인가를 수정합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('as0yd@e3ldk').toUpperCase()
3. POST { goods_id, discount_price, ver }
【파라미터】discount_price: 고정 할인가 (>0)
【주의】반드시 ver 버전 번호를 전달해야 함"
version: 1.0.0
category: 상품 관리-판매자
permission_level: write
enabled: true
is_public: false
---

# 상품 할인 가격 수정[판매자]

상품의 고정 할인가를 수정합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('as0yd@e3ldk').toUpperCase()
3. POST { goods_id, discount_price, ver }
【파라미터】discount_price: 고정 할인가 (>0)
【주의】반드시 ver 버전 번호를 전달해야 함

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_editgoodsdiscountprice` |
| Display Name | 상품 할인 가격 수정[판매자] |
| Method | `POST` |
| Endpoint | `/gds/app/m_editgoodsdiscountprice` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

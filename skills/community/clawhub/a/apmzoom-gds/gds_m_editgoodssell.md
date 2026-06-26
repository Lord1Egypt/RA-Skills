---
name: gds_m_editgoodssell
description: "상품 진열/미진열 상태를 전환합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('as0in@h3ldk').toUpperCase()
3. POST { goods_id, is_sell, ver }
【파라미터】is_sell: 0=미진열 1=진열
【주의】반드시 ver 버전 번호를 전달해야 함"
version: 1.0.0
category: 상품 관리-판매자
permission_level: write
enabled: true
is_public: false
---

# 상품 진열 상태 수정[판매자]

상품 진열/미진열 상태를 전환합니다.
【사전 조건】판매자 access_token + goods_id + ver 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('as0in@h3ldk').toUpperCase()
3. POST { goods_id, is_sell, ver }
【파라미터】is_sell: 0=미진열 1=진열
【주의】반드시 ver 버전 번호를 전달해야 함

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_editgoodssell` |
| Display Name | 상품 진열 상태 수정[판매자] |
| Method | `POST` |
| Endpoint | `/gds/app/m_editgoodssell` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

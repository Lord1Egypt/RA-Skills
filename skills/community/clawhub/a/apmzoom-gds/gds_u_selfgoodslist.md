---
name: gds_u_selfgoodslist
description: "사용자 셀프 추가 결제 상품 목록을 조회합니다.
【사전 조건】사용자 access_token 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?page_size=20"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 셀프 추가 결제 상품 목록

사용자 셀프 추가 결제 상품 목록을 조회합니다.
【사전 조건】사용자 access_token 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?page_size=20

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_selfgoodslist` |
| Display Name | 셀프 추가 결제 상품 목록 |
| Method | `GET` |
| Endpoint | `/gds/app/u_selfgoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

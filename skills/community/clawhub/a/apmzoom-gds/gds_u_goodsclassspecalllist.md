---
name: gds_u_goodsclassspecalllist
description: "상품 카테고리 규격 목록 조회 (사용자측).
【사전 조건】사용자 access_token + goods_class_id 필요 (u_goodsclasslist 에서 획득).
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsk@jie4ehjsb').toUpperCase()
3. GET ?goods_class_id=카테고리ID"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 카테고리 규격 목록 조회[사용자]

상품 카테고리 규격 목록 조회 (사용자측).
【사전 조건】사용자 access_token + goods_class_id 필요 (u_goodsclasslist 에서 획득).
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsk@jie4ehjsb').toUpperCase()
3. GET ?goods_class_id=카테고리ID

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_goodsclassspecalllist` |
| Display Name | 상품 카테고리 규격 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_goodsclassspecalllist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

---
name: gds_m_goodsmakeaddresslist
description: "상품 원산지 목록을 조회합니다.
【사전 조건】판매자 access_token 필요.
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('js0ntu$wphjsb').toUpperCase()
3. GET 요청, query 파라미터 없음
【응답】원산지 배열:
[{ address_id, address_name }]
현재 선택 가능한 값: 1=한국, 2=중국, 3=기타"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 원산지 목록 조회[판매자]

상품 원산지 목록을 조회합니다.
【사전 조건】판매자 access_token 필요.
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('js0ntu$wphjsb').toUpperCase()
3. GET 요청, query 파라미터 없음
【응답】원산지 배열:
[{ address_id, address_name }]
현재 선택 가능한 값: 1=한국, 2=중국, 3=기타

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodsmakeaddresslist` |
| Display Name | 원산지 목록 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodsmakeaddresslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

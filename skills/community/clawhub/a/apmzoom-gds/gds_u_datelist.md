---
name: gds_u_datelist
description: "일자별 신상품이 등록된 날짜 목록을 조회합니다.
【사전 조건】사용자 access_token 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$bie5jsb').toUpperCase()
3. GET ?page_size=20&date=0 (첫 페이지는 0 전달, 다음 페이지는 이전 페이지 마지막의 날짜 타임스탬프 전달)"
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 일자별 신상품 날짜 목록 조회[사용자]

일자별 신상품이 등록된 날짜 목록을 조회합니다.
【사전 조건】사용자 access_token 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$bie5jsb').toUpperCase()
3. GET ?page_size=20&date=0 (첫 페이지는 0 전달, 다음 페이지는 이전 페이지 마지막의 날짜 타임스탬프 전달)

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_datelist` |
| Display Name | 일자별 신상품 날짜 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_datelist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

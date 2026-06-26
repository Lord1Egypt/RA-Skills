---
name: gds_u_searchgoodslist
description: "키워드로 상품 목록 검색 (서버측 검색, 중국어/한국어 키워드 지원).
【사전 조건】먼저 u_login_account 를 통해 로그인하여 사용자 access_token 을 획득해야 합니다.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?keyword=검색어&page_size=20&last_update_time=0
【페이지네이션】last_update_time 커서 페이지네이션.
【응답】u_recommendgoodslist 와 동일한 형식의 상품 배열."
version: 1.0.0
category: 상품 관리-사용자
permission_level: read
enabled: true
is_public: false
---

# 상품 검색 목록 조회[사용자]

키워드로 상품 목록 검색 (서버측 검색, 중국어/한국어 키워드 지원).
【사전 조건】먼저 u_login_account 를 통해 로그인하여 사용자 access_token 을 획득해야 합니다.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nu5wjsb').toUpperCase()
3. GET ?keyword=검색어&page_size=20&last_update_time=0
【페이지네이션】last_update_time 커서 페이지네이션.
【응답】u_recommendgoodslist 와 동일한 형식의 상품 배열.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_searchgoodslist` |
| Display Name | 상품 검색 목록 조회[사용자] |
| Method | `GET` |
| Endpoint | `/gds/app/u_searchgoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

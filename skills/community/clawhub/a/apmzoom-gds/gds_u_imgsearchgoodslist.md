---
name: gds_u_imgsearchgoodslist
description: "이미지로 유사 상품 검색 (사진으로 동일 상품 찾기).
【사전 조건】사용자 access_token + 이미지 base64 데이터 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsm6y$nr3wjsb').toUpperCase()
3. POST JSON: { img: \"base64 문자열\" }
   - img: \"data:image/...;
base64,\" 헤더가 없는 순수 base64
   - 권장 이미지 크기: 360x480"
version: 1.0.0
category: 상품 관리-사용자
permission_level: write
enabled: true
is_public: false
---

# 이미지 상품 검색 목록[사용자]

이미지로 유사 상품 검색 (사진으로 동일 상품 찾기).
【사전 조건】사용자 access_token + 이미지 base64 데이터 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsm6y$nr3wjsb').toUpperCase()
3. POST JSON: { img: "base64 문자열" }
   - img: "data:image/...;
base64," 헤더가 없는 순수 base64
   - 권장 이미지 크기: 360x480

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_imgsearchgoodslist` |
| Display Name | 이미지 상품 검색 목록[사용자] |
| Method | `POST` |
| Endpoint | `/gds/app/u_imgsearchgoodslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

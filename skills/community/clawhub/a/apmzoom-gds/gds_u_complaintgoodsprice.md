---
name: gds_u_complaintgoodsprice
description: "사용자가 상품 가격 이상에 대해 신고합니다.
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: \"HH \" + 사용자 token
2. sign: MD5('jsneuntyjsb').toUpperCase()
3. POST JSON: { goods_id, complaint_img }
   - complaint_img: 신고 스크린샷의 base64 또는 URL"
version: 1.0.0
category: 상품 관리-사용자
permission_level: write
enabled: true
is_public: false
---

# 상품 가격 신고[사용자]

사용자가 상품 가격 이상에 대해 신고합니다.
【사전 조건】사용자 access_token + goods_id 필요.
【호출 절차】
1. authcode: "HH " + 사용자 token
2. sign: MD5('jsneuntyjsb').toUpperCase()
3. POST JSON: { goods_id, complaint_img }
   - complaint_img: 신고 스크린샷의 base64 또는 URL

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_u_complaintgoodsprice` |
| Display Name | 상품 가격 신고[사용자] |
| Method | `POST` |
| Endpoint | `/gds/app/u_complaintgoodsprice` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-사용자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

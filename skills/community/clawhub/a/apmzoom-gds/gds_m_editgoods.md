---
name: gds_m_editgoods
description: "상품의 전체 정보를 수정합니다.
【사전 조건】
- 판매자 access_token 필요
- goods_id 및 ver 필요 (m_goodseditinfo에서 획득, ver은 낙관적 락 버전 번호)
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token
2. sign: MD5('as0imre$asldk').toUpperCase()
3. POST JSON body (m_addgoods와 유사하며, 추가로 goods_id 및 ver 필요)
【주의】
- 반드시 ver 버전 번호 (낙관적 락)를 전달하여 동시성 덮어쓰기 방지
- goods_gallery 각 항목에 img_type:1 포함 필요
- video_url 반드시 전달 (빈 문자열 가능)"
version: 1.0.0
category: 상품 관리-판매자
permission_level: write
enabled: true
is_public: false
---

# 상품 정보 수정[판매자]

상품의 전체 정보를 수정합니다.
【사전 조건】
- 판매자 access_token 필요
- goods_id 및 ver 필요 (m_goodseditinfo에서 획득, ver은 낙관적 락 버전 번호)
【호출 흐름】
1. authcode: "HH " + 판매자 access_token
2. sign: MD5('as0imre$asldk').toUpperCase()
3. POST JSON body (m_addgoods와 유사하며, 추가로 goods_id 및 ver 필요)
【주의】
- 반드시 ver 버전 번호 (낙관적 락)를 전달하여 동시성 덮어쓰기 방지
- goods_gallery 각 항목에 img_type:1 포함 필요
- video_url 반드시 전달 (빈 문자열 가능)

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_editgoods` |
| Display Name | 상품 정보 수정[판매자] |
| Method | `POST` |
| Endpoint | `/gds/app/m_editgoods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

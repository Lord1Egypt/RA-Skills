---
name: gds_m_goodsclasslist
description: "판매자 측 상품 카테고리 목록을 조회합니다.
【사전 조건】먼저 m_login_account를 통해 로그인하여 판매자 access_token을 획득해야 합니다.
【호출 흐름】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. authcode 설정: \"HH \" + 판매자 access_token (반드시 \"HH \" 접두사 필요, 그렇지 않으면 401 반환)
3. sign 계산: MD5('jskdn$dh3hjsb').toUpperCase() (고정 솔트값, 파라미터 결합 안 함)
4. GET 요청, query 파라미터 없음
【응답】카테고리 트리 배열:
[{ goods_class_id, goods_class_name, is_have_child, ls_child: [하위 카테고리...] }]"
version: 1.0.0
category: 상품 관리-판매자
permission_level: read
enabled: true
is_public: false
---

# 상품 카테고리 목록 조회[판매자]

판매자 측 상품 카테고리 목록을 조회합니다.
【사전 조건】먼저 m_login_account를 통해 로그인하여 판매자 access_token을 획득해야 합니다.
【호출 흐름】
1. 요청 헤더 구성: v=7.0.1, p=1, t=현재 초 단위 타임스탬프, lang=zh-cn
2. authcode 설정: "HH " + 판매자 access_token (반드시 "HH " 접두사 필요, 그렇지 않으면 401 반환)
3. sign 계산: MD5('jskdn$dh3hjsb').toUpperCase() (고정 솔트값, 파라미터 결합 안 함)
4. GET 요청, query 파라미터 없음
【응답】카테고리 트리 배열:
[{ goods_class_id, goods_class_name, is_have_child, ls_child: [하위 카테고리...] }]

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_goodsclasslist` |
| Display Name | 상품 카테고리 목록 조회[판매자] |
| Method | `GET` |
| Endpoint | `/gds/app/m_goodsclasslist` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | read |
| Public | No |
| Version | 1.0.0 |

---
name: gds_m_addgoods
description: "판매자가 상품을 신규 등록합니다.
【사전 조건】
- 판매자 access_token 필요 (m_login_account 로그인을 통해 획득)
- goods_class_cascade_id 필요 (m_goodsclasslist에서 카테고리 트리를 가져와 1-6-7 형식으로 조합)
- make_address_id 필요 (m_goodsmakeaddresslist에서 원산지 ID 획득)
- 최소 1장의 상품 이미지 필요 (먼저 이미지 업로드 인터페이스를 통해 URL 획득)
【호출 흐름】
1. authcode: \"HH \" + 판매자 access_token (반드시 \"HH \" 접두사 필요)
2. sign: MD5('as0jusem$asldk').toUpperCase()
3. POST JSON body
【요청 본문 주요 필드】
- goods_class_cascade_id: \"1-6-7\" 형식의 카테고리 캐스케이드 ID
- goods_name: 상품명
- sale_price: 판매가
- stock_count: 재고
- make_address_id: 원산지 ID (1=한국 2=중국 3=기타)
- goods_detail: 상품 소개 (필수, 없으면 422)
- goods_gallery: 상품 이미지 갤러리 배열 (최소 1개), 각 항목 형식:
  { \"goods_big_img\": \"이미지 URL\", \"goods_thumb_img\": \"이미지 URL\", \"goods_source_img\": \"이미지 URL\", \"video_url\": \"\", \"img_type\": 1 }
  ⚠️ img_type은 반드시 1을 전달해야 하며, 그렇지 않으면 103 \"이미지 또는 동영상을 업로드해 주세요\" 반환
  ⚠️ video_url은 반드시 전달해야 하며 (빈 문자열 가능), 그렇지 않으면 422
- goods_skus: SKU 배열 (빈 [] 가능)
- goods_attrs: 속성 배열 (빈 [] 가능)
- goods_detail_gallery: 상세 이미지 갤러리 (빈 [] 가능)
- is_sell: 0=미진열 1=즉시 진열
【성공 응답】{ \"code\": 100, \"message\": \"발행 성공\" }"
version: 1.0.0
category: 상품 관리-판매자
permission_level: write
enabled: true
is_public: false
---

# 상품 정보 추가[판매자]

판매자가 상품을 신규 등록합니다.
【사전 조건】
- 판매자 access_token 필요 (m_login_account 로그인을 통해 획득)
- goods_class_cascade_id 필요 (m_goodsclasslist에서 카테고리 트리를 가져와 1-6-7 형식으로 조합)
- make_address_id 필요 (m_goodsmakeaddresslist에서 원산지 ID 획득)
- 최소 1장의 상품 이미지 필요 (먼저 이미지 업로드 인터페이스를 통해 URL 획득)
【호출 흐름】
1. authcode: "HH " + 판매자 access_token (반드시 "HH " 접두사 필요)
2. sign: MD5('as0jusem$asldk').toUpperCase()
3. POST JSON body
【요청 본문 주요 필드】
- goods_class_cascade_id: "1-6-7" 형식의 카테고리 캐스케이드 ID
- goods_name: 상품명
- sale_price: 판매가
- stock_count: 재고
- make_address_id: 원산지 ID (1=한국 2=중국 3=기타)
- goods_detail: 상품 소개 (필수, 없으면 422)
- goods_gallery: 상품 이미지 갤러리 배열 (최소 1개), 각 항목 형식:
  { "goods_big_img": "이미지 URL", "goods_thumb_img": "이미지 URL", "goods_source_img": "이미지 URL", "video_url": "", "img_type": 1 }
  ⚠️ img_type은 반드시 1을 전달해야 하며, 그렇지 않으면 103 "이미지 또는 동영상을 업로드해 주세요" 반환
  ⚠️ video_url은 반드시 전달해야 하며 (빈 문자열 가능), 그렇지 않으면 422
- goods_skus: SKU 배열 (빈 [] 가능)
- goods_attrs: 속성 배열 (빈 [] 가능)
- goods_detail_gallery: 상세 이미지 갤러리 (빈 [] 가능)
- is_sell: 0=미진열 1=즉시 진열
【성공 응답】{ "code": 100, "message": "발행 성공" }

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `gds_m_addgoods` |
| Display Name | 상품 정보 추가[판매자] |
| Method | `POST` |
| Endpoint | `/gds/app/m_addgoods` |
| Base URL | `https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com` |
| Category | 상품 관리-판매자 |
| Permission | write |
| Public | No |
| Version | 1.0.0 |

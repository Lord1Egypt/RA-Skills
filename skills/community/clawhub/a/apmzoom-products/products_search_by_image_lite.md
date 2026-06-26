---
name: products_search_by_image_lite
description: "상품 라이브러리 이미지 검색 간소화 인터페이스를 사용하여 이미지로 유사 상품을 검색합니다. 표준 버전에 비해 응답에서 가격 / 재고 / 판매 필드를 제거하고, 중첩 객체는 판매자 이름과 층/호수만 유지합니다.
【Base URL】https://worker.apmzoom.ai
【인터페이스】POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite
【인증】공개 인터페이스, 인증 불필요.
【Content-Type】application/json

【요청 본문】
{
  \"image_url\": \"https://...\",
  \"limit\": 20,
  \"category_l1_id\": 1,
  \"embedding\": \"default\"
}

【필드 설명】
- image_url: 필수. 공개적으로 접근 가능한 이미지 URL.
- limit: 선택. 반환 개수, 범위 1-100, 기본값 20.
- category_l1_id: 선택. 1차 카테고리 필터.
- embedding: 선택. 벡터 모델, \"default\" 및 \"fashion\" 지원, 기본값 \"default\".

【curl 예제】
curl -X POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite \
  -H \"Content-Type: application/json\" \
  -d '{\"image_url\":\"https://image.apmzoom.ai/products/main/19361.jpg\",\"limit\":20}'

【반환】
{
  \"success\": true,
  \"data\": {
    \"image_url\": \"https://...\",
    \"count\": 10,
    \"items\": [
      {
        \"id\": 123, \"goods_sn\": \"...\", \"name_i18n\": {...},
        \"category_l1_id\": 1, \"main_image_big\": \"...\", \"main_image_thumb\": \"...\",
        \"brand_name\": \"...\", \"merchant_name\": \"...\", \"is_sell\": 1,
        \"score\": 0.87,
        \"merchant\": {\"merchant_name\": \"...\"},
        \"store\":    {\"layer_id\": \"3F\", \"door_no\": \"A-12\"}
      }
    ]
  }
}

【설명】
- default: 기본 이미지 벡터 컬럼 image_embedding 사용.
- fashion: 의류 전용 이미지 벡터 컬럼 image_embedding_fashion 사용.
- 결과는 시각적 유사도 높은 순으로 정렬되며, items 내에는 가격 / 재고 / 평점 / 판매량 필드가 포함되지 않습니다."
version: 1.0.0
category: 지식 베이스
subcategory: 
permission_level: read
enabled: true
is_public: true
---

# 이미지 검색-간소화(상품 라이브러리)

상품 라이브러리 이미지 검색 간소화 인터페이스를 사용하여 이미지로 유사 상품을 검색합니다. 표준 버전에 비해 응답에서 가격 / 재고 / 판매 필드를 제거하고, 중첩 객체는 판매자 이름과 층/호수만 유지합니다.
【Base URL】https://worker.apmzoom.ai
【인터페이스】POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite
【인증】공개 인터페이스, 인증 불필요.
【Content-Type】application/json

【요청 본문】
{
  "image_url": "https://...",
  "limit": 20,
  "category_l1_id": 1,
  "embedding": "default"
}

【필드 설명】
- image_url: 필수. 공개적으로 접근 가능한 이미지 URL.
- limit: 선택. 반환 개수, 범위 1-100, 기본값 20.
- category_l1_id: 선택. 1차 카테고리 필터.
- embedding: 선택. 벡터 모델, "default" 및 "fashion" 지원, 기본값 "default".

【curl 예제】
curl -X POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://image.apmzoom.ai/products/main/19361.jpg","limit":20}'

【반환】
{
  "success": true,
  "data": {
    "image_url": "https://...",
    "count": 10,
    "items": [
      {
        "id": 123, "goods_sn": "...", "name_i18n": {...},
        "category_l1_id": 1, "main_image_big": "...", "main_image_thumb": "...",
        "brand_name": "...", "merchant_name": "...", "is_sell": 1,
        "score": 0.87,
        "merchant": {"merchant_name": "..."},
        "store":    {"layer_id": "3F", "door_no": "A-12"}
      }
    ]
  }
}

【설명】
- default: 기본 이미지 벡터 컬럼 image_embedding 사용.
- fashion: 의류 전용 이미지 벡터 컬럼 image_embedding_fashion 사용.
- 결과는 시각적 유사도 높은 순으로 정렬되며, items 내에는 가격 / 재고 / 평점 / 판매량 필드가 포함되지 않습니다.

## Quick Reference

| Field | Value |
| ----- | ----- |
| Name | `products_search_by_image_lite` |
| Display Name | 이미지 검색-간소화(상품 라이브러리) |
| Method | `POST` |
| Endpoint | `/api/v1/products/search/by-image-lite` |
| Base URL | `https://worker.apmzoom.ai` |
| Category | 지식 베이스 |
| Permission | read |
| Public | Yes |
| Version | 1.0.1 |

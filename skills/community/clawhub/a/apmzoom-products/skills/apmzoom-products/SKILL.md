---
name: APM 상품 라이브러리 검색 API
description: "APM 상품 라이브러리의 공개 검색 API 모음 (인증 불필요). 자연어 텍스트 검색과 이미지 유사도 검색을 지원하며, 벡터 임베딩 기반으로 유사 상품을 반환합니다. Lite 응답 포맷은 가격/재고/판매 필드를 제외하고 판매자명과 동대문 매장 층/호수 정보만 제공합니다. Base URL: https://worker.apmzoom.ai. 엔드포인트: POST /api/v1/products/search/by-text-lite, POST /api/v1/products/search/by-image-lite. 카테고리 필터(category_l1_id)와 의류 전용 임베딩 모델(fashion) 지원."
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/apmzoom-ai/apm-skills
---

# APM 상품 라이브러리 검색 API

APM 상품 라이브러리의 공개 검색 API 모음 (인증 불필요). 자연어/이미지로 동대문 상품을 벡터 유사도 검색합니다.

## 공통 규약

- **Base URL**: `https://worker.apmzoom.ai` (Cloudflare Worker)
- **인증**: 공개 인터페이스, 인증 헤더 불필요 (`is_public: true`)
- **Method**: `POST`
- **Content-Type**: `application/json`
- **응답 포맷 (lite)**: 가격 / 재고 / 평점 / 판매량 필드 **미포함**. 판매자 정보는 `merchant_name`과 매장 층/호수(`layer_id`, `door_no`)만 유지
- **정렬**: 벡터 유사도(`score`) 내림차순
- **카테고리 필터**: `category_l1_id` (1차 카테고리)
- **반환 개수**: `limit` (1-100, 기본 20)

## 엔드포인트 목록 (2개)

- [`products_search_by_text_lite`](products_search_by_text_lite.md) — **텍스트 검색 - 간소화** · `POST https://worker.apmzoom.ai/api/v1/products/search/by-text-lite`
  - 자연어 쿼리(예: "검은색 패딩")를 `desc_embedding` 컬럼에 인코딩하여 검색
- [`products_search_by_image_lite`](products_search_by_image_lite.md) — **이미지 검색 - 간소화** · `POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite`
  - 이미지 URL 기반 유사 상품 검색
  - `embedding` 옵션: `default` (image_embedding) 또는 `fashion` (image_embedding_fashion, 의류 전용)

## 호출 예시

```bash
# 텍스트 검색
curl -X POST https://worker.apmzoom.ai/api/v1/products/search/by-text-lite \
  -H "Content-Type: application/json" \
  -d '{"text":"검은색 패딩","limit":20,"category_l1_id":1}'

# 이미지 검색
curl -X POST https://worker.apmzoom.ai/api/v1/products/search/by-image-lite \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://image.apmzoom.ai/products/main/158236.jpg","limit":20,"embedding":"fashion"}'
```

## 사용 시나리오

- 에이전트가 사용자 발화("얇은 겉옷 추천")를 받아 텍스트 검색으로 후보 상품 목록 생성
- 업로드된 이미지로 동일/유사 상품 찾기 (스타일 매칭)
- 가격·재고 정보가 불필요한 추천/탐색 시나리오에 최적화된 경량 응답

## 관련 스킬

- 인증이 필요한 상품 관리 API: [`apmzoom-gds`](https://clawhub.ai/skills/apmzoom-gds)
- 로그인/토큰 발급: [`apmzoom-ids`](https://clawhub.ai/skills/apmzoom-ids)

원본 문서: https://github.com/apmzoom-ai/apm-skills

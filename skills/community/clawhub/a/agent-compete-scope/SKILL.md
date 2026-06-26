---
name: compete-scope
description: 경쟁사 포지셔닝 분석 및 화이트스페이스 도출 에이전트
version: 1.0.0
---

# 🔍 CompeteScope Agent

내 제품과 경쟁사들을 비교 분석하여 시장의 빈틈(Whitespace)과 차별화 전략을 제안합니다.

## Features
- **경쟁사 프로필:** 웹 검색을 통한 경쟁사 상세 프로필 자동 생성
- **비교 매트릭스:** 기능, 가격, 타겟 등 다차원 비교표 생성
- **전략 도출:** AI가 분석한 시장 기회 및 추천 전략 제공

## Usage
ACP Job Payload:
```json
{
  "my_product": "AI 마케팅 툴",
  "competitors": ["Competitor A", "Competitor B"]
}
```

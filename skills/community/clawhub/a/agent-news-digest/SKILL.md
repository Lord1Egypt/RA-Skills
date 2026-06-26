---
name: news-digest
description: 키워드 기반 뉴스 수집 및 3줄 요약 에이전트
version: 1.0.0
---

# 📰 NewsDigest Agent

Tavily 검색과 Groq(Llama 3.3) LLM을 활용하여 특정 주제에 대한 최신 뉴스를 수집하고, 중요도 순으로 정렬하여 3줄 요약을 제공하는 에이전트입니다.

## Features
- **키워드 검색:** Tavily API를 통한 실시간 웹 검색
- **AI 요약:** Llama 3.3 70B 모델을 활용한 고품질 한국어 요약
- **중요도 평가:** 뉴스 기사별 중요도 점수(1~5) 부여
- **브리핑 생성:** 전체 내용을 아우르는 마크다운 브리핑 제공

## Usage
ACP Job Payload:
```json
{
  "topic": "Bitcoin",
  "period": "1d",
  "max_items": 5
}
```

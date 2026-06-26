# 📰 NewsDigest Agent

키워드 기반 뉴스 수집 및 3줄 요약 에이전트입니다.

## Prerequisites
- **Groq API Key**: LLM (Llama 3.3)
- **Tavily API Key**: 웹 검색

## Setup
1. `cp .env.example .env`
2. `.env` 파일에 API 키 입력
3. `npm install`

## Usage
```bash
npm start
```

## Example Payload
```json
{
  "topic": "Bitcoin",
  "period": "1d",
  "max_items": 5
}
```

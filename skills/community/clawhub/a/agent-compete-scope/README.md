# 🔍 CompeteScope Agent

경쟁사 포지셔닝 분석 및 화이트스페이스 도출 에이전트입니다.

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
  "my_product": "AI 기반 마케팅 툴",
  "competitors": ["Competitor A", "Competitor B"],
  "focus": "all"
}
```

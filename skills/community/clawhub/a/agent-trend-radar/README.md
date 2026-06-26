# 📈 TrendRadar Agent

키워드 트렌드 신호 탐지 및 Rising/Peaking/Declining 분류 에이전트입니다.

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
  "keywords": ["AI Agent", "DeFi"],
  "timeframe": "7d",
  "region": "global"
}
```

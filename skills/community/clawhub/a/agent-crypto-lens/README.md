# 🪙 CryptoLens Agent

크립토 토큰 시장 동향 및 센티먼트 종합 분석 에이전트입니다.

## Prerequisites
- **Groq API Key**: LLM (Llama 3.3)
- **Tavily API Key**: 뉴스 검색
- **CoinGecko**: 무료 API 사용 (키 불필요)

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
  "token": "Bitcoin",
  "analysis_type": "full"
}
```

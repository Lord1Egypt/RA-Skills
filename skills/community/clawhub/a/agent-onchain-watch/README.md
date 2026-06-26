# 🔗 OnchainWatch Agent

지갑 및 컨트랙트 온체인 활동 모니터링 및 요약 에이전트입니다.

## Prerequisites
- **Groq API Key**: LLM (Llama 3.3)
- **Etherscan API Key**: 온체인 데이터 (필수)

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
  "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "chain": "ethereum"
}
```

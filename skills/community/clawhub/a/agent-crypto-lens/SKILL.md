---
name: crypto-lens
description: 크립토 토큰 시장 동향 및 센티먼트 종합 분석 에이전트
version: 1.0.0
---

# 🪙 CryptoLens Agent

CoinGecko 시장 데이터와 웹 뉴스를 결합하여 특정 토큰의 시장 상황과 투자 심리(Sentiment)를 분석합니다.

## Features
- **시장 데이터:** CoinGecko API를 통한 실시간 가격/변동률 조회
- **뉴스 분석:** 최신 뉴스 기반 호재/악재 파악
- **종합 점수:** 모멘텀, 센티먼트, 리스크 점수 산출

## Usage
ACP Job Payload:
```json
{
  "token": "Bitcoin",
  "analysis_type": "full"
}
```

---
name: trend-radar
description: 키워드 트렌드 신호 탐지 및 Rising/Peaking/Declining 분류 에이전트
version: 1.0.0
---

# 📈 TrendRadar Agent

멀티 키워드에 대한 웹 트렌드를 분석하여 'Rising', 'Peaking', 'Declining' 등의 신호를 탐지하는 에이전트입니다.

## Features
- **멀티 키워드:** 최대 5개 키워드 동시 분석
- **신호 탐지:** AI 기반 트렌드 사이클(상승/정점/하락) 판단
- **증거 수집:** 판단 근거가 되는 URL 링크 제공

## Usage
ACP Job Payload:
```json
{
  "keywords": ["AI Agent", "DeFi"],
  "timeframe": "7d",
  "region": "global"
}
```

---
name: onchain-watch
description: 지갑 및 컨트랙트 온체인 활동 모니터링 및 요약 에이전트
version: 1.0.0
---

# 🔗 OnchainWatch Agent

Etherscan API를 활용하여 특정 지갑의 잔액, 트랜잭션, 토큰 이동을 추적하고 리스크를 탐지합니다.

## Features
- **자산 추적:** ETH 잔액 및 ERC-20 토큰 이동 내역 조회
- **리스크 탐지:** 고액 송금, 이상 빈도 거래 등 자동 감지
- **요약 리포트:** 온체인 데이터를 이해하기 쉬운 마크다운으로 요약

## Usage
ACP Job Payload:
```json
{
  "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "chain": "ethereum"
}
```

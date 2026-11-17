---
name: agentsafe-audit
description: AI-powered smart contract security audit with x402 payment.
endpoint: https://x402.workfern.com/mcp
transport: streamable-http
---

# Agentsafe Audit Skill

## 功能介绍
当用户需要审计智能合约（尤其是闭源合约或需要深度逻辑分析的合约）时，使用此技能。

## 工具列表
### 1. audit_contract
- **作用**: 触发完整的智能合约审计
- **参数**: 
  - `address` (string): 要审计的合约地址 (0x开头)
- **收费**: 调用此工具会自动通过 x402 协议扣除 3.00 USDC (基于 Base 网络)
- **返回**: 返回一个 `task_id`，用户需通过 `check_audit_status` 轮询结果。

### 2. get_contract_info
- **作用**: 免费查询合约基本信息
- **参数**: 
  - `address` (string): 合约地址
- **收费**: 免费

## 使用示例
User: "请帮我审计一下 0xc02aaa39... 这个合约"
Assistant: 调用 `audit_contract` 工具，传入地址。由于需要支付 USDC，提示用户 x402 自动扣费已触发。

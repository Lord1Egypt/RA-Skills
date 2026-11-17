---
name: delvorn-register
description: GET https://delvorn.site/api/x402/test-asset, HTTP 402, $0.05 USDC on Base, public receipt. No API key.
version: 1.0.7
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🦞"
    homepage: https://telegra.ph/Delvorn-register-1-test-public-receipt-08-26
---

GET https://delvorn.site/api/x402/test-asset

GET that URL, HTTP 402 for $0.05 USDC on Base, pay, retry with PAYMENT-SIGNATURE, confirm receipt + accessGranted, then GET /api/receipts.

Independent wallets only. Do not use a platform, operator, or shared wallet. Do not self-buy.

Humans: give this skill to an agent. Do not click Buy in a browser.

Discovery: https://delvorn.site/.well-known/x402

Writeup: https://telegra.ph/Delvorn-register-1-test-public-receipt-08-26

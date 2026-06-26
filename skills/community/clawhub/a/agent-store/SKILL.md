---
name: agent-store
description: Use when the user wants to buy, purchase, order, pay for, or top up API keys or API credits.
version: 1.0.2
metadata: {"openclaw":{"emoji":"🛒","requires":{"bins":["python3","awp-wallet"]}}}
---

# Agent Store Skill

## When to use this skill

Use this skill when the user wants to buy, purchase, order, pay for, or top up API keys or API credits.

### intent word:
- buy
- order
- purchase
- pay for
- get
- top up

### product word:
- api key
- api keys
- api credit
- api credits

### Examples:
- I want to buy API keys
- Help me order API credits
- Purchase more API credits
- Get an API key
- Top up my API credits

## Execution requirement

Use [scripts/store.py](./scripts/store.py) as the only entry point:

- `python3 apps/agent-store-skill/scripts/store.py <product_type> <log_file>`

Run the bundled Python script and use its log file as the execution report, and report user in "How to report result" section.
DO NOT create other scripts, wrappers, curl flows, or debugging helpers for this task.
DO NOT extend `scripts/store.py` to perform that follow-up automatically. The script ends once it returns the final delivery JSON.
DO NOT investigate or debug the underlying API or wallet flow in chat.

### Arguments:

- `product_type`: `api_credits`, `api_key`, or `vps_instance`
- `log_file`: plain-text log file path for step-by-step reporting, in your workspace's logs folder 


- `X402_BASE_RPC_URL` defaults to `https://mainnet.base.org` for EIP-2612 nonce reads on Base
- the API-side facilitator config now lives in `apps/facilitator/config/x402.config.json` with the facilitator signer key in `apps/facilitator/config/x402.secrets.env`; committed examples live next to them
- the bundled Python client bypasses proxies automatically for loopback `API_HOST` and loopback x402 RPC endpoints
- [`awp-wallet`](https://github.com/awp-core/awp-wallet) must be installed and on `PATH`
- `awp-wallet allowances` must be available for Permit2-only assets
- `awp-wallet approve` must be available for Permit2-only assets
- `awp-wallet sign-typed-data` must be available

### What the script does:

- finds the first active product for the requested `product_type`
- chooses one supported payment asset for that product, preferring `awp`, then `usdc`, then `usdt`
- creates an order request on `POST /orders` with `payment_asset`
- handles the `402 PAYMENT-REQUIRED` x402 challenge
- with the committed facilitator defaults, `awp` is permit-capable and `usdc` / `usdt` remain Permit2 assets until the server config says otherwise
- sends explicit `Accept`, `Content-Type`, and `User-Agent` headers on x402 RPC requests
- if the server advertises `extensions.eip2612GasSponsoring`, signs both the Permit2 witness payload and the EIP-2612 permit extension and skips `approve`
- otherwise ensures Permit2 approval with `awp-wallet allowances` and `awp-wallet approve`
- retries the same `POST /orders` call with `PAYMENT-SIGNATURE`
- uses the successful signed retry response as the order summary and polls `GET /orders/{order_id}/delivery` for the detailed delivery result
- tolerates a short `404 order_not_found` race while the delivery record becomes visible
- keeps an in-progress sidecar at `<log_file>.attempt.json` so restarted runs reuse the same order idempotency key until the flow reaches a terminal state
- writes step logs to `log_file`
- prints the final order-delivery JSON to stdout

## Before running an `api_key` purchase:

- Detect if the active model provider is `agent-store`. If so, inform the user that no purchase is needed, can purchase `api_credits` instead.

## Before running an `api_credits` purchase:

- use the standard purchase flow directly; the API credits workflow now always performs a real top-up through the API service

## After a successful `api_credits` purchase:

- reply with a short summary that includes the remain_credits, payment asset, and transaction hash, do not convert remain_credits to tokens, use original number.

## After a successful `api_key` purchase:

1. inspect `delivery_result.base_url`, `delivery_result.key`, and `delivery_result.supported_models`
2. open your runtime configuration file and check whether `models.providers.agent-store` exists; if not, create it
3. set the provider base URL to `delivery_result.base_url`
4. set the provider API key to `delivery_result.key`
5. set the provider API to `openai-completions`
6. replace the provider models with the returned `supported_models`; use each model key as the model name
7. update only your own active model selection to the first model in `supported_models`; do not change other agents' model selections in the same config file
8. send one minimal verification request through the updated `agent-store` provider with the first model to confirm the gateway works
9. reply with a short summary that includes the result, order amount, payment asset, transaction hash, and the verified model you will use next
10. start a new session with that verified model
11. do not restart the gateway


## Failure handling:

- if the script succeeds, use its stdout and `log_file` as the result
- if the script fails, do not build alternate flows or debug further
- report the failure from `log_file`

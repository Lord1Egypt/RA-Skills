---
name: clawhub-x402-payments
description: Implements USDC x402 payments via PayAI (EIP-3009) and DHM x402 payments via EVVM native (signed pay). Use when adding x402 payment flows, PayAI Echo integration, EVVM pay() for DHM, agent-to-agent payments with Privy, or when the user asks how to do USDC/DHM x402 in the ClawHub/NHS EVVM app.
---

# ClawHub x402 Payments (USDC via PayAI + DHM via EVVM)

This skill documents the two x402 payment flows in the NHS EVVM / ClawHub app: **USDC via PayAI Echo** and **DHM via EVVM native**. Reference implementation lives in this repo.

## Reference paths

| Flow | Client UI | Server / config |
|------|-----------|------------------|
| USDC (PayAI) | `frontend/src/components/sections/USDCX402TestSection.tsx` | Config: `frontend/src/config/contracts.ts` (X402_USDC_ECHO_URL, USDC_BASE_SEPOLIA) |
| DHM (EVVM) | `frontend/src/components/sections/X402TestSection.tsx` | `server/src/index.ts` (GET 402, POST /payments/evvm/dhm) |
| EVVM sign | `frontend/src/lib/evvmSign.ts` | — |

Chain: **Base Sepolia** (chainId 84532).

---

## Flow 1: USDC x402 via PayAI Echo

PayAI returns **402** with an `accepts` array (not `options`). Client picks a USDC option, builds EIP-3009 `TransferWithAuthorization`, signs EIP-712, sends signature in `PAYMENT-SIGNATURE` header, retries the same URL; server returns 200 and may set `PAYMENT-RESPONSE` header with result (e.g. `transaction` hash).

### Client steps

1. **Request resource**  
   `GET <Echo URL>` (e.g. `https://x402.payai.network/api/base-sepolia/paid-content`).

2. **Parse 402**  
   - Prefer `PAYMENT-REQUIRED` response header (base64-encoded JSON).  
   - Fallback: response body may be JSON with `accepts` array.  
   - Type: `{ x402Version?, error?, resource?, accepts: Array<{ scheme, network, amount, asset, payTo, maxTimeoutSeconds?, extra? }> }`.

3. **Pick USDC option**  
   - From `accepts`, choose entry where `asset` matches USDC on Base Sepolia or `extra.name === "USDC"`.  
   - Use `amount`, `asset`, `payTo`, `extra.name` / `extra.version` for EIP-712.

4. **Build EIP-3009 authorization**  
   - Domain: `name` = `extra?.name ?? "USDC"`, `version` = `extra?.version ?? "2"`, `chainId` = 84532, `verifyingContract` = `asset`.  
   - Type: `TransferWithAuthorization`: `from`, `to`, `value`, `validAfter` (0), `validBefore` (e.g. now + 300s), `nonce` (32 random bytes as hex).  
   - Sign with `signTypedData` (EIP-712).

5. **Send payment and retry**  
   - Build payload: `{ x402Version: 2, scheme, network, accepted: { scheme, network, amount, asset, payTo, maxTimeoutSeconds, extra? }, payload: { signature, authorization: message }, extensions: {} }`.  
   - `PAYMENT-SIGNATURE` = base64(JSON.stringify(payload)).  
   - Same URL: `GET` with header `PAYMENT-SIGNATURE: <base64>`.

6. **Read result**  
   - On 200: body is content. Optional `PAYMENT-RESPONSE` or `X-PAYMENT-RESPONSE` header (base64 JSON) may contain `transaction` (tx hash) etc.

### Config

- `VITE_X402_USDC_ECHO_URL`: PayAI Echo endpoint (default: `https://x402.payai.network/api/base-sepolia/paid-content`).  
- USDC on Base Sepolia: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`.

---

## Flow 2: DHM x402 via EVVM native

Server returns **402** with `PAYMENT-REQUIRED: 1` and a JSON body containing `options` (EVVM pay options with `to`, `suggestedNonce`, etc.). Client signs an EVVM pay message (personal_sign), POSTs to server’s payment endpoint; server executes `pay()` on EVVM Core and returns content + txHash.

### Server (402 + payment endpoint)

1. **Protected resource**  
   `GET /clinical/mri-slot` (or similar): if not paid, respond with `402`, `PAYMENT-REQUIRED: 1`, and body:
   - `resource`, `description`, `to` (recipient address), `suggestedNonce`
   - `options`: array with at least one option: `id`, `type: "evvm_pay"`, `chainId`, `evvmId`, `coreAddress`, `token` (DHM), `to`, `suggestedNonce`, `amount`, `priorityFee`, `executor` (or null), `isAsyncExec`.

2. **Payment execution**  
   `POST /payments/evvm/dhm` body: `from`, `to`, `toIdentity`, `token`, `amount`, `priorityFee`, `executor`, `nonce`, `isAsyncExec`, `signature`.  
   Server calls EVVM Core `pay(...)` with executor key, waits for receipt, returns `{ status, txHash, content }`.

### Client steps

1. **Request resource**  
   `GET <X402_SERVER_URL>/clinical/mri-slot`.

2. **Detect 402**  
   `res.status === 402` or `res.headers.get("PAYMENT-REQUIRED") === "1"`. Parse body as JSON: `{ resource, description?, to, suggestedNonce?, options }`.

3. **Pick option**  
   `options.find(o => o.type === "evvm_pay" || o.id === "dhm-evvm") ?? options[0]`. Ensure `to` and `suggestedNonce` are present.

4. **Build EVVM pay message**  
   - Hash payload for Core: `keccak256(encodeAbiParameters("string, address, string, address, uint256, uint256", ["pay", to, toIdentity, token, amount, priorityFee]))`.  
   - Message string: `evvmId, coreAddress, hashPayload, executor, nonce, isAsyncExec` (comma-separated).  
   - Use `buildEvvmPayMessageCoreDoc` from `frontend/src/lib/evvmSign.ts` with: evvmId, coreAddress, to, "", token, amount, priorityFee, executor, nonce, isAsyncExec.

5. **Sign and submit**  
   - `signMessage` (personal_sign) the message string.  
   - POST to `POST <X402_SERVER_URL>/payments/evvm/dhm` with JSON body: `from`, `to`, `toIdentity: ""`, `token`, `amount`, `priorityFee`, `executor`, `nonce`, `isAsyncExec`, `signature`.  
   - Response 200: `content` (unlocked resource), `txHash`.

### Config

- `VITE_X402_SERVER_URL`: DHM x402 server (e.g. `https://evvm-x402-dhm.fly.dev` or localhost).  
- Server env: `EXECUTOR_PRIVATE_KEY`, `RPC_URL`, `RECIPIENT_ADDRESS`, `EVVM_ID`, `EVVM_CORE_ADDRESS`, `DHM_TOKEN_ADDRESS` (see `server/.env.example`).

---

## Checklist for adding or debugging

**USDC (PayAI)**  
- [ ] 402 parsed from header or body; `accepts` used (not `options`).  
- [ ] EIP-712 domain and `TransferWithAuthorization` match USDC contract (name/version from `extra` or "USDC"/"2").  
- [ ] `PAYMENT-SIGNATURE` is base64 JSON; same URL retried with GET + header.  
- [ ] `PAYMENT-RESPONSE` decoded when present for tx hash / receipt.

**DHM (EVVM)**  
- [ ] 402 body has `options[].to` and `suggestedNonce`; client uses them in the signed message.  
- [ ] Message built with `hashDataForPayCore` + `buildEvvmMessageV3` (see evvmSign.ts).  
- [ ] POST body matches server expectation (from, to, token, amount, nonce, executor, isAsyncExec, signature).  
- [ ] Server has `EXECUTOR_PRIVATE_KEY` and RPC to submit `pay()`.

---

## Quick copy-paste (types)

**PayAI 402 (accepts):**
```ts
type PaymentRequirement = {
  scheme: string;
  network: string;
  amount: string;
  asset: string;
  payTo: string;
  maxTimeoutSeconds?: number;
  extra?: { name?: string; version?: string; [k: string]: unknown };
};
// 402 body: { x402Version?, error?, resource?, accepts: PaymentRequirement[] }
```

**EVVM 402 (options):**
```ts
type PaymentOption = {
  id: string;
  type: string;
  chainId: number;
  evvmId: string;
  coreAddress: string;
  token: string;
  to?: string;
  suggestedNonce?: string;
  amount: string;
  priorityFee: string;
  executor: string | null;
  isAsyncExec: boolean;
};
// 402 body: { resource, description?, to?, suggestedNonce?, options: PaymentOption[] }
```

For full code, see the reference paths at the top of this skill.

---

## Homework for hackathon: agent-to-agent with Privy

The flows above use a **browser wallet** (human-in-the-loop). Participants can extend the app so an **agent** can pay autonomously using the **Privy Agentic Wallets** skill.

### Leverage the Privy skill

- **Skill**: [privy-io/privy-agentic-wallets-skill](https://github.com/privy-io/privy-agentic-wallets-skill) — create server wallets that AI agents control with policy guardrails; sign and send transactions via the Privy API (no user click).
- **Install in project**:  
  `git clone https://github.com/privy-io/privy-agentic-wallets-skill.git .cursor/skills/privy`  
  (or into `~/.openclaw/workspace/skills/privy` for OpenClaw). Add `PRIVY_APP_ID` and `PRIVY_APP_SECRET` from [dashboard.privy.io](https://dashboard.privy.io).

### Homework tasks

1. **Same protocol, different signer**  
   Keep the x402 protocol (402 → build payload → sign → POST) unchanged. The only change is **who signs**: instead of `signMessageAsync` / `signTypedDataAsync` in the browser, the agent path uses the Privy API to sign with a **Privy server wallet** (same message / typed data).

2. **DHM agent payer**  
   - Create a Privy server wallet on Base Sepolia (via Privy skill) with a policy that limits spending (e.g. max amount, or only EVVM Core + your x402 server).  
   - Implement an **agent path**: GET 402 from `/clinical/mri-slot` → build EVVM pay message (reuse `buildEvvmPayMessageCoreDoc`) → sign the message via **Privy’s sign API** (see Privy skill references) → POST to `/payments/evvm/dhm` with the same body.  
   - Expose this as a small backend route or script that the agent calls (e.g. “pay for MRI slot as agent”), so the same resource can be unlocked without a connected browser wallet.

3. **USDC agent payer (optional)**  
   - Same idea for PayAI Echo: GET 402 → pick USDC option → build EIP-3009 `TransferWithAuthorization` → sign via **Privy’s sign typed data API** (EIP-712) → send `PAYMENT-SIGNATURE` and retry.  
   - Use a Privy server wallet with a policy that restricts to the PayAI/USDC flow if desired.

4. **Dual mode (stretch)**  
   - In the UI or API, support both “Pay as me” (current wallet) and “Pay as agent” (Privy server wallet). Shared: 402 parsing and payload building; only the signer (browser vs Privy) differs.

### Why this fits the skill

- The **protocol** (x402, EVVM pay, EIP-3009) stays the same; the skill above is the single source of truth for payloads and endpoints.  
- The Privy skill adds **how to get an agent-owned wallet and how to sign with it**. Combining both skills gives hackathon participants a clear path: learn x402 from this skill, add autonomous payers using the Privy skill.

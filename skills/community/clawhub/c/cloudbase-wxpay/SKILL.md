---
name: cloudbase-wxpay
description: "This skill provides battle-tested guidance for integrating WeChat Mini Program payment and refund flows using Tencent CloudBase. It covers cloud.cloudPay.unifiedOrder() for payments, cloud.cloudPay.refund() for refunds, cloud functions, deployment via CLI, and a catalog of critical pitfalls with fixes. Use this skill when building, debugging, or reviewing mini-program payment features on CloudBase — especially when payments go to simulated mode, refunds silently fail, or cloud-call access_token errors surface."
agent_created: true
---

# CloudBase 微信小程序支付集成

一站式指南：微信支付 + 原路退款 + CloudBase 云开发，含踩坑全记录。

## Overview

This skill encodes a full payment-refund integration cycle on CloudBase:
unified-order payment → order management → server-side refund → historical
order backfill. It covers both the happy path and every trap encountered
during a real production build, so future integrations skip the debugging
marathon.

## When to Use

Trigger this skill when:

- Building a new WeChat Mini Program that needs payment via CloudBase
- Debugging "payment went to simulated mode" or "env vars missing on deploy"
- Implementing refunds and getting `returnCode` / `resultCode` confusion
- Seeing `-501001 invalid wx openapi access_token` during refund calls
- Historical orders need backfilled refunds
- Reviewing payment/refund code for correctness

## Prerequisites

- WeChat Mini Program with CloudBase (云开发) enabled
- WeChat Pay merchant account (微信支付商户号) associated with the mini program
- CloudBase CLI (`tcb`) installed and logged in: `npm i -g @cloudbase/cli`
- Cloud functions: `order`, `payment` (minimum)

## Architecture Overview

```
Mini Program (wx.cloud.callFunction)
    ↓
order 云函数 (business logic, status management)
    ↓
payment 云函数 (wraps cloud.cloudPay.* calls)
    ↓
CloudBase cloud.cloudPay.unifiedOrder() / refund()
    ↓
WeChat Pay API
```

### Key separation principle

Keep payment calls in a dedicated `payment` cloud function — never spread
`cloud.cloudPay.*` across multiple functions. This isolates the cloud-call
context dependency and makes debugging tractable.

---

## Payment Integration Workflow

### Step 1: Unified Order (统一下单)

In the `payment` cloud function, the core call:

```js
const result = await cloud.cloudPay.unifiedOrder({
  body: '商品描述',
  outTradeNo: orderId,       // unique order number
  totalFee: 1,               // integer fen (分), e.g. 1 = 0.01 CNY
  spbillCreateIp: '127.0.0.1',
  tradeType: 'JSAPI',
  envId: 'your-env-id',      // HARDCODE, never DYNAMIC_CURRENT_ENV
  functionName: 'payment',
  subMchId: '',              // omit if not sub-merchant mode
});
```

Critical:
- `envId` does NOT work with `cloud.DYNAMIC_CURRENT_ENV` — hardcode the
  environment ID string.
- Remove `subAppId` unless in sub-merchant mode. Case mismatches cause
  cryptic API errors.
- `totalFee` is in **fen (分)**, not yuan.

### Step 2: Upload Cloud Functions via CLI (NOT DevTools)

DevTools auto-upload does **not** carry environment variables
(`WX_MCH_ID`, etc.) to the cloud → payment silently falls back to simulated
mode (no real charge).

Use CLI deployment:

```bash
tcb fn deploy payment --envId <your-env-id>
tcb fn deploy order --envId <your-env-id>
```

Verify deployment with:

```bash
tcb fn list --envId <your-env-id>
```

### Step 3: Environment Variables

In `cloudbaserc.json` or CloudBase console, ensure:

```json
{
  "env": {
    "WX_APPID": "wx...",
    "WX_MCH_ID": "1...",
    "WX_MCH_KEY": "..."
  }
}
```

The payment cloud function must read these at runtime:

```js
const mchId = process.env.WX_MCH_ID;
if (!mchId) {
  // This is the symptom of DevTools deploy — abort with clear error
  return { code: -1, message: 'WX_MCH_ID not set — use CLI deployment' };
}
```

---

## Refund Integration Workflow

### Step 1: Core Refund Call

In the `payment` cloud function, add a `refund` action:

```js
async function handleRefund(orderId, totalFee, refundFee, outRefundNo) {
  const result = await cloud.cloudPay.refund({
    subMchId: '',                    // omit if not sub-merchant
    transactionId: orderId,
    outTradeNo: orderId,
    outRefundNo: outRefundNo || generateOutRefundNo(orderId),
    totalFee: totalFee,             // original total in fen
    refundFee: refundFee,           // amount to refund in fen
    envId: 'your-env-id',           // hardcoded, same as payment
    functionName: 'payment',
  });

  return result;
}
```

### Step 2: CRITICAL — Double-Layer Return Check

**This is the #1 cause of silent refund failures.** The `refund` return
object has two layers, both must be checked:

```js
const refundResult = await cloud.cloudPay.refund({...});

// Layer 1: CloudBase wrapper
if (refundResult.returnCode !== 'SUCCESS') {
  return { code: -1, errMsg: refundResult.returnMsg || 'refund wrapper failed' };
}

// Layer 2: WeChat Pay result
if (refundResult.resultCode !== 'SUCCESS') {
  return {
    code: -1,
    errCode: refundResult.errCode,
    errMsg: refundResult.errCodeDes || 'refund payment failed',
  };
}

// Only now is the refund truly successful
// Store refundTransactionId from result.refundId or result.transactionId
return {
  code: 0,
  refundTransactionId: refundResult.refundId,
};
```

**Never** check only `code` and assume success — the old code path that caused
`refundTransactionId` to be empty did exactly this.

### Step 3: Order Status After Refund

The `order` cloud function should:

1. Call `payment` cloud function's `refund` action
2. Check `returnCode` AND `resultCode` on the returned result
3. Only set `refundTransactionId` and `refundedAt` when both succeed
4. If refund fails, DO NOT change status to `user_cancelled` — leave as-is
   and surface the error

```js
// In order cloud function, processRefund action:
const refundRes = await callPaymentCloud('refund', { orderId, totalFee, refundFee });

if (refundRes.returnCode !== 'SUCCESS' || refundRes.resultCode !== 'SUCCESS') {
  return { code: -1, errCode: refundRes.errCode, errMsg: refundRes.errCodeDes };
}

// Only now update the order document:
await db.collection('orders').doc(orderId).update({
  data: {
    status: 'user_cancelled',
    refundedAt: new Date(),
    refundTransactionId: refundRes.refundId,
  },
});
```

---

## Critical Pitfalls Catalog

For the full pitfall catalog with debugging commands and fix recipes,
load `references/gotchas.md`.

Quick reference of the top 5 pitfalls:

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 1 | DevTools deploy loses env vars | Payment goes to simulated mode, `WX_MCH_ID` is empty | Use `tcb fn deploy` CLI |
| 2 | `envId: cloud.DYNAMIC_CURRENT_ENV` | `unifiedOrder` returns unexpected data | Hardcode env ID string |
| 3 | `subAppId` case mismatch | `unifiedOrder` returns `resultCode: FAIL` | Remove `subAppId` if not using sub-merchant |
| 4 | Refund return not checked properly | `refundTransactionId` stays empty, order marked "refunded" but money never returned | Double-layer check: `returnCode` + `resultCode` |
| 5 | CLI `tcb fn invoke` for refund | `-501001 invalid wx openapi access_token` | Cloud calls need mini-program context; use `wx.cloud.callFunction` from mini program side |

---

## Cloud Call Context Rules

`cloud.cloudPay.refund()` and `cloud.cloudPay.unifiedOrder()` are
**cloud calls (云调用)**. They require WeChat-side authentication context.
Only these invocation methods carry valid context:

| Method | Works? | Reason |
|--------|--------|--------|
| `wx.cloud.callFunction` from Mini Program | ✅ Yes | Carries user session + WeChat auth |
| Timer trigger (定时触发器) | ✅ Yes | Platform injects context |
| HTTP API trigger | ✅ Yes | Platform injects context |
| `tcb fn invoke` (CLI) | ❌ No | No mini-program session → access_token failure |
| CloudBase console "Test" button | ❌ No | Same reason as CLI |

**Rule**: Any cloud call needing WeChat Pay access_token must originate from
one of the three "✅ Yes" methods. When testing refunds or troubleshooting
historical orders, trigger through the Mini Program UI, not CLI.

---

## Deployment Checklist

Before testing payment in production:

- [ ] Cloud functions deployed via `tcb fn deploy` (not DevTools)
- [ ] `envId` hardcoded as string in all `cloud.cloudPay.*` calls
- [ ] `WX_MCH_ID`, `WX_APPID`, `WX_MCH_KEY` set as environment variables
- [ ] Payment cloud function reads env vars and fails fast if missing
- [ ] `subAppId` removed from `unifiedOrder` unless sub-merchant mode
- [ ] Refund code has double-layer `returnCode` + `resultCode` check
- [ ] Historical order backfill uses mini-program-side trigger (not CLI)

## Debugging a Failed Refund

When a user reports "order cancelled but money not returned":

1. **Query the order document**: Check `refundTransactionId` — if empty string,
   refund never executed.
   ```bash
   tcb db query --envId <env-id> -c orders --where '{"_id":"<doc-id>"}'
   ```

2. **Check order status**: If status is `user_cancelled` but
   `refundTransactionId` is empty, the old bug is confirmed.

3. **Fix**: Add a `force_refund` action in the `payment` cloud function that
   bypasses status checks, then trigger it from the Mini Program via
   `wx.cloud.callFunction({ name: 'payment', data: { action: 'force_refund', orderId } })`.

4. **Cleanup**: After backfilling, remove `force_refund` and any related UI
   buttons — they are temporary fixes, not intended for users.

## Resources

- `references/gotchas.md` — Full pitfall catalog with debugging commands,
  error code reference, and the exact chain of bugs encountered during the
  real build.

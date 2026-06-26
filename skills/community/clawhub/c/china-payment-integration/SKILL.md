---
name: china-payment-integration
description: "Integrate Chinese payment methods (WeChat Pay, Alipay, UnionPay) into applications. Teach AI agents how to implement payment flows, handle callbacks, manage refunds, and comply with Chinese payment regulations. Covers: WeChat Pay JSAPI/H5/Native/Mini Program payment, Alipay web/mobile payment, dual-payment unified interface, refund and reconciliation, and payment compliance. Triggers on: 微信支付集成, wechat pay integration, 支付宝集成, alipay integration, 银联支付, unionpay, 中国支付接入, china payment integration, 微信小程序支付, mini program payment, 支付回调, payment callback, 退款处理, refund processing, 支付合规, payment compliance, 双支付统一接口, dual payment interface"
---

# China Payment Integration - 中国支付集成专家

You are an expert at integrating Chinese payment methods into applications. You handle WeChat Pay, Alipay, and UnionPay — the three pillars of Chinese digital payments.

## Core Philosophy

**In China, if you can't accept WeChat Pay or Alipay, you can't collect money.** Credit cards are secondary. Your job is to make payment integration painless and compliant.

## Payment Landscape

| Method | Market Share | Best For | Settlement |
|--------|-------------|----------|------------|
| WeChat Pay | ~40% | Mini Programs, social commerce, in-app | T+1 |
| Alipay | ~55% | E-commerce, web payments, subscriptions | T+1 |
| UnionPay | ~5% | Large transactions, government, banking | T+1 |

## Workflow 1: WeChat Pay Integration

### Prerequisites
1. Register merchant account: https://pay.weixin.qq.com
2. Get merchant ID (mchid), API key (apiV3Key), and certificate
3. Set payment callback URL (notify_url)

### JSAPI Payment (In-WeChat Browser)
```javascript
// Backend: Create order (Node.js)
const WxPay = require('wechatpay-node-v3');
const pay = new WxPay({
  appid: 'wx1234567890',
  mchid: '1234567890',
  publicKey: Buffer.from(process.env.WX_CERT),
  privateKey: Buffer.from(process.env.WX_KEY),
  apiV3Key: process.env.WX_API_V3_KEY,
});

// Step 1: Create prepay order
const result = await pay.transactions_jsapi({
  description: 'Product Name',
  out_trade_no: `ORDER_${Date.now()}`,
  notify_url: 'https://your-domain.com/api/pay/wechat/callback',
  amount: { total: 100, currency: 'CNY' }, // total in 分 (cents)
  payer: { openid: userOpenId },
});

// Step 2: Return payment params to frontend
const payParams = {
  appId: 'wx1234567890',
  timeStamp: String(Math.floor(Date.now() / 1000)),
  nonceStr: crypto.randomUUID(),
  package: `prepay_id=${result.prepay_id}`,
  signType: 'RSA',
};
payParams.paySign = pay.sign(payParams);

// Frontend: Call WeChat JSAPI
// WeixinJSBridge.invoke('getBrandWCPayRequest', payParams, callback);
```

### Native Payment (QR Code)
```javascript
// For desktop web — generates QR code for user to scan
const result = await pay.transactions_native({
  description: 'Product Name',
  out_trade_no: `ORDER_${Date.now()}`,
  notify_url: 'https://your-domain.com/api/pay/wechat/callback',
  amount: { total: 100, currency: 'CNY' },
});
// result.code_url → generate QR code for this URL
```

### Mini Program Payment
```javascript
// Same as JSAPI but called from mini program
const result = await pay.transactions_jsapi({
  description: 'Product Name',
  out_trade_no: `ORDER_${Date.now()}`,
  notify_url: 'https://your-domain.com/api/pay/wechat/callback',
  amount: { total: 100, currency: 'CNY' },
  payer: { openid: userOpenId },
});

// Frontend: wx.requestPayment
// wx.requestPayment({ timeStamp, nonceStr, package, signType, paySign });
```

### Payment Callback Handler
```javascript
// POST /api/pay/wechat/callback
app.post('/api/pay/wechat/callback', async (req, res) => {
  try {
    // Step 1: Verify signature
    const signature = req.headers['wechatpay-signature'];
    const timestamp = req.headers['wechatpay-timestamp'];
    const nonce = req.headers['wechatpay-nonce'];
    
    // Step 2: Decrypt notification
    const decrypted = pay.decipher_gcm(
      req.body.resource.ciphertext,
      req.body.resource.associated_data,
      req.body.resource.nonce,
    );
    
    const payment = JSON.parse(decrypted);
    
    // Step 3: Process payment result
    if (payment.trade_state === 'SUCCESS') {
      await Order.updateOne(
        { out_trade_no: payment.out_trade_no },
        { 
          status: 'paid',
          transaction_id: payment.transaction_id,
          paid_at: new Date(payment.success_time),
        }
      );
    }
    
    // Step 4: Acknowledge
    res.json({ code: 'SUCCESS', message: 'OK' });
  } catch (err) {
    console.error('Payment callback error:', err);
    res.json({ code: 'FAIL', message: err.message });
  }
});
```

## Workflow 2: Alipay Integration

### Prerequisites
1. Register at https://open.alipay.com
2. Create app, get appid
3. Upload RSA2 public key, get Alipay public key
4. Set payment callback URL

### Web Payment (PC)
```javascript
const AlipaySdk = require('alipay-sdk').default;
const alipay = new AlipaySdk({
  appId: '2021001234567890',
  privateKey: process.env.ALIPAY_PRIVATE_KEY,
  alipayPublicKey: process.env.ALIPAY_PUBLIC_KEY,
});

// Create payment page
const result = alipay.pageExec('alipay.trade.page.pay', {
  method: 'GET',
  bizContent: {
    out_trade_no: `ORDER_${Date.now()}`,
    total_amount: '1.00', // 元 (yuan, not cents!)
    subject: 'Product Name',
    product_code: 'FAST_INSTANT_TRADE_PAY',
    notify_url: 'https://your-domain.com/api/pay/alipay/callback',
    return_url: 'https://your-domain.com/payment/success',
  },
});
// Redirect user to result (Alipay payment page)
```

### Mobile Payment (H5)
```javascript
const result = alipay.pageExec('alipay.trade.wap.pay', {
  method: 'GET',
  bizContent: {
    out_trade_no: `ORDER_${Date.now()}`,
    total_amount: '1.00',
    subject: 'Product Name',
    product_code: 'QUICK_WAP_WAY',
    quit_url: 'https://your-domain.com/payment/cancel',
  },
});
```

### Alipay Callback Handler
```javascript
app.post('/api/pay/alipay/callback', async (req, res) => {
  // Step 1: Verify signature
  const isValid = alipay.checkNotifySign(req.body);
  if (!isValid) return res.send('fail');
  
  // Step 2: Process
  if (req.body.trade_status === 'TRADE_SUCCESS') {
    await Order.updateOne(
      { out_trade_no: req.body.out_trade_no },
      { status: 'paid', transaction_id: req.body.trade_no }
    );
  }
  
  // Step 3: Acknowledge
  res.send('success');
});
```

## Workflow 3: Dual-Payment Unified Interface

**When**: Support both WeChat Pay and Alipay with one codebase

```javascript
class ChinaPayment {
  constructor() {
    this.wechatPay = new WxPay(wxConfig);
    this.alipay = new AlipaySdk(alipayConfig);
  }

  async createOrder({ method, orderId, amount, description, openid }) {
    switch (method) {
      case 'wechat_jsapi':
        return this._wechatJSAPI(orderId, amount, description, openid);
      case 'wechat_native':
        return this._wechatNative(orderId, amount, description);
      case 'alipay_page':
        return this._alipayPage(orderId, amount, description);
      case 'alipay_wap':
        return this._alipayWAP(orderId, amount, description);
      default:
        throw new Error(`Unsupported payment method: ${method}`);
    }
  }

  async handleCallback(provider, req) {
    switch (provider) {
      case 'wechat':
        return this._handleWechatCallback(req);
      case 'alipay':
        return this._handleAlipayCallback(req);
    }
  }

  // Amount conversion helper
  _toFen(yuan) { return Math.round(yuan * 100); }  // WeChat uses 分
  _toYuan(fen) { return (fen / 100).toFixed(2); }   // Alipay uses 元
}
```

## Workflow 4: Refund Processing

```javascript
// WeChat Refund
async function wechatRefund(out_trade_no, refund_amount, total_amount) {
  const result = await pay.refund({
    out_trade_no,
    out_refund_no: `REFUND_${Date.now()}`,
    amount: {
      refund: refund_amount,  // in 分
      total: total_amount,    // in 分
      currency: 'CNY',
    },
    reason: 'User requested refund',
  });
  return result;
}

// Alipay Refund
async function alipayRefund(out_trade_no, refund_amount) {
  const result = await alipay.exec('alipay.trade.refund', {
    bizContent: {
      out_trade_no,
      refund_amount: refund_amount.toFixed(2),  // in 元
    },
  });
  return result;
}
```

## Workflow 5: Payment Compliance Checklist

### Required for All Payment Integrations
- [ ] **Business license** (营业执照) — required for merchant accounts
- [ ] **ICP filing** — required for payment callback URLs
- [ ] **User agreement** — terms of service with payment terms
- [ ] **Refund policy** — clearly stated refund process
- [ ] **Invoice support** (发票) — Chinese users expect fapiao
- [ ] **Data encryption** — card/bank info must be encrypted
- [ ] **Transaction logging** — keep records for 5+ years
- [ ] **Anti-fraud** — implement rate limiting and suspicious activity detection

### WeChat Pay Specific
- [ ] Mini Program payment only works within WeChat ecosystem
- [ ] Virtual goods cannot use WeChat Pay (use in-app purchase API instead)
- [ ] Subscription payments require special approval

### Alipay Specific
- [ ] Real-name verification required for merchants
- [ ] Annual transaction limits apply for personal accounts
- [ ] Cross-border payments require separate qualification

## Safety Rules

1. **Never store payment credentials** — use tokens/references only
2. **Always verify callback signatures** — never trust unverified callbacks
3. **Idempotency** — handle duplicate callbacks gracefully (check order status before processing)
4. **Amount in correct unit** — WeChat uses 分(cents), Alipay uses 元(yuan) — this is the #1 bug
5. **HTTPS only** — payment callbacks must use HTTPS
6. **Test in sandbox first** — both WeChat and Alipay provide sandbox environments
7. **Monitor for chargebacks** — set up alerts for dispute notifications

## Quick Reference

```bash
# WeChat Pay sandbox
# https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=23_1

# Alipay sandbox
# https://open.alipay.com/develop/sandbox/app

# Test payment amount conventions
# 0.01元 = 1分 (minimum test amount)
# Amount ending in 1 = success, 2 = fail (in sandbox)
```

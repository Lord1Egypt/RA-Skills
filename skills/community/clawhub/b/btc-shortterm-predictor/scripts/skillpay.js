/**
 * SkillPay Billing Integration
 * 收费接口 - 每次调用扣费 0.005 USDT
 */

const BILLING_API_URL = 'https://skillpay.me';
const BILLING_API_KEY = process.env.SKILLPAY_API_KEY || 'sk_a267a27a1eb8381a762a9a6cdb1ea7d722f9f45f345b7319cfd3cccd9fae35c5';
const SKILL_ID = '0525333e-9ef5-4c67-ac65-1463a8ca3d65'; // BTC短线预测

/**
 * 扣费
 */
async function chargeUser(userId, amount = 0.005) {
  if (process.env.SKILLPAY_DEV === 'true') {
    console.log('⚠️  开发模式：跳过扣费');
    return { ok: true, balance: 999 };
  }
  
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: amount,
    }),
  });
  
  const data = await resp.json();
  
  if (data.success) {
    return { ok: true, balance: data.balance };
  }
  
  return { 
    ok: false, 
    balance: data.balance, 
    paymentUrl: data.payment_url 
  };
}

/**
 * 生成充值链接
 */
async function getPaymentLink(userId, amount = 8) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': BILLING_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      amount,
    }),
  });
  const data = await resp.json();
  return data.payment_url;
}

module.exports = { 
  chargeUser, 
  getPaymentLink,
  SKILL_PRICE: 0.005
};

// ═════════════════════════════════════════════════════════════
// SkillPay Billing Integration
// スキルペイ決統合 / 결제 연동 / Интеграция биллинга SkillPay

const BILLING_API_URL = 'https://skillpay.me';
const API_KEY = 'sk_f072a786149bc07fc8730b4683dc00f3e050e72441922284ca803cdee2b994b5';
const SKILL_ID = '9469b85f-f40f-4ada-ad9c-bdd9db1167cc';

// ① Check balance / 查余额 / 残高確認 / 잔액 확인 / Проверка баланса
async function checkBalance(userId) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/balance?user_id=${userId}`, {
    headers: { 'X-API-Key': API_KEY }
  });
  const data = await resp.json();
  return data.balance; // USDT amount / USDT 金额
}

// ② Charge per call / 每次调用扣费 / 呼び出しごとの課金 / 호출당 과금 / Списание за вызов
async function chargeUser(userId) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/charge`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      skill_id: SKILL_ID,
      amount: 0.001, // USDT per call / 每次调用单价
    }),
  });
  const data = await resp.json();
  if (data.success) {
    return { ok: true, balance: data.balance };
  }
  // Insufficient balance → get payment link
  // 余额不足 → 生成充值链接
  // 残高不足 → 決済リンク生成
  // 잔액 부족 → 결제 링크 생성
  // Недостаточно средств → ссылка на оплату
  return { ok: false, balance: data.balance, paymentUrl: data.payment_url };
}

// ③ Generate payment link / 生成充值链接 / 決済リンク生成 / 결제 링크 생성 / Ссылка на оплату
async function getPaymentLink(userId, amount) {
  const resp = await fetch(`${BILLING_API_URL}/api/v1/billing/payment-link`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      amount
    }),
  });
  const data = await resp.json();
  return data.payment_url; // BNB Chain USDT payment link / BNB链 USDT 付款链接
}

// ════════════ Usage example / 使用示例 ════════════ //
// async function handleRequest(userId) {
//   const result = await chargeUser(userId);
//   if (result.ok) {
//     // ✅ Execute your skill logic here
//     // ✅ 在这里执行你的 Skill 逻辑
//     return { success: true };
//   } else {
//     // ❌ Insufficient balance, return payment link to user
//     // ❌ 余额不足，返回充值链接给用户
//     return { success: false, paymentUrl: result.paymentUrl };
//   }
// }

module.exports = {
  checkBalance,
  chargeUser,
  getPaymentLink
};

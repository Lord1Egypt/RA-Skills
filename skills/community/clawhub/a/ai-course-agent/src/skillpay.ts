/**
 * SkillPay Billing SDK — Node.js
 *
 * [EN] 1 USDT = 1000 tokens | 1 call = 1 token | Min deposit 8 USDT
 * [中文] 1 USDT = 1000 tokens | 每次 1 token | 最低充值 8 USDT
 * [日本語] 1 USDT = 1000トークン | 1回1トークン | 最低8 USDT
 * [한국어] 1 USDT = 1000토큰 | 1회 1토큰 | 최소 8 USDT
 * [Русский] 1 USDT = 1000 токенов | 1 вызов = 1 токен | Мин. 8 USDT
 *
 * Endpoints:
 * POST /billing/charge — Deduct / 扣费 / 課金 / 차감 / Списание
 * GET /billing/balance — Balance / 余额 / 残高 / 잔액 / Баланс
 * POST /billing/payment-link — Pay link / 充值 / 入金 / 결제 / Оплата
 */

import axios from 'axios';

const BILLING_URL = 'https://skillpay.me/api/v1/billing';

interface ChargeResult {
  ok: boolean;
  balance: number;
  payment_url?: string;
}

interface BillingConfig {
  apiKey: string;
  skillId: string;
}

/**
 * Get billing configuration (hardcoded - DO NOT expose to users!)
 * 
 * These values belong to the skill author and are used to receive payments.
 * Users cannot and should not modify these values.
 */
function getBillingConfig(): BillingConfig {
  // Hardcoded credentials - payments go to skill author's account
  const apiKey = 'sk_ee2a96e814192bbe11402f4c624cfa524de6d23babf3baab7b4b306accee9ee5';
  const skillId = '476d912d-e597-4be0-a031-6ffe2adf3b13';

  return { apiKey, skillId };
}

/**
 * Get headers for billing API
 */
function getHeaders(): Record<string, string> {
  const { apiKey } = getBillingConfig();
  return {
    'X-API-Key': apiKey,
    'Content-Type': 'application/json',
  };
}

/**
 * Charge user for skill usage
 * 扣费 / 課金 / 차감 / Списание
 *
 * @param userId - User identifier
 * @param amount - Amount to charge (default: 0 = use default rate)
 * @returns Charge result with balance and payment URL if insufficient
 */
export async function chargeUser(
  userId: string,
  amount: number = 0,
): Promise<ChargeResult> {
  const { skillId } = getBillingConfig();
  const headers = getHeaders();

  try {
    const { data } = await axios.post(
      BILLING_URL + '/charge',
      {
        user_id: userId,
        skill_id: skillId,
        amount,
      },
      { headers },
    );

    if (data.success) {
      return { ok: true, balance: data.balance };
    }

    return {
      ok: false,
      balance: data.balance,
      payment_url: data.payment_url,
    };
  } catch (error) {
    console.error('[SkillPay] Charge error:', error);
    throw new Error('Failed to charge user. Please try again later.');
  }
}

/**
 * Get user balance
 * 余额 / 残高 / 잔액 / Баланс
 *
 * @param userId - User identifier
 * @returns Current balance in tokens
 */
export async function getBalance(userId: string): Promise<number> {
  const headers = getHeaders();

  try {
    const { data } = await axios.get(BILLING_URL + '/balance', {
      params: { user_id: userId },
      headers,
    });

    return data.balance;
  } catch (error) {
    console.error('[SkillPay] Get balance error:', error);
    throw new Error('Failed to get balance. Please try again later.');
  }
}

/**
 * Generate payment link for user top-up
 * 充值链接 / 入金リンク / 결제링크 / Ссылка на оплату
 *
 * @param userId - User identifier
 * @param amount - Amount to top up in USDT (default: 8 USDT min)
 * @returns Payment URL
 */
export async function getPaymentLink(
  userId: string,
  amount: number = 8,
): Promise<string> {
  const headers = getHeaders();

  try {
    const { data } = await axios.post(
      BILLING_URL + '/payment-link',
      {
        user_id: userId,
        amount,
      },
      { headers },
    );

    return data.payment_url;
  } catch (error) {
    console.error('[SkillPay] Get payment link error:', error);
    throw new Error('Failed to generate payment link. Please try again later.');
  }
}

/**
 * Handle billing for skill execution
 * 处理技能计费 / スキル課金処理 / 스킬 결제 처리 / Обработка оплаты навыка
 *
 * Usage example:
 * ```typescript
 * const billing = await handleBilling(userId);
 * if (!billing.ok) {
 *   return { success: false, message: billing.message, paymentUrl: billing.paymentUrl };
 * }
 * // ✅ Proceed with skill execution
 * ```
 *
 * @param userId - User identifier
 * @returns Billing result with status and payment URL if needed
 */
export async function handleBilling(userId: string): Promise<{
  ok: boolean;
  message: string;
  paymentUrl?: string;
  balance?: number;
}> {
  try {
    const charge = await chargeUser(userId);

    if (charge.ok) {
      return {
        ok: true,
        message: `✅ 扣费成功，剩余余额: ${charge.balance} tokens`,
        balance: charge.balance,
      };
    }

    // Insufficient balance
    return {
      ok: false,
      message: `❌ 余额不足 (当前: ${charge.balance} tokens)`,
      paymentUrl: charge.payment_url,
      balance: charge.balance,
    };
  } catch (error) {
    const errorMsg = error instanceof Error ? error.message : String(error);
    console.error('[SkillPay] Billing error:', errorMsg);
    return {
      ok: false,
      message: `⚠️ 计费系统错误: ${errorMsg}`,
    };
  }
}

export default {
  chargeUser,
  getBalance,
  getPaymentLink,
  handleBilling,
};

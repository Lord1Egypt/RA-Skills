import type { BillingResult, ChargeParams } from "./types";

export type { BillingResult };

const SKILLPAY_API = "https://skillpay.me/api/v1/billing/charge";

export async function chargeUser(params: ChargeParams): Promise<BillingResult> {
  const { userId, apiKey, priceUsdt, skillId, fetchFn = fetch } = params;

  try {
    const response = await fetchFn(SKILLPAY_API, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey,
      },
      body: JSON.stringify({
        user_id: userId,
        skill_id: skillId,
        amount: priceUsdt,
      }),
    });

    const data = await response.json();
    return data as BillingResult;
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : "Billing request failed",
    };
  }
}

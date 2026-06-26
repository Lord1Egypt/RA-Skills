import type { CreemWebhookPayload, ChurnContext, LLMDecision } from "./types.js";

interface ProductEntity {
  id: string;
  name: string;
  price: number;
}

interface CustomerEntity {
  id: string;
  email?: string;
}

interface CreemClient {
  subscriptions: {
    get(id: string): Promise<{
      id: string;
      product: ProductEntity | string;
      customer: CustomerEntity | string;
      createdAt: Date;
      status: string;
    }>;
  };
  transactions: {
    search(customerId: string): Promise<{
      items: Array<{ amount: number }>;
    }>;
  };
}

export async function extractChurnContext(
  payload: CreemWebhookPayload,
  creem: CreemClient,
): Promise<ChurnContext> {
  const obj = payload.object as Record<string, unknown>;
  const subId = (obj.id as string) ?? "";

  const sub = await creem.subscriptions.get(subId);

  // Handle union: product is ProductEntity | string
  const product = typeof sub.product === "string" ? null : sub.product;
  const productId = typeof sub.product === "string" ? sub.product : sub.product.id;
  const productName = product?.name ?? "Unknown Plan";
  const priceInCents = product?.price ?? 0;

  // Handle union: customer is CustomerEntity | string
  const customerId = typeof sub.customer === "string" ? sub.customer : sub.customer.id;
  const customerEmail = typeof sub.customer === "string" ? "unknown" : (sub.customer.email ?? "unknown");

  // Tenure: sub.createdAt is a Date object
  const tenureMonths = Math.max(1, Math.round(
    (Date.now() - sub.createdAt.getTime()) / (1000 * 60 * 60 * 24 * 30)
  ));

  // Fetch transactions for total revenue
  let totalRevenueCents = 0;
  try {
    const txns = await creem.transactions.search(customerId);
    totalRevenueCents = (txns.items ?? []).reduce((sum, t) => sum + (t.amount ?? 0), 0);
  } catch { /* continue with 0 */ }

  const cancelReason = (obj.cancel_reason as string)
    ?? (obj.cancelReason as string)
    ?? "not provided";

  return {
    subscriptionId: subId,
    customerId,
    productId,
    customerEmail,
    productName,
    price: priceInCents / 100,
    tenureMonths,
    totalRevenue: totalRevenueCents / 100,
    cancelReason,
  };
}

export function shouldAutoExecute(decision: LLMDecision, threshold: number): boolean {
  if (decision.action === "NO_ACTION") return false;
  return decision.confidence >= threshold;
}

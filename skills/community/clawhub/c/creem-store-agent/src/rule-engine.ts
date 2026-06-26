import type { CreemEventType, CreemWebhookPayload } from "./types.js";

const EMOJI_MAP: Record<CreemEventType, string> = {
  "checkout.completed": "💰",
  "subscription.active": "🎉",
  "subscription.paid": "🔄",
  "subscription.canceled": "❌",
  "subscription.scheduled_cancel": "⏰",
  "subscription.unpaid": "🚫",
  "subscription.past_due": "⚠️",
  "subscription.paused": "⏸️",
  "subscription.expired": "💀",
  "subscription.trialing": "🆓",
  "subscription.update": "📝",
  "refund.created": "💸",
  "dispute.created": "🚨",
};

const URGENCY_MAP: Partial<Record<CreemEventType, "high" | "medium">> = {
  "dispute.created": "high",
  "subscription.past_due": "high",
  "refund.created": "medium",
  "subscription.expired": "medium",
};

const TITLE_MAP: Record<CreemEventType, string> = {
  "checkout.completed": "New Sale",
  "subscription.active": "New Subscription",
  "subscription.paid": "Subscription Renewed",
  "subscription.canceled": "Subscription Canceled",
  "subscription.scheduled_cancel": "Cancellation Scheduled",
  "subscription.unpaid": "Subscription Unpaid",
  "subscription.past_due": "Payment Failed",
  "subscription.paused": "Subscription Paused",
  "subscription.expired": "Subscription Expired",
  "subscription.trialing": "Trial Started",
  "subscription.update": "Subscription Updated",
  "refund.created": "Refund Issued",
  "dispute.created": "Dispute Opened",
};

export function getEventEmoji(eventType: CreemEventType): string {
  return EMOJI_MAP[eventType] ?? "📌";
}

export function getEventUrgency(eventType: CreemEventType): "high" | "medium" | "low" {
  return URGENCY_MAP[eventType] ?? "low";
}

function getStr(obj: Record<string, unknown>, path: string): string {
  const parts = path.split(".");
  let current: unknown = obj;
  for (const part of parts) {
    if (current == null || typeof current !== "object") return "";
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "string" ? current : "";
}

function getNum(obj: Record<string, unknown>, path: string): number | null {
  const parts = path.split(".");
  let current: unknown = obj;
  for (const part of parts) {
    if (current == null || typeof current !== "object") return null;
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "number" ? current : null;
}

function formatCents(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`;
}

export function formatEventAlert(payload: CreemWebhookPayload): string {
  const { eventType, object: obj } = payload;
  const emoji = getEventEmoji(eventType);
  const urgency = getEventUrgency(eventType);
  const title = TITLE_MAP[eventType] ?? eventType;

  const urgencyPrefix = urgency === "high" ? "🔴 URGENT: " : "";
  const email = getStr(obj, "customer.email");
  const productName = getStr(obj, "product.name");
  const amount = getNum(obj, "amount");

  const lines: string[] = [];
  lines.push(`${emoji} ${urgencyPrefix}${title}`);
  if (email) lines.push(`Customer: ${email}`);
  if (productName) lines.push(`Product: ${productName}`);
  if (amount !== null) lines.push(`Amount: ${formatCents(amount)}`);
  lines.push(`Event: ${payload.id}`);

  return lines.join("\n");
}

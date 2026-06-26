import { readFileSync } from "node:fs";
import { createHmac } from "node:crypto";

// Load .env
try {
  const env = readFileSync(new URL("../.env", import.meta.url), "utf-8");
  for (const line of env.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 1) continue;
    const key = trimmed.slice(0, eq);
    const val = trimmed.slice(eq + 1);
    if (!process.env[key]) process.env[key] = val;
  }
} catch {}

const WEBHOOK_URL = process.env.WEBHOOK_URL ?? "http://localhost:3000/webhook/creem";
const WEBHOOK_SECRET = process.env.CREEM_WEBHOOK_SECRET ?? "whsec_demo_secret";

async function sendWebhookEvent(payload: Record<string, unknown>): Promise<void> {
  const body = JSON.stringify(payload);
  const signature = createHmac("sha256", WEBHOOK_SECRET).update(body).digest("hex");

  const response = await fetch(WEBHOOK_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "creem-signature": signature,
    },
    body,
  });

  const status = response.status;
  const result = await response.text();
  console.log(`[${status}] ${payload.eventType}: ${result}`);
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function runDemo(): Promise<void> {
  console.log("🍦 Creem Store Agent — Demo Script");
  console.log("=".repeat(40));
  console.log(`Sending events to: ${WEBHOOK_URL}\n`);

  // 1. New sale
  console.log("📌 Scene 1: New sale comes in...");
  await sendWebhookEvent({
    eventType: "checkout.completed",
    id: "evt_demo_001",
    created_at: Math.floor(Date.now() / 1000),
    object: {
      amount: 4900,
      currency: "USD",
      customer: { email: "alice@startup.io" },
      product: { name: "Pro Plan" },
    },
  });
  await delay(3000);

  // 2. New subscription active
  console.log("\n📌 Scene 2: Subscription activated...");
  await sendWebhookEvent({
    eventType: "subscription.active",
    id: "evt_demo_002",
    created_at: Math.floor(Date.now() / 1000),
    object: {
      id: "sub_demo_alice",
      customerId: "cus_demo_alice",
      customer: { email: "alice@startup.io" },
      product: { name: "Pro Plan" },
    },
  });
  await delay(3000);

  // 3. Churn event — triggers LLM analysis
  console.log("\n📌 Scene 3: Long-time customer cancels (triggers AI analysis)...");
  await sendWebhookEvent({
    eventType: "subscription.canceled",
    id: "evt_demo_003",
    created_at: Math.floor(Date.now() / 1000),
    object: {
      id: "sub_demo_bob",
      customerId: "cus_demo_bob",
      customer: { email: "bob@enterprise.co" },
      product: { name: "Business Plan" },
      cancelReason: "switching to competitor",
    },
  });
  await delay(5000);

  // 4. Payment failure
  console.log("\n📌 Scene 4: Payment fails...");
  await sendWebhookEvent({
    eventType: "subscription.past_due",
    id: "evt_demo_004",
    created_at: Math.floor(Date.now() / 1000),
    object: {
      id: "sub_demo_carol",
      customerId: "cus_demo_carol",
      customer: { email: "carol@agency.dev" },
      product: { name: "Team Plan" },
    },
  });
  await delay(3000);

  // 5. Dispute
  console.log("\n📌 Scene 5: Dispute opened...");
  await sendWebhookEvent({
    eventType: "dispute.created",
    id: "evt_demo_005",
    created_at: Math.floor(Date.now() / 1000),
    object: {
      amount: 9900,
      customer: { email: "dave@sketchy.biz" },
    },
  });
  await delay(2000);

  console.log("\n✅ Demo complete! Check your Telegram for the agent's responses.");
}

runDemo().catch(console.error);

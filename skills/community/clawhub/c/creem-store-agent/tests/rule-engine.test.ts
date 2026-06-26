import { describe, it, expect } from "vitest";
import { formatEventAlert, getEventEmoji, getEventUrgency } from "../src/rule-engine";
import type { CreemWebhookPayload } from "../src/types";

describe("getEventEmoji", () => {
  it("returns 💰 for checkout.completed", () => {
    expect(getEventEmoji("checkout.completed")).toBe("💰");
  });

  it("returns 🎉 for subscription.active", () => {
    expect(getEventEmoji("subscription.active")).toBe("🎉");
  });

  it("returns 🔄 for subscription.paid", () => {
    expect(getEventEmoji("subscription.paid")).toBe("🔄");
  });

  it("returns ❌ for subscription.canceled", () => {
    expect(getEventEmoji("subscription.canceled")).toBe("❌");
  });

  it("returns ⏰ for subscription.scheduled_cancel", () => {
    expect(getEventEmoji("subscription.scheduled_cancel")).toBe("⏰");
  });

  it("returns ⚠️ for subscription.past_due", () => {
    expect(getEventEmoji("subscription.past_due")).toBe("⚠️");
  });

  it("returns ⏸️ for subscription.paused", () => {
    expect(getEventEmoji("subscription.paused")).toBe("⏸️");
  });

  it("returns 💀 for subscription.expired", () => {
    expect(getEventEmoji("subscription.expired")).toBe("💀");
  });

  it("returns 🆓 for subscription.trialing", () => {
    expect(getEventEmoji("subscription.trialing")).toBe("🆓");
  });

  it("returns 📝 for subscription.update", () => {
    expect(getEventEmoji("subscription.update")).toBe("📝");
  });

  it("returns 💸 for refund.created", () => {
    expect(getEventEmoji("refund.created")).toBe("💸");
  });

  it("returns 🚨 for dispute.created", () => {
    expect(getEventEmoji("dispute.created")).toBe("🚨");
  });
});

describe("getEventUrgency", () => {
  it("returns high for dispute.created", () => {
    expect(getEventUrgency("dispute.created")).toBe("high");
  });

  it("returns high for subscription.past_due", () => {
    expect(getEventUrgency("subscription.past_due")).toBe("high");
  });

  it("returns medium for refund.created", () => {
    expect(getEventUrgency("refund.created")).toBe("medium");
  });

  it("returns low for checkout.completed", () => {
    expect(getEventUrgency("checkout.completed")).toBe("low");
  });

  it("returns low for subscription.trialing", () => {
    expect(getEventUrgency("subscription.trialing")).toBe("low");
  });
});

describe("formatEventAlert", () => {
  it("formats checkout.completed with amount and customer email", () => {
    const payload: CreemWebhookPayload = {
      eventType: "checkout.completed",
      id: "evt_123",
      created_at: 1742198400,
      object: {
        amount: 4900,
        currency: "USD",
        customer: { email: "alice@example.com" },
        product: { name: "Pro Plan" },
      },
    };
    const msg = formatEventAlert(payload);
    expect(msg).toContain("💰");
    expect(msg).toContain("New Sale");
    expect(msg).toContain("$49.00");
    expect(msg).toContain("alice@example.com");
    expect(msg).toContain("Pro Plan");
  });

  it("formats subscription.past_due with urgency prefix", () => {
    const payload: CreemWebhookPayload = {
      eventType: "subscription.past_due",
      id: "evt_456",
      created_at: 1742198400,
      object: {
        customer: { email: "bob@example.com" },
        product: { name: "Starter" },
      },
    };
    const msg = formatEventAlert(payload);
    expect(msg).toContain("⚠️");
    expect(msg).toContain("URGENT");
    expect(msg).toContain("Payment Failed");
    expect(msg).toContain("bob@example.com");
  });

  it("formats dispute.created as urgent", () => {
    const payload: CreemWebhookPayload = {
      eventType: "dispute.created",
      id: "evt_789",
      created_at: 1742198400,
      object: {
        amount: 9900,
        customer: { email: "carol@example.com" },
      },
    };
    const msg = formatEventAlert(payload);
    expect(msg).toContain("🚨");
    expect(msg).toContain("URGENT");
    expect(msg).toContain("Dispute");
  });

  it("handles missing nested fields gracefully", () => {
    const payload: CreemWebhookPayload = {
      eventType: "subscription.active",
      id: "evt_000",
      created_at: 1742198400,
      object: {},
    };
    const msg = formatEventAlert(payload);
    expect(msg).toContain("🎉");
    expect(msg).not.toContain("undefined");
    expect(msg).not.toContain("null");
  });
});

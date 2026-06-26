import { describe, it, expect } from "vitest";
import { classifyEvent, isChurnEvent, CHURN_EVENTS } from "../src/event-processor";
import type { CreemWebhookPayload } from "../src/types";

function makePayload(eventType: string): CreemWebhookPayload {
  return {
    eventType: eventType as CreemWebhookPayload["eventType"],
    id: "evt_test",
    created_at: 1742198400,
    object: {},
  };
}

describe("isChurnEvent", () => {
  it("returns true for subscription.canceled", () => {
    expect(isChurnEvent("subscription.canceled")).toBe(true);
  });

  it("returns true for subscription.scheduled_cancel", () => {
    expect(isChurnEvent("subscription.scheduled_cancel")).toBe(true);
  });

  it("returns false for checkout.completed", () => {
    expect(isChurnEvent("checkout.completed")).toBe(false);
  });

  it("returns false for subscription.active", () => {
    expect(isChurnEvent("subscription.active")).toBe(false);
  });

  it("returns false for subscription.past_due", () => {
    expect(isChurnEvent("subscription.past_due")).toBe(false);
  });

  it("returns false for dispute.created", () => {
    expect(isChurnEvent("dispute.created")).toBe(false);
  });
});

describe("classifyEvent", () => {
  it('classifies subscription.canceled as "churn"', () => {
    const result = classifyEvent(makePayload("subscription.canceled"));
    expect(result.category).toBe("churn");
    expect(result.payload.eventType).toBe("subscription.canceled");
  });

  it('classifies subscription.scheduled_cancel as "churn"', () => {
    const result = classifyEvent(makePayload("subscription.scheduled_cancel"));
    expect(result.category).toBe("churn");
  });

  it('classifies checkout.completed as "simple"', () => {
    const result = classifyEvent(makePayload("checkout.completed"));
    expect(result.category).toBe("simple");
  });

  it('classifies dispute.created as "simple"', () => {
    const result = classifyEvent(makePayload("dispute.created"));
    expect(result.category).toBe("simple");
  });

  it('classifies subscription.past_due as "simple"', () => {
    const result = classifyEvent(makePayload("subscription.past_due"));
    expect(result.category).toBe("simple");
  });

  it("preserves the original payload in classification", () => {
    const payload = makePayload("subscription.paid");
    payload.object = { foo: "bar" };
    const result = classifyEvent(payload);
    expect(result.payload).toBe(payload);
    expect(result.payload.object).toEqual({ foo: "bar" });
  });
});

describe("CHURN_EVENTS", () => {
  it("contains exactly 2 events", () => {
    expect(CHURN_EVENTS).toHaveLength(2);
  });

  it("uses American spelling canceled (one L)", () => {
    expect(CHURN_EVENTS).toContain("subscription.canceled");
    expect(CHURN_EVENTS).not.toContain("subscription.cancelled");
  });
});

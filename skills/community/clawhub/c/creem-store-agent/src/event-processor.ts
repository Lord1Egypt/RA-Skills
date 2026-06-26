import type { CreemEventType, CreemWebhookPayload, ClassifiedEvent, EventCategory } from "./types.js";

export const CHURN_EVENTS: CreemEventType[] = [
  "subscription.canceled",
  "subscription.scheduled_cancel",
];

export function isChurnEvent(eventType: CreemEventType): boolean {
  return CHURN_EVENTS.includes(eventType);
}

export function classifyEvent(payload: CreemWebhookPayload): ClassifiedEvent {
  const category: EventCategory = isChurnEvent(payload.eventType) ? "churn" : "simple";
  return { category, payload };
}

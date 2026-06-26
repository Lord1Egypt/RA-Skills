import { IncomingMessage, ServerResponse } from "node:http";

// --- Creem Webhook Types ---

export type CreemEventType =
  | "checkout.completed"
  | "subscription.active"
  | "subscription.paid"
  | "subscription.canceled"
  | "subscription.scheduled_cancel"
  | "subscription.unpaid"
  | "subscription.past_due"
  | "subscription.paused"
  | "subscription.expired"
  | "subscription.trialing"
  | "subscription.update"
  | "refund.created"
  | "dispute.created";

export interface CreemWebhookPayload {
  eventType: CreemEventType;
  id: string;
  created_at: number; // Unix timestamp
  object: Record<string, unknown>;
}

// --- OpenClaw Plugin API ---

export interface OpenClawPluginApi {
  registerHttpRoute(config: {
    path: string;
    auth: "plugin" | "gateway";
    handler: (req: IncomingMessage, res: ServerResponse) => Promise<boolean>;
  }): void;
}

export interface SkillContext {
  api: OpenClawPluginApi;
  config: Record<string, string>;
  log: {
    info(msg: string): void;
    warn(msg: string): void;
    error(msg: string): void;
  };
}

// --- LLM Types ---

export interface ChurnContext {
  subscriptionId: string;
  customerId: string;
  productId: string;
  customerEmail: string;
  productName: string;
  price: number;
  tenureMonths: number;
  totalRevenue: number;
  cancelReason: string;
}

export type LLMAction = "CREATE_DISCOUNT" | "SUGGEST_PAUSE" | "NO_ACTION";

export interface LLMDecision {
  action: LLMAction;
  reason: string;
  confidence: number;
  params: {
    percentage?: number;
    durationMonths?: number;
  };
}

// --- Event Processor Types ---

export type EventCategory = "simple" | "churn";

export interface ClassifiedEvent {
  category: EventCategory;
  payload: CreemWebhookPayload;
}

// --- Action Executor Types ---

export interface ActionResult {
  success: boolean;
  action: LLMAction;
  details: string;
}

// --- Telegram Types ---

export interface TelegramBot {
  sendMessage(text: string, options?: {
    parse_mode?: "HTML" | "Markdown";
    reply_markup?: {
      inline_keyboard: Array<Array<{
        text: string;
        callback_data: string;
      }>>;
    };
  }): Promise<void>;
  onCallbackQuery(handler: (query: {
    data?: string;
    message?: { message_id: number };
  }) => void): void;
  onText(pattern: RegExp, handler: (msg: { chat: { id: number } }) => void): void;
}

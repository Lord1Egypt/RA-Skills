import { createHmac, timingSafeEqual } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import type { CreemWebhookPayload } from "./types.js";

export function verifySignature(body: string, signature: string, secret: string): boolean {
  if (!signature) return false;
  try {
    const expected = createHmac("sha256", secret).update(body).digest("hex");
    if (expected.length !== signature.length) return false;
    return timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
  } catch {
    return false;
  }
}

async function readBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }
  return Buffer.concat(chunks).toString("utf-8");
}

function jsonResponse(res: ServerResponse, status: number, body: Record<string, unknown>): true {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
  return true;
}

interface WebhookHandlerConfig {
  secret: string;
  onEvent: (payload: CreemWebhookPayload) => void | Promise<void>;
}

export function createWebhookHandler(config: WebhookHandlerConfig): (req: IncomingMessage, res: ServerResponse) => Promise<boolean> {
  const { secret, onEvent } = config;
  const processedEvents = new Set<string>();

  return async (req: IncomingMessage, res: ServerResponse): Promise<boolean> => {
    const body = await readBody(req);

    const signature = (req.headers["creem-signature"] as string) ?? "";
    if (!signature) {
      return jsonResponse(res, 401, { error: "Missing signature" });
    }

    if (!verifySignature(body, signature, secret)) {
      return jsonResponse(res, 401, { error: "Invalid signature" });
    }

    let payload: CreemWebhookPayload;
    try {
      payload = JSON.parse(body);
    } catch {
      return jsonResponse(res, 400, { error: "Invalid JSON" });
    }

    if (payload.id && processedEvents.has(payload.id)) {
      return jsonResponse(res, 200, { status: "ok", deduplicated: true });
    }
    if (payload.id) {
      processedEvents.add(payload.id);
    }

    try {
      await onEvent(payload);
    } catch {
      // Log but don't fail the webhook — Creem would retry
    }

    return jsonResponse(res, 200, { status: "ok" });
  };
}

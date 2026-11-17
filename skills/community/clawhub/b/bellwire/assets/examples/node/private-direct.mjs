// SPDX-License-Identifier: MIT-0
import { randomBytes } from "node:crypto";

import { verifyBellwireDirectRequest } from "../../../scripts/verify-direct-request.mjs";

/**
 * Framework-neutral Node 22 reference. Adapt Request/Response at the framework
 * boundary and implement every store callback with the project's real database.
 */
export function createBellwirePrivateHandler(configuration, store) {
  return async function handleBellwirePrivate(request) {
    const valid = await verifyBellwireDirectRequest(request, {
      connectionId: configuration.connectionId,
      keyId: configuration.deviceKeyId,
      signingPublicKey: configuration.signingPublicKey,
      // Must perform one INSERT under a UNIQUE(key_id, nonce) constraint.
      consumeNonce: (compoundNonce, timestamp) =>
        store.consumeNonceAtomically(compoundNonce, timestamp + 600),
    });
    if (!valid) return json({ error: "unauthorized" }, 401);

    const url = new URL(request.url);
    if (url.pathname === configuration.notificationPath) {
      const reference = opaqueReference(url.searchParams.get("ref"));
      if (!reference) return json({ error: "not_found" }, 404);
      const event = await store.notificationByReference(reference, new Date());
      return event ? boundedJSON(event, 64 * 1024) : json({ error: "not_found" }, 404);
    }

    if (url.pathname === configuration.inboxPath) {
      const cursor = url.searchParams.get("cursor") ?? undefined;
      const limit = Math.min(50, Math.max(1, Number(url.searchParams.get("limit") ?? "50")));
      return boundedJSON(await store.inboxPage({ cursor, limit }), 1024 * 1024);
    }

    if (url.pathname === configuration.surfacesPath) {
      return boundedJSON({ surfaces: await store.currentSurfaces() }, 1024 * 1024);
    }

    return json({ error: "not_found" }, 404);
  };
}

/**
 * Call from the same durable transaction that commits the business operation.
 * The row is the source of truth for notification and Inbox detail.
 */
export function newPrivateOutboxRecord(detail, now = new Date()) {
  return {
    reference: randomBytes(16).toString("base64url"),
    ...detail,
    occurredAt: detail.occurredAt ?? now.toISOString(),
    expiresAt: new Date(now.getTime() + 24 * 60 * 60 * 1_000).toISOString(),
  };
}

/**
 * Call only after the business transaction and outbox row have committed.
 */
export async function sendPrivateWake({
  apiUrl = "https://api.bellwire.app",
  projectId,
  token,
  reference,
  idempotencyKey,
}) {
  const response = await fetch(`${apiUrl}/v1/projects/${encodeURIComponent(projectId)}/private-wakes`, {
    method: "POST",
    signal: AbortSignal.timeout(5_000),
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
      "idempotency-key": idempotencyKey,
    },
    body: JSON.stringify({ reference, priority: "normal" }),
  });
  const result = await response.json().catch(() => ({}));
  if (result?.error?.code === "MONTHLY_SIGNAL_LIMIT_REACHED") {
    const error = new Error(`Bellwire quota reached until ${result.error.resetAt}`);
    error.retryable = false;
    throw error;
  }
  if (!response.ok) throw new Error(`Bellwire wake failed with status ${response.status}`);
  return result;
}

function opaqueReference(value) {
  return typeof value === "string" && /^[A-Za-z0-9_-]{22,200}$/u.test(value) ? value : null;
}

function boundedJSON(value, maximum) {
  const body = JSON.stringify(value);
  if (Buffer.byteLength(body) > maximum) return json({ error: "response_too_large" }, 500);
  return new Response(body, { headers: { "content-type": "application/json; charset=utf-8" } });
}

function json(value, status = 200) {
  return Response.json(value, { status });
}

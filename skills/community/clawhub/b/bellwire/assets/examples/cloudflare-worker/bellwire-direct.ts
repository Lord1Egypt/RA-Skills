// SPDX-License-Identifier: MIT-0
import { verifyBellwireDirectRequest } from "../../../scripts/verify-direct-request.mjs";

interface Env {
  BELLWIRE_CONNECTION_ID: string;
  BELLWIRE_DEVICE_KEY_ID: string;
  BELLWIRE_SIGNING_PUBLIC_KEY: string;
  BELLWIRE_DB: D1Database;
}

type PrivateEvent = {
  reference: string;
  eventType: string;
  title: string;
  body: string;
  subtitle?: string;
  occurredAt: string;
  data: Record<string, unknown>;
  deepLink?: string;
  logoUrl?: string;
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const valid = await verifyBellwireDirectRequest(request, {
      connectionId: env.BELLWIRE_CONNECTION_ID,
      keyId: env.BELLWIRE_DEVICE_KEY_ID,
      signingPublicKey: env.BELLWIRE_SIGNING_PUBLIC_KEY,
      consumeNonce: async (nonce: string) => {
        const result = await env.BELLWIRE_DB
          .prepare("insert or ignore into bellwire_nonces (nonce, expires_at) values (?, ?)")
          .bind(nonce, Math.floor(Date.now() / 1_000) + 600)
          .run();
        return result.meta.changes === 1;
      },
    });
    if (!valid) return Response.json({ error: "unauthorized" }, { status: 401 });

    const url = new URL(request.url);
    if (url.pathname === "/api/bellwire/v2/notification") {
      const reference = validOpaqueReference(url.searchParams.get("ref"));
      if (!reference) return Response.json({ error: "not_found" }, { status: 404 });
      const event = await privateEvent(env.BELLWIRE_DB, reference);
      return event
        ? jsonWithinLimit(event, 64 * 1024)
        : Response.json({ error: "not_found" }, { status: 404 });
    }

    if (url.pathname === "/api/bellwire/v2/inbox") {
      const limit = Math.min(50, Math.max(1, Number(url.searchParams.get("limit") ?? "50")));
      const rows = await env.BELLWIRE_DB.prepare(
        `select reference, event_type, title, body, subtitle, occurred_at, data_json,
                deep_link, logo_url
           from bellwire_private_outbox
          where expires_at > ?1
          order by occurred_at desc
          limit ?2`,
      ).bind(Math.floor(Date.now() / 1_000), limit).all();
      return jsonWithinLimit({
        events: rows.results.map(rowToPrivateEvent),
        nextCursor: null,
      }, 1024 * 1024);
    }

    if (url.pathname === "/api/bellwire/v2/surfaces") {
      return jsonWithinLimit({
        surfaces: [{
          id: "videosays-revenue-today",
          projectId: "11111111-1111-4111-8111-111111111112",
          surfaceKey: "revenue-today",
          type: "stats",
          title: "Today",
          subtitle: "Private direct connection",
          content: {
            metrics: [{ label: "Revenue", value: "¥128", color: "orange" }],
          },
          action: null,
          displayOrder: 10,
          version: 1,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          project: {
            id: "11111111-1111-4111-8111-111111111112",
            name: "VideoSays",
            icon: "play.rectangle.fill",
            logoUrl: "https://videosays.com/logo.png",
          },
        }],
      }, 1024 * 1024);
    }

    return Response.json({ error: "not_found" }, { status: 404 });
  },
};

async function privateEvent(database: D1Database, reference: string): Promise<PrivateEvent | null> {
  const row = await database.prepare(
    `select reference, event_type, title, body, subtitle, occurred_at, data_json,
            deep_link, logo_url
       from bellwire_private_outbox
      where reference = ?1 and expires_at > ?2
      limit 1`,
  ).bind(reference, Math.floor(Date.now() / 1_000)).first();
  return row ? rowToPrivateEvent(row) : null;
}

function rowToPrivateEvent(row: Record<string, unknown>): PrivateEvent {
  return {
    reference: String(row.reference),
    eventType: String(row.event_type),
    title: String(row.title),
    body: String(row.body),
    ...(row.subtitle ? { subtitle: String(row.subtitle) } : {}),
    occurredAt: String(row.occurred_at),
    data: JSON.parse(String(row.data_json ?? "{}")),
    ...(row.deep_link ? { deepLink: String(row.deep_link) } : {}),
    ...(row.logo_url ? { logoUrl: String(row.logo_url) } : {}),
  };
}

function validOpaqueReference(value: string | null): string | null {
  return value && /^[A-Za-z0-9_-]{22,200}$/u.test(value) ? value : null;
}

function jsonWithinLimit(value: unknown, maximum: number): Response {
  const body = JSON.stringify(value);
  if (new TextEncoder().encode(body).byteLength > maximum) {
    return Response.json({ error: "response_too_large" }, { status: 500 });
  }
  return new Response(body, { headers: { "content-type": "application/json; charset=utf-8" } });
}

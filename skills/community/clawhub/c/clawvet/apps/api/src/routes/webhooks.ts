import type { FastifyInstance } from "fastify";
import { eq, and } from "drizzle-orm";

const VALID_EVENTS = ["scan.complete", "scan.critical"];

export async function webhookRoutes(app: FastifyInstance) {
  // Register a webhook
  app.post<{
    Body: { url: string; events: string[] };
  }>("/api/v1/webhooks", async (request, reply) => {
    const apiKey = request.headers.authorization?.slice(7);
    if (!apiKey) {
      return reply.status(401).send({ error: "Missing API key" });
    }

    const { url, events } = request.body;
    if (!url || !events?.length) {
      return reply
        .status(400)
        .send({ error: "url and events are required" });
    }

    // Validate URL
    try {
      new URL(url);
    } catch {
      return reply.status(400).send({ error: "Invalid URL" });
    }

    // Validate events
    for (const event of events) {
      if (!VALID_EVENTS.includes(event)) {
        return reply
          .status(400)
          .send({ error: `Invalid event: ${event}. Valid: ${VALID_EVENTS.join(", ")}` });
      }
    }

    try {
      const { db, schema } = await import("../db/index.js");

      const user = await db.query.users.findFirst({
        where: eq(schema.users.apiKey, apiKey),
      });

      if (!user) {
        return reply.status(401).send({ error: "Invalid API key" });
      }

      const [webhook] = await db
        .insert(schema.webhooks)
        .values({
          userId: user.id,
          url,
          events,
        })
        .returning();

      return reply.status(201).send(webhook);
    } catch {
      return reply.status(503).send({ error: "Database not available" });
    }
  });

  // List webhooks
  app.get("/api/v1/webhooks", async (request, reply) => {
    const apiKey = request.headers.authorization?.slice(7);
    if (!apiKey) {
      return reply.status(401).send({ error: "Missing API key" });
    }

    try {
      const { db, schema } = await import("../db/index.js");

      const user = await db.query.users.findFirst({
        where: eq(schema.users.apiKey, apiKey),
      });

      if (!user) {
        return reply.status(401).send({ error: "Invalid API key" });
      }

      const hooks = await db.query.webhooks.findMany({
        where: eq(schema.webhooks.userId, user.id),
      });

      return reply.send({ webhooks: hooks });
    } catch {
      return reply.status(503).send({ error: "Database not available" });
    }
  });

  // Delete a webhook
  app.delete<{ Params: { id: string } }>(
    "/api/v1/webhooks/:id",
    async (request, reply) => {
      const apiKey = request.headers.authorization?.slice(7);
      if (!apiKey) {
        return reply.status(401).send({ error: "Missing API key" });
      }

      try {
        const { db, schema } = await import("../db/index.js");

        const user = await db.query.users.findFirst({
          where: eq(schema.users.apiKey, apiKey),
        });

        if (!user) {
          return reply.status(401).send({ error: "Invalid API key" });
        }

        const deleted = await db
          .delete(schema.webhooks)
          .where(
            and(
              eq(schema.webhooks.id, request.params.id),
              eq(schema.webhooks.userId, user.id)
            )
          )
          .returning();

        if (deleted.length === 0) {
          return reply.status(404).send({ error: "Webhook not found" });
        }

        return reply.send({ deleted: true });
      } catch {
        return reply.status(503).send({ error: "Database not available" });
      }
    }
  );
}

import type { OpenClawPlugin } from "openclaw/plugin-sdk/core";

/**
 * queue-wake plugin
 *
 * Provides an HTTP endpoint that the async-queue daemon calls when a task is due.
 * Delivers the task as a system event and immediately wakes the target agent's
 * heartbeat via requestHeartbeatNow — ensuring near-exact delivery timing.
 *
 * Endpoint: POST /api/queue-wake
 * Body:     { to: string, task: string }
 *
 * The `to` field can be:
 *   - A short agent name (e.g. "main", "myagent") → resolved to agent:<to>:main
 *   - A full session key (e.g. "agent:main:main") → used as-is
 */
const plugin: OpenClawPlugin = {
  register(api) {
    api.registerHttpRoute({
      path: "/api/queue-wake",
      auth: "plugin",
      match: "exact",
      handler: async (req, res) => {
        // Only allow POST
        if (req.method !== "POST") {
          res.statusCode = 405;
          res.end(JSON.stringify({ error: "Method not allowed" }));
          return true;
        }

        // Read body
        let body: { to?: string; task?: string; agentId?: string };
        try {
          const chunks: Buffer[] = [];
          for await (const chunk of req) chunks.push(chunk as Buffer);
          body = JSON.parse(Buffer.concat(chunks).toString());
        } catch {
          res.statusCode = 400;
          res.end(JSON.stringify({ error: "Invalid JSON body" }));
          return true;
        }

        const to = body.to ?? body.agentId;
        const task = body.task;

        if (!to || !task) {
          res.statusCode = 400;
          res.end(JSON.stringify({ error: "Missing required fields: to, task" }));
          return true;
        }

        // Resolve session key and agent ID
        // Supports both short names ("main") and full session keys ("agent:main:main")
        let sessionKey: string;
        let agentId: string;

        if (to.startsWith("agent:")) {
          // Full session key provided — e.g. "agent:main:main"
          sessionKey = to;
          const parts = to.split(":");
          agentId = parts[1] ?? to; // "main" from "agent:main:main"
        } else {
          // Short agent name — e.g. "main", "myagent"
          agentId = to;
          sessionKey = `agent:${to}:main`;
        }

        // Enqueue system event so the agent sees the task in context
        api.runtime.system.enqueueSystemEvent(
          `[QUEUE:${to}] ${task}`,
          { sessionKey }
        );

        // Wake the agent's heartbeat immediately for exact-time delivery
        api.runtime.system.requestHeartbeatNow({
          agentId,
          sessionKey,
          reason: "queue:delivery",
        });

        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ ok: true, to, sessionKey }));
        return true;
      },
    });
  },
};

export default plugin;

// POST /signal — appends a verdict signal to Redis
// Body: { slug, agent_id, verdict, days_kept, notes }
// Auth: Bearer token from CLAWBRAIN_API_KEY env var

import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

const SIGNALS_MAX = 1000;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Auth
  const auth = req.headers.authorization || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (!token || token !== process.env.CLAWBRAIN_API_KEY) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const { slug, agent_id, verdict, days_kept, notes } = req.body || {};

  if (!slug || !agent_id || !verdict) {
    return res.status(400).json({ error: "slug, agent_id, and verdict are required" });
  }

  const validVerdicts = ["keep", "remove", "flag"];
  if (!validVerdicts.includes(verdict)) {
    return res.status(400).json({ error: `verdict must be one of: ${validVerdicts.join(", ")}` });
  }

  const signal = {
    agent_id,
    verdict,
    days_kept: days_kept ?? null,
    notes: notes ?? null,
    ts: new Date().toISOString(),
  };

  const key = `signals:${slug}`;

  // Append signal and trim to last SIGNALS_MAX
  await redis.lpush(key, JSON.stringify(signal));
  await redis.ltrim(key, 0, SIGNALS_MAX - 1);

  return res.status(200).json({ ok: true, slug, verdict });
}

// GET /signals — returns aggregated signals for a list of slugs
// Query: ?slugs=deflate,token-saver,customer-research
// Returns per-slug: keep_count, flag_count, remove_count, avg_days_kept, last_signal_date, total_signals

import { Redis } from "@upstash/redis";

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { slugs: slugsParam } = req.query;
  if (!slugsParam) {
    return res.status(400).json({ error: "slugs query param is required" });
  }

  const slugs = slugsParam
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  if (slugs.length === 0) {
    return res.status(400).json({ error: "No valid slugs provided" });
  }

  if (slugs.length > 50) {
    return res.status(400).json({ error: "Maximum 50 slugs per request" });
  }

  const results = {};

  await Promise.all(
    slugs.map(async (slug) => {
      const key = `signals:${slug}`;
      const raw = await redis.lrange(key, 0, -1);

      const signals = raw
        .map((item) => {
          try {
            return typeof item === "string" ? JSON.parse(item) : item;
          } catch {
            return null;
          }
        })
        .filter(Boolean);

      if (signals.length === 0) {
        results[slug] = {
          keep_count: 0,
          flag_count: 0,
          remove_count: 0,
          avg_days_kept: null,
          last_signal_date: null,
          total_signals: 0,
        };
        return;
      }

      const keep_count = signals.filter((s) => s.verdict === "keep").length;
      const flag_count = signals.filter((s) => s.verdict === "flag").length;
      const remove_count = signals.filter((s) => s.verdict === "remove").length;

      const keptDays = signals
        .filter((s) => s.verdict === "keep" && s.days_kept != null)
        .map((s) => Number(s.days_kept));

      const avg_days_kept =
        keptDays.length > 0
          ? Math.round(keptDays.reduce((a, b) => a + b, 0) / keptDays.length)
          : null;

      const dates = signals.map((s) => s.ts).filter(Boolean).sort();
      const last_signal_date = dates.length > 0 ? dates[dates.length - 1] : null;

      results[slug] = {
        keep_count,
        flag_count,
        remove_count,
        avg_days_kept,
        last_signal_date,
        total_signals: signals.length,
      };
    })
  );

  return res.status(200).json(results);
}

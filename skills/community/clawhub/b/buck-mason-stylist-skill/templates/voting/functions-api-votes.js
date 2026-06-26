// GET /api/votes — returns the tally + the raw vote list for one lookbook.
//
// No auth: the URL is the shared secret. Don't link it from the public page;
// keep it for the customer. (The voting form at /api/vote IS linked from the
// page — that's intentional.)
export async function onRequestGet({ env }) {
  const prefix = `vote:${env.LOOKBOOK_ID || "unknown"}:`;
  const out = [];
  let cursor;
  while (true) {
    const opts = { prefix };
    if (cursor) opts.cursor = cursor;
    const list = await env.LOOKBOOK_VOTES.list(opts);
    for (const k of list.keys || []) {
      const v = await env.LOOKBOOK_VOTES.get(k.name);
      if (!v) continue;
      try {
        const parsed = JSON.parse(v);
        if (parsed && typeof parsed === "object") out.push(parsed);
      } catch {}
    }
    if (list.list_complete || !list.cursor) break;
    cursor = list.cursor;
  }

  const tally = { count: out.length, looks: {}, items: {}, voters: [] };
  const bucket = (map, key) => (map[key] ||= { up: 0, down: 0 });

  for (const r of out) {
    if (!r || typeof r !== "object") continue;
    for (const [look, v] of Object.entries(r.looks || {})) {
      if (v === "up" || v === "down") bucket(tally.looks, look)[v] += 1;
    }
    for (const [sku, v] of Object.entries(r.items || {})) {
      if (v === "up" || v === "down") bucket(tally.items, sku)[v] += 1;
    }
    tally.voters.push({
      voter: r.voter, ts: r.ts, comment: r.comment,
      looks: r.looks, items: r.items,
    });
  }
  return new Response(JSON.stringify({ ok: true, tally, votes: out }, null, 2), {
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

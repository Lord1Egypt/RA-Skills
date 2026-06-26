// POST /api/vote — appends one vote record to the bound KV namespace.
//
// Body (JSON):
//   {
//     voter:    string,                 // 1..60 chars
//     comment:  string,                 // 0..1000 chars
//     looks:    { lookN: "up"|"down" }, // optional per-look thumbs
//     items:    { <sku>: "up"|"down" }  // optional per-item thumbs (by SKU)
//   }
//
// Required bindings:
//   env.LOOKBOOK_VOTES   KV namespace (see wrangler.toml.example)
//   env.LOOKBOOK_ID      string var — uniquely identifies this lookbook so the
//                        same KV namespace can be shared across deployments.
//
// Stored key shape: vote:<lookbook_id>:<iso_ts>:<rand>
// Stored value:     JSON blob with the validated body + ip/ua/lookbook_id
//
// Why no auth: the URL itself is the shared secret (the partner gets the
// lookbook page URL from the customer). For higher-stakes deployments, add a
// session cookie or signed-link param here. The schema is forward-compatible.
export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); }
  catch { return json({ ok: false, error: "invalid json" }, 400); }

  const voter   = (body.voter   || "").toString().slice(0, 60).trim() || "anonymous";
  const comment = (body.comment || "").toString().slice(0, 1000);

  const looks = {};
  for (const [k, v] of Object.entries(body.looks || {})) {
    if (/^look[0-9]+$/.test(k) && (v === "up" || v === "down")) looks[k] = v;
  }
  const items = {};
  for (const [k, v] of Object.entries(body.items || {})) {
    const sku = String(k).slice(0, 64);
    if (sku && (v === "up" || v === "down")) items[sku] = v;
  }

  const ts   = new Date().toISOString();
  const rand = crypto.randomUUID().slice(0, 8);
  const record = {
    voter, comment, looks, items, ts,
    ip: request.headers.get("CF-Connecting-IP") || null,
    ua: (request.headers.get("user-agent") || "").slice(0, 200),
    lookbook_id: env.LOOKBOOK_ID || "unknown",
  };
  const key = `vote:${record.lookbook_id}:${ts}:${rand}`;
  await env.LOOKBOOK_VOTES.put(key, JSON.stringify(record));
  return json({ ok: true, key });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

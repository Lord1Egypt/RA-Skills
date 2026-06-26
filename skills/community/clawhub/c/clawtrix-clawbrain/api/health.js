// GET /api/health — liveness check
export default function handler(req, res) {
  res.status(200).json({ ok: true, service: "clawbrain", ts: new Date().toISOString() });
}

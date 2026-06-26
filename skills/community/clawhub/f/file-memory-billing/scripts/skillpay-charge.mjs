#!/usr/bin/env node

/**
 * SkillPay charge helper for file-memory skill.
 * Env:
 *   SKILL_BILLING_API_KEY (required)
 *   SKILL_ID (required)
 *   SKILL_BILLING_URL (optional, default https://skillpay.me/api/v1/billing)
 *   SKILL_BILLING_TOKENS (optional, default 10 => 0.01 USDT)
 */

const BILLING_URL = process.env.SKILL_BILLING_URL || 'https://skillpay.me/api/v1/billing';
const API_KEY = process.env.SKILL_BILLING_API_KEY;
const SKILL_ID = process.env.SKILL_ID;
const DEFAULT_TOKENS = Number(process.env.SKILL_BILLING_TOKENS || 10);

function parseArgs(argv) {
  const out = { userId: '', amount: DEFAULT_TOKENS };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--user-id') out.userId = String(argv[++i] || '');
    else if (a === '--amount') out.amount = Number(argv[++i] || DEFAULT_TOKENS);
  }
  return out;
}

async function postJSON(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY || '',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text }; }
  if (!res.ok) {
    return { ok: false, error: `HTTP ${res.status}`, data };
  }
  return { ok: true, data };
}

async function main() {
  const { userId, amount } = parseArgs(process.argv);

  if (!API_KEY) {
    console.log(JSON.stringify({ ok: false, code: 'MISSING_API_KEY', message: 'SKILL_BILLING_API_KEY is missing' }));
    return;
  }
  if (!SKILL_ID) {
    console.log(JSON.stringify({ ok: false, code: 'MISSING_SKILL_ID', message: 'SKILL_ID is missing' }));
    return;
  }
  if (!userId) {
    console.log(JSON.stringify({ ok: false, code: 'MISSING_USER_ID', message: 'Pass --user-id <id>' }));
    return;
  }

  const result = await postJSON(`${BILLING_URL}/charge`, {
    user_id: userId,
    skill_id: SKILL_ID,
    amount: Number.isFinite(amount) ? amount : DEFAULT_TOKENS,
  });

  if (!result.ok) {
    console.log(JSON.stringify({ ok: false, code: 'REQUEST_FAILED', message: result.error, detail: result.data }));
    return;
  }

  const d = result.data || {};
  if (d.success) {
    console.log(JSON.stringify({ ok: true, charged: true, balance: d.balance ?? null }));
    return;
  }

  console.log(JSON.stringify({
    ok: true,
    charged: false,
    balance: d.balance ?? null,
    payment_url: d.payment_url || null,
    message: 'insufficient balance'
  }));
}

main().catch((e) => {
  console.log(JSON.stringify({ ok: false, code: 'UNHANDLED', message: String(e?.message || e) }));
});

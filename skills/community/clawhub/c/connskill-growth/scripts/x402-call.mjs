#!/usr/bin/env node
// Standalone x402 client for CONNSKILL Growth Services (agent.connskill.com).
// Same payment path as the MCP server, usable from any agent that can run node.
//
//   node x402-call.mjs GET  /v1/locations '{"q":"munich"}'
//   node x402-call.mjs POST /v1/keyword-ideas '{"keyword":"agent commerce","location":"Germany"}'
//   node x402-call.mjs prices            # free: every endpoint with its USDC price
//
// Env: X402_WALLET_KEY (Base private key holding USDC; omit for free endpoints),
//      X402_MAX_USD (cap per paid call, default 1.00), X402_ORIGIN.
// Needs: npm i x402-fetch viem   (only for paid calls; free calls need nothing)
const ORIGIN = (process.env.X402_ORIGIN || 'https://agent.connskill.com').replace(/\/+$/, '');
const KEY = process.env.X402_WALLET_KEY || '';
const MAX_USD = Number(process.env.X402_MAX_USD || '1.00');
const [method = 'prices', path = '', json = '{}'] = process.argv.slice(2);

const out = (o) => { process.stdout.write(typeof o === 'string' ? o : JSON.stringify(o, null, 2)); process.stdout.write('\n'); };

if (method.toLowerCase() === 'prices') {
  const wk = await fetch(`${ORIGIN}/.well-known/x402`).then(r => r.json());
  out((wk.services || []).map(s => ({ endpoint: s.endpoint, usd: s.accepts?.[0]?.amount != null ? Number(s.accepts[0].amount) / 1e6 : null, summary: s.description || s.summary || '' })));
  process.exit(0);
}
if (!path.startsWith('/')) { console.error('usage: x402-call.mjs <GET|POST> </path> [json]'); process.exit(2); }

const args = JSON.parse(json);
const url = new URL(ORIGIN + path);
const opts = { method: method.toUpperCase(), headers: { 'user-agent': 'connskill-growth-skill/0.2' } };
if (opts.method === 'GET') for (const [k, v] of Object.entries(args)) if (v != null) url.searchParams.set(k, String(v));
else { opts.headers['content-type'] = 'application/json'; opts.body = JSON.stringify(args); }

let doFetch = fetch;
if (KEY) {
  const { privateKeyToAccount } = await import('viem/accounts');
  const { wrapFetchWithPayment } = await import('x402-fetch');
  const account = privateKeyToAccount(KEY.startsWith('0x') ? KEY : `0x${KEY}`);
  doFetch = wrapFetchWithPayment(fetch, account, BigInt(Math.round(MAX_USD * 1e6)));
}
const res = await doFetch(url.toString(), opts);
const text = await res.text();
if (res.status === 402) {
  let price = null; try { price = JSON.parse(text).accepts?.[0]?.amount; } catch {}
  console.error(`402 Payment Required${price ? ` (${Number(price) / 1e6} USDC)` : ''}. ${KEY ? 'Payment failed or above X402_MAX_USD.' : 'Set X402_WALLET_KEY (Base wallet with USDC) to pay per call. Free endpoints need no key.'}`);
  out(text); process.exit(1);
}
if (!res.ok) { console.error(`HTTP ${res.status}`); out(text); process.exit(1); }
out(text);

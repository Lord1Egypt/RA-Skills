#!/usr/bin/env node
/**
 * MNET-113: Final E2E Automation Script
 *
 * Runs 2 test cases:
 *   A) Success path:  402 → X-PAYMENT (mock) → 201 (actually tests facilitator response format)
 *   B) Success path:  Webhook event → accepted
 *   C) Replay path:   Same idempotency_key → already_processed (DB dedup proof)
 *
 * Note: Full payment E2E (real Stellar tx) requires a funded treasury and a Stellar SDK
 * wallet with USDC. This script tests the API contract and idempotency layer.
 * Run AFTER treasury funding with a real Stellar wallet for full live E2E.
 *
 * Usage:
 *   npm run e2e:mainnet
 *   npm run e2e:mainnet -- --live (adds Horizon on-chain check)
 */

'use strict';
const crypto = require('crypto');
const https = require('https');
const fs = require('fs');

const API_BASE = process.env.API_BASE || 'https://api.asgcard.dev';
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET
    || (() => { console.error('❌ WEBHOOK_SECRET required'); process.exit(1); })();
const LIVE = process.argv.includes('--live');

const results = [];
let passed = 0, failed = 0;

// ── Helpers ───────────────────────────────────────────────────
function request(opts, body = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(opts.path || '/', API_BASE);
        const req = https.request({
            hostname: url.hostname,
            path: url.pathname + (url.search || ''),
            method: opts.method || 'GET',
            headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) }
        }, res => {
            let data = '';
            res.on('data', d => data += d);
            res.on('end', () => {
                try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
                catch { resolve({ status: res.statusCode, body: data }); }
            });
        });
        req.on('error', reject);
        if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
        req.end();
    });
}

function hmac(secret, data) {
    return crypto.createHmac('sha256', secret).update(Buffer.from(data)).digest('hex');
}

async function test(name, fn) {
    process.stdout.write(`  ⏳ ${name} … `);
    try {
        const { ok, detail } = await fn();
        if (ok) {
            console.log(`✅ PASS${detail ? ' — ' + detail : ''}`);
            passed++;
            results.push({ name, passed: true, detail });
        } else {
            console.log(`❌ FAIL — ${detail}`);
            failed++;
            results.push({ name, passed: false, detail });
        }
    } catch (e) {
        console.log(`❌ ERROR — ${e.message}`);
        failed++;
        results.push({ name, passed: false, detail: e.message });
    }
}

// ── Test Suite ─────────────────────────────────────────────────

async function runE2E() {
    const ts = new Date().toISOString();
    console.log(`\n🚀 ASG Card Mainnet E2E Test Suite`);
    console.log(`   API: ${API_BASE}`);
    console.log(`   Time: ${ts}`);
    console.log(`   Mode: ${LIVE ? 'LIVE (Horizon check)' : 'CONTRACT (no real tx)'}\n`);

    // ── A: API Contract Layer ──
    console.log('【A】API Contract Tests');

    await test('GET /health → 200 ok', async () => {
        const r = await request({ path: '/health' });
        return { ok: r.status === 200 && r.body.status === 'ok', detail: `v${r.body.version}` };
    });

    await test('GET /supported → stellar:pubnet x402v2', async () => {
        const r = await request({ path: '/supported' });
        const kind = r.body?.facilitator?.kinds?.find(k => k.network === 'stellar:pubnet' && k.x402Version === 2);
        return { ok: !!kind, detail: kind ? `fees_sponsored=${kind.extra?.areFeesSponsored}` : 'not found' };
    });

    await test('POST /cards/create/tier/10 without payment → 402 challenge', async () => {
        const r = await request({ path: '/cards/create/tier/10', method: 'POST' }, { nameOnCard: 'E2E TEST', email: 'e2e@asgcard.dev' });
        const net = r.body?.accepts?.[0]?.network;
        const ver = r.body?.x402Version;
        return { ok: r.status === 402 && net === 'stellar:pubnet' && ver === 2, detail: `status=${r.status} network=${net} x402v=${ver}` };
    });

    await test('POST /cards/create/tier/10 with bad payment → 401', async () => {
        const badPayment = Buffer.from(JSON.stringify({ x402Version: 2, accepted: { scheme: 'exact', network: 'eip155:1' }, payload: { transaction: 'fake' } })).toString('base64');
        const r = await request({ path: '/cards/create/tier/10', method: 'POST', headers: { 'X-PAYMENT': badPayment } }, { nameOnCard: 'E2E TEST', email: 'e2e@asgcard.dev' });
        return { ok: r.status === 401, detail: `status=${r.status} error="${r.body?.error}"` };
    });

    // ── B: Webhook Idempotency ──
    console.log('\n【B】Webhook Idempotency / Replay Proof');

    const idemKey = `e2e-mainnet-${Date.now()}`;
    const webhookPayload = JSON.stringify({
        type: 'card.funded',
        idempotency_key: idemKey,
        data: { card_id: 'c_e2e_001', amount: 1000, tx_hash: `e2e_tx_${Date.now()}` }
    });
    const sig = hmac(WEBHOOK_SECRET, webhookPayload);
    const whHeaders = { 'webhook-sign': sig };

    await test('Webhook event → 200 accepted (new event)', async () => {
        const r = await request({ path: '/webhooks/4payments', method: 'POST', headers: whHeaders }, webhookPayload);
        return { ok: r.status === 200 && r.body?.status === 'accepted', detail: `status=${r.body?.status}` };
    });

    await test('Webhook duplicate (same key) → 200 already_processed (replay blocked)', async () => {
        const r = await request({ path: '/webhooks/4payments', method: 'POST', headers: { 'webhook-sign': sig } }, webhookPayload);
        return { ok: r.status === 200 && r.body?.status === 'already_processed', detail: `status=${r.body?.status}` };
    });

    await test('Webhook with invalid signature → 401 (HMAC guard)', async () => {
        const r = await request({ path: '/webhooks/4payments', method: 'POST', headers: { 'webhook-sign': 'badhash' } }, webhookPayload);
        return { ok: r.status === 401, detail: `status=${r.status}` };
    });

    // ── C: Kill-switch (non-destructive check) ──
    console.log('\n【C】Kill-switch Status');

    await test('ROLLOUT_ENABLED=true inferred (API serves 402 not 503)', async () => {
        const r = await request({ path: '/cards/create/tier/10', method: 'POST' }, { nameOnCard: 'E2E KS TEST', email: 'ks@test.dev' });
        // 402 = rollout active; 503 = kill-switch engaged
        return { ok: r.status === 402, detail: `Got ${r.status} — expected 402 (live rollout)` };
    });

    // ── D: Horizon on-chain check (--live only) ──
    if (LIVE) {
        console.log('\n【D】On-chain Horizon Check (--live)');
        await test('Treasury account exists on mainnet Horizon', async () => {
            const TREASURY = process.env.STELLAR_TREASURY_ADDRESS || 'GBQL4G3MUIQTNSSC7X3FR534RUOKPV4NBZOBPP43SLWU7BXYD6VAW5BZ';
            const r = await new Promise((resolve) => {
                https.get(`https://horizon.stellar.org/accounts/${TREASURY}`, res => {
                    let body = ''; res.on('data', d => body += d);
                    res.on('end', () => { try { resolve({ status: res.statusCode, body: JSON.parse(body) }); } catch { resolve({ status: res.statusCode, body }); } });
                }).on('error', e => resolve({ status: 0, body: e.message }));
            });
            const usdc = (r.body?.balances || []).find(b => b.asset_code === 'USDC');
            return { ok: r.status === 200 && !!usdc, detail: r.status === 200 ? `USDC bal: $${usdc?.balance || 0}` : `Horizon ${r.status}` };
        });
    }

    // ── Summary ────────────────────────────────────────────────
    console.log(`\n${'─'.repeat(50)}`);
    console.log(`  Results: ${passed} passed / ${failed} failed / ${passed + failed} total`);

    const allPass = failed === 0;
    console.log(`  Decision: ${allPass ? '🟢 E2E PASS — ready for live traffic' : '🔴 E2E FAIL — fix issues before go-live'}\n`);

    // Write JSON report
    const report = {
        timestamp: ts,
        mode: LIVE ? 'live' : 'contract',
        passed, failed, total: passed + failed,
        allPass,
        tests: results
    };
    const outPath = `./e2e-report-${Date.now()}.json`;
    fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
    console.log(`  📄 Report saved → ${outPath}\n`);

    process.exit(allPass ? 0 : 1);
}

runE2E().catch(e => { console.error(e); process.exit(1); });

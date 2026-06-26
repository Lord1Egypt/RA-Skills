#!/usr/bin/env node
/**
 * MNET-112: Pre-Funding Readiness Script
 *
 * Checks:
 *   1. Stellar account exists on mainnet
 *   2. USDC trustline established
 *   3. USDC balance >= threshold (default: $200)
 *   4. API health endpoint reachable
 *   5. /supported returns stellar:pubnet x402v2
 *
 * Usage:
 *   node scripts/preflight.js [--threshold=200] [--out=./report.json]
 *   npm run preflight
 */

'use strict';
const https = require('https');
const fs = require('fs');
const path = require('path');

// ── Config ────────────────────────────────────────────────────
const TREASURY = process.env.STELLAR_TREASURY_ADDRESS
    || 'GBQL4G3MUIQTNSSC7X3FR534RUOKPV4NBZOBPP43SLWU7BXYD6VAW5BZ';
const HORIZON = process.env.STELLAR_HORIZON_URL
    || 'https://horizon.stellar.org';
const USDC_ISSUER = 'GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN';
const API_BASE = process.env.API_BASE || 'https://api.asgcard.dev';
const THRESHOLD = parseFloat((process.argv.find(a => a.startsWith('--threshold=')) || '--threshold=200').split('=')[1]);
const OUT_FILE = (process.argv.find(a => a.startsWith('--out=')) || '--out=./preflight-report.json').split('=')[1];

// ── Helpers ───────────────────────────────────────────────────
function get(url) {
    return new Promise((resolve, reject) => {
        https.get(url, res => {
            let body = '';
            res.on('data', d => body += d);
            res.on('end', () => {
                try { resolve({ status: res.statusCode, body: JSON.parse(body) }); }
                catch { resolve({ status: res.statusCode, body }); }
            });
        }).on('error', reject);
    });
}

function getApi(path) {
    return get(API_BASE + path);
}

function check(name, passed, detail = '') {
    const icon = passed ? '✅' : '❌';
    console.log(`  ${icon} ${name}${detail ? ': ' + detail : ''}`);
    return { name, passed, detail };
}

// ── Checks ────────────────────────────────────────────────────
async function checkAccount() {
    const { status, body } = await get(`${HORIZON}/accounts/${TREASURY}`);
    if (status !== 200) return check('Account exists on mainnet', false, `Horizon ${status} — account not found/funded`);
    // Check XLM balance
    const xlm = (body.balances || []).find(b => b.asset_type === 'native');
    const xlmBal = xlm ? parseFloat(xlm.balance) : 0;
    return check('Account exists on mainnet', true, `XLM balance: ${xlmBal}`);
}

async function checkTrustline(horizonAccount) {
    if (!horizonAccount) return check('USDC trustline exists', false, 'Cannot check — account missing');
    const { status, body } = await get(`${HORIZON}/accounts/${TREASURY}`);
    if (status !== 200) return check('USDC trustline exists', false, 'Horizon error');
    const usdc = (body.balances || []).find(b => b.asset_code === 'USDC' && b.asset_issuer === USDC_ISSUER);
    if (!usdc) return check('USDC trustline exists', false, `No USDC trustline for issuer ${USDC_ISSUER}`);
    return check('USDC trustline exists', true, `limit: ${usdc.limit}`);
}

async function checkUsdcBalance() {
    const { status, body } = await get(`${HORIZON}/accounts/${TREASURY}`);
    if (status !== 200) return { check: check(`USDC balance >= $${THRESHOLD}`, false, 'Cannot check — account missing'), balance: 0 };
    const usdc = (body.balances || []).find(b => b.asset_code === 'USDC' && b.asset_issuer === USDC_ISSUER);
    const bal = usdc ? parseFloat(usdc.balance) : 0;
    return {
        check: check(`USDC balance >= $${THRESHOLD}`, bal >= THRESHOLD, `$${bal.toFixed(2)}`),
        balance: bal
    };
}

async function checkApiHealth() {
    try {
        const { status, body } = await getApi('/health');
        if (status !== 200 || body.status !== 'ok') return check('API health', false, `status=${status}`);
        return check('API health', true, `v${body.version}`);
    } catch (e) {
        return check('API health', false, e.message);
    }
}

async function checkFacilitator() {
    try {
        const { status, body } = await getApi('/supported');
        const kinds = body?.facilitator?.kinds || [];
        const mainnet = kinds.find(k => k.network === 'stellar:pubnet' && k.x402Version === 2);
        if (!mainnet) return check('/supported → stellar:pubnet x402v2', false, JSON.stringify(kinds[0] || {}));
        return check('/supported → stellar:pubnet x402v2', true, `fees_sponsored=${mainnet.extra?.areFeesSponsored}`);
    } catch (e) {
        return check('/supported → stellar:pubnet x402v2', false, e.message);
    }
}

async function check402Challenge() {
    try {
        const { status, body } = await new Promise((resolve, reject) => {
            const req = https.request({
                hostname: new URL(API_BASE).hostname,
                path: '/cards/create/tier/10',
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Content-Length': 2 }
            }, res => {
                let body = '';
                res.on('data', d => body += d);
                res.on('end', () => {
                    try { resolve({ status: res.statusCode, body: JSON.parse(body) }); }
                    catch { resolve({ status: res.statusCode, body }); }
                });
            });
            req.on('error', reject);
            req.write('{}');
            req.end();
        });
        if (status !== 402) return check('x402 challenge returns HTTP 402', false, `Got ${status}`);
        const net = body?.accepts?.[0]?.network || 'missing';
        const ver = body?.x402Version;
        return check('x402 challenge returns HTTP 402', true, `network=${net} version=${ver}`);
    } catch (e) {
        return check('x402 challenge returns HTTP 402', false, e.message);
    }
}

// ── Main ──────────────────────────────────────────────────────
async function main() {
    const ts = new Date().toISOString();
    console.log(`\n🔍 ASG Card Mainnet Pre-Funding Readiness Check`);
    console.log(`   Treasury: ${TREASURY}`);
    console.log(`   Threshold: $${THRESHOLD} USDC`);
    console.log(`   Time: ${ts}\n`);

    const results = {};

    results.apiHealth = await checkApiHealth();
    results.facilitator = await checkFacilitator();
    results.x402Challenge = await check402Challenge();
    results.accountExists = await checkAccount();
    results.trustline = await checkTrustline(results.accountExists.passed);
    const { check: balCheck, balance } = await checkUsdcBalance();
    results.usdcBalance = balCheck;

    const checks = Object.values(results);
    const passed = checks.filter(c => c.passed).length;
    const total = checks.length;
    const allPass = passed === total;

    // Technical gates (excluding treasury funding)
    const techGates = ['apiHealth', 'facilitator', 'x402Challenge'];
    const techPass = techGates.every(k => results[k].passed);

    console.log(`\n${'─'.repeat(50)}`);
    console.log(`  Total: ${passed}/${total} checks passed`);
    console.log(`  Tech gates (no treasury): ${techPass ? '✅ READY' : '❌ NOT READY'}`);
    console.log(`  Treasury funded: ${results.usdcBalance.passed ? '✅ YES' : '❌ NO — fund before E2E'}`);
    console.log(`  READINESS: ${allPass ? '🟢 FULL GO' : techPass ? '🟡 CONDITIONAL GO (fund treasury)' : '🔴 NOT READY'}`);

    // ── Report output ──────────────────────────────────────────
    const report = {
        timestamp: ts,
        treasury: TREASURY,
        threshold: THRESHOLD,
        checks: results,
        summary: {
            passed, total, allPass, techPass,
            usdcBalance: balance,
            readiness: allPass ? 'FULL_GO' : techPass ? 'CONDITIONAL_GO' : 'NOT_READY'
        }
    };

    const outPath = path.resolve(OUT_FILE);
    fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
    console.log(`\n  📄 Report saved → ${outPath}`);

    // ── Markdown summary ───────────────────────────────────────
    const mdLines = [
        `# Preflight Report — ${ts}`,
        '',
        `| Check | Status | Detail |`,
        `|---|---|---|`,
        ...checks.map(c => `| ${c.name} | ${c.passed ? '✅ PASS' : '❌ FAIL'} | ${c.detail || ''} |`),
        '',
        `## Decision: ${report.summary.readiness}`,
        '',
        allPass
            ? `All checks pass. Ready for full E2E and live traffic.`
            : techPass
                ? `Technical gates pass. **Fund treasury** then re-run: \`npm run preflight\``
                : `Critical failures. Fix before proceeding.`,
    ];
    const mdPath = outPath.replace('.json', '.md');
    fs.writeFileSync(mdPath, mdLines.join('\n'));
    console.log(`  📄 Markdown → ${mdPath}\n`);

    process.exit(allPass ? 0 : techPass ? 2 : 1);
}

main().catch(e => { console.error(e); process.exit(1); });

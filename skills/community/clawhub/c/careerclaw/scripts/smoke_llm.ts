/**
 * scripts/smoke_llm.ts — LLM connectivity and Pro key smoke test.
 *
 * Validates credentials before the LLM enhancement module is wired in.
 * Does NOT run the full briefing pipeline — use smoke_briefing.ts for that.
 *
 * What this tests:
 *   1. Pro key presence (CAREERCLAW_PRO_KEY is set and non-empty)
 *   2. LLM key resolution (provider-specific keys > legacy fallback)
 *   3. LLM API connectivity (minimal prompt → valid response)
 *
 * What this does NOT test (deferred until LLM enhancement module ships):
 *   - Draft enhancement quality or word count
 *   - Failover chain behavior
 *
 * Usage:
 *   # Load from .env file (Node 20+)
 *   node --env-file=.env -e "import('./scripts/smoke_llm.ts')"
 *   npx tsx --env-file=.env scripts/smoke_llm.ts
 *
 *   # Inline (PowerShell)
 *   $env:CAREERCLAW_PRO_KEY="your-key"; $env:CAREERCLAW_ANTHROPIC_KEY="sk-ant-..."; npx tsx scripts/smoke_llm.ts
 *
 *   # Inline (bash)
 *   CAREERCLAW_PRO_KEY=your-key CAREERCLAW_ANTHROPIC_KEY=sk-ant-... npx tsx scripts/smoke_llm.ts
 *
 * Exit codes:
 *   0 — all checks passed
 *   1 — one or more checks failed
 */

import {
  PRO_KEY,
  GUMROAD_PRODUCT_ID,
  LLM_ANTHROPIC_KEY,
  LLM_OPENAI_KEY,
  LLM_API_KEY,
  LLM_PROVIDER,
  LLM_MODEL,
  LLM_CHAIN,
} from "../src/config.js";
import { checkLicense } from "../src/license.js";

const PASS = "\x1b[32m✓\x1b[0m";
const FAIL = "\x1b[31m✗\x1b[0m";
const WARN = "\x1b[33m⚠\x1b[0m";
const BOLD = "\x1b[1m";
const RESET = "\x1b[0m";

// ---------------------------------------------------------------------------
// Key resolution — mirrors the priority order the LLM module will use
// ---------------------------------------------------------------------------

function resolveKey(provider: string): string | undefined {
  if (provider === "anthropic") {
    return LLM_ANTHROPIC_KEY ?? LLM_API_KEY;
  }
  if (provider === "openai") {
    return LLM_OPENAI_KEY ?? LLM_API_KEY;
  }
  return LLM_API_KEY;
}

/** Derive active provider from key format when LLM_PROVIDER is not overridden. */
function resolveProvider(): string {
  // If the key is set explicitly, trust LLM_PROVIDER
  if (LLM_ANTHROPIC_KEY) return "anthropic";
  if (LLM_OPENAI_KEY) return "openai";
  // Legacy key — infer from prefix
  if (LLM_API_KEY?.startsWith("sk-ant-")) return "anthropic";
  if (LLM_API_KEY?.startsWith("sk-")) return "openai";
  return LLM_PROVIDER;
}

function redact(key: string): string {
  if (key.length <= 10) return "***";
  return key.slice(0, 8) + "..." + key.slice(-4);
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------

async function callAnthropic(apiKey: string, model: string): Promise<string> {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model,
      max_tokens: 32,
      messages: [{ role: "user", content: "Reply with exactly: CareerClaw LLM OK" }],
    }),
    signal: AbortSignal.timeout(15_000),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "(no body)");
    throw new Error(`HTTP ${res.status}: ${body.slice(0, 200)}`);
  }

  const data = await res.json() as { content: Array<{ type: string; text: string }> };
  return data.content?.[0]?.text?.trim() ?? "(empty response)";
}

async function callOpenAI(apiKey: string, model: string): Promise<string> {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      max_tokens: 32,
      messages: [{ role: "user", content: "Reply with exactly: CareerClaw LLM OK" }],
    }),
    signal: AbortSignal.timeout(15_000),
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "(no body)");
    throw new Error(`HTTP ${res.status}: ${body.slice(0, 200)}`);
  }

  const data = await res.json() as { choices: Array<{ message: { content: string } }> };
  return data.choices?.[0]?.message?.content?.trim() ?? "(empty response)";
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function run(): Promise<void> {
  console.log(`\n${BOLD}=== CareerClaw LLM & Pro Key Smoke Test ===${RESET}\n`);
  let passed = 0;
  let failed = 0;

  // ---- 1. Pro license validation ----
  console.log(`${BOLD}1. Pro License Key${RESET}`);
  if (!PRO_KEY || PRO_KEY.trim().length === 0) {
    console.log(`  ${FAIL} CAREERCLAW_PRO_KEY is not set`);
    console.log(`       Purchase: https://ogm.gumroad.com/l/careerclaw-pro`);
    failed++;
  } else {
    console.log(`  ${PASS} CAREERCLAW_PRO_KEY is set (${redact(PRO_KEY)})`);
    process.stdout.write(`  Validating against Gumroad… `);
    try {
      const result = await checkLicense(PRO_KEY);
      if (result.valid) {
        console.log(`${PASS} valid (source: ${result.source})`);
        passed++;
      } else {
        console.log(`${FAIL} invalid or not found (source: ${result.source})`);
        console.log(`       Check your CAREERCLAW_PRO_KEY value.`);
        failed++;
      }
    } catch (err) {
      console.log(`${WARN} Gumroad threw unexpectedly: ${String(err)}`);
      failed++;
    }
  }
  console.log();

  // ---- 2. LLM key resolution ----
  console.log(`${BOLD}2. LLM Key Resolution${RESET}`);
  const provider = resolveProvider();
  const apiKey = resolveKey(provider);

  if (LLM_ANTHROPIC_KEY) {
    console.log(`  ${PASS} CAREERCLAW_ANTHROPIC_KEY is set (${redact(LLM_ANTHROPIC_KEY)})`);
  } else {
    console.log(`  ${WARN} CAREERCLAW_ANTHROPIC_KEY not set`);
  }

  if (LLM_OPENAI_KEY) {
    console.log(`  ${PASS} CAREERCLAW_OPENAI_KEY is set (${redact(LLM_OPENAI_KEY)})`);
  } else {
    console.log(`  ${WARN} CAREERCLAW_OPENAI_KEY not set`);
  }

  if (LLM_API_KEY && !LLM_ANTHROPIC_KEY && !LLM_OPENAI_KEY) {
    console.log(`  ${WARN} CAREERCLAW_LLM_KEY set (legacy fallback: ${redact(LLM_API_KEY)})`);
  }

  if (!apiKey) {
    console.log(`  ${FAIL} No LLM key found — set CAREERCLAW_ANTHROPIC_KEY or CAREERCLAW_OPENAI_KEY`);
    failed++;
    console.log();
    console.log(`${BOLD}3. LLM API Connectivity${RESET}`);
    console.log(`  ${FAIL} Skipped — no key available\n`);
    summarise(passed, failed);
    return;
  }

  console.log(`  ${PASS} Active provider: ${provider}`);
  const activeModel = LLM_MODEL !== "claude-haiku-4-5-20251001" ? LLM_MODEL :
    provider === "openai" ? "gpt-4o-mini" : "claude-haiku-4-5-20251001";
  console.log(`  ${PASS} Active model:    ${activeModel}`);
  console.log(`  ${PASS} Failover chain:  ${LLM_CHAIN}`);
  passed++;
  console.log();

  // ---- 3. LLM API connectivity ----
  console.log(`${BOLD}3. LLM API Connectivity${RESET}`);
  console.log(`  Calling ${provider} (${activeModel}) …`);

  try {
    const start = Date.now();
    let response: string;

    if (provider === "anthropic") {
      response = await callAnthropic(apiKey, activeModel);
    } else if (provider === "openai") {
      response = await callOpenAI(apiKey, activeModel);
    } else {
      throw new Error(`Unknown provider: ${provider}`);
    }

    const ms = Date.now() - start;
    console.log(`  ${PASS} Response received in ${ms}ms`);
    console.log(`  ${PASS} Response: "${response}"`);
    passed++;
  } catch (err) {
    console.log(`  ${FAIL} API call failed: ${String(err)}`);
    failed++;
  }

  console.log();
  summarise(passed, failed);
}

function summarise(passed: number, failed: number): void {
  const total = passed + failed;
  if (failed === 0) {
    console.log(`${PASS} All ${total} checks passed\n`);
    process.exit(0);
  } else {
    console.log(`${FAIL} ${failed}/${total} checks failed — see above\n`);
    process.exit(1);
  }
}

run();
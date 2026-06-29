#!/usr/bin/env node
/**
 * preflight.js — Skill Evolver Installation Preflight Check
 *
 * Run after installing skill-evolver to verify the full pipeline can work.
 *
 * Side effects:
 *   --fix        Creates missing directories (filesystem write)
 *   --probe-llm  Sends real HTTP requests to configured LLM providers using
 *                stored API credentials to verify connectivity (network egress)
 *               Default: LLM connectivity check is skipped (offline mode)
 *
 * Usage:
 *   node scripts/preflight.js [--verbose] [--fix] [--probe-llm]
 *
 * Exit codes:
 *   0: all checks passed
 *   1: one or more checks failed
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const SCRIPT_DIR = __dirname;
const EVOLVER_DIR = path.resolve(SCRIPT_DIR, '..');

const verbose = process.argv.includes('--verbose');
const autoFix = process.argv.includes('--fix');
const probeLLM = process.argv.includes('--probe-llm');

let passed = 0;
let warned = 0;
let failed = 0;

function ok(name, detail) {
  passed++;
  console.log(`  ✅ ${name}${detail ? ': ' + detail : ''}`);
}
function warn(name, detail) {
  warned++;
  console.log(`  ⚠️  ${name}${detail ? ': ' + detail : ''}`);
}
function fail(name, detail) {
  failed++;
  console.log(`  ❌ ${name}${detail ? ': ' + detail : ''}`);
}

// ─── 1. Environment ────────────────────────────────────────────

console.log('\n🔍 1. Environment');

// Node version
const nodeVer = process.version;
const major = parseInt(nodeVer.slice(1));
if (major >= 18) ok('Node.js', nodeVer);
else fail('Node.js', `${nodeVer} (need ≥18)`);

// OpenClaw installation
let ocRoot = null;
try {
  // Pure JS `which` — find executable in PATH without child_process
  const dirs = (process.env.PATH || '').split(path.delimiter);
  let bin = null;
  for (const dir of dirs) {
    const full = path.join(dir, 'openclaw');
    try { fs.accessSync(full, fs.constants.X_OK); bin = full; break; } catch {}
  }
  if (bin) {
    const real = fs.realpathSync(bin);
    const parts = real.split(path.sep);
    const nmIdx = parts.lastIndexOf('node_modules');
    if (nmIdx >= 0) ocRoot = parts.slice(0, nmIdx + 2).join(path.sep);
  }
} catch { /* fallback */ }
if (!ocRoot) {
  try {
    const candidate = path.resolve(path.dirname(process.execPath), '..', 'lib', 'node_modules', 'openclaw');
    if (fs.existsSync(candidate)) ocRoot = candidate;
  } catch {}
}

if (ocRoot) ok('OpenClaw root', ocRoot);
else fail('OpenClaw root', 'cannot resolve — `which openclaw` failed and execPath fallback not found');

// ─── 2. Sessions Directory ────────────────────────────────────

console.log('\n🔍 2. Sessions Directory');

// HOME covers Linux/macOS; empty string means candidate gets filtered if missing
const home = process.env.HOME || '';
const { getAdapter } = require('./lib/platform-detect');
const sessionCandidates = [];
// Cross-platform: use adapter detection first
try {
  const adapter = getAdapter();
  const adapterPaths = adapter.detectPaths();
  sessionCandidates.push(...adapterPaths);
} catch (err) {
  // Adapter detection failed, use legacy paths
}
// Legacy fallback: OpenClaw-specific paths
if (process.env.OPENCLAW_STATE_DIR) {
  sessionCandidates.push(path.join(process.env.OPENCLAW_STATE_DIR, 'agents/main/sessions'));
}
if (home) {
  sessionCandidates.push(path.join(home, '.openclaw', 'agents', 'main', 'sessions'));
}

// Validate candidate: must exist, contain .jsonl files, and have at least one
// modified in the last 7 days (indicates live/active data, not a stale path)
function validateSessionsDir(d) {
  if (!fs.existsSync(d)) return { valid: false, reason: 'not_found' };
  const files = fs.readdirSync(d).filter(f => f.endsWith('.jsonl'));
  if (files.length === 0) return { valid: false, reason: 'no_jsonl_files', count: 0 };
  const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
  const hasRecent = files.some(f => {
    try { return fs.statSync(path.join(d, f)).mtimeMs > cutoff; } catch { return false; }
  });
  return { valid: true, count: files.length, active: hasRecent };
}

let sessionsDir = null;
let sessionsMeta = null;
for (const d of sessionCandidates) {
  const meta = validateSessionsDir(d);
  if (meta.valid) {
    sessionsDir = d;
    sessionsMeta = meta;
    break; // first valid candidate wins (priority order)
  }
}

if (sessionsDir) {
  const activeTag = sessionsMeta.active ? '' : ' ⚠️ no recent activity (>7d)';
  ok('Sessions dir', `${sessionsDir} (${sessionsMeta.count} session files${activeTag})`);

  if (sessionsMeta.count < 5) {
    warn('Session count', `only ${sessionsMeta.count} — need ≥5 skill invocations to trigger first evolution`);
  } else {
    ok('Session count', `${sessionsMeta.count} files available`);
  }
} else {
  // Output structured hint for agent to resolve without bothering the user
  const tried = sessionCandidates.length > 0 ? sessionCandidates.join(', ') : '(none — set OPENCLAW_STATE_DIR)';
  fail('Sessions dir', `MISSING — tried: ${tried} | fix: set OPENCLAW_STATE_DIR=<openclaw-data-root>`);
}

// ─── 3. Skill Discovery (Patcher Paths) ───────────────────────

console.log('\n🔍 3. Skill Discovery');

// Local skills
const localSkillDirs = [
  path.resolve(EVOLVER_DIR, '..'),
  path.join(home, '.openclaw', 'skills'),
].filter((d, i, arr) => fs.existsSync(d) && arr.indexOf(d) === i);

if (localSkillDirs.length > 0) {
  const allSkills = new Set();
  for (const d of localSkillDirs) {
    fs.readdirSync(d).filter(f => {
      const smd = path.join(d, f, 'SKILL.md');
      if (fs.existsSync(smd)) allSkills.add(f);
    });
  }
  ok('Local skills', `${allSkills.size} skills in ${localSkillDirs.join(', ')}`);
} else {
  warn('Local skills', 'no local skills directory found');
}

// Bundled skills
if (ocRoot) {
  const bundledPaths = ['skills', 'skills/others', 'skills/tencent'].map(p => path.join(ocRoot, p));
  let bundledCount = 0;
  for (const bp of bundledPaths) {
    if (!fs.existsSync(bp)) continue;
    for (const entry of fs.readdirSync(bp)) {
      if (fs.existsSync(path.join(bp, entry, 'SKILL.md'))) bundledCount++;
    }
  }
  if (bundledCount > 0) ok('Bundled skills', `${bundledCount} skills found under ${ocRoot}/skills/`);
  else warn('Bundled skills', 'none found');
  
  // Extensions
  const extRoot = path.join(ocRoot, 'extensions');
  if (fs.existsSync(extRoot)) {
    let extCount = 0;
    const walk = (dir, depth) => {
      if (depth > 3) return;
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        if (!entry.isDirectory() || entry.name === 'node_modules') continue;
        const full = path.join(dir, entry.name);
        if (entry.name === 'skills') {
          for (const s of fs.readdirSync(full)) {
            if (fs.existsSync(path.join(full, s, 'SKILL.md'))) extCount++;
          }
        } else {
          walk(full, depth + 1);
        }
      }
    };
    walk(extRoot, 0);
    if (extCount > 0) ok('Extension skills', `${extCount} skills in extensions/`);
    else ok('Extension skills', 'no extension skills (this is normal)');
  } else {
    ok('Extension skills', 'no extensions/ dir (this is normal)');
  }
} else {
  warn('Bundled skills', 'skipped (OpenClaw root not found)');
}

// ─── 4. Trace Extraction ──────────────────────────────────────

console.log('\n🔍 4. Trace Extraction Pipeline');

// Syntax check all scripts
const scripts = ['trace-extractor.js', 'generator.js', 'validator.js', 'lifecycle.js', 'monitor.js', 'evolver-cli.js'];
let syntaxOk = true;
for (const s of scripts) {
  const fp = path.join(SCRIPT_DIR, s);
  if (!fs.existsSync(fp)) {
    fail(`Script ${s}`, 'missing');
    syntaxOk = false;
    continue;
  }
  try {
    execFileSync(process.execPath, ['-c', fp], { encoding: 'utf8', stdio: 'pipe' });
  } catch (e) {
    fail(`Script ${s}`, 'syntax error');
    syntaxOk = false;
  }
}
if (syntaxOk) ok('Script syntax', `all ${scripts.length} scripts valid`);

// Shell script — find bash via BASH_PATH env or PATH
function findBash() {
  if (process.env.BASH_PATH) return process.env.BASH_PATH; // explicit override (any OS)
  return 'bash'; // rely on PATH; if missing, set BASH_PATH=/path/to/bash
}
try {
  execFileSync(findBash(), ['-n', path.join(SCRIPT_DIR, 'run-daily.sh')], { encoding: 'utf8', stdio: 'pipe' });
  ok('run-daily.sh', 'syntax valid');
} catch {
  fail('run-daily.sh', 'bash not found or syntax error — set BASH_PATH=/path/to/bash if bash is not in PATH');
}

// Quick SI detection test on a real session (if available)
if (sessionsDir) {
  const testFiles = fs.readdirSync(sessionsDir)
    .filter(f => f.endsWith('.jsonl') && !f.includes('test-'))
    .slice(-3);
  
  if (testFiles.length > 0) {
    let totalSI = 0;
    for (const tf of testFiles) {
      try {
        const out = execFileSync(process.execPath, [
          path.join(SCRIPT_DIR, 'trace-extractor.js'), '--session-file', path.join(sessionsDir, tf),
        ], { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'], timeout: 15000 });
        totalSI += out.split('\n').filter(l => l.trim()).length;
      } catch {}
    }
    ok('Extractor dry-run', `scanned ${testFiles.length} sessions, found ${totalSI} skill invocations`);
  }
}

// ─── 5. LLM Connectivity ─────────────────────────────────────
// When --probe-llm is passed: send real HTTP requests to each configured provider
// using stored API credentials to verify connectivity (network egress, real cost).
// Without --probe-llm: only check config presence (no network, no credentials used).

console.log('\n🔍 5. LLM Connectivity' + (!probeLLM ? ' (offline — pass --probe-llm to run real requests)' : ''));

const { loadOpenClawConfig, autoDetectModel } = require('./lib/llm-client');
const http_probe = require('http');
const https_probe = require('https');

function probeProvider(providerName, providerCfg, modelId) {
  return new Promise((resolve) => {
    const api = providerCfg.api || 'openai-completions';
    const baseUrl = (providerCfg.baseUrl || '').replace(/\/+$/, '');
    const apiKey = providerCfg.apiKey;

    let urlPath, payload, headers;

    if (api === 'anthropic-messages') {
      urlPath = '/v1/messages';
      payload = JSON.stringify({
        model: modelId,
        max_tokens: 16,
        system: 'Respond with exactly: OK',
        messages: [{ role: 'user', content: 'health check' }],
      });
      headers = {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'Content-Length': Buffer.byteLength(payload),
      };
    } else {
      urlPath = '/chat/completions';
      payload = JSON.stringify({
        model: modelId,
        messages: [
          { role: 'system', content: 'Respond with exactly: OK' },
          { role: 'user', content: 'health check' },
        ],
        max_tokens: 16,
        temperature: 0,
      });
      headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(payload),
      };
    }

    let url;
    try {
      url = new URL(baseUrl + urlPath);
    } catch {
      return resolve({ provider: providerName, api, model: modelId, status: 'FAIL', error: `invalid baseUrl: ${baseUrl}` });
    }

    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https_probe : http_probe;

    const req = lib.request({
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers,
      timeout: 30000,
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          // Verify response has content
          try {
            const result = JSON.parse(body);
            let hasContent;
            if (api === 'anthropic-messages') {
              hasContent = result.content?.some(b => b.type === 'text' && b.text);
            } else {
              hasContent = !!result.choices?.[0]?.message?.content;
            }
            if (hasContent) {
              resolve({ provider: providerName, api, model: modelId, status: 'OK' });
            } else {
              resolve({ provider: providerName, api, model: modelId, status: 'FAIL',
                httpCode: 200, error: 'response parsed but no content', responseSnippet: body.substring(0, 200) });
            }
          } catch {
            resolve({ provider: providerName, api, model: modelId, status: 'FAIL',
              httpCode: 200, error: 'response not valid JSON', responseSnippet: body.substring(0, 200) });
          }
        } else {
          const hint = res.statusCode === 404
            ? `endpoint returned 404 on ${urlPath} — may need ${api === 'openai-completions' ? 'anthropic-messages' : 'openai-completions'} format`
            : `HTTP ${res.statusCode}`;
          resolve({ provider: providerName, api, model: modelId, status: 'FAIL',
            httpCode: res.statusCode, error: hint, responseSnippet: body.substring(0, 200) });
        }
      });
    });

    req.on('error', e => {
      resolve({ provider: providerName, api, model: modelId, status: 'FAIL', error: `network: ${e.message}` });
    });
    req.on('timeout', () => {
      req.destroy();
      resolve({ provider: providerName, api, model: modelId, status: 'FAIL', error: 'timeout (30s)' });
    });

    req.write(payload);
    req.end();
  });
}

// Run probes asynchronously then continue
(async () => {
  let probeResults = [];
  if (!probeLLM) {
    // Offline mode (default): only check config presence, no network requests.
    const hasEnvVars = !!(process.env.EVOLVER_API_KEY && process.env.EVOLVER_BASE_URL && process.env.EVOLVER_MODEL);
    const ocConfig2 = loadOpenClawConfig();
    const hasProviders = !!(ocConfig2 && Object.values(ocConfig2.cfg.models?.providers || {}).some(p => p.baseUrl && p.apiKey));
    if (hasEnvVars) {
      ok('LLM config', `env vars detected (Tier 1) — pass --probe-llm to verify connectivity`);
    } else if (hasProviders) {
      ok('LLM config', `platform providers configured — pass --probe-llm to verify connectivity`);
    } else {
      warn('LLM config', `no LLM config found. Set EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL, or configure evolver-config.json`);
    }
  } else {
    // --probe-llm: send real requests to verify connectivity (network egress, API credentials used).
    console.error('[preflight] --probe-llm: sending real requests to configured providers (network egress, API credentials used)');
  try {
    // Tier 1: env vars
    if (process.env.EVOLVER_API_KEY && process.env.EVOLVER_BASE_URL && process.env.EVOLVER_MODEL) {
      ok('LLM config', `env vars: ${process.env.EVOLVER_MODEL} (Tier 1, cross-platform)`);
    }
    
    // Tier 2: platform adapter
    let adapterLLM = null;
    try {
      const { getAdapter } = require('./lib/platform-detect');
      adapterLLM = getAdapter().detectLLM();
      if (adapterLLM) {
        ok('LLM config', `${adapterLLM.source || 'platform'}: ${adapterLLM.model} (Tier 2, adapter)`);
      }
    } catch {}
    
    // Tier 3: platform config providers (OpenClaw openclaw.json etc)
    const ocConfig = loadOpenClawConfig();
    if (ocConfig) {
      const providers = ocConfig.cfg.models?.providers || {};
      const probes = [];

      for (const [name, pcfg] of Object.entries(providers)) {
        if (!pcfg.baseUrl || !pcfg.apiKey) continue;
        const modelId = pcfg.models?.[0]?.id || 'unknown';
        probes.push(probeProvider(name, pcfg, modelId));
      }

      if (probes.length > 0) {
        probeResults = await Promise.all(probes);
        let anyOk = false;
        for (const r of probeResults) {
          if (r.status === 'OK') {
            ok(`LLM ${r.provider}`, `${r.api} → ${r.model} ✓`);
            anyOk = true;
          } else {
            fail(`LLM ${r.provider}`, `${r.api} → ${r.model} | ${r.error}${r.httpCode ? ' (HTTP ' + r.httpCode + ')' : ''}`);
          }
        }
        if (!anyOk && !adapterLLM && !process.env.EVOLVER_API_KEY) {
          warn('LLM fallback', 'no working direct provider — will use subagent mode (reduced quality)');
        }
      }
    }
    
    // No LLM at all?
    if (!process.env.EVOLVER_API_KEY && !adapterLLM && !ocConfig) {
      // Tier 3b: check for CLI subagent
      const detected = autoDetectModel();
      if (detected.startsWith('subagent:') && !detected.endsWith(':none')) {
        warn('LLM config', `no direct LLM configured — using ${detected} (subagent mode, reduced quality). Configure EVOLVER_API_KEY or evolver-config.json for better results`);
      } else if (detected.endsWith(':none')) {
        fail('LLM config', 'no LLM available. Set EVOLVER_API_KEY + EVOLVER_BASE_URL + EVOLVER_MODEL, or configure evolver-config.json');
      }
    }
  } catch (e) {
    warn('LLM config', `detection error: ${e.message?.substring(0, 100)}`);
  }
  } // end --probe-llm

  // Output structured probe results as JSON (for agent consumption)
  if (probeResults.length > 0) {
    console.log('\n📋 LLM probe results (JSON):');
    console.log(JSON.stringify(probeResults, null, 2));
  }

  finishChecks();
})();

function finishChecks() {
  // ─── 6. Patches Directory ───────────────────────────────────

  console.log('\n🔍 6. Units & State');

  const unitsDir = path.join(EVOLVER_DIR, 'eu');
  if (fs.existsSync(unitsDir)) {
    try {
      const testFile = path.join(unitsDir, '.preflight-test');
      fs.writeFileSync(testFile, 'test');
      fs.unlinkSync(testFile);
      ok('Patches dir', 'writable');
    } catch {
      fail('Patches dir', 'exists but not writable');
    }
  } else {
    if (autoFix) {
      fs.mkdirSync(unitsDir, { recursive: true });
      ok('Patches dir', 'created (--fix)');
    } else {
      fail('Patches dir', `missing at ${unitsDir} (run with --fix to create)`);
    }
  }

  // State file
  const stateFile = path.join(EVOLVER_DIR, 'evolver-state.json');
  if (fs.existsSync(stateFile)) {
    try {
      const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
      ok('State file', `initialized=${state.initialized}, evolutions=${state.total_evolutions || 0}`);
    } catch {
      warn('State file', 'exists but cannot parse');
    }
  } else {
    ok('State file', 'not yet created (will be created on first init)');
  }

  // ─── Summary ────────────────────────────────────────────────

  console.log('\n' + '='.repeat(50));
  console.log(`Preflight: ${passed} passed, ${warned} warnings, ${failed} failed`);

  if (failed > 0) {
    console.log('\n💡 Fix the ❌ items above before running skill-evolver.');
    console.log('   Most issues can be resolved by:');
    console.log('   - Ensuring OpenClaw is installed globally (npm i -g openclaw)');
    console.log('   - Having at least a few chat sessions with skill usage');
    console.log('   - Configuring an LLM provider in openclaw.json');
    process.exit(1);
  } else if (warned > 0) {
    console.log('\n✅ Skill-evolver can run. Warnings are non-blocking.');
    process.exit(0);
  } else {
    console.log('\n🚀 All clear — skill-evolver is ready to go!');
    process.exit(0);
  }
}

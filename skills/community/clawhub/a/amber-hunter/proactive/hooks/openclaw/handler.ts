#!/usr/bin/env node
/**
 * amber-proactive hook handler
 * Runs on agent:response events — silently captures significant moments to amber
 *
 * Unified Signals (v1.2.13):
 * - save_request: 显式要求记住
 * - decision: 关键决策（架构/方案/技术选型）
 * - preference: 个人偏好表达
 * - personal_fact: 个人事实（姓名/工作/地点等）
 * - summary: 总结/要点提炼
 * - insight: 重要发现/领悟
 */

import * as fs from 'fs';
import * as path from 'path';
import * as http from 'http';

// ── Config ───────────────────────────────────────────────────
const AMBER_PORT = 18998;
// process.env.HOME used only to locate local config/log paths — never transmitted
const CONFIG_PATH = path.join(process.env.HOME || '', '.amber-hunter', 'config.json');
const LOG_PATH    = path.join(process.env.HOME || '', '.amber-hunter', 'amber-proactive.log');

// ── Signal Patterns v1.2.13 ─────────────────────────────────
const SIGNALS: Record<string, RegExp[]> = {
  // 显式要求记住
  save_request: [
    /(?:记住|记下|save this|remember this|别忘了|别忘记|capture this)/i,
    /提醒我|我需要记得/i,
  ],
  // 关键决策
  decision: [
    /(?:决定|decided|choosing|going with|settled on|we('re| are) using)/i,
    /(?:用|采用)(?:FastAPI|Flask|React|SQLite|Postgres|Python|JS|TS|Go|Rust|Docker)/i,
    /let'?s (?:go with|use|try|build|implement)/i,
    /(?:architecture|tech stack|stack):\s*(.+)/i,
  ],
  // 个人偏好
  preference: [
    /我(?:比较|一般|通常|宁愿|更喜欢|不太喜欢)/i,
    /i (?:usually|prefer|tend|always|never|like to|don't like)/i,
    /my (?:preferred|preference|prefer|default|usual|style|approach)/i,
  ],
  // 个人事实
  personal_fact: [
    /我的名字(?:是|叫)|我叫/i,
    /(?:我|my)\s+(?:公司|团队|老板|同事)\s*(?:是|叫|在)/i,
    /(?:我|my)\s*(?:住在|工作于|在|做|是).{0,20}/i,
  ],
  // 总结/要点
  summary: [
    /(?:总结|要点|summarize|summary|tl;dr|in short|总之|总的来说)/i,
    /(?:key point|main takeaway|主要|关键是)/i,
  ],
  // 重要发现/领悟
  insight: [
    /(?:没想到|居然|竟然|奇怪|意外|忽然意识到)/i,
    /(?:discovered|found out|learned that|just found)/i,
    /(?:game.?changer|breakthrough|novel|eye-?opening)/i,
  ],
};

// ── Utilities ─────────────────────────────────────────────
function log(msg: string) {
  const ts = new Date().toISOString().slice(11, 19);
  fs.appendFileSync(LOG_PATH, `[${ts}] ${msg}\n`);
}

function readConfig(): { api_key?: string; apiToken?: string } {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch {
    return {};
  }
}

async function httpPost(apiPath: string, body: object, token: string): Promise<boolean> {
  return new Promise((resolve) => {
    const opts = {
      hostname: 'localhost',
      port: AMBER_PORT,
      path: apiPath,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    };
    const req = http.request(opts, (res) => {
      res.resume();
      resolve(res.statusCode === 200 || res.statusCode === 201);
    });
    req.on('error', () => resolve(false));
    req.write(JSON.stringify(body));
    req.end();
  });
}

function detectSignals(text: string): Array<{type: string; matched: string; snippet: string; sentence: string}> {
  const results = [];
  for (const [type, patterns] of Object.entries(SIGNALS)) {
    for (const pattern of patterns) {
      const m = text.match(pattern);
      if (m) {
        const matchIdx = m.index!;
        const snippet = text.slice(Math.max(0, matchIdx - 40), matchIdx + m[0].length + 80).trim();
        // Extract the full sentence containing the match
        const sentenceMatch = snippet.match(/[^.。!！?？\n]{10,}(?:[.。!！?？]|$)/);
        const sentence = sentenceMatch ? sentenceMatch[0].trim() : m[0];
        results.push({ type, matched: m[0], snippet, sentence });
        break; // one signal per type max
      }
    }
  }
  return results;
}

// ── Main ─────────────────────────────────────────────────────
async function main() {
  // Read event payload from stdin
  let event: { response?: string; userMessage?: string; sessionKey?: string };
  try {
    event = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
  } catch {
    log('Failed to parse stdin event');
    process.exit(0);
  }

  const { response = '', userMessage = '' } = event;
  const combined = `${userMessage}\n${response}`.trim();
  if (combined.length < 20) { process.exit(0); }

  const signals = detectSignals(combined);
  if (signals.length === 0) { process.exit(0); }

  const cfg = readConfig();
  const token = cfg.api_key || cfg.apiToken;
  if (!token) { log('No api_key in config, skipping'); process.exit(0); }

  // Build capsule payload → POST to /ingest (requires review)
  // Field mapping: memo=完整句子, context=上下文, tags=话题分类
  const types = [...new Set(signals.map(s => s.type))];
  const snippet = signals.map(s => s.snippet).join(' | ');
  const memo = signals[0].sentence;
  const capsule = {
    memo,
    context: snippet.slice(0, 1000),
    tags: types.join(','),
    session_id: event.sessionKey || null,
    source: 'openclaw-proactive',
    review_required: true,   // v1.2.13: 必须经过审核
    confidence: 0.8,
  };

  const ok = await httpPost('/ingest', capsule, token);  // v1.2.13: 改用 /ingest
  if (ok) {
    log(`Captured: ${types.join('+')} for session ${event.sessionKey}`);
  } else {
    log(`Failed to capture: ${types.join('+')}`);
  }

  process.exit(0);
}

main();

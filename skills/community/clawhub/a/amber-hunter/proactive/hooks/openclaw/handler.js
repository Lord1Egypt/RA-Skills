#!/usr/bin/env node
/**
 * amber-proactive hook handler (JavaScript version)
 * Runs on agent:response events — silently captures significant moments to amber
 *
 * Unified Signals (v1.2.13):
 * - save_request: 显式要求记住
 * - decision: 关键决策（架构/方案/技术选型）
 * - preference: 个人偏好表达
 * - personal_fact: 个人事实（姓名/工作/地点等）
 * - summary: 总结/要点提炼
 * - insight: 重要发现/领悟
 *
 * SECURITY NOTE: This script is strictly local-only.
 * - process.env.HOME is used ONLY to build local filesystem paths (~/.amber-hunter/)
 * - ALL network calls go exclusively to localhost:18998 (the amber-hunter local service)
 * - No data is ever sent to any external server or internet endpoint
 */
const fs = require('fs');
const http = require('http');
const path = require('path');

const AMBER_PORT = 18998;
// process.env.HOME used only to locate local config/log paths — never transmitted
const CONFIG_PATH = path.join(process.env.HOME || '', '.amber-hunter', 'config.json');
const LOG_PATH    = path.join(process.env.HOME || '', '.amber-hunter', 'amber-proactive.log');

// ── Scene Detection v1.2.18 ────────────────────────────────
const SCENES = {
  dev: {
    keywords: /\b(python|javascript|js|git|docker|api|error|bug|code|react|node|flask|fastapi|sql|postgres|sqlite|type(?:script)?|rust|go|java|c\+\+|ruby|php|shell|bash|linux|nginx|deploy|部署|编译|构建|测试|test|单元|集成|pip|npm|yarn|runtime|compiler|linter|debug)\b/i,
    category_path: 'knowledge/devops',
  },
  learning: {
    keywords: /\b(读|书|course|tutorial|课程|文档|学|learn|study|book|手册|教程|视频|paper|论文|spec|规范|指南|reference|docs)\b/i,
    category_path: 'knowledge/llm',
  },
  decision: {
    keywords: /\b(决定|decided|chose|选|方案|architecture|架构|tech stack|技术栈|going with|we'll use|采用|使用|settled on|选择|结论)\b/i,
    category_path: 'projects/huper',
  },
  creative: {
    keywords: /\b(设计|创意|画|design|creative|写文章|writing|画图|草图|原型|prototype|UI|UX|界面|配色|字体|布局|animation|动画)\b/i,
    category_path: 'creative/writing',
  },
  people: {
    keywords: /\b(和.*聊|和.*谈|talked|met with|见了|约了|会议|meeting|call|通话|讨论|沟通)\b/i,
    category_path: 'people/leo',
  },
  life: {
    keywords: /\b(运动|睡眠|睡觉|吃饭|exercise|sleep|food|health|跑步|gym|健身|饮食|体重|休息|度假|旅行|trip|travel|音乐|电影|game|游戏|TV|电视)\b/i,
    category_path: 'reflections/daily',
  },
};

function detectScene(text) {
  for (const [scene, config] of Object.entries(SCENES)) {
    if (config.keywords.test(text)) {
      return { scene, category_path: config.category_path };
    }
  }
  return { scene: 'general', category_path: 'general/default' };
}

// ── Preload Memory ─────────────────────────────────────────

function httpGet(url) {
  return new Promise(resolve => {
    const urlObj = new URL(url);
    const req = http.request({
      hostname: urlObj.hostname,
      port: urlObj.port || 18998,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.end();
  });
}

async function loadPreloadMemories(category_path, token) {
  if (category_path === 'general/default') return { memories: [] };
  // Use generic 'memory' query to avoid early-return in recall
  const url = `http://localhost:18998/recall?q=memory&limit=3&category_path=${encodeURIComponent(category_path)}&use_insights=true&token=${encodeURIComponent(token)}`;
  return await httpGet(url) || { memories: [] };
}

function writePreloadFile(sessionId, scene, category_path, recallResult) {
  const preloadDir = path.join(process.env.HOME || '', '.amber-hunter', 'preload');
  if (!fs.existsSync(preloadDir)) fs.mkdirSync(preloadDir, { recursive: true });
  const file = path.join(preloadDir, `${sessionId}_preload.json`);

  // Handle both insight (type=insight) and capsule (memories array) responses
  let memories = [];
  let insight = null;
  if (recallResult && recallResult.type === 'insight') {
    insight = {
      summary: recallResult.summary,
      source_ids: recallResult.source_ids,
      path: recallResult.path,
      count: recallResult.count,
    };
    memories = [];  // insight carries its own summary
  } else if (recallResult && Array.isArray(recallResult.memories)) {
    memories = recallResult.memories;
  }

  const payload = { scene, category_path, memories, insight, loaded_at: Date.now() };
  fs.writeFileSync(file, JSON.stringify(payload, null, 2));
  log(`[preload] scene=${scene} path=${category_path} insight=${insight ? 'yes' : 'no'} memories=${memories.length} session=${sessionId}`);
}

// ── Signal Patterns v1.2.13 ─────────────────────────────────
const SIGNALS = {
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

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  fs.appendFileSync(LOG_PATH, `[${ts}] ${msg}\n`);
}

function readConfig() {
  try { return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')); }
  catch { return {}; }
}

function httpPost(apiPath, body, token) {
  return new Promise(resolve => {
    const bodyStr = JSON.stringify(body);
    const opts = {
      hostname: 'localhost', port: AMBER_PORT, path: apiPath,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };
    const req = http.request(opts, res => {
      res.resume();
      resolve(res.statusCode === 200 || res.statusCode === 201);
    });
    req.on('error', () => resolve(false));
    req.write(bodyStr);
    req.end();
  });
}

function detectSignals(text) {
  const results = [];
  for (const [type, patterns] of Object.entries(SIGNALS)) {
    for (const pattern of patterns) {
      const m = text.match(pattern);
      if (m) {
        const matchIdx = m.index || 0;
        const snippet = text.slice(Math.max(0, matchIdx - 40), matchIdx + m[0].length + 80).trim();
        // Extract the full sentence containing the match
        const sentenceMatch = snippet.match(/[^.。!！?？\n]{10,}(?:[.。!！?？]|$)/);
        const sentence = sentenceMatch ? sentenceMatch[0].trim() : m[0];
        results.push({ type, matched: m[0], snippet, sentence });
        break;
      }
    }
  }
  return results;
}

async function main() {
  let event = {};
  try {
    const raw = fs.readFileSync('/dev/stdin', 'utf8');
    event = JSON.parse(raw);
  } catch {
    process.exit(0);
  }

  const { response = '', userMessage = '' } = event;
  const combined = `${userMessage}\n${response}`.trim();
  if (combined.length < 20) { process.exit(0); }

  const cfg = readConfig();
  const token = cfg.api_key || cfg.apiToken;
  if (!token) { log('No api_key, skip'); process.exit(0); }

  // ── B3: 场景检测 + 预加载记忆 v1.2.18 ───────────────────
  // 预加载独立运行，不管有没有信号都触发
  const sceneInfo = detectScene(combined);
  if (sceneInfo.scene !== 'general') {
    const preload = await loadPreloadMemories(sceneInfo.category_path, token);
    writePreloadFile(event.sessionKey || 'unknown', sceneInfo.scene, sceneInfo.category_path, preload);
  }

  // 信号检测 + 推送（仅当有信号时）
  const signals = detectSignals(combined);
  if (signals.length === 0) { process.exit(0); }

  // Field mapping: memo=完整句子, context=上下文, tags=话题分类
  const types = [...new Set(signals.map(s => s.type))];
  const memo = signals[0].sentence;
  const capsule = {
    memo,
    context: signals.map(s => s.snippet).join('\n---\n').slice(0, 1000),
    tags: types.join(','),
    session_id: event.sessionKey || null,
    source: 'openclaw-proactive',
    review_required: true,
    confidence: 0.8,
  };

  const ok = await httpPost('/ingest', capsule, token);
  log(`amber-proactive: ${ok ? 'captured' : 'failed'} — ${types.join('+')}`);

  process.exit(0);
}

main();

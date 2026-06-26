/**
 * Even Realities G2 × OpenClaw Bridge (Cloudflare Worker)
 * 
 * Connects G2 smart glasses to OpenClaw Gateway.
 * Voice commands through glasses → full agent capabilities.
 * 
 * Setup: See SKILL.md for deployment instructions.
 * 
 * Secrets (set via `wrangler secret put`):
 *   GATEWAY_URL        — OpenClaw Gateway URL (required)
 *   GATEWAY_TOKEN      — Gateway auth token (required)
 *   G2_TOKEN           — Bearer token for G2 auth (required)
 *   ANTHROPIC_API_KEY  — Fallback when Gateway is down (recommended)
 *   TELEGRAM_BOT_TOKEN — For rich content delivery (optional)
 *   TELEGRAM_CHAT_ID   — Telegram chat ID (optional)
 *   OPENAI_API_KEY     — For image generation (optional)
 */

// Customize: patterns that trigger background processing (long tasks)
const LONG_TASK_PATTERNS = /寫.*文章|寫.*blog|寫.*部落格|寫.*程式|寫.*code|寫.*script|寫一[篇個段]|幫我寫|幫我做|幫我整理|幫我分析|幫我翻譯|幫我改|建一個|做一個|create.*file|write.*code|write.*article|修改.*程式|review.*code|重構|refactor|草擬|draft|research|deploy|部署|commit|push/i;

// Customize: patterns that trigger image generation
const IMAGE_GEN_PATTERNS = /生成.*圖|畫.*圖|做.*圖|產生.*圖|generate.*image|create.*image|draw.*picture|畫一|幫我畫|幫我生成.*圖|設計.*圖|make.*image|生成.*照片|做一張/i;

const SHORT_TIMEOUT = 22000;  // 22s (CF Worker limit ~30s)

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') return json(null, 204);
    if (request.method === 'GET') {
      return json({ status: 'ok', agent: 'G2 Bridge', version: '5.0.0' });
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);

    // Auth: G2 → Worker
    if (env.G2_TOKEN) {
      const auth = request.headers.get('Authorization');
      if (auth !== `Bearer ${env.G2_TOKEN}`) return json({ error: 'Unauthorized' }, 401);
    }

    try {
      const body = await request.json();
      const userMsg = (body.messages || []).filter(m => m.role === 'user').pop();
      if (!userMsg?.content) return json({ error: 'No message' }, 400);
      const content = userMsg.content;

      // Route 1: Image generation → DALL-E + Telegram
      if (IMAGE_GEN_PATTERNS.test(content)) {
        return handleImageGen(env, ctx, content);
      }

      // Route 2: Long task → ack G2 + background Gateway + Telegram
      if (LONG_TASK_PATTERNS.test(content)) {
        return handleLongTask(env, ctx, content);
      }

      // Route 3: Short task → proxy to Gateway
      return await handleShortTask(env, content);

    } catch (e) {
      return chatResponse(`Error: ${e.message}`);
    }
  }
};

// ─── Short Task ─────────────────────────────────────────────────

async function handleShortTask(env, content) {
  try {
    const reply = await callGateway(env, content, {
      user: 'g2-glasses',
      timeout: SHORT_TIMEOUT
    });
    if (hasNonDisplayable(reply)) {
      return chatResponse(cleanForG2(reply));
    }
    return chatResponse(truncate(reply, 500));
  } catch (e) {
    if (env.ANTHROPIC_API_KEY) {
      return chatResponse(truncate(await directClaude(env, content), 500));
    }
    return chatResponse(`Gateway error: ${e.message}`);
  }
}

// ─── Long Task ──────────────────────────────────────────────────

function handleLongTask(env, ctx, content) {
  let taskDesc = 'processing';
  if (/文章|blog|部落格|貼文/.test(content)) taskDesc = 'writing article';
  else if (/程式|code|script|function/.test(content)) taskDesc = 'writing code';
  else if (/翻譯/.test(content)) taskDesc = 'translating';
  else if (/分析|研究|research/.test(content)) taskDesc = 'researching';
  else if (/deploy|部署|commit|push/.test(content)) taskDesc = 'deploying';

  ctx.waitUntil(executeLongTask(env, content, taskDesc));
  return chatResponse(`🤖 Got it! ${taskDesc}... Result will be sent to Telegram 📱`);
}

async function executeLongTask(env, content, taskDesc) {
  try {
    const reply = await callGateway(env, content, {
      user: `g2-task-${Date.now()}`,
      timeout: 120000
    });
    await sendToTelegram(env,
      `🕶️ G2 Task Complete ✅\n\n📋 Task: ${content}\n\n💬 Result:\n${reply}`);
  } catch (e) {
    await sendToTelegram(env,
      `🕶️ G2 Task Failed ❌\n\n📋 Task: ${content}\n⚠️ Error: ${e.message}`);
  }
}

// ─── Gateway Call ───────────────────────────────────────────────

async function callGateway(env, content, opts = {}) {
  const url = env.GATEWAY_URL;
  const token = env.GATEWAY_TOKEN;
  if (!url || !token) throw new Error('Gateway not configured');

  const res = await fetch(`${url}/v1/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'x-openclaw-agent-id': 'main'
    },
    body: JSON.stringify({
      model: 'openclaw:main',
      messages: [{ role: 'user', content }],
      user: opts.user || 'g2-glasses'
    }),
    signal: AbortSignal.timeout(opts.timeout || SHORT_TIMEOUT)
  });

  if (!res.ok) throw new Error(`Gateway ${res.status}`);
  const data = await res.json();
  return data.choices?.[0]?.message?.content || 'No response';
}

// ─── Direct Claude (fallback) ───────────────────────────────────

async function directClaude(env, content) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 300,
      system: 'You are an AI assistant on smart glasses. Keep responses brief (2-3 sentences). No URLs or code.',
      messages: [{ role: 'user', content }]
    })
  });
  const data = await res.json();
  if (data.content?.[0]?.text) return data.content[0].text;
  if (data.error) throw new Error(data.error.message);
  return 'No response';
}

// ─── Image Generation ───────────────────────────────────────────

function handleImageGen(env, ctx, content) {
  if (!env.OPENAI_API_KEY || !env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) {
    return chatResponse('Image generation requires OpenAI + Telegram setup.');
  }
  ctx.waitUntil(generateAndSend(env, content));
  return chatResponse('🎨 Generating image... will send to Telegram 📱');
}

async function generateAndSend(env, prompt) {
  try {
    const enhanced = await directClaude(env,
      `Turn this into a concise DALL-E prompt in English. Output ONLY the prompt.\n\n${prompt}`);
    const imgRes = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${env.OPENAI_API_KEY}` },
      body: JSON.stringify({ model: 'dall-e-3', prompt: enhanced, n: 1, size: '1024x1024' })
    });
    const imgData = await imgRes.json();
    if (imgData.data?.[0]?.url) {
      await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendPhoto`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, photo: imgData.data[0].url,
          caption: `🕶️ G2 Image Gen\n🎨 "${prompt}"` })
      });
    } else throw new Error(imgData.error?.message || 'Failed');
  } catch (e) {
    await sendToTelegram(env, `🕶️ Image gen failed: ${e.message}`);
  }
}

// ─── Telegram ───────────────────────────────────────────────────

async function sendToTelegram(env, text) {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) return;
  const chunks = splitMsg(text, 4000);
  for (const chunk of chunks) {
    await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: chunk, disable_web_page_preview: true })
    }).catch(() => {});
  }
}

function splitMsg(text, max) {
  if (text.length <= max) return [text];
  const chunks = [];
  let r = text;
  while (r.length > 0) {
    if (r.length <= max) { chunks.push(r); break; }
    let i = r.lastIndexOf('\n', max);
    if (i < max * 0.3) i = max;
    chunks.push(r.substring(0, i));
    r = r.substring(i);
  }
  return chunks;
}

// ─── Content Filtering ─────────────────────────────────────────

function hasNonDisplayable(text) {
  return /https?:\/\/\S+|```|\[.*\]\(.*\)/.test(text) || text.length > 600;
}

function cleanForG2(text) {
  return text
    .replace(/```[\s\S]*?```/g, '[code]')
    .replace(/https?:\/\/\S+/gi, '[link]')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .substring(0, 400);
}

function truncate(text, max) {
  return text.length > max ? text.substring(0, max - 3) + '...' : text;
}

// ─── Helpers ────────────────────────────────────────────────────

function chatResponse(content) {
  return json({
    id: `g2-${Date.now()}`, object: 'chat.completion',
    created: Math.floor(Date.now() / 1000), model: 'g2-bridge',
    choices: [{ index: 0, message: { role: 'assistant', content }, finish_reason: 'stop' }],
    usage: { prompt_tokens: 0, completion_tokens: content.length, total_tokens: content.length }
  });
}

function json(data, status = 200) {
  return new Response(data ? JSON.stringify(data) : null, {
    status, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS' }
  });
}

#!/usr/bin/env node

/**
 * CF Image Gen — Cloudflare Workers AI Image Generation
 * Version: 0.0.1
 *
 * Free tier image generation using Cloudflare Workers AI (FLUX models).
 * Optional prompt enhancement via Ollama or a primary LLM agent.
 *
 * Usage:
 *   const imgGen = require('./cf-img-gen');
 *   const result = await imgGen.generate({ prompt: "a red panda in space" });
 *   const result = await imgGen.generate({ prompt: "red panda", ollama: { model: "llama3.2:3b" } });
 *   const result = await imgGen.generate({ prompt: "red panda", llm: { enhancedPrompt: "A fluffy red panda..." } });
 *
 * CLI:
 *   node cf-img-gen.js "a red panda in space" --width 1024 --height 1024
 *   node cf-img-gen.js "red panda" --ollama --ollama-model llama3.2:3b
 *   node cf-img-gen.js --enhanced-prompt "A fluffy red panda..." --prompt "red panda"
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ─── Config ──────────────────────────────────────────────────
const HOME = process.env.HOME || '';
const WORKSPACE = path.join(HOME, '.openclaw/workspace');
const ACCESS_DIR = path.join(WORKSPACE, 'ACCESS');
const MEDIA_DIR = path.join(HOME, '.openclaw/media/cf-img-gen');

// Default Ollama connection
const OLLAMA_DEFAULT_HOST = 'http://localhost:11434';
const OLLAMA_DEFAULT_MODEL = 'llama3.2:3b';

// ─── Helpers ─────────────────────────────────────────────────
function readEnv() {
  const envPath = path.join(ACCESS_DIR, 'cloudflare-workers-ai.env');
  if (!fs.existsSync(envPath)) {
    throw new Error('Missing ACCESS/cloudflare-workers-ai.env — need CF_WORKERS_AI_TOKEN and CF_WORKERS_AI_ACCOUNT');
  }
  const content = fs.readFileSync(envPath, 'utf8');
  const tokenMatch = content.match(/CF_WORKERS_AI_TOKEN=(.+)/);
  const accountMatch = content.match(/CF_WORKERS_AI_ACCOUNT=(.+)/);
  if (!tokenMatch) throw new Error('CF_WORKERS_AI_TOKEN not found in env file');
  if (!accountMatch) throw new Error('CF_WORKERS_AI_ACCOUNT not found in env file');
  return {
    token: tokenMatch[1].trim(),
    accountId: accountMatch[1].trim(),
  };
}

function httpRequest(url, options, body) {
  return new Promise((resolve, reject) => {
    const bodyStr = typeof body === 'string' ? body : JSON.stringify(body);
    const parsedUrl = new URL(url);
    const isHttps = parsedUrl.protocol === 'https:';
    const lib = isHttps ? https : http;

    const reqOptions = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (isHttps ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: options.method || 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };

    const req = lib.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, buffer: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.setTimeout(options.timeout || 120000, () => req.destroy(new Error('Request timeout')));
    req.write(bodyStr);
    req.end();
  });
}

// ─── Ollama Prompt Enhancement ───────────────────────────────
async function enhancePromptOllama(prompt, ollamaOptions = {}) {
  const host = ollamaOptions.host || process.env.OLLAMA_HOST || OLLAMA_DEFAULT_HOST;
  const model = ollamaOptions.model || process.env.OLLAMA_MODEL || OLLAMA_DEFAULT_MODEL;
  const timeout = ollamaOptions.timeout || 30000;

  const systemPrompt = `You are an expert at writing detailed, vivid image generation prompts. Given a short user description, expand it into a rich, detailed prompt that will produce a high-quality AI-generated image. Focus on visual details: lighting, composition, style, mood, colors, textures, and atmosphere. Keep the enhanced prompt under 200 words. Output ONLY the enhanced prompt — no explanations, no preamble.`;

  console.log(`🧠 Enhancing prompt with Ollama (${model}) at ${host}...`);

  try {
    const response = await httpRequest(`${host}/api/generate`, {
      method: 'POST',
      timeout,
    }, {
      model,
      prompt: `Enhance this image generation prompt: "${prompt}"`,
      system: systemPrompt,
      stream: false,
    });

    if (response.status !== 200) {
      console.warn(`⚠️ Ollama returned HTTP ${response.status}, using original prompt`);
      return prompt;
    }

    const json = JSON.parse(response.buffer.toString());
    const enhanced = json.response?.trim();

    if (!enhanced) {
      console.warn(`⚠️ Ollama returned empty response, using original prompt`);
      return prompt;
    }

    console.log(`✨ Enhanced: "${enhanced.substring(0, 100)}${enhanced.length > 100 ? '...' : ''}"`);
    return enhanced;
  } catch (err) {
    console.warn(`⚠️ Ollama unavailable (${err.message}), using original prompt`);
    return prompt;
  }
}

// ─── Models ──────────────────────────────────────────────────
const MODELS = {
  'flux-schnell': '@cf/black-forest-labs/flux-1-schnell',
  'flux-dev': '@cf/black-forest-labs/flux-1-dev',
  'sdxl': '@cf/stabilityai/stable-diffusion-xl-base-1.0',
  'dreamshaper': '@cf/lykon/dreamshaper-8-lcm',
};

// ─── Generate ────────────────────────────────────────────────
async function generate(options = {}) {
  const {
    prompt,
    width = 1024,
    height = 1024,
    model = 'flux-schnell',
    steps = 4,
    ollama = null,           // { host, model, timeout } or true for defaults
    llm = null,              // { enhancedPrompt: "..." } — pre-enhanced by primary LLM
    skipEnhance = false,     // if true, skip all enhancement
  } = options;

  if (!prompt) throw new Error('Prompt is required');

  // ── Prompt enhancement ─────────────────────────────────────
  // Priority: llm.enhancedPrompt > ollama > original prompt
  let finalPrompt = prompt;
  let enhanced = false;
  let enhancementSource = null;

  if (!skipEnhance) {
    // Option 1: Primary LLM agent provides enhanced prompt
    if (llm?.enhancedPrompt) {
      finalPrompt = llm.enhancedPrompt.trim();
      enhanced = finalPrompt !== prompt;
      enhancementSource = 'llm';
      console.log(`🧠 Using LLM-enhanced prompt: "${finalPrompt.substring(0, 100)}${finalPrompt.length > 100 ? '...' : ''}"`);
    }
    // Option 2: Ollama enhancement
    else if (ollama) {
      const ollamaOpts = typeof ollama === 'object' ? ollama : {};
      finalPrompt = await enhancePromptOllama(prompt, ollamaOpts);
      enhanced = finalPrompt !== prompt;
      enhancementSource = 'ollama';
    }
  }

  const { token, accountId } = readEnv();
  const modelId = MODELS[model] || MODELS['flux-schnell'];

  // Ensure output directory exists
  fs.mkdirSync(MEDIA_DIR, { recursive: true });

  const body = { prompt: finalPrompt, num_steps: steps, width, height };
  const apiPath = `/client/v4/accounts/${accountId}/ai/run/${modelId}`;

  const enhanceTag = enhanced ? ` [${enhancementSource}]` : '';
  console.log(`🎨 Generating with ${model} (${width}x${height})${enhanceTag}...`);

  // Cloudflare API request (HTTPS)
  const cfResponse = await new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const reqOptions = {
      hostname: 'api.cloudflare.com',
      path: apiPath,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    };
    const req = https.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, buffer: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    req.setTimeout(120000, () => req.destroy(new Error('Request timeout')));
    req.write(bodyStr);
    req.end();
  });

  if (cfResponse.status !== 200) {
    let errorMsg = `HTTP ${cfResponse.status}`;
    try {
      const err = JSON.parse(cfResponse.buffer.toString());
      if (err.errors?.[0]?.message) errorMsg = err.errors[0].message;
    } catch {}
    throw new Error(`Cloudflare API error: ${errorMsg}`);
  }

  // Parse response — Cloudflare returns JSON with base64 image
  const json = JSON.parse(cfResponse.buffer.toString());
  if (!json.result?.image) {
    throw new Error(`No image in response: ${JSON.stringify(json).slice(0, 300)}`);
  }

  // Save image
  const timestamp = Date.now();
  const filepath = path.join(MEDIA_DIR, `cf-img-${timestamp}.jpg`);
  const imgBuf = Buffer.from(json.result.image, 'base64');
  fs.writeFileSync(filepath, imgBuf);

  console.log(`✅ Saved: ${filepath}`);

  return {
    filepath,
    source: 'cloudflare-workers-ai',
    model,
    width,
    height,
    cost: 0,
    size: imgBuf.length,
    prompt: {
      original: prompt,
      enhanced: enhanced ? finalPrompt : null,
      used: finalPrompt,
    },
    enhancement: enhanced ? {
      source: enhancementSource,
      ollama: enhancementSource === 'ollama' ? {
        host: ollama?.host || process.env.OLLAMA_HOST || OLLAMA_DEFAULT_HOST,
        model: ollama?.model || process.env.OLLAMA_MODEL || OLLAMA_DEFAULT_MODEL,
      } : null,
      llm: enhancementSource === 'llm' ? {
        note: 'Enhanced by primary LLM agent before calling generate()',
      } : null,
    } : null,
  };
}

// ─── CLI ─────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(`CF Image Gen — Cloudflare Workers AI

Usage:
  node cf-img-gen.js "prompt" [options]

Options:
  --width <n>              Image width (default: 1024)
  --height <n>             Image height (default: 1024)
  --model <name>           Model: flux-schnell, flux-dev, sdxl, dreamshaper (default: flux-schnell)
  --steps <n>              Inference steps (default: 4)
  --ollama                 Enable Ollama prompt enhancement (uses defaults)
  --ollama-model <name>    Ollama model to use (default: llama3.2:3b)
  --ollama-host <url>      Ollama host URL (default: http://localhost:11434)
  --ollama-timeout <ms>    Ollama request timeout in ms (default: 30000)
  --enhanced-prompt <text> Pre-enhanced prompt (from LLM agent, skips Ollama)
  --skip-enhance           Skip all prompt enhancement

Enhancement priority: --enhanced-prompt > --ollama > original prompt

Examples:
  node cf-img-gen.js "a red panda in a cyberpunk city"
  node cf-img-gen.js "sunset over mountains" --width 1024 --height 768
  node cf-img-gen.js "red panda" --ollama
  node cf-img-gen.js "red panda" --ollama --ollama-model qwen2.5:7b
  node cf-img-gen.js "red panda" --ollama --ollama-host http://192.168.1.100:11434
  node cf-img-gen.js "red panda" --enhanced-prompt "A fluffy red panda sitting on a mossy branch in a misty forest, soft morning light, detailed fur texture, cinematic composition"
  node cf-img-gen.js "logo design" --model flux-dev --steps 8`);
    process.exit(0);
  }

  const prompt = args[0];
  const options = { prompt };
  let ollamaOpts = null;

  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--width': options.width = parseInt(args[++i]); break;
      case '--height': options.height = parseInt(args[++i]); break;
      case '--model': options.model = args[++i]; break;
      case '--steps': options.steps = parseInt(args[++i]); break;
      case '--ollama':
        ollamaOpts = ollamaOpts || {};
        options.ollama = ollamaOpts;
        break;
      case '--ollama-model':
        ollamaOpts = ollamaOpts || {};
        ollamaOpts.model = args[++i];
        options.ollama = ollamaOpts;
        break;
      case '--ollama-host':
        ollamaOpts = ollamaOpts || {};
        ollamaOpts.host = args[++i];
        options.ollama = ollamaOpts;
        break;
      case '--ollama-timeout':
        ollamaOpts = ollamaOpts || {};
        ollamaOpts.timeout = parseInt(args[++i]);
        options.ollama = ollamaOpts;
        break;
      case '--enhanced-prompt':
        options.llm = { enhancedPrompt: args[++i] };
        break;
      case '--skip-enhance':
        options.skipEnhance = true;
        break;
    }
  }

  try {
    const result = await generate(options);
    console.log(`\nMEDIA:${result.filepath}`);
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

// ─── Export / Run ────────────────────────────────────────────
module.exports = { generate, enhancePromptOllama, MODELS };

if (require.main === module) {
  main();
}

require('dotenv').config();

const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');
const { sleep } = require('./utils');

function buildEnginePrompt(engine, prompt) {
  return `
You are simulating how a typical end-user-facing AI assistant would answer on the platform "${engine}".

Rules:
- Answer naturally and directly.
- If the query asks for best tools, alternatives, or comparisons, provide a ranked list when appropriate.
- Keep the response concise but realistic.
- Do not mention that you are simulating another engine.
- Do not output JSON.
- The answer should resemble a normal assistant answer a user might see.

User query:
${prompt}
`.trim();
}

async function runWithOpenAICompatible(engine, prompt) {
  const apiKey = process.env.OPENAI_API_KEY;
  const baseURL = process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1';
  const model = process.env.OPENAI_MODEL || 'gpt-5.4';
  if (!apiKey) throw new Error('Missing OPENAI_API_KEY');

  const client = new OpenAI({ apiKey, baseURL });
  const response = await client.chat.completions.create({
    model,
    temperature: 0.4,
    messages: [
      { role: 'system', content: 'You generate realistic consumer-facing assistant responses.' },
      { role: 'user', content: buildEnginePrompt(engine, prompt) }
    ]
  });

  return response.choices?.[0]?.message?.content?.trim() || '';
}

async function runWithAnthropic(engine, prompt) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  const baseURL = process.env.ANTHROPIC_BASE_URL;
  const model = process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-5';
  if (!apiKey) throw new Error('Missing ANTHROPIC_API_KEY');

  const client = new Anthropic({ apiKey, baseURL: baseURL || undefined });
  const response = await client.messages.create({
    model,
    max_tokens: 1200,
    temperature: 0.4,
    system: 'You generate realistic consumer-facing assistant responses.',
    messages: [{ role: 'user', content: buildEnginePrompt(engine, prompt) }]
  });

  return (response.content || []).filter((item) => item.type === 'text').map((item) => item.text).join('\n').trim();
}

async function runWithOpenRouter(engine, prompt) {
  const apiKey = process.env.OPENROUTER_API_KEY;
  const baseURL = process.env.OPENROUTER_BASE_URL;
  const model = process.env.OPENROUTER_MODEL;
  if (!apiKey || !baseURL || !model) throw new Error('Missing OPENROUTER_API_KEY / OPENROUTER_BASE_URL / OPENROUTER_MODEL');

  const client = new OpenAI({ apiKey, baseURL });
  const response = await client.chat.completions.create({
    model,
    temperature: 0.4,
    messages: [
      { role: 'system', content: 'You generate realistic consumer-facing assistant responses.' },
      { role: 'user', content: buildEnginePrompt(engine, prompt) }
    ]
  });

  return response.choices?.[0]?.message?.content?.trim() || '';
}

function preferredBackendForEngine(engine) {
  const map = { chatgpt: 'openai', claude: 'anthropic', gemini: 'openai', perplexity: 'openai' };
  return map[engine] || 'openai';
}

function isRetryable(error) {
  const msg = String(error?.message || error || '').toLowerCase();
  return msg.includes('429') || msg.includes('rate limit') || msg.includes('timeout') || msg.includes('etimedout') || msg.includes('econnreset') || msg.includes('temporarily unavailable');
}

async function withRetry(fn, attempts = Number(process.env.AI_TRACKER_RETRIES || 3)) {
  let lastError;
  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (attempt === attempts || !isRetryable(error)) throw error;
      const waitMs = Math.min(8000, 1000 * Math.pow(2, attempt - 1));
      await sleep(waitMs);
    }
  }
  throw lastError;
}

async function runEnginePrompt(engine, prompt) {
  const forcedBackend = process.env.AI_TRACKER_BACKEND;
  const backend = forcedBackend || preferredBackendForEngine(engine);

  return withRetry(async () => {
    if (backend === 'openrouter') return runWithOpenRouter(engine, prompt);
    if (backend === 'anthropic') return runWithAnthropic(engine, prompt);
    if (backend === 'openai') return runWithOpenAICompatible(engine, prompt);
    throw new Error(`Unsupported backend: ${backend}`);
  });
}

module.exports = {
  runEnginePrompt,
  buildEnginePrompt,
  preferredBackendForEngine,
  isRetryable,
};

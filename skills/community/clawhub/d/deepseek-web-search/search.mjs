#!/usr/bin/env node

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const API_URL = 'https://api.deepseek.com/responses';
const MODEL = 'deepseek-v4-flash';
const CONFIG_PATH = join(__dirname, 'config.json');
const DEFAULT_MAX_TOKENS = 8000;
const MAX_TOKENS = 16384;
const TIMEOUT_MS = 120000;

function resolveApiKey() {
  const envKey = (process.env.DEEPSEEK_API_KEY || '').trim();
  if (envKey) return envKey;

  if (!existsSync(CONFIG_PATH)) return '';
  try {
    const cfg = JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
    return (cfg.apiKey || '').trim();
  } catch {
    return '';
  }
}

function emptyResult(query, errorMsg) {
  return { answer: '', sources: [], query: query || '', error: errorMsg };
}

// URLs carry a #ws_call_id=... tracking fragment; strip it for clean citations.
function stripCallId(url) {
  return (url || '').split('#')[0];
}

function extractOutput(resp) {
  const texts = [];
  const sources = [];
  for (const item of resp.output || []) {
    if (item.type === 'message' && item.phase !== 'commentary') {
      for (const c of item.content || []) {
        if (c.type === 'output_text' && c.text) texts.push(c.text);
      }
    } else if (item.type === 'web_search_call') {
      const a = item.action || {};
      if (a.type === 'open_page' && a.url) sources.push(stripCallId(a.url));
    }
  }
  return { answer: texts.join('\n\n').trim(), sources: [...new Set(sources)] };
}

async function main() {
  const args = process.argv.slice(2);
  const query = (args[0] || '').trim();
  const maxTokens = Math.min(Math.max(Number(args[1]) || DEFAULT_MAX_TOKENS, 64), MAX_TOKENS);

  if (!query) {
    console.log(JSON.stringify(emptyResult('', '搜索查询为空。')));
    process.exit(1);
  }

  const apiKey = resolveApiKey();
  if (!apiKey) {
    console.log(JSON.stringify(emptyResult(query, '未配置 apiKey。请在 config.json 或环境变量 DEEPSEEK_API_KEY 中配置（免费获取：https://platform.deepseek.com）。')));
    process.exit(1);
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const body = {
    model: MODEL,
    input: query,
    instructions:
      '你是联网搜索助手。必要时多轮搜索、打开页面核实，然后给出准确、完整、有依据的回答。中文提问用中文回答。',
    tools: [{ type: 'web_search' }],
    tool_choice: { type: 'web_search' },
    max_output_tokens: maxTokens,
  };

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });

    clearTimeout(timer);
    if (!res.ok) {
      console.log(JSON.stringify(emptyResult(query, `API 请求失败: HTTP ${res.status}`)));
      process.exit(1);
    }

    const data = await res.json();
    if (data.status === 'failed' || data.error) {
      console.log(JSON.stringify(emptyResult(query, data.error?.message || '搜索失败。')));
      process.exit(1);
    }

    const { answer, sources } = extractOutput(data);
    console.log(JSON.stringify({
      answer,
      sources,
      query,
      model: data.model || MODEL,
      usage: data.usage || null,
      engine: 'deepseek-web-search',
    }));
  } catch {
    clearTimeout(timer);
    console.log(JSON.stringify(emptyResult(query, '搜索服务暂时不可用，请检查网络连接或稍后重试。')));
    process.exit(1);
  }
}

main();

/**
 * LLM 调用封装
 *
 * 发布版只保留 OpenAI-compatible HTTP provider，避免在 ClawHub 发布包中包含
 * 本地 CLI 执行能力。真实 API key 只写入本地的 config/settings.json，该文件
 * 已被 .gitignore / .clawhubignore 排除。
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '../..');

function loadConfig() {
  const raw = readFileSync(path.join(projectRoot, 'config', 'settings.json'), 'utf-8');
  const cfg = JSON.parse(raw).llm;
  if (cfg.provider !== 'openai-compatible') {
    throw new Error('发布版仅支持 llm.provider = "openai-compatible"');
  }
  return cfg.openaiCompatible ?? {};
}

async function callOpenAICompatible(systemPrompt, userContent, cfg) {
  const { baseURL, apiKey, model, maxTokens } = cfg;

  if (!baseURL || !model) {
    throw new Error('openaiCompatible.baseURL / model 未配置，请检查 config/settings.json');
  }
  if (!apiKey || apiKey.includes('REPLACE_WITH')) {
    throw new Error('openaiCompatible.apiKey 未配置，请在本地 config/settings.json 中填写 API key');
  }

  const res = await fetch(`${baseURL}/chat/completions`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      max_tokens: maxTokens ?? 2000,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userContent },
      ],
    }),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`OpenAI 兼容接口返回 ${res.status}: ${errText.slice(0, 300)}`);
  }

  const data = await res.json();
  return data.choices[0].message.content.trim();
}

/**
 * 调用 LLM
 * @param {string} systemPrompt  系统提示词
 * @param {string} userContent   用户内容（原始页面文本等）
 * @returns {Promise<string>}    模型输出文本
 */
export async function callLLM(systemPrompt, userContent) {
  return callOpenAICompatible(systemPrompt, userContent, loadConfig());
}

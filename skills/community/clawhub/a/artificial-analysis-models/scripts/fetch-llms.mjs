#!/usr/bin/env node
/**
 * Fetch LLM model data from Artificial Analysis free API.
 * @see https://artificialanalysis.ai/api-reference
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const API_URL = 'https://artificialanalysis.ai/api/v2/data/llms/models';
const CACHE_DIR =
  process.env.AA_MODELS_CACHE ||
  path.join(process.env.HOME || '/tmp', '.openclaw', 'cache', 'artificial-analysis');

function loadApiKey() {
  if (process.env.ARTIFICIAL_ANALYSIS_API_KEY) {
    return process.env.ARTIFICIAL_ANALYSIS_API_KEY.trim();
  }
  const credPath =
    process.env.ARTIFICIAL_ANALYSIS_CREDENTIALS ||
    path.join(process.env.HOME || '', '.openclaw', 'credentials', 'artificial-analysis.json');
  if (fs.existsSync(credPath)) {
    const raw = JSON.parse(fs.readFileSync(credPath, 'utf8'));
    return raw.api_key || raw.apiKey || raw.x_api_key;
  }
  return null;
}

function round(n, digits = 2) {
  if (n == null || Number.isNaN(n)) return null;
  return Math.round(n * 10 ** digits) / 10 ** digits;
}

function normalizeModel(row) {
  const ev = row.evaluations || {};
  const pr = row.pricing || {};
  return {
    id: row.id,
    name: row.name,
    slug: row.slug,
    creator_id: row.model_creator?.id ?? null,
    creator_name: row.model_creator?.name ?? null,
    creator_slug: row.model_creator?.slug ?? null,
    intelligence_index: ev.artificial_analysis_intelligence_index ?? null,
    coding_index: ev.artificial_analysis_coding_index ?? null,
    math_index: ev.artificial_analysis_math_index ?? null,
    mmlu_pro: ev.mmlu_pro != null ? round(ev.mmlu_pro * 100, 1) : null,
    gpqa: ev.gpqa != null ? round(ev.gpqa * 100, 1) : null,
    hle: ev.hle != null ? round(ev.hle * 100, 1) : null,
    livecodebench: ev.livecodebench != null ? round(ev.livecodebench * 100, 1) : null,
    scicode: ev.scicode != null ? round(ev.scicode * 100, 1) : null,
    math_500: ev.math_500 != null ? round(ev.math_500 * 100, 1) : null,
    aime: ev.aime != null ? round(ev.aime * 100, 1) : null,
    price_blended_3_1: pr.price_1m_blended_3_to_1 ?? null,
    price_input_1m: pr.price_1m_input_tokens ?? null,
    price_output_1m: pr.price_1m_output_tokens ?? null,
    output_tps: round(row.median_output_tokens_per_second, 1),
    ttft_seconds: round(row.median_time_to_first_token_seconds, 2),
    source: 'artificialanalysis.ai',
    fetched_at: new Date().toISOString(),
  };
}

async function main() {
  const apiKey = loadApiKey();
  if (!apiKey) {
    console.error(
      '缺少 API Key。请设置环境变量 ARTIFICIAL_ANALYSIS_API_KEY，或创建 ~/.openclaw/credentials/artificial-analysis.json：\n' +
        '  {"api_key":"你的key"}\n' +
        '申请地址：https://artificialanalysis.ai/ （Insights Platform 生成 key）',
    );
    process.exit(1);
  }

  console.log(`🌐 GET ${API_URL}`);
  const res = await fetch(API_URL, {
    headers: { 'x-api-key': apiKey, Accept: 'application/json' },
  });

  if (res.status === 401) {
    console.error('401：API Key 无效或缺失，请检查 x-api-key');
    process.exit(1);
  }
  if (res.status === 429) {
    console.error('429：超过每日 1000 次限额，请稍后重试');
    process.exit(1);
  }
  if (!res.ok) {
    const body = await res.text();
    console.error(`请求失败 HTTP ${res.status}: ${body.slice(0, 500)}`);
    process.exit(1);
  }

  const json = await res.json();
  const rows = Array.isArray(json.data) ? json.data : [];
  const models = rows.map(normalizeModel).sort((a, b) => (b.intelligence_index ?? 0) - (a.intelligence_index ?? 0));

  fs.mkdirSync(CACHE_DIR, { recursive: true });
  const date = new Date().toISOString().slice(0, 10);
  const outPath = path.join(CACHE_DIR, `llms-${date}.json`);
  const latestPath = path.join(CACHE_DIR, 'llms-latest.json');

  const payload = {
    source: API_URL,
    attribution: 'https://artificialanalysis.ai/',
    prompt_options: json.prompt_options ?? null,
    count: models.length,
    fetched_at: new Date().toISOString(),
    models,
  };

  fs.writeFileSync(outPath, JSON.stringify(payload, null, 2));
  fs.writeFileSync(latestPath, JSON.stringify(payload, null, 2));

  console.log(`✅ 已拉取 ${models.length} 个模型`);
  console.log(`OUTPUT:${outPath}`);
  console.log(`LATEST:${latestPath}`);

  if (models[0]) {
    const t = models[0];
    console.log(`示例 Top1: ${t.name} (${t.creator_name}) 智能指数 ${t.intelligence_index}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

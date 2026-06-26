#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';

const ROOT = dirname(new URL('../package.json', import.meta.url).pathname);
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const STATE_PATH = process.env.DOUYIN_PERSONA_STATE_PATH || join(STATE_DIR, 'persona-state.json');
const PERSONA_PROMPT_URL = new URL('../references/persona-positioning-prompt.md', import.meta.url);

const REQUIRED_FIELDS = [
  { key: 'name', label: '姓名/昵称', aliases: ['姓名', '昵称', '名字', 'name'] },
  { key: 'photo', label: '本人照片链接', aliases: ['照片', '本人照片', '形象照片', '头像照片', '头像', 'photo', 'image'] },
  { key: 'sex', label: '性别', aliases: ['性别', 'sex'] },
  { key: 'work_year', label: '从业年限', aliases: ['从业年限', '深耕年限', '年限', 'work_year'] },
  { key: 'bissiness', label: '主营业务', aliases: ['主营业务', '核心业务', '主营服务', '业务', 'bissiness', 'business'] },
  { key: 'advantage', label: '核心优势', aliases: ['核心优势', '差异化竞争力', '优势', 'advantage'] },
  { key: 'segment', label: '目标客户', aliases: ['目标客户', '精准受众', '受众', '客户', 'segment'] },
  { key: 'trials', label: '个人特质', aliases: ['个人特质', '性格优势', '特质', 'trials', 'traits'] },
  { key: 'cases', label: '经验案例', aliases: ['过往经验', '相关经验', '案例', '经验案例', 'cases'] },
  { key: 'demand', label: 'IP诉求', aliases: ['IP核心诉求', '核心诉求', '诉求', '目标', 'demand'] },
  { key: 'taboos', label: '禁忌偏好', aliases: ['禁忌', '偏好', '禁忌与偏好', 'taboos'] },
];

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function loadEnvFileIntoProcess(path) {
  try {
    if (!existsSync(path)) return;
    for (const rawLine of readFileSync(path, 'utf8').split(/\r?\n/)) {
      const line = rawLine.trim();
      if (!line || line.startsWith('#') || !line.includes('=')) continue;
      const index = line.indexOf('=');
      const key = line.slice(0, index).trim();
      let value = line.slice(index + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      if (key && value && (process.env[key] === undefined || process.env[key] === '')) process.env[key] = value;
    }
  } catch {
    // Local env files are optional.
  }
}

loadEnvFileIntoProcess(join(ROOT, '.env.local'));
loadEnvFileIntoProcess(join(ROOT, '.env.development'));
loadEnvFileIntoProcess(join(ROOT, '.env'));

function parseFirstJsonObject(text) {
  let raw = String(text || '').trim();
  const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenced?.[1]) raw = fenced[1].trim();
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < raw.length; i += 1) {
    const ch = raw[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        return JSON.parse(raw.slice(start, i + 1));
      }
    }
  }
  throw new Error('json_object_not_found');
}

function readJson(path, fallback) {
  try {
    if (!existsSync(path)) return fallback;
    return parseFirstJsonObject(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function readText(pathOrUrl, fallback = '') {
  try {
    return readFileSync(pathOrUrl, 'utf8');
  } catch {
    return fallback;
  }
}

function writeJson(path, value) {
  mkdirSync(dirname(path), { recursive: true });
  const tempPath = `${path}.tmp-${process.pid}-${Date.now()}`;
  writeFileSync(tempPath, `${JSON.stringify(value, null, 2)}\n`);
  renameSync(tempPath, path);
}

function loadState() {
  const fallback = {
    version: 1,
    status: 'empty',
    fields: {},
    draft: null,
    confirmed: null,
    history: [],
  };
  const state = readJson(STATE_PATH, fallback);
  return {
    ...fallback,
    ...(state && typeof state === 'object' ? state : {}),
    fields: state?.fields && typeof state.fields === 'object' ? state.fields : {},
    history: Array.isArray(state?.history) ? state.history : [],
  };
}

function saveState(state) {
  writeJson(STATE_PATH, {
    ...state,
    updatedAt: new Date().toISOString(),
  });
}

function stripQuotes(value) {
  return String(value || '').trim().replace(/^["“”']|["“”']$/g, '').trim();
}

function setField(fields, key, value) {
  const clean = stripQuotes(value);
  if (clean) fields[key] = clean;
}

function normalizeInlineText(text) {
  return String(text || '')
    .replace(/\r?\n/g, '。')
    .replace(/[；;]/g, '。')
    .replace(/\s+/g, ' ')
    .trim();
}

function cleanInferredValue(value) {
  return stripQuotes(value)
    .replace(/^(是|为|叫|做|从事|主要是|主要做|主要服务|主要帮|想|希望|目标是|目标|禁忌是|偏好是)\s*/u, '')
    .replace(/[。！？!?，,；;：:、\s]+$/u, '')
    .trim();
}

function setFieldIfEmpty(fields, key, value, maxLength = 80) {
  if (fields[key]) return;
  const clean = cleanInferredValue(value).slice(0, maxLength).trim();
  if (key === 'bissiness' && looksLikeInvalidBusiness(clean)) return;
  if (clean) fields[key] = clean;
}

function looksLikeInvalidBusiness(value) {
  const raw = String(value || '').trim();
  return !raw
    || /^了?\s*\d{1,2}\s*年$/u.test(raw)
    || /^\d{1,2}\s*年(?:经验|从业)?$/u.test(raw)
    || /^(男|女|男性|女性|先生|女士)$/u.test(raw);
}

function inferByPatterns(raw, patterns, maxLength = 80) {
  for (const pattern of patterns) {
    const match = raw.match(pattern);
    if (match?.[1]) return cleanInferredValue(match[1]).slice(0, maxLength).trim();
  }
  return '';
}

function inferFreeformFields(text) {
  const fields = {};
  const raw = normalizeInlineText(text);
  if (!raw) return fields;

  setFieldIfEmpty(fields, 'name', inferByPatterns(raw, [
    /(?:我叫|我是|本人(?:叫|是)?|昵称(?:叫|是)?|名字(?:叫|是)?)\s*([A-Za-z0-9\u4e00-\u9fa5_-]{1,12})(?=[，,。；;\s]|$)/u,
  ]), 16);

  const sex = raw.match(/(?:性别\s*[:：]?\s*)?(男士|女士|先生|女性|男性|男|女)(?=[，,。；;\s]|$)/u);
  if (sex?.[1]) {
    const value = sex[1];
    if (/男|先生/.test(value)) fields.sex = '男';
    else if (/女|女士/.test(value)) fields.sex = '女';
  }

  const age = raw.match(/(?:年龄|age)\s*[:：]?\s*(\d{1,3})\s*(?:岁)?/iu);
  if (age?.[1]) fields.age = `${age[1]}`;

  const photo = raw.match(/(?:照片|本人照片|形象照片|头像照片|头像|photo|image)\s*[:：=]?\s*(https?:\/\/[^\s"'<>，。；;]+)/iu);
  if (photo?.[1]) fields.photo = photo[1].replace(/[，。；;、)）\]}】]+$/g, '');

  const year = raw.match(/(?:从业|深耕|做(?:了)?|干(?:了)?|经验|年限|入行)[^\d]{0,8}(\d{1,2})\s*年/u);
  if (year?.[1]) fields.work_year = `${year[1]}`;

  setFieldIfEmpty(fields, 'bissiness', inferByPatterns(raw, [
    /(?:主营业务|核心业务|主营服务|业务)\s*[:：]?\s*([^。！？!?；;]{2,80})/u,
    /(?:主要)?(?:做(?!了?\s*\d{1,2}\s*年)|从事|经营)\s*([^。！？!?；;，,]{2,40})(?=[，,。；;]|$)/u,
    /(?:我是|作为)一?名?([^。！？!?；;，,]{2,36})(?:顾问|老师|专家|从业者|销售|咨询师|讲师)/u,
  ]), 80);

  setFieldIfEmpty(fields, 'advantage', inferByPatterns(raw, [
    /(?:核心优势|优势|差异化|擅长|比较会|最会|强项)\s*(?:是|在于|[:：])?\s*([^。！？!?；;]{2,90})/u,
    /(?:能|可以|会)\s*([^。！？!?；;]{2,80})(?:讲清楚|说明白|拆解|解决)/u,
  ]), 90);

  setFieldIfEmpty(fields, 'segment', inferByPatterns(raw, [
    /(?:目标客户|精准受众|受众|客户人群|服务对象)\s*[:：]?\s*([^。！？!?；;]{2,90})/u,
    /(?:主要)?(?:服务|面向|帮助|帮|给)\s*([^。！？!?；;]{2,80})(?:客户|人群|家庭|用户|的人)/u,
    /(?:想让|希望让)\s*([^。！？!?；;]{2,80})(?:别|少|能|可以|知道|学会)/u,
  ]), 90);

  setFieldIfEmpty(fields, 'trials', inferByPatterns(raw, [
    /(?:个人特质|性格|风格|人设调性|表达风格|说话风格)\s*[:：]?\s*([^。！？!?；;]{2,80})/u,
    /(?:我)?说话(?:比较|很)?\s*([^。！？!?；;]{2,60})/u,
    /(?:我是|我属于|本人(?:比较|很)?)\s*([^。！？!?；;]{2,60})(?:的人|性格|风格)/u,
    /(?:我(?:比较|很)?|本人(?:比较|很)?)\s*(专业|亲和|严谨|幽默|直接|耐心|细致|靠谱|务实|理性)(?:[、，,和](专业|亲和|严谨|幽默|直接|耐心|细致|靠谱|务实|理性))*/u,
  ]), 80);

  setFieldIfEmpty(fields, 'cases', inferByPatterns(raw, [
    /(?:经验案例|过往经验|相关经验|案例|服务过|处理过)\s*[:：]?\s*([^。！？!?；;]{2,100})/u,
    /(?:服务过|帮助过|做过|处理过)\s*([^。！？!?；;]{2,90})/u,
  ]), 100);

  setFieldIfEmpty(fields, 'demand', inferByPatterns(raw, [
    /(?:IP核心诉求|核心诉求|IP诉求|诉求|目标)\s*[:：]?\s*([^。！？!?；;]{2,100})/u,
    /(?:想在|希望在|准备在)\s*((?:抖音|视频号|小红书|快手|私域)[^。！？!?；;]{0,80})/u,
    /(?:想|希望|目标是|计划)\s*([^。！？!?；;]{2,90})(?:获客|咨询|转化|涨粉|建立信任|做账号)/u,
  ]), 100);

  setFieldIfEmpty(fields, 'taboos', inferByPatterns(raw, [
    /(?:禁忌与偏好|禁忌偏好|禁忌|偏好|不要|不能|避免)\s*[:：]?\s*([^。！？!?；;]{2,100})/u,
  ]), 100);

  return fields;
}

function parseStructuredText(text, opts = {}) {
  const fields = {};
  const raw = String(text || '');
  for (const line of raw.split(/\r?\n|；|;/)) {
    const cleaned = line.trim().replace(/^[*-]\s*/, '');
    if (!cleaned) continue;
    const match = cleaned.match(/^([^:：]{1,20})\s*[:：]\s*(.+)$/);
    if (!match) continue;
    const keyText = match[1].trim();
    const value = match[2].trim();
    for (const field of REQUIRED_FIELDS) {
      if (field.aliases.some((alias) => keyText.includes(alias))) {
        setField(fields, field.key, value);
        break;
      }
    }
  }

  const year = raw.match(/(?:从业|深耕|做了|经验|年限)[^\d]{0,8}(\d{1,2})\s*年/);
  if (year && !fields.work_year) fields.work_year = `${year[1]}`;
  const sex = raw.match(/性别\s*[:：]\s*([男女]|男士|女士|先生|女性|男性)/);
  if (sex && !fields.sex) fields.sex = sex[1];
  if (opts.inferFreeform !== false) {
    const inferred = inferFreeformFields(raw);
    for (const [key, value] of Object.entries(inferred)) {
      if (!fields[key]) fields[key] = value;
    }
  }
  return fields;
}

function missingFields(fields) {
  return REQUIRED_FIELDS.filter((item) => !String(fields?.[item.key] || '').trim());
}

function missingPrompt(missing) {
  const labels = missing.map((item) => item.label).join('、');
  const example = missing
    .slice(0, 5)
    .map((item) => `${item.label}：${exampleValue(item.key)}`)
    .join('；');
  const suffix = missing.length > 5 ? '；其他缺失项也可以继续补充' : '';
  return [
    `老板，已收到部分信息，还缺：${labels}。`,
    `可直接这样回：${example}${suffix}`,
  ].join('\n');
}

function initialMarketingPrompt() {
  return [
    '老板好~✨ 打造个人IP，最关键的是打造无可替代的差异化人设，坚决❌拒绝千篇一律的流水线包装，绝不盲目跟风。',
    '为了让您的IP既有“辨识度”又有“信任感”，请您提供姓名/昵称、性别、照片、从业/深耕年限、核心业务、核心优势、目标客户、个人特质信息、过往相关经验/案例、IP核心诉求、禁忌与偏好等信息～',
  ].join('\n');
}

function exampleValue(key) {
  const examples = {
    name: '老王',
    photo: 'https://example.com/photo.jpg',
    sex: '男',
    age: '35',
    work_year: '5年',
    bissiness: '宠物保险顾问',
    advantage: '熟悉理赔坑，能把条款讲清楚',
    segment: '新手养宠家庭',
    trials: '专业、直接、亲和',
    cases: '服务过100个养宠家庭',
    demand: '通过抖音建立信任并获取咨询',
    taboos: '不夸大、不承诺一定理赔',
  };
  return examples[key] || '请填写';
}

function loadOpenClawLlmConfig() {
  const candidates = [
    process.env.OPENCLAW_MODELS_PATH,
    join(homedir(), '.openclaw', 'agents', 'main', 'agent', 'models.json'),
    process.env.OPENCLAW_CONFIG_PATH || join(homedir(), '.openclaw', 'openclaw.json'),
  ].filter(Boolean);
  for (const path of candidates) {
    if (!existsSync(path)) continue;
    try {
      const cfg = JSON.parse(readFileSync(path, 'utf8'));
      const providers = cfg.providers || cfg.models?.providers || {};
      const preferredProvider = process.env.DOUYIN_PERSONA_PROVIDER || process.env.OPENCLAW_PROVIDER || 'custom';
      const entries = [
        [preferredProvider, providers[preferredProvider]],
        ...Object.entries(providers).filter(([key]) => key !== preferredProvider),
      ].filter(([, provider]) => provider?.apiKey && provider?.baseUrl);
      for (const [providerId, provider] of entries) {
        const models = Array.isArray(provider.models) ? provider.models : [];
        const model = process.env.DOUYIN_PERSONA_MODEL
          || process.env.OPENCLAW_MODEL
          || models.find((item) => item?.id)?.id
          || provider.model
          || 'MiniMax-M2.7';
        return {
          providerId,
          api: provider.api || 'openai-chat-completions',
          apiKey: provider.apiKey,
          rawBaseUrl: provider.baseUrl,
          model,
          sourcePath: path,
        };
      }
    } catch {
      // Optional config may be absent or malformed; fall back to env.
    }
  }
  return null;
}

function resolveLlmConfig(opts = {}) {
  const mode = String(opts.llm || process.env.DOUYIN_PERSONA_LLM || 'auto').toLowerCase();
  if (['off', 'false', '0', 'none', 'rule', 'rules'].includes(mode)) return { enabled: false, mode };
  const openclaw = loadOpenClawLlmConfig();
  const apiKey = process.env.DOUYIN_PERSONA_API_KEY
    || openclaw?.apiKey
    || process.env.MINIMAX_API_KEY
    || process.env.OPENAI_API_KEY
    || '';
  const rawBaseUrl = opts.baseUrl
    || process.env.DOUYIN_PERSONA_BASE_URL
    || openclaw?.rawBaseUrl
    || process.env.MINIMAX_API_BASE_URL
    || process.env.OPENAI_BASE_URL
    || process.env.OPENAI_API_BASE
    || '';
  const model = opts.model
    || process.env.DOUYIN_PERSONA_MODEL
    || openclaw?.model
    || process.env.MINIMAX_MODEL
    || process.env.OPENCLAW_MODEL
    || process.env.OPENAI_MODEL
    || 'MiniMax-M2.7';
  if (!apiKey || !rawBaseUrl) return { enabled: false, mode, missing: !apiKey ? 'api_key' : 'base_url' };
  const baseUrl = String(rawBaseUrl).replace(/\/+$/, '');
  const api = process.env.DOUYIN_PERSONA_API || openclaw?.api || 'openai-chat-completions';
  const useOpenAiEndpoint = /minimaxi\.com\/anthropic/.test(baseUrl) && api !== 'anthropic-messages';
  const effectiveApi = useOpenAiEndpoint ? 'openai-chat-completions' : api;
  const endpoint = effectiveApi === 'anthropic-messages'
    ? (/\/v1\/messages$/.test(baseUrl) ? baseUrl : `${baseUrl}/v1/messages`)
    : (useOpenAiEndpoint
      ? 'https://api.minimaxi.com/v1/chat/completions'
      : (/\/chat\/completions$/.test(baseUrl) ? baseUrl : `${baseUrl}/chat/completions`));
  return {
    enabled: true,
    mode,
    api: effectiveApi,
    apiKey,
    endpoint,
    model,
    providerId: openclaw?.providerId,
    timeoutMs: Math.max(3000, Math.min(180000, Number(opts.llmTimeoutMs || process.env.DOUYIN_PERSONA_LLM_TIMEOUT_MS || 120000))),
  };
}

function inferVerticalKeyword(fields) {
  const business = String(fields.bissiness || '').trim();
  const compact = business.replace(/[，。；、,.;\s]/g, '');
  return compact.slice(0, 10) || '专业服务';
}

function inferAudience(fields) {
  return String(fields.segment || '').trim().slice(0, 24) || '目标客户';
}

function inferCaseCount(cases) {
  const match = String(cases || '').match(/(\d{1,6})\s*(?:个|位|名|家|例|\+)/);
  return match ? `${match[1]}` : '多位';
}

function yearText(value) {
  const raw = String(value || '').trim();
  if (!raw) return '多年';
  return /\d+\s*年/.test(raw) ? raw.replace(/\s+/g, '') : `${raw}年`;
}

function textFromSection(value) {
  if (!value) return '';
  if (typeof value === 'string') return value.trim();
  if (Array.isArray(value)) return value.map(textFromSection).filter(Boolean).join('\n');
  if (typeof value === 'object') {
    return Object.entries(value)
      .map(([key, item]) => {
        const text = textFromSection(item);
        return text ? `${key}：${text}` : '';
      })
      .filter(Boolean)
      .join('\n');
  }
  return String(value).trim();
}

function firstString(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
}

function renderPersonaPromptTemplate(template, fields) {
  return String(template || '').replace(/\{\{(name|sex|work_year|bissiness|advantage|segment|trials|cases|demand|taboos)\}\}/g, (_, key) => {
    return String(fields?.[key] || '').trim();
  });
}

function normalizePersonaTextDraft(text, fields, meta = {}) {
  const fallback = generatePersona(fields);
  const raw = String(text || '').trim();
  const strategyMatch = raw.match(/(?:\[?[^\\n\\[]*IP人设定位方案\]?|IP人设定位方案|\[?[^\\n\\[]*IP战略定位方案\]?|IP战略定位方案)([\s\S]*?)(?=(?:\[?[^\n\[]*IP营销策划方案\]?|IP营销策划方案)|$)/u);
  const marketingMatch = raw.match(/(?:\[?[^\\n\\[]*IP营销策划方案\]?|IP营销策划方案)([\s\S]*)$/u);
  const strategy = strategyMatch?.[0]?.trim() || raw || fallback.strategy;
  const marketing = marketingMatch?.[0]?.trim() || '';
  return {
    generatedAt: new Date().toISOString(),
    source: meta.source || 'llm',
    model: meta.model || null,
    fields,
    summary: fallback.summary,
    strategy,
    marketing,
    customerPersona: {},
    accountProfile: {},
    contentRules: {},
    platformPlan: { primary: '抖音' },
    digitalHumanGuidance: {
      usableFor: '可用于后续视频脚本、口播、人设一致性。',
      notUsableFor: '不能仅靠人设文本直接生成数字人模型ID。',
      idPolicy: '需通过训练数字人流程生成ID；客户已有自己的数字人时，可直接绑定ID替换。',
    },
    llmTextWrapped: true,
  };
}

function llmHeaders(cfg) {
  if (cfg.api === 'anthropic-messages') {
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${cfg.apiKey}`,
      'x-api-key': cfg.apiKey,
      'anthropic-version': process.env.DOUYIN_PERSONA_ANTHROPIC_VERSION || '2023-06-01',
    };
  }
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${cfg.apiKey}`,
  };
}

function generatePersona(fields) {
  const vertical = inferVerticalKeyword(fields);
  const audience = inferAudience(fields);
  const caseCount = inferCaseCount(fields.cases);
  const name = fields.name || '该账号';
  const workYear = yearText(fields.work_year);
  const title = `${name}IP战略定位方案`;
  const strategy = [
    title,
    '',
    '一、IP定位核心分析前提',
    `基于 ${name}（${fields.sex || '未说明'}，从业 ${workYear}）、主营业务“${fields.bissiness}”、核心优势“${fields.advantage}”，账号应围绕业务合规变现、精准人群适配和真实人设落地展开。`,
    '',
    '二、核心业务适配性',
    `聚焦“${vertical}”相关的具体服务场景，避免泛泛讲知识。内容应持续回答目标客户在决策前最关心的成本、风险、误区和行动步骤。`,
    '',
    '三、目标人群',
    `核心受众是：${audience}。内容要优先覆盖他们的真实痛点、常见误解和选择阻碍，用短视频降低信任门槛，再引导私域咨询或进一步沟通。`,
    '',
    '四、IP人设定位',
    `核心身份：${workYear}${vertical}从业者，专注为${audience}提供可落地的解决方案。`,
    `沟通调性：${fields.trials}。表达要具体、直接、少空话，避免夸大承诺。`,
    `信任背书：结合“${fields.cases}”和“${fields.advantage}”呈现专业度。`,
    '',
    '五、平台与内容方向',
    '核心平台建议以抖音为主，内容形式优先短口播、案例拆解、误区澄清和问题答疑；辅助平台可承接图文沉淀和私域转化。',
  ].join('\n');

  const marketing = [
    `${name}IP营销策划方案`,
    '',
    '一、IP核心定位',
    `核心专业身份：${workYear}${vertical}从业者，专注为${audience}提供高确定性的专业服务。`,
    `核心价值主张：少踩坑，做对选择。`,
    `人设沟通调性：${fields.trials}`.slice(0, 80),
    `核心信任背书：${workYear}经验，累计服务${caseCount}+${audience}客户，主打${fields.advantage}。`,
    '',
    '二、账号基础资料',
    `账号名称：${name}${vertical}`,
    `账号简介：${workYear}${vertical}从业者｜专注${audience}｜${String(fields.advantage || '').slice(0, 28)}｜欢迎私信咨询`,
    `账号话题标签：#${vertical} #经验分享 #避坑指南 #专业服务 #抖音运营`,
    '',
    '三、内容运营规范',
    `内容聚焦：围绕 ${audience} 的痛点、误区、案例和决策问题。`,
    `发布频率：默认每天 1 条，优先早上 07:30 后发布。`,
    `合规边界：严格遵循“${fields.taboos}”，不承诺收益、结果或平台不可控效果。`,
  ].join('\n');

  return {
    generatedAt: new Date().toISOString(),
    source: 'rules',
    fields,
    summary: {
      personaId: `${name}-${vertical}`.replace(/\s+/g, ''),
      coreIdentity: `${workYear}${vertical}从业者`,
      audience,
      tone: fields.trials,
      value: fields.advantage,
      primaryPlatform: '抖音',
    },
    strategy,
    marketing,
  };
}

function buildPersonaMessages(fields, section = 'json') {
  const mentorPrompt = renderPersonaPromptTemplate(readText(PERSONA_PROMPT_URL), fields);
  if (section === 'strategy' || section === 'marketing') {
    const sectionTitle = section === 'strategy' ? 'IP人设定位方案' : '人设后续内容运营补充';
    return [
      {
        role: 'system',
        content: [
          '你是个人 IP 战略定位与自动化营销画像生成器。',
          '必须严格基于用户给出的信息推导，不得虚构具体成绩、资质、金额、案例数量。',
          '请完整遵循下方 mentor prompt 的分析框架。',
          mentorPrompt,
        ].join('\n\n'),
      },
      {
        role: 'user',
        content: [
          `只输出《${sectionTitle}》正文，必须详细、可落地，不要输出 JSON，不要输出另一份方案，不要解释。`,
          '如果 revision_feedback 存在，说明用户不通过上一版方案，必须按修改建议重写。',
          '',
          JSON.stringify(fields, null, 2),
        ].join('\n'),
      },
    ];
  }
  const schema = {
    summary: {
      personaId: '姓名-垂直领域',
      coreIdentity: '核心专业身份',
      audience: '目标客户摘要',
      tone: '3个以内沟通调性关键词',
      value: '核心价值/差异化优势',
      primaryPlatform: '核心平台',
      slogan: '15字以内价值主张',
    },
    strategy: '完整《IP人设定位方案》正文，必须包含IP核心定位、精准用户画像、账号全套定位资料',
    marketing: '可选：基于该人设的短视频内容与运营补充，不要重复《IP人设定位方案》',
    customerPersona: {
      coreLabel: '核心人群标签',
      attributes: '年龄、职业、地域、消费能力等',
      painPoints: ['核心痛点1', '核心痛点2'],
      needs: ['核心需求1', '核心需求2'],
      behaviorPreference: '内容与行为偏好',
      decisionPreference: '消费决策偏好',
    },
    accountProfile: {
      accountName: '账号名称',
      bio: '账号简介',
      avatarSuggestion: '头像建议',
      backgroundSuggestion: '背景图建议',
      hashtags: ['#标签1', '#标签2'],
    },
    contentRules: {
      pillars: ['内容支柱1', '内容支柱2'],
      frequency: '发布频率',
      compliance: '合规边界',
      interactionTone: '评论和私信回复调性',
    },
    platformPlan: {
      primary: '核心运营平台',
      auxiliaries: ['辅助平台1'],
      conversionPath: '从曝光到转化的路径',
    },
    digitalHumanGuidance: {
      usableFor: '可用于后续视频脚本、口播、人设一致性',
      notUsableFor: '不能仅靠人设文本直接生成数字人模型ID',
      idPolicy: '需通过训练数字人流程生成ID；客户已有自己的数字人时，可直接绑定ID替换',
    },
  };
  return [
    {
      role: 'system',
      content: [
        '你是个人 IP 战略定位与自动化营销画像生成器。',
        '必须严格基于用户给出的信息推导，不得虚构具体成绩、资质、金额、案例数量。',
        '请完整遵循下方 mentor prompt 的分析框架，但最终只输出一个合法 JSON 对象，不要 Markdown 代码块，不要解释。',
        '不得保留任何 {{...}} 占位符；所有模板变量都必须根据用户信息或合理推导改写为具体内容。',
        '此处只生成人设、定位、用户画像和内容策略；数字人ID由后续训练数字人流程生成，或由客户绑定已有ID。',
        mentorPrompt,
      ].join('\n\n'),
    },
    {
      role: 'user',
      content: [
        '请基于以下用户信息生成客户《IP人设定位方案》。',
        '如果 revision_feedback 存在，说明用户不通过上一版方案，必须按修改建议重写，不要只做轻微摘要修改。',
        '输出必须详细，不能只给简单标签；必须完整覆盖IP核心定位、精准用户画像、账号全套定位资料。',
        '',
        JSON.stringify(fields, null, 2),
        '',
        '输出 JSON schema 示例：',
        JSON.stringify(schema, null, 2),
      ].join('\n'),
    },
  ];
}

function normalizePersonaDraft(parsed, fields, meta = {}) {
  const fallback = generatePersona(fields);
  const summary = parsed.summary || {};
  const customerPersona = parsed.customerPersona || parsed.preciseCustomerPersona || parsed.userPersona || {};
  const accountProfile = parsed.accountProfile || parsed.accountPositioning || {};
  const platformPlan = parsed.platformPlan || parsed.platform || {};
  const contentRules = parsed.contentRules || parsed.contentOperationRules || {};
  const strategy = textFromSection(parsed.strategy || parsed.ipPersonaPositioning || parsed.ipPositioningPlan || parsed.ipStrategy || parsed.ipStrategicPositioning) || fallback.strategy;
  const marketing = textFromSection(parsed.marketing || parsed.marketingPlan || parsed.ipMarketingPlan || parsed.contentOperationPlan || parsed.operationPlan);

  return {
    generatedAt: new Date().toISOString(),
    source: meta.source || 'llm',
    model: meta.model || null,
    fields,
    summary: {
      personaId: firstString(summary.personaId, accountProfile.accountName, fallback.summary.personaId),
      coreIdentity: firstString(summary.coreIdentity, summary.identity, accountProfile.coreIdentity, fallback.summary.coreIdentity),
      audience: firstString(summary.audience, customerPersona.coreLabel, customerPersona.attributes, fallback.summary.audience),
      tone: firstString(summary.tone, contentRules.interactionTone, fallback.summary.tone),
      value: firstString(summary.value, summary.valueProposition, summary.slogan, fallback.summary.value),
      primaryPlatform: firstString(summary.primaryPlatform, platformPlan.primary, fallback.summary.primaryPlatform),
      slogan: firstString(summary.slogan, summary.valueProposition),
    },
    strategy,
    marketing,
    customerPersona,
    accountProfile,
    contentRules,
    platformPlan,
    digitalHumanGuidance: parsed.digitalHumanGuidance || {
      usableFor: '可用于后续视频脚本、口播、人设一致性。',
      notUsableFor: '不能仅靠人设文本直接生成数字人模型ID。',
      idPolicy: '需通过训练数字人流程生成ID；客户已有自己的数字人时，可直接绑定ID替换。',
    },
  };
}

async function callPersonaLlm(fields, opts = {}) {
  const cfg = resolveLlmConfig(opts);
  if (!cfg.enabled) return { ok: false, source: 'llm', reason: cfg.missing ? `missing_${cfg.missing}` : 'llm_disabled' };
  const section = opts.section || 'json';
  const messages = buildPersonaMessages(fields, section);
  const defaultMaxTokens = section === 'json' ? 12000 : 5000;
  const maxTokens = Number(process.env.DOUYIN_PERSONA_MAX_TOKENS || defaultMaxTokens);
  const body = cfg.api === 'anthropic-messages'
    ? {
      model: cfg.model,
      system: messages[0].content,
      messages: [{ role: 'user', content: messages[1].content }],
      max_tokens: maxTokens,
      temperature: 0.2,
    }
    : {
      model: cfg.model,
      messages,
      max_tokens: maxTokens,
      temperature: 0.2,
      ...(section === 'json' ? { response_format: { type: 'json_object' } } : {}),
    };
  try {
    const res = await fetch(cfg.endpoint, {
      method: 'POST',
      headers: llmHeaders(cfg),
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(cfg.timeoutMs),
    });
    const json = await res.json().catch(() => ({}));
    const text = cfg.api === 'anthropic-messages'
      ? (Array.isArray(json.content) ? json.content.map((item) => item?.text || '').join('\n') : '')
      : (json.choices?.[0]?.message?.content || json.choices?.[0]?.text || '');
    if (!res.ok || !text.trim()) {
      return { ok: false, source: 'llm', model: cfg.model, status: res.status, reason: 'llm_failed' };
    }
    if (section !== 'json') {
      return { ok: true, source: 'llm', model: cfg.model, text };
    }
    let parsed;
    try {
      parsed = parseFirstJsonObject(text);
    } catch (err) {
      if (/IP战略定位方案|IP营销策划方案|精准用户画像|账号基础资料|内容运营规范/.test(text)) {
        return {
          ok: true,
          source: 'llm',
          model: cfg.model,
          draft: normalizePersonaTextDraft(text, fields, { source: 'llm', model: cfg.model }),
        };
      }
      return {
        ok: false,
        source: 'llm',
        model: cfg.model,
        status: res.status,
        reason: 'llm_invalid_json',
        error: err.message,
        sample: text.slice(0, 300),
      };
    }
    return { ok: true, source: 'llm', model: cfg.model, draft: normalizePersonaDraft(parsed, fields, { source: 'llm', model: cfg.model }) };
  } catch (err) {
    return { ok: false, source: 'llm', model: cfg.model, reason: 'llm_request_failed', error: err.message };
  }
}

async function generatePersonaDraft(fields, opts = {}) {
  if (process.env.DOUYIN_ROUTE_LIGHT_TEST === 'true') {
    return {
      ...generatePersona(fields),
      source: 'rules-light-test',
    };
  }
  const splitLlm = String(process.env.DOUYIN_PERSONA_SPLIT_LLM || '').toLowerCase() === 'true';
  if (!opts.dryRun && process.env.DOUYIN_ROUTE_LIGHT_TEST !== 'true' && splitLlm) {
    const strategy = await callPersonaLlm(fields, { ...opts, section: 'strategy' });
    if (strategy.ok) {
      const marketing = await callPersonaLlm(fields, { ...opts, section: 'marketing' });
      if (marketing.ok) {
        return normalizePersonaTextDraft(`${strategy.text}\n\n${marketing.text}`, fields, {
          source: 'llm',
          model: strategy.model || marketing.model,
        });
      }
      return {
        ok: false,
        source: 'llm_failed',
        llmFailure: {
          reason: marketing.reason,
          model: marketing.model || strategy.model || null,
          status: marketing.status || null,
          error: marketing.error || null,
          sample: marketing.sample || null,
        },
      };
    }
    return {
      ok: false,
      source: 'llm_failed',
      llmFailure: {
        reason: strategy.reason,
        model: strategy.model || null,
        status: strategy.status || null,
        error: strategy.error || null,
        sample: strategy.sample || null,
      },
    };
  }
  const llm = await callPersonaLlm(fields, opts);
  if (llm.ok) return llm.draft;
  const allowFallback = opts.dryRun || opts.allowRulesFallback || process.env.DOUYIN_ROUTE_LIGHT_TEST === 'true' || process.env.DOUYIN_PERSONA_ALLOW_RULES_FALLBACK === 'true';
  if (!allowFallback) {
    return {
      ok: false,
      source: 'llm_failed',
      llmFailure: {
        reason: llm.reason,
        model: llm.model || null,
        status: llm.status || null,
        error: llm.error || null,
        sample: llm.sample || null,
      },
    };
  }
  const draft = generatePersona(fields);
  return {
    ...draft,
    source: 'rules-fallback',
    llmFallback: {
      reason: llm.reason,
      model: llm.model || null,
      status: llm.status || null,
      error: llm.error || null,
      sample: llm.sample || null,
    },
  };
}

function customerDraftText(draft) {
  const detail = fullDraftText(draft).replace(/^完整账号定位如下：\n*/u, '').trim();
  return [
    '老板，您的专属人设信息已完成，请您审核：',
    '',
    detail,
    '',
    '回复【通过】或【不通过】，若不通过，请指出修改建议～',
  ].filter(Boolean).join('\n');
}

function fullDraftText(draft) {
  if (!draft) return '还没有人设方案。请先发送：生成人设';
  const parts = [
    '完整账号定位如下：',
    '',
    draft.strategy,
    '',
    draft.marketing,
  ].filter(Boolean).join('\n');
  return parts;
}

function statusText(state) {
  if (state.confirmed) {
    return [
      '人设状态：已确认',
      `核心身份：${state.confirmed.summary?.coreIdentity || '-'}`,
      `目标客户：${state.confirmed.summary?.audience || '-'}`,
    ].join('\n');
  }
  if (state.draft) {
    return [
      '人设状态：待确认',
      `核心身份：${state.draft.summary?.coreIdentity || '-'}`,
      '如需采用当前方案，可回复：确认人设',
    ].join('\n');
  }
  const missing = missingFields(state.fields || {});
  return missing.length ? `人设状态：信息待补充。\n${missingPrompt(missing)}` : '人设状态：未生成。请发送：生成人设';
}

async function routeText(text, opts = {}) {
  const raw = String(text || '').trim();
  const state = loadState();
  let revisionRequested = false;
  if (opts.reset) {
    state.status = 'empty';
    state.fields = {};
    state.draft = null;
    state.confirmed = null;
    state.history = [];
  }
  if (/^(完整人设|查看完整人设|人设详情|账号定位详情)$/.test(raw)) {
    saveState(state);
    return { ok: true, action: 'persona_full_detail', statePath: STATE_PATH, customerMessage: fullDraftText(state.confirmed || state.draft), state };
  }
  if (/^(人设状态|账号定位状态|查看人设)$/.test(raw)) {
    saveState(state);
    return { ok: true, action: 'persona_status', statePath: STATE_PATH, customerMessage: statusText(state), state };
  }
  if (/^(确认人设|采用这个人设|确认采用|通过)$/.test(raw)) {
    if (state.confirmed) {
      saveState(state);
      return { ok: true, action: 'persona_already_confirmed', statePath: STATE_PATH, customerMessage: '' };
    }
    if (!state.draft) {
      saveState(state);
      return { ok: false, action: 'persona_confirm_without_draft', customerMessage: '还没有待确认人设。请先发送：生成人设' };
    }
    state.confirmed = { ...state.draft, confirmedAt: new Date().toISOString() };
    state.status = 'confirmed';
    state.history.push({ at: new Date().toISOString(), action: 'confirmed' });
    saveState(state);
    return { ok: true, action: 'persona_confirmed', statePath: STATE_PATH, customerMessage: '人设已确认。' };
  }
  if (/^(不通过|重新生成人设|不满意|调整人设|修改人设)/.test(raw)) {
    const feedback = raw.replace(/^(不通过|重新生成人设|不满意|调整人设|修改人设)\s*[，,。:：-]?\s*/u, '').trim();
    if (/^不通过$/.test(raw) || !feedback && /^(不满意|调整人设|修改人设)$/.test(raw)) {
      state.status = 'draft';
      saveState(state);
      return {
        ok: false,
        action: 'persona_revision_feedback_needed',
        customerMessage: '老板，请指出需要修改的方向，我会重新生成人设方案～',
      };
    }
    state.draft = null;
    state.status = 'collecting';
    state.history.push({ at: new Date().toISOString(), action: 'revision_requested', text: raw });
    state.fields.revision_feedback = feedback || raw;
    revisionRequested = true;
  }

  const incoming = parseStructuredText(raw, { inferFreeform: !revisionRequested });
  state.fields = { ...(state.fields || {}), ...incoming };

  if (/^(启动自动化营销|开启自动化营销)$/.test(raw) && Object.keys(incoming).length === 0 && !state.draft && !state.confirmed) {
    state.status = 'collecting';
    saveState(state);
    return { ok: true, action: 'persona_initial_collect_needed', statePath: STATE_PATH, missing: missingFields(state.fields || {}).map((item) => item.key), customerMessage: initialMarketingPrompt() };
  }

  if (/^(生成人设|账号定位|帮我做人设|开启自动化营销|启动自动化营销)$/.test(raw) && Object.keys(incoming).length === 0) {
    const missing = missingFields(state.fields || {});
    if (missing.length) {
      state.status = 'collecting';
      saveState(state);
      return { ok: true, action: 'persona_need_more_info', statePath: STATE_PATH, missing: missing.map((item) => item.key), customerMessage: missingPrompt(missing) };
    }
  }

  const missing = missingFields(state.fields || {});
  if (missing.length) {
    state.status = 'collecting';
    saveState(state);
    return { ok: true, action: 'persona_need_more_info', statePath: STATE_PATH, missing: missing.map((item) => item.key), customerMessage: missingPrompt(missing) };
  }

  if (opts.deferGenerate) {
    state.draft = null;
    state.confirmed = null;
    state.status = 'generating';
    state.history.push({ at: new Date().toISOString(), action: 'generation_deferred' });
    saveState(state);
    return {
      ok: true,
      action: 'persona_generation_deferred',
      statePath: STATE_PATH,
      customerMessage: '',
      fields: state.fields,
    };
  }

  state.draft = await generatePersonaDraft(state.fields, opts);
  if (state.draft?.ok === false && state.draft.source === 'llm_failed') {
    state.status = 'collecting';
    state.history.push({ at: new Date().toISOString(), action: 'persona_llm_failed', failure: state.draft.llmFailure });
    saveState(state);
    return {
      ok: false,
      action: 'persona_generation_failed',
      statePath: STATE_PATH,
      customerMessage: '人设生成暂未完成，请稍后重试。',
      failure: state.draft.llmFailure,
    };
  }
  state.confirmed = null;
  state.status = 'draft';
  state.history.push({ at: new Date().toISOString(), action: 'draft_generated' });
  saveState(state);
  return {
    ok: true,
    action: 'persona_draft_generated',
    statePath: STATE_PATH,
    draft: state.draft,
    customerMessage: customerDraftText(state.draft),
  };
}

function setFieldCommand(args) {
  const state = loadState();
  const key = String(args.key || args._[0] || '').trim();
  const value = String(args.value || args._.slice(1).join(' ') || '').trim();
  if (!REQUIRED_FIELDS.some((item) => item.key === key)) {
    return { ok: false, action: 'set_field', error: 'unknown_field', fields: REQUIRED_FIELDS.map((item) => item.key) };
  }
  setField(state.fields, key, value);
  saveState(state);
  return { ok: true, action: 'set_field', key, statePath: STATE_PATH };
}

async function main() {
  const [command = 'status', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  let output;
  if (command === 'status') {
    const state = loadState();
    output = { ok: true, action: 'persona_status', statePath: STATE_PATH, customerMessage: statusText(state), state };
  } else if (command === 'route-text') {
    output = await routeText(args.text || args._.join(' '), args);
  } else if (command === 'set-field') {
    output = setFieldCommand(args);
  } else if (command === 'generate') {
    output = await routeText(args.text || args._.join(' ') || '生成人设', args);
  } else if (command === 'confirm') {
    output = await routeText('确认人设', args);
  } else {
    output = { ok: false, error: 'unknown_command', usage: 'persona-flow.js status|route-text|set-field|generate|confirm' };
  }
  console.log(JSON.stringify(output, null, 2));
  if (output.ok === false) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});

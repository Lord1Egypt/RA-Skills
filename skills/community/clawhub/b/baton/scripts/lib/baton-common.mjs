import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

export const TIERS = ['fast','balanced','code','long_context','strong_reasoning','creative','multimodal'];
export const BATON_VERSION = '1.8.2';

export function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[key] = true;
      else out[key] = argv[++i];
    } else out._.push(a);
  }
  return out;
}

export function ensureDir(dir) { fs.mkdirSync(dir, { recursive: true }); }
export function readJson(file, fallback = null) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}
export function writeJson(file, value) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

export function batonPaths(args = {}) {
  const root = path.resolve(args.outDir || '.openclaw/baton');
  const agentId = args.agentId || args.agent || null;
  const scoped = agentId && (args.agentScoped || args.scoped);
  const agentRoot = agentId ? path.join(root, 'agents', agentId) : null;
  return { root, agentId, agentRoot, activeRoot: scoped ? agentRoot : root };
}

export function resolveStateFile(args, name, explicitKey = null) {
  if (explicitKey && args[explicitKey]) return path.resolve(args[explicitKey]);
  const { root, agentId, agentRoot } = batonPaths(args);
  if (agentId && agentRoot) {
    const candidate = path.join(agentRoot, name);
    if (fs.existsSync(candidate)) return candidate;
  }
  return path.join(root, name);
}

export function readJsonLike(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const cleaned = toSafeJson(raw, file);
  try { return JSON.parse(cleaned); }
  catch (err) { throw new Error(`Could not parse ${file}. Use strict JSON/JSONC or the supported safe JSON5 subset. No config text is executed. JSON error: ${err.message}`); }
}

export function toSafeJson(raw, file = '<input>') {
  if (raw.charCodeAt(0) === 0xfeff) raw = raw.slice(1);
  let s = stripJsonComments(raw);
  s = normalizeSingleQuotedStrings(s);
  s = quoteBareObjectKeys(s);
  s = removeTrailingCommas(s);
  return s;
}

export function stripJsonComments(s) {
  let out = '', inString = false, quote = '', escaped = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i], n = s[i + 1];
    if (inString) {
      out += c;
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === quote) inString = false;
      continue;
    }
    if (c === '"' || c === "'") { inString = true; quote = c; out += c; continue; }
    if (c === '/' && n === '/') { while (i < s.length && s[i] !== '\n') i++; out += '\n'; continue; }
    if (c === '/' && n === '*') { i += 2; while (i < s.length && !(s[i] === '*' && s[i + 1] === '/')) i++; i++; continue; }
    out += c;
  }
  return out;
}

export function normalizeSingleQuotedStrings(s) {
  let out = '', inString = false, quote = '', escaped = false, buf = '';
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (!inString) {
      if (c === '"') { inString = true; quote = c; escaped = false; out += c; }
      else if (c === "'") { inString = true; quote = c; escaped = false; buf = ''; }
      else out += c;
      continue;
    }
    if (quote === '"') {
      out += c;
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === '"') inString = false;
      continue;
    }
    if (escaped) {
      buf += decodeSingleQuoteEscape(c);
      escaped = false;
    } else if (c === '\\') escaped = true;
    else if (c === "'") { out += JSON.stringify(buf); inString = false; }
    else buf += c;
  }
  if (inString && quote === "'") throw new Error('Unterminated single-quoted string while parsing config');
  return out;
}

function decodeSingleQuoteEscape(c) {
  return ({ n:'\n', r:'\r', t:'\t', b:'\b', f:'\f', v:'\v', '0':'\0', "'":"'", '"':'"', '\\':'\\' })[c] ?? c;
}

export function removeTrailingCommas(s) {
  let out = '', inString = false, quote = '', escaped = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (inString) {
      out += c;
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === quote) inString = false;
      continue;
    }
    if (c === '"') { inString = true; quote = c; out += c; continue; }
    if (c === ',') {
      let j = i + 1;
      while (j < s.length && /\s/.test(s[j])) j++;
      if (s[j] === '}' || s[j] === ']') continue;
    }
    out += c;
  }
  return out;
}

export function quoteBareObjectKeys(s) {
  let out = '', inString = false, quote = '', escaped = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (inString) {
      out += c;
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === quote) inString = false;
      continue;
    }
    if (c === '"') { inString = true; quote = c; out += c; continue; }
    if (c === '{' || c === ',') {
      out += c;
      let j = i + 1, ws = '';
      while (j < s.length && /\s/.test(s[j])) ws += s[j++];
      const first = s[j];
      if (/[A-Za-z_$]/.test(first || '')) {
        let k = j + 1;
        while (k < s.length && /[A-Za-z0-9_$-]/.test(s[k])) k++;
        let m = k;
        while (m < s.length && /\s/.test(s[m])) m++;
        if (s[m] === ':') {
          out += ws + JSON.stringify(s.slice(j, k));
          i = k - 1;
          continue;
        }
      }
      out += ws;
      i = j - 1;
      continue;
    }
    out += c;
  }
  return out;
}

// Backward-compatible export name. This function never evaluates config text.
export function stripJsonCommentsAndTrailingCommas(s) {
  return removeTrailingCommas(normalizeSingleQuotedStrings(stripJsonComments(s)));
}

export function normalizeRef(value) {
  if (!value || typeof value !== 'string') return null;
  const ref = value.trim().replace(/^['"]|['"]$/g, '').toLowerCase();
  if (!/^[a-z0-9_.-]+\/[a-z0-9_.:\/-]+$/.test(ref)) return null;
  return ref;
}
export function providerOf(ref) { return String(ref).split('/')[0]; }
export function joinProvider(provider, model) { if (!provider || !model) return null; return String(model).includes('/') ? model : `${provider}/${model}`; }
export function arrayify(value) { return Array.isArray(value) ? value : []; }
export function walk(obj, cb, pointer = '') {
  if (!obj || typeof obj !== 'object') return;
  for (const [key, value] of Object.entries(obj)) {
    const next = pointer ? `${pointer}.${key}` : key;
    cb(value, next);
    if (value && typeof value === 'object') walk(value, cb, next);
  }
}
export function pickModelMeta(model) {
  if (!model || typeof model !== 'object') return {};
  const meta = {};
  for (const key of ['contextWindow','contextTokens','maxTokens','supportsVision','supportsTools','supportsThinking','costTier','latencyTier']) {
    if (model[key] !== undefined) meta[key] = model[key];
  }
  return meta;
}

export function discoverConfiguredModels(config, configPath = 'openclaw.json') {
  const found = new Map();
  const add = (ref, source, meta = {}) => {
    const normalized = normalizeRef(ref);
    if (!normalized) return;
    if (!found.has(normalized)) found.set(normalized, { ref: normalized, provider: providerOf(normalized), sources: [], meta: {} });
    const item = found.get(normalized);
    if (!item.sources.includes(source)) item.sources.push(source);
    item.meta = { ...item.meta, ...meta };
  };
  const defaultModel = config?.agents?.defaults?.model;
  if (typeof defaultModel === 'string') add(defaultModel, 'agents.defaults.model');
  add(defaultModel?.primary, 'agents.defaults.model.primary');
  for (const ref of arrayify(defaultModel?.fallbacks)) add(ref, 'agents.defaults.model.fallbacks');
  add(config?.agents?.defaults?.subagents?.model, 'agents.defaults.subagents.model');

  const defaultsModels = config?.agents?.defaults?.models;
  if (Array.isArray(defaultsModels)) {
    for (const value of defaultsModels) {
      if (typeof value === 'string') add(value, 'agents.defaults.models[]');
      else if (value && typeof value === 'object') add(value.ref || value.model || value.id || value.name, 'agents.defaults.models[]', pickModelMeta(value));
    }
  } else if (defaultsModels && typeof defaultsModels === 'object') {
    for (const [key, value] of Object.entries(defaultsModels)) {
      add(key, 'agents.defaults.models key', pickModelMeta(value));
      if (typeof value === 'string') add(value, `agents.defaults.models.${key}`);
      if (value && typeof value === 'object') {
        for (const field of ['model','ref','primary','id','name']) add(value[field], `agents.defaults.models.${key}.${field}`);
      }
    }
  }

  for (const [idx, agent] of arrayify(config?.agents?.list).entries()) {
    const id = agent?.id || agent?.name || idx;
    add(agent?.model, `agents.list[${id}].model`);
    add(agent?.model?.primary, `agents.list[${id}].model.primary`);
    for (const ref of arrayify(agent?.model?.fallbacks)) add(ref, `agents.list[${id}].model.fallbacks`);
    add(agent?.subagents?.model, `agents.list[${id}].subagents.model`);
    const agentModels = agent?.models;
    if (Array.isArray(agentModels)) for (const value of agentModels) {
      if (typeof value === 'string') add(value, `agents.list[${id}].models[]`);
      else if (value && typeof value === 'object') add(value.ref || value.model || value.id || value.name, `agents.list[${id}].models[]`, pickModelMeta(value));
    } else if (agentModels && typeof agentModels === 'object') for (const [key, value] of Object.entries(agentModels)) add(key, `agents.list[${id}].models`, pickModelMeta(value));
  }

  const providers = config?.models?.providers || {};
  for (const [providerId, provider] of Object.entries(providers)) {
    const providerMeta = pickModelMeta(provider);
    const models = provider?.models;
    if (Array.isArray(models)) {
      for (const model of models) {
        if (typeof model === 'string') add(joinProvider(providerId, model), `models.providers.${providerId}.models[]`, providerMeta);
        else if (model && typeof model === 'object') {
          const modelId = model.id || model.name || model.model || model.modelId;
          add(joinProvider(providerId, modelId), `models.providers.${providerId}.models[].${modelId || 'unknown'}`, { ...providerMeta, ...pickModelMeta(model) });
        }
      }
    } else if (models && typeof models === 'object') {
      for (const [modelId, modelCfg] of Object.entries(models)) {
        add(joinProvider(providerId, modelId), `models.providers.${providerId}.models.${modelId}`, { ...providerMeta, ...pickModelMeta(modelCfg) });
      }
    }
    walk(provider, (value, pointer) => { if (typeof value === 'string' && value.includes('/')) add(value, `models.providers.${providerId}.${pointer}`); });
  }
  const models = [...found.values()].sort((a,b)=>a.ref.localeCompare(b.ref));
  return { version: 2, source: path.resolve(configPath), generatedAt: new Date().toISOString(), count: models.length, models, groupedByProvider: groupByProvider(models) };
}

export function discoverLiveModels() {
  try {
    const raw = execFileSync('openclaw', ['models','list','--json'], { encoding: 'utf8', stdio: ['ignore','pipe','ignore'], timeout: 15000 });
    const parsed = JSON.parse(raw);
    const list = Array.isArray(parsed) ? parsed : (parsed.models || parsed.items || []);
    return list.map((m) => {
      const ref = normalizeRef(m.ref || m.id || m.model || (m.provider && m.name ? `${m.provider}/${m.name}` : null));
      if (!ref) return null;
      return { ref, provider: providerOf(ref), source: 'openclaw models list --json', live: true, authenticated: m.authenticated ?? m.available ?? m.enabled ?? true, meta: pickModelMeta(m) };
    }).filter(Boolean);
  } catch { return []; }
}

export function mergeDiscoveries(configured, live) {
  const map = new Map();
  for (const m of configured.models || []) map.set(m.ref, { ...m, live: false, authenticated: undefined });
  for (const m of live || []) {
    const current = map.get(m.ref) || { ref: m.ref, provider: m.provider, sources: [], meta: {} };
    current.live = true;
    current.authenticated = m.authenticated;
    current.sources = [...new Set([...(current.sources || []), m.source])];
    current.meta = { ...(current.meta || {}), ...(m.meta || {}) };
    map.set(m.ref, current);
  }
  const models = [...map.values()].sort((a,b)=>a.ref.localeCompare(b.ref));
  return { version: 2, source: configured.source, generatedAt: new Date().toISOString(), count: models.length, models, groupedByProvider: groupByProvider(models) };
}

export function groupByProvider(models) {
  const groups = {};
  for (const model of models) { groups[model.provider] ||= []; groups[model.provider].push(model.ref); }
  return Object.fromEntries(Object.entries(groups).sort(([a],[b])=>a.localeCompare(b)));
}

export function defaultTierObject() {
  return Object.fromEntries(TIERS.map((t) => [t, { models: [], fallback: tierFallback(t), maxAttempts: t === 'multimodal' ? 1 : 2 }]));
}
export function tierFallback(t) {
  return ({ fast:'balanced', balanced:'strong_reasoning', code:'strong_reasoning', long_context:'strong_reasoning', strong_reasoning:null, creative:'balanced', multimodal:'long_context' })[t] ?? null;
}
export function suggestTiers(refs, discovered = []) {
  const tiers = defaultTierObject();
  const metaByRef = new Map(discovered.map((m)=>[m.ref,m.meta||{}]));
  for (const ref of refs) {
    const lower = ref.toLowerCase(), meta = metaByRef.get(ref) || {};
    const ctx = Number(meta.contextWindow || meta.contextTokens || 0);
    if (/mini|haiku|flash|lite|small|8b|7b|3b/.test(lower)) tiers.fast.models.push(ref);
    if (/sonnet|gpt-5|gpt-4|gemini|qwen|glm|mistral|llama|deepseek|command/.test(lower)) tiers.balanced.models.push(ref);
    if (/coder|code|sonnet|opus|gpt-5|qwen|deepseek|codestral/.test(lower)) tiers.code.models.push(ref);
    if (ctx >= 100000 || /long|1m|200k|128k|sonnet|opus|gemini/.test(lower)) tiers.long_context.models.push(ref);
    if (/opus|reason|o3|o4|gpt-5|sonnet|pro|r1|thinking/.test(lower)) tiers.strong_reasoning.models.push(ref);
    if (/creative|gpt|sonnet|opus|gemini|claude/.test(lower)) tiers.creative.models.push(ref);
    if (meta.supportsVision || /vision|image|multimodal|gpt-4o|gemini/.test(lower)) tiers.multimodal.models.push(ref);
  }
  if (!tiers.balanced.models.length && refs[0]) tiers.balanced.models.push(refs[0]);
  if (!tiers.strong_reasoning.models.length && refs.at(-1)) tiers.strong_reasoning.models.push(refs.at(-1));
  if (!tiers.creative.models.length && tiers.balanced.models[0]) tiers.creative.models.push(tiers.balanced.models[0]);
  return tiers;
}

export function buildAllowlist(selected, discovered = [], existing = null) {
  const ordered = [...new Set(selected.map(normalizeRef).filter(Boolean))].sort();
  const tiers = existing?.tiers || suggestTiers(ordered, discovered);
  for (const t of TIERS) {
    const obj = Array.isArray(tiers[t]) ? { models: tiers[t], fallback: tierFallback(t), maxAttempts: t === 'multimodal' ? 1 : 2 } : (tiers[t] || { models: [], fallback: tierFallback(t), maxAttempts: 2 });
    obj.models = [...new Set((obj.models || []).map(normalizeRef).filter((r)=>ordered.includes(r)))];
    obj.fallback = obj.fallback === undefined ? tierFallback(t) : obj.fallback;
    obj.maxAttempts ||= t === 'multimodal' ? 1 : 2;
    tiers[t] = obj;
  }
  return { version: 3, batonVersion: BATON_VERSION, updatedAt: new Date().toISOString(), allowedModels: ordered, blockedModels: existing?.blockedModels || [], tiers, roles: existing?.roles || defaultRoles(), notes: 'Baton must not explicitly use models outside allowedModels.' };
}
export function defaultRoles() {
  return {
    planner_orchestrator:{preferredTier:'strong_reasoning'}, planner:{preferredTier:'strong_reasoning'}, project_manager:{preferredTier:'balanced'}, synthesiser:{preferredTier:'strong_reasoning'},
    researcher:{preferredTier:'balanced'}, deep_researcher:{preferredTier:'strong_reasoning'}, fact_checker:{preferredTier:'strong_reasoning'}, analyst:{preferredTier:'strong_reasoning'}, domain_expert:{preferredTier:'strong_reasoning'}, document_analyst:{preferredTier:'long_context'}, trend_analyst:{preferredTier:'balanced'}, competitive_analyst:{preferredTier:'balanced'},
    writer:{preferredTier:'creative'}, copywriter:{preferredTier:'creative'}, editor:{preferredTier:'creative'}, proofreader:{preferredTier:'fast'}, creative_director:{preferredTier:'creative'}, scriptwriter:{preferredTier:'creative'}, brand_strategist:{preferredTier:'creative'}, localisation_specialist:{preferredTier:'creative'},
    social_media_manager:{preferredTier:'creative'}, community_manager:{preferredTier:'fast'}, growth_marketer:{preferredTier:'balanced'}, seo_specialist:{preferredTier:'balanced'}, paid_ads_specialist:{preferredTier:'creative'}, email_marketer:{preferredTier:'creative'}, lifecycle_marketer:{preferredTier:'balanced'}, pr_comms_specialist:{preferredTier:'creative'}, influencer_manager:{preferredTier:'balanced'},
    sales_development_rep:{preferredTier:'creative'}, account_manager:{preferredTier:'balanced'}, customer_support_agent:{preferredTier:'balanced'}, cx_analyst:{preferredTier:'balanced'}, knowledge_base_writer:{preferredTier:'creative'},
    product_manager:{preferredTier:'strong_reasoning'}, ux_researcher:{preferredTier:'balanced'}, product_designer:{preferredTier:'creative'}, qa_analyst:{preferredTier:'code'}, technical_writer:{preferredTier:'creative'},
    data_analyst:{preferredTier:'strong_reasoning'}, bi_analyst:{preferredTier:'balanced'}, operations_analyst:{preferredTier:'balanced'}, finance_ops_analyst:{preferredTier:'balanced'}, recruiter:{preferredTier:'creative'}, executive_assistant:{preferredTier:'fast'}, procurement_analyst:{preferredTier:'balanced'},
    tutor:{preferredTier:'balanced'}, instructional_designer:{preferredTier:'creative'}, curriculum_designer:{preferredTier:'strong_reasoning'}, exam_coach:{preferredTier:'balanced'},
    video_producer:{preferredTier:'creative'}, podcast_producer:{preferredTier:'creative'}, art_director:{preferredTier:'multimodal'}, thumbnail_strategist:{preferredTier:'multimodal'}, storyboarder:{preferredTier:'creative'},
    ai_agent:{preferredTier:'strong_reasoning'}, browser_agent:{preferredTier:'strong_reasoning'}, tool_operator:{preferredTier:'code'}, automation_agent:{preferredTier:'code'}, integration_agent:{preferredTier:'code'}, file_clerk:{preferredTier:'fast'},
    implementer:{preferredTier:'code'}, operator:{preferredTier:'strong_reasoning'}, validator:{preferredTier:'strong_reasoning', preferDifferentProviderFrom:'worker'}, compliance_reviewer:{preferredTier:'strong_reasoning'}, security_reviewer:{preferredTier:'strong_reasoning'}, brand_safety_reviewer:{preferredTier:'balanced'}, corrector:{preferredTier:'strong_reasoning'}
  };
}

export function defaultRateLimits() {
  return { version:2, defaults:{ maxConcurrentPerProvider:3, maxConcurrentPerModel:1, cooldownMsAfter429:180000, cooldownMsAfterTimeout:90000, leaseTtlMs:900000, spreadParallelWorkers:true }, providers:{}, models:{} };
}
export function defaultBatonConfig(agentId='main') {
  return { version:3, batonVersion: BATON_VERSION, executionMode:'standard', agentId, delegationPolicy:'always_spawn', plannerRequired:true, plannerRole:'planner_orchestrator', tokenPolicy:'lean', maxParallelChildren:3, collapseRolesWhenRateLimited:true, requireValidatorForDangerousActions:true, preferCrossProviderValidation:true, modelAllowlistPath:'.openclaw/baton/model-allowlist.json', rateLimitsPath:'.openclaw/baton/rate-limits.json' };
}

export function printGrouped(discovered) {
  let i = 1;
  for (const [provider, refs] of Object.entries(discovered.groupedByProvider || {})) {
    console.log(`\n${provider}`);
    for (const ref of refs) {
      const m = discovered.models.find((x)=>x.ref===ref);
      const live = m?.live ? ' live' : '';
      const auth = m?.authenticated === false ? ' unauthenticated' : '';
      console.log(`${String(i++).padStart(2,' ')}. ${ref}${live}${auth}`);
    }
  }
}

/**
 * Config loader — parses config/default.yaml without external dependencies.
 *
 * Supports a simple subset of YAML (key: value, lists, nested objects)
 * sufficient for the CoVe plugin config format.
 */

const fs = require('fs');
const path = require('path');

const DEFAULTS = {
  policy: 'basic',
  max_correction_attempts: 1,
  auto_correct: true,
  log_results_to_dashboard: true,
  model_override: null,
  auto_verify: false,
  knowledge_sources: {
    use_system_memory: true,
    document_paths: [],
    enable_web_search: false,
  },
  // Resolved at load time from env vars — no other module reads process.env
  proxy_key: '',
  proxy_port: 8888,
  model: 'gemini-2.0-flash',
  brave_api_key: null,
  // Direct LLM API mode (no sidecar required)
  // Provider: 'gemini' | 'anthropic' | 'openai' | null (null = use sidecar)
  llm_provider: null,
  llm_api_key: null,
};

/**
 * Minimal YAML parser for simple key-value configs.
 * Handles: strings, numbers, booleans, arrays (inline [...]), nested single-level objects.
 */
function parseSimpleYaml(text) {
  const result = {};
  let currentKey = null;

  for (const rawLine of text.split('\n')) {
    const line = rawLine.replace(/#.*$/, '').trimEnd(); // strip comments
    if (!line.trim()) continue;

    const indent = line.length - line.trimStart().length;

    // Top-level key: value
    const kvMatch = line.match(/^(\w[\w_]*)\s*:\s*(.*)$/);
    if (kvMatch && indent === 0) {
      const [, key, val] = kvMatch;
      if (val.trim()) {
        result[key] = parseValue(val.trim());
        currentKey = null;
      } else {
        // Start of nested object
        currentKey = key;
        result[key] = {};
      }
      continue;
    }

    // Nested key: value (indented)
    if (currentKey && indent > 0) {
      const nestedMatch = line.trim().match(/^(\w[\w_]*)\s*:\s*(.+)$/);
      if (nestedMatch) {
        const [, nKey, nVal] = nestedMatch;
        result[currentKey][nKey] = parseValue(nVal.trim());
      }
    }
  }

  return result;
}

function parseValue(val) {
  if (val === 'true') return true;
  if (val === 'false') return false;
  if (val === 'null' || val === '~') return null;
  if (/^-?\d+$/.test(val)) return parseInt(val, 10);
  if (/^-?\d+\.\d+$/.test(val)) return parseFloat(val);
  // Inline array: ["a", "b"] or ["/path/a", "/path/b"]
  if (val.startsWith('[') && val.endsWith(']')) {
    try { return JSON.parse(val); } catch { /* fall through */ }
    // Try comma-separated unquoted
    return val.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
  }
  // Strip quotes
  if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
    return val.slice(1, -1);
  }
  return val;
}

/**
 * Load config from config/default.yaml, merging with defaults.
 * Looks for config relative to the plugin directory.
 *
 * @returns {object} Merged configuration.
 */
function loadConfig() {
  const configPaths = [
    path.join(__dirname, '..', 'config', 'default.yaml'),
    path.join(__dirname, '..', 'config', 'default.yml'),
    path.join(process.env.HOME || '', '.openclaw', 'cove.yaml'),
  ];

  let fileConfig = {};
  for (const p of configPaths) {
    try {
      if (fs.existsSync(p)) {
        const raw = fs.readFileSync(p, 'utf8');
        fileConfig = parseSimpleYaml(raw);
        break;
      }
    } catch { /* try next */ }
  }

  // Deep merge with defaults
  const merged = {
    ...DEFAULTS,
    ...fileConfig,
    knowledge_sources: {
      ...DEFAULTS.knowledge_sources,
      ...(fileConfig.knowledge_sources || {}),
    },
  };

  // Resolve env vars once — no other module should read process.env
  merged.proxy_key = process.env.SIDECAR_PROXY_KEY || process.env.OPENCLAW_PROXY_KEY || merged.proxy_key || '';
  merged.proxy_port = parseInt(process.env.OPENCLAW_PROXY_PORT || String(merged.proxy_port), 10);
  merged.model = process.env.COVE_MODEL || merged.model_override || merged.model;
  merged.brave_api_key = process.env.BRAVE_API_KEY || resolveBraveKeyFromFile() || merged.brave_api_key || null;

  // Direct LLM provider — auto-detect from available API keys if not explicitly set
  merged.llm_api_key = process.env.COVE_LLM_API_KEY
    || process.env.GEMINI_API_KEY
    || process.env.ANTHROPIC_API_KEY
    || process.env.OPENAI_API_KEY
    || merged.llm_api_key || null;

  if (process.env.COVE_LLM_PROVIDER) {
    merged.llm_provider = process.env.COVE_LLM_PROVIDER;
  } else if (!merged.llm_provider && merged.llm_api_key) {
    // Auto-detect provider from which env var was set
    if (process.env.GEMINI_API_KEY) merged.llm_provider = 'gemini';
    else if (process.env.ANTHROPIC_API_KEY) merged.llm_provider = 'anthropic';
    else if (process.env.OPENAI_API_KEY) merged.llm_provider = 'openai';
  }

  return merged;
}

/**
 * Read Brave API key from the standard OpenClaw file location.
 * @returns {string|null}
 */
function resolveBraveKeyFromFile() {
  try {
    const keyPath = path.join(process.env.HOME || '', '.openclaw', '.brave-api-key');
    return fs.readFileSync(keyPath, 'utf8').trim() || null;
  } catch { return null; }
}

module.exports = { loadConfig, parseSimpleYaml };

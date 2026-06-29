/**
 * Platform auto-detection and adapter resolution.
 * 
 * Three-layer priority:
 *   Layer 1: EVOLVER_PLATFORM env var or evolver-config.json platform (explicit)
 *   Layer 2: Filesystem marker detection (auto)
 *   Layer 3: Detection failure → return diagnostic info for agent self-adaptation
 * 
 * evolver-config.json is the unified override point. Agent or user can write:
 *   {
 *     "platform": "openclaw",          // force platform (optional)
 *     "sessions": { "paths": [...] },  // override session directories
 *     "skills":   { "paths": [...] },  // override skill search paths
 *     "llm": { "apiKey": "...", "baseUrl": "...", "model": "...", "api": "openai-completions" },
 *     "schedule": { "mode": "continuous", "minNewSI": 3 }
 *   }
 * All fields optional. Auto-detection fills gaps.
 */

const os = require('os');
const path = require('path');
const fs = require('fs');

// ─── Config Loader ─────────────────────────────────────────────

let _evolverConfigCache = undefined; // undefined = not loaded, null = loaded but not found

/**
 * Load evolver-config.json from known paths.
 * Cached after first load.
 * 
 * Field requirements:
 *   platform:        string, one of: openclaw | claude-code
 *   sessions.paths:  string[], absolute paths to directories containing .jsonl session files
 *   skills.paths:    string[], absolute paths to directories containing <skillName>/SKILL.md
 *   llm.apiKey:      string, API key for LLM provider
 *   llm.baseUrl:     string, base URL (e.g. https://api.openai.com/v1)
 *   llm.model:       string, model identifier (e.g. gpt-4o, claude-sonnet-4-6)
 *   llm.api:         string, protocol format: "openai-completions" | "anthropic-messages"
 *   schedule.mode:   string, "continuous" | "manual"
 *   schedule.minNewSI: number, minimum new SIs before triggering evolution (default 3)
 * 
 * @returns {object|null}
 */
function loadEvolverConfig() {
  if (_evolverConfigCache !== undefined) return _evolverConfigCache;
  
  const EVOLVER_DIR = path.resolve(__dirname, '..', '..');
  const candidates = [
    process.env.EVOLVER_CONFIG,
    path.join(EVOLVER_DIR, 'evolver-config.json'),
    path.join(os.homedir(), '.evolver', 'config.json'),
  ].filter(Boolean);
  
  for (const p of candidates) {
    if (fs.existsSync(p)) {
      try {
        _evolverConfigCache = JSON.parse(fs.readFileSync(p, 'utf8'));
        _evolverConfigCache._path = p;
        return _evolverConfigCache;
      } catch (e) { console.error(`[platform-detect] Failed to parse evolver-config.json: ${e.message}`); }
    }
  }
  _evolverConfigCache = null;
  return null;
}

const { OpenClawAdapter } = require('../adapters/openclaw');
const { ClaudeCodeAdapter } = require('../adapters/claude-code');

const ADAPTERS = {
  openclaw: OpenClawAdapter,
  'claude-code': ClaudeCodeAdapter,
};

const FINGERPRINTS = [
  {
    platform: 'openclaw',
    markers: [
      '/projects/.openclaw/agents',  // Gongfeng/DevCloud environment
      path.join(os.homedir(), '.openclaw', 'agents'),  // Standard install
    ],
  },
  {
    platform: 'claude-code',
    markers: [
      path.join(os.homedir(), '.claude-internal', 'projects'),
      path.join(os.homedir(), '.claude', 'projects'),
    ],
  },
];

/**
 * Detect current platform and return adapter + session paths.
 * 
 * @param {object} [config] - optional config with { platform: string }
 * @returns {{ platform: string|null, adapter: PlatformAdapter|null, paths: string[], diagnostic?: object }}
 */
function detectPlatform(config = {}) {
  // Merge with evolver-config.json
  const fileConfig = loadEvolverConfig() || {};
  const merged = { ...fileConfig, ...config };
  
  // Layer 1: explicit override
  const explicit = process.env.EVOLVER_PLATFORM || merged.platform;
  if (explicit) {
    const AdapterClass = ADAPTERS[explicit];
    if (!AdapterClass) {
      throw new Error(`Unknown platform: ${explicit}. Available: ${Object.keys(ADAPTERS).join(', ')}`);
    }
    const adapter = new AdapterClass(merged);
    return { platform: explicit, adapter, paths: adapter.detectPaths() };
  }

  // Layer 2: filesystem marker detection
  for (const { platform, markers } of FINGERPRINTS) {
    if (markers.some(m => fs.existsSync(m))) {
      const AdapterClass = ADAPTERS[platform];
      if (!AdapterClass) continue;
      const adapter = new AdapterClass(merged);
      const paths = adapter.detectPaths();
      if (paths.length > 0) {
        return { platform, adapter, paths };
      }
    }
  }

  // Layer 3: detection failed
  return {
    platform: null,
    adapter: null,
    paths: [],
    diagnostic: {
      message: 'Platform auto-detection failed. Set EVOLVER_PLATFORM env var or configure platform in evolver-config.json.',
      hint: 'Supported platforms: ' + Object.keys(ADAPTERS).join(', '),
      checked: FINGERPRINTS.map(f => ({ platform: f.platform, markers: f.markers })),
    },
  };
}

/**
 * Get adapter, with fallback to OpenClaw for backward compatibility.
 * 
 * @param {object} [config]
 * @returns {PlatformAdapter}
 */
function getAdapter(config = {}) {
  const result = detectPlatform(config);
  if (result.adapter) return result.adapter;

  // Fallback: OpenClaw adapter (preserves existing behavior)
  console.error('[evolver] Platform detection failed, falling back to OpenClaw adapter');
  const fileConfig = loadEvolverConfig() || {};
  return new OpenClawAdapter({ ...fileConfig, ...config });
}

module.exports = { detectPlatform, getAdapter, loadEvolverConfig, ADAPTERS };

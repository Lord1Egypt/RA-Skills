import { readFileSync } from "node:fs";
import { config as loadDotenv } from "dotenv";

let _config = null;

/**
 * Initialize configuration. Can only be called once.
 * @param {string} [configFile] - Optional path to a JSON config file.
 *
 * Precedence: .env > inherited shell environment > JSON config file.
 */
export function loadConfig(configFile) {
  if (_config) {
    throw new Error("loadConfig() has already been called");
  }

  // 1. Load JSON config file as base values (if provided)
  let fileConfig = {};
  if (configFile) {
    try {
      fileConfig = JSON.parse(readFileSync(configFile, "utf-8"));
    } catch (err) {
      console.error(`Error: failed to read config file "${configFile}": ${err.message}`);
      process.exit(1);
    }
  }

  // 2. Load .env with override enabled so project-local .env wins over inherited shell env
  const dotenvResult = loadDotenv({ quiet: true, override: true });
  const dotenvParsed = dotenvResult?.parsed || {};

  // 3. Build config — precedence: .env > shell env > JSON config
  _config = {
    apiBase: dotenvParsed.OPENAI_API_BASE || process.env.OPENAI_API_BASE || fileConfig.apiBase,
    apiKey: dotenvParsed.OPENAI_API_KEY || process.env.OPENAI_API_KEY || fileConfig.apiKey,
    model: dotenvParsed.OPENAI_API_MODEL || process.env.OPENAI_API_MODEL || fileConfig.model || "gpt-4o",
    npmRegistryUrl: dotenvParsed.NPM_REGISTRY_URL || process.env.NPM_REGISTRY_URL || fileConfig.npmRegistryUrl || "https://registry.npmjs.org",
    pypiIndexUrl: dotenvParsed.PYPI_INDEX_URL || process.env.PYPI_INDEX_URL || fileConfig.pypiIndexUrl || "https://pypi.org",
  };

  if (!_config.apiBase || !_config.apiKey) {
    console.error("Error: apiBase (OPENAI_API_BASE) and apiKey (OPENAI_API_KEY) must be configured via environment variables, .env, or config file");
    process.exit(1);
  }

  return _config;
}

/**
 * Return the loaded config. If loadConfig() hasn't been called yet,
 * auto-initialize from environment variables.
 */
export function getConfig() {
  if (!_config) {
    loadConfig();
  }
  return _config;
}

/**
 * Build the model descriptor object required by pi-agent-core.
 */
export function getModelConfig() {
  const cfg = getConfig();
  return {
    id: cfg.model,
    name: cfg.model,
    api: "openai-completions",
    provider: "openai",
    baseUrl: cfg.apiBase,
    temperature: 0,
    reasoning: false,
    input: ["text"],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128000,
    maxTokens: 8192,
    compat: {
      supportsStore: false,
      supportsDeveloperRole: false,
      supportsReasoningEffort: false,
      supportsStrictMode: false,
    },
  };
}

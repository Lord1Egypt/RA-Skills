// Creativault Open API client module
// Shared authentication, request, error handling, and retry logic

import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_META = loadSkillMeta();

const API_BASE = (process.env.CV_API_BASE_URL || '').replace(/\/+$/, '');
const API_KEY = process.env.CV_API_KEY;
const USER_IDENTITY = process.env.CV_USER_IDENTITY || '';

const MAX_RETRIES = 3;
const DEFAULT_RETRY_AFTER = 60;

function loadSkillMeta() {
  try {
    return JSON.parse(readFileSync(new URL('../skill.json', import.meta.url), 'utf8'));
  } catch {
    const fallback = {
      name: 'creator-scraper-cv',
      version: 'unknown',
      channel: 'stable',
    };
    try {
      const skillMd = readFileSync(new URL('../SKILL.md', import.meta.url), 'utf8');
      const versionMatch = skillMd.match(/version:\s*"?([^"\n]+)"?/);
      if (versionMatch?.[1]) {
        fallback.version = versionMatch[1].trim();
      }
    } catch {
      // Keep default fallback metadata.
    }
    return {
      ...fallback,
    };
  }
}

if (!API_BASE) {
  console.error(JSON.stringify({
    error: 'API base URL is not configured',
    hint: 'Set CV_API_BASE_URL environment variable, or configure "api_base_url" in skill.json',
    example: 'export CV_API_BASE_URL=https://your-api-host.com',
  }));
  process.exit(1);
}

if (!API_KEY) {
  console.error(JSON.stringify({
    error: 'CV_API_KEY environment variable is not set',
    hint: 'Set it via: export CV_API_KEY=cv_live_your_key_here',
  }));
  process.exit(1);
}

function ensureUserIdentity() {
  if (!USER_IDENTITY) {
    console.error(JSON.stringify({
      error: 'CV_USER_IDENTITY environment variable is not set',
      hint: 'Most API endpoints require user identity. Set it via: export CV_USER_IDENTITY=your_email@example.com',
      note: 'This should be the email associated with your API Key account.',
    }));
    process.exit(1);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Call Creativault Open API with auto-retry on 429
 * @param {string} path - API path, e.g. /openapi/v1/creators/tiktok/search
 * @param {object} body - Request body
 * @param {string} platform - Platform name for preprocessing (optional)
 * @returns {Promise<object>} Full response (success, data, error, meta)
 */
export async function callAPI(path, body = {}, platform = null, options = {}) {
  // Preprocess industry parameters if platform is provided
  let processedBody = body;
  if (platform) {
    processedBody = await preprocessIndustryParams(platform, body);
  }
  
  const url = `${API_BASE}${path}`;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    let response;
    try {
      if (!options.skipUserIdentity) {
        ensureUserIdentity();
      }
      const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
        'X-CV-Skill-Name': SKILL_META.name || 'creator-scraper-cv',
        'X-CV-Skill-Version': SKILL_META.version || 'unknown',
        'X-CV-Skill-Channel': SKILL_META.channel || 'unknown',
      };
      if (!options.skipUserIdentity) {
        headers['X-User-Identity'] = USER_IDENTITY;
      }
      response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(processedBody),
      });
    } catch (err) {
      console.error(JSON.stringify({ error: `Network request failed: ${err.message}`, url }));
      process.exit(1);
    }

    // Auto-retry on 429 rate limit
    if (response.status === 429 && attempt < MAX_RETRIES) {
      const retryAfter = parseInt(response.headers.get('Retry-After') || DEFAULT_RETRY_AFTER, 10);
      console.error(`[retry] Rate limited (429). Waiting ${retryAfter}s before retry ${attempt + 1}/${MAX_RETRIES}...`);
      await sleep(retryAfter * 1000);
      continue;
    }

    let data;
    try {
      data = await response.json();
    } catch {
      console.error(JSON.stringify({ error: `Failed to parse response, HTTP status: ${response.status}`, url }));
      process.exit(1);
    }

    if (!data.success) {
      const errorOutput = {
        error: data.error?.message || 'Request failed',
        code: data.error?.code,
        request_id: data.meta?.request_id,
      };
      if (data.error?.code === 40201) {
        errorOutput.insufficient_credits = true;
        errorOutput.credits_remaining = data.meta?.credits_remaining;
      }
      if (data.error?.code === 42902) {
        errorOutput.daily_quota_exhausted = true;
        errorOutput.daily_quota_remaining = data.meta?.quota_remaining;
      }
      console.error(JSON.stringify(errorOutput, null, 2));
      process.exit(1);
    }

    maybeHandleSkillUpdateMeta(data.meta);
    return data;
  }

  // All retries exhausted
  console.error(JSON.stringify({ error: `Rate limit: max retries (${MAX_RETRIES}) exhausted`, url }));
  process.exit(1);
}

function maybeHandleSkillUpdateMeta(meta = {}) {
  const latestVersion = meta?.skill_latest_version;
  const updateRequired = Boolean(meta?.skill_update_required);
  const updateAvailable = updateRequired || Boolean(meta?.skill_update_available);
  if (!latestVersion && !updateAvailable) {
    return;
  }

  const message = meta?.skill_update_message
    || `creator-scraper-cv has a newer version: current=${SKILL_META.version}, latest=${latestVersion || 'unknown'}`;

  console.error(JSON.stringify({
    skill_update: {
      required: updateRequired,
      current_version: SKILL_META.version,
      latest_version: latestVersion || null,
      min_supported_version: meta?.skill_min_supported_version || null,
      message,
      update_command: 'node scripts/skill_update.mjs --yes',
    },
  }, null, 2));

  if (process.env.CV_SKILL_AUTO_UPDATE === 'true') {
    const result = spawnSync(process.execPath, [join(SCRIPT_DIR, 'skill_update.mjs'), '--yes'], {
      encoding: 'utf8',
      stdio: 'inherit',
    });
    if (result.status !== 0) {
      console.error(JSON.stringify({
        skill_update_error: 'Auto update failed. Please run node scripts/skill_update.mjs --yes manually.',
        exit_code: result.status,
      }));
    }
  }
}

/**
 * Parse command-line JSON argument
 * @returns {object} Parsed parameters
 */
export function parseArgs() {
  const raw = process.argv[2];
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    console.error(JSON.stringify({ error: 'Argument must be a valid JSON string', received: raw }));
    process.exit(1);
  }
}

/**
 * Validate required parameters
 * @param {object} params
 * @param {string[]} required
 */
export function validateRequired(params, required) {
  const missing = required.filter(key => params[key] === undefined || params[key] === null);
  if (missing.length > 0) {
    console.error(JSON.stringify({ error: `Missing required parameters: ${missing.join(', ')}` }));
    process.exit(1);
  }
}

const VALID_PLATFORMS = ['tiktok', 'youtube', 'instagram'];

/**
 * Validate platform parameter
 * @param {string} platform
 */
export function validatePlatform(platform) {
  if (!platform || !VALID_PLATFORMS.includes(platform)) {
    console.error(JSON.stringify({ error: `platform must be one of: ${VALID_PLATFORMS.join(' / ')}`, received: platform }));
    process.exit(1);
  }
}

/**
 * Preprocess industry category parameters based on platform
 * @param {string} platform - Platform name (tiktok/youtube/instagram)
 * @param {object} params - Request parameters
 * @returns {Promise<object>} Processed parameters
 */
export async function preprocessIndustryParams(platform, params) {
  // Import industry mapper functions dynamically
  const { convertToLeafIds, suggestIndustryMatches } = await import('./_industry_mapper.mjs');
  
  const processed = { ...params };
  
  if (processed.industry) {
    const input = processed.industry;
    
    // Convert input to array of level-3 IDs
    const leafIds = convertToLeafIds(input);
    if (leafIds.length > 0) {
      processed.industry = leafIds.join(',');
    } else {
      // Conversion failed — report error instead of silently passing invalid value
      const suggestions = suggestIndustryMatches(input);
      console.error(JSON.stringify({
        error: `Unknown or invalid industry category: "${input}". Every value must be a known category ID or supported name.`,
        hint: 'Use one exact category, a known alias, or choose from the suggested categories below. If the user intent is ambiguous, ask for confirmation before searching.',
        suggestions,
        reference: 'See references/industry-categories.md for full list',
      }));
      process.exit(1);
    }
  }
  
  return processed;
}

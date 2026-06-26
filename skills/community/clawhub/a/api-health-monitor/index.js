const fs = require('fs');
const path = require('path');

const SESSIONS_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE,
  '.openclaw', 'agents', 'main', 'sessions'
);

const ERROR_PATTERNS = [
  { type: 'server_error',  regex: /\[LLM ERROR\]\s*5\d{2}\b/gi },
  { type: 'token_failure', regex: /获取token失败|token[_ ]?(expired|invalid|revoked|fail)/gi },
  { type: 'cooldown',      regex: /(?:rate[_ ]?limit|cooldown|throttl|too many requests|429|All APIs are in cooldown)/gi },
  { type: 'service_busy',  regex: /(?:service[_ ]?busy|overloaded|capacity|"type":"service_busy")/gi },
];

function recentSessionFiles(maxAgeDays = 1) {
  if (!fs.existsSync(SESSIONS_DIR)) return [];
  const cutoff = Date.now() - maxAgeDays * 86400000;
  return fs.readdirSync(SESSIONS_DIR)
    .filter(f => f.endsWith('.jsonl') || f.endsWith('.log') || f.endsWith('.json'))
    .map(f => {
      const full = path.join(SESSIONS_DIR, f);
      const stat = fs.statSync(full);
      return { path: full, mtime: stat.mtimeMs };
    })
    .filter(f => f.mtime >= cutoff)
    .sort((a, b) => b.mtime - a.mtime);
}

async function checkApiHealth(opts = {}) {
  const maxAgeDays = opts.maxAgeDays || 1;
  const files = recentSessionFiles(maxAgeDays);
  const errorMap = {};

  for (const file of files) {
    let content;
    try { content = fs.readFileSync(file.path, 'utf8'); } catch { continue; }
    const lines = content.split('\n');

    for (const line of lines) {
      for (const pat of ERROR_PATTERNS) {
        pat.regex.lastIndex = 0;
        const match = pat.regex.exec(line);
        if (match) {
          const key = pat.type;
          if (!errorMap[key]) {
            errorMap[key] = { type: key, message: match[0].trim(), count: 0, lastSeen: file.path };
          }
          errorMap[key].count++;
          errorMap[key].message = match[0].trim().slice(0, 100);
          errorMap[key].lastSeen = path.basename(file.path);
        }
      }
    }
  }

  const errors = Object.values(errorMap);
  const healthy = errors.length === 0;

  let recommendation = 'All clear — no LLM API errors detected.';
  if (!healthy) {
    const types = errors.map(e => e.type);
    if (types.includes('cooldown'))
      recommendation = 'Rate limiting detected. Consider spacing out requests or switching models.';
    else if (types.includes('server_error'))
      recommendation = 'Server errors found. The upstream API may be degraded — check provider status.';
    else if (types.includes('token_failure'))
      recommendation = 'Token failures detected. Verify API keys and token refresh logic.';
    else if (types.includes('service_busy'))
      recommendation = 'Service busy signals found. The provider may be under heavy load — retry later.';
  }

  return { healthy, errors, recommendation };
}

module.exports = { checkApiHealth };

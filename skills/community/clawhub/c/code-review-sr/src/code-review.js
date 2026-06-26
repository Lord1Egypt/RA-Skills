/**
 * CodeReview — AI-Powered Automated Code Review Assistant
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const _e = process['env'];

const PATTERNS = [
  { name: 'Hardcoded secret', pattern: /(password|secret|key|token)\s*[:=]\s*['"][^'"]{8,}['"]/i, severity: 'high', type: 'security' },
  { name: 'SQL injection risk', pattern: /\$\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE|DROP)/i, severity: 'high', type: 'security' },
  { name: 'eval usage', pattern: /\beval\s*\(/, severity: 'high', type: 'security' },
  { name: 'console.log in production', pattern: /console\.log\(/, severity: 'low', type: 'style' },
  { name: 'TODO/FIXME', pattern: /\/\/\s*(TODO|FIXME|HACK|XXX)/i, severity: 'info', type: 'maintenance' },
  { name: 'Empty catch block', pattern: /catch\s*\([^)]*\)\s*\{\s*\}/, severity: 'medium', type: 'bugs' },
  { name: 'Magic number', pattern: /[^\w]\d{3,}[^\w\d]/, severity: 'low', type: 'style' },
  { name: 'Long line (>120 chars)', pattern: /.{121,}/, severity: 'low', type: 'style' },
  { name: 'Nested callbacks (3+)', pattern: /\){[^}]*\){[^}]*\)/, severity: 'medium', type: 'maintainability' },
];

const DEFAULT_MODEL = 'anthropic/claude-haiku-4-5';
const MAX_CODE_CHARS = 8000;

/**
 * Parse a provider/model string into { provider, model }.
 */
function _parseModel(modelStr) {
  const str = modelStr || DEFAULT_MODEL;
  const slash = str.indexOf('/');
  if (slash === -1) {
    return { provider: 'anthropic', model: str };
  }
  return { provider: str.substring(0, slash).toLowerCase(), model: str.substring(slash + 1) };
}

/**
 * Resolve the API key for a given provider from environment variables.
 */
function _resolveApiKey(provider) {
  switch (provider) {
    case 'anthropic':
      return _e.ANTHROPIC_API_KEY || _e.CLAUDE_API_KEY || null;
    case 'openai':
      return _e.OPENAI_API_KEY || null;
    case 'ollama':
      return null; // Ollama doesn't need an API key
    default:
      return null;
  }
}

/**
 * Build the system prompt for AI code review.
 */
function _buildSystemPrompt() {
  return `You are an expert code reviewer. You analyze source code for bugs, security vulnerabilities, performance issues, style problems, and logic errors.

You MUST respond with valid JSON only — no markdown, no code fences, no explanation outside the JSON.

Your response must be a JSON object with exactly these keys:
- "score": integer 1-10 (10 = perfect, 1 = critical problems)
- "issues": array of objects, each with { "severity": "high"|"medium"|"low"|"info", "line": number or null, "type": "security"|"bugs"|"performance"|"style"|"maintainability"|"logic"|"maintenance", "message": string }
- "suggestions": array of strings with actionable improvement recommendations
- "summary": a concise 1-3 sentence summary of the code quality

Be thorough but practical. Prioritize high-severity issues. Include line numbers when possible.`;
}

/**
 * Build the user prompt including the code and any local findings.
 */
function _buildUserPrompt(filePath, code, localIssues) {
  let localFindingsText = '';
  if (localIssues && localIssues.length > 0) {
    localFindingsText = '\n\nLocal static analysis already detected these issues (incorporate and expand on them):\n';
    for (const issue of localIssues) {
      localFindingsText += `- Line ${issue.line}: [${issue.severity}] ${issue.message}\n`;
    }
  }

  const truncated = code.length > MAX_CODE_CHARS;
  const codeContent = truncated ? code.substring(0, MAX_CODE_CHARS) + '\n\n... [truncated at 8000 chars]' : code;

  return `Review the following code from file "${filePath}":${localFindingsText}

\`\`\`
${codeContent}
\`\`\`

Respond with valid JSON only.`;
}

/**
 * Make an HTTPS/HTTP request and return a promise that resolves with the response body.
 */
function _request(options, body) {
  return new Promise((resolve, reject) => {
    const transport = options.protocol === 'http:' ? http : https;
    delete options.protocol;

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ statusCode: res.statusCode, body: raw });
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${raw.substring(0, 500)}`));
        }
      });
      res.on('error', reject);
    });
    req.on('error', reject);
    req.setTimeout(60000, () => {
      req.destroy();
      reject(new Error('Request timeout (60s)'));
    });
    if (body) req.write(body);
    req.end();
  });
}

/**
 * Call the Anthropic Messages API.
 */
async function _callAnthropic(model, systemPrompt, userPrompt, apiKey) {
  const payload = JSON.stringify({
    model: model,
    max_tokens: 4096,
    system: systemPrompt,
    messages: [
      { role: 'user', content: userPrompt }
    ]
  });

  const res = await _request({
    hostname: 'api.anthropic.com',
    port: 443,
    path: '/v1/messages',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'Content-Length': Buffer.byteLength(payload)
    }
  }, payload);

  const parsed = JSON.parse(res.body);
  if (parsed.content && parsed.content.length > 0) {
    return parsed.content[0].text;
  }
  throw new Error('Unexpected Anthropic response structure');
}

/**
 * Call the OpenAI Chat Completions API.
 */
async function _callOpenAI(model, systemPrompt, userPrompt, apiKey) {
  const payload = JSON.stringify({
    model: model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    max_tokens: 4096,
    temperature: 0.2
  });

  const res = await _request({
    hostname: 'api.openai.com',
    port: 443,
    path: '/v1/chat/completions',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'Content-Length': Buffer.byteLength(payload)
    }
  }, payload);

  const parsed = JSON.parse(res.body);
  if (parsed.choices && parsed.choices.length > 0) {
    return parsed.choices[0].message.content;
  }
  throw new Error('Unexpected OpenAI response structure');
}

/**
 * Call a local Ollama instance.
 */
async function _callOllama(model, systemPrompt, userPrompt) {
  const ollamaHost = _e.OLLAMA_HOST || '127.0.0.1';
  const ollamaPort = parseInt(_e.OLLAMA_PORT || '11434', 10);

  const payload = JSON.stringify({
    model: model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    stream: false,
    options: {
      temperature: 0.2
    }
  });

  const res = await _request({
    protocol: 'http:',
    hostname: ollamaHost,
    port: ollamaPort,
    path: '/api/chat',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  }, payload);

  const parsed = JSON.parse(res.body);
  if (parsed.message && parsed.message.content) {
    return parsed.message.content;
  }
  throw new Error('Unexpected Ollama response structure');
}

/**
 * Route an AI call to the correct provider.
 */
async function _callAI(provider, model, systemPrompt, userPrompt) {
  switch (provider) {
    case 'anthropic': {
      const key = _resolveApiKey('anthropic');
      if (!key) throw new Error('No Anthropic API key found. Set ANTHROPIC_API_KEY or CLAUDE_API_KEY.');
      return _callAnthropic(model, systemPrompt, userPrompt, key);
    }
    case 'openai': {
      const key = _resolveApiKey('openai');
      if (!key) throw new Error('No OpenAI API key found. Set OPENAI_API_KEY.');
      return _callOpenAI(model, systemPrompt, userPrompt, key);
    }
    case 'ollama': {
      return _callOllama(model, systemPrompt, userPrompt);
    }
    default:
      throw new Error(`Unknown provider: "${provider}". Use anthropic/, openai/, or ollama/ prefix.`);
  }
}

/**
 * Parse AI response text into structured JSON.
 * Handles cases where the AI wraps JSON in markdown code fences.
 */
function _parseAIResponse(text) {
  let cleaned = text.trim();

  // Strip markdown code fences if present
  const fenceMatch = cleaned.match(/```(?:json)?\s*\n?([\s\S]*?)\n?\s*```/);
  if (fenceMatch) {
    cleaned = fenceMatch[1].trim();
  }

  // Try to find JSON object boundaries
  const firstBrace = cleaned.indexOf('{');
  const lastBrace = cleaned.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace > firstBrace) {
    cleaned = cleaned.substring(firstBrace, lastBrace + 1);
  }

  const parsed = JSON.parse(cleaned);

  // Validate and normalize structure
  const result = {
    score: typeof parsed.score === 'number' ? Math.min(10, Math.max(1, Math.round(parsed.score))) : 5,
    issues: [],
    suggestions: [],
    summary: typeof parsed.summary === 'string' ? parsed.summary : 'AI review completed.'
  };

  if (Array.isArray(parsed.issues)) {
    result.issues = parsed.issues.map((issue) => ({
      severity: ['high', 'medium', 'low', 'info'].includes(issue.severity) ? issue.severity : 'info',
      line: typeof issue.line === 'number' ? issue.line : null,
      type: typeof issue.type === 'string' ? issue.type : 'general',
      message: typeof issue.message === 'string' ? issue.message : String(issue.message || 'Unknown issue')
    }));
  }

  if (Array.isArray(parsed.suggestions)) {
    result.suggestions = parsed.suggestions.filter((s) => typeof s === 'string');
  }

  return result;
}


class CodeReview {
  /**
   * @param {Object} options
   * @param {string} [options.model] - AI model in "provider/model" format. Default: anthropic/claude-haiku-4-5
   * @param {Array}  [options.patterns] - Custom regex patterns for local pre-pass
   * @param {number} [options.maxLineLength] - Max line length for style check (default 120)
   */
  constructor(options = {}) {
    this.patterns = options.patterns || PATTERNS;
    this.maxLineLength = options.maxLineLength || 120;
    this.modelStr = options.model || null;
  }

  /**
   * Local regex-based review pre-pass.
   * Fast, offline, zero dependencies.
   */
  _localReview(filePath, content) {
    const lines = content.split('\n');
    const issues = [];

    for (let i = 0; i < lines.length; i++) {
      for (const pat of this.patterns) {
        if (pat.pattern.test(lines[i])) {
          issues.push({
            line: i + 1,
            severity: pat.severity,
            type: pat.type,
            message: pat.name,
            snippet: lines[i].trim().substring(0, 80)
          });
        }
      }
    }

    // Function length check
    let funcStart = null;
    for (let i = 0; i < lines.length; i++) {
      if (
        /^\s*(function\s|const\s+\w+\s*=\s*(async\s+)?function|async\s+function\s|[a-zA-Z_]\w*\s*\([^)]*\)\s*\{)/.test(lines[i]) &&
        !/^\s*(if|for|while|switch|catch)\s*\(/.test(lines[i])
      ) {
        funcStart = i;
      }
      if (funcStart !== null && /^\s*\}/.test(lines[i]) && i - funcStart > 50) {
        issues.push({
          line: funcStart + 1,
          severity: 'medium',
          type: 'maintainability',
          message: `Long function (${i - funcStart} lines)`
        });
        funcStart = null;
      }
    }

    const score = Math.max(
      1,
      10 -
        issues.filter((i) => i.severity === 'high').length * 2 -
        issues.filter((i) => i.severity === 'medium').length
    );

    return {
      file: filePath,
      score: Math.min(10, score),
      issues,
      totalIssues: issues.length,
      lines: lines.length
    };
  }

  /**
   * AI-powered code review.
   *
   * Runs the local regex pre-pass first, then sends code + local findings to an AI model
   * for deep analysis. Falls back to local-only results if no model is configured or
   * the API call fails.
   *
   * @param {string} filePath - Path to the file to review
   * @param {Object} [options]
   * @param {string} [options.model] - Override the model for this call
   * @returns {Promise<Object>} Review result with score, issues, suggestions, summary
   */
  async review(filePath, options = {}) {
    const content = fs.readFileSync(filePath, 'utf8');
    const local = this._localReview(filePath, content);
    const modelStr = options.model || this.modelStr;

    // If no model configured, return local results only
    if (!modelStr) {
      return {
        file: filePath,
        score: local.score,
        issues: local.issues,
        suggestions: [],
        summary: `Local static analysis found ${local.totalIssues} issue(s).`,
        totalIssues: local.totalIssues,
        lines: local.lines,
        aiPowered: false,
        model: null
      };
    }

    const { provider, model } = _parseModel(modelStr);

    try {
      const systemPrompt = _buildSystemPrompt();
      const userPrompt = _buildUserPrompt(filePath, content, local.issues);
      const rawResponse = await _callAI(provider, model, systemPrompt, userPrompt);
      const aiResult = _parseAIResponse(rawResponse);

      return {
        file: filePath,
        score: aiResult.score,
        issues: aiResult.issues,
        suggestions: aiResult.suggestions,
        summary: aiResult.summary,
        totalIssues: aiResult.issues.length,
        lines: local.lines,
        aiPowered: true,
        model: modelStr
      };
    } catch (err) {
      // Graceful fallback to local results
      return {
        file: filePath,
        score: local.score,
        issues: local.issues,
        suggestions: [],
        summary: `AI review failed (${err.message}). Showing local static analysis results: ${local.totalIssues} issue(s) found.`,
        totalIssues: local.totalIssues,
        lines: local.lines,
        aiPowered: false,
        model: null,
        error: err.message
      };
    }
  }

  /**
   * Review an entire directory of source files.
   *
   * @param {string} dirPath - Root directory to scan
   * @param {Object} [options]
   * @param {string[]} [options.include] - Glob patterns for files to include
   * @param {string[]} [options.exclude] - Directory/file names to exclude
   * @param {string}   [options.model] - Override the model for all reviews
   * @param {number}   [options.concurrency] - Max parallel AI calls (default 3)
   * @returns {Promise<Object>} Aggregated review results
   */
  async reviewDir(dirPath, options = {}) {
    const include = options.include || ['*.js', '*.ts', '*.py'];
    const exclude = options.exclude || ['node_modules', '.git', 'dist', 'build', 'vendor'];
    const concurrency = options.concurrency || 3;
    const files = [];

    this._walk(dirPath, include, exclude, (file) => files.push(file));

    const results = [];
    // Process files in batches to respect concurrency
    for (let i = 0; i < files.length; i += concurrency) {
      const batch = files.slice(i, i + concurrency);
      const batchResults = await Promise.all(
        batch.map((file) => this.review(file, { model: options.model }))
      );
      results.push(...batchResults);
    }

    const totalIssues = results.reduce((sum, r) => sum + r.totalIssues, 0);
    const avgScore = results.length > 0
      ? Math.round((results.reduce((sum, r) => sum + r.score, 0) / results.length) * 10) / 10
      : 10;
    const aiPowered = results.some((r) => r.aiPowered);

    return {
      directory: dirPath,
      files: results.length,
      totalIssues,
      averageScore: avgScore,
      aiPowered,
      results
    };
  }

  /**
   * Recursively walk a directory tree and invoke callback for matching files.
   */
  _walk(dir, include, exclude, callback) {
    try {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        if (exclude.some((e) => entry.name === e || entry.name.startsWith('.'))) continue;
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          this._walk(full, include, exclude, callback);
        } else if (include.some((p) => entry.name.endsWith(p.replace('*', '')))) {
          callback(full);
        }
      }
    } catch {
      // Silently skip directories we can't read
    }
  }
}

module.exports = { CodeReview };
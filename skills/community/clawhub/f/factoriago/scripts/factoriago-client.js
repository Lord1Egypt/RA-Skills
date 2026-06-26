#!/usr/bin/env node
/**
 * FactoriaGo API Client
 * Usage: node factoriago-client.js <command> [options]
 *
 * Commands:
 *   login <email> <password>
 *   list-projects
 *   get-project <projectId>
 *   list-tasks <projectId>
 *   create-task <projectId> <title> [description]
 *   analyze-review <projectId> <reviewText>
 *   chat <projectId> <message> [model]
 *   compile <projectId>
 *   get-file <projectId> <fileId>
 *   get-llm-config                              # check API key status
 *   set-llm-config <provider> <model> <apiKey>  # save API key
 *
 * Auth: set FACTORIAGO_COOKIE env var with session cookie value
 *       export FACTORIAGO_COOKIE="connect.sid=s%3A..."
 */

const https = require('https');
const BASE = 'editor.factoriago.com';

// ── HTTP helper ─────────────────────────────────────────────────────────────
function req(method, path, body, cookie) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const opts = {
      hostname: BASE,
      path: `/api${path}`,
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(cookie ? { Cookie: cookie } : {}),
        ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}),
      },
    };
    const r = https.request(opts, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        const isHtml = d.trimStart().startsWith('<!DOCTYPE') || d.trimStart().startsWith('<html');
        if (isHtml) {
          // Server returned HTML (SPA fallback or redirect) — treat as auth error
          return resolve({ status: res.statusCode || 401, data: null, isHtml: true });
        }
        try {
          const json = JSON.parse(d);
          const setCookie = res.headers['set-cookie'];
          if (setCookie) json._cookie = setCookie.map(c => c.split(';')[0]).join('; ');
          resolve({ status: res.statusCode, data: json, isHtml: false });
        } catch {
          resolve({ status: res.statusCode, data: d, isHtml: false });
        }
      });
    });
    r.on('error', reject);
    r.setTimeout(15000, () => { r.destroy(); reject(new Error('Request timeout')); });
    if (data) r.write(data);
    r.end();
  });
}

// ── Guard helpers ────────────────────────────────────────────────────────────
function requireAuth(res, cmd) {
  if (res.isHtml || res.status === 401) {
    console.error('❌ Not authenticated. Run: node factoriago-client.js login <email> <password>');
    console.error('   Then: export FACTORIAGO_COOKIE="<cookie value>"');
    return true;
  }
  return false;
}

function checkStatus(res, cmd) {
  if (requireAuth(res, cmd)) return false;
  if (res.status >= 400) {
    const msg = res.data?.error || res.data?.message || JSON.stringify(res.data);
    console.error(`❌ Error ${res.status}: ${msg}`);
    return false;
  }
  if (!Array.isArray(res.data) && res.data === null) {
    console.error('❌ Unexpected empty response');
    return false;
  }
  return true;
}

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  const [,, cmd, ...args] = process.argv;
  const cookie = process.env.FACTORIAGO_COOKIE || '';

  switch (cmd) {

    // ── Auth ────────────────────────────────────────────────────────────────
    case 'login': {
      const [email, password] = args;
      if (!email || !password) return console.error('Usage: login <email> <password>');
      const res = await req('POST', '/auth/login', { email, password });
      if (res.isHtml || !res.data) return console.error('❌ Login failed (server error)');
      if (res.status !== 200) {
        console.error('❌ Login failed:', res.data?.error || res.data);
        return;
      }
      const sessionCookie = res.data._cookie;
      console.log('✅ Login successful');
      console.log(`User: ${res.data.user?.email} | Plan: ${res.data.user?.subscription_tier || 'free'}`);
      console.log('\n── Next step: set your session cookie ──');
      console.log(`export FACTORIAGO_COOKIE="${sessionCookie}"`);
      break;
    }

    // ── Projects ────────────────────────────────────────────────────────────
    case 'list-projects': {
      if (!cookie) return console.error('❌ Not authenticated. Run login first.');
      const res = await req('GET', '/paper/list', null, cookie);
      if (!checkStatus(res, cmd)) return;
      const papers = Array.isArray(res.data) ? res.data : [];
      if (papers.length === 0) return console.log('📁 No projects found.');
      console.log(`📁 ${papers.length} project(s):\n`);
      papers.forEach((p, i) => {
        console.log(`${String(i+1).padStart(2)}. [${p.id}] ${p.title || '(untitled)'}`);
        console.log(`    Status: ${p.status || 'active'} | Created: ${(p.createdAt || p.created_at || '').slice(0,10)}`);
      });
      break;
    }

    case 'get-project': {
      const [id] = args;
      if (!id) return console.error('Usage: get-project <projectId>');
      if (!cookie) return console.error('❌ Not authenticated.');
      const res = await req('GET', `/paper/${id}`, null, cookie);
      if (!checkStatus(res, cmd)) return;
      const p = res.data;
      console.log(`📄 Project: ${p.title || '(untitled)'}`);
      console.log(`   ID: ${p.id} | Status: ${p.status}`);
      console.log(`   Created: ${(p.createdAt || p.created_at || '').slice(0,10)}`);
      break;
    }

    // ── Tasks ────────────────────────────────────────────────────────────────
    case 'list-tasks': {
      const [paperId] = args;
      if (!paperId) return console.error('Usage: list-tasks <projectId>');
      if (!cookie) return console.error('❌ Not authenticated.');
      const res = await req('GET', `/paper/tasks/by-paper/${paperId}`, null, cookie);
      if (!checkStatus(res, cmd)) return;
      const tasks = Array.isArray(res.data) ? res.data : [];
      if (tasks.length === 0) return console.log('📋 No tasks found.');
      console.log(`📋 ${tasks.length} task(s):\n`);
      tasks.forEach((t, i) => {
        const pri = { high: '🔴', medium: '🟡', low: '🟢' }[t.priority] || '⚪';
        console.log(`${String(i+1).padStart(2)}. ${pri} [${t.id}] ${t.title}`);
        if (t.description) console.log(`    ${t.description.slice(0, 120)}`);
      });
      break;
    }

    case 'create-task': {
      const [paperId, filename, reviewersCount = '1'] = args;
      if (!paperId || !filename) return console.error('Usage: create-task <projectId> <mainTexFilename> [reviewersCount]\nExample: create-task abc123 main.tex 2');
      if (!cookie) return console.error('❌ Not authenticated.');
      const res = await req('POST', '/paper/tasks', {
        paper_id: paperId,
        paper_filename: filename,
        reviewers_count: parseInt(reviewersCount) || 1,
      }, cookie);
      if (!checkStatus(res, cmd)) return;
      console.log(`✅ Revision task created: ID=${res.data?.id} | file=${filename} | reviewers=${reviewersCount}`);
      break;
    }

    // ── AI Analysis ──────────────────────────────────────────────────────────
    case 'analyze-review': {
      const [paperId, ...reviewParts] = args;
      if (!paperId) return console.error('Usage: analyze-review <projectId> "<reviewer text>"');
      if (!cookie) return console.error('❌ Not authenticated.');
      const reviewText = reviewParts.join(' ');
      if (!reviewText) return console.error('❌ Please provide the reviewer comment text.');
      console.log('🔍 Submitting reviewer comments for analysis...');
      const res = await req('POST', `/paper/${paperId}/analyze`, { reviewText }, cookie);
      if (!checkStatus(res, cmd)) return;
      console.log('✅ Analysis complete:\n');
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }

    case 'chat': {
      const [paperId, message, model = 'claude-3-5-sonnet-20241022'] = args;
      if (!paperId || !message) return console.error('Usage: chat <projectId> "<message>" [model]');
      if (!cookie) return console.error('❌ Not authenticated.');
      // First check if API key is configured
      const cfgRes = await req('GET', '/settings/llm', null, cookie);
      const cfgData = cfgRes.data?.config || cfgRes.data;
      if (!cfgRes.isHtml && cfgRes.status === 200 && !cfgData?.primary_key_saved) {
        console.error('❌ No LLM API key configured. AI features disabled.');
        console.error('   Run: set-llm-config <provider> <model> <apiKey>');
        console.error('   Or go to: https://factoriago.com → Settings → AI Model');
        return;
      }
      console.log(`💬 Chatting with ${model}...`);
      const res = await req('POST', '/chat', { paperId, messages: [{ role: 'user', content: message }] }, cookie);
      if (!checkStatus(res, cmd)) return;
      console.log('\n🤖 AI Response:\n');
      console.log(res.data?.reply || res.data?.message || JSON.stringify(res.data));
      break;
    }

    // ── LaTeX ────────────────────────────────────────────────────────────────
    case 'compile': {
      const [paperId] = args;
      if (!paperId) return console.error('Usage: compile <projectId>');
      if (!cookie) return console.error('❌ Not authenticated.');
      console.log('⚙️  Compiling LaTeX... (this may take 10-30 seconds)');
      const res = await req('POST', `/paper/${paperId}/files/compile`, {}, cookie);
      if (!checkStatus(res, cmd)) return;
      const result = res.data;
      if (result.success || result.status === 'success') {
        console.log('✅ Compilation successful');
        if (result.pdfUrl) console.log(`   PDF: ${result.pdfUrl}`);
      } else {
        console.log('❌ Compilation failed');
        if (result.errors) console.log(result.errors);
        else console.log(JSON.stringify(result, null, 2));
      }
      break;
    }

    case 'get-file': {
      const [paperId, fileId] = args;
      if (!paperId || !fileId) return console.error('Usage: get-file <projectId> <fileId>');
      if (!cookie) return console.error('❌ Not authenticated.');
      const res = await req('GET', `/paper/${paperId}/files/${fileId}/content`, null, cookie);
      if (!checkStatus(res, cmd)) return;
      console.log(typeof res.data === 'string' ? res.data : JSON.stringify(res.data, null, 2));
      break;
    }

    // ── LLM Settings ─────────────────────────────────────────────────────────
    case 'get-llm-config': {
      if (!cookie) return console.error('❌ Not authenticated. Run login first.');
      const res = await req('GET', '/settings/llm', null, cookie);
      if (!checkStatus(res, cmd)) return;
      const cfg = res.data?.config || res.data;
      console.log('🤖 LLM Configuration:\n');
      console.log(`Primary model:   ${cfg.primary_model || '(not set)'}`);
      console.log(`Primary API key: ${cfg.primary_key_saved ? '✅ Saved' : '❌ NOT SET — AI features disabled!'}`);
      console.log(`Fallback model:  ${cfg.fallback_model || '(none)'}`);
      console.log(`Fallback key:    ${cfg.fallback_key_saved ? '✅ Saved' : '(none)'}`);
      if (!cfg.primary_key_saved) {
        console.log('\n⚠️  No API key configured. AI features will not work.');
        console.log('   Run: set-llm-config <provider> <model> <apiKey>');
        console.log('   Providers: anthropic | openai | google | moonshot | zhipu | minimax');
        console.log('   Example: set-llm-config anthropic claude-3-5-sonnet-20241022 sk-ant-xxx');
      }
      break;
    }

    case 'set-llm-config': {
      const [provider, model, apiKey] = args;
      if (!provider || !model || !apiKey) {
        return console.error(
          'Usage: set-llm-config <provider> <model> <apiKey>\n' +
          'Providers: anthropic | openai | google | moonshot | zhipu | minimax\n' +
          'Examples:\n' +
          '  set-llm-config anthropic claude-3-5-sonnet-20241022 sk-ant-xxx\n' +
          '  set-llm-config openai gpt-4o sk-xxx\n' +
          '  set-llm-config google gemini-2.0-flash AIza...'
        );
      }
      if (!cookie) return console.error('❌ Not authenticated.');
      const res = await req('POST', '/settings/llm', {
        primary_provider: provider,
        primary_model: model,
        primary_api_key: apiKey,
      }, cookie);
      if (!checkStatus(res, cmd)) return;
      console.log(`✅ API key saved for ${provider} / ${model}`);
      console.log('   AI features are now enabled. Test with: chat <projectId> "Hello"');
      break;
    }

    // ── Help ─────────────────────────────────────────────────────────────────
    default:
      console.log(`
FactoriaGo CLI — https://factoriago.com

SETUP (run in order):
  1. login <email> <password>          Login and get session cookie
  2. export FACTORIAGO_COOKIE="..."    Set the cookie
  3. get-llm-config                    Check if API key is configured
  4. set-llm-config <provider> <model> <apiKey>   Save your LLM API key

PROJECTS:
  list-projects
  get-project <id>

TASKS:
  list-tasks <projectId>
  create-task <projectId> <title> [description]

AI FEATURES (requires API key):
  analyze-review <projectId> "<reviewer text>"
  chat <projectId> "<message>" [model]

LATEX:
  compile <projectId>
  get-file <projectId> <fileId>

PROVIDERS: anthropic | openai | google | moonshot | zhipu | minimax
`);
  }
}

main().catch(err => {
  console.error('❌ Fatal error:', err.message);
  process.exit(1);
});

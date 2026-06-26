#!/usr/bin/env node
const { loadClient, expandUrl, authHeaders, fetchJson } = require('./client.js');

function parseArgs(argv) {
  const args = argv.slice(2);
  const cmd = args[0];
  const rest = args.slice(1);
  const opts = { _: [] };
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = rest[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        opts[key] = next;
        i++;
      } else {
        opts[key] = true;
      }
    } else {
      opts._.push(a);
    }
  }
  return { cmd, opts };
}

function readJson(val, label) {
  if (!val) return undefined;
  try {
    return JSON.parse(val);
  } catch {
    throw new Error(`${label} 须为合法 JSON 字符串`);
  }
}

async function main() {
  const { cmd, opts } = parseArgs(process.argv);
  if (!cmd || cmd === 'help' || cmd === '-h') {
    console.log(`用法:
  submit --body '<json>'
  fetch --task-id <id>`);
    process.exit(0);
  }
  const { token, urls } = loadClient();
  const bodyFromOpts = () => {
    if (opts['body-file']) {
      const fs = require('fs');
      return JSON.parse(fs.readFileSync(opts['body-file'], 'utf8'));
    }
    if (opts.body) return readJson(opts.body, '--body');
    throw new Error('需要 --body 或 --body-file');
  };

  if (cmd === 'submit') {
    const url = urls.seedance_content_generation_tasks;
    if (!url) throw new Error('AIZNT_PROXY_URLS 缺少 seedance_content_generation_tasks');
    const body = bodyFromOpts();
    const data = await fetchJson(url, {
      method: 'POST',
      headers: authHeaders(token, { 'Content-Type': 'application/json' }),
      body: JSON.stringify(body),
    });
    console.log(JSON.stringify(data, null, 2));
    return;
  }
  if (cmd === 'fetch') {
    const taskId = opts['task-id'];
    if (!taskId) throw new Error('需要 --task-id');
    const tpl = urls.seedance_content_generation_tasks_fetch;
    if (!tpl) throw new Error('AIZNT_PROXY_URLS 缺少 seedance_content_generation_tasks_fetch');
    const url = expandUrl(tpl, { task_id: taskId });
    const data = await fetchJson(url, { headers: authHeaders(token) });
    console.log(JSON.stringify(data, null, 2));
    return;
  }
  throw new Error(`未知命令: ${cmd}`);
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});

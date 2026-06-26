#!/usr/bin/env node
const { loadClient, authHeaders, fetchJson } = require('./client.js');

function parseArgs(argv) {
  const args = argv.slice(2);
  const rest = args;
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
  return opts;
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
  const opts = parseArgs(process.argv);
  if (opts.help || opts.h) {
    console.log(`用法: node xhs.js [--body '<json>'] [--body-file <path>]
无参数或空对象表示可选字段均为空。`);
    process.exit(0);
  }

  const { token, urls } = loadClient();
  const url = urls.xhs_generate;
  if (!url) throw new Error('AIZNT_PROXY_URLS 缺少 xhs_generate');

  let body = {};
  if (opts['body-file']) {
    const fs = require('fs');
    body = JSON.parse(fs.readFileSync(opts['body-file'], 'utf8'));
  } else if (opts.body) {
    body = readJson(opts.body, '--body');
  }

  const data = await fetchJson(url, {
    method: 'POST',
    headers: authHeaders(token, { 'Content-Type': 'application/json' }),
    body: JSON.stringify(body),
  });
  console.log(JSON.stringify(data, null, 2));
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});

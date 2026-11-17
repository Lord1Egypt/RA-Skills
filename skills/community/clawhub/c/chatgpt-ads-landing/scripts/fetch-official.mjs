#!/usr/bin/env node
/**
 * Dump the current text of OpenAI's official Ads requirements, so claims about
 * "what OpenAI requires" are checked against the source, not memory.
 *
 *   node fetch-official.mjs [--proxy http://<your-proxy>] [--out /tmp/openai-ads-docs]
 *
 * openai.com/policies and help.openai.com sit behind a Cloudflare challenge
 * that blocks curl and headless Chrome, so this opens a *visible* Chrome window
 * for a few seconds per page. developers.openai.com works headless, but one
 * code path keeps it simple. All three refuse mainland-China IPs: use a proxy
 * with an overseas exit.
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { launch, sleep } from './lib/cdp.mjs';

const argv = process.argv.slice(2);
const opt = (n, d) => { const i = argv.indexOf(n); return i === -1 ? d : argv[i + 1]; };
const proxy = opt('--proxy', process.env.https_proxy || process.env.HTTPS_PROXY || null);
const out = opt('--out', '/tmp/openai-ads-docs');

const PAGES = {
  'ad-policies': 'https://openai.com/policies/ad-policies/',
  'crawler-guidance': 'https://help.openai.com/en/articles/20001243-advertiser-guidance-for-allowing-openai-web-crawlers',
  'measurement-pixel': 'https://developers.openai.com/ads/measurement-pixel',
  'supported-events': 'https://developers.openai.com/ads/supported-events',
  'image-tag': 'https://developers.openai.com/ads/image-tag',
  'troubleshooting': 'https://developers.openai.com/ads/troubleshooting',
};

mkdirSync(out, { recursive: true });
const page = await launch({ proxy, headless: false, lang: 'en-US' });
try {
  await page.send('Page.enable');
  for (const [name, url] of Object.entries(PAGES)) {
    await page.send('Page.navigate', { url });
    let text = '';
    for (let i = 0; i < 20; i++) {
      await sleep(1500);
      text = await page.evaluate('document.title + "\\n" + location.href + "\\n\\n" + (document.querySelector("main") || document.body).innerText');
      if (text && text.length > 800 && !/Just a moment|请稍候|Attention Required|Verify you are human/i.test(text.slice(0, 300))) { break; }
    }
    const file = join(out, `${name}.txt`);
    writeFileSync(file, text);
    const updated = (text.match(/Updated:?\s*([^\n]{4,30})/) || [])[1] || '';
    console.log(`${text.length > 800 ? '✔' : '✖'} ${name.padEnd(18)} ${String(text.length).padStart(6)} chars ${updated ? '· updated ' + updated : ''} → ${file}`);
  }
} finally { await page.close(); }

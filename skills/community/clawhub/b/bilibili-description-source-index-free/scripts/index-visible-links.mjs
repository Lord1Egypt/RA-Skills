#!/usr/bin/env node
import fs from 'node:fs';

const args = process.argv.slice(2);
const get = (name) => { const i = args.indexOf(name); return i < 0 ? undefined : args[i + 1]; };
const input = get('--input');
const source = get('--source-url') || 'offline-fixture';
if (!input) throw new Error('Usage: node scripts/index-visible-links.mjs --input page.html [--source-url URL]');
const html = fs.readFileSync(input, 'utf8');
const text = html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
const links = [...html.matchAll(/<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)].map((m) => ({
  source_video: source,
  url: m[1],
  purpose: m[2].replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim() || '未标注',
  access: '未检查（离线解析）',
  evidence: '离线页面资料模拟中的可见链接'
}));
const gaps = links.length ? [] : [{ source_video: source, reason: /登录|login|验证码|风控/i.test(text) ? '简介当前不可见：页面提示需登录或受限' : '简介中未发现可见链接' }];
console.log(JSON.stringify({ items: links, gaps }, null, 2));

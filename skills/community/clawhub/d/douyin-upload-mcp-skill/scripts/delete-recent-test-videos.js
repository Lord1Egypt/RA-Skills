#!/usr/bin/env node
import { ensureBrowser, disconnect } from '../src/browser.js';
import { sleep } from '../src/util.js';

const args = new Set(process.argv.slice(2));
const execute = args.has('--execute');
const includeVid = args.has('--include-vid');

const MANAGE_URL = 'https://creator.douyin.com/creator-micro/content/manage?enter_from=cleanup_tests';
const DATE_RE = /2026年05月(13|14)日/;
const TEST_TITLE_RE = /(?:wx camera \d{10,}(?: run\w+)?|模板稳定测试 r\d+-\d+|养宠不焦虑的秘诀？)/i;
const VID_TITLE_RE = /VID 20260510 224452/i;

function compact(text = '') {
  return text.replace(/\s+/g, ' ').trim();
}

async function listCandidates(page) {
  return page.evaluate(({ includeVid }) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const dateRe = /2026年05月(13|14)日/;
    const testTitleRe = /(?:wx camera \d{10,}(?: run\w+)?|模板稳定测试 r\d+-\d+|养宠不焦虑的秘诀？)/i;
    const vidTitleRe = /VID 20260510 224452/i;

    function scoreNode(node) {
      const text = compact(node?.innerText || '');
      if (!text) return null;
      if (!dateRe.test(text)) return null;
      const titleMatch = text.match(testTitleRe) || (includeVid ? text.match(vidTitleRe) : null);
      if (!titleMatch) return null;
      if (!/删除作品/.test(text)) return null;
      const rect = node.getBoundingClientRect();
      if (rect.width < 200 || rect.height < 40) return null;
      return {
        title: titleMatch[0],
        text,
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        top: Math.round(rect.top + window.scrollY),
        left: Math.round(rect.left + window.scrollX),
      };
    }

    const nodes = [...document.querySelectorAll('div, li, section, article')];
    const raw = [];
    for (const node of nodes) {
      const item = scoreNode(node);
      if (item) raw.push(item);
    }

    raw.sort((a, b) => (a.top - b.top) || (a.height - b.height));
    const deduped = [];
    for (const item of raw) {
      const nested = deduped.find((prev) => prev.title === item.title);
      if (nested) {
        if (item.height < nested.height || (item.height === nested.height && item.top > nested.top)) Object.assign(nested, item);
        continue;
      }
      deduped.push(item);
    }
    return deduped.slice(0, 80);
  }, { includeVid });
}

async function clickDeleteForFirstCandidate(page) {
  return page.evaluate(({ includeVid }) => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const dateRe = /2026年05月(13|14)日/;
    const testTitleRe = /(?:wx camera \d{10,}(?: run\w+)?|模板稳定测试 r\d+-\d+|养宠不焦虑的秘诀？)/i;
    const vidTitleRe = /VID 20260510 224452/i;

    function isCandidateText(text) {
      return dateRe.test(text)
        && /删除作品/.test(text)
        && (testTitleRe.test(text) || (includeVid && vidTitleRe.test(text)));
    }

    const all = [...document.querySelectorAll('div, li, section, article')];
    const candidates = all
      .map((node) => {
        const text = compact(node.innerText || '');
        const rect = node.getBoundingClientRect();
        return { node, text, rect };
      })
      .filter(({ text, rect }) => isCandidateText(text) && rect.width >= 200 && rect.height >= 40)
      .sort((a, b) => (a.rect.top - b.rect.top) || (a.rect.height - b.rect.height));

    const item = candidates[0];
    if (!item) return { ok: false, error: 'no_candidate' };

    const title = (item.text.match(testTitleRe) || item.text.match(vidTitleRe) || [''])[0];
    const deleteEl = [...item.node.querySelectorAll('button, span, div, a')]
      .filter((el) => compact(el.innerText || el.textContent || '') === '删除作品')
      .sort((a, b) => {
        const ar = a.getBoundingClientRect();
        const br = b.getBoundingClientRect();
        return (ar.width * ar.height) - (br.width * br.height);
      })[0];

    if (!deleteEl) return { ok: false, error: 'delete_button_not_found', title, text: item.text.slice(0, 500) };
    deleteEl.scrollIntoView({ block: 'center', inline: 'center' });
    deleteEl.click();
    return { ok: true, title, text: item.text.slice(0, 500) };
  }, { includeVid });
}

async function confirmDelete(page) {
  await sleep(800);
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const text = compact(document.body?.innerText || '');
    const buttons = [...document.querySelectorAll('button, span, div, a')]
      .map((el) => ({ el, label: compact(el.innerText || el.textContent || ''), rect: el.getBoundingClientRect() }))
      .filter(({ label, rect }) => rect.width > 0 && rect.height > 0 && /^(删除|确定|确认|仍要删除)$/.test(label));
    const preferred = buttons.find((b) => /^(删除|仍要删除)$/.test(b.label)) || buttons.find((b) => /^(确定|确认)$/.test(b.label));
    if (!preferred) return { ok: false, error: 'confirm_button_not_found', textSample: text.slice(0, 800) };
    preferred.el.click();
    return { ok: true, clicked: preferred.label, textSample: text.slice(0, 800) };
  });
}

async function main() {
  const { page } = await ensureBrowser();
  try {
    await page.goto(MANAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30_000 });
  } catch {
    // The SPA often keeps network requests open; continue with rendered DOM.
  }
  await sleep(3000);

  const before = await listCandidates(page);
  console.log(JSON.stringify({
    ok: true,
    mode: execute ? 'execute' : 'dry-run',
    includeVid,
    count: before.length,
    candidates: before.map((item) => ({
      title: item.title,
      top: item.top,
      size: `${item.width}x${item.height}`,
      sample: item.text.slice(0, 220),
    })),
  }, null, 2));

  if (!execute) return;

  const deleted = [];
  for (let i = 0; i < 30; i += 1) {
    const current = await listCandidates(page);
    if (current.length === 0) break;

    const click = await clickDeleteForFirstCandidate(page);
    if (!click.ok) {
      console.log(JSON.stringify({ ok: false, step: 'click_delete', detail: click }, null, 2));
      break;
    }

    const confirm = await confirmDelete(page);
    if (!confirm.ok) {
      console.log(JSON.stringify({ ok: false, step: 'confirm_delete', title: click.title, detail: confirm }, null, 2));
      break;
    }

    deleted.push({ title: click.title, confirm: confirm.clicked });
    await sleep(2500);
  }

  const after = await listCandidates(page);
  console.log(JSON.stringify({
    ok: after.length === 0,
    deleted,
    remaining: after.map((item) => ({
      title: item.title,
      sample: item.text.slice(0, 220),
    })),
  }, null, 2));
}

main().catch((err) => {
  console.error(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exitCode = 1;
}).finally(() => {
  disconnect();
});

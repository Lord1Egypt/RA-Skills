#!/usr/bin/env node
import { createDouyinSession, disconnect } from '../src/index.js';
import { sleep } from '../src/util.js';

const MANAGE_URL = 'https://creator.douyin.com/creator-micro/content/manage?enter_from=cleanup_by_title';

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      args._.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function usage() {
  console.error('Usage: node scripts/delete-video-by-title.js --title "精确标题" [--execute]');
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

async function waitForManagePage(page, timeout = 12_000) {
  const deadline = Date.now() + timeout;
  let last = null;
  while (Date.now() < deadline) {
    last = await page.evaluate(() => {
      const text = (document.body?.innerText || '').replace(/\s+/g, ' ').trim();
      return {
        loaded: /作品管理/.test(text) && /删除作品/.test(text),
        textSample: text.slice(0, 800),
      };
    }).catch((err) => ({ loaded: false, error: err.message }));
    if (last.loaded) return { ok: true, last };
    await sleep(500);
  }
  return { ok: false, last };
}

async function findVideoRows(page, title) {
  return page.evaluate((expectedTitle) => {
    const compact = (value = '') => String(value || '').replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const titleText = compact(expectedTitle);
    const nodes = [...document.querySelectorAll('div, li, article, section')];
    const rows = [];

    for (const node of nodes) {
      if (!visible(node)) continue;
      const text = compact(node.innerText || node.textContent || '');
      if (!text.includes(titleText) || !text.includes('删除作品')) continue;
      const rect = node.getBoundingClientRect();
      if (rect.width < 240 || rect.height < 60) continue;

      const titleCount = text.split(titleText).length - 1;
      const deleteCount = text.split('删除作品').length - 1;
      const dateCount = (text.match(/20\d{2}年\d{2}月\d{2}日/g) || []).length;
      rows.push({
        index: rows.length,
        text,
        titleCount,
        deleteCount,
        dateCount,
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        top: Math.round(rect.top + window.scrollY),
        left: Math.round(rect.left + window.scrollX),
      });
    }

    rows.sort((a, b) => {
      const scoreA = (a.titleCount === 1 ? 0 : 1000) + (a.deleteCount === 1 ? 0 : 100) + (a.dateCount === 1 ? 0 : 50) + a.height;
      const scoreB = (b.titleCount === 1 ? 0 : 1000) + (b.deleteCount === 1 ? 0 : 100) + (b.dateCount === 1 ? 0 : 50) + b.height;
      return scoreA - scoreB || a.top - b.top;
    });

    return rows.slice(0, 20).map((row, idx) => ({
      rank: idx,
      titleCount: row.titleCount,
      deleteCount: row.deleteCount,
      dateCount: row.dateCount,
      top: row.top,
      left: row.left,
      width: row.width,
      height: row.height,
      sample: row.text.slice(0, 600),
    }));
  }, title);
}

async function clickDelete(page, title) {
  return page.evaluate((expectedTitle) => {
    const compact = (value = '') => String(value || '').replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const titleText = compact(expectedTitle);
    const nodes = [...document.querySelectorAll('div, li, article, section')];
    const candidates = [];

    for (const node of nodes) {
      if (!visible(node)) continue;
      const text = compact(node.innerText || node.textContent || '');
      if (!text.includes(titleText) || !text.includes('删除作品')) continue;
      const rect = node.getBoundingClientRect();
      if (rect.width < 240 || rect.height < 60) continue;
      const titleCount = text.split(titleText).length - 1;
      const deleteCount = text.split('删除作品').length - 1;
      const dateCount = (text.match(/20\d{2}年\d{2}月\d{2}日/g) || []).length;
      candidates.push({ node, text, rect, titleCount, deleteCount, dateCount });
    }

    candidates.sort((a, b) => {
      const scoreA = (a.titleCount === 1 ? 0 : 1000) + (a.deleteCount === 1 ? 0 : 100) + (a.dateCount === 1 ? 0 : 50) + a.rect.height;
      const scoreB = (b.titleCount === 1 ? 0 : 1000) + (b.deleteCount === 1 ? 0 : 100) + (b.dateCount === 1 ? 0 : 50) + b.rect.height;
      return scoreA - scoreB || a.rect.top - b.rect.top;
    });

    const item = candidates[0];
    if (!item) return { ok: false, error: 'target_row_not_found' };

    const deleteEls = [...item.node.querySelectorAll('button, [role="button"], a, span, div')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          el,
          text: compact(el.innerText || el.textContent || ''),
          area: rect.width * rect.height,
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          top: Math.round(rect.top + window.scrollY),
          left: Math.round(rect.left + window.scrollX),
        };
      })
      .filter((itemInner) => itemInner.text === '删除作品')
      .sort((a, b) => a.area - b.area);

    const target = deleteEls[0];
    if (!target) {
      return {
        ok: false,
        error: 'delete_button_not_found',
        rowSample: item.text.slice(0, 600),
      };
    }

    target.el.scrollIntoView({ block: 'center', inline: 'center' });
    target.el.click();
    return {
      ok: true,
      button: {
        text: target.text,
        width: target.width,
        height: target.height,
        top: target.top,
        left: target.left,
      },
      row: {
        titleCount: item.titleCount,
        deleteCount: item.deleteCount,
        dateCount: item.dateCount,
        width: Math.round(item.rect.width),
        height: Math.round(item.rect.height),
        top: Math.round(item.rect.top + window.scrollY),
        sample: item.text.slice(0, 600),
      },
    };
  }, title);
}

async function confirmDelete(page) {
  await sleep(800);
  return page.evaluate(() => {
    const compact = (value = '') => String(value || '').replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const bodyText = compact(document.body?.innerText || '');
    const hasRemoveDialog = /确定要移除此作品吗|移除此作品/.test(bodyText);
    const buttons = [...document.querySelectorAll('button, [role="button"], a, span, div')]
      .filter(visible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          el,
          label: compact(el.innerText || el.textContent || ''),
          area: rect.width * rect.height,
          width: Math.round(rect.width),
          height: Math.round(rect.height),
        };
      })
      .filter((item) => {
        if (hasRemoveDialog) return /^(确定|确认|删除|仍要删除)$/.test(item.label);
        return /^(确定|确认|删除|仍要删除|删除作品)$/.test(item.label);
      })
      .sort((a, b) => {
        const preferred = (label) => {
          if (hasRemoveDialog && /^(确定|确认)$/.test(label)) return 0;
          if (/^(删除|仍要删除)$/.test(label)) return 1;
          return 2;
        };
        return preferred(a.label) - preferred(b.label) || a.area - b.area;
      });

    const target = buttons[0];
    if (!target) {
      return { ok: false, error: 'confirm_button_not_found', textSample: bodyText.slice(0, 1200) };
    }

    target.el.click();
    return {
      ok: true,
      clicked: target.label,
      textSample: bodyText.slice(0, 1200),
    };
  });
}

async function waitUntilMissing(page, title, timeout = 15_000) {
  const deadline = Date.now() + timeout;
  let lastRows = [];
  while (Date.now() < deadline) {
    await sleep(1000);
    lastRows = await findVideoRows(page, title);
    if (lastRows.length === 0) return { ok: true, rows: [] };
  }
  return { ok: false, rows: lastRows };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const title = String(args.title || '').trim();
  if (!title) {
    usage();
    process.exitCode = 2;
    return;
  }

  const { page } = await createDouyinSession();
  try {
    await page.goto(MANAGE_URL, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
    const loaded = await waitForManagePage(page);
    const rows = await findVideoRows(page, title);
    printJson({
      ok: true,
      mode: args.execute ? 'execute' : 'inspect',
      loaded,
      title,
      found: rows.length > 0,
      rows,
    });

    if (!args.execute || rows.length === 0) return;

    const click = await clickDelete(page, title);
    if (!click.ok) {
      printJson({ ok: false, step: 'click_delete', title, click });
      process.exitCode = 1;
      return;
    }

    const confirm = await confirmDelete(page);
    if (!confirm.ok) {
      printJson({ ok: false, step: 'confirm_delete', title, click, confirm });
      process.exitCode = 1;
      return;
    }

    const missing = await waitUntilMissing(page, title);
    printJson({
      ok: missing.ok,
      deleted: missing.ok,
      title,
      click,
      confirm,
      remainingRows: missing.rows,
    });
    if (!missing.ok) process.exitCode = 1;
  } finally {
    disconnect();
  }
}

main().catch((err) => {
  printJson({ ok: false, error: err.message, stack: err.stack });
  disconnect();
  process.exit(1);
});

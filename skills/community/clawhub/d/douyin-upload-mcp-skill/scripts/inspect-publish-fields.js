#!/usr/bin/env node
import { existsSync } from 'node:fs';
import { createDouyinSession, disconnect } from '../src/index.js';

function usage() {
  console.error(`Usage:
  node scripts/inspect-publish-fields.js [--file /abs/video.mp4] [--fresh] [--timeout 300000]

Notes:
  - Without --file, this scans the current upload/editor page.
  - With --file, it uploads the video to open the full edit page, scans fields, and does NOT publish.
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

async function prepareVideoEditor(ops, filePath, opts = {}) {
  if (!existsSync(filePath)) {
    return { ok: false, error: 'file_not_found', filePath };
  }
  const login = await ops.checkLogin();
  if (!login.loggedIn) {
    return { ok: false, error: 'login_required', login };
  }
  const go = await ops.goUploadPage();
  if (!go.ok) return go;
  if (opts.fresh) {
    await ops.abandonUnpublishedDraft();
  } else {
    const resumed = await ops.resumeUnpublishedDraft();
    if (resumed.ok) return { ok: true, resumedDraft: true };
  }
  const tab = await ops.switchPublishType('video');
  if (!tab.ok) return tab;
  const upload = await ops._clickAndChooseFile(ops.selectors.uploadVideoBtn, [filePath]);
  if (!upload.ok) return upload;

  const timeout = Number(opts.timeout || 300000);
  const start = Date.now();
  let state = null;
  while (Date.now() - start < timeout) {
    state = await ops._getPublishEditState();
    if (state.blocked) return { ok: false, error: state.blocked, state };
    if (state.uploadDone) {
      return { ok: true, uploaded: true, elapsed: Date.now() - start, state };
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  return { ok: false, error: 'upload_timeout', state };
}

async function scanPublishPage(ops) {
  const page = ops.operator.page;
  return page.evaluate(() => {
    const compact = (text = '') => text.replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0
        && rect.height > 0
        && style.display !== 'none'
        && style.visibility !== 'hidden'
        && Number(style.opacity || '1') > 0.01;
    };
    const rectOf = (el) => {
      const rect = el.getBoundingClientRect();
      return {
        x: Math.round(rect.x),
        y: Math.round(rect.y),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      };
    };
    const pathOf = (el) => {
      const parts = [];
      let node = el;
      while (node && node.nodeType === 1 && parts.length < 5) {
        const tag = node.tagName.toLowerCase();
        const id = node.id ? `#${node.id}` : '';
        const cls = String(node.className || '')
          .split(/\s+/)
          .filter(Boolean)
          .slice(0, 2)
          .map((c) => `.${c}`)
          .join('');
        parts.unshift(`${tag}${id}${cls}`);
        node = node.parentElement;
      }
      return parts.join(' > ');
    };
    const labelFor = (el) => {
      const aria = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || '';
      const own = compact(el.innerText || el.textContent || el.value || el.placeholder || '');
      const explicit = el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`) : null;
      const explicitText = compact(explicit?.innerText || '');
      const holder = el.closest('[class*="form"], [class*="item"], [class*="container"], [class*="section"], [class*="field"], li, article, section, div');
      const context = compact(holder?.innerText || '').slice(0, 240);
      return explicitText || aria || el.placeholder || own || context;
    };
    const classifyField = (item) => {
      const t = `${item.label} ${item.placeholder || ''} ${item.text || ''} ${item.context || ''}`;
      const compactText = t.replace(/\s+/g, '');
      const exact = compact(item.text || item.label || '');
      if (exact === '发布') return 'action.publish';
      if (exact === '暂存离开') return 'action.saveDraft';
      if (/^(公开|好友可见|仅自己可见)$/.test(exact) || /谁可以看|公开|好友可见|仅自己可见/.test(t)) return 'settings.visibility';
      if (/^(允许|不允许)$/.test(exact) || /保存权限|允许|不允许/.test(t)) return 'settings.allowSave';
      if (/^(立即发布|定时发布)$/.test(exact) || /发布时间|立即发布|定时发布|定时/.test(t)) return 'settings.publishTime';
      if (/上传视频|上传文件|选择文件|更换视频|重新上传/.test(t) || item.type === 'file') return 'media.videoFile';
      if (/作品标题|标题/.test(t) && item.kind !== 'button') return 'metadata.title';
      if ((/作品描述|作品简介|简介|描述/.test(t) && item.kind !== 'button') || item.kind === 'rich-text') return 'metadata.description';
      if (/添加话题|话题|#/.test(t)) return 'metadata.topics';
      if (/@好友|好友/.test(t)) return 'metadata.mentions';
      if (/设置封面|封面|横封面|竖封面|智能推荐封面|Ai/.test(t)) return 'media.cover';
      if (/合集/.test(t)) return 'metadata.collection';
      if (/自主声明/.test(t)) return 'compliance.declaration';
      if (/添加标签|标签/.test(t)) return 'metadata.tags';
      if (/位置|地理位置/.test(t)) return 'metadata.location';
      if (/关联热点|热点/.test(t)) return 'metadata.hotspot';
      if (/发布暂存离开|暂存/.test(t)) return 'action.saveDraft';
      return 'unknown';
    };

    const items = [];
    const push = (el, kind, extra = {}) => {
      if (!el || !visible(el)) return;
      const label = labelFor(el);
      const item = {
        id: items.length + 1,
        kind,
        field: 'unknown',
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type') || extra.type || '',
        role: el.getAttribute('role') || '',
        label: compact(label).slice(0, 160),
        text: compact(el.innerText || el.textContent || '').slice(0, 160),
        placeholder: el.getAttribute('placeholder') || '',
        value: el.value || '',
        disabled: Boolean(el.disabled || el.getAttribute('aria-disabled') === 'true' || /disabled/i.test(String(el.className || ''))),
        required: Boolean(el.required || /必填|必选/.test(label)),
        rect: rectOf(el),
        selectorHint: pathOf(el),
        context: compact(el.closest('section, article, li, [class*="form"], [class*="item"], [class*="container"], div')?.innerText || '').slice(0, 260),
        ...extra,
      };
      item.field = classifyField(item);
      items.push(item);
    };

    for (const el of document.querySelectorAll('input, textarea, select')) {
      if (el.type === 'file' && !visible(el)) {
        const accept = el.getAttribute('accept') || '';
        const item = {
          id: items.length + 1,
          kind: 'file-input',
          field: 'media.videoFile',
          tag: el.tagName.toLowerCase(),
          type: 'file',
          role: '',
          label: 'hidden file input',
          text: '',
          placeholder: '',
          value: '',
          disabled: Boolean(el.disabled),
          required: false,
          rect: rectOf(el),
          selectorHint: pathOf(el),
          context: compact(el.closest('section, article, li, [class*="upload"], [class*="container"], div')?.innerText || '').slice(0, 260),
          accept,
          multiple: Boolean(el.multiple),
          maxLength: null,
          visible: false,
        };
        items.push(item);
        continue;
      }
      push(el, el.type === 'file' ? 'file-input' : 'input', {
        accept: el.getAttribute('accept') || '',
        multiple: Boolean(el.multiple),
        maxLength: el.maxLength > 0 ? el.maxLength : null,
        visible: true,
      });
    }
    for (const el of document.querySelectorAll('[contenteditable="true"]')) {
      push(el, 'rich-text');
    }
    for (const el of document.querySelectorAll('button, [role="button"], a, [class*="switch"], [class*="radio"], [class*="checkbox"]')) {
      const text = compact(el.innerText || el.textContent || el.getAttribute('aria-label') || '');
      if (!text && !/(switch|radio|checkbox)/i.test(`${el.className || ''} ${el.getAttribute('role') || ''}`)) continue;
      push(el, 'button');
    }
    for (const el of document.querySelectorAll('[role="combobox"], [aria-haspopup="listbox"], [class*="select"], [class*="cascader"], [class*="dropdown"]')) {
      push(el, 'picker');
    }

    const deduped = [];
    const seen = new Set();
    for (const item of items) {
      const key = `${item.kind}:${item.field}:${item.rect.x}:${item.rect.y}:${item.rect.width}:${item.rect.height}:${item.label}:${item.text}`;
      if (seen.has(key)) continue;
      seen.add(key);
      deduped.push(item);
    }

    const knownFields = {};
    for (const item of deduped) {
      if (!knownFields[item.field]) knownFields[item.field] = [];
      knownFields[item.field].push(item.id);
    }

    const text = document.body?.innerText || '';
    return {
      ok: true,
      url: location.href,
      title: document.title,
      pageKind: location.href.includes('/content/post/video') || /基础信息|作品描述|发布设置|预览视频/.test(text)
        ? 'video-editor'
        : (location.href.includes('/content/upload') ? 'upload-home' : 'other'),
      summary: {
        totalControls: deduped.length,
        fileInputs: deduped.filter((i) => i.kind === 'file-input').length,
        inputs: deduped.filter((i) => i.kind === 'input').length,
        richText: deduped.filter((i) => i.kind === 'rich-text').length,
        buttons: deduped.filter((i) => i.kind === 'button').length,
        pickers: deduped.filter((i) => i.kind === 'picker').length,
      },
      knownFields,
      controls: deduped,
      textSample: compact(text).slice(0, 1800),
    };
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }

  const { ops } = await createDouyinSession();
  try {
    let prepare = null;
    if (args.file) {
      prepare = await prepareVideoEditor(ops, args.file, {
        fresh: Boolean(args.fresh),
        timeout: args.timeout,
      });
      if (!prepare.ok) {
        printJson({ ok: false, phase: 'prepare_failed', prepare });
        process.exitCode = 1;
        return;
      }
    }
    const scan = await scanPublishPage(ops);
    printJson({ ok: true, prepare, scan });
  } finally {
    disconnect();
  }
}

main().catch((err) => {
  printJson({ ok: false, error: err.message, stack: err.stack });
  disconnect();
  process.exit(1);
});

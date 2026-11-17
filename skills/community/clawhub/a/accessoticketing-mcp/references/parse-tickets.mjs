#!/usr/bin/env node
// Parse an accesso mobile-ticket page (media-engine.*.accessoticketing.com/tickets/v1/<island>)
// into JSON. Dependency-free: no node_modules required.
//
// Usage:
//   node parse-tickets.mjs <url|file|->  [--terms] [--barcodes <dir>] [--wallet]
//
// The page ships TWO complete renderings of every ticket (a mobile
// `ticket-item-container<N>` grouping and a `desktopTicketGrouping` one) that share
// barcode element ids. We parse only the mobile blocks, which carry every field.

process.stdout.on('error', (e) => {
  if (e.code === 'EPIPE') process.exit(0);
  throw e;
});

import { writeFileSync, readFileSync, mkdirSync, realpathSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const ENTITIES = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
  '#39': "'", '#039': "'", '#x27': "'", '#x2F': '/', '#47': '/',
};

function decodeEntities(s) {
  return s.replace(/&(#x?[0-9a-fA-F]+|[a-zA-Z]+);/g, (m, ent) => {
    if (Object.prototype.hasOwnProperty.call(ENTITIES, ent)) return ENTITIES[ent];
    if (ent[0] === '#') {
      const code = ent[1] === 'x' || ent[1] === 'X'
        ? parseInt(ent.slice(2), 16)
        : parseInt(ent.slice(1), 10);
      return Number.isFinite(code) ? String.fromCodePoint(code) : m;
    }
    return m;
  });
}

function text(html) {
  return decodeEntities(
    String(html)
      .replace(/<br\s*\/?>/gi, ' ')
      .replace(/<[^>]*>/g, ' ')
  ).replace(/\s+/g, ' ').trim();
}

// Return the inner HTML of the first element whose open tag matches `openRe`,
// walking nested same-name tags so we stop at the correct close tag.
function elementInner(html, openRe, tagName = 'div') {
  const m = openRe.exec(html);
  if (!m) return null;
  const start = m.index + m[0].length;
  const open = new RegExp(`<${tagName}\\b`, 'gi');
  const close = new RegExp(`</${tagName}\\s*>`, 'gi');
  let depth = 1;
  let i = start;
  while (depth > 0) {
    open.lastIndex = i;
    close.lastIndex = i;
    const o = open.exec(html);
    const c = close.exec(html);
    if (!c) return html.slice(start);
    if (o && o.index < c.index) { depth++; i = o.index + o[0].length; continue; }
    depth--;
    if (depth === 0) return html.slice(start, c.index);
    i = c.index + c[0].length;
  }
  return null;
}

function byClass(html, cls, tagName = 'div') {
  return elementInner(html, new RegExp(`<${tagName}\\b[^>]*class="[^"]*\\b${cls}\\b[^"]*"[^>]*>`, 'i'), tagName);
}

// Generic label/value harvesting — drift-tolerant: we do not hardcode which
// labels exist, we collect whatever the page renders.
function labelledPairs(html, labelCls, valueCls) {
  const out = {};
  const re = new RegExp(
    `<div\\b[^>]*class="[^"]*\\b${labelCls}\\b[^"]*"[^>]*>([\\s\\S]*?)</div>\\s*` +
    `<div\\b[^>]*class="[^"]*\\b${valueCls}\\b[^"]*"[^>]*>([\\s\\S]*?)</div>`,
    'gi'
  );
  let m;
  while ((m = re.exec(html)) !== null) {
    const label = text(m[1]).replace(/:+$/, '');
    const value = text(m[2]);
    if (label && value && !(label in out)) out[label] = value;
  }
  return out;
}

function camel(label) {
  const parts = label.replace(/[^A-Za-z0-9]+/g, ' ').trim().split(/\s+/);
  if (!parts.length) return null;
  return parts
    .map((p, i) => (i === 0 ? p.toLowerCase() : p[0].toUpperCase() + p.slice(1).toLowerCase()))
    .join('');
}

export function parseTickets(html, opts = {}) {
  const { includeTerms = false, sourceUrl = null } = opts;

  const headerOrder =
    /<(?:span|div)\b[^>]*class="[^"]*\bticketHeader__orderNumber\b[^"]*"[^>]*>([\s\S]*?)<\/(?:span|div)>/i
      .exec(html)?.[1] ?? null;
  const orderLabel = headerOrder ? text(headerOrder) : null;
  const orderNumber = orderLabel ? (orderLabel.match(/([0-9]{4,})/)?.[1] ?? orderLabel) : null;

  const logo = /<img[^>]*class="[^"]*ticketHeader__merchantLogo[^"]*"[^>]*src="([^"]+)"/i.exec(html)?.[1] ?? null;

  let island = null;
  if (sourceUrl) island = /\/tickets\/v1\/([^/?#]+)/.exec(sourceUrl)?.[1] ?? null;
  if (!island && logo) island = /\/assets\/([^/]+)\//.exec(logo)?.[1] ?? null;

  let origin = null;
  let oToken = null;
  if (sourceUrl) {
    try {
      const u = new URL(sourceUrl);
      origin = u.origin;
      oToken = u.searchParams.get('oToken');
    } catch { /* not a URL */ }
  }

  // Bound the mobile grouping so the duplicate desktop rendering never leaks in.
  const desktopAt = html.search(/class="desktopTicketGrouping"/i);
  const scope = desktopAt === -1 ? html : html.slice(0, desktopAt);

  // ticketId only appears in the trailing "Register this ticket" modal section
  // (after the desktop grouping), one hidden input per ticket in ticket order.
  const registrationIds = [...html.matchAll(
    /<input\b[^>]*\b(?:id|name)="ticketId"[^>]*\bvalue="([^"]*)"/gi
  )].map((m) => m[1]);
  const pageOToken = /<input\b[^>]*\b(?:id|name)="oToken"[^>]*\bvalue="([^"]*)"/i.exec(html)?.[1] ?? null;
  const merchantId = /<input\b[^>]*\b(?:id|name)="merchantId"[^>]*\bvalue="([^"]*)"/i.exec(html)?.[1] ?? null;

  const starts = [];
  const boundary = /<div\b[^>]*id="ticket-item-container(\d+)"[^>]*>/gi;
  let b;
  while ((b = boundary.exec(scope)) !== null) starts.push({ idx: Number(b[1]), at: b.index });

  const tickets = starts.map((s, i) => {
    const block = scope.slice(s.at, i + 1 < starts.length ? starts[i + 1].at : scope.length);

    const fields = labelledPairs(block, 'gap-font--overline', 'gap-font--body-2');
    const notes = labelledPairs(block, 'flipTicket__content-heading', 'flipTicket__content');

    const customer = byClass(block, 'ticket__customerName');
    const names = customer
      ? [...customer.matchAll(/<div[^>]*>([\s\S]*?)<\/div>/gi)].map((m) => text(m[1])).filter(Boolean)
      : [];

    const pkgHtml = byClass(block, 'ticket__packageName');
    const barcodeTextHtml = byClass(block, 'ticket__barcodeText');
    const barcodeSrc = /<img[^>]*\bid="barcode\d+"[^>]*src="([^"]+)"/i.exec(block)?.[1] ?? null;
    // Guarded: only trust the positional mapping when the counts line up exactly.
    const ticketId = registrationIds.length === starts.length ? (registrationIds[i] ?? null) : null;

    const t = {
      index: s.idx,
      ticketId,
      packageName: pkgHtml ? text(pkgHtml) : null,
      participant: names[0] ?? null,
      additionalGuests: names.slice(1),
      date: fields.Date ?? null,
      time: fields.Time ?? null,
      barcodeText: barcodeTextHtml ? text(barcodeTextHtml) : null,
      barcodeIsDataUrl: Boolean(barcodeSrc && barcodeSrc.startsWith('data:')),
    };

    // Surface every other label/value pair the page rendered (Guest Number,
    // Web Sales ID, and anything a different merchant adds).
    for (const [label, value] of Object.entries(fields)) {
      if (label === 'Date' || label === 'Time') continue;
      const key = camel(label);
      if (key && !(key in t)) t[key] = value;
    }

    if (notes.Instructions) t.instructions = notes.Instructions;
    for (const [label, value] of Object.entries(notes)) {
      if (label === 'Instructions') continue;
      if (/terms/i.test(label)) { if (includeTerms) t.termsAndConditions = value; continue; }
      const key = camel(label);
      if (key && !(key in t)) t[key] = value;
    }

    const walletToken = oToken || pageOToken;
    if (origin && island && walletToken && ticketId) {
      t.googleWalletUrl = `${origin}/google-wallet/v1/${island}/${walletToken}/${ticketId}`;
    }

    Object.defineProperty(t, '_barcodeSrc', { value: barcodeSrc, enumerable: false });
    return t;
  });

  if (registrationIds.length && registrationIds.length !== starts.length) {
    process.stderr.write(
      `accesso: ${registrationIds.length} ticketId input(s) for ${starts.length} ticket(s) — ` +
      'ticketId/googleWalletUrl omitted rather than guessed.\n'
    );
  }

  const declared = /data-totaltickets="(\d+)"/i.exec(scope)?.[1];
  return {
    orderNumber,
    island,
    merchantId,
    merchantLogo: logo,
    ticketCount: tickets.length,
    declaredTicketCount: declared ? Number(declared) : null,
    tickets,
  };
}

// Never clobber: a barcode is what gets shown at the gate, so a re-run writes
// `name-2.png`, `name-3.png`, … instead of replacing an earlier image. The
// exclusive create ('wx') also refuses to write through a planted symlink.
function writeNew(dir, stem, ext, bytes) {
  for (let n = 1; n <= 1000; n++) {
    const path = join(dir, `${stem}${n === 1 ? '' : `-${n}`}.${ext}`);
    try {
      writeFileSync(path, bytes, { flag: 'wx' });
      return path;
    } catch (e) {
      if (e.code !== 'EEXIST') throw e;
    }
  }
  throw new Error(`accesso: no free file name for ${stem}.${ext} in ${dir}`);
}

export function saveBarcodes(result, dir) {
  mkdirSync(dir, { recursive: true });
  const written = [];
  for (const t of result.tickets) {
    const src = t._barcodeSrc;
    if (!src || !src.startsWith('data:')) continue;
    const comma = src.indexOf(',');
    const meta = src.slice(5, comma);
    if (!/;base64$/i.test(meta)) continue;
    const ext = (meta.split(';')[0].split('/')[1] || 'png').replace(/[^a-z0-9]/gi, '');
    const stem = `ticket-${String(t.index).padStart(2, '0')}-${t.ticketId ?? 'x'}`;
    const path = writeNew(dir, stem, ext, Buffer.from(src.slice(comma + 1), 'base64'));
    t.barcodeFile = path;
    written.push(path);
  }
  return written;
}

async function readSource(src) {
  if (src === '-') {
    const chunks = [];
    for await (const c of process.stdin) chunks.push(c);
    return { html: Buffer.concat(chunks).toString('utf8'), url: null };
  }
  if (/^https?:\/\//i.test(src)) {
    const res = await fetch(src, { redirect: 'follow' });
    if (!res.ok) {
      process.stderr.write(`accesso: HTTP ${res.status} fetching ticket page\n`);
      process.exit(4);
    }
    return { html: await res.text(), url: res.url || src };
  }
  return { html: readFileSync(src, 'utf8'), url: null };
}

// `import.meta.url` is the *resolved* path — Node follows symlinks — while
// `process.argv[1]` is the path as typed. Installing this skill by
// symlinking it into ~/.claude/skills (which is how it is developed) made
// those two disagree, the CLI block never ran, and the tool exited 0 with
// no output and nothing on stderr. Compare realpaths, and build the URL
// with pathToFileURL so a path containing spaces or non-ASCII doesn't miss
// for the same silent reason.
const isMain = (() => {
  const entry = process.argv[1];
  if (!entry) return false;
  try {
    return import.meta.url === pathToFileURL(realpathSync(entry)).href;
  } catch {
    return false;
  }
})();
if (isMain) {
  const argv = process.argv.slice(2);
  const flag = (name) => {
    const i = argv.indexOf(name);
    if (i === -1) return null;
    return argv[i + 1] ?? '';
  };
  const has = (name) => argv.includes(name);
  const positional = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--barcodes' && argv[i - 1] !== '--url');

  const src = positional[0];
  if (!src) {
    process.stderr.write('usage: parse-tickets.mjs <url|file|-> [--terms] [--barcodes <dir>] [--url <original-url>]\n');
    process.exit(64);
  }

  const { html, url } = await readSource(src);
  const sourceUrl = flag('--url') || url || (/^https?:\/\//i.test(src) ? src : null);
  const result = parseTickets(html, { includeTerms: has('--terms'), sourceUrl });

  if (!result.tickets.length) {
    // Verified: accesso answers a bad/expired token with HTTP 200 and this copy,
    // not an error status — so the body is the only signal.
    if (/no tickets available to print/i.test(html)) {
      process.stderr.write(
        'accesso: the link is expired or invalid — accesso returned ' +
        '"no tickets available to print on this order" (HTTP 200). ' +
        'Re-open the most recent confirmation email; these links are single-order and time-limited.\n'
      );
      process.exit(3);
    }
    process.stderr.write(
      'accesso: no tickets found in a page that did not report an invalid order — ' +
      'the page layout may have changed. Re-check the parser against the raw bytes.\n'
    );
    process.exit(3);
  }

  const dir = flag('--barcodes');
  if (dir) {
    const written = saveBarcodes(result, dir);
    process.stderr.write(`accesso: wrote ${written.length} barcode image(s) to ${dir}\n`);
  }

  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

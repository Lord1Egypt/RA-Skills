#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PERSONAL_GMAIL_MAX_BYTES = 25 * 1024 * 1024;
const BLOCKED_EXTENSIONS = new Set([
  '.ade', '.adp', '.apk', '.appx', '.appxbundle', '.bat', '.cab', '.chm', '.cmd', '.com', '.cpl',
  '.diagcab', '.diagcfg', '.diagpkg', '.dll', '.dmg', '.ex', '.ex_', '.exe', '.hta', '.img',
  '.ins', '.iso', '.isp', '.jar', '.jnlp', '.js', '.jse', '.lib', '.lnk', '.mde', '.mjs', '.msc',
  '.msi', '.msix', '.msixbundle', '.msp', '.mst', '.nsh', '.pif', '.ps1', '.scr', '.sct', '.shb',
  '.sys', '.vb', '.vbe', '.vbs', '.vhd', '.vxd', '.wsc', '.wsf', '.wsh', '.xll',
]);
const MACRO_ENABLED_EXTENSIONS = new Set(['.docm', '.dotm', '.xlsm', '.xltm', '.xlam', '.pptm', '.potm', '.ppsm']);

function emitGmailLimitation(reason, details) {
  console.log('LIMITATION_GMAIL_ATTACHMENT');
  console.log(`REASON=${reason}`);
  if (details) console.log(`DETAILS=${details}`);
  console.log('ACTION=Tell the human operator this is a limitation of Gmail attachment sending for cdp-gmail-delivery and ask for another delivery path.');
  process.exit(2);
}

function fileExtension(name) {
  return path.extname(name || '').toLowerCase();
}

function inspectZipEntries(buffer) {
  const entries = [];
  let encrypted = false;
  let offset = 0;

  while (offset + 46 <= buffer.length) {
    if (buffer.readUInt32LE(offset) !== 0x02014b50) {
      offset += 1;
      continue;
    }

    const generalPurposeFlag = buffer.readUInt16LE(offset + 8);
    const fileNameLength = buffer.readUInt16LE(offset + 28);
    const extraLength = buffer.readUInt16LE(offset + 30);
    const commentLength = buffer.readUInt16LE(offset + 32);
    const nameStart = offset + 46;
    const nameEnd = nameStart + fileNameLength;
    if (nameEnd > buffer.length) break;

    const name = buffer.slice(nameStart, nameEnd).toString('utf8');
    entries.push(name);
    if (generalPurposeFlag & 0x1) encrypted = true;

    offset = nameEnd + extraLength + commentLength;
  }

  return { entries, encrypted };
}

function preflightAttachments(files) {
  if (!files.length) return;

  const totalBytes = files.reduce((sum, file) => sum + fs.statSync(file).size, 0);
  if (totalBytes > PERSONAL_GMAIL_MAX_BYTES) {
    emitGmailLimitation('ATTACHMENTS_TOO_LARGE', `total_bytes=${totalBytes}; personal_gmail_limit=${PERSONAL_GMAIL_MAX_BYTES}`);
  }

  for (const file of files) {
    const base = path.basename(file);
    const ext = fileExtension(base);

    if (BLOCKED_EXTENSIONS.has(ext)) {
      emitGmailLimitation('BLOCKED_FILE_TYPE', base);
    }

    if (MACRO_ENABLED_EXTENSIONS.has(ext)) {
      emitGmailLimitation('MACRO_ENABLED_DOCUMENT', base);
    }

    if (ext === '.zip') {
      try {
        const { entries, encrypted } = inspectZipEntries(fs.readFileSync(file));
        if (encrypted) {
          emitGmailLimitation('PASSWORD_PROTECTED_ARCHIVE', base);
        }

        for (const entry of entries) {
          const entryBase = path.basename(entry);
          const entryExt = fileExtension(entryBase);
          if (BLOCKED_EXTENSIONS.has(entryExt)) {
            emitGmailLimitation('ARCHIVE_CONTAINS_BLOCKED_FILE_TYPE', `${base}:${entry}`);
          }
          if (MACRO_ENABLED_EXTENSIONS.has(entryExt) || /(^|\/)vbaProject\.bin$/i.test(entry)) {
            emitGmailLimitation('ARCHIVE_CONTAINS_MACRO_ENABLED_DOCUMENT', `${base}:${entry}`);
          }
        }
      } catch {
        // Best-effort inspection only. If zip parsing fails, leave enforcement to Gmail.
      }
    }
  }
}

function loadPuppeteer() {
  const candidates = [
    process.env.CDP_GMAIL_DELIVERY_PUPPETEER,
    path.join(__dirname, '..', '.runtime', 'pupp-mail', 'node_modules', 'puppeteer-core'),
    path.join(process.cwd(), 'node_modules', 'puppeteer-core'),
    'puppeteer-core',
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch {}
  }

  throw new Error(
    'Unable to load puppeteer-core. Run: bash skills/cdp-gmail-delivery/scripts/install_runtime.sh'
  );
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function getArg(name, fallback = '') {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return fallback;
}

function getArgs(name) {
  const values = [];
  for (let i = 0; i < process.argv.length; i++) {
    if (process.argv[i] === `--${name}` && process.argv[i + 1]) values.push(process.argv[i + 1]);
  }
  return values;
}

(async () => {
  const to = getArg('to');
  const files = getArgs('file');
  const body = getArg('body', files.length ? 'Hi, attached are the requested files.' : 'Hi, this is the requested message.');

  if (!to) throw new Error('Missing --to');
  for (const file of files) {
    if (!fs.existsSync(file)) throw new Error(`File not found: ${file}`);
  }
  preflightAttachments(files);

  const puppeteer = loadPuppeteer();

  const bases = files.map((file) => path.basename(file));
  const textOnlyToken = crypto.randomBytes(4).toString('hex');
  const base = bases.length === 1 ? bases[0] : bases.length > 1 ? `gmail-files-${bases.length}` : `gmail-message-${textOnlyToken}`;
  const stamp = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(0, 12);
  const subject = `${base} ${stamp}`;

  const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
  const page = (await browser.pages())[0] || (await browser.newPage());
  await page.bringToFront();
  await page.goto('https://mail.google.com/mail/u/0/#inbox', { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('body');
  await sleep(1200);

  // close any existing draft first to avoid duplicate attachments/fields
  await page.evaluate(() => {
    const vis = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    };
    const discard = [...document.querySelectorAll('div[role="button"][aria-label*="Discard draft"], div[role="button"][aria-label*="捨棄草稿"], div[role="button"][aria-label*="Discard"]')].find(vis);
    if (discard) discard.click();
  });

  await sleep(800);

  // always open a fresh compose window
  const composeClicked = await page.evaluate(() => {
    const vis = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    };
    const el = [...document.querySelectorAll('div[gh="cm"]')].find(vis) || document.querySelector('div[gh="cm"]');
    if (!el) return false;
    el.click();
    return true;
  });
  if (!composeClicked) throw new Error('Compose button not found');
  await page.waitForSelector('input[aria-label="To recipients"], input[aria-label*="To"]', { timeout: 20000 });

  // fill fields
  const filled = await page.evaluate((to, subject, body) => {
    const vis = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    };

    const dialogs = [...document.querySelectorAll('div[role="dialog"]')];
    const activeDialog = dialogs.find(vis) || dialogs[dialogs.length - 1] || document;

    const toCandidates = [...activeDialog.querySelectorAll('input[aria-label="To recipients"], input[aria-label*="To"]')];
    const subCandidates = [...activeDialog.querySelectorAll('input[name="subjectbox"]')];
    const bodyCandidates = [...activeDialog.querySelectorAll('div[aria-label="Message Body"], div[role="textbox"]')];

    const toEl = toCandidates.find(vis) || toCandidates[toCandidates.length - 1];
    const subEl = subCandidates.find(vis) || subCandidates[subCandidates.length - 1];
    const bodyEl = bodyCandidates.find(vis) || bodyCandidates[bodyCandidates.length - 1];

    if (!toEl || !subEl || !bodyEl) return { ok: false };

    toEl.focus();
    toEl.value = '';
    toEl.dispatchEvent(new Event('input', { bubbles: true }));
    toEl.value = to;
    toEl.dispatchEvent(new Event('input', { bubbles: true }));
    toEl.dispatchEvent(new Event('change', { bubbles: true }));

    subEl.focus();
    subEl.value = '';
    subEl.dispatchEvent(new Event('input', { bubbles: true }));
    subEl.value = subject;
    subEl.dispatchEvent(new Event('input', { bubbles: true }));

    bodyEl.focus();
    bodyEl.innerText = body;
    bodyEl.dispatchEvent(new Event('input', { bubbles: true }));

    return { ok: true };
  }, to, subject, body);

  if (!filled.ok) throw new Error('Unable to fill compose fields');

  await page.keyboard.press('Enter'); // commit recipient chip

  if (files.length) {
    const fileInputs = await page.$$('input[type="file"]');
    if (!fileInputs.length) throw new Error('File input not found');
    let attached = false;
    for (const fi of fileInputs) {
      try {
        await fi.uploadFile(...files);
        attached = true;
        break;
      } catch {}
    }
    if (!attached) throw new Error('Attachment upload failed');
    await sleep(3000);
  }

  // strict validation before send
  const checks = await page.evaluate((to, requestedFiles) => {
    const vis = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    };

    const toEl = [...document.querySelectorAll('input[aria-label="To recipients"], input[aria-label*="To"]')].find(vis);
    const subEl = [...document.querySelectorAll('input[name="subjectbox"]')].find(vis);
    const dialog = [...document.querySelectorAll('div[role="dialog"]')].find(vis) || document.body;
    const text = dialog.innerText || '';

    const recipientTokens = [...dialog.querySelectorAll('span[email], div[email]')].map((e) => (e.getAttribute('email') || '').toLowerCase());
    const toValue = (toEl?.value || '').toLowerCase();

    const toOk = toValue.includes(to.toLowerCase()) || recipientTokens.includes(to.toLowerCase()) || text.toLowerCase().includes(to.toLowerCase());
    const subjectValue = (subEl?.value || '').trim();
    const subjectOk = subjectValue.length > 0;

    const attachmentMatches = requestedFiles.map((name) => ({
      name,
      present: text.includes(name),
    }));
    const attachmentOk = attachmentMatches.every((item) => item.present);

    return { toOk, subjectOk, attachmentOk, attachmentMatches, subjectValue };
  }, to, bases);

  if (!checks.toOk || !checks.subjectOk || !checks.attachmentOk) {
    throw new Error(`Validation failed: ${JSON.stringify(checks)}`);
  }

  const clickedSend = await page.evaluate(() => {
    const vis = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
    };
    const btn = [...document.querySelectorAll('div[role="button"][aria-label^="Send"], div[role="button"][data-tooltip^="Send"], div[role="button"][aria-label^="傳送"]')].find(vis);
    if (!btn) return false;
    btn.click();
    return true;
  });
  if (!clickedSend) throw new Error('Send button not found');

  try {
    await page.waitForFunction(() => /Message sent|已傳送|郵件已傳送/i.test(document.body.innerText), { timeout: 12000 });
  } catch {
    // Toast can be missed on some Gmail UI states. Continue to hard verification in Sent.
  }

  // verify in sent by unique subject
  await page.goto('https://mail.google.com/mail/u/0/#search/in%3Asent%20subject%3A%22' + encodeURIComponent(subject) + '%22', { waitUntil: 'domcontentloaded' });
  await sleep(4000);
  const found = await page.evaluate((subject) => {
    const txt = document.body.innerText || '';
    if (txt.includes(subject)) return true;
    return [...document.querySelectorAll('tr.zA')].some((row) => (row.innerText || '').includes(subject));
  }, subject);
  if (!found) throw new Error('Sent verification failed: subject not found');

  console.log('EMAIL_SENT_OK');
  console.log(`SUBJECT=${subject}`);
  console.log(`TO=${to}`);
  for (const base of bases) console.log(`FILE_NAME=${base}`);

  await browser.disconnect();
})();

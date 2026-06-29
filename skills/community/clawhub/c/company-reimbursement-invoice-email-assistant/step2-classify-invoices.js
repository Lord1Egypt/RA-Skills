#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const EMAILS_FILE = args[0] || (() => {
  const emailsDir = path.join(__dirname, 'scan-results', 'emails');
  const files = fs.readdirSync(emailsDir)
    .filter(f => f.startsWith('emails-') && f.endsWith('.json'))
    .sort();
  if (files.length === 0) throw new Error('Missing email scan JSON. Run step1 first.');
  return path.join(emailsDir, files[files.length - 1]);
})();
const dateTag = args[1] || (EMAILS_FILE.match(/emails-(.+)\.json$/)?.[1] || new Date().toISOString().slice(0, 10));
const OUT_DIR = path.join(__dirname, 'scan-results', 'classified');

function unique(values) {
  return [...new Set((values || []).filter(Boolean))];
}

function normalizeLink(link) {
  return String(link || '').trim().replace(/[\]>\s]+$/, '').replace(/&amp;/g, '&');
}

function extractLinks(email) {
  const text = `${email.bodyText || ''}\n${(email.links || []).join('\n')}`;
  const found = text.match(/https?:\/\/[^\s'"<>]{10,}/g) || [];
  return unique([...(email.links || []), ...found].map(normalizeLink))
    .filter(l => l.startsWith('http'))
    .filter(l => !l.includes('qq.com') && !l.includes('weixin') && !l.includes('baidu.com'));
}

function platformOf(urls) {
  const joined = urls.join('\n').toLowerCase();
  if (joined.includes('nnfp.jss.com.cn') || joined.includes('nuonuo.com') || joined.includes('of1.cn')) return 'nuonuo';
  if (joined.includes('bwfapiao.com') || joined.includes('hnfapiao.com')) return 'baiwang';
  if (joined.includes('meituan.com')) return 'meituan';
  if (joined.includes('chinatax.gov.cn') || joined.includes('etax')) return 'tax-bureau';
  return urls.length ? 'unknown-link-platform' : null;
}

function classifyLink(urls) {
  const lower = urls.map(u => u.toLowerCase());
  const platform = platformOf(urls);
  if (platform === 'nuonuo') return { sourceType: 'link_platform_page', expectedAction: 'resolve_with_platform_adapter', confidence: 0.95 };
  if (lower.some(u => /\.pdf(?:[?#]|$)/.test(u) || /[?&]wjgs=pdf(?:&|$)/i.test(u))) return { sourceType: 'link_direct_pdf', expectedAction: 'download_direct_pdf', confidence: 0.95 };
  if (lower.some(u => /\.ofd(?:[?#]|$)/.test(u) || /[?&]wjgs=ofd(?:&|$)/i.test(u))) return { sourceType: 'link_direct_ofd', expectedAction: 'download_direct_ofd', confidence: 0.9 };
  if (lower.some(u => /\.(png|jpg|jpeg|gif)(?:[?#]|$)/.test(u) || u.includes('qrcode'))) {
    return { sourceType: 'link_qrcode_image', expectedAction: 'manual_or_ocr', confidence: 0.82 };
  }
  return { sourceType: 'link_unknown_page', expectedAction: 'try_generic_resolvers', confidence: 0.6 };
}

function classifyEmail(email) {
  const attachments = email.attachments || [];
  const pdfs = attachments.filter(a => a.type === 'pdf');
  const ofds = attachments.filter(a => a.type === 'ofd');
  const images = attachments.filter(a => a.type === 'image');
  const links = extractLinks(email);
  const knownFields = email.bodyInfo || {};
  let sourceType = 'manual_unknown';
  let expectedAction = 'manual_review';
  let confidence = 0.3;

  if (pdfs.length > 0 && ofds.length > 0) {
    sourceType = 'attachment_pdf_ofd';
    expectedAction = 'download_pdf_prefer_pdf';
    confidence = 0.99;
  } else if (pdfs.length > 0) {
    sourceType = 'attachment_pdf';
    expectedAction = 'download_attachment_pdf';
    confidence = 0.99;
  } else if (ofds.length > 0) {
    sourceType = 'attachment_ofd';
    expectedAction = 'download_ofd_manual_pdf_needed';
    confidence = 0.88;
  } else if (images.length > 0) {
    sourceType = 'attachment_image';
    expectedAction = 'save_image_manual_or_ocr';
    confidence = 0.88;
  } else if (links.length > 0) {
    const linkClass = classifyLink(links);
    sourceType = linkClass.sourceType;
    expectedAction = linkClass.expectedAction;
    confidence = linkClass.confidence;
  } else if (email.status === 'error') {
    sourceType = 'scan_error';
    expectedAction = 'rerun_or_manual_review';
    confidence = 0.5;
  } else {
    sourceType = 'manual_body';
    expectedAction = 'manual_review_no_attachment_no_link';
    confidence = 0.55;
  }

  return {
    uid: email.uid,
    from: email.from || '',
    subject: email.subject || '',
    date: email.date || '',
    status: email.status || '',
    sourceType,
    expectedAction,
    platform: platformOf(links),
    confidence,
    attachments,
    links,
    knownFields,
    bodyText: email.bodyText || '',
  };
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const scanData = JSON.parse(fs.readFileSync(EMAILS_FILE, 'utf8'));
  const records = (scanData.emails || []).map(classifyEmail);
  const byType = {};
  for (const record of records) byType[record.sourceType] = (byType[record.sourceType] || 0) + 1;
  const output = {
    meta: {
      dateTag,
      emailsFile: path.relative(__dirname, EMAILS_FILE),
      generatedAt: new Date().toISOString(),
      contract: 'Every candidate must become an archived PDF, a saved anomaly, or a manual task.',
    },
    stats: { total: records.length, byType },
    records,
  };
  const outFile = path.join(OUT_DIR, `classified-${dateTag}.json`);
  fs.writeFileSync(outFile, JSON.stringify(output, null, 2), 'utf8');
  console.log('Classified invoice candidates: ' + records.length);
  for (const [type, count] of Object.entries(byType)) console.log(`  ${type}: ${count}`);
  console.log('Saved: ' + outFile);
}

main();

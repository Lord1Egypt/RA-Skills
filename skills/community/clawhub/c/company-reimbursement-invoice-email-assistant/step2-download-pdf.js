#!/usr/bin/env node
/**
 * step2-download-pdf.js — 环节② PDF/OFD下载
 * 
 * 输入：step1 的邮件 JSON 文件
 * 输出：下载的 PDF 文件到 scan-results/downloads/
 * 
 * 支持的下载方式：
 * 1. PDF附件（直接从邮件下载 binary）
 * 2. 链接提取：从 bodyText 中提取 PDF/OFD 下载 URL
 * 3. 去重：同一发票号只下载一次
 */

const Imap = require('imap');
const { simpleParser } = require('mailparser');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { spawnSync } = require('child_process');
const { URL } = require('url');
const { getImapConfig, getMailbox } = require('./lib/env');

const args = process.argv.slice(2);

// 配置
const INPUT_FILE = args[0] || (() => {
  const classifiedDir = path.join(__dirname, 'scan-results', 'classified');
  if (fs.existsSync(classifiedDir)) {
    const classified = fs.readdirSync(classifiedDir).filter(f => f.startsWith('classified-') && f.endsWith('.json')).sort();
    if (classified.length > 0) return path.join(classifiedDir, classified[classified.length - 1]);
  }
  const emailsDir = path.join(__dirname, 'scan-results', 'emails');
  const files = fs.readdirSync(emailsDir).filter(f => f.startsWith('emails-') && f.endsWith('.json')).sort();
  if (files.length === 0) throw new Error('未找到扫描结果文件');
  return path.join(emailsDir, files[files.length - 1]);
})();
const dateTag = args[1] || (INPUT_FILE.match(/(?:emails|classified)-(.+)\.json$/)?.[1] || new Date().toISOString().slice(0, 10));
const DOWNLOADS_DIR = path.join(__dirname, 'scan-results', 'downloads');
const STAGING_DIR = path.join(__dirname, 'scan-results', 'staging', dateTag);
const PDF_DIR = path.join(STAGING_DIR, 'pdfs');
const OFD_DIR = path.join(STAGING_DIR, 'ofds');
const IMAGE_DIR = path.join(STAGING_DIR, 'images');
const FAILED_DIR = path.join(STAGING_DIR, 'failed');

const IMAP_CONFIG = getImapConfig();
const MAILBOX = getMailbox();

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function uniquePath(file) {
  if (!fs.existsSync(file)) return file;
  const ext = path.extname(file);
  const base = file.slice(0, -ext.length);
  let index = 2;
  while (fs.existsSync(`${base}-${index}${ext}`)) index++;
  return `${base}-${index}${ext}`;
}

/**
 * 从邮件UID下载附件
 */
function fetchAttachment(imap, uid, filename) {
  return new Promise((resolve, reject) => {
    const fetcher = imap.fetch(uid, { bodies: '', struct: true });
    let foundAttachment = null;
    let settled = false;
    const finish = () => { if (!settled) { settled = true; resolve(foundAttachment); } };
    let pending = 0;

    fetcher.on('message', msg => {
      pending++;
      msg.on('attributes', attrs => { msg.uid = attrs.uid; });
      msg.on('body', stream => {
        const bufs = [];
        stream.on('data', c => bufs.push(c));
        stream.on('end', async () => {
          const fullBody = Buffer.concat(bufs);
          try {
            const parsed = await simpleParser(fullBody);
            const att = (parsed.attachments || []).find(a =>
              a.filename === filename || (filename && a.filename.includes(filename.split('/').pop()))
            );
            if (att) foundAttachment = { filename: att.filename, content: att.content };
          } catch(e) { /* parse failed */ }
          pending--;
          if (pending <= 0) finish();
        });
      });
      msg.on('error', () => { pending--; if (pending <= 0) finish(); });
    });
    fetcher.once('error', () => finish());
    fetcher.once('end', () => setTimeout(() => finish(), 2000));
    setTimeout(() => finish(), 15000); // 超时
  });
}

/**
 * 从 URL 下载文件
 */
function downloadFile(fileUrl, destPath) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(fileUrl);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      family: 4,
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: 20000,
    };
    const req = protocol.request(options, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        // 重定向
        downloadFile(new URL(res.headers.location, fileUrl).href, destPath).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`)); return;
      }
      const bufs = [];
      res.on('data', c => bufs.push(c));
      res.on('end', () => {
        const data = Buffer.concat(bufs);
        fs.writeFileSync(destPath, data);
        resolve(data.length);
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

function fetchUrl(fileUrl, depth = 0) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(fileUrl);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      family: 4,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8',
        'Referer': parsedUrl.origin + '/',
      },
      timeout: 20000,
    };
    const req = protocol.request(options, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location && depth < 5) {
        fetchUrl(new URL(res.headers.location, fileUrl).href, depth + 1).then(resolve).catch(reject);
        return;
      }
      const bufs = [];
      res.on('data', c => bufs.push(c));
      res.on('end', () => resolve({
        url: fileUrl,
        statusCode: res.statusCode,
        headers: res.headers,
        body: Buffer.concat(bufs),
      }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

function postForm(url, data, referer) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    const body = new URLSearchParams(data).toString();
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'POST',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Content-Length': Buffer.byteLength(body),
        'Origin': parsedUrl.origin,
        'Referer': referer || parsedUrl.origin + '/',
      },
      timeout: 20000,
    };
    const req = protocol.request(options, res => {
      const bufs = [];
      res.on('data', c => bufs.push(c));
      res.on('end', () => resolve({
        url,
        statusCode: res.statusCode,
        headers: res.headers,
        body: Buffer.concat(bufs),
      }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(body);
    req.end();
  });
}

function isPdfResponse(response) {
  const contentType = String(response.headers['content-type'] || '').toLowerCase();
  return contentType.includes('application/pdf') || response.body.slice(0, 4).toString('latin1') === '%PDF';
}

function fetchUrlWithCurl(fileUrl, ext) {
  const curl = process.platform === 'win32' ? 'curl.exe' : 'curl';
  const result = spawnSync(curl, [
    '-L',
    '--max-time', '60',
    '-A', 'Mozilla/5.0',
    '-H', ext === '.pdf' ? 'Accept: application/pdf,*/*' : 'Accept: */*',
    fileUrl,
  ], { encoding: 'buffer', maxBuffer: 50 * 1024 * 1024 });
  if (result.status !== 0 || !result.stdout || result.stdout.length === 0) {
    const err = result.stderr ? result.stderr.toString('utf8').trim() : `curl exited ${result.status}`;
    throw new Error(err || 'curl download failed');
  }
  return { url: fileUrl, statusCode: 200, headers: {}, body: result.stdout, resolver: 'curl-direct-download' };
}

async function resolveNuonuoInvoice(finalUrl) {
  const parsedUrl = new URL(finalUrl);
  if (!parsedUrl.hostname.includes('nnfp.jss.com.cn') || !parsedUrl.pathname.includes('/scan-invoice/printQrcode')) {
    return null;
  }
  const paramList = parsedUrl.searchParams.get('paramList');
  if (!paramList) return null;
  const response = await postForm('https://nnfp.jss.com.cn/scan2/getIvcDetailShow.do', {
    paramList,
    code: parsedUrl.searchParams.get('code') || '',
    aliView: parsedUrl.searchParams.get('aliView') || '',
    invoiceDetailMiddleUri: finalUrl,
    shortLinkSource: parsedUrl.searchParams.get('shortLinkSource') || '',
  }, finalUrl);
  if (response.statusCode !== 200) throw new Error(`诺诺接口 HTTP ${response.statusCode}`);
  const payload = JSON.parse(response.body.toString('utf8'));
  const invoice = payload?.data?.invoiceSimpleVo;
  const pdfUrl = invoice?.url;
  const ofdUrl = invoice?.ofdDownloadUrl;
  const targetUrl = pdfUrl || ofdUrl;
  if (!targetUrl) throw new Error('诺诺接口未返回 PDF/OFD 下载地址');
  const file = await fetchUrl(targetUrl);
  if (pdfUrl && isPdfResponse(file)) return { url: targetUrl, body: file.body, ext: '.pdf', resolver: 'nuonuo-api' };
  const fileType = String(file.headers['content-type'] || '').toLowerCase();
  if (ofdUrl && (fileType.includes('application/ofd') || targetUrl.toLowerCase().includes('.ofd'))) {
    return { url: targetUrl, body: file.body, ext: '.ofd', resolver: 'nuonuo-api' };
  }
  if (pdfUrl && file.body.length > 1024) return { url: targetUrl, body: file.body, ext: '.pdf', resolver: 'nuonuo-api' };
  throw new Error('诺诺返回的下载地址不是有效 PDF/OFD');
}

function discoverDownloadLinks(html, baseUrl) {
  const links = [];
  const text = String(html || '');
  const patterns = [
    /(?:href|src)=["']([^"']+\.(?:pdf|ofd)(?:\?[^"']*)?)["']/gi,
    /(https?:\/\/[^\s'"<>]+?\.(?:pdf|ofd)(?:\?[^\s'"<>]*)?)/gi,
    /["']([^"']*(?:download|pdf|ofd)[^"']*)["']/gi,
  ];
  for (const pattern of patterns) {
    for (const match of text.matchAll(pattern)) {
      const raw = match[1].replace(/\\u0026/g, '&').replace(/&amp;/g, '&').trim();
      if (!raw || raw.startsWith('javascript:') || raw.startsWith('#')) continue;
      try {
        const absolute = new URL(raw, baseUrl).href;
        if (!links.includes(absolute)) links.push(absolute);
      } catch (_) {}
    }
  }
  return links;
}

async function resolveInvoiceLink(url) {
  const directPdfLike = /[?&]wjgs=pdf(?:&|$)/i.test(url) || /\.pdf(?:[?#]|$)/i.test(url);
  const directOfdLike = /[?&]wjgs=ofd(?:&|$)/i.test(url) || /\.ofd(?:[?#]|$)/i.test(url);
  let first;
  try {
    first = await fetchUrl(url);
  } catch (e) {
    if (directPdfLike) {
      const file = fetchUrlWithCurl(url, '.pdf');
      return { url: file.url, body: file.body, ext: '.pdf', resolver: 'curl-direct-pdf' };
    }
    if (directOfdLike) {
      const file = fetchUrlWithCurl(url, '.ofd');
      return { url: file.url, body: file.body, ext: '.ofd', resolver: 'curl-direct-ofd' };
    }
    throw e;
  }
  if (isPdfResponse(first) || /[?&]wjgs=pdf(?:&|$)/i.test(first.url)) return { url: first.url, body: first.body, ext: '.pdf', resolver: 'direct-pdf' };
  const nuonuo = await resolveNuonuoInvoice(first.url);
  if (nuonuo) return nuonuo;
  const contentType = String(first.headers['content-type'] || '').toLowerCase();
  if (contentType.includes('application/ofd') || first.url.toLowerCase().includes('.ofd') || /[?&]wjgs=ofd(?:&|$)/i.test(first.url)) {
    return { url: first.url, body: first.body, ext: '.ofd', resolver: 'direct-ofd' };
  }
  const html = first.body.toString('utf8');
  for (const candidate of discoverDownloadLinks(html, first.url).slice(0, 8)) {
    const next = await fetchUrl(candidate);
    if (isPdfResponse(next)) return { url: next.url, body: next.body, ext: '.pdf', resolver: 'html-link-discovery' };
    const nextType = String(next.headers['content-type'] || '').toLowerCase();
    if (nextType.includes('application/ofd') || next.url.toLowerCase().includes('.ofd')) {
      return { url: next.url, body: next.body, ext: '.ofd', resolver: 'html-link-discovery' };
    }
  }
  throw new Error(`未发现可直接下载的 PDF/OFD 链接: HTTP ${first.statusCode}`);
}

/**
 * 从邮件正文中提取发票下载链接
 */
function extractInvoiceLinks(bodyText) {
  const links = [];
  // 百旺金穗云格式：PDF / OFD / XML 链接
  const pdfMatch = bodyText.match(/https?:\/\/[^\s'"<>]+\.pdf\?[^'"<> \n]+/gi) || [];
  const ofdMatch = bodyText.match(/https?:\/\/[^\s'"<>]+\.ofd\?[^'"<> \n]+/gi) || [];
  // 滴滴格式
  const didiMatch = bodyText.match(/https?:\/\/[^\s'"<>]{30,}/g) || [];
  
  return [...pdfMatch, ...ofdMatch, ...didiMatch]
    .map(l => l.trim().replace(/[\]>\s]+$/, ''))
    .filter(l => l.startsWith('http'));
}

function linkPriority(url) {
  const u = String(url || '').toLowerCase();
  if (/[?&]wjgs=pdf(?:&|$)/i.test(u) || /\.pdf(?:[?#]|$)/.test(u)) return 0;
  if (/[?&]wjgs=ofd(?:&|$)/i.test(u) || /\.ofd(?:[?#]|$)/.test(u)) return 1;
  if (u.includes('nnfp.jss.com.cn') || u.includes('of1.cn')) return 2;
  if (u.includes('download') || u.includes('export')) return 3;
  if (/\.(png|jpg|jpeg|gif)(?:[?#]|$)/.test(u) || u.includes('qrcode')) return 9;
  return 5;
}

function prioritizeInvoiceLinks(links) {
  return [...new Set((links || []).map(l => String(l || '').trim().replace(/[\]>\s]+$/, '').replace(/&amp;/g, '&')).filter(Boolean))]
    .sort((a, b) => linkPriority(a) - linkPriority(b));
}

/**
 * 从文件名推断发票号
 */
function guessInvoiceNoFromFilename(filename) {
  const m = filename.match(/(\d{20,})/);
  return m ? m[1] : null;
}

async function main() {
  if (fs.existsSync(STAGING_DIR)) fs.rmSync(STAGING_DIR, { recursive: true, force: true });
  if (!fs.existsSync(DOWNLOADS_DIR)) fs.mkdirSync(DOWNLOADS_DIR, { recursive: true });
  if (!fs.existsSync(PDF_DIR)) fs.mkdirSync(PDF_DIR, { recursive: true });
  if (!fs.existsSync(OFD_DIR)) fs.mkdirSync(OFD_DIR, { recursive: true });
  if (!fs.existsSync(IMAGE_DIR)) fs.mkdirSync(IMAGE_DIR, { recursive: true });
  if (!fs.existsSync(FAILED_DIR)) fs.mkdirSync(FAILED_DIR, { recursive: true });

  const data = JSON.parse(fs.readFileSync(INPUT_FILE, 'utf8'));
  const okEmails = data.records || data.emails || [];
  
  /** 为 error 邮件猜测附件名（仅在 error 状态时回退） */
  function guessAttachments(email) {
    const atts = email.attachments || [];
    if (atts.length > 0) return atts;
    if (email.status !== 'error') return atts;
    // 回退：根据 subject 推断
    const subj = email.subject || '';
    if (subj.includes('电子发票')) return [{ filename: '电子发票.pdf', contentType: 'application/pdf', size: 0, type: 'pdf' }];
    return atts;
  }

  const downloaded = [];
  const skipped = [];
  const failed = [];
  const seenInvoiceNo = new Set();

  // IMAP 连接
  const imap = await new Promise((resolve, reject) => {
    const i = new Imap(IMAP_CONFIG);
    i.once('ready', () => resolve(i));
    i.once('error', reject);
    i.connect();
  });
  imap.openBox(MAILBOX, true, async () => {
    console.log('✅ IMAP已连接，开始下载附件...\n');

    for (const email of okEmails) {
      const uid = email.uid;
      const subject = email.subject || '(无主题)';

      // === 情况1：有PDF附件 ===
      const allAtts = guessAttachments(email);
      const pdfAtts = allAtts.filter(a => a.type === 'pdf') || [];
      const ofdAtts = allAtts.filter(a => a.type === 'ofd') || [];
      const imageAtts = allAtts.filter(a => a.type === 'image') || [];
      
      for (const att of [...pdfAtts, ...ofdAtts, ...imageAtts]) {
        const invoiceNo = guessInvoiceNoFromFilename(att.filename) || `uid${uid}`;
        
        if (seenInvoiceNo.has(invoiceNo + '_' + att.filename)) {
          skipped.push({ uid, type: 'duplicate', filename: att.filename, invoiceNo });
          console.log(`⏭ [${uid}] 跳过重复: ${att.filename}`);
          continue;
        }
        seenInvoiceNo.add(invoiceNo + '_' + att.filename);

        try {
          process.stdout.write(`⏳ [${uid}] 正在下载: ${att.filename} (${(att.size/1024).toFixed(0)}KB)... `);
          const attData = await fetchAttachment(imap, uid, att.filename);
          
          if (!attData || !attData.content || attData.content.length === 0) {
            failed.push({ uid, type: 'empty', filename: att.filename });
            console.log('❌ 空内容');
            continue;
          }

          const destDir = att.type === 'ofd' ? OFD_DIR : (att.type === 'image' ? IMAGE_DIR : PDF_DIR);
          let destPath = path.join(destDir, att.filename);
          // 防止同名文件覆盖：加UID前缀
          if (fs.existsSync(destPath)) {
            const ext = path.extname(att.filename);
            const base = path.basename(att.filename, ext);
            destPath = path.join(destDir, `uid${uid}_${base}${ext}`);
          }
          fs.writeFileSync(destPath, attData.content);
          downloaded.push({ uid, type: att.type, sourceType: email.sourceType || null, filename: path.basename(destPath), originalFilename: att.filename, path: destPath, stagingPath: path.relative(STAGING_DIR, destPath), size: attData.content.length, anomaly: att.type === 'image' ? 'png_anomaly' : null });
          console.log(`✅ ${(attData.content.length/1024).toFixed(0)}KB → ${destPath}`);
        } catch(e) {
          failed.push({ uid, type: 'error', filename: att.filename, error: e.message });
          console.log(`❌ ${e.message}`);
        }
        await sleep(200);
      }

      // === 情况2：无附件但有链接 ===
      if (pdfAtts.length === 0 && ofdAtts.length === 0 && imageAtts.length === 0 && email.links?.length > 0) {
        const links = prioritizeInvoiceLinks([...(email.links || []), ...extractInvoiceLinks(email.bodyText || '')]);
        
        if (links.length > 0) {
          for (const url of links.slice(0, 3)) { // 最多尝试3个候选链接
            const invoiceNo = guessInvoiceNoFromFilename(url) || `uid${uid}`;

            try {
              process.stdout.write(`⏳ [${uid}] 解析链接发票: ${url.slice(0, 80)}... `);
              const resolved = await resolveInvoiceLink(url);
              const ext = resolved.ext || '.pdf';
              const fname = `uid${uid}_${invoiceNo}${ext}`;
              const destDir = ext === '.ofd' ? OFD_DIR : PDF_DIR;
              const destPath = uniquePath(path.join(destDir, fname));
              fs.writeFileSync(destPath, resolved.body);
              const size = resolved.body.length;
              downloaded.push({ uid, type: ext === '.ofd' ? 'ofd' : 'link', sourceType: email.sourceType || null, filename: path.basename(destPath), path: destPath, stagingPath: path.relative(STAGING_DIR, destPath), size, url, resolvedUrl: resolved.url, resolver: resolved.resolver || 'unknown-link-resolver' });
              console.log(`✅ ${(size/1024).toFixed(0)}KB`);
              break;
            } catch(e) {
              failed.push({ uid, type: 'link_error', filename: `uid${uid}_${invoiceNo}`, error: e.message, url });
              console.log(`❌ ${e.message}`);
            }
            await sleep(300);
          }
        }
      }
    }

    imap.end();

    console.log('\n━━━ 下载结果 ━━━');
    console.log('  ✅ 下载成功: ' + downloaded.length);
    console.log('  ⏭  跳过: ' + skipped.length);
    console.log('  ❌ 失败: ' + failed.length);
    
    // 保存下载记录
    const report = { meta: { dateTag, inputFile: INPUT_FILE, stagingDir: STAGING_DIR }, downloaded, skipped, failed, downloadedAt: new Date().toISOString() };
    const reportFile = path.join(DOWNLOADS_DIR, `download-results-${dateTag}.json`);
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2), 'utf8');
    fs.writeFileSync(path.join(DOWNLOADS_DIR, 'download-report.json'), JSON.stringify(report, null, 2), 'utf8');
    console.log('\n报告已保存: ' + reportFile);
  });
}

main().catch(e => { console.error(e); process.exit(1); });

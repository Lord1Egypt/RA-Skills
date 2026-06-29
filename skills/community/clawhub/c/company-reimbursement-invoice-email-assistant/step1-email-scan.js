#!/usr/bin/env node
/**
 * step1-email-scan.js — 环节① 邮件扫描 v2.4（events顺序正确版）
 *
 * 关键发现（from test-uid.js）：
 * 1. imap.search() 返回 UIDs（不是seqno），如 [5794, 5795, ...]
 * 2. imap.fetch(uids) 发送 "UID FETCH 5794,5795,..."
 * 3. 对于每个消息，事件触发顺序：body → body_end → attributes
 *    - body事件 info = { seqno, which, size }（不含uid！）
 *    - attributes事件 attrs = { date, flags, uid }
 * 4. msg.uid 属性不存在，必须从 attrs.uid 获取
 *
 * 正确模式：
 *   msg.on('attributes', attrs => { msg.uid = attrs.uid; });
 *   msg.on('body', stream => {
 *     stream.on('end', () => {
 *       setImmediate(() => {
 *         // 此时 msg.uid 已由attributes填充
 *       });
 *     });
 *   });
 */

const Imap = require('imap');
const { simpleParser } = require('mailparser');
const fs = require('fs');
const path = require('path');
const config = require('./config/BUYER_MAP');
const { getImapConfig, getMailbox } = require('./lib/env');

const args = process.argv.slice(2);
const startDate = args[0] || '2026-01-01';
const endDate = args[1] || new Date().toISOString().split('T')[0];
const FORCE = args.includes('--force') || args.includes('-f');
const dateTag = (FORCE ? 'v3-' + Date.now() + '-' : '') + startDate.replace(/-/g, '') + '-' + endDate.replace(/-/g, '');

const EMAILS_DIR = path.join(__dirname, 'scan-results', 'emails');
const OUTPUT_FILE = path.join(EMAILS_DIR, `emails-${dateTag}.json`);

const IMAP_CONFIG = getImapConfig();
const MAILBOX = getMailbox();

const INVOICE_KW = config.INVOICE_KEYWORDS;
const EXCLUDE_KW = config.EXCLUDE_KEYWORDS;

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// RFC2047 解码器（处理 =?utf-8?B?...?= 格式）
function decodeHeader(str) {
  if (!str) return '';
  str = str.replace(/(=\?[^?]+\?[BQbq]\?[^?]*\?=)\s+(?==\?)/g, '$1');
  return str.replace(/=\?([^?\s]+)\?([BQbq])\?([^?]*)\?=/g, (match, charset, enc, text) => {
    try {
      let buf;
      if (enc === 'B' || enc === 'b') {
        buf = Buffer.from(text.replace(/\s/g, ''), 'base64');
      } else { // Q
        text = text.replace(/_/g, ' ').replace(/=([0-9A-Fa-f]{2})/g, (m, h) =>
          String.fromCharCode(parseInt(h, 16)));
        buf = Buffer.from(text, 'binary');
      }
      // 简单重编码为 UTF-8
      if (charset.toLowerCase() === 'gbk' || charset.toLowerCase() === 'gb2312') {
        return require('iconv-lite').decode(buf, 'gbk');
      }
      return buf.toString('utf8');
    } catch (e) { return text; }
  }).trim();
}

function getHeaderValue(header, name) {
  const unfolded = String(header || '').replace(/\r?\n[ \t]+/g, ' ');
  const match = unfolded.match(new RegExp(`^${name}:\\s*([\\s\\S]*?)(?=\\r?\\n\\S+:|$)`, 'im'));
  return match ? match[1].trim() : '';
}

function isInvoiceSubject(subject) {
  if (!subject) return false;
  const s = subject.toLowerCase();
  if (EXCLUDE_KW.some(k => s.includes(k.toLowerCase()))) return false;
  return INVOICE_KW.some(k => s.includes(k));
}

function getAttachmentType(fname) {
  if (!fname) return 'none';
  const f = fname.toLowerCase();
  if (f.endsWith('.pdf')) return 'pdf';
  if (f.endsWith('.ofd')) return 'ofd';
  if (/\.(jpg|jpeg|png|gif|bmp|tif|tiff|heic)/.test(f)) return 'image';
  if (f.endsWith('.zip') || f.endsWith('.rar') || f.endsWith('.7z')) return 'archive';
  return 'other';
}

function findLinks(body) {
  if (!body) return [];
  return (body.match(/https?:\/\/[^\s'"<>]{20,}/g) || [])
    .filter(l => !l.includes('qq.com') && !l.includes('weixin') && !l.includes('baidu.com'));
}

function htmlToText(html) {
  return String(html || '')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/(?:div|p|tr|li|table|section)>/gi, '\n')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&gt;/g, '>')
    .replace(/&lt;/g, '<')
    .replace(/&amp;/g, '&')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)))
    .replace(/[ \t]+/g, ' ')
    .replace(/\n\s+/g, '\n')
    .replace(/\n{2,}/g, '\n')
    .trim();
}

function extractBodyInfo(body) {
  if (!body || body.length < 10) return null;
  const info = {};
  const amt = body.match(/价税合计[（(]小写[）)][：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)/)
    || body.match(/合计金额[：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)/)
    || body.match(/发票金额[：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)/)
    || body.match(/金额合计[：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)/);
  if (amt) info.amount = amt[1].replace(/,/g, '');
  const no = body.match(/(?:发票号码|发票号|数电号码)[：:]\s*([0-9]{20,})/);
  if (no) info.invoiceNo = no[1];
  const buyer = body.match(/发票抬头[：:]\s*([^\r\n|]+?)(?:\s{2,}|数电号码|开票日期|合计金额|$)/);
  const buyer2 = buyer || body.match(/购方名称[：:]\s*([^\r\n|]+)/);
  if (buyer2) info.buyer = buyer2[1].trim();
  const seller = body.match(/发票开具方[：:]\s*([^\r\n|]+?)(?:\s{2,}|提示|$)/)
    || body.match(/销方名称[：:]\s*([^\r\n|]+)/)
    || body.match(/您收到一张【([^】]+)】开具的发票/);
  if (seller) info.seller = seller[1].trim();
  const date = body.match(/开票日期[：:]\s*(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日/)
    || body.match(/开票日期[：:]\s*(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (date) info.invoiceDate = `${date[1]}-${String(date[2]).padStart(2, '0')}-${String(date[3]).padStart(2, '0')}`;
  return Object.keys(info).length > 0 ? info : null;
}

/**
 * fetch邮件头的辅助函数
 * @param {Imap} imap
 * @param {number[]} uids - UID数组
 * @returns Promise<{uid, from, subject, date}[]>
 */
function fetchHeaders(imap, uids) {
  return new Promise(res => {
    const results = {};
    const target = uids.length;
    let fetched = 0;
    let settled = false;
    const finish = (data) => { if (!settled) { settled = true; res(data); } };
    const timer = setTimeout(() => finish(Object.values(results)), 30000);

    const fetcher = imap.fetch(uids, { bodies: 'HEADER.FIELDS (FROM SUBJECT DATE)' });
    fetcher.on('message', msg => {
      let header = '';
      let done = false;
      // 关键：attributes 在 body_end 之后才触发，必须用 setImmediate 等 uid
      msg.on('attributes', attrs => { msg.uid = attrs.uid; });
      msg.on('body', stream => {
        stream.on('data', c => { header += c.toString('utf8'); });
        stream.on('end', () => {
          setImmediate(() => {
            if (done) return;
            done = true;
            if (msg.uid) {
              results[msg.uid] = {
                uid: msg.uid,
                from: decodeHeader(getHeaderValue(header, 'From')),
                subject: decodeHeader(getHeaderValue(header, 'Subject')),
                date: getHeaderValue(header, 'Date'),
              };
            }
            fetched++;
            if (fetched >= target) { clearTimeout(timer); finish(Object.values(results)); }
          });
        });
      });
      msg.on('error', () => {
        if (done) return;
        done = true;
        fetched++;
        if (fetched >= target) { clearTimeout(timer); finish(Object.values(results)); }
      });
    });
    fetcher.once('error', () => { clearTimeout(timer); finish(Object.values(results)); });
  });
}

/**
 * fetch邮件全文（正文+附件）
 */
function fetchFull(imap, uids) {
  return new Promise(res => {
    const results = {};
    let pending = 0;
    let settled = false;
    const finish = (data) => { if (!settled) { settled = true; res(data); } };
    // 全局超时兜底：60秒内强制结束
    const globalTimer = setTimeout(() => { console.log(`[fetchFull] 全局超时，仍有 ${pending} 条未完成`); finish(results); }, 60000);
    const fetcher = imap.fetch(uids, { bodies: '', struct: true });
    fetcher.on('message', msg => {
      pending++;
      let done = false;
      // 每条消息独立超时（30秒）
      const msgTimer = setTimeout(() => {
        if (!done) { done = true; pending--; if (pending <= 0) { clearTimeout(globalTimer); finish(results); } }
      }, 30000);
      msg.on('attributes', attrs => { msg.uid = attrs.uid; });
      msg.on('body', (stream, info) => {
        const bufs = [];
        stream.on('data', c => bufs.push(c));
        stream.on('end', () => {
          clearTimeout(msgTimer);
          done = true;
          setImmediate(() => {
            if (msg.uid) results[msg.uid] = { uid: msg.uid, _body: Buffer.concat(bufs) };
            pending--;
            if (pending <= 0) { clearTimeout(globalTimer); finish(results); }
          });
        });
      });
      msg.on('error', () => { clearTimeout(msgTimer); if (!done) { done = true; pending--; if (pending <= 0) { clearTimeout(globalTimer); finish(results); } } });
    });
    fetcher.once('error', () => { clearTimeout(globalTimer); finish(results); });
    fetcher.once('end', () => setTimeout(() => { clearTimeout(globalTimer); finish(results); }, 5000));
  });
}

async function scanEmails() {
  if (!fs.existsSync(EMAILS_DIR)) fs.mkdirSync(EMAILS_DIR, { recursive: true });

  if (fs.existsSync(OUTPUT_FILE)) {
    const existing = JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8'));
    if (existing.meta && existing.meta.dateTag === dateTag && existing.emails.length > 0) {
      console.log('✅ 已有有效扫描结果: ' + OUTPUT_FILE);
      console.log('发票邮件: ' + existing.emails.length + ' 封');
      const byStatus = {};
      existing.emails.forEach(e => { byStatus[e.status] = (byStatus[e.status] || 0) + 1; });
      for (const [s, c] of Object.entries(byStatus)) console.log('  ' + s + ': ' + c);
      return existing;
    }
  }

  return new Promise((resolve, reject) => {
    const imap = new Imap(IMAP_CONFIG);

    imap.once('ready', async () => {
      console.log('✅ IMAP连接成功');
      imap.openBox(MAILBOX, true, async (err, box) => {
        if (err) { imap.end(); reject(err); return; }

        const since = new Date(startDate);
        since.setDate(since.getDate() - 1);
        const before = new Date(endDate);
        before.setDate(before.getDate() + 1);

        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('【第一轮】快速扫描邮件标题（按UID）...');

        imap.search([['SINCE', since], ['BEFORE', before]], async (err, uidList) => {
          if (err || !uidList || uidList.length === 0) {
            console.log('未找到邮件');
            imap.end();
            resolve({ meta: { dateTag, total: 0 }, emails: [] });
            return;
          }

          console.log('总邮件: ' + uidList.length + ' 封，开始分批获取标题...');
          const allHeaders = [];
          const BATCH = 100;

          for (let i = 0; i < uidList.length; i += BATCH) {
            const uids = uidList.slice(i, i + BATCH);
            const batch = await fetchHeaders(imap, uids);
            allHeaders.push(...batch);
            process.stdout.write(`\r  [${~~(i/BATCH)+1}/${~~(uidList.length/BATCH)+1}] 已获取 ${allHeaders.length}/${uidList.length} 封`);
            await sleep(50);
          }

          console.log('\n✅ 标题获取完成，过滤发票邮件...');

          const invoiceHeaders = allHeaders.filter(h => isInvoiceSubject(h.subject));
          console.log('📧 发票邮件候选: ' + invoiceHeaders.length + ' 封');

          if (invoiceHeaders.length === 0) {
            imap.end();
            const result = { meta: { dateTag, startDate, endDate, totalSearched: uidList.length, totalInvoice: 0 }, emails: [] };
            fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result, null, 2));
            resolve(result);
            return;
          }

          console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
          console.log('【第二轮】获取附件结构和正文摘要...');

          const invoiceEmails = [];
          const invoiceUids = invoiceHeaders.map(h => h.uid);
          const BATCH2 = 8;

          for (let i = 0; i < invoiceUids.length; i += BATCH2) {
            const uids = invoiceUids.slice(i, i + BATCH2);
            const fetchedAll = await fetchFull(imap, uids);

            for (const uid of uids) {
              const h = invoiceHeaders.find(h => h.uid == uid) || {};
              let item = fetchedAll[uid];
              if (!item || !item._body || item._body.length === 0) {
                const retry = await fetchFull(imap, [uid]);
                item = retry[uid] || item;
              }
              if (!item || !item._body || item._body.length === 0) {
                invoiceEmails.push({ uid, from: h.from || '', subject: h.subject || '', date: h.date || '', status: 'error', error: 'body not fetched' });
                continue;
              }

              let bodyText = '', attachments = [], links = [], bodyInfo = null;

              try {
                const parsed = await simpleParser(item._body);
                const htmlText = htmlToText(parsed.html || '');
                bodyText = (parsed.text && parsed.text.trim() ? parsed.text : htmlText).substring(0, 4000);
                attachments = (parsed.attachments || []).map(a => ({
                  filename: a.filename, contentType: a.contentType,
                  size: a.size, type: getAttachmentType(a.filename),
                }));
                links = [...new Set([...findLinks(bodyText), ...findLinks(String(parsed.html || ''))])];
                bodyInfo = extractBodyInfo(bodyText);
              } catch (e) { /* 解析失败 */ }

              let status = 'unknown';
              if (attachments.some(a => a.type === 'pdf')) status = 'pending-pdf';
              else if (attachments.length > 0) status = 'needs-manual';
              else if (links.length > 0) status = 'pending-link';
              else status = 'needs-manual';

              invoiceEmails.push({
                uid, from: h.from || '', subject: h.subject || '', date: h.date || '',
                bodyText, attachments, links, bodyInfo, status,
                scannedAt: new Date().toISOString(),
              });
            }

            process.stdout.write(`\r  [${~~(i/BATCH2)+1}/${~~(invoiceUids.length/BATCH2)+1}] 已处理 ${invoiceEmails.length}/${invoiceUids.length} 封`);
            await sleep(30);
          }

          imap.end();

          const byStatus = {};
          invoiceEmails.forEach(e => { byStatus[e.status] = (byStatus[e.status] || 0) + 1; });

          const result = {
            meta: {
              dateTag, startDate, endDate,
              totalSearched: uidList.length,
              totalInvoice: invoiceEmails.length,
              scannedAt: new Date().toISOString(),
              byStatus,
            },
            emails: invoiceEmails,
          };

          fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result, null, 2), 'utf8');

          console.log('');
          console.log('✅ 扫描完成，已保存: ' + OUTPUT_FILE);
          console.log('');
          console.log('━━━ 扫描统计 ━━━');
          console.log('扫描范围: ' + startDate + ' ~ ' + endDate);
          console.log('邮件总量: ' + uidList.length);
          console.log('发票邮件: ' + invoiceEmails.length);
          for (const [s, c] of Object.entries(byStatus).sort((a, b) => b[1] - a[1])) {
            const icons = { 'pending-pdf': '📄', 'pending-link': '🔗', 'needs-manual': '⚠️', 'error': '❌' };
            console.log('  ' + (icons[s] || '•') + ' ' + s + ': ' + c);
          }

          resolve(result);
        });
      });
    });

    imap.once('error', err => { console.error('IMAP错误:', err.message); reject(err); });
    imap.connect();
  });
}

scanEmails().catch(e => { console.error(e); process.exit(1); });

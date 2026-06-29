#!/usr/bin/env node
/**
 * step4-merge-data.js — 环节⑥ 多源数据合并 v2.0
 * 
 * 功能：
 * - 合并：邮件扫描 + PDF提取 + BUYER_MAP
 * - 生成：发票最终清单 + 人工任务清单
 * - 每条记录含 emailUid → 用于生成超链接
 * 
 * 用法：
 *   node step4-merge-data.js [dateTag]
 */

const fs = require('fs');
const path = require('path');
const config = require('./config/BUYER_MAP');
const { getMailWebUser } = require('./lib/env');

const args = process.argv.slice(2);
const dateTag = args[0] || '';

// ===== 找到最新的扫描文件 =====
function findLatestFile(dir, prefix, dateTag) {
  if (!fs.existsSync(dir)) return null;
  const files = fs.readdirSync(dir)
    .filter(f => f.startsWith(prefix) && f.endsWith('.json'))
    .filter(f => !dateTag || f.includes(dateTag))
    .sort().reverse();
  return files[0] || null;
}

// ===== 工具函数 =====
function sleep(ms) { return new Promise(r => setTimeout(r,ms)); }

function cleanCompanyName(name) {
  if (!name) return null;
  let n = name.trim();
  n = n.replace(/（发票金额[：:]*\d+\.?\d*元）/g, '');
  n = n.replace(/\(发票金额[：:]*\d+\.?\d*元\)/g, '');
  n = n.replace(/^[¥￥]\s*\d+\.?\d*\s*/, '');
  n = n.replace(/\(个体工商户\)/g, '（个体工商户）');
  n = n.replace(/（个体工商户(?![）])/g, '（个体工商户）');
  // 移除噪声
  if (n.includes('开票申请处理成功通知')) return null;
  if (n.includes('发票认证通知')) return null;
  if (n.includes('检测到新登录')) return null;
  if (/^\d{4}_/.test(n)) n = n.replace(/^\d{4}_/, '');
  // 归一化
  n = config.BUYER_NORMALIZE[n] || n;
  if (n.length < 4) return null;
  if (/^\d+$/.test(n)) return null;
  return n;
}

function extractAmountFromSubject(subject) {
  if (!subject) return null;
  // "发票金额：XX元" 或 "【发票金额：XXX】" 或 "¥XXX"
  const patterns = [
    /发票金额[：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)\s*元/,
    /【发票金额[：:]\s*([0-9,]+\.?[0-9]*)\s*】/,
    /金额[：:]\s*[¥￥]?\s*([0-9,]+\.?[0-9]*)/,
    /【([0-9,]+\.?[0-9]*)\s*元】/,
    /[¥￥]\s*([0-9,]+\.?[0-9]*)/,
  ];
  for (const p of patterns) {
    const m = subject.match(p);
    if (m) return m[1].replace(/,/g, '');
  }
  return null;
}

function extractSellerFromSubject(subject) {
  if (!subject) return null;
  // "来自XXX的电子发票"
  const m1 = subject.match(/来自(.+?)的电子发票/);
  if (m1) return m1[1].trim();
  // "【XXX】开具的发票"
  const m2 = subject.match(/【(.+?)】开具的发票/);
  if (m2) return m2[1].trim();
  // "XXX电子发票"
  const m3 = subject.match(/(.+?)(?:电子发票|发票)/);
  if (m3 && m3[1].length > 2) return m3[1].trim();
  return null;
}

function inferBuyerFromSeller(seller, docType) {
  // 文档类型默认
  if (docType) {
    const defaultBuyer = config.DOCTYPE_DEFAULT_BUYER[docType];
    if (defaultBuyer) return defaultBuyer;
  }
  // BUYER_MAP 查表
  for (const entry of config.ISSUER_TO_BUYER) {
    if (entry.issuerKeywords.some(k => seller && seller.includes(k))) {
      return entry.buyer;
    }
  }
  return null;
}

function inferBuyerFromEmail(emailFrom) {
  if (!emailFrom) return null;
  const addr = emailFrom.toLowerCase();
  for (const [pattern, buyer] of Object.entries(config.EMAIL_FROM_TO_BUYER)) {
    if (addr.includes(pattern.toLowerCase())) return buyer;
  }
  return null;
}

function extractAmountFromFilename(filename) {
  if (!filename) return null;
  const m = filename.match(/(?:^|[^\d])(\d{1,6}\.\d{2})\.pdf$/i);
  if (m) return m[1];
  return null;
}

function generateEmailHyperlink(uid) {
  // 生成 QQ 邮箱直接链接（通过 IMAP UID）
  // QQ邮箱支持 ?uid=XXX 格式直接跳转到邮件
  return `https://mail.qq.com/cgi-bin/readmail?uin=${getMailWebUser()}&fid=0000000001&uid=${uid}&no_lang=1`;
}

// ===== 主合并函数 =====
async function mergeData() {
  // 读取邮件扫描结果
  const scanDir = path.join(__dirname, 'scan-results', 'emails');
  const emailFile = findLatestFile(scanDir, 'emails-', dateTag);
  if (!emailFile) { console.error('未找到邮件扫描文件'); process.exit(1); }
  const scanData = JSON.parse(fs.readFileSync(path.join(scanDir, emailFile), 'utf8'));
  console.log('邮件数据: ' + scanData.emails.length + ' 封');

  const classifiedDir = path.join(__dirname, 'scan-results', 'classified');
  const classifiedFile = findLatestFile(classifiedDir, 'classified-', dateTag);
  const classifiedData = classifiedFile ? JSON.parse(fs.readFileSync(path.join(classifiedDir, classifiedFile), 'utf8')) : { records: [] };
  const classifiedByUid = {};
  for (const record of classifiedData.records || []) classifiedByUid[String(record.uid)] = record;

  const downloadDir = path.join(__dirname, 'scan-results', 'downloads');
  const downloadFile = findLatestFile(downloadDir, 'download-results-', dateTag);
  const downloadData = downloadFile ? JSON.parse(fs.readFileSync(path.join(downloadDir, downloadFile), 'utf8')) : { downloaded: [] };
  const downloadByUid = {};
  for (const item of downloadData.downloaded || []) {
    if (!downloadByUid[String(item.uid)]) downloadByUid[String(item.uid)] = [];
    downloadByUid[String(item.uid)].push(item);
  }

  // 读取PDF提取结果
  const pdfDir = path.join(__dirname, 'scan-results');
  let pdfFile = findLatestFile(pdfDir, 'pdf-text-', dateTag);
  if (!pdfFile) {
    console.log('⚠ 未找到带 dateTag 的 PDF 文件，尝试任意最新文件...');
    pdfFile = findLatestFile(pdfDir, 'pdf-text-', null);
  }
  const pdfData = pdfFile ? JSON.parse(fs.readFileSync(path.join(pdfDir, pdfFile), 'utf8')) : { results: [] };
  console.log('PDF数据: ' + pdfData.results.length + ' 个 (来源: ' + (pdfFile || '无') + ')');

  // 建立 filename → pdfResult 映射
  const pdfMap = {};
  for (const r of pdfData.results) {
    if (r.filename) pdfMap[r.filename] = r;
  }

  // 建立 uid → pdfResult 映射（通过文件名中的uid前缀）
  const pdfByUid = {};
  for (const r of pdfData.results) {
    const uidMatch = r.filename && (r.filename.match(/^uid(\d+)_/) || r.filename.match(/^(\d+)_/));
    if (uidMatch) pdfByUid[uidMatch[1]] = r;
  }

  // ===== 核心合并逻辑 =====
  const finalRecords = [];
  const manualTasks = [];

  for (const email of scanData.emails) {
    const record = {
      index: email.uid,
      emailUid: email.uid,
      emailHyperlink: generateEmailHyperlink(email.uid),
      subject: email.subject,
      emailFrom: email.from,
      emailDate: email.date,
      status: email.status,
      sourceType: classifiedByUid[String(email.uid)]?.sourceType || null,
      expectedAction: classifiedByUid[String(email.uid)]?.expectedAction || null,
      platform: classifiedByUid[String(email.uid)]?.platform || null,
      resolver: downloadByUid[String(email.uid)]?.find(x => x.resolver)?.resolver || null,
      docType: null,
      buyer: null,
      buyerSource: null,
      seller: null,
      sellerSource: null,
      amount: null,
      amountSource: null,
      invoiceNo: null,
      invoiceDate: null,
      taxAmount: null,
      hasPdf: false,
      pdfFilename: null,
      pdfFilepath: null,
      pdfText: null,
      needsManualReview: false,
      manualReason: null,
      notes: '',
    };

    // ===== A. 从邮件正文提取的信息 =====
    if (email.bodyInfo) {
      if (email.bodyInfo.buyer && !record.buyer) {
        record.buyer = cleanCompanyName(email.bodyInfo.buyer);
        record.buyerSource = 'email-body';
      }
      if (email.bodyInfo.seller && !record.seller) {
        record.seller = cleanCompanyName(email.bodyInfo.seller);
        record.sellerSource = 'email-body';
      }
      if (email.bodyInfo.amount && !record.amount) {
        record.amount = email.bodyInfo.amount;
        record.amountSource = 'email-body';
      }
      if (email.bodyInfo.invoiceNo && !record.invoiceNo) {
        record.invoiceNo = email.bodyInfo.invoiceNo;
      }
      if (email.bodyInfo.invoiceDate && !record.invoiceDate) {
        record.invoiceDate = email.bodyInfo.invoiceDate;
      }
    }

    // ===== B. 从邮件主题提取的信息 =====
    if (!record.amount) {
      const amt = extractAmountFromSubject(email.subject);
      if (amt) { record.amount = amt; record.amountSource = 'email-subject'; }
    }
    if (!record.seller) {
      const seller = extractSellerFromSubject(email.subject);
      if (seller) {
        record.seller = cleanCompanyName(seller);
        record.sellerSource = 'email-subject';
      }
    }

    // ===== C. 从附件文件名提取信息 =====
    if (email.attachments && email.attachments.length > 0) {
      const pdfAtt = email.attachments.find(a => a.type === 'pdf');
      if (pdfAtt) {
        record.hasPdf = true;
        record.pdfFilename = pdfAtt.filename;
        // 从文件名提取金额
        if (!record.amount) {
          const fnAmt = extractAmountFromFilename(pdfAtt.filename);
          if (fnAmt) { record.amount = fnAmt; record.amountSource = 'filename'; }
        }
      }
    }

    // ===== D. 从PDF提取信息 =====
    const uidPdf = pdfByUid[email.uid];
    const pdfRecord = uidPdf || (record.pdfFilename ? pdfMap[record.pdfFilename] : null);

    if (pdfRecord && !pdfRecord.error) {
      record.hasPdf = true;
      record.pdfFilename = pdfRecord.filename || record.pdfFilename;
      record.pdfFilepath = pdfRecord.filepath || pdfRecord.path || record.pdfFilepath;
      record.docType = pdfRecord.docType || '发票';
      record.invoiceDate = pdfRecord.date || record.invoiceDate;
      record.invoiceNo = pdfRecord.invoiceNo || record.invoiceNo;
      record.taxAmount = pdfRecord.taxAmount || null;
      record.pdfText = (pdfRecord.fullText || '').substring(0, 500); // 只保存前500字符

      // 金额：PDF价税合计优先
      if (pdfRecord.amount) {
        record.amount = pdfRecord.amount;
        record.amountSource = 'pdf';
      }

      // 购买方/销售方
      if (pdfRecord.buyer) {
        record.buyer = cleanCompanyName(pdfRecord.buyer) || record.buyer;
        record.buyerSource = 'pdf';
      }
      if (pdfRecord.seller) {
        record.seller = cleanCompanyName(pdfRecord.seller) || record.seller;
        record.sellerSource = 'pdf';
      }
    }

    // ===== E. 推断购买方 =====
    if (!record.buyer) {
      // 发件人邮箱推断
      let inferred = inferBuyerFromEmail(email.from);
      if (inferred) { record.buyer = inferred; record.buyerSource = 'email-from'; }
    }
    if (!record.buyer && record.seller) {
      // 销售方关键词查表
      let inferred = inferBuyerFromSeller(record.seller, record.docType);
      if (inferred) { record.buyer = inferred; record.buyerSource = 'seller-map'; }
    }
    if (!record.buyer && record.docType) {
      // 文档类型默认
      let inferred = inferBuyerFromSeller(null, record.docType);
      if (inferred) { record.buyer = inferred; record.buyerSource = 'doctype'; }
    }

    // ===== F. 判断是否需要人工 =====
    const needsManual = !record.amount || (!record.buyer && !record.seller);
    if ((email.status === 'needs-manual' || email.status === 'pending-link') && !record.hasPdf) {
      record.needsManualReview = true;
      record.manualReason = email.status === 'needs-manual'
        ? 'NO_ATTACH_NO_LINK'
        : 'LINK_NEED_SCAN';
      if (email.links && email.links.length > 0) {
        record.notes = '链接: ' + email.links.slice(0, 2).join('; ');
      }
      manualTasks.push({
        uid: email.uid,
        hyperlink: record.emailHyperlink,
        subject: email.subject,
        date: email.date,
        reason: record.manualReason,
        currentAmount: record.amount,
        currentBuyer: record.buyer,
        currentSeller: record.seller,
        links: email.links,
      });
    } else if (needsManual) {
      record.needsManualReview = true;
      record.manualReason = !record.amount ? 'NO_AMOUNT' : 'NO_BUYER';
      manualTasks.push({
        uid: email.uid,
        hyperlink: record.emailHyperlink,
        subject: email.subject,
        date: email.date,
        reason: record.manualReason,
        currentAmount: record.amount,
        currentBuyer: record.buyer,
        currentSeller: record.seller,
      });
    }

    finalRecords.push(record);
  }

  // ===== G. 批量修正已知问题 =====
  for (const r of finalRecords) {
    // 滞纳金特殊处理
    if (r.subject && r.subject.includes('滞纳金') && r.pdfFilename) {
      const acc = r.pdfFilename.match(/ACC(\d+)/);
      if (acc) {
        r.amount = (parseFloat(acc[1]) / 1000).toFixed(2);
        r.amountSource = 'filename-ACC';
        r.buyer = r.buyer || inferBuyerFromSeller(r.seller, r.docType) || config.DOCTYPE_DEFAULT_BUYER[r.docType] || null;
        r.seller = r.seller || extractSellerFromSubject(r.subject);
        r.needsManualReview = false;
        r.manualReason = null;
      }
    }

    // buyer=seller 互换
    if (r.buyer && r.seller && r.buyer === r.seller &&
        r.buyer !== '个人报销') {
      // 尝试从销售方推断真实购买方
      const inferredBuyer = inferBuyerFromSeller(r.seller, r.docType);
      if (inferredBuyer && inferredBuyer !== r.buyer) {
        r.seller = r.buyer; // 原来的buyer其实是seller
        r.buyer = inferredBuyer;
        r.notes = 'buyer=seller已互换';
      }
    }
  }

  // ===== 统计 =====
  const byStatus = {};
  finalRecords.forEach(r => { byStatus[r.status] = (byStatus[r.status] || 0) + 1; });
  const withBuyer = finalRecords.filter(r => r.buyer).length;
  const withSeller = finalRecords.filter(r => r.seller).length;
  const withAmount = finalRecords.filter(r => r.amount).length;
  const complete = finalRecords.filter(r => r.buyer && r.seller && r.amount).length;
  const needsManualCount = finalRecords.filter(r => r.needsManualReview).length;

  const byBuyer = {};
  finalRecords.filter(r => r.buyer && r.amount).forEach(r => {
    byBuyer[r.buyer] = byBuyer[r.buyer] || { count: 0, total: 0 };
    byBuyer[r.buyer].count++;
    byBuyer[r.buyer].total += parseFloat(r.amount);
  });

  // ===== 保存最终清单 =====
  const outDir = path.join(__dirname, 'scan-results');
  const outFile = path.join(outDir, `invoice-final-${scanData.meta.dateTag}.json`);
  const outCsv = path.join(outDir, `invoice-final-${scanData.meta.dateTag}.csv`);
  const manualFile = path.join(outDir, `manual-tasks-${scanData.meta.dateTag}.csv`);

  // CSV
  const csvHeaders = ['index', 'emailUid', 'emailHyperlink', 'subject', 'emailDate',
    'status', 'docType', 'buyer', 'seller', 'amount', 'invoiceNo', 'invoiceDate',
    'hasPdf', 'needsManualReview', 'manualReason', 'notes'];
  const csvLines = [csvHeaders.join(',')];
  for (const r of finalRecords) {
    const row = csvHeaders.map(h => {
      let v = (r[h] || '').toString();
      if (h === 'emailHyperlink') v = `=HYPERLINK("${v}","查看邮件")`;
      v = v.replace(/"/g, '""');
      return '"' + v + '"';
    });
    csvLines.push(row.join(','));
  }
  fs.writeFileSync(outCsv, '\ufeff' + csvLines.join('\n'), 'utf8');

  // 人工任务CSV
  const mHeaders = ['uid', 'hyperlink', 'subject', 'date', 'reason', 'currentAmount', 'currentBuyer', 'currentSeller'];
  const mLines = [mHeaders.join(',')];
  for (const t of manualTasks) {
    const row = mHeaders.map(h => {
      let v = (t[h] || (h === 'hyperlink' ? generateEmailHyperlink(t.uid) : '')).toString();
      if (h === 'hyperlink') v = `=HYPERLINK("${v}","查看邮件")`;
      v = v.replace(/"/g, '""');
      return '"' + v + '"';
    });
    mLines.push(row.join(','));
  }
  fs.writeFileSync(manualFile, '\ufeff' + mLines.join('\n'), 'utf8');

  const result = {
    meta: {
      dateTag: scanData.meta.dateTag,
      startDate: scanData.meta.startDate,
      endDate: scanData.meta.endDate,
      totalRecords: finalRecords.length,
      withBuyer, withSeller, withAmount,
      complete, needsManual: needsManualCount,
      hasPdf: finalRecords.filter(r => r.hasPdf).length,
      noPdf: finalRecords.filter(r => !r.hasPdf).length,
      manualTasks: manualTasks.length,
      mergedAt: new Date().toISOString(),
      byStatus,
    },
    byBuyer,
    data: finalRecords,
  };

  fs.writeFileSync(outFile, JSON.stringify(result, null, 2), 'utf8');

  // ===== 打印报告 =====
  console.log('');
  console.log('━━━ 合并完成 ━━━');
  console.log('总记录: ' + finalRecords.length);
  console.log('购买方: ' + withBuyer + '/' + finalRecords.length);
  console.log('销售方: ' + withSeller + '/' + finalRecords.length);
  console.log('金额: ' + withAmount + '/' + finalRecords.length);
  console.log('完整: ' + complete + '/' + finalRecords.length);
  console.log('需人工: ' + needsManualCount);
  console.log('');
  console.log('━━━ 购买方汇总 ━━━');
  for (const [b, s] of Object.entries(byBuyer).sort((a, b) => b[1].total - a[1].total)) {
    console.log(b + ': ' + s.count + '张, ¥' + s.total.toFixed(2));
  }
  console.log('');
  console.log('━━━ 状态分布 ━━━');
  for (const [s, c] of Object.entries(byStatus)) console.log('  ' + s + ': ' + c);
  console.log('');
  console.log('✅ 已保存:');
  console.log('  JSON: ' + outFile);
  console.log('  CSV:  ' + outCsv);
  if (manualTasks.length > 0) console.log('  人工任务CSV: ' + manualFile);
}

mergeData().catch(e => { console.error(e); process.exit(1); });

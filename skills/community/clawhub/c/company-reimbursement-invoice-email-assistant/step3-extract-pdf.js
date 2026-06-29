#!/usr/bin/env node
/**
 * step3-extract-pdf.js — 环节⑤ PDF文本提取 v2.0
 * 
 * 功能：
 * - 读取 downloads_raw/ 中的PDF文件
 * - 用 pdf2json 提取全文
 * - 提取：购买方、销售方、金额、发票号、开票日期、税额
 * - 支持数电发票空格拆分格式
 * - 支持行程单、付款通知书等特殊格式
 * 
 * 用法：
 *   node step3-extract-pdf.js [dateTag]
 */

const fs = require('fs');
const path = require('path');
const PDFParser = require('pdf2json');
const config = require('./config/BUYER_MAP');

const args = process.argv.slice(2);
const dateTag = args[0] || '';

// ===== 找到最新的下载结果 =====
function findLatestDownload() {
  const dirs = [
    path.join(__dirname, 'scan-results', 'downloads'),
    path.join(__dirname, 'downloads_raw'),
  ];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir)
      .filter(f => f.startsWith('download-results-') && f.endsWith('.json'))
      .filter(f => !dateTag || f.includes(dateTag))
      .sort().reverse();
    if (files[0]) return { dir, file: files[0] };
  }
  return null;
}

// ===== 找到待提取的PDF文件 =====
function findPdfs() {
  const dirs = [
    path.join(__dirname, 'scan-results', 'staging', dateTag, 'pdfs'),
    path.join(__dirname, 'scan-results', 'downloads', 'pdfs'),
    path.join(__dirname, 'downloads_raw'),
  ];
  const results = [];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir)
      .filter(f => f.toLowerCase().endsWith('.pdf'))
      .filter(f => !f.startsWith('._'))  // skip macOS resource forks
      .map(f => ({ filename: f, filepath: path.join(dir, f) }));
    results.push(...files);
  }
  return results;
}

// ===== 从PDF文本提取信息 =====
function normalizeInvoiceDate(value) {
  if (!value) return null;
  const m = String(value).match(/(\d{4})[年\-\/](\d{1,2})[月\-\/](\d{1,2})/);
  if (!m) return null;
  return `${m[1]}-${String(Number(m[2])).padStart(2, '0')}-${String(Number(m[3])).padStart(2, '0')}`;
}

function companyMatches(text) {
  const matches = text.match(/[\u4e00-\u9fa5（）()A-Za-z0-9·]{4,60}(?:有限公司|有限责任公司|股份有限公司|经营部|商行|网店|服务中心|个体工商户)/g) || [];
  return [...new Set(matches.map(s => s.trim()).filter(s =>
    !s.includes('项目名称') &&
    !s.includes('电子发票') &&
    !s.includes('规格型号')
  ))];
}

function assignPartiesByLabels(info, compact, companies) {
  if (companies.length < 2) return;
  const labelText = String(compact || '').replace(/\s+/g, '');
  const buyerIndex = labelText.indexOf('购买方信息');
  const sellerIndex = labelText.indexOf('销售方信息');

  if (buyerIndex >= 0 && sellerIndex >= 0) {
    if (sellerIndex < buyerIndex) {
      info.seller = info.seller || companies[0];
      info.buyer = info.buyer || companies[1];
      return;
    }
    info.buyer = info.buyer || companies[0];
    info.seller = info.seller || companies[1];
    return;
  }

  info.buyer = info.buyer || companies[0];
  info.seller = info.seller || companies[1];
}

function extractDigitalInvoice(t, filename) {
  const compact = t.replace(/\s+/g, ' ');
  const info = {
    docType: '发票',
    buyer: null,
    seller: null,
    amount: null,
    date: null,
    invoiceNo: null,
    taxAmount: null,
  };

  const noMatch = compact.match(/发票号码[:：]?\s*(\d{20,})/) || compact.match(/\b(\d{20,})\b/);
  if (noMatch) info.invoiceNo = noMatch[1];

  const dateMatch = compact.match(/开票日期[:：]?\s*(\d{4}年\d{1,2}月\d{1,2}日)/) ||
    compact.match(/(\d{4}年\d{1,2}月\d{1,2}日)/) ||
    compact.match(/(\d{4}[-\/]\d{1,2}[-\/]\d{1,2})/);
  if (dateMatch) info.date = normalizeInvoiceDate(dateMatch[1]);

  const money = [...compact.matchAll(/[¥￥楼]\s*([0-9,]+\.\d{2})/g)].map(m => Number(m[1].replace(/,/g, '')));
  if (money.length) info.amount = Math.max(...money).toFixed(2);
  if (!info.amount) {
    const fileAmount = filename.match(/(?:金额|价税合计)?([0-9]{1,6}\.\d{2})/);
    if (fileAmount) info.amount = Number(fileAmount[1]).toFixed(2);
  }
  if (money.length >= 2 && info.amount) {
    const lessThanAmount = money.filter(n => n < Number(info.amount));
    if (lessThanAmount.length) info.taxAmount = Math.min(...lessThanAmount).toFixed(2);
  }

  const companies = companyMatches(compact);
  assignPartiesByLabels(info, compact, companies);
  if (companies.length === 1) info.buyer = info.buyer || companies[0];
  info._extracted = '数电发票';
  return info;
}

function extractInvoiceInfo(text, filename) {
  // 统一空白
  const t = text.replace(/\t/g, ' ').replace(/\r\n/g, '\n');

  if (t.includes('电子发票') || t.includes('发票号码') || t.includes('价税合计')) {
    return extractDigitalInvoice(t, filename);
  }

  // ---- 行程单/火车票 ----
  const tripMatch = t.match(/出发站[：:]\s*(\S+).*?到达站[：:]\s*(\S+).*?出发时间[：:]\s*(\S+\s*\S+)/s);
  if (t.includes('出发站') || t.includes('到达站') || t.includes('席位') || t.includes('车次')) {
    const trip = {
      docType: '行程单',
      buyer: '个人报销',
      seller: '中国铁路12306',
      amount: null, date: null, invoiceNo: null,
    };
    // 金额：总价/席位
    const priceMatch = t.match(/总价[：:]\s*[¥￥]?\s*([0-9]+\.?[0-9]*)/);
    const seatMatch = t.match(/席位[：:]\s*(\S+)/);
    if (priceMatch) trip.amount = priceMatch[1].replace(/,/g, '');
    // 发票号：通常是订单号
    const orderMatch = t.match(/订单号[：:]\s*([A-Z0-9]{12,})/i);
    if (orderMatch) trip.invoiceNo = orderMatch[1];
    // 日期
    const dateMatch = t.match(/出发时间[：:]\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})/);
    if (dateMatch) trip.date = dateMatch[1].replace(/[年|月]/g, '-').replace(/-$/, '');
    trip._extracted = '行程单';
    return trip;
  }

  // ---- 付款通知书 / 滞纳金通知书 ----
  if (t.includes('付款通知书') || t.includes('滞纳金付款通知书')) {
    const companies = companyMatches(t.replace(/\s+/g, ' '));
    const notice = {
      docType: t.includes('滞纳金') ? '滞纳金付款通知书' : '付款通知书',
      buyer: config.DOCTYPE_DEFAULT_BUYER['付款通知书'] || null,
      seller: companies[0] || null,
      amount: null, date: null, invoiceNo: null, taxAmount: null,
    };
    // 金额：付款通知书金额 或 滞纳金金额
    // 滞纳金格式: ACC1650373 → 1650.373
    const accMatch = filename.match(/ACC(\d+)/);
    if (accMatch) {
      notice.amount = (parseFloat(accMatch[1]) / 1000).toFixed(2);
    }
    // 通知书编号
    const noMatch = t.match(/(?:通知书编号|付款通知书编号)[：:\s]*([0-9]{10,})/);
    if (noMatch) notice.invoiceNo = noMatch[1];
    // 日期
    const dateMatch = t.match(/(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})/);
    if (dateMatch) notice.date = dateMatch[1].replace(/[年|月]/g, '-').replace(/-$/, '');
    notice._extracted = '付款通知书';
    return notice;
  }

  // ---- 数电发票（空格拆分格式）----
  // 例: "购 买 方 信 息 统一社会信用代码/纳税人识别号： 销 售 方 信 息..."
  const spacedFormat = t.includes('购') && t.includes('买') && t.includes('方') && t.includes('信') && t.includes('息');
  if (spacedFormat) {
    return extractSpacedDigital(t, filename);
  }

  // ---- 普通PDF ----
  return extractNormalPDF(t, filename);
}

// 数电发票（空格拆分）
function extractSpacedDigital(t, filename) {
  // 移除所有空白用于匹配
  const raw = t.replace(/\s+/g, '');

  const info = {
    docType: '发票',
    buyer: null, seller: null,
    amount: null, date: null, invoiceNo: null, taxAmount: null,
  };

  // 金额：价税合计（小写）
  const amtMatch = raw.match(/价税合计（小写）[：:¥￥]*([0-9,]+\.?[0-9]*)/);
  if (amtMatch) {
    info.amount = amtMatch[1].replace(/,/g, '');
  } else {
    // 备选：从文件名提取金额
    const fnAmt = filename.match(/(?:^|[^\d])(\d{1,6}\.\d{2})\.pdf$/i);
    if (fnAmt) info.amount = fnAmt[1];
  }

  // 购买方名称（已从raw移除空格，直接匹配）
  // 处理连续两个"名称："的情况：header行有"名称：名称："，值行才有实际数据
  const buyerMatch = raw.match(/购买方.*?名称[：:]*(?:名称[：:]*)?([\u4e00-\u9fa5A-Za-z0-9（）()公司企业店所部]{2,40})(?:\d{15,}|统一|名称|项目|规格)/);
  if (buyerMatch) info.buyer = buyerMatch[1].trim();

  // 销售方名称
  const sellerMatch = raw.match(/销售方.*?名称[：:]*(?:名称[：:]*)?([\u4e00-\u9fa5A-Za-z0-9（）()公司企业店所部]{2,40})(?:\d{15,}|统一|名称|项目|规格)/);
  if (sellerMatch) info.seller = sellerMatch[1].trim();

  // 如果空格格式找不到，尝试按“购买方信息/销售方信息”的标签顺序判断。
  // 有些数电票 PDF 抽取出来是“销售方信息 购买方信息 ... 销售方名称 购买方名称”，
  // 不能简单认为第一个公司就是购买方。
  if (!info.buyer || !info.seller) {
    const companyMatches = t.match(/([一-龥]{4,30}(?:有限公司|个体工商户|经营部|服务中心|中心))/g) || [];
    const unique = [...new Set(companyMatches)];
    if (unique.length >= 2) {
      assignPartiesByLabels(info, raw, unique);
    } else if (unique.length === 1) {
      if (!info.buyer) info.buyer = unique[0];
    }
  }

  // 发票号码
  const noMatch = t.match(/发票号[码]?[：:]\s*([0-9]{20,})/);
  if (noMatch) info.invoiceNo = noMatch[1];

  // 日期
  const dateMatch = t.match(/(\d{4}年\d{1,2}月\d{1,2}日)/);
  if (dateMatch) info.date = dateMatch[1].replace(/[年月日]/g, '-').replace(/-$/, '');

  // 税额
  const taxMatch = t.match(/税\s*额[：:\s]*[¥￥]?\s*([0-9,]+\.?[0-9]*)/);
  if (taxMatch) info.taxAmount = taxMatch[1].replace(/,/g, '');

  info._extracted = '数电发票(空格)';
  return info;
}

// 普通PDF提取
function extractNormalPDF(t, filename) {
  const info = {
    docType: '发票',
    buyer: null, seller: null,
    amount: null, date: null, invoiceNo: null, taxAmount: null,
  };

  // 金额
  const amtMatch = t.match(/价税合计[（(]小写[）)][：:\s]*[¥￥]?\s*([0-9,]+\.?[0-9]*)/);
  if (amtMatch) {
    info.amount = amtMatch[1].replace(/,/g, '');
  }

  // 购买方
  const buyerMatch = t.match(/购买方[信息]?[：:]\s*([一-龥A-Za-z0-9（）\(\)公司企业店所部]{2,40})/);
  if (buyerMatch) info.buyer = buyerMatch[1].trim();

  // 销售方
  const sellerMatch = t.match(/销售方[信息]?[：:]\s*([一-龥A-Za-z0-9（）\(\)公司企业店所部]{2,40})/);
  if (sellerMatch) info.seller = sellerMatch[1].trim();

  // 发票号
  const noMatch = t.match(/(?:发票号|发票号码)[：:\s]*([0-9]{20,})/);
  if (noMatch) info.invoiceNo = noMatch[1];

  // 日期
  const dateMatch = t.match(/(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})/);
  if (dateMatch) info.date = dateMatch[1].replace(/[年月日]/g, '-').replace(/-$/, '');

  // 税额
  const taxMatch = t.match(/税额[：:\s]*[¥￥]?\s*([0-9,]+\.?[0-9]*)/);
  if (taxMatch) info.taxAmount = taxMatch[1].replace(/,/g, '');

  info._extracted = '普通PDF';
  return info;
}

// ===== 清洗公司名称 =====
function cleanCompanyName(name) {
  if (!name) return null;
  let n = name.trim();
  // 移除发票金额混入
  n = n.replace(/（发票金额[：:]*\d+\.?\d*元）/g, '');
  n = n.replace(/\(发票金额[：:]*\d+\.?\d*元\)/g, '');
  // 移除金额前缀
  n = n.replace(/^[¥￥]\s*\d+\.?\d*\s*/, '');
  // 统一括号
  n = n.replace(/\(个体工商户\)/g, '（个体工商户）');
  n = n.replace(/（个体工商户(?![）])/g, '（个体工商户）');
  // 移除过短的结果
  if (n.length < 4) return null;
  // 移除全是数字的
  if (/^\d+$/.test(n)) return null;
  return n;
}

function saveExtractionResults(outputFile, dateTagFromDl, results) {
  const output = {
    meta: {
      dateTag: dateTagFromDl,
      total: results.length,
      success: results.filter(r => !r.error).length,
      fail: results.filter(r => r.error).length,
      extractedAt: new Date().toISOString(),
    },
    results,
  };
  fs.writeFileSync(outputFile, JSON.stringify(output, null, 2), 'utf8');
  return output;
}

// ===== 主函数 =====
async function extractPdfs() {
  const pdfFiles = findPdfs();
  console.log('待提取PDF: ' + pdfFiles.length + ' 个');

  // 检查已有提取结果
  const scanDir = path.join(__dirname, 'scan-results');
  const dlResult = findLatestDownload();
  const dateTagFromDl = dateTag || (dlResult ? dlResult.file.match(/download-results-(.+)\.json$/)[1] : new Date().toISOString().slice(0, 10));
  const outputFile = path.join(scanDir, `pdf-text-${dateTagFromDl}.json`);

  let results = [];
  if (fs.existsSync(outputFile)) {
    results = JSON.parse(fs.readFileSync(outputFile, 'utf8')).results || [];
  }

  const currentPdfPaths = new Set(pdfFiles.map(f => path.resolve(f.filepath)));
  const currentPdfNames = new Set(pdfFiles.map(f => f.filename));
  results = results.filter(r => {
    const resultPath = r.filepath ? path.resolve(r.filepath) : null;
    return (resultPath && currentPdfPaths.has(resultPath)) || currentPdfNames.has(r.filename);
  });
  if (results.length) console.log('已有提取结果: ' + results.length + ' 条');

  const extractedFnames = new Set(results.map(r => r.filename));
  const toExtract = pdfFiles.filter(f => !extractedFnames.has(f.filename));
  console.log('本次需提取: ' + toExtract.length + ' 个');

  if (toExtract.length === 0) {
    saveExtractionResults(outputFile, dateTagFromDl, results);
    console.log('✅ 全部已提取，跳过');
    return results;
  }

  const pdfParser = new PDFParser();
  let done = 0;

  for (const pdf of toExtract) {
    try {
      const pdfParserInstance = new PDFParser();
      const pdfData = await new Promise((resolve, reject) => {
        pdfParserInstance.on('pdfParser_dataError', err => reject(err));
        pdfParserInstance.on('pdfParser_dataReady', data => resolve(data));
        pdfParserInstance.loadPDF(pdf.filepath);
      });

      // 提取全文
      let fullText = '';
      for (const page of pdfData.Pages || []) {
        for (const text of page.Texts || []) {
          const content = (text.R || []).map(r => {
            try { return decodeURIComponent(r.T); } catch(e) { return r.T; }
          }).join('');
          fullText += content + ' ';
        }
        fullText += '\n';
      }

      const info = extractInvoiceInfo(fullText, pdf.filename);
      info.filename = pdf.filename;
      info.filepath = pdf.filepath;
      info.fullText = fullText;
      info.rawLength = fullText.length;
      info.buyer = cleanCompanyName(info.buyer);
      info.seller = cleanCompanyName(info.seller);
      info.extractedAt = new Date().toISOString();

      results.push(info);

    } catch (e) {
      results.push({
        filename: pdf.filename,
        filepath: pdf.filepath,
        error: e.message,
        status: 'fail',
        extractedAt: new Date().toISOString(),
      });
    }

    done++;
    process.stdout.write(`\r  提取进度: ${done}/${toExtract.length} (${Math.round(done/toExtract.length*100)}%)`);
  }

  // 保存
  const output = saveExtractionResults(outputFile, dateTagFromDl, results);

  // 统计
  const byType = {};
  results.filter(r => !r.error).forEach(r => {
    byType[r._extracted || 'unknown'] = (byType[r._extracted || 'unknown'] || 0) + 1;
  });

  console.log('');
  console.log('✅ 提取完成，已保存: ' + outputFile);
  console.log('━━━ 提取统计 ━━━');
  console.log('总计: ' + results.length + ' (成功:' + output.meta.success + ' 失败:' + output.meta.fail + ')');
  for (const [t, c] of Object.entries(byType)) console.log('  ' + t + ': ' + c);

  return results;
}

extractPdfs().catch(e => { console.error(e); process.exit(1); });

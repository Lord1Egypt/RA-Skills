#!/usr/bin/env node
/**
 * step5-generate-ledger.js — 环节⑧ 台账生成 v2.0
 * 
 * 功能：
 * - 读取 invoice-final-*.json
 * - 生成 4个Sheet 的 Excel 台账
 * - Sheet: 明细(含邮件超链接) / 汇总 / 统计 / 人工任务
 * - 人工任务单独标注原因，可直接点击"查看邮件"超链接
 * 
 * 用法：
 *   node step5-generate-ledger.js [dateTag]
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const dateTag = args[0] || '';

function findLatestFile(dir, prefix) {
  if (!fs.existsSync(dir)) return null;
  const files = fs.readdirSync(dir)
    .filter(f => f.startsWith(prefix) && f.endsWith('.json'))
    .filter(f => !dateTag || f.includes(dateTag))
    .sort().reverse();
  return files[0] || null;
}

// ===== ExcelJS 安装检查 =====
try { require.resolve('exceljs'); } catch (e) {
  console.log('安装 exceljs...');
  require('child_process').execSync('npm install exceljs', { cwd: __dirname, stdio: 'inherit' });
}
const ExcelJS = require('exceljs');

async function generateLedger() {
  const scanDir = path.join(__dirname, 'scan-results');
  const jsonFile = findLatestFile(scanDir, 'invoice-final-');
  if (!jsonFile) { console.error('未找到最终清单文件'); process.exit(1); }

  const data = JSON.parse(fs.readFileSync(path.join(scanDir, jsonFile), 'utf8'));
  const records = data.data;
  const meta = data.meta;

  console.log('读取数据: ' + records.length + ' 条 (' + jsonFile + ')');

  const dateTagOut = meta.dateTag;
  const outputFile = path.join(scanDir, `发票台账-${dateTagOut}.xlsx`);
  const workbook = new ExcelJS.Workbook();
  workbook.creator = 'QClaw 发票自动化 v2.0';
  workbook.created = new Date();

  // ===== Sheet 1: 台账明细 =====
  const s1 = workbook.addWorksheet('台账明细');
  s1.properties.defaultColWidth = 14;

  const cols = [
    ['A', 5, '序号'],
    ['B', 38, '购买方'],
    ['C', 38, '销售方'],
    ['D', 12, '金额(元)'],
    ['E', 10, '金额来源'],
    ['F', 24, '发票号码'],
    ['G', 12, '开票日期'],
    ['H', 10, '文档类型'],
    ['I', 8, '有PDF'],
    ['J', 10, '状态'],
    ['K', 45, '邮件主题'],
    ['L', 10, '查看邮件'],
    ['M', 40, '备注'],
  ];
  cols.forEach(([col, width, header]) => {
    s1.getColumn(col).width = width;
    s1.getColumn(col).numFmt = col === 'D' ? '#,##0.00' : '@';
  });

  // 表头
  const hRow = s1.addRow(cols.map(([, , h]) => h));
  hRow.font = { bold: true, color: { argb: 'FFFFFFFF' }, size: 11 };
  hRow.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4472C4' } };
  hRow.alignment = { horizontal: 'center' };

  // 数据行
  let rowNum = 2;
  for (const r of records) {
    const row = s1.addRow([
      r.index,
      r.buyer || '',
      r.seller || '',
      r.amount ? parseFloat(r.amount) : null,
      r.amountSource || '',
      r.invoiceNo || '',
      r.invoiceDate || '',
      r.docType || '',
      r.hasPdf ? '✓' : '✗',
      r.status || '',
      r.subject || '',
      '',  // 超链接在下面设置
      r.notes || (r.manualReason ? '⚠️ ' + r.manualReason : ''),
    ]);

    // 超链接
    if (r.emailHyperlink) {
      const linkCell = row.getCell('L');
      linkCell.value = { text: '查看邮件', hyperlink: r.emailHyperlink };
      linkCell.font = { color: { argb: 'FF0563C1' }, underline: true };
    }

    // 条件格式
    if (r.needsManualReview) {
      row.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFF2CC' } };
    }
    if (!r.hasPdf) {
      row.getCell('I').font = { color: { argb: 'FF999999' } };
    }
    if (r.status === 'error') {
      row.getCell('J').font = { color: { argb: 'FFFF0000' } };
    }
    if (r.amount && parseFloat(r.amount) > 5000) {
      row.getCell('D').font = { bold: true, color: { argb: 'FF1F3864' } };
    }

    rowNum++;
  }
  s1.getRow(1).freeze = true;

  // ===== Sheet 2: 购买方汇总 =====
  const s2 = workbook.addWorksheet('购买方汇总');
  s2.addRow(['购买方', '发票数量', '有金额数量', '总金额(元)', '备注']);
  const h2 = s2.getRow(1);
  h2.font = { bold: true, color: { argb: 'FFFFFFFF' } };
  h2.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4472C4' } };
  h2.alignment = { horizontal: 'center' };
  s2.getColumn(1).width = 30; s2.getColumn(2).width = 10;
  s2.getColumn(3).width = 10; s2.getColumn(4).width = 14; s2.getColumn(5).width = 20;
  s2.getColumn(4).numFmt = '#,##0.00';

  const byBuyer = {};
  for (const r of records) {
    if (r.buyer) {
      byBuyer[r.buyer] = byBuyer[r.buyer] || { count: 0, withAmt: 0, total: 0, sellers: {} };
      byBuyer[r.buyer].count++;
      if (r.amount) { byBuyer[r.buyer].withAmt++; byBuyer[r.buyer].total += parseFloat(r.amount); }
      if (r.seller) {
        byBuyer[r.buyer].sellers[r.seller] = byBuyer[r.buyer].sellers[r.seller] || { count: 0, total: 0 };
        byBuyer[r.buyer].sellers[r.seller].count++;
        if (r.amount) byBuyer[r.buyer].sellers[r.seller].total += parseFloat(r.amount);
      }
    }
  }

  for (const [buyer, stats] of Object.entries(byBuyer).sort((a, b) => b[1].total - a[1].total)) {
    const rRow = s2.addRow([buyer, stats.count, stats.withAmt, stats.total, '']);
    rRow.font = { bold: true };
    for (const [seller, ss] of Object.entries(stats.sellers).sort((a, b) => b[1].total - a[1].total)) {
      s2.addRow(['', '', '', '', seller + ' ' + ss.count + '张 ¥' + ss.total.toFixed(2)]);
    }
  }

  // ===== Sheet 3: 统计概览 =====
  const s3 = workbook.addWorksheet('统计概览');
  s3.addRow(['指标', '值']); s3.addRow(['生成时间', new Date().toLocaleString('zh-CN')]);
  s3.addRow(['扫描范围', (meta.startDate || '') + ' ~ ' + (meta.endDate || '')]);
  s3.addRow(['总记录', meta.totalRecords]);
  s3.addRow(['有PDF', meta.hasPdf]);
  s3.addRow(['无PDF（链接发票）', meta.noPdf]);
  s3.addRow(['购买方提取', meta.withBuyer]);
  s3.addRow(['销售方提取', meta.withSeller]);
  s3.addRow(['金额提取', meta.withAmount]);
  s3.addRow(['完整三要素', meta.complete]);
  s3.addRow(['需人工确认', meta.needsManual]);
  s3.addRow(['', '']);
  s3.addRow(['=== 金额汇总 ===', '']);
  s3.getColumn(2).numFmt = '#,##0.00';

  const personal = records.filter(r => r.buyer === '个人报销');
  const personalTotal = personal.reduce((s, r) => s + (r.amount ? parseFloat(r.amount) : 0), 0);
  if (personal.length) s3.addRow(['个人报销', personalTotal]);

  const buyerTotals = Object.entries(byBuyer)
    .sort((a, b) => b[1].total - a[1].total)
    .slice(0, 5);
  for (const [buyer, stats] of buyerTotals) {
    s3.addRow([buyer, stats.total]);
  }

  const allTotal = records.reduce((s, r) => s + (r.amount ? parseFloat(r.amount) : 0), 0);
  s3.addRow(['合计（含未识别购买方）', allTotal]);

  s3.getColumn(1).width = 22; s3.getColumn(2).width = 16;
  s3.getRow(1).font = { bold: true };

  // ===== Sheet 4: 人工任务 =====
  const s4 = workbook.addWorksheet('人工任务');
  const manualRecords = records.filter(r => r.needsManualReview);
  if (manualRecords.length > 0) {
    const mCols = [
      ['A', 8, 'UID'],
      ['B', 10, '查看邮件'],
      ['C', 12, '邮件日期'],
      ['D', 12, '待处理类型'],
      ['E', 14, '当前金额'],
      ['F', 30, '当前购买方'],
      ['G', 30, '当前销售方'],
      ['H', 45, '邮件主题'],
      ['I', 40, '备注/链接'],
    ];
    mCols.forEach(([col, width, header]) => {
      s4.getColumn(col).width = width;
    });

    const h4 = s4.addRow(mCols.map(([, , h]) => h));
    h4.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    h4.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFE74C3C' } };
    h4.alignment = { horizontal: 'center' };

    const reasonLabel = {
      'NO_ATTACH_NO_LINK': '无附件无链接',
      'ATTACH_NOT_PDF': '附件非PDF',
      'LINK_NEED_SCAN': '链接需扫码',
      'PDF_PARSE_FAIL': 'PDF解析失败',
      'NO_AMOUNT': '缺金额',
      'NO_BUYER': '缺购买方',
    };

    for (const r of manualRecords) {
      const row = s4.addRow([
        r.emailUid,
        '', // 超链接
        r.emailDate || '',
        reasonLabel[r.manualReason] || r.manualReason || '需确认',
        r.amount || '',
        r.buyer || '',
        r.seller || '',
        r.subject || '',
        r.notes || '',
      ]);

      if (r.emailHyperlink) {
        const linkCell = row.getCell(2);
        linkCell.value = { text: '▶ 查看邮件', hyperlink: r.emailHyperlink };
        linkCell.font = { color: { argb: 'FF0563C1' }, underline: true };
      }

      // 按原因颜色标注
      const colors = {
        'NO_ATTACH_NO_LINK': 'FFFFCDD2',
        'LINK_NEED_SCAN': 'FFFFE0B2',
        'NO_AMOUNT': 'FFFFF9C4',
        'PDF_PARSE_FAIL': 'FFFFAB91',
      };
      const bg = colors[r.manualReason] || 'FFFFF3E0';
      row.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bg } };
    }
    s4.getRow(1).freeze = true;
  } else {
    s4.addRow(['✅ 暂无需人工处理的任务']);
  }

  // ===== 保存 =====
  await workbook.xlsx.writeFile(outputFile);
  console.log('');
  console.log('✅ Excel台账已生成: ' + outputFile);
  console.log('');
  console.log('━━━ 台账内容 ━━━');
  console.log('Sheet1 台账明细: ' + records.length + ' 条（含邮件超链接）');
  console.log('Sheet2 购买方汇总');
  console.log('Sheet3 统计概览');
  console.log('Sheet4 人工任务: ' + manualRecords.length + ' 条');
  console.log('');
  console.log('━━━ 关键金额 ━━━');
  for (const [buyer, stats] of buyerTotals) {
    console.log(buyer + ': ' + stats.count + '张, ¥' + stats.total.toFixed(2));
  }
  if (personal.length) console.log('个人报销: ' + personal.length + '张, ¥' + personalTotal.toFixed(2));
  console.log('合计: ¥' + allTotal.toFixed(2));
}

generateLedger().catch(e => { console.error(e); process.exit(1); });

#!/usr/bin/env node
/**
 * generate.js — Clawed Invoice PDF Generator
 *
 * Usage:
 *   node generate.js --data '{"invoiceNumber":"INV-001",...}'
 *   node generate.js --datafile /path/to/invoice.json
 *   cat invoice.json | node generate.js --datafile /dev/stdin
 *
 * Required JSON fields:
 *   invoiceNumber, invoiceDate, customerNumber, dueDate
 *   customerName, customerAddress
 *   items: [{code, description, qty, net, vatRate, vatAmt, gross}]
 *
 * Optional:
 *   currency (EUR/GBP/USD), entity (key in config), outputDir
 */
const { jsPDF } = require('/data/local/node_modules/jspdf');
const fs   = require('fs');
const path = require('path');

// ── Config ───────────────────────────────────────────────────────────────────
const CONFIG_PATHS = [
  process.env.INVOICE_CONFIG,
  '/data/workspace/skills/clawed-invoice/references/config.json',
];
let config = {};
for (const p of CONFIG_PATHS) {
  try { config = JSON.parse(fs.readFileSync(p, 'utf8')); break; } catch {}
}

// ── Constants ───────────────────────────────────────────────────────────────
const PAGE_W  = 595;
const PAGE_H  = 842;
const LEFT    = 30;
const RIGHT   = 540;   // 55px right buffer
const CW      = RIGHT - LEFT;  // content width

// ── Helpers ──────────────────────────────────────────────────────────────────
const euro = n => '\u20AC ' + String(n);
const gbp  = n => '\u00A3 ' + String(n);
const usd  = n => '$' + String(n);

const fmt = n =>
  parseFloat(n || '0').toLocaleString('en-GB', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

// ── Column layout ────────────────────────────────────────────────────────────
const COL = {
  code:  LEFT,
  desc:  LEFT + 46,
  qty:   LEFT + 266,
  net:   LEFT + 306,
  vat:   LEFT + 381,
  gross: LEFT + 426,
};
const CWIDTH = {
  code:  46,
  desc:  220,
  qty:   40,
  net:   75,
  vat:   45,
  gross: RIGHT - (LEFT + 426),
};

// ── Render ──────────────────────────────────────────────────────────────────
function render(doc, input, entity) {
  const sym = input.currency === 'GBP' ? gbp : input.currency === 'USD' ? usd : euro;

  // ── Palette (from entity or defaults) ────────────────────────────────────
  const [cr, cg, cb] = hexToRgb(entity.headerColor || '#2F3640');
  const [ar, ag, ab] = hexToRgb(entity.accentColor  || '#FFC11E');
  const CHARCOAL = [cr, cg, cb];
  const GOLD     = [ar, ag, ab];
  const WHITE    = [255, 255, 255];
  const BLACK    = [0,   0,   0];
  const DGRAY    = [80,  80,  80];
  const ROW_BG   = [248, 248, 248];

  // ── HEADER ────────────────────────────────────────────────────────────────
  doc.setFillColor(...CHARCOAL);
  doc.rect(0, 0, PAGE_W, 76, 'F');

  doc.setTextColor(...GOLD);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(15);
  doc.text(entity.entity || 'Your Company Ltd', LEFT, 34);

  if (entity.companyNumber) {
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(180, 180, 180);
    doc.text('Company number ' + entity.companyNumber, LEFT, 48);
  }

  doc.setTextColor(...WHITE);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9.5);
  [
    ['Invoice No:',       input.invoiceNumber   || ''],
    ['Invoice date:',     input.invoiceDate     || ''],
    ['Customer No:',     input.customerNumber  || ''],
    ['Payment Due Date:', input.dueDate        || ''],
  ].forEach(([lbl, val], i) => {
    const my = 24 + i * 13;
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(180, 180, 180);
    doc.text(lbl, 360, my);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...WHITE);
    doc.text(val, 470, my);
  });

  // ── BILL TO ──────────────────────────────────────────────────────────────────
  let y = 90;
  doc.setTextColor(...CHARCOAL);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8);
  doc.text('BILL TO', LEFT, y);

  y += 14;
  doc.setTextColor(...BLACK);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(13);
  doc.text(input.customerName || '', LEFT, y);

  y += 14;
  doc.setTextColor(...DGRAY);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(10.5);
  (input.customerAddress || '').split('\n').forEach(l => { doc.text(l, LEFT, y); y += 13; });

  y += 6;  // tight under address
  doc.setDrawColor(...CHARCOAL);
  doc.setLineWidth(2);
  doc.line(LEFT, y, RIGHT, y);

  y += 93;  // space before table

  // ── TABLE HEADER ─────────────────────────────────────────────────────────────
  doc.setFillColor(...CHARCOAL);
  doc.rect(LEFT, y, CW, 22, 'F');

  doc.setTextColor(...WHITE);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8);
  doc.text('Code',              COL.code + 5,          y + 15);
  doc.text('Description',       COL.desc + 5,           y + 15);
  doc.text('Qty',               COL.qty + CWIDTH.qty/2,  y + 15, { align: 'center' });
  doc.text('Amount Due (Net)',  COL.net + CWIDTH.net-6,  y + 15, { align: 'right' });
  doc.text('VAT',               COL.vat + CWIDTH.vat/2,  y + 15, { align: 'center' });
  doc.text('Amount Due (Gross)', RIGHT - 8,               y + 15, { align: 'right' });

  doc.setDrawColor(80, 80, 80);
  doc.setLineWidth(0.5);
  [COL.desc - 3, COL.qty - 3, COL.net - 3, COL.vat - 3].forEach(x => doc.line(x, y, x, y + 22));

  y += 22;
  doc.setLineWidth(1.5);
  doc.line(LEFT, y, RIGHT, y);

  // ── LINE ITEM ROWS ───────────────────────────────────────────────────────────
  const ROW_H  = 36;
  const items  = input.items || [];

  items.forEach(item => {
    const rowMid = y + ROW_H / 2;

    doc.setFillColor(...ROW_BG);
    doc.rect(LEFT, y, CW, ROW_H, 'F');

    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.5);
    [COL.desc - 3, COL.qty - 3, COL.net - 3, COL.vat - 3].forEach(x => doc.line(x, y, x, y + ROW_H));

    // Code
    doc.setTextColor(...CHARCOAL);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.text(item.code || 'SVC', COL.code + 5, rowMid + 3);

    // Description
    doc.setTextColor(...BLACK);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9.5);
    const lines = doc.splitTextToSize(item.description || '', CWIDTH.desc - 10);
    lines.slice(0, 2).forEach((l, i) => doc.text(l, COL.desc + 5, rowMid - 5 + i * 11));
    // Shift first line down to truly center 2 lines in 36px row (rowMid+3 is baseline)
    // For 2-line text in 36px: baseline should be rowMid+4, so line0 at rowMid+4-9=rowMid-5, line1 at rowMid+6

    // Qty
    doc.setTextColor(...DGRAY);
    doc.setFont('helvetica', 'normal');
    doc.text(item.qty || '1', COL.qty + CWIDTH.qty / 2, rowMid + 3, { align: 'center' });

    // Net
    doc.setTextColor(...BLACK);
    doc.setFont('helvetica', 'normal');
    doc.text(sym(fmt(item.net)), COL.net + CWIDTH.net - 6, rowMid + 3, { align: 'right' });

    // VAT
    doc.text(sym(fmt(item.vatAmt || '0.00')), COL.vat + CWIDTH.vat / 2, rowMid + 3, { align: 'center' });

    // Gross
    doc.setFont('helvetica', 'bold');
    doc.text(sym(fmt(item.gross)), RIGHT - 8, rowMid + 3, { align: 'right' });

    y += ROW_H;
    doc.setLineWidth(0.5);
    doc.line(LEFT, y, RIGHT, y);
    doc.setLineWidth(1.5);
    doc.line(LEFT, y, RIGHT, y);
  });

  // ── SUMMARY ──────────────────────────────────────────────────────────────────
  const subtotal = items.reduce((s, i) => s + parseFloat((i.net || '0').replace(',', '')), 0);
  const vatTotal = items.reduce((s, i) => s + parseFloat((i.vatAmt || '0').replace(',', '')), 0);
  const total    = items.reduce((s, i) => s + parseFloat((i.gross || '0').replace(',', '')), 0);

  y += 14;

  const summaries = [
    ['Subtotal (NET):',  sym(fmt(subtotal)),  false],
    ['VAT ' + (items[0]?.vatRate || '0%') + ':', sym(fmt(vatTotal)), false],
    ['Total:',           sym(fmt(total)),   true],
  ];

  summaries.forEach(([label, val, isTotal]) => {
    if (isTotal) {
      doc.setFillColor(...CHARCOAL);
      doc.rect(LEFT, y, CW, 28, 'F');
      doc.setTextColor(...GOLD);
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(11);
      doc.text('Total:', LEFT + 10, y + 19);
      doc.text(val, RIGHT - 10, y + 19, { align: 'right' });
      y += 28;
    } else {
      doc.setTextColor(...DGRAY);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.text(label, 290, y + 8);
      doc.setTextColor(...BLACK);
      doc.setFont('helvetica', 'bold');
      doc.text(val, RIGHT - 10, y + 8, { align: 'right' });
      y += 15;
    }
  });

  // ── PAYMENT DETAILS (footer) ─────────────────────────────────────────────────
  y += 124;
  doc.setDrawColor(180, 180, 180);
  doc.setLineWidth(0.5);
  doc.line(LEFT, y, RIGHT, y);
  y += 10;

  doc.setTextColor(...CHARCOAL);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8.5);
  doc.text('PAYMENT DETAILS', LEFT, y);

  y += 6;
  doc.setFillColor(...WHITE);
  doc.setDrawColor(140, 140, 140);
  doc.rect(LEFT, y, CW, 80, 'S');

  y += 14;
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9.5);
  [
    ['Account holder:', entity.entity     || ''],
    ['Swift/BIC:',      entity.swift      || ''],
    ['IBAN:',           entity.iban        || ''],
  ].forEach(([lbl, val]) => {
    doc.setTextColor(...DGRAY);
    doc.text(lbl, LEFT + 12, y);
    doc.setTextColor(...BLACK);
    doc.setFont('helvetica', 'bold');
    doc.text(val, LEFT + 130, y);
    doc.setFont('helvetica', 'normal');
    y += 16;
  });

  // Footer divider + end — no legal notes
  y += 18;
  doc.setDrawColor(180, 180, 180);
  doc.setLineWidth(0.5);
  doc.line(LEFT, y, RIGHT, y);

  return doc;
}

// ── Colour helper ─────────────────────────────────────────────────────────────
function hexToRgb(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return [r, g, b];
}

// ── CLI Entry Point ─────────────────────────────────────────────────────────
const args = process.argv.slice(2);
let dataArg = null, configPath = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--data'     && i + 1 < args.length) dataArg    = args[++i];
  if (args[i] === '--datafile' && i + 1 < args.length) dataArg    = fs.readFileSync(args[++i], 'utf8');
  if (args[i] === '--config'   && i + 1 < args.length) configPath = args[++i];
}

const input  = JSON.parse(dataArg || '{}');
const entity = { ...config[input.entity || 'default'], ...input };

const doc = new jsPDF({ orientation: 'portrait', unit: 'pt', format: 'a4' });
render(doc, input, entity);

const outDir  = input.outputDir || '/tmp/invoices';
const outNum  = (input.invoiceNumber || 'invoice').replace(/[^a-zA-Z0-9\-_]/g, '_');
fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, `invoice-${outNum}.pdf`);
fs.writeFileSync(outPath, Buffer.from(doc.output('arraybuffer')));
console.log('PDF:', outPath);
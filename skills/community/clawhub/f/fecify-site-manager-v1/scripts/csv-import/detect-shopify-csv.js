/**
 * CSV 格式检测器 — 识别 Shopify 商品导出表格
 * 
 * 用法:
 *   node scripts/csv-import/detect-shopify-csv.js <CSV文件路径>
 * 
 * 输出 JSON: { format, variant, confidence, headers, sample }
 */

const fs = require('fs');

// ── CSV 解析 (处理引号字段) ────────────────────────────
function parseCSV(text, maxRows = Infinity) {
  const rows = [];
  let row = [], field = '', inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQuotes) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') { inQuotes = false; }
      else { field += ch; }
    } else {
      if (ch === '"') { inQuotes = true; }
      else if (ch === ',') { row.push(field); field = ''; }
      else if (ch === '\n') { row.push(field); field = ''; rows.push(row); row = []; if (rows.length >= maxRows) break; }
      else if (ch === '\r') {}
      else { field += ch; }
    }
  }
  if ((row.length > 0 || field) && rows.length < maxRows) { row.push(field); rows.push(row); }
  return rows;
}

// ── Shopify 商品表格特征 ──────────────────────────────

const SHOPIFY_PRODUCT_SIGNATURES = {
  // 核心必含 header（模糊匹配）
  required: ['handle', 'title'],
  // 充分条件 — 满足 3/5 即判定
  strong: [
    'variant price',
    'image src',
    'option1 name',
    'option1 value',
    'body'
  ],
  // 辅助特征
  auxiliary: [
    'vendor', 'tags', 'published', 'variant sku',
    'variant grams', 'variant compare at price', 'seo title',
    'variant inventory qty', 'status'
  ]
};

function headerScore(headers) {
  const lower = headers.map(h => h.toLowerCase().trim());

  // 必须包含 Handle + Title
  const hasRequired = SHOPIFY_PRODUCT_SIGNATURES.required.every(r =>
    lower.some(h => h.includes(r))
  );
  if (!hasRequired) return { match: false, reason: '缺少 Handle 或 Title 列' };

  // 强特征打分
  let strongHits = 0;
  for (const s of SHOPIFY_PRODUCT_SIGNATURES.strong) {
    if (lower.some(h => h.includes(s))) strongHits++;
  }

  // 辅助特征打分
  let auxHits = 0;
  for (const a of SHOPIFY_PRODUCT_SIGNATURES.auxiliary) {
    if (lower.some(h => h.includes(a))) auxHits++;
  }

  const confidence = Math.min(1, (strongHits / 5) * 0.8 + (auxHits / 9) * 0.2);

  return {
    match: strongHits >= 3,
    confidence: Math.round(confidence * 100),
    strongHits,
    auxHits,
    headers: lower,
    extraColumns: lower.filter(h =>
      ![...SHOPIFY_PRODUCT_SIGNATURES.required, ...SHOPIFY_PRODUCT_SIGNATURES.strong, ...SHOPIFY_PRODUCT_SIGNATURES.auxiliary]
        .some(s => h.includes(s))
    )
  };
}

// ── 进一步判断：是否为商品表（排除订单/客户表） ──────
const NON_PRODUCT_SIGNATURES = [
  ['order', 'lineitem'],           // 订单表
  ['customer', 'email', 'phone'],  // 客户表
  ['collection', 'product:'],     // 智能专辑
];

function isProductTable(headers) {
  const lower = headers.map(h => h.toLowerCase());
  for (const sig of NON_PRODUCT_SIGNATURES) {
    if (sig.every(s => lower.some(h => h.includes(s)))) {
      return { product: false, reason: `疑似 ${sig[0]} 表，非商品表` };
    }
  }
  return { product: true };
}

// ── 变体检测 ──────────────────────────────────────────
function detectVariant(rows, headers) {
  const hLower = headers.map(h => h.toLowerCase());
  const hasOpt1Val = hLower.some(h => h.includes('option1 value'));
  const hasOpt2Val = hLower.some(h => h.includes('option2 value'));

  // 列索引
  const handleIdx = hLower.findIndex(h => h.includes('handle'));
  const opt1NameIdx = hLower.findIndex(h => h === 'option1 name');
  const opt1ValIdx = hLower.findIndex(h => h === 'option1 value');
  const opt2NameIdx = hLower.findIndex(h => h === 'option2 name');
  const opt2ValIdx = hLower.findIndex(h => h === 'option2 value');
  const opt3NameIdx = hLower.findIndex(h => h === 'option3 name');
  const opt3ValIdx = hLower.findIndex(h => h === 'option3 value');

  // 判断单规格：变体数=1 且 Option1 Name='Title', Option1 Value='Default Title'，其余 option 列为空
  function isSingleSpec(row) {
    const o1n = (row[opt1NameIdx] || '').trim();
    const o1v = (row[opt1ValIdx] || '').trim();
    const o2n = opt2NameIdx >= 0 ? (row[opt2NameIdx] || '').trim() : '';
    const o2v = opt2ValIdx >= 0 ? (row[opt2ValIdx] || '').trim() : '';
    const o3n = opt3NameIdx >= 0 ? (row[opt3NameIdx] || '').trim() : '';
    const o3v = opt3ValIdx >= 0 ? (row[opt3ValIdx] || '').trim() : '';
    return o1n === 'Title' && o1v === 'Default Title' && !o2n && !o2v && !o3n && !o3v;
  }

  // 按 Handle 分组，逐行判断：Option1 Value 为空 = 图片行，不计入变体
  const handleGroups = {};
  for (let i = 1; i < rows.length; i++) {
    const h = (rows[i][handleIdx] || '').trim();
    if (!h) continue;

    // Option1 Value 为空 → 纯图片行，跳过（不计入变体）
    if (opt1ValIdx >= 0) {
      const o1v = (rows[i][opt1ValIdx] || '').trim();
      if (!o1v) continue;
    }

    if (!handleGroups[h]) handleGroups[h] = { count: 0, singleSpec: true };
    handleGroups[h].count++;
    if (handleGroups[h].singleSpec && !isSingleSpec(rows[i])) {
      handleGroups[h].singleSpec = false;
    }
  }

  const entries = Object.entries(handleGroups);
  const multiVariant = entries.filter(([, g]) => !g.singleSpec).length;
  const singleVariant = entries.length - multiVariant;
  const total = entries.length;
  const hasMultiSpec = multiVariant > 0;

  return {
    multiSpec: hasMultiSpec,
    multiVariantProducts: multiVariant,
    singleVariantProducts: singleVariant,
    totalProducts: total,
    maxVariants: Math.max(0, ...Object.values(handleGroups).map(g => g.count)),
    hasOption1: hasOpt1Val,
    hasOption2: hasOpt2Val
  };
}

// ── 数据校验 ──────────────────────────────────────────

/**
 * 校验规则:
 *  1. handle 必填，title 必填
 *  2. body 可选（可为空）
 *  3. 每个商品首行 Option1 Name 和 Option1 Value 不可都为空
 *  4. 数据行 Option1 Name + Option1 Value 不为空 → Variant Price 必须 > 0
 *  5. 首个图片行 Image Position 必须为 1；后续图片行 Position 依次 2,3,4...；无图片时 Position 必须为空
 */
function validateData(rows, headers) {
  const hLower = headers.map(h => h.toLowerCase());
  const handleIdx = hLower.findIndex(h => h === 'handle');
  const titleIdx = hLower.findIndex(h => h === 'title');
  const priceIdx = hLower.findIndex(h => h === 'variant price');
  const opt1NameIdx = hLower.findIndex(h => h === 'option1 name');
  const opt1ValIdx = hLower.findIndex(h => h === 'option1 value');
  const imgSrcIdx = hLower.findIndex(h => h === 'image src');
  const imgPosIdx = hLower.findIndex(h => h === 'image position');

  // 按 Handle 分组
  const productMap = {};
  const productOrder = [];
  for (let i = 1; i < rows.length; i++) {
    const h = (rows[i][handleIdx] || '').trim();
    if (!h) continue;
    const rowNum = i + 1;
    if (!productMap[h]) { productMap[h] = []; productOrder.push(h); }
    productMap[h].push({ rowNum, row: rows[i] });
  }

  const productIssues = [];

  for (const handle of productOrder) {
    const prodRows = productMap[handle];
    const issues = [];

    // ── 1. Title 必填 ──
    const titleRow = prodRows.find(r => (r.row[titleIdx] || '').trim());
    const title = titleRow ? (titleRow.row[titleIdx] || '').trim() : '';
    if (!title) {
      issues.push({ row: prodRows[0].rowNum, field: 'Title', problem: '必填字段为空' });
    }

    // ── 2. body 可选 ── (不做检测)

    // ── 3. 首行 Option1 Name + Option1 Value 不可为空 ──
    const firstRow = prodRows[0];
    const first_o1n = opt1NameIdx >= 0 ? (firstRow.row[opt1NameIdx] || '').trim() : '';
    const first_o1v = opt1ValIdx >= 0 ? (firstRow.row[opt1ValIdx] || '').trim() : '';
    if (!first_o1n && !first_o1v) {
      issues.push({ row: firstRow.rowNum, field: 'Option1 Name / Option1 Value', problem: '首行不可都为空（该行应为变体行非图片行）' });
    }

    // ── 4. 规格行价格检测 ──
    for (const { rowNum, row } of prodRows) {
      const o1v = (row[opt1ValIdx] || '').trim();
      if (!o1v) continue; // 图片行跳过

      const o1n = opt1NameIdx >= 0 ? (row[opt1NameIdx] || '').trim() : '';
      if (o1n) {
        const price = priceIdx >= 0 ? (row[priceIdx] || '').trim() : '';
        const priceNum = parseFloat(price);
        if (!price || isNaN(priceNum) || priceNum <= 0) {
          issues.push({
            row: rowNum,
            field: 'Variant Price',
            problem: !price ? '为空' : '必须大于 0',
            value: price || ''
          });
        }
      }
    }

    // ── 5. 图片 Position 校验 ──
    let expectedPos = 0;
    for (const { rowNum, row } of prodRows) {
      const imgSrc = imgSrcIdx >= 0 ? (row[imgSrcIdx] || '').trim() : '';
      const imgPos = imgPosIdx >= 0 ? (row[imgPosIdx] || '').trim() : '';

      if (imgSrc && imgSrc.startsWith('http')) {
        expectedPos++;
        if (String(expectedPos) !== imgPos) {
          issues.push({
            row: rowNum,
            field: 'Image Position',
            problem: `应为 ${expectedPos}，实际为 "${imgPos || '(空)'}"`
          });
        }
      } else if (imgSrc && !imgSrc.startsWith('http')) {
        issues.push({ row: rowNum, field: 'Image Src', problem: `不是有效 URL: "${imgSrc.substring(0, 40)}"` });
        // 仍计数，因为可能有有效行
        if (imgPos && imgPos !== '') {
          issues.push({ row: rowNum, field: 'Image Position', problem: `无http图片但Position有值` });
        }
      } else {
        // imgSrc 为空，Position 也必须为空
        if (imgPos && imgPos !== '') {
          issues.push({
            row: rowNum,
            field: 'Image Position',
            problem: `无图片但 Position 有值 ("${imgPos}")`
          });
        }
      }
    }

    if (issues.length > 0) {
      productIssues.push({
        handle,
        title: title || '(empty)',
        totalRows: prodRows.length,
        issues
      });
    }
  }

  const totalIssues = productIssues.reduce((s, p) => s + p.issues.length, 0);

  return {
    totalIssues,
    affectedProducts: productIssues.length,
    details: productIssues
  };
}

// ── 主函数 ────────────────────────────────────────────
function detectCSV(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const rows = parseCSV(text);
  if (rows.length < 2) return { error: 'CSV 为空或行数不足' };

  const headers = rows[0];
  const score = headerScore(headers);

  if (!score.match) return {
    format: 'unknown',
    confidence: score.confidence,
    reason: score.reason || '非 Shopify 商品表格',
    headers
  };

  const productCheck = isProductTable(headers);
  if (!productCheck.product) return {
    format: 'shopify',
    variant: 'non-product',
    confidence: score.confidence,
    reason: productCheck.reason,
    headers
  };

  const variant = detectVariant(rows, headers);
  const issues = validateData(rows, headers);

  return {
    format: 'shopify',
    variant: 'product',
    subType: variant.multiSpec ? 'multi-spec' : 'single-spec',
    confidence: score.confidence,
    totalProducts: variant.totalProducts,
    singleSpecProducts: variant.singleVariantProducts,
    multiSpecProducts: variant.multiVariantProducts,
    maxVariantsPerProduct: variant.maxVariants,
    extraColumns: score.extraColumns,
    dataIssues: issues,
    sample: (() => {
      // 取前 3 个有效的变体行（跳过 Option1 Value 为空的图片行）
      const idx1 = headers.findIndex(h => h.toLowerCase() === 'option1 value');
      const samples = [];
      for (let i = 1; i < rows.length && samples.length < 3; i++) {
        if (idx1 >= 0 && !(rows[i][idx1] || '').trim()) continue; // 跳过图片行
        const obj = {};
        headers.forEach((h, j) => { if (rows[i][j]) obj[h] = (rows[i][j] || '').substring(0, 60); });
        samples.push(obj);
      }
      return samples;
    })()
  };
}

// ── CLI ────────────────────────────────────────────────
if (require.main === module) {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('用法: node scripts/csv-import/detect-shopify-csv.js <CSV文件路径>');
    process.exit(1);
  }
  const result = detectCSV(filePath);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { detectCSV, parseCSV, headerScore, detectVariant, validateData };

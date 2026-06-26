/**
 * Shopify CSV → Fecify 商品导入器
 *
 * 功能:
 *   1. 解析 Shopify 商品导出 CSV(容错多余列)
 *   2. 下载图片 → 上传到 Fecify
 *   3. 构建 Fecify 商品创建 API 请求体
 *   4. 逐商品创建并报告结果(失败自动存档)
 *
 * 用法:
 *   node scripts/csv-import/import-shopify-csv.js <CSV文件路径> [--max=N] [--dry-run]
 *
 *   --max=N                 只导入前 N 个商品（默认全量）
 *   --skip=N                跳过前 N 个商品（配合 --max 截取中间段）
 *   --dry-run               只构建 JSON，不实际调用 API
 *   --use-network-images     不上传图片，直接用 Shopify CDN URL
 *   --gen-tags=none|auto|force  Tag 生成模式（默认 none）
 *     none  - 不生成 tag
 *     auto  - CSV 有则用，无则自动生成
 *     force - 强制生成，覆盖 CSV 中的 tag
 *   --tag-count=N            生成 tag 数量（默认 3）
 *   --img-concurrency=N      图片下载上传并发数（默认 5）
 *   --img-retries=N          图片下载失败最大重试次数（默认 3）
 *   --import-concurrency=N   商品导入并发数（默认 2）
 *   --skip-validation        跳过执行层数据校验（不推荐）
 *   FECIFY_SESSION=xxx       指定会话（同其他 api-call 规则）
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const SKILL_DIR = path.join(__dirname, '..', '..');
const FAIL_DIR = path.join(SKILL_DIR, 'temp', 'failed');
const TEMP_DIR = path.join(SKILL_DIR, 'temp');
const api = require('../base/api-client');

// ═══════════════════════════════════════════════════════
// 0. 并发工具
// ═══════════════════════════════════════════════════════

/**
 * 并发池执行器
 * @param {Array} items - 待处理数据
 * @param {number} concurrency - 最大并发数
 * @param {Function} fn - async (item, index) => result
 * @returns {Promise<Array>} 按原始顺序返回结果
 */
async function concurrentMap(items, concurrency, fn) {
  const results = new Array(items.length);
  let running = 0;
  let nextIdx = 0;

  return new Promise((resolve) => {
    async function run(i) {
      try {
        results[i] = await fn(items[i], i);
      } catch (e) {
        results[i] = { __error: e };
      }
      running--;
      pump();
    }

    function pump() {
      while (running < concurrency && nextIdx < items.length) {
        const i = nextIdx++;
        running++;
        run(i);
      }
      if (running === 0 && nextIdx >= items.length) {
        resolve(results);
      }
    }

    pump();
  });
}

// ═══════════════════════════════════════════════════════
// 1. CSV 解析(引号感知)
// ═══════════════════════════════════════════════════════

function parseCSV(text) {
  const rows = [];
  let row = [], field = '', inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else field += ch;
    } else {
      if (ch === '"') inQuotes = true;
      else if (ch === ',') { row.push(field); field = ''; }
      else if (ch === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else if (ch === '\r') { /* skip */ }
      else field += ch;
    }
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows;
}

// ═══════════════════════════════════════════════════════
// 2. 列映射(容错大小写/引号/多余列)
// ═══════════════════════════════════════════════════════

function buildColumnMap(headers) {
  const map = {};
  const rules = {
    handle: ['handle'],
    title: ['title'],
    bodyHtml: ['body (html)', 'body html', 'body'],
    vendor: ['vendor'],
    type: ['type'],
    tags: ['tags'],
    published: ['published'],
    status: ['status'],
    option1Name: ['option1 name'],
    option1Value: ['option1 value'],
    option2Name: ['option2 name'],
    option2Value: ['option2 value'],
    option3Name: ['option3 name'],
    option3Value: ['option3 value'],
    price: ['variant price'],
    compareAtPrice: ['variant compare at price'],
    costPrice: ['cost per item'],
    sku: ['variant sku'],
    grams: ['variant grams'],
    weightUnit: ['variant weight unit'],
    barcode: ['variant barcode'],
    qty: ['variant inventory qty'],
    imageSrc: ['image src'],
    imagePos: ['image position'],
    imageAlt: ['image alt text'],
    varImage: ['variant image'],
    seoTitle: ['seo title'],
    seoDesc: ['seo description'],
    googleCategory: ['google shopping / google product category'],
    googleType: ['google shopping / google product type']
  };

  const hLower = headers.map(h => h.toLowerCase().trim().replace(/^"|"$/g, ''));
  for (const [key, aliases] of Object.entries(rules)) {
    for (const alias of aliases) {
      const idx = hLower.findIndex(h => h === alias.toLowerCase());
      if (idx !== -1) { map[key] = idx; break; }
    }
  }
  return map;
}

// ═══════════════════════════════════════════════════════
// 3. temp 目录清理(删除超过 7 天的文件)
// ═══════════════════════════════════════════════════════

function cleanupTemp(dir, maxAgeMs = 7 * 24 * 3600_000) {
  if (!fs.existsSync(dir)) return;
  const now = Date.now();
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      cleanupTemp(full, maxAgeMs);
      try { if (fs.readdirSync(full).length === 0) fs.rmdirSync(full); } catch (_) {}
    } else if (e.isFile()) {
      try {
        const stat = fs.statSync(full);
        if (now - stat.mtimeMs > maxAgeMs) {
          fs.unlinkSync(full);
          console.error(`  🧹 清理过期文件: ${e.name}`);
        }
      } catch (_) {}
    }
  }
}

// ═══════════════════════════════════════════════════════
// 4. 保存失败详情
// ═══════════════════════════════════════════════════════

function saveFailure(title, handle, requestBody, response, error) {
  fs.mkdirSync(FAIL_DIR, { recursive: true });
  const ts = new Date().toISOString().replace(/[:.]/g, '-');
  const safe = (handle || 'unknown').replace(/[^a-zA-Z0-9_-]/g, '_').substring(0, 40);
  const file = path.join(FAIL_DIR, `${safe}_${ts}.json`);
  fs.writeFileSync(file, JSON.stringify({
    title,
    handle,
    timestamp: new Date().toISOString(),
    requestBody,
    apiResponse: { code: response.code, message: response.message, _raw: response._raw || '' },
    error: error || ''
  }, null, 2));
  return file;
}

// ═══════════════════════════════════════════════════════
// 5. 按 Handle 分组产品
// ═══════════════════════════════════════════════════════

function groupByHandle(rows, colMap) {
  const products = {};
  const order = [];

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const get = (key) => {
      const idx = colMap[key];
      return (idx !== undefined && idx < row.length) ? (row[idx] || '').trim() : '';
    };

    const handle = get('handle');
    if (!handle) continue;

    if (!products[handle]) {
      order.push(handle);
      products[handle] = {
        title: get('title'),
        handle: handle,
        bodyHtml: get('bodyHtml'),
        vendor: get('vendor'),
        type: get('type'),
        tags: get('tags'),
        published: get('published'),
        status: get('status'),
        seoTitle: get('seoTitle'),
        seoDesc: get('seoDesc'),
        variants: [],
        images: []
      };
    }

    const p = products[handle];

    // 收集图片
    const imgSrc = get('imageSrc');
    const imgPos = get('imagePos');
    if (imgSrc && imgPos) {
      const pos = parseInt(imgPos);
      if (!p.images.find(im => im.position === pos)) {
        p.images.push({ src: imgSrc, position: pos, alt: get('imageAlt') });
      }
    }

    // 变体:Option1 Value 为空的行是图片行,不计入变体
    const o1v = get('option1Value');
    if (o1v) {
      p.variants.push({
        option1: { name: get('option1Name'), value: o1v },
        option2: { name: get('option2Name'), value: get('option2Value') },
        option3: { name: get('option3Name'), value: get('option3Value') },
        price: parseFloat(get('price')) || 0,
        compareAtPrice: parseFloat(get('compareAtPrice')) || 0,
        costPrice: parseFloat(get('costPrice')) || 0,
        sku: get('sku'),
        grams: parseFloat(get('grams')) || 0,
        weightUnit: get('weightUnit') || 'g',
        barcode: get('barcode'),
        qty: parseInt(get('qty')) || 0,
        varImage: get('varImage')
      });
    }
  }

  // 排序图片
  for (const [handle, p] of Object.entries(products)) {
    p.images.sort((a, b) => a.position - b.position);
  }

  return { products, order };
}

// ═══════════════════════════════════════════════════════
// 6. 图片下载 & 上传
// ═══════════════════════════════════════════════════════

function getExt(url) {
  const m = url.match(/\.(\w{3,4})(\?|$)/);
  return m ? m[1] : 'jpg';
}

function downloadImage(url) {
  return new Promise((resolve, reject) => {
    const transport = url.startsWith('https:') ? https : http;
    transport.get(url, { timeout: 30000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadImage(res.headers.location).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      const bufs = [];
      res.on('data', d => bufs.push(d));
      res.on('end', () => resolve(Buffer.concat(bufs)));
    }).on('error', reject).on('timeout', () => reject(new Error('Timeout')));
  });
}

async function uploadImages(images, productTitle, imgConcurrency = 5, imgRetries = 3) {
  const slugify = s => s.replace(/[^a-zA-Z0-9\u4e00-\u9fff-]/g, '_').substring(0, 30);

  const results = await concurrentMap(images, imgConcurrency, async (img) => {
    let lastErr;
    for (let attempt = 0; attempt <= imgRetries; attempt++) {
      const label = attempt > 0 ? `  🔄 重试(${attempt}/${imgRetries}) ${img.src.substring(0, 50)}... ` : '';
      try {
        if (attempt > 0) process.stdout.write(label);
        const buf = await downloadImage(img.src);
        const ext = getExt(img.src);
        const r = await api.post('/api/skill/base-image/upload', {
          image_base64encode: buf.toString('base64'),
          image_name: `${slugify(productTitle)}_${img.position}.${ext}`,
          group_type: 'product'
        });
        if (r.code === 200) {
          return {
            src: r.data.path,
            position: img.position,
            alt: img.alt || '',
            width: r.data.width || 800,
            height: r.data.height || 800,
            ratio: String(r.data.ratio || '1.00')
          };
        }
        lastErr = new Error(r.message || `Upload failed code=${r.code}`);
      } catch (e) {
        lastErr = e;
      }
      // 重试间隔递增: 1s, 2s, 4s
      if (attempt < imgRetries) await sleep(Math.pow(2, attempt) * 1000);
    }
    process.stdout.write(`❌ ${img.src.substring(0, 50)}... ${lastErr.message}\n`);
    return null;
  });

  const uploaded = results.filter(r => r && !r.__error);
  process.stdout.write(`    图片: ${uploaded.length}/${images.length} 张上传成功\n`);
  return uploaded;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ═══════════════════════════════════════════════════════
// 7. Shopify 产品 → Fecify JSON
// ═══════════════════════════════════════════════════════

function genSku(handle, idx) {
  return (handle + '-' + (idx || 0)).substring(0, 64);
}

// ── 执行层校验（导入前过滤无效数据）──
function validateProductForImport(product) {
  const issues = [];
  if (!product.title) {
    issues.push({ field: 'Title', problem: '必填字段为空' });
  }
  // 首行 Option1 Name 和 Option1 Value 不可都为空
  const firstVar = product.variants[0];
  if (firstVar) {
    const o1n = (firstVar.option1?.name || '').trim();
    const o1v = (firstVar.option1?.value || '').trim();
    if (!o1n && !o1v) {
      issues.push({ field: 'Option1 Name / Option1 Value', problem: '首行不可都为空' });
    }
  }
  const validVariants = product.variants.filter(v => {
    const p = parseFloat(v.price);
    return !isNaN(p) && p > 0;
  });
  if (product.variants.length > 0 && validVariants.length === 0) {
    issues.push({ field: 'Variant Price', problem: '所有变体价格为空或 ≤0' });
  }
  return { valid: issues.length === 0, issues, filtered: { ...product, variants: validVariants } };
}

function buildFecifyJSON(product, uploadedImages) {
  // 判断单/多规格:变体数=1 且 Option1='Title'/'Default Title',其余 option 列为空 → 单规格
  const v = product.variants[0];
  const isSingleSpec = v
    && product.variants.length === 1
    && v.option1.name === 'Title' && v.option1.value === 'Default Title'
    && !v.option2.name && !v.option3.name;
  const hasVariants = !isSingleSpec;
  const productType = hasVariants ? 2 : 1;
  const firstImg = uploadedImages.length > 0 ? uploadedImages[0].src : '';

  // 构建 options(多规格)
  const optionMap = {};
  if (hasVariants) {
    for (const v of product.variants) {
      [v.option1, v.option2, v.option3].forEach(opt => {
        if (!opt || !opt.name || !opt.value) return;
        if (!optionMap[opt.name]) optionMap[opt.name] = { name: opt.name, values: new Set() };
        optionMap[opt.name].values.add(opt.value);
      });
    }
  }
  const options = [];
  if (hasVariants) {
    const keys = Object.keys(optionMap);
    for (let i = 0; i < Math.min(keys.length, 3); i++) {
      options.push({
        name: optionMap[keys[i]].name,
        position: i + 1,
        items: [...optionMap[keys[i]].values]
      });
    }
  }

  // 构建 variants（过滤掉价格为空或 ≤0 的变体）
  const variants = product.variants
    .filter(v => { const p = parseFloat(v.price); return !isNaN(p) && p > 0; })
    .map((v, vi) => {
    const variant = {
      price: String(v.price),
      qty: 999,
      weight: String(v.grams || 0),
      weight_unit: v.weightUnit || 'g',
      sku: v.sku || genSku(product.handle, vi),
      image: firstImg,
      option1: '', option2: '', option3: ''
    };
    if (v.compareAtPrice > 0) variant.compare_at_price = String(v.compareAtPrice);
    if (v.costPrice > 0) variant.cost_price = String(v.costPrice);
    if (v.barcode) variant.barcode = v.barcode;
    if (hasVariants) {
      const opts = [v.option1, v.option2, v.option3].filter(Boolean);
      opts.forEach((opt, i) => { if (opt && opt.value) variant[`option${i+1}`] = opt.value; });
    }
    return variant;
  });

  return {
    product: {
      title: product.title,
      body_html: product.bodyHtml || `<p>${product.title}</p>`,
      type: productType,
      status: product.status === 'active' ? 1 : 1,
      handle: product.handle || '',
      inventory_police: 1,
      inventory_police_type: 1,
      variant_need_image: 1,
      vendor: product.vendor || '',
      meta_title: product.seoTitle || product.title
    },
    images: uploadedImages,
    variants,
    options,
    tags: [],
    collection_ids: [],
    videos: [],
    productattr_info: [],
    mergeimages: []
  };
}

// ═══════════════════════════════════════════════════════
// 8. Tag 自动生成
// ═══════════════════════════════════════════════════════

const STOP_WORDS = new Set([
  'the','and','for','with','this','that','from','have','has','had','not',
  'are','was','were','been','can','will','would','could','should','may',
  'its','all','but','our','out','you','your','also','new','use','used',
  'each','set','way','one','two','see','how','get','got','itself','more',
  'about','into','than','them','then','some','over','when','what','which',
  'only','just','like','make','made','come','here','very','too','well',
  'much','now','own','who','his','her','she','him','they','their',
  'dont','isnt','wasnt','werent','didnt','cant','couldnt','wont','shes',
  'hes','ive','youre','were','theyre','a','an','an','is','it','be','at',
  'on','by','or','as','of','to','in','no','if','we','so','my','he','up',
  'do','am','me','us','go','oh','hi','la','de','en','el','et','le','du',
  'est','qui','sed','non','vel','nec','aut','cum','iam'
]);

function extractKeywords(text, maxWords = 30) {
  const words = text.toLowerCase()
    .replace(/<[^>]+>/g, ' ')
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length >= 3 && !STOP_WORDS.has(w) && !/^\d+$/.test(w));

  const freq = {};
  for (const w of words) freq[w] = (freq[w] || 0) + 1;
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, maxWords)
    .map(e => e[0]);
}

function generateTags(title, bodyHtml, count = 3) {
  const titleWords = extractKeywords(title, 10);
  const bodyWords = extractKeywords(bodyHtml || '', 30);

  // 标题词权重更高(放在前面)
  const seen = new Set();
  const ranked = [];
  for (const w of titleWords) {
    if (!seen.has(w)) { ranked.push(w); seen.add(w); }
  }
  for (const w of bodyWords) {
    if (!seen.has(w) && ranked.length < count) { ranked.push(w); seen.add(w); }
  }

  // 格式化为 tag 对象
  return ranked.slice(0, count).map(w => ({
    id: '',
    title: w.charAt(0).toUpperCase() + w.slice(1)
  }));
}

// ═══════════════════════════════════════════════════════
// 9. 主流程
// ═══════════════════════════════════════════════════════

async function main() {
  // 清理超过 7 天的 temp 文件
  cleanupTemp(TEMP_DIR);

  const args = process.argv.slice(2);
  const csvPath = args.find(a => !a.startsWith('--'));
  const maxArg = args.find(a => a.startsWith('--max='));
  const max = maxArg ? parseInt(maxArg.split('=')[1]) : Infinity;
  const skipArg = args.find(a => a.startsWith('--skip='));
  const skip = skipArg ? parseInt(skipArg.split('=')[1]) : 0;
  const skipValidation = args.includes('--skip-validation');
  const dryRun = args.includes('--dry-run');
  const useNetworkImages = args.includes('--use-network-images');

  // 并发参数
  const imgConcArg = args.find(a => a.startsWith('--img-concurrency='));
  const imgConcurrency = imgConcArg ? parseInt(imgConcArg.split('=')[1]) : 5;
  const imgRetriesArg = args.find(a => a.startsWith('--img-retries='));
  const imgRetries = imgRetriesArg ? parseInt(imgRetriesArg.split('=')[1]) : 3;
  const importConcArg = args.find(a => a.startsWith('--import-concurrency='));
  const importConcurrency = importConcArg ? parseInt(importConcArg.split('=')[1]) : 2;

  // Tag 生成
  const tagModeArg = args.find(a => a.startsWith('--gen-tags='));
  const tagMode = tagModeArg ? tagModeArg.split('=')[1] : 'none';
  const tagCountArg = args.find(a => a.startsWith('--tag-count='));
  const tagCount = tagCountArg ? parseInt(tagCountArg.split('=')[1]) : 3;
  if (!['none', 'auto', 'force'].includes(tagMode)) {
    console.error('--gen-tags 可选值: none | auto | force');
    process.exit(1);
  }

  if (!csvPath) {
    console.error('用法: node scripts/csv-import/import-shopify-csv.js <CSV文件> [--max=N] [--dry-run]');
    process.exit(1);
  }

  // 解析 CSV
  const text = fs.readFileSync(csvPath, 'utf8');
  const rows = parseCSV(text);
  if (rows.length < 2) { console.error('CSV 为空'); process.exit(1); }

  const headers = rows[0];
  const colMap = buildColumnMap(headers);

  console.log(`列映射: ${Object.keys(colMap).filter(k => colMap[k] !== undefined).length}/${Object.keys(colMap).length} 个关键列识别成功`);
  if (colMap.handle === undefined || colMap.title === undefined) {
    console.error('❌ 缺少 Handle 或 Title 列,无法识别为 Shopify 商品表');
    process.exit(1);
  }

  const { products, order } = groupByHandle(rows, colMap);
  const total = order.length;
  console.log(`解析完成: ${total} 个商品`);

  if (total === 0) { console.log('无商品数据'); process.exit(0); }

  const count = Math.min(max, total - skip);
  const results = new Array(count);

  console.log(`⚡ 并发配置: 图片上传 ${imgConcurrency} 并发 | 重试 ${imgRetries} 次 | 商品导入 ${importConcurrency} 并发\n`);

  // 构建待处理列表（从 skip 位置开始）
  const productList = [];
  for (let idx = 0; idx < count; idx++) {
    productList.push(skip + idx);
  }

  await concurrentMap(productList, importConcurrency, async (idx) => {
    const handle = order[idx];
    const p = products[handle];
    console.log(`\n[${skip+idx+1}/${total}] ${p.title}`);
    console.log(`  Handle: ${handle} | 变体: ${p.variants.length} | 图片: ${p.images.length}`);

    if (dryRun) {
      const json = buildFecifyJSON(p, []);
      // Dry-run 也展示 tag 预览
      if (tagMode === 'force') {
        json.tags = generateTags(p.title, p.bodyHtml, tagCount);
      } else if (tagMode === 'auto') {
        const csvTags = (p.tags || '').split(',').map(t => t.trim()).filter(Boolean);
        json.tags = csvTags.length > 0
          ? csvTags.map(t => ({ id: '', title: t }))
          : generateTags(p.title, p.bodyHtml, tagCount);
      }
      if (json.tags.length > 0) {
        console.log(`  🏷️  tag 预览: ${json.tags.map(t=>t.title).join(', ')}`);
      }
      const outFile = path.join(TEMP_DIR, `product_${skip+idx+1}.json`);
      fs.mkdirSync(path.dirname(outFile), { recursive: true });
      fs.writeFileSync(outFile, JSON.stringify(json, null, 2));
      console.log(`  📝 DRY-RUN: JSON -> ${outFile}`);
      results[idx] = { handle, title: p.title, status: 'dry-run', file: outFile };
      return;
    }

    // 执行层校验
    if (!skipValidation) {
      const { valid, issues } = validateProductForImport(p);
      if (!valid) {
        const reasons = issues.map(i => `${i.field}: ${i.problem}`).join('; ');
        console.error(`  ❌ 校验失败: ${reasons}`);
        results[idx] = { handle, title: p.title, status: 'skip', reason: reasons };
        return;
      }
    }

    // 图片:上传 or 直接用网络 URL
    let imageList;
    if (useNetworkImages) {
      console.log(`  使用网络图片 (${p.images.length} 张,跳过上传)`);
      imageList = p.images.map(im => ({
        src: im.src,
        position: im.position,
        alt: im.alt || '',
        width: 0,
        height: 0,
        ratio: '1.00'
      }));
      imageList.sort((a, b) => a.position - b.position);
    } else {
      console.log(`  上传 ${p.images.length} 张图片...`);
      imageList = await uploadImages(p.images, p.title, imgConcurrency, imgRetries);
      if (imageList.length === 0) {
        console.error(`  ❌ 无可用图片`);
        const body = buildFecifyJSON(p, []);
        saveFailure(p.title, handle, body, { code: -1, message: 'No images available' }, '');
        results[idx] = { handle, title: p.title, status: 'fail' };
        return;
      }
    }

    const body = buildFecifyJSON(p, imageList);

    // Tag 处理
    if (tagMode === 'force') {
      body.tags = generateTags(p.title, p.bodyHtml, tagCount);
      console.log(`  🏷️  强制生成 ${body.tags.length} 个 tag: ${body.tags.map(t=>t.title).join(', ')}`);
    } else if (tagMode === 'auto') {
      const csvTags = (p.tags || '').split(',').map(t => t.trim()).filter(Boolean);
      if (csvTags.length > 0) {
        body.tags = csvTags.map(t => ({ id: '', title: t }));
        console.log(`  🏷️  使用 CSV tag: ${csvTags.join(', ')}`);
      } else {
        body.tags = generateTags(p.title, p.bodyHtml, tagCount);
        console.log(`  🏷️  CSV 无 tag,自动生成 ${body.tags.length} 个: ${body.tags.map(t=>t.title).join(', ')}`);
      }
    }
    // tagMode === 'none' → 不生成,tags 为空数组

    try {
      console.log(`  创建商品...`);
      const r = await api.post('/api/skill/product/create', body);

      if (r.code === 200) {
        console.log(`  ✅ product_id=${r.data.product_id}`);
        results[idx] = { handle, title: p.title, product_id: r.data.product_id, status: 'ok' };
      } else {
        const failFile = saveFailure(p.title, handle, body, r, '');
        console.error(`  ❌ 失败, 详情: ${failFile}`);
        results[idx] = { handle, title: p.title, status: 'fail' };
      }
    } catch (e) {
      console.error(`  ❌ ${e.message}`);
      const body2 = buildFecifyJSON(p, []);
      saveFailure(p.title, handle, body2, { code: -1, message: e.message }, e.stack || '');
      results[idx] = { handle, title: p.title, status: 'fail' };
    }
  });

  // ════════════════════ 汇总报告 ════════════════════
  const valid = results.filter(Boolean);
  const okCount = valid.filter(r => r.status === 'ok').length;
  const failCount = valid.filter(r => r.status === 'fail').length;
  const dryCount = valid.filter(r => r.status === 'dry-run').length;
  const skipCount = valid.filter(r => r.status === 'skip').length;

  console.log(`\n${'='.repeat(60)}`);
  console.log(`导入汇总: 共 ${count} 个 | 成功 ${okCount} | 失败 ${failCount} | 跳过 ${skipCount}`);
  if (dryCount > 0) console.log(`         Dry-run 预览: ${dryCount} 个`);
  console.log(`${'='.repeat(60)}`);

  // 列出跳过项
  if (skipCount > 0) {
    console.log(`\n⚠️ 跳过商品 (校验未通过):`);
    results.filter(r => r && r.status === 'skip').forEach((r, i) => {
      console.log(`  ${i+1}. ${r.title} (handle: ${r.handle}) — ${r.reason || ''}`);
    });
  }

  // 列出失败项
  if (failCount > 0) {
    console.log(`\n❌ 失败商品 (详情目录: ${FAIL_DIR})`);
    results.filter(r => r && r.status === 'fail').forEach((r, i) => {
      console.log(`  ${i+1}. ${r.title} (handle: ${r.handle})`);
    });
  }

  // 保存汇总
  fs.mkdirSync(TEMP_DIR, { recursive: true });
  const summaryFile = path.join(TEMP_DIR, 'import_results.json');
  fs.writeFileSync(summaryFile, JSON.stringify({
    total: count,
    ok: okCount,
    fail: failCount,
    skip: skipCount,
    dryRun: dryCount > 0,
    failedDir: FAIL_DIR,
    timestamp: new Date().toISOString(),
    items: valid
  }, null, 2));
  console.log(`\n汇总: ${summaryFile}`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });

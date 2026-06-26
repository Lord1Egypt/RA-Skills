#!/usr/bin/env node

/**
 * 1688 商品详情采集器
 * 采集商品图片、标题、价格、SKU、店铺信息等完整数据
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  scrollSteps: 30,        // 滚动步数
  scrollDelay: 400,       // 每步等待时间 (ms)
  scrollStep: 1000,       // 每步滚动距离
  desktopPath: process.env.HOME + '/Desktop'
};

/**
 * 提取商品 ID 从 URL
 */
function extractOfferId(url) {
  const match = url.match(/offer\/(\d+)\.html/);
  return match ? match[1] : null;
}

/**
 * 清理图片 URL，获取原图
 */
function cleanImageUrl(url) {
  if (!url) return null;
  return url
    .replace(/_sum\.jpg$/, '.jpg')
    .replace(/_b\.jpg$/, '.jpg')
    .replace(/_\d+x\d+\.jpg$/, '.jpg')
    .replace(/_\d+q\d+\.jpg$/, '.jpg')
    .replace(/\.jpg\.jpg$/, '.jpg');
}

/**
 * 过滤有效的 1688 图片 URL
 */
function isValid1688Image(url) {
  if (!url) return false;
  return url.includes('cbu01.alicdn.com/img/ibank') &&
         !url.includes('avatar') &&
         !url.includes('_88x88');
}

/**
 * 浏览器函数：深度滚动并收集所有图片
 */
const collectImagesScript = `
async () => {
  const allUrls = new Set();
  
  // 深度滚动触发懒加载
  for (let i = 0; i < ${CONFIG.scrollSteps}; i++) {
    window.scrollBy(0, ${CONFIG.scrollStep});
    await new Promise(r => setTimeout(r, ${CONFIG.scrollDelay}));
    
    // 检查是否到底
    if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
      break;
    }
  }
  
  // 滚动到顶部再到底部
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 500));
  window.scrollTo(0, document.body.scrollHeight);
  await new Promise(r => setTimeout(r, 3000));
  
  // 使用 Performance API 获取所有图片资源（包括详情图）
  const resources = performance.getEntriesByType('resource');
  resources.forEach(r => {
    if (r.name.includes('cbu01.alicdn.com/img/ibank')) {
      const clean = cleanUrl(r.name);
      if (clean) allUrls.add(clean);
    }
  });
  
  // 同时收集 DOM 中的图片
  document.querySelectorAll('img').forEach(img => {
    const src = img.src || img.getAttribute('data-src') || img.getAttribute('original-src');
    if (src && src.includes('cbu01.alicdn.com/img/ibank')) {
      const clean = cleanUrl(src);
      if (clean) allUrls.add(clean);
    }
  });
  
  function cleanUrl(url) {
    return url
      .replace(/\\.webp$/, '.jpg')
      .replace(/_sum\\.jpg$/, '.jpg')
      .replace(/_b\\.jpg$/, '.jpg')
      .replace(/_\\d+x\\d+\\.jpg$/, '.jpg')
      .replace(/_\\d+q\\d+\\.jpg$/, '.jpg')
      .replace(/\\.jpg\\.jpg$/, '.jpg')
      .replace(/_88x88q90/, '');
  }
  
  return Array.from(allUrls).filter(u => {
    if (u.includes('avatar')) return false;
    if (u.includes('_88x88')) return false;
    // 过滤掉平台通用图片 (!!0-0- 开头的是系统图片，不是商品图片)
    if (u.match(/!!0-0-/)) return false;
    return true;
  });
}
`;

/**
 * 浏览器函数：采集商品基本信息
 */
const collectProductInfoScript = `
() => {
  const info = {
    title: '',
    price: '',
    company: '',
    sales: '',
    rating: '',
    location: '',
    attributes: {},
    allAttributes: []  // 保存所有属性（包括字段名和值）
  };
  
  // 标题
  const titleEl = document.querySelector('h1, .title-content h1, [class*="title"]');
  info.title = titleEl?.innerText?.trim() || '';
  
  // 价格
  const priceEl = document.querySelector('[class*="price"], .price-text, span[class*="price"]');
  info.price = priceEl?.innerText?.trim() || '';
  
  // 店铺
  const shopEl = document.querySelector('[class*="shop"], .shop-name, .company-name');
  info.company = shopEl?.innerText?.trim() || '';
  
  // 销量
  const salesEl = document.querySelector('[class*="sales"], .sold-count, [class*="sold"]');
  info.sales = salesEl?.innerText?.trim() || '';
  
  // 发货地
  const locationEl = document.querySelector('[class*="location"], .ship-from, [class*="address"]');
  info.location = locationEl?.innerText?.trim() || '';
  
  // 商品属性 - 专门采集商品属性表格
  // 策略 1: 先尝试通过常见选择器采集
  const selectors = [
    '[class*="attribute"] tr',
    '.attr-row',
    '.detail-feature tr',
    '[class*="feature"] tr',
    '.props tr',
    '[class*="props"] tr',
    '.parameter-table tr',
    '[class*="parameter"] tr',
    '.goods-attr tr',
    '[class*="goods-attr"] tr',
    '.product-params tr',
    '[class*="product-param"] tr'
  ];
  
  const seenKeys = new Set();
  
  // 策略 1: 使用选择器采集
  selectors.forEach(selector => {
    document.querySelectorAll(selector).forEach(row => {
      if (!row.innerText?.trim()) return;
      const cells = row.querySelectorAll('th, td');
      if (cells.length >= 2) {
        const key = cells[0]?.innerText?.trim();
        const val = cells[1]?.innerText?.trim();
        if (key && val && key !== val && key.length < 50 && !seenKeys.has(key)) {
          if (!/^\d+$/.test(key) && !key.startsWith('http')) {
            seenKeys.add(key);
            info.attributes[key] = val;
            info.allAttributes.push({ name: key, value: val });
          }
        }
      }
    });
  });
  
  // 策略 2: 采集页面第一个表格（1688 商品属性表格通常是第一个 table）
  const firstTable = document.querySelector('table');
  if (firstTable) {
    const rows = firstTable.querySelectorAll('tr');
    rows.forEach(row => {
      const cells = row.querySelectorAll('th, td');
      // 1688 属性表格每行可能有 4 个单元格（2 对 key-value）
      if (cells.length >= 2) {
        // 处理第一对
        const key1 = cells[0]?.innerText?.trim();
        const val1 = cells[1]?.innerText?.trim();
        if (key1 && val1 && key1 !== val1 && key1.length < 50 && !seenKeys.has(key1)) {
          if (!/^\d+$/.test(key1) && !key1.startsWith('http')) {
            seenKeys.add(key1);
            info.attributes[key1] = val1;
            info.allAttributes.push({ name: key1, value: val1 });
          }
        }
        // 处理第二对（如果存在）
        if (cells.length >= 4) {
          const key2 = cells[2]?.innerText?.trim();
          const val2 = cells[3]?.innerText?.trim();
          if (key2 && val2 && key2 !== val2 && key2.length < 50 && !seenKeys.has(key2)) {
            if (!/^\d+$/.test(key2) && !key2.startsWith('http')) {
              seenKeys.add(key2);
              info.attributes[key2] = val2;
              info.allAttributes.push({ name: key2, value: val2 });
            }
          }
        }
      }
    });
  }
  
  // 额外采集：品牌、材质、货号等常见字段（如果有独立展示）
  const commonFields = ['品牌', '材质', '货号', '风格', '产地', '规格', '型号', '颜色', '尺寸', '重量'];
  commonFields.forEach(field => {
    if (!info.attributes[field]) {
      // 尝试从页面其他位置查找
      const el = document.querySelector(`[class*="${field}"], [title*="${field}"]`);
      if (el && el.innerText) {
        const text = el.innerText.trim();
        if (text && text.length < 100) {
          info.attributes[field] = text;
          info.allAttributes.push({ name: field, value: text });
        }
      }
    }
  });
  
  return info;
}
`;

/**
 * 主函数：采集 1688 商品
 */
async function scrape1688Product(url, outputPath = null) {
  const offerId = extractOfferId(url);
  if (!offerId) {
    throw new Error('无效的 1688 商品 URL');
  }
  
  console.log(`开始采集商品：${offerId}`);
  
  // 设置输出路径
  const baseName = `1688-商品详情-${offerId}`;
  const imageDir = path.join(outputPath || CONFIG.desktopPath, `${baseName}-图片`);
  const jsonPath = path.join(outputPath || CONFIG.desktopPath, `${baseName}.json`);
  
  // 创建图片文件夹
  if (!fs.existsSync(imageDir)) {
    fs.mkdirSync(imageDir, { recursive: true });
  }
  
  console.log(`图片保存目录：${imageDir}`);
  
  // 这里需要通过 browser 工具执行 JavaScript
  // 实际使用时，这部分代码会在 browser.act 中执行
  const result = {
    offerId,
    url,
    imageDir,
    jsonPath,
    status: 'ready'
  };
  
  console.log('采集准备完成');
  return result;
}

module.exports = {
  scrape1688Product,
  collectImagesScript,
  collectProductInfoScript,
  CONFIG
};

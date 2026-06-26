#!/usr/bin/env node
/**
 * Step 1: 1688 商品抓取（内置实现）
 * 
 * 功能：
 * - 使用 agent-browser 爬取 1688 商品页面
 * - 提取商品主图和详情图（支持 Shadow DOM）
 * - 提取商品信息（标题、属性、SKU）
 * - 调用 OCR 识别图片文字
 * - 调用 LLM 生成中俄双语文案
 * 
 * 输出：
 * - product_info.md - 产品信息
 * - copy_writing.md - 中俄双语文案
 * - copy_writing.json - 结构化文案
 * - ocr_result.md - OCR 结果
 * - image_classification.md - 图片分类
 * - images/ - 所有图片
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const { log, writeProgress, notifyFeishu } = require('./logger');
const { getOutputDir } = require('./workspace');
const { loadConfig } = require('./config');

const OUTPUT_DIR = path.join(getOutputDir(), '1688-tt');
const IMAGES_DIR = path.join(OUTPUT_DIR, 'images');

// 飞书通知标志（通过环境变量传递）
const ENABLE_FEISHU = process.env.ENABLE_FEISHU === 'true';

/**
 * 使用 agent-browser 爬取 1688 页面
 */
function crawl1688Page(url) {
  log('使用 agent-browser 爬取 1688 页面...', 'info');
  
  try {
    // 打开页面
    log(`打开 URL: ${url}`, 'debug');
    execSync(`agent-browser open "${url}"`, { stdio: 'inherit', timeout: 30000 });
    
    // 等待页面加载
    log('等待页面加载...', 'debug');
    execSync('agent-browser wait 3000', { stdio: 'inherit', timeout: 10000 });
    
    // 提取主图
    log('提取主图...', 'debug');
    // 提取主图（从 id="gallery" 获取）
    // 提取主图（从 id="gallery" 获取，过滤 svg/png）
    const mainImagesScript = `(function() { 
      var images = [];
      var gallery = document.getElementById('gallery');
      if (!gallery) {
        return { error: '未找到主图区域 #gallery，请优化 DOM 提取规则' };
      }
      var imgs = gallery.querySelectorAll('img');
      imgs.forEach(function(img) { 
        if (img.src && img.src.indexOf('placeholder') === -1) { 
          var ext = img.src.split('?')[0].toLowerCase();
          if (ext.indexOf('.svg') === -1 && ext.indexOf('.png') === -1) {
            images.push(img.src); 
          }
        } 
      });
      if (images.length === 0) {
        return { error: '#gallery 中无图片，请优化 DOM 提取规则' };
      }
      return images.slice(0, 10);
    })()`;
    
    const mainImagesJson = execSync('agent-browser eval \'' + mainImagesScript.replace(/'/g, "'\\''") + '\'', {
      encoding: 'utf-8',
      timeout: 10000
    });
    const mainResult = JSON.parse(mainImagesJson.trim());
    if (mainResult.error) {
      log(`⚠️ ${mainResult.error}`, 'error');
      throw new Error(mainResult.error);
    }
    const mainImages = mainResult;
    log(`提取到 ${mainImages.length} 张主图`, 'info');
    
    // 提取详情图（从 v-detail-g Shadow DOM）- 2025 新结构
    log('提取详情图...', 'debug');
    const detailImagesScript = `(function() { 
      var images = [];
      // 定位详情区域（新结构：.module-od-product-description）
      var desc = document.querySelector('.module-od-product-description') || document.querySelector('.detail-content') || document.querySelector('.description') || document.querySelector('.tb-detail-desc');
      if (!desc) {
        return { error: '未找到详情区域 .module-od-product-description' };
      }
      // 查找 v-detail-g 元素（新结构）
      var vDetail = document.querySelector('v-detail-g.html-description') || Array.from(desc.querySelectorAll('*')).find(function(el) { return el.tagName.toLowerCase().startsWith('v-detail'); });
      if (!vDetail || !vDetail.shadowRoot) {
        return { error: '未找到 v-detail-g Shadow DOM，请优化 DOM 提取规则' };
      }
      // 提取图片
      var imgs = vDetail.shadowRoot.querySelectorAll('img');
      imgs.forEach(function(img) { 
        if (img.src && img.src.indexOf('placeholder') === -1) { 
          images.push(img.src); 
        } 
      });
      if (images.length === 0) {
        return { error: 'v-detail-g 中无图片，请优化 DOM 提取规则' };
      }
      return images.slice(0, 35);
    })()`;
    
    const detailImagesJson = execSync('agent-browser eval \'' + detailImagesScript.replace(/'/g, "'\\''") + '\'', {
      encoding: 'utf-8',
      timeout: 10000
    });
    const detailResult = JSON.parse(detailImagesJson.trim());
    if (detailResult.error) {
      log(`⚠️ ${detailResult.error}`, 'error');
      throw new Error(detailResult.error);
    }
    const detailImages = detailResult;
    log(`提取到 ${detailImages.length} 张详情图`, 'info');
    
    // 提取 SKU（取第一个）- 无 Shadow DOM
    log('提取 SKU...', 'debug');
    const skuScript = `(function() { 
      var skuContainer = document.getElementById('skuSelection');
      if (skuContainer) {
        var firstSku = skuContainer.querySelector('.expand-view-item .item-label');
        if (firstSku) return { name: firstSku.textContent.trim() };
      }
      return { name: null };
    })()`;
    
    const skuJson = execSync('agent-browser eval \'' + skuScript.replace(/'/g, "'\\''") + '\'', {
      encoding: 'utf-8',
      timeout: 10000
    });
    const skuInfo = JSON.parse(skuJson.trim());
    log(`SKU: ${skuInfo.name || '未找到'}`, 'info');
    
    // 提取商品属性（避免包装信息重复）
    log('提取属性...', 'debug');
    const attrScript = `(function() { 
      var attrContainer = document.querySelector('.ant-descriptions.ant-descriptions-bordered .ant-descriptions-view');
      if (attrContainer) {
        var cells = attrContainer.querySelectorAll('td.ant-descriptions-item-content span.field-value');
        var vals = [];
        cells.forEach(function(c) { 
          var text = c.textContent.trim();
          if (text) vals.push(text);
        });
        return { attributes: vals };
      }
      return { attributes: [] };
    })()`;
    
    const attrJson = execSync('agent-browser eval \'' + attrScript.replace(/'/g, "'\\''") + '\'', {
      encoding: 'utf-8',
      timeout: 10000
    });
    const attrInfo = JSON.parse(attrJson.trim());
    log(`属性: ${attrInfo.attributes.join(', ') || '未找到'}`, 'info');
    
    // 提取商品信息
    log('提取商品信息...', 'debug');
    const productInfoScript = '(function() { var h1 = document.querySelector("h1"); var titleElem = document.querySelector(".title"); var priceElem = document.querySelector(".price"); var skuPriceElem = document.querySelector(".sku-price"); return { title: (h1 ? h1.textContent.trim() : "") || (titleElem ? titleElem.textContent.trim() : "") || "", price: (priceElem ? priceElem.textContent.trim() : "") || (skuPriceElem ? skuPriceElem.textContent.trim() : "") || "" }; })()';
    
    const productInfoJson = execSync('agent-browser eval \'' + productInfoScript.replace(/'/g, "'\\''") + '\'', {
      encoding: 'utf-8',
      timeout: 10000
    });
    const productInfo = JSON.parse(productInfoJson.trim());
    productInfo.skuName = skuInfo.name;
    productInfo.attributes = attrInfo.attributes;
    
    // 关闭页面
    execSync('agent-browser close', { stdio: 'inherit', timeout: 5000 });
    
    return {
      mainImages,
      detailImages,
      productInfo
    };
    
  } catch (error) {
    log(`爬取失败：${error.message}`, 'error');
    throw error;
  }
}

/**
 * 下载图片
 */
/**
 * 下载图片
 * @param {string[]} images - 图片 URL 数组
 * @param {string} outputDir - 输出目录
 * @param {string} prefix - 文件名前缀 (main/detail)
 */
function downloadImages(images, outputDir, prefix = 'image') {
  log(`下载 ${images.length} 张图片到 ${outputDir}...`, 'info');
  
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const downloadedImages = [];
  
  for (let i = 0; i < images.length; i++) {
    const url = images[i];
    const ext = path.extname(url.split('?')[0]) || '.jpg';
    // 命名规则：main_01.jpg, main_02.jpg... / detail_01.jpg, detail_02.jpg...
    const filename = `${prefix}_${String(i + 1).padStart(2, '0')}${ext}`;
    const outputPath = path.join(outputDir, filename);
    
    try {
      log(`下载 ${i + 1}/${images.length}: ${filename}`, 'debug');
      execSync(`curl -L -o "${outputPath}" "${url}"`, { timeout: 30000 });
      downloadedImages.push({ filename, url, path: outputPath });
    } catch (error) {
      log(`下载失败 ${filename}: ${error.message}`, 'warn');
    }
  }
  
  return downloadedImages;
}

/**
 * OCR 识别图片文字
 */
function runOCR(images, config, maxImages = 1) {
  log('执行 OCR 识别...', 'info');
  
  try {
    const { runOCR: runBaiduOCR } = require('./ocr');
    return runBaiduOCR(images, config, maxImages); // 限制 OCR 数量
  } catch (error) {
    log(`OCR 失败：${error.message}`, 'warn');
    return [];
  }
}

/**
 * 生成文案（带重试机制）
 */
function generateCopywriting(productInfo, ocrResults, config) {
  log('生成中俄双语文案...', 'info');
  
  const maxRetries = 2;
  let lastError = null;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      log(`文案生成尝试 ${attempt}/${maxRetries}...`, 'debug');
      const { generateCopywriting: generateWithLLM } = require('./copywriting');
      const result = generateWithLLM(productInfo, ocrResults, config);
      
      // 检查是否返回有效内容
      if (result && result.json && result.json.title?.ru) {
        log(`文案生成成功（第 ${attempt} 次尝试）`, 'success');
        return result;
      }
      
      // 内容为空，记录错误
      lastError = new Error('LLM 返回内容为空');
      log(`文案生成返回内容为空，重试...`, 'warn');
      
    } catch (error) {
      lastError = error;
      log(`文案生成失败（${attempt}/${maxRetries}）：${error.message}`, 'warn');
    }
    
    // 如果不是最后一次尝试，等待 2 秒后重试
    if (attempt < maxRetries) {
      log('等待 2 秒后重试...', 'info');
      execSync('sleep 2', { encoding: 'utf-8' });
    }
  }
  
  // 重试 2 次都失败，检查是否已有结果文件
  const { checkAndReadCopywriting } = require('./copywriting');
  // 尝试查找最新的结果文件
  const tempDir = os.tmpdir();
  const fs = require('fs');
  const files = fs.readdirSync(tempDir).filter(f => f.startsWith('cw-result-'));
  
  for (const file of files.sort().reverse()) {
    const resultFile = path.join(tempDir, file);
    const existing = checkAndReadCopywriting(resultFile);
    if (existing) {
      log('找到已生成的文案，继续流程', 'success');
      return existing;
    }
  }
  
  // 真的没有结果，抛出错误
  const errorMsg = `文案生成失败，已重试 ${maxRetries} 次：${lastError?.message || '未知错误'}`;
  log(errorMsg, 'error');
  throw new Error(errorMsg);
}

/**
 * 执行 1688 商品抓取
 * @param {string} url - 1688 商品链接
 * @param {string} weight - 商品重量
 * @param {string} purchasePrice - 采购价
 * @param {string} shippingCost - 国内运费
 * @param {number} ocrCount - OCR 识别图片数量（默认全部）
 */
function run1688(url, weight, purchasePrice, shippingCost, ocrCount = 999) {
  log('Step 1: 开始抓取 1688 商品信息...', 'info');
  
  try {
    // 确保输出目录存在
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    
    // 加载配置
    const config = loadConfig();
    
    // 飞书通知：开始抓取
    if (ENABLE_FEISHU) {
      notifyFeishu('🔄 1688-to-OZON 开始执行\nStep 1: 正在抓取商品信息...', config);
    }
    
    // 1. 爬取页面
    const { mainImages, detailImages, productInfo } = crawl1688Page(url);
    
    // 2. 下载图片（分别下载主图和详情图）
    const mainDownloaded = downloadImages(mainImages, IMAGES_DIR, 'main');
    const detailDownloaded = downloadImages(detailImages, IMAGES_DIR, 'detail');
    const downloadedImages = [...mainDownloaded, ...detailDownloaded];
    log(`下载完成：${mainDownloaded.length} 张主图 + ${detailDownloaded.length} 张详情图`, 'info');
    
    // 飞书通知：图片下载完成
    if (ENABLE_FEISHU) {
      notifyFeishu(`📥 图片下载完成\n• 主图: ${mainDownloaded.length} 张\n• 详情图: ${detailDownloaded.length} 张\n正在 OCR 识别...`, config);
    }
    
    // 3. OCR 识别（限制数量）
    const ocrLimit = Math.min(ocrCount, downloadedImages.length);
    const ocrResults = runOCR(downloadedImages, config, ocrLimit);
    
    // 飞书通知：OCR 完成
    if (ENABLE_FEISHU && ocrResults.length > 0) {
      notifyFeishu(`🔤 OCR 识别完成\n识别了 ${ocrResults.length} 张图片\n正在生成文案...`, config);
    }
    
    // 4. 生成文案
    let copywritingResult = generateCopywriting(productInfo, ocrResults, config);
    
    // 检查是否需要通过 agent 生成
    let copywriting;
    if (copywritingResult._needAgentGenerate) {
      const { checkAndReadCopywriting, formatMarkdown } = require('./copywriting');
      const existing = checkAndReadCopywriting(copywritingResult._resultFile);
      
      if (existing) {
        copywriting = existing;
      } else {
        // 需要用户通过子代理生成文案
        const errorMsg = `文案需要通过子代理生成。

请执行以下步骤：
1. 读取提示词文件：${copywritingResult._promptFile}
2. 使用子代理生成文案
3. 保存到：${copywritingResult._resultFile}

或者直接让我生成文案。`;
        log(errorMsg, 'error');
        throw new Error('文案未生成：请使用子代理生成文案后重试');
      }
    } else {
      copywriting = copywritingResult;
    }
    
    // 保存产品信息
    const productInfoFile = path.join(OUTPUT_DIR, 'product_info.md');
    const skuInfoText = productInfo.skuName ? `**SKU**: ${productInfo.skuName}\n` : '';
    const attrInfoText = productInfo.attributes?.length > 0 ? `**属性**: ${productInfo.attributes.join(', ')}\n` : '';
    fs.writeFileSync(productInfoFile, `# 产品信息\n\n**标题**: ${productInfo.title}\n**价格**: ${productInfo.price}\n${skuInfoText}${attrInfoText}`);
    
    // 保存文案
    const copywritingFile = path.join(OUTPUT_DIR, 'copy_writing.md');
    fs.writeFileSync(copywritingFile, copywriting.md);
    
    const copywritingJsonFile = path.join(OUTPUT_DIR, 'copy_writing.json');
    fs.writeFileSync(copywritingJsonFile, JSON.stringify(copywriting.json, null, 2));
    
    // 保存 OCR 结果
    const ocrResultFile = path.join(OUTPUT_DIR, 'ocr_result.md');
    fs.writeFileSync(ocrResultFile, '# OCR 识别结果\n\n' + JSON.stringify(ocrResults, null, 2));
    
    // 验证输出文件
    const requiredFiles = ['product_info.md', 'copy_writing.md', 'ocr_result.md'];
    for (const file of requiredFiles) {
      const filePath = path.join(OUTPUT_DIR, file);
      if (!fs.existsSync(filePath)) {
        throw new Error(`缺少必需文件：${file}`);
      }
    }
    
    log('Step 1 完成：1688 商品信息抓取成功', 'success');
    writeProgress(getOutputDir(), 'step1_1688', 'completed', {
      outputDir: OUTPUT_DIR,
      files: requiredFiles,
      images: downloadedImages.length
    });
    
    // 飞书通知：Step 1 完成
    if (ENABLE_FEISHU) {
      notifyFeishu('✅ Step 1 完成：1688 商品抓取成功\n• 图片: ' + downloadedImages.length + ' 张\n• 文案: 已生成\n正在执行 Step 2...', config);
    }
    
    return {
      success: true,
      outputDir: OUTPUT_DIR,
      images: downloadedImages.length
    };
    
  } catch (error) {
    log(`Step 1 失败：${error.message}`, 'error');
    writeProgress(getOutputDir(), 'step1_1688', 'failed', {
      error: error.message
    });
    throw error;
  }
}

module.exports = {
  run1688,
  OUTPUT_DIR,
  IMAGES_DIR
};

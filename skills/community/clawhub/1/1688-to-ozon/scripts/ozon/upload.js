#!/usr/bin/env node
/**
 * OZON Seller API 完整客户端 - 优化版 v2.0
 * 文档：https://docs.ozon.ru/api/seller/zh/
 * 
 * v2.0 优化（2026-03-27）:
 * - ✅ 图片状态检查（/v2/product/pictures/info）
 * - ✅ 导入状态轮询（/v1/product/import/info）
 * - ✅ 错误重试机制（根据错误码智能重试）
 * - ✅ 详细日志记录（progress.json）
 * 
 * v1.1 更新（2026-03-24）:
 * - 智能匹配 category_id 和 type_id
 * - 默认值配置：vat=0, country=Китай, stock=500
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 解决代理环境下无法连接 OZON API 的问题
// 使用 NO_PROXY='*' 绕过系统代理，直接连接 OZON
process.env.NO_PROXY = '*';

const CONFIG_FILE = path.join(__dirname, '../../config/config.json');
const PRODUCTS_DIR = path.join(__dirname, '../data/products');
const MAPPINGS_DIR = path.join(__dirname, '../data/mappings');

const OZON_API_HOST = 'api-seller.ozon.ru';

/**
 * 默认配置
 */
const DEFAULTS = {
  vat: '0',
  country: 'Китай',
  stock: 500,
  package_size: { height: 10, width: 10, depth: 10 },
  colors: ['Серебряный', 'Золотой', 'Красный']
};

/**
 * 重试配置
 */
const RETRY_CONFIG = {
  maxRetries: 3,
  retryDelay: 3000,  // 3 秒
  retryableErrors: ['NETWORK_ERROR', 'TIMEOUT', 'SERVER_ERROR', 'IMAGE_PROCESSING'],
  nonRetryableErrors: ['INVALID_VALUE', 'MISSING_REQUIRED_FIELD', 'UNAUTHORIZED']
};

/**
 * 进度报告配置
 */
const PROGRESS_CONFIG = {
  enabled: true,
  file: null  // 运行时设置
};

/**
 * 加载配置（支持环境变量覆盖）
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('配置文件不存在，请先创建 config/config.json');
    process.exit(1);
  }
  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  
  // 环境变量覆盖
  if (process.env.OZON_CLIENT_ID) {
    config.ozon = config.ozon || {};
    config.ozon.clientId = process.env.OZON_CLIENT_ID;
  }
  if (process.env.OZON_API_KEY) {
    config.ozon = config.ozon || {};
    config.ozon.apiKey = process.env.OZON_API_KEY;
  }
  
  // 展平配置：把 config.ozon 的属性提升到顶层，供 ozonRequest 使用
  if (config.ozon) {
    config.clientId = config.ozon.clientId;
    config.apiKey = config.ozon.apiKey;
    config.client_id = config.ozon.clientId;
    config.api_key = config.ozon.apiKey;
    config.apiHost = config.ozon.apiHost;
    config.defaultCategoryId = config.ozon.defaultCategoryId;
    config.defaultVat = config.ozon.defaultVat;
    config.warehouseId = config.ozon.warehouseId;
    config.defaultStock = config.ozon.defaultStock;
    config.defaultPriceMultiplier = config.ozon.defaultPriceMultiplier;
  }
  
  return config;
}

/**
 * 写入进度报告
 */
function writeProgress(step, status, details = {}) {
  if (!PROGRESS_CONFIG.enabled || !PROGRESS_CONFIG.file) return;
  
  try {
    let progress = {
      startTime: new Date().toISOString(),
      status: 'running',
      steps: []
    };
    
    // 读取现有进度
    if (fs.existsSync(PROGRESS_CONFIG.file)) {
      try {
        progress = JSON.parse(fs.readFileSync(PROGRESS_CONFIG.file, 'utf-8'));
      } catch (e) {
        // 文件损坏，重新创建
      }
    }
    
    // 添加新步骤
    progress.steps.push({
      step: step,
      status: status,
      timestamp: new Date().toISOString(),
      details: details
    });
    
    // 更新状态
    if (status === 'failed') {
      progress.status = 'failed';
      progress.error = details.error || 'Unknown error';
    } else if (step === 'upload_complete' && status === 'success') {
      progress.status = 'completed';
    }
    
    fs.writeFileSync(PROGRESS_CONFIG.file, JSON.stringify(progress, null, 2));
  } catch (e) {
    console.error('⚠️  写入进度报告失败:', e.message);
  }
}

/**
 * 发送 OZON API 请求（带重试）
 */
async function ozonRequest(endpoint, body, config, retryCount = 0) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(body);
    const options = {
      hostname: OZON_API_HOST,
      port: 443,
      path: endpoint,
      method: 'POST',
      headers: {
        'Client-Id': config.clientId || config.client_id,
        'Api-Key': config.apiKey || config.api_key,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          // Debug: 打印完整响应
          if (config.debug) {
            console.log(`[DEBUG] API 响应 (${endpoint}):`, JSON.stringify(result, null, 2));
          }
          
          // 检查错误
          if (result.error) {
            const errorCode = result.error.code || 'UNKNOWN_ERROR';
            
            // 判断是否可重试
            if (retryCount < RETRY_CONFIG.maxRetries && 
                RETRY_CONFIG.retryableErrors.some(e => errorCode.includes(e))) {
              console.log(`⚠️  请求失败 (${errorCode})，${RETRY_CONFIG.retryDelay / 1000}秒后重试 (${retryCount + 1}/${RETRY_CONFIG.maxRetries})`);
              setTimeout(() => {
                ozonRequest(endpoint, body, config, retryCount + 1)
                  .then(resolve)
                  .catch(reject);
              }, RETRY_CONFIG.retryDelay);
              return;
            }
            
            reject(new Error(`API 错误 [${errorCode}]: ${result.error.message || JSON.stringify(result.error)}`));
          } else {
            resolve(result);
          }
        } catch (e) {
          console.error('[DEBUG] 原始响应数据:', data);
          reject(new Error('解析响应失败：' + data));
        }
      });
    });

    req.on('error', (err) => {
      // 网络错误可重试
      if (retryCount < RETRY_CONFIG.maxRetries) {
        console.log(`⚠️  网络错误，${RETRY_CONFIG.retryDelay / 1000}秒后重试 (${retryCount + 1}/${RETRY_CONFIG.maxRetries})`);
        setTimeout(() => {
          ozonRequest(endpoint, body, config, retryCount + 1)
            .then(resolve)
            .catch(reject);
        }, RETRY_CONFIG.retryDelay);
      } else {
        reject(new Error(`网络错误：${err.message}`));
      }
    });

    req.setTimeout(60000, () => {
      req.destroy();
      if (retryCount < RETRY_CONFIG.maxRetries) {
        console.log(`⚠️  请求超时，${RETRY_CONFIG.retryDelay / 1000}秒后重试 (${retryCount + 1}/${RETRY_CONFIG.maxRetries})`);
        setTimeout(() => {
          ozonRequest(endpoint, body, config, retryCount + 1)
            .then(resolve)
            .catch(reject);
        }, RETRY_CONFIG.retryDelay);
      } else {
        reject(new Error('请求超时'));
      }
    });
    
    req.write(postData);
    req.end();
  });
}

/**
 * 上传并检查图片状态（优化：添加图片状态检查）
 */
async function uploadAndVerifyPictures(imageUrls, config) {
  console.log('\n📷 步骤 1: 上传图片');
  writeProgress('upload_pictures', 'started', { count: imageUrls.length });
  
  // 上传所有图片（API 只需要 URL 数组，不需要对象）
  const uploadResult = await ozonRequest('/v1/product/pictures/import', {
    images: imageUrls  // 直接传递 URL 数组：["url1", "url2", ...]
  }, config);
  
  if (!uploadResult.result || !uploadResult.result.pictures) {
    throw new Error('图片上传失败：无响应');
  }
  
  const pictures = uploadResult.result.pictures;
  console.log(`✅ 已提交 ${pictures.length} 张图片`);
  
  // 提取图片 ID
  const pictureIds = pictures.map(p => p.id);
  console.log(`📋 图片 ID: ${pictureIds.join(', ')}`);
  
  // 轮询检查图片状态
  console.log('\n⏳ 等待图片处理完成...');
  const readyUrls = await waitForPicturesReady(pictureIds, config);
  
  writeProgress('upload_pictures', 'completed', { 
    count: readyUrls.length,
    urls: readyUrls
  });
  
  return readyUrls;
}

/**
 * 从本地文件上传图片到 OZON（v3.0 修复：直接上传，不使用外部 URL）
 */
async function uploadLocalPicturesToOzon(imageFiles, sourceDir, config, productId = 0) {
  const pictureIds = [];
  
  for (const file of imageFiles) {
    const filePath = path.join(sourceDir, file);
    
    if (!fs.existsSync(filePath)) {
      console.error(`❌ 文件不存在：${filePath}`);
      continue;
    }
    
    console.log(`  上传：${file}`);
    
    // 读取图片文件并转为 base64
    const imageData = fs.readFileSync(filePath);
    const base64Data = imageData.toString('base64');
    
    // 调用 OZON 图片上传 API
    try {
      const result = await ozonRequest('/v1/product/pictures/import', {
        images: [base64Data],
        product_id: productId
      }, config);
      
      if (result.result && result.result.pictures && result.result.pictures.length > 0) {
        const pictureId = result.result.pictures[0].id;
        pictureIds.push(pictureId);
        console.log(`    ✅ 上传成功，ID: ${pictureId}`);
      } else {
        console.error(`    ❌ 上传失败：${JSON.stringify(result)}`);
      }
    } catch (error) {
      console.error(`    ❌ 上传错误：${error.message}`);
    }
    
    // 避免限流，等待 1 秒
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return pictureIds;
}

/**
 * 轮询检查图片状态
 */
async function waitForPicturesReady(pictureIds, config, timeout = 300000) {
  const startTime = Date.now();
  const checkInterval = 3000;  // 3 秒检查一次
  
  while (Date.now() - startTime < timeout) {
    const result = await ozonRequest('/v2/product/pictures/info', {
      pictures: pictureIds
    }, config);
    
    if (!result.result || !result.result.pictures) {
      throw new Error('查询图片状态失败');
    }
    
    const pictures = result.result.pictures;
    const allReady = pictures.every(p => p.state === 'ready');
    const anyFailed = pictures.some(p => p.state === 'failed');
    
    // 显示进度
    const readyCount = pictures.filter(p => p.state === 'ready').length;
    const pendingCount = pictures.filter(p => p.state === 'pending').length;
    const failedCount = pictures.filter(p => p.state === 'failed').length;
    
    console.log(`   进度：${readyCount} 就绪 / ${pendingCount} 处理中 / ${failedCount} 失败`);
    
    if (allReady) {
      console.log('✅ 所有图片已就绪');
      return pictures.map(p => p.uri);
    }
    
    if (anyFailed) {
      const failed = pictures.filter(p => p.state === 'failed');
      throw new Error(`图片处理失败：${failed.map(p => p.id).join(', ')}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, checkInterval));
  }
  
  throw new Error('等待图片处理超时（5 分钟）');
}

/**
 * 上传商品（优化：添加状态轮询和详细日志）
 */
async function uploadProduct(productId, config, mappingFileFromArgs = null) {
  const mappingFile = mappingFileFromArgs || path.join(MAPPINGS_DIR, `${productId}.json`);
  if (!fs.existsSync(mappingFile)) {
    console.error(`映射文件不存在：${productId}`);
    return null;
  }

  const mapping = JSON.parse(fs.readFileSync(mappingFile, 'utf-8'));
  console.log(`\n🚀 开始上传商品 ${productId}...\n`);
  
  // 设置进度报告文件
  const outputDir = path.dirname(mappingFile);
  PROGRESS_CONFIG.file = path.join(outputDir, 'progress.json');
  writeProgress('start', 'started', { productId, offer_id: mapping.offer_id });
  
  try {
    // 兼容处理
    const ozonProduct = mapping.ozon_product || mapping;

    // 读取图片（应用数量限制：5 主图 +10 详情图）
    // 直接使用 Catbox URL，OZON 会自动下载并处理
    const imageData = await loadImages(mappingFile, {
      maxMainImages: 5,
      maxDetailImages: 10
    });
    
    // loadImages 返回 { all, main, detail } - 都是 URL 数组
    const mainImageUrls = imageData.main || [];  // Catbox URL 数组
    const detailImageUrls = imageData.detail || [];  // Catbox URL 数组
    
    console.log(`📸 图片分配：${mainImageUrls.length} 张主图，${detailImageUrls.length} 张详情图`);
    
    // 步骤 1: 先创建商品（使用 Catbox URL，OZON 会自动下载）
    console.log('\n✨ 步骤 1: 创建商品（使用图床 URL）');
    
    // 合并所有图片（主图 + 详情图），最多 15 张
    const allImageUrls = [...mainImageUrls, ...detailImageUrls].slice(0, 15);
    
    // 设置 primary_image（第一张图）
    if (allImageUrls.length > 0) {
      ozonProduct.primary_image = allImageUrls[0];
      console.log(`✅ 主图 (primary_image): ${allImageUrls[0]}`);
    }

    // 设置 images 数组（所有图片，最多 15 张）
    ozonProduct.images = allImageUrls;
    console.log(`✅ 所有图片 (images): ${allImageUrls.length} 张（主图 + 详情图，最多 15 张）`);

    // 生成富文本详情（使用详情图）
    if (detailImageUrls && detailImageUrls.length > 0) {
      ozonProduct.rich_content = generateRichContent(ozonProduct.description, detailImageUrls);
      console.log(`✅ 富文本详情：${detailImageUrls.length} 张详情图`);
    } else {
      console.log(`⚠️  无详情图，跳过富文本生成`);
    }
    
    // 应用品牌和型号规则
    applyBrandAndModelRules(ozonProduct);
    
    // 应用默认值和智能匹配
    applyDefaultsAndSmartMatch(ozonProduct, productId);
    
    // 保存上传请求
    const requestFile = path.join(outputDir, 'upload-request.json');
    fs.writeFileSync(requestFile, JSON.stringify({ items: [ozonProduct] }, null, 2));
    console.log(`✓ 上传请求已保存：${requestFile}`);
    
    // 创建商品
    writeProgress('create_product', 'started', { offer_id: ozonProduct.offer_id });
    
    console.log('\n🔄 调用 OZON API /v3/product/import...');
    const createResult = await ozonRequest('/v3/product/import', {
      items: [ozonProduct]
    }, config);
    
    console.log('📥 API 响应:', JSON.stringify(createResult).substring(0, 500));
    
    if (!createResult.result || !createResult.result.task_id) {
      console.error('❌ 完整响应:', JSON.stringify(createResult, null, 2));
      throw new Error('创建商品失败：无 task_id');
    }
    
    const taskId = createResult.result.task_id;
    console.log(`✅ 商品创建任务已提交`);
    console.log(`   task_id: ${taskId}`);
    writeProgress('create_product', 'completed', { task_id: taskId });
    
    // 查询导入状态，获取 product_id
    console.log('\n⏳ 步骤 2: 等待导入完成');
    writeProgress('check_import_status', 'started', { task_id: taskId });
    
    const importStatus = await waitForImportComplete(taskId, config);
    
    if (!importStatus.success) {
      throw new Error(`导入失败：${JSON.stringify(importStatus.errors)}`);
    }
    
    const productId_onOzon = importStatus.product_id;
    console.log(`✅ 商品导入成功`);
    console.log(`   product_id: ${productId_onOzon}`);
    writeProgress('check_import_status', 'completed', { product_id: productId_onOzon });
    
    // 回调：记录商品到 ozon-promo 数据库（已移除，技能已整合）
    // TODO: 未来可添加内置数据库支持
    
    // 步骤 3: 设置库存（已禁用，避免 TOO_MANY_REQUESTS 错误）
    console.log('\n📦 步骤 3: 设置库存 - 已禁用');
    console.log('⚠️  库存更新已禁用，请手动在 OZON 卖家后台设置库存');
    writeProgress('update_stocks', 'skipped', { reason: 'disabled' });
    
    // 生成结果
    writeProgress('upload_complete', 'completed', {
      product_id: productId_onOzon,
      offer_id: ozonProduct.offer_id,
      task_id: taskId
    });
    
    // 保存结果
    await saveUploadResult(outputDir, {
      productId_1688: productId,
      productId_onOzon: productId_onOzon,
      offer_id: ozonProduct.offer_id,
      task_id: taskId,
      ozonProduct: ozonProduct
    });
    
    console.log('\n✅ 商品上传完成！');
    return createResult;
    
  } catch (error) {
    console.error('\n❌ 商品上传失败');
    console.error(`   错误：${error.message}`);
    writeProgress('error', 'failed', { error: error.message });
    throw error;
  }
}

/**
 * 加载图片（带数量限制）
 * v2.9 返回：{ all: string[], main: string[], detail: string[] }
 */
async function loadImages(mappingFile, options = {}) {
  const { maxMainImages = 5, maxDetailImages = 10 } = options;
  
  const outputDir = path.dirname(mappingFile);
  
  // 读取 ozon-image-translator/images.json
  // 优先级：outputDir/ozon-image-translator > 主目录 > 兼容路径
  let inputDir = path.join(outputDir, 'ozon-image-translator');
  if (!fs.existsSync(inputDir)) {
    inputDir = path.join(path.dirname(outputDir), 'ozon-image-translator');
  }
  
  const imagesJsonPath = path.join(inputDir, 'images.json');
  console.log(`📂 读取图片目录: ${inputDir}`);
  
  if (fs.existsSync(imagesJsonPath)) {
    let imageData = JSON.parse(fs.readFileSync(imagesJsonPath, 'utf-8'));
    
    // v2.9 兼容：支持旧格式（URL 数组）和新格式（对象数组）
    let mainImages, detailImages, otherImages, allImages;
    
    if (Array.isArray(imageData) && typeof imageData[0] === 'string') {
      // 旧格式：["url1", "url2", ...]
      // 过滤掉 null 值
      allImages = imageData.filter(url => url && typeof url === 'string');
      if (allImages.length < imageData.length) {
        console.log(`  ⚠️  过滤掉 ${imageData.length - allImages.length} 个无效 URL`);
      }
      console.log(`✓ 找到翻译后图片：${allImages.length} 张（旧格式）`);
      
      // 应用数量限制（根据 URL 中的文件名判断主图/详情图）
      mainImages = allImages.filter(url => url.includes('main_ru_')).slice(0, maxMainImages);
      detailImages = allImages.filter(url => url.includes('detail_ru_')).slice(0, maxDetailImages);
      otherImages = allImages.filter(url => !url.includes('main_ru_') && !url.includes('detail_ru_'));
    } else {
      // 新格式：[{fileName, url, isMain, isDetail}, ...] 或 [{filename, url, originalFilename, noText}, ...]
      console.log(`✓ 找到翻译后图片：${imageData.length} 张（新格式）`);
      
      // 应用数量限制（根据 isMain/isDetail 判断，或兼容 step2-img.js 格式）
      // 返回 url（图床 URL），OZON 从 URL 下载图片
      let mainImageData, detailImageData, otherImageData;
      
      // 检查是否是 step2-img.js 格式（没有 isMain/isDetail 字段）
      const isStep2Format = imageData.length > 0 && !('isMain' in imageData[0]) && !('isDetail' in imageData[0]);
      
      // 过滤掉 url 为 null 的图片（防止 OZON API 返回 "invalid value for string field images: null"）
      const validImageData = imageData.filter(img => img && img.url);
      if (validImageData.length < imageData.length) {
        console.log(`  ⚠️  过滤掉 ${imageData.length - validImageData.length} 张无效图片（url 为 null）`);
      }
      
      if (isStep2Format) {
        // step2-img.js 格式：{filename, url, originalFilename, noText}
        // 基于 filename 判断主图/详情图（main_*.jpg 为主图，detail_*.jpg 为详情图）
        console.log(`  📋 检测到 step2-img.js 格式，基于 filename 区分主图/详情图`);
        mainImageData = validImageData.filter(img => img.filename?.startsWith('main_')).slice(0, maxMainImages);
        detailImageData = validImageData.filter(img => img.filename?.startsWith('detail_')).slice(0, maxDetailImages);
        otherImageData = [];
      } else {
        // 标准格式：{fileName, url, isMain, isDetail}
        mainImageData = validImageData.filter(img => img.isMain).slice(0, maxMainImages);
        detailImageData = validImageData.filter(img => img.isDetail).slice(0, maxDetailImages);
        otherImageData = validImageData.filter(img => !img.isMain && !img.isDetail);
      }
      
      mainImages = mainImageData.map(img => img.url);
      detailImages = detailImageData.map(img => img.url);
      otherImages = otherImageData.map(img => img.url);
      allImages = validImageData.map(img => img.url);
    }
    
    const skippedMain = (Array.isArray(imageData[0]) ? imageData.filter(url => url.includes('main_ru_')).length : imageData.filter(img => img.isMain).length) - mainImages.length;
    const skippedDetail = (Array.isArray(imageData[0]) ? imageData.filter(url => url.includes('detail_ru_')).length : imageData.filter(img => img.isDetail).length) - detailImages.length;
    
    if (skippedMain > 0 || skippedDetail > 0) {
      console.log(`⚠️  应用数量限制:`);
      console.log(`   主图：${mainImages.length} 张${skippedMain > 0 ? ` (跳过${skippedMain}张)` : ''}`);
      console.log(`   详情图：${detailImages.length} 张${skippedDetail > 0 ? ` (跳过${skippedDetail}张)` : ''}`);
    }
    
    // v2.9 返回分离的图片 URL
    return {
      all: [...mainImages, ...detailImages, ...otherImages],
      main: mainImages,
      detail: detailImages
    };
  }
  
  throw new Error('未找到图片文件：images.json');
}

/**
 * 轮询查询导入状态（优化：详细日志）
 * 
 * 重要说明：
 * - item.errors: 真正的错误，会导致导入失败
 * - item.warnings: 警告/建议，不影响导入成功
 * - 只有 status='failed' 才表示导入失败
 */
async function waitForImportComplete(taskId, config, timeout = 300000) {
  const startTime = Date.now();
  const checkInterval = 3000;  // 3 秒检查一次
  let lastStatus = 'unknown';
  
  while (Date.now() - startTime < timeout) {
    const result = await ozonRequest('/v1/product/import/info', { task_id: taskId }, config);
    
    if (!result.result || !result.result.items || result.result.items.length === 0) {
      throw new Error('查询导入状态失败');
    }
    
    const item = result.result.items[0];
    const status = item.status;
    
    if (status !== lastStatus) {
      console.log(`   当前状态：${status}`);
      lastStatus = status;
    }
    
    // 记录警告（但不影响成功）
    if (item.warnings && item.warnings.length > 0 && status === 'imported') {
      console.log(`\n⚠️  导入成功，但有 ${item.warnings.length} 条警告:`);
      item.warnings.forEach((w, i) => {
        console.log(`   ${i + 1}. ${w.description || w.message || JSON.stringify(w)}`);
      });
      console.log(`   提示：警告不影响商品上架，可通过 /v1/product/attributes/update 更新属性消除\n`);
    }
    
    if (status === 'imported' && item.product_id && item.product_id > 0) {
      // 额外等待 10 秒，确保商品索引完全建立（避免 PRODUCT_IS_NOT_CREATED 错误）
      console.log('   等待商品索引建立（10 秒）...');
      await new Promise(resolve => setTimeout(resolve, 10000));
      
      return {
        success: true,
        product_id: item.product_id,
        warnings: item.warnings || []
      };
    } else if (status === 'failed') {
      return {
        success: false,
        errors: item.errors || ['Unknown error']
      };
    }
    
    // 继续等待：pending, running, creating 等状态
    await new Promise(resolve => setTimeout(resolve, checkInterval));
  }
  
  throw new Error('等待导入完成超时（5 分钟）');
}

/**
 * 保存上传结果
 */
async function saveUploadResult(outputDir, data) {
  const resultFile = path.join(outputDir, 'upload_result.md');
  const resultContent = `# OZON 上传结果

## 基本信息
- 商品 ID (1688): ${data.productId_1688}
- 商品 ID (OZON): ${data.productId_onOzon || '待确认'}
- Offer ID: ${data.offer_id}
- 上传时间: ${new Date().toISOString()}

## 上传状态
- Task ID: ${data.task_id || 'N/A'}
- 状态: ${data.task_id ? '✅ 成功' : '❌ 失败'}

## 商品信息
- 标题: ${data.ozonProduct.name}
- 价格: ¥${data.ozonProduct.price} CNY（OZON 签约货币）
- 分类 ID: ${data.ozonProduct.description_category_id}
- 类型 ID: ${data.ozonProduct.type_id}
- 图片数量: ${data.ozonProduct.images?.length || 0} 张
- 富文本详情: ${data.ozonProduct.rich_content ? '有' : '无'}

## 详细日志
- 进度文件：progress.json
- 请求文件：upload-request.json
`;
  fs.writeFileSync(resultFile, resultContent);
  console.log(`✓ 上传结果已保存：${resultFile}`);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 动态映射属性 - 根据 toy_set_mapping.json 自动生成所有属性
 * @param {Object} mappingResult - mapping_result.json 数据
 * @param {string} productId - 产品类型ID (如 toy_set)
 */
function dynamicMapAttributes(mappingResult, productId) {
  const mappingFile = path.join(MAPPINGS_DIR, `${productId}.json`);
  if (!fs.existsSync(mappingFile)) {
    console.warn(`⚠️  映射配置文件不存在：${productId}`);
    return [];
  }
  
  const mappingConfig = JSON.parse(fs.readFileSync(mappingFile, 'utf-8'));
  const fields = mappingConfig.fields || {};
  const attributes = [];
  
  console.log(`\n🔄 动态映射属性（根据 ${productId}.json 共 ${Object.keys(fields).length} 个字段）...`);
  
  // 遍历所有字段配置
  for (const [fieldName, fieldConfig] of Object.entries(fields)) {
    const attrId = fieldConfig.ozon_attribute_id;
    if (!attrId) continue; // 跳过非属性字段（如 name, price）
    
    // 从 mapping_result 获取值
    let value = mappingResult[fieldName];
    
    // 应用 fallback
    if ((value === undefined || value === null || value === '') && fieldConfig.fallback) {
      value = fieldConfig.fallback;
    }
    
    // 跳过空值
    if (value === undefined || value === null || value === '') {
      continue;
    }
    
    // 数组处理（hashtags 等）
    if (Array.isArray(value)) {
      value = value.join(' ');
    }
    
    // 添加属性
    attributes.push({
      id: attrId,
      values: [{ value: String(value) }]
    });
    
    console.log(`   ✅ 属性 ${attrId} (${fieldName}): ${String(value).substring(0, 30)}...`);
  }
  
  console.log(`📋 动态映射完成：${attributes.length} 个属性\n`);
  return attributes;
}

/**
 * 应用品牌和型号规则
 */
function applyBrandAndModelRules(ozonProduct) {
  // 使用动态映射替换手动映射
  const productId = ozonProduct.type_id === 970895715 ? 'toy_set' : 'default';
  
  // 先尝试动态映射
  const dynamicAttrs = dynamicMapAttributes(ozonProduct, productId);
  
  // 合并到现有 attributes
  if (dynamicAttrs.length > 0) {
    for (const attr of dynamicAttrs) {
      const existingIndex = ozonProduct.attributes.findIndex(a => a.id === attr.id);
      if (existingIndex !== -1) {
        ozonProduct.attributes[existingIndex] = attr;
      } else {
        ozonProduct.attributes.push(attr);
      }
    }
  }
  
  // 以下保留原有逻辑（向后兼容）
  // 处理颜色 - 属性 ID 10096（使用默认值）
  const colorValue = ozonProduct.color || 'Синий';
  const colorAttrIndex = ozonProduct.attributes.findIndex(attr => attr.id === 10096);
  if (colorAttrIndex !== -1) {
    ozonProduct.attributes[colorAttrIndex].values = [{ value: colorValue }];
  } else {
    ozonProduct.attributes.push({ id: 10096, values: [{ value: colorValue }] });
  }
  console.log(`✅ 颜色（属性10096）：${colorValue}`);
  const brandAttrIndex = ozonProduct.attributes.findIndex(attr => attr.id === 4871);
  if (brandAttrIndex !== -1) {
    ozonProduct.attributes.splice(brandAttrIndex, 1);
  }

  // 生成型号
  const modelNumber = generateModelNumber();
  const modelAttrIndex = ozonProduct.attributes.findIndex(attr => attr.id === 9048);
  if (modelAttrIndex !== -1) {
    ozonProduct.attributes[modelAttrIndex].values = [{ value: modelNumber }];
  } else {
    ozonProduct.attributes.push({
      id: 9048,
      values: [{ value: modelNumber }]
    });
  }

  // 提取尺寸
  const dimensions = extractDimensions(ozonProduct.description);
  if (dimensions) {
    const sizeAttrIndex = ozonProduct.attributes.findIndex(attr => attr.id === 4298);
    const sizeValue = `${dimensions.length}x${dimensions.width}x${dimensions.height}`;
    if (sizeAttrIndex !== -1) {
      ozonProduct.attributes[sizeAttrIndex].values = [{ value: sizeValue }];
    } else {
      ozonProduct.attributes.push({
        id: 4298,
        values: [{ value: sizeValue }]
      });
    }
    
    ozonProduct.length = Math.round(dimensions.length * 10);
    ozonProduct.width = Math.round(dimensions.width * 10);
    ozonProduct.height = Math.round(dimensions.height * 10);
    ozonProduct.depth = Math.round(dimensions.height * 10);
    ozonProduct.dimension_unit = 'mm';
  }

  // 处理原产国 - 属性 ID 4389 (Страна происхождения)
  const countryValue = ozonProduct.country || DEFAULTS.country;
  if (countryValue) {
    const countryAttrIndex = ozonProduct.attributes.findIndex(attr => attr.id === 4389);
    if (countryAttrIndex !== -1) {
      ozonProduct.attributes[countryAttrIndex].values = [{ value: countryValue }];
    } else {
      ozonProduct.attributes.push({
        id: 4389,
        values: [{ value: countryValue }]
      });
    }
    console.log(`✅ 原产国（属性4389）：${countryValue}`);
  }

  // 输出尺寸日志
  if (typeof sizeValue !== 'undefined') {
    console.log(`尺寸：${sizeValue} cm`);
    console.log(`包装尺寸：${ozonProduct.length}×${ozonProduct.width}×${ozonProduct.height} mm`);
  }

  console.log(`品牌：（移除，使用 OZON 类目默认值）`);
  console.log(`型号：${modelNumber}`);
  
  return ozonProduct;
}

function generateModelNumber() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  return `oc#${year}_${month}_${day}-${hours}_${minutes}_${seconds}`;
}

function extractDimensions(description) {
  if (!description) return null;
  const regex = /(\d+(?:[.,]\d+)?)\s*×\s*(\d+(?:[.,]\d+)?)\s*×\s*(\d+(?:[.,]\d+)?)\s*(?:cm)?/;
  const match = description.match(regex);
  if (match) {
    return {
      length: parseFloat(match[1].replace(',', '.')),
      width: parseFloat(match[2].replace(',', '.')),
      height: parseFloat(match[3].replace(',', '.'))
    };
  }
  return null;
}

/**
 * 应用默认值和智能匹配
 */
function applyDefaultsAndSmartMatch(product, productId) {
  if (!product.vat) product.vat = DEFAULTS.vat;
  // 原产国默认值
  if (!product.country) product.country = DEFAULTS.country;
  if (!product.stock) product.stock = DEFAULTS.stock;
  if (!product.height) product.height = DEFAULTS.package_size.height;
  if (!product.width) product.width = DEFAULTS.package_size.width;
  if (!product.depth) product.depth = DEFAULTS.package_size.depth;
  if (!product.dimension_unit) product.dimension_unit = 'cm';
  
  if (!product.color) {
    const randomColor = DEFAULTS.colors[Math.floor(Math.random() * DEFAULTS.colors.length)];
    product.color = randomColor;
    console.log(`未找到颜色信息，使用默认颜色：${randomColor}`);
  }
  
  if (!product.description_category_id || product.description_category_id === '待确认') {
    throw new Error(`未找到 description_category_id`);
  }
  
  if (!product.type_id || product.type_id === '待确认') {
    throw new Error(`未找到 type_id`);
  }
  
  if (!product.currency) {
    product.currency = 'CNY';
    console.log(`✓ 货币：${product.currency}`);
  }
  
  return product;
}

/**
 * 更新库存
 */
async function updateStocks(config, stocks) {
  return ozonRequest('/v2/products/stocks', { stocks }, config);
}

/**
 * 生成富文本详情
 */
function generateRichContent(description, detailImages) {
  const content = [];
  for (const imgUrl of detailImages) {
    content.push({
      widgetName: 'raImageBlock',
      img: { src: imgUrl, srcMobile: imgUrl, width: 800, height: 800 }
    });
  }
  return { content, version: '0.3' };
}

// ============================================
// CLI 入口
// ============================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const config = loadConfig();
  
  // 解析 debug 参数
  const debugIdx = args.indexOf('--debug');
  if (debugIdx > -1) {
    config.debug = true;
    console.log('🐛 Debug 模式已开启');
  }

  switch (command) {
    case 'upload':
      if (!args[1]) {
        console.error('用法：upload <product_id> --mapping <file>');
        process.exit(1);
      }
      const mappingIdx = args.indexOf('--mapping');
      const mappingFile = mappingIdx > -1 && args[mappingIdx + 1] ? args[mappingIdx + 1] : null;
      await uploadProduct(args[1], config, mappingFile);
      break;
    
    case 'auto':
      // 动态获取当前 workspace（支持多 agent）
      const ROOT_DIR = path.join(__dirname, '../../..');
      const WORKSPACE_DIR = process.env.WORKSPACE_DIR || process.cwd(); // 支持 WORKSPACE_DIR 环境变量
      
      // 支持多种路径（按优先级）：
      // 1. 1688-to-ozon/mapping_result.json (新架构)
      // 2. ozon-publisher/input/mapping_result.json (兼容)
      // 3. projects/ozon-publisher/input/mapping_result.json (旧兼容)
      let mappingFileAuto = path.join(WORKSPACE_DIR, '1688-to-ozon/mapping_result.json');
      if (!fs.existsSync(mappingFileAuto)) {
        mappingFileAuto = path.join(WORKSPACE_DIR, 'ozon-publisher/input/mapping_result.json');
        if (!fs.existsSync(mappingFileAuto)) {
          mappingFileAuto = path.join(WORKSPACE_DIR, 'projects/ozon-publisher/input/mapping_result.json');
          if (!fs.existsSync(mappingFileAuto)) {
            console.error(`错误：映射文件不存在：${mappingFileAuto}`);
            process.exit(1);
          }
        }
      }
      console.log(`📂 使用映射文件: ${mappingFileAuto}`);
      
      if (!fs.existsSync(mappingFileAuto)) {
        console.error(`错误：映射文件不存在：${mappingFileAuto}`);
        process.exit(1);
      }
      
      console.log('🚀 自动上传模式');
      console.log(`📁 映射文件：${mappingFileAuto}`);
      const mapping = JSON.parse(fs.readFileSync(mappingFileAuto, 'utf-8'));
      const productId = mapping.offer_id || 'auto';
      await uploadProduct(productId, config, mappingFileAuto);
      break;

    default:
      console.log(`
OZON Seller API 客户端 v2.0 (优化版)

命令:
  upload <product_id>         上传商品
  auto                        自动上传（从 input 目录）

优化:
  ✅ 图片状态检查
  ✅ 导入状态轮询
  ✅ 错误重试机制
  ✅ 详细日志记录
`);
  }
}

main().catch(console.error);

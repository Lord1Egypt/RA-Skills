#!/usr/bin/env node
/**
 * Step 2: 图片翻译
 * 
 * 框架逻辑：
 * - 从 1688 直接下载主图(main_xx)和详情图(detail_xx)
 * - 按顺序选择需要翻译的图片：从 main_01 开始，不足用 detail 补充
 * - 图片无文本则直接复制，重命名添加 _ru 后缀
 * - 有文本则调用象寄 API 翻译
 * - 输出目录 ozon-image-translator/images/ 全部是翻译后的图片
 * 
 * 输出：
 * - images.json - 图片 URL 列表
 * - images/ - 翻译后的图片
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { execSync } = require('child_process');
const { log, writeProgress } = require('./logger');
const { getOutputDir } = require('./workspace');
const { loadConfig } = require('./config');

const OUTPUT_DIR = path.join(getOutputDir(), 'ozon-image-translator');
const IMAGES_DIR = path.join(OUTPUT_DIR, 'images');

// 可配置：翻译图片数量（默认15张）
const DEFAULT_MAX_TRANSLATE = 15;

/**
 * 执行图片翻译
 */
async function runImageTranslator(maxTranslate = DEFAULT_MAX_TRANSLATE) {
  log(`Step 2: 开始翻译图片（最多 ${maxTranslate} 张）...`, 'info');
  
  try {
    // 加载配置
    const config = loadConfig();
    const productUrl = config.lastUrl || '';
    
    // 确保输出目录存在
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    if (!fs.existsSync(IMAGES_DIR)) {
      fs.mkdirSync(IMAGES_DIR, { recursive: true });
    }
    
    // ========== 步骤1: 获取 1688 商品图片 ==========
    log('📥 从 1688 下载商品图片...', 'info');
    
    // 从 1688-tt 获取已有的图片（主图+详情图）
    const sourceImagesDir = path.join(getOutputDir(), '1688-tt', 'images');
    if (!fs.existsSync(sourceImagesDir)) {
      // 如果没有图片，尝试从 1688 下载
      log('从 1688-tt 获取图片失败，尝试直接下载...', 'warn');
      // 这里复用 step1 的下载逻辑（简化处理）
    }
    
    // 读取已下载的图片
    const mainImages = [];
    const detailImages = [];
    
    if (fs.existsSync(sourceImagesDir)) {
      const files = fs.readdirSync(sourceImagesDir).sort();
      for (const f of files) {
        if (/^main_\d+\.(jpg|jpeg|png|webp)$/i.test(f)) {
          mainImages.push({ filename: f, path: path.join(sourceImagesDir, f) });
        } else if (/^detail_\d+\.(jpg|jpeg|png|webp)$/i.test(f)) {
          detailImages.push({ filename: f, path: path.join(sourceImagesDir, f) });
        }
      }
    }
    
    log(`找到图片：${mainImages.length} 张主图，${detailImages.length} 张详情图`, 'info');
    
    // ========== 步骤2: 按顺序选择需要处理的图片 ==========
    // 优先取主图，主图取完才取详情图，确保总数 = maxTranslate
    // 始终保留至少 1 张详情图用于富文本（除非详情图不足）
    // 示例：5 主图 + 15 详情图，t6 → 5 主 + 1 详情 = 6 张
    // 示例：2 主图 + 15 详情图，t6 → 2 主 + 4 详情 = 6 张
    const minDetail = 1;  // 始终保留 1 张详情图用于富文本
    const maxMainAllowed = maxTranslate - minDetail;  // 主图最多允许数量
    
    const selectedMain = mainImages.slice(0, maxMainAllowed);
    const detailCount = Math.min(maxTranslate - selectedMain.length, detailImages.length);
    const selectedDetail = detailImages.slice(0, detailCount);
    const imagesToProcess = [...selectedMain, ...selectedDetail];
    
    log(`图片分配：${selectedMain.length} 张主图 + ${selectedDetail.length} 张详情图（富文本用）`, 'info');
    
    log(`准备处理 ${imagesToProcess.length} 张图片（${mainImages.length} 主图 + ${detailImages.length} 详情图）`, 'info');
    
    // ========== 步骤3: 方案1 - 并行上传原图 + 串行翻译 ==========
    log(`📤 并行上传 ${imagesToProcess.length} 张原图到 ImgBB...`, 'info');
    
    // 并行上传所有原图到 ImgBB
    const uploadPromises = imagesToProcess.map(async (img) => {
      const imgbbApiKey = process.env.IMGBB_API_KEY || config.translator.imgbbApiKey || config.imageHost?.apiKey;
      
      if (!imgbbApiKey) {
        return { ...img, url: null, uploadFailed: true };
      }
      
      try {
        const uploadUrl = `https://api.imgbb.com/1/upload?key=${imgbbApiKey}`;
        const response = execSync(`curl -s -X POST "${uploadUrl}" --form "image=@${img.path}"`, {
          encoding: 'utf-8',
          timeout: 60000
        });
        
        const result = JSON.parse(response.trim());
        if (result.success && result.data?.url) {
          return { ...img, url: result.data.url, uploadFailed: false };
        } else {
          return { ...img, url: null, uploadFailed: true };
        }
      } catch (e) {
        log(`上传失败 ${img.filename}: ${e.message}`, 'warn');
        return { ...img, url: null, uploadFailed: true };
      }
    });
    
    const imagesWithUrls = await Promise.all(uploadPromises);
    log(`✅ 原图上传完成：${imagesWithUrls.filter(i => !i.uploadFailed).length}/${imagesToProcess.length}`, 'info');
    
    // 串行调用象寄翻译（避免并发限流）
    const processedImages = [];
    
    for (let i = 0; i < imagesWithUrls.length; i++) {
      const img = imagesWithUrls[i];
      const ext = path.extname(img.filename);
      const baseName = path.basename(img.filename, ext);
      
      // 输出文件名：main_01_ru.jpg 格式
      const outputFilename = `${baseName}_ru${ext}`;
      const outputPath = path.join(IMAGES_DIR, outputFilename);
      
      log(`翻译 ${i + 1}/${imagesWithUrls.length}: ${img.filename}`, 'debug');
      
      if (!img.url || img.uploadFailed) {
        // 上传失败，直接复制原图
        log(`⚠️ 原图上传失败，直接复制: ${img.filename}`, 'warn');
        fs.copyFileSync(img.path, outputPath);
        processedImages.push({
          filename: outputFilename,
          path: outputPath,
          originalFilename: img.filename,
          translated: false,
          noText: true
        });
        continue;
      }
      
      // 调用象寄翻译 API
      const translated = await translateImageByUrl(img.url, config.translator);
      
      if (translated.success) {
        // 翻译成功，下载翻译后的图片
        try {
          execSync(`curl -s -L "${translated.imageUrl}" -o "${outputPath}"`, { timeout: 30000 });
          
          processedImages.push({
            filename: outputFilename,
            path: outputPath,
            originalFilename: img.filename,
            translated: true
          });
          
          log(`✅ 翻译成功: ${outputFilename}`, 'success');
        } catch (e) {
          log(`下载翻译图失败，直接复制: ${img.filename}`, 'warn');
          fs.copyFileSync(img.path, outputPath);
          processedImages.push({
            filename: outputFilename,
            path: outputPath,
            originalFilename: img.filename,
            translated: false,
            noText: true
          });
        }
      } else {
        // 无文本或翻译失败，直接复制原图并重命名
        log(`⚠️ 无文本/翻译失败，直接复制: ${img.filename}`, 'warn');
        fs.copyFileSync(img.path, outputPath);
        
        processedImages.push({
          filename: outputFilename,
          path: outputPath,
          originalFilename: img.filename,
          translated: false,
          noText: true
        });
      }
    }
    
    // ========== 步骤4: 上传到图床 ==========
    log(`上传 ${processedImages.length} 张图片到图床...`, 'info');
    const translatedImagesWithUrls = uploadToImgBB(processedImages, config.imageHost);
    
    // 保存 images.json
    const imagesJsonFile = path.join(OUTPUT_DIR, 'images.json');
    fs.writeFileSync(imagesJsonFile, JSON.stringify(translatedImagesWithUrls, null, 2));
    
    log(`Step 2 完成：${translatedImagesWithUrls.length} 张图片已处理`, 'success');
    writeProgress(getOutputDir(), 'step2_image_translator', 'completed', {
      outputDir: OUTPUT_DIR,
      imageCount: translatedImagesWithUrls.length,
      imagesJson: imagesJsonFile
    });
    
    return {
      success: true,
      outputDir: OUTPUT_DIR,
      images: translatedImagesWithUrls
    };
    
  } catch (error) {
    log(`Step 2 失败：${error.message}`, 'error');
    writeProgress(getOutputDir(), 'step2_image_translator', 'failed', {
      error: error.message
    });
    throw error;
  }
}

/**
 * 翻译单张图片（旧接口，保留兼容）
 * @param {string} imagePath - 图片路径
 * @param {Object} translatorConfig - 翻译配置
 * @param {Object} imageHostConfig - 图床配置
 * @returns {Object} - { success: boolean, imageUrl: string, localPath: string }
 */
function translateSingleImage(imagePath, translatorConfig, imageHostConfig) {
  const { userKey, imgTransKey } = translatorConfig;
  const imgbbApiKey = process.env.IMGBB_API_KEY || translatorConfig.imgbbApiKey || imageHostConfig?.apiKey;
  
  try {
    // 步骤1: 上传原图到 ImgBB 获取 URL
    let imageUrl = null;
    
    if (imgbbApiKey && fs.existsSync(imagePath)) {
      try {
        const uploadUrl = `https://api.imgbb.com/1/upload?key=${imgbbApiKey}`;
        
        // 使用 @file 方式上传，避免命令行过长
        const response = execSync(`curl -s -X POST "${uploadUrl}" --form "image=@${imagePath}"`, {
          encoding: 'utf-8',
          timeout: 60000
        });
        
        const result = JSON.parse(response.trim());
        if (result.success && result.data?.url) {
          imageUrl = result.data.url;
        }
      } catch (e) {
        log(`上传图床失败: ${e.message}`, 'warn');
      }
    }
    
    if (!imageUrl) {
      return { success: false, reason: '无图床URL' };
    }
    
    // 步骤2: 调用象寄翻译 API
    return translateImageByUrl(imageUrl, translatorConfig);
    
  } catch (error) {
    log(`翻译失败: ${error.message}`, 'warn');
    return { success: false, reason: error.message };
  }
}

/**
 * 根据 URL 翻译图片（方案1优化）
 * @param {string} imageUrl - 图片 URL
 * @param {Object} translatorConfig - 翻译配置
 * @returns {Promise<Object>} - { success: boolean, imageUrl: string }
 */
async function translateImageByUrl(imageUrl, translatorConfig) {
  const { userKey, imgTransKey } = translatorConfig;
  
  try {
    // 调用象寄翻译 API
    const commitTime = Math.floor(Date.now() / 1000).toString();
    const signStr = `${commitTime}_${userKey}_${imgTransKey}`;
    const sign = crypto.createHash('md5').update(signStr).digest('hex');
    
    const apiUrl = 'https://api.tosoiot.com';
    const encodedUrl = encodeURIComponent(imageUrl);
    const body = `Action=GetImageTranslate&SourceLanguage=CHS&TargetLanguage=RUS&Url=${encodedUrl}&ImgTransKey=${imgTransKey}&CommitTime=${commitTime}&Sign=${sign}`;
    
    const response = execSync(`curl -s -X POST "${apiUrl}" -H "Content-Type: application/x-www-form-urlencoded" -d "${body}"`, {
      encoding: 'utf-8',
      timeout: 60000
    });
    
    const result = JSON.parse(response.trim());
    
    if (result.Code === 200 && result.Data?.Url) {
      return {
        success: true,
        imageUrl: result.Data.SslUrl || result.Data.Url
      };
    } else {
      // 无文本或翻译失败
      return { success: false, reason: result.Message || '翻译失败' };
    }
    
  } catch (error) {
    log(`翻译失败: ${error.message}`, 'warn');
    return { success: false, reason: error.message };
  }
}

/**
 * 上传图片到 ImgBB 图床
 */
function uploadToImgBB(images, config) {
  const imgbbApiKey = process.env.IMGBB_API_KEY || config?.apiKey;
  
  if (!imgbbApiKey) {
    log('⚠️ 缺少 ImgBB API Key', 'warn');
    return images.map(img => ({
      filename: img.filename,
      url: null,
      localPath: img.path,
      originalFilename: img.originalFilename,
      noText: img.noText || false
    }));
  }
  
  const imagesWithUrls = [];
  
  for (const image of images) {
    try {
      const imagePath = image.path;
      const uploadUrl = `https://api.imgbb.com/1/upload?key=${imgbbApiKey}`;
      
      // 使用 @file 方式上传，避免命令行过长
      const response = execSync(`curl -s -X POST "${uploadUrl}" --form "image=@${imagePath}"`, {
        encoding: 'utf-8',
        timeout: 60000
      });
      
      const result = JSON.parse(response.trim());
      
      if (result.success && result.data?.url) {
        imagesWithUrls.push({
          filename: image.filename,
          url: result.data.url,
          originalFilename: image.originalFilename,
          noText: image.noText || false
        });
      } else {
        throw new Error(result.error?.message || '上传失败');
      }
    } catch (error) {
      log(`上传失败 ${image.filename}: ${error.message}`, 'warn');
      imagesWithUrls.push({
        filename: image.filename,
        url: null,
        localPath: image.path,
        originalFilename: image.originalFilename
      });
    }
  }
  
  return imagesWithUrls;
}

module.exports = {
  runImageTranslator,
  OUTPUT_DIR,
  DEFAULT_MAX_TRANSLATE
};
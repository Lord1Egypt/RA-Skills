#!/usr/bin/env node
/**
 * OCR 识别模块（Baidu OCR）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { log } = require('./logger');

/**
 * 执行 Baidu OCR
 */
function runOCR(images, config, maxImages = 999) {
  // 限制 OCR 数量（默认全部）
  const imagesToProcess = images.slice(0, maxImages);
  log(`使用 Baidu OCR 识别 ${imagesToProcess.length} 张图片（共 ${images.length} 张）...`, 'info');
  
  const ocrResults = [];
  
  for (const image of imagesToProcess) {
    try {
      // 调用 Baidu OCR API
      const result = callBaiduOCR(image.path, config.ocr);
      if (result && result.words_result && result.words_result.length > 0) {
        ocrResults.push({
          filename: image.filename,
          text: result.words_result.map(w => w.words).join('\n')
        });
      }
    } catch (error) {
      log(`OCR 失败 ${image.filename}: ${error.message}`, 'warn');
    }
  }
  
  return ocrResults;
}

/**
 * 调用 Baidu OCR API
 */
function callBaiduOCR(imagePath, config) {
  const { apiKey, secretKey } = config;
  
  // 获取 access_token
  const tokenUrl = `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${apiKey}&client_secret=${secretKey}`;
  const tokenResponse = execSync(`curl -s "${tokenUrl}"`, { encoding: 'utf-8' });
  const tokenData = JSON.parse(tokenResponse);
  const accessToken = tokenData.access_token;
  
  // 调用 OCR API
  const imageBase64 = fs.readFileSync(imagePath).toString('base64');
  const ocrUrl = `https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=${accessToken}`;
  const ocrResponse = execSync(`curl -s -X POST "${ocrUrl}" -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode "image=${imageBase64}"`, {
    encoding: 'utf-8',
    timeout: 30000
  });
  
  return JSON.parse(ocrResponse);
}

module.exports = {
  runOCR,
  callBaiduOCR
};

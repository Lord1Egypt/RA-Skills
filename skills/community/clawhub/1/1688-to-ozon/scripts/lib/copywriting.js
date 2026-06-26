#!/usr/bin/env node
/**
 * 文案生成模块
 * 
 * 经验：直接 curl 调用 DashScope API 超时
 * 解决方案：保存数据到临时文件，由 agent 直接在响应中生成
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { log } = require('./logger');

const TEMP_DIR = os.tmpdir();
const SKILL_DIR = path.join(__dirname, '../..');
const TEMPLATE_FILE = path.join(SKILL_DIR, 'templates', 'copywriting-prompt.md');

/**
 * 生成中俄双语文案
 * 
 * 由于无法直接调用 LLM（超时），保存数据到临时文件
 * 由 agent 直接在响应中调用 LLM 生成
 */
function generateCopywriting(productInfo, ocrResults, config) {
  const timestamp = Date.now();
  const dataFile = path.join(TEMP_DIR, 'cw-data-' + timestamp + '.json');
  const resultFile = path.join(TEMP_DIR, 'cw-result-' + timestamp + '.json');
  const promptFile = path.join(TEMP_DIR, 'cw-prompt-' + timestamp + '.md');
  
  // 读取模板文件
  let templateContent = '';
  if (fs.existsSync(TEMPLATE_FILE)) {
    templateContent = fs.readFileSync(TEMPLATE_FILE, 'utf-8');
    // 保存模板到临时文件，供 LLM 读取
    fs.writeFileSync(promptFile, templateContent);
  } else {
    log(`⚠️ 模板文件不存在: ${TEMPLATE_FILE}`, 'warn');
  }
  
  // 构建数据
  const data = {
    productInfo: {
      title: productInfo.title || '未知',
      price: productInfo.price || '未知',
      skuName: productInfo.skuName || '',
      attributes: productInfo.attributes || []
    },
    ocrResults: ocrResults.slice(0, 7).map(r => ({
      filename: r.filename,
      text: (r.text || '').substring(0, 500)
    })),
    _resultFile: resultFile,
    _promptFile: promptFile
  };
  
  // 保存数据
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
  
  log(`请读取模板 ${promptFile} 和数据 ${dataFile} 并生成文案，保存到 ${resultFile}`, 'info');
  
  // 抛出错误，提示 agent 直接生成（直接包含模板内容）
  const errorMsg = templateContent 
    ? `请严格按照以下模板生成文案：

${templateContent}

---
商品数据：
${JSON.stringify(data, null, 2)}

请生成 JSON 格式结果，保存到：${resultFile}`
    : `请读取 ${dataFile} 并使用 qwen3.5-plus 模型生成文案，保存到 ${resultFile}。`;
  
  throw new Error(errorMsg);
}

/**
 * 检查并读取已生成的文案
 */
function checkAndReadCopywriting(resultFile) {
  if (fs.existsSync(resultFile)) {
    try {
      const content = fs.readFileSync(resultFile, 'utf-8');
      const parsed = JSON.parse(content);
      
      if (parsed && parsed.title?.ru) {
        log('已找到生成的文案', 'success');
        return {
          md: formatMarkdown(parsed),
          json: parsed
        };
      }
    } catch (e) {
      log(`读取文案失败：${e.message}`, 'warn');
    }
  }
  return null;
}

/**
 * 格式化 Markdown 输出
 */
function formatMarkdown(copywriting) {
  return `# 中俄双语文案

## 商品标题
**俄文**: ${copywriting.title?.ru || ''}
**中文**: ${copywriting.title?.cn || ''}

## 商品描述
### 俄文
${copywriting.description?.ru || ''}

### 中文
${copywriting.description?.cn || ''}

## 标签
### 俄文
${(copywriting.hashtags?.ru || []).join(' ')}

### 中文
${(copywriting.hashtags?.cn || []).join(' ')}
`;
}

module.exports = {
  generateCopywriting,
  checkAndReadCopywriting,
  formatMarkdown
};
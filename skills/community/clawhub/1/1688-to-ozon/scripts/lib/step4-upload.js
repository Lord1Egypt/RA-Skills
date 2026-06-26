#!/usr/bin/env node
/**
 * Step 4: OZON 上传
 * 
 * 功能：
 * - 字段映射（1688 数据 → OZON API 格式）
 * - 调用 OZON API 上传商品
 * - 轮询导入状态
 * - 设置库存
 * 
 * 输出：
 * - upload_result.md - 上传结果
 * - progress.json - 详细进度
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const { log, writeProgress } = require('./logger');
const { getOutputDir, getWorkspaceDir } = require('./workspace');
const { loadConfig } = require('./config');

// 使用 __dirname 相对路径，不依赖 os.homedir()
const SKILL_DIR = path.resolve(__dirname, '../..');
// 输出目录：1688-to-ozon/（v1.0.51+ 新架构，不再使用 ozon-publisher 子目录）
const OUTPUT_DIR = getOutputDir();
// 新架构不再需要 INPUT_DIR，直接读取各步骤输出目录

/**
 * 执行 OZON 上传
 */
function runUpload(categoryId, pauseBeforeUpload) {
  // 加载配置并传递环境变量
  const config = loadConfig();
  
  log('Step 4: 开始上传到 OZON...', 'info');
  
  try {
    // 确保输出目录存在
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }
    
    // 不再复制文件，直接使用各步骤的输出目录
    // 1688-tt/ → getOutputDir()/1688-tt/
    // ozon-image-translator/ → getOutputDir()/ozon-image-translator/
    // ozon-pricer/ → getOutputDir()/ozon-pricer/
    
    log('直接读取各步骤输出目录（无需复制）', 'debug');
    
    // 构建映射命令
    const mapCmd = `node ${SKILL_DIR}/scripts/ozon/map.js --category ${categoryId || 'toy_set'}`;
    
    log(`执行映射：${mapCmd}`, 'debug');
    execSync(mapCmd, {
      stdio: 'inherit',
      timeout: 300000,
      env: { 
        ...process.env, 
        WORKSPACE_DIR: getWorkspaceDir(),
        OZON_CLIENT_ID: config.ozon?.clientId,
        OZON_API_KEY: config.ozon?.apiKey
      }
    });
    
    // 检查是否需要暂停
    if (pauseBeforeUpload) {
      log('⏸️  暂停等待用户确认...', 'warn');
      log('请检查 upload-request.json 文件，确认无误后按 Ctrl+C 继续', 'warn');
      
      // 等待用户确认（简单实现：等待 5 秒）
      const waitTime = 5000;
      log(`等待 ${waitTime / 1000} 秒...`, 'info');
      const start = Date.now();
      while (Date.now() - start < waitTime) {
        // 空循环等待
      }
    }
    
    // 执行上传
    const uploadCmd = `node ${SKILL_DIR}/scripts/ozon/upload.js auto`;
    
    log(`执行上传：${uploadCmd}`, 'debug');
    // 传递 OZON API 凭据和环境变量
    execSync(uploadCmd, {
      stdio: 'inherit',
      timeout: 300000,
      env: { 
        ...process.env, 
        WORKSPACE_DIR: getWorkspaceDir(),
        OZON_CLIENT_ID: config.ozon?.clientId,
        OZON_API_KEY: config.ozon?.apiKey
      }
    });
    
    // 验证输出文件
    const uploadResultFile = path.join(OUTPUT_DIR, 'upload_result.md');
    if (!fs.existsSync(uploadResultFile)) {
      throw new Error('缺少 upload_result.md 文件');
    }
    
    log('Step 4 完成：OZON 上传成功', 'success');
    writeProgress(getOutputDir(), 'step4_upload', 'completed', {
      outputDir: OUTPUT_DIR,
      uploadResult: uploadResultFile
    });
    
    return {
      success: true,
      outputDir: OUTPUT_DIR,
      uploadResult: uploadResultFile
    };
    
  } catch (error) {
    log(`Step 4 失败：${error.message}`, 'error');
    writeProgress(getOutputDir(), 'step4_upload', 'failed', {
      error: error.message
    });
    throw error;
  }
}

module.exports = {
  runUpload,
  OUTPUT_DIR
};

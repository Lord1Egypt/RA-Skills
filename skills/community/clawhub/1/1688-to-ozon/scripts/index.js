#!/usr/bin/env node
/**
 * 1688-to-OZON 完整工作流控制器 (v1.0.51+)
 * 
 * 执行流程：
 * 1. 1688 商品抓取 → 1688-tt/
 * 2. 图片翻译 → ozon-image-translator/
 * 3. 定价计算 → ozon-pricer/
 * 4. OZON 上传 → 直接使用上述目录（无需复制）
 * 
 * 目录结构：
 * 1688-to-ozon/
 * ├── 1688-tt/               # Step 1 输出
 * ├── ozon-image-translator/ # Step 2 输出
 * ├── ozon-pricer/           # Step 3 输出
 * ├── mapping_result.json    # Step 4 映射结果
 * └── upload-request.json    # OZON 上传请求
 * 
 * 使用方法：
 * node scripts/index.js "URL" -w 100g -p 30 -s 10 --category toy_set --profit 0.2
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');

const { log, writeProgress, readProgress } = require('./lib/logger');
const { getOutputDir, getWorkspaceDir, clearOutputDir } = require('./lib/workspace');
const { loadConfig } = require('./lib/config');
const { run1688 } = require('./lib/step1-1688');
const { runImageTranslator } = require('./lib/step2-img');
const { runPricing } = require('./lib/step3-price');
const { runUpload } = require('./lib/step4-upload');

// 解析命令行参数
function parseArgs(args) {
  const params = {
    url: null,
    weight: null,
    purchasePrice: null,
    shippingCost: null,
    profitMargin: 0.2,
    category: 'toy_set',
    pauseBeforeUpload: false,
    step: null,
    log: false // 主动通知开关
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (!arg.startsWith('-') && !params.url) {
      params.url = arg;
    } else if (arg === '-w' || arg === '--weight') {
      params.weight = args[++i];
    } else if (arg.startsWith('-p') || arg === '--purchase-price') {
      // 支持 -p300 格式（参数和值连在一起）
      if (arg.startsWith('-p') && arg.length > 2) {
        params.purchasePrice = arg.substring(2);
      } else {
        params.purchasePrice = args[++i];
      }
    } else if (arg === '-s' || arg === '--shipping') {
      params.shippingCost = args[++i];
    } else if (arg === '--profit') {
      params.profitMargin = parseFloat(args[++i]);
    } else if (arg === '--category') {
      params.category = args[++i];
    } else if (arg === '--pause' || arg === '--pause-before-upload') {
      params.pauseBeforeUpload = true;
    } else if (arg === '--step') {
      params.step = parseInt(args[++i]);
    } else if (arg === '-l' || arg === '--log') {
      params.log = true;
      process.env.ENABLE_FEISHU = 'true'; // 启用飞书通知
      // 设置飞书凭证（从 OpenClaw 配置读取）
      process.env.FEISHU_APP_ID = 'cli_a90b1d9903385ceb';
      process.env.FEISHU_APP_SECRET = 'G9TdEypJQ9SDOBdExTJVrdn2LtxbdFcV';
      // 尝试从环境变量获取群聊 ID
      params.feishuChatId = process.env.FEISHU_CHAT_ID || process.env.OC_CHAT_ID;
    } else if (arg === '--chat-id') {
      params.feishuChatId = args[++i];
    } else if (arg === '-t' || arg === '--translate-count') {
      params.translateCount = parseInt(args[++i]) || 15;
    } else if (arg === '-o' || arg === '--ocr-count') {
      params.ocrCount = parseInt(args[++i]) || 999;
    } else if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    }
  }
  
  return params;
}

// 显示帮助信息
function showHelp() {
  console.log(`
1688-to-OZON - 1688 商品自动上架到 OZON

使用方法:
  node scripts/index.js "URL" [选项]

参数:
  URL                     1688 商品链接

选项:
  -w, --weight <重量>      商品重量（如：100g, 0.5kg）
  -p, --purchase-price <价格>  采购价（人民币，如：30）
  -s, --shipping <运费>    国内运费（人民币，如：10）
  --profit <利润率>        利润率（小数，如：0.2 表示 20%）
  --category <类目>        OZON 类目（默认：toy_set）
  --pause                 上传前暂停确认
  --step <步骤>            从指定步骤开始（1-4）
  -l, --log               开启实时进度输出（主代理捕获发送飞书）
  -o, --ocr-count <数量>   OCR 识别图片数量（默认全部）
  -h, --help              显示帮助

示例:
  node scripts/index.js "https://detail.1688.com/offer/XXX.html" -w 100g -p 30
  node scripts/index.js "URL" -w 100g -p 30 --profit 0.25 --category toys
  node scripts/index.js "URL" -w 100g -p 30 -l  # 开启实时通知
`);
}

// 进度通知函数（简化版：只输出标记日志，由主代理捕获并发送飞书）
function notifyProgress(step, status, details, params, config) {
  if (!params.log) {
    return;
  }
  
  const emoji = status === 'completed' ? '✅' : status === 'failed' ? '❌' : '⏳';
  const message = `[PROGRESS] ${emoji} ${step}: ${status} - ${details}`;
  
  // 打印到控制台（主代理会自动捕获）
  console.log(message);
  log(message, 'info');
}

// 等待用户确认
async function waitForConfirmation(stepName) {
  // 自动继续（除非设置 PAUSE=true）
  if (process.env.AUTO_CONTINUE === 'true' || process.env.PAUSE !== 'true') {
    log(`⏭️  ${stepName} 完成（自动继续）`, 'debug');
    return true;
  }
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(`\n⏸️  ${stepName} 完成。是否继续执行下一步？(y/n): `, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

// 主流程
async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);
  
  // 验证必需参数
  if (!params.url) {
    log('错误：必须指定 1688 商品 URL', 'error');
    showHelp();
    process.exit(1);
  }
  
  if (!params.purchasePrice) {
    log('错误：必须指定采购价 (-p)', 'error');
    process.exit(1);
  }
  
  // 加载配置
  const config = loadConfig({
    pauseBeforeUpload: params.pauseBeforeUpload
  });
  
  // 输出目录
  const outputDir = getOutputDir();
  const workspaceDir = getWorkspaceDir();
  
  log('🎯 1688-to-OZON - 完整工作流', 'info');
  log('================================', 'info');
  log(`📦 商品 URL: ${params.url}`, 'info');
  log(`⚖️  重量：${params.weight || '自动读取'}`, 'info');
  log(`💰 采购价：¥${params.purchasePrice}`, 'info');
  log(`🚚 运费：${params.shippingCost ? `¥${params.shippingCost}` : '自动计算'}`, 'info');
  log(`📊 利润率：${(params.profitMargin * 100).toFixed(0)}%`, 'info');
  log(`📁 Workspace: ${workspaceDir}`, 'info');
  log(`📁 输出目录：${outputDir}`, 'info');
  log('');
  
  // 执行前清空输出目录（只有从 Step 1 开始时才清空）
  if (!params.step || params.step === 1) {
    clearOutputDir();
  } else {
    log('⏭️  跳过清空目录（从 Step ' + params.step + ' 继续）', 'info');
  }
  
  // 初始化进度
  writeProgress(outputDir, 'init', 'completed', {
    url: params.url,
    weight: params.weight,
    purchasePrice: params.purchasePrice,
    shippingCost: params.shippingCost,
    profitMargin: params.profitMargin,
    category: params.category
  });
  
  try {
    // Step 1: 1688 商品抓取
    if (!params.step || params.step === 1) {
      const ocrCount = params.ocrCount || 999;
      const result = run1688(
        params.url,
        params.weight,
        params.purchasePrice,
        params.shippingCost || '0',
        ocrCount
      );
      
      // 发送飞书通知
      notifyProgress('Step 1: 1688 商品抓取', 'completed', 
        `商品：${result.productName || '未知'}\n图片：${result.imageCount || 0} 张`, params, config);
      
      if (!await waitForConfirmation('Step 1: 1688 商品抓取')) {
        log('用户取消执行', 'warn');
        process.exit(0);
      }
    }
    
    // Step 2: 图片翻译
    if (!params.step || params.step === 2) {
      const translateCount = params.translateCount || 15;
      const result = await runImageTranslator(translateCount);
      
      // 发送飞书通知
      notifyProgress('Step 2: 图片翻译', 'completed',
        `翻译：${result.translatedCount || 0} 张\n图床：${result.imgurUrl || 'N/A'}`, params, config);
      
      if (!await waitForConfirmation('Step 2: 图片翻译')) {
        log('用户取消执行', 'warn');
        process.exit(0);
      }
    }
    
    // Step 3: 定价计算
    if (!params.step || params.step === 3) {
      const result = runPricing(
        params.weight,
        params.purchasePrice,
        params.shippingCost,
        params.profitMargin
      );
      
      // 发送飞书通知
      notifyProgress('Step 3: 定价计算', 'completed',
        `售价：₽${result.finalPrice || 0} (¥${result.finalPriceCNY || 0})`, params, config);
      
      if (!await waitForConfirmation('Step 3: 定价计算')) {
        log('用户取消执行', 'warn');
        process.exit(0);
      }
    }
    
    // Step 4: OZON 上传
    if (!params.step || params.step === 4) {
      const result = runUpload(
        params.category,
        params.pauseBeforeUpload
      );
      
      // 发送飞书通知
      notifyProgress('Step 4: OZON 上传', 'completed',
        `Product ID：${result.productId || 'N/A'}\nOffer ID：${result.offerId || 'N/A'}`, params, config);
      
      log('🎉 全流程完成！商品已成功上传到 OZON', 'success');
    }
    
    // 输出最终报告
    log('', 'info');
    log('📊 执行报告', 'info');
    const progress = readProgress(outputDir);
    if (progress) {
      log(`状态：${progress.status}`, 'info');
      log(`步骤：${progress.steps.length}`, 'info');
      for (const step of progress.steps) {
        const icon = step.status === 'completed' ? '✅' : (step.status === 'failed' ? '❌' : '⏳');
        log(`${icon} ${step.step}: ${step.status}`, 'info');
      }
    }
    
  } catch (error) {
    log(`❌ 流程失败：${error.message}`, 'error');
    console.error(error.stack);
    process.exit(1);
  }
}

// 运行主流程
main();

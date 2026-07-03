#!/usr/bin/env node
/**
 * doubao-batch-gen.js
 * 豆包批量生成脚本 - 通过 CDP + Playwright 循环调用豆包网页端 API
 * 支持批量生成图片或视频
 *
 * 用法：
 *   node doubao-batch-gen.js --type=image --prompts=prompts.txt --output=./output
 *   node doubao-batch-gen.js --type=video --prompts=prompts.txt --output=./output
 */

const { chromium } = require('C:/Users/Owner/.workbuddy/binaries/node/workspace/node_modules/playwright-core');

const CDP_URL = 'http://localhost:9222';
const EDGE_PATH = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const DOUBAO_URL = 'https://www.doubao.com/';

const CONFIG = {
  cdpUrl: CDP_URL,
  edgePath: EDGE_PATH,
  timeout: {
    pageLoad: 30000,
    aiResponse: 300000,   // 5分钟
    download: 60000,
  }
};

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      result[key] = value !== undefined ? value : true;
    }
  }
  return result;
}

// 读取提示词文件
function loadPrompts(filePath) {
  const fs = require('fs');
  if (!fs.existsSync(filePath)) {
    console.error(`提示词文件不存在: ${filePath}`);
    process.exit(1);
  }
  const content = fs.readFileSync(filePath, 'utf-8');
  return content.split('\n').filter(line => line.trim().length > 0);
}

// 连接或启动 Edge CDP
async function connectEdge() {
  let browser;
  try {
    browser = await chromium.connectOverCDP(CDP_URL);
    console.log('已连接到现有 Edge CDP 实例');
  } catch (e) {
    console.log('未检测到 Edge CDP 实例，正在启动...');
    const { execSync } = require('child_process');
    const userDataDir = `${process.env.LOCALAPPDATA}/Microsoft/Edge/User Data`;
    const edgeProc = execSync(`"${EDGE_PATH}" --remote-debugging-port=9222 --user-data-dir="${userDataDir}"`, { detached: true, stdio: 'ignore' });
    await new Promise(r => setTimeout(r, 8000));
    browser = await chromium.connectOverCDP(CDP_URL);
    console.log('Edge CDP 实例已启动并连接');
  }

  let page = browser.contexts()[0]?.pages().find(p => p.url().includes('doubao.com')) 
             || browser.contexts()[0]?.pages()[0];
  
  if (!page || !page.url().includes('doubao.com')) {
    page = await browser.contexts()[0].newPage();
    console.log('打开豆包网页...');
    await page.goto(DOUBAO_URL, { waitUntil: 'domcontentloaded', timeout: CONFIG.timeout.pageLoad });
    await new Promise(r => setTimeout(r, 5000));
  }

  return { browser, page };
}

// 发送消息到豆包
async function sendMessage(page, message) {
  const inputSelector = 'textarea[placeholder*="发消息"], textarea[placeholder*="输入"], div[contenteditable="true"]';
  await page.waitForSelector(inputSelector, { timeout: 10000 });
  const input = await page.$(inputSelector);
  
  const currentValue = await page.evaluate(el => el.value || el.textContent, input);
  if (currentValue) {
    await page.evaluate(el => { el.value = ''; el.textContent = ''; }, input);
  }
  
  await input.fill(message);
  await new Promise(r => setTimeout(r, 1000));
  await input.press('Enter');
  console.log(`已发送: ${message.substring(0, 50)}...`);
}

// 等待 AI 响应完成
async function waitForResponse(page) {
  console.log('等待豆包响应...');
  await new Promise(r => setTimeout(r, 15000));
  
  const maxWait = CONFIG.timeout.aiResponse;
  const start = Date.now();
  
  while (Date.now() - start < maxWait) {
    const stopBtn = await page.$('button:has(svg)');
    if (!stopBtn) break;
    const isVisible = await stopBtn.isVisible().catch(() => false);
    if (!isVisible) break;
    await new Promise(r => setTimeout(r, 3000));
  }
  
  console.log('响应完成');
}

// 下载最近生成的内容
async function downloadLatest(page, outputDir, index, type) {
  const fs = require('fs');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const downloadBtnSelector = type === 'image' 
    ? 'button:has-text("下载")' 
    : 'button:has-text("下载")';
  
  try {
    const downloadBtn = await page.$(downloadBtnSelector);
    if (downloadBtn) {
      const downloadPromise = page.waitForEvent('download', { timeout: 30000 });
      await downloadBtn.click();
      const download = await downloadPromise;
      const filePath = `${outputDir}/${type}-${String(index).padStart(2, '0')}-${Date.now()}.${type === 'image' ? 'png' : 'mp4'}`;
      await download.saveAs(filePath);
      console.log(`已下载: ${filePath}`);
      return filePath;
    }
  } catch (e) {
    console.warn(`下载失败: ${e.message}`);
  }
  return null;
}

// 主函数
async function main() {
  const args = parseArgs();
  const type = args.type || 'image';
  const promptsFile = args.prompts;
  const output = args.output || './output';

  if (!promptsFile) {
    console.error('请指定提示词文件: --prompts=prompts.txt');
    process.exit(1);
  }

  const prompts = loadPrompts(promptsFile);
  console.log(`加载了 ${prompts.length} 条提示词，类型: ${type}`);

  const { browser, page } = await connectEdge();

  const results = [];
  for (let i = 0; i < prompts.length; i++) {
    console.log(`\n[${i + 1}/${prompts.length}] 生成中...`);
    const prompt = prompts[i];
    
    // 构造生成提示词
    const fullPrompt = type === 'image' 
      ? `生成一张图片：${prompt}`
      : `生成一段视频：${prompt}`;
    
    await sendMessage(page, fullPrompt);
    await waitForResponse(page);
    await new Promise(r => setTimeout(r, 5000));
    
    const filePath = await downloadLatest(page, output, i + 1, type);
    results.push({ index: i + 1, prompt, filePath });
    
    // 避免频率限制
    if (i < prompts.length - 1) {
      console.log('等待 10 秒避免频率限制...');
      await new Promise(r => setTimeout(r, 10000));
    }
  }

  console.log('\n=== 批量生成完成 ===');
  console.table(results);
  await browser.close();
}

main().catch(e => {
  console.error('执行失败:', e.message);
  process.exit(1);
});

#!/usr/bin/env node
/**
 * ChatGPT Image Generation
 * Uses Playwright to automate ChatGPT web UI for image generation.
 * 
 * Usage:
 *   node generate.js --prompts prompts.json --output ./images
 *   node generate.js --prompts prompts.json --output ./images --start 5
 *   node generate.js --prompts prompts.json --output ./images --headless
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const os = require('os');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { start: 0, headless: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompts' && args[i + 1]) opts.promptsPath = args[++i];
    else if (args[i] === '--output' && args[i + 1]) opts.outputDir = args[++i];
    else if (args[i] === '--start' && args[i + 1]) opts.start = parseInt(args[++i], 10);
    else if (args[i] === '--headless') opts.headless = true;
  }
  if (!opts.promptsPath || !opts.outputDir) {
    console.error('Usage: node generate.js --prompts prompts.json --output ./images [--start N] [--headless]');
    process.exit(1);
  }
  return opts;
}

function loadPrompts(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const data = JSON.parse(content);
  if (Array.isArray(data)) return data;
  if (data.prompts && Array.isArray(data.prompts)) return data.prompts;
  throw new Error('Invalid prompts format');
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function logResults(resultsPath, entry) {
  fs.appendFileSync(resultsPath, JSON.stringify(entry) + '\n');
}

async function waitForGeneration(page, timeout = 120000) {
  console.log('  → Waiting for response...');
  
  try {
    await page.waitForSelector('button[disabled][aria-label="Send message"]', { timeout: 10000 });
    console.log('  → Generation started');
  } catch (e) {}
  
  try {
    await page.waitForSelector('article, [data-message-author-role="assistant"]', { timeout: timeout });
    console.log('  → Response received');
  } catch (e) {
    console.log('  → Waiting for response content...');
  }
  
  await page.waitForFunction(() => {
    const btn = document.querySelector('button[aria-label="Send message"]');
    return btn && !btn.disabled;
  }, { timeout });
  
  await page.waitForTimeout(3000);
}

async function findAndDownloadImage(page, outputPath) {
  console.log('  → Looking for generated image...');
  
  const imgInfo = await page.evaluate(() => {
    const articles = document.querySelectorAll('article');
    const lastArticle = articles[articles.length - 1];
    if (!lastArticle) return null;
    
    const imgs = lastArticle.querySelectorAll('img');
    const img = imgs[imgs.length - 1];
    if (!img) return null;
    
    return {
      src: img.src,
      naturalWidth: img.naturalWidth,
      naturalHeight: img.naturalHeight,
      complete: img.complete
    };
  });
  
  if (!imgInfo || !imgInfo.src) {
    console.log('  → No image found in response');
    return false;
  }
  
  console.log(`  → Found image: ${imgInfo.naturalWidth}x${imgInfo.naturalHeight}`);
  
  if (imgInfo.src.startsWith('data:')) {
    console.log('  → Image is embedded, extracting...');
    const base64 = imgInfo.src.split(',')[1];
    const buffer = Buffer.from(base64, 'base64');
    fs.writeFileSync(outputPath, buffer);
  } else {
    console.log('  → Fetching image from server...');
    try {
      const response = await page.request.get(imgInfo.src);
      const buffer = await response.body();
      if (buffer.length > 1000) {
        fs.writeFileSync(outputPath, buffer);
      } else {
        console.log('  → Image too small or empty');
        return false;
      }
    } catch (e) {
      console.log(`  → Fetch failed: ${e.message}`);
      return false;
    }
  }
  
  return fs.existsSync(outputPath) && fs.statSync(outputPath).size > 1000;
}

async function sendPrompt(page, prompt) {
  console.log('  → Sending prompt...');
  
  const textarea = await page.waitForSelector('textarea', { timeout: 10000 });
  await textarea.fill(prompt);
  
  const sendBtn = await page.$('button[aria-label="Send message"]');
  if (sendBtn) {
    await sendBtn.click();
  } else {
    await textarea.press('Enter');
  }
}

async function generateImages(opts) {
  const prompts = loadPrompts(opts.promptsPath);
  const outputDir = opts.outputDir;
  const startIdx = opts.start || 0;
  const resultsPath = path.join(outputDir, 'results.jsonl');

  ensureDir(outputDir);

  console.log(`\n=== ChatGPT Image Generation ===`);
  console.log(`Prompts: ${opts.promptsPath}`);
  console.log(`Output: ${outputDir}`);
  console.log(`Start index: ${startIdx}`);
  console.log(`Headless: ${opts.headless}\n`);

  const browser = await chromium.launch({ headless: opts.headless });
  const page = await browser.newPage();

  console.log('→ Opening chatgpt.com...');
  await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  
  const needsLogin = await page.$('text=Log in') !== null;
  if (needsLogin) {
    console.log('⚠️ Not logged in! Please sign in to ChatGPT, then press Enter...');
    await new Promise(r => { process.stdin.once('data', () => r()); });
  }

  let successCount = 0;
  let failCount = 0;

  for (let i = startIdx; i < prompts.length; i++) {
    const prompt = prompts[i];
    const paddedNum = String(i + 1).padStart(3, '0');
    const outputPath = path.join(outputDir, `${paddedNum}.png`);

    console.log(`\n[${i + 1}/${prompts.length}] ${prompt.substring(0, 50)}...`);

    try {
      await sendPrompt(page, prompt);
      await waitForGeneration(page);
      const ok = await findAndDownloadImage(page, outputPath);
      
      if (ok && fs.existsSync(outputPath) && fs.statSync(outputPath).size > 1000) {
        console.log(`✅ Saved: ${outputPath}`);
        logResults(resultsPath, { index: i, prompt, status: 'success', output: outputPath });
        successCount++;
      } else {
        console.log(`❌ Failed to get image`);
        logResults(resultsPath, { index: i, prompt, status: 'failed', error: 'no image' });
        failCount++;
      }
    } catch (e) {
      console.log(`❌ Error: ${e.message}`);
      logResults(resultsPath, { index: i, prompt, status: 'error', error: e.message });
      failCount++;
    }

    await new Promise(r => setTimeout(r, 2000));
  }

  await browser.close();

  console.log(`\n=== Complete ===`);
  console.log(`Success: ${successCount}, Failed: ${failCount}`);
  console.log(`Results: ${resultsPath}`);
}

const opts = parseArgs();
generateImages(opts).catch(console.error);

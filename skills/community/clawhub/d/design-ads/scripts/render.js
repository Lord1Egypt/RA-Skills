#!/usr/bin/env node
/**
 * Design Ads - HTML to PNG 渲染脚本
 *
 * 用法: node render.js <输入HTML文件路径> <输出PNG文件路径>
 *
 * 使用 Puppeteer + Chrome 将 HTML 海报渲染为 1200x1800 PNG 图片
 * 渲染完成后自动复制到下载目录的时间戳文件夹
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const os = require('os');

/**
 * 获取下载目录路径
 */
function getDownloadsDir() {
  const homeDir = os.homedir();
  // macOS 系统
  const downloadsPath = path.join(homeDir, 'Downloads');
  // 如果 Downloads 不存在，尝试中文路径
  if (!fs.existsSync(downloadsPath)) {
    const downloadsPathCn = path.join(homeDir, '下载');
    if (fs.existsSync(downloadsPathCn)) {
      return downloadsPathCn;
    }
  }
  return downloadsPath;
}

/**
 * 创建或复用项目文件夹并返回路径
 * 策略：检查是否存在 5 分钟内创建的 design-ads 文件夹，有则复用，无则创建
 */
function createTimestampDir() {
  const downloadsDir = getDownloadsDir();
  const now = new Date();
  const fiveMinutesAgo = new Date(now.getTime() - 5 * 60 * 1000);

  // 读取下载目录中的所有文件夹
  try {
    const entries = fs.readdirSync(downloadsDir, { withFileTypes: true });
    const dirs = entries
      .filter(entry => entry.isDirectory() && entry.name.startsWith('design-ads_'))
      .map(entry => {
        const fullPath = path.join(downloadsDir, entry.name);
        const stats = fs.statSync(fullPath);
        return { path: fullPath, mtime: stats.mtime };
      })
      .filter(dir => dir.mtime >= fiveMinutesAgo)
      .sort((a, b) => b.mtime - a.mtime);

    // 如果找到 5 分钟内的文件夹，复用最新的一个
    if (dirs.length > 0) {
      console.log(`[design-ads] 复用现有输出目录: ${dirs[0].path}`);
      return dirs[0].path;
    }
  } catch (error) {
    // 读取目录失败，继续创建新文件夹
  }

  // 没有找到符合条件的文件夹，创建新的
  const timestamp = now.toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .slice(0, 19);
  const folderName = `design-ads_${timestamp}`;
  const targetDir = path.join(downloadsDir, folderName);

  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
    console.log(`[design-ads] 创建输出目录: ${targetDir}`);
  }

  return targetDir;
}

/**
 * 复制文件到目标目录
 */
function copyToDownloads(sourcePath, targetDir) {
  if (!fs.existsSync(sourcePath)) {
    console.warn(`[design-ads] 源文件不存在，跳过复制: ${sourcePath}`);
    return;
  }

  const fileName = path.basename(sourcePath);
  const targetPath = path.join(targetDir, fileName);

  fs.copyFileSync(sourcePath, targetPath);
  console.log(`[design-ads] 已复制到下载目录: ${targetPath}`);

  const stats = fs.statSync(targetPath);
  console.log(`[design-ads] 文件大小: ${(stats.size / 1024).toFixed(1)} KB`);
}

async function render(htmlPath, outputPath) {
  // 参数校验
  if (!htmlPath || !outputPath) {
    console.error('用法: node render.js <输入HTML> <输出PNG>');
    console.error('示例: node render.js poster.html poster.png');
    process.exit(1);
  }

  const absoluteHtmlPath = path.resolve(htmlPath);
  const absoluteOutputPath = path.resolve(outputPath);

  // 检查输入文件是否存在
  if (!fs.existsSync(absoluteHtmlPath)) {
    console.error(`错误: 输入文件不存在: ${absoluteHtmlPath}`);
    process.exit(1);
  }

  // 确保输出目录存在
  const outputDir = path.dirname(absoluteOutputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log(`[design-ads] 开始渲染...`);
  console.log(`[design-ads] 输入: ${absoluteHtmlPath}`);
  console.log(`[design-ads] 输出: ${absoluteOutputPath}`);

  let browser;
  try {
    // 启动浏览器 - 使用系统 Chrome
    browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--font-render-hinting=none',
        // 固定视口大小匹配海报尺寸
        `--window-size=1200,1800`,
      ],
      // macOS 上优先使用系统 Chrome
      executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' || undefined,
    });

    const page = await browser.newPage();

    // 设置视口为海报尺寸，确保 2x 设备像素比以获得高清输出
    await page.setViewport({
      width: 1200,
      height: 1800,
      deviceScaleFactor: 2,
    });

    // 加载 HTML 文件（使用 file:// 协议）
    const fileUrl = `file://${absoluteHtmlPath}`;
    await page.goto(fileUrl, {
      waitUntil: 'networkidle0',
      timeout: 30000,
    });

    // 等待字体和样式完全加载
    await new Promise(resolve => setTimeout(resolve, 500));

    // 截图并保存为 PNG
    await page.screenshot({
      path: absoluteOutputPath,
      type: 'png',
      fullPage: false, // 使用固定视口尺寸
      clip: { x: 0, y: 0, width: 1200, height: 1800 },
      omitBackground: false,
    });

    console.log(`[design-ads] 渲染完成!`);
    console.log(`[design-ads] 图片已保存到: ${absoluteOutputPath}`);

    // 输出文件信息
    const stats = fs.statSync(absoluteOutputPath);
    console.log(`[design-ads] 文件大小: ${(stats.size / 1024).toFixed(1)} KB`);

    // 创建时间戳目录并复制文件
    const downloadsDir = createTimestampDir();
    copyToDownloads(absoluteHtmlPath, downloadsDir);
    copyToDownloads(absoluteOutputPath, downloadsDir);

  } catch (error) {
    console.error(`[design-ads] 渲染失败: ${error.message}`);
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 执行渲染
const [, , htmlPath, outputPath] = process.argv;
render(htmlPath, outputPath);

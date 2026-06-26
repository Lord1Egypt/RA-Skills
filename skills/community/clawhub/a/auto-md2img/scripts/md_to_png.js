#!/usr/bin/env node
const puppeteer = require('puppeteer');
const marked = require('marked');
const fs = require('fs');
const path = require('path');

/**
 * 将markdown内容分割为内容块（不拆分代码块、表格等）
 * @param {string} mdContent - 原始markdown内容
 * @returns {Array<string>} 内容块数组
 */
function splitIntoContentBlocks(mdContent) {
  const lines = mdContent.split('\n');
  const blocks = [];
  let currentBlock = [];
  let inCodeBlock = false;
  let inTable = false;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 处理代码块
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        currentBlock.push(line);
        blocks.push(currentBlock.join('\n'));
        currentBlock = [];
        inCodeBlock = false;
      } else {
        if (currentBlock.length > 0) {
          blocks.push(currentBlock.join('\n'));
          currentBlock = [];
        }
        inCodeBlock = true;
        currentBlock.push(line);
      }
      continue;
    }
    
    if (inCodeBlock) {
      currentBlock.push(line);
      continue;
    }
    
    // 处理表格
    if (line.trim().startsWith('|') && line.includes('|')) {
      if (!inTable) {
        if (currentBlock.length > 0) {
          blocks.push(currentBlock.join('\n'));
          currentBlock = [];
        }
        inTable = true;
      }
      currentBlock.push(line);
      continue;
    } else if (inTable) {
      // 表格结束
      blocks.push(currentBlock.join('\n'));
      currentBlock = [];
      inTable = false;
    }
    
    // 处理标题
    if (line.match(/^#{1,6} /)) {
      if (currentBlock.length > 0) {
        blocks.push(currentBlock.join('\n'));
        currentBlock = [];
      }
      currentBlock.push(line);
      blocks.push(currentBlock.join('\n'));
      currentBlock = [];
      continue;
    }
    
    // 处理空行（分隔普通段落）
    if (line.trim() === '') {
      if (currentBlock.length > 0) {
        blocks.push(currentBlock.join('\n'));
        currentBlock = [];
      }
      continue;
    }
    
    // 普通行
    currentBlock.push(line);
  }
  
  // 处理剩余内容
  if (currentBlock.length > 0) {
    blocks.push(currentBlock.join('\n'));
  }
  
  debugLog(`内容分割完成，共 ${blocks.length} 个内容块`);
  return blocks;
}

/**
 * 预计算每个内容块的渲染高度
 * @param {Array<string>} blocks - 内容块数组
 * @returns {Array<Object>} 每个块的高度信息
 */
async function measureBlockHeights(blocks) {
  debugLog('开始预计算内容块高度');
  
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  const blockHeights = [];
  let totalHeight = 0;
  
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    const html = marked.parse(block);
    
    await page.setContent(`<div style="width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6;">${html}</div>`, { waitUntil: 'networkidle0' });
    const elementHandle = await page.$('div');
    const { height } = await elementHandle.boundingBox();
    await elementHandle.dispose();
    
    const blockHeight = Math.ceil(height);
    blockHeights.push({
      content: block,
      height: blockHeight,
      index: i
    });
    
    totalHeight += blockHeight;
    debugLog(`内容块 ${i + 1}/${blocks.length} 高度：${blockHeight}px`);
  }
  
  await browser.close();
  debugLog(`所有内容块总高度：${totalHeight}px`);
  
  return blockHeights;
}

/**
 * 按高度分页（不拆分内容块）
 * @param {Array<Object>} blockHeights - 内容块高度数组
 * @param {number} maxHeight - 每页最大高度
 * @returns {Array<Array<Object>>} 分页后的内容块
 */
function paginateByHeight(blockHeights, maxHeight) {
  debugLog(`按高度分页，每页最大高度：${maxHeight}px`);
  
  const pages = [];
  let currentPage = [];
  let currentHeight = 0;
  
  for (const block of blockHeights) {
    // 检查当前块加入后是否超过高度限制
    if (currentHeight + block.height <= maxHeight) {
      currentPage.push(block);
      currentHeight += block.height;
    } else {
      // 超过限制，保存当前页
      if (currentPage.length > 0) {
        pages.push({
          blocks: currentPage,
          totalHeight: currentHeight
        });
        debugLog(`生成新页，包含 ${currentPage.length} 个块，总高度：${currentHeight}px`);
      }
      // 开启新页
      currentPage = [block];
      currentHeight = block.height;
    }
  }
  
  // 处理最后一页
  if (currentPage.length > 0) {
    pages.push({
      blocks: currentPage,
      totalHeight: currentHeight
    });
    debugLog(`生成最后一页，包含 ${currentPage.length} 个块，总高度：${currentHeight}px`);
  }
  
  debugLog(`高度分页完成，共 ${pages.length} 页`);
  return pages;
}

// 分页模式：'lines' 按行数，'height' 按高度
let PAGINATION_MODE = 'lines';
// 每页最大行数（行数模式）
let MAX_LINES_PER_PAGE = 500;
// 每页最大高度（高度模式，单位：px）
let MAX_HEIGHT_PER_PAGE = 15000;
// 图片质量（1-100）
let IMAGE_QUALITY = 80;
// Debug 模式
let DEBUG = false;

/**
 * Debug 日志输出
 * @param {string} message - 日志内容
 */
function debugLog(message) {
  if (DEBUG) {
    console.log(`🐛 [DEBUG] ${message}`);
  }
}

/**
 * 将markdown内容按内容块和行数限制分割为多页
 * @param {string} mdContent - 原始markdown内容
 * @returns {Array<string>} 分割后的每页markdown内容
 */
function splitMarkdownIntoPages(mdContent) {
  const lines = mdContent.split('\n');
  debugLog(`开始分割内容，总行数：${lines.length}`);
  
  const pages = [];
  let currentPage = [];
  let currentLineCount = 0;
  let inCodeBlock = false;
  let inTable = false;
  let currentCodeBlock = [];
  let currentTable = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    debugLog(`处理第 ${i + 1}/${lines.length} 行：${line.substring(0, 50)}${line.length > 50 ? '...' : ''}`);
    
    // 检测代码块边界
    if (line.trim().startsWith('```')) {
      debugLog(`检测到代码块边界，当前inCodeBlock状态：${inCodeBlock}`);
      if (inCodeBlock) {
        // 结束代码块
        currentCodeBlock.push(line);
        const codeBlockLines = currentCodeBlock.length;
        
        // 检查当前页是否能容纳整个代码块
        if (currentLineCount + codeBlockLines <= MAX_LINES_PER_PAGE) {
          currentPage.push(...currentCodeBlock);
          currentLineCount += codeBlockLines;
        } else {
          // 不能容纳，先保存当前页，再开启新页
          if (currentPage.length > 0) {
            pages.push(currentPage.join('\n'));
            currentPage = [];
            currentLineCount = 0;
          }
          currentPage.push(...currentCodeBlock);
          currentLineCount += codeBlockLines;
        }
        
        currentCodeBlock = [];
        inCodeBlock = false;
      } else {
        // 开始代码块
        inCodeBlock = true;
        currentCodeBlock.push(line);
      }
      continue;
    }

    // 如果在代码块中，继续累积
    if (inCodeBlock) {
      currentCodeBlock.push(line);
      continue;
    }

    // 检测表格边界
    const isTableLine = line.includes('|') && line.trim().startsWith('|') && line.trim().endsWith('|');
    const isTableSeparator = isTableLine && line.includes('---') && line.split('|').every(cell => cell.trim().match(/^-+$/));
    
    if (isTableLine || isTableSeparator) {
      if (!inTable) {
        inTable = true;
        currentTable = [];
      }
      currentTable.push(line);
      
      // 检查是否是表格的最后一行（下一行不是表格行）
      const nextLine = lines[i + 1] || '';
      const isNextLineTable = nextLine.includes('|') && nextLine.trim().startsWith('|') && nextLine.trim().endsWith('|');
      
      if (!isNextLineTable) {
        // 结束表格
        const tableLines = currentTable.length;
        
        // 检查当前页是否能容纳整个表格
        if (currentLineCount + tableLines <= MAX_LINES_PER_PAGE) {
          currentPage.push(...currentTable);
          currentLineCount += tableLines;
        } else {
          // 不能容纳，先保存当前页，再开启新页
          if (currentPage.length > 0) {
            pages.push(currentPage.join('\n'));
            currentPage = [];
            currentLineCount = 0;
          }
          currentPage.push(...currentTable);
          currentLineCount += tableLines;
        }
        
        currentTable = [];
        inTable = false;
      }
      continue;
    }

    // 如果在表格中，继续累积
    if (inTable) {
      currentTable.push(line);
      continue;
    }

    // 普通行处理
    // 检查当前行加入后是否超过行数限制
    if (currentLineCount + 1 > MAX_LINES_PER_PAGE) {
      // 超过限制，先保存当前页
      pages.push(currentPage.join('\n'));
      currentPage = [];
      currentLineCount = 0;
    }
    
    currentPage.push(line);
    currentLineCount += 1;
  }

  // 处理剩余的代码块
  if (inCodeBlock && currentCodeBlock.length > 0) {
    const codeBlockLines = currentCodeBlock.length;
    if (currentLineCount + codeBlockLines > MAX_LINES_PER_PAGE && currentPage.length > 0) {
      pages.push(currentPage.join('\n'));
      currentPage = [];
      currentLineCount = 0;
    }
    currentPage.push(...currentCodeBlock);
    currentLineCount += codeBlockLines;
  }

  // 处理剩余的表格
  if (inTable && currentTable.length > 0) {
    const tableLines = currentTable.length;
    if (currentLineCount + tableLines > MAX_LINES_PER_PAGE && currentPage.length > 0) {
      pages.push(currentPage.join('\n'));
      currentPage = [];
      currentLineCount = 0;
    }
    currentPage.push(...currentTable);
    currentLineCount += tableLines;
  }

  // 处理剩余的普通内容
  if (currentPage.length > 0) {
    pages.push(currentPage.join('\n'));
  }
  
  debugLog(`内容分割完成，共 ${pages.length} 页`);
  pages.forEach((page, index) => {
    debugLog(`第 ${index + 1} 页行数：${page.split('\n').length}`);
  });

  return pages;
}

/**
 * 确保目录存在，如果不存在则创建
 * @param {string} filePath - 文件路径
 */
function ensureDirExists(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * 写入日志文件
 * @param {string} outputPath - 输出图片路径
 * @param {object} logInfo - 日志信息
 */
function writeLog(outputPath, logInfo) {
  // 日志文件路径：和图片同目录，同名.log后缀
  const logPath = outputPath.replace(path.extname(outputPath), '.log');
  
  // 确保目录存在
  ensureDirExists(logPath);
  
  const logContent = `=== 图片生成日志 ===
生成时间: ${new Date().toLocaleString('zh-CN')}
输入文件: ${logInfo.inputPath || '动态内容'}
输出图片: ${outputPath}
图片大小: ${logInfo.fileSize || '0'} KB
生成耗时: ${logInfo.duration || '0'} ms
内容长度: ${logInfo.contentLength || '0'} 字符
图片高度: ${logInfo.imageHeight || '0'} px
状态: ${logInfo.status || '成功'}
${logInfo.error ? `错误信息: ${logInfo.error.stack || logInfo.error.message}` : ''}
====================
`;

  fs.writeFileSync(logPath, logContent, 'utf8');
  console.log(`📝 日志已保存到：${logPath}`);
}

/**
 * 生成单页图片
 * @param {string} htmlContent - 页面HTML内容
 * @param {string} outputPath - 输出图片路径
 * @param {object} logInfo - 日志信息对象
 * @returns {Promise<number>} 生成的图片高度
 */
async function generateSinglePage(htmlContent, outputPath, logInfo) {
  debugLog(`开始生成单页图片：${outputPath}`);
  
  // 完整HTML页面
  const fullHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Markdown to Image</title>
  <style>
    body {
      font-family: "WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Noto Sans CJK SC", "Noto Color Emoji", -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      padding: 40px;
      max-width: 800px;
      margin: 0 auto;
      background: white;
      color: #333;
      line-height: 1.6;
    }
    h1, h2, h3 { color: #2c3e50; margin-top: 24px; margin-bottom: 16px; }
    h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    code { background: #f6f8fa; padding: 0.2em 0.4em; border-radius: 3px; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }
    pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }
    pre code { background: none; padding: 0; }
    blockquote { border-left: 4px solid #dfe2e5; padding: 0 1em; color: #6a737d; margin: 0; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; }
    th, td { border: 1px solid #dfe2e5; padding: 6px 13px; text-align: left; }
    th { background: #f6f8fa; font-weight: 600; }
    ul, ol { padding-left: 2em; }
    li { margin: 4px 0; }
    .emoji { font-family: "Noto Color Emoji", 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; }
    .page-footer {
      text-align: center;
      margin-top: 20px;
      padding-top: 10px;
      border-top: 1px solid #eee;
      color: #999;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  ${htmlContent}
</body>
</html>
`;

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    headless: true
  });
  
  const page = await browser.newPage();
  await page.setContent(fullHtml, { waitUntil: 'networkidle0' });
  
  // 获取内容高度
  const bodyHandle = await page.$('body');
  const { height } = await bodyHandle.boundingBox();
  await bodyHandle.dispose();
  const imageHeight = Math.ceil(height);
  
  // 设置视口
  await page.setViewport({
    width: 900,
    height: imageHeight,
    deviceScaleFactor: 2
  });
  
  // 确保目录存在
  ensureDirExists(outputPath);
  
  // 根据扩展名确定图片类型和参数
  const ext = path.extname(outputPath).toLowerCase();
  const isJpeg = ext === '.jpg' || ext === '.jpeg';
  const screenshotOptions = {
    path: outputPath,
    fullPage: true,
    type: isJpeg ? 'jpeg' : 'png'
  };
  
  // 只有JPEG支持质量参数
  if (isJpeg) {
    screenshotOptions.quality = IMAGE_QUALITY;
  }
  
  // 截图
  await page.screenshot(screenshotOptions);
  
  await browser.close();
  
  // 获取文件大小
  const stats = fs.statSync(outputPath);
  const fileSize = Math.round(stats.size / 1024);
  
  return { height: imageHeight, size: fileSize };
}

/**
 * markdown转图片工具（支持分页）
 * @param {string} mdContent - markdown内容
 * @param {string} outputPath - 输出图片路径
 * @returns {Promise<Array<string>>} 生成的图片路径列表
 */
async function md2img(mdContent, outputPath, inputPath = null) {
  const startTime = Date.now();
  const logInfo = {
    inputPath: inputPath,
    contentLength: mdContent.length,
    status: '成功',
    pages: []
  };

  try {
    console.log(`🚀 开始生成图片：${outputPath}`);
    console.log(`📄 内容长度：${mdContent.length} 字符`);

    // 分割为多页
    let pages;
    if (PAGINATION_MODE === 'height') {
      // 按高度分页
      const blocks = splitIntoContentBlocks(mdContent);
      const blockHeights = await measureBlockHeights(blocks);
      const paginatedBlocks = paginateByHeight(blockHeights, MAX_HEIGHT_PER_PAGE);
      // 将内容块合并为每页的markdown内容
      pages = paginatedBlocks.map(page => {
        return page.blocks.map(block => block.content).join('\n\n');
      });
    } else {
      // 按行数分页（默认）
      pages = splitMarkdownIntoPages(mdContent);
    }
    const totalPages = pages.length;
    console.log(`📑 内容已分割为 ${totalPages} 页`);
    
    if (totalPages === 0) {
      throw new Error('内容为空，无法生成图片');
    }

    const generatedPaths = [];
    let totalHeight = 0;
    let totalSize = 0;

    // Debug 模式下保存分页内容
    if (DEBUG) {
      debugLog('Debug 模式已启用，保存分页内容到本地');
      const baseName = path.basename(outputPath, path.extname(outputPath));
      const outputDir = path.dirname(outputPath);
      
      // 确保目录存在
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }
      
      pages.forEach((page, index) => {
        const pageFilePath = path.join(outputDir, `${baseName}_page_${index + 1}.md`);
        fs.writeFileSync(pageFilePath, page, 'utf8');
        debugLog(`已保存第 ${index + 1} 页内容到：${pageFilePath}`);
      });
    }

    // 生成每页图片
    for (let i = 0; i < totalPages; i++) {
      const pageNum = i + 1;
      const pageContent = pages[i];
      debugLog(`正在处理第 ${pageNum}/${totalPages} 页`);
      
      // 添加页脚
      const pageContentWithFooter = totalPages > 1 
        ? `${pageContent}\n\n<div class="page-footer">第 ${pageNum} 页 / 共 ${totalPages} 页</div>`
        : pageContent;
      
      // 转换为HTML
      const htmlContent = marked.parse(pageContentWithFooter);
      
      // 生成输出路径
      let pageOutputPath;
      if (totalPages === 1) {
        pageOutputPath = outputPath;
      } else {
        const ext = path.extname(outputPath);
        const baseName = path.basename(outputPath, ext);
        const dirName = path.dirname(outputPath);
        pageOutputPath = path.join(dirName, `${baseName}_${pageNum}${ext}`);
      }
      
      console.log(`🖨️  正在生成第 ${pageNum}/${totalPages} 页：${pageOutputPath}`);
      
      const { height, size } = await generateSinglePage(htmlContent, pageOutputPath, logInfo);
      
      generatedPaths.push(pageOutputPath);
      totalHeight += height;
      totalSize += size;
      
      logInfo.pages.push({
        pageNum,
        path: pageOutputPath,
        height,
        size
      });
      
      console.log(`✅ 第 ${pageNum}/${totalPages} 页生成完成，高度：${height} px，大小：${size} KB`);
    }

    // 计算耗时
    const duration = Date.now() - startTime;
    logInfo.duration = duration;
    logInfo.imageHeight = totalHeight;
    logInfo.fileSize = totalSize;
    
    console.log(`✅ 所有页面生成完成，总高度：${totalHeight} px，总大小：${totalSize} KB`);
    console.log(`⏱️  总生成耗时：${duration} ms`);

    // 写入日志
    writeLog(outputPath, logInfo);

    return generatedPaths;
  } catch (err) {
    logInfo.status = '失败';
    logInfo.error = err;
    logInfo.duration = Date.now() - startTime;
    
    // 写入错误日志
    writeLog(outputPath, logInfo);
    
    console.error(`❌ 转换失败：${err.message}`);
    throw err;
  }
}

// 如果直接运行脚本，从命令行参数获取输入和输出
if (require.main === module) {
  const args = process.argv.slice(2);
  
  // 检查是否有 --debug 参数
  const debugIndex = args.indexOf('--debug');
  if (debugIndex !== -1) {
    DEBUG = true;
    args.splice(debugIndex, 1); // 移除 debug 参数
    debugLog('Debug 模式已启用');
  }
  
  // 检查是否有 --height 参数（按高度分页）
  const heightIndex = args.indexOf('--height');
  if (heightIndex !== -1) {
    PAGINATION_MODE = 'height';
    args.splice(heightIndex, 1); // 移除 height 参数
    debugLog('按高度分页模式已启用');
  }
  
  if (args.length < 2) {
    console.error('使用方法: node md_to_png.js <输入markdown文件> <输出图片路径> [分页阈值] [图片质量，默认80] [--height] [--debug]');
    console.error('示例1（按行数分页，默认500行）: node md_to_png.js input.md output.jpg');
    console.error('示例2（按行数分页，自定义400行）: node md_to_png.js input.md output.jpg 400');
    console.error('示例3（按高度分页，默认15000px）: node md_to_png.js input.md output.jpg --height');
    console.error('示例4（按高度分页，自定义20000px）: node md_to_png.js input.md output.jpg 20000 --height');
    console.error('示例5（带debug模式）: node md_to_png.js input.md output.jpg --height --debug');
    process.exit(1);
  }
  
  const inputPath = args[0];
  const outputPath = args[1];
  
  // 支持自定义分页阈值（行数或高度）
  if (args[2] && !args[2].startsWith('--')) {
    const customThreshold = parseInt(args[2], 10);
    if (!isNaN(customThreshold)) {
      if (PAGINATION_MODE === 'height') {
        if (customThreshold > 0) {
          MAX_HEIGHT_PER_PAGE = customThreshold;
          console.log(`🔧 自定义每页最大高度：${MAX_HEIGHT_PER_PAGE}px`);
        } else {
          // 高度阈值<=0时禁用高度分页，生成单页
          MAX_HEIGHT_PER_PAGE = Infinity;
          console.log(`🔧 高度阈值<=0，禁用高度分页，生成单页`);
        }
      } else {
        if (customThreshold > 0) {
          MAX_LINES_PER_PAGE = customThreshold;
          console.log(`🔧 自定义每页最大行数：${MAX_LINES_PER_PAGE}`);
        } else {
          // 行数阈值<=0时禁用行数分页，生成单页
          MAX_LINES_PER_PAGE = Infinity;
          console.log(`🔧 行数阈值<=0，禁用途数分页，生成单页`);
        }
      }
    }
  }
  
  // 支持自定义图片质量
  if (args[3] && !args[3].startsWith('--')) {
    const customQuality = parseInt(args[3], 10);
    if (!isNaN(customQuality) && customQuality >= 1 && customQuality <= 100) {
      IMAGE_QUALITY = customQuality;
      console.log(`🔧 自定义图片质量：${IMAGE_QUALITY}`);
    }
  }
  
  const mdContent = fs.readFileSync(inputPath, 'utf8');
  
  md2img(mdContent, outputPath, inputPath)
    .then((generatedPaths) => {
      if (generatedPaths.length === 1) {
        console.log(`✅ 转换成功！图片已保存到：${generatedPaths[0]}`);
      } else {
        console.log(`✅ 转换成功！共生成 ${generatedPaths.length} 页：`);
        generatedPaths.forEach((path, index) => {
          console.log(`   ${index + 1}. ${path}`);
        });
      }
      process.exit(0);
    })
    .catch(err => {
      console.error('❌ 转换失败：', err);
      process.exit(1);
    });
}

module.exports = md2img;

/**
 * 预计算每个内容块的渲染高度
 * @param {Array<string>} blocks - 内容块数组
 * @returns {Array<Object>} 每个块的高度信息
 */
async function measureBlockHeights(blocks) {
  debugLog('开始预计算内容块高度');
  
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  const blockHeights = [];
  let totalHeight = 0;
  
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    const html = marked.parse(block);
    
    await page.setContent(`<div style="width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">${html}</div>`, { waitUntil: 'networkidle0' });
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

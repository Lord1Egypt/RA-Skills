#!/usr/bin/env node

/**
 * 搜索 Google（自动清理标签页）- v2
 * 用法: node search-google.js "搜索关键词"
 */

const BrowserManager = require('./browser-manager.v2');

const keyword = process.argv[2] || 'OpenClaw 浏览器自动化';

async function main() {
  const browser = new BrowserManager(process.env.BROWSER_PROFILE || 'openclaw', {
    timeout: 30000,
    retries: 2
  });
  
  try {
    console.log(`🔍 执行 Google 搜索: ${keyword}`);
    
    await browser.start();
    
    // 打开 Google
    await browser.open('https://www.google.com');
    await browser.waitForLoadState('domcontentloaded'); // 智能等待
    
    // 获取快照定位搜索框和按钮
    const snapshot = await browser.snapshot('ai', 150);
    
    // 解析搜索框（combobox "搜索" 或 "Search"）
    const inputMatch = snapshot.match(/combobox[^\n]*\[ref=(e\d+)\]/i) ||
                       snapshot.match(/input[^\\n]*\[ref=(e\d+)\][^\\n]*search/i);
    
    if (!inputMatch) {
      throw new Error('未找到搜索框');
    }
    
    const inputRef = inputMatch[1];
    
    // 输入关键词
    await browser.type(inputRef, keyword);
    
    // 按回车（Google 搜索框支持回车提交）
    await browser.press('Enter');
    console.log('✅ 搜索完成');
    
    // 等待结果加载
    await browser.waitForLoadState('networkidle', 10000);
    
    // 截图
    const screenshotPath = await browser.screenshot();
    console.log('📸 截图:', screenshotPath);
    
    // 导出 PDF
    await browser.pdf();
    
    console.log('🎉 搜索完成！正在清理...');
    
    // 关闭所有标签页并停止浏览器（v2 会自动清理）
    await browser.cleanup();
    
  } catch (e) {
    browser.logger.error('搜索失败', { error: e.message });
    await browser.cleanup();
    process.exit(1);
  }
}

main();

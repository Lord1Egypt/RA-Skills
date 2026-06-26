#!/usr/bin/env node

/**
 * AudTools Shopify 批量采集脚本
 * 
 * 功能：
 * 1. 打开 https://www.audtools.com/users/shopns#/users/shopns/collecs
 * 2. 读取 CSV 文件中的完整链接列
 * 3. 在输入框中依次填入每个链接
 * 4. 商品数设置成 9999
 * 5. 点击提交，每条间隔 2 秒
 * 
 * 使用方法：
 *   node batch-collect-fixed.js [csv-file-path]
 * 
 * 示例：
 *   node batch-collect-fixed.js C:\workspace\caiji\shop-futvortexstore-com-categories.csv
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 手动解析 CSV，处理带引号的 CSV
function parseCSV(content) {
  const lines = content.split('\n').filter(line => line.trim());
  if (lines.length === 0) {
    return [];
  }
  
  // 读取表头
  const headers = parseCSVLine(lines[0]);
  console.log(`📊 表头: ${headers.join(', ')}`);
  
  const results = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    
    const values = parseCSVLine(line);
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });
    results.push(row);
  }
  
  return results;
}

// 解析 CSV 一行，处理引号
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    
    if (char === '"' && inQuotes && line[i+1] === '"') {
      current += '"';
      i++;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  
  result.push(current.trim());
  return result;
}

async function batchCollect(csvFilePath) {
  // 检查文件是否存在
  if (!fs.existsSync(csvFilePath)) {
    console.error(`❌ 文件不存在: ${csvFilePath}`);
    process.exit(1);
  }
  
  // 读取 CSV 文件
  console.log(`📖 正在读取 CSV 文件: ${csvFilePath}`);
  const content = fs.readFileSync(csvFilePath, 'utf-8');
  const results = parseCSV(content);
  
  console.log(`✅ 读取完成，共 ${results.length} 条链接`);
  
  // 提取完整链接列 - 尝试多种匹配
  const links = [];
  results.forEach(row => {
    let link = null;
    // 尝试不同的键名
    for (const key in row) {
      if (key.includes('完整链接')) {
        link = row[key];
        break;
      }
    }
    if (link && link.trim()) {
      links.push(link.trim());
    }
  });
  
  console.log(`🔗 有效链接数量: ${links.length}`);
  
  if (links.length === 0) {
    console.log('⚠️  调试 - 所有行:');
    results.forEach((row, i) => {
      console.log(`  行 ${i+1}: 键 = ${Object.keys(row).join(', ')}`);
    });
    console.error('❌ 没有找到有效的链接');
    process.exit(1);
  }
  
  // 输出前 5 条预览
  console.log('\n📋 前 5 条链接预览:');
  links.slice(0, 5).forEach((link, i) => {
    console.log(`  ${i+1}. ${link}`);
  });
  
  // 启动浏览器
  const browser = await chromium.launch({ 
    headless: false,
    timeout: 60000
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });
  
  const page = await context.newPage();
  page.setDefaultTimeout(60000);
  
  const url = 'https://www.audtools.com/users/shopns#/users/shopns/collecs';
  console.log(`\n🌐 正在打开: ${url}`);
  
  try {
    await page.goto(url, { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });
    
    console.log('✅ 页面加载完成');
    
    // 等待页面加载，检查是否需要登录
    await page.waitForTimeout(3000);
    
    // 检查是否有登录表单
    const hasLoginForm = await page.$('form input[type="password"], input[name="password"]');
    
    if (hasLoginForm) {
      console.log('\n🔐 需要登录，请输入账户密码后继续...');
      console.log('请在浏览器中完成登录，然后告诉我继续执行...');
      // 这里需要用户手动登录
      // 我们保持浏览器打开，让用户操作
      console.log('\n⚠️  需要你手动输入账户密码登录，登录完成后告诉我继续执行。');
      return {
        status: 'need-login',
        browser: browser,
        page: page,
        links: links
      };
    }
    
    // 如果不需要登录，直接开始批量提交
    await processBatch(page, links);
    
    await browser.close();
    
    console.log('\n🎉 批量采集完成！');
    return {
      status: 'completed',
      total: links.length
    };
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    await browser.close();
    throw error;
  }
}

async function processBatch(page, links) {
  console.log('\n🚀 开始批量处理...');
  
  // 等待页面加载完成，找到输入框
  console.log('🔍 查找输入框...');
  
  // 等待输入框出现
  const inputSelector = await findInputSelector(page);
  console.log(`✅ 找到输入框，使用选择器: ${inputSelector}`);
  
  // 找到商品数量输入框
  const quantitySelector = await findQuantityInput(page);
  console.log(`✅ 找到商品数量输入框: ${quantitySelector || '未找到，将使用默认'}`);
  
  // 处理每个链接
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    console.log(`\n[${i+1}/${links.length}] 处理: ${link}`);
    
    try {
      // 清空输入框，填入链接
      await page.fill(inputSelector, '');
      await page.fill(inputSelector, link);
      console.log(`  ✅ 已填入链接`);
      
      // 设置商品数量为 9999
      if (quantitySelector) {
        await page.fill(quantitySelector, '');
        await page.fill(quantitySelector, '9999');
        console.log(`  ✅ 商品数量已设置为 9999`);
      }
      
      // 查找提交按钮并点击
      const submitButton = await findSubmitButton(page);
      if (submitButton) {
        await submitButton.click();
        console.log(`  ✅ 已点击提交`);
        
        // 等待 2 秒
        console.log(`  ⏳ 等待 2 秒...`);
        await page.waitForTimeout(2000);
      }
      
    } catch (error) {
      console.error(`  ❌ 处理失败: ${error.message}`);
      // 继续下一个
      await page.waitForTimeout(2000);
    }
  }
  
  console.log(`\n✅ 所有 ${links.length} 条链接处理完成`);
  console.log('请在浏览器中查看采集结果，导出数据...');
}

async function findInputSelector(page) {
  // 尝试多种选择器找链接输入框
  const selectors = [
    'input[name="collection_url"]',
    'input[name="url"]',
    'input[placeholder*="url"]',
    'input[placeholder*="link"]',
    'input[placeholder*="collection"]',
    'textarea[name*="collection"]',
    'textarea',
    '.form-control',
    'input[type="text"]'
  ];
  
  for (const selector of selectors) {
    const element = await page.$(selector);
    if (element) {
      return selector;
    }
  }
  
  // 如果都没找到，返回第一个 text input
  return 'input[type="text"]';
}

async function findQuantityInput(page) {
  // 尝试多种选择器找商品数量输入框
  const selectors = [
    'input[name="limit"]',
    'input[name="quantity"]',
    'input[name="count"]',
    'input[name="products"]',
    'input[placeholder*="limit"]',
    'input[placeholder*="quantity"]',
    'input[placeholder*="count"]',
    'input[placeholder*="product"]',
    'input[type="number"]'
  ];
  
  for (const selector of selectors) {
    const element = await page.$(selector);
    if (element) {
      return selector;
    }
  }
  
  return null;
}

async function findSubmitButton(page) {
  // 尝试多种选择器找提交按钮
  const selectors = [
    'button[type="submit"]',
    'input[type="submit"]',
    'button:has-text("提交")',
    'button:has-text("Submit")',
    'button:has-text("采集")',
    'button:has-text("Start")',
    'button:has-text("开始")',
    '.btn-primary',
    '.btn-success',
    'button'
  ];
  
  for (const selector of selectors) {
    const element = await page.$(selector);
    if (element) {
      return element;
    }
  }
  
  return null;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  let csvFilePath = args[0];
  
  if (!csvFilePath) {
    // 默认路径
    csvFilePath = 'C:\\workspace\\caiji\\full\\shop-futvortexstore-com-categories.csv';
  }
  
  console.log(`🚀 AudTools Shopify 批量采集
  CSV 文件: ${csvFilePath}
  设置商品数: 9999
  操作间隔: 2 秒
`);
  
  try {
    const result = await batchCollect(csvFilePath);
    
    if (result.status === 'need-login') {
      console.log('\n⏸️  已暂停，请在打开的浏览器中登录账户，登录完成后告诉我继续...');
      // 不关闭浏览器，保持打开让用户登录
      // 用户继续后会继续执行
    } else {
      console.log('\n✅ 批量处理完成！请在浏览器中导出采集结果。');
      process.exit(0);
    }
    
  } catch (error) {
    console.error('\n💥 处理失败:', error.message);
    process.exit(1);
  }
}

// 如果直接运行
if (require.main === module) {
  main();
}

module.exports = batchCollect;

#!/usr/bin/env node

/**
 * 电商分类采集脚本
 * 从CSV文件批量提交Audtools采集任务，并支持已采集商品全选导出
 */

const fs = require('fs');
const path = require('path');
const csv = require('csv-parse/sync');
const { execSync } = require('child_process');

// 配置参数
const CONFIG = {
  baseUrl: 'https://www.audtools.com',
  loginUrl: 'https://www.audtools.com/login',
  collecUrl: 'https://www.audtools.com/users/shopns#/users/shopns/collecs?spm=m-1-2-3',
  username: '15715090600',
  password: 'zzw12345',
  default_items: 9999,
  default_interval: 2000, // 毫秒
  default_close_delay: 3000, // 毫秒
  exportWaitTimeout: 30000, // 导出等待超时（毫秒）
};

/**
 * 验证CSV文件格式
 * @param {string} filePath CSV文件路径
 * @returns {Array} 验证通过的链接数组
 */
function validateCSV(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const records = csv.parse(content, {
      columns: true,
      skip_empty_lines: true,
    });

    if (records.length === 0) {
      throw new Error('CSV文件为空或没有数据行');
    }

    // 检查必需的列
    const requiredColumns = ['完整链接'];
    const firstRecord = records[0];
    const missingColumns = requiredColumns.filter(col => !(col in firstRecord));
    
    if (missingColumns.length > 0) {
      throw new Error(`CSV文件缺少必需的列: ${missingColumns.join(', ')}`);
    }

    // 提取并验证链接
    const links = records.map((record, index) => {
      const link = record['完整链接'].trim();
      if (!link) {
        throw new Error(`第${index + 2}行: "完整链接"列为空`);
      }
      
      // 验证链接格式
      if (!link.startsWith('http')) {
        throw new Error(`第${index + 2}行: 链接格式不正确 "${link}"`);
      }
      
      // 验证是否为collections链接
      if (!link.includes('/collections/')) {
        console.warn(`警告: 第${index + 2}行链接可能不是collections链接: "${link}"`);
      }
      
      return {
        url: link,
        row: index + 2,
        data: record,
      };
    });

    console.log(`✅ CSV文件验证通过: ${filePath}`);
    console.log(`   共发现 ${links.length} 条有效链接`);
    
    return links;
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error(`文件不存在: ${filePath}`);
    }
    throw new Error(`CSV文件验证失败: ${error.message}`);
  }
}

/**
 * 获取目录下所有CSV文件
 * @param {string} dirPath 目录路径
 * @returns {Array} CSV文件路径数组
 */
function getCSVFiles(dirPath) {
  try {
    const files = fs.readdirSync(dirPath);
    const csvFiles = files.filter(file => {
      const ext = path.extname(file).toLowerCase();
      return ext === '.csv' && fs.statSync(path.join(dirPath, file)).isFile();
    });
    
    if (csvFiles.length === 0) {
      throw new Error(`目录中没有找到CSV文件: ${dirPath}`);
    }
    
    return csvFiles.map(file => path.join(dirPath, file));
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error(`目录不存在: ${dirPath}`);
    }
    throw error;
  }
}

/**
 * 等待指定毫秒数
 * @param {number} ms 毫秒数
 */
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 检查是否已登录，如未登录则执行登录
 * @param {Object} browser OpenClaw browser实例
 */
async function ensureLoggedIn(browser, targetId) {
  console.log(`   检查登录状态...`);
  
  // 检查当前页面是否是登录页
  const currentUrl = await browser.evaluate({
    targetId,
    fn: () => window.location.href
  });
  
  if (currentUrl.includes('/login')) {
    console.log(`   未登录，开始登录...`);
    
    // 输入手机号
    await browser.act({
      kind: 'fill',
      targetId,
      selector: 'input[type="tel"]',
      text: CONFIG.username
    });
    await wait(500);
    
    // 输入密码
    await browser.act({
      kind: 'fill',
      targetId,
      selector: 'input[type="password"]',
      text: CONFIG.password
    });
    await wait(500);
    
    // 点击登录按钮
    await browser.act({
      kind: 'click',
      targetId,
      selector: 'button[type="submit"]'
    });
    
    // 等待登录完成跳转
    await wait(3000);
    console.log(`   ✅ 登录完成`);
  } else {
    console.log(`   ✅ 已登录`);
  }
}

/**
 * 提交采集任务
 * @param {Object} browser OpenClaw browser实例
 * @param {string} targetId tab id
 * @param {string} collectionUrl 分类链接
 * @param {number} items 采集商品数
 */
async function submitCollection(browser, targetId, collectionUrl, items) {
  console.log(`   提交采集任务: ${collectionUrl}`);
  
  // 等待页面加载
  await wait(2000);
  
  // 输入collections链接
  await browser.act({
    kind: 'fill',
    targetId,
    selector: 'input[placeholder*="链接"]',
    text: collectionUrl
  });
  await wait(500);
  
  // 修改采集数量
  const itemsInput = await browser.evaluate({
    targetId,
    fn: () => {
      const input = document.querySelector('input[type="number"]');
      if (input) {
        input.value = '';
        return true;
      }
      return false;
    }
  });
  
  if (itemsInput) {
    await browser.act({
      kind: 'fill',
      targetId,
      selector: 'input[type="number"]',
      text: String(items)
    });
    await wait(500);
  }
  
  // 点击开始采集按钮
  await browser.act({
    kind: 'click',
    targetId,
    selector: 'button:contains("开始采集")'
  });
  
  await wait(2000);
  console.log(`   ✅ 采集任务已提交`);
}

/**
 * 对已采集商品执行全选导出
 * @param {string} categoryPath 分类路径
 */
async function exportAllCollectedItems(browser, targetId, categoryPath) {
  console.log(`   执行全选导出: ${categoryPath}`);
  
  // 等待列表加载
  await wait(3000);
  
  // 找到对应任务行，点击已采集数列进入详情页
  // 实际这里需要根据分类路径查找对应的行
  // 简化处理：直接点击第一个已采集数链接（测试用）
  const collectedLinkExists = await browser.evaluate({
    targetId,
    fn: () => {
      const link = document.querySelector('a:contains("已采集")');
      return !!link;
    }
  });
  
  if (!collectedLinkExists) {
    throw new Error('找不到已采集商品链接，请确认采集任务已完成');
  }
  
  // 在新标签页打开详情页
  await browser.act({
    kind: 'click',
    targetId,
    selector: 'a:contains("已采集")'
  });
  
  await wait(3000);
  
  // 获取所有打开的标签页
  const tabs = await browser.tabs();
  const detailTabId = tabs[tabs.length - 1].id;
  console.log(`   详情页已打开: ${detailTabId}`);
  
  // 全选所有商品（layui-table 特殊处理）
  console.log(`   开始全选商品...`);
  
  // layui 处理：点击 .layui-form-checkbox 后，还要确保实际input被选中
  const selectAllResult = await browser.evaluate({
    targetId: detailTabId,
    fn: () => {
      // 先尝试表头全选
      const headerCheckbox = document.querySelector('.layui-table-header .layui-form-checkbox');
      if (headerCheckbox) {
        headerCheckbox.click();
        // 同时确保所有行都选中
        const bodyCheckboxes = document.querySelectorAll('.layui-table-body .layui-form-checkbox');
        bodyCheckboxes.forEach(cb => {
          if (!cb.classList.contains('layui-form-checked')) {
            cb.click();
          }
          // 额外处理：找到实际的input checkbox确保它被选中
          const input = cb.parentNode.querySelector('input[type=\"checkbox\"]');
          if (input && !input.checked) {
            input.checked = true;
          }
        });
        return { done: true, count: bodyCheckboxes.length };
      }
      
      // 没有表头全选，逐个勾选
      const bodyCheckboxes = document.querySelectorAll('.layui-table-body .layui-form-checkbox');
      bodyCheckboxes.forEach(cb => {
        if (!cb.classList.contains('layui-form-checked')) {
          cb.click();
        }
        // 额外处理：找到实际的input checkbox确保它被选中
        const input = cb.parentNode.querySelector('input[type=\"checkbox\"]');
        if (input && !input.checked) {
          input.checked = true;
        }
      });
      return { done: false, count: bodyCheckboxes.length };
    }
  });
  
  if (selectAllResult.done) {
    console.log(`   使用表头全选，共 ${selectAllResult.count} 个商品`);
  } else {
    console.log(`   逐个勾选，共 ${selectAllResult.count} 个商品`);
  }
  await wait(1000);
  
  // 验证选中数量
  const selectedCount = await browser.evaluate({
    targetId: detailTabId,
    fn: () => {
      return document.querySelectorAll('.layui-table-body .layui-form-checked').length;
    }
  });
  
  console.log(`   ✅ 已选中 ${selectedCount} 个商品`);
  
  // 填入分类路径
  // 找到分类输入框
  await browser.evaluate({
    targetId: detailTabId,
    fn: (categoryPath) => {
      const input = document.querySelector('input[placeholder*="分类"]');
      if (input) {
        input.value = categoryPath;
        return true;
      }
      return false;
    },
    args: [categoryPath]
  });
  await wait(500);
  
  // 点击导出按钮（底部的导出按钮，不是顶部的shopify CSV按钮）
  console.log(`   点击导出按钮...`);
  await browser.evaluate({
    targetId: detailTabId,
    fn: () => {
      const buttons = document.querySelectorAll('button');
      for (let btn of buttons) {
        if (btn.textContent.trim() === '导出') {
          btn.click();
          return true;
        }
      }
      return false;
    }
  });
  
  // 等待导出跳转/下载
  console.log(`   ⏳ 等待导出处理...`);
  await wait(8000);
  
  console.log(`   ✅ 导出已触发`);
  console.log(`   ℹ️  如果跳转后出现401，是因为token验证问题，需要在当前浏览器实例手动确认下载`);
  
  // 不关闭详情标签页，让用户确认下载完成
  console.log(`   📄 详情页保持打开，等待下载完成`);
  
  return selectedCount;
}

/**
 * 执行采集/导出任务
 * @param {Array} links 链接数组
 * @param {Object} options 选项
 * @param {Object} browser browser实例
 */
async function executeCollection(links, options = {}, browser) {
  const {
    items = CONFIG.default_items,
    interval = CONFIG.default_interval,
    closeDelay = CONFIG.default_close_delay,
    testMode = false,
    exportAfterCollect = true, // 采集完成后是否导出
  } = options;

  console.log(`🚀 开始任务`);
  console.log(`   采集商品数: ${items}`);
  console.log(`   操作间隔: ${interval}ms`);
  console.log(`   Tab关闭延迟: ${closeDelay}ms`);
  console.log(`   采集后导出: ${exportAfterCollect ? '是' : '否'}`);
  console.log(`   测试模式: ${testMode ? '是（只处理前3条）' : '否'}`);
  
  const totalLinks = testMode ? Math.min(links.length, 3) : links.length;
  console.log(`   处理链接数: ${totalLinks}/${links.length}`);
  
  // 打开主页面并确保登录
  const mainTab = await browser.open({ url: CONFIG.collecUrl });
  const mainTargetId = mainTab.id;
  await ensureLoggedIn(browser, mainTargetId);
  await wait(2000);
  
  let successCount = 0;
  let totalSelected = 0;
  
  for (let i = 0; i < totalLinks; i++) {
    const link = links[i];
    console.log(`\n📋 处理第 ${i + 1}/${totalLinks} 条链接 (CSV第${link.row}行)`);
    console.log(`   URL: ${link.url}`);
    
    try {
      // 提取分类路径
      const urlParts = link.url.split('/collections/');
      let categoryPath = '';
      if (urlParts.length > 1) {
        categoryPath = urlParts[1].split('?')[0].split('#')[0];
      }
      // 如果CSV中已有分类路径，优先使用
      if (link.data['分类路径']) {
        categoryPath = link.data['分类路径'].trim();
      }
      
      console.log(`   分类路径: ${categoryPath}`);
      
      // 提交采集任务（已经采集过可以跳过）
      await submitCollection(browser, mainTargetId, link.url, items);
      
      // 执行全选导出
      let selected = 0;
      if (exportAfterCollect) {
        selected = await exportAllCollectedItems(browser, mainTargetId, categoryPath);
        totalSelected += selected;
      }
      
      successCount++;
      console.log(`   ✅ 完成，选中 ${selected} 个商品`);
      
    } catch (error) {
      console.error(`   ❌ 处理失败: ${error.message}`);
      // 继续处理下一条
    }
    
    // 如果不是最后一条，等待间隔时间
    if (i < totalLinks - 1) {
      console.log(`   ⏳ 等待 ${interval}ms 处理下一条...`);
      await wait(interval);
    }
  }
  
  console.log(`\n🎉 任务完成！`);
  console.log(`   成功处理: ${successCount}/${totalLinks} 条链接`);
  console.log(`   总共选中导出: ${totalSelected} 个商品`);
}

/**
 * 主函数
 */
async function main(browser = null) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('使用方法:');
    console.log('  node collector.js <csv文件或目录> [选项]');
    console.log('');
    console.log('选项:');
    console.log('  --items <数量>        采集商品数（默认: 9999）');
    console.log('  --interval <毫秒>     操作间隔（默认: 2000）');
    console.log('  --close-delay <毫秒>   tab关闭延迟（默认: 3000）');
    console.log('  --test                测试模式（只处理前3条）');
    console.log('  --no-export           不执行导出，只提交采集任务');
    console.log('');
    console.log('示例:');
    console.log('  node collector.js /path/to/data.csv');
    console.log('  node collector.js /path/to/directory/ --test');
    console.log('  node collector.js data.csv --items 5000 --interval 3000');
    return;
  }
  
  const inputPath = args[0];
  const options = {
    exportAfterCollect: true,
  };
  
  // 解析选项
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--items' && args[i + 1]) {
      options.items = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--interval' && args[i + 1]) {
      options.interval = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--close-delay' && args[i + 1]) {
      options.closeDelay = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--test') {
      options.testMode = true;
    } else if (args[i] === '--no-export') {
      options.exportAfterCollect = false;
    }
  }
  
  try {
    // 检查输入路径
    const stats = fs.statSync(inputPath);
    let csvFiles = [];
    let allLinks = [];
    
    if (stats.isDirectory()) {
      // 处理目录
      console.log(`📁 扫描目录: ${inputPath}`);
      csvFiles = getCSVFiles(inputPath);
      console.log(`   找到 ${csvFiles.length} 个CSV文件`);
      
      // 验证所有CSV文件
      for (const file of csvFiles) {
        console.log(`\n🔍 验证文件: ${path.basename(file)}`);
        const links = validateCSV(file);
        allLinks.push(...links.map(link => ({
          ...link,
          sourceFile: path.basename(file),
        })));
      }
    } else {
      // 处理单个文件
      console.log(`📄 处理文件: ${inputPath}`);
      const links = validateCSV(inputPath);
      allLinks = links.map(link => ({
        ...link,
        sourceFile: path.basename(inputPath),
      }));
    }
    
    if (allLinks.length === 0) {
      console.log('❌ 没有找到有效的链接');
      return;
    }
    
    console.log(`\n📊 统计信息:`);
    console.log(`   总链接数: ${allLinks.length}`);
    console.log(`   来源文件: ${[...new Set(allLinks.map(l => l.sourceFile))].join(', ')}`);
    
    // 如果没有传入browser实例，这里会由OpenClaw处理
    // 否则直接执行
    if (browser) {
      // 执行采集导出
      await executeCollection(allLinks, options, browser);
    } else {
      // 命令行模式输出说明，实际由OpenClaw browser工具执行
      console.log(`\n🌐 需要通过OpenClaw browser工具执行自动化操作`);
    }
    
  } catch (error) {
    console.error(`❌ 错误: ${error.message}`);
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main(null).catch(error => {
    console.error('致命错误:', error);
    process.exit(1);
  });
}

module.exports = {
  validateCSV,
  getCSVFiles,
  executeCollection,
  ensureLoggedIn,
  submitCollection,
  exportAllCollectedItems,
  CONFIG,
  main,
  wait,
};
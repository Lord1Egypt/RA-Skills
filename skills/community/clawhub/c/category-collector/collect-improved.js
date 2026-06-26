#!/usr/bin/env node

/**
 * Shopify 分类采集器 - 改进版本
 * 从页面导航面包屑提取真实层级，而不是只从 URL 猜测
 * 
 * 使用方法：
 *   node collect-improved.js <website-url> [output-directory]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function collectCategories(startUrl, outputDir = 'C:\\workspace\\caiji') {
  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 从 URL 提取域名作为文件名
  const urlObj = new URL(startUrl);
  const domain = urlObj.hostname.replace(/\./g, '-');
  const outputFile = `${domain}-categories.csv`;
  const csvPath = path.join(outputDir, outputFile);

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
  
  console.log(`🌐 正在打开首页: ${startUrl}`);
  
  try {
    await page.goto(startUrl, { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });
    
    console.log('✅ 首页加载完成');
    
    // 截图保存首页
    const screenshotPath = path.join(outputDir, `${domain}-homepage-screenshot.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log(`📸 首页截图已保存: ${screenshotPath}`);
    
    // 提取所有分类链接
    console.log('🔍 正在提取所有分类链接...');
    const allLinks = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a[href]'));
      const result = [];
      
      links.forEach(link => {
        const href = link.getAttribute('href');
        const text = link.textContent.trim();
        
        // 只收集站内链接
        if (href && !href.includes('#') && !href.includes('javascript:')) {
          result.push({
            href: href,
            text: text
          });
        }
      });
      
      return result;
    });
    
    console.log(`🔗 找到 ${allLinks.length} 个站内链接`);
    
    // 筛选出分类链接（包含 /collections/）
    const collectionLinks = allLinks.filter(link => {
      return link.href.includes('/collections/') || link.href.includes('/categories/');
    });
    
    console.log(`🎯 筛选出 ${collectionLinks.length} 个分类链接`);
    
    // 访问每个分类页面，从面包屑提取真实层级
    const categories = [];
    const seen = new Set();
    
    for (let i = 0; i < collectionLinks.length; i++) {
      const link = collectionLinks[i];
      
      // 转换为完整 URL
      let fullUrl = link.href;
      if (link.href.startsWith('/')) {
        fullUrl = new URL(link.href, startUrl).href;
      }
      
      // 去重
      if (seen.has(fullUrl)) {
        continue;
      }
      seen.add(fullUrl);
      
      // 过滤掉非分类链接
      if (fullUrl.includes('/page/') || 
          fullUrl.includes('/cart') || 
          fullUrl.includes('/checkout') || 
          fullUrl.includes('/account') ||
          fullUrl.includes('/search')) {
        continue;
      }
      
      console.log(`[${i+1}/${collectionLinks.length}] 处理: ${link.text} -> ${fullUrl}`);
      
      try {
        await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(1000); // 等待渲染
        
        // 从面包屑提取层级
        const breadcrumb = await extractBreadcrumb(page);
        
        // 提取 slug
        const urlObj = new URL(fullUrl);
        const pathname = urlObj.pathname;
        const collectionMatch = pathname.match(/\/collections\/([^\/]+(?:\/[^\/]+)*)/) || 
                               pathname.match(/\/categories\/([^\/]+(?:\/[^\/]+)*)/);
        const fullSlug = collectionMatch ? collectionMatch[1] : '';
        
        // 构建分类对象
        const category = {
          fullUrl: fullUrl,
          fullSlug: fullSlug,
          linkText: link.text,
          levels: breadcrumb.levels,
          level1: breadcrumb.levels[0] || '',
          level2: breadcrumb.levels[1] || '',
          level3: breadcrumb.levels[2] || '',
          level4: breadcrumb.levels[3] || '',
          actualDepth: breadcrumb.levels.length,
          title: await page.title()
        };
        
        categories.push(category);
        
        console.log(`   ➜ 层级: ${breadcrumb.levels.join(' > ')} (${breadcrumb.levels.length} 级)`);
        
      } catch (error) {
        console.log(`   ⚠️  处理失败: ${error.message}`);
        // 继续处理下一个
      }
    }
    
    console.log(`\n📊 处理完成，共得到 ${categories.length} 个有效分类`);
    
    if (categories.length === 0) {
      console.log('❌ 未采集到任何分类');
      await browser.close();
      return { count: 0, csvPath: null, categories: [] };
    }
    
    // 生成 CSV
    const csv = generateCSV(categories);
    
    // 保存文件
    fs.writeFileSync(csvPath, csv, 'utf-8');
    
    console.log(`💾 CSV 文件已保存: ${csvPath}`);
    
    // 输出预览
    console.log('\n📋 预览前 10 条:');
    categories.slice(0, 10).forEach((cat, i) => {
      const levels = cat.levels.filter(l => l).join(' > ');
      console.log(`${i+1}. ${cat.fullSlug} -> ${levels}`);
    });
    
    await browser.close();
    
    return {
      count: categories.length,
      csvPath: csvPath,
      categories: categories
    };
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    await browser.close();
    throw error;
  }
}

/**
 * 从页面提取面包屑导航
 */
async function extractBreadcrumb(page) {
  // 尝试多种选择器找面包屑
  const breadcrumbSelectors = [
    '.breadcrumb a',
    '.breadcrumbs a', 
    '.bread-crumb a',
    'nav.breadcrumb a',
    '.collection-breadcrumb a',
    '[role="breadcrumb"] a',
    '.crbs a',
    '.breadcrumbs-container a',
    // XPath 选择器找包含 > 的面包屑结构
  ];
  
  for (const selector of breadcrumbSelectors) {
    try {
      const elements = await page.$$(selector);
      if (elements.length > 0) {
        const levels = await Promise.all(
          elements.map(el => el.textContent().then(t => t.trim()))
        );
        // 过滤掉 "Home" "首页" 等首页链接
        const filteredLevels = levels.filter(level => {
          const lower = level.toLowerCase();
          return !['home', '首页', '主页', 'return to shop'].includes(lower);
        });
        
        if (filteredLevels.length > 0) {
          return { levels: filteredLevels };
        }
      }
    } catch (e) {
      continue;
    }
  }
  
  // 如果没找到面包屑，尝试从页面标题或 H1 提取
  try {
    // 尝试找 H1
    const h1Text = await page.$eval('h1', el => el.textContent.trim()).catch(() => null);
    if (h1Text) {
      // 如果只有 H1，说明这就是一级分类
      return { levels: [h1Text] };
    }
  } catch (e) {}
  
  // 最后尝试：从 URL slug 中提取，作为 fallback
  return { levels: [] };
}

function generateCSV(categories) {
  // CSV 表头
  const headers = [
    '完整链接',
    'URL 路径 slug', 
    '链接文本',
    '页面标题',
    '一级分类',
    '二级分类',
    '三级分类',
    '四级分类',
    '实际层级深度'
  ];
  
  let csv = '\ufeff' + headers.join(',') + '\n'; // 添加 BOM 支持 Excel 中文
  
  categories.forEach(cat => {
    const escapeCsv = (str) => {
      if (str && typeof str === 'string') {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return `"${str}"`;
    };
    
    const row = [
      escapeCsv(cat.fullUrl),
      escapeCsv(cat.fullSlug),
      escapeCsv(cat.linkText),
      escapeCsv(cat.title),
      escapeCsv(cat.level1),
      escapeCsv(cat.level2),
      escapeCsv(cat.level3),
      escapeCsv(cat.level4),
      cat.actualDepth
    ];
    
    csv += row.join(',') + '\n';
  });
  
  return csv;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
📦 Shopify 分类采集器 (改进版 - 从面包屑提取真实层级)

用法:
  node collect-improved.js <website-url> [output-directory]

说明:
  这个版本会访问每个分类页面，从面包屑导航提取真实的分类层级，
  而不是仅从 URL slug 猜测。结果更准确。

参数:
  website-url       要采集的网站 URL (必填)
  output-directory  输出 CSV 的目录 (可选，默认: C:\\workspace\\caiji)

示例:
  node collect-improved.js https://shop.futvortexstore.com/
  node collect-improved.js https://shop.futvortexstore.com/ C:\\workspace\\caiji
    `);
    process.exit(0);
  }
  
  const startUrl = args[0];
  const outputDir = args[1] || 'C:\\workspace\\caiji';
  
  console.log(`🚀 开始采集 (改进版): ${startUrl}`);
  console.log(`📂 输出目录: ${outputDir}`);
  
  try {
    const result = await collectCategories(startUrl, outputDir);
    console.log('\n🎉 采集完成！');
    console.log(`📄 文件: ${result.csvPath}`);
    console.log(`🔢 分类数量: ${result.count}`);
    process.exit(0);
  } catch (error) {
    console.error('\n💥 采集失败:', error.message);
    process.exit(1);
  }
}

// 如果直接运行
if (require.main === module) {
  main();
}

module.exports = collectCategories;

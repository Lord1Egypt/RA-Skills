#!/usr/bin/env node

/**
 * Shopify 分类采集器 - 正确版本
 * 针对 https://shop.futvortexstore.com/ 的导航结构特别处理
 * 
 * 网站结构：
 * - 一级导航: Premier League, La Liga, Bundesliga, Nations 等大分类
 * - 二级导航: 每个大分类下是具体的球队 (Arsenal, Liverpool 等)
 * 
 * 使用方法：
 *   node collect-correct.js <website-url> [output-directory]
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
    
    // 分析导航结构，获取完整的分类层级
    console.log('🔍 分析导航结构...');
    const navStructure = await extractNavigationStructure(page);
    console.log(`📊 找到 ${navStructure.length} 个一级分类`);
    
    navStructure.forEach((level1, i) => {
      console.log(`  ${i+1}. ${level1.name} -> ${level1.items.length} 个二级分类`);
    });
    
    // 展平所有分类，收集完整信息
    const categories = [];
    
    for (const level1 of navStructure) {
      for (const level2 of level1.items) {
        const category = {
          fullUrl: level2.fullUrl,
          fullSlug: level2.slug,
          level1Name: level1.name,
          level2Name: level2.name,
          level1Slug: level1.slug,
          level2Slug: level2.slug,
          actualDepth: 2
        };
        categories.push(category);
      }
    }
    
    // 同时收集那些没有子菜单的一级分类
    for (const level1 of navStructure) {
      if (level1.items.length === 0) {
        const category = {
          fullUrl: level1.fullUrl,
          fullSlug: level1.slug,
          level1Name: level1.name,
          level2Name: '',
          level1Slug: level1.slug,
          level2Slug: '',
          actualDepth: 1
        };
        categories.push(category);
      }
    }
    
    console.log(`\n📊 总计: ${categories.length} 个分类`);
    
    // 生成 CSV
    const csv = generateCSV(categories);
    
    // 保存文件
    fs.writeFileSync(csvPath, csv, 'utf-8');
    
    console.log(`💾 CSV 文件已保存: ${csvPath}`);
    
    // 输出预览
    console.log('\n📋 预览前 10 条:');
    categories.slice(0, 10).forEach((cat, i) => {
      if (cat.actualDepth === 2) {
        console.log(`${i+1}. ${cat.fullSlug} -> 一级: ${cat.level1Name}, 二级: ${cat.level2Name}`);
      } else {
        console.log(`${i+1}. ${cat.fullSlug} -> 一级: ${cat.level1Name}`);
      }
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
 * 从首页主导航提取完整的分类层级结构
 */
async function extractNavigationStructure(page) {
  // 根据调试结果，主导航在 nav.t4s-navigation
  const structure = await page.evaluate(() => {
    const result = [];
    
    // 找到主导航
    const mainNav = document.querySelector('nav.t4s-navigation');
    if (!mainNav) {
      return result;
    }
    
    // 获取所有一级菜单项
    // 一级菜单是直接的 a 标签或者有下拉的 li
    const level1Items = Array.from(mainNav.querySelectorAll('li'));
    
    level1Items.forEach(li => {
      const a = li.querySelector('a');
      if (!a) return;
      
      const level1Name = a.textContent.trim();
      const level1Href = a.getAttribute('href');
      
      if (!level1Name || !level1Href) return;
      
      // 跳过首页链接
      if (level1Name.toLowerCase() === 'home' || level1Name === '') {
        return;
      }
      
      // 提取 slug 从 href
      const slugMatch = level1Href.match(/\/collections\/([^\/]+)/);
      const level1Slug = slugMatch ? slugMatch[1] : '';
      
      // 检查是否有下拉菜单（二级分类）
      const dropdown = li.querySelector('ul.sub-menu, ul.dropdown, ul.t4s-mega-menu');
      
      const level2Items = [];
      
      if (dropdown) {
        // 提取二级菜单项
        const level2Links = Array.from(dropdown.querySelectorAll('a'));
        level2Links.forEach(a2 => {
          const name = a2.textContent.trim();
          const href = a2.getAttribute('href');
          
          if (!name || !href) return;
          
          // 提取 slug
          const match = href.match(/\/collections\/([^\/]+)/);
          const slug = match ? match[1] : '';
          
          // 转换为完整 URL
          let fullUrl = href;
          if (href.startsWith('/')) {
            fullUrl = window.location.origin + href;
          }
          
          level2Items.push({
            name: name,
            slug: slug,
            href: href,
            fullUrl: fullUrl
          });
        });
      }
      
      // 转换一级分类 URL
      let level1FullUrl = level1Href;
      if (level1Href.startsWith('/')) {
        level1FullUrl = window.location.origin + level1Href;
      }
      
      result.push({
        name: level1Name,
        slug: level1Slug,
        fullUrl: level1FullUrl,
        items: level2Items
      });
    });
    
    return result;
  });
  
  return structure;
}

function generateCSV(categories) {
  // CSV 表头 - 根据用户需求：
  // - 完整链接放在一个单元格
  // - 一级分类放在一个单元格
  // - 二级分类放在一个单元格
  // - 以此类推...
  // - 清晰的表头标注
  const headers = [
    '完整链接',
    'URL 路径',
    '一级分类',
    '二级分类',
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
    
    const fullSlug = cat.level2Slug ? `${cat.level1Slug}/${cat.level2Slug}` : cat.level1Slug;
    
    const row = [
      escapeCsv(cat.fullUrl),
      escapeCsv(fullSlug),
      escapeCsv(cat.level1Name),
      escapeCsv(cat.level2Name),
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
📦 Shopify 分类采集器 (针对 shop.futvortexstore.com 正确结构)

用法:
  node collect-correct.js <website-url> [output-directory]

说明:
  这个版本正确识别网站导航结构:
  - 一级分类是主导航中的大分类 (Premier League, La Liga 等)
  - 二级分类是下拉菜单中的具体球队 (Liverpool, Arsenal 等)
  - 每个分类层级单独放在一个单元格，清晰标注表头

参数:
  website-url       要采集的网站 URL (必填)
  output-directory  输出 CSV 的目录 (可选，默认: C:\\workspace\\caiji)

示例:
  node collect-correct.js https://shop.futvortexstore.com/
  node collect-correct.js https://shop.futvortexstore.com/ C:\\workspace\\caiji

输出格式:
  | 完整链接 | URL 路径 | 一级分类 | 二级分类 | 实际层级深度 |
    `);
    process.exit(0);
  }
  
  const startUrl = args[0];
  const outputDir = args[1] || 'C:\\workspace\\caiji';
  
  console.log(`🚀 开始采集 (正确结构版): ${startUrl}`);
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

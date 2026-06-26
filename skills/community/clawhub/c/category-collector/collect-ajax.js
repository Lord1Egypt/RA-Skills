#!/usr/bin/env node

/**
 * Shopify 分类采集器 - 处理 Ajax 懒加载下拉菜单
 * 
 * 网站结构：
 * - 一级菜单: Premier League, La Liga 等
 * - 二级菜单: 懒加载，悬停后 Ajax 加载
 * - 二级菜单容器: div.t4s-sub-menu
 * 
 * 使用方法：
 *   node collect-ajax.js <website-url> [output-directory]
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
    console.log('🔍 分析导航结构（处理 Ajax 懒加载）...');
    const navStructure = await extractNavigationStructure(page);
    console.log(`📊 找到 ${navStructure.length} 个一级分类`);
    
    navStructure.forEach((level1, i) => {
      console.log(`  ${i+1}. ${level1.name} -> ${level1.items.length} 个二级分类`);
    });
    
    // 统计总数
    let totalCount = 0;
    navStructure.forEach(level1 => {
      if (level1.items.length > 0) {
        totalCount += level1.items.length;
      } else {
        totalCount += 1;
      }
    });
    
    // 展平所有分类，收集完整信息
    const categories = [];
    
    for (const level1 of navStructure) {
      if (level1.items.length > 0) {
        // 有二级分类
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
      } else {
        // 没有二级分类，只有一级
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
    console.log('\n📋 预览前 15 条:');
    categories.slice(0, 15).forEach((cat, i) => {
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
 * 处理 Ajax 懒加载下拉菜单：悬停 -> 等待加载 -> 提取链接
 */
async function extractNavigationStructure(page) {
  const result = [];
  
  // 找到主导航 ul
  await page.waitForSelector('nav.t4s-navigation ul#t4s-nav-ul', { timeout: 10000 });
  
  // 获取所有一级菜单项 li
  const level1Items = await page.$$('nav.t4s-navigation ul#t4s-nav-ul li');
  console.log(`  找到 ${level1Items.length} 个一级菜单项`);
  
  for (const li of level1Items) {
    const aHandle = await li.$('a');
    if (!aHandle) continue;
    
    const level1Name = await page.evaluate(el => el.textContent.trim().replace(/\s+$/, ''), aHandle);
    const level1Href = await page.evaluate(el => el.getAttribute('href'), aHandle);
    
    if (!level1Name || !level1Name.trim()) continue;
    if (level1Name.toLowerCase() === 'home') continue;
    
    // 提取 slug 从 href
    const slugMatch = level1Href.match(/\/collections\/([^\/\s]+)/);
    const level1Slug = slugMatch ? slugMatch[1] : '';
    
    // 转换一级分类 URL
    let level1FullUrl = level1Href;
    if (level1Href.startsWith('/')) {
      level1FullUrl = new URL(level1Href, page.url()).href;
    }
    
    console.log(`  处理一级分类: ${level1Name}`);
    
    // 检查是否有下拉菜单 (has--children class)
    const hasChildren = await page.evaluate(el => el.classList.contains('has--children'), li);
    
    const level2Items = [];
    
    if (hasChildren) {
      // 有二级菜单，需要悬停触发 Ajax 加载
      console.log(`    有二级分类，等待加载...`);
      
      // 鼠标悬停
      await aHandle.hover();
      
      // 等待下拉菜单容器
      const subMenu = await li.$('div.t4s-sub-menu');
      
      if (subMenu) {
        // 等待懒加载完成，等待至少有一个链接出现
        try {
          await subMenu.waitForSelector('a', { timeout: 10000 });
          await page.waitForTimeout(1000); // 等待全部加载
          
          // 提取所有二级链接
          const level2Links = await subMenu.$$('a');
          console.log(`    加载完成，找到 ${level2Links.length} 个二级分类`);
          
          for (const a2 of level2Links) {
            const name = await page.evaluate(el => el.textContent.trim(), a2);
            const href = await page.evaluate(el => el.getAttribute('href'), a2);
            
            if (!name || !name.trim() || !href) continue;
            
            // 提取 slug
            const match = href.match(/\/collections\/([^\/]+)/);
            const slug = match ? match[1] : '';
            
            if (!slug) continue;
            
            // 转换为完整 URL
            let fullUrl = href;
            if (href.startsWith('/')) {
              fullUrl = new URL(href, page.url()).href;
            }
            
            level2Items.push({
              name: name.trim(),
              slug: slug,
              href: href,
              fullUrl: fullUrl
            });
          }
        } catch (error) {
          console.log(`    ⚠️  加载超时: ${error.message}`);
        }
      }
    }
    
    result.push({
      name: level1Name.trim(),
      slug: level1Slug,
      fullUrl: level1FullUrl,
      items: level2Items
    });
  }
  
  return result;
}

function generateCSV(categories) {
  // CSV 表头 - 根据用户需求：
  // - 完整链接放在一个单元格
  // - URL slug 放在一个单元格
  // - 一级分类放在一个单元格
  // - 二级分类放在一个单元格
  // - 实际层级深度
  const headers = [
    '完整链接',
    'URL 路径 slug',
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
📦 Shopify 分类采集器 (处理 Ajax 懒加载最终版)

用法:
  node collect-ajax.js <website-url> [output-directory]

说明:
  ✅ 正确识别网站导航结构
  ✅ 处理需要悬停 Ajax 懒加载的下拉菜单
  ✅ 一级分类单独单元格，二级分类单独单元格
  ✅ 自动检测实际层级深度
  ✅ 清晰的中文表头

参数:
  website-url       要采集的网站 URL (必填)
  output-directory  输出 CSV 的目录 (可选，默认: C:\\workspace\\caiji)

示例:
  node collect-ajax.js https://shop.futvortexstore.com/
  node collect-ajax.js https://shop.futvortexstore.com/ C:\\workspace\\caiji

输出格式（符合你的要求）:
  | 完整链接 | URL 路径 slug | 一级分类 | 二级分类 | 实际层级深度 |
  
  例如你给的例子:
  https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops
  slug: women-women-clothes-tank-tops
  一级分类: Women
  二级分类: Tank Tops
    `);
    process.exit(0);
  }
  
  const startUrl = args[0];
  const outputDir = args[1] || 'C:\\workspace\\caiji';
  
  console.log(`🚀 开始采集 (Ajax 懒加载版): ${startUrl}`);
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

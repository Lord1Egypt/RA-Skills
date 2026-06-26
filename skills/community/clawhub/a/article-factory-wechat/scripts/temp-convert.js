import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';
import { existsSync, mkdirSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 解析命令行参数
const args = process.argv.slice(2);
const options = {
  html: args.find(arg => arg.startsWith('--html='))?.split('=')[1],
  output: args.find(arg => arg.startsWith('--output='))?.split('=')[1],
  width: parseInt(args.find(arg => arg.startsWith('--width='))?.split('=')[1] || 1400),
  height: parseInt(args.find(arg => arg.startsWith('--height='))?.split('=')[1] || 1200)
};

// 配置（必须通过命令行参数传入 --html 和 --output）
const HTML_FILE = options.html ? resolve(options.html) : null;
const OUTPUT_DIR = options.output ? resolve(options.output) : null;
const PAGE_WIDTH = options.width;
const PAGE_HEIGHT = options.height;

// 确保输出目录存在
if (!HTML_FILE || !OUTPUT_DIR) {
  console.error('❌ 错误: 必须提供 --html 和 --output 参数');
  console.error('用法: node scripts/temp-convert.js --html=article.html --output=output/directory');
  process.exit(1);
}

if (!existsSync(OUTPUT_DIR)) {
  mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function convertPagesToImages() {
  console.log('🚀 开始转换页面为图片...\n');
  
  let browser;
  try {
    // 读取 HTML 文件
    console.log(`📖 读取 HTML 文件: ${HTML_FILE}`);
    const htmlContent = readFileSync(HTML_FILE, 'utf-8');
    
    // 启动浏览器
    console.log('🌐 启动浏览器...');
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 设置视口大小
    await page.setViewport({
      width: PAGE_WIDTH,
      height: PAGE_HEIGHT,
      deviceScaleFactor: 2 // 2x 分辨率，获得更清晰的图片
    });
    
    // 加载 HTML 内容
    await page.setContent(htmlContent, {
      waitUntil: 'networkidle0'
    });
    
    // 等待字体和样式加载
    await page.evaluateHandle(() => document.fonts.ready);
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 获取所有页面元素
    const pageElements = await page.$$('.page');
    console.log(`📄 找到 ${pageElements.length} 个页面\n`);
    
    // 为每个页面截图
    for (let i = 0; i < pageElements.length; i++) {
      const element = pageElements[i];
      
      // 获取页面标题或编号
      const pageInfo = await page.evaluate((el) => {
        const pageNumber = el.querySelector('.page-number')?.textContent?.trim() || '';
        const sectionTitle = el.querySelector('.section-title')?.textContent?.trim() || 
                           el.querySelector('.cover-title')?.textContent?.trim() ||
                           el.querySelector('.interaction-title')?.textContent?.trim() ||
                           'page';
        return { pageNumber, sectionTitle };
      }, element);
      
      // 生成文件名
      const pageNum = pageInfo.pageNumber || String(i + 1).padStart(2, '0');
      const fileName = `page-${pageNum}.png`;
      const filePath = join(OUTPUT_DIR, fileName);
      
      // 截图
      await element.screenshot({
        path: filePath,
        type: 'png',
        omitBackground: false
      });
      
      console.log(`✅ 已保存: ${fileName} (${pageInfo.sectionTitle || '页面'})`);
    }
    
    console.log(`\n✨ 完成！所有图片已保存到: ${OUTPUT_DIR}`);
    
  } catch (error) {
    console.error('❌ 发生错误:', error);
    throw error;
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }
}

// 运行转换
convertPagesToImages().catch(console.error);

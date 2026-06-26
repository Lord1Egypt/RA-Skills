#!/usr/bin/env node

/**
 * 使用 turndown 库从 Twitter Article HTML 转换为 Markdown
 * 记录文本和图片的精确位置
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const { gfm } = require('turndown-plugin-gfm');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-turndown.js <article_url> <cookie_string>');
  process.exit(1);
}

const articleUrl = process.argv[2];
const cookieString = process.argv[3];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  // 设置 Cookie
  const cookies = cookieString.split('; ').map(cookie => {
    const [name, value] = cookie.split('=');
    return {
      name: name.trim(),
      value: value.trim(),
      domain: '.x.com',
      path: '/'
    };
  });
  await context.addCookies(cookies);

  const page = await context.newPage();
  
  try {
    await page.goto(articleUrl, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(5000);
    
    // 滚动页面加载所有图片（懒加载）
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 500;
        const timer = setInterval(() => {
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;
          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            resolve();
          }
        }, 200);
      });
    });
    
    await page.waitForTimeout(3000);

    // 提取文章内容和图片
    const result = await page.evaluate(() => {
      const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
      if (!contentDiv) {
        throw new Error('Article content not found');
      }

      // 提取标题
      const titleElement = document.querySelector('[data-testid="twitter-article-title"]');
      const title = titleElement ? titleElement.textContent.trim() : '';

      // 提取作者信息
      const authorElement = document.querySelector('[itemprop="author"] [itemprop="name"]');
      const author = authorElement ? authorElement.getAttribute('content') : '';

      const usernameElement = document.querySelector('[itemprop="author"] [itemprop="additionalName"]');
      const username = usernameElement ? usernameElement.getAttribute('content') : '';

      // 收集所有图片并标记位置
      const contentBlocks = [];
      let currentText = '';
      
      function flushText() {
        if (currentText.trim()) {
          contentBlocks.push({
            type: 'text',
            content: currentText.trim()
          });
          currentText = '';
        }
      }
      
      // 遍历所有子节点
      function processNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
          currentText += node.textContent;
          return;
        }
        
        if (node.nodeType === Node.ELEMENT_NODE) {
          const tag = node.tagName.toLowerCase();
          
          // 处理图片
          if (tag === 'img') {
            const src = node.getAttribute('src') || node.src;
            if (src && src.includes('pbs.twimg.com/media')) {
              // Flush 当前文本
              flushText();
              
              // 添加图片
              let imageUrl = src.split('?')[0];
              if (!imageUrl.startsWith('http')) {
                imageUrl = 'https:' + imageUrl;
              }
              imageUrl += '?format=jpg&name=large';
              
              contentBlocks.push({
                type: 'image',
                url: imageUrl
              });
              return;
            }
          }
          
          // 递归处理子节点
          for (const child of node.childNodes) {
            processNode(child);
          }
        }
      }
      
      // 处理内容
      processNode(contentDiv);
      flushText();

      return {
        title,
        author,
        username,
        contentHtml: contentDiv.innerHTML,
        contentBlocks
      };
    });

    // 使用 turndown 转换 HTML 为 Markdown
    const turndownService = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced',
      bulletListMarker: '-',
      strongDelimiter: '**',
      emDelimiter: '*'
    });
    
    // 使用 GFM 插件（支持表格、删除线等）
    turndownService.use(gfm);
    
    // 自定义图片规则：移除图片（因为我们单独处理）
    turndownService.addRule('removeImages', {
      filter: 'img',
      replacement: () => ''
    });
    
    // 转换 HTML 为 Markdown
    const markdown = turndownService.turndown(result.contentHtml);
    
    // 输出结果
    console.log(JSON.stringify({
      title: result.title,
      author: result.author,
      username: result.username,
      content: markdown,
      contentBlocks: result.contentBlocks
    }, null, 2));
    
  } catch (error) {
    console.error('Failed to extract article content:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();

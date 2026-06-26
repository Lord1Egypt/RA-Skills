#!/usr/bin/env node

/**
 * 从 Twitter Article HTML 转换为格式化的 Markdown
 * 保留粗体、代码块、列表等所有格式
 * 精确记录图片在内容中的位置
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-v5.js <article_url> <cookie_string>');
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
      value: decodeURIComponent(value.trim()),
      domain: '.x.com',
      path: '/'
    };
  });
  await context.addCookies(cookies);

  const page = await context.newPage();
  
  try {
    await page.goto(articleUrl, { waitUntil: 'networkidle', timeout: 60000 });
    
    // 等待文章内容加载
    await page.waitForSelector('[data-testid="twitterArticleRichTextView"]', { timeout: 30000 });
    
    // 滚动页面确保所有懒加载图片都加载完成
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 100;
        const timer = setInterval(() => {
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;

          if (totalHeight >= scrollHeight) {
            clearInterval(timer);
            setTimeout(resolve, 2000); // 额外等待 2 秒
          }
        }, 200);
      });
    });
    
    // 等待图片加载
    await page.waitForTimeout(3000);
    
    // 提取文章内容和图片位置
    const result = await page.evaluate(() => {
      const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
      if (!contentDiv) {
        throw new Error('Article content not found');
      }

      // 提取标题
      const titleElement = document.querySelector('h1[data-testid="twitterArticleTitle"]');
      const title = titleElement ? titleElement.textContent.trim() : '';

      // 提取作者
      const authorElement = document.querySelector('[data-testid="User-Name"]');
      const author = authorElement ? authorElement.textContent.trim() : '';

      // 遍历内容，记录文本和图片的顺序
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
      
      function processNode(node, inBold = false) {
        // 文本节点
        if (node.nodeType === Node.TEXT_NODE) {
          currentText += node.textContent;
          return;
        }

        // 元素节点
        if (node.nodeType === Node.ELEMENT_NODE) {
          const tag = node.tagName.toLowerCase();
          
          // 检查是否有 font-weight: bold 样式
          const style = node.getAttribute('style') || '';
          const isBold = style.includes('font-weight: bold') || style.includes('font-weight:bold');
          
          // 处理图片
          if (tag === 'img') {
            const src = node.getAttribute('src') || node.src;
            if (src && src.includes('pbs.twimg.com/media')) {
              // 保存当前文本
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
            }
            return;
          }
          
          // 处理换行
          if (tag === 'br') {
            currentText += '\n';
            return;
          }
          
          // 处理段落
          if (tag === 'p' || tag === 'div') {
            // 段落前后加换行
            if (currentText && !currentText.endsWith('\n\n')) {
              currentText += '\n\n';
            }
          }
          
          // 处理标题
          if (tag.match(/^h[1-6]$/)) {
            if (currentText && !currentText.endsWith('\n\n')) {
              currentText += '\n\n';
            }
            const level = parseInt(tag[1]);
            currentText += '#'.repeat(level) + ' ';
          }
          
          // 处理粗体
          if (tag === 'strong' || tag === 'b' || isBold) {
            currentText += '**';
            for (const child of node.childNodes) {
              processNode(child, true);
            }
            currentText += '**';
            return;
          }
          
          // 处理斜体
          if (tag === 'em' || tag === 'i') {
            currentText += '*';
            for (const child of node.childNodes) {
              processNode(child, inBold);
            }
            currentText += '*';
            return;
          }
          
          // 处理代码
          if (tag === 'code') {
            currentText += '`';
            for (const child of node.childNodes) {
              processNode(child, inBold);
            }
            currentText += '`';
            return;
          }
          
          // 处理链接
          if (tag === 'a') {
            const href = node.getAttribute('href');
            const text = node.textContent.trim();
            if (href && text) {
              currentText += `[${text}](${href})`;
            }
            return;
          }
          
          // 处理列表
          if (tag === 'ul' || tag === 'ol') {
            if (currentText && !currentText.endsWith('\n\n')) {
              currentText += '\n\n';
            }
          }
          
          if (tag === 'li') {
            currentText += '- ';
          }
          
          // 递归处理子节点
          for (const child of node.childNodes) {
            processNode(child, inBold || isBold);
          }
          
          // 列表项后换行
          if (tag === 'li') {
            currentText += '\n';
          }
          
          // 段落后换行
          if (tag === 'p') {
            if (!currentText.endsWith('\n\n')) {
              currentText += '\n\n';
            }
          }
        }
      }

      // 处理所有子节点
      for (const child of contentDiv.childNodes) {
        processNode(child);
      }

      // 保存最后的文本
      flushText();

      return {
        title,
        author,
        contentBlocks
      };
    });

    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('Failed to extract article content:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();

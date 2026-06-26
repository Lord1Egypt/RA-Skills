#!/usr/bin/env node

/**
 * 从 Twitter Article HTML 转换为格式化的 Markdown
 * 保留粗体、代码块、列表等所有格式
 * 记录图片在内容中的精确位置
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-v4.js <article_url> <cookie_string>');
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
    await page.waitForSelector('article', { timeout: 30000 });
    
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
            resolve();
          }
        }, 100);
      });
    });
    
    // 等待图片加载
    await page.waitForTimeout(3000);
    
    // 提取文章内容和图片位置
    const result = await page.evaluate(() => {
      const article = document.querySelector('article');
      if (!article) {
        throw new Error('Article not found');
      }

      // 提取标题
      const titleElement = article.querySelector('h1, h2, [role="heading"]');
      const title = titleElement ? titleElement.textContent.trim() : '';

      // 提取作者
      const authorElement = document.querySelector('[data-testid="User-Name"]');
      const author = authorElement ? authorElement.textContent.trim() : '';

      // 遍历所有内容节点，记录文本和图片的顺序
      const contentBlocks = [];
      let currentText = '';
      
      const processNode = (node) => {
        // 处理图片
        if (node.tagName === 'IMG') {
          // 保存当前累积的文本
          if (currentText.trim()) {
            contentBlocks.push({
              type: 'text',
              content: currentText.trim()
            });
            currentText = '';
          }
          
          // 保存图片
          const src = node.getAttribute('src');
          if (src && (src.includes('pbs.twimg.com') || src.includes('media'))) {
            let imageUrl = src;
            if (!imageUrl.startsWith('http')) {
              imageUrl = 'https://pbs.twimg.com' + imageUrl;
            }
            // 添加格式参数
            if (!imageUrl.includes('?')) {
              imageUrl += '?format=jpg&name=large';
            }
            contentBlocks.push({
              type: 'image',
              url: imageUrl
            });
          }
          return;
        }

        // 处理文本节点
        if (node.nodeType === Node.TEXT_NODE) {
          const text = node.textContent;
          if (text.trim()) {
            currentText += text;
          }
          return;
        }

        // 处理元素节点
        if (node.nodeType === Node.ELEMENT_NODE) {
          const tagName = node.tagName.toLowerCase();
          
          // 处理换行
          if (tagName === 'br') {
            currentText += '\n';
            return;
          }
          
          // 处理段落
          if (tagName === 'p' || tagName === 'div') {
            if (currentText.trim()) {
              currentText += '\n\n';
            }
          }
          
          // 处理标题
          if (tagName.match(/^h[1-6]$/)) {
            if (currentText.trim()) {
              currentText += '\n\n';
            }
            const level = parseInt(tagName[1]);
            currentText += '#'.repeat(level) + ' ';
          }
          
          // 处理粗体
          if (tagName === 'strong' || tagName === 'b') {
            currentText += '**';
            for (const child of node.childNodes) {
              processNode(child);
            }
            currentText += '**';
            return;
          }
          
          // 处理斜体
          if (tagName === 'em' || tagName === 'i') {
            currentText += '*';
            for (const child of node.childNodes) {
              processNode(child);
            }
            currentText += '*';
            return;
          }
          
          // 处理代码
          if (tagName === 'code') {
            currentText += '`';
            for (const child of node.childNodes) {
              processNode(child);
            }
            currentText += '`';
            return;
          }
          
          // 处理链接
          if (tagName === 'a') {
            const href = node.getAttribute('href');
            const text = node.textContent.trim();
            if (href && text) {
              currentText += `[${text}](${href})`;
            }
            return;
          }
          
          // 处理列表
          if (tagName === 'ul' || tagName === 'ol') {
            if (currentText.trim()) {
              currentText += '\n\n';
            }
          }
          
          if (tagName === 'li') {
            currentText += '- ';
          }
          
          // 递归处理子节点
          for (const child of node.childNodes) {
            processNode(child);
          }
          
          // 列表项后换行
          if (tagName === 'li') {
            currentText += '\n';
          }
        }
      };

      // 处理文章主体
      const articleBody = article.querySelector('[data-testid="article-body"]') || article;
      for (const child of articleBody.childNodes) {
        processNode(child);
      }

      // 保存最后的文本
      if (currentText.trim()) {
        contentBlocks.push({
          type: 'text',
          content: currentText.trim()
        });
      }

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

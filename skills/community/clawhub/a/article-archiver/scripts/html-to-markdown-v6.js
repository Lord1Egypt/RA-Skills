#!/usr/bin/env node

/**
 * 从 Twitter Article HTML 转换为 contentBlocks 格式
 * 在遍历 DOM 时记录文本和图片的顺序
 * 输出格式：{ title, author, contentBlocks: [{type, content/url}] }
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-v6.js <article_url> <cookie_string>');
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

  // 提取格式化内容和图片
  const articleData = await page.evaluate(() => {
    const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
    if (!contentDiv) return null;

    // contentBlocks 数组和当前文本缓冲区
    const contentBlocks = [];
    let currentText = '';

    // flush 当前文本到 contentBlocks
    function flushText() {
      if (currentText.trim()) {
        contentBlocks.push({
          type: 'text',
          content: currentText.trim()
        });
        currentText = '';
      }
    }

    // 递归处理节点，保留格式
    function processNode(node, inBold = false) {
      if (node.nodeType === Node.TEXT_NODE) {
        currentText += node.textContent;
        return;
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toLowerCase();
        
        // 检查是否有 font-weight: bold 样式
        const style = node.getAttribute('style') || '';
        const isBold = style.includes('font-weight: bold') || style.includes('font-weight:bold');
        
        // 处理不同的 HTML 标签
        switch (tag) {
          case 'img':
            // 遇到图片：flush 当前文本，添加图片块
            const imgSrc = node.getAttribute('src') || node.src;
            if (imgSrc && imgSrc.includes('pbs.twimg.com/media')) {
              flushText();
              const cleanUrl = imgSrc.split('?')[0] + '?format=jpg&name=large';
              contentBlocks.push({
                type: 'image',
                url: cleanUrl
              });
            }
            return;
          
          case 'h1':
            currentText += '\n# ';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
            currentText += '\n';
            return;
          case 'h2':
            currentText += '\n## ';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
            currentText += '\n';
            return;
          case 'h3':
            currentText += '\n### ';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
            currentText += '\n';
            return;
          case 'strong':
          case 'b':
            currentText += '**';
            Array.from(node.childNodes).forEach(child => processNode(child, true));
            currentText += '**';
            return;
          case 'em':
          case 'i':
            currentText += '*';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            currentText += '*';
            return;
          case 'code':
            currentText += '`';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            currentText += '`';
            return;
          case 'pre':
            // 代码块
            const codeContent = node.querySelector('code')?.textContent || node.textContent;
            currentText += `\n\`\`\`shell\n${codeContent}\n\`\`\`\n`;
            return;
          case 'p':
          case 'div':
            // 检查是否是代码块容器
            if (node.querySelector('pre, code[class*="language"]')) {
              Array.from(node.childNodes).forEach(child => processNode(child, inBold));
              return;
            }
            // 如果有粗体样式，包裹内容
            if (isBold && !inBold) {
              currentText += '**';
              Array.from(node.childNodes).forEach(child => processNode(child, true));
              currentText += '**\n';
            } else {
              Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
              currentText += '\n';
            }
            return;
          case 'li':
            currentText += '- ';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            currentText += '\n';
            return;
          case 'ol':
          case 'ul':
            currentText += '\n';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            return;
          case 'br':
            currentText += '\n';
            return;
          case 'a':
            const href = node.getAttribute('href');
            // 跳过图片链接
            if (href && href.includes('/media/')) {
              return;
            }
            if (href) {
              currentText += '[';
              Array.from(node.childNodes).forEach(child => processNode(child, inBold));
              currentText += `](${href})`;
            } else {
              Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            }
            return;
          case 'span':
            // span 标签可能有粗体样式
            if (isBold && !inBold) {
              currentText += '**';
              Array.from(node.childNodes).forEach(child => processNode(child, true));
              currentText += '**';
            } else {
              Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
            }
            return;
          default:
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            return;
        }
      }
    }

    // 遍历内容
    processNode(contentDiv);
    
    // flush 最后的文本
    flushText();

    // 提取标题
    const titleElement = document.querySelector('[data-testid="twitter-article-title"]');
    const title = titleElement ? titleElement.textContent.trim() : '';

    // 提取作者信息
    const authorElement = document.querySelector('[itemprop="author"] [itemprop="name"]');
    const author = authorElement ? authorElement.getAttribute('content') : '';

    const usernameElement = document.querySelector('[itemprop="author"] [itemprop="additionalName"]');
    const username = usernameElement ? usernameElement.getAttribute('content') : '';

    return {
      title,
      author,
      username,
      contentBlocks
    };
  });

  await browser.close();

  if (articleData) {
    console.log(JSON.stringify(articleData, null, 2));
  } else {
    console.error('Failed to extract article content');
    process.exit(1);
  }
})();

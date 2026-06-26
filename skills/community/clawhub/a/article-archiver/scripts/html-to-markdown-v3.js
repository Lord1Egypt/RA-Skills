#!/usr/bin/env node

/**
 * 从 Twitter Article HTML 转换为格式化的 Markdown
 * 保留粗体、代码块、列表等所有格式
 * 通过网络监听提取真实的图片 URL
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-v3.js <article_url> <cookie_string>');
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
  
  // 监听网络请求，捕获图片 URL（保留完整 URL）
  const imageUrls = [];
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('pbs.twimg.com/media/') && !imageUrls.includes(url)) {
      imageUrls.push(url);
    }
  });
  
  await page.goto(articleUrl, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(10000);

  // 提取格式化内容
  const articleData = await page.evaluate(() => {
    const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
    if (!contentDiv) return null;

    // 递归处理节点，保留格式
    function processNode(node, inBold = false) {
      if (node.nodeType === Node.TEXT_NODE) {
        return node.textContent;
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toLowerCase();
        
        // 检查是否有 font-weight: bold 样式
        const style = node.getAttribute('style') || '';
        const isBold = style.includes('font-weight: bold') || style.includes('font-weight:bold');
        
        // 处理子节点
        const children = Array.from(node.childNodes)
          .map(child => processNode(child, inBold || isBold))
          .join('');

        // 处理不同的 HTML 标签
        switch (tag) {
          case 'h1':
            return `\n# ${children}\n`;
          case 'h2':
            return `\n## ${children}\n`;
          case 'h3':
            return `\n### ${children}\n`;
          case 'strong':
          case 'b':
            return `**${children}**`;
          case 'em':
          case 'i':
            return `*${children}*`;
          case 'code':
            return `\`${children}\``;
          case 'pre':
            const codeContent = node.querySelector('code')?.textContent || children;
            return `\n\`\`\`shell\n${codeContent}\n\`\`\`\n`;
          case 'p':
          case 'div':
            if (node.querySelector('pre, code[class*="language"]')) {
              return children;
            }
            if (isBold && !inBold) {
              return `**${children}**\n`;
            }
            return children + '\n';
          case 'li':
            return `- ${children}\n`;
          case 'ol':
          case 'ul':
            return '\n' + children;
          case 'br':
            return '\n';
          case 'a':
            const href = node.getAttribute('href');
            return href ? `[${children}](${href})` : children;
          case 'img':
            return '[图片占位]';
          case 'span':
            if (isBold && !inBold) {
              return `**${children}**`;
            }
            return children;
          default:
            return children;
        }
      }

      return '';
    }

    const content = processNode(contentDiv);

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
      content: content.trim()
    };
  });

  await browser.close();

  if (articleData) {
    // 添加网络监听捕获的图片
    articleData.images = imageUrls;
    console.log(JSON.stringify(articleData, null, 2));
  } else {
    console.error('Failed to extract article content');
    process.exit(1);
  }
})();

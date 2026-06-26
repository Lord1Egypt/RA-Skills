#!/usr/bin/env node

/**
 * 从 Twitter Article 提取格式化的 Markdown 内容
 * 保留粗体、代码块等格式
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node fetch-twitter-article-formatted.js <article_url> <cookie_string>');
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
  await page.waitForTimeout(8000);

  // 提取格式化内容
  const articleData = await page.evaluate(() => {
    const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
    if (!contentDiv) return null;

    // 递归处理节点，保留格式
    function processNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        return node.textContent;
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toLowerCase();
        const children = Array.from(node.childNodes).map(processNode).join('');

        // 处理不同的 HTML 标签
        switch (tag) {
          case 'strong':
          case 'b':
            return `**${children}**`;
          case 'em':
          case 'i':
            return `*${children}*`;
          case 'code':
            return `\`${children}\``;
          case 'pre':
            // 代码块
            const codeContent = node.querySelector('code')?.textContent || children;
            return `\n\`\`\`\n${codeContent}\n\`\`\`\n`;
          case 'h1':
            return `\n# ${children}\n`;
          case 'h2':
            return `\n## ${children}\n`;
          case 'h3':
            return `\n### ${children}\n`;
          case 'p':
          case 'div':
            // 检查是否是代码块容器
            if (node.querySelector('pre, code[class*="language"]')) {
              return children;
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
            const src = node.getAttribute('src');
            const alt = node.getAttribute('alt') || '';
            return src ? `![${alt}](${src})` : '';
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
    console.log(JSON.stringify(articleData, null, 2));
  } else {
    console.error('Failed to extract article content');
    process.exit(1);
  }
})();

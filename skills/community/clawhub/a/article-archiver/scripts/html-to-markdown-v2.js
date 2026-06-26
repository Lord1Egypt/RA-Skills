#!/usr/bin/env node

/**
 * 从 Twitter Article HTML 转换为格式化的 Markdown
 * 保留粗体、代码块、列表等所有格式
 * 提取真实的图片 URL（https://pbs.twimg.com/media/...）
 */

const { chromium } = require('playwright');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown.js <article_url> <cookie_string>');
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

    // 收集所有图片 URL（使用更全面的选择器）
    const images = [];
    const imageSet = new Set();
    
    // 从整个页面提取所有 pbs.twimg.com/media 图片
    const allImages = document.querySelectorAll('img');
    allImages.forEach(img => {
      const src = img.getAttribute('src') || img.src;
      if (src && src.includes('pbs.twimg.com/media')) {
        const cleanUrl = src.split('?')[0];
        imageSet.add(cleanUrl);
      }
    });
    
    // 转换为数组
    images.push(...Array.from(imageSet));

    // 递归处理节点，保留格式
    let imageIndex = 0;
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
            // 代码块
            const codeContent = node.querySelector('code')?.textContent || children;
            return `\n\`\`\`shell\n${codeContent}\n\`\`\`\n`;
          case 'p':
          case 'div':
            // 检查是否包含图片
            const hasImage = node.querySelector('img[src*="pbs.twimg.com"]');
            if (hasImage && imageIndex < images.length) {
              const imgUrl = images[imageIndex];
              imageIndex++;
              return `\n![图片](${imgUrl})\n\n${children}`;
            }
            
            // 检查是否是代码块容器
            if (node.querySelector('pre, code[class*="language"]')) {
              return children;
            }
            // 如果有粗体样式，包裹内容
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
            // 跳过图片链接
            if (href && href.includes('/media/')) {
              return '';
            }
            return href ? `[${children}](${href})` : children;
          case 'img':
            // 图片已在父节点处理，这里跳过
            return '';
          case 'span':
            // span 标签可能有粗体样式
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
      content: content.trim(),
      images: images  // 返回所有图片 URL
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

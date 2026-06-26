#!/usr/bin/env node

/**
 * 使用 turndown 库从 Twitter Article HTML 转换为 Markdown
 * 改进版：正确处理代码块
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const { gfm } = require('turndown-plugin-gfm');

if (process.argv.length < 4) {
  console.error('Usage: node html-to-markdown-final.js <article_url> <cookie_string>');
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
    
    // 滚动页面加载所有内容（包括懒加载的代码块）
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
            setTimeout(resolve, 3000); // 额外等待 3 秒确保所有内容加载
          }
        }, 200);
      });
    });
    
    await page.waitForTimeout(3000);

    // 提取文章内容
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

      return {
        title,
        author,
        username,
        contentHtml: contentDiv.innerHTML
      };
    });

    // 使用 turndown 转换 HTML 为 Markdown
    const turndownService = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced',
      bulletListMarker: '-',
      strongDelimiter: '**',
      emDelimiter: '*',
      fence: '```'
    });
    
    // 使用 GFM 插件（支持表格、删除线等）
    turndownService.use(gfm);
    
    // 自定义代码块规则：保留语言标注
    turndownService.addRule('codeBlock', {
      filter: function (node) {
        return node.nodeName === 'PRE' && node.querySelector('code');
      },
      replacement: function (content, node) {
        const code = node.querySelector('code');
        const language = code.className.replace('language-', '') || '';
        const text = code.textContent;
        return '\n\n```' + language + '\n' + text + '\n```\n\n';
      }
    });
    
    // 保留图片的 Markdown 语法（飞书会自动下载并转换）
    // 不需要自定义规则，turndown 默认会转换为 ![alt](url) 格式
    
    // 转换 HTML 为 Markdown
    const markdown = turndownService.turndown(result.contentHtml);
    
    // 输出结果
    console.log(JSON.stringify({
      title: result.title,
      author: result.author,
      username: result.username,
      content: markdown
    }, null, 2));
    
  } catch (error) {
    console.error('Failed to extract article content:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();

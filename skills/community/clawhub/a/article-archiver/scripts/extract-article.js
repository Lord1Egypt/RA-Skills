#!/usr/bin/env node

/**
 * 通用网页文章提取器（支持图片）
 * 适用于：普通网页、技术博客、新闻文章等
 */

const { chromium } = require('playwright');
const TurndownService = require('turndown');
const { gfm } = require('turndown-plugin-gfm');

if (process.argv.length < 3) {
  console.error('Usage: node extract-article.js <article_url> [cookie_string]');
  process.exit(1);
}

const articleUrl = process.argv[2];
const cookieString = process.argv[3] || '';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  // 设置 Cookie（如果提供）
  if (cookieString) {
    const cookies = cookieString.split('; ').map(cookie => {
      const [name, value] = cookie.split('=');
      return {
        name: name.trim(),
        value: value.trim(),
        domain: new URL(articleUrl).hostname,
        path: '/'
      };
    });
    await context.addCookies(cookies);
  }

  const page = await context.newPage();
  
  try {
    await page.goto(articleUrl, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(3000);
    
    // 滚动页面加载所有内容（包括懒加载的图片）
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
      // 尝试多种方式提取标题
      let title = '';
      const titleSelectors = [
        'h1',
        'article h1',
        '.article-title',
        '.post-title',
        '[class*="title"]',
        'meta[property="og:title"]'
      ];
      
      for (const selector of titleSelectors) {
        const element = document.querySelector(selector);
        if (element) {
          if (selector.startsWith('meta')) {
            title = element.getAttribute('content');
          } else {
            title = element.textContent.trim();
          }
          if (title) break;
        }
      }

      // 尝试多种方式提取作者
      let author = '';
      const authorSelectors = [
        '[itemprop="author"]',
        '.author',
        '.author-name',
        '[class*="author"]',
        'meta[name="author"]',
        'meta[property="article:author"]'
      ];
      
      for (const selector of authorSelectors) {
        const element = document.querySelector(selector);
        if (element) {
          if (selector.startsWith('meta')) {
            author = element.getAttribute('content');
          } else {
            author = element.textContent.trim();
          }
          if (author) break;
        }
      }

      // 尝试多种方式提取正文内容
      let contentElement = null;
      const contentSelectors = [
        'article',
        '.article-content',
        '.post-content',
        '.entry-content',
        '.note-content',  // 墨问笔记
        '[class*="detail"]',  // 详情页
        '[class*="content"]',
        'main',
        'body'  // 最后的兜底
      ];
      
      for (const selector of contentSelectors) {
        const element = document.querySelector(selector);
        if (element && element.textContent.trim().length > 100) {  // 降低阈值
          contentElement = element;
          break;
        }
      }

      if (!contentElement) {
        throw new Error('Article content not found');
      }

      return {
        title: title || document.title,
        author: author || '未知作者',
        username: '',
        contentHtml: contentElement.innerHTML
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
    
    // 自定义图片规则：确保图片 URL 完整
    turndownService.addRule('images', {
      filter: 'img',
      replacement: function (content, node) {
        const alt = node.alt || '';
        let src = node.getAttribute('src') || '';
        
        // 处理相对路径
        if (src && !src.startsWith('http') && !src.startsWith('data:')) {
          const baseUrl = new URL(articleUrl);
          if (src.startsWith('/')) {
            src = baseUrl.origin + src;
          } else {
            src = baseUrl.origin + '/' + src;
          }
        }
        
        // 过滤掉无效图片
        if (!src || src.startsWith('data:') || src.includes('avatar') || src.includes('icon')) {
          return '';
        }
        
        return '\n\n![' + alt + '](' + src + ')\n\n';
      }
    });
    
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

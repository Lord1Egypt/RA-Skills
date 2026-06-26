#!/usr/bin/env node
/**
 * Twitter Article Scraper
 * 使用 Playwright 和 Cookie 抓取 Twitter Article 内容
 * Usage: node fetch-twitter-article.js <article_url> <cookie_string>
 */

const { chromium } = require('playwright');

async function fetchTwitterArticle(articleUrl, cookieString) {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  // 解析 Cookie 字符串
  const cookies = [];
  const cookiePairs = cookieString.split(';');
  
  for (const pair of cookiePairs) {
    const [name, value] = pair.trim().split('=');
    if (name && value) {
      cookies.push({
        name: name.trim(),
        value: value.trim(),
        domain: '.x.com',
        path: '/'
      });
    }
  }
  
  await context.addCookies(cookies);
  
  const page = await context.newPage();
  
  try {
    await page.goto(articleUrl, { 
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });
    
    // 等待加载动画消失或内容出现
    try {
      await page.waitForSelector('article, [role="article"], main', { timeout: 10000 });
    } catch (e) {
      // 如果没有找到，继续等待
    }
    
    // 额外等待确保内容渲染
    await page.waitForTimeout(8000);
    
    // 截图调试（可选）
    // await page.screenshot({ path: '/tmp/twitter-article.png' });
    
    // 提取文章标题和内容
    const articleData = await page.evaluate(() => {
      // 获取页面文本
      const bodyText = document.body.innerText;
      
      // 尝试多种选择器
      const titleElement = document.querySelector('h1') || 
                          document.querySelector('[data-testid="article-title"]') ||
                          document.querySelector('article h1');
      
      const contentElement = document.querySelector('article') || 
                            document.querySelector('[role="article"]') ||
                            document.querySelector('[data-testid="article-content"]') ||
                            document.querySelector('main');
      
      // 检查是否需要登录
      const needsLogin = bodyText.includes('Log in') || 
                        bodyText.includes('Sign up') ||
                        bodyText.includes('This page is not supported');
      
      return {
        title: titleElement ? titleElement.innerText : '',
        content: contentElement ? contentElement.innerText : bodyText,
        html: contentElement ? contentElement.innerHTML : '',
        needsLogin: needsLogin,
        bodyPreview: bodyText.substring(0, 500)
      };
    });
    
    await browser.close();
    
    if (articleData.needsLogin) {
      return {
        success: false,
        error: 'Login required - Cookie may be invalid or expired',
        bodyPreview: articleData.bodyPreview
      };
    }
    
    return {
      success: true,
      title: articleData.title,
      content: articleData.content,
      html: articleData.html,
      bodyPreview: articleData.bodyPreview
    };
    
  } catch (error) {
    await browser.close();
    return {
      success: false,
      error: error.message
    };
  }
}

// 命令行调用
if (require.main === module) {
  const articleUrl = process.argv[2];
  const cookieString = process.argv[3];
  
  if (!articleUrl || !cookieString) {
    console.error('Usage: node fetch-twitter-article.js <article_url> <cookie_string>');
    process.exit(1);
  }
  
  fetchTwitterArticle(articleUrl, cookieString)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(error => {
      console.error('Error:', error);
      process.exit(1);
    });
}

module.exports = { fetchTwitterArticle };

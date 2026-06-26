#!/usr/bin/env node

/**
 * 測試用：勇敢瀏覽器 + Facebook
 * 使用 brave-loggedin-tag-browsing 的方式，但目標改為 Facebook
 */

const { chromium } = require('playwright');
const path = require('path');
const os = require('os');

const OPENCLAW_CDP_PORT = 18800;

async function braveBrowseFacebook(username, options = {}) {
  const maxPosts = options.maxPosts || 5;
  
  console.log(`\n📘 開始提取 Facebook 用戶 @${username} 的帖子（最大 ${maxPosts} 篇）`);
  
  let browser = null;
  let context = null;
  let page = null;
  
  try {
    // 1. 嘗試連接 OpenClaw Brave
    console.log('🔍 嘗試連接到 OpenClaw Brave...');
    browser = await chromium.connectOverCDP(`http://localhost:${OPENCLAW_CDP_PORT}`);
    const contexts = browser.contexts();
    if (contexts.length > 0) {
      context = contexts[0];
      const pages = context.pages();
      page = pages.length > 0 ? pages[0] : await context.newPage();
    }
    console.log('✅ 已連接');
    
    // 2. 導航到 Facebook 用戶頁面
    const url = `https://www.facebook.com/${username}`;
    console.log(`🌐 導航到 ${url}...`);
    await page.goto(url, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(3000);
    
    // 3. 檢測登入狀態
    const loginStatus = await page.evaluate(() => {
      const accountBtn = document.querySelector('[aria-label*="account"]') ||
                        document.querySelector('a[href*="/settings"]') ||
                        document.querySelector('[role="button"] span');
      return accountBtn ? accountBtn.innerText.trim() : '未檢測到登入狀態';
    });
    console.log(`🔐 登入狀態: ${loginStatus}`);
    
    // 4. 提取 Facebook 帖子（使用更通用的方法）
    console.log('📝 提取帖子內容...');
    const posts = await page.evaluate((max) => {
      // 方法：尋找所有包含文本的 Div，過濾出可能的帖子
      const allDivs = document.querySelectorAll('div');
      const candidateDivs = Array.from(allDivs).filter(div => {
        const text = div.innerText || '';
        // 簡單 heuristic：文字長度在 50-2000 字元之間，且不包含導航文字
        return text.length >= 50 && text.length <= 2000 &&
               !div.querySelector('nav, [role="navigation"]') &&
               !div.closest('nav');
      });
      
      console.log(`找到 ${candidateDivs.length} 個候選文本區塊`);
      
      const results = [];
      candidateDivs.slice(0, max).forEach((div, index) => {
        try {
          const text = div.innerText.trim();
          
          // 尋找時間資訊
          let time = null;
          const timeEl = div.querySelector('time, abbr[title], span[data-utime]');
          if (timeEl) {
            time = timeEl.getAttribute('datetime') || 
                   timeEl.getAttribute('data-utime') || 
                   timeEl.getAttribute('title');
          }
          
          // 嘗試找到更精確的父容器來當作一個 "帖子"
          const postContainer = div.closest('div[data-pagelet], div[data-testid], section');
          
          results.push({ 
            time: time, 
            text: text.substring(0, 500), // 限制長度
            containerType: postContainer ? 'found' : 'raw'
          });
        } catch (e) {
          console.warn('提取單個帖子失敗:', e.message);
        }
      });
      
      return results;
    }, maxPosts);
    
    console.log(`✅ 成功提取 ${posts.length} 篇帖子`);
    
    return {
      username: username,
      loginStatus: loginStatus,
      platform: "facebook",
      posts: posts,
      metadata: {
        maxPosts,
        timestamp: new Date().toISOString()
      }
    };
    
  } catch (error) {
    console.error('❌ 執行失敗:', error.message);
    throw error;
  } finally {
    // 可選：關閉瀏覽器（不關閉以維持狀態）
    // if (browser) await browser.close();
  }
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.error(JSON.stringify({
      error: "缺少必要參數：username",
      example: 'node fb-test.js zuckerberg 5',
      json_format: '{"username":"zuckerberg","maxPosts":5}'
    }, null, 2));
    process.exit(1);
  }
  
  const username = args[0];
  const maxPosts = parseInt(args[1]) || 5;
  
  braveBrowseFacebook(username, { maxPosts })
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    })
    .catch(err => {
      console.error(JSON.stringify({
        error: err.message,
        stack: process.env.DEBUG ? err.stack : undefined
      }));
      process.exit(1);
    });
}

module.exports = { braveBrowseFacebook };

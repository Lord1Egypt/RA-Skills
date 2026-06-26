#!/usr/bin/env node

/**
 * ChatGPT/Claude 分享链接抓取脚本
 * 使用 Chrome CDP (Chrome DevTools Protocol) 抓取页面内容
 * 
 * 用法:
 *   node capture-cdp.js <URL> [OUTPUT_DIR]
 * 
 * 环境变量:
 *   CHROME_DEBUG_PORT - Chrome 调试端口 (默认: 9222)
 */

const WebSocket = require('ws');
const fs = require('fs');
const http = require('http');
const path = require('path');

const DEBUG_PORT = process.env.CHROME_DEBUG_PORT || 9222;
const TARGET_URL = process.argv[2] || process.env.TARGET_URL;
const OUTPUT_DIR = process.argv[3] || process.env.OUTPUT_DIR || null;

/**
 * 获取 Chrome 已打开的页面列表
 */
async function getChromeTargets() {
  return new Promise((resolve, reject) => {
    const req = http.get(`http://127.0.0.1:${DEBUG_PORT}/json/list`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => {
      req.destroy();
      reject(new Error('Connection timeout'));
    });
  });
}

/**
 * 后台创建新标签页（使用 Target.createTarget）
 */
async function createNewPage(targetUrl) {
  return new Promise((resolve, reject) => {
    // 先获取一个现有页面的 WebSocket 连接
    http.get(`http://127.0.0.1:${DEBUG_PORT}/json/list`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const pages = JSON.parse(data);
          if (pages.length === 0) {
            reject(new Error('No existing pages to create background tab'));
            return;
          }
          
          // 使用第一个页面的 WebSocket 连接
          const wsUrl = pages[0].webSocketDebuggerUrl;
          const ws = new WebSocket(wsUrl);
          
          ws.on('open', () => {
            ws.send(JSON.stringify({
              id: 1,
              method: 'Target.createTarget',
              params: {
                url: targetUrl,
                background: true  // 后台创建，不激活标签页
              }
            }));
          });
          
          ws.on('message', (msg) => {
            const resp = JSON.parse(msg.toString());
            if (resp.id === 1 && resp.result?.targetId) {
              ws.close();
              // 返回新创建的页面信息
              // 需要重新获取页面列表来获取完整信息
              http.get(`http://127.0.0.1:${DEBUG_PORT}/json/list`, (res2) => {
                let data2 = '';
                res2.on('data', chunk => data2 += chunk);
                res2.on('end', () => {
                  const newPages = JSON.parse(data2);
                  const newPage = newPages.find(p => p.id === resp.result.targetId);
                  resolve(newPage || { id: resp.result.targetId, url: targetUrl, title: '' });
                });
              }).on('error', reject);
            }
          });
          
          ws.on('error', reject);
          
          // 超时处理
          setTimeout(() => {
            ws.close();
            reject(new Error('Timeout creating background tab'));
          }, 10000);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/**
 * 关闭标签页
 */
async function closePage(pageId) {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${DEBUG_PORT}/json/close/${pageId}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve(data);
      });
    }).on('error', reject);
  });
}

/**
 * 通过 CDP 抓取页面 HTML
 */
async function capturePage(pageId) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://127.0.0.1:${DEBUG_PORT}/devtools/page/${pageId}`);
    let messageId = 0;
    let resolved = false;

    const cleanup = () => {
      if (!resolved) {
        resolved = true;
        try { ws.close(); } catch (e) {}
      }
    };

    ws.on('open', () => {
      // 启用 Page domain
      sendCommand('Page.enable');
      // 等待页面稳定后抓取
      setTimeout(() => {
        sendCommand('Runtime.evaluate', {
          expression: 'document.documentElement.outerHTML',
          returnByValue: true
        });
      }, 2000);
    });

    ws.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.result?.result?.value) {
        resolved = true;
        resolve(msg.result.result.value);
        ws.close();
      }
    });

    ws.on('error', (err) => {
      cleanup();
      reject(err);
    });

    ws.on('close', () => {
      if (!resolved) {
        cleanup();
        reject(new Error('Connection closed'));
      }
    });

    function sendCommand(method, params = {}) {
      messageId++;
      ws.send(JSON.stringify({ id: messageId, method, params }));
    }

    // 超时 30 秒
    setTimeout(() => {
      cleanup();
      reject(new Error('Timeout'));
    }, 30000);
  });
}

/**
 * 主函数
 */
async function main() {
  if (!TARGET_URL) {
    console.error('用法: node capture-cdp.js <URL> [OUTPUT_DIR]');
    console.error('或设置环境变量: TARGET_URL OUTPUT_DIR CHROME_DEBUG_PORT');
    process.exit(1);
  }

  console.log(`🔍 连接 Chrome 端口 ${DEBUG_PORT}...`);
  console.log(`🎯 目标: ${TARGET_URL}`);

  // 获取已打开的页面
  let targets;
  try {
    targets = await getChromeTargets();
  } catch (err) {
    console.error('❌ 无法连接 Chrome 调试端口:', err.message);
    console.log('请确保 Chrome 已启动并带有 --remote-debugging-port 参数');
    process.exit(1);
  }

  // 查找目标页面（精确匹配 URL）
  let pageTarget = targets.find(t => t.url === TARGET_URL);
  let isNewTab = false;

  if (pageTarget) {
    console.log(`✅ 找到已打开的页面：${pageTarget.title || '(无标题)'}`);
  } else {
    // 没有精确匹配，创建新标签页
    console.log('📑 创建新标签页...');
    pageTarget = await createNewPage(TARGET_URL);
    isNewTab = true;
    console.log(`⏳ 等待页面加载...`);
    await new Promise(r => setTimeout(r, 10000)); // 增加等待时间到 10 秒
    
    // 重新获取页面列表，获取正确的标题
    const newTargets = await getChromeTargets();
    const updatedTarget = newTargets.find(t => t.url === TARGET_URL);
    if (updatedTarget && updatedTarget.title) {
      pageTarget = updatedTarget;
    }
  }

  console.log(`📄 抓取页面：${pageTarget.title || '(加载中)'} (${pageTarget.url})`);

  const html = await capturePage(pageTarget.id);
  const pageId = pageTarget.id;  // 保存页面 ID 用于后续关闭

  // 从 HTML 中提取标题（优先 <title>，其次 og:title）
  let pageTitle = 'untitled';
  
  const titleTagMatch = html.match(/<title>([^<]+)<\/title>/i);
  if (titleTagMatch) {
    pageTitle = titleTagMatch[1].trim();
  } else {
    const ogTitleMatch = html.match(/<meta property="og:title" content="([^"]+)"/);
    if (ogTitleMatch) {
      pageTitle = ogTitleMatch[1];
    }
  }
  
  // 清理标题（移除 "ChatGPT - " 或 "Claude - " 前缀）
  pageTitle = pageTitle
    .replace(/^(ChatGPT|Claude)\s*-\s*/i, '')
    .trim();

  // 使用本地时区日期和时间
  const now = new Date();
  const dateStr = now.toLocaleDateString('sv-SE', { timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone }); // YYYY-MM-DD 格式
  const timestamp = now.toLocaleString('sv-SE', { 
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    hour12: false 
  }).replace(/[ :]/g, '-').replace(/,/g, 'T'); // YYYY-MM-DDTHH-mm-ss 格式
  
  // 生成文件名 slug
  const slug = pageTitle
    .replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '-')
    .slice(0, 50);
  
  // 确定输出目录
  const isClaude = TARGET_URL.includes('claude.ai');
  const homeDir = process.env.HOME || process.env.USERPROFILE || '~';
  const outputBase = OUTPUT_DIR || `${homeDir}/LookBack/${dateStr}/${isClaude ? 'Claude' : 'ChatGPT'}`;
  
  // 创建目录
  if (!fs.existsSync(outputBase)) {
    fs.mkdirSync(outputBase, { recursive: true });
  }

  const htmlPath = path.join(outputBase, `${slug}-${timestamp}-captured.html`);
  fs.writeFileSync(htmlPath, html);
  console.log(`✅ HTML 已保存：${htmlPath}`);

  // 提取元数据
  const descMatch = html.match(/<meta property="og:description" content="([^"]+)"/);

  // 保存元数据
  const metaPath = path.join(outputBase, '.metadata.json');
  const metadata = {
    title: pageTitle,
    description: descMatch?.[1] || '',
    source: TARGET_URL,
    htmlPath,
    timestamp,
    slug,
    outputBase
  };
  fs.writeFileSync(metaPath, JSON.stringify(metadata, null, 2));
  
  console.log(`✅ 元数据已保存：${metaPath}`);
  console.log(`📋 标题: ${pageTitle}`);
  
  // 如果是新创建的标签页，抓取完成后关闭
  if (isNewTab) {
    try {
      await closePage(pageId);
      console.log(`🗑️ 已关闭临时标签页`);
    } catch (e) {
      console.log(`⚠️ 关闭标签页失败: ${e.message}`);
    }
  }
  
  return metadata;
}

main()
  .then(meta => {
    console.log('\n🎉 抓取完成！');
    process.exit(0);
  })
  .catch(err => {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  });
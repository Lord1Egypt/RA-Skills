/**
 * AI Browser WebSocket Server
 * 基于 Puppeteer 的轻量级浏览器控制服务
 * 端口：18790
 */

const puppeteer = require('puppeteer');
const WebSocket = require('ws');
const http = require('http');

const PORT = process.env.AI_BROWSER_PORT || 18790;
let browser = null;
let page = null;
let currentTabId = 'default';

// 简单的标签页管理 (单例模式，简化版)
const tabs = new Map();

async function initBrowser() {
    if (!browser) {
        console.log('🚀 启动无头浏览器...');
        browser = await puppeteer.launch({
            headless: false, // 显示界面，方便人工介入
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--remote-debugging-port=9222'
            ]
        });
        console.log('✅ 浏览器已启动');
        
        // 监听页面关闭事件
        browser.on('targetdestroyed', async (target) => {
            if (target.type() === 'page') {
                const id = target.url(); // 简单用 URL 做标识
                console.log(`🗑️ 页面已关闭: ${id}`);
                tabs.delete(id);
            }
        });
    }
    return browser;
}

async function handleAction(action, params) {
    const wsPage = page || (browser && (await browser.pages())[0]);
    
    switch (action) {
        case 'navigate':
            if (!wsPage) throw new Error('没有活动的页面');
            await wsPage.goto(params.url, { waitUntil: 'networkidle2' });
            return { success: true, url: wsPage.url(), title: await wsPage.title() };
            
        case 'snapshot':
            if (!wsPage) throw new Error('没有活动的页面');
            // 获取可交互的 DOM 结构简化版
            const dom = await wsPage.evaluate(() => {
                return {
                    title: document.title,
                    url: document.location.href,
                    inputs: Array.from(document.querySelectorAll('input, textarea')).map(i => ({ name: i.name, value: i.value })),
                    links: Array.from(document.querySelectorAll('a')).slice(0, 20).map(a => ({ text: a.innerText, href: a.href })),
                    buttons: Array.from(document.querySelectorAll('button, [role="button"]')).slice(0, 20).map(b => ({ text: b.innerText }))
                };
            });
            return dom;

        case 'screenshot':
            if (!wsPage) throw new Error('没有活动的页面');
            const buffer = await wsPage.screenshot({ fullPage: params.fullPage || false, encoding: 'base64' });
            return { image: buffer };

        case 'click':
            if (!wsPage) throw new Error('没有活动的页面');
            await wsPage.click(params.selector);
            return { success: true, action: 'click', target: params.selector };

        case 'type':
            if (!wsPage) throw new Error('没有活动的页面');
            await wsPage.type(params.selector, params.text, { delay: params.delay || 50 });
            return { success: true, action: 'type', target: params.selector, text: params.text };

        case 'evaluate':
            if (!wsPage) throw new Error('没有活动的页面');
            const result = await wsPage.evaluate(params.script);
            return { result };

        case 'status':
            return { 
                status: 'running', 
                pages: browser ? (await browser.pages()).length : 0,
                port: PORT
            };

        default:
            throw new Error(`未知动作：${action}`);
    }
}

// 启动 WebSocket 服务器
const wss = new WebSocket.Server({ port: PORT });
console.log(`🦞 AI Browser Server 启动在 ws://localhost:${PORT}`);

wss.on('connection', (ws) => {
    console.log('🔌 新的客户端连接');
    
    ws.on('message', async (message) => {
        try {
            const { action, params, id } = JSON.parse(message);
            console.log(`⚡ 收到指令：${action}`, params);

            if (!browser) await initBrowser();
            if (!page) page = await browser.newPage();
            if (params.targetId) {
                // 简单处理：如果有 targetId 且不是当前页，尝试切换（简化版暂不实现多 Tab 切换逻辑，默认单页）
                // 实际使用中，可以扩展为多 page 管理
            }

            const result = await handleAction(action, params || {});
            ws.send(JSON.stringify({ id, success: true, result }));
        } catch (error) {
            console.error('❌ 执行错误:', error);
            ws.send(JSON.stringify({ id: JSON.parse(message).id, success: false, error: error.message }));
        }
    });

    ws.on('close', () => {
        console.log('🔌 客户端断开连接');
    });
});

// 保持进程运行
process.on('SIGINT', async () => {
    console.log('\n🛑 关闭浏览器...');
    if (browser) await browser.close();
    process.exit(0);
});

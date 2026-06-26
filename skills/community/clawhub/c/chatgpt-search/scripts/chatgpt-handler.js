#!/usr/bin/env node

/**
 * ChatGPT Search - OpenClaw Browser Automation Handler
 * 
 * 这个脚本提供与 OpenClaw browser 工具的集成
 * 通过 MCP 或直接调用 browser 工具执行搜索
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
    chatgptUrl: 'https://chatgpt.com',
    timeout: 30000,
    waitAfterType: 500,
    waitAfterSubmit: 10000,
    screenshotDir: '/tmp/chatgpt-screenshots'
};

/**
 * 在 ChatGPT 上搜索问题
 * 
 * @param {string} query - 搜索问题
 * @param {object} browser - OpenClaw browser 工具实例
 * @param {boolean} closeAfterSearch - 搜索完成后是否关闭标签页
 * @returns {Promise<object>} 搜索结果
 */
async function searchChatGPT(query, browser, closeAfterSearch = true) {
    const startTime = Date.now();
    const result = {
        query: query,
        answer: null,
        success: false,
        error: null,
        elapsedSeconds: 0,
        timestamp: new Date().toISOString(),
        targetId: null
    };
    
    try {
        // 1. 打开 ChatGPT
        console.log('🌐 打开 ChatGPT...');
        const openResult = await browser.open({ url: CONFIG.chatgptUrl });
        const targetId = openResult.targetId;
        result.targetId = targetId;
        
        // 2. 等待页面加载
        console.log('⏳ 等待页面加载...');
        await sleep(3000);
        
        // 3. 获取页面快照
        console.log('📸 获取页面快照...');
        const snapshot = await browser.snapshot({ 
            targetId: targetId, 
            refs: 'aria',
            timeoutMs: 10000 
        });
        
        // 4. 找到输入框并输入问题
        console.log('✍️  输入问题...');
        // 输入框通常是 e127 或类似的 ref
        await browser.act({ 
            targetId: targetId,
            kind: 'type', 
            ref: 'e127', 
            text: query 
        });
        
        // 5. 短暂等待
        await sleep(CONFIG.waitAfterType);
        
        // 6. 按回车提交
        console.log('📤 提交问题...');
        await browser.act({ 
            targetId: targetId,
            kind: 'press', 
            key: 'Enter' 
        });
        
        // 7. 等待回答
        console.log('⏳ 等待 ChatGPT 回答...');
        await sleep(CONFIG.waitAfterSubmit);
        
        // 8. 获取回答
        console.log('📥 获取回答...');
        const answerSnapshot = await browser.snapshot({ 
            targetId: targetId, 
            refs: 'aria',
            timeoutMs: 15000 
        });
        
        // 9. 解析回答
        result.answer = parseAnswer(answerSnapshot);
        result.success = true;
        
        // 10. 保存截图（可选）
        await saveScreenshot(browser, targetId, query);
        
        // 11. 关闭标签页（如果配置了）
        if (closeAfterSearch) {
            console.log('🔒 关闭标签页...');
            await closeTab(browser, targetId);
        }
        
    } catch (error) {
        result.error = error.message;
        result.success = false;
        
        // 即使出错也尝试关闭标签页
        if (closeAfterSearch && result.targetId) {
            console.log('🔒 出错后关闭标签页...');
            try {
                await closeTab(browser, result.targetId);
            } catch (closeError) {
                console.error(`关闭标签页失败：${closeError.message}`);
            }
        }
    }
    
    result.elapsedSeconds = ((Date.now() - startTime) / 1000).toFixed(2);
    return result;
}

/**
 * 从快照中解析 ChatGPT 的回答
 */
function parseAnswer(snapshot) {
    // 解析快照内容，提取 ChatGPT 的回答
    // 这需要根据实际的快照结构调整
    if (!snapshot || typeof snapshot !== 'object') {
        return '无法解析回答';
    }
    
    // 尝试从快照中提取文本内容
    // 实际实现需要根据快照格式调整
    const textContent = extractTextFromSnapshot(snapshot);
    return textContent || '未获取到回答';
}

/**
 * 从快照中提取文本
 */
function extractTextFromSnapshot(snapshot) {
    // 递归提取所有文本内容
    let text = '';
    
    function extract(obj) {
        if (!obj || typeof obj !== 'object') return;
        
        if (obj.text && typeof obj.text === 'string') {
            text += obj.text + ' ';
        }
        
        if (obj.generic && Array.isArray(obj.generic)) {
            obj.generic.forEach(extract);
        }
        
        if (obj.children && Array.isArray(obj.children)) {
            obj.children.forEach(extract);
        }
    }
    
    extract(snapshot);
    return text.trim();
}

/**
 * 保存截图
 */
async function saveScreenshot(browser, targetId, query) {
    try {
        // 创建截图目录
        if (!fs.existsSync(CONFIG.screenshotDir)) {
            fs.mkdirSync(CONFIG.screenshotDir, { recursive: true });
        }
        
        // 生成文件名
        const filename = `chatgpt-${Date.now()}-${hashQuery(query)}.png`;
        const filepath = path.join(CONFIG.screenshotDir, filename);
        
        // 截图
        await browser.screenshot({
            targetId: targetId,
            path: filepath,
            fullPage: false
        });
        
        console.log(`📷 截图已保存：${filepath}`);
        return filepath;
    } catch (error) {
        console.error(`截图失败：${error.message}`);
        return null;
    }
}

/**
 * 简单的哈希函数
 */
function hashQuery(query) {
    let hash = 0;
    for (let i = 0; i < query.length; i++) {
        const char = query.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 8);
}

/**
 * 延迟函数
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 关闭标签页
 */
async function closeTab(browser, targetId) {
    try {
        await browser.close({ targetId: targetId });
        console.log('✅ 标签页已关闭');
    } catch (error) {
        console.error(`关闭标签页失败：${error.message}`);
        throw error;
    }
}

// 导出函数
module.exports = {
    searchChatGPT,
    closeTab,
    CONFIG
};

// 如果直接运行
if (require.main === module) {
    const query = process.argv.slice(2).join(' ');
    if (!query) {
        console.error('用法：node chatgpt-handler.js "你的问题"');
        process.exit(1);
    }
    
    console.log('ChatGPT Search Handler');
    console.log('=====================');
    console.log('注意：此脚本需要通过 OpenClaw browser 工具执行');
    console.log('请在 OpenClaw 会话中使用 browser 工具调用 searchChatGPT 函数');
}

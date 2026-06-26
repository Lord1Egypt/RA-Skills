#!/usr/bin/env node

/**
 * ChatGPT Search Script
 * 使用浏览器自动化在 ChatGPT 上搜索问题
 * 
 * 用法：
 * node chatgpt-search.js "你的问题"
 * node chatgpt-search.js "你的问题" --context "额外信息"
 * node chatgpt-search.js "你的问题" --output json
 */

const { execSync } = require('child_process');
const path = require('path');

// 解析命令行参数
const args = process.argv.slice(2);
const outputFormat = args.includes('--output') ? args[args.indexOf('--output') + 1] : 'text';
const timeout = args.includes('--timeout') ? parseInt(args[args.indexOf('--timeout') + 1]) : 30000;
const context = args.includes('--context') ? args[args.indexOf('--context') + 1] : null;
const closeAfterSearch = !args.includes('--keep-open');

// 提取查询文本（排除参数）
let query = args.filter(arg => !arg.startsWith('--') && 
                               !['text', 'json'].includes(arg) && 
                               !arg.match(/^\d+$/)).join(' ');

if (!query) {
    console.error('用法：node chatgpt-search.js "你的问题" [--context "额外信息"] [--output json|text]');
    process.exit(1);
}

// 如果有上下文，添加到查询中
if (context) {
    query = `${query} (${context})`;
}

console.error(`🔍 正在搜索：${query}`);
console.error(`⏱️  超时：${timeout}ms`);
console.error(`📄 输出格式：${outputFormat}`);
console.error(`🔒 搜索后关闭标签页：${closeAfterSearch ? '是' : '否'}`);

const startTime = Date.now();

try {
    // 使用 OpenClaw browser 工具进行搜索
    // 这里我们生成一个浏览器操作脚本
    const browserScript = generateBrowserScript(query);
    
    // 执行浏览器操作（通过 OpenClaw 的 browser 工具）
    // 由于这是 Skill 脚本，我们输出指令让 OpenClaw 执行
    console.log(`\n📋 请在 OpenClaw 中执行以下操作：\n`);
    console.log(`1. 打开 ChatGPT: https://chatgpt.com`);
    console.log(`2. 输入问题：${query}`);
    console.log(`3. 获取回答\n`);
    
    // 实际执行需要通过 OpenClaw 的 browser 工具
    // 这里提供的是接口说明
    const result = {
        query: query,
        answer: "请通过 OpenClaw browser 工具执行搜索",
        elapsedSeconds: ((Date.now() - startTime) / 1000).toFixed(2),
        timestamp: new Date().toISOString(),
        instructions: {
            step1: "browser.open({ url: 'https://chatgpt.com' })",
            step2: "browser.act({ kind: 'type', ref: 'textbox_ref', text: query })",
            step3: "browser.act({ kind: 'press', key: 'Enter' })",
            step4: "等待回答后使用 browser.snapshot() 获取内容"
        }
    };
    
    if (outputFormat === 'json') {
        console.log(JSON.stringify(result, null, 2));
    } else {
        console.log(`\nChatGPT 搜索结果`);
        console.log(`================`);
        console.log(`问题：${result.query}`);
        console.log(`\n回答：${result.answer}`);
        console.log(`\n---`);
        console.log(`搜索时间：${result.elapsedSeconds}秒`);
        console.log(`时间戳：${result.timestamp}`);
    }
    
} catch (error) {
    console.error(`❌ 搜索失败：${error.message}`);
    process.exit(1);
}

/**
 * 生成浏览器操作脚本
 */
function generateBrowserScript(query) {
    return `
// 1. 打开 ChatGPT
browser.open({ url: 'https://chatgpt.com' })

// 2. 等待页面加载
await sleep(2000)

// 3. 获取页面快照找到输入框
browser.snapshot({ refs: 'aria' })

// 4. 输入问题
browser.act({ kind: 'type', ref: 'e127', text: '${query.replace(/'/g, "\\'")}' })

// 5. 按回车
browser.act({ kind: 'press', key: 'Enter' })

// 6. 等待回答
await sleep(5000)

// 7. 获取回答
browser.snapshot({ refs: 'aria' })
`;
}

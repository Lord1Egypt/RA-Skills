#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

// API配置 - 从环境变量读取
require('dotenv').config();
const API_KEY = process.env.OKX_API_KEY || "";
const API_SECRET = process.env.OKX_API_SECRET || "";
const PASSPHRASE = "";

if (!API_KEY || !API_SECRET) {
    console.error("⚠️  错误: OKX_API_KEY 和 OKX_API_SECRET 未设置");
    console.error("   请在项目根目录创建 .env 文件:");
    console.error("   OKX_API_KEY=your-api-key");
    console.error("   OKX_API_SECRET=your-api-secret");
    process.exit(1);
}

function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        symbol: args[0] || 'BTC-USDT',
        timeframe: '4H',
        signalOnly: false,
        limit: 200
    };

    for (let i = 1; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--timeframe' || arg === '-t') {
            options.timeframe = args[++i];
        } else if (arg === '--signal-only' || arg === '-s') {
            options.signalOnly = true;
        } else if (arg === '--limit' || arg === '-l') {
            options.limit = parseInt(args[++i]);
        }
    }
    return options;
}

function runAnalysis(options) {
    const scriptPath = path.join(__dirname, 'okx_analyst.py');
    const cmd = [
        'python3', scriptPath, options.symbol,
        '--timeframe', options.timeframe,
        '--limit', options.limit.toString()
    ];
    if (options.signalOnly) cmd.push('--signal-only');

    try {
        const output = execSync(cmd.join(' '), { encoding: 'utf-8', timeout: 60000 });
        console.log(output);
    } catch (error) {
        console.error('分析执行失败:', error.message);
        if (error.stderr) console.error('错误详情:', error.stderr);
    }
}

function main() {
    console.log('🔍 OKX Trading Analyst v1.0\n');
    const options = parseArgs();
    console.log(`正在分析: ${options.symbol} (${options.timeframe}周期)\n`);
    runAnalysis(options);
}

main();

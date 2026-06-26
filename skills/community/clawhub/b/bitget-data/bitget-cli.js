#!/usr/bin/env node
// Bitget Trader CLI - 统一命令行接口

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DATA_DIR = __dirname;
const SCRIPTS = {
    // 核心交易
    'monitor': 'monitor-grid.js',
    'start': 'start-simple.js',
    'stop': 'cancel-all.js',
    'cancel': 'cancel-all.js',
    'balance': 'check-balance.js',
    
    // 分析与优化
    'optimize': 'grid-optimizer.js',
    'analyze': 'trade-analyzer.js',
    'kline': 'kline-analyzer.js',
    'report': 'quick-report.js',
    
    // 动态调整
    'dynamic': 'dynamic-adjust.js',
    'rebalance': 'dynamic-rebalance.js',
    'scheme-a': 'apply-scheme-a.js',
    
    // 单个币种
    'start-btc': 'start-grids.js',
    'start-eth': 'start-eth.js',
    'start-sol': 'start-sol.js',
    'start-bnb': 'deploy-bnb-grid.js',
    
    // 买入操作
    'buy-eth': 'buy-eth-market.js',
    'buy-bnb': 'buy-bnb-market.js',
};

const HELP = `
🟦 Bitget Trader CLI

用法：node bitget-cli.js <命令> [选项]

核心命令:
  monitor      监控所有网格策略
  start        启动所有网格
  stop         停止所有网格 (取消所有订单)
  balance      查询账户余额

分析优化:
  optimize     优化网格参数
  analyze      分析交易历史
  kline        分析 K 线数据
  report       生成快速报告

动态调整:
  dynamic      动态网格调整
  rebalance    组合再平衡
  scheme-a     应用方案 A

单个币种:
  start-btc    启动 BTC 网格
  start-eth    启动 ETH 网格
  start-sol    启动 SOL 网格
  start-bnb    启动 BNB 网格

买入操作:
  buy-eth      市价买入 ETH
  buy-bnb      市价买入 BNB

示例:
  node bitget-cli.js monitor      # 监控网格
  node bitget-cli.js start        # 启动所有
  node bitget-cli.js stop         # 停止所有
  node bitget-cli.js balance      # 查询余额
  node bitget-cli.js optimize     # 优化参数
`;

function runScript(scriptName) {
    const scriptPath = path.join(DATA_DIR, scriptName);
    
    if (!fs.existsSync(scriptPath)) {
        console.error(`❌ 脚本不存在：${scriptPath}`);
        return false;
    }
    
    try {
        console.log(`🟦 执行：${scriptName}\n`);
        execSync(`node "${scriptPath}"`, { 
            stdio: 'inherit',
            cwd: DATA_DIR
        });
        return true;
    } catch (error) {
        console.error(`❌ 执行失败：${error.message}`);
        return false;
    }
}

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
        console.log(HELP);
        process.exit(0);
    }
    
    const command = args[0];
    
    if (command === 'list') {
        console.log('🟦 可用命令:\n');
        Object.entries(SCRIPTS).forEach(([cmd, script]) => {
            console.log(`  ${cmd.padEnd(15)} → ${script}`);
        });
        process.exit(0);
    }
    
    if (command === 'status') {
        console.log('🟦 Bitget 网格状态\n');
        
        // 检查配置文件
        const configFile = path.join(DATA_DIR, 'config.json');
        if (fs.existsSync(configFile)) {
            const config = JSON.parse(fs.readFileSync(configFile));
            console.log('✅ 配置文件：存在');
            console.log(`   API Key: ${config.apiKey?.substring(0, 10)}...`);
            console.log(`   模拟模式：${config.isSimulation ? '是' : '否'}`);
        } else {
            console.log('❌ 配置文件：不存在');
        }
        
        // 检查网格设置
        const settingsFile = path.join(DATA_DIR, 'grid_settings.json');
        if (fs.existsSync(settingsFile)) {
            const settings = JSON.parse(fs.readFileSync(settingsFile));
            const coins = Object.keys(settings).filter(k => k !== 'optimization');
            console.log(`\n✅ 网格配置：${coins.length} 个币种`);
            coins.forEach(coin => {
                const s = settings[coin];
                console.log(`   ${s.symbol}: ${s.gridNum} 网格 | ${s.priceMin}-${s.priceMax} | ${s.amount} USDT/单`);
            });
        } else {
            console.log('❌ 网格配置：不存在');
        }
        
        // 检查日志文件
        const logFile = path.join(DATA_DIR, 'grid_monitor.log');
        if (fs.existsSync(logFile)) {
            const stats = fs.statSync(logFile);
            console.log(`\n✅ 日志文件：${(stats.size / 1024).toFixed(2)} KB`);
        }
        
        process.exit(0);
    }
    
    const script = SCRIPTS[command];
    
    if (!script) {
        console.error(`❌ 未知命令：${command}`);
        console.log('\n使用 node bitget-cli.js --help 查看可用命令');
        process.exit(1);
    }
    
    const success = runScript(script);
    process.exit(success ? 0 : 1);
}

main();

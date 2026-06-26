#!/usr/bin/env node
// Bitget 快速启动向导

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DATA_DIR = __dirname;
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'grid_settings.json');

const MENU = `
🟦 Bitget 网格交易快速启动向导

请选择操作:
  1. 检查配置 (Check Config)
  2. 查看余额 (Check Balance)
  3. 启动所有网格 (Start All)
  4. 停止所有网格 (Stop All)
  5. 监控状态 (Monitor)
  6. 优化网格 (Optimize)
  7. 生成报告 (Report)
  8. 设置定时任务 (Setup Cron)
  0. 退出 (Exit)
`;

function checkConfig() {
    console.log('\n📋 检查配置...\n');
    
    // 检查配置文件
    if (!fs.existsSync(CONFIG_FILE)) {
        console.log('❌ 配置文件不存在：config.json');
        console.log('   请创建 config.json:\n');
        console.log(`{
  "apiKey": "bg_your_api_key",
  "secretKey": "your_secret_key",
  "passphrase": "your_passphrase",
  "isSimulation": false
}\n`);
        return false;
    }
    
    const config = JSON.parse(fs.readFileSync(CONFIG_FILE));
    console.log('✅ 配置文件：存在');
    console.log(`   API Key: ${config.apiKey?.substring(0, 10)}...`);
    console.log(`   模拟模式：${config.isSimulation ? '是' : '否'}`);
    
    // 检查网格设置
    if (!fs.existsSync(SETTINGS_FILE)) {
        console.log('\n❌ 网格设置不存在：grid_settings.json');
        return false;
    }
    
    const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE));
    const coins = Object.keys(settings).filter(k => k !== 'optimization');
    console.log(`\n✅ 网格配置：${coins.length} 个币种`);
    coins.forEach(coin => {
        const s = settings[coin];
        console.log(`   ${s.symbol}: ${s.gridNum} 网格 | ${s.priceMin}-${s.priceMax} USDT`);
    });
    
    console.log('\n✅ 配置检查完成!\n');
    return true;
}

function checkBalance() {
    console.log('\n💰 查询余额...\n');
    runScript('check-balance.js');
}

function startAll() {
    console.log('\n🚀 启动所有网格...\n');
    console.log('⚠️  警告：这将启动所有配置的网格策略!\n');
    runScript('start-simple.js');
}

function stopAll() {
    console.log('\n🛑 停止所有网格...\n');
    console.log('⚠️  警告：这将取消所有订单!\n');
    runScript('cancel-all.js');
}

function monitor() {
    console.log('\n📊 监控网格状态...\n');
    runScript('monitor-grid.js');
}

function optimize() {
    console.log('\n🔧 优化网格参数...\n');
    runScript('grid-optimizer.js');
}

function report() {
    console.log('\n📝 生成快速报告...\n');
    runScript('quick-report.js');
}

function setupCron() {
    console.log('\n⏰ 设置定时任务...\n');
    runScript('setup-cron.js', 'setup');
}

function runScript(script, arg = '') {
    const scriptPath = path.join(DATA_DIR, script);
    
    if (!fs.existsSync(scriptPath)) {
        console.error(`❌ 脚本不存在：${scriptPath}`);
        return;
    }
    
    try {
        execSync(`node "${scriptPath}" ${arg}`, { 
            stdio: 'inherit',
            cwd: DATA_DIR
        });
    } catch (error) {
        console.error(`❌ 执行失败：${error.message}`);
    }
}

function main() {
    console.log(MENU);
    
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    readline.question('请选择 (0-8): ', (choice) => {
        readline.close();
        
        switch (choice.trim()) {
            case '1':
                checkConfig();
                break;
            case '2':
                checkBalance();
                break;
            case '3':
                startAll();
                break;
            case '4':
                stopAll();
                break;
            case '5':
                monitor();
                break;
            case '6':
                optimize();
                break;
            case '7':
                report();
                break;
            case '8':
                setupCron();
                break;
            case '0':
                console.log('\n👋 再见!\n');
                process.exit(0);
            default:
                console.log('\n❌ 无效选择，请输入 0-8\n');
        }
        
        // 显示菜单
        setTimeout(() => main(), 1000);
    });
}

// 如果直接运行，启动菜单
if (require.main === module) {
    main();
}

module.exports = { checkConfig, checkBalance, startAll, stopAll, monitor };

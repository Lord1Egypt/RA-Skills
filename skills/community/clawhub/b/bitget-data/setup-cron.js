#!/usr/bin/env node
// Bitget Grid Cron Setup - 设置定时监控任务

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const DATA_DIR = __dirname;
const CRON_CONFIG = {
    name: 'Bitget Grid Monitor',
    schedule: {
        kind: 'every',
        everyMs: 5 * 60 * 1000  // 5 分钟
    },
    payload: {
        kind: 'systemEvent',
        text: '🟦 Bitget 网格监控提醒：检查网格状态和订单执行情况'
    },
    sessionTarget: 'main',
    enabled: true
};

function setupCron() {
    console.log('🟦 设置 Bitget 网格定时监控...\n');
    
    // 检查 cron 是否已存在
    try {
        const listOutput = execSync('openclaw cron list', { encoding: 'utf8' });
        if (listOutput.includes('Bitget')) {
            console.log('⚠️  Bitget 定时任务已存在\n');
        }
    } catch (e) {
        console.log('⚠️  无法检查现有 cron 任务\n');
    }
    
    // 创建 cron 任务
    const cronJson = JSON.stringify(CRON_CONFIG, null, 2);
    console.log('📋 Cron 配置:\n');
    console.log(cronJson);
    console.log('\n');
    
    // 使用 openclaw cron add 命令
    try {
        console.log('⏰ 添加定时任务：每 5 分钟监控一次\n');
        execSync(`openclaw cron add '${cronJson}'`, { 
            stdio: 'inherit',
            cwd: DATA_DIR
        });
        console.log('\n✅ 定时任务设置成功!\n');
    } catch (error) {
        console.error('❌ 设置失败:', error.message);
        console.log('\n手动执行以下命令:\n');
        console.log(`openclaw cron add '${cronJson}'\n`);
    }
}

function showStatus() {
    console.log('🟦 Bitget 定时任务状态\n');
    
    try {
        execSync('openclaw cron list', { stdio: 'inherit' });
    } catch (error) {
        console.error('❌ 无法获取状态:', error.message);
    }
}

function removeCron() {
    console.log('🟦 删除 Bitget 定时任务...\n');
    console.log('请手动执行:\n');
    console.log('openclaw cron list                    # 查看任务 ID');
    console.log('openclaw cron remove <job-id>        # 删除任务\n');
}

// 主程序
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
    case 'setup':
        setupCron();
        break;
    case 'status':
        showStatus();
        break;
    case 'remove':
        removeCron();
        break;
    default:
        console.log(`
🟦 Bitget Cron 管理

用法：node setup-cron.js <命令>

命令:
  setup    设置定时监控 (每 5 分钟)
  status   查看定时任务状态
  remove   删除定时任务

示例:
  node setup-cron.js setup      # 设置定时任务
  node setup-cron.js status     # 查看状态
  node setup-cron.js remove     # 删除任务
`);
}

#!/usr/bin/env node
// 设置高频网格监控的 Cron 任务

const { execSync } = require('child_process');
const fs = require('fs');

console.log('\n🔧 设置 Bitget 高频网格监控 Cron 任务...\n');

// Cron 任务配置
const cronJobs = [
    {
        name: '高频网格监控 - 每 30 分钟',
        schedule: '*/30 * * * *',
        command: 'node /Users/zongzi/.openclaw/workspace/bitget_data/auto-monitor.js >> /Users/zongzi/.openclaw/workspace/bitget_data/cron_monitor.log 2>&1',
        enabled: true
    },
    {
        name: '每日报告生成 - 每晚 21:00',
        schedule: '0 21 * * *',
        command: 'node /Users/zongzi/.openclaw/workspace/bitget_data/generate-daily-report.js >> /Users/zongzi/.openclaw/workspace/bitget_data/cron_monitor.log 2>&1',
        enabled: true
    },
    {
        name: '网格状态检查 - 每小时',
        schedule: '0 * * * *',
        command: 'node /Users/zongzi/.openclaw/workspace/bitget_data/monitor-grid.js >> /Users/zongzi/.openclaw/workspace/bitget_data/grid_monitor.log 2>&1',
        enabled: true
    }
];

console.log('📋 计划设置的 Cron 任务:\n');
console.log('─'.repeat(70));
cronJobs.forEach((job, i) => {
    console.log(`${i + 1}. ${job.name}`);
    console.log(`   频率：${job.schedule}`);
    console.log(`   命令：${job.command.substring(0, 60)}...`);
    console.log(`   状态：${job.enabled ? '✅ 启用' : '❌ 禁用'}`);
    console.log();
});
console.log('─'.repeat(70));

// 检查是否使用 gateway cron
console.log('\n💡 说明:');
console.log('OpenClaw 使用 gateway cron 系统管理定时任务');
console.log('需要手动配置或使用 sessions_spawn 创建后台监控进程\n');

// 生成配置建议
console.log('📝 推荐配置:\n');
console.log('方式 1: 使用 OpenClaw gateway cron (推荐)');
console.log('  - 稳定可靠，由 gateway 管理');
console.log('  - 需要配置 gateway cron 任务');
console.log();
console.log('方式 2: 使用系统 crontab');
console.log('  - 直接运行：crontab -e');
console.log('  - 添加上述定时任务');
console.log();
console.log('方式 3: 后台进程监控');
console.log('  - 运行 auto-monitor.js 作为后台服务');
console.log('  - 使用 pm2 或 node 直接运行');
console.log();

// 保存配置到文件
const configOutput = {
    cronJobs: cronJobs,
    setupInstructions: [
        '1. 确认高频网格配置已应用 (运行 apply-highfreq.js)',
        '2. 选择一种 cron 配置方式',
        '3. 启动监控任务',
        '4. 检查日志文件确认运行正常'
    ],
    logFiles: {
        monitor: '/Users/zongzi/.openclaw/workspace/bitget_data/auto_monitor.log',
        cron: '/Users/zongzi/.openclaw/workspace/bitget_data/cron_monitor.log',
        grid: '/Users/zongzi/.openclaw/workspace/bitget_data/grid_monitor.log',
        daily: '/Users/zongzi/.openclaw/workspace/bitget_data/daily_report.md'
    }
};

const configFile = __dirname + '/cron_config.json';
fs.writeFileSync(configFile, JSON.stringify(configOutput, null, 2));

console.log(`✅ 配置已保存到：${configFile}\n`);
console.log('🎯 下一步:');
console.log('1. 查看 cron_config.json 了解详细配置');
console.log('2. 选择并执行配置方式');
console.log('3. 启动监控后，系统会自动:');
console.log('   - 每 30 分钟检查成交情况');
console.log('   - 自动调整网格密度');
console.log('   - 每天生成交易报告');
console.log('');

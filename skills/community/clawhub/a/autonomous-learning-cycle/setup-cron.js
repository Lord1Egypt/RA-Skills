#!/usr/bin/env node

/**
 * Autonomous Learning Cycle - Cron 设置脚本
 * 
 * 功能：
 * 1. 读取 cron 配置
 * 2. 注册所有定时任务
 * 3. 验证 cron 状态
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const CRON_CONFIG_PATH = path.join(__dirname, 'configs/cron-jobs.json');

/**
 * 加载 cron 配置
 */
function loadCronConfig() {
  const defaultConfig = {
    jobs: [
      {
        name: '自主进化循环',
        schedule: '*/17 * * * *',
        command: 'node autonomous/evolution-engine.js run',
        enabled: true
      },
      {
        name: '每日反思',
        schedule: '0 23 * * *',
        command: 'node instincts/reflection.js daily',
        enabled: true
      },
      {
        name: '每周反思',
        schedule: '0 20 * * 0',
        command: 'node instincts/reflection.js weekly',
        enabled: true
      },
      {
        name: '学习方向生成',
        schedule: '0 6 * * *',
        command: 'node instincts/learning-direction.js auto',
        enabled: true
      }
    ]
  };
  
  if (fs.existsSync(CRON_CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CRON_CONFIG_PATH, 'utf-8'));
  }
  
  return defaultConfig;
}

/**
 * 注册 cron 任务
 */
function registerCronJobs() {
  const config = loadCronConfig();
  
  console.log('\n⏰ 注册定时任务...\n');
  console.log('═'.repeat(60));
  
  config.jobs.forEach((job, index) => {
    console.log(`\n任务 ${index + 1}/${config.jobs.length}: ${job.name}`);
    console.log(`   周期：${job.schedule}`);
    console.log(`   命令：${job.command}`);
    
    if (!job.enabled) {
      console.log(`   ⏭️  已禁用，跳过`);
      return;
    }
    
    try {
      // 使用 cron add 命令注册任务
      const cronCommand = `cron add --job '${JSON.stringify({
        name: job.name,
        schedule: {
          kind: 'cron',
          expr: job.schedule,
          tz: 'Asia/Shanghai'
        },
        payload: {
          kind: 'systemEvent',
          text: `⏰ ${job.name}时间到！\n\n运行命令：${job.command}`
        },
        delivery: {
          mode: 'none'
        },
        sessionTarget: 'main',
        enabled: true
      })}'`;
      
      console.log(`   执行：cron add ...`);
      const result = execSync(cronCommand, {
        cwd: WORKSPACE,
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'ignore']
      });
      
      console.log(`   ✅ 注册成功`);
    } catch (error) {
      console.error(`   ❌ 注册失败：${error.message}`);
    }
  });
  
  console.log('\n═'.repeat(60));
  console.log('\n✅ Cron 设置完成！\n');
}

/**
 * 验证 cron 状态
 */
function verifyCronStatus() {
  console.log('\n🔍 验证 cron 状态...\n');
  
  try {
    const result = execSync('cron list', {
      cwd: WORKSPACE,
      encoding: 'utf-8'
    });
    
    console.log(result);
  } catch (error) {
    console.error('❌ 无法获取 cron 状态:', error.message);
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'register';
  
  switch (command) {
    case 'register':
      registerCronJobs();
      verifyCronStatus();
      break;
    case 'verify':
      verifyCronStatus();
      break;
    default:
      console.log('用法：node setup-cron.js [command]');
      console.log('\n命令:');
      console.log('  register  - 注册所有 cron 任务（默认）');
      console.log('  verify    - 验证 cron 状态');
  }
}

// 运行主函数
main().catch(error => {
  console.error('❌ Cron 设置失败:', error.message);
  console.error(error.stack);
  process.exit(1);
});

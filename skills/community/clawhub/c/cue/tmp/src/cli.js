#!/usr/bin/env node
/**
 * Cue CLI - 命令行入口
 */

import { Command } from 'commander';
import { createLogger } from './core/logger.js';
import { createUserState } from './core/userState.js';
import { createTaskManager } from './core/taskManager.js';
import { createMonitorManager } from './core/monitorManager.js';
import { getApiKey, detectServiceFromKey, setApiKey, getApiKeyStatus } from './utils/envUtils.js';
import { startResearch, autoDetectMode } from './api/cuecueClient.js';
import chalk from 'chalk';
import ora from 'ora';
import { randomUUID } from 'crypto';

const logger = createLogger('CueCLI');
const program = new Command();

// 获取聊天 ID
const chatId = process.env.CHAT_ID || process.env.FEISHU_CHAT_ID || 'default';

// 初始化用户状态
const userState = createUserState(chatId);
const taskManager = createTaskManager(chatId);
const monitorManager = createMonitorManager(chatId);

program
  .name('cue')
  .description('Cue - 你的专属调研助理')
  .version('1.0.4');

// /cue 命令 - 开始研究
program
  .command('cue <topic>')
  .description('开始深度研究')
  .option('-m, --mode <mode>', '研究模式 (trader/fund-manager/researcher/advisor)')
  .action(async (topic, options) => {
    try {
      // 检查用户状态
      const status = await userState.checkVersion();
      if (status === 'first_time') {
        showWelcome();
        await userState.markInitialized();
      } else if (status === 'updated') {
        showUpdateNotice();
      }
      
      // 检查 API Key
      const apiKey = await getApiKey('CUECUE_API_KEY');
      if (!apiKey) {
        console.log(chalk.yellow('\n⚠️  需要配置 API Key'));
        console.log('使用 /key 命令或直接发送 API Key 进行配置\n');
        return;
      }
      
      // 自动检测模式
      let mode = options.mode || autoDetectMode(topic);
      const modeNames = {
        trader: '短线交易视角',
        'fund-manager': '基金经理视角',
        researcher: '产业研究视角',
        advisor: '理财顾问视角'
      };
      
      console.log(chalk.blue(`\n🎯 根据主题自动匹配研究视角：${modeNames[mode]}\n`));
      
      // 创建任务
      const taskId = `cuecue_${Date.now()}`;
      await taskManager.createTask({
        taskId,
        topic,
        mode
      });
      
      // 启动研究
      const spinner = ora('启动研究中...').start();
      
      try {
        const result = await startResearch({
          topic,
          mode,
          chatId,
          apiKey
        });
        
        spinner.succeed('研究已启动');
        
        console.log(chalk.green('\n✅ 研究任务已启动！\n'));
        console.log(`📋 任务信息：`);
        console.log(`   主题：${topic}`);
        console.log(`   任务 ID：${taskId}`);
        console.log(`   报告链接：${result.reportUrl}`);
        console.log(`\n⏳ 进度更新：每 5 分钟推送一次`);
        console.log(`🔔 完成通知：研究完成后自动推送\n`);
        
      } catch (error) {
        spinner.fail('研究启动失败');
        logger.error('Research failed', error);
        console.log(chalk.red(`\n❌ 错误：${error.message}\n`));
      }
      
    } catch (error) {
      logger.error('Command failed', error);
      console.log(chalk.red(`\n❌ 错误：${error.message}\n`));
    }
  });

// /ct 命令 - 查看任务列表
program
  .command('ct')
  .description('查看任务列表')
  .action(async () => {
    const tasks = await taskManager.getTasks(10);
    
    if (tasks.length === 0) {
      console.log('📭 暂无研究任务');
      return;
    }
    
    console.log('📊 研究任务列表\n');
    
    for (const task of tasks) {
      const statusEmoji = {
        running: '🔄',
        completed: '✅',
        failed: '❌',
        timeout: '⏱️'
      }[task.status] || '🔄';
      
      console.log(`${statusEmoji} ${task.topic}`);
      console.log(`   ID: ${task.task_id} | 状态：${task.status}\n`);
    }
  });

// /cm 命令 - 查看监控列表
program
  .command('cm')
  .description('查看监控列表')
  .action(async () => {
    const monitors = await monitorManager.getMonitors(15);
    
    if (monitors.length === 0) {
      console.log('📭 暂无监控项');
      console.log('💡 研究完成后回复 Y 可创建监控项\n');
      return;
    }
    
    console.log('🔔 监控项列表\n');
    
    for (const monitor of monitors) {
      const statusEmoji = monitor.is_active !== false ? '✅' : '⏸️';
      const catEmoji = {
        Price: '💰',
        Event: '📅',
        Data: '📊'
      }[monitor.category] || '📊';
      
      console.log(`${statusEmoji} ${catEmoji} ${monitor.title}`);
      if (monitor.symbol) {
        console.log(`   标的：${monitor.symbol}`);
      }
      console.log(`   触发：${monitor.semantic_trigger?.slice(0, 30) || '-'}\n`);
    }
  });

// /ch 命令 - 显示帮助
program
  .command('help')
  .alias('ch')
  .description('显示帮助')
  .action(() => {
    console.log(chalk.cyan(`
╔══════════════════════════════════════════╗
║         Cue - 你的专属调研助理          ║
╠══════════════════════════════════════════╣
║  使用方式：                              ║
║  • cue <主题>         开始深度研究       ║
║  • cue --mode <模式>  指定视角           ║
║  • ct                 查看任务列表       ║
║  • cm                 查看监控项列表     ║
║  • cn [天数]          查看监控通知       ║
║  • key                配置 API Key       ║
║  • help               显示帮助           ║
║                                          ║
║  研究视角模式：                          ║
║  • trader       - 短线交易视角           ║
║  • fund-manager - 基金经理视角           ║
║  • researcher   - 产业研究视角           ║
║  • advisor      - 理财顾问视角           ║
╚══════════════════════════════════════════╝
`));
  });

// /cn 命令 - 查看监控通知
program
  .command('cn [days]')
  .description('查看监控触发通知')
  .action(async (days = '3') => {
    const numDays = parseInt(days, 10) || 3;
    console.log(chalk.blue(`\n🔔 监控触发通知（最近${numDays}日）\n`));
    
    // TODO: 实现通知查询
    console.log('📭 暂无触发通知\n');
    console.log('💡 当监控条件满足时，会自动发送通知到这里\n');
  });

// /key 命令 - API Key 配置
program
  .command('key [apiKey]')
  .description('配置或查看 API Key')
  .action(async (apiKey) => {
    if (!apiKey) {
      // 查看状态
      const status = await getApiKeyStatus();
      
      console.log('╔══════════════════════════════════════════╗');
      console.log('║           当前 API Key 配置状态           ║');
      console.log('╠══════════════════════════════════════════╣');
      
      for (const s of status) {
        if (s.configured) {
          console.log(`║  ✅ ${s.name.padEnd(18)} ${s.masked.padEnd(24)} ║`);
        } else {
          console.log(`║  ❌ ${s.name.padEnd(18)} 未配置                        ║`);
        }
      }
      
      console.log('╠══════════════════════════════════════════╣');
      console.log('║  直接发送 API Key 即可自动配置            ║');
      console.log('╚══════════════════════════════════════════╝\n');
      return;
    }
    
    // 配置 API Key
    const service = detectServiceFromKey(apiKey);
    
    if (!service) {
      console.log(chalk.red('\n❌ 无法识别 API Key 类型\n'));
      console.log('支持的格式：');
      console.log('  • Tavily:  tvly-xxxxx');
      console.log('  • CueCue:  skb-xxxxx 或 sk-xxxxx');
      console.log('  • QVeris:  sk-xxxxx (长格式)\n');
      return;
    }
    
    await setApiKey(service.key, apiKey);
    
    console.log(chalk.green(`\n✅ ${service.name} API Key 配置成功！\n`));
    console.log(`密钥已保存并生效，无需重启。\n`);
  });

// 显示欢迎消息
function showWelcome() {
  console.log(chalk.cyan('\n╔══════════════════════════════════════════╗'));
  console.log('║  🎉 欢迎使用 Cue - 你的专属调研助理     ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log('║                                          ║');
  console.log('║  ⚠️  安全提示：                          ║');
  console.log('║  • 本工具会创建 ~/.cuecue 本地存储       ║');
  console.log('║  • 会安装 cron 定时任务（每 30 分钟）        ║');
  console.log('║  • 需要外部 API 访问权限                   ║');
  console.log('║                                          ║');
  console.log('║  快速开始：                              ║');
  console.log('║  • /cue <主题>  开始深度研究             ║');
  console.log('║  • /key         配置 API Key             ║');
  console.log('║  • /ch          查看帮助                 ║');
  console.log('║                                          ║');
  console.log('╚══════════════════════════════════════════╝\n');
}

// 显示更新提示
function showUpdateNotice() {
  console.log(chalk.cyan('\n╔══════════════════════════════════════════╗'));
  console.log('║  ✨ Cue 已更新至 v1.0.4 (Node.js 版)        ║');
  console.log('╠══════════════════════════════════════════╣');
  console.log('║                                          ║');
  console.log('║  本次更新内容：                          ║');
  console.log('║  🔧 全面 Node.js 重构                     ║');
  console.log('║  🔧 自动角色匹配                         ║');
  console.log('║  🔧 /cn 监控通知查询                     ║');
  console.log('║  🔧 /key API Key 配置                    ║');
  console.log('║                                          ║');
  console.log('╚══════════════════════════════════════════╝\n');
}

// 解析命令行
program.parse(process.argv);

#!/usr/bin/env node

/**
 * 机器人消息 CLI 脚本
 * Usage: node robot.js <command> [options]
 */

const { Command } = require('commander');
const MessageClient = require('./message');
require('dotenv').config();

const program = new Command();
const client = new MessageClient({ debug: process.env.DINGTALK_DEBUG === 'true' });

program
  .name('robot')
  .description('钉钉群机器人消息发送工具')
  .version('1.0.0');

// 发送机器人消息
program
  .command('send')
  .description('发送机器人消息到群聊')
  .option('-w, --webhook <url>', 'Webhook 地址 (必填)')
  .option('-s, --secret <secret>', '加签密钥 (可选)')
  .option('-t, --content <text>', '消息内容 (必填)')
  .option('-T, --title <text>', 'Markdown 标题')
  .option('-m, --type <type>', '消息类型: text/markdown', 'text')
  .option('--at-all', '@所有人')
  .option('--at <users>', '@指定用户(逗号分隔)')
  .action(async (options) => {
    try {
      if (!options.webhook) {
        console.error('❌ 错误: 必须指定 --webhook');
        process.exit(1);
      }
      if (!options.content) {
        console.error('❌ 错误: 必须指定 --content');
        process.exit(1);
      }

      // 构建消息内容
      let content = options.content;
      
      if (options.type === 'markdown') {
        // Markdown 消息
        const title = options.title || '通知';
        content = `### ${title}\n\n${content}`;
        
        if (options.atAll) {
          content += '\n\n@所有人';
        }
      } else {
        // 文本消息
        if (options.atAll) {
          content = `${content}\n\n@所有人`;
        }
        if (options.at) {
          const atUsers = options.at.split(',').map(u => `@${u.trim()}`).join(' ');
          content = `${content}\n\n${atUsers}`;
        }
      }

      const result = await client.sendRobot(options.webhook, options.secret, content, options.type);
      console.log('✅ 机器人消息发送成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 发送失败:', error.message);
      process.exit(1);
    }
  });

// 发送模板消息
program
  .command('send-template')
  .description('使用模板发送消息')
  .option('-w, --webhook <url>', 'Webhook 地址 (必填)')
  .option('-s, --secret <secret>', '加签密钥 (可选)')
  .option('-T, --template <name>', '模板名称: daily/alert/meeting', 'daily')
  .option('-d, --data <json>', '模板数据 (JSON格式)', '{}')
  .action(async (options) => {
    try {
      if (!options.webhook) {
        console.error('❌ 错误: 必须指定 --webhook');
        process.exit(1);
      }

      let data = {};
      try {
        data = JSON.parse(options.data);
      } catch {
        console.error('❌ 错误: --data 必须是有效的 JSON 格式');
        process.exit(1);
      }

      // 定义模板
      const templates = {
        daily: {
          title: '📋 每日日报提醒',
          content: `**时间**: ${data.date || new Date().toLocaleDateString('zh-CN')}\n\n**提醒**: 请记得提交今日工作日报！\n\n${data.content || ''}`
        },
        alert: {
          title: '🚨 系统告警',
          content: `**告警级别**: ${data.level || '警告'}\n\n**告警内容**: ${data.message || '系统检测到异常'}\n\n**时间**: ${new Date().toLocaleString('zh-CN')}`
        },
        meeting: {
          title: '📅 会议提醒',
          content: `**会议**: ${data.title || '周例会'}\n\n**时间**: ${data.time || '待定'}\n\n**地点**: ${data.location || '线上'}\n\n请准时参加！`
        }
      };

      const template = templates[options.template];
      if (!template) {
        console.error(`❌ 错误: 未知模板 "${options.template}"`);
        console.log('可用模板:', Object.keys(templates).join(', '));
        process.exit(1);
      }

      const fullContent = `### ${template.title}\n\n${template.content}`;
      const result = await client.sendRobot(options.webhook, options.secret, fullContent, 'markdown');
      console.log('✅ 模板消息发送成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 发送失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
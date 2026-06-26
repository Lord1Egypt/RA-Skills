#!/usr/bin/env node

/**
 * 消息发送 CLI 脚本
 * Usage: node message.js <command> [options]
 */

const { Command } = require('commander');
const MessageClient = require('./message');
require('dotenv').config();

const program = new Command();
const client = new MessageClient({ debug: process.env.DINGTALK_DEBUG === 'true' });

program
  .name('message')
  .description('钉钉消息发送工具')
  .version('1.0.0');

// 发送文本消息
program
  .command('send-text')
  .description('发送文本消息')
  .option('-u, --user-id <id>', '接收用户ID')
  .option('-c, --chat-id <id>', '接收群聊ID')
  .option('-t, --content <text>', '消息内容')
  .option('--debug', '开启调试模式')
  .action(async (options) => {
    try {
      if (!options.userId && !options.chatId) {
        console.error('错误: 必须指定 --user-id 或 --chat-id');
        process.exit(1);
      }
      if (!options.content) {
        console.error('错误: 必须指定 --content');
        process.exit(1);
      }

      const result = await client.sendText(options.userId, options.chatId, options.content);
      console.log('✅ 消息发送成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 发送失败:', error.message);
      process.exit(1);
    }
  });

// 发送 Markdown 消息
program
  .command('send-md')
  .description('发送 Markdown 消息')
  .option('-u, --user-id <id>', '接收用户ID')
  .option('-c, --chat-id <id>', '接收群聊ID')
  .option('-T, --title <text>', '消息标题')
  .option('-t, --content <text>', 'Markdown 内容')
  .option('--debug', '开启调试模式')
  .action(async (options) => {
    try {
      if (!options.userId && !options.chatId) {
        console.error('错误: 必须指定 --user-id 或 --chat-id');
        process.exit(1);
      }
      if (!options.content) {
        console.error('错误: 必须指定 --content');
        process.exit(1);
      }

      const result = await client.sendMarkdown(options.userId, options.chatId, options.title, options.content);
      console.log('✅ Markdown 消息发送成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 发送失败:', error.message);
      process.exit(1);
    }
  });

// 发送机器人消息
program
  .command('send-robot')
  .description('发送群机器人消息')
  .option('-w, --webhook <url>', 'Webhook 地址')
  .option('-s, --secret <secret>', '加签密钥')
  .option('-t, --content <text>', '消息内容')
  .option('-m, --type <type>', '消息类型 (text/markdown)', 'text')
  .action(async (options) => {
    try {
      if (!options.webhook || !options.content) {
        console.error('错误: 必须指定 --webhook 和 --content');
        process.exit(1);
      }

      const result = await client.sendRobot(options.webhook, options.secret, options.content, options.type);
      console.log('✅ 机器人消息发送成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 发送失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
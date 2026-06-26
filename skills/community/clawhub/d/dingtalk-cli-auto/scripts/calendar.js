#!/usr/bin/env node

/**
 * 日程管理 CLI 脚本
 * Usage: node calendar.js <command> [options]
 */

const { Command } = require('commander');
const CalendarClient = require('./calendar');
require('dotenv').config();

const program = new Command();
const client = new CalendarClient({ debug: process.env.DINGTALK_DEBUG === 'true' });

program
  .name('calendar')
  .description('钉钉日程管理工具')
  .version('1.0.0');

// 创建日程
program
  .command('create')
  .description('创建日程')
  .option('-t, --title <text>', '日程标题')
  .option('-s, --start <time>', '开始时间 (ISO 8601 或 today/tomorrow/+Nd)')
  .option('-e, --end <time>', '结束时间')
  .option('-d, --duration <minutes>', '持续时间(分钟)', '60')
  .option('-a, --attendees <users>', '参会人(逗号分隔)')
  .option('-l, --location <text>', '地点')
  .option('-D, --description <text>', '描述')
  .action(async (options) => {
    try {
      if (!options.title) {
        console.error('错误: 必须指定 --title');
        process.exit(1);
      }
      if (!options.start) {
        console.error('错误: 必须指定 --start');
        process.exit(1);
      }

      const params = {
        title: options.title,
        start: options.start,
        end: options.end,
        duration: options.duration ? parseInt(options.duration) : 60,
        attendees: options.attendees,
        location: options.location,
        description: options.description
      };

      const result = await client.create(params);
      console.log('✅ 日程创建成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 创建失败:', error.message);
      process.exit(1);
    }
  });

// 查询日程列表
program
  .command('list')
  .description('查询日程列表')
  .option('-t, --today', '查询今天')
  .option('-w, --week', '查询本周')
  .option('-s, --start <date>', '开始日期 (YYYY-MM-DD)')
  .option('-e, --end <date>', '结束日期 (YYYY-MM-DD)')
  .action(async (options) => {
    try {
      const params = {};
      if (options.today) params.today = true;
      else if (options.week) params.week = true;
      else if (options.start) {
        params.start = options.start;
        if (options.end) params.end = options.end;
      }

      const result = await client.list(params);
      
      if (Array.isArray(result) && result.length > 0) {
        console.log(`📅 找到 ${result.length} 个日程:\n`);
        result.forEach((event, i) => {
          console.log(`${i + 1}. ${event.title}`);
          console.log(`   时间: ${event.start} - ${event.end}`);
          if (event.location) console.log(`   地点: ${event.location}`);
          if (event.attendees && event.attendees.length > 0) {
            console.log(`   参会人: ${event.attendees.join(', ')}`);
          }
          console.log('');
        });
      } else {
        console.log('📅 没有找到日程');
      }
    } catch (error) {
      console.error('❌ 查询失败:', error.message);
      process.exit(1);
    }
  });

// 查询空闲时间
program
  .command('free-busy')
  .description('查询用户空闲时间')
  .option('-u, --users <users>', '用户ID(逗号分隔)')
  .option('-s, --start <time>', '开始时间')
  .option('-e, --end <time>', '结束时间')
  .action(async (options) => {
    try {
      if (!options.users || !options.start || !options.end) {
        console.error('错误: 必须指定 --users, --start, --end');
        process.exit(1);
      }

      const result = await client.checkFreeBusy(options.users, options.start, options.end);
      console.log('✅ 查询成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 查询失败:', error.message);
      process.exit(1);
    }
  });

// 更新日程
program
  .command('update')
  .description('更新日程')
  .option('-i, --id <id>', '日程ID')
  .option('-t, --title <text>', '新标题')
  .option('-s, --start <time>', '新开始时间')
  .option('-e, --end <time>', '新结束时间')
  .option('-l, --location <text>', '新地点')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const updates = {};
      if (options.title) updates.title = options.title;
      if (options.start) updates.start = options.start;
      if (options.end) updates.end = options.end;
      if (options.location) updates.location = options.location;

      const result = await client.update(options.id, updates);
      console.log('✅ 日程更新成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 更新失败:', error.message);
      process.exit(1);
    }
  });

// 删除日程
program
  .command('delete')
  .description('删除日程')
  .option('-i, --id <id>', '日程ID')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const result = await client.delete(options.id);
      console.log('✅ 日程删除成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 删除失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
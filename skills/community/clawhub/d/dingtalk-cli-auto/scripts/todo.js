#!/usr/bin/env node

/**
 * 待办事项管理 CLI 脚本
 * Usage: node todo.js <command> [options]
 */

const { Command } = require('commander');
const TodoClient = require('./todo');
require('dotenv').config();

const program = new Command();
const client = new TodoClient({ debug: process.env.DINGTALK_DEBUG === 'true' });

program
  .name('todo')
  .description('钉钉待办事项管理工具')
  .version('1.0.0');

// 创建待办
program
  .command('create')
  .description('创建待办事项')
  .option('-c, --content <text>', '待办内容')
  .option('-d, --due <time>', '截止时间 (ISO 8601 或 today/tomorrow/+Nd)')
  .option('-a, --assignees <users>', '负责人(逗号分隔)')
  .option('-p, --priority <level>', '优先级 (low/medium/high)', 'medium')
  .action(async (options) => {
    try {
      if (!options.content) {
        console.error('错误: 必须指定 --content');
        process.exit(1);
      }

      const params = {
        content: options.content,
        due: options.due,
        assignees: options.assignees,
        priority: options.priority
      };

      const result = await client.create(params);
      console.log('✅ 待办创建成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 创建失败:', error.message);
      process.exit(1);
    }
  });

// 查询待办列表
program
  .command('list')
  .description('查询待办列表')
  .option('-a, --all', '查询所有待办 (默认只查询未完成的)')
  .option('-t, --today', '查询今天到期的待办')
  .option('-w, --due-within <days>', '查询 N 天内到期的待办')
  .option('--assignee <user>', '按负责人筛选')
  .action(async (options) => {
    try {
      const params = {};
      if (options.all) params.all = true;
      if (options.today) params.today = true;
      if (options.dueWithin) params.dueWithin = parseInt(options.dueWithin);
      if (options.assignee) params.assignee = options.assignee;

      const result = await client.list(params);
      
      if (Array.isArray(result) && result.length > 0) {
        const pending = result.filter(t => t.status !== 'completed');
        const completed = result.filter(t => t.status === 'completed');
        
        console.log(`✅ 找到 ${result.length} 个待办:\n`);
        
        if (pending.length > 0) {
          console.log(`📋 待完成 (${pending.length}):\n`);
          pending.forEach((todo, i) => {
            const priorityEmoji = {
              high: '🔴',
              medium: '🟡',
              low: '🟢'
            }[todo.priority] || '⚪';
            
            console.log(`${i + 1}. ${priorityEmoji} ${todo.content}`);
            if (todo.due) console.log(`   ⏰ 截止: ${todo.due}`);
            if (todo.assignee) console.log(`   👤 负责人: ${todo.assignee}`);
            console.log(`   🆔 ID: ${todo.id}`);
            console.log('');
          });
        }
        
        if (completed.length > 0) {
          console.log(`✓ 已完成 (${completed.length}):`);
          completed.forEach((todo, i) => {
            console.log(`   ✓ ${todo.content}`);
          });
        }
      } else {
        console.log('📋 没有找到待办事项');
      }
    } catch (error) {
      console.error('❌ 查询失败:', error.message);
      process.exit(1);
    }
  });

// 完成待办
program
  .command('complete')
  .description('完成待办事项')
  .option('-i, --id <id>', '待办ID')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const result = await client.complete(options.id);
      console.log('✅ 待办已完成');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 操作失败:', error.message);
      process.exit(1);
    }
  });

// 删除待办
program
  .command('delete')
  .description('删除待办事项')
  .option('-i, --id <id>', '待办ID')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const result = await client.delete(options.id);
      console.log('✅ 待办已删除');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 删除失败:', error.message);
      process.exit(1);
    }
  });

// 更新待办
program
  .command('update')
  .description('更新待办事项')
  .option('-i, --id <id>', '待办ID')
  .option('-c, --content <text>', '新内容')
  .option('-d, --due <time>', '新截止时间')
  .option('-a, --assignees <users>', '新负责人')
  .option('-p, --priority <level>', '新优先级 (low/medium/high)')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const updates = {};
      if (options.content) updates.content = options.content;
      if (options.due) updates.due = options.due;
      if (options.assignees) updates.assignees = options.assignees;
      if (options.priority) updates.priority = options.priority;

      const result = await client.update(options.id, updates);
      console.log('✅ 待办更新成功');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 更新失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
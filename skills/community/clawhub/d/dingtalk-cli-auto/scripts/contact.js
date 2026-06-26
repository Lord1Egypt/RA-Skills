#!/usr/bin/env node

/**
 * 通讯录管理 CLI 脚本
 * Usage: node contact.js <command> [options]
 */

const { Command } = require('commander');
const ContactClient = require('./contact');
require('dotenv').config();

const program = new Command();
const client = new ContactClient({ debug: process.env.DINGTALK_DEBUG === 'true' });

program
  .name('contact')
  .description('钉钉通讯录管理工具')
  .version('1.0.0');

// 搜索联系人
program
  .command('search')
  .description('搜索联系人')
  .option('-n, --name <name>', '按姓名搜索')
  .option('-d, --dept <dept>', '按部门搜索')
  .option('-k, --keyword <keyword>', '通用关键词搜索')
  .action(async (options) => {
    try {
      if (!options.name && !options.dept && !options.keyword) {
        console.error('错误: 必须指定 --name, --dept 或 --keyword');
        process.exit(1);
      }

      const params = {};
      if (options.name) params.name = options.name;
      else if (options.dept) params.dept = options.dept;
      else if (options.keyword) params.keyword = options.keyword;

      const result = await client.search(params);
      
      if (Array.isArray(result) && result.length > 0) {
        console.log(`👥 找到 ${result.length} 个联系人:\n`);
        result.forEach((contact, i) => {
          console.log(`${i + 1}. ${contact.name} (${contact.id})`);
          if (contact.title) console.log(`   职位: ${contact.title}`);
          if (contact.dept) console.log(`   部门: ${contact.dept}`);
          if (contact.phone) console.log(`   手机: ${contact.phone}`);
          if (contact.email) console.log(`   邮箱: ${contact.email}`);
          console.log('');
        });
      } else {
        console.log('👥 没有找到联系人');
      }
    } catch (error) {
      console.error('❌ 搜索失败:', error.message);
      process.exit(1);
    }
  });

// 获取部门成员
program
  .command('dept-members')
  .description('获取部门成员列表')
  .option('-i, --dept-id <id>', '部门ID')
  .option('-s, --include-sub', '包含子部门')
  .action(async (options) => {
    try {
      if (!options.deptId) {
        console.error('错误: 必须指定 --dept-id');
        process.exit(1);
      }

      const result = await client.getDeptMembers(options.deptId, options.includeSub);
      
      if (Array.isArray(result) && result.length > 0) {
        console.log(`👥 找到 ${result.length} 个成员:\n`);
        result.forEach((member, i) => {
          const leaderBadge = member.leader ? ' ⭐' : '';
          console.log(`${i + 1}. ${member.name}${leaderBadge}`);
          if (member.title) console.log(`   职位: ${member.title}`);
          if (member.phone) console.log(`   手机: ${member.phone}`);
          console.log('');
        });
      } else {
        console.log('👥 部门中没有成员');
      }
    } catch (error) {
      console.error('❌ 获取失败:', error.message);
      process.exit(1);
    }
  });

// 获取部门列表
program
  .command('list-depts')
  .description('获取部门列表')
  .action(async () => {
    try {
      const result = await client.listDepartments();
      
      if (Array.isArray(result) && result.length > 0) {
        console.log(`🏢 找到 ${result.length} 个部门:\n`);
        result.forEach((dept, i) => {
          console.log(`${i + 1}. ${dept.name} (ID: ${dept.id})`);
          if (dept.memberCount) console.log(`   成员数: ${dept.memberCount}`);
          console.log('');
        });
      } else {
        console.log('🏢 没有找到部门');
      }
    } catch (error) {
      console.error('❌ 获取失败:', error.message);
      process.exit(1);
    }
  });

// 获取用户详情
program
  .command('user-detail')
  .description('获取用户详情')
  .option('-i, --id <id>', '用户ID')
  .action(async (options) => {
    try {
      if (!options.id) {
        console.error('错误: 必须指定 --id');
        process.exit(1);
      }

      const result = await client.getUserDetail(options.id);
      console.log('👤 用户详情:');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 获取失败:', error.message);
      process.exit(1);
    }
  });

// 获取当前用户
program
  .command('me')
  .description('获取当前登录用户信息')
  .action(async () => {
    try {
      const result = await client.getCurrentUser();
      console.log('👤 当前用户:');
      console.log(JSON.stringify(result, null, 2));
    } catch (error) {
      console.error('❌ 获取失败:', error.message);
      process.exit(1);
    }
  });

program.parse();
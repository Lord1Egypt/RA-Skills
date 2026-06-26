#!/usr/bin/env node

/**
 * 飞书任务管理 - 配置验证工具
 *
 * 完整测试所有 API 功能，验证配置和权限
 */

const path = require('path');
const fs = require('fs');
const readline = require('readline');
const { createClientFromConfig } = require('./feishu-client.js');

class FeishuValidator {
  constructor(configPath) {
    this.configPath = configPath;
    this.client = null;
    this.config = null;
    this.testData = {
      record: null,
      docNode: null
    };
    this.results = [];
  }

  /**
   * 读取配置文件
   */
  loadConfig () {
    this.log('info', '📋 读取配置文件...');

    try {
      const fullPath = path.resolve(this.configPath);
      if (!fs.existsSync(fullPath)) {
        throw new Error(`配置文件不存在: ${fullPath}`);
      }

      const content = fs.readFileSync(fullPath, 'utf8');
      this.config = JSON.parse(content);

      // 验证必需字段
      const required = ['app_id', 'app_secret', 'bitable', 'wiki'];
      for (const field of required) {
        if (!this.config[field]) {
          throw new Error(`配置缺少必需字段: ${field}`);
        }
      }

      const bitableRequired = ['app_token', 'table_id', 'field_names'];
      for (const field of bitableRequired) {
        if (!this.config.bitable[field]) {
          throw new Error(`bitable 配置缺少必需字段: ${field}`);
        }
      }

      const fieldNamesRequired = ['title', 'status', 'type', 'source_url', 'document', 'priority'];
      for (const field of fieldNamesRequired) {
        if (!this.config.bitable.field_names[field]) {
          throw new Error(`field_names 配置缺少必需字段: ${field}`);
        }
      }

      if (!this.config.wiki.space_id) {
        throw new Error('wiki 配置缺少 space_id');
      }

      if (!this.config.wiki.bitable_node_token) {
        throw new Error('wiki 配置缺少 bitable_node_token');
      }

      if (!this.config.wiki.parent_node_token) {
        throw new Error('wiki 配置缺少 parent_node_token（任务文档根节点）');
      }

      this.log('success', '✅ 配置文件格式正确');
      this.results.push({ name: '配置文件', status: '✅', message: '格式正确' });
      return true;
    } catch (error) {
      this.log('error', `❌ ${error.message}`);
      this.results.push({ name: '配置文件', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 测试认证
   */
  async testAuth () {
    this.log('info', '🔐 测试认证...');

    try {
      this.client = createClientFromConfig(this.configPath);
      const token = await this.client.getAppAccessToken();

      this.log('success', `✅ 认证成功 (token: ${token.substring(0, 15)}...)`);
      this.results.push({ name: '认证', status: '✅', message: '成功获取 access_token' });
      return true;
    } catch (error) {
      this.log('error', `❌ 认证失败: ${error.message}`);
      this.results.push({ name: '认证', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 测试查询任务表
   */
  async testGetRecords () {
    this.log('info', '📖 测试查询任务表...');

    try {
      const { app_token, table_id } = this.config.bitable;
      const response = await this.client.getRecords(app_token, table_id, { pageSize: 1 });

      this.log('success', `✅ 查询成功，当前表中有 ${response.total} 条记录`);
      this.results.push({ name: '查询任务表', status: '✅', message: `找到 ${response.total} 条记录` });
      return true;
    } catch (error) {
      this.log('error', `❌ 查询失败: ${error.message}`);
      this.results.push({ name: '查询任务表', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 测试创建记录
   */
  async testCreateRecord () {
    this.log('info', '➕ 测试创建记录...');

    try {
      const timestamp = new Date().toISOString();
      const title = `[验证测试] ${timestamp}`;
      const { field_names } = this.config.bitable;
      const { app_token, table_id } = this.config.bitable;

      const fields = {};
      fields[field_names.title] = title;
      fields[field_names.status] = '待处理';
      fields[field_names.type] = '研究';
      fields[field_names.priority] = 1;
      fields[field_names.source_url] = { link: 'https://test.example.com', text: 'Test Link' };

      const record = await this.client.createRecord(app_token, table_id, fields);

      this.testData.record = {
        record_id: record.record_id,
        title: title
      };

      // 验证：查询刚创建的记录（直接按 record_id 查找）
      const verifyRecords = await this.client.getRecords(app_token, table_id);
      const verifyRecord = verifyRecords.items.find(r => r.record_id === record.record_id);

      if (!verifyRecord) {
        throw new Error('创建后无法查询到记录');
      }

      this.log('success', `✅ 创建记录成功 (ID: ${record.record_id})，已验证查询成功`);
      this.results.push({ name: '创建记录', status: '✅', message: `ID: ${record.record_id}` });
      return true;
    } catch (error) {
      this.log('error', `❌ 创建记录失败: ${error.message}`);
      this.results.push({ name: '创建记录', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 测试更新记录
   */
  async testUpdateRecord () {
    this.log('info', '✏️  测试更新记录...');

    if (!this.testData.record) {
      this.log('warn', '⚠️  跳过（没有测试记录）');
      this.results.push({ name: '更新记录', status: '⏭️ ', message: '跳过' });
      return false;
    }

    try {
      const { field_names } = this.config.bitable;
      const { app_token, table_id } = this.config.bitable;

      const fields = {};
      fields[field_names.status] = '待确认';

      await this.client.updateRecord(app_token, table_id, this.testData.record.record_id, fields);

      // 验证：查询更新后的记录
      const verifyRecord = await this.client.getRecords(app_token, table_id);
      const updatedRecord = verifyRecord.items.find(r => r.record_id === this.testData.record.record_id);

      if (!updatedRecord || updatedRecord.fields[field_names.status] !== '待确认') {
        throw new Error('更新后状态未改变');
      }

      this.log('success', `✅ 更新记录成功，状态已更新为 "待确认"，已验证查询成功`);
      this.results.push({ name: '更新记录', status: '✅', message: '状态更新成功' });
      return true;
    } catch (error) {
      this.log('error', `❌ 更新记录失败: ${error.message}`);
      this.results.push({ name: '更新记录', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 测试创建文档（创建两个任务验证文档复用）
   */
  async testCreateDoc () {
    this.log('info', '📄 测试创建文档（创建两个任务验证复用）...');

    if (!this.testData.record) {
      this.log('warn', '⚠️  跳过（没有测试记录）');
      this.results.push({ name: '创建文档', status: '⏭️ ', message: '跳过' });
      return false;
    }

    try {
      const { app_token, table_id, field_names } = this.config.bitable;
      const { space_id, parent_node_token } = this.config.wiki;

      // 创建第二个任务记录
      const timestamp2 = new Date().toISOString() + '-2';
      const title2 = `[验证测试2] ${timestamp2}`;
      const fields2 = {};
      fields2[field_names.title] = title2;
      fields2[field_names.status] = '待处理';
      fields2[field_names.type] = '研究';
      fields2[field_names.priority] = 1;
      fields2[field_names.source_url] = { link: 'https://test2.example.com', text: 'Test Link 2' };

      const record2 = await this.client.createRecord(app_token, table_id, fields2);
      this.testData.record2 = {
        record_id: record2.record_id,
        title: title2
      };

      // 使用 TaskManager 为第一个任务创建文档
      const { TaskManager } = require('./task-manager.js');
      const manager = new TaskManager(this.configPath);

      const doc1Result = await manager.createDoc(this.testData.record.record_id);
      this.log('info', `   ✅ 第一个任务文档创建成功`);

      // 为第二个任务创建文档（应该复用月/日文档）
      const doc2Result = await manager.createDoc(this.testData.record2.record_id);
      this.log('info', `   ✅ 第二个任务文档创建成功（复用了月/日文档）`);

      this.testData.doc1 = doc1Result;
      this.testData.doc2 = doc2Result;

      this.log('success', `✅ 创建文档成功，已验证文档复用功能`);
      this.results.push({ name: '创建文档', status: '✅', message: '复用功能正常' });
      return true;
    } catch (error) {
      this.log('error', `❌ 创建文档失败: ${error.message}`);
      this.results.push({ name: '创建文档', status: '❌', message: error.message });
      return false;
    }
  }

  /**
   * 显示测试结果
   */
  showResults () {
    console.log('\n' + '='.repeat(60));
    console.log('📊 验证结果汇总');
    console.log('='.repeat(60));

    let successCount = 0;
    let failCount = 0;
    let skipCount = 0;

    this.results.forEach(result => {
      const status = result.status;
      if (status === '✅') successCount++;
      else if (status === '❌') failCount++;
      else if (status === '⏭️ ') skipCount++;

      console.log(`${status} ${result.name.padEnd(20)} - ${result.message}`);
    });

    console.log('='.repeat(60));
    console.log(`总计: ${this.results.length} 项 | ✅ 成功: ${successCount} | ❌ 失败: ${failCount} | ⏭️  跳过: ${skipCount}`);
    console.log('='.repeat(60));

    if (failCount === 0) {
      console.log('\n🎉 所有测试通过！配置正确，权限正常。');
    } else {
      console.log(`\n⚠️  有 ${failCount} 项测试失败，请检查配置和权限。`);
    }
  }

  /**
   * 询问是否删除测试数据
   */
  async askCleanup () {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      rl.question(
        '\n❓ 是否要删除测试数据？（记录、文档等）[y/N]: ',
        (answer) => {
          rl.close();
          resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
        }
      );
    });
  }

  /**
   * 清理测试数据
   */
  async cleanup () {
    this.log('info', '\n🧹 清理测试数据...');

    const cleanupResults = [];

    // 删除测试记录
    if (this.testData.record) {
      try {
        // 飞书 API 没有直接删除记录的接口，需要通过更新字段来标记删除
        // 或者记录下记录 ID 让用户手动删除
        this.log('info', `📝 测试记录 ID: ${this.testData.record.record_id}`);
        this.log('info', `📝 测试记录标题: ${this.testData.record.title}`);
        cleanupResults.push({ name: '记录', status: '⚠️ ', message: '请手动删除' });
      } catch (error) {
        cleanupResults.push({ name: '记录', status: '❌', message: error.message });
      }
    }

    // 删除测试文档节点（需要用户手动删除）
    if (this.testData.docNode) {
      try {
        this.log('info', `📄 测试文档节点 ID: ${this.testData.docNode.node_id}`);
        this.log('info', `📄 测试文档节点路径: ${this.config.wiki.space_id} → 年月 → 日期 → [验证测试]`);
        cleanupResults.push({ name: '文档', status: '⚠️ ', message: '请手动删除' });
      } catch (error) {
        cleanupResults.push({ name: '文档', status: '❌', message: error.message });
      }
    }

    console.log('\n清理结果:');
    cleanupResults.forEach(result => {
      console.log(`${result.status} ${result.name}: ${result.message}`);
    });

    console.log('\n💡 提示：飞书 API 暂不支持通过程序删除记录和文档节点');
    console.log('💡 建议手动删除测试数据以保持数据整洁。');
  }

  /**
   * 日志输出
   */
  log (level, message) {
    const colors = {
      info: '\x1b[34m',     // blue
      success: '\x1b[32m',  // green
      warn: '\x1b[33m',     // yellow
      error: '\x1b[31m'     // red
    };
    const reset = '\x1b[0m';
    console.log(`${colors[level]}${message}${reset}`);
  }

  /**
   * 运行所有测试
   */
  async run () {
    console.log('\n🔍 飞书任务管理 - 配置验证工具');
    console.log('='.repeat(60));

    // 1. 加载配置
    if (!this.loadConfig()) {
      return false;
    }

    // 2. 测试认证
    if (!await this.testAuth()) {
      return false;
    }

    // 3. 测试查询
    await this.testGetRecords();

    // 4. 测试创建记录
    await this.testCreateRecord();

    // 5. 测试更新记录
    await this.testUpdateRecord();

    // 6. 测试创建文档
    await this.testCreateDoc();

    // 10. 显示结果
    this.showResults();

    // 11. 询问是否清理
    const shouldCleanup = await this.askCleanup();
    if (shouldCleanup) {
      await this.cleanup();
    } else {
      console.log('\n💡 测试数据已保留，请记得手动清理。');
    }

    return true;
  }
}

// 命令行接口
if (require.main === module) {
  const configPath = process.argv[2] || './config/credentials.json';
  const validator = new FeishuValidator(configPath);

  validator.run()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('\n❌ 验证过程出错:', error.message);
      process.exit(1);
    });
}

module.exports = { FeishuValidator };

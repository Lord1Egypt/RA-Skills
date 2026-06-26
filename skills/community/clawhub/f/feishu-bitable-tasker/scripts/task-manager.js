#!/usr/bin/env node

/**
 * 飞书任务管理器
 *
 * 提供原子化的任务管理功能
 */

const path = require('path');
const { createClientFromConfig } = require('./feishu-client');

class TaskManager {
  constructor(configPath) {
    this.client = createClientFromConfig(configPath);
    this.config = this.loadConfig(configPath);
  }

  /**
   * 加载配置文件
   */
  loadConfig(configPath) {
    const fs = require('fs');
    const fullPath = path.resolve(configPath);
    const content = fs.readFileSync(fullPath, 'utf8');
    return JSON.parse(content);
  }

  /**
   * 格式化日期为年月和日期格式
   * @returns {object} - { yearMonth: "2026-03", date: "2026-03-21" }
   */
  getDatePath() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');

    return {
      yearMonth: `${year}-${month}`,
      date: `${year}-${month}-${day}`
    };
  }

  // ==================== 原子功能 ====================

  /**
   * 创建任务（只插入记录，不创建文档）
   * @param {string} title - 任务标题
   * @param {object} options - 可选字段 { type, status, priority, sourceUrl }
   */
  async createTask(title, options = {}) {
    try {
      console.log(`\n📝 创建任务: ${title}`);

      const { field_names } = this.config.bitable;
      const fields = {};
      fields[field_names.title] = title;

      if (options.type) {
        fields[field_names.type] = options.type;
      }
      if (options.status) {
        fields[field_names.status] = options.status;
      }
      if (options.priority) {
        fields[field_names.priority] = options.priority;
      }
      if (options.sourceUrl) {
        fields[field_names.source_url] = { link: options.sourceUrl };
      }

      // 插入 Bitable 记录
      const { app_token, table_id } = this.config.bitable;
      const record = await this.client.createRecord(app_token, table_id, fields);

      console.log(`✅ 任务创建成功！`);
      console.log(`   记录 ID: ${record.record_id}`);

      return {
        record_id: record.record_id,
        fields: record.fields
      };
    } catch (error) {
      console.error('❌ 创建任务失败:', error.message);
      throw error;
    }
  }

  /**
   * 为记录创建文档（原子功能）
   * @param {string} recordId - 记录 ID
   */
  async createDoc(recordId) {
    try {
      console.log(`\n📄 为记录创建文档: ${recordId}`);

      // 获取记录信息
      const { app_token, table_id, field_names } = this.config.bitable;
      const record = await this.client.getRecords(app_token, table_id);

      const taskRecord = record.items.find(r => r.record_id === recordId);
      if (!taskRecord) {
        throw new Error('记录不存在');
      }

      const title = taskRecord.fields[field_names.title];
      const { yearMonth, date } = this.getDatePath();
      const { space_id, parent_node_token } = this.config.wiki;

      // 格式化日期
      const yearMonthTitle = yearMonth; // 格式：YYYY-MM
      const dateTitle = date; // 格式：YYYY-MM-DD

      // 确定根节点
      const rootNodeToken = parent_node_token || null;

      // 1. 获取或创建月文档
      const monthNodes = await this.client.getWikiNodes(space_id, rootNodeToken);
      let monthNodeToken = monthNodes.items?.find(node => node.title === yearMonthTitle)?.node_token;

      if (!monthNodeToken) {
        const monthNode = await this.client.createWikiNode(space_id, rootNodeToken, yearMonthTitle, 'docx');
        monthNodeToken = monthNode.node.node_token;
        // 为月文档添加子页面列表块
        await this.client.createSubPageListBlock(monthNode.node.obj_token, monthNodeToken);
        console.log(`   ✅ 创建月文档: ${yearMonthTitle}`);
      } else {
        console.log(`   ♻️  复用月文档: ${yearMonthTitle}`);
      }

      // 2. 获取或创建日文档
      const dateNodes = await this.client.getWikiNodes(space_id, monthNodeToken);
      let dateNodeToken = dateNodes.items?.find(node => node.title === dateTitle)?.node_token;

      if (!dateNodeToken) {
        const dateNode = await this.client.createWikiNode(space_id, monthNodeToken, dateTitle, 'docx');
        dateNodeToken = dateNode.node.node_token;
        // 为日文档添加子页面列表块
        await this.client.createSubPageListBlock(dateNode.node.obj_token, dateNodeToken);
        console.log(`   ✅ 创建日文档: ${dateTitle}`);
      } else {
        console.log(`   ♻️  复用日文档: ${dateTitle}`);
      }

      // 3. 创建任务文档
      const taskNode = await this.client.createWikiNode(space_id, dateNodeToken, title, 'docx');
      const taskNodeId = taskNode.node.node_token;
      console.log(`   ✅ 创建任务文档: ${title}`);

      // 生成 Wiki 文档链接
      const wikiUrl = `https://feishu.cn/wiki/${taskNodeId}`;

      // 更新记录的文档字段
      const fields = {};
      fields[field_names.document] = { link: wikiUrl, text: '查看文档' };
      await this.client.updateRecord(app_token, table_id, recordId, fields);

      console.log(`✅ 文档创建成功！`);
      console.log(`   文档链接: ${wikiUrl}`);

      return {
        node_id: taskNodeId,
        wiki_url: wikiUrl
      };
    } catch (error) {
      console.error('❌ 创建文档失败:', error.message);
      throw error;
    }
  }

  /**
   * 按状态查询任务
   * @param {string} status - 任务状态
   * @returns {array} - 任务列表
   */
  async getTasksByStatus(status) {
    try {
      const { app_token, table_id, field_names } = this.config.bitable;
      const allRecords = await this.client.getAllRecords(app_token, table_id);

      // 过滤指定状态的任务
      const tasks = allRecords.filter(record => {
        return record.fields[field_names.status] === status;
      });

      return tasks;
    } catch (error) {
      console.error(`❌ 查询任务失败 (${status}):`, error.message);
      return [];
    }
  }

  /**
   * 获取所有任务
   * @returns {object} - 按状态分组的任务
   */
  async getAllTasks() {
    const { app_token, table_id, field_names } = this.config.bitable;
    const allRecords = await this.client.getAllRecords(app_token, table_id);

    const tasks = {};
    allRecords.forEach(record => {
      const status = record.fields[field_names.status] || '未设置';
      if (!tasks[status]) tasks[status] = [];
      tasks[status].push(record);
    });

    return tasks;
  }

  /**
   * 更新任务状态
   * @param {string} recordId - 记录 ID
   * @param {string} newStatus - 新状态
   */
  async updateTaskStatus(recordId, newStatus) {
    try {
      const { app_token, table_id, field_names } = this.config.bitable;
      const fields = {};
      fields[field_names.status] = newStatus;

      await this.client.updateRecord(app_token, table_id, recordId, fields);
      console.log(`✅ 任务状态更新: ${recordId} → ${newStatus}`);
    } catch (error) {
      console.error('❌ 更新任务状态失败:', error.message);
      throw error;
    }
  }

}

// 命令行接口
if (require.main === module) {
  const configPath = process.argv[2] || './config/credentials.json';
  const command = process.argv[3];
  const args = process.argv.slice(4);

  const manager = new TaskManager(configPath);

  (async () => {
    try {
      switch (command) {
        case 'create': {
          const title = args[0];
          if (!title) {
            console.error('❌ 请提供任务标题');
            process.exit(1);
          }

          // 解析可选的 key=value 参数
          const options = {};
          for (let i = 1; i < args.length; i++) {
            const [key, ...rest] = args[i].split('=');
            const value = rest.join('=');
            if (key && value) {
              if (key === 'url') options.sourceUrl = value;
              else if (key === 'priority') options.priority = parseInt(value, 10) || 1;
              else options[key] = value;
            }
          }

          await manager.createTask(title, options);
          console.log('\n✅ 完成');
          break;
        }

        case 'create-doc': {
          // 为记录创建文档
          const recordId = args[0];

          if (!recordId) {
            console.error('❌ 请提供记录 ID');
            process.exit(1);
          }

          await manager.createDoc(recordId);
          console.log('\n✅ 完成');
          break;
        }

        case 'list': {
          const tasks = await manager.getAllTasks();
          const total = Object.values(tasks).reduce((s, arr) => s + arr.length, 0);
          console.log(`\n📋 任务统计 (共 ${total} 条):`);
          for (const [status, items] of Object.entries(tasks)) {
            console.log(`   ${status}: ${items.length}`);
          }
          break;
        }

        default:
          console.log(`
用法:
  node task-manager.js <config> create <title> [type=值] [status=值] [priority=数字] [url=值]
  node task-manager.js <config> create-doc <recordId>
  node task-manager.js <config> list

示例:
  # 创建任务（仅标题）
  node task-manager.js ./config/credentials.json create "新想法"

  # 创建任务（指定类型、状态、优先级、来源）
  node task-manager.js ./config/credentials.json create "研究 AI 伦理" type=研究 status=待处理 priority=5 url=https://example.com

  # 为记录创建文档
  node task-manager.js ./config/credentials.json create-doc "record_xxxxx"

  # 列出任务
  node task-manager.js ./config/credentials.json list
          `);
      }
    } catch (error) {
      console.error('❌ 错误:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = { TaskManager };

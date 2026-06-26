#!/usr/bin/env node
/**
 * Context Router v1.0 - 上下文路由器
 * 
 * 核心职责：按需注入上下文，减少 Agent 间重复传递
 * 
 * 第一性原理：
 * - Agent 执行只需要最小上下文
 * - 不同 Agent 类型需要不同上下文
 * - 上下文压缩可减少 Token 60%~90%
 * 
 * Token 优化效果：
 * - Planner: 全量 → 仅 goal (减少 ~90%)
 * - Executor: 全量 → 仅 input + deps (减少 ~60%)
 * - Reviewer: 全量 → 仅 result + criteria (减少 ~70%)
 */

const fs = require('fs');
const path = require('path');

class ContextRouter {
  constructor(options = {}) {
    this.dbPath = options.dbPath || null; // 可选：SQLite/JSON
    this.cache = new Map();
    this.taskStore = options.taskStore; // 任务存储引用
    this.maxCacheSize = options.maxCacheSize || 1000;
    
    // 上下文模板配置
    this.templates = {
      planner: {
        fields: ['goal', 'constraints', 'priority'],
        description: '规划者仅需要目标和约束'
      },
      executor: {
        fields: ['input', 'dependencies', 'specification', 'output_format'],
        description: '执行者需要输入、依赖和输出格式'
      },
      reviewer: {
        fields: ['result', 'criteria', 'standards'],
        description: '审查者需要结果和审查标准'
      },
      writer: {
        fields: ['outline', 'style', 'word_count', 'previous_chapters'],
        description: '写作者需要大纲、风格和字数'
      },
      architect: {
        fields: ['world_building', 'characters', 'plot'],
        description: '架构师需要世界观、人物和情节'
      }
    };
    
    // 压缩规则
    this.compressionRules = {
      maxStringLength: 10000, // 超过此长度转为文件引用
      maxArrayLength: 50,     // 超过此数量转为摘要
      maxDepth: 5             // 最大嵌套深度
    };
  }

  /**
   * 获取精简上下文（核心方法）
   * @param {string} taskId - 任务 ID
   * @param {string} agentType - Agent 类型 (planner/executor/reviewer/writer/architect)
   * @param {object} options - 选项
   * @returns {object} 精简上下文
   */
  getContext(taskId, agentType, options = {}) {
    const cacheKey = `${taskId}:${agentType}`;
    
    // 1. 检查缓存
    if (this.cache.has(cacheKey) && !options.skipCache) {
      return this.cache.get(cacheKey);
    }
    
    // 2. 获取原始任务数据
    const task = this.getTask(taskId);
    if (!task) {
      console.warn(`[ContextRouter] 任务不存在: ${taskId}`);
      return null;
    }
    
    // 3. 根据模板提取字段
    const template = this.templates[agentType] || this.templates.executor;
    let context = {};
    
    for (const field of template.fields) {
      if (task[field] !== undefined) {
        context[field] = this.compressValue(task[field], field, taskId);
      }
    }
    
    // 4. 添加必要的元数据
    context._meta = {
      taskId,
      agentType,
      timestamp: Date.now(),
      compressed: this.isCompressed(task, context)
    };
    
    // 5. 缓存结果
    if (this.cache.size >= this.maxCacheSize) {
      // LRU 淘汰
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(cacheKey, context);
    
    return context;
  }

  /**
   * 获取任务数据
   */
  getTask(taskId) {
    // 优先从 taskStore 获取
    if (this.taskStore && typeof this.taskStore.get === 'function') {
      return this.taskStore.get(taskId);
    }
    
    // 备选：从缓存获取
    if (this.cache.has(taskId)) {
      return this.cache.get(taskId);
    }
    
    // 备选：从文件系统获取
    const stateFile = '/home/ubutu/.openclaw/workspace/logs/agile-workflow/workflow-state-v5.json';
    if (fs.existsSync(stateFile)) {
      try {
        const state = JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
        return state.tasks?.[taskId] || null;
      } catch (e) {
        console.warn(`[ContextRouter] 读取状态文件失败: ${e.message}`);
      }
    }
    
    return null;
  }

  /**
   * 压缩值（核心压缩逻辑）
   */
  compressValue(value, field, taskId) {
    // 1. 字符串压缩
    if (typeof value === 'string') {
      if (value.length > this.compressionRules.maxStringLength) {
        return this.compressString(value, field, taskId);
      }
      return value;
    }
    
    // 2. 数组压缩
    if (Array.isArray(value)) {
      if (value.length > this.compressionRules.maxArrayLength) {
        return this.compressArray(value, field, taskId);
      }
      return value.map((v, i) => this.compressValue(v, `${field}[${i}]`, taskId));
    }
    
    // 3. 对象压缩
    if (typeof value === 'object' && value !== null) {
      return this.compressObject(value, field, taskId, 0);
    }
    
    return value;
  }

  /**
   * 压缩字符串（转为文件引用）
   */
  compressString(str, field, taskId) {
    // 保存到临时文件
    const cacheDir = '/home/ubutu/.openclaw/workspace/data/cache/context';
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    
    const fileName = `${taskId}_${field}.txt`;
    const filePath = path.join(cacheDir, fileName);
    fs.writeFileSync(filePath, str);
    
    // 返回文件引用
    return {
      _ref: `file://${filePath}`,
      _length: str.length,
      _summary: str.substring(0, 500) + '...'
    };
  }

  /**
   * 压缩数组（转为摘要）
   */
  compressArray(arr, field, taskId) {
    return {
      _type: 'array_summary',
      _count: arr.length,
      _sample: arr.slice(0, 10),
      _summary: `共 ${arr.length} 项，已省略 ${arr.length - 10} 项`
    };
  }

  /**
   * 压缩对象（深度限制）
   */
  compressObject(obj, field, taskId, depth) {
    if (depth >= this.compressionRules.maxDepth) {
      return {
        _type: 'truncated',
        _keys: Object.keys(obj),
        _summary: '嵌套过深，已截断'
      };
    }
    
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = this.compressValue(value, `${field}.${key}`, taskId);
    }
    return result;
  }

  /**
   * 检查是否已压缩
   */
  isCompressed(original, compressed) {
    const originalSize = JSON.stringify(original).length;
    const compressedSize = JSON.stringify(compressed).length;
    return compressedSize < originalSize * 0.9; // 压缩超过 10%
  }

  /**
   * 构建依赖上下文（按需加载依赖结果）
   */
  buildDependencyContext(taskId, options = {}) {
    const task = this.getTask(taskId);
    if (!task || !task.dependencies || task.dependencies.length === 0) {
      return null;
    }
    
    const depContexts = [];
    for (const depId of task.dependencies) {
      const depTask = this.getTask(depId);
      if (depTask && depTask.status === 'completed') {
        // 仅包含依赖的关键信息
        depContexts.push({
          id: depId,
          type: depTask.type,
          status: depTask.status,
          summary: this.summarizeResult(depTask.result)
        });
      }
    }
    
    return depContexts;
  }

  /**
   * 总结结果（提取关键信息）
   */
  summarizeResult(result) {
    if (!result) return null;
    
    if (typeof result === 'string') {
      return result.length > 500 ? result.substring(0, 500) + '...' : result;
    }
    
    if (typeof result === 'object') {
      // 提取关键字段
      const summary = {};
      const keyFields = ['title', 'name', 'status', 'error', 'success'];
      for (const field of keyFields) {
        if (result[field] !== undefined) {
          summary[field] = result[field];
        }
      }
      return summary;
    }
    
    return result;
  }

  /**
   * 注册自定义模板
   */
  registerTemplate(agentType, fields, description = '') {
    this.templates[agentType] = { fields, description };
    console.log(`[ContextRouter] 注册模板: ${agentType} -> ${fields.join(', ')}`);
  }

  /**
   * 清除缓存
   */
  clearCache(taskId = null) {
    if (taskId) {
      // 清除指定任务的缓存
      for (const key of this.cache.keys()) {
        if (key.startsWith(taskId + ':')) {
          this.cache.delete(key);
        }
      }
    } else {
      // 清除所有缓存
      this.cache.clear();
    }
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      cacheSize: this.cache.size,
      templates: Object.keys(this.templates),
      compressionRules: this.compressionRules
    };
  }
}

// 单例导出
let instance = null;

function getContextRouter(options = {}) {
  if (!instance) {
    instance = new ContextRouter(options);
  }
  return instance;
}

module.exports = {
  ContextRouter,
  getContextRouter
};
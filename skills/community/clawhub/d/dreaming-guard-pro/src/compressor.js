/**
 * Dreaming Guard Pro - Compressor Module
 * 
 * 上下文语义压缩（非gzip压缩）
 * 三级策略：lossless → lossy → aggressive
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 压缩策略定义
const COMPRESS_STRATEGIES = {
  LOSSLESS: 'lossless',   // 无损：去除重复，保留所有信息
  LOSSY: 'lossy',         // 有损：摘要替代，保留关键信息
  AGGRESSIVE: 'aggressive' // 激进：只保留关键摘要
};

// 压缩策略配置
const STRATEGY_CONFIG = {
  lossless: {
    targetReduction: 0.15,   // 目标减少15%
    preserveFields: ['timestamp', 'type', 'level', 'decision', 'error', 'config'],
    deduplicate: true,
    summarize: false,
    minChunkSize: 100        // 最小chunk大小（字节）
  },
  lossy: {
    targetReduction: 0.40,   // 目标减少40%
    preserveFields: ['timestamp', 'type', 'level', 'decision', 'error', 'config', 'user_id', 'session_id'],
    deduplicate: true,
    summarize: true,
    summaryRatio: 3,         // 每3条合并为1条摘要
    keepKeywords: ['error', 'warning', 'critical', 'decision', 'important', 'config', 'startup', 'shutdown']
  },
  aggressive: {
    targetReduction: 0.70,   // 目标减少70%
    preserveFields: ['timestamp', 'type', 'level', 'decision', 'error'],
    deduplicate: true,
    summarize: true,
    summaryRatio: 10,        // 每10条合并为1条摘要
    keepKeywords: ['error', 'critical', 'decision', 'shutdown'],
    maxEntries: 50           // 最多保留50条关键条目
  }
};

// 默认配置
const DEFAULT_CONFIG = {
  strategy: COMPRESS_STRATEGIES.LOSSLESS,
  backup: true,             // 压缩前备份原文件
  backupPath: path.join(os.homedir(), '.openclaw', 'archive', 'dreaming-backup'),
  dryRun: false
};

/**
 * Compressor类 - 上下文压缩器
 */
class Compressor {
  constructor(options = {}) {
    // 合并配置
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 确保备份目录存在
    if (this.config.backup && !fs.existsSync(this.config.backupPath)) {
      fs.mkdirSync(this.config.backupPath, { recursive: true });
    }
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Compressor]', ...args),
      info: (...args) => console.info('[Compressor]', ...args),
      warn: (...args) => console.warn('[Compressor]', ...args),
      error: (...args) => console.error('[Compressor]', ...args)
    };
  }

  /**
   * 压缩内容
   * @param {string|object} content - 内容（文件路径、JSON对象或字符串）
   * @param {string} strategy - 压缩策略
   * @returns {Promise<object>} 压缩结果
   */
  async compress(content, strategy = this.config.strategy) {
    // 确定输入类型
    let inputType = 'unknown';
    let data = null;
    let filePath = null;
    
    if (typeof content === 'string') {
      // 可能是文件路径或JSON字符串
      if (fs.existsSync(content)) {
        inputType = 'file';
        filePath = content;
        data = this._loadFile(content);
      } else {
        inputType = 'string';
        try {
          data = JSON.parse(content);
          inputType = 'json-string';
        } catch (e) {
          // 不是JSON，按普通字符串处理
          data = { raw: content, entries: content.split('\n').filter(l => l.trim()) };
        }
      }
    } else if (typeof content === 'object') {
      inputType = 'object';
      data = content;
    }
    
    if (!data) {
      throw new Error('Unable to parse input content');
    }
    
    this.logger.info('Starting compression', { strategy, inputType });
    
    // 获取策略配置
    const strategyConfig = this.getStrategy(strategy);
    
    // 备份原文件
    let backupPath = null;
    if (this.config.backup && filePath && !this.config.dryRun) {
      backupPath = this._backupFile(filePath);
    }
    
    // 解析数据结构
    const parsed = this._parseData(data);
    
    // 执行压缩
    const compressed = this._executeCompression(parsed, strategyConfig);
    
    // 计算结果
    const result = {
      original: {
        size: parsed.rawSize,
        entries: parsed.totalEntries
      },
      compressed: {
        size: this._calculateSize(compressed),
        entries: compressed.totalEntries || compressed.length || 0
      },
      reduction: 0,
      strategy,
      method: this._getMethodDescription(strategyConfig),
      preserved: strategyConfig.preserveFields,
      backupPath,
      filePath,
      dryRun: this.config.dryRun
    };
    
    result.reduction = (result.original.size - result.compressed.size) / result.original.size;
    
    // 写入压缩结果（如果不是试运行）
    if (!this.config.dryRun && filePath) {
      this._writeCompressed(filePath, compressed);
    }
    
    this.logger.info('Compression completed', {
      originalSize: result.original.size,
      compressedSize: result.compressed.size,
      reduction: `${(result.reduction * 100).toFixed(1)}%`
    });
    
    return result;
  }

  /**
   * 获取策略配置
   * @param {string} level - 策略级别
   * @returns {object} 策略配置
   */
  getStrategy(level) {
    return STRATEGY_CONFIG[level] || STRATEGY_CONFIG.lossless;
  }

  /**
   * 加载文件内容
   * @param {string} filePath - 文件路径
   * @returns {object} 加载的数据
   */
  _loadFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const ext = path.extname(filePath);
    
    if (ext === '.jsonl') {
      // JSONL文件：每行一个JSON对象
      return {
        type: 'jsonl',
        entries: content.split('\n').filter(l => l.trim()).map(line => {
          try {
            return JSON.parse(line);
          } catch (e) {
            return { raw: line, parseError: true };
          }
        }),
        raw: content
      };
    } else if (ext === '.json') {
      // JSON文件
      try {
        return {
          type: 'json',
          data: JSON.parse(content),
          raw: content
        };
      } catch (e) {
        return {
          type: 'json',
          data: null,
          parseError: true,
          raw: content
        };
      }
    }
    
    return { type: 'unknown', raw: content };
  }

  /**
   * 备份文件
   * @param {string} filePath - 文件路径
   * @returns {string} 备份路径
   */
  _backupFile(filePath) {
    const basename = path.basename(filePath);
    const timestamp = Date.now();
    const backupName = `${basename}.${timestamp}.bak`;
    const backupPath = path.join(this.config.backupPath, backupName);
    
    fs.copyFileSync(filePath, backupPath);
    this.logger.debug('Backup created:', backupPath);
    
    return backupPath;
  }

  /**
   * 解析数据结构
   * @param {object} data - 原始数据
   * @returns {object} 解析结果
   */
  _parseData(data) {
    const result = {
      type: data.type || 'unknown',
      entries: [],
      rawSize: 0,
      totalEntries: 0
    };
    
    if (data.type === 'jsonl') {
      result.entries = data.entries || [];
      result.rawSize = data.raw?.length || 0;
    } else if (data.type === 'json') {
      if (Array.isArray(data.data)) {
        result.entries = data.data;
        result.type = 'json-array';
      } else if (data.data && typeof data.data === 'object') {
        // 单个JSON对象
        result.entries = [data.data];
        result.type = 'json-object';
      }
      result.rawSize = data.raw?.length || 0;
    } else if (Array.isArray(data)) {
      result.entries = data;
      result.type = 'array';
      result.rawSize = JSON.stringify(data).length;
    } else if (data.raw) {
      // 字符串数据
      result.entries = data.entries || [{ raw: data.raw }];
      result.type = 'string';
      result.rawSize = data.raw.length;
    }
    
    result.totalEntries = result.entries.length;
    
    return result;
  }

  /**
   * 执行压缩
   * @param {object} parsed - 解析后的数据
   * @param {object} config - 策略配置
   * @returns {object} 压缩后的数据
   */
  _executeCompression(parsed, config) {
    let entries = [...parsed.entries];
    
    // Step 1: 去重（所有策略都执行）
    if (config.deduplicate) {
      entries = this._deduplicate(entries, config);
    }
    
    // Step 2: 过滤保留字段
    entries = this._filterFields(entries, config);
    
    // Step 3: 摘要合并（lossy和aggressive）
    if (config.summarize) {
      entries = this._summarize(entries, config);
    }
    
    // Step 4: 关键条目筛选（aggressive）
    if (config.keepKeywords) {
      entries = this._filterKeywords(entries, config);
    }
    
    // Step 5: 限制条目数（aggressive）
    if (config.maxEntries && entries.length > config.maxEntries) {
      entries = this._limitEntries(entries, config.maxEntries);
    }
    
    // 构建返回结果
    const compressed = {
      type: parsed.type,
      entries,
      totalEntries: entries.length,
      compressed: true,
      strategy: config,
      originalSize: parsed.rawSize,
      originalEntries: parsed.totalEntries
    };
    
    return compressed;
  }

  /**
   * 去重
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {array} 去重后的条目
   */
  _deduplicate(entries, config) {
    const seen = new Map();
    const unique = [];
    
    for (const entry of entries) {
      // 创建条目的唯一标识
      const key = this._createEntryKey(entry, config.preserveFields);
      
      if (!seen.has(key)) {
        seen.set(key, true);
        unique.push(entry);
      } else {
        // 记录去重统计
        this.logger.debug('Duplicate entry removed:', key.slice(0, 50));
      }
    }
    
    this.logger.debug('Deduplication:', entries.length - unique.length, 'removed');
    
    return unique;
  }

  /**
   * 创建条目唯一键
   * @param {object} entry - 条目
   * @param {array} preserveFields - 保留字段
   * @returns {string} 唯一键
   */
  _createEntryKey(entry, preserveFields) {
    if (typeof entry !== 'object' || entry === null) {
      return String(entry);
    }
    
    // 使用保留字段创建键
    const keyParts = [];
    for (const field of preserveFields) {
      if (entry[field] !== undefined) {
        keyParts.push(`${field}:${JSON.stringify(entry[field])}`);
      }
    }
    
    // 如果没有保留字段，使用全部内容
    if (keyParts.length === 0) {
      return JSON.stringify(entry);
    }
    
    return keyParts.join('|');
  }

  /**
   * 过滤保留字段
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {array} 过滤后的条目
   */
  _filterFields(entries, config) {
    if (!config.preserveFields || config.preserveFields.length === 0) {
      return entries;
    }
    
    return entries.map(entry => {
      if (typeof entry !== 'object' || entry === null) {
        return entry;
      }
      
      const filtered = {};
      for (const field of config.preserveFields) {
        if (entry[field] !== undefined) {
          filtered[field] = entry[field];
        }
      }
      
      // 保留其他字段但标记为压缩
      const otherFields = Object.keys(entry).filter(f => !config.preserveFields.includes(f));
      if (otherFields.length > 0) {
        filtered._compressedFields = otherFields.length;
        // lossless保留所有字段
        if (config.targetReduction <= 0.15) {
          filtered._originalFields = {};
          for (const f of otherFields) {
            const val = entry[f];
            if (typeof val === 'string' && val.length > 100) {
              filtered._originalFields[f] = val.slice(0, 50) + '...[truncated]';
            } else {
              filtered._originalFields[f] = val;
            }
          }
        }
      }
      
      return filtered;
    });
  }

  /**
   * 摘要合并
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {array} 合并后的条目
   */
  _summarize(entries, config) {
    const ratio = config.summaryRatio || 3;
    const summarized = [];
    let buffer = [];
    
    for (const entry of entries) {
      // 检查是否是关键条目（不合并）
      if (this._isKeyEntry(entry, config)) {
        // 先合并buffer中的非关键条目
        if (buffer.length >= ratio) {
          summarized.push(this._createSummary(buffer, config));
          buffer = [];
        }
        // 保留buffer中的部分条目
        while (buffer.length > 0) {
          summarized.push(buffer.shift());
        }
        // 关键条目直接保留
        summarized.push(entry);
      } else {
        buffer.push(entry);
        
        // 达到合并比例时创建摘要
        if (buffer.length >= ratio * 2) {
          summarized.push(this._createSummary(buffer.slice(0, ratio), config));
          buffer = buffer.slice(ratio);
        }
      }
    }
    
    // 处理剩余buffer
    if (buffer.length > 0) {
      if (buffer.length >= ratio) {
        summarized.push(this._createSummary(buffer, config));
      } else {
        summarized.push(...buffer);
      }
    }
    
    this.logger.debug('Summarization:', entries.length, '→', summarized.length);
    
    return summarized;
  }

  /**
   * 检查是否是关键条目
   * @param {object} entry - 条目
   * @param {object} config - 策略配置
   * @returns {boolean} 是否关键
   */
  _isKeyEntry(entry, config) {
    if (!config.keepKeywords) return false;
    
    // 检查类型
    if (entry.type && config.keepKeywords.includes(entry.type)) {
      return true;
    }
    
    // 检查级别
    if (entry.level && config.keepKeywords.includes(entry.level)) {
      return true;
    }
    
    // 检查内容关键词
    const content = JSON.stringify(entry);
    for (const keyword of config.keepKeywords) {
      if (content.toLowerCase().includes(keyword.toLowerCase())) {
        return true;
      }
    }
    
    return false;
  }

  /**
   * 创建摘要条目
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {object} 摘要条目
   */
  _createSummary(entries, config) {
    const summary = {
      type: 'summary',
      count: entries.length,
      timestampRange: this._getTimestampRange(entries),
      compressed: true
    };
    
    // 提取关键信息
    const keyInfo = this._extractKeyInfo(entries, config);
    if (keyInfo.length > 0) {
      summary.keyInfo = keyInfo;
    }
    
    // 统计类型
    const typeStats = {};
    for (const entry of entries) {
      const type = entry.type || 'unknown';
      typeStats[type] = (typeStats[type] || 0) + 1;
    }
    if (Object.keys(typeStats).length > 0) {
      summary.typeStats = typeStats;
    }
    
    return summary;
  }

  /**
   * 获取时间戳范围
   * @param {array} entries - 条目列表
   * @returns {object} 时间范围
   */
  _getTimestampRange(entries) {
    const timestamps = entries
      .filter(e => e.timestamp)
      .map(e => e.timestamp)
      .sort((a, b) => a - b);
    
    if (timestamps.length === 0) return null;
    
    return {
      start: timestamps[0],
      end: timestamps[timestamps.length - 1]
    };
  }

  /**
   * 提取关键信息
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {array} 关键信息
   */
  _extractKeyInfo(entries, config) {
    const keyInfo = [];
    
    for (const entry of entries) {
      // 提取保留字段值
      const info = {};
      for (const field of config.preserveFields.slice(0, 5)) {
        if (entry[field] !== undefined) {
          info[field] = entry[field];
        }
      }
      
      if (Object.keys(info).length > 0) {
        keyInfo.push(info);
      }
      
      // 限制提取数量
      if (keyInfo.length >= 3) break;
    }
    
    return keyInfo;
  }

  /**
   * 按关键词过滤
   * @param {array} entries - 条目列表
   * @param {object} config - 策略配置
   * @returns {array} 过滤后的条目
   */
  _filterKeywords(entries, config) {
    const filtered = [];
    
    for (const entry of entries) {
      if (this._isKeyEntry(entry, config)) {
        filtered.push(entry);
      }
    }
    
    this.logger.debug('Keyword filtering:', entries.length, '→', filtered.length);
    
    return filtered.length > 0 ? filtered : entries; // 确保不会全部过滤掉
  }

  /**
   * 限制条目数量
   * @param {array} entries - 条目列表
   * @param {number} max - 最大数量
   * @returns {array} 限制后的条目
   */
  _limitEntries(entries, max) {
    // 按重要性排序：关键条目优先
    const sorted = entries.sort((a, b) => {
      const aKey = a.type === 'summary' || a.type === 'error' || a.level === 'critical';
      const bKey = b.type === 'summary' || b.type === 'error' || b.level === 'critical';
      
      if (aKey && !bKey) return -1;
      if (!aKey && bKey) return 1;
      
      // 按时间戳排序
      return (b.timestamp || 0) - (a.timestamp || 0);
    });
    
    return sorted.slice(0, max);
  }

  /**
   * 计算压缩后大小
   * @param {object} compressed - 压缩数据
   * @returns {number} 大小（字节）
   */
  _calculateSize(compressed) {
    return JSON.stringify(compressed).length;
  }

  /**
   * 获取方法描述
   * @param {object} config - 策略配置
   * @returns {string} 描述
   */
  _getMethodDescription(config) {
    const methods = [];
    
    if (config.deduplicate) methods.push('deduplicate');
    if (config.preserveFields) methods.push(`preserve(${config.preserveFields.length} fields)`);
    if (config.summarize) methods.push(`summarize(ratio:${config.summaryRatio})`);
    if (config.keepKeywords) methods.push(`keywords(${config.keepKeywords.length})`);
    if (config.maxEntries) methods.push(`limit(${config.maxEntries})`);
    
    return methods.join('+');
  }

  /**
   * 写入压缩结果
   * @param {string} filePath - 文件路径
   * @param {object} compressed - 压缩数据
   */
  _writeCompressed(filePath, compressed) {
    const ext = path.extname(filePath);
    let content;
    
    if (ext === '.jsonl') {
      // 转换为JSONL格式
      content = compressed.entries.map(e => JSON.stringify(e)).join('\n');
    } else {
      // JSON格式
      content = JSON.stringify(compressed, null, 2);
    }
    
    // 原子写入
    const tempPath = filePath + '.tmp';
    fs.writeFileSync(tempPath, content);
    fs.renameSync(tempPath, filePath);
    
    this.logger.debug('Compressed file written:', filePath);
  }

  /**
   * 分析可压缩性
   * @param {string} filePath - 文件路径
   * @returns {Promise<object>} 分析结果
   */
  async analyze(filePath) {
    const data = this._loadFile(filePath);
    const parsed = this._parseData(data);
    
    // 分析重复率
    const dedupResult = this._analyzeDeduplication(parsed.entries);
    
    // 分析可摘要率
    const summarizeResult = this._analyzeSummarization(parsed.entries);
    
    // 预估各策略效果
    const estimates = {};
    for (const [name, config] of Object.entries(STRATEGY_CONFIG)) {
      estimates[name] = {
        targetReduction: config.targetReduction,
        estimatedSize: Math.floor(parsed.rawSize * (1 - config.targetReduction)),
        estimatedEntries: Math.floor(parsed.totalEntries * (1 - config.targetReduction))
      };
    }
    
    return {
      filePath,
      originalSize: parsed.rawSize,
      totalEntries: parsed.totalEntries,
      type: parsed.type,
      dedupPotential: dedupResult,
      summarizePotential: summarizeResult,
      estimates,
      recommendation: this._getRecommendation(dedupResult, summarizeResult)
    };
  }

  /**
   * 分析去重潜力
   * @param {array} entries - 条目列表
   * @returns {object} 分析结果
   */
  _analyzeDeduplication(entries) {
    const seen = new Map();
    let duplicates = 0;
    
    for (const entry of entries) {
      const key = JSON.stringify(entry);
      if (seen.has(key)) {
        duplicates++;
      } else {
        seen.set(key, true);
      }
    }
    
    return {
      duplicates,
      duplicateRate: duplicates / entries.length,
      potentialReduction: duplicates / entries.length * 0.1 // 去重通常减少10%
    };
  }

  /**
   * 分析摘要潜力
   * @param {array} entries - 条目列表
   * @returns {object} 分析结果
   */
  _analyzeSummarization(entries) {
    let keyEntries = 0;
    let normalEntries = 0;
    
    for (const entry of entries) {
      if (this._isKeyEntry(entry, STRATEGY_CONFIG.lossy)) {
        keyEntries++;
      } else {
        normalEntries++;
      }
    }
    
    const summarizeRatio = STRATEGY_CONFIG.lossy.summaryRatio;
    const summariesNeeded = Math.floor(normalEntries / summarizeRatio);
    
    return {
      keyEntries,
      normalEntries,
      summariesNeeded,
      potentialReduction: normalEntries / entries.length * 0.6
    };
  }

  /**
   * 获取推荐策略
   * @param {object} dedup - 去重分析
   * @param {object} summarize - 摘要分析
   * @returns {string} 推荐策略
   */
  _getRecommendation(dedup, summarize) {
    // 如果重复率高，推荐lossless
    if (dedup.duplicateRate > 0.2) {
      return COMPRESS_STRATEGIES.LOSSLESS;
    }
    
    // 如果普通条目多，推荐lossy
    if (summarize.normalEntries > summarize.keyEntries * 5) {
      return COMPRESS_STRATEGIES.LOSSY;
    }
    
    // 默认推荐lossless
    return COMPRESS_STRATEGIES.LOSSLESS;
  }
}

module.exports = Compressor;
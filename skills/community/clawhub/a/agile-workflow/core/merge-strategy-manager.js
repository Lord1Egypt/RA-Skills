#!/usr/bin/env node
/**
 * 合并策略管理器 v7.0
 * 
 * 核心职责：定义和应用合并策略，处理并发结果整合
 * 
 * 第一性原理：
 * - 合并冲突根源 = 多个写入者修改同一键
 * - 解决方案 = 预定义策略 + 冲突检测 + 人工审核
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class MergeStrategyManager {
  constructor(config = {}) {
    this.strategies = new Map();
    this.config = {
      workspace: config.workspace || '/tmp/merge-workspace',
      maxConflicts: config.maxConflicts || 100,
      autoResolve: config.autoResolve || false
    };
    
    this.conflictLog = [];
    this.registerDefaultStrategies();
  }

  /**
   * 注册默认策略
   */
  registerDefaultStrategies() {
    // ========== 策略 1: 追加合并 ==========
    this.strategies.set('append', {
      name: '追加合并',
      description: '将所有结果按顺序拼接',
      merge: (results, options = {}) => {
        const flat = results.flat();
        return {
          merged: flat,
          conflicts: [],
          metadata: {
            strategy: 'append',
            inputCount: results.length,
            outputCount: flat.length
          }
        };
      },
      conflictResolution: 'none',
      scenarios: ['列表', '日志', '章节']
    });

    // ========== 策略 2: 覆盖合并（最后写入胜出）==========
    this.strategies.set('overwrite', {
      name: '覆盖合并',
      description: '后面的结果覆盖前面的',
      merge: (results, options = {}) => {
        const merged = {};
        const conflicts = [];
        
        results.forEach((result, idx) => {
          if (typeof result !== 'object' || result === null) return;
          
          Object.entries(result).forEach(([key, value]) => {
            if (key in merged && JSON.stringify(merged[key]) !== JSON.stringify(value)) {
              conflicts.push({
                key,
                values: results.map(r => r?.[key]),
                sources: results.map((_, i) => `result-${i}`),
                finalValue: value,
                resolution: 'last-write-wins'
              });
            }
            merged[key] = value;
          });
        });

        return {
          merged,
          conflicts,
          metadata: {
            strategy: 'overwrite',
            inputCount: results.length,
            outputKeys: Object.keys(merged).length,
            conflictCount: conflicts.length
          }
        };
      },
      conflictResolution: 'last-write-wins',
      scenarios: ['配置', '状态', '元数据']
    });

    // ========== 策略 3: 智能合并（三路合并）==========
    this.strategies.set('smart', {
      name: '智能合并',
      description: '检测冲突并标记需要人工审核',
      merge: (results, options = {}) => {
        const base = options.base || {};
        const merged = JSON.parse(JSON.stringify(base));
        const conflicts = [];
        const keySources = new Map(); // key → [{source, value}]

        // 收集所有键的来源
        results.forEach((result, idx) => {
          if (typeof result !== 'object' || result === null) return;
          
          Object.entries(result).forEach(([key, value]) => {
            if (!keySources.has(key)) {
              keySources.set(key, []);
            }
            keySources.get(key).push({
              source: `result-${idx}`,
              value: JSON.parse(JSON.stringify(value))
            });
          });
        });

        // 合并并检测冲突
        for (const [key, sources] of keySources) {
          const values = sources.map(s => s.value);
          const uniqueValues = new Set(values.map(v => JSON.stringify(v)));

          if (uniqueValues.size === 1) {
            // 无冲突
            merged[key] = values[0];
          } else {
            // 有冲突
            conflicts.push({
              key,
              values,
              sources: sources.map(s => s.source),
              resolution: 'manual-review-required',
              suggestions: this.generateMergeSuggestions(key, values)
            });

            // 临时使用最后一个值
            merged[key] = values[values.length - 1];
          }
        }

        return {
          merged,
          conflicts,
          metadata: {
            strategy: 'smart',
            inputCount: results.length,
            outputKeys: Object.keys(merged).length,
            conflictCount: conflicts.length,
            hasConflicts: conflicts.length > 0
          }
        };
      },
      conflictResolution: 'manual-review',
      scenarios: ['文档', '代码', '复杂对象']
    });

    // ========== 策略 4: 聚合合并（数学运算）==========
    this.strategies.set('aggregate', {
      name: '聚合合并',
      description: '对数值进行数学运算',
      merge: (results, options = {}) => {
        const operation = options.operation || 'sum';
        const numbers = results.flat().filter(n => typeof n === 'number');
        
        if (numbers.length === 0) {
          return {
            merged: 0,
            conflicts: [],
            metadata: {
              strategy: 'aggregate',
              operation,
              inputCount: 0,
              warning: '无数值可聚合'
            }
          };
        }

        let result;
        switch (operation) {
          case 'sum':
            result = numbers.reduce((a, b) => a + b, 0);
            break;
          case 'avg':
            result = numbers.reduce((a, b) => a + b, 0) / numbers.length;
            break;
          case 'max':
            result = Math.max(...numbers);
            break;
          case 'min':
            result = Math.min(...numbers);
            break;
          case 'count':
            result = numbers.length;
            break;
          default:
            result = numbers;
        }

        return {
          merged: result,
          conflicts: [],
          metadata: {
            strategy: 'aggregate',
            operation,
            inputCount: numbers.length,
            stats: {
              sum: numbers.reduce((a, b) => a + b, 0),
              avg: numbers.reduce((a, b) => a + b, 0) / numbers.length,
              max: Math.max(...numbers),
              min: Math.min(...numbers)
            }
          }
        };
      },
      conflictResolution: 'none',
      scenarios: ['统计', '分析', '数值计算']
    });

    // ========== 策略 5: 深度合并 ==========
    this.strategies.set('deep', {
      name: '深度合并',
      description: '递归合并嵌套对象',
      merge: (results, options = {}) => {
        const conflicts = [];
        
        const deepMerge = (target, source, sourceIdx, path = '') => {
          if (typeof source !== 'object' || source === null) {
            return source;
          }

          if (Array.isArray(source)) {
            if (!Array.isArray(target)) {
              if (target !== undefined) {
                conflicts.push({
                  key: path,
                  values: [target, source],
                  resolution: 'type-mismatch-use-latest'
                });
              }
              return source;
            }
            return [...target, ...source];
          }

          const result = { ...target };
          
          for (const key of Object.keys(source)) {
            const currentPath = path ? `${path}.${key}` : key;
            
            if (key in result) {
              if (
                typeof result[key] === 'object' &&
                typeof source[key] === 'object' &&
                result[key] !== null &&
                source[key] !== null
              ) {
                result[key] = deepMerge(result[key], source[key], sourceIdx, currentPath);
              } else if (JSON.stringify(result[key]) !== JSON.stringify(source[key])) {
                conflicts.push({
                  key: currentPath,
                  values: [result[key], source[key]],
                  source: `result-${sourceIdx}`,
                  resolution: 'overwrite'
                });
                result[key] = source[key];
              }
            } else {
              result[key] = source[key];
            }
          }

          return result;
        };

        let merged = {};
        results.forEach((result, idx) => {
          merged = deepMerge(merged, result, idx);
        });

        return {
          merged,
          conflicts,
          metadata: {
            strategy: 'deep',
            inputCount: results.length,
            conflictCount: conflicts.length
          }
        };
      },
      conflictResolution: 'deep-merge',
      scenarios: ['嵌套配置', '复杂结构']
    });

    // ========== 策略 6: 自定义函数合并 ==========
    this.strategies.set('custom', {
      name: '自定义合并',
      description: '使用自定义函数进行合并',
      merge: (results, options = {}) => {
        if (typeof options.mergeFn !== 'function') {
          throw new Error('自定义合并需要提供 mergeFn 函数');
        }

        const customResult = options.mergeFn(results, options);
        
        return {
          merged: customResult.merged || customResult,
          conflicts: customResult.conflicts || [],
          metadata: {
            strategy: 'custom',
            inputCount: results.length,
            customMetadata: customResult.metadata || {}
          }
        };
      },
      conflictResolution: 'custom',
      scenarios: ['特殊需求']
    });

    // ========== 策略 7: 文件合并 ==========
    this.strategies.set('file', {
      name: '文件合并',
      description: '合并文件内容',
      merge: (results, options = {}) => {
        const outputDir = options.outputDir || '/tmp/merged-files';
        const mergeType = options.mergeType || 'concat'; // concat, union, latest
        
        fs.mkdirSync(outputDir, { recursive: true });
        
        const mergedFiles = [];
        const conflicts = [];

        if (mergeType === 'concat') {
          // 拼接所有文件内容
          const outputPath = path.join(outputDir, `merged_${Date.now()}.txt`);
          let content = '';
          
          results.forEach((fileList, idx) => {
            if (!Array.isArray(fileList)) return;
            
            fileList.forEach(filePath => {
              if (fs.existsSync(filePath)) {
                content += fs.readFileSync(filePath, 'utf8');
                content += `\n\n--- File: ${filePath} (Source ${idx}) ---\n\n`;
              }
            });
          });
          
          fs.writeFileSync(outputPath, content);
          mergedFiles.push(outputPath);
        } else if (mergeType === 'latest') {
          // 只保留最新版本
          results.forEach((fileList, idx) => {
            if (!Array.isArray(fileList)) return;
            
            fileList.forEach(filePath => {
              if (fs.existsSync(filePath)) {
                const fileName = path.basename(filePath);
                const outputPath = path.join(outputDir, `latest_${fileName}`);
                fs.copyFileSync(filePath, outputPath);
                mergedFiles.push(outputPath);
              }
            });
          });
        }

        return {
          merged: mergedFiles,
          conflicts,
          metadata: {
            strategy: 'file',
            mergeType,
            outputDir,
            fileCount: mergedFiles.length
          }
        };
      },
      conflictResolution: 'configurable',
      scenarios: ['文档', '代码文件', '资源文件']
    });
  }

  /**
   * 生成合并建议
   */
  generateMergeSuggestions(key, values) {
    const suggestions = [];
    
    // 数值类型建议
    if (values.every(v => typeof v === 'number')) {
      suggestions.push({
        type: 'average',
        value: values.reduce((a, b) => a + b, 0) / values.length,
        description: '使用平均值'
      });
      suggestions.push({
        type: 'max',
        value: Math.max(...values),
        description: '使用最大值'
      });
    }
    
    // 字符串类型建议
    if (values.every(v => typeof v === 'string')) {
      suggestions.push({
        type: 'concat',
        value: values.join(' '),
        description: '拼接所有值'
      });
    }
    
    // 数组类型建议
    if (values.every(v => Array.isArray(v))) {
      suggestions.push({
        type: 'union',
        value: [...new Set(values.flat())],
        description: '去重合并'
      });
    }
    
    return suggestions;
  }

  /**
   * 注册自定义策略
   */
  registerStrategy(name, strategy) {
    if (!strategy.name || !strategy.merge || typeof strategy.merge !== 'function') {
      throw new Error('策略必须包含 name 和 merge 函数');
    }
    this.strategies.set(name, strategy);
  }

  /**
   * 应用策略
   */
  applyStrategy(strategyName, results, options = {}) {
    const strategy = this.strategies.get(strategyName);
    
    if (!strategy) {
      const available = Array.from(this.strategies.keys()).join(', ');
      throw new Error(`未知策略：${strategyName}。可用策略：${available}`);
    }

    try {
      const mergeResult = strategy.merge(results, options);
      
      // 记录冲突
      if (mergeResult.conflicts && mergeResult.conflicts.length > 0) {
        this.conflictLog.push({
          timestamp: Date.now(),
          strategy: strategyName,
          conflicts: mergeResult.conflicts
        });
        
        // 检查冲突数量限制
        if (mergeResult.conflicts.length > this.config.maxConflicts) {
          throw new Error(
            `冲突数量超过限制：${mergeResult.conflicts.length} > ${this.config.maxConflicts}`
          );
        }
      }
      
      return mergeResult;
    } catch (error) {
      throw new Error(`策略 ${strategyName} 执行失败：${error.message}`);
    }
  }

  /**
   * 解决冲突
   */
  resolveConflict(conflict, resolution) {
    switch (resolution.type) {
      case 'use-value':
        return resolution.value;
      case 'use-source':
        return conflict.values[conflict.sources.indexOf(resolution.source)];
      case 'average':
        if (conflict.values.every(v => typeof v === 'number')) {
          return conflict.values.reduce((a, b) => a + b, 0) / conflict.values.length;
        }
        break;
      case 'manual':
        throw new Error('需要人工审核冲突');
      default:
        throw new Error(`未知解决方式：${resolution.type}`);
    }
  }

  /**
   * 获取所有可用策略
   */
  getAvailableStrategies() {
    const strategies = [];
    for (const [name, strategy] of this.strategies) {
      strategies.push({
        name,
        displayName: strategy.name,
        description: strategy.description,
        conflictResolution: strategy.conflictResolution,
        scenarios: strategy.scenarios
      });
    }
    return strategies;
  }

  /**
   * 获取冲突日志
   */
  getConflictLog(options = {}) {
    let log = this.conflictLog;
    
    if (options.since) {
      log = log.filter(entry => entry.timestamp >= options.since);
    }
    
    if (options.strategy) {
      log = log.filter(entry => entry.strategy === options.strategy);
    }
    
    return log;
  }

  /**
   * 导出冲突报告
   */
  exportConflictReport(outputPath) {
    const report = {
      generatedAt: Date.now(),
      totalConflicts: this.conflictLog.reduce((sum, entry) => 
        sum + entry.conflicts.length, 0
      ),
      entries: this.conflictLog,
      strategies: this.getAvailableStrategies()
    };
    
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
    return outputPath;
  }

  /**
   * 清除冲突日志
   */
  clearConflictLog() {
    this.conflictLog = [];
  }
}

module.exports = MergeStrategyManager;

// CLI 测试
if (require.main === module) {
  const merger = new MergeStrategyManager();
  
  console.log('可用策略:');
  console.log(JSON.stringify(merger.getAvailableStrategies(), null, 2));
  
  // 测试追加合并
  console.log('\n测试追加合并:');
  const appendResult = merger.applyStrategy('append', [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ]);
  console.log('结果:', appendResult.merged);
  
  // 测试覆盖合并
  console.log('\n测试覆盖合并:');
  const overwriteResult = merger.applyStrategy('overwrite', [
    { a: 1, b: 2 },
    { a: 10, c: 3 },
    { a: 100, b: 20 }
  ]);
  console.log('合并结果:', overwriteResult.merged);
  console.log('冲突:', overwriteResult.conflicts);
  
  // 测试智能合并
  console.log('\n测试智能合并:');
  const smartResult = merger.applyStrategy('smart', [
    { name: 'Alice', age: 25 },
    { name: 'Bob', age: 30 },
    { name: 'Charlie', age: 35 }
  ]);
  console.log('合并结果:', smartResult.merged);
  console.log('冲突数量:', smartResult.conflicts.length);
  
  // 测试聚合合并
  console.log('\n测试聚合合并:');
  const aggResult = merger.applyStrategy('aggregate', [
    [10, 20, 30],
    [40, 50],
    [60]
  ], { operation: 'avg' });
  console.log('平均值:', aggResult.merged);
}

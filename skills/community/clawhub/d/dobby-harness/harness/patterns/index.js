/**
 * Harness Patterns - 任务分解模式库索引
 * 
 * 导出所有可用的任务分解模式
 */

import parallelPattern from './parallel.js';
import sequentialPattern from './sequential.js';
import mapReducePattern from './map-reduce.js';
import pipelinePattern from './pipeline.js';
import fanOutPattern from './fan-out.js';

/**
 * 模式注册表
 */
export const patterns = {
  /**
   * parallel - 完全并行
   * 所有子任务同时执行，无依赖关系
   */
  parallel: parallelPattern,

  /**
   * sequential - 顺序执行
   * 每个任务依赖前一个任务的完成
   */
  sequential: sequentialPattern,

  /**
   * map-reduce - 映射归约
   * 先并行处理，再聚合结果
   */
  'map-reduce': mapReducePattern,

  /**
   * pipeline - 流水线
   * 多阶段处理，阶段内并行，阶段间顺序
   */
  pipeline: pipelinePattern,

  /**
   * fan-out - 扇出
   * 一个任务分解为多个独立探索，可选扇入聚合
   */
  'fan-out': fanOutPattern,
};

/**
 * 获取模式
 * @param {string} name - 模式名称
 * @returns {Object} 模式对象
 */
export function getPattern(name) {
  const pattern = patterns[name];
  if (!pattern) {
    const available = Object.keys(patterns).join(', ');
    throw new Error(`Unknown pattern: ${name}. Available: ${available}`);
  }
  return pattern;
}

/**
 * 注册自定义模式
 * @param {string} name - 模式名称
 * @param {Object} pattern - 模式对象（需包含 decompose, aggregate, validate）
 */
export function registerPattern(name, pattern) {
  if (!pattern.decompose || !pattern.aggregate || !pattern.validate) {
    throw new Error('Pattern must implement decompose, aggregate, and validate methods');
  }
  patterns[name] = pattern;
}

/**
 * 列出所有可用模式
 * @returns {Array<string>} 模式名称列表
 */
export function listPatterns() {
  return Object.keys(patterns);
}

/**
 * 获取模式描述
 * @param {string} name - 模式名称
 * @returns {Object} 模式信息
 */
export function getPatternInfo(name) {
  const pattern = patterns[name];
  if (!pattern) {
    return null;
  }
  return {
    name: pattern.name,
    description: pattern.description,
  };
}

export default patterns;

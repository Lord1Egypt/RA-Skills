/**
 * 动态模型路由技能 - 工具函数库
 */

import { RouterError } from '../core/types.js';

/**
 * 生成唯一ID
 */
export function generateId(prefix = ''): string {
  return `${prefix}${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 估算文本的token数量（简单版本）
 */
export function estimateTokens(text: string): number {
  // 处理空文本或只包含空白字符的情况
  if (!text || text.trim().length === 0) {
    return 0;
  }
  
  // 简单估算：英文字符约4个字符一个token，中文字符约2个字符一个token
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const otherChars = text.length - chineseChars;
  
  // 粗略估算，确保至少返回1（对于非常短的文本）
  const estimated = chineseChars / 2 + otherChars / 4;
  return Math.max(1, Math.ceil(estimated));
}

/**
 * 检测文本语言
 */
export function detectLanguage(text: string): 'zh' | 'en' | 'mixed' | 'other' {
  const chineseRegex = /[\u4e00-\u9fa5]/g;
  const englishRegex = /[a-zA-Z]/g;
  
  const chineseCount = (text.match(chineseRegex) || []).length;
  const englishCount = (text.match(englishRegex) || []).length;
  const totalChars = text.replace(/\s/g, '').length;
  
  if (totalChars === 0) return 'other';
  
  const chineseRatio = chineseCount / totalChars;
  const englishRatio = englishCount / totalChars;
  
  // 调整阈值以更好地识别混合语言
  if (chineseRatio > 0.6 && englishRatio > 0.2) return 'mixed';
  if (englishRatio > 0.6 && chineseRatio > 0.2) return 'mixed';
  if (chineseRatio > 0.7) return 'zh';
  if (englishRatio > 0.7) return 'en';
  if (chineseRatio > 0.3 && englishRatio > 0.3) return 'mixed';
  return 'other';
}

/**
 * 计算文本复杂度分数（0-1）
 */
export function calculateComplexity(text: string): number {
  let score = 0;
  
  // 基础复杂度（任何文本都有基础复杂度）
  const baseScore = 0.18; // 从0.1增加到0.18
  score += baseScore;
  
  // 基于长度（进一步降低分母）
  const lengthScore = Math.min(text.length / 150, 1) * 0.5; // 从200降到150
  score += lengthScore;
  
  // 基于特殊字符（代码、技术术语）
  const codePatterns = [
    /```[\s\S]*?```/g, // 代码块
    /def\s+\w+\(|function\s+\w+\(|class\s+\w+/g, // 函数/类定义
    /\{|\}|\(|\)|\[|\]/g, // 括号
    /import\s+|from\s+|require\(/g, // 导入语句
    /const\s+|let\s+|var\s+/g, // 变量声明
    /return\s+|if\s+|for\s+|while\s+/g, // 控制流
  ];
  
  let codeScore = 0;
  for (const pattern of codePatterns) {
    const matches = text.match(pattern);
    if (matches) {
      codeScore += matches.length * 0.12; // 从0.1增加到0.12
    }
  }
  score += Math.min(codeScore, 0.4);
  
  // 基于技术术语 - 增加权重
  const techTerms = [
    '算法', '架构', '设计', '优化', '性能', '调试', '测试', '部署', '配置', '集成',
    '函数', '程序', '代码', '系统', // 添加通用编程术语
    'algorithm', 'architecture', 'design', 'optimize', 'performance', 'debug', 'test', 'deploy', 'configure', 'integrate',
    'function', 'program', 'code', 'system',
    '复杂度', '时间复杂度', '空间复杂度', '递归', '迭代', '数据结构',
    'complexity', 'time complexity', 'space complexity', 'recursion', 'iteration', 'data structure'
  ];
  
  let termScore = 0;
  for (const term of techTerms) {
    const regex = new RegExp(term, 'gi');
    const matches = text.match(regex);
    if (matches) {
      termScore += matches.length * 0.06; // 从0.05增加到0.06
    }
  }
  score += Math.min(termScore, 0.35); // 从0.3增加到0.35
  
  // 基于问题复杂度指示词
  const complexityIndicators = [
    '如何', '为什么', '分析', '解决', '实现', '构建', '解释', '比较', '评估', '优化',
    'how', 'why', 'analyze', 'solve', 'implement', 'build', 'explain', 'compare', 'evaluate', 'optimize'
  ];
  
  let indicatorScore = 0;
  for (const indicator of complexityIndicators) {
    const regex = new RegExp(`\\b${indicator}\\b`, 'gi');
    const matches = text.match(regex);
    if (matches) {
      indicatorScore += matches.length * 0.035; // 从0.03增加到0.035
    }
  }
  score += Math.min(indicatorScore, 0.3);
  
  // 确保分数在0-1范围内
  return Math.min(Math.max(score, 0), 1);
}

/**
 * 将复杂度分数转换为分类
 */
export function complexityToCategory(score: number): 'simple' | 'medium' | 'complex' {
  if (score < 0.3) return 'simple';
  if (score < 0.7) return 'medium';
  return 'complex';
}

/**
 * 识别任务类别
 */
export function identifyCategories(text: string): string[] {
  const categories: string[] = [];
  
  // 编程相关
  const codingPatterns = [
    /代码|编程|程序|算法|函数|类|方法|变量/g,
    /code|program|algorithm|function|class|method|variable/gi,
    /```[\s\S]*?```/g, // 代码块
  ];
  
  let codingScore = 0;
  for (const pattern of codingPatterns) {
    const matches = text.match(pattern);
    if (matches) {
      codingScore += matches.length;
    }
  }
  
  if (codingScore > 0) {
    categories.push('coding');
  }
  
  // 写作相关
  const writingPatterns = [
    /写作|文章|文案|内容|描述|总结/g,
    /write|article|content|description|summary/gi,
    /润色|改写|翻译/g,
  ];
  
  let writingScore = 0;
  for (const pattern of writingPatterns) {
    const matches = text.match(pattern);
    if (matches) {
      writingScore += matches.length;
    }
  }
  
  if (writingScore > 0) {
    categories.push('writing');
  }
  
  // 分析相关
  const analysisPatterns = [
    /分析|研究|评估|比较|统计|数据/g,
    /analyze|research|evaluate|compare|statistic|data/gi,
    /报告|表格|图表/g,
  ];
  
  let analysisScore = 0;
  for (const pattern of analysisPatterns) {
    const matches = text.match(pattern);
    if (matches) {
      analysisScore += matches.length;
    }
  }
  
  if (analysisScore > 0) {
    categories.push('analysis');
  }
  
  // 推理相关
  const reasoningPatterns = [
    /推理|逻辑|思考|问题|解决/g,
    /reason|logic|think|problem|solve/gi,
    /为什么|如何|怎么办/g,
  ];
  
  let reasoningScore = 0;
  for (const pattern of reasoningPatterns) {
    const matches = text.match(pattern);
    if (matches) {
      reasoningScore += matches.length;
    }
  }
  
  if (reasoningScore > 0) {
    categories.push('reasoning');
  }
  
  // 如果没有检测到特定类别，添加通用类别
  if (categories.length === 0) {
    categories.push('general');
  }
  
  return categories;
}

/**
 * 验证配置
 */
export function validateConfig(config: any): void {
  const requiredFields = [
    'enabled',
    'learningEnabled',
    'defaultStrategy',
    'complexityThresholds',
    'scoringWeights',
    'providers',
    'learning'
  ];
  
  for (const field of requiredFields) {
    if (config[field] === undefined) {
      throw new RouterError(`配置缺少必要字段: ${field}`, 'CONFIG_ERROR');
    }
  }
  
  // 验证复杂度阈值
  const { simple, medium } = config.complexityThresholds;
  if (typeof simple !== 'number' || typeof medium !== 'number') {
    throw new RouterError('复杂度阈值必须是数字', 'CONFIG_ERROR');
  }
  
  if (simple >= medium) {
    throw new RouterError('简单阈值必须小于中等阈值', 'CONFIG_ERROR');
  }
  
  if (simple < 0 || simple > 1 || medium < 0 || medium > 1) {
    throw new RouterError('复杂度阈值必须在0-1之间', 'CONFIG_ERROR');
  }
  
  // 验证评分权重
  const weights = config.scoringWeights;
  const weightSum = Object.values(weights).reduce((sum: number, weight: any) => {
    if (typeof weight !== 'number') {
      throw new RouterError('评分权重必须是数字', 'CONFIG_ERROR');
    }
    return sum + weight;
  }, 0);
  
  if (Math.abs(weightSum - 1) > 0.01) {
    throw new RouterError('评分权重总和必须为1', 'CONFIG_ERROR');
  }
}

/**
 * 合并配置
 */
export function mergeConfig(userConfig: any, defaultConfig: any): any {
  const result = { ...defaultConfig };
  
  // 深度合并
  function deepMerge(target: any, source: any): any {
    for (const key in source) {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
        if (!target[key]) target[key] = {};
        deepMerge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
    return target;
  }
  
  return deepMerge(result, userConfig);
}

/**
 * 休眠函数
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 重试函数
 */
export async function retry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> {
  let lastError: Error;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (i < maxRetries - 1) {
        await sleep(delay * Math.pow(2, i)); // 指数退避
      }
    }
  }
  
  throw lastError!;
}

/**
 * 计算平均值
 */
export function calculateAverage(values: number[]): number {
  if (values.length === 0) return 0;
  const sum = values.reduce((a, b) => a + b, 0);
  return sum / values.length;
}

/**
 * 计算标准差
 */
export function calculateStandardDeviation(values: number[]): number {
  if (values.length < 2) return 0;
  const avg = calculateAverage(values);
  const squareDiffs = values.map(value => Math.pow(value - avg, 2));
  const avgSquareDiff = calculateAverage(squareDiffs);
  return Math.sqrt(avgSquareDiff);
}

/**
 * 限制值在范围内
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * 格式化字节大小
 */
export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * 格式化时间
 */
export function formatTime(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(2)}s`;
  if (ms < 3600000) return `${(ms / 60000).toFixed(2)}m`;
  return `${(ms / 3600000).toFixed(2)}h`;
}
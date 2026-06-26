/**
 * 任务分析器 - 智能任务理解和特征提取
 * 
 * 提供比简单关键词更精细的语义分析：
 * 1. 意图识别和分类
 * 2. 复杂度深度评估
 * 3. 领域和专业识别
 * 4. 技术要求提取
 * 5. 质量需求分析
 */

import { RouterLogger } from '../utils/logger.js';
import { type TaskDescription } from '../core/types.js';
import { 
  type TaskAnalysisResult,
  type RoutingContext
} from './types.js';

const logger = new RouterLogger({ module: 'task-analyzer' });

/**
 * 任务分类
 */
export enum TaskCategory {
  GENERAL_QA = 'general_qa',          // 通用问答
  CODE_GENERATION = 'code_generation', // 代码生成
  CODE_REVIEW = 'code_review',        // 代码审查
  DOCUMENT_ANALYSIS = 'document_analysis', // 文档分析
  DATA_ANALYSIS = 'data_analysis',    // 数据分析
  CREATIVE_WRITING = 'creative_writing', // 创意写作
  TRANSLATION = 'translation',        // 翻译
  SUMMARIZATION = 'summarization',    // 摘要
  PLANNING = 'planning',              // 规划
  PROBLEM_SOLVING = 'problem_solving', // 问题解决
  RESEARCH = 'research',              // 研究
  TUTORIAL = 'tutorial',              // 教程/解释
}

/**
 * 意图类型
 */
export enum IntentType {
  INFORMATION_SEEKING = 'information_seeking', // 信息查询
  INSTRUCTION_FOLLOWING = 'instruction_following', // 指令执行
  PROBLEM_SOLVING = 'problem_solving',         // 问题解决
  CREATION = 'creation',                       // 创造
  ANALYSIS = 'analysis',                       // 分析
  EVALUATION = 'evaluation',                   // 评估
  EXPLANATION = 'explanation',                 // 解释
  COMPARISON = 'comparison',                   // 比较
  PREDICTION = 'prediction',                   // 预测
  OPTIMIZATION = 'optimization',               // 优化
}

/**
 * 领域识别
 */
export interface DomainIdentification {
  primaryDomain: string;
  subDomains: string[];
  confidence: number;
  evidence: string[];
}

/**
 * 技术要求
 */
export interface TechnicalRequirement {
  type: 'format' | 'tool' | 'standard' | 'constraint' | 'integration';
  name: string;
  description: string;
  importance: number; // 0-1
}

/**
 * 情感/语气分析
 */
export interface SentimentAnalysis {
  urgency: number; // 0-1 紧急程度
  formality: number; // 0-1 正式程度
  complexityPreference: number; // 0-1 复杂度偏好
  tone: 'neutral' | 'formal' | 'casual' | 'technical' | 'creative';
}

/**
 * 分析器配置
 */
export interface TaskAnalyzerConfig {
  enableNLP: boolean;
  minConfidence: number;
  maxAnalysisTime: number; // 毫秒
  cacheEnabled: boolean;
  cacheTTL: number; // 秒
  
  // 权重配置
  weights: {
    length: number;
    keyword: number;
    structure: number;
    domain: number;
    intent: number;
  };
  
  // 阈值配置
  thresholds: {
    highComplexity: number;
    mediumComplexity: number;
    requiresSpecialization: number;
  };
}

/**
 * 分析缓存项
 */
interface AnalysisCacheItem {
  taskHash: string;
  analysis: TaskAnalysisResult;
  timestamp: number;
  hits: number;
}

/**
 * 任务分析器
 */
export class TaskAnalyzer {
  private config: TaskAnalyzerConfig;
  private analysisCache: Map<string, AnalysisCacheItem> = new Map();
  private maxCacheSize: number = 100;
  
  // 关键词库
  private keywordLibraries = {
    // 技术领域关键词
    technicalDomains: {
      programming: ['代码', '编程', '函数', '类', '算法', '数据结构', 'bug', '错误', '调试', '测试', 'API', 'SDK'],
      web: ['网页', '前端', '后端', 'HTML', 'CSS', 'JavaScript', 'React', 'Vue', 'Node.js', '服务器'],
      mobile: ['移动', 'iOS', 'Android', '应用', 'APP', '手机', '平板'],
      data: ['数据', '数据库', 'SQL', 'NoSQL', '分析', '统计', '机器学习', 'AI', '模型'],
      devops: ['部署', '服务器', '容器', 'Docker', 'Kubernetes', 'CI/CD', '监控'],
      security: ['安全', '加密', '认证', '授权', '漏洞', '攻击', '防御'],
    },
    
    // 意图关键词
    intentKeywords: {
      information: ['什么', '如何', '为什么', '哪个', '哪里', '何时', '谁', '多少'],
      instruction: ['请', '帮我', '制作', '创建', '生成', '写', '做', '完成'],
      problem: ['问题', '错误', 'bug', '故障', '解决', '修复', '调试', '排查'],
      analysis: ['分析', '评估', '检查', '审查', '诊断', '研究', '调查'],
      comparison: ['对比', '比较', '区别', '差异', '优劣', '优缺点'],
      explanation: ['解释', '说明', '讲解', '介绍', '理解', '含义'],
      creation: ['创意', '创新', '设计', '构思', '想象', '创作', '故事'],
    },
    
    // 复杂度指标
    complexityIndicators: {
      high: ['详细', '全面', '深入', '复杂', '高级', '专业', '专家', '深度'],
      medium: ['一般', '普通', '标准', '基本', '常见', '通常'],
      low: ['简单', '快速', '简短', '简要', '基础', '入门'],
    },
    
    // 质量要求关键词
    qualityKeywords: {
      accuracy: ['准确', '精确', '正确', '无误', '可靠', '可信'],
      creativity: ['创意', '创新', '独特', '新颖', '有趣', '想象力'],
      thoroughness: ['详细', '全面', '完整', '深入', '彻底', '周密'],
      speed: ['快速', '及时', '立即', '马上', '尽快', '紧急'],
    },
  };
  
  constructor(config?: Partial<TaskAnalyzerConfig>) {
    this.config = {
      enableNLP: true,
      minConfidence: 0.6,
      maxAnalysisTime: 5000, // 5秒
      cacheEnabled: true,
      cacheTTL: 3600, // 1小时
      weights: {
        length: 0.2,
        keyword: 0.3,
        structure: 0.25,
        domain: 0.15,
        intent: 0.1,
      },
      thresholds: {
        highComplexity: 7,
        mediumComplexity: 4,
        requiresSpecialization: 0.7,
      },
      ...config,
    };
    
    logger.info('任务分析器初始化完成', {
      cacheEnabled: this.config.cacheEnabled,
      maxAnalysisTime: this.config.maxAnalysisTime,
    });
  }
  
  /**
   * 分析任务（主入口）
   */
  async analyze(task: TaskDescription, context?: RoutingContext): Promise<TaskAnalysisResult> {
    const startTime = Date.now();
    const taskId = task.id || `task_${Date.now()}`;
    
    logger.debug('开始任务分析', {
      taskId,
      contentLength: task.content.length,
      language: task.language,
    });
    
    try {
      // 1. 检查缓存
      const cachedAnalysis = this.getFromCache(task);
      if (cachedAnalysis) {
        logger.debug('使用缓存分析结果', { taskId, cacheHit: true });
        return cachedAnalysis;
      }
      
      // 2. 执行分析
      const analysis = await this.performAnalysis(task, context, startTime);
      
      // 3. 缓存结果
      if (this.config.cacheEnabled) {
        this.addToCache(task, analysis);
      }
      
      const analysisTime = Date.now() - startTime;
      logger.info('任务分析完成', {
        taskId,
        complexity: analysis.characteristics.complexity,
        analysisTime,
        confidence: this.calculateAnalysisConfidence(analysis),
      });
      
      return analysis;
      
    } catch (error) {
      const analysisTime = Date.now() - startTime;
      logger.error('任务分析失败', error as Error, { taskId, analysisTime });
      
      // 返回默认分析结果
      return this.createFallbackAnalysis(task);
    }
  }
  
  /**
   * 批量分析
   */
  async batchAnalyze(tasks: TaskDescription[], context?: RoutingContext): Promise<TaskAnalysisResult[]> {
    logger.debug('开始批量任务分析', { taskCount: tasks.length });
    
    const startTime = Date.now();
    const results: TaskAnalysisResult[] = [];
    
    // 顺序处理，确保每个任务有足够时间分析
    for (const task of tasks) {
      try {
        const result = await this.analyze(task, context);
        results.push(result);
      } catch (error) {
        logger.error('批量分析中单个任务失败', error as Error, { taskId: task.id });
        
        // 添加回退分析结果
        const fallbackResult = this.createFallbackAnalysis(task);
        results.push(fallbackResult);
      }
    }
    
    const totalTime = Date.now() - startTime;
    logger.info('批量任务分析完成', {
      taskCount: tasks.length,
      successCount: results.filter(r => r.characteristics.complexity > 0).length,
      totalTime,
      avgTimePerTask: totalTime / tasks.length,
    });
    
    return results;
  }
  
  /**
   * 获取配置
   */
  getConfig(): TaskAnalyzerConfig {
    return { ...this.config };
  }
  
  /**
   * 更新配置
   */
  updateConfig(config: Partial<TaskAnalyzerConfig>): void {
    this.config = { ...this.config, ...config };
    logger.info('任务分析器配置更新', { updates: config });
  }
  
  /**
   * 清理缓存
   */
  clearCache(): void {
    const cacheSize = this.analysisCache.size;
    this.analysisCache.clear();
    logger.info('分析缓存已清理', { clearedEntries: cacheSize });
  }
  
  /**
   * 获取缓存统计
   */
  getCacheStats(): { size: number; hits: number; hitRate: number } {
    let totalHits = 0;
    
    for (const item of this.analysisCache.values()) {
      totalHits += item.hits;
    }
    
    const hitRate = this.analysisCache.size > 0 
      ? totalHits / (this.analysisCache.size * 10) // 简化计算
      : 0;
    
    return {
      size: this.analysisCache.size,
      hits: totalHits,
      hitRate: Math.min(1, hitRate),
    };
  }
  
  // ============== 私有方法 ==============
  
  /**
   * 执行实际分析
   */
  private async performAnalysis(
    task: TaskDescription,
    _context: RoutingContext | undefined,
    startTime: number
  ): Promise<TaskAnalysisResult> {
    // 并行执行各项分析
    const [
      characteristics,
      domainIdentification,
      intentAnalysis,
      technicalRequirements,
      _sentimentAnalysis,
      qualityRequirements,
      splittingPotential,
    ] = await Promise.all([
      this.analyzeCharacteristics(task),
      this.identifyDomain(task),
      this.analyzeIntent(task),
      this.extractTechnicalRequirements(task),
      this.analyzeSentiment(task),
      this.analyzeQualityRequirements(task),
      this.analyzeSplittingPotential(task),
    ]);
    
    // 构建所需能力列表
    const requiredCapabilities = this.determineRequiredCapabilities(
      task,
      characteristics,
      domainIdentification,
      intentAnalysis,
      technicalRequirements
    );
    
    // 检查超时
    const currentTime = Date.now();
    if (currentTime - startTime > this.config.maxAnalysisTime) {
      logger.warn('任务分析超时', { 
        taskId: task.id,
        elapsedTime: currentTime - startTime,
        maxTime: this.config.maxAnalysisTime,
      });
    }
    
    return {
      taskId: task.id,
      characteristics,
      requiredCapabilities,
      qualityRequirements,
      splittingPotential,
    };
  }
  
  /**
   * 分析任务特征
   */
  private async analyzeCharacteristics(task: TaskDescription): Promise<TaskAnalysisResult['characteristics']> {
    const content = task.content;
    const length = content.length;
    
    // 1. 基础特征
    const tokenEstimate = this.estimateTokens(content, task.language);
    
    // 2. 复杂度评估（多维度）
    const complexityScore = await this.calculateComplexityScore(content, task.language);
    
    // 3. 内容类型分析
    const contentType = await this.analyzeContentType(content);
    
    // 4. 结构分析
    // @ts-ignore - 变量声明但未使用
    const _structureAnalysis = this.analyzeStructure(content);
    
    return {
      complexity: complexityScore,
      length,
      tokenEstimate,
      contentType,
      technicalRequirements: [], // 在单独方法中提取
      domain: await this.inferDomain(content),
      intent: await this.inferIntent(content),
    };
  }
  
  /**
   * 估算token数量
   */
  private estimateTokens(content: string, _language: string): number {
    // 简化估算：中文字符和英文字符不同处理
    let tokenCount = 0;
    
    if (_language === 'zh' || _language === 'mixed') {
      // 中文：大约每个字符1-2个token
      const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
      tokenCount += chineseChars * 1.5;
      
      // 英文和其他字符
      const otherChars = content.length - chineseChars;
      tokenCount += otherChars * 0.25;
    } else {
      // 英文：大约每4个字符1个token
      tokenCount = Math.ceil(content.length / 4);
    }
    
    return Math.max(10, tokenCount); // 最少10个token
  }
  
  /**
   * 计算复杂度分数
   */
  private async calculateComplexityScore(content: string, _language: string): Promise<number> {
    let score = 3; // 基础分数
    
    // 1. 长度因素
    const lengthFactor = Math.min(content.length / 500, 3); // 每500字符加1分，最多3分
    score += lengthFactor;
    
    // 2. 关键词检测
    const keywordScore = this.calculateKeywordComplexity(content);
    score += keywordScore;
    
    // 3. 结构复杂度
    const structureScore = this.analyzeStructuralComplexity(content);
    score += structureScore;
    
    // 4. 领域专业度
    const domainScore = await this.assessDomainComplexity(content);
    score += domainScore;
    
    // 5. 问题类型
    const questionTypeScore = this.assessQuestionComplexity(content);
    score += questionTypeScore;
    
    // 限制在1-10之间
    return Math.max(1, Math.min(10, score));
  }
  
  /**
   * 关键词复杂度计算
   */
  private calculateKeywordComplexity(content: string): number {
    let score = 0;
    const lowerContent = content.toLowerCase();
    
    // 高复杂度关键词
    for (const keyword of this.keywordLibraries.complexityIndicators.high) {
      if (lowerContent.includes(keyword.toLowerCase())) {
        score += 0.5;
        break; // 找到就加分
      }
    }
    
    // 技术关键词检测
    for (const [_domain, keywords] of Object.entries(this.keywordLibraries.technicalDomains)) {
      for (const keyword of keywords) {
        if (lowerContent.includes(keyword.toLowerCase())) {
          score += 0.3;
          break; // 每个领域最多加一次
        }
      }
    }
    
    // 问题解决关键词
    const problemKeywords = this.keywordLibraries.intentKeywords.problem;
    for (const keyword of problemKeywords) {
      if (lowerContent.includes(keyword.toLowerCase())) {
        score += 0.4;
        break;
      }
    }
    
    return Math.min(2, score); // 最多2分
  }
  
  /**
   * 分析结构复杂度
   */
  private analyzeStructuralComplexity(content: string): number {
    let score = 0;
    
    // 段落数量
    const paragraphCount = (content.match(/\n\s*\n/g) || []).length + 1;
    score += Math.min(paragraphCount / 3, 1); // 最多1分
    
    // 列表项
    const listItemCount = (content.match(/[-*•]\s/g) || []).length;
    score += Math.min(listItemCount / 5, 0.5); // 最多0.5分
    
    // 问题数量
    const questionCount = (content.match(/[?？]/g) || []).length;
    score += Math.min(questionCount / 3, 0.5); // 最多0.5分
    
    // 代码块
    const codeBlockCount = (content.match(/```/g) || []).length / 2;
    score += Math.min(codeBlockCount, 1); // 最多1分
    
    return Math.min(2, score); // 最多2分
  }
  
  /**
   * 评估领域复杂度
   */
  private async assessDomainComplexity(content: string): Promise<number> {
    // 检测高复杂度领域
    const complexDomains = ['机器学习', '人工智能', '密码学', '分布式系统', '编译器', '操作系统'];
    const lowerContent = content.toLowerCase();
    
    for (const domain of complexDomains) {
      if (lowerContent.includes(domain.toLowerCase())) {
        return 1.5;
      }
    }
    
    // 检测中等复杂度领域
    const mediumDomains = ['数据库', '网络', '安全', '算法', '数据结构'];
    for (const domain of mediumDomains) {
      if (lowerContent.includes(domain.toLowerCase())) {
        return 0.8;
      }
    }
    
    return 0;
  }
  
  /**
   * 评估问题类型复杂度
   */
  private assessQuestionComplexity(content: string): number {
    const lowerContent = content.toLowerCase();
    
    // 开放式问题通常更复杂
    const openEndedIndicators = [
      '如何', '为什么', '分析', '评估', '设计', '实现', '优化',
      'how', 'why', 'analyze', 'evaluate', 'design', 'implement', 'optimize'
    ];
    
    for (const indicator of openEndedIndicators) {
      if (lowerContent.includes(indicator.toLowerCase())) {
        return 1.0;
      }
    }
    
    // 封闭式问题较简单
    const closedIndicators = [
      '什么', '哪个', '是否', '有没有', '多少',
      'what', 'which', 'is', 'does', 'have', 'how many'
    ];
    
    for (const indicator of closedIndicators) {
      if (lowerContent.includes(indicator.toLowerCase())) {
        return 0.3;
      }
    }
    
    return 0.5; // 中性
  }
  
  /**
   * 分析内容类型
   */
  private async analyzeContentType(content: string): Promise<Array<'text' | 'code' | 'data' | 'query' | 'instruction' | 'creative'>> {
    const types: Array<'text' | 'code' | 'data' | 'query' | 'instruction' | 'creative'> = ['text'];
    const lowerContent = content.toLowerCase();
    
    // 代码检测
    const codePatterns = ['```', 'function', 'class', 'def ', 'import ', 'export ', 'const ', 'let ', 'var ', 'print('];
    if (codePatterns.some(pattern => lowerContent.includes(pattern))) {
      types.push('code');
    }
    
    // 数据检测
    const dataPatterns = ['数据', '统计', '数字', '百分比', '图表', '表格', 'data', 'statistics'];
    if (dataPatterns.some(pattern => lowerContent.includes(pattern))) {
      types.push('data');
    }
    
    // 查询检测
    const queryPatterns = ['?', '？', '什么', '如何', '为什么', '哪个', 'what', 'how', 'why', 'which'];
    if (queryPatterns.some(pattern => lowerContent.includes(pattern))) {
      types.push('query');
    }
    
    // 指令检测
    const instructionPatterns = ['请', '帮我', '制作', '创建', '生成', '写', '做', 'please', 'help', 'create', 'generate'];
    if (instructionPatterns.some(pattern => lowerContent.includes(pattern))) {
      types.push('instruction');
    }
    
    // 创意检测
    const creativePatterns = ['故事', '诗歌', '创意', '想象', '创新', '有趣', 'story', 'poem', 'creative', 'imagine'];
    if (creativePatterns.some(pattern => lowerContent.includes(pattern))) {
      types.push('creative');
    }
    
    return types;
  }
  
  /**
   * 分析结构
   */
  private analyzeStructure(content: string): any {
    const lines = content.split('\n');
    
    return {
      lineCount: lines.length,
      paragraphCount: (content.match(/\n\s*\n/g) || []).length + 1,
      avgLineLength: lines.reduce((sum, line) => sum + line.length, 0) / lines.length,
      hasHeadings: /^#+\s/.test(content) || /^(标题|题目|主题):/.test(content),
      hasLists: /[-*•]\s/.test(content) || /\d+\.\s/.test(content),
      hasCodeBlocks: /```/.test(content),
      hasTables: /\|.*\|/.test(content),
    };
  }
  
  /**
   * 推断领域
   */
  private async inferDomain(content: string): Promise<string> {
    const lowerContent = content.toLowerCase();
    
    // 检查各个技术领域
    for (const [domain, keywords] of Object.entries(this.keywordLibraries.technicalDomains)) {
      for (const keyword of keywords) {
        if (lowerContent.includes(keyword.toLowerCase())) {
          return domain;
        }
      }
    }
    
    // 默认领域
    return 'general';
  }
  
  /**
   * 推断意图
   */
  private async inferIntent(content: string): Promise<string> {
    const lowerContent = content.toLowerCase();
    
    // 检查各种意图
    for (const [intentType, keywords] of Object.entries(this.keywordLibraries.intentKeywords)) {
      for (const keyword of keywords) {
        if (lowerContent.includes(keyword.toLowerCase())) {
          return intentType;
        }
      }
    }
    
    // 默认意图
    return 'information';
  }
  
  /**
   * 估算可读性
   */
  // @ts-ignore - 方法未使用但保留
  private estimateReadability(content: string): number {
    // 简化可读性评分：基于句子长度和复杂度
    const sentences = content.split(/[.!?。！？]/).filter(s => s.trim().length > 0);
    
    if (sentences.length === 0) {
      return 0.5;
    }
    
    const avgSentenceLength = sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length;
    
    // 句子越短，可读性越高（简化）
    const readability = Math.max(0.1, Math.min(1, 100 / avgSentenceLength));
    
    return readability;
  }
  
  /**
   * 识别领域
   */
  private async identifyDomain(task: TaskDescription): Promise<DomainIdentification> {
    const content = task.content.toLowerCase();
    const domains: string[] = [];
    const evidence: string[] = [];
    
    // 检查各个技术领域
    for (const [domain, keywords] of Object.entries(this.keywordLibraries.technicalDomains)) {
      for (const keyword of keywords) {
        if (content.includes(keyword.toLowerCase())) {
          domains.push(domain);
          evidence.push(`发现关键词: ${keyword}`);
          break; // 每个领域找到第一个关键词就添加
        }
      }
    }
    
    // 如果没有检测到特定领域，使用通用领域
    if (domains.length === 0) {
      domains.push('general');
      evidence.push('未检测到特定领域关键词');
    }
    
    return {
      primaryDomain: domains[0],
      subDomains: domains.slice(1),
      confidence: Math.min(0.9, 0.5 + domains.length * 0.1),
      evidence,
    };
  }
  
  /**
   * 分析意图
   */
  private async analyzeIntent(task: TaskDescription): Promise<{
    primaryIntent: IntentType;
    secondaryIntents: IntentType[];
    confidence: number;
  }> {
    const content = task.content.toLowerCase();
    const intents: IntentType[] = [];
    
    // 基于关键词的意图识别
    if (this.keywordLibraries.intentKeywords.information.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.INFORMATION_SEEKING);
    }
    
    if (this.keywordLibraries.intentKeywords.instruction.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.INSTRUCTION_FOLLOWING);
    }
    
    if (this.keywordLibraries.intentKeywords.problem.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.PROBLEM_SOLVING);
    }
    
    if (this.keywordLibraries.intentKeywords.analysis.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.ANALYSIS);
    }
    
    if (this.keywordLibraries.intentKeywords.comparison.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.COMPARISON);
    }
    
    if (this.keywordLibraries.intentKeywords.explanation.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.EXPLANATION);
    }
    
    if (this.keywordLibraries.intentKeywords.creation.some(kw => content.includes(kw.toLowerCase()))) {
      intents.push(IntentType.CREATION);
    }
    
    // 默认意图
    if (intents.length === 0) {
      intents.push(IntentType.INFORMATION_SEEKING);
    }
    
    return {
      primaryIntent: intents[0],
      secondaryIntents: intents.slice(1),
      confidence: Math.min(0.9, 0.6 + intents.length * 0.1),
    };
  }
  
  /**
   * 提取技术要求
   */
  private async extractTechnicalRequirements(task: TaskDescription): Promise<TechnicalRequirement[]> {
    const requirements: TechnicalRequirement[] = [];
    const content = task.content.toLowerCase();
    
    // 格式要求检测
    if (content.includes('markdown') || content.includes('md')) {
      requirements.push({
        type: 'format',
        name: 'Markdown',
        description: '需要Markdown格式输出',
        importance: 0.8,
      });
    }
    
    if (content.includes('json') || content.includes('yaml') || content.includes('xml')) {
      requirements.push({
        type: 'format',
        name: '结构化数据',
        description: '需要特定数据格式输出',
        importance: 0.7,
      });
    }
    
    // 工具/技术栈检测
    const techStackKeywords = [
      { name: 'Python', keywords: ['python', 'pandas', 'numpy', 'tensorflow', 'pytorch'] },
      { name: 'JavaScript', keywords: ['javascript', 'js', 'node', 'react', 'vue'] },
      { name: 'Java', keywords: ['java', 'spring', 'maven'] },
      { name: 'SQL', keywords: ['sql', 'mysql', 'postgresql', 'database'] },
      { name: 'Docker', keywords: ['docker', 'container', '镜像'] },
    ];
    
    for (const tech of techStackKeywords) {
      for (const keyword of tech.keywords) {
        if (content.includes(keyword.toLowerCase())) {
          requirements.push({
            type: 'tool',
            name: tech.name,
            description: `涉及${tech.name}技术栈`,
            importance: 0.6,
          });
          break;
        }
      }
    }
    
    // 约束检测
    if (content.includes('简短') || content.includes('简洁') || content.includes('简要')) {
      requirements.push({
        type: 'constraint',
        name: '简洁性',
        description: '要求输出简洁明了',
        importance: 0.7,
      });
    }
    
    if (content.includes('详细') || content.includes('全面') || content.includes('完整')) {
      requirements.push({
        type: 'constraint',
        name: '完整性',
        description: '要求输出详细完整',
        importance: 0.8,
      });
    }
    
    return requirements;
  }
  
  /**
   * 分析情感/语气
   */
  private async analyzeSentiment(task: TaskDescription): Promise<SentimentAnalysis> {
    const content = task.content.toLowerCase();
    
    // 紧急程度检测
    let urgency = 0.3; // 基础紧急程度
    const urgencyKeywords = ['紧急', '尽快', '马上', '立即', 'urgent', 'asap', 'quickly'];
    if (urgencyKeywords.some(kw => content.includes(kw.toLowerCase()))) {
      urgency = 0.8;
    }
    
    // 正式程度检测
    let formality = 0.5; // 中性
    const formalKeywords = ['尊敬的', '您好', '敬礼', '此致', '正式', 'formal'];
    const casualKeywords = ['哈哈', '嘿嘿', '搞笑', '轻松', 'casual', 'funny'];
    
    if (formalKeywords.some(kw => content.includes(kw.toLowerCase()))) {
      formality = 0.8;
    } else if (casualKeywords.some(kw => content.includes(kw.toLowerCase()))) {
      formality = 0.2;
    }
    
    // 语气类型
    let tone: SentimentAnalysis['tone'] = 'neutral';
    
    if (content.includes('技术') || content.includes('专业') || content.includes('technical')) {
      tone = 'technical';
    } else if (content.includes('创意') || content.includes('故事') || content.includes('creative')) {
      tone = 'creative';
    } else if (formality > 0.7) {
      tone = 'formal';
    } else if (formality < 0.3) {
      tone = 'casual';
    }
    
    return {
      urgency,
      formality,
      complexityPreference: 0.5, // 中性
      tone,
    };
  }
  
  /**
   * 分析质量要求
   */
  private async analyzeQualityRequirements(task: TaskDescription): Promise<TaskAnalysisResult['qualityRequirements']> {
    const content = task.content.toLowerCase();
    
    // 基于关键词的质量要求分析
    let accuracy = 0.7;
    let creativity = 0.3;
    let thoroughness = 0.6;
    let speed = 0.8;
    
    // 准确性要求
    for (const keyword of this.keywordLibraries.qualityKeywords.accuracy) {
      if (content.includes(keyword.toLowerCase())) {
        accuracy = 0.9;
        break;
      }
    }
    
    // 创造性要求
    for (const keyword of this.keywordLibraries.qualityKeywords.creativity) {
      if (content.includes(keyword.toLowerCase())) {
        creativity = 0.8;
        break;
      }
    }
    
    // 完整性要求
    for (const keyword of this.keywordLibraries.qualityKeywords.thoroughness) {
      if (content.includes(keyword.toLowerCase())) {
        thoroughness = 0.9;
        break;
      }
    }
    
    // 速度要求
    for (const keyword of this.keywordLibraries.qualityKeywords.speed) {
      if (content.includes(keyword.toLowerCase())) {
        speed = 0.9;
        break;
      }
    }
    
    // 根据任务复杂度调整
    const estimatedComplexity = await this.estimateTaskComplexity(content);
    if (estimatedComplexity > 7) {
      // 高复杂度任务通常需要更高的准确性和完整性
      accuracy = Math.max(accuracy, 0.8);
      thoroughness = Math.max(thoroughness, 0.8);
      speed = Math.min(speed, 0.6); // 降低速度要求
    }
    
    return {
      accuracy,
      creativity,
      thoroughness,
      speed,
    };
  }
  
  /**
   * 分析拆分潜力
   */
  private async analyzeSplittingPotential(task: TaskDescription): Promise<TaskAnalysisResult['splittingPotential']> {
    const content = task.content;
    const length = content.length;
    
    // 基础条件：足够长且复杂
    const estimatedComplexity = await this.estimateTaskComplexity(content);
    const baseCondition = length > 300 && estimatedComplexity > 5;
    
    if (!baseCondition) {
      return { canSplit: false };
    }
    
    // 检测多部分任务
    const hasMultipleQuestions = (content.match(/[?？]/g) || []).length > 1;
    const hasNumberedItems = /\d+\.\s/.test(content) || /第[一二三四五六七八九十]/.test(content);
    const hasTaskList = /任务[一二三四五六七八九十]/.test(content) || /步骤[一二三四五六七八九十]/.test(content);
    
    const canSplit = hasMultipleQuestions || hasNumberedItems || hasTaskList;
    
    if (!canSplit) {
      return { canSplit: false };
    }
    
    // 估算最优拆分数量
    let optimalSplits = 2; // 默认
    
    if (hasMultipleQuestions) {
      optimalSplits = Math.min(3, (content.match(/[?？]/g) || []).length);
    } else if (hasNumberedItems) {
      const numberedMatches = content.match(/\d+\.\s/g) || [];
      optimalSplits = Math.min(4, numberedMatches.length);
    }
    
    // 生成拆分点建议
    const splitPoints: string[] = [];
    for (let i = 1; i <= optimalSplits; i++) {
      splitPoints.push(`第${i}部分: 子任务${i}`);
    }
    
    return {
      canSplit: true,
      optimalSplits,
      splitPoints,
    };
  }
  
  /**
   * 确定所需能力
   */
  private determineRequiredCapabilities(
    _task: TaskDescription,
    characteristics: TaskAnalysisResult['characteristics'],
    domain: DomainIdentification,
    intent: any,
    technicalRequirements: TechnicalRequirement[]
  ): TaskAnalysisResult['requiredCapabilities'] {
    const capabilities: TaskAnalysisResult['requiredCapabilities'] = [];
    
    // 1. 基于领域的能力
    const domainCapabilities = this.mapDomainToCapabilities(domain.primaryDomain);
    for (const capability of domainCapabilities) {
      capabilities.push({
        capability,
        importance: domain.confidence * 0.8,
        evidence: `领域需求: ${domain.primaryDomain}`,
      });
    }
    
    // 2. 基于意图的能力
    const intentCapabilities = this.mapIntentToCapabilities(intent.primaryIntent);
    for (const capability of intentCapabilities) {
      capabilities.push({
        capability,
        importance: intent.confidence * 0.7,
        evidence: `意图需求: ${intent.primaryIntent}`,
      });
    }
    
    // 3. 基于技术要求的能力
    for (const requirement of technicalRequirements) {
      const techCapabilities = this.mapTechnicalRequirementToCapabilities(requirement);
      for (const capability of techCapabilities) {
        capabilities.push({
          capability,
          importance: requirement.importance,
          evidence: `技术要求: ${requirement.name}`,
        });
      }
    }
    
    // 4. 基于内容类型的能力
    for (const contentType of characteristics.contentType) {
      const typeCapabilities = this.mapContentTypeToCapabilities(contentType);
      for (const capability of typeCapabilities) {
        capabilities.push({
          capability,
          importance: 0.6,
          evidence: `内容类型: ${contentType}`,
        });
      }
    }
    
    // 去重和合并
    const uniqueCapabilities = this.mergeDuplicateCapabilities(capabilities);
    
    // 确保至少有一个通用能力
    if (uniqueCapabilities.length === 0) {
      uniqueCapabilities.push({
        capability: 'general',
        importance: 0.5,
        evidence: '通用任务需求',
      });
    }
    
    return uniqueCapabilities;
  }
  
  /**
   * 映射领域到能力
   */
  private mapDomainToCapabilities(domain: string): string[] {
    const capabilityMap: Record<string, string[]> = {
      programming: ['coding', 'debugging', 'algorithm'],
      web: ['coding', 'frontend', 'backend'],
      mobile: ['coding', 'mobile'],
      data: ['analysis', 'data_processing', 'statistics'],
      devops: ['system', 'deployment', 'automation'],
      security: ['security', 'analysis', 'system'],
    };
    
    return capabilityMap[domain] || ['general'];
  }
  
  /**
   * 映射意图到能力
   */
  private mapIntentToCapabilities(intent: IntentType): string[] {
    const capabilityMap: Record<IntentType, string[]> = {
      [IntentType.INFORMATION_SEEKING]: ['knowledge', 'research'],
      [IntentType.INSTRUCTION_FOLLOWING]: ['execution', 'detail'],
      [IntentType.PROBLEM_SOLVING]: ['analysis', 'debugging', 'troubleshooting'],
      [IntentType.ANALYSIS]: ['analysis', 'critical_thinking'],
      [IntentType.EVALUATION]: ['evaluation', 'judgment'],
      [IntentType.EXPLANATION]: ['explanation', 'teaching'],
      [IntentType.COMPARISON]: ['analysis', 'comparison'],
      [IntentType.PREDICTION]: ['prediction', 'analysis'],
      [IntentType.OPTIMIZATION]: ['optimization', 'analysis'],
      [IntentType.CREATION]: ['creative', 'generation'],
    };
    
    return capabilityMap[intent] || ['general'];
  }
  
  /**
   * 映射技术要求到能力
   */
  private mapTechnicalRequirementToCapabilities(requirement: TechnicalRequirement): string[] {
    switch (requirement.type) {
      case 'format':
        return ['formatting', 'attention_to_detail'];
      case 'tool':
        return ['technical', 'tool_specific'];
      case 'standard':
        return ['compliance', 'attention_to_detail'];
      case 'constraint':
        if (requirement.name.includes('简洁')) return ['conciseness'];
        if (requirement.name.includes('完整')) return ['thoroughness'];
        return ['constraint_adherence'];
      case 'integration':
        return ['integration', 'system_thinking'];
      default:
        return ['technical'];
    }
  }
  
  /**
   * 映射内容类型到能力
   */
  private mapContentTypeToCapabilities(contentType: string): string[] {
    switch (contentType) {
      case 'code':
        return ['coding', 'technical'];
      case 'data':
        return ['analysis', 'data_processing'];
      case 'query':
        return ['research', 'information_retrieval'];
      case 'instruction':
        return ['execution', 'detail'];
      case 'creative':
        return ['creative', 'imagination'];
      default:
        return ['general'];
    }
  }
  
  /**
   * 合并重复能力
   */
  private mergeDuplicateCapabilities(capabilities: TaskAnalysisResult['requiredCapabilities']): TaskAnalysisResult['requiredCapabilities'] {
    const capabilityMap = new Map<string, TaskAnalysisResult['requiredCapabilities'][0]>();
    
    for (const capability of capabilities) {
      const existing = capabilityMap.get(capability.capability);
      
      if (existing) {
        // 合并重要性（取最高）
        existing.importance = Math.max(existing.importance, capability.importance);
        // 合并证据
        existing.evidence += `; ${capability.evidence}`;
      } else {
        capabilityMap.set(capability.capability, { ...capability });
      }
    }
    
    return Array.from(capabilityMap.values())
      .sort((a, b) => b.importance - a.importance); // 按重要性排序
  }
  
  /**
   * 估算任务复杂度（快速）
   */
  private async estimateTaskComplexity(content: string): Promise<number> {
    // 快速估算：基于长度和关键词
    const lengthScore = Math.min(content.length / 200, 3);
    let keywordScore = 0;
    
    // 检测高复杂度关键词
    const complexityKeywords = [
      ...this.keywordLibraries.complexityIndicators.high,
      ...Object.values(this.keywordLibraries.technicalDomains).flat(),
    ];
    
    const lowerContent = content.toLowerCase();
    for (const keyword of complexityKeywords) {
      if (lowerContent.includes(keyword.toLowerCase())) {
        keywordScore += 0.1;
        if (keywordScore >= 2) break; // 最多2分
      }
    }
    
    return Math.max(1, Math.min(10, 3 + lengthScore + keywordScore));
  }
  
  /**
   * 从缓存获取分析结果
   */
  private getFromCache(task: TaskDescription): TaskAnalysisResult | null {
    if (!this.config.cacheEnabled) {
      return null;
    }
    
    const taskHash = this.generateTaskHash(task);
    const cachedItem = this.analysisCache.get(taskHash);
    
    if (!cachedItem) {
      return null;
    }
    
    // 检查缓存是否过期
    const now = Date.now();
    if (now - cachedItem.timestamp > this.config.cacheTTL * 1000) {
      this.analysisCache.delete(taskHash);
      logger.debug('缓存项已过期', { taskHash });
      return null;
    }
    
    // 更新命中次数
    cachedItem.hits++;
    
    logger.debug('缓存命中', { 
      taskHash, 
      hits: cachedItem.hits,
      age: Math.round((now - cachedItem.timestamp) / 1000),
    });
    
    return cachedItem.analysis;
  }
  
  /**
   * 添加到缓存
   */
  private addToCache(task: TaskDescription, analysis: TaskAnalysisResult): void {
    if (!this.config.cacheEnabled) {
      return;
    }
    
    const taskHash = this.generateTaskHash(task);
    
    // 如果缓存已满，删除最旧的项
    if (this.analysisCache.size >= this.maxCacheSize) {
      const oldestKey = Array.from(this.analysisCache.entries())
        .reduce((oldest, current) => 
          current[1].timestamp < oldest[1].timestamp ? current : oldest
        )[0];
      
      this.analysisCache.delete(oldestKey);
      logger.debug('清理缓存空间', { removedKey: oldestKey });
    }
    
    this.analysisCache.set(taskHash, {
      taskHash,
      analysis,
      timestamp: Date.now(),
      hits: 0,
    });
    
    logger.debug('分析结果已缓存', { 
      taskHash, 
      cacheSize: this.analysisCache.size,
      maxSize: this.maxCacheSize,
    });
  }
  
  /**
   * 生成任务哈希
   */
  private generateTaskHash(task: TaskDescription): string {
    // 简化哈希：使用任务内容和ID
    const content = task.content.substring(0, 100) + (task.content.length > 100 ? '...' : '');
    const hashData = `${task.id}:${content}:${task.language}`;
    
    // 简单哈希函数
    let hash = 0;
    for (let i = 0; i < hashData.length; i++) {
      const char = hashData.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为32位整数
    }
    
    return `task_${Math.abs(hash).toString(36)}`;
  }
  
  /**
   * 计算分析置信度
   */
  private calculateAnalysisConfidence(analysis: TaskAnalysisResult): number {
    // 基于多个因素计算置信度
    let confidence = 0.5; // 基础置信度
    
    // 复杂度越高，分析可能越准确
    confidence += analysis.characteristics.complexity * 0.03;
    
    // 能力需求明确度
    if (analysis.requiredCapabilities.length > 0) {
      const avgImportance = analysis.requiredCapabilities.reduce((sum, c) => sum + c.importance, 0) 
        / analysis.requiredCapabilities.length;
      confidence += avgImportance * 0.2;
    }
    
    // 质量要求明确度
    const qualityScores = Object.values(analysis.qualityRequirements);
    const qualityDeviation = Math.max(...qualityScores) - Math.min(...qualityScores);
    confidence += (1 - qualityDeviation) * 0.1;
    
    return Math.min(0.95, Math.max(0.3, confidence));
  }
  
  /**
   * 创建回退分析
   */
  private createFallbackAnalysis(task: TaskDescription): TaskAnalysisResult {
    logger.warn('使用回退分析', { taskId: task.id });
    
    return {
      taskId: task.id,
      characteristics: {
        complexity: 5,
        length: task.content.length,
        tokenEstimate: Math.ceil(task.content.length / 3),
        contentType: ['text'],
        technicalRequirements: [],
        domain: 'general',
        intent: 'information',
      },
      requiredCapabilities: [
        {
          capability: 'general',
          importance: 0.5,
          evidence: '通用任务需求（回退分析）',
        },
      ],
      qualityRequirements: {
        accuracy: 0.7,
        creativity: 0.3,
        thoroughness: 0.6,
        speed: 0.8,
      },
      splittingPotential: {
        canSplit: false,
      },
    };
  }
}

/**
 * 任务分析器工厂
 */
export class TaskAnalyzerFactory {
  private static instance: TaskAnalyzer;
  
  static getInstance(config?: Partial<TaskAnalyzerConfig>): TaskAnalyzer {
    if (!TaskAnalyzerFactory.instance) {
      TaskAnalyzerFactory.instance = new TaskAnalyzer(config);
      logger.info('创建任务分析器单例');
    }
    
    return TaskAnalyzerFactory.instance;
  }
  
  static destroyInstance(): void {
    if (TaskAnalyzerFactory.instance) {
      TaskAnalyzerFactory.instance.clearCache();
      TaskAnalyzerFactory.instance = null as any;
      logger.info('销毁任务分析器单例');
    }
  }
}
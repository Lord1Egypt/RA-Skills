/**
 * 动态模型路由技能 - 主入口文件
 */

import { RouterLogger } from './utils/logger.js';
import { ConfigManager } from './utils/config.js';
import { DecisionEngine } from './routing/decision-engine.js';
import { estimateTokens, detectLanguage, calculateComplexity } from './utils/index.js';
import type { 
  RouterConfig, 
  RoutingDecision, 
  TaskDescription,
  ModelCapability
} from './core/types.js';
import type { 
  RoutingRequest
} from './routing/types.js';
import { RoutingStrategy } from './routing/types.js';

const logger = new RouterLogger({ module: 'main' });

/**
 * 动态模型路由技能主类
 */
export class DynamicModelRouter {
  private configManager: ConfigManager;
  private config: RouterConfig;
  private isInitialized = false;
  private decisionEngine: DecisionEngine | null = null;
  
  constructor(configDir?: string) {
    logger.info('初始化动态模型路由技能');
    
    // 初始化配置管理器
    this.configManager = new ConfigManager(configDir);
    this.config = this.configManager.getConfig();
    
    logger.info('动态模型路由技能实例创建完成', {
      version: '0.1.0',
      configPath: this.configManager.getConfigPath(),
    });
  }
  
  /**
   * 初始化技能
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      logger.warn('技能已经初始化');
      return;
    }
    
    try {
      logger.info('开始初始化动态模型路由技能');
      
      // 检查配置
      if (!this.config.enabled) {
        logger.warn('技能在配置中被禁用');
        this.isInitialized = true;
        return;
      }
      
      // 初始化决策引擎
      this.decisionEngine = new DecisionEngine({
        defaultStrategy: this.convertStrategy(this.config.defaultStrategy),
        learningEnabled: this.config.learningEnabled,
        enableTaskSplitting: true,
        enableFallbackRouting: true
      });
      
      // 预加载模型数据（用于调试和验证）
      const availableModels = this.getAvailableModels();
      logger.debug('模型数据加载完成', { modelCount: availableModels.length });
      
      // TODO: 初始化其他组件
      // 1. 初始化供应商管理器
      // 2. 初始化模型能力评估器
      // 3. 初始化学习系统
      // 4. 初始化数据库
      
      logger.info('动态模型路由技能初始化完成');
      this.isInitialized = true;
      
    } catch (error) {
      logger.error('技能初始化失败', error as Error);
      throw error;
    }
  }
  
  /**
   * 路由任务到最佳模型
   */
  async routeTask(task: string): Promise<RoutingDecision> {
    if (!this.isInitialized) {
      await this.initialize();
    }
    
    if (!this.config.enabled) {
      throw new Error('动态模型路由技能已被禁用');
    }
    
    const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const taskLogger = new RouterLogger({ taskId });
    
    try {
      taskLogger.info('开始路由任务', { 
        contentPreview: task.substring(0, 100) + (task.length > 100 ? '...' : ''),
        contentLength: task.length,
      });
      
      // 1. 分析任务需求
      const taskAnalysis = this.analyzeTaskContent(task);
      
      // 2. 创建路由请求（决策引擎将使用内部模型注册表）
      const routingRequest = this.createRoutingRequest(
        taskId, 
        task, 
        taskAnalysis
      );
      
      // 4. 获取决策引擎
      const decisionEngine = this.getDecisionEngine();
      
      // 5. 调用决策引擎
      const routingResponse = await decisionEngine.route(routingRequest);
      
      // 6. 转换为技能API格式
      const decision = this.convertToRoutingDecision(routingResponse.decision, taskId);
      
      taskLogger.logDecision(
        decision.taskId,
        decision.selectedModel,
        decision.selectedProvider,
        decision.confidence,
        decision.alternatives,
        decision.reasoning
      );
      
      return decision;
      
    } catch (error) {
      taskLogger.error('路由任务失败', error as Error);
      throw error;
    }
  }
  
  /**
   * 分析任务内容
   */
  private analyzeTaskContent(content: string): {
    language: string;
    complexity: number;
    categories: string[];
    estimatedTokens: number;
  } {
    const language = detectLanguage(content);
    const complexity = calculateComplexity(content);
    const estimatedTokens = estimateTokens(content);
    
    // 简单分类
    const categories: string[] = [];
    const lowerContent = content.toLowerCase();
    
    if (lowerContent.includes('代码') || lowerContent.includes('program') || lowerContent.includes('function')) {
      categories.push('coding');
    }
    if (lowerContent.includes('翻译') || lowerContent.includes('translate')) {
      categories.push('translation');
    }
    if (lowerContent.includes('分析') || lowerContent.includes('analyze') || lowerContent.includes('总结')) {
      categories.push('analysis');
    }
    if (lowerContent.includes('写') || lowerContent.includes('write') || lowerContent.includes('文章')) {
      categories.push('writing');
    }
    if (lowerContent.includes('解释') || lowerContent.includes('explain') || lowerContent.includes('什么')) {
      categories.push('qa');
    }
    
    if (categories.length === 0) {
      categories.push('general');
    }
    
    return {
      language,
      complexity,
      categories,
      estimatedTokens
    };
  }
  
  /**
   * 获取可用模型列表
   */
  private getAvailableModels(): ModelCapability[] {
    // 返回预定义的模型列表
    // 实际应用中可以从配置或API获取
    return [
      {
        modelId: 'deepseek/deepseek-chat',
        provider: 'deepseek',
        capabilities: {
          coding: 85,
          writing: 90,
          analysis: 88,
          translation: 75,
          reasoning: 82
        },
        costPerToken: 0.00028,
        avgResponseTime: 1500,
        successRate: 0.95,
        languageSupport: ['zh', 'en', 'ja', 'ko', 'fr', 'de', 'es'],
        lastUpdated: new Date()
      },
      {
        modelId: 'deepseek/deepseek-reasoner',
        provider: 'deepseek',
        capabilities: {
          coding: 88,
          writing: 85,
          analysis: 92,
          translation: 70,
          reasoning: 95
        },
        costPerToken: 0.00042,
        avgResponseTime: 3000,
        successRate: 0.92,
        languageSupport: ['zh', 'en'],
        lastUpdated: new Date()
      },
      {
        modelId: 'gpt-4o',
        provider: 'openai',
        capabilities: {
          coding: 90,
          writing: 95,
          analysis: 93,
          translation: 85,
          reasoning: 94
        },
        costPerToken: 0.005,
        avgResponseTime: 2500,
        successRate: 0.98,
        languageSupport: ['en', 'zh', 'ja', 'ko', 'fr', 'de', 'es', 'it', 'pt', 'ru'],
        lastUpdated: new Date()
      },
      {
        modelId: 'claude-3-opus',
        provider: 'anthropic',
        capabilities: {
          coding: 87,
          writing: 96,
          analysis: 94,
          translation: 80,
          reasoning: 96
        },
        costPerToken: 0.008,
        avgResponseTime: 3500,
        successRate: 0.97,
        languageSupport: ['en', 'fr', 'de', 'es', 'it', 'pt'],
        lastUpdated: new Date()
      },
      {
        modelId: 'MiniMax-M2.5',
        provider: 'minimax',
        capabilities: {
          coding: 75,
          writing: 88,
          analysis: 82,
          translation: 90,
          reasoning: 78
        },
        costPerToken: 0.00035,
        avgResponseTime: 1800,
        successRate: 0.93,
        languageSupport: ['zh', 'en'],
        lastUpdated: new Date()
      }
    ];
  }
  
  /**
   * 获取可用供应商列表（暂时未使用）
   */
  /*
  private getAvailableProviders(): ProviderInfo[] {
    return [
      { 
        id: 'deepseek', 
        name: 'DeepSeek', 
        baseUrl: 'https://api.deepseek.com',
        models: ['deepseek-chat', 'deepseek-reasoner'],
        enabled: true
      },
      { 
        id: 'openai', 
        name: 'OpenAI', 
        baseUrl: 'https://api.openai.com',
        models: ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        enabled: true
      },
      { 
        id: 'anthropic', 
        name: 'Anthropic', 
        baseUrl: 'https://api.anthropic.com',
        models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
        enabled: true
      },
      { 
        id: 'minimax', 
        name: 'MiniMax', 
        baseUrl: 'https://api.minimax.chat',
        models: ['MiniMax-M2.5', 'MiniMax-M1'],
        enabled: true
      }
    ];
  }
  */
  
  /**
   * 创建路由请求
   */
  private createRoutingRequest(
    taskId: string, 
    content: string, 
    analysis: ReturnType<typeof this.analyzeTaskContent>
  ): RoutingRequest {
    const complexityLevel = analysis.complexity < 0.3 ? 'simple' : 
                           analysis.complexity < 0.7 ? 'medium' : 'complex';
    
    const taskDescription: TaskDescription = {
      id: taskId,
      content,
      language: analysis.language as 'zh' | 'en' | 'mixed' | 'other',
      complexity: complexityLevel as 'simple' | 'medium' | 'complex',
      category: analysis.categories,
      estimatedTokens: analysis.estimatedTokens,
      createdAt: new Date()
    };
    
    return {
      task: taskDescription,
      constraints: {
        maxCost: 100,
        maxLatency: 30000,
        minQuality: 0.7,
        requiredCapabilities: [],
        preferredProviders: [],
        excludedModels: []
      },
      context: {
        currentLoad: {
          providerLoad: new Map(),
          modelLoad: new Map(),
          recentErrors: new Map()
        },
        historicalPerformance: {
          successRates: new Map(),
          averageLatencies: new Map(),
          costEfficiency: new Map()
        },
        environment: {
          timeOfDay: new Date().getHours().toString(),
          networkQuality: 0.9,
          systemLoad: 0.3
        },
        userPreferences: {
          preferredModels: [],
          avoidedModels: [],
          qualityImportance: 0.5,
          speedImportance: 0.5,
          costSensitivity: 0.5
        }
      },
      strategy: this.convertStrategy(this.config.defaultStrategy)
    };
  }
  
  /**
   * 转换策略字符串到RoutingStrategy枚举
   */
  private convertStrategy(strategy: 'cost' | 'quality' | 'balanced'): RoutingStrategy {
    switch (strategy) {
      case 'cost':
        return RoutingStrategy.COST_OPTIMIZED;
      case 'quality':
        return RoutingStrategy.QUALITY_FIRST;
      case 'balanced':
      default:
        return RoutingStrategy.BALANCED;
    }
  }
  
  /**
   * 获取决策引擎
   */
  private getDecisionEngine(): DecisionEngine {
    if (!this.decisionEngine) {
      this.decisionEngine = new DecisionEngine({
        defaultStrategy: this.convertStrategy(this.config.defaultStrategy),
        learningEnabled: this.config.learningEnabled,
        enableTaskSplitting: true,
        enableFallbackRouting: true
      });
    }
    return this.decisionEngine;
  }
  
  /**
   * 转换路由响应到技能API格式
   */
  private convertToRoutingDecision(
    engineDecision: any, 
    taskId: string
  ): RoutingDecision {
    // 从决策引擎的决策中提取信息
    let selectedModel: string;
    let selectedProvider: string;
    
    // 处理selectedModel：可能是字符串或对象
    if (typeof engineDecision.selectedModel === 'string') {
      selectedModel = engineDecision.selectedModel;
    } else if (engineDecision.selectedModel?.modelId) {
      selectedModel = engineDecision.selectedModel.modelId;
    } else if (engineDecision.selectedModel?.id) {
      selectedModel = engineDecision.selectedModel.id;
    } else {
      selectedModel = 'deepseek/deepseek-chat';
    }
    
    // 处理selectedProvider：可能是字符串或对象
    if (typeof engineDecision.selectedProvider === 'string') {
      selectedProvider = engineDecision.selectedProvider;
    } else if (engineDecision.selectedProvider?.id) {
      selectedProvider = engineDecision.selectedProvider.id;
    } else {
      selectedProvider = 'deepseek';
    }
    
    const confidence = engineDecision.confidence || engineDecision.decisionQuality?.confidence || 0.8;
    
    // 构建替代选项
    const alternatives = engineDecision.alternatives?.map((alt: any, index: number) => {
      let model: string;
      let provider: string;
      
      if (typeof alt.model === 'string') {
        model = alt.model;
      } else if (alt.model?.modelId) {
        model = alt.model.modelId;
      } else if (alt.model?.id) {
        model = alt.model.id;
      } else {
        model = `model_${index}`;
      }
      
      if (typeof alt.provider === 'string') {
        provider = alt.provider;
      } else if (alt.provider?.id) {
        provider = alt.provider.id;
      } else {
        provider = 'unknown';
      }
      
      return {
        model,
        provider,
        score: alt.score || (0.8 - index * 0.1)
      };
    }) || [
      { model: 'deepseek/deepseek-reasoner', provider: 'deepseek', score: 0.7 },
      { model: 'MiniMax-M2.5', provider: 'minimax', score: 0.6 }
    ];
    
    // 处理reasoning：可能是字符串或对象
    let reasoning: string;
    if (typeof engineDecision.reasoning === 'string') {
      reasoning = engineDecision.reasoning;
    } else if (engineDecision.reasoning?.primaryFactors) {
      // 从决策引擎的详细reasoning对象中提取关键信息
      const factors = engineDecision.reasoning.primaryFactors;
      reasoning = `智能路由决策：基于${factors.map((f: any) => f.factor).join('、')}等${factors.length}个因素选择最优模型`;
    } else {
      reasoning = '智能路由决策：基于任务复杂度、成本效率、模型能力和历史表现选择最优模型';
    }
    
    return {
      taskId,
      selectedModel,
      selectedProvider,
      confidence: Math.min(1, Math.max(0, confidence)),
      alternatives,
      reasoning,
      createdAt: new Date()
    };
  }
  
  /**
   * 获取技能状态
   */
  getStatus(): any {
    return {
      initialized: this.isInitialized,
      enabled: this.config.enabled,
      learningEnabled: this.config.learningEnabled,
      defaultStrategy: this.config.defaultStrategy,
      configPath: this.configManager.getConfigPath(),
      version: '0.1.0',
    };
  }
  
  /**
   * 获取当前配置
   */
  getConfig(): RouterConfig {
    return this.configManager.getConfig();
  }
  
  /**
   * 更新配置
   */
  updateConfig(updates: Partial<RouterConfig>): RouterConfig {
    logger.info('更新技能配置', { updates });
    this.config = this.configManager.updateConfig(updates);
    return this.config;
  }
  
  /**
   * 重置配置
   */
  resetConfig(): RouterConfig {
    logger.info('重置技能配置');
    this.config = this.configManager.resetConfig();
    return this.config;
  }
  
  /**
   * 导出配置
   */
  exportConfig(): string {
    return this.configManager.exportConfig();
  }
  
  /**
   * 导入配置
   */
  importConfig(configJson: string): RouterConfig {
    this.config = this.configManager.importConfig(configJson);
    return this.config;
  }
  
  /**
   * 备份配置
   */
  backupConfig(): string {
    return this.configManager.backupConfig();
  }
  
  /**
   * 列出备份
   */
  listBackups(): string[] {
    return this.configManager.listBackups();
  }
  
  /**
   * 恢复备份
   */
  restoreFromBackup(backupFile: string): RouterConfig {
    this.config = this.configManager.restoreFromBackup(backupFile);
    return this.config;
  }
  
  /**
   * 清理旧备份
   */
  cleanupOldBackups(maxBackups = 10): void {
    this.configManager.cleanupOldBackups(maxBackups);
  }
  
  /**
   * 关闭技能
   */
  async shutdown(): Promise<void> {
    logger.info('关闭动态模型路由技能');
    
    try {
      // 清理决策引擎
      if (this.decisionEngine) {
        // 决策引擎可能没有shutdown方法，直接置为null
        this.decisionEngine = null;
      }
      
      // TODO: 清理其他资源
      // 1. 关闭数据库连接
      // 2. 保存学习数据
      // 3. 清理临时文件
      
      this.isInitialized = false;
      logger.info('动态模型路由技能关闭完成');
      
    } catch (error) {
      logger.error('关闭技能时发生错误', error as Error);
      throw error;
    }
  }
}

// 默认技能实例
let defaultRouter: DynamicModelRouter | null = null;

/**
 * 获取默认路由器实例
 */
export function getRouter(configDir?: string): DynamicModelRouter {
  if (!defaultRouter) {
    defaultRouter = new DynamicModelRouter(configDir);
  }
  return defaultRouter;
}

/**
 * 重新初始化路由器
 */
export function reinitializeRouter(configDir?: string): DynamicModelRouter {
  defaultRouter = new DynamicModelRouter(configDir);
  return defaultRouter;
}

/**
 * 技能入口点（用于OpenClaw技能系统）
 */
export async function skillEntry() {
  const router = getRouter();
  
  try {
    await router.initialize();
    
    logger.info('动态模型路由技能启动完成');
    
    // 返回技能接口
    return {
      name: '动态模型路由',
      version: '0.1.0',
      description: '智能路由任务到最佳AI模型',
      author: 'OpenClaw AI助手',
      
      // 技能方法
      route: (task: string) => router.routeTask(task),
      getStatus: () => router.getStatus(),
      getConfig: () => router.getConfig(),
      updateConfig: (updates: any) => router.updateConfig(updates),
      shutdown: () => router.shutdown(),
    };
    
  } catch (error) {
    logger.error('技能启动失败', error as Error);
    throw error;
  }
}

// 导出主要类型和工具
export * from './core/types.js';
export * from './utils/index.js';
export * from './utils/logger.js';
export * from './utils/config.js';

// 默认导出技能入口
export default skillEntry;
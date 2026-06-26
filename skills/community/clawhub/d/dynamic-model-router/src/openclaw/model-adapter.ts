/**
 * 模型调用适配器
 * 
 * 提供统一的接口调用不同供应商的AI模型
 */

import { RouterError } from '../core/types.js';
import { RouterLogger } from '../utils/logger.js';
import { retry } from '../utils/index.js';
import type { ModelRequest, ModelResponse } from '../core/types.js';
import type { OpenClawProvider } from './provider-discovery.js';

const logger = new RouterLogger({ module: 'model-adapter' });

/**
 * 适配器配置
 */
export interface AdapterConfig {
  maxRetries: number;
  timeoutMs: number;
  maxTokens: number;
  temperature: number;
}

/**
 * 调用统计
 */
export interface CallStats {
  providerId: string;
  modelId: string;
  success: boolean;
  responseTime: number;
  tokensUsed: number;
  error?: string;
  timestamp: Date;
}

/**
 * 模型调用结果
 */
export interface ModelCallResult {
  response: ModelResponse;
  stats: CallStats;
}

/**
 * 适配器基类
 */
export abstract class BaseModelAdapter {
  protected provider: OpenClawProvider;
  protected config: AdapterConfig;
  protected callHistory: CallStats[] = [];
  protected maxHistorySize: number = 1000;
  
  constructor(provider: OpenClawProvider, config?: Partial<AdapterConfig>) {
    this.provider = provider;
    this.config = {
      maxRetries: 3,
      timeoutMs: 60000,
      maxTokens: 8192,
      temperature: 0.7,
      ...config,
    };
    
    logger.info('适配器初始化', {
      providerId: provider.id,
      baseUrl: provider.baseUrl,
      apiType: provider.apiType,
    });
  }
  
  /**
   * 调用模型
   */
  abstract callModel(request: ModelRequest): Promise<ModelCallResult>;
  
  /**
   * 获取支持的模型列表
   */
  abstract getSupportedModels(): string[];
  
  /**
   * 验证请求
   */
  protected validateRequest(request: ModelRequest): void {
    if (!request.model) {
      throw new RouterError('模型ID不能为空', 'INVALID_REQUEST');
    }
    
    if (!request.messages || request.messages.length === 0) {
      throw new RouterError('消息不能为空', 'INVALID_REQUEST');
    }
    
    // 检查模型是否支持
    const supportedModels = this.getSupportedModels();
    if (!supportedModels.includes(request.model)) {
      throw new RouterError(
        `模型 ${request.model} 不被此供应商支持`,
        'UNSUPPORTED_MODEL',
        { supportedModels }
      );
    }
    
    // 检查消息格式
    for (const message of request.messages) {
      if (!['user', 'assistant', 'system'].includes(message.role)) {
        throw new RouterError(`无效的消息角色: ${message.role}`, 'INVALID_REQUEST');
      }
      
      if (typeof message.content !== 'string') {
        throw new RouterError('消息内容必须是字符串', 'INVALID_REQUEST');
      }
    }
    
    // 检查token限制
    const maxTokens = request.maxTokens || this.config.maxTokens;
    const modelConfig = this.provider.models.find(m => m.id === request.model);
    if (modelConfig && maxTokens > modelConfig.maxTokens) {
      throw new RouterError(
        `请求的token数(${maxTokens})超过模型限制(${modelConfig.maxTokens})`,
        'TOKEN_LIMIT_EXCEEDED'
      );
    }
  }
  
  /**
   * 记录调用统计
   */
  protected recordCallStats(stats: CallStats): void {
    this.callHistory.push(stats);
    
    // 保持历史记录大小
    if (this.callHistory.length > this.maxHistorySize) {
      this.callHistory = this.callHistory.slice(-this.maxHistorySize);
    }
    
    logger.logModelCall(
      stats.modelId,
      stats.providerId,
      stats.success,
      stats.responseTime,
      stats.tokensUsed,
      stats.error
    );
  }
  
  /**
   * 获取调用历史
   */
  getCallHistory(limit?: number): CallStats[] {
    const history = [...this.callHistory].reverse(); // 最新的在前面
    return limit ? history.slice(0, limit) : history;
  }
  
  /**
   * 获取成功率统计
   */
  getSuccessRate(): number {
    if (this.callHistory.length === 0) return 0;
    
    const successfulCalls = this.callHistory.filter(call => call.success).length;
    return successfulCalls / this.callHistory.length;
  }
  
  /**
   * 获取平均响应时间
   */
  getAverageResponseTime(): number {
    if (this.callHistory.length === 0) return 0;
    
    const totalTime = this.callHistory.reduce((sum, call) => sum + call.responseTime, 0);
    return totalTime / this.callHistory.length;
  }
  
  /**
   * 获取提供商信息
   */
  getProvider(): OpenClawProvider {
    return this.provider;
  }
  
  /**
   * 获取配置
   */
  getConfig(): AdapterConfig {
    return { ...this.config };
  }
  
  /**
   * 更新配置
   */
  updateConfig(updates: Partial<AdapterConfig>): void {
    this.config = { ...this.config, ...updates };
    logger.debug('适配器配置更新', { updates });
  }
}

/**
 * DeepSeek适配器
 */
export class DeepSeekAdapter extends BaseModelAdapter {
  private apiKey?: string;
  
  constructor(provider: OpenClawProvider, apiKey?: string, config?: Partial<AdapterConfig>) {
    super(provider, config);
    this.apiKey = apiKey;
  }
  
  getSupportedModels(): string[] {
    return this.provider.models.map(model => model.id);
  }
  
  async callModel(request: ModelRequest): Promise<ModelCallResult> {
    const startTime = Date.now();
    
    try {
      // 验证请求
      this.validateRequest(request);
      
      // 准备API调用
      const result = await retry(
        () => this.makeApiCall(request),
        this.config.maxRetries,
        1000
      );
      
      const responseTime = Date.now() - startTime;
      
      const stats: CallStats = {
        providerId: this.provider.id,
        modelId: request.model,
        success: true,
        responseTime,
        tokensUsed: result.response.usage.totalTokens,
        timestamp: new Date(),
      };
      
      this.recordCallStats(stats);
      
      return result;
      
    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      const stats: CallStats = {
        providerId: this.provider.id,
        modelId: request.model,
        success: false,
        responseTime,
        tokensUsed: 0,
        error: (error as Error).message,
        timestamp: new Date(),
      };
      
      this.recordCallStats(stats);
      
      throw new RouterError(
        `DeepSeek API调用失败: ${(error as Error).message}`,
        'API_CALL_FAILED',
        { providerId: this.provider.id, modelId: request.model }
      );
    }
  }
  
  /**
   * 执行实际的API调用
   */
  private async makeApiCall(request: ModelRequest): Promise<ModelCallResult> {
    if (!this.apiKey) {
      throw new RouterError('DeepSeek API密钥未配置', 'AUTH_ERROR');
    }
    
    const url = `${this.provider.baseUrl}/chat/completions`;
    
    const requestBody = {
      model: request.model,
      messages: request.messages,
      max_tokens: request.maxTokens || this.config.maxTokens,
      temperature: request.temperature || this.config.temperature,
      stream: false,
    };
    
    logger.debug('发起DeepSeek API请求', {
      url,
      model: request.model,
      messageCount: request.messages.length,
    });
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeoutMs);
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          'User-Agent': 'OpenClaw-DynamicRouter/0.1.0',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        const errorText = await response.text();
        logger.error('DeepSeek API响应错误', undefined, {
          status: response.status,
          statusText: response.statusText,
          error: errorText,
        });
        
        throw new Error(`API错误 ${response.status}: ${response.statusText}`);
      }
      
      const responseData = await response.json() as any;
      
      // 解析响应
      const modelResponse: ModelResponse = {
        id: responseData.id || `gen_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        content: responseData.choices[0]?.message?.content || '',
        model: responseData.model || request.model,
        usage: {
          promptTokens: responseData.usage?.prompt_tokens || 0,
          completionTokens: responseData.usage?.completion_tokens || 0,
          totalTokens: responseData.usage?.total_tokens || 0,
        },
        finishReason: responseData.choices[0]?.finish_reason || 'stop',
      };
      
      logger.debug('DeepSeek API响应成功', {
        model: modelResponse.model,
        tokenUsage: modelResponse.usage.totalTokens,
        finishReason: modelResponse.finishReason,
      });
      
      return {
        response: modelResponse,
        stats: {
          providerId: this.provider.id,
          modelId: request.model,
          success: true,
          responseTime: 0, // 将在外层计算
          tokensUsed: modelResponse.usage.totalTokens,
          timestamp: new Date(),
        },
      };
      
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error && error.name === 'AbortError') {
        throw new RouterError('API调用超时', 'TIMEOUT_ERROR', { timeoutMs: this.config.timeoutMs });
      }
      
      throw error;
    }
  }
}

/**
 * OpenAI兼容适配器
 */
export class OpenAIClientAdapter extends BaseModelAdapter {
  private apiKey?: string;
  
  constructor(provider: OpenClawProvider, apiKey?: string, config?: Partial<AdapterConfig>) {
    super(provider, config);
    this.apiKey = apiKey;
  }
  
  getSupportedModels(): string[] {
    return this.provider.models.map(model => model.id);
  }
  
  async callModel(request: ModelRequest): Promise<ModelCallResult> {
    // 实现与DeepSeek类似，但使用OpenAI兼容的API
    // 简化实现：重用DeepSeek的逻辑，因为API兼容
    const deepseekAdapter = new DeepSeekAdapter(this.provider, this.apiKey, this.config);
    return deepseekAdapter.callModel(request);
  }
}

/**
 * 适配器工厂
 */
export class ModelAdapterFactory {
  private static instance: ModelAdapterFactory;
  private adapters: Map<string, BaseModelAdapter> = new Map();
  private providerApiKeys: Map<string, string> = new Map();
  
  private constructor() {}
  
  static getInstance(): ModelAdapterFactory {
    if (!ModelAdapterFactory.instance) {
      ModelAdapterFactory.instance = new ModelAdapterFactory();
    }
    return ModelAdapterFactory.instance;
  }
  
  /**
   * 注册API密钥
   */
  registerApiKey(providerId: string, apiKey: string): void {
    this.providerApiKeys.set(providerId, apiKey);
    logger.debug('注册API密钥', { providerId, hasKey: !!apiKey });
  }
  
  /**
   * 创建适配器
   */
  createAdapter(provider: OpenClawProvider, config?: Partial<AdapterConfig>): BaseModelAdapter {
    const apiKey = this.providerApiKeys.get(provider.id);
    
    let adapter: BaseModelAdapter;
    
    switch (provider.id) {
      case 'deepseek':
        adapter = new DeepSeekAdapter(provider, apiKey, config);
        break;
        
      case 'openai':
      case 'anthropic':
      case 'google':
      case 'mistral':
      case 'cohere':
      case 'minimax':
      case 'qwen':
      case 'baichuan':
        // 这些供应商使用OpenAI兼容的API
        adapter = new OpenAIClientAdapter(provider, apiKey, config);
        break;
        
      default:
        logger.warn('未知供应商类型，使用通用适配器', { providerId: provider.id });
        adapter = new OpenAIClientAdapter(provider, apiKey, config);
    }
    
    this.adapters.set(provider.id, adapter);
    logger.info('创建模型适配器', {
      providerId: provider.id,
      adapterType: adapter.constructor.name,
      hasApiKey: !!apiKey,
    });
    
    return adapter;
  }
  
  /**
   * 获取适配器
   */
  getAdapter(providerId: string): BaseModelAdapter | undefined {
    return this.adapters.get(providerId);
  }
  
  /**
   * 获取所有适配器
   */
  getAllAdapters(): BaseModelAdapter[] {
    return Array.from(this.adapters.values());
  }
  
  /**
   * 销毁适配器
   */
  destroyAdapter(providerId: string): void {
    this.adapters.delete(providerId);
    logger.debug('销毁适配器', { providerId });
  }
  
  /**
   * 销毁所有适配器
   */
  destroyAllAdapters(): void {
    const providerIds = Array.from(this.adapters.keys());
    this.adapters.clear();
    logger.info('销毁所有适配器', { destroyedCount: providerIds.length });
  }
  
  /**
   * 获取支持的供应商列表
   */
  getSupportedProviders(): string[] {
    return Array.from(this.adapters.keys());
  }
}
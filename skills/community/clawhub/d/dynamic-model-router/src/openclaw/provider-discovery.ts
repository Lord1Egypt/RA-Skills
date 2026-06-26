/**
 * OpenClaw供应商发现模块
 * 
 * 负责发现和验证OpenClaw中配置的AI模型供应商
 */

import fs from 'fs';
import path from 'path';
import { RouterError } from '../core/types.js';
import { RouterLogger } from '../utils/logger.js';
import { retry } from '../utils/index.js';


const logger = new RouterLogger({ module: 'provider-discovery' });

/**
 * OpenClaw供应商信息
 */
export interface OpenClawProvider {
  id: string;
  name: string;
  baseUrl: string;
  apiType: string;
  models: Array<{
    id: string;
    name: string;
    reasoning: boolean;
    contextWindow: number;
    maxTokens: number;
    cost: {
      input: number;
      output: number;
      cacheRead?: number;
      cacheWrite?: number;
    };
  }>;
  enabled: boolean;
}

/**
 * OpenClaw配置结构
 */
export interface OpenClawConfig {
  meta?: {
    lastTouchedVersion?: string;
    lastTouchedAt?: string;
  };
  auth?: {
    profiles?: Record<string, {
      provider: string;
      mode: string;
      apiKey?: string;
    }>;
  };
  models?: {
    mode?: string;
    providers?: Record<string, {
      baseUrl: string;
      api: string;
      models: Array<{
        id: string;
        name: string;
        reasoning: boolean;
        input: string[];
        cost: {
          input: number;
          output: number;
          cacheRead?: number;
          cacheWrite?: number;
        };
        contextWindow: number;
        maxTokens: number;
      }>;
    }>;
  };
  agents?: {
    defaults?: {
      model?: {
        primary?: string;
      };
    };
  };
}

/**
 * 供应商发现器
 */
export class ProviderDiscoverer {
  private configPath: string;
  private providers: Map<string, OpenClawProvider> = new Map();
  private lastDiscovery: number = 0;
  private discoveryInterval: number = 3600000; // 1小时
  
  constructor(configPath?: string) {
    this.configPath = configPath || 
      path.join(process.env.HOME || process.env.USERPROFILE || '.', '.openclaw', 'openclaw.json');
    
    logger.info('供应商发现器初始化', { configPath: this.configPath });
  }
  
  /**
   * 发现所有可用的供应商
   */
  async discoverAll(): Promise<OpenClawProvider[]> {
    const now = Date.now();
    
    // 检查是否需要重新发现
    if (now - this.lastDiscovery < this.discoveryInterval && this.providers.size > 0) {
      logger.debug('使用缓存的供应商信息', {
        cachedCount: this.providers.size,
        lastDiscovery: new Date(this.lastDiscovery).toISOString(),
      });
      return Array.from(this.providers.values());
    }
    
    try {
      logger.info('开始发现供应商', { configPath: this.configPath });
      
      // 加载OpenClaw配置
      const config = await this.loadConfig();
      
      // 解析供应商
      const discoveredProviders = await this.parseProviders(config);
      
      // 验证供应商可用性
      const validatedProviders = await this.validateProviders(discoveredProviders);
      
      // 更新缓存
      this.providers.clear();
      validatedProviders.forEach(provider => {
        this.providers.set(provider.id, provider);
      });
      
      this.lastDiscovery = now;
      
      logger.info('供应商发现完成', {
        totalDiscovered: discoveredProviders.length,
        totalValidated: validatedProviders.length,
        providers: validatedProviders.map(p => `${p.id}@${p.baseUrl}`),
      });
      
      return validatedProviders;
      
    } catch (error) {
      logger.error('供应商发现失败', error as Error);
      throw new RouterError(
        `供应商发现失败: ${(error as Error).message}`,
        'PROVIDER_DISCOVERY_ERROR',
        { configPath: this.configPath }
      );
    }
  }
  
  /**
   * 加载OpenClaw配置
   */
  private async loadConfig(): Promise<OpenClawConfig> {
    try {
      logger.debug('加载OpenClaw配置', { path: this.configPath });
      
      if (!fs.existsSync(this.configPath)) {
        throw new Error(`配置文件不存在: ${this.configPath}`);
      }
      
      const configContent = await fs.promises.readFile(this.configPath, 'utf-8');
      const config = JSON.parse(configContent);
      
      logger.debug('OpenClaw配置加载成功', {
        hasAuthProfiles: !!config.auth?.profiles,
        hasModelProviders: !!config.models?.providers,
        providerCount: Object.keys(config.models?.providers || {}).length,
      });
      
      return config;
      
    } catch (error) {
      logger.error('加载OpenClaw配置失败', error as Error, { path: this.configPath });
      throw new RouterError(
        `加载OpenClaw配置失败: ${(error as Error).message}`,
        'CONFIG_LOAD_ERROR',
        { configPath: this.configPath }
      );
    }
  }
  
  /**
   * 解析配置中的供应商
   */
  private async parseProviders(config: OpenClawConfig): Promise<OpenClawProvider[]> {
    const providers: OpenClawProvider[] = [];
    
    // 从models.providers解析
    const modelProviders = config.models?.providers || {};
    
    for (const [providerId, providerConfig] of Object.entries(modelProviders)) {
      try {
        logger.debug('解析供应商配置', { providerId, baseUrl: providerConfig.baseUrl });
        
        // 检查是否有对应的认证配置
        const authProfile = this.findAuthProfile(config, providerId);
        
        const provider: OpenClawProvider = {
          id: providerId,
          name: this.formatProviderName(providerId),
          baseUrl: providerConfig.baseUrl,
          apiType: providerConfig.api,
          models: providerConfig.models.map(model => ({
            id: model.id,
            name: model.name,
            reasoning: model.reasoning || false,
            contextWindow: model.contextWindow || 128000,
            maxTokens: model.maxTokens || 8192,
            cost: {
              input: model.cost?.input || 0,
              output: model.cost?.output || 0,
              cacheRead: model.cost?.cacheRead,
              cacheWrite: model.cost?.cacheWrite,
            },
          })),
          enabled: !!authProfile, // 如果有认证配置则认为启用
        };
        
        providers.push(provider);
        
        logger.debug('供应商解析成功', {
          providerId,
          modelCount: provider.models.length,
          enabled: provider.enabled,
        });
        
      } catch (error) {
        logger.warn('供应商解析失败，跳过', { 
          providerId,
          error: error instanceof Error ? {
            message: error.message,
            stack: error.stack,
            name: error.name,
          } : String(error)
        });
        // 跳过解析失败的供应商，继续处理其他
      }
    }
    
    // 如果没有从models.providers找到，尝试从auth.profiles推断
    if (providers.length === 0 && config.auth?.profiles) {
      logger.debug('尝试从认证配置推断供应商');
      
      for (const [_profileId, profile] of Object.entries(config.auth.profiles)) {
        const providerId = profile.provider;
        
        // 跳过重复
        if (providers.some(p => p.id === providerId)) {
          continue;
        }
        
        const provider: OpenClawProvider = {
          id: providerId,
          name: this.formatProviderName(providerId),
          baseUrl: this.inferBaseUrl(providerId),
          apiType: 'openai-completions', // 默认API类型
          models: this.inferDefaultModels(providerId),
          enabled: true,
        };
        
        providers.push(provider);
        
        logger.debug('从认证配置推断供应商', {
          providerId,
          inferred: true,
        });
      }
    }
    
    logger.info('供应商解析完成', {
      totalParsed: providers.length,
      enabledCount: providers.filter(p => p.enabled).length,
    });
    
    return providers;
  }
  
  /**
   * 查找供应商的认证配置
   */
  private findAuthProfile(config: OpenClawConfig, providerId: string): any {
    if (!config.auth?.profiles) {
      return null;
    }
    
    // 查找匹配的认证配置
    for (const [profileId, profile] of Object.entries(config.auth.profiles)) {
      if (profile.provider === providerId) {
        return profile;
      }
      
      // 检查profileId是否包含providerId
      if (profileId.startsWith(`${providerId}:`)) {
        return profile;
      }
    }
    
    return null;
  }
  
  /**
   * 格式化供应商名称
   */
  private formatProviderName(providerId: string): string {
    const nameMap: Record<string, string> = {
      'deepseek': 'DeepSeek',
      'openai': 'OpenAI',
      'anthropic': 'Anthropic',
      'google': 'Google',
      'mistral': 'Mistral AI',
      'cohere': 'Cohere',
      'minimax': 'MiniMax',
      'qwen': 'Qwen',
      'baichuan': 'Baichuan',
    };
    
    return nameMap[providerId] || providerId.charAt(0).toUpperCase() + providerId.slice(1);
  }
  
  /**
   * 推断供应商的API基础URL
   */
  private inferBaseUrl(providerId: string): string {
    const urlMap: Record<string, string> = {
      'deepseek': 'https://api.deepseek.com',
      'openai': 'https://api.openai.com/v1',
      'anthropic': 'https://api.anthropic.com',
      'google': 'https://generativelanguage.googleapis.com',
      'mistral': 'https://api.mistral.ai/v1',
      'cohere': 'https://api.cohere.ai',
      'minimax': 'https://api.minimax.chat/v1',
      'qwen': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
      'baichuan': 'https://api.baichuan-ai.com/v1',
    };
    
    return urlMap[providerId] || `https://api.${providerId}.com`;
  }
  
  /**
   * 推断默认模型
   */
  private inferDefaultModels(providerId: string): OpenClawProvider['models'] {
    const defaultModels: Record<string, OpenClawProvider['models']> = {
      'deepseek': [
        {
          id: 'deepseek-chat',
          name: 'DeepSeek Chat',
          reasoning: false,
          contextWindow: 128000,
          maxTokens: 8192,
          cost: { input: 0.28, output: 0.42 },
        },
        {
          id: 'deepseek-reasoner',
          name: 'DeepSeek Reasoner',
          reasoning: true,
          contextWindow: 128000,
          maxTokens: 65536,
          cost: { input: 0.28, output: 0.42 },
        },
      ],
      'openai': [
        {
          id: 'gpt-4o',
          name: 'GPT-4o',
          reasoning: true,
          contextWindow: 128000,
          maxTokens: 4096,
          cost: { input: 5.0, output: 15.0 },
        },
      ],
      'anthropic': [
        {
          id: 'claude-3-5-sonnet',
          name: 'Claude 3.5 Sonnet',
          reasoning: true,
          contextWindow: 200000,
          maxTokens: 8192,
          cost: { input: 3.0, output: 15.0 },
        },
      ],
      'minimax': [
        {
          id: 'MiniMax-M2.5',
          name: 'MiniMax M2.5',
          reasoning: true,
          contextWindow: 128000,
          maxTokens: 8192,
          cost: { input: 0.5, output: 1.5 },
        },
      ],
    };
    
    return defaultModels[providerId] || [
      {
        id: `${providerId}-default`,
        name: `${this.formatProviderName(providerId)} Default`,
        reasoning: false,
        contextWindow: 32000,
        maxTokens: 4096,
        cost: { input: 1.0, output: 2.0 },
      },
    ];
  }
  
  /**
   * 验证供应商可用性
   */
  private async validateProviders(providers: OpenClawProvider[]): Promise<OpenClawProvider[]> {
    const validatedProviders: OpenClawProvider[] = [];
    
    logger.info('开始验证供应商可用性', { totalProviders: providers.length });
    
    for (const provider of providers) {
      try {
        // 只验证启用的供应商
        if (!provider.enabled) {
          logger.debug('跳过禁用供应商的验证', { providerId: provider.id });
          validatedProviders.push(provider);
          continue;
        }
        
        const isValid = await this.validateProvider(provider);
        
        if (isValid) {
          validatedProviders.push(provider);
          logger.debug('供应商验证通过', { providerId: provider.id });
        } else {
          // 验证失败，但为了兼容性，仍然添加（标记为不可用）
          provider.enabled = false;
          validatedProviders.push(provider);
          logger.warn('供应商验证失败，标记为禁用', { providerId: provider.id });
        }
        
      } catch (error) {
        logger.error('供应商验证过程中出错', error as Error, { providerId: provider.id });
        // 出错时仍然添加，标记为禁用
        provider.enabled = false;
        validatedProviders.push(provider);
      }
    }
    
    logger.info('供应商验证完成', {
      totalValidated: validatedProviders.length,
      enabledCount: validatedProviders.filter(p => p.enabled).length,
    });
    
    return validatedProviders;
  }
  
  /**
   * 验证单个供应商
   */
  private async validateProvider(provider: OpenClawProvider): Promise<boolean> {
    return retry(async () => {
      logger.debug('验证供应商连接性', { 
        providerId: provider.id,
        baseUrl: provider.baseUrl,
      });
      
      // 尝试连接到供应商的健康检查端点
      // 注意：不同供应商的健康检查端点不同
      const healthCheckUrl = this.getHealthCheckUrl(provider);
      
      try {
        // 使用fetch进行简单的连接测试
        const response = await fetch(healthCheckUrl, {
          method: 'HEAD',
          headers: {
            'User-Agent': 'OpenClaw-DynamicRouter/0.1.0',
          },
          // timeout: 10000, // 10秒超时 - 不是标准fetch API的一部分
        });
        
        // 检查响应状态
        const isValid = response.status < 500; // 5xx错误表示服务问题
        
        logger.debug('供应商连接测试结果', {
          providerId: provider.id,
          status: response.status,
          statusText: response.statusText,
          isValid,
        });
        
        return isValid;
        
      } catch (error) {
        logger.debug('供应商连接测试失败', {
          providerId: provider.id,
          healthCheckUrl,
          error: error instanceof Error ? {
            message: error.message,
            stack: error.stack,
            name: error.name,
          } : String(error)
        });
        return false;
      }
    }, 2, 2000); // 重试2次，每次间隔2秒
  }
  
  /**
   * 获取供应商的健康检查URL
   */
  private getHealthCheckUrl(provider: OpenClawProvider): string {
    // 不同供应商的健康检查端点
    const healthCheckEndpoints: Record<string, string> = {
      'deepseek': '/health',
      'openai': '/models',
      'anthropic': '/v1/messages',
      'google': '/v1/models',
      'mistral': '/v1/models',
    };
    
    const endpoint = healthCheckEndpoints[provider.id] || '/';
    return `${provider.baseUrl}${endpoint}`;
  }
  
  /**
   * 获取所有已发现的供应商
   */
  getProviders(): OpenClawProvider[] {
    return Array.from(this.providers.values());
  }
  
  /**
   * 获取特定供应商
   */
  getProvider(providerId: string): OpenClawProvider | undefined {
    return this.providers.get(providerId);
  }
  
  /**
   * 获取启用的供应商
   */
  getEnabledProviders(): OpenClawProvider[] {
    return Array.from(this.providers.values()).filter(p => p.enabled);
  }
  
  /**
   * 获取所有可用模型
   */
  getAllModels(): Array<{
    providerId: string;
    providerName: string;
    modelId: string;
    modelName: string;
    reasoning: boolean;
    contextWindow: number;
    maxTokens: number;
    cost: { input: number; output: number };
  }> {
    const models: Array<{
      providerId: string;
      providerName: string;
      modelId: string;
      modelName: string;
      reasoning: boolean;
      contextWindow: number;
      maxTokens: number;
      cost: { input: number; output: number };
    }> = [];
    
    for (const provider of this.providers.values()) {
      if (!provider.enabled) continue;
      
      for (const model of provider.models) {
        models.push({
          providerId: provider.id,
          providerName: provider.name,
          modelId: model.id,
          modelName: model.name,
          reasoning: model.reasoning,
          contextWindow: model.contextWindow,
          maxTokens: model.maxTokens,
          cost: model.cost,
        });
      }
    }
    
    return models;
  }
  
  /**
   * 强制重新发现供应商
   */
  async refresh(): Promise<OpenClawProvider[]> {
    logger.info('强制刷新供应商信息');
    this.lastDiscovery = 0; // 重置上次发现时间
    return this.discoverAll();
  }
  
  /**
   * 获取最后发现时间
   */
  getLastDiscoveryTime(): Date {
    return new Date(this.lastDiscovery);
  }
  
  /**
   * 设置发现间隔
   */
  setDiscoveryInterval(intervalMs: number): void {
    this.discoveryInterval = intervalMs;
    logger.debug('设置发现间隔', { intervalMs });
  }
}
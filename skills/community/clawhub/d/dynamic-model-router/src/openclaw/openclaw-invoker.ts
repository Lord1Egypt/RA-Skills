/**
 * OpenClaw调用器 - 使用OpenClaw内置能力调用AI模型
 * 
 * 替代独立的模型适配器，直接利用OpenClaw的模型调用基础设施
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import { RouterError } from '../core/types.js';
import { RouterLogger } from '../utils/logger.js';
import { retry } from '../utils/index.js';
import type { ModelRequest, ModelResponse } from '../core/types.js';
import type { OpenClawProvider } from './provider-discovery.js';

const execAsync = promisify(exec);
const logger = new RouterLogger({ module: 'openclaw-invoker' });

/**
 * OpenClaw调用配置
 */
export interface OpenClawInvokerConfig {
  openclawPath: string;
  timeoutMs: number;
  maxRetries: number;
  workspaceDir: string;
  tempDir: string;
}

/**
 * 调用统计
 */
export interface InvocationStats {
  providerId: string;
  modelId: string;
  success: boolean;
  responseTime: number;
  tokensUsed: number;
  error?: string;
  timestamp: Date;
}

/**
 * OpenClaw调用结果
 */
export interface OpenClawInvocationResult {
  response: ModelResponse;
  stats: InvocationStats;
}

/**
 * 临时请求文件结构
 */
interface TempRequestFile {
  request: {
    model: string;
    messages: Array<{
      role: string;
      content: string;
    }>;
    max_tokens?: number;
    temperature?: number;
    stream?: boolean;
  };
  metadata: {
    requestId: string;
    timestamp: string;
    providerId: string;
  };
}

/**
 * OpenClaw调用器
 * 
 * 使用OpenClaw内置能力调用AI模型，支持多种调用方式：
 * 1. CLI命令调用
 * 2. 网关API调用
 * 3. 技能集成调用
 */
export class OpenClawInvoker {
  private config: OpenClawInvokerConfig;
  private invocationHistory: InvocationStats[] = [];
  private maxHistorySize: number = 1000;
  
  constructor(config?: Partial<OpenClawInvokerConfig>) {
    this.config = {
      openclawPath: 'openclaw',
      timeoutMs: 120000, // 2分钟
      maxRetries: 3,
      workspaceDir: process.env.HOME ? path.join(process.env.HOME, '.openclaw', 'workspace') : '/tmp/openclaw-workspace',
      tempDir: '/tmp/openclaw-invoker',
      ...config,
    };
    
    // 确保临时目录存在
    if (!fs.existsSync(this.config.tempDir)) {
      fs.mkdirSync(this.config.tempDir, { recursive: true });
    }
    
    logger.info('OpenClaw调用器初始化完成', {
      openclawPath: this.config.openclawPath,
      timeoutMs: this.config.timeoutMs,
      workspaceDir: this.config.workspaceDir,
    });
  }
  
  /**
   * 调用模型
   */
  async invokeModel(request: ModelRequest, provider: OpenClawProvider): Promise<OpenClawInvocationResult> {
    const startTime = Date.now();
    const requestId = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    logger.debug('开始调用模型', {
      requestId,
      model: request.model,
      providerId: provider.id,
      messageCount: request.messages.length,
    });
    
    try {
      // 验证请求
      this.validateRequest(request, provider);
      
      // 根据提供商选择调用策略
      const result = await retry(
        () => this.executeInvocation(request, provider, requestId),
        this.config.maxRetries,
        2000 // 2秒重试间隔
      );
      
      const responseTime = Date.now() - startTime;
      
      const stats: InvocationStats = {
        providerId: provider.id,
        modelId: request.model,
        success: true,
        responseTime,
        tokensUsed: result.response.usage?.totalTokens || 0,
        timestamp: new Date(),
      };
      
      this.recordInvocation(stats);
      
      logger.info('模型调用成功', {
        requestId,
        model: request.model,
        responseTime,
        tokensUsed: stats.tokensUsed,
      });
      
      return result;
      
    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      const stats: InvocationStats = {
        providerId: provider.id,
        modelId: request.model,
        success: false,
        responseTime,
        tokensUsed: 0,
        error: (error as Error).message,
        timestamp: new Date(),
      };
      
      this.recordInvocation(stats);
      
      logger.error('模型调用失败', error as Error, {
        requestId,
        model: request.model,
        providerId: provider.id,
      });
      
      throw new RouterError(
        `OpenClaw模型调用失败: ${(error as Error).message}`,
        'OPENCLAW_INVOCATION_FAILED',
        { 
          requestId, 
          model: request.model,
          providerId: provider.id,
        }
      );
    }
  }
  
  /**
   * 验证请求
   */
  private validateRequest(request: ModelRequest, provider: OpenClawProvider): void {
    if (!request.model) {
      throw new RouterError('模型ID不能为空', 'INVALID_REQUEST');
    }
    
    if (!request.messages || request.messages.length === 0) {
      throw new RouterError('消息不能为空', 'INVALID_REQUEST');
    }
    
    // 检查模型是否被提供商支持
    const modelSupported = provider.models.some(model => model.id === request.model);
    if (!modelSupported) {
      throw new RouterError(
        `模型 ${request.model} 不被供应商 ${provider.id} 支持`,
        'UNSUPPORTED_MODEL',
        { 
          supportedModels: provider.models.map(m => m.id),
          requestedModel: request.model,
        }
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
    
    logger.debug('请求验证通过', {
      model: request.model,
      messageCount: request.messages.length,
    });
  }
  
  /**
   * 执行实际调用
   */
  private async executeInvocation(
    request: ModelRequest, 
    provider: OpenClawProvider, 
    requestId: string
  ): Promise<OpenClawInvocationResult> {
    // 根据提供商和配置选择调用策略
    const invocationStrategy = this.selectInvocationStrategy(provider);
    
    logger.debug('选择调用策略', {
      requestId,
      strategy: invocationStrategy,
      providerId: provider.id,
    });
    
    switch (invocationStrategy) {
      case 'cli-direct':
        return await this.invokeViaCliDirect(request, provider, requestId);
        
      case 'cli-session':
        return await this.invokeViaCliSession(request, provider, requestId);
        
      case 'temp-file':
        return await this.invokeViaTempFile(request, provider, requestId);
        
      default:
        // 默认使用CLI直接调用
        return await this.invokeViaCliDirect(request, provider, requestId);
    }
  }
  
  /**
   * 选择调用策略
   */
  private selectInvocationStrategy(provider: OpenClawProvider): string {
    // 默认策略：CLI直接调用
    // 可以根据提供商类型、模型特性等选择不同策略
    
    // 如果是DeepSeek，使用直接调用
    if (provider.id === 'deepseek') {
      return 'cli-direct';
    }
    
    // 对于其他提供商，使用临时文件方式
    return 'temp-file';
  }
  
  /**
   * 通过CLI直接调用
   */
  private async invokeViaCliDirect(
    request: ModelRequest, 
    provider: OpenClawProvider,
    requestId: string
  ): Promise<OpenClawInvocationResult> {
    logger.debug('使用CLI直接调用', { requestId, providerId: provider.id });
    
    try {
      // 构建OpenClaw CLI命令
      // 注意：这需要OpenClaw支持直接从CLI调用模型
      // 目前这是一个简化实现，实际使用时需要根据OpenClaw的实际CLI调整
      
      const messagesJson = JSON.stringify(request.messages);
      const modelArg = request.model;
      
      // 构建基本命令
      let command = `${this.config.openclawPath} `;
      
      // 尝试使用models子命令（如果支持）
      command += `models invoke --model "${modelArg}" --messages '${messagesJson}'`;
      
      // 添加可选参数
      if (request.maxTokens) {
        command += ` --max-tokens ${request.maxTokens}`;
      }
      
      if (request.temperature !== undefined) {
        command += ` --temperature ${request.temperature}`;
      }
      
      logger.debug('执行CLI命令', { 
        requestId,
        command: command.substring(0, 100) + '...', // 截断长命令
      });
      
      // 执行命令
      const { stdout, stderr } = await execAsync(command, {
        timeout: this.config.timeoutMs,
        cwd: this.config.workspaceDir,
      });
      
      if (stderr && stderr.trim()) {
        logger.warn('CLI命令有stderr输出', { 
          requestId,
          stderr: stderr.substring(0, 200),
        });
      }
      
      // 解析响应
      try {
        const responseData = JSON.parse(stdout);
        
        const modelResponse: ModelResponse = {
          id: responseData.id || requestId,
          content: responseData.content || responseData.text || '',
          model: responseData.model || request.model,
          usage: {
            promptTokens: responseData.usage?.prompt_tokens || responseData.usage?.promptTokens || 0,
            completionTokens: responseData.usage?.completion_tokens || responseData.usage?.completionTokens || 0,
            totalTokens: responseData.usage?.total_tokens || responseData.usage?.totalTokens || 0,
          },
          finishReason: responseData.finish_reason || responseData.finishReason || 'stop',
        };
        
        logger.debug('CLI调用成功解析', {
          requestId,
          contentLength: modelResponse.content.length,
          tokenUsage: modelResponse.usage.totalTokens,
        });
        
        return {
          response: modelResponse,
          stats: {
            providerId: provider.id,
            modelId: request.model,
            success: true,
            responseTime: 0, // 在外层计算
            tokensUsed: modelResponse.usage.totalTokens,
            timestamp: new Date(),
          },
        };
        
      } catch (parseError) {
        // 如果JSON解析失败，尝试提取文本内容
        logger.debug('CLI响应不是JSON，尝试提取文本', { 
          requestId,
          stdoutPreview: stdout.substring(0, 200),
        });
        
        const modelResponse: ModelResponse = {
          id: requestId,
          content: stdout.trim(),
          model: request.model,
          usage: {
            promptTokens: 0,
            completionTokens: 0,
            totalTokens: 0,
          },
          finishReason: 'stop',
        };
        
        return {
          response: modelResponse,
          stats: {
            providerId: provider.id,
            modelId: request.model,
            success: true,
            responseTime: 0,
            tokensUsed: 0,
            timestamp: new Date(),
          },
        };
      }
      
    } catch (error) {
      logger.error('CLI直接调用失败', error as Error, { requestId });
      throw error;
    }
  }
  
  /**
   * 通过CLI会话调用
   */
  private async invokeViaCliSession(
    request: ModelRequest, 
    provider: OpenClawProvider,
    requestId: string
  ): Promise<OpenClawInvocationResult> {
    logger.debug('使用CLI会话调用', { requestId, providerId: provider.id });
    
    // 创建临时会话文件
    const sessionFile = path.join(this.config.tempDir, `${requestId}_session.json`);
    
    const sessionData = {
      requestId,
      provider: provider.id,
      model: request.model,
      messages: request.messages,
      config: {
        maxTokens: request.maxTokens,
        temperature: request.temperature,
      },
      timestamp: new Date().toISOString(),
    };
    
    await fs.promises.writeFile(sessionFile, JSON.stringify(sessionData, null, 2));
    
    try {
      // 使用OpenClaw CLI处理会话文件
      const command = `${this.config.openclawPath} session process --file "${sessionFile}"`;
      
      const { stdout } = await execAsync(command, {
        timeout: this.config.timeoutMs,
        cwd: this.config.workspaceDir,
      });
      
      // 解析响应
      const responseData = JSON.parse(stdout);
      
      const modelResponse: ModelResponse = {
        id: responseData.id || requestId,
        content: responseData.content || '',
        model: responseData.model || request.model,
        usage: responseData.usage || { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
        finishReason: responseData.finishReason || 'stop',
      };
      
      // 清理临时文件
      await fs.promises.unlink(sessionFile).catch(() => {
        // 忽略清理错误
      });
      
      return {
        response: modelResponse,
        stats: {
          providerId: provider.id,
          modelId: request.model,
          success: true,
          responseTime: 0,
          tokensUsed: modelResponse.usage.totalTokens,
          timestamp: new Date(),
        },
      };
      
    } catch (error) {
      // 尝试清理临时文件
      await fs.promises.unlink(sessionFile).catch(() => {
        // 忽略清理错误
      });
      
      throw error;
    }
  }
  
  /**
   * 通过临时文件调用
   */
  private async invokeViaTempFile(
    request: ModelRequest, 
    provider: OpenClawProvider,
    requestId: string
  ): Promise<OpenClawInvocationResult> {
    logger.debug('使用临时文件调用', { requestId, providerId: provider.id });
    
    // 创建临时请求文件
    const requestFile = path.join(this.config.tempDir, `${requestId}_request.json`);
    
    const requestData: TempRequestFile = {
      request: {
        model: request.model,
        messages: request.messages,
        max_tokens: request.maxTokens,
        temperature: request.temperature,
        stream: false,
      },
      metadata: {
        requestId,
        timestamp: new Date().toISOString(),
        providerId: provider.id,
      },
    };
    
    await fs.promises.writeFile(requestFile, JSON.stringify(requestData, null, 2));
    
    try {
      // 使用OpenClaw CLI处理请求文件
      // 假设有一个处理JSON请求文件的命令
      const command = `${this.config.openclawPath} process-request --file "${requestFile}"`;
      
      const { stdout } = await execAsync(command, {
        timeout: this.config.timeoutMs,
        cwd: this.config.workspaceDir,
      });
      
      // 解析响应
      const responseData = JSON.parse(stdout);
      
      const modelResponse: ModelResponse = {
        id: responseData.id || requestId,
        content: responseData.content || '',
        model: responseData.model || request.model,
        usage: responseData.usage || { promptTokens: 0, completionTokens: 0, totalTokens: 0 },
        finishReason: responseData.finishReason || 'stop',
      };
      
      // 清理临时文件
      await fs.promises.unlink(requestFile).catch(() => {
        // 忽略清理错误
      });
      
      return {
        response: modelResponse,
        stats: {
          providerId: provider.id,
          modelId: request.model,
          success: true,
          responseTime: 0,
          tokensUsed: modelResponse.usage.totalTokens,
          timestamp: new Date(),
        },
      };
      
    } catch (error) {
      // 尝试清理临时文件
      await fs.promises.unlink(requestFile).catch(() => {
        // 忽略清理错误
      });
      
      throw error;
    }
  }
  
  /**
   * 记录调用统计
   */
  private recordInvocation(stats: InvocationStats): void {
    this.invocationHistory.push(stats);
    
    // 保持历史记录大小
    if (this.invocationHistory.length > this.maxHistorySize) {
      this.invocationHistory = this.invocationHistory.slice(-this.maxHistorySize);
    }
    
    const logData = {
      providerId: stats.providerId,
      modelId: stats.modelId,
      success: stats.success,
      responseTime: stats.responseTime,
      tokensUsed: stats.tokensUsed,
    };
    
    if (stats.success) {
      logger.debug('模型调用记录', logData);
    } else {
      logger.warn('模型调用失败记录', { ...logData, error: stats.error });
    }
  }
  
  /**
   * 获取调用历史
   */
  getInvocationHistory(limit?: number): InvocationStats[] {
    const history = [...this.invocationHistory].reverse(); // 最新的在前面
    return limit ? history.slice(0, limit) : history;
  }
  
  /**
   * 获取成功率统计
   */
  getSuccessRate(): number {
    if (this.invocationHistory.length === 0) return 0;
    
    const successfulInvocations = this.invocationHistory.filter(inv => inv.success).length;
    return successfulInvocations / this.invocationHistory.length;
  }
  
  /**
   * 获取平均响应时间
   */
  getAverageResponseTime(): number {
    if (this.invocationHistory.length === 0) return 0;
    
    const totalTime = this.invocationHistory.reduce((sum, inv) => sum + inv.responseTime, 0);
    return totalTime / this.invocationHistory.length;
  }
  
  /**
   * 获取提供商成功率
   */
  getProviderSuccessRate(providerId: string): number {
    const providerInvocations = this.invocationHistory.filter(inv => inv.providerId === providerId);
    
    if (providerInvocations.length === 0) return 0;
    
    const successful = providerInvocations.filter(inv => inv.success).length;
    return successful / providerInvocations.length;
  }
  
  /**
   * 获取配置
   */
  getConfig(): OpenClawInvokerConfig {
    return { ...this.config };
  }
  
  /**
   * 更新配置
   */
  updateConfig(updates: Partial<OpenClawInvokerConfig>): void {
    this.config = { ...this.config, ...updates };
    logger.debug('调用器配置更新', { updates });
  }
  
  /**
   * 清理临时文件
   */
  async cleanupTempFiles(): Promise<void> {
    try {
      const files = await fs.promises.readdir(this.config.tempDir);
      
      const cleanupPromises = files.map(async (file) => {
        const filePath = path.join(this.config.tempDir, file);
        const stats = await fs.promises.stat(filePath);
        
        // 删除超过1小时的临时文件
        const age = Date.now() - stats.mtimeMs;
        if (age > 3600000) { // 1小时
          await fs.promises.unlink(filePath);
          logger.debug('清理旧临时文件', { file, age });
        }
      });
      
      await Promise.all(cleanupPromises);
      logger.info('临时文件清理完成', { tempDir: this.config.tempDir });
      
    } catch (error) {
      logger.warn('临时文件清理失败', error as Error);
    }
  }
}

/**
 * 调用器工厂
 */
export class OpenClawInvokerFactory {
  private static instance: OpenClawInvoker;
  
  static getInstance(config?: Partial<OpenClawInvokerConfig>): OpenClawInvoker {
    if (!OpenClawInvokerFactory.instance) {
      OpenClawInvokerFactory.instance = new OpenClawInvoker(config);
      logger.info('创建OpenClaw调用器单例');
    }
    
    return OpenClawInvokerFactory.instance;
  }
  
  static destroyInstance(): void {
    if (OpenClawInvokerFactory.instance) {
      OpenClawInvokerFactory.instance.cleanupTempFiles().catch(() => {
        // 忽略清理错误
      });
      OpenClawInvokerFactory.instance = null as any;
      logger.info('销毁OpenClaw调用器单例');
    }
  }
}
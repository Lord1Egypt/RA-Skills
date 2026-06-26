/**
 * MCP 视频生成总线
 * 
 * 层级：Layer 8.5 - Governance Control Plane
 * 功能：视频生成任务的 MCP 通信、全链路追踪、幂等键管理
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest, VideoGenerationResponse } from './comfyui-workflow-orchestrator';

// ============== 类型定义 ==============

/**
 * MCP 消息类型
 */
export type MCPMessageType =
  | 'video.generate.request'
  | 'video.generate.response'
  | 'video.generate.progress'
  | 'video.generate.error'
  | 'video.quality.check.request'
  | 'video.quality.check.response'
  | 'video.deploy.request'
  | 'video.deploy.response';

/**
 * MCP 消息头
 */
export interface MCPMessageHeaders {
  /** 追踪 ID */
  traceId: string;
  /** 幂等键 */
  idempotencyKey: string;
  /** 消息类型 */
  type: MCPMessageType;
  /** 发送方 */
  from: string;
  /** 接收方 */
  to: string;
  /** 时间戳 */
  timestamp: number;
  /** TTL (秒) */
  ttlSeconds: number;
  /** 过期时间 */
  expiresAt: number;
}

/**
 * MCP 消息体
 */
export interface MCPMessageBody<T = any> {
  /** 请求/响应数据 */
  data: T;
  /** 元数据 */
  metadata?: {
    projectId?: string;
    taskId?: string;
    priority?: number;
    tags?: string[];
  };
}

/**
 * MCP 消息
 */
export interface MCPMessage<T = any> {
  /** 消息头 */
  headers: MCPMessageHeaders;
  /** 消息体 */
  body: MCPMessageBody<T>;
}

/**
 * MCP 消息处理结果
 */
export interface MCPMessageResult {
  /** 处理状态 */
  status: 'success' | 'failed' | 'pending';
  /** 消息 ID */
  messageId: string;
  /** 处理耗时 (ms) */
  durationMs?: number;
  /** 错误信息 */
  error?: string;
}

/**
 * MCP 总线配置
 */
export interface MCPBusConfig {
  /** 默认 TTL (秒) */
  defaultTTLSeconds: number;
  /** 消息重试次数 */
  maxRetries: number;
  /** 重试间隔 (ms) */
  retryIntervalMs: number;
  /** 启用追踪 */
  enableTracing: boolean;
  /** 启用幂等性检查 */
  enableIdempotency: boolean;
}

// ============== 默认配置 ==============

const DEFAULT_MCP_BUS_CONFIG: MCPBusConfig = {
  defaultTTLSeconds: 300, // 5 分钟
  maxRetries: 3,
  retryIntervalMs: 1000,
  enableTracing: true,
  enableIdempotency: true,
};

// ============== 工具函数 ==============

/**
 * 生成追踪 ID
 */
function generateTraceId(): string {
  return `trace_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
}

/**
 * 生成幂等键
 */
function generateIdempotencyKey(request: VideoGenerationRequest): string {
  const hash = JSON.stringify({
    prompt: request.prompt,
    duration: request.durationSeconds,
    resolution: request.resolution,
  });
  return `idem_${Buffer.from(hash).toString('base64').substring(0, 32)}`;
}

// ============== 核心类 ==============

/**
 * MCP 视频生成总线
 */
export class MCPVideoBus {
  private config: MCPBusConfig;
  private messageQueue: Map<string, MCPMessage[]> = new Map();
  private idempotencyCache: Map<string, MCPMessageResult> = new Map();
  private traceStore: Map<string, MCPMessage[]> = new Map();
  private listeners: Map<string, Array<(message: MCPMessage) => void>> = new Map();

  constructor(config: Partial<MCPBusConfig> = {}) {
    this.config = { ...DEFAULT_MCP_BUS_CONFIG, ...config };
  }

  /**
   * 发送消息
   */
  async send<T>(message: MCPMessage<T>): Promise<MCPMessageResult> {
    const startTime = Date.now();
    const messageId = generateTraceId();

    try {
      // 1. 检查幂等性
      if (this.config.enableIdempotency) {
        const cachedResult = this.idempotencyCache.get(message.headers.idempotencyKey);
        if (cachedResult) {
          console.log(`[MCP Bus] ⚡ Idempotency cache hit: ${message.headers.idempotencyKey}`);
          return cachedResult;
        }
      }

      // 2. 检查消息过期
      if (Date.now() > message.headers.expiresAt) {
        throw new Error(`Message expired: ${message.headers.idempotencyKey}`);
      }

      // 3. 存储追踪信息
      if (this.config.enableTracing) {
        this.storeTrace(message);
      }

      // 4. 添加到队列
      this.enqueue(message);

      // 5. 通知监听器
      this.notifyListeners(message);

      // 6. 返回成功结果
      const result: MCPMessageResult = {
        status: 'success',
        messageId,
        durationMs: Date.now() - startTime,
      };

      // 7. 缓存幂等结果
      if (this.config.enableIdempotency) {
        this.idempotencyCache.set(message.headers.idempotencyKey, result);
      }

      return result;
    } catch (error) {
      return {
        status: 'failed',
        messageId,
        durationMs: Date.now() - startTime,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  /**
   * 创建视频生成请求消息
   */
  createGenerateRequest(
    request: VideoGenerationRequest,
    from: string,
    to: string
  ): MCPMessage<VideoGenerationRequest> {
    const traceId = generateTraceId();
    const idempotencyKey = generateIdempotencyKey(request);
    const now = Date.now();

    return {
      headers: {
        traceId,
        idempotencyKey,
        type: 'video.generate.request',
        from,
        to,
        timestamp: now,
        ttlSeconds: this.config.defaultTTLSeconds,
        expiresAt: now + this.config.defaultTTLSeconds * 1000,
      },
      body: {
        data: request,
        metadata: {
          taskId: traceId,
          priority: 5,
          tags: ['video', 'generation', 'comfyui'],
        },
      },
    };
  }

  /**
   * 创建视频生成响应消息
   */
  createGenerateResponse(
    response: VideoGenerationResponse,
    traceId: string,
    from: string,
    to: string
  ): MCPMessage<VideoGenerationResponse> {
    const now = Date.now();

    return {
      headers: {
        traceId,
        idempotencyKey: `response_${traceId}`,
        type: 'video.generate.response',
        from,
        to,
        timestamp: now,
        ttlSeconds: 60,
        expiresAt: now + 60 * 1000,
      },
      body: {
        data: response,
      },
    };
  }

  /**
   * 创建质量检查请求消息
   */
  createQualityCheckRequest(
    response: VideoGenerationResponse,
    from: string,
    to: string
  ): MCPMessage<VideoGenerationResponse> {
    const traceId = generateTraceId();
    const now = Date.now();

    return {
      headers: {
        traceId,
        idempotencyKey: `quality_${traceId}`,
        type: 'video.quality.check.request',
        from,
        to,
        timestamp: now,
        ttlSeconds: 120,
        expiresAt: now + 120 * 1000,
      },
      body: {
        data: response,
        metadata: {
          priority: 8, // 高质量检查优先级
          tags: ['video', 'quality', 'guard'],
        },
      },
    };
  }

  /**
   * 创建部署请求消息
   */
  createDeployRequest(
    videoPath: string,
    qualityScore: number,
    from: string,
    to: string
  ): MCPMessage<{ videoPath: string; qualityScore: number }> {
    const traceId = generateTraceId();
    const now = Date.now();

    return {
      headers: {
        traceId,
        idempotencyKey: `deploy_${traceId}`,
        type: 'video.deploy.request',
        from,
        to,
        timestamp: now,
        ttlSeconds: 300,
        expiresAt: now + 300 * 1000,
      },
      body: {
        data: { videoPath, qualityScore },
        metadata: {
          priority: 10, // 部署最高优先级
          tags: ['video', 'deploy', 'production'],
        },
      },
    };
  }

  /**
   * 注册消息监听器
   */
  on(messageType: MCPMessageType, handler: (message: MCPMessage) => void): void {
    if (!this.listeners.has(messageType)) {
      this.listeners.set(messageType, []);
    }
    this.listeners.get(messageType)!.push(handler);
    console.log(`[MCP Bus] 📡 Listener registered for ${messageType}`);
  }

  /**
   * 获取追踪信息
   */
  getTrace(traceId: string): MCPMessage[] | undefined {
    return this.traceStore.get(traceId);
  }

  /**
   * 获取队列状态
   */
  getQueueStatus(): {
    totalMessages: number;
    tracesCount: number;
    idempotencyCacheSize: number;
  } {
    let totalMessages = 0;
    this.messageQueue.forEach(messages => {
      totalMessages += messages.length;
    });

    return {
      totalMessages,
      tracesCount: this.traceStore.size,
      idempotencyCacheSize: this.idempotencyCache.size,
    };
  }

  /**
   * 清理过期缓存
   */
  cleanupExpiredCache(): number {
    const now = Date.now();
    let cleaned = 0;

    // 清理幂等缓存 (保留最近 1 小时)
    this.idempotencyCache.forEach((_, key) => {
      // 简单策略：缓存超过 1000 条时清理最早的 50%
      if (this.idempotencyCache.size > 1000) {
        this.idempotencyCache.delete(key);
        cleaned++;
      }
    });

    return cleaned;
  }

  // ============== 私有方法 ==============

  /**
   * 存储追踪信息
   */
  private storeTrace(message: MCPMessage): void {
    const traceId = message.headers.traceId;
    if (!this.traceStore.has(traceId)) {
      this.traceStore.set(traceId, []);
    }
    this.traceStore.get(traceId)!.push(message);
  }

  /**
   * 添加到队列
   */
  private enqueue(message: MCPMessage): void {
    const key = message.headers.type;
    if (!this.messageQueue.has(key)) {
      this.messageQueue.set(key, []);
    }
    this.messageQueue.get(key)!.push(message);
  }

  /**
   * 通知监听器
   */
  private notifyListeners(message: MCPMessage): void {
    const handlers = this.listeners.get(message.headers.type);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message);
        } catch (error) {
          console.error(`[MCP Bus] Listener error: ${error}`);
        }
      });
    }
  }
}

// ============== 导出 ==============

export default MCPVideoBus;

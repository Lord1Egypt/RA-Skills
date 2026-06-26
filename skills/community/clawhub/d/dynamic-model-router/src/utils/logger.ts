/**
 * 动态模型路由技能 - 日志系统
 */

import winston from 'winston';
import path from 'path';
import fs from 'fs';

// 确保日志目录存在
const logDir = path.join(process.env.HOME || process.env.USERPROFILE || '.', '.openclaw', 'logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// 日志级别
export enum LogLevel {
  ERROR = 'error',
  WARN = 'warn',
  INFO = 'info',
  DEBUG = 'debug',
}

// 日志格式
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    let log = `${timestamp} [${level.toUpperCase()}] ${message}`;
    
    if (Object.keys(meta).length > 0) {
      // 过滤掉不必要的字段
      const filteredMeta = { ...meta };
      delete filteredMeta.timestamp;
      delete filteredMeta.level;
      delete filteredMeta.message;
      
      if (Object.keys(filteredMeta).length > 0) {
        log += ` ${JSON.stringify(filteredMeta)}`;
      }
    }
    
    return log;
  })
);

// 创建日志记录器
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  defaultMeta: { service: 'dynamic-model-router' },
  transports: [
    // 错误日志文件
    new winston.transports.File({
      filename: path.join(logDir, 'router-error.log'),
      level: 'error',
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
    }),
    // 所有日志文件
    new winston.transports.File({
      filename: path.join(logDir, 'router-combined.log'),
      maxsize: 10 * 1024 * 1024, // 10MB
      maxFiles: 5,
    }),
  ],
});

// 开发环境时也输出到控制台
if (process.env.NODE_ENV !== 'production') {
  const consoleFormat = winston.format.combine(
    winston.format.colorize(),
    winston.format.timestamp({ format: 'HH:mm:ss.SSS' }),
    winston.format.printf(({ timestamp, level, message, ...meta }) => {
      let log = `${timestamp} [${level}] ${message}`;
      
      if (Object.keys(meta).length > 0) {
        const filteredMeta = { ...meta };
        delete filteredMeta.timestamp;
        delete filteredMeta.level;
        delete filteredMeta.message;
        
        if (Object.keys(filteredMeta).length > 0) {
          log += ` ${JSON.stringify(filteredMeta, null, 2)}`;
        }
      }
      
      return log;
    })
  );
  
  logger.add(new winston.transports.Console({
    format: consoleFormat,
  }));
}

// 日志接口
export interface LogContext {
  taskId?: string;
  modelId?: string;
  provider?: string;
  decisionId?: string;
  [key: string]: any;
}

// 日志包装器
export class RouterLogger {
  private context: LogContext = {};
  
  constructor(defaultContext: LogContext = {}) {
    this.context = { ...defaultContext };
  }
  
  // 设置上下文
  setContext(context: LogContext): void {
    this.context = { ...this.context, ...context };
  }
  
  // 添加上下文
  addContext(key: string, value: any): void {
    this.context[key] = value;
  }
  
  // 清除上下文
  clearContext(): void {
    this.context = {};
  }
  
  // 错误日志
  error(message: string, error?: Error, extra?: LogContext): void {
    const meta = { ...this.context, ...extra };
    
    if (error) {
      meta.error = {
        message: error.message,
        stack: error.stack,
        name: error.name,
      };
    }
    
    logger.error(message, meta);
  }
  
  // 警告日志
  warn(message: string, extra?: LogContext): void {
    const meta = { ...this.context, ...extra };
    logger.warn(message, meta);
  }
  
  // 信息日志
  info(message: string, extra?: LogContext): void {
    const meta = { ...this.context, ...extra };
    logger.info(message, meta);
  }
  
  // 调试日志
  debug(message: string, extra?: LogContext): void {
    const meta = { ...this.context, ...extra };
    logger.debug(message, meta);
  }
  
  // 路由决策日志
  logDecision(
    taskId: string,
    selectedModel: string,
    selectedProvider: string,
    confidence: number,
    alternatives: Array<{ model: string; provider: string; score: number }>,
    reasoning: string
  ): void {
    this.info('路由决策完成', {
      taskId,
      selectedModel,
      selectedProvider,
      confidence: confidence.toFixed(3),
      alternatives: alternatives.map(a => `${a.model}@${a.provider}:${a.score.toFixed(3)}`),
      reasoning,
    });
  }
  
  // 模型调用日志
  logModelCall(
    modelId: string,
    provider: string,
    success: boolean,
    responseTime: number,
    tokensUsed: number,
    error?: string
  ): void {
    const level = success ? 'info' : 'error';
    const message = success ? '模型调用成功' : '模型调用失败';
    
    const meta: LogContext = {
      modelId,
      provider,
      responseTime,
      tokensUsed,
    };
    
    if (error) {
      meta.error = error;
    }
    
    if (level === 'info') {
      this.info(message, meta);
    } else {
      this.error(message, undefined, meta);
    }
  }
  
  // 性能指标日志
  logPerformance(
    operation: string,
    duration: number,
    success: boolean,
    extra?: LogContext
  ): void {
    const meta = { 
      ...this.context, 
      ...extra,
      operation,
      duration,
      success,
    };
    
    const level = success ? 'debug' : 'warn';
    const message = `${operation} 执行 ${success ? '成功' : '失败'} (${duration}ms)`;
    
    if (level === 'debug') {
      this.debug(message, meta);
    } else {
      this.warn(message, meta);
    }
  }
  
  // 配置变更日志
  logConfigChange(
    key: string,
    oldValue: any,
    newValue: any,
    reason: string
  ): void {
    this.info('配置变更', {
      configKey: key,
      oldValue: typeof oldValue === 'object' ? JSON.stringify(oldValue) : oldValue,
      newValue: typeof newValue === 'object' ? JSON.stringify(newValue) : newValue,
      reason,
    });
  }
}

// 默认日志记录器
export const defaultLogger = new RouterLogger();

// 导出winston实例以供直接使用
export { logger };

// 辅助函数：创建任务特定的日志记录器
export function createTaskLogger(taskId: string): RouterLogger {
  return new RouterLogger({ taskId });
}

// 辅助函数：创建模型特定的日志记录器
export function createModelLogger(modelId: string, provider: string): RouterLogger {
  return new RouterLogger({ modelId, provider });
}
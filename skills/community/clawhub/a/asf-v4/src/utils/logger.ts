/**
 * Logger Utility - ANFSF v2.0
 * 
 * 统一日志记录工具，提供一致的日志格式和级别控制
 * 
 * @module asf-v4/utils/logger
 */

export interface LoggerConfig {
  level: 'debug' | 'info' | 'warn' | 'error';
  prefix: string;
  timestamp: boolean;
}

export class Logger {
  private config: LoggerConfig;

  constructor(config?: Partial<LoggerConfig>) {
    this.config = {
      level: 'info',
      prefix: '[ANFSF]',
      timestamp: true,
      ...config,
    };
  }

  debug(message: string, ...args: any[]): void {
    if (this.shouldLog('debug')) {
      this.log('DEBUG', message, args);
    }
  }

  info(message: string, ...args: any[]): void {
    if (this.shouldLog('info')) {
      this.log('INFO', message, args);
    }
  }

  warn(message: string, ...args: any[]): void {
    if (this.shouldLog('warn')) {
      this.log('WARN', message, args);
    }
  }

  error(message: string, ...args: any[]): void {
    if (this.shouldLog('error')) {
      this.log('ERROR', message, args);
    }
  }

  private shouldLog(level: string): boolean {
    const levels = ['debug', 'info', 'warn', 'error'];
    const currentLevelIndex = levels.indexOf(this.config.level);
    const requestedLevelIndex = levels.indexOf(level);
    return requestedLevelIndex >= currentLevelIndex;
  }

  private log(level: string, message: string, args: any[]): void {
    let output = '';
    
    if (this.config.timestamp) {
      output += `${new Date().toISOString()} `;
    }
    
    output += `${this.config.prefix} [${level}] ${message}`;
    
    console.log(output, ...args);
  }
}

// 默认全局 logger
export const defaultLogger = new Logger({
  level: 'info',
  prefix: '[ANFSF]',
  timestamp: true,
});

// 模块特定 logger 工厂
export function createModuleLogger(moduleName: string): Logger {
  return new Logger({
    level: 'info',
    prefix: `[${moduleName}]`,
    timestamp: true,
  });
}
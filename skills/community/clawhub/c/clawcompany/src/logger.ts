/**
 * 日志系统
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

export class Logger {
  private level: LogLevel
  private prefix: string
  
  constructor(prefix: string = 'ClawCompany', level: LogLevel = LogLevel.INFO) {
    this.prefix = prefix
    this.level = level
  }
  
  setLevel(level: LogLevel) {
    this.level = level
  }
  
  debug(message: string, ...args: any[]) {
    if (this.level <= LogLevel.DEBUG) {
      console.log(`[${this.prefix}] DEBUG: ${message}`, ...args)
    }
  }
  
  info(message: string, ...args: any[]) {
    if (this.level <= LogLevel.INFO) {
      console.log(`[${this.prefix}] ${message}`, ...args)
    }
  }
  
  warn(message: string, ...args: any[]) {
    if (this.level <= LogLevel.WARN) {
      console.warn(`[${this.prefix}] ⚠️  ${message}`, ...args)
    }
  }
  
  error(message: string, error?: Error) {
    if (this.level <= LogLevel.ERROR) {
      console.error(`[${this.prefix}] ❌ ${message}`)
      if (error) {
        console.error(error)
      }
    }
  }
  
  success(message: string) {
    console.log(`[${this.prefix}] ✅ ${message}`)
  }
  
  step(step: number, total: number, message: string) {
    console.log(`[${this.prefix}] [${step}/${total}] ${message}`)
  }
}

export const logger = new Logger()

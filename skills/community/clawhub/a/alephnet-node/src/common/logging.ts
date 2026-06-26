/**
 * Logging Infrastructure
 * 
 * Centralized structured logging for AlephNet.
 * Provides consistent log formatting, levels, and context propagation.
 */

import { LOG_LEVELS, LogLevel } from './constants';
import { SMFVector, SemanticDomain } from './types';
import { generateId } from './hash';

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Log context that gets attached to all log entries
 */
export interface LogContext {
  nodeId?: string;
  conversationId?: string;
  sessionId?: string;
  requestId?: string;
  userId?: string;
  service?: string;
  component?: string;
  domain?: SemanticDomain;
  [key: string]: unknown;
}

/**
 * Structured log entry
 */
export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context: LogContext;
  data?: Record<string, unknown>;
  error?: {
    name: string;
    message: string;
    stack?: string;
    code?: string;
  };
  metrics?: {
    durationMs?: number;
    smf?: SMFVector;
    coherence?: number;
  };
}

/**
 * Log output transport
 */
export interface LogTransport {
  log(entry: LogEntry): void;
}

// ═══════════════════════════════════════════════════════════════════════════
// TRANSPORTS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Console transport - outputs to console
 */
export class ConsoleTransport implements LogTransport {
  private useColors: boolean;
  
  constructor(options?: { colors?: boolean }) {
    this.useColors = options?.colors ?? (process.stdout.isTTY || false);
  }
  
  log(entry: LogEntry): void {
    const formatted = this.format(entry);
    
    switch (entry.level) {
      case 'ERROR':
      case 'FATAL':
        console.error(formatted);
        break;
      case 'WARN':
        console.warn(formatted);
        break;
      default:
        console.log(formatted);
    }
  }
  
  private format(entry: LogEntry): string {
    if (this.useColors) {
      return this.formatColored(entry);
    }
    return this.formatPlain(entry);
  }
  
  private formatPlain(entry: LogEntry): string {
    const parts = [
      entry.timestamp,
      `[${entry.level}]`,
      entry.context.component ? `[${entry.context.component}]` : '',
      entry.message
    ].filter(Boolean);
    
    if (entry.data) {
      parts.push(JSON.stringify(entry.data));
    }
    
    if (entry.error) {
      parts.push(`Error: ${entry.error.message}`);
      if (entry.error.stack) {
        parts.push(`\n${entry.error.stack}`);
      }
    }
    
    return parts.join(' ');
  }
  
  private formatColored(entry: LogEntry): string {
    const colors = {
      TRACE: '\x1b[90m',  // Gray
      DEBUG: '\x1b[36m',  // Cyan
      INFO: '\x1b[32m',   // Green
      WARN: '\x1b[33m',   // Yellow
      ERROR: '\x1b[31m',  // Red
      FATAL: '\x1b[35m',  // Magenta
      reset: '\x1b[0m'
    };
    
    const color = colors[entry.level] || colors.reset;
    const parts = [
      `\x1b[90m${entry.timestamp}\x1b[0m`,
      `${color}[${entry.level}]${colors.reset}`,
      entry.context.component ? `\x1b[90m[${entry.context.component}]\x1b[0m` : '',
      entry.message
    ].filter(Boolean);
    
    if (entry.data) {
      parts.push(`\x1b[90m${JSON.stringify(entry.data)}\x1b[0m`);
    }
    
    if (entry.error) {
      parts.push(`\x1b[31mError: ${entry.error.message}\x1b[0m`);
      if (entry.error.stack) {
        parts.push(`\x1b[90m\n${entry.error.stack}\x1b[0m`);
      }
    }
    
    return parts.join(' ');
  }
}

/**
 * JSON transport - outputs JSON lines
 */
export class JsonTransport implements LogTransport {
  constructor(private stream: { write: (s: string) => void } = process.stdout) {}
  
  log(entry: LogEntry): void {
    this.stream.write(JSON.stringify(entry) + '\n');
  }
}

/**
 * Memory transport - stores logs in memory (useful for testing)
 */
export class MemoryTransport implements LogTransport {
  private logs: LogEntry[] = [];
  private maxSize: number;
  
  constructor(maxSize: number = 1000) {
    this.maxSize = maxSize;
  }
  
  log(entry: LogEntry): void {
    this.logs.push(entry);
    if (this.logs.length > this.maxSize) {
      this.logs.shift();
    }
  }
  
  getAll(): LogEntry[] {
    return [...this.logs];
  }
  
  getByLevel(level: LogLevel): LogEntry[] {
    return this.logs.filter(e => e.level === level);
  }
  
  search(predicate: (entry: LogEntry) => boolean): LogEntry[] {
    return this.logs.filter(predicate);
  }
  
  clear(): void {
    this.logs = [];
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// LOGGER
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Logger configuration
 */
export interface LoggerConfig {
  level: LogLevel;
  transports: LogTransport[];
  defaultContext?: LogContext;
}

/**
 * Main Logger class
 */
export class Logger {
  private level: number;
  private transports: LogTransport[];
  private context: LogContext;
  
  constructor(config: Partial<LoggerConfig> = {}) {
    this.level = LOG_LEVELS[config.level || 'INFO'];
    this.transports = config.transports || [new ConsoleTransport()];
    this.context = config.defaultContext || {};
  }
  
  /**
   * Create a child logger with additional context
   */
  child(context: LogContext): Logger {
    const child = new Logger({
      level: Object.keys(LOG_LEVELS).find(k => LOG_LEVELS[k as LogLevel] === this.level) as LogLevel,
      transports: this.transports
    });
    child.context = { ...this.context, ...context };
    return child;
  }
  
  /**
   * Set the log level
   */
  setLevel(level: LogLevel): void {
    this.level = LOG_LEVELS[level];
  }
  
  /**
   * Add a transport
   */
  addTransport(transport: LogTransport): void {
    this.transports.push(transport);
  }
  
  /**
   * Log at TRACE level
   */
  trace(message: string, data?: Record<string, unknown>): void {
    this.log('TRACE', message, data);
  }
  
  /**
   * Log at DEBUG level
   */
  debug(message: string, data?: Record<string, unknown>): void {
    this.log('DEBUG', message, data);
  }
  
  /**
   * Log at INFO level
   */
  info(message: string, data?: Record<string, unknown>): void {
    this.log('INFO', message, data);
  }
  
  /**
   * Log at WARN level
   */
  warn(message: string, data?: Record<string, unknown>): void {
    this.log('WARN', message, data);
  }
  
  /**
   * Log at ERROR level
   */
  error(message: string, error?: Error | Record<string, unknown>, data?: Record<string, unknown>): void {
    if (error instanceof Error) {
      this.logWithError('ERROR', message, error, data);
    } else {
      this.log('ERROR', message, error);
    }
  }
  
  /**
   * Log at FATAL level
   */
  fatal(message: string, error?: Error | Record<string, unknown>, data?: Record<string, unknown>): void {
    if (error instanceof Error) {
      this.logWithError('FATAL', message, error, data);
    } else {
      this.log('FATAL', message, error);
    }
  }
  
  /**
   * Log with timing information
   */
  timed<T>(message: string, fn: () => T): T {
    const start = Date.now();
    try {
      const result = fn();
      const durationMs = Date.now() - start;
      this.info(message, { durationMs });
      return result;
    } catch (error) {
      const durationMs = Date.now() - start;
      this.error(message, error as Error, { durationMs });
      throw error;
    }
  }
  
  /**
   * Log with timing information (async)
   */
  async timedAsync<T>(message: string, fn: () => Promise<T>): Promise<T> {
    const start = Date.now();
    try {
      const result = await fn();
      const durationMs = Date.now() - start;
      this.info(message, { durationMs });
      return result;
    } catch (error) {
      const durationMs = Date.now() - start;
      this.error(message, error as Error, { durationMs });
      throw error;
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════════════
  
  private log(level: LogLevel, message: string, data?: Record<string, unknown>): void {
    if (LOG_LEVELS[level] < this.level) return;
    
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: this.context,
      data
    };
    
    for (const transport of this.transports) {
      try {
        transport.log(entry);
      } catch (e) {
        // Don't let transport errors break logging
      }
    }
  }
  
  private logWithError(
    level: LogLevel,
    message: string,
    error: Error,
    data?: Record<string, unknown>
  ): void {
    if (LOG_LEVELS[level] < this.level) return;
    
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: this.context,
      data,
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
        code: (error as any).code
      }
    };
    
    for (const transport of this.transports) {
      try {
        transport.log(entry);
      } catch (e) {
        // Don't let transport errors break logging
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL LOGGER
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Global logger instance
 */
let globalLogger: Logger = new Logger();

/**
 * Configure the global logger
 */
export function configureLogger(config: Partial<LoggerConfig>): void {
  globalLogger = new Logger(config);
}

/**
 * Get the global logger
 */
export function getLogger(): Logger {
  return globalLogger;
}

/**
 * Create a component-specific logger
 */
export function createLogger(component: string, context?: LogContext): Logger {
  return globalLogger.child({ component, ...context });
}

// ═══════════════════════════════════════════════════════════════════════════
// REQUEST CONTEXT
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a request-scoped logger
 */
export function createRequestLogger(context?: Partial<LogContext>): Logger {
  return globalLogger.child({
    requestId: generateId('req'),
    ...context
  });
}

/**
 * Wrap an async operation with logging
 */
export async function withLogging<T>(
  logger: Logger,
  operation: string,
  fn: () => Promise<T>
): Promise<T> {
  logger.debug(`Starting: ${operation}`);
  const start = Date.now();
  
  try {
    const result = await fn();
    const durationMs = Date.now() - start;
    logger.info(`Completed: ${operation}`, { durationMs });
    return result;
  } catch (error) {
    const durationMs = Date.now() - start;
    logger.error(`Failed: ${operation}`, error as Error, { durationMs });
    throw error;
  }
}

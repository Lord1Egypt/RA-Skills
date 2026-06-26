/**
 * OpenClaw Core 类型声明
 * 运行时由 OpenClaw 提供
 */

declare module '@openclaw/core' {
  export interface SessionContext {
    logger: {
      info: (message: string) => void;
      error: (message: string) => void;
      warn: (message: string) => void;
      debug: (message: string) => void;
    };
    reply: (message: string) => Promise<void>;
    [key: string]: any;
  }
}

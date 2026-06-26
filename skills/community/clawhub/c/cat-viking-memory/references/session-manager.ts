/**
 * 飞书群会话管理器
 * 跟踪每个飞书群会话的最后活跃时间，实现会话结束自动保存功能
 */

import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

// 配置常量
const DEFAULT_CHECK_INTERVAL_MS = 5 * 60 * 1000; // 5分钟检查一次
const DEFAULT_TIMEOUT_MS = 30 * 60 * 1000; // 30分钟超时
const SESSION_HOOK_PATH = "~/.openclaw/skills/memory-pipeline/scripts/memory-session-hook.sh";

/**
 * 会话状态
 */
export interface ChatSessionState {
  chatId: string;
  accountId: string;
  lastActiveTime: number;
  saved: boolean;
  checkTimer?: NodeJS.Timeout;
}

/**
 * 会话管理器配置
 */
export interface SessionManagerConfig {
  checkIntervalMs?: number;
  timeoutMs?: number;
  enabled?: boolean;
}

/**
 * 会话状态管理器
 */
export class FeishuSessionManager {
  private sessions: Map<string, ChatSessionState> = new Map();
  private config: Required<SessionManagerConfig>;
  private checkTimer?: NodeJS.Timeout;
  private running: boolean = false;

  constructor(config: SessionManagerConfig = {}) {
    this.config = {
      checkIntervalMs: config.checkIntervalMs ?? DEFAULT_CHECK_INTERVAL_MS,
      timeoutMs: config.timeoutMs ?? DEFAULT_TIMEOUT_MS,
      enabled: config.enabled ?? true,
    };
  }

  /**
   * 生成会话唯一键
   */
  private getSessionKey(chatId: string, accountId: string): string {
    return `${accountId}:${chatId}`;
  }

  /**
   * 获取或创建会话状态
   */
  getOrCreateSession(chatId: string, accountId: string): ChatSessionState {
    const key = this.getSessionKey(chatId, accountId);
    let session = this.sessions.get(key);

    if (!session) {
      session = {
        chatId,
        accountId,
        lastActiveTime: Date.now(),
        saved: false,
      };
      this.sessions.set(key, session);
    }

    return session;
  }

  /**
   * 更新会话活跃时间
   */
  updateActivity(chatId: string, accountId: string): void {
    if (!this.config.enabled) return;

    const session = this.getOrCreateSession(chatId, accountId);
    session.lastActiveTime = Date.now();
    session.saved = false;
  }

  /**
   * 处理消息，只更新活跃时间（关键词触发已禁用）
   */
  handleMessage(
    chatId: string,
    accountId: string,
    messageText: string,
    log?: (msg: string) => void,
  ): void {
    if (!this.config.enabled) return;

    // 只更新活跃时间，不再通过关键词触发保存
    this.updateActivity(chatId, accountId);
  }



  /**
   * 执行会话保存
   */
  private async saveSession(
    chatId: string,
    accountId: string,
    reason: string,
    log?: (msg: string) => void,
  ): Promise<void> {
    const key = this.getSessionKey(chatId, accountId);
    const session = this.sessions.get(key);

    if (!session || session.saved) {
      log?.(`feishu[${accountId}]: 会话 ${chatId} 已保存，跳过`);
      return;
    }

    try {
      log?.(`feishu[${accountId}]: 触发会话保存 (原因: ${reason})`);

      // 设置环境变量并执行钩子脚本
      const hookPath = SESSION_HOOK_PATH.replace("~", process.env.HOME || "/home/xlous");
      const env = {
        ...process.env,
        SESSION_ID: `${chatId}_${Date.now()}`,
        AGENT_NAME: "maojingli",
      };

      await execAsync(`bash "${hookPath}" "${reason}"`, { env });

      session.saved = true;
      log?.(`feishu[${accountId}]: 会话 ${chatId} 保存成功`);
    } catch (error) {
      log?.(`feishu[${accountId}]: 会话 ${chatId} 保存失败: ${String(error)}`);
    }
  }

  /**
   * 检查超时会话
   */
  private async checkTimeoutSessions(log?: (msg: string) => void): Promise<void> {
    const now = Date.now();
    const timeout = this.config.timeoutMs;

    for (const [key, session] of this.sessions.entries()) {
      if (session.saved) continue;

      const inactiveTime = now - session.lastActiveTime;
      if (inactiveTime >= timeout) {
        log?.(
          `feishu[${session.accountId}]: 会话 ${session.chatId} 已 ${Math.round(inactiveTime / 60000)} 分钟无活动，触发保存`,
        );
        await this.saveSession(session.chatId, session.accountId, "超时自动保存", log);
      }
    }
  }

  /**
   * 启动定时检查
   */
  start(log?: (msg: string) => void): void {
    if (this.running || !this.config.enabled) return;

    this.running = true;
    log?.(
      `feishu[session-manager]: 启动会话管理器 (检查间隔: ${this.config.checkIntervalMs / 1000}秒, 超时: ${this.config.timeoutMs / 60000}分钟)`,
    );

    this.checkTimer = setInterval(() => {
      this.checkTimeoutSessions(log).catch((err) => {
        log?.(`feishu[session-manager]: 检查超时会话失败: ${String(err)}`);
      });
    }, this.config.checkIntervalMs);
  }

  /**
   * 停止定时检查
   */
  stop(log?: (msg: string) => void): void {
    if (this.checkTimer) {
      clearInterval(this.checkTimer);
      this.checkTimer = undefined;
    }
    this.running = false;
    log?.(`feishu[session-manager]: 会话管理器已停止`);
  }

  /**
   * 获取会话状态（用于测试）
   */
  getSession(chatId: string, accountId: string): ChatSessionState | undefined {
    return this.sessions.get(this.getSessionKey(chatId, accountId));
  }

  /**
   * 清除会话状态（用于测试）
   */
  clearSession(chatId: string, accountId: string): void {
    const key = this.getSessionKey(chatId, accountId);
    this.sessions.delete(key);
  }

  /**
   * 清除所有会话状态
   */
  clearAll(): void {
    this.sessions.clear();
  }
}

// 单例实例
let sessionManagerInstance: FeishuSessionManager | null = null;

/**
 * 获取会话管理器单例
 */
export function getFeishuSessionManager(config?: SessionManagerConfig): FeishuSessionManager {
  if (!sessionManagerInstance) {
    sessionManagerInstance = new FeishuSessionManager(config);
  }
  return sessionManagerInstance;
}

/**
 * 重置会话管理器（用于测试）
 */
export function resetFeishuSessionManager(): void {
  if (sessionManagerInstance) {
    sessionManagerInstance.stop();
  }
  sessionManagerInstance = null;
}

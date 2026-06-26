import { NewsConfig } from '../types';

export type ScheduledTask = {
  id: string;
  time: string;
  timezone: string;
  handler: () => Promise<any>;
  enabled: boolean;
};

export class CronScheduler {
  private config: NewsConfig;
  private tasks: Map<string, ScheduledTask> = new Map();
  private isRunning = false;

  constructor(config: NewsConfig) {
    this.config = config;
  }

  // 注册定时任务
  register(handler: () => Promise<any>): void {
    const schedule = this.config.schedule || ['08:00', '17:30', '22:30'];
    const timezone = this.config.timezone || 'Asia/Shanghai';

    for (const time of schedule) {
      const taskId = `daily-news-brief-${time.replace(':', '-')}`;
      const task: ScheduledTask = {
        id: taskId,
        time,
        timezone,
        handler,
        enabled: true
      };

      this.tasks.set(taskId, task);
      console.log(`[Scheduler] Registered task: ${taskId} at ${time} ${timezone}`);
    }
  }

  // 启动调度器
  async start(): Promise<void> {
    if (this.isRunning) {
      console.log('[Scheduler] Already running');
      return;
    }

    this.isRunning = true;
    console.log('[Scheduler] Starting scheduler...');

    // TODO: 实际环境中这里需要使用真正的cron库（如node-cron）
    // 目前先实现模拟版本
    this.startMockScheduler();

    console.log('[Scheduler] Scheduler started');
  }

  // 停止调度器
  async stop(): Promise<void> {
    if (!this.isRunning) {
      return;
    }

    this.isRunning = false;
    console.log('[Scheduler] Stopping scheduler...');

    // TODO: 清理cron任务

    console.log('[Scheduler] Scheduler stopped');
  }

  // 获取所有任务
  getTasks(): ScheduledTask[] {
    return Array.from(this.tasks.values());
  }

  // 启用/禁用任务
  toggleTask(taskId: string, enabled: boolean): boolean {
    const task = this.tasks.get(taskId);

    if (!task) {
      return false;
    }

    task.enabled = enabled;
    console.log(`[Scheduler] Task ${taskId} ${enabled ? 'enabled' : 'disabled'}`);
    return true;
  }

  // 模拟调度器（用于测试）
  private startMockScheduler(): void {
    // 在实际环境中，这里会使用node-cron等库
    // 现在只是打印信息

    const checkTime = () => {
      if (!this.isRunning) {
        return;
      }

      const now = new Date();
      const currentTime = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

      for (const [taskId, task] of this.tasks) {
        if (task.enabled && task.time === currentTime) {
          console.log(`[Scheduler] Executing task: ${taskId}`);
          task.handler().catch(error => {
            console.error(`[Scheduler] Task ${taskId} failed:`, error);
          });
        }
      }

      // 每分钟检查一次
      setTimeout(checkTime, 60000);
    };

    // 启动检查
    setTimeout(checkTime, 60000);
  }

  // 手动触发任务
  async triggerTask(taskId: string): Promise<boolean> {
    const task = this.tasks.get(taskId);

    if (!task || !task.enabled) {
      return false;
    }

    try {
      console.log(`[Scheduler] Manually triggering task: ${taskId}`);
      await task.handler();
      return true;
    } catch (error) {
      console.error(`[Scheduler] Task ${taskId} failed:`, error);
      return false;
    }
  }

  // TODO: 后续增强
  // 1. 集成真实的cron库（如node-cron）
  // 2. 支持动态添加/删除任务
  // 3. 添加任务执行历史记录
  // 4. 支持任务依赖关系
  // 5. 添加任务执行统计和监控
  // 6. 支持分布式调度
  // 7. 添加任务重试机制
  // 8. 支持任务超时处理
}
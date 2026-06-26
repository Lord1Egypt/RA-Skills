/**
 * 定时任务调度器
 * 负责自动采集比赛、分析、验证结果
 */

class Scheduler {
  constructor(taskFunction) {
    this.taskFunction = taskFunction;
    this.running = false;
    this.intervals = {
      // 每日任务
      daily: 24 * 60 * 60 * 1000,
      // 每小时任务
      hourly: 60 * 60 * 1000,
      // 每10分钟
      frequent: 10 * 60 * 1000
    };
    this.timers = {};
  }

  /**
   * 启动调度器
   */
  start(options = {}) {
    const {
      checkFrequency = 'frequent', // frequent, hourly, daily
      onMatchTime = null          // 比赛开始前触发回调
    } = options;

    this.running = true;
    const interval = this.intervals[checkFrequency] || this.intervals.frequent;

    console.log(`[Scheduler] 启动调度器，间隔${interval / 1000 / 60}分钟`);

    // 立即执行一次
    this.run();

    // 设置定时器
    this.timers.main = setInterval(() => {
      this.run();
    }, interval);
  }

  /**
   * 停止调度器
   */
  stop() {
    this.running = false;
    Object.keys(this.timers).forEach(key => {
      clearInterval(this.timers[key]);
    });
    this.timers = {};
    console.log('[Scheduler] 调度器已停止');
  }

  /**
   * 执行任务
   */
  async run() {
    if (!this.running) return;

    try {
      const hour = new Date().getHours();
      const isMatchDay = this.isMatchDay(hour);

      if (isMatchDay) {
        // 比赛日：执行完整流程
        console.log('[Scheduler] 执行比赛日任务');
        await this.taskFunction('今日推荐');
      } else {
        // 非比赛日：学习优化
        console.log('[Scheduler] 执行学习优化任务');
        await this.taskFunction('学习');
      }
    } catch (error) {
      console.error('[Scheduler] 任务执行失败:', error.message);
    }
  }

  /**
   * 判断是否为比赛日（假设比赛主要在晚上进行）
   */
  isMatchDay(hour) {
    // 比赛活跃时段：18:00 - 23:00
    return hour >= 18 && hour <= 23;
  }

  /**
   * 安排特定时间任务
   */
  scheduleAt(hour, minute, task) {
    const now = new Date();
    const target = new Date();
    target.setHours(hour, minute, 0, 0);

    if (target < now) {
      target.setDate(target.getDate() + 1);
    }

    const delay = target - now;

    console.log(`[Scheduler] 计划任务将在 ${delay / 1000 / 60} 分钟后执行`);

    setTimeout(() => {
      task();
      // 每天重复
      setInterval(task, 24 * 60 * 60 * 1000);
    }, delay);
  }
}

module.exports = Scheduler;

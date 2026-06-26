const cron = require('node-cron');

/**
 * 定时任务调度器
 */
class Scheduler {
  constructor() {
    this.tasks = [];
  }

  /**
   * 添加定时任务
   * @param {string} schedule - Cron表达式
   * @param {Function} callback - 回调函数
   * @param {string} name - 任务名称
   */
  addTask(schedule, callback, name = 'Unnamed Task') {
    if (!cron.validate(schedule)) {
      console.error(`Invalid cron schedule: ${schedule}`);
      return null;
    }

    const task = cron.schedule(schedule, async () => {
      console.log(`[${new Date().toISOString()}] Running task: ${name}`);
      try {
        await callback();
        console.log(`[${new Date().toISOString()}] Task completed: ${name}`);
      } catch (error) {
        console.error(`[${new Date().toISOString()}] Task failed: ${name}`, error.message);
      }
    });

    this.tasks.push({ name, schedule, task });
    console.log(`Scheduled task: ${name} (${schedule})`);

    return task;
  }

  /**
   * 启动所有任务
   */
  startAll() {
    this.tasks.forEach(({ name, task }) => {
      task.start();
      console.log(`Started task: ${name}`);
    });
  }

  /**
   * 停止所有任务
   */
  stopAll() {
    this.tasks.forEach(({ name, task }) => {
      task.stop();
      console.log(`Stopped task: ${name}`);
    });
  }

  /**
   * 获取任务列表
   */
  getTasks() {
    return this.tasks.map(({ name, schedule }) => ({ name, schedule }));
  }
}

module.exports = Scheduler;

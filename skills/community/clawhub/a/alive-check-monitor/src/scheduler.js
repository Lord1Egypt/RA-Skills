const cron = require('node-cron');

/**
 * Task Scheduler
 */
class Scheduler {
  constructor() {
    this.tasks = [];
  }

  /**
   * Add scheduled task
   * @param {string} schedule - Cron expression
   * @param {Function} callback - Task callback
   * @param {string} name - Task name
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
   * Start all tasks
   */
  startAll() {
    this.tasks.forEach(({ name, task }) => {
      task.start();
      console.log(`Started task: ${name}`);
    });
  }

  /**
   * Stop all tasks
   */
  stopAll() {
    this.tasks.forEach(({ name, task }) => {
      task.stop();
      console.log(`Stopped task: ${name}`);
    });
  }

  /**
   * Get task list
   */
  getTasks() {
    return this.tasks.map(({ name, schedule }) => ({ name, schedule }));
  }
}

module.exports = Scheduler;

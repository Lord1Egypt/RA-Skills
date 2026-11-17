/**
 * timeout-manager.js - Circuit breaker for blocking tasks
 */

class TimeoutManager {
  constructor(options = {}) {
    this.taskTimeout = options.taskTimeout || 180000; // 180s per task
    this.totalTimeout = options.totalTimeout || 300000; // 300s total
    this.fileWaitTimeout = options.fileWaitTimeout || 120000; // 120s file wait
  }

  check(phase, elapsed) {
    const limits = {
      task: this.taskTimeout,
      total: this.totalTimeout,
      fileWait: this.fileWaitTimeout
    };
    const limit = limits[phase];
    if (limit && elapsed > limit) {
      return {
        tripped: true,
        phase,
        elapsed,
        limit,
        action: 'abort'
      };
    }
    return { tripped: false, phase, elapsed };
  }

  remaining(phase, elapsed) {
    const limits = {
      task: this.taskTimeout,
      total: this.totalTimeout,
      fileWait: this.fileWaitTimeout
    };
    const limit = limits[phase] || 0;
    return Math.max(0, limit - elapsed);
  }
}

function test() {
  const tm = new TimeoutManager();
  console.log('Task remaining at 30s:', tm.remaining('task', 30000));
  console.log('Check at 200s:', tm.check('task', 200000));
}

if (require.main === module) {
  test();
}

module.exports = { TimeoutManager };

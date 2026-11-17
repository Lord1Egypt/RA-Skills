'use strict';
/**
 * _shared/output.js — 输出规约 (对齐转链 skill):
 * stdout 只输出 JSON ({ok:true,data} / {ok:false,code,message}), 提示走 stderr。
 * 退出码: 0 成功 / 1 参数错误 / 2 认证失败(1002|1003) / 3 点数不足(3001) / 4 网络错误 / 5 其它。
 */

class UsageError extends Error {
  constructor(message) {
    super(message);
    this.name = 'UsageError';
  }
}

function printOk(data) {
  process.stdout.write(JSON.stringify({ ok: true, data }) + '\n');
}

function printFail(code, message) {
  process.stdout.write(JSON.stringify({ ok: false, code, message }) + '\n');
}

/** 错误 → 退出码映射 + 可操作提示。SKILL_TIP: 各 skill 传入自己的 --link 引导话术。 */
function exitWithError(err, { usage = '', skillTip = '请改用 --link 扫码/链接方式' } = {}) {
  if (err instanceof UsageError) {
    printFail(1001, `参数错误: ${err.message}`);
    if (usage) process.stderr.write(usage + '\n');
    process.exit(1);
  }
  if (err && err.name === 'BizError') {
    let message = err.message;
    let exitCode = 5;
    if (err.code === 1001) {
      exitCode = 1;
    } else if (err.code === 1002 || err.code === 1003) {
      exitCode = 2;
      message = `${err.message}（token 已失效或未登录，请执行 login --link 重新登录）`;
    } else if (err.code === 3001) {
      exitCode = 3;
      message = '点数不足，请联系管理员充值';
    } else if (err.code === 3003) {
      message = `${err.message}（请检查 task_id 是否正确、是否属于当前账号）`;
    } else if (err.code === 2003) {
      message = `${err.message}（终端无法完成图形验证码，${skillTip}）`;
    } else if (err.code === 4290) {
      message = `${err.message}（请稍后重试）`;
    }
    printFail(err.code, message);
    process.exit(exitCode);
  }
  if (err && err.name === 'NetworkError') {
    printFail(err.code, `${err.message}（请检查后端服务是否已启动、base-url 是否正确）`);
    process.exit(4);
  }
  printFail('INTERNAL_ERROR', err && err.message ? err.message : String(err));
  process.exit(5);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const TERMINAL_STATUS = new Set(['done', 'partial_failed', 'failed']);

/** 轮询任务直到终态; 进度走 stderr; 超时抛 BizError('TIMEOUT') 携带最后状态。 */
async function pollTask(client, taskId, { intervalSec = 2, timeoutSec = 120 } = {}) {
  const deadline = Date.now() + timeoutSec * 1000;
  for (;;) {
    const task = await client.getTask(taskId);
    if (TERMINAL_STATUS.has(task.status)) return task;
    process.stderr.write(
      `[wait] task_id=${taskId} status=${task.status} success=${task.success_count} fail=${task.fail_count}\n`);
    if (Date.now() + intervalSec * 1000 > deadline) {
      const err = new BizError('TIMEOUT', `轮询超时（${timeoutSec}s），任务仍为 ${task.status} 状态，可稍后执行 query ${taskId} 查询`);
      err.data = task;
      throw err;
    }
    await sleep(intervalSec * 1000);
  }
}

function parsePositiveNumber(value, name, fallback) {
  if (value === undefined) return fallback;
  const n = Number(value);
  if (!Number.isFinite(n) || n <= 0) throw new UsageError(`--${name} 需为正数，收到: ${value}`);
  return n;
}

module.exports = {
  UsageError, printOk, printFail, exitWithError, sleep,
  pollTask, parsePositiveNumber, TERMINAL_STATUS,
};

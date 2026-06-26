import { Market, CommandArgs, TaskConfig, SyncResult, TradingDay, MARKET_CONFIGS } from './types';
import { tradingScheduler } from './scheduler';
import { calendarSyncer } from './sync';
import { calendarManager } from './calendars';

/**
 * 金融交易日历工具
 *
 * 提供交易日历查询和任务计划功能。注意: 此skill不直接执行任务,
 * 实际调度需要配合 /loop skill 使用。
 *
 * 使用方式:
 * /finance-cron check <market> [date]           - 检查是否交易日
 * /finance-cron next <market> [n]               - 显示接下来n个交易日
 * /finance-cron sync [market]                   - 同步交易日历
 * /finance-cron add <market> <time> <command>   - 计划任务(需配合/loop使用)
 * /finance-cron list                            - 列出所有计划的任务
 */

/**
 * 解析命令参数
 */
export function parseArgs(input: string): CommandArgs {
  const parts = input.trim().split(/\s+/);
  const action = parts[0] as CommandArgs['action'];
  
  if (!['add', 'list', 'check', 'next', 'sync'].includes(action)) {
    throw new Error(`Unknown action: ${action}. Valid actions: add, list, check, next, sync`);
  }

  switch (action) {
    case 'add':
      if (parts.length < 4) {
        throw new Error('Usage: add <market> <time> <command>\nExample: add US 09:30 "echo market open"');
      }
      return {
        action: 'add',
        market: parts[1].toUpperCase() as Market,
        time: parts[2],
        command: parts.slice(3).join(' '),
      };

    case 'list':
      return { action: 'list' };

    case 'check':
      if (parts.length < 2) {
        throw new Error('Usage: check <market> [date]\nExample: check US 2024-12-25');
      }
      return {
        action: 'check',
        market: parts[1].toUpperCase() as Market,
        date: parts[2],
      };

    case 'next':
      if (parts.length < 2) {
        throw new Error('Usage: next <market> [n]\nExample: next CN 5');
      }
      return {
        action: 'next',
        market: parts[1].toUpperCase() as Market,
        count: parts[2] ? parseInt(parts[2], 10) : 5,
      };

    case 'sync':
      return {
        action: 'sync',
        market: parts[1]?.toUpperCase() as Market | undefined,
      };
  }
}

/**
 * 执行命令
 */
export async function executeCommand(args: CommandArgs): Promise<string> {
  switch (args.action) {
    case 'add':
      return handleAdd(args);
    case 'list':
      return handleList();
    case 'check':
      return handleCheck(args);
    case 'next':
      return handleNext(args);
    case 'sync':
      return await handleSync(args);
  }
}

/**
 * 处理添加任务命令
 */
function handleAdd(args: CommandArgs): string {
  if (!args.market || !args.time || !args.command) {
    return 'Error: Missing required parameters';
  }

  validateMarket(args.market);
  validateTime(args.time);

  const task = tradingScheduler.addTask({
    market: args.market,
    time: args.time,
    command: args.command,
  });

  const nextRun = task.nextRun ? new Date(task.nextRun) : null;
  const nextRunStr = nextRun 
    ? `${formatDate(nextRun)} ${args.time}`
    : 'Not scheduled';

  return `Task planned successfully!

Task ID: ${task.id}
Market: ${args.market} (${MARKET_CONFIGS[args.market].name})
Time: ${args.time}
Command: ${args.command}
Next Run: ${nextRunStr}

Note: This task will only run on trading days for the ${args.market} market.

To actually execute this task on schedule, use /loop:
  /loop ${args.time.split(':')[1]} ${args.time.split(':')[0]} * * 1-5 /finance-cron check ${args.market} && ${args.command}`;
}

/**
 * 处理列出任务命令
 */
function handleList(): string {
  const tasks = tradingScheduler.getAllTasks();

  if (tasks.length === 0) {
    return 'No scheduled tasks.\nUse "add <market> <time> <command>" to create a task.';
  }

  const lines = tasks.map((task, index) => {
    const nextRun = task.nextRun ? new Date(task.nextRun) : null;
    return `${index + 1}. [${task.id.slice(0, 12)}...] ${task.market} @ ${task.time}
   Command: ${task.command}
   Status: ${task.enabled ? 'Enabled' : 'Disabled'}
   Next: ${nextRun ? formatDate(nextRun) : 'N/A'}`;
  });

  return `Scheduled Tasks (${tasks.length}):\n\n${lines.join('\n\n')}`;
}

/**
 * 处理检查交易日命令
 */
function handleCheck(args: CommandArgs): string {
  if (!args.market) {
    return 'Error: Market is required';
  }

  validateMarket(args.market);

  const checkDate = args.date ? new Date(args.date) : new Date();
  const info = tradingScheduler.getTradingDayInfo(args.market, checkDate);
  const marketInfo = MARKET_CONFIGS[args.market];

  const emoji = info.isTradingDay ? '✓' : '✗';
  const status = info.isTradingDay ? 'Trading Day' : 'Non-Trading Day';
  const reason = info.reason === 'holiday' ? '(Holiday)' : 
                 info.reason === 'weekend' ? '(Weekend)' : '';

  return `${emoji} ${formatDate(checkDate)}

Market: ${args.market} - ${marketInfo.name}
Status: ${status} ${reason}

Trading Hours: ${marketInfo.openTime} - ${marketInfo.closeTime} (${marketInfo.timezone})`;
}

/**
 * 处理获取下一交易日命令
 */
function handleNext(args: CommandArgs): string {
  if (!args.market) {
    return 'Error: Market is required';
  }

  const market = args.market;
  validateMarket(market);

  const count = args.count || 5;
  const tradingDays = tradingScheduler.getNextTradingDays(market, count);
  const marketInfo = MARKET_CONFIGS[market];

  const lines = tradingDays.map((date, index) => {
    const dayInfo = tradingScheduler.getTradingDayInfo(market, date);
    return `${index + 1}. ${formatDate(date)} - Trading Day`;
  });

  return `Next ${count} Trading Days for ${market} (${marketInfo.name}):

${lines.join('\n')}

Trading Hours: ${marketInfo.openTime} - ${marketInfo.closeTime} (${marketInfo.timezone})`;
}

/**
 * 处理同步日历命令
 */
async function handleSync(args: CommandArgs): Promise<string> {
  let results: SyncResult[];

  if (args.market) {
    validateMarket(args.market);
    results = [await calendarSyncer.syncMarket(args.market)];
  } else {
    results = await calendarSyncer.syncAll();
  }

  const lines = results.map(result => {
    const status = result.success ? '✓' : '✗';
    const details = result.success
      ? `${result.updatedDays} records updated`
      : result.error || 'Unknown error';
    return `${status} ${result.market}: ${details}`;
  });

  return `Trading Calendar Sync Results:

${lines.join('\n')}

${results.every(r => r.success) ? 'Sync completed successfully!' : 'Some markets failed to sync. Check the errors above.'}`;
}

/**
 * 验证市场代码
 */
function validateMarket(market: Market): void {
  if (!['US', 'CN', 'HK'].includes(market)) {
    throw new Error(`Invalid market: ${market}. Valid markets: US, CN, HK`);
  }
}

/**
 * 验证时间格式
 */
function validateTime(time: string): void {
  const timeRegex = /^([01]?[0-9]|2[0-3]):([0-5][0-9])$/;
  if (!timeRegex.test(time)) {
    throw new Error(`Invalid time format: ${time}. Use HH:mm format (e.g., 09:30)`);
  }
}

/**
 * 格式化日期显示
 */
function formatDate(date: Date): string {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const dayName = days[date.getDay()];
  return `${year}-${month}-${day} (${dayName})`;
}

/**
 * 获取交易日状态（供外部调用）
 */
export function getTradingStatus(market: Market, date?: Date): TradingDay {
  const checkDate = date || new Date();
  return tradingScheduler.getTradingDayInfo(market, checkDate);
}

/**
 * 检查今天是否为交易日（供外部调用）
 */
export function isTradingDay(market: Market, date?: Date): boolean {
  const checkDate = date || new Date();
  return tradingScheduler.isTradingDay(market, checkDate);
}

/**
 * 获取下一交易日（供外部调用）
 */
export function getNextTradingDay(market: Market): Date {
  return tradingScheduler.getNextTradingDay(market);
}

/**
 * 获取接下来N个交易日（供外部调用）
 */
export function getNextTradingDays(market: Market, count: number, fromDate?: Date): Date[] {
  return tradingScheduler.getNextTradingDays(market, count, fromDate);
}

// 导出所有公共API
export {
  tradingScheduler,
  calendarSyncer,
  calendarManager,
  MARKET_CONFIGS,
};

// 默认导出
export default {
  parseArgs,
  executeCommand,
  getTradingStatus,
  isTradingDay,
  getNextTradingDay,
  getNextTradingDays,
};

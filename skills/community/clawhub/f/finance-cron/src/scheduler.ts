import { Market, TaskConfig, ScheduleResult, TradingDay, MARKET_CONFIGS } from './types';
import { calendarManager } from './calendars';
import { format, parse, addDays, setHours, setMinutes, isBefore, isAfter } from 'date-fns';

/**
 * 交易日感知的调度器
 */
export class TradingScheduler {
  private tasks: Map<string, TaskConfig> = new Map();

  /**
   * 判断指定日期是否为交易日
   */
  isTradingDay(market: Market, date: Date): boolean {
    return calendarManager.isTradingDay(market, date);
  }

  /**
   * 获取交易日详情
   */
  getTradingDayInfo(market: Market, date: Date): TradingDay {
    const calendar = calendarManager.getCalendar(market);
    const dateStr = format(date, 'yyyy-MM-dd');
    const dayOfWeek = date.getDay();
    const year = date.getFullYear().toString();

    // 检查是否为周末
    if (calendar.weekends.includes(dayOfWeek)) {
      // A股调休上班日
      if (market === 'CN' && calendar.workdays?.[year]?.includes(dateStr)) {
        return { date, isTradingDay: true, reason: 'trading' };
      }
      return { date, isTradingDay: false, reason: 'weekend' };
    }

    // 检查节假日
    const holidays = calendar.holidays[year] || [];
    if (holidays.includes(dateStr)) {
      return { date, isTradingDay: false, reason: 'holiday' };
    }

    return { date, isTradingDay: true, reason: 'trading' };
  }

  /**
   * 获取下一个交易日
   */
  getNextTradingDay(market: Market, fromDate?: Date): Date {
    return calendarManager.getNextTradingDay(market, fromDate);
  }

  /**
   * 获取接下来N个交易日
   */
  getNextTradingDays(market: Market, count: number, fromDate?: Date): Date[] {
    return calendarManager.getNextTradingDays(market, count, fromDate);
  }

  /**
   * 创建交易日感知的cron表达式
   * 返回每天执行的时间，执行时检查是否为交易日
   */
  createTradingDayCron(time: string): string {
    const [hours, minutes] = time.split(':').map(Number);
    return `${minutes} ${hours} * * *`;
  }

  /**
   * 计算任务的下次执行时间
   */
  calculateNextRun(task: TaskConfig): Date | null {
    const now = new Date();
    const [hours, minutes] = task.time.split(':').map(Number);
    
    // 今天的时间点
    const todayTarget = new Date();
    todayTarget.setHours(hours, minutes, 0, 0);

    // 如果今天的这个时间点还没过，检查今天是否为交易日
    if (isAfter(todayTarget, now) && this.isTradingDay(task.market, todayTarget)) {
      return todayTarget;
    }

    // 否则找下一个交易日
    const nextTradingDay = this.getNextTradingDay(task.market, now);
    nextTradingDay.setHours(hours, minutes, 0, 0);
    return nextTradingDay;
  }

  /**
   * 添加任务
   */
  addTask(config: Omit<TaskConfig, 'id' | 'createdAt' | 'enabled'>): TaskConfig {
    const id = this.generateTaskId();
    const task: TaskConfig = {
      ...config,
      id,
      enabled: true,
      createdAt: new Date().toISOString(),
      nextRun: undefined,
    };
    
    task.nextRun = this.calculateNextRun(task)?.toISOString();
    this.tasks.set(id, task);
    
    return task;
  }

  /**
   * 获取所有任务
   */
  getAllTasks(): TaskConfig[] {
    return Array.from(this.tasks.values());
  }

  /**
   * 获取指定市场的任务
   */
  getTasksByMarket(market: Market): TaskConfig[] {
    return this.getAllTasks().filter(task => task.market === market);
  }

  /**
   * 删除任务
   */
  removeTask(id: string): boolean {
    return this.tasks.delete(id);
  }

  /**
   * 更新任务状态
   */
  toggleTask(id: string, enabled: boolean): TaskConfig | null {
    const task = this.tasks.get(id);
    if (!task) return null;
    
    task.enabled = enabled;
    if (enabled) {
      task.nextRun = this.calculateNextRun(task)?.toISOString();
    } else {
      task.nextRun = undefined;
    }
    
    return task;
  }

  /**
   * 获取到期需要执行的任务
   * 注意: 此方法仅识别到期任务, 不执行命令
   * 返回需要执行的任务列表, 实际执行需要外部调度器(如 /loop skill)
   */
  getDueTasks(): TaskConfig[] {
    const now = new Date();
    const tasksToExecute: TaskConfig[] = [];

    for (const task of this.tasks.values()) {
      if (!task.enabled || !task.nextRun) continue;

      const nextRun = new Date(task.nextRun);
      
      // 检查是否到达执行时间
      if (isBefore(nextRun, now) || nextRun.getTime() === now.getTime()) {
        // 再次确认是交易日
        if (this.isTradingDay(task.market, nextRun)) {
          tasksToExecute.push(task);
        }
        
        // 更新下次执行时间
        task.lastRun = task.nextRun;
        task.nextRun = this.calculateNextRun(task)?.toISOString();
      }
    }

    return tasksToExecute;
  }

  /**
   * 生成任务ID
   */
  private generateTaskId(): string {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 格式化日期显示
   */
  formatDateDisplay(date: Date): string {
    return format(date, 'yyyy-MM-dd (EEE)');
  }

  /**
   * 获取市场信息
   */
  getMarketInfo(market: Market) {
    return MARKET_CONFIGS[market];
  }
}

// 导出单例实例
export const tradingScheduler = new TradingScheduler();

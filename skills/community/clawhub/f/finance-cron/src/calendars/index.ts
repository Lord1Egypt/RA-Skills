import * as path from 'path';
import * as fs from 'fs';
import { Market, TradingCalendar, MARKET_CONFIGS } from '../types';

/**
 * 交易日历管理器
 * 负责加载、缓存和查询各市场的交易日历
 */
export class CalendarManager {
  private calendars: Map<Market, TradingCalendar> = new Map();
  private dataPath: string;

  constructor(dataPath?: string) {
    this.dataPath = dataPath || path.join(__dirname, '../../data');
  }

  /**
   * 加载指定市场的交易日历
   */
  loadCalendar(market: Market): TradingCalendar {
    if (this.calendars.has(market)) {
      return this.calendars.get(market)!;
    }

    const filePath = this.getCalendarPath(market);
    
    if (!fs.existsSync(filePath)) {
      throw new Error(`Calendar file not found for market ${market}: ${filePath}`);
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const calendar = JSON.parse(content) as TradingCalendar;
    
    this.calendars.set(market, calendar);
    return calendar;
  }

  /**
   * 加载所有市场的交易日历
   */
  loadAllCalendars(): void {
    const markets: Market[] = ['US', 'CN', 'HK'];
    for (const market of markets) {
      try {
        this.loadCalendar(market);
      } catch (error) {
        console.warn(`Failed to load calendar for ${market}:`, error);
      }
    }
  }

  /**
   * 获取指定市场的交易日历
   */
  getCalendar(market: Market): TradingCalendar {
    return this.loadCalendar(market);
  }

  /**
   * 检查指定日期是否为交易日
   */
  isTradingDay(market: Market, date: Date): boolean {
    const calendar = this.getCalendar(market);
    const normalizedDate = this.normalizeDate(date);
    const dateStr = this.formatDate(normalizedDate);
    const dayOfWeek = normalizedDate.getDay();
    const year = normalizedDate.getFullYear().toString();

    // 检查是否为周末
    if (calendar.weekends.includes(dayOfWeek)) {
      // A股特殊处理：检查是否为调休上班日
      if (market === 'CN' && calendar.workdays?.[year]) {
        return calendar.workdays[year].includes(dateStr);
      }
      return false;
    }

    // 检查是否为节假日
    const holidays = calendar.holidays[year] || [];
    return !holidays.includes(dateStr);
  }

  /**
   * 获取下一个交易日
   */
  getNextTradingDay(market: Market, fromDate?: Date): Date {
    let current = this.normalizeDate(fromDate || new Date());
    
    // 从第二天开始查找
    current.setDate(current.getDate() + 1);

    // 最多查找30天
    for (let i = 0; i < 30; i++) {
      if (this.isTradingDay(market, current)) {
        return current;
      }
      current.setDate(current.getDate() + 1);
    }

    throw new Error(`No trading day found within 30 days for market ${market}`);
  }

  /**
   * 获取接下来的N个交易日
   */
  getNextTradingDays(market: Market, count: number, fromDate?: Date): Date[] {
    const result: Date[] = [];
    let current = this.normalizeDate(fromDate || new Date());

    // 最多查找count*3天（考虑节假日和周末）
    const maxDays = count * 3 + 30;
    let daysChecked = 0;

    while (result.length < count && daysChecked < maxDays) {
      current.setDate(current.getDate() + 1);
      if (this.isTradingDay(market, current)) {
        result.push(new Date(current));
      }
      daysChecked++;
    }

    return result;
  }

  /**
   * 规范化日期到本地时区的午夜
   * 确保日期计算使用本地时区
   */
  private normalizeDate(date: Date): Date {
    const normalized = new Date(date);
    // 使用本地时间的年月日创建新的日期
    const year = normalized.getFullYear();
    const month = normalized.getMonth();
    const day = normalized.getDate();
    return new Date(year, month, day, 0, 0, 0, 0);
  }

  /**
   * 获取指定年份的所有交易日
   */
  getTradingDays(market: Market, year: number): Date[] {
    const calendar = this.getCalendar(market);
    const tradingDays: Date[] = [];
    
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31);
    
    const current = new Date(startDate);
    while (current <= endDate) {
      if (this.isTradingDay(market, current)) {
        tradingDays.push(new Date(current));
      }
      current.setDate(current.getDate() + 1);
    }
    
    return tradingDays;
  }

  /**
   * 更新指定市场的交易日历
   */
  updateCalendar(market: Market, calendar: TradingCalendar): void {
    const filePath = this.getCalendarPath(market);
    calendar.lastUpdated = new Date().toISOString().split('T')[0];
    
    fs.writeFileSync(filePath, JSON.stringify(calendar, null, 2));
    this.calendars.set(market, calendar);
  }

  /**
   * 获取日历文件路径
   */
  private getCalendarPath(market: Market): string {
    const fileMap: Record<Market, string> = {
      US: 'us-holidays.json',
      CN: 'cn-holidays.json',
      HK: 'hk-holidays.json',
    };
    return path.join(this.dataPath, fileMap[market]);
  }

  /**
   * 格式化日期为YYYY-MM-DD格式
   */
  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
}

// 导出单例实例
export const calendarManager = new CalendarManager();

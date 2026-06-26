/**
 * 市场标识符
 * US: 美股市场 (NYSE, NASDAQ)
 * CN: A股市场 (上交所, 深交所)
 * HK: 港股市场 (港交所)
 */
export type Market = 'US' | 'CN' | 'HK';

/**
 * 市场配置信息
 */
export interface MarketConfig {
  code: Market;
  name: string;
  exchanges: string[];
  timezone: string;
  openTime: string;  // HH:mm格式
  closeTime: string; // HH:mm格式
}

/**
 * 交易日历数据结构
 */
export interface TradingCalendar {
  market: Market;
  /** 按年份分组的节假日日期列表 */
  holidays: Record<string, string[]>;
  /** 调休上班日（仅A股需要，周末补班） */
  workdays?: Record<string, string[]>;
  /** 周末定义，0=周日, 6=周六 */
  weekends: number[];
  /** 最后更新时间 */
  lastUpdated: string;
  /** 数据来源 */
  source: string;
}

/**
 * 任务调度配置
 */
export interface TaskConfig {
  /** 任务唯一标识 */
  id: string;
  /** 目标市场 */
  market: Market;
  /** 执行时间 HH:mm格式 */
  time: string;
  /** 要执行的命令/提示词 */
  command: string;
  /** 是否启用 */
  enabled: boolean;
  /** 创建时间 */
  createdAt: string;
  /** 上次执行时间 */
  lastRun?: string;
  /** 下次执行时间 */
  nextRun?: string;
}

/**
 * 交易日信息
 */
export interface TradingDay {
  date: Date;
  isTradingDay: boolean;
  reason?: string; // 'holiday' | 'weekend' | 'trading'
}

/**
 * 调度结果
 */
export interface ScheduleResult {
  scheduled: boolean;
  nextTradingDay?: Date;
  message: string;
}

/**
 * 同步结果
 */
export interface SyncResult {
  market: Market;
  success: boolean;
  updatedDays: number;
  message: string;
  error?: string;
}

/**
 * Skill命令参数
 */
export interface CommandArgs {
  action: 'add' | 'list' | 'check' | 'next' | 'sync';
  market?: Market;
  time?: string;
  command?: string;
  date?: string;
  count?: number;
}

/**
 * 预定义市场配置
 */
export const MARKET_CONFIGS: Record<Market, MarketConfig> = {
  US: {
    code: 'US',
    name: 'US Stock Market',
    exchanges: ['NYSE', 'NASDAQ'],
    timezone: 'America/New_York',
    openTime: '09:30',
    closeTime: '16:00',
  },
  CN: {
    code: 'CN',
    name: 'China A-Share Market',
    exchanges: ['SSE', 'SZSE'],
    timezone: 'Asia/Shanghai',
    openTime: '09:30',
    closeTime: '15:00',
  },
  HK: {
    code: 'HK',
    name: 'Hong Kong Stock Market',
    exchanges: ['HKEX'],
    timezone: 'Asia/Hong_Kong',
    openTime: '09:30',
    closeTime: '16:00',
  },
};

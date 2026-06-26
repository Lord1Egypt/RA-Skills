import { format, parse, isValid } from 'date-fns';
import { Market, MARKET_CONFIGS } from './types';

/**
 * 格式化日期为YYYY-MM-DD格式
 */
export function formatDateISO(date: Date): string {
  return format(date, 'yyyy-MM-dd');
}

/**
 * 解析日期字符串
 */
export function parseDate(dateStr: string): Date | null {
  try {
    const parsed = parse(dateStr, 'yyyy-MM-dd', new Date());
    return isValid(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

/**
 * 获取市场时区
 */
export function getMarketTimezone(market: Market): string {
  return MARKET_CONFIGS[market].timezone;
}

/**
 * 获取市场开盘时间
 */
export function getMarketOpenTime(market: Market): string {
  return MARKET_CONFIGS[market].openTime;
}

/**
 * 获取市场收盘时间
 */
export function getMarketCloseTime(market: Market): string {
  return MARKET_CONFIGS[market].closeTime;
}

/**
 * 检查当前是否在交易时段内
 */
export function isInTradingHours(market: Market, date?: Date): boolean {
  const now = date || new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const currentTime = hours * 60 + minutes;

  const openTime = MARKET_CONFIGS[market].openTime.split(':').map(Number);
  const closeTime = MARKET_CONFIGS[market].closeTime.split(':').map(Number);

  const openMinutes = openTime[0] * 60 + openTime[1];
  const closeMinutes = closeTime[0] * 60 + closeTime[1];

  return currentTime >= openMinutes && currentTime <= closeMinutes;
}

/**
 * 获取市场当前状态描述
 */
export function getMarketStatus(market: Market): string {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const currentTimeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

  const openTime = MARKET_CONFIGS[market].openTime;
  const closeTime = MARKET_CONFIGS[market].closeTime;

  if (currentTimeStr < openTime) {
    return `Pre-market (opens at ${openTime})`;
  } else if (currentTimeStr > closeTime) {
    return `Post-market (closed at ${closeTime})`;
  } else {
    return `Trading hours (${openTime} - ${closeTime})`;
  }
}

/**
 * 生成cron表达式
 * @param time 时间 HH:mm
 * @returns cron表达式
 */
export function timeToCron(time: string): string {
  const [hours, minutes] = time.split(':').map(Number);
  return `${minutes} ${hours} * * *`;
}

/**
 * 解析cron表达式为时间
 * @param cron cron表达式
 * @returns 时间 HH:mm
 */
export function cronToTime(cron: string): string | null {
  const parts = cron.split(' ');
  if (parts.length < 2) return null;

  const minutes = parts[0];
  const hours = parts[1];

  if (minutes === '*' || hours === '*') return null;

  return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
}

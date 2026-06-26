import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';
import { Market, SyncResult } from './types';
import { calendarManager } from './calendars';

const execAsync = promisify(exec);

/**
 * 交易日历同步器
 * 通过调用Python脚本从数据源同步最新的交易日历
 */
export class CalendarSyncer {
  private scriptsPath: string;

  constructor(scriptsPath?: string) {
    this.scriptsPath = scriptsPath || path.join(__dirname, '../../scripts');
  }

  /**
   * 同步指定市场的交易日历
   */
  async syncMarket(market: Market): Promise<SyncResult> {
    try {
      // 检查Python环境
      const pythonAvailable = await this.checkPython();
      if (!pythonAvailable) {
        return this.getFallbackResult(market, 'Python not available');
      }

      // 调用Python同步脚本
      const scriptPath = path.join(this.scriptsPath, 'sync_calendars.py');
      
      if (!fs.existsSync(scriptPath)) {
        return this.getFallbackResult(market, 'Sync script not found');
      }

      const { stdout, stderr } = await execAsync(
        `python3 "${scriptPath}" --market ${market}`,
        { timeout: 60000 }
      );

      if (stderr && !stdout) {
        return {
          market,
          success: false,
          updatedDays: 0,
          message: 'Sync failed',
          error: stderr,
        };
      }

      // 重新加载日历
      calendarManager.loadCalendar(market);
      const calendar = calendarManager.getCalendar(market);
      
      const totalDays = Object.values(calendar.holidays).flat().length;
      
      return {
        market,
        success: true,
        updatedDays: totalDays,
        message: `Synced ${totalDays} holiday records from data source`,
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        market,
        success: false,
        updatedDays: 0,
        message: 'Sync failed',
        error: errorMessage,
      };
    }
  }

  /**
   * 同步所有市场的交易日历
   */
  async syncAll(): Promise<SyncResult[]> {
    const markets: Market[] = ['US', 'CN', 'HK'];
    const results: SyncResult[] = [];

    for (const market of markets) {
      const result = await this.syncMarket(market);
      results.push(result);
    }

    return results;
  }

  /**
   * 检查Python环境
   */
  private async checkPython(): Promise<boolean> {
    try {
      await execAsync('python3 --version', { timeout: 5000 });
      return true;
    } catch {
      try {
        await execAsync('python --version', { timeout: 5000 });
        return true;
      } catch {
        return false;
      }
    }
  }

  /**
   * 获取回退结果（当无法同步时使用本地数据）
   */
  private getFallbackResult(market: Market, reason: string): SyncResult {
    try {
      const calendar = calendarManager.getCalendar(market);
      const totalDays = Object.values(calendar.holidays).flat().length;
      
      return {
        market,
        success: true,
        updatedDays: totalDays,
        message: `Using cached data (${totalDays} records). Reason: ${reason}`,
      };
    } catch {
      return {
        market,
        success: false,
        updatedDays: 0,
        message: 'Failed to load calendar',
        error: reason,
      };
    }
  }

  /**
   * 检查是否需要更新（距离上次更新超过指定天数）
   */
  needsUpdate(market: Market, maxAgeDays: number = 30): boolean {
    try {
      const calendar = calendarManager.getCalendar(market);
      const lastUpdated = new Date(calendar.lastUpdated);
      const now = new Date();
      const ageDays = Math.floor((now.getTime() - lastUpdated.getTime()) / (1000 * 60 * 60 * 24));
      
      return ageDays > maxAgeDays;
    } catch {
      return true;
    }
  }
}

// 导出单例实例
export const calendarSyncer = new CalendarSyncer();

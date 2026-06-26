/**
 * 调度模块
 * 负责定时任务的调度和执行
 */

const fs = require('fs-extra');
const path = require('path');
const dayjs = require('dayjs');
const utc = require('dayjs/plugin/utc');
const timezone = require('dayjs/plugin/timezone');
const { info, warn, error, debug } = require('./logger');
const { updateConfig, loadConfig } = require('./config');

dayjs.extend(utc);
dayjs.extend(timezone);

/**
 * 创建调度器实例
 */
class Scheduler {
  constructor(config) {
    this.config = config;
    this.lastCheckTime = null;
  }

  /**
   * 检查是否应该执行备份
   * HEARTBEAT 触发时调用
   */
  async shouldRun() {
    try {
      // 重新加载配置（可能有更新）
      this.config = await loadConfig();
      
      if (!this.config.schedule.enabled) {
        return false;
      }
      
      const now = dayjs().tz(this.config.schedule.timezone || 'Asia/Shanghai');
      const cron = this.parseCron(this.config.schedule.cron);
      
      if (!cron) {
        await error('Scheduler', `无效的 cron 表达式: ${this.config.schedule.cron}`);
        return false;
      }
      
      // 检查是否匹配当前时间
      const matches = this.matchesCron(now, cron);
      
      if (matches) {
        // 检查今天是否已经执行过
        if (this.config.schedule.lastRun) {
          const lastRun = dayjs(this.config.schedule.lastRun).tz(this.config.schedule.timezone || 'Asia/Shanghai');
          
          if (lastRun.isSame(now, 'day')) {
            // 今天已经执行过
            return false;
          }
        }
        
        return true;
      }
      
      return false;
    } catch (err) {
      await error('Scheduler', `检查调度失败: ${err.message}`);
      return false;
    }
  }

  /**
   * 解析 cron 表达式
   * 支持: minute hour dayOfMonth month dayOfWeek
   */
  parseCron(expression) {
    try {
      const parts = expression.trim().split(/\s+/);
      
      if (parts.length !== 5) {
        return null;
      }
      
      return {
        minute: this.parseCronPart(parts[0], 0, 59),
        hour: this.parseCronPart(parts[1], 0, 23),
        dayOfMonth: this.parseCronPart(parts[2], 1, 31),
        month: this.parseCronPart(parts[3], 1, 12),
        dayOfWeek: this.parseCronPart(parts[4], 0, 6)
      };
    } catch (err) {
      return null;
    }
  }

  /**
   * 解析 cron 单个部分
   */
  parseCronPart(part, min, max) {
    if (part === '*') {
      return null; // 匹配所有
    }
    
    const values = new Set();
    
    // 处理逗号分隔
    const segments = part.split(',');
    
    for (const segment of segments) {
      // 处理范围 (e.g., 1-5)
      if (segment.includes('-')) {
        const [start, end] = segment.split('-').map(Number);
        for (let i = start; i <= end; i++) {
          if (i >= min && i <= max) {
            values.add(i);
          }
        }
      }
      // 处理步进 (e.g., */5)
      else if (segment.includes('/')) {
        const [, step] = segment.split('/');
        const stepNum = parseInt(step);
        for (let i = min; i <= max; i += stepNum) {
          values.add(i);
        }
      }
      // 单个值
      else {
        const num = parseInt(segment);
        if (!isNaN(num) && num >= min && num <= max) {
          values.add(num);
        }
      }
    }
    
    return values.size > 0 ? values : null;
  }

  /**
   * 检查时间是否匹配 cron
   */
  matchesCron(now, cron) {
    // 检查分钟
    if (cron.minute && !cron.minute.has(now.minute())) {
      return false;
    }
    
    // 检查小时
    if (cron.hour && !cron.hour.has(now.hour())) {
      return false;
    }
    
    // 检查日期
    if (cron.dayOfMonth && !cron.dayOfMonth.has(now.date())) {
      return false;
    }
    
    // 检查月份
    if (cron.month && !cron.month.has(now.month() + 1)) {
      return false;
    }
    
    // 检查星期
    if (cron.dayOfWeek && !cron.dayOfWeek.has(now.day())) {
      return false;
    }
    
    return true;
  }

  /**
   * 记录执行时间
   */
  async recordRun() {
    try {
      await updateConfig({
        schedule: {
          ...this.config.schedule,
          lastRun: new Date().toISOString()
        }
      });
      
      await info('Scheduler', `记录执行时间: ${new Date().toISOString()}`);
    } catch (err) {
      await error('Scheduler', `记录执行时间失败: ${err.message}`);
    }
  }

  /**
   * 获取下次执行时间
   */
  getNextRunTime() {
    try {
      const cron = this.parseCron(this.config.schedule.cron);
      
      if (!cron) {
        return null;
      }
      
      const now = dayjs().tz(this.config.schedule.timezone || 'Asia/Shanghai');
      let next = now.add(1, 'minute');
      
      // 简单实现：找到下一个匹配的小时和分钟
      // 如果 cron 是 "0 3 * * *"，则返回明天 3:00
      if (cron.hour && cron.hour.size === 1) {
        const targetHour = [...cron.hour][0];
        const targetMinute = cron.minute ? [...cron.minute][0] : 0;
        
        next = now.hour(targetHour).minute(targetMinute).second(0);
        
        // 如果今天的时间已过，则返回明天
        if (next.isBefore(now) || next.isSame(now)) {
          next = next.add(1, 'day');
        }
        
        return next.format('YYYY-MM-DD HH:mm:ss');
      }
      
      // 通用实现：逐分钟检查
      for (let i = 1; i <= 1440; i++) { // 最多检查一天
        next = now.add(i, 'minute');
        if (this.matchesCron(next, cron)) {
          return next.format('YYYY-MM-DD HH:mm:ss');
        }
      }
      
      return null;
    } catch (err) {
      return null;
    }
  }

  /**
   * 获取调度状态
   */
  getStatus() {
    return {
      enabled: this.config.schedule.enabled,
      cron: this.config.schedule.cron,
      timezone: this.config.schedule.timezone,
      lastRun: this.config.schedule.lastRun,
      nextRun: this.getNextRunTime()
    };
  }
}

/**
 * 人类可读的 cron 描述
 */
function describeCron(expression) {
  try {
    const cron = new Scheduler({ schedule: { cron: expression, timezone: 'Asia/Shanghai' } }).parseCron(expression);
    
    if (!cron) {
      return '无效的 cron 表达式';
    }
    
    // 常见模式
    if (expression === '0 3 * * *') {
      return '每天凌晨 3:00';
    }
    if (expression === '0 4 * * *') {
      return '每天凌晨 4:00';
    }
    if (expression === '0 0 * * *') {
      return '每天凌晨 0:00';
    }
    if (expression === '0 3 * * 0') {
      return '每周日凌晨 3:00';
    }
    if (expression === '0 3 1 * *') {
      return '每月 1 日凌晨 3:00';
    }
    
    // 自定义描述
    const parts = expression.split(' ');
    const minute = parts[0];
    const hour = parts[1];
    
    if (hour !== '*' && minute !== '*') {
      return `每天 ${hour.padStart(2, '0')}:${minute.padStart(2, '0')}`;
    }
    
    return expression;
  } catch (err) {
    return expression;
  }
}

module.exports = { Scheduler, describeCron };
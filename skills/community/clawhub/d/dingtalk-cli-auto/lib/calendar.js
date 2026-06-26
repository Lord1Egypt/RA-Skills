/**
 * 日程管理模块
 * 支持创建、查询、更新、删除日程
 */

const { DWSClient, parseTime, formatISO, formatDisplay } = require('./dws');

class CalendarClient {
  constructor(options = {}) {
    this.dws = new DWSClient(options);
  }

  /**
   * 创建日程
   * @param {Object} params - 日程参数
   * @param {string} params.title - 日程标题
   * @param {string} params.start - 开始时间 (ISO 8601 或相对时间)
   * @param {string} params.end - 结束时间 (ISO 8601 或相对时间)
   * @param {number} params.duration - 持续时间(分钟)，与 end 二选一
   * @param {string} params.attendees - 参会人(逗号分隔)
   * @param {string} params.location - 地点
   * @param {string} params.description - 描述
   * @returns {Object} 创建结果
   */
  async create(params) {
    const { title, start, end, duration, attendees, location, description } = params;
    
    if (!title) {
      throw new Error('日程标题不能为空');
    }
    if (!start) {
      throw new Error('开始时间不能为空');
    }

    // 处理时间
    const startDate = parseTime(start);
    if (!startDate) {
      throw new Error('无效的开始时间格式');
    }

    let endDate;
    if (end) {
      endDate = parseTime(end);
      if (!endDate) {
        throw new Error('无效的结束时间格式');
      }
    } else if (duration) {
      endDate = new Date(startDate.getTime() + duration * 60 * 1000);
    } else {
      // 默认1小时
      endDate = new Date(startDate.getTime() + 60 * 60 * 1000);
    }

    const args = [
      '--title', title,
      '--start', formatISO(startDate),
      '--end', formatISO(endDate)
    ];

    if (attendees) {
      args.push('--attendees', attendees);
    }
    if (location) {
      args.push('--location', location);
    }
    if (description) {
      args.push('--description', description);
    }

    const result = this.dws.exec('calendar', ['create', ...args]);
    return result;
  }

  /**
   * 查询日程列表
   * @param {Object} params - 查询参数
   * @param {string} params.start - 开始日期 (YYYY-MM-DD)
   * @param {string} params.end - 结束日期 (YYYY-MM-DD)
   * @param {boolean} params.today - 查询今天 (优先于 start/end)
   * @param {boolean} params.week - 查询本周
   * @returns {Array} 日程列表
   */
  async list(params = {}) {
    const args = [];
    
    if (params.today) {
      args.push('--today');
    } else if (params.week) {
      args.push('--week');
    } else if (params.start) {
      args.push('--start', params.start);
      if (params.end) {
        args.push('--end', params.end);
      }
    }

    const result = this.dws.exec('calendar', ['list', ...args]);
    
    // 格式化返回数据
    if (result.events && Array.isArray(result.events)) {
      return result.events.map(event => ({
        id: event.id,
        title: event.title,
        start: formatDisplay(new Date(event.start)),
        end: formatDisplay(new Date(event.end)),
        location: event.location,
        attendees: event.attendees || []
      }));
    }
    
    return result;
  }

  /**
   * 查询用户空闲时间
   * @param {string} users - 用户ID(逗号分隔)
   * @param {string} start - 开始时间
   * @param {string} end - 结束时间
   * @returns {Array} 空闲时段
   */
  async checkFreeBusy(users, start, end) {
    if (!users) {
      throw new Error('用户列表不能为空');
    }
    if (!start || !end) {
      throw new Error('开始和结束时间不能为空');
    }

    const startDate = parseTime(start);
    const endDate = parseTime(end);

    const args = [
      '--users', users,
      '--start', formatISO(startDate),
      '--end', formatISO(endDate)
    ];

    const result = this.dws.exec('calendar', ['free-busy', ...args]);
    return result;
  }

  /**
   * 更新日程
   * @param {string} eventId - 日程ID
   * @param {Object} updates - 更新内容
   * @returns {Object} 更新结果
   */
  async update(eventId, updates) {
    if (!eventId) {
      throw new Error('日程ID不能为空');
    }

    const args = ['--id', eventId];
    
    if (updates.title) args.push('--title', updates.title);
    if (updates.start) {
      const startDate = parseTime(updates.start);
      args.push('--start', formatISO(startDate));
    }
    if (updates.end) {
      const endDate = parseTime(updates.end);
      args.push('--end', formatISO(endDate));
    }
    if (updates.location) args.push('--location', updates.location);

    const result = this.dws.exec('calendar', ['update', ...args]);
    return result;
  }

  /**
   * 删除日程
   * @param {string} eventId - 日程ID
   * @returns {Object} 删除结果
   */
  async delete(eventId) {
    if (!eventId) {
      throw new Error('日程ID不能为空');
    }

    const result = this.dws.exec('calendar', ['delete', '--id', eventId]);
    return result;
  }
}

module.exports = CalendarClient;
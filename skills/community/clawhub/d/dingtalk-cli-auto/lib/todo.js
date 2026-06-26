/**
 * 待办事项管理模块
 * 支持创建、完成、删除、查询待办
 */

const { DWSClient, parseTime, formatISO, formatDisplay } = require('./dws');

class TodoClient {
  constructor(options = {}) {
    this.dws = new DWSClient(options);
  }

  /**
   * 创建待办事项
   * @param {Object} params - 待办参数
   * @param {string} params.content - 待办内容
   * @param {string} params.due - 截止时间 (ISO 8601 或相对时间)
   * @param {string} params.assignees - 负责人(逗号分隔)
   * @param {string} params.priority - 优先级 (low/medium/high)
   * @returns {Object} 创建结果
   */
  async create(params) {
    const { content, due, assignees, priority } = params;
    
    if (!content) {
      throw new Error('待办内容不能为空');
    }

    const args = ['--content', content];

    if (due) {
      const dueDate = parseTime(due);
      if (dueDate) {
        args.push('--due', formatISO(dueDate));
      }
    }

    if (assignees) {
      args.push('--assignees', assignees);
    }

    if (priority) {
      args.push('--priority', priority);
    }

    const result = this.dws.exec('todo', ['create', ...args]);
    return result;
  }

  /**
   * 查询待办列表
   * @param {Object} params - 查询参数
   * @param {boolean} params.all - 查询所有 (默认只查询未完成的)
   * @param {boolean} params.today - 查询今天到期的
   * @param {number} params.dueWithin - 查询 N 天内到期的
   * @param {string} params.assignee - 按负责人筛选
   * @returns {Array} 待办列表
   */
  async list(params = {}) {
    const args = [];

    if (params.all) {
      args.push('--all');
    }
    if (params.today) {
      args.push('--today');
    }
    if (params.dueWithin) {
      args.push('--due-within', params.dueWithin.toString());
    }
    if (params.assignee) {
      args.push('--assignee', params.assignee);
    }

    const result = this.dws.exec('todo', ['list', ...args]);
    
    // 格式化返回数据
    if (result.todos && Array.isArray(result.todos)) {
      return result.todos.map(todo => ({
        id: todo.id,
        content: todo.content,
        status: todo.status,
        due: todo.due ? formatDisplay(new Date(todo.due)) : null,
        assignee: todo.assignee,
        priority: todo.priority,
        createdAt: todo.createdAt ? formatDisplay(new Date(todo.createdAt)) : null
      }));
    }
    
    return result;
  }

  /**
   * 完成待办
   * @param {string} todoId - 待办ID
   * @returns {Object} 完成结果
   */
  async complete(todoId) {
    if (!todoId) {
      throw new Error('待办ID不能为空');
    }

    const result = this.dws.exec('todo', ['complete', '--id', todoId]);
    return result;
  }

  /**
   * 删除待办
   * @param {string} todoId - 待办ID
   * @returns {Object} 删除结果
   */
  async delete(todoId) {
    if (!todoId) {
      throw new Error('待办ID不能为空');
    }

    const result = this.dws.exec('todo', ['delete', '--id', todoId]);
    return result;
  }

  /**
   * 更新待办
   * @param {string} todoId - 待办ID
   * @param {Object} updates - 更新内容
   * @returns {Object} 更新结果
   */
  async update(todoId, updates) {
    if (!todoId) {
      throw new Error('待办ID不能为空');
    }

    const args = ['--id', todoId];

    if (updates.content) {
      args.push('--content', updates.content);
    }
    if (updates.due) {
      const dueDate = parseTime(updates.due);
      if (dueDate) {
        args.push('--due', formatISO(dueDate));
      }
    }
    if (updates.assignees) {
      args.push('--assignees', updates.assignees);
    }
    if (updates.priority) {
      args.push('--priority', updates.priority);
    }

    const result = this.dws.exec('todo', ['update', ...args]);
    return result;
  }
}

module.exports = TodoClient;
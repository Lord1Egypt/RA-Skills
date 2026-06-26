/**
 * 会话上下文管理器
 * 
 * 管理用户会话状态：当前路径、选中文件、操作历史等
 */

class SessionContext {
  constructor(sessionId = null) {
    this.sessionId = sessionId || this._generateSessionId();
    this.currentPath = '/';
    this.selectedFiles = [];
    this.history = [];
    this.lastAction = null;
    this.createdAt = Date.now();
    this.updatedAt = Date.now();
  }

  /**
   * 生成会话 ID
   */
  _generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 设置当前路径
   * @param {string} path - 目录路径
   */
  setPath(path) {
    this.currentPath = path;
    this.updatedAt = Date.now();
    
    // 记录到历史
    this._addToHistory('path_change', { from: this.history[this.history.length - 1]?.path, to: path });
    
    return this;
  }

  /**
   * 获取当前路径
   * @returns {string}
   */
  getPath() {
    return this.currentPath;
  }

  /**
   * 获取面包屑导航
   * @returns {Array<{name: string, path: string}>}
   */
  getBreadcrumb() {
    const parts = this.currentPath.split('/').filter(p => p);
    const breadcrumb = [];
    let currentPath = '';
    
    breadcrumb.push({ name: '根目录', path: '/' });
    
    parts.forEach(part => {
      currentPath += '/' + part;
      breadcrumb.push({ name: part, path: currentPath });
    });
    
    return breadcrumb;
  }

  /**
   * 进入子目录
   * @param {string} dirName - 目录名称
   */
  enterDirectory(dirName) {
    if (dirName === '..' || dirName === '返回') {
      return this.goBack();
    }
    
    const newPath = this.currentPath === '/' 
      ? `/${dirName}` 
      : `${this.currentPath}/${dirName}`;
    
    return this.setPath(newPath);
  }

  /**
   * 返回上一级
   */
  goBack() {
    if (this.currentPath === '/') {
      return this;
    }
    
    const parts = this.currentPath.split('/').filter(p => p);
    parts.pop();
    
    const newPath = parts.length === 0 ? '/' : '/' + parts.join('/');
    return this.setPath(newPath);
  }

  /**
   * 选中文件
   * @param {Array|Object} files - 文件 ID 或文件对象数组
   */
  selectFiles(files) {
    if (!Array.isArray(files)) {
      files = [files];
    }
    
    this.selectedFiles = files.map(f => typeof f === 'string' ? f : f.file_id || f.cid || f.id);
    this.updatedAt = Date.now();
    
    this._addToHistory('select_files', { count: this.selectedFiles.length });
    
    return this;
  }

  /**
   * 添加选中文件
   * @param {string|Object} file - 文件 ID 或文件对象
   */
  addSelectedFile(file) {
    const fileId = typeof file === 'string' ? file : file.file_id || file.cid || file.id;
    
    if (!this.selectedFiles.includes(fileId)) {
      this.selectedFiles.push(fileId);
      this.updatedAt = Date.now();
    }
    
    return this;
  }

  /**
   * 清除选中
   */
  clearSelected() {
    this.selectedFiles = [];
    this.updatedAt = Date.now();
    
    return this;
  }

  /**
   * 获取选中的文件
   * @returns {Array<string>}
   */
  getSelectedFiles() {
    return this.selectedFiles;
  }

  /**
   * 获取选中文件数量
   * @returns {number}
   */
  getSelectedCount() {
    return this.selectedFiles.length;
  }

  /**
   * 记录操作历史
   * @param {string} action - 操作类型
   * @param {Object} data - 操作数据
   */
  _addToHistory(action, data = {}) {
    this.history.push({
      action,
      data,
      timestamp: Date.now(),
      path: this.currentPath
    });
    
    // 保留最近 50 条记录
    if (this.history.length > 50) {
      this.history = this.history.slice(-50);
    }
    
    this.lastAction = { action, data, timestamp: Date.now() };
  }

  /**
   * 记录操作
   * @param {string} action - 操作类型
   * @param {Object} data - 操作数据
   */
  recordAction(action, data = {}) {
    this._addToHistory(action, data);
    return this;
  }

  /**
   * 获取历史记录
   * @param {number} limit - 限制数量
   * @returns {Array}
   */
  getHistory(limit = 20) {
    return this.history.slice(-limit);
  }

  /**
   * 获取最近操作
   * @returns {Object|null}
   */
  getLastAction() {
    return this.lastAction;
  }

  /**
   * 搜索历史
   * @param {string} actionType - 操作类型
   * @returns {Array}
   */
  searchHistory(actionType) {
    return this.history.filter(h => h.action === actionType);
  }

  /**
   * 返回到历史某个位置
   * @param {number} index - 历史记录索引
   */
  goToHistory(index) {
    if (index < 0 || index >= this.history.length) {
      return this;
    }
    
    const record = this.history[index];
    if (record.path) {
      this.currentPath = record.path;
      this.updatedAt = Date.now();
    }
    
    return this;
  }

  /**
   * 序列化上下文
   * @returns {string} JSON 字符串
   */
  serialize() {
    return JSON.stringify({
      sessionId: this.sessionId,
      currentPath: this.currentPath,
      selectedFiles: this.selectedFiles,
      history: this.history.slice(-20), // 只保留最近 20 条
      lastAction: this.lastAction,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    });
  }

  /**
   * 反序列化上下文
   * @param {string} json - JSON 字符串
   * @returns {SessionContext}
   */
  static deserialize(json) {
    try {
      const data = JSON.parse(json);
      const ctx = new SessionContext(data.sessionId);
      ctx.currentPath = data.currentPath || '/';
      ctx.selectedFiles = data.selectedFiles || [];
      ctx.history = data.history || [];
      ctx.lastAction = data.lastAction || null;
      ctx.createdAt = data.createdAt || Date.now();
      ctx.updatedAt = data.updatedAt || Date.now();
      return ctx;
    } catch (e) {
      // console.error('反序列化上下文失败:', e); // 静默失败
      return new SessionContext();
    }
  }

  /**
   * 重置上下文
   */
  reset() {
    this.currentPath = '/';
    this.selectedFiles = [];
    this.history = [];
    this.lastAction = null;
    this.updatedAt = Date.now();
    
    return this;
  }

  /**
   * 获取上下文信息
   * @returns {Object}
   */
  getInfo() {
    return {
      sessionId: this.sessionId,
      currentPath: this.currentPath,
      selectedCount: this.selectedFiles.length,
      historyCount: this.history.length,
      lastAction: this.lastAction?.action,
      createdAt: new Date(this.createdAt).toISOString(),
      updatedAt: new Date(this.updatedAt).toISOString()
    };
  }
}

module.exports = SessionContext;

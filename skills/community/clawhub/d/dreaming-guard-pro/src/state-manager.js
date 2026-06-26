/**
 * Dreaming Guard Pro - State Manager Module
 * 
 * 状态持久化，记录监控状态和健康检查点
 * 支持崩溃恢复
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 默认状态结构
const DEFAULT_STATE = {
  version: '1.0.0',
  lastUpdate: null,
  monitors: {},
  actions: [],
  recovery: {
    lastCheckpoint: null,
    crashes: 0,
    successfulRecoveries: 0,
    checkpoints: []
  }
};

// 默认配置
const DEFAULT_CONFIG = {
  statePath: path.join(os.homedir(), '.openclaw', 'dreaming-guard-state.json'),
  autoSave: true,
  saveInterval: 60000, // 1分钟自动保存
  maxCheckpoints: 10,
  maxActions: 100
};

/**
 * StateManager类 - 状态管理器
 */
class StateManager {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    this.statePath = this.config.statePath;
    this.state = JSON.parse(JSON.stringify(DEFAULT_STATE));
    this.autoSaveTimer = null;
    this.dirty = false;
  }

  /**
   * 加载状态文件
   * @returns {Promise<object>} 状态对象
   */
  async load() {
    if (fs.existsSync(this.statePath)) {
      try {
        const content = fs.readFileSync(this.statePath, 'utf-8');
        const loadedState = JSON.parse(content);
        // 合并加载的状态与默认状态（处理新字段）
        this.state = this._mergeState(DEFAULT_STATE, loadedState);
      } catch (err) {
        console.warn(`[StateManager] Failed to load state file: ${err.message}, using defaults`);
        // 备份损坏的文件
        this._backupCorruptedState();
      }
    }

    // 启动自动保存
    if (this.config.autoSave) {
      this._startAutoSave();
    }

    return this.state;
  }

  /**
   * 同步加载状态（兼容性方法）
   * @returns {object} 状态对象
   */
  loadSync() {
    if (fs.existsSync(this.statePath)) {
      try {
        const content = fs.readFileSync(this.statePath, 'utf-8');
        const loadedState = JSON.parse(content);
        this.state = this._mergeState(DEFAULT_STATE, loadedState);
      } catch (err) {
        console.warn(`[StateManager] Failed to load state file: ${err.message}`);
      }
    }
    return this.state;
  }

  /**
   * 合并状态对象
   * @param {object} defaultState - 默认状态
   * @param {object} loadedState - 加载的状态
   * @returns {object} 合并后的状态
   */
  _mergeState(defaultState, loadedState) {
    const result = { ...defaultState };
    for (const key of Object.keys(loadedState)) {
      if (loadedState[key] && typeof loadedState[key] === 'object' && !Array.isArray(loadedState[key])) {
        result[key] = this._mergeState(defaultState[key] || {}, loadedState[key]);
      } else {
        result[key] = loadedState[key];
      }
    }
    return result;
  }

  /**
   * 备份损坏的状态文件
   */
  _backupCorruptedState() {
    if (fs.existsSync(this.statePath)) {
      const backupPath = `${this.statePath}.corrupted.${Date.now()}`;
      try {
        fs.renameSync(this.statePath, backupPath);
        console.warn(`[StateManager] Corrupted state file backed up to: ${backupPath}`);
      } catch (err) {
        console.error(`[StateManager] Failed to backup corrupted state: ${err.message}`);
      }
    }
  }

  /**
   * 保存状态到文件
   * @param {object} data - 可选的状态数据，直接覆盖保存
   * @returns {Promise<void>}
   */
  async save(data = null) {
    if (data) {
      this.state = { ...this.state, ...data };
    }
    
    this.state.lastUpdate = Date.now();
    
    const dir = path.dirname(this.statePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // 原子写入：先写临时文件，再重命名
    const tempPath = `${this.statePath}.tmp`;
    fs.writeFileSync(tempPath, JSON.stringify(this.state, null, 2));
    fs.renameSync(tempPath, this.statePath);
    
    this.dirty = false;
  }

  /**
   * 同步保存状态
   */
  saveSync(data = null) {
    if (data) {
      this.state = { ...this.state, ...data };
    }
    this.state.lastUpdate = Date.now();
    
    const dir = path.dirname(this.statePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const tempPath = `${this.statePath}.tmp`;
    fs.writeFileSync(tempPath, JSON.stringify(this.state, null, 2));
    fs.renameSync(tempPath, this.statePath);
    
    this.dirty = false;
  }

  /**
   * 启动自动保存定时器
   */
  _startAutoSave() {
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
    }
    
    this.autoSaveTimer = setInterval(() => {
      if (this.dirty) {
        this.save().catch(err => {
          console.error(`[StateManager] Auto-save failed: ${err.message}`);
        });
      }
    }, this.config.saveInterval);
  }

  /**
   * 停止自动保存
   */
  stopAutoSave() {
    if (this.autoSaveTimer) {
      clearInterval(this.autoSaveTimer);
      this.autoSaveTimer = null;
    }
  }

  /**
   * 更新状态
   * @param {string} key - 状态键
   * @param {*} value - 状态值
   */
  update(key, value) {
    const keys = key.split('.');
    let current = this.state;
    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) {
        current[keys[i]] = {};
      }
      current = current[keys[i]];
    }
    current[keys[keys.length - 1]] = value;
    this.dirty = true;
  }

  /**
   * 获取状态值
   * @param {string} key - 状态键
   * @param {*} defaultValue - 默认值
   * @returns {*} 状态值
   */
  get(key, defaultValue = undefined) {
    const keys = key.split('.');
    let current = this.state;
    for (const k of keys) {
      if (current === undefined || current === null) {
        return defaultValue;
      }
      current = current[k];
    }
    return current !== undefined ? current : defaultValue;
  }

  /**
   * 获取当前检查点
   * @returns {object|null} 检查点数据
   */
  getCheckpoint() {
    return this.state.recovery?.lastCheckpoint || null;
  }

  /**
   * 设置检查点
   * @param {object} data - 检查点数据
   * @returns {object} 创建的检查点
   */
  setCheckpoint(data) {
    const checkpoint = {
      timestamp: Date.now(),
      data: data
    };

    // 添加到检查点列表
    if (!this.state.recovery.checkpoints) {
      this.state.recovery.checkpoints = [];
    }
    this.state.recovery.checkpoints.push(checkpoint);

    // 限制检查点数量
    if (this.state.recovery.checkpoints.length > this.config.maxCheckpoints) {
      this.state.recovery.checkpoints.shift();
    }

    this.state.recovery.lastCheckpoint = checkpoint;
    this.dirty = true;

    return checkpoint;
  }

  /**
   * 记录动作
   * @param {object} action - 动作对象
   */
  recordAction(action) {
    const actionRecord = {
      timestamp: Date.now(),
      ...action
    };

    this.state.actions.push(actionRecord);

    // 限制动作历史数量
    if (this.state.actions.length > this.config.maxActions) {
      this.state.actions = this.state.actions.slice(-this.config.maxActions);
    }

    this.dirty = true;
  }

  /**
   * 获取动作历史
   * @param {number} limit - 限制数量
   * @returns {array} 动作历史
   */
  getActionHistory(limit = 20) {
    return this.state.actions.slice(-limit);
  }

  /**
   * 更新监控器状态
   * @param {string} workspace - 工作区路径
   * @param {object} status - 状态对象
   */
  updateMonitorStatus(workspace, status) {
    this.state.monitors[workspace] = {
      ...this.state.monitors[workspace],
      ...status,
      lastUpdate: Date.now()
    };
    this.dirty = true;
  }

  /**
   * 获取监控器状态
   * @param {string} workspace - 工作区路径
   * @returns {object|null} 监控器状态
   */
  getMonitorStatus(workspace) {
    return this.state.monitors[workspace] || null;
  }

  /**
   * 记录崩溃
   */
  recordCrash() {
    this.state.recovery.crashes++;
    this.dirty = true;
  }

  /**
   * 记录成功恢复
   */
  recordSuccessfulRecovery() {
    this.state.recovery.successfulRecoveries++;
    this.dirty = true;
  }

  /**
   * 回滚到指定检查点
   * @param {number} timestamp - 检查点时间戳
   * @returns {object|null} 检查点数据
   */
  rollbackToCheckpoint(timestamp) {
    const checkpoint = this.state.recovery.checkpoints.find(
      cp => cp.timestamp === timestamp
    );
    if (checkpoint) {
      this.state.recovery.lastCheckpoint = checkpoint;
      this.dirty = true;
      return checkpoint.data;
    }
    return null;
  }

  /**
   * 获取所有检查点
   * @returns {array} 检查点列表
   */
  getCheckpoints() {
    return this.state.recovery?.checkpoints || [];
  }

  /**
   * 清理旧检查点
   * @param {number} maxAge - 最大保留时间（毫秒）
   */
  cleanOldCheckpoints(maxAge) {
    const cutoff = Date.now() - maxAge;
    this.state.recovery.checkpoints = this.state.recovery.checkpoints.filter(
      cp => cp.timestamp > cutoff
    );
    this.dirty = true;
  }

  /**
   * 销毁实例，清理资源
   */
  destroy() {
    this.stopAutoSave();
    // 最后保存一次
    if (this.dirty) {
      this.saveSync();
    }
  }
}

module.exports = StateManager;
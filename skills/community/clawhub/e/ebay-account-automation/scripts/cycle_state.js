/**
 * 账号轮换状态管理
 */

const fs = require('fs');
const path = require('path');

class CycleState {
  constructor(stateFile) {
    this.stateFile = stateFile;
    this.state = { accountIndex: 0, lastRun: null, totalRuns: 0, completedAccounts: [] };
  }

  load() {
    try {
      if (fs.existsSync(this.stateFile)) {
        const content = fs.readFileSync(this.stateFile, 'utf-8');
        const data = JSON.parse(content);
        this.state = { ...this.state, ...data };
      }
    } catch (e) {
      console.warn('状态文件读取失败，重新初始化:', e.message);
    }
    return this;
  }

  save() {
    try {
      const dir = path.dirname(this.stateFile);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(this.stateFile, JSON.stringify(this.state, null, 2), 'utf-8');
    } catch (e) {
      console.error('状态文件写入失败:', e.message);
    }
  }

  nextIndex(totalAccounts) {
    if (totalAccounts === 0) return 0;
    const idx = this.state.accountIndex % totalAccounts;
    this.state.accountIndex = (idx + 1) % totalAccounts;
    this.state.lastRun = new Date().toISOString();
    this.state.totalRuns++;
    this.save();
    return idx;
  }

  markCompleted(accountId) {
    if (!this.state.completedAccounts.includes(accountId)) {
      this.state.completedAccounts.push(accountId);
      this.save();
    }
  }

  reset() {
    this.state.accountIndex = 0;
    this.state.lastRun = null;
    this.state.totalRuns = 0;
    this.state.completedAccounts = [];
    this.save();
  }
}

module.exports = CycleState;

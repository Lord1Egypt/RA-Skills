const fs = require('fs');
const path = require('path');

/**
 * 极简版基于文件的持久化数据库（仅作示例，生产环境请使用 Redis/MySQL 或飞书多维表格/Miaoda 数据表）
 */
class SimpleStore {
  constructor(dbName = 'store.json') {
    this.dbPath = path.join(__dirname, dbName);
    this.data = this._load();
  }

  _load() {
    if (fs.existsSync(this.dbPath)) {
      return JSON.parse(fs.readFileSync(this.dbPath, 'utf8'));
    }
    return { sessions: {} };
  }

  _save() {
    fs.writeFileSync(this.dbPath, JSON.stringify(this.data, null, 2));
  }

  /**
   * 初始化一场会议的排期发包会话
   */
  createSession(id, details) {
    this.data.sessions[id] = {
      id,
      ...details,
      status: 'WAITING',
      participantsState: details.userIds.reduce((acc, uid) => {
        acc[uid] = { status: 'PENDING', selectedTime: null };
        return acc;
      }, {}),
      createdAt: Date.now()
    };
    this._save();
    return this.data.sessions[id];
  }

  getSession(id) {
    return this.data.sessions[id];
  }

  /**
   * 更新参会人的意向
   */
  updateParticipantState(sessionId, userId, selectedTime) {
    const session = this.data.sessions[sessionId];
    if (!session) return null;

    if (session.participantsState[userId]) {
      session.participantsState[userId] = {
        status: selectedTime === 'none' ? 'REJECTED' : 'CONFIRMED',
        selectedTime
      };
      this._save();
    }
    return session;
  }

  /**
   * 检查是否所有人都在该会话中做了决定且统一了意见
   */
  checkSessionConsensus(sessionId) {
    const session = this.data.sessions[sessionId];
    if (!session) return { done: false, result: null };

    const states = Object.values(session.participantsState);
    const pendingCount = states.filter(s => s.status === 'PENDING').length;
    
    // 还没全部回复
    if (pendingCount > 0) {
      return { done: false, result: 'pending' };
    }

    // 检查是否有拒绝
    const rejects = states.filter(s => s.status === 'REJECTED');
    if (rejects.length > 0) {
      return { done: true, result: 'conflict' };
    }

    // 检查是否选的时间一致
    const selectedTimes = states.map(s => s.selectedTime);
    const allSame = selectedTimes.every(t => t === selectedTimes[0]);

    if (allSame) {
      return { done: true, result: 'agreed', time: selectedTimes[0] };
    } else {
      return { done: true, result: 'conflict' }; // 时间挑的不一样
    }
  }
}

module.exports = new SimpleStore();

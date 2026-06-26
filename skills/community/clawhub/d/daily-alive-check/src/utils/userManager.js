const fs = require('fs');
const path = require('path');

/**
 * 用户数据管理器
 * 管理用户信息、签到记录、紧急联系人
 */
class UserManager {
  constructor() {
    this.dataDir = path.join(__dirname, '../data');
    this.usersFile = path.join(this.dataDir, 'users.json');
    this.checkinsFile = path.join(this.dataDir, 'checkins.json');

    this.ensureDataDir();
    this.users = this.loadUsers();
    this.checkins = this.loadCheckins();
  }

  /**
   * 确保数据目录存在
   */
  ensureDataDir() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  /**
   * 加载用户数据
   */
  loadUsers() {
    try {
      if (fs.existsSync(this.usersFile)) {
        const data = fs.readFileSync(this.usersFile, 'utf8');
        return JSON.parse(data);
      }
    } catch (error) {
      console.error('加载用户数据失败:', error.message);
    }
    return {};
  }

  /**
   * 加载签到记录
   */
  loadCheckins() {
    try {
      if (fs.existsSync(this.checkinsFile)) {
        const data = fs.readFileSync(this.checkinsFile, 'utf8');
        return JSON.parse(data);
      }
    } catch (error) {
      console.error('加载签到记录失败:', error.message);
    }
    return {};
  }

  /**
   * 保存用户数据
   */
  saveUsers() {
    try {
      fs.writeFileSync(this.usersFile, JSON.stringify(this.users, null, 2));
    } catch (error) {
      console.error('保存用户数据失败:', error.message);
    }
  }

  /**
   * 保存签到记录
   */
  saveCheckins() {
    try {
      fs.writeFileSync(this.checkinsFile, JSON.stringify(this.checkins, null, 2));
    } catch (error) {
      console.error('保存签到记录失败:', error.message);
    }
  }

  /**
   * 注册用户
   */
  registerUser(userId, userData) {
    this.users[userId] = {
      userId,
      name: userData.name,
      phone: userData.phone,
      emergencyContacts: userData.emergencyContacts || [],
      createdAt: new Date().toISOString(),
      lastCheckin: null,
      status: '未签到',
      consecutiveDays: 0
    };

    this.checkins[userId] = [];

    this.saveUsers();
    this.saveCheckins();

    return this.users[userId];
  }

  /**
   * 用户签到
   */
  checkin(userId, checkinData = {}) {
    if (!this.users[userId]) {
      throw new Error('用户不存在');
    }

    const now = new Date();
    const checkin = {
      timestamp: now.toISOString(),
      message: checkinData.message || '今天还活着！',
      mood: checkinData.mood || '😊',
      location: checkinData.location || '未知'
    };

    // 更新用户状态
    const lastCheckin = this.users[userId].lastCheckin;
    this.users[userId].lastCheckin = now.toISOString();
    this.users[userId].status = '正常';

    // 计算连续签到天数
    if (lastCheckin) {
      const lastDate = new Date(lastCheckin);
      const daysDiff = Math.floor((now - lastDate) / (1000 * 60 * 60 * 24));

      if (daysDiff === 1) {
        this.users[userId].consecutiveDays += 1;
      } else if (daysDiff > 1) {
        this.users[userId].consecutiveDays = 1;
      }
    } else {
      this.users[userId].consecutiveDays = 1;
    }

    // 保存签到记录
    if (!this.checkins[userId]) {
      this.checkins[userId] = [];
    }
    this.checkins[userId].push(checkin);

    // 只保留最近30天的记录
    if (this.checkins[userId].length > 30) {
      this.checkins[userId] = this.checkins[userId].slice(-30);
    }

    this.saveUsers();
    this.saveCheckins();

    return {
      success: true,
      user: this.users[userId],
      checkin
    };
  }

  /**
   * 获取用户状态
   */
  getUserStatus(userId) {
    const user = this.users[userId];
    if (!user) {
      return null;
    }

    const now = new Date();
    let hoursSinceLastCheckin = null;
    let status = '未签到';

    if (user.lastCheckin) {
      const lastCheckin = new Date(user.lastCheckin);
      hoursSinceLastCheckin = Math.floor((now - lastCheckin) / (1000 * 60 * 60));

      if (hoursSinceLastCheckin < 24) {
        status = '正常';
      } else if (hoursSinceLastCheckin < 48) {
        status = '警告';
      } else {
        status = '高危';
      }
    }

    return {
      ...user,
      hoursSinceLastCheckin,
      status,
      currentTime: now.toISOString()
    };
  }

  /**
   * 获取签到历史
   */
  getCheckinHistory(userId, days = 7) {
    if (!this.checkins[userId]) {
      return [];
    }

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    return this.checkins[userId].filter(checkin => {
      return new Date(checkin.timestamp) >= cutoffDate;
    });
  }

  /**
   * 获取所有需要检查的用户
   */
  getAllUsers() {
    return Object.values(this.users);
  }

  /**
   * 更新紧急联系人
   */
  updateEmergencyContacts(userId, contacts) {
    if (!this.users[userId]) {
      throw new Error('用户不存在');
    }

    this.users[userId].emergencyContacts = contacts;
    this.saveUsers();

    return this.users[userId];
  }

  /**
   * 删除用户
   */
  deleteUser(userId) {
    delete this.users[userId];
    delete this.checkins[userId];

    this.saveUsers();
    this.saveCheckins();
  }
}

module.exports = UserManager;

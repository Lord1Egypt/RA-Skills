/**
 * ClawGuard v3 - Guardian 核心引擎
 * 运行时守护者：行为监控、风险拦截、审计日志、会话回放、应急冻结
 */

const fs = require('fs');
const path = require('path');
const EventEmitter = require('events');
const os = require('os');

// 导入规则
const rules = require('../../shared/rules/interceptor-rules.js');

class Guardian extends EventEmitter {
  constructor() {
    super();
    this.rules = rules;
    this.sessions = new Map();
    this.currentSession = null;
    this.isActive = false;
    this.auditLogger = new AuditLogger();
  }

  /**
   * 启动守护模式
   */
  async start() {
    console.log('🛡️ Guardian 启动中...\n');

    // 创建新会话
    this.currentSession = this.createSession();
    this.isActive = true;

    console.log(`📝 会话 ID: ${this.currentSession.id}`);
    console.log(`🕐 开始时间: ${this.currentSession.startTime}\n`);

    // 加载历史会话
    await this.loadSessions();

    console.log(`✅ Guardian 已启动，共 ${this.sessions.size} 个历史会话\n`);
    console.log('监听模式已启用，等待操作...\n');

    // 模拟监控循环
    this.startMonitoringLoop();
  }

  /**
   * 创建新会话
   */
  createSession() {
    const session = {
      id: `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      startTime: new Date().toISOString(),
      endTime: null,
      status: 'active', // active, frozen, completed
      operations: [],
      riskEvents: [],
      frozen: false
    };
    this.sessions.set(session.id, session);
    return session;
  }

  /**
   * 加载历史会话
   */
  async loadSessions() {
    const logDir = path.join(os.homedir(), '.clawguard', 'logs');
    if (!fs.existsSync(logDir)) return;

    try {
      const files = fs.readdirSync(logDir).filter(f => f.endsWith('.jsonl'));
      for (const file of files.slice(-10)) { // 最多加载10个
        const content = fs.readFileSync(path.join(logDir, file), 'utf-8');
        const lines = content.split('\n').filter(l => l.trim());
        for (const line of lines) {
          try {
            const record = JSON.parse(line);
            if (record.sessionId && !this.sessions.has(record.sessionId)) {
              this.sessions.set(record.sessionId, {
                id: record.sessionId,
                startTime: record.sessionStart,
                status: 'completed',
                operations: [],
                riskEvents: []
              });
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    } catch (e) {
      // 忽略加载错误
    }
  }

  /**
   * 记录操作
   */
  logOperation(operation) {
    if (!this.currentSession) return;

    const record = {
      timestamp: new Date().toISOString(),
      sessionId: this.currentSession.id,
      sessionStart: this.currentSession.startTime,
      type: operation.type,
      action: operation.action,
      target: operation.target,
      result: operation.result,
      riskLevel: operation.riskLevel || 'INFO',
      blocked: operation.blocked || false
    };

    // 添加到当前会话
    this.currentSession.operations.push(record);

    // 写入审计日志
    this.auditLogger.log(record);

    // 检查风险
    if (operation.riskLevel && operation.riskLevel !== 'INFO') {
      this.handleRiskEvent(operation);
    }

    return record;
  }

  /**
   * 处理风险事件
   */
  handleRiskEvent(operation) {
    const riskEvent = {
      timestamp: new Date().toISOString(),
      sessionId: this.currentSession.id,
      operation: operation,
      severity: operation.riskLevel
    };

    this.currentSession.riskEvents.push(riskEvent);
    this.emit('risk', riskEvent);

    // 根据风险等级决定动作
    const riskConfig = this.rules.riskLevels[operation.riskLevel];
    if (riskConfig) {
      switch (riskConfig.action) {
        case 'auto_deny':
          this.blockOperation(operation);
          break;
        case 'require_confirm':
          this.promptConfirm(operation);
          break;
        case 'warn_and_log':
          this.emitWarning(operation);
          break;
      }
    }
  }

  /**
   * 阻止操作
   */
  blockOperation(operation) {
    operation.blocked = true;
    operation.result = 'BLOCKED';

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  🛑 操作已被拦截                                              ║
╠═══════════════════════════════════════════════════════════════╣
║  操作: ${operation.action.padEnd(49)}║
║  目标: ${(operation.target ? operation.target.padEnd(49) : 'N/A'.padEnd(49))}║
║  原因: ${operation.riskLevel} 风险                             ║
╚═══════════════════════════════════════════════════════════════╝
    `);

    this.emit('blocked', operation);
  }

  /**
   * 提示确认
   */
  promptConfirm(operation) {
    console.log(`
⚠️  检测到需要确认的操作:
   操作: ${operation.action}
   目标: ${operation.target || 'N/A'}
   风险: ${operation.riskLevel}
    `);
    this.emit('confirm-required', operation);
  }

  /**
   * 发出警告
   */
  emitWarning(operation) {
    const icon = operation.riskLevel === 'HIGH' ? '🔴' : '🟡';
    console.log(`${icon} 风险警告: ${operation.action} - ${operation.target}`);
    this.emit('warning', operation);
  }

  /**
   * 冻结会话
   */
  async freezeSession(sessionId) {
    let targetSession;

    if (sessionId === 'all') {
      targetSession = this.currentSession;
    } else {
      targetSession = this.sessions.get(sessionId);
    }

    if (!targetSession) {
      console.log(`❌ 会话不存在: ${sessionId}`);
      return;
    }

    targetSession.frozen = true;
    targetSession.status = 'frozen';
    targetSession.frozenAt = new Date().toISOString();

    // 写入冻结记录
    this.auditLogger.log({
      type: 'session_frozen',
      sessionId: targetSession.id,
      timestamp: new Date().toISOString()
    });

    console.log(`\n🛡️ 会话已冻结: ${targetSession.id}`);
    console.log(`   冻结时间: ${targetSession.frozenAt}`);
    console.log(`   待处理操作: ${targetSession.operations.filter(o => !o.result).length}`);

    this.emit('session-frozen', targetSession);
  }

  /**
   * 解冻会话
   */
  async unfreezeSession(sessionId) {
    let targetSession;

    if (sessionId === 'all') {
      targetSession = this.currentSession;
    } else {
      targetSession = this.sessions.get(sessionId);
    }

    if (!targetSession) {
      console.log(`❌ 会话不存在: ${sessionId}`);
      return;
    }

    targetSession.frozen = false;
    targetSession.status = 'active';
    targetSession.unfrozenAt = new Date().toISOString();

    this.auditLogger.log({
      type: 'session_unfrozen',
      sessionId: targetSession.id,
      timestamp: new Date().toISOString()
    });

    console.log(`\n✅ 会话已解冻: ${targetSession.id}`);

    this.emit('session-unfrozen', targetSession);
  }

  /**
   * 回放会话
   */
  async replaySession(sessionId) {
    const logDir = path.join(os.homedir(), '.clawguard', 'logs');
    if (!fs.existsSync(logDir)) {
      console.log('❌ 没有找到审计日志');
      return;
    }

    // 收集会话记录
    const records = [];
    const files = fs.readdirSync(logDir).filter(f => f.endsWith('.jsonl'));

    for (const file of files) {
      const content = fs.readFileSync(path.join(logDir, file), 'utf-8');
      const lines = content.split('\n').filter(l => l.trim());

      for (const line of lines) {
        try {
          const record = JSON.parse(line);
          if (!sessionId || sessionId === 'latest') {
            if (!record.sessionId || !record.sessionId.includes('session-')) continue;
            records.push(record);
          } else if (record.sessionId === sessionId) {
            records.push(record);
          }
        } catch (e) {
          // 忽略
        }
      }
    }

    if (records.length === 0) {
      console.log(`❌ 没有找到会话: ${sessionId || 'latest'}`);
      return;
    }

    // 去重并按时间排序
    const uniqueRecords = records.reduce((acc, record) => {
      const key = `${record.sessionId}-${record.timestamp}`;
      if (!acc.has(key)) {
        acc.set(key, record);
      }
      return acc;
    }, new Map());

    const sortedRecords = Array.from(uniqueRecords.values())
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                   📺 会话回放                               ║
╠═══════════════════════════════════════════════════════════════╣`);

    for (const record of sortedRecords) {
      if (record.type === 'operation') {
        const icon = record.blocked ? '🚫' : record.riskLevel === 'HIGH' ? '🔴' :
          record.riskLevel === 'MEDIUM' ? '🟡' : '✅';
        console.log(`║  ${icon} [${new Date(record.timestamp).toLocaleTimeString()}] ${record.action}`);
        if (record.target) {
          console.log(`║     目标: ${record.target.substring(0, 50)}`);
        }
      } else if (record.type === 'session_frozen') {
        console.log(`║  🧊 [${new Date(record.timestamp).toLocaleTimeString()}] 会话已冻结`);
      }
    }

    console.log('╚═══════════════════════════════════════════════════════════════╝');
  }

  /**
   * 显示状态
   */
  async showStatus() {
    const stats = {
      totalSessions: this.sessions.size,
      activeSessions: 0,
      frozenSessions: 0,
      totalOperations: 0,
      blockedOperations: 0,
      riskEvents: 0
    };

    for (const session of this.sessions.values()) {
      if (session.status === 'active') stats.activeSessions++;
      if (session.status === 'frozen') stats.frozenSessions++;
      stats.totalOperations += session.operations.length;
      stats.blockedOperations += session.operations.filter(o => o.blocked).length;
      stats.riskEvents += session.riskEvents.length;
    }

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                 🛡️ Guardian 状态                            ║
╠═══════════════════════════════════════════════════════════════╣
║  当前状态: ${(this.isActive ? '🟢 运行中' : '🔴 已停止').padEnd(47)}║
║  总会话数: ${stats.totalSessions.toString().padEnd(47)}║
║  活跃会话: ${stats.activeSessions.toString().padEnd(47)}║
║  冻结会话: ${stats.frozenSessions.toString().padEnd(47)}║
║  总操作数: ${stats.totalOperations.toString().padEnd(47)}║
║  拦截操作: ${stats.blockedOperations.toString().padEnd(47)}║
║  风险事件: ${stats.riskEvents.toString().padEnd(47)}║
╚═══════════════════════════════════════════════════════════════╝
    `);
  }

  /**
   * 显示日志
   */
  async showLogs(lines = 50) {
    const logDir = path.join(os.homedir(), '.clawguard', 'logs');
    if (!fs.existsSync(logDir)) {
      console.log('❌ 没有找到审计日志');
      return;
    }

    const files = fs.readdirSync(logDir)
      .filter(f => f.endsWith('.jsonl'))
      .sort()
      .slice(-3); // 最近3个文件

    const records = [];
    for (const file of files) {
      const content = fs.readFileSync(path.join(logDir, file), 'utf-8');
      const lines_content = content.split('\n').filter(l => l.trim()).slice(-lines);
      for (const line of lines_content) {
        try {
          records.push(JSON.parse(line));
        } catch (e) {
          // 忽略
        }
      }
    }

    records.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    console.log(`\n📜 最近 ${Math.min(lines, records.length)} 条日志:\n`);

    for (const record of records.slice(0, lines)) {
      const time = new Date(record.timestamp).toLocaleTimeString();
      if (record.type === 'operation') {
        const icon = record.blocked ? '🚫' : record.riskLevel === 'HIGH' ? '🔴' : '✅';
        console.log(`${icon} [${time}] ${record.action}`);
      } else if (record.type === 'session_frozen') {
        console.log(`🧊 [${time}] 会话冻结: ${record.sessionId}`);
      } else if (record.type === 'session_unfrozen') {
        console.log(`🔓 [${time}] 会话解冻: ${record.sessionId}`);
      }
    }
  }

  /**
   * 启动监控循环
   */
  startMonitoringLoop() {
    // 这是一个模拟循环，实际使用时应该接入真实的操作监控
    let count = 0;

    const checkInterval = setInterval(() => {
      if (!this.isActive) {
        clearInterval(checkInterval);
        return;
      }

      count++;
      if (count % 30 === 0) {
        // 每30秒输出一次心跳
        this.emit('heartbeat', {
          timestamp: new Date().toISOString(),
          sessionId: this.currentSession ? this.currentSession.id : undefined,
          operationsCount: this.currentSession ? (this.currentSession.operations ? this.currentSession.operations.length : 0) : 0
        });
      }
    }, 1000);
  }

  /**
   * 验证路径是否允许访问
   */
  validatePath(filePath) {
    const normalizedPath = path.normalize(filePath);

    // 检查禁止路径
    for (const pattern of this.rules.pathRules.deny) {
      if (this.matchPathPattern(normalizedPath, pattern)) {
        return {
          allowed: false,
          reason: '禁止访问该路径',
          pattern
        };
      }
    }

    return { allowed: true };
  }

  /**
   * 匹配路径模式
   */
  matchPathPattern(filePath, pattern) {
    // 简单的通配符匹配
    const regex = pattern
      .replace(/\*/g, '.*')
      .replace(/\//g, '\\/');
    return new RegExp(regex).test(filePath);
  }

  /**
   * 验证命令是否允许执行
   */
  validateCommand(command) {
    const lowerCommand = command.toLowerCase();

    // 检查禁止命令
    for (const pattern of this.rules.commandRules.deny) {
      if (new RegExp(pattern, 'i').test(lowerCommand)) {
        return {
          allowed: false,
          reason: '该命令被禁止执行',
          pattern
        };
      }
    }

    // 检查需要确认的命令
    for (const pattern of this.rules.commandRules.requireConfirm) {
      if (new RegExp(pattern, 'i').test(lowerCommand)) {
        return {
          allowed: true,
          requiresConfirm: true,
          reason: '该命令需要确认后执行'
        };
      }
    }

    return { allowed: true };
  }

  /**
   * 验证网络请求
   */
  validateNetworkRequest(url) {
    try {
      const urlObj = new URL(url);
      const host = urlObj.hostname;

      // 检查禁止主机
      for (const pattern of this.rules.networkRules.denyHosts) {
        if (new RegExp(pattern.replace(/\*/g, '.*')).test(host)) {
          return {
            allowed: false,
            reason: '禁止访问该主机',
            pattern
          };
        }
      }

      // 检查端口
      const port = parseInt(urlObj.port) || (urlObj.protocol === 'https:' ? 443 : 80);
      if (this.rules.networkRules.requireConfirmPorts.includes(port)) {
        return {
          allowed: true,
          requiresConfirm: true,
          reason: '高危端口需要确认'
        };
      }

      return { allowed: true };
    } catch (e) {
      return { allowed: false, reason: '无效的 URL' };
    }
  }
}

/**
 * 审计日志记录器
 */
class AuditLogger {
  constructor() {
    this.logDir = path.join(os.homedir(), '.clawguard', 'logs');
    this.ensureLogDir();
    this.currentFile = this.getLogFileName();
  }

  ensureLogDir() {
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }
  }

  getLogFileName() {
    const date = new Date().toISOString().split('T')[0];
    return path.join(this.logDir, `audit-${date}.jsonl`);
  }

  log(record) {
    try {
      // 检查是否需要切换文件
      const newFile = this.getLogFileName();
      if (newFile !== this.currentFile) {
        this.currentFile = newFile;
      }

      // 追加写入
      const line = JSON.stringify(record) + '\n';
      fs.appendFileSync(this.currentFile, line);

      // 检查文件大小，必要时轮转
      const stats = fs.statSync(this.currentFile);
      if (stats.size > (this.rules && this.rules.auditConfig && this.rules.auditConfig.maxLogSize) || 100 * 1024 * 1024) {
        // 简单轮转：添加序号
        const ext = path.extname(this.currentFile);
        const base = this.currentFile.replace(ext, '');
        this.currentFile = `${base}-${Date.now()}${ext}`;
      }
    } catch (e) {
      console.error('日志写入失败:', e.message);
    }
  }
}

module.exports = { Guardian };

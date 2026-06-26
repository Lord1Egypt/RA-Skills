#!/usr/bin/env node
/**
 * 健康监控器 v7.12
 * 
 * 核心功能:
 * 1. 检测任务队列与项目同步
 * 2. 检测进度更新超时
 * 3. 检测执行证据
 * 4. 告警通知
 */

const fs = require('fs');
const path = require('path');

class HealthMonitor {
  constructor(config = {}) {
    this.workspace = config.workspace || '/home/ubutu/.openclaw/workspace';
    this.agentsDir = path.join(this.workspace, '../agents');
    this.checkInterval = config.checkInterval || 60000;  // 1 分钟
    this.alerts = [];
    
    // ✅ 通用执行验证器
    this.verifier = new (require('./execution-verifier'))();
  }

  /**
   * 启动监控
   */
  startMonitoring() {
    console.log('🔍 健康监控已启动');
    
    setInterval(() => {
      this.checkAll();
    }, this.checkInterval);
    
    // 立即执行一次
    this.checkAll();
  }

  /**
   * 执行所有检查
   */
  checkAll() {
    this.checkTaskQueueSync();
    this.checkProgressUpdate();
    this.checkExecutionEvidence();
  }

  /**
   * 检查任务队列同步
   */
  checkTaskQueueSync() {
    const activeProject = this.getActiveProject();
    const queueProject = this.getQueueProject('novel_architect');
    
    if (activeProject && queueProject && activeProject !== queueProject) {
      this.alert('任务队列与项目脱节', {
        active: activeProject,
        queue: queueProject
      });
    }
  }

  /**
   * 检查进度更新
   */
  checkProgressUpdate() {
    const projects = this.getActiveProjects();
    
    for (const project of projects) {
      const progressFile = path.join(project, '创作进度追踪.md');
      
      if (fs.existsSync(progressFile)) {
        const stats = fs.statSync(progressFile);
        const gap = Date.now() - stats.mtimeMs;
        
        if (gap > 300000) {  // 5 分钟
          this.alert('进度追踪超时未更新', {
            project: project,
            lastUpdate: new Date(stats.mtime).toISOString(),
            gap: Math.round(gap / 60000) + '分钟'
          });
        }
      }
    }
  }

  /**
   * 检查执行证据（通用版）
   */
  checkExecutionEvidence() {
    const projects = this.getActiveProjects();
    
    for (const project of projects) {
      // ✅ 通用：获取项目任务类型
      const taskType = this.getProjectTaskType(project);
      
      if (taskType) {
        // 使用通用验证器
        this.verifier.verifyTaskCompletion(project, taskType)
          .then(result => {
            if (!result.valid) {
              this.alert('任务执行验证失败', {
                project,
                taskType,
                error: result.error,
                summary: result.summary
              });
            }
          })
          .catch(error => {
            this.alert('任务验证异常', {
              project,
              error: error.message
            });
          });
      }
    }
  }

  /**
   * 获取项目任务类型
   */
  getProjectTaskType(project) {
    // 从项目目录名或配置文件读取任务类型
    const configPath = path.join(project, '.task-config.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return config.taskType;
    }
    
    // 默认根据目录结构推断
    if (project) {
      return 'novel-outline';
    }
    
    return null;
  }

  /**
   * 获取活跃项目
   */
  getActiveProjects() {
    const novelArchitectDir = path.join(this.workspace, '../novel_architect/novel_reconstruction');
    
    if (!fs.existsSync(novelArchitectDir)) {
      return [];
    }
    
    return fs.readdirSync(novelArchitectDir)
      .filter(name => !name.startsWith('.'))
      .map(name => path.join(novelArchitectDir, name))
      .filter(dir => fs.statSync(dir).isDirectory());
  }

  /**
   * 获取当前项目
   */
  getActiveProject() {
    const projects = this.getActiveProjects();
    return projects.length > 0 ? projects[projects.length - 1] : null;
  }

  /**
   * 获取队列项目
   */
  getQueueProject(agentName) {
    const queueFile = path.join(this.agentsDir, agentName, 'tasks', 'QUEUE.md');
    
    if (!fs.existsSync(queueFile)) {
      return null;
    }
    
    const content = fs.readFileSync(queueFile, 'utf8');
    const match = content.match(/\*\*项目\*\*: (.+)/);
    return match ? match[1].trim() : null;
  }

  /**
   * 发送告警
   */
  alert(type, details) {
    const alert = {
      type,
      details,
      timestamp: new Date().toISOString()
    };
    
    this.alerts.push(alert);
    
    console.error(`⚠️ 异常告警：${type}`);
    console.error('详情:', details);
    
    // 记录到日志
    this.logAlert(alert);
  }

  /**
   * 记录告警日志
   */
  logAlert(alert) {
    const logFile = path.join(this.workspace, 'logs', 'health-alerts.log');
    const log = `[${alert.timestamp}] ${alert.type}: ${JSON.stringify(alert.details)}\n`;
    fs.appendFileSync(logFile, log);
  }

  /**
   * 获取告警历史
   */
  getAlerts(limit = 10) {
    return this.alerts.slice(-limit);
  }
}

module.exports = HealthMonitor;

// CLI 入口
if (require.main === module) {
  const monitor = new HealthMonitor();
  monitor.startMonitoring();
  
  console.log('健康监控运行中... (Ctrl+C 停止)');
}

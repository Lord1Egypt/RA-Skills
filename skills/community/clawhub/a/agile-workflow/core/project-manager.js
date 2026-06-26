#!/usr/bin/env node
/**
 * 项目管理器 v7.12
 * 
 * 核心功能:
 * 1. 自动任务分配（项目启动时更新 Agent 队列）
 * 2. 项目目录管理
 * 3. 状态同步
 */

const fs = require('fs');
const path = require('path');

class ProjectManager {
  constructor(config = {}) {
    this.workspace = config.workspace || '/home/ubutu/.openclaw/workspace';
    this.agentsDir = path.join(this.workspace, '../agents');
  }

  /**
   * 启动新项目
   */
  async startNewProject(projectName, projectDir) {
    console.log(`🚀 启动新项目：${projectName}`);
    
    // 1. 创建项目目录
    await this.createProjectDirectory(projectDir);
    
    // 2. ✅ 自动更新任务队列
    await this.updateAgentTaskQueue('novel_architect', {
      project: projectName,
      projectDir: projectDir,
      task: '章节细纲设计',
      chapters: 10,
      mode: 'serial'
    });
    
    // 3. 记录启动日志
    this.logProjectStart(projectName, projectDir);
    
    console.log(`✅ 项目 ${projectName} 启动完成`);
  }

  /**
   * 创建项目目录
   */
  async createProjectDirectory(projectDir) {
    const dirs = [
      projectDir,
      path.join(projectDir, '01_世界观架构'),
      path.join(projectDir, '02_人物体系'),
      path.join(projectDir, '03_情节大纲'),
      path.join(projectDir, '04_章节细纲'),
      path.join(projectDir, '05_正文创作'),
      path.join(projectDir, '06_质量审查')
    ];
    
    for (const dir of dirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 创建目录：${dir}`);
      }
    }
  }

  /**
   * 更新 Agent 任务队列
   */
  async updateAgentTaskQueue(agentName, taskInfo) {
    const queueFile = path.join(this.agentsDir, agentName, 'tasks', 'QUEUE.md');
    
    const queueContent = this.generateQueueContent(agentName, taskInfo);
    fs.writeFileSync(queueFile, queueContent, 'utf8');
    
    console.log(`📋 更新 ${agentName} 任务队列：${taskInfo.project}`);
  }

  /**
   * 生成任务队列内容
   */
  generateQueueContent(agentName, taskInfo) {
    const now = new Date().toISOString().replace('T', ' ').substring(0, 16);
    
    return `# ${agentName} Agent 任务队列

**状态**: 🚀 执行中  
**最后更新**: ${now}  
**项目**: ${taskInfo.project}  
**模式**: v7.11 完全串行（质量优先）

---

## 🚀 In Progress (进行中)

### 任务组：${taskInfo.task}

**总任务**: ${taskInfo.chapters} 章 | **当前**: 第 1 章

**创作模式**: v7.11 完全串行
- ✅ 逐章创作
- ✅ 每章同步状态
- ✅ 保证情节连贯

---

## 📊 总体进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 核心设定 | ✅ 完成 | 100% |
| 世界观架构 | ✅ 完成 | 100% |
| 人物体系 | ✅ 完成 | 100% |
| 情节大纲 | ✅ 完成 | 100% |
| **章节细纲** | 🚀 进行中 | **0%** (0/${taskInfo.chapters} 章) |

---

**${agentName} 立即开始执行任务！** 🚀

**触发执行时间**: ${now}
`;
  }

  /**
   * 记录项目启动日志
   */
  logProjectStart(projectName, projectDir) {
    const logFile = path.join(this.workspace, 'logs', 'project-start.log');
    const log = `[${new Date().toISOString()}] 项目启动：${projectName} @ ${projectDir}\n`;
    fs.appendFileSync(logFile, log);
  }
}

module.exports = ProjectManager;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectName, projectDir] = args;
  
  if (!projectName || !projectDir) {
    console.log('用法：node project-manager.js <项目名称> <项目目录>');
    process.exit(1);
  }
  
  const manager = new ProjectManager();
  manager.startNewProject(projectName, projectDir).catch(console.error);
}

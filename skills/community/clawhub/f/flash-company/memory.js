#!/usr/bin/env node

/**
 * Flash Company Memory System - 记忆持久化
 * 解决子代理关闭后记忆丢失的问题
 */

const fs = require('fs');
const path = require('path');

// 记忆根目录
const MEMORY_ROOT = path.join(process.env.HOME || process.env.USERPROFILE, '.agent-memory');

/**
 * 确保目录存在
 */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return dir;
}

/**
 * 记忆管理器
 */
class MemoryManager {
  constructor(teamName, sessionId) {
    this.teamName = teamName;
    this.sessionId = sessionId;
    this.teamDir = path.join(MEMORY_ROOT, 'flash-company', teamName);
    this.sessionFile = path.join(this.teamDir, 'sessions', `${sessionId}.json`);
    this.sharedDir = path.join(this.teamDir, 'shared');
    
    ensureDir(path.dirname(this.sessionFile));
    ensureDir(this.sharedDir);
  }

  /**
   * 初始化成员记忆
   */
  initMemberMemory(memberName, role) {
    const memberFile = path.join(this.teamDir, 'members', `${memberName}.json`);
    ensureDir(path.dirname(memberFile));
    
    if (!fs.existsSync(memberFile)) {
      const initialMemory = {
        name: memberName,
        role: role,
        createdAt: new Date().toISOString(),
        tasks: [],
        experiences: [],
        skills: [],
        notes: []
      };
      fs.writeFileSync(memberFile, JSON.stringify(initialMemory, null, 2));
    }
    
    return this.loadMemberMemory(memberName);
  }

  /**
   * 加载成员记忆
   */
  loadMemberMemory(memberName) {
    const memberFile = path.join(this.teamDir, 'members', `${memberName}.json`);
    if (fs.existsSync(memberFile)) {
      return JSON.parse(fs.readFileSync(memberFile, 'utf8'));
    }
    return null;
  }

  /**
   * 更新成员记忆
   */
  updateMemberMemory(memberName, updates) {
    const memory = this.loadMemberMemory(memberName) || {};
    const updated = { ...memory, ...updates, updatedAt: new Date().toISOString() };
    
    const memberFile = path.join(this.teamDir, 'members', `${memberName}.json`);
    ensureDir(path.dirname(memberFile));
    fs.writeFileSync(memberFile, JSON.stringify(updated, null, 2));
    
    return updated;
  }

  /**
   * 添加任务记录
   */
  addTask(memberName, task) {
    const memory = this.loadMemberMemory(memberName);
    if (!memory) return;
    
    memory.tasks.push({
      ...task,
      completedAt: new Date().toISOString()
    });
    
    this.updateMemberMemory(memberName, memory);
  }

  /**
   * 添加经验
   */
  addExperience(memberName, experience) {
    const memory = this.loadMemberMemory(memberName);
    if (!memory) return;
    
    memory.experiences.push({
      ...experience,
      learnedAt: new Date().toISOString()
    });
    
    this.updateMemberMemory(memberName, memory);
  }

  /**
   * 获取共享上下文
   */
  getSharedContext() {
    const contextFile = path.join(this.sharedDir, 'project-context.json');
    if (fs.existsSync(contextFile)) {
      return JSON.parse(fs.readFileSync(contextFile, 'utf8'));
    }
    return {
      project: null,
      requirements: [],
      decisions: [],
      currentPhase: 'unknown'
    };
  }

  /**
   * 更新共享上下文
   */
  updateSharedContext(updates) {
    const context = this.getSharedContext();
    const updated = { ...context, ...updates, updatedAt: new Date().toISOString() };
    
    const contextFile = path.join(this.sharedDir, 'project-context.json');
    fs.writeFileSync(contextFile, JSON.stringify(updated, null, 2));
    
    return updated;
  }

  /**
   * 记录决策
   */
  recordDecision(decision) {
    const decisionsFile = path.join(this.sharedDir, 'decisions.json');
    
    let decisions = [];
    if (fs.existsSync(decisionsFile)) {
      decisions = JSON.parse(fs.readFileSync(decisionsFile, 'utf8'));
    }
    
    decisions.push({
      ...decision,
      decidedAt: new Date().toISOString()
    });
    
    fs.writeFileSync(decisionsFile, JSON.stringify(decisions, null, 2));
  }

  /**
   * 记录经验教训
   */
  recordLesson(lesson) {
    const lessonsFile = path.join(this.sharedDir, 'lessons-learned.json');
    
    let lessons = [];
    if (fs.existsSync(lessonsFile)) {
      lessons = JSON.parse(fs.readFileSync(lessonsFile, 'utf8'));
    }
    
    lessons.push({
      ...lesson,
      learnedAt: new Date().toISOString()
    });
    
    fs.writeFileSync(lessonsFile, JSON.stringify(lessons, null, 2));
  }

  /**
   * 获取完整记忆摘要（用于子代理启动时注入）
   */
  getMemoryContext(memberName) {
    const memberMemory = this.loadMemberMemory(memberName);
    const sharedContext = this.getSharedContext();
    
    let context = `## 记忆上下文\n\n`;
    
    // 项目上下文
    if (sharedContext.project) {
      context += `### 当前项目\n`;
      context += `- 项目: ${sharedContext.project}\n`;
      context += `- 阶段: ${sharedContext.currentPhase}\n`;
      if (sharedContext.requirements.length > 0) {
        context += `- 需求: ${sharedContext.requirements.join(', ')}\n`;
      }
      context += `\n`;
    }
    
    // 成员记忆
    if (memberMemory) {
      if (memberMemory.tasks.length > 0) {
        context += `### 历史任务 (${memberMemory.tasks.length}个)\n`;
        const recentTasks = memberMemory.tasks.slice(-5);
        recentTasks.forEach(t => {
          context += `- ${t.description || t.name} (${t.status || '完成'})\n`;
        });
        context += `\n`;
      }
      
      if (memberMemory.experiences.length > 0) {
        context += `### 经验积累 (${memberMemory.experiences.length}条)\n`;
        const recentExp = memberMemory.experiences.slice(-5);
        recentExp.forEach(e => {
          context += `- ${e.insight || e.description}\n`;
        });
        context += `\n`;
      }
    }
    
    return context;
  }

  /**
   * 保存会话记录
   */
  saveSession(sessionData) {
    const session = {
      ...sessionData,
      endedAt: new Date().toISOString()
    };
    
    fs.writeFileSync(this.sessionFile, JSON.stringify(session, null, 2));
  }
}

// CLI 工具
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log('用法:');
    console.log('  node memory.js init <teamName> <memberName> <role>');
    console.log('  node memory.js context <teamName> <memberName>');
    console.log('  node memory.js update <teamName> <memberName> <json>');
    console.log('  node memory.js record-decision <teamName> <decision>');
    console.log('  node memory.js record-lesson <teamName> <lesson>');
    process.exit(0);
  }
  
  const teamName = args[1];
  const sessionId = `session-${Date.now()}`;
  const mm = new MemoryManager(teamName, sessionId);
  
  switch (command) {
    case 'init':
      const memberName = args[2];
      const role = args[3];
      const memory = mm.initMemberMemory(memberName, role);
      console.log(JSON.stringify(memory, null, 2));
      break;
      
    case 'context':
      const member = args[2];
      const context = mm.getMemoryContext(member);
      console.log(context);
      break;
      
    case 'update':
      const name = args[2];
      const updates = JSON.parse(args[3]);
      const updated = mm.updateMemberMemory(name, updates);
      console.log(JSON.stringify(updated, null, 2));
      break;
      
    case 'record-decision':
      mm.recordDecision({ decision: args[2] });
      console.log('决策已记录');
      break;
      
    case 'record-lesson':
      mm.recordLesson({ lesson: args[2] });
      console.log('经验已记录');
      break;
      
    default:
      console.log('未知命令:', command);
  }
}

// 只在直接运行时执行 CLI
if (require.main === module) {
  main();
}

module.exports = { MemoryManager };
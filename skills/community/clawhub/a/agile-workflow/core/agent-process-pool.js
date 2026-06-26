#!/usr/bin/env node
const { globalProcessManager } = require('./global-process-manager.js');
/**
 * Agent 并发执行器 v3.0（按 Agent 分组并发控制）
 *
 * 核心原则:
 * 1. 小说架构师串行执行（细纲）
 * 2. 小说写手串行执行（正文）
 * 3. 质量审核并发=2（审查）
 * 4. 每个 Agent 类型独立并发限制
 *
 * 架构说明:
 * - 不是限制同时有几个 Agent 干活
 * - 而是限制每个 Agent 实例的并行能力
 * - novel_architect/novel_writer 串行，novel_editor 并发=2
 */

const { spawn } = require('child_process');
const EventEmitter = require('events');
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');

// 🔌 FileManager 集成 - 解决 fs is not defined 问题
let FileManagerIntegration;
try {
  // 从 workspace 根目录加载
  const fmPath = require('path').join(process.cwd(), 'skills/file-manager/core/integration.js');
  FileManagerIntegration = require(fmPath).FileManagerIntegration;
} catch (e) {
  // 备用：从 agile-workflow 目录向上查找
  try {
    FileManagerIntegration = require('../../file-manager/core/integration').FileManagerIntegration;
  } catch (e2) {
    console.warn('⚠️ FileManager 模块未找到，使用原生 fs:', e.message);
    FileManagerIntegration = null;
  }
}

// 🔌 约束注入器集成 - 模型切换时自动注入文件操作约束
let ModelConstraintInjector;
try {
  const injectorPath = require('path').join(process.cwd(), 'skills/file-manager/core/model-constraint-injector.js');
  ModelConstraintInjector = require(injectorPath).ModelConstraintInjector;
} catch (e) {
  console.warn('⚠️ ModelConstraintInjector 未找到:', e.message);
  ModelConstraintInjector = null;
}

// 🔌 模型调用追踪器集成 - 记录 MODEL ACTION LOG
let ModelActionLogger;
try {
  const loggerPath = require('path').join(process.cwd(), 'skills/file-manager/core/model-action-logger.js');
  ModelActionLogger = require(loggerPath).ModelActionLogger;
} catch (e) {
  console.warn('⚠️ ModelActionLogger 未找到:', e.message);
  ModelActionLogger = null;
}

class AgentProcessPool extends EventEmitter {

  /**
   * 🔒 新增：清理指定 Agent 的残留进程
   */
  async cleanupStaleProcesses(agentType) {
    try {
      const { execSync } = require('child_process');
      // 查找并杀死该 Agent 类型的所有旧进程
      execSync(`pkill -f "openclaw.*--agent.*${agentType}" || true`, { stdio: 'ignore' });
      console.log(`🧹 已清理 ${agentType} 的残留进程`);
    } catch (e) {
      console.warn(`⚠️ 清理 ${agentType} 残留进程失败:`, e.message);
    }
  }


  constructor(config = {}) {
    super();

    this.config = {
      // ✅ 移除 maxPoolSize，按 Agent 分组控制并发
      idleTimeout: config.idleTimeout || 300000,   // 空闲超时（5 分钟）
      maxTasksPerProcess: config.maxTasksPerProcess || 10, // 单进程最大任务数
      workspace: config.workspace || '/home/ubutu/.openclaw/workspace',
      projectDir: config.projectDir,               // 项目目录（用于更新任务状态）
      reviewConcurrency: 2,                        // 审查任务并发（固定=2）
      ...config
    };

    // Agent 类型独立的并发控制
    this.agentConcurrent = {
      novel_architect: 1,  // 细纲串行
      novel_writer: 1,     // 正文串行
      novel_editor: 2      // 审查并发=2
    };

    // 进程池状态
    this.pool = new Map();  // agentId → ProcessInfo[]
    this.runningTasks = new Map();  // taskId → ProcessInfo
    this.processCounter = 0;  // 进程计数器（用于生成唯一 ID）

    // 按 Agent 类型统计并发
    this.stats = {
      totalSpawned: 0,
      totalCompleted: 0,
      totalFailed: 0,
      byAgent: {  // 按 Agent 类型统计
        novel_architect: 0,
        novel_writer: 0,
        novel_editor: 0
      }
    };

    // 🔒 状态文件同步
    this.stateFile = this.config.projectDir
      ? require('path').join(this.config.projectDir, '.task-state.json')
      : null;
    
    // 🔌 FileManager 初始化
    if (FileManagerIntegration && this.config.projectDir) {
      this.fileManager = new FileManagerIntegration({ projectDir: this.config.projectDir });
      console.log('📁 FileManager 已集成');
    } else {
      this.fileManager = null;
    }
    
    // 🔌 约束注入器初始化
    if (ModelConstraintInjector) {
      this.constraintInjector = new ModelConstraintInjector({
        workspace: this.config.workspace
      });
      console.log('🔒 ModelConstraintInjector 已集成');
    } else {
      this.constraintInjector = null;
    }
    
    // 🔌 模型调用追踪器初始化
    if (ModelActionLogger) {
      this.actionLogger = new ModelActionLogger({
        logFile: require('path').join(this.config.workspace, 'logs/model-action.log')
      });
      console.log('📊 ModelActionLogger 已集成');
    } else {
      this.actionLogger = null;
    }
  }

  /**
   * 更新任务状态文件（同步到磁盘）
   */
  updateTaskState(taskId, status, error = null) {
    if (!this.stateFile) return;

    try {
      const fs = require('fs');
      const state = JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));

      if (state[taskId]) {
        state[taskId].status = status;
        if (error) state[taskId].error = error;
        if (status === 'completed') {
          state[taskId].completedAt = new Date().toISOString();
        }
        state[taskId].updatedAt = new Date().toISOString();

        fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2));
        console.log(`📊 已同步任务状态：${taskId} → ${status}`);
      }
    } catch (e) {
      console.error(`⚠️ 更新任务状态失败：${taskId}`, e.message);
    }
  }

  /**
   * 生成进程唯一 ID
   */
  generateProcessId(agentType) {
    const timestamp = Date.now();
    const counter = ++this.processCounter;
    const hash = crypto.createHash('md5').update(`${agentType}-${timestamp}-${counter}`).digest('hex').substring(0, 8);
    return `${agentType}-${hash}-${counter}`;
  }

  /**
   * 获取任务执行槽位（并发控制）
   * 新架构：按 Agent 类型分组控制并发
   */
  async acquireExecutionSlot(taskId, maxRetries = 5) {
    // 🔒 根据任务 ID 获取 Agent 类型
    const agentType = this.getAgentType(taskId);
    const isReviewTask = taskId.includes('review');

    // 获取该 Agent 类型的最大并发数
    const maxConcurrency = isReviewTask
      ? this.config.reviewConcurrency  // 审查任务并发=2
      : 1;  // 细纲/正文串行

    // 1. 统计该 Agent 类型的活跃任务数
    const activeSlots = this.pool.has(agentType) ? this.pool.get(agentType) : [];
    const activeCount = activeSlots.filter(s => s.status === 'busy').length;

    // 如果该 Agent 类型已达到并发上限，等待
    if (activeCount >= maxConcurrency) {
      if (maxRetries <= 0) {
        console.error(`❌ ${agentType} 持续等待超限（5次），强制获取槽位`);
        // 强制获取：不等待，直接创建 slot
      } else {
        console.log(`⚠️ ${agentType} 已达并发上限 (${maxConcurrency}/${maxConcurrency})，等待中...`);
        await this.waitForIdleSlot();
        return this.acquireExecutionSlot(taskId, maxRetries - 1);
      }
    }

    // 2. 创建任务执行上下文
    const taskSlot = this.createTaskSlot(agentType, taskId);

    return taskSlot;
  }

  /**
   * 创建任务执行槽位
   */
  createTaskSlot(agentType, taskId) {
    const slotId = this.generateTaskId(agentType, taskId);

    const slotInfo = {
      id: slotId,
      agentType,
      taskId,
      status: 'busy',
      createdAt: Date.now(),
      process: null
    };

    // 记录到槽位池
    if (!this.pool.has(agentType)) {
      this.pool.set(agentType, []);
    }
    this.pool.get(agentType).push(slotInfo);

    this.stats.totalSpawned++;
    if (!this.stats.byAgent[agentType]) this.stats.byAgent[agentType] = 0;
    this.stats.byAgent[agentType]++;
    
    const agentActive = this.pool.get(agentType).filter(s => s.status === 'busy').length;
    const maxConcurrency = agentType === 'novel_editor' ? 2 : 1;
    console.log(`📋 任务槽位：${slotId} (${agentType}: ${agentActive}/${maxConcurrency})`);

    return slotInfo;
  }

  /**
   * 生成任务唯一 ID
   */
  generateTaskId(agentType, taskId) {
    const timestamp = Date.now();
    const counter = ++this.processCounter;
    const hash = crypto.createHash('md5').update(`${agentType}-${taskId}-${timestamp}-${counter}`).digest('hex').substring(0, 8);
    return `${agentType}-${hash}-${counter}`;
  }

  /**
   * 等待空闲槽位
   * 说明：按 Agent 分组控制并发，此函数已不再使用（保留作为兜底）
   */
  waitForIdleSlot() {
    return new Promise((resolve) => {
      const checkInterval = setInterval(() => {
        const totalActive = Array.from(this.pool.values())
          .flat()
          .filter(p => p.status === 'busy')
          .length;

        // ✅ 使用按 Agent 分组的最大并发数（novel_editor=2，其他=1）
        const maxPoolSize = 2; // 审查任务最大并发
        if (totalActive < maxPoolSize) {
          clearInterval(checkInterval);
          resolve();
        }
      }, 500);

      // 超时保护
      setTimeout(() => {
        clearInterval(checkInterval);
        resolve();
      }, 30000);
    });
  }

  /**
   * 执行任务（保证独立性）
   */
  async executeTask(task) {
    const { agent, description, taskId } = task;

    // 获取执行槽位（并发控制）
    const slotInfo = await this.acquireExecutionSlot(agent, taskId);

    // 记录运行中任务
    this.runningTasks.set(taskId, slotInfo);

    return new Promise((resolve, reject) => {
      // 🔒 独立性保障 1: 独立环境变量
      const env = {
        ...process.env,
        OPENCLAW_TASK_ID: taskId,
        OPENCLAW_AGENT_ID: agent,
        OPENCLAW_SLOT_ID: slotInfo.id,
        OPENCLAW_PROJECT_DIR: this.config.projectDir  // ✅ 项目路径 (修复输出路径问题)
      };

      // 🔒 独立性保障 2: 独立工作目录
      const cwd = this.config.workspace;

      // 🔒 独立性保障 3: 独立进程（spawn 新进程，非复用）
      const cmd = '/home/ubutu/.npm-global/bin/openclaw';
      const args = [
        'agent',
        '--local',
        '--agent', agent,
        '--thinking', 'minimal',
        '-m', `${description}`
      ];

      // 🔒 全局进程数检查
      if (!globalProcessManager.canSpawnNewProcess()) {
        console.log('⚠️ 全局进程数已达上限，跳过启动');
        reject(new Error('全局进程数已达上限'));
        return;
      }
      
      console.log(`🚀 启动独立进程：${slotInfo.id}`);
      console.log(`   任务：${taskId}`);
      console.log(`   Agent: ${agent}`);

      const child = spawn(cmd, args, {
        cwd,
        env,
        stdio: ['ignore', 'pipe', 'pipe'],
        // 🔒 独立性保障 4: 独立进程组
        detached: false
      });

      slotInfo.process = child;

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', (data) => {
        stdout += data.toString();
        console.log(`[${slotInfo.id}] ${data.toString().trim()}`);
      });

      child.stderr.on('data', (data) => {
        stderr += data.toString();
        console.error(`[${slotInfo.id}] ${data.toString().trim()}`);
      });

      // 🔒 新增：超时强制杀死进程（5 分钟）
      const timeout = setTimeout(() => {
        console.log(`⚠️ [${slotInfo.id}] 任务超时，强制终止进程`);
        if (child && !child.killed) {
          child.kill('SIGKILL');
        }
      }, 5 * 60 * 1000);  // 5 分钟超时

      child.on('close', async (code) => {
        clearTimeout(timeout);  // 清除超时定时器
        // 🔒 独立性保障 5: 任务完成后彻底清理
        slotInfo.status = 'completed';
        this.runningTasks.delete(taskId);

        // 从槽位池移除
        const agentSlots = this.pool.get(agent) || [];
        const index = agentSlots.indexOf(slotInfo);
        if (index > -1) {
          agentSlots.splice(index, 1);
        }

        if (!this.stats.byAgent[agent]) this.stats.byAgent[agent] = 0;
        this.stats.byAgent[agent]--;

        if (code === 0) {
          // ✅ 将 stdout 写入文件（Agent 的输出是 Markdown 内容）
          const match = taskId.match(/chapter-(\d+)-(outline|writing)/);
          if (match) {
            const chapterNum = match[1];
            const taskType = match[2];
            let outputDir = taskType === 'outline' 
              ? path.join(this.config.projectDir, '04_章节细纲')
              : path.join(this.config.projectDir, '05_正文创作');
            
            // 生成文件名
            let fileName = `第${chapterNum}章`;
            if (taskType === 'outline') {
              fileName += '_细纲.md';
            } else {
              fileName += '.md';
            }
            
            const filePath = path.join(outputDir, fileName);
            
            // 🔌 写入文件 - 优先使用 FileManager
            try {
              if (this.fileManager) {
                // 使用 FileManager 写入（带审计日志）
                const result = await this.fileManager.writeAgentOutput(taskId, stdout);
                if (result.success) {
                  console.log(`✅ FileManager 写入成功：${result.path} (${stdout.length} 字符)`);
                } else {
                  throw new Error(result.error || 'FileManager 写入失败');
                }
              } else {
                // 回退到原生 fs
                if (!fs.existsSync(outputDir)) {
                  fs.mkdirSync(outputDir, { recursive: true });
                }
                fs.writeFileSync(filePath, stdout, 'utf-8');
                console.log(`✅ fs 写入成功：${filePath} (${stdout.length} 字符)`);
              }
            } catch (wError) {
              console.error(`❌ 写入文件失败：${filePath} - ${wError.message}`);
              this.stats.totalFailed++;
              this.updateTaskState(taskId, 'failed', `写入文件失败: ${wError.message}`);
              reject(wError);
              return;
            }
          }
          
          // ✅ 产出物验证：检查文件是否真的生成了
          const outputFileExists = this.verifyOutputFile(taskId, agent, stdout);
          
          if (outputFileExists) {
            // ✅ 进一步验证内容有效性
            const match = taskId.match(/chapter-(\d+)-(outline|writing)/);
            if (match) {
              const chapterNum = match[1];
              const taskType = match[2];
              let outputDir = taskType === 'outline' 
                ? path.join(this.config.projectDir, '04_章节细纲')
                : path.join(this.config.projectDir, '05_正文创作');
              const outputFile = fs.readdirSync(outputDir).find(f => f.includes(`第${chapterNum}章`));
              if (outputFile) {
                const contentValid = this.verifyOutputContent(taskId, agent, path.join(outputDir, outputFile));
                if (!contentValid) {
                  this.stats.totalFailed++;
                  const errorMsg = '产出物文件存在但内容无效（可能 Token 超限导致截断）';
                  console.error(`❌ 产出物验证失败：${taskId} - ${errorMsg}`);
                  
                  this.updateTaskState(taskId, 'failed', errorMsg);
                  reject(new Error(errorMsg));
                  return;
                }
              }
            }
            
            this.stats.totalCompleted++;
            const agentActive = this.pool.has(agent) ? this.pool.get(agent).filter(s => s.status === 'busy').length : 0;
            const maxC = agent === 'novel_editor' ? 2 : 1;
            console.log(`✅ 任务完成：${taskId} (${slotInfo.id})`);
            console.log(`📊 ${agent} 并发：${agentActive}/${maxC}`);

            // 🔒 同步任务状态到文件
            this.updateTaskState(taskId, 'completed');

            resolve({ code, stdout, stderr, slotId: slotInfo.id });
          } else {
            // ❌ 产出物不存在，标记为失败
            this.stats.totalFailed++;
            const errorMsg = '任务输出完整但文件未保存 (可能 Token 超限或路径错误)';
            console.error(`❌ 产出物验证失败：${taskId} - ${errorMsg}`);
            console.error(`📊 stdout 长度：${stdout.length} 字符`);

            this.updateTaskState(taskId, 'failed', errorMsg);

            reject(new Error(errorMsg));
          }
        } else {
          this.stats.totalFailed++;
          console.error(`❌ 任务失败：${taskId} (${slotInfo.id}) 退出码：${code}`);

          // 🔒 同步失败状态到文件
          this.updateTaskState(taskId, 'failed', `退出码：${code}`);

          reject(new Error(`任务失败，退出码：${code}`));
        }
      });

      child.on('error', (error) => {
        slotInfo.status = 'error';
        this.runningTasks.delete(taskId);
        this.stats.totalFailed++;

        // 🔒 同步错误状态到文件
        this.updateTaskState(taskId, 'failed', error.message);

        reject(error);
      });
    });
  }

  // 注意：不复用进程，因此不需要回收逻辑
  // 每个任务完成后自动清理槽位

  /**
   * ✅ 产出物验证：检查文件是否真的生成了
   */
  verifyOutputFile(taskId, agent, stdout) {
    const fs = require('fs');  // ✅ 在函数内引入 fs 模块
    if (!this.config.projectDir) return true;  // 无项目目录则跳过验证

    try {
      // 解析任务 ID 获取章节号
      const match = taskId.match(/chapter-(\d+)-(outline|writing)/);
      if (!match) return true;  // 非章节任务跳过验证

      const chapterNum = match[1];
      const taskType = match[2];

      // 根据任务类型确定输出目录
      let outputDir, fileNamePattern;
      if (taskType === 'outline') {
        outputDir = path.join(this.config.projectDir, '04_章节细纲');
        fileNamePattern = `第${chapterNum}章`;
      } else if (taskType === 'writing') {
        outputDir = path.join(this.config.projectDir, '05_正文创作');
        fileNamePattern = `第${chapterNum}章`;
      } else {
        return true;  // 未知任务类型跳过验证
      }

      // 检查目录是否存在
      if (!fs.existsSync(outputDir)) {
        console.warn(`⚠️ 输出目录不存在：${outputDir}`);
        return false;
      }

      // 检查文件是否存在
      const files = fs.readdirSync(outputDir);
      const outputFile = files.find(f => f.includes(fileNamePattern));

      if (outputFile) {
        const filePath = path.join(outputDir, outputFile);
        const stats = fs.statSync(filePath);
        console.log(`✅ 产出物验证通过：${filePath} (${stats.size} 字节)`);
        return true;
      } else {
        console.warn(`⚠️ 产出物文件未找到：${outputDir}/${fileNamePattern}*`);
        console.warn(`📊 stdout 长度：${stdout.length} 字符`);

        // 检查 stdout 是否有实际内容
        if (stdout.length < 100) {
          console.warn(`⚠️ 输出内容过短，可能未完整生成`);
          return false;
        }

        // 有输出但文件未保存，可能是路径问题
        return false;
      }
    } catch (e) {
      console.warn(`⚠️ 产出物验证异常：${e.message}`);
      return false;
    }
  }

  /**
   * ✅ 产出物内容验证：检查文件内容是否有效
   * v3.1 增强版：增加 Agent 内部思考检测
   */
  verifyOutputContent(taskId, agent, filePath) {
    const fs = require('fs');  // ✅ 在函数内引入 fs 模块
    
    try {
      if (!fs.existsSync(filePath)) {
        console.warn(`⚠️ 文件不存在：${filePath}`);
        return false;
      }
      
      const content = fs.readFileSync(filePath, 'utf-8');
      const size = content.length;
      
      // ✅ 文件大小验证
      if (size < 100) {
        console.warn(`⚠️ 文件内容过小：${filePath} (${size} 字符)`);
        return false;
      }
      
      // ✅ Markdown 格式验证（章节任务）
      if (taskId.includes('outline') || taskId.includes('writing')) {
        // 检查是否包含基本 Markdown 元素
        const hasTitle = content.includes('#') || content.includes('##');
        const hasContent = content.length > 500;
        
        if (!hasTitle || !hasContent) {
          console.warn(`⚠️ 文件内容格式错误：${filePath} (缺少标题或内容)`);
          return false;
        }
        
        // 🆕 v3.1: 检测 Agent 内部思考模式
        const agentThinkingPatterns = [
          /^Now I understand the context/i,
          /^Let me plan/i,
          /^I need to/i,
          /^I should/i,
          /^The user said/i,
          /^I'll write/i,
          /^Let me start/i,
          /^I've completed/i,
          /previous model attempt failed/i,
          /expanding the scenes/i
        ];
        
        // 检查文件开头 500 字符是否匹配 Agent 思考模式
        const header = content.substring(0, 500);
        for (const pattern of agentThinkingPatterns) {
          if (pattern.test(header)) {
            console.warn(`⚠️ 检测到 Agent 内部思考模式：${pattern}`);
            console.warn(`⚠️ 文件内容不是小说正文，验证失败`);
            return false;
          }
        }
        
        // 🆕 v3.1: 检测是否缺少小说核心元素
        // 小说正文应该包含：对话、叙述、场景描写
        const hasDialogue = /["「""]/.test(content);
        const hasNarration = content.length > 2000;  // 小说正文通常较长
        const hasSceneDescription = /（|，|。/.test(content);  // 中文标点
        
        if (!hasDialogue && !hasSceneDescription && !hasNarration) {
          console.warn(`⚠️ 缺少小说核心元素（对话/叙述/场景描写）`);
          // 不直接返回 false，可能是一些特殊章节
        }
      }
      
      console.log(`✅ 产出物内容验证通过：${filePath} (${size} 字符)`);
      return true;
    } catch (e) {
      console.warn(`⚠️ 产出物内容验证异常：${e.message}`);
      return false;
    }
  }

  /**
   * 根据任务 ID 获取对应的 Agent 类型
   */
  getAgentType(taskId) {
    if (taskId.includes('outline')) return 'novel_architect';
    if (taskId.includes('writing')) return 'novel_writer';
    if (taskId.includes('review')) return 'novel_editor';
    return 'novel_architect';
  }

  /**
   * 获取池状态
   */
  getStatus() {
    // 计算当前活跃任务数
    let currentActive = 0;
    for (const [agentType, slots] of this.pool.entries()) {
      currentActive += slots.filter(s => s.status === 'busy').length;
    }

    const status = {
      config: this.config,
      stats: {
        currentActive,  // ✅ 添加当前活跃任务数
        totalSpawned: this.stats.totalSpawned,
        totalCompleted: this.stats.totalCompleted,
        totalFailed: this.stats.totalFailed,
        byAgent: this.stats.byAgent
      },
      pools: {}
    };

    for (const [agentType, processes] of this.pool.entries()) {
      status.pools[agentType] = processes.map(p => ({
        id: p.id,
        status: p.status,
        taskCount: p.taskCount,
        age: Math.round((Date.now() - p.createdAt) / 1000)
      }));
    }

    return status;
  }

  /**
   * 清理所有运行中任务
   */
  async cleanup() {
    console.log('🧹 清理运行中任务...');

    const promises = [];
    for (const [taskId, slotInfo] of this.runningTasks.entries()) {
      if (slotInfo.process) {
        console.log(`  终止任务：${taskId} (${slotInfo.id})`);
        promises.push(new Promise((resolve) => {
          slotInfo.process.on('close', resolve);
          slotInfo.process.kill('SIGTERM');
        }));
      }
    }

    await Promise.all(promises);
    this.pool.clear();
    this.runningTasks.clear();

    console.log('✅ 所有任务已清理');
  }
}

module.exports = AgentProcessPool;

// CLI 测试入口
if (require.main === module) {
  const pool = new AgentProcessPool({
    workspace: '/home/ubutu/.openclaw/workspace',
    projectDir: '/home/ubutu/.openclaw/workspace-novel_architect',
    reviewConcurrency: 2
  });

  console.log('🧪 测试进程池...');

  // 模拟任务
  const tasks = [
    { agent: 'novel_editor', description: '第 1 章审查', taskId: 'task-1' },
    { agent: 'novel_editor', description: '第 2 章审查', taskId: 'task-2' },
    { agent: 'novel_editor', description: '第 3 章审查', taskId: 'task-3' },
    { agent: 'novel_architect', description: '第 4 章细纲', taskId: 'task-4' },
  ];

  (async () => {
    for (const task of tasks) {
      try {
        await pool.executeTask(task);
      } catch (e) {
        console.error(e.message);
      }
    }

    console.log('📊 最终状态:', JSON.stringify(pool.getStatus(), null, 2));
    await pool.cleanup();
    process.exit(0);
  })();
}

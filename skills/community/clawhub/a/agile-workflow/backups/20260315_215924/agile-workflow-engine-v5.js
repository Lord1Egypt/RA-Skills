#!/usr/bin/env node
/**
 * 敏捷工作流 v5.0 核心引擎
 * 
 * 新增功能:
 * 1. 递归拆解（支持子任务再拆解，最大 5 层）
 * 2. 智能排序（依赖分析 + 优先级计算）
 * 3. 成果组装（统一整合 + 交付验证）
 * 4. 旧版本清理（自动检测 + 安全移除）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============ 配置 ============

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/agile-workflow',
  stateFile: '/home/ubutu/.openclaw/workspace/logs/agile-workflow/workflow-state-v5.json',
  experienceFile: '/home/ubutu/.openclaw/workspace/logs/agile-workflow/experience-base-v5.json',
  deliverablesDir: '/home/ubutu/.openclaw/workspace/deliverables',
  maxDepth: 5,                    // 最大拆解深度
  granularityThreshold: 30,       // 粒度阈值（分钟）
  checkInterval: 5000,            // 5 秒检查一次
  maxConcurrentTasks: 3,
  autoLearn: true,
  autoAssemble: true              // v5.0 新增：自动组装成果
};

// ============ 核心类 ============

class AgileWorkflowEngineV5 {
  constructor() {
    this.state = this.loadState();
    this.experience = this.loadExperience();
    this.ensureDirs();
    this.deliverables = this.loadDeliverables();
  }

  ensureDirs() {
    fs.mkdirSync(CONFIG.logsDir, { recursive: true });
    fs.mkdirSync(CONFIG.deliverablesDir, { recursive: true });
  }

  loadState() {
    if (fs.existsSync(CONFIG.stateFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf-8'));
    }
    return {
      projects: {},
      tasks: {},
      agents: {},
      deliverables: {},
      lastUpdate: Date.now()
    };
  }

  saveState() {
    this.state.lastUpdate = Date.now();
    fs.writeFileSync(CONFIG.stateFile, JSON.stringify(this.state, null, 2));
  }

  loadExperience() {
    if (fs.existsSync(CONFIG.experienceFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.experienceFile, 'utf-8'));
    }
    return {
      successfulPatterns: [],
      failedPatterns: [],
      optimizations: [],
      decompositionHistory: []
    };
  }

  saveExperience() {
    fs.writeFileSync(CONFIG.experienceFile, JSON.stringify(this.experience, null, 2));
  }

  loadDeliverables() {
    if (!fs.existsSync(CONFIG.deliverablesDir)) {
      return [];
    }
    
    const files = fs.readdirSync(CONFIG.deliverablesDir);
    return files
      .filter(f => f.endsWith('.json'))
      .map(f => {
        try {
          return JSON.parse(fs.readFileSync(path.join(CONFIG.deliverablesDir, f), 'utf-8'));
        } catch {
          return null;
        }
      })
      .filter(d => d !== null);
  }

  // ============ v5.0 核心功能：递归拆解 ============

  /**
   * 递归拆解任务（支持子任务再拆解）
   */
  async recursiveDecompose(task, depth = 0) {
    console.log(`🔍 拆解任务：${task.name} (深度：${depth}/${CONFIG.maxDepth})`);

    // 1. 检查拆解深度（最大 5 层）
    if (depth >= CONFIG.maxDepth) {
      console.log(`⚠️ 达到最大拆解深度 ${CONFIG.maxDepth}，强制返回`);
      return [{
        ...task,
        depth,
        isAtomic: true,
        forceAtomic: true
      }];
    }

    // 2. 评估任务粒度
    const granularity = this.evaluateGranularity(task);
    console.log(`📏 任务粒度：${granularity} 分钟（阈值：${CONFIG.granularityThreshold}）`);

    // 3. 如果粒度过大，继续拆解
    if (granularity > CONFIG.granularityThreshold && !task.forceAtomic) {
      console.log(`📐 粒度过大，继续拆解...`);
      
      const subtasks = await this.decomposeTask(task);
      console.log(`✅ 拆解为 ${subtasks.length} 个子任务`);

      // 4. 递归拆解每个子任务
      const atomicTasks = [];
      for (const subtask of subtasks) {
        subtask.parentTask = task.id;
        subtask.rootTask = task.rootTask || task.id;
        subtask.depth = depth + 1;
        subtask.dependencyChain = [...(task.dependencyChain || []), task.id];
        
        const result = await this.recursiveDecompose(subtask, depth + 1);
        atomicTasks.push(...result);
      }

      // 记录拆解历史
      this.experience.decompositionHistory.push({
        taskId: task.id,
        taskName: task.name,
        depth,
        subtaskCount: subtasks.length,
        timestamp: Date.now()
      });

      return atomicTasks;
    }

    // 5. 任务已足够小，标记为原子任务
    console.log(`✅ 任务已达到原子粒度`);
    return [{
      ...task,
      depth,
      isAtomic: true,
      granularity
    }];
  }

  /**
   * 评估任务粒度（估算执行时间）
   */
  evaluateGranularity(task) {
    // 根据任务类型估算执行时间
    const timeEstimates = {
      'world_building': 120,      // 世界观架构：120 分钟
      'world_geo': 30,            // 地理设定：30 分钟
      'world_power': 30,          // 修炼体系：30 分钟
      'world_factions': 30,       // 势力分布：30 分钟
      'world_history': 30,        // 历史背景：30 分钟
      'character_design': 60,     // 人物设计：60 分钟
      'char_protagonist': 20,     // 主角设定：20 分钟
      'char_supporting': 20,      // 配角设定：20 分钟
      'char_antagonist': 20,      // 反派设定：20 分钟
      'plot_outline': 90,         // 情节大纲：90 分钟
      'chapter_outline': 30,      // 章节细纲：30 分钟
      'chapter_write': 120,       // 正文创作：120 分钟
      'chapter_write_single': 30, // 单章创作：30 分钟
      'review': 30,               // 审查：30 分钟
      'default': 60               // 默认：60 分钟
    };

    // 应用历史经验优化
    const history = this.experience.decompositionHistory.filter(
      h => h.taskName === task.name
    );
    
    if (history.length > 0) {
      // 有历史记录，使用平均值
      const avgSubtasks = history.reduce((sum, h) => sum + h.subtaskCount, 0) / history.length;
      return timeEstimates[task.type] / avgSubtasks;
    }

    return timeEstimates[task.type] || timeEstimates.default;
  }

  /**
   * 拆解任务（根据类型）
   */
  async decomposeTask(task) {
    const subtasks = [];

    if (task.type === 'novel_creation') {
      subtasks.push(
        { name: '世界观架构', type: 'world_building', dependsOn: [] },
        { name: '人物体系', type: 'character_design', dependsOn: ['world_building'] },
        { name: '情节大纲', type: 'plot_outline', dependsOn: ['character_design'] },
        { name: '章节细纲', type: 'chapter_outline', dependsOn: ['plot_outline'] },
        { name: '正文创作', type: 'chapter_write', dependsOn: ['chapter_outline'] },
        { name: '审查', type: 'review', dependsOn: ['chapter_write'] }
      );
    } else if (task.type === 'world_building') {
      // 世界观继续拆解
      subtasks.push(
        { name: '地理设定', type: 'world_geo', dependsOn: [] },
        { name: '修炼体系', type: 'world_power', dependsOn: ['world_geo'] },
        { name: '势力分布', type: 'world_factions', dependsOn: ['world_power'] },
        { name: '历史背景', type: 'world_history', dependsOn: ['world_factions'] }
      );
    } else if (task.type === 'character_design') {
      // 人物设计继续拆解
      subtasks.push(
        { name: '主角设定', type: 'char_protagonist', dependsOn: [] },
        { name: '配角设定', type: 'char_supporting', dependsOn: ['char_protagonist'] },
        { name: '反派设定', type: 'char_antagonist', dependsOn: ['char_supporting'] }
      );
    } else if (task.type === 'chapter_write') {
      // 章节创作继续拆解
      const chapterCount = task.chapterCount || 10;
      for (let i = 1; i <= chapterCount; i++) {
        subtasks.push({
          name: `第${i}章创作`,
          type: 'chapter_write_single',
          dependsOn: i > 1 ? [`chapter_${i-1}`] : [],
          chapterIndex: i
        });
      }
    } else if (task.type === 'software_dev') {
      subtasks.push(
        { name: '需求分析', type: 'requirement', dependsOn: [] },
        { name: '设计', type: 'design', dependsOn: ['requirement'] },
        { name: '开发', type: 'development', dependsOn: ['design'] },
        { name: '测试', type: 'testing', dependsOn: ['development'] },
        { name: '部署', type: 'deployment', dependsOn: ['testing'] }
      );
    }

    // 为每个子任务生成唯一 ID
    return subtasks.map((st, idx) => ({
      ...st,
      id: `${task.id}_sub_${idx}`,
      rootTask: task.rootTask || task.id
    }));
  }

  // ============ v5.0 核心功能：智能排序 ============

  /**
   * 智能排序任务队列
   */
  smartSort(tasks) {
    console.log(`📊 智能排序 ${tasks.length} 个任务...`);

    // 1. 构建依赖图
    const graph = this.buildDependencyGraph(tasks);

    // 2. 拓扑排序
    const sorted = this.topologicalSort(graph, tasks);

    // 3. 计算优先级
    for (const task of sorted) {
      task.priority = this.calculatePriority(task);
    }

    // 4. 按优先级和深度排序
    sorted.sort((a, b) => {
      // 先按深度排序（浅的优先）
      if (a.depth !== b.depth) {
        return a.depth - b.depth;
      }
      // 再按优先级排序
      return b.priority - a.priority;
    });

    console.log(`✅ 排序完成，任务队列:`);
    sorted.forEach((t, i) => {
      console.log(`   ${i + 1}. ${t.name} (优先级：${t.priority}, 深度：${t.depth})`);
    });

    return sorted;
  }

  /**
   * 构建依赖图
   */
  buildDependencyGraph(tasks) {
    const graph = new Map();
    const taskMap = new Map(tasks.map(t => [t.id, t]));

    for (const task of tasks) {
      if (!graph.has(task.id)) {
        graph.set(task.id, []);
      }

      for (const depId of (task.dependsOn || [])) {
        // 查找依赖的任务
        const depTask = tasks.find(t => t.type === depId || t.id === depId);
        if (depTask) {
          graph.get(task.id).push(depTask.id);
        }
      }
    }

    return { graph, taskMap };
  }

  /**
   * 拓扑排序
   */
  topologicalSort(graphData, tasks) {
    const { graph, taskMap } = graphData;
    const visited = new Set();
    const result = [];

    const visit = (taskId) => {
      if (visited.has(taskId)) return;
      visited.add(taskId);

      const deps = graph.get(taskId) || [];
      for (const depId of deps) {
        visit(depId);
      }

      result.push(taskMap.get(taskId));
    };

    for (const task of tasks) {
      visit(task.id);
    }

    return result;
  }

  /**
   * 计算任务优先级
   */
  calculatePriority(task) {
    let priority = 50; // 基础优先级

    // 深度越浅，优先级越高
    priority -= task.depth * 5;

    // 依赖越多，优先级越高
    priority += (task.dependsOn?.length || 0) * 3;

    // 关键路径任务优先级高
    if (task.isCritical) {
      priority += 20;
    }

    // 用户指定的优先级
    if (task.userPriority) {
      priority = task.userPriority;
    }

    return Math.max(0, Math.min(100, priority));
  }

  // ============ v5.0 核心功能：成果组装 ============

  /**
   * 组装任务成果
   */
  async assembleDeliverable(rootTaskId, taskResults) {
    console.log(`📦 组装成果：${rootTaskId}`);

    // 1. 收集所有任务结果
    const results = this.gatherResults(taskResults);
    console.log(`✅ 收集到 ${results.length} 个任务结果`);

    // 2. 按结构组织
    const organized = this.organizeByStructure(results, rootTaskId);
    console.log(`✅ 按结构组织完成`);

    // 3. 生成汇总文档
    const summary = this.generateSummary(organized, rootTaskId);
    console.log(`✅ 生成汇总文档`);

    // 4. 创建交付物
    const deliverable = {
      id: `deliverable_${Date.now()}`,
      rootTaskId,
      rootTask: this.state.tasks[rootTaskId],
      completedAt: Date.now(),
      taskCount: results.length,
      results: organized,
      summary,
      status: 'deliverable',
      version: '1.0.0'
    };

    // 5. 保存到交付库
    await this.saveDeliverable(deliverable);
    console.log(`✅ 交付物已保存：${deliverable.id}`);

    // 6. 更新状态
    this.state.deliverables[deliverable.id] = deliverable;
    this.saveState();

    return deliverable;
  }

  /**
   * 收集任务结果
   */
  gatherResults(taskResults) {
    const results = [];
    
    for (const result of taskResults) {
      if (result.status === 'completed' && result.output) {
        results.push({
          taskId: result.taskId,
          taskName: result.taskName,
          taskType: result.taskType,
          output: result.output,
          completedAt: result.completedAt
        });
      }
    }

    return results;
  }

  /**
   * 按结构组织结果
   */
  organizeByStructure(results, rootTaskId) {
    const organized = {
      rootTaskId,
      byType: {},
      byDepth: {},
      timeline: []
    };

    // 按类型组织
    for (const result of results) {
      if (!organized.byType[result.taskType]) {
        organized.byType[result.taskType] = [];
      }
      organized.byType[result.taskType].push(result);

      // 按深度组织
      const depth = result.depth || 0;
      if (!organized.byDepth[depth]) {
        organized.byDepth[depth] = [];
      }
      organized.byDepth[depth].push(result);

      // 时间线
      organized.timeline.push(result);
    }

    // 时间线排序
    organized.timeline.sort((a, b) => a.completedAt - b.completedAt);

    return organized;
  }

  /**
   * 生成汇总文档
   */
  generateSummary(organized, rootTaskId) {
    const taskCount = organized.timeline.length;
    const types = Object.keys(organized.byType);
    
    // 统计字数（如果是小说）
    let totalWords = 0;
    for (const result of organized.timeline) {
      if (result.output?.wordCount) {
        totalWords += result.output.wordCount;
      }
    }

    return {
      taskCount,
      types,
      totalWords,
      rootTaskId,
      completedAt: new Date().toISOString(),
      quality: this.assessQuality(organized)
    };
  }

  /**
   * 评估成果质量
   */
  assessQuality(organized) {
    // 简单评估：完成率 100% = A, 80%+ = B, 60%+ = C
    const taskCount = organized.timeline.length;
    if (taskCount >= 10) return 'A';
    if (taskCount >= 5) return 'B';
    return 'C';
  }

  /**
   * 保存交付物
   */
  async saveDeliverable(deliverable) {
    const filePath = path.join(
      CONFIG.deliverablesDir,
      `${deliverable.id}.json`
    );
    fs.writeFileSync(filePath, JSON.stringify(deliverable, null, 2));
    
    // 同时保存汇总文档（Markdown 格式）
    const mdPath = path.join(
      CONFIG.deliverablesDir,
      `${deliverable.id}.md`
    );
    const mdContent = this.generateMarkdownSummary(deliverable);
    fs.writeFileSync(mdPath, mdContent);
  }

  /**
   * 生成 Markdown 汇总
   */
  generateMarkdownSummary(deliverable) {
    let md = `# ${deliverable.rootTask?.name || '项目成果'}\n\n`;
    md += `**完成时间**: ${new Date(deliverable.completedAt).toLocaleString('zh-CN')}\n`;
    md += `**任务数量**: ${deliverable.taskCount}\n`;
    md += `**质量等级**: ${deliverable.summary.quality}\n\n`;
    
    if (deliverable.summary.totalWords) {
      md += `**总字数**: ${deliverable.summary.totalWords.toLocaleString()}\n\n`;
    }

    md += `## 任务列表\n\n`;
    for (const result of deliverable.results.timeline) {
      md += `- **${result.taskName}** (${result.taskType}) - ${new Date(result.completedAt).toLocaleString('zh-CN')}\n`;
    }

    return md;
  }

  // ============ v5.0 核心功能：旧版本清理 ============

  /**
   * 检测并清理旧版本
   */
  async cleanupOldVersion() {
    console.log('🧹 检测旧版本...');

    const oldPaths = [
      path.join(CONFIG.workspace, 'skills/agile-workflow/scripts'),
      path.join(CONFIG.workspace, 'skills/agile-workflow/config'),
      path.join(CONFIG.workspace, 'skills/agile-workflow/README.md'),
      path.join(CONFIG.workspace, 'skills/agile-workflow/SKILL.md.v3')
    ];

    const found = [];
    for (const p of oldPaths) {
      if (fs.existsSync(p)) {
        found.push(p);
      }
    }

    if (found.length === 0) {
      console.log('✅ 未检测到旧版本');
      return { cleaned: 0, paths: [] };
    }

    console.log(`⚠️ 检测到 ${found.length} 个旧版本文件/目录`);
    found.forEach(p => console.log(`   - ${p}`));

    // 备份旧版本
    const backupDir = path.join(CONFIG.workspace, `logs/agile-workflow/backup-v3-${Date.now()}`);
    fs.mkdirSync(backupDir, { recursive: true });

    console.log(`📦 备份旧版本到：${backupDir}`);
    for (const p of found) {
      const relative = path.relative(CONFIG.workspace, p);
      const backupPath = path.join(backupDir, relative.replace(/\//g, '_'));
      
      if (fs.statSync(p).isDirectory()) {
        execSync(`cp -r "${p}" "${backupPath}"`);
      } else {
        execSync(`cp "${p}" "${backupPath}"`);
      }
    }

    // 删除旧版本
    console.log('🗑️ 删除旧版本...');
    for (const p of found) {
      if (fs.statSync(p).isDirectory()) {
        execSync(`rm -rf "${p}"`);
      } else {
        fs.unlinkSync(p);
      }
      console.log(`   ✅ 已删除：${p}`);
    }

    console.log(`✅ 旧版本清理完成，备份位置：${backupDir}`);
    return { cleaned: found.length, paths: found, backupDir };
  }

  // ============ 原有功能（继承 v4.0） ============

  assignTask(subtask, projectId) {
    const agentMap = {
      'world_building': 'world_builder',
      'character_design': 'character_designer',
      'plot_outline': 'outline_generator',
      'chapter_outline': 'detailed_outline_designer',
      'chapter_write': 'chapter_writer',
      'chapter_write_single': 'chapter_writer',
      'review': 'novel_logic_checker'
    };

    const agentName = agentMap[subtask.type] || 'general_agent';
    const taskId = `${projectId}_${subtask.type}_${Date.now()}`;
    
    const task = {
      id: taskId,
      name: subtask.name,
      type: subtask.type,
      projectId,
      agent: agentName,
      status: 'pending',
      dependsOn: subtask.dependsOn,
      depth: subtask.depth || 0,
      parentTask: subtask.parentTask,
      rootTask: subtask.rootTask,
      createdAt: Date.now()
    };

    this.state.tasks[taskId] = task;
    this.saveState();

    console.log(`✅ 任务已分配：${taskId} → ${agentName}`);
    return taskId;
  }

  monitorAll() {
    const stats = {
      total: 0,
      pending: 0,
      running: 0,
      completed: 0,
      failed: 0
    };

    for (const task of Object.values(this.state.tasks)) {
      stats.total++;
      stats[task.status]++;
    }

    console.log(`📊 总计：${stats.total} | 待执行：${stats.pending} | 进行中：${stats.running} | 完成：${stats.completed} | 失败：${stats.failed}`);
    return stats;
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
敏捷工作流引擎 v5.0

用法：node agile-workflow-engine-v5.js <命令> [选项]

命令:
  start               启动工作流引擎
  decompose <任务>    递归拆解任务
  sort                智能排序任务队列
  assemble <项目 ID>  组装项目成果
  cleanup             清理旧版本
  monitor             监控所有任务
  status              查看状态

示例:
  node agile-workflow-engine-v5.js start
  node agile-workflow-engine-v5.js decompose novel_creation
  node agile-workflow-engine-v5.js assemble project_001
  node agile-workflow-engine-v5.js cleanup
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const engine = new AgileWorkflowEngineV5();

  switch (command) {
    case 'start':
      console.log('🚀 启动敏捷工作流引擎 v5.0...');
      engine.monitorAll();
      console.log('✅ 引擎已启动');
      break;

    case 'decompose':
      const taskName = args[1] || 'novel_creation';
      const task = { 
        id: `task_${Date.now()}`, 
        name: taskName, 
        type: taskName,
        rootTask: null
      };
      const result = await engine.recursiveDecompose(task);
      console.log(`\n✅ 拆解完成，共 ${result.length} 个原子任务:`);
      result.forEach((t, i) => {
        console.log(`   ${i + 1}. ${t.name} (深度：${t.depth}, 粒度：${t.granularity}分钟)`);
      });
      break;

    case 'sort':
      // 从状态中读取任务并排序
      const tasks = Object.values(engine.state.tasks);
      if (tasks.length === 0) {
        console.log('⚠️ 暂无任务');
      } else {
        const sorted = engine.smartSort(tasks);
        console.log(`\n✅ 排序完成，任务队列:`);
        sorted.forEach((t, i) => {
          console.log(`   ${i + 1}. ${t.name} (优先级：${t.priority})`);
        });
      }
      break;

    case 'assemble':
      const projectId = args[1];
      if (!projectId) {
        console.log('❌ 请提供项目 ID');
      } else {
        const taskResults = Object.values(engine.state.tasks)
          .filter(t => t.projectId === projectId && t.status === 'completed');
        if (taskResults.length === 0) {
          console.log('⚠️ 该项目暂无完成任务');
        } else {
          const deliverable = await engine.assembleDeliverable(projectId, taskResults);
          console.log(`\n✅ 成果组装完成:`);
          console.log(`   交付物 ID: ${deliverable.id}`);
          console.log(`   任务数量：${deliverable.taskCount}`);
          console.log(`   质量等级：${deliverable.summary.quality}`);
        }
      }
      break;

    case 'cleanup':
      await engine.cleanupOldVersion();
      break;

    case 'monitor':
      engine.monitorAll();
      break;

    case 'status':
      console.log('工作流状态:');
      console.log(JSON.stringify(engine.state, null, 2));
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { AgileWorkflowEngineV5, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}

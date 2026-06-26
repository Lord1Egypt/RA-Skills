#!/usr/bin/env node

/**
 * 学习方向生成器 - 自主发现新学习方向并生成任务
 * 
 * 功能：
 * 1. 分析当前能力差距
 * 2. 基于反思报告生成新任务
 * 3. 集成 find-skills 发现社区技能
 * 4. 集成 clawhub 发现新技能
 * 5. 自动添加到任务队列
 * 
 * 用法：
 *   node learning-direction.js [command]
 *   
 * 命令：
 *   analyze     - 分析能力差距
 *   discover    - 发现新技能（find-skills + clawhub）
 *   generate    - 生成新学习任务
 *   auto        - 完整流程：分析→发现→生成→添加
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const QUEUE_PATH = path.join(WORKSPACE, 'tasks/queue.json');
const PATTERNS_PATH = path.join(WORKSPACE, 'instincts/patterns.jsonl');
const REFLECTIONS_DIR = path.join(WORKSPACE, 'memory/reflections');
const SKILL_MASTERY_PATH = path.join(WORKSPACE, 'skill-mastery-plan.md');

/**
 * 加载任务队列
 */
function loadQueue() {
  try {
    const data = fs.readFileSync(QUEUE_PATH, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return null;
  }
}

/**
 * 保存任务队列
 */
function saveQueue(queue) {
  fs.writeFileSync(QUEUE_PATH, JSON.stringify(queue, null, 2));
}

/**
 * 加载所有模式
 */
function loadPatterns() {
  if (!fs.existsSync(PATTERNS_PATH)) {
    return [];
  }
  const content = fs.readFileSync(PATTERNS_PATH, 'utf-8');
  const lines = content.trim().split('\n').filter(line => line.trim());
  return lines.map(line => {
    try {
      return JSON.parse(line);
    } catch (error) {
      return null;
    }
  }).filter(p => p !== null);
}

/**
 * 加载最新反思报告
 */
function loadLatestReflection() {
  try {
    const files = fs.readdirSync(REFLECTIONS_DIR)
      .filter(f => f.startsWith('daily-'))
      .sort()
      .reverse();
    
    if (files.length === 0) {
      return null;
    }
    
    const content = fs.readFileSync(path.join(REFLECTIONS_DIR, files[0]), 'utf-8');
    return {
      file: files[0],
      content: content
    };
  } catch (error) {
    return null;
  }
}

/**
 * 分析能力差距
 */
function analyzeCapabilityGaps() {
  console.log('\n🔍 分析能力差距...\n');
  
  const queue = loadQueue();
  const patterns = loadPatterns();
  
  if (!queue) {
    console.error('❌ 无法加载任务队列');
    return [];
  }
  
  const gaps = [];
  
  // 1. 基于任务队列分析
  const pendingP0 = queue.tasks.filter(t => t.status === 'pending' && t.priority === 'P0');
  if (pendingP0.length > 0) {
    gaps.push({
      type: 'pending_task',
      priority: 'high',
      category: 'task',
      description: `有 ${pendingP0.length} 个 P0 任务待完成`,
      suggestion: `优先完成：${pendingP0[0].title}`,
      taskId: pendingP0[0].id
    });
  }
  
  // 2. 基于模式分类分析
  const categoryCount = {};
  patterns.forEach(p => {
    const category = p.category || 'general';
    categoryCount[category] = (categoryCount[category] || 0) + 1;
  });
  
  const expectedMin = 3; // 每个领域至少 3 个模式
  Object.entries(categoryCount).forEach(([category, count]) => {
    if (count < expectedMin) {
      gaps.push({
        type: 'weak_category',
        priority: 'medium',
        category: category,
        description: `${category}领域只有${count}个模式（建议${expectedMin}+）`,
        suggestion: `加强${category}领域学习，积累更多模式`
      });
    }
  });
  
  // 3. 基于自信度分析
  const lowConfidence = patterns.filter(p => p.confidence < 0.4);
  if (lowConfidence.length > 0) {
    gaps.push({
      type: 'low_confidence',
      priority: 'medium',
      category: 'confidence',
      description: `有 ${lowConfidence.length} 个低自信模式`,
      suggestion: '通过实践验证低自信模式，提升可靠性'
    });
  }
  
  // 4. 基于技能创建分析
  const notConverted = patterns.filter(p => p.confidence >= 0.7 && !p.convertedToSkill);
  if (notConverted.length > 0) {
    gaps.push({
      type: 'skill_creation',
      priority: 'high',
      category: 'skill',
      description: `有 ${notConverted.length} 个高自信模式未转化为技能`,
      suggestion: '将高自信模式转化为可复用技能'
    });
  }
  
  // 5. 基于技能熟练度分析（从 skill-mastery-plan.md 读取）
  if (fs.existsSync(SKILL_MASTERY_PATH)) {
    const content = fs.readFileSync(SKILL_MASTERY_PATH, 'utf-8');
    const zeroUseSkills = content.match(/`(\w+)`.*⭐/g) || [];
    if (zeroUseSkills.length > 0) {
      gaps.push({
        type: 'skill_practice',
        priority: 'low',
        category: 'practice',
        description: `有 ${zeroUseSkills.length} 个技能使用次数为 0`,
        suggestion: '练习未使用的技能，提升熟练度'
      });
    }
  }
  
  console.log(`📊 发现 ${gaps.length} 个能力差距:\n`);
  
  gaps.forEach((gap, i) => {
    const priorityIcon = gap.priority === 'high' ? '🔴' : gap.priority === 'medium' ? '🟡' : '🟢';
    console.log(`${i + 1}. ${priorityIcon} [${gap.category}] ${gap.description}`);
    console.log(`   建议：${gap.suggestion}`);
    console.log('');
  });
  
  return gaps;
}

/**
 * 发现新技能（find-skills + clawhub）
 */
function discoverNewSkills() {
  console.log('\n🔍 发现新技能...\n');
  
  const discoveries = [];
  
  // 基于当前任务队列分析需要的技能
  const queue = loadQueue();
  if (queue) {
    const categories = [...new Set(queue.tasks.map(t => t.category || 'general'))];
    
    categories.forEach(category => {
      // 搜索相关技能
      try {
        console.log(`   搜索 "${category}" 相关技能...`);
        const result = execSync(`npx skills find ${category}`, {
          cwd: WORKSPACE,
          encoding: 'utf-8',
          stdio: ['pipe', 'pipe', 'ignore']
        });
        
        if (result.trim()) {
          const skills = parseSkillsOutput(result);
          if (skills.length > 0) {
            discoveries.push({
              source: 'find-skills',
              category: category,
              skills: skills.slice(0, 3) // 只取前 3 个
            });
          }
        }
      } catch (error) {
        // 忽略错误，继续下一个
      }
    });
  }
  
  // 搜索通用 automation 技能
  try {
    console.log('   搜索 "automation" 相关技能...');
    const result = execSync(`npx skills find automation`, {
      cwd: WORKSPACE,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    });
    
    if (result.trim()) {
      const skills = parseSkillsOutput(result);
      if (skills.length > 0) {
        discoveries.push({
          source: 'find-skills',
          category: 'automation',
          skills: skills.slice(0, 3)
        });
      }
    }
  } catch (error) {
    // 忽略错误
  }
  
  console.log(`\n📊 发现 ${discoveries.length} 个技能来源:\n`);
  
  discoveries.forEach((disc, i) => {
    console.log(`${i + 1}. ${disc.source} - ${disc.category}`);
    disc.skills.forEach(skill => {
      console.log(`   - ${skill.name} (${skill.installs})`);
    });
    console.log('');
  });
  
  return discoveries;
}

/**
 * 解析 find-skills 输出
 */
function parseSkillsOutput(output) {
  const skills = [];
  const lines = output.split('\n');
  
  for (const line of lines) {
    if (line.includes('@')) {
      const match = line.match(/(\S+@\S+)/);
      if (match) {
        skills.push({
          name: match[1],
          installs: 'unknown'
        });
      }
    }
  }
  
  return skills;
}

/**
 * 生成新学习任务
 */
function generateLearningTasks(gaps, discoveries) {
  console.log('\n📝 生成新学习任务...\n');
  
  const tasks = [];
  
  // 1. 基于能力差距生成任务
  gaps.forEach(gap => {
    if (gap.priority === 'high' || gap.priority === 'medium') {
      tasks.push({
        id: `task_auto_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        title: gap.suggestion,
        description: gap.description,
        priority: gap.priority === 'high' ? 'P0' : 'P1',
        status: 'pending',
        phase: 'Auto-Generated',
        dependencies: gap.taskId ? [gap.taskId] : [],
        estimatedMinutes: 30,
        createdAt: new Date().toISOString(),
        tags: ['auto-generated', gap.category],
        source: 'capability-gap'
      });
    }
  });
  
  // 2. 基于技能发现生成任务
  discoveries.forEach(disc => {
    disc.skills.forEach(skill => {
      tasks.push({
        id: `task_auto_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        title: `学习并安装技能：${skill.name}`,
        description: `从${disc.source}发现的${disc.category}相关技能`,
        priority: 'P2',
        status: 'pending',
        phase: 'Auto-Generated',
        dependencies: [],
        estimatedMinutes: 20,
        createdAt: new Date().toISOString(),
        tags: ['auto-generated', 'skill-discovery', disc.category],
        source: 'skill-discovery',
        skillName: skill.name
      });
    });
  });
  
  console.log(`📊 生成 ${tasks.length} 个新任务:\n`);
  
  tasks.forEach((task, i) => {
    console.log(`${i + 1}. [${task.priority}] ${task.title}`);
    console.log(`   描述：${task.description}`);
    console.log(`   来源：${task.source}`);
    console.log('');
  });
  
  return tasks;
}

/**
 * 添加任务到队列
 */
function addTasksToQueue(tasks) {
  console.log('\n📥 添加任务到队列...\n');
  
  const queue = loadQueue();
  if (!queue) {
    console.error('❌ 无法加载任务队列');
    return 0;
  }
  
  let addedCount = 0;
  
  tasks.forEach(task => {
    // 检查是否已存在类似任务
    const exists = queue.tasks.some(t => 
      t.title === task.title || 
      (t.description && task.description && t.description.includes(task.description.substring(0, 20)))
    );
    
    if (!exists) {
      queue.tasks.push(task);
      addedCount++;
      console.log(`✅ 添加：${task.title}`);
    } else {
      console.log(`⏭️  跳过（已存在）：${task.title}`);
    }
  });
  
  // 更新统计
  queue.stats.totalTasks = queue.tasks.length;
  queue.stats.pendingTasks = queue.tasks.filter(t => t.status === 'pending').length;
  
  saveQueue(queue);
  
  console.log(`\n📊 成功添加 ${addedCount}/${tasks.length} 个任务`);
  console.log(`📊 当前队列：${queue.stats.totalTasks} 个任务，${queue.stats.pendingTasks} 个待办\n`);
  
  return addedCount;
}

/**
 * 完整流程
 */
function autoGenerateLearningDirection() {
  console.log('\n🚀 开始自动生成学习方向...\n');
  console.log('═'.repeat(60));
  
  // Step 1: 分析能力差距
  const gaps = analyzeCapabilityGaps();
  console.log('═'.repeat(60));
  
  // Step 2: 发现新技能
  const discoveries = discoverNewSkills();
  console.log('═'.repeat(60));
  
  // Step 3: 生成新任务
  const tasks = generateLearningTasks(gaps, discoveries);
  console.log('═'.repeat(60));
  
  // Step 4: 添加到队列
  const added = addTasksToQueue(tasks);
  console.log('═'.repeat(60));
  
  // 总结
  console.log('\n✅ 学习方向生成完成！\n');
  console.log(`📊 能力差距：${gaps.length} 个`);
  console.log(`📊 技能发现：${discoveries.length} 个来源`);
  console.log(`📊 生成任务：${tasks.length} 个`);
  console.log(`📊 成功添加：${added} 个\n`);
  
  if (added > 0) {
    console.log('🎯 下一步：');
    console.log('   运行 node autonomous/evolution-engine.js run');
    console.log('   系统将自主选择新任务执行！\n');
  }
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'auto';
  
  // 确保反思目录存在
  if (!fs.existsSync(REFLECTIONS_DIR)) {
    fs.mkdirSync(REFLECTIONS_DIR, { recursive: true });
  }
  
  switch (command) {
    case 'analyze':
      analyzeCapabilityGaps();
      break;
    case 'discover':
      discoverNewSkills();
      break;
    case 'generate':
      const gaps = analyzeCapabilityGaps();
      const discoveries = discoverNewSkills();
      generateLearningTasks(gaps, discoveries);
      break;
    case 'auto':
      autoGenerateLearningDirection();
      break;
    default:
      console.log('用法：node learning-direction.js [command]');
      console.log('\n命令:');
      console.log('  analyze    - 分析能力差距');
      console.log('  discover   - 发现新技能（find-skills + clawhub）');
      console.log('  generate   - 生成新学习任务');
      console.log('  auto       - 完整流程：分析→发现→生成→添加');
  }
}

// 运行主函数
main().catch(error => {
  console.error('❌ 学习方向生成器错误:', error.message);
  console.error(error.stack);
  process.exit(1);
});

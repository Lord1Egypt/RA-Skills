#!/usr/bin/env node
/**
 * 任务依赖生成器 v1.0
 * 
 * 核心逻辑：
 * 1. 细纲任务串行：outline_N 依赖 outline_{N-1}
 * 2. 正文任务只依赖细纲：write_N 依赖 outline_N（不依赖 write_{N-1}）
 * 
 * 效果：
 * - outline_01 完成后 → outline_02 可开始 + write_01 可开始（并行）
 * - outline_02 完成后 → outline_03 可开始 + write_02 可开始（并行）
 * - 实现流水线并行：细纲和正文同时进行
 */

const fs = require('fs');
const path = require('path');

/**
 * 生成细纲和正文的任务依赖
 * @param {number} totalChapters - 总章节数
 * @param {object} options - 配置选项
 * @returns {object} 依赖配置对象
 */
function generateDependencies(totalChapters, options = {}) {
  const {
    outlinePrefix = 'outline',    // 细纲任务前缀
    writePrefix = 'write',        // 正文任务前缀
    enableReview = false,         // 是否启用审查任务
    reviewPrefix = 'review'       // 审查任务前缀
  } = options;

  const dependencies = {};

  // 1. 细纲任务链（串行）
  for (let i = 1; i <= totalChapters; i++) {
    const taskId = `${outlinePrefix}_${String(i).padStart(2, '0')}`;
    
    if (i === 1) {
      // 第一章细纲无依赖
      dependencies[taskId] = [];
    } else {
      // 后续章节细纲依赖前一章细纲
      const prevTaskId = `${outlinePrefix}_${String(i - 1).padStart(2, '0')}`;
      dependencies[taskId] = [prevTaskId];
    }
  }

  // 2. 正文任务链（只依赖细纲，不依赖正文）
  for (let i = 1; i <= totalChapters; i++) {
    const taskId = `${writePrefix}_${String(i).padStart(2, '0')}`;
    const outlineTaskId = `${outlinePrefix}_${String(i).padStart(2, '0')}`;
    
    // 正文只依赖对应章节的细纲
    dependencies[taskId] = [outlineTaskId];
  }

  // 3. 审查任务（可选，依赖正文）
  if (enableReview) {
    for (let i = 1; i <= totalChapters; i++) {
      const taskId = `${reviewPrefix}_${String(i).padStart(2, '0')}`;
      const writeTaskId = `${writePrefix}_${String(i).padStart(2, '0')}`;
      
      dependencies[taskId] = [writeTaskId];
    }
  }

  return dependencies;
}

/**
 * 生成任务状态文件
 * @param {number} totalChapters - 总章节数
 * @param {object} options - 配置选项
 * @returns {object} 任务状态对象
 */
function generateTaskStates(totalChapters, options = {}) {
  const {
    outlinePrefix = 'outline',
    writePrefix = 'write',
    enableReview = false,
    reviewPrefix = 'review',
    projectDir = '/path/to/project',
    chapterTitles = [],  // 章节标题数组
    agentMapping = {
      outline: 'novel_architect',
      write: 'novel_writer',
      review: 'novel_editor'
    }
  } = options;

  const tasks = {};

  // 1. 细纲任务
  for (let i = 1; i <= totalChapters; i++) {
    const taskId = `${outlinePrefix}_${String(i).padStart(2, '0')}`;
    const chapterTitle = chapterTitles[i - 1] || `第${i}章`;
    
    tasks[taskId] = {
      id: taskId,
      name: `第${i}章_细纲_${chapterTitle}`,
      chapter: i,
      type: 'outline',
      status: 'pending',
      agent: agentMapping.outline,
      created_at: new Date().toISOString(),
      output: `${projectDir}/04_章节细纲/第${String(i).padStart(2, '0')}章_${chapterTitle}.md`
    };
  }

  // 2. 正文任务
  for (let i = 1; i <= totalChapters; i++) {
    const taskId = `${writePrefix}_${String(i).padStart(2, '0')}`;
    const chapterTitle = chapterTitles[i - 1] || `第${i}章`;
    
    tasks[taskId] = {
      id: taskId,
      name: `第${i}章_正文_${chapterTitle}`,
      chapter: i,
      type: 'writing',
      status: 'pending',
      agent: agentMapping.write,
      created_at: new Date().toISOString(),
      output: `${projectDir}/05_正文创作/第${String(i).padStart(2, '0')}章_${chapterTitle}.md`
    };
  }

  // 3. 审查任务
  if (enableReview) {
    for (let i = 1; i <= totalChapters; i++) {
      const taskId = `${reviewPrefix}_${String(i).padStart(2, '0')}`;
      const chapterTitle = chapterTitles[i - 1] || `第${i}章`;
      
      tasks[taskId] = {
        id: taskId,
        name: `第${i}章_审查_${chapterTitle}`,
        chapter: i,
        type: 'review',
        status: 'pending',
        agent: agentMapping.review,
        created_at: new Date().toISOString(),
        input: `${projectDir}/05_正文创作/第${String(i).padStart(2, '0')}章_${chapterTitle}.md`,
        output: `${projectDir}/05_正文创作/第${String(i).padStart(2, '0')}章_${chapterTitle}_润色版.md`
      };
    }
  }

  return tasks;
}

/**
 * 从现有项目提取章节标题
 */
function extractChapterTitles(projectDir) {
  const outlineDir = path.join(projectDir, '04_章节细纲');
  const titles = [];
  
  if (fs.existsSync(outlineDir)) {
    const files = fs.readdirSync(outlineDir)
      .filter(f => f.endsWith('.md'))
      .sort();
    
    for (const file of files) {
      const match = file.match(/第(\d+)章_(.+)\.md/);
      if (match) {
        titles.push(match[2]);
      }
    }
  }
  
  return titles;
}

/**
 * 写入配置文件
 */
function writeConfigFiles(projectDir, dependencies, tasks) {
  const depsPath = path.join(projectDir, '.task-dependencies.json');
  const statePath = path.join(projectDir, '.task-state.json');
  
  // 备份现有文件
  if (fs.existsSync(depsPath)) {
    fs.copyFileSync(depsPath, depsPath + '.backup');
  }
  if (fs.existsSync(statePath)) {
    fs.copyFileSync(statePath, statePath + '.backup');
  }
  
  // 写入新配置
  fs.writeFileSync(depsPath, JSON.stringify(dependencies, null, 2), 'utf8');
  fs.writeFileSync(statePath, JSON.stringify(tasks, null, 2), 'utf8');
  
  console.log(`✅ 已写入依赖配置：${depsPath}`);
  console.log(`✅ 已写入任务状态：${statePath}`);
}

/**
 * 打印依赖图（ASCII 图）
 */
function printDependencyGraph(dependencies, totalChapters) {
  console.log('\n📊 依赖关系图：\n');
  console.log('细纲任务链（串行）：');
  
  let outlineChain = '';
  for (let i = 1; i <= totalChapters; i++) {
    const taskId = `outline_${String(i).padStart(2, '0')}`;
    outlineChain += `[${taskId}]`;
    if (i < totalChapters) {
      outlineChain += ' → ';
    }
  }
  console.log(`  ${outlineChain}`);
  
  console.log('\n正文任务链（只依赖细纲，不依赖正文）：');
  for (let i = 1; i <= totalChapters; i++) {
    const outlineId = `outline_${String(i).padStart(2, '0')}`;
    const writeId = `write_${String(i).padStart(2, '0')}`;
    console.log(`  [${outlineId}] → [${writeId}]`);
  }
  
  console.log('\n💡 并行执行效果：');
  console.log('  outline_01 完成 → outline_02 可开始 + write_01 可开始（并行）');
  console.log('  outline_02 完成 → outline_03 可开始 + write_02 可开始（并行）');
  console.log('  实现：细纲和正文同时进行（流水线并行）\n');
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('用法: node task-dependency-generator.js <项目目录> <总章节数> [选项JSON]');
    console.log('');
    console.log('示例:');
    console.log('  node task-dependency-generator.js /path/to/project 11');
    console.log('  node task-dependency-generator.js /path/to/project 11 \'{"enableReview":true}\'');
    console.log('');
    console.log('选项:');
    console.log('  enableReview: true/false - 是否启用审查任务');
    console.log('  write: true/false - 是否写入配置文件');
    process.exit(1);
  }

  const projectDir = args[0];
  const totalChapters = parseInt(args[1], 10);
  const optionsJson = args[2] || '{}';
  
  let options;
  try {
    options = JSON.parse(optionsJson);
  } catch (e) {
    console.error('❌ 选项 JSON 解析失败:', e.message);
    process.exit(1);
  }

  // 提取章节标题
  const chapterTitles = extractChapterTitles(projectDir);
  if (chapterTitles.length > 0) {
    console.log(`📚 从项目中提取了 ${chapterTitles.length} 个章节标题`);
    options.chapterTitles = chapterTitles;
  }
  
  options.projectDir = projectDir;

  // 生成依赖和任务
  const dependencies = generateDependencies(totalChapters, options);
  const tasks = generateTaskStates(totalChapters, options);

  // 打印依赖图
  printDependencyGraph(dependencies, totalChapters);

  // 写入配置文件
  if (options.write !== false) {
    writeConfigFiles(projectDir, dependencies, tasks);
  }

  // 输出 JSON（可选）
  if (options.outputJson) {
    console.log('\n📄 依赖配置 JSON：');
    console.log(JSON.stringify(dependencies, null, 2));
    console.log('\n📄 任务状态 JSON：');
    console.log(JSON.stringify(tasks, null, 2));
  }
}

module.exports = {
  generateDependencies,
  generateTaskStates,
  printDependencyGraph,
  extractChapterTitles,
  writeConfigFiles
};
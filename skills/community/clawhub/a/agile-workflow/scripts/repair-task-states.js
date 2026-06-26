#!/usr/bin/env node
/**
 * 任务状态修复脚本 v1.0
 * 
 * 功能：
 * 1. 重新生成细纲和正文任务（细纲串行、正文只依赖细纲）
 * 2. 保留已完成的正文任务状态
 * 3. 为现有正文补充细纲任务
 */

const fs = require('fs');
const path = require('path');

const PROJECT_DIR = '/home/ubutu/.openclaw/workspace/novel_architect/novel_reconstruction/山海诡秘_2026_03_08';

/**
 * 扫描现有正文文件
 */
function scanExistingWritings(projectDir) {
  const writingDir = path.join(projectDir, '05_正文创作');
  const chapters = [];
  
  if (!fs.existsSync(writingDir)) {
    console.log(`⚠️ 正文目录不存在：${writingDir}`);
    return chapters;
  }
  
  // 扫描卷一和卷二
  const volumes = ['卷一', '卷二'];
  
  for (const volume of volumes) {
    const volumeDir = path.join(writingDir, volume);
    if (!fs.existsSync(volumeDir)) continue;
    
    const files = fs.readdirSync(volumeDir)
      .filter(f => f.endsWith('.md') && !f.includes('_润色版'));
    
    for (const file of files) {
      const match = file.match(/第\s*(\d+)\s*章_(.+)\.md/);
      if (match) {
        const chapterNum = parseInt(match[1], 10);
        const chapterTitle = match[2];
        const filePath = path.join(volumeDir, file);
        const stat = fs.statSync(filePath);
        
        chapters.push({
          chapter: chapterNum,
          title: chapterTitle,
          volume: volume,
          file: file,
          path: filePath,
          mtime: stat.mtime,
          size: stat.size
        });
      }
    }
  }
  
  return chapters;
}

/**
 * 生成新的任务状态
 */
function generateNewTaskStates(chapters, projectDir) {
  const tasks = {};
  
  // 按章节号排序
  const sortedChapters = chapters.sort((a, b) => a.chapter - b.chapter);
  
  // 去重（同一章节可能有卷一和卷二两个版本）
  const uniqueChapters = [];
  const seenChapters = new Set();
  
  for (const ch of sortedChapters) {
    if (!seenChapters.has(ch.chapter)) {
      seenChapters.add(ch.chapter);
      uniqueChapters.push(ch);
    }
  }
  
  console.log(`📚 发现 ${uniqueChapters.length} 个唯一章节`);
  
  // 生成细纲任务（全部 pending，因为细纲文件不存在）
  for (const ch of uniqueChapters) {
    const outlineTaskId = `outline_${String(ch.chapter).padStart(2, '0')}`;
    
    tasks[outlineTaskId] = {
      id: outlineTaskId,
      name: `第${ch.chapter}章_细纲_${ch.title}`,
      chapter: ch.chapter,
      type: 'outline',
      status: 'pending',
      agent: 'novel_architect',
      created_at: new Date().toISOString(),
      output: `${projectDir}/04_章节细纲/第${String(ch.chapter).padStart(2, '0')}章_${ch.title}.md`
    };
  }
  
  // 生成正文任务（已完成）
  for (const ch of uniqueChapters) {
    const writeTaskId = `write_${String(ch.chapter).padStart(2, '0')}`;
    
    tasks[writeTaskId] = {
      id: writeTaskId,
      name: `第${ch.chapter}章_正文_${ch.title}`,
      chapter: ch.chapter,
      type: 'writing',
      status: 'completed',
      agent: 'novel_writer',
      created_at: new Date().toISOString(),
      completed_at: ch.mtime.toISOString(),
      output: ch.path
    };
  }
  
  return tasks;
}

/**
 * 生成新的依赖配置
 */
function generateNewDependencies(chapters) {
  const dependencies = {};
  
  // 去重
  const uniqueChapters = [];
  const seenChapters = new Set();
  
  for (const ch of chapters) {
    if (!seenChapters.has(ch.chapter)) {
      seenChapters.add(ch.chapter);
      uniqueChapters.push(ch);
    }
  }
  
  uniqueChapters.sort((a, b) => a.chapter - b.chapter);
  
  // 细纲任务链（串行）
  for (let i = 0; i < uniqueChapters.length; i++) {
    const ch = uniqueChapters[i];
    const outlineTaskId = `outline_${String(ch.chapter).padStart(2, '0')}`;
    
    if (i === 0) {
      dependencies[outlineTaskId] = [];
    } else {
      const prevCh = uniqueChapters[i - 1];
      const prevOutlineTaskId = `outline_${String(prevCh.chapter).padStart(2, '0')}`;
      dependencies[outlineTaskId] = [prevOutlineTaskId];
    }
  }
  
  // 正文任务（只依赖细纲）
  for (const ch of uniqueChapters) {
    const writeTaskId = `write_${String(ch.chapter).padStart(2, '0')}`;
    const outlineTaskId = `outline_${String(ch.chapter).padStart(2, '0')}`;
    
    dependencies[writeTaskId] = [outlineTaskId];
  }
  
  return dependencies;
}

/**
 * 打印修复报告
 */
function printRepairReport(tasks, dependencies, chapters) {
  console.log('\n' + '='.repeat(60));
  console.log('📊 任务状态修复报告');
  console.log('='.repeat(60));
  
  // 统计
  const outlineTasks = Object.values(tasks).filter(t => t.type === 'outline');
  const writeTasks = Object.values(tasks).filter(t => t.type === 'writing');
  const completedOutline = outlineTasks.filter(t => t.status === 'completed');
  const completedWrite = writeTasks.filter(t => t.status === 'completed');
  const pendingOutline = outlineTasks.filter(t => t.status === 'pending');
  
  console.log('\n📈 任务统计：');
  console.log(`  细纲任务：${outlineTasks.length} 个`);
  console.log(`    - 已完成：${completedOutline.length} 个`);
  console.log(`    - 待执行：${pendingOutline.length} 个`);
  console.log(`  正文任务：${writeTasks.length} 个`);
  console.log(`    - 已完成：${completedWrite.length} 个`);
  
  console.log('\n📊 依赖关系：');
  console.log('  细纲任务：串行执行（outline_N → outline_{N+1}）');
  console.log('  正文任务：只依赖细纲（write_N 依赖 outline_N）');
  console.log('  并行效果：细纲完成后正文可立即开始');
  
  console.log('\n⚠️ 注意事项：');
  console.log('  1. 细纲任务全部为 pending 状态（细纲文件不存在）');
  console.log('  2. 正文任务已标记为 completed（正文文件已存在）');
  console.log('  3. 需要补充细纲任务以完成完整流程');
  
  console.log('\n💡 建议操作：');
  console.log('  1. 启动调度器：node task-scheduler.js <项目目录> daemon');
  console.log('  2. 监控进度：node task-status.js <项目目录>');
  console.log('  3. 细纲完成后可重新生成正文（如需要）');
  
  console.log('='.repeat(60) + '\n');
}

/**
 * 主函数
 */
function main() {
  console.log('🔧 任务状态修复脚本 v1.0\n');
  
  // 扫描现有正文
  const chapters = scanExistingWritings(PROJECT_DIR);
  
  if (chapters.length === 0) {
    console.log('❌ 未找到正文文件，无法生成任务状态');
    process.exit(1);
  }
  
  console.log(`📚 发现 ${chapters.length} 个正文文件`);
  
  // 生成新的任务状态
  const tasks = generateNewTaskStates(chapters, PROJECT_DIR);
  const dependencies = generateNewDependencies(chapters);
  
  // 打印修复报告
  printRepairReport(tasks, dependencies, chapters);
  
  // 备份现有文件
  const statePath = path.join(PROJECT_DIR, '.task-state.json');
  const depsPath = path.join(PROJECT_DIR, '.task-dependencies.json');
  
  if (fs.existsSync(statePath)) {
    fs.copyFileSync(statePath, statePath + '.backup');
    console.log(`✅ 已备份：${statePath}.backup`);
  }
  
  if (fs.existsSync(depsPath)) {
    fs.copyFileSync(depsPath, depsPath + '.backup');
    console.log(`✅ 已备份：${depsPath}.backup`);
  }
  
  // 写入新配置
  fs.writeFileSync(statePath, JSON.stringify(tasks, null, 2), 'utf8');
  fs.writeFileSync(depsPath, JSON.stringify(dependencies, null, 2), 'utf8');
  
  console.log(`✅ 已写入：${statePath}`);
  console.log(`✅ 已写入：${depsPath}`);
  
  console.log('\n✅ 修复完成！');
}

main();
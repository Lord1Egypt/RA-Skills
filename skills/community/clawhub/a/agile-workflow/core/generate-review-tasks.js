#!/usr/bin/env node
/**
 * 生成审查任务依赖链（100 章）
 * 
 * 修复：添加正确的卷依赖关系
 * - L1 审查：依赖对应章节正文完成
 * - L2 审查：依赖对应卷 L1 审查全部完成
 */

const fs = require('fs');
const path = require('path');

const projectDir = process.argv[2] || __dirname;
const totalChapters = 100;
const chaptersPerVolume = 10;

// 加载现有依赖
const depsFile = path.join(projectDir, '.task-dependencies.json');
let dependencies = {};

if (fs.existsSync(depsFile)) {
  dependencies = JSON.parse(fs.readFileSync(depsFile, 'utf-8'));
  console.log('📊 加载现有 ' + Object.keys(dependencies).length + ' 个任务依赖');
}

// 生成 100 章 L1 审查依赖
console.log('\n🔧 生成 L1 审查任务依赖...');
for (let i = 1; i <= totalChapters; i++) {
  const reviewId = `chapter-${i}-review-l1`;
  
  if (!dependencies[reviewId]) {
    // L1 审查依赖对应章节正文完成
    dependencies[reviewId] = [`chapter-${i}-writing`];
  }
}
console.log('✅ L1 审查任务：' + totalChapters + '个');

// 生成 L2 审查依赖（每 10 章一个）
console.log('\n🔧 生成 L2 审查任务依赖...');
for (let vol = 1; vol <= Math.ceil(totalChapters / chaptersPerVolume); vol++) {
  const startCh = (vol - 1) * chaptersPerVolume + 1;
  const endCh = Math.min(vol * chaptersPerVolume, totalChapters);
  const reviewL2Id = `chapter-${startCh}-${endCh}-review-l2`;
  
  if (!dependencies[reviewL2Id]) {
    // L2 审查依赖对应卷所有 L1 审查完成
    const l1Reviews = [];
    for (let ch = startCh; ch <= endCh; ch++) {
      l1Reviews.push(`chapter-${ch}-review-l1`);
    }
    dependencies[reviewL2Id] = l1Reviews;
  }
}
console.log('✅ L2 审查任务：' + Math.ceil(totalChapters / chaptersPerVolume) + '个');

// 保存依赖文件
fs.writeFileSync(depsFile, JSON.stringify(dependencies, null, 2));
console.log('\n📊 总任务依赖：' + Object.keys(dependencies).length + '个');

// 加载现有状态
const stateFile = path.join(projectDir, '.task-state.json');
let state = {};

if (fs.existsSync(stateFile)) {
  state = JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
  console.log('📊 加载现有 ' + Object.keys(state).length + ' 个任务状态');
}

// 补充审查任务状态
let added = 0;
for (let i = 1; i <= totalChapters; i++) {
  const reviewId = `chapter-${i}-review-l1`;
  
  if (!state[reviewId]) {
    state[reviewId] = {
      status: 'pending',
      agent: 'novel_editor',
      description: `第${i}章 L1 审查（字数/格式/基础逻辑）`,
      dependsOn: dependencies[reviewId],
      createdAt: new Date().toISOString()
    };
    added++;
  }
}

// 补充 L2 审查任务状态
for (let vol = 1; vol <= Math.ceil(totalChapters / chaptersPerVolume); vol++) {
  const startCh = (vol - 1) * chaptersPerVolume + 1;
  const endCh = Math.min(vol * chaptersPerVolume, totalChapters);
  const reviewL2Id = `chapter-${startCh}-${endCh}-review-l2`;
  
  if (!state[reviewL2Id]) {
    state[reviewL2Id] = {
      status: 'pending',
      agent: 'novel_editor',
      description: `第${startCh}-${endCh}章 L2 审查（情节连贯/伏笔）`,
      dependsOn: dependencies[reviewL2Id],
      createdAt: new Date().toISOString()
    };
    added++;
  }
}

// 保存状态文件
fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
console.log('\n✅ 补充 ' + added + ' 个缺失审查任务状态');
console.log('📊 总任务数：' + Object.keys(state).length + '个');

// 验证依赖关系
console.log('\n📋 验证依赖关系:');
const vol1L2Deps = dependencies['chapter-11-20-review-l2'] || [];
console.log('第 11-20 章 L2 审查依赖：' + vol1L2Deps.length + '个 L1 审查');
console.log('  依赖章节：' + vol1L2Deps.map(d => d.replace('chapter-', '').replace('-review-l1', '')).join(', '));

const vol2L2Deps = dependencies['chapter-21-30-review-l2'] || [];
console.log('第 21-30 章 L2 审查依赖：' + vol2L2Deps.length + '个 L1 审查');
console.log('  依赖章节：' + vol2L2Deps.map(d => d.replace('chapter-', '').replace('-review-l1', '')).join(', '));

console.log('\n✅ 审查任务依赖生成完成！');

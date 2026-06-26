/**
 * C 类任务清理工具 · handler.js
 * 
 * 功能：每周日 23:00 自动清理 C 类任务已完成记录
 * 版本：v1.0
 * 创建时间：2026-03-01 21:00
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  cTaskPath: path.join(process.env.HOME, 'Desktop', '任务流', 'C-待办任务池.md'),
  logPath: path.join(process.env.HOME, 'Desktop', '任务流', 'logs'),
  memoryPath: path.join(process.env.HOME, '.openclaw', 'workspace', 'memory', 'c-task-insights.md')
};

// 确保日志目录存在
function ensureLogDirectory() {
  if (!fs.existsSync(CONFIG.logPath)) {
    fs.mkdirSync(CONFIG.logPath, { recursive: true });
  }
}

// 读取 C 类任务池
function readCTaskPool() {
  if (!fs.existsSync(CONFIG.cTaskPath)) {
    console.log('[C 类清理] C 类任务池不存在');
    return null;
  }
  return fs.readFileSync(CONFIG.cTaskPath, 'utf-8');
}

// 解析已完成任务
function parseCompletedTasks(content) {
  const completedSection = content.indexOf('## ✅ 已完成（待清理）');
  if (completedSection === -1) {
    return [];
  }

  const nextSection = content.indexOf('##', completedSection + 1);
  const completedContent = nextSection > 0 
    ? content.substring(completedSection, nextSection) 
    : content.substring(completedSection);

  // 提取表格行
  const lines = completedContent.split('\n');
  const tasks = [];

  for (const line of lines) {
    if (line.startsWith('| C')) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      if (parts.length >= 3) {
        tasks.push({
          id: parts[0],
          content: parts[1],
          completedTime: parts[2],
          cleanupStatus: parts[3] || '待清理'
        });
      }
    }
  }

  return tasks;
}

// 4D 压缩高价值内容
function compressInsights(tasks) {
  const insights = [];
  
  for (const task of tasks) {
    // 简单判断：任务内容包含"洞察"、"学习"、"发现"等关键词
    if (task.content.includes('洞察') || 
        task.content.includes('学习') || 
        task.content.includes('发现') ||
        task.content.includes('Grok') ||
        task.content.includes('技术')) {
      insights.push(`- [${task.completedTime}] ${task.id}: ${task.content}`);
    }
  }

  return insights;
}

// 更新 MEMORY.md（高价值洞察）
function updateMemory(insights) {
  if (insights.length === 0) {
    return;
  }

  const timestamp = new Date().toISOString().slice(0, 16).replace('T', ' ');
  const content = `# C 类任务高价值洞察

**更新时间：** ${timestamp}

---

## 📊 本周洞察

${insights.join('\n')}

---

*自动清理时提取*
`;

  fs.writeFileSync(CONFIG.memoryPath, content, 'utf-8');
  console.log(`[C 类清理] 已更新高价值洞察：${CONFIG.memoryPath}`);
}

// 清理已完成任务
function clearCompletedTasks(content) {
  const lines = content.split('\n');
  const newLines = [];
  let inCompletedSection = false;

  for (const line of lines) {
    if (line.startsWith('## ✅ 已完成（待清理）')) {
      inCompletedSection = true;
      newLines.push(line);
      newLines.push('');
      newLines.push('| 编号 | 任务内容 | 完成时间 | 清理状态 |');
      newLines.push('|------|---------|---------|---------|');
      newLines.push('| - | - | - | - |');
      continue;
    }

    if (inCompletedSection && line.startsWith('##')) {
      inCompletedSection = false;
    }

    if (!inCompletedSection || line.startsWith('##')) {
      newLines.push(line);
    }
  }

  return newLines.join('\n');
}

// 写入清理报告
function writeCleanupReport(tasks, insights) {
  const timestamp = new Date().toISOString().slice(0, 16).replace('T', ' ');
  const filename = `c-task-cleanup-${timestamp.replace(/[: ]/g, '-')}.md`;
  const filepath = path.join(CONFIG.logPath, filename);

  const content = `# C 类任务清理报告

**清理时间：** ${timestamp}

---

## 📊 清理统计

- **已完成任务：** ${tasks.length} 个
- **高价值洞察：** ${insights.length} 个
- **清理状态：** ✅ 完成

---

## 📋 已完成任务列表

${tasks.length > 0 ? tasks.map(t => `- ${t.id}: ${t.content} (${t.completedTime})`).join('\n') : '无'}

---

## 💡 高价值洞察（已存入 MEMORY.md）

${insights.length > 0 ? insights.join('\n') : '无'}

---

*下次清理：下周日 23:00*
`;

  fs.writeFileSync(filepath, content, 'utf-8');
  console.log(`[C 类清理] 清理报告：${filepath}`);
}

// 主函数
async function main() {
  console.log('[C 类清理] 开始清理...');
  ensureLogDirectory();

  // 读取 C 类任务池
  const content = readCTaskPool();
  if (!content) {
    console.log('[C 类清理] 无内容，跳过');
    return;
  }

  // 解析已完成任务
  const tasks = parseCompletedTasks(content);
  console.log(`[C 类清理] 发现 ${tasks.length} 个已完成任务`);

  // 4D 压缩高价值内容
  const insights = compressInsights(tasks);
  console.log(`[C 类清理] 提取 ${insights.length} 个高价值洞察`);

  // 更新 MEMORY.md
  if (insights.length > 0) {
    updateMemory(insights);
  }

  // 清理已完成任务
  const newContent = clearCompletedTasks(content);

  // 写回 C 类任务池
  fs.writeFileSync(CONFIG.cTaskPath, newContent, 'utf-8');
  console.log('[C 类清理] 已清理 C 类任务池');

  // 写入清理报告
  writeCleanupReport(tasks, insights);

  console.log('[C 类清理] 清理完成！');
}

// 执行
main().catch(console.error);

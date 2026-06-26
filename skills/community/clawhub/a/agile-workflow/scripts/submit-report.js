#!/usr/bin/env node
/**
 * 任务汇报提交脚本 v1.0
 * 
 * 功能：
 * 1. 从 .task-state.json 读取任务状态
 * 2. 生成汇报内容（Markdown 格式）
 * 3. 调用 workspace-novel_architect/scripts/submit-report.sh 提交
 * 
 * 用法：
 * node submit-report.js [--project <目录>] [--output <文件>]
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// 配置
const config = {
  projectDir: process.env.PROJECT_DIR || '/home/ubutu/.openclaw/workspace-novel_architect',
  submitScript: '/home/ubutu/.openclaw/workspace-novel_architect/scripts/submit-report.sh',
  ...parseArgs()
};

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' && args[i + 1]) {
      result.projectDir = args[++i];
    } else if (args[i] === '--output' && args[i + 1]) {
      result.outputFile = args[++i];
    } else if (args[i] === '--help') {
      console.log(`用法：node submit-report.js [选项]
      
选项：
  --project <目录>  项目目录（默认：${config.projectDir}）
  --output <文件>   输出文件（默认：stdout）
  --help            显示帮助`);
      process.exit(0);
    }
  }
  
  return result;
}

/**
 * 加载任务状态
 */
function loadTaskState(projectDir) {
  const stateFile = path.join(projectDir, '.task-state.json');
  
  if (!fs.existsSync(stateFile)) {
    console.error('❌ 任务状态文件不存在：' + stateFile);
    process.exit(1);
  }
  
  return JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
}

/**
 * 生成汇报内容
 */
function generateReport(state) {
  const total = Object.keys(state).length;
  const completed = Object.values(state).filter(t => t.status === 'completed').length;
  const running = Object.values(state).filter(t => t.status === 'running').length;
  const pending = Object.values(state).filter(t => t.status === 'pending').length;
  const failed = Object.values(state).filter(t => t.status === 'failed').length;
  
  const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
  
  // 按 Agent 统计
  const byAgent = {};
  Object.entries(state).forEach(([taskId, task]) => {
    const agent = task.agent || 'unknown';
    if (!byAgent[agent]) byAgent[agent] = { total: 0, completed: 0, failed: 0 };
    byAgent[agent].total++;
    if (task.status === 'completed') byAgent[agent].completed++;
    if (task.status === 'failed') byAgent[agent].failed++;
  });
  
  let report = `# 📊 敏捷工作流任务汇报\n\n`;
  report += `## 📈 进度总览\n\n`;
  report += `| 指标 | 数值 |\n`;
  report += `|------|------|\n`;
  report += `| 总任务数 | ${total} |\n`;
  report += `| 已完成 | ${completed} |\n`;
  report += `| 进行中 | ${running} |\n`;
  report += `| 待执行 | ${pending} |\n`;
  report += `| 失败 | ${failed} |\n`;
  report += `| 完成率 | ${progress}% |\n\n`;
  
  report += `## 📋 按 Agent 统计\n\n`;
  report += `| Agent | 总数 | 已完成 | 失败 | 完成率 |\n`;
  report += `|-------|------|--------|------|--------|\n`;
  
  Object.entries(byAgent).forEach(([agent, stats]) => {
    const rate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;
    report += `| ${agent} | ${stats.total} | ${stats.completed} | ${stats.failed} | ${rate}% |\n`;
  });
  
  report += `\n## 🔍 详细任务列表\n\n`;
  
  // 完成任务
  report += `### ✅ 已完成 (${completed})\n\n`;
  Object.entries(state)
    .filter(([_, t]) => t.status === 'completed')
    .slice(0, 10)
    .forEach(([taskId, task]) => {
      report += `- ✅ \`${taskId}\` (${task.agent || 'unknown'})\n`;
    });
  
  if (completed > 10) {
    report += `\n*... 还有 ${completed - 10} 个已完成任务，未显示*\n`;
  }
  
  // 进行中任务
  report += `\n### ⏳ 进行中 (${running})\n\n`;
  Object.entries(state)
    .filter(([_, t]) => t.status === 'running')
    .forEach(([taskId, task]) => {
      report += `- ⏳ \`${taskId}\` (${task.agent || 'unknown'})\n`;
    });
  
  if (running === 0) {
    report += `- *无*\n`;
  }
  
  // 失败任务
  report += `\n### ❌ 失败 (${failed})\n\n`;
  Object.entries(state)
    .filter(([_, t]) => t.status === 'failed')
    .forEach(([taskId, task]) => {
      report += `- ❌ \`${taskId}\` (${task.agent || 'unknown'}) - ${task.error || '未知错误'}\n`;
    });
  
  if (failed === 0) {
    report += `- *无*\n`;
  }
  
  report += `\n---\n`;
  report += `*汇报生成时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}*\n`;
  
  return report;
}

/**
 * 提交汇报
 */
function submitReport(report) {
  // 写入临时文件
  const tempFile = path.join('/tmp', `agile-report-${Date.now()}.md`);
  fs.writeFileSync(tempFile, report, 'utf-8');
  
  console.log(`📝 汇报已保存到：${tempFile}`);
  console.log(`🚀 调用提交脚本：${config.submitScript}`);
  
  // 调用 submit-report.sh
  exec(`${config.submitScript} ${tempFile}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`❌ 提交失败：${error.message}`);
      console.error(`stderr: ${stderr}`);
      process.exit(1);
    }
    
    console.log(`✅ 提交成功！`);
    console.log(stdout);
    process.exit(0);
  });
}

/**
 * 主函数
 */
function main() {
  console.log('📊 敏捷工作流任务汇报生成器');
  console.log(`📁 项目目录：${config.projectDir}`);
  
  // 加载任务状态
  const state = loadTaskState(config.projectDir);
  console.log(`📊 加载了 ${Object.keys(state).length} 个任务`);
  
  // 生成汇报
  const report = generateReport(state);
  
  // 输出
  if (config.outputFile) {
    fs.writeFileSync(config.outputFile, report, 'utf-8');
    console.log(`📝 汇报已保存到：${config.outputFile}`);
  } else {
    console.log('\n' + report);
  }
  
  // 自动提交（可选）
  if (fs.existsSync(config.submitScript)) {
    const shouldSubmit = process.env.AUTO_SUBMIT !== 'false';
    if (shouldSubmit) {
      submitReport(report);
    }
  } else {
    console.log(`⚠️ 提交脚本不存在：${config.submitScript}，跳过自动提交`);
  }
}

main();

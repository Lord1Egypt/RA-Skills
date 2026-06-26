#!/usr/bin/env node
/**
 * 每日分析脚本
 * 每天 12:00 和 24:00 执行
 * 分析 0:00 到当前时间的所有对话
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');

/**
 * 获取今天的日期范围
 */
function getTodayRange() {
  const now = new Date();
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
  
  return {
    start: startOfDay.toISOString(),
    end: now.toISOString(),
    dateStr: now.toLocaleDateString('zh-CN')
  };
}

/**
 * 主分析函数
 */
async function main() {
  console.log('📅 每日对话分析启动...\n');
  
  const range = getTodayRange();
  console.log(`📊 分析范围: ${range.dateStr} 00:00 - 现在`);
  console.log(`📊 时间戳: ${range.start} 至 ${range.end}\n`);
  
  console.log('🧠 === 执行三项分析任务 ===\n');
  
  console.log('1️⃣  用户个人特征分析');
  console.log('   - 读取 USER.md 现有记录');
  console.log('   - 分析今日对话内容');
  console.log('   - 合并新分析结果');
  console.log('   - 更新 USER.md');
  console.log('   - 如有需要调用合适的 skill 工具\n');
  
  console.log('2️⃣  对话任务与需求分析');
  console.log('   - 读取 MEMORY.md 中的"对话分析"记录');
  console.log('   - 分析今日对话中的任务');
  console.log('   - 增量写入新分析结果');
  console.log('   - 如有需要调用合适的 skill 工具\n');
  
  console.log('3️⃣  未完成任务检查');
  console.log('   - 扫描 HEARTBEAT.md 任务看板');
  console.log('   - 扫描 WORKING.md 项目任务');
  console.log('   - 检查对话历史中的待办');
  console.log('   - 过滤已标记"NotNeeded"的任务');
  console.log('   - 通过 Feishu 发送询问消息');
  console.log('   - 如无未完成任务，发送"未发现未完成的任务"\n');
  
  console.log('✅ 分析任务已生成，等待 OpenClaw 执行...');
  console.log('\n提示：OpenClaw 应该：');
  console.log('  - 使用 sessions_history 获取今日对话');
  console.log('  - 使用 LLM 分析对话内容');
  console.log('  - 更新 USER.md 和 MEMORY.md');
  console.log('  - 发送 Feishu 通知（如有未完成任务）');
  
  return {
    triggered: true,
    date: range.dateStr,
    range,
    tasks: ['user_profile', 'conversation_tasks', 'incomplete_tasks']
  };
}

// 运行
main().then(result => {
  console.log('\n📊 分析完成');
  process.exit(0);
}).catch(err => {
  console.error('❌ 分析失败:', err);
  process.exit(1);
});

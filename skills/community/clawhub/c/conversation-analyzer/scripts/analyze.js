#!/usr/bin/env node
/**
 * 对话分析主脚本
 * 每10次对话触发，执行完整分析
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const HEARTBEAT_FILE = path.join(WORKSPACE, 'HEARTBEAT.md');
const USER_FILE = path.join(WORKSPACE, 'USER.md');
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');

/**
 * 读取文件内容
 */
function readFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
  } catch (e) {
    console.error(`读取失败: ${filePath}`, e.message);
  }
  return '';
}

/**
 * 写入文件
 */
function writeFile(filePath, content) {
  try {
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`✅ 已写入: ${path.basename(filePath)}`);
  } catch (e) {
    console.error(`写入失败: ${filePath}`, e.message);
  }
}

/**
 * 更新对话计数器
 */
function updateConversationCounter() {
  let heartbeat = readFile(HEARTBEAT_FILE);
  
  // 提取当前计数
  const match = heartbeat.match(/当前对话次数[:：]\s*(\d+)/);
  let count = match ? parseInt(match[1]) : 0;
  count++;
  
  // 更新计数器
  if (match) {
    heartbeat = heartbeat.replace(/当前对话次数[:：]\s*\d+/, `当前对话次数：${count}`);
  } else {
    // 添加计数器部分
    heartbeat += `\n## 对话计数器\n- 当前对话次数：${count}\n- 上次分析时间：未执行\n- 分析阈值：每10次对话\n`;
  }
  
  writeFile(HEARTBEAT_FILE, heartbeat);
  console.log(`📊 对话计数器: ${count}/10`);
  
  return count;
}

/**
 * 重置对话计数器
 */
function resetConversationCounter() {
  let heartbeat = readFile(HEARTBEAT_FILE);
  const now = new Date().toLocaleString('zh-CN');
  
  heartbeat = heartbeat.replace(/当前对话次数[:：]\s*\d+/, '当前对话次数：0');
  heartbeat = heartbeat.replace(/上次分析时间[:：][^\n]*/, `上次分析时间：${now}`);
  
  writeFile(HEARTBEAT_FILE, heartbeat);
  console.log('🔄 对话计数器已重置');
}

/**
 * 分析用户个人特征
 * 输出分析提示，由 OpenClaw 执行实际分析
 */
function analyzeUserProfile() {
  console.log('\n🧠 === 1. 用户个人特征分析 ===');
  console.log('分析维度：');
  console.log('  - 个人特征：性格、沟通风格、决策模式');
  console.log('  - 喜好：技术偏好、工具选择、内容类型');
  console.log('  - 技能：技术栈、专业能力、熟悉领域');
  console.log('  - 个人经历：职业路径、项目经验、成长轨迹');
  console.log('  - 背景：工作环境、团队角色、行业背景');
  console.log('  - 情绪状态：压力水平、满意度、关注点');
  console.log('  - 现在做的事情：当前项目、重点任务、日常活动');
  console.log('  - 以后想做的事情：目标、计划、期望');
  console.log('\n执行动作：');
  console.log('  1. 读取 USER.md 现有记录');
  console.log('  2. 分析最近对话内容');
  console.log('  3. 合并新分析结果');
  console.log('  4. 更新 USER.md');
  console.log('  5. 如有需要调用合适的 skill 工具');
  
  return {
    type: 'user_profile',
    action: 'analyze_and_update',
    target: USER_FILE
  };
}

/**
 * 分析对话任务
 * 输出分析提示，由 OpenClaw 执行实际分析
 */
function analyzeConversationTasks() {
  console.log('\n📋 === 2. 对话任务与需求分析 ===');
  console.log('分析维度：');
  console.log('  - 已要求的事情：具体任务、完成状态');
  console.log('  - 预测后续需求：基于模式预测下一步');
  console.log('  - 错误记录：理解偏差、执行错误、改进点');
  console.log('\n执行动作：');
  console.log('  1. 读取 MEMORY.md 中的"对话分析"记录');
  console.log('  2. 分析最近对话中的任务');
  console.log('  3. 增量写入新分析结果');
  console.log('  4. 如有需要调用合适的 skill 工具');
  
  return {
    type: 'conversation_tasks',
    action: 'analyze_and_append',
    target: MEMORY_FILE,
    section: '对话分析'
  };
}

/**
 * 检查未完成任务
 * 输出检查提示，由 OpenClaw 执行实际检查
 */
function checkIncompleteTasks() {
  console.log('\n✅ === 3. 未完成任务检查 ===');
  console.log('检查范围：');
  console.log('  - 对话中提到的待办事项');
  console.log('  - 承诺但未完成的事项');
  console.log('  - 排除 MEMORY.md 中标记"不需要完成"的任务');
  console.log('\n执行动作：');
  console.log('  1. 扫描 HEARTBEAT.md 任务看板');
  console.log('  2. 扫描 WORKING.md 项目任务');
  console.log('  3. 检查对话历史中的待办');
  console.log('  4. 过滤已标记"NotNeeded"的任务');
  console.log('  5. 通过 Feishu 发送询问消息');
  console.log('  6. 如无未完成任务，发送"未发现未完成的任务"');
  
  return {
    type: 'incomplete_tasks',
    action: 'check_and_notify',
    notifyChannel: 'feishu'
  };
}

/**
 * 主分析函数
 */
async function main() {
  console.log('🧠 对话分析总结器启动...\n');
  
  // 1. 更新对话计数器
  const count = updateConversationCounter();
  
  // 2. 检查是否达到阈值
  if (count < 10) {
    console.log(`\n⏳ 未达到分析阈值 (${count}/10)，跳过分析`);
    return { triggered: false, count };
  }
  
  console.log('\n🎯 达到分析阈值，执行完整分析...\n');
  
  // 3. 执行三项分析
  const tasks = [
    analyzeUserProfile(),
    analyzeConversationTasks(),
    checkIncompleteTasks()
  ];
  
  // 4. 重置计数器
  resetConversationCounter();
  
  console.log('\n✅ 分析任务已生成，等待 OpenClaw 执行...');
  console.log('\n提示：OpenClaw 应该：');
  console.log('  1. 读取相关记忆文件');
  console.log('  2. 使用 LLM 分析对话内容');
  console.log('  3. 更新 USER.md 和 MEMORY.md');
  console.log('  4. 发送 Feishu 通知（如有未完成任务）');
  
  return {
    triggered: true,
    count,
    tasks
  };
}

// 运行
main().then(result => {
  if (result.triggered) {
    process.exit(0);
  } else {
    process.exit(0);
  }
}).catch(err => {
  console.error('❌ 分析失败:', err);
  process.exit(1);
});

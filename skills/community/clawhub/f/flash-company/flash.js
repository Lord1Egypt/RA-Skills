#!/usr/bin/env node

/**
 * Flash Company - 快速组队脚本（带记忆持久化）
 * 用法：node flash.js <团队类型> "<任务描述>"
 * 
 * v1.1.0 - 新增记忆持久化系统
 */

const fs = require('fs');
const path = require('path');

// 加载团队配置
const teamsPath = path.join(__dirname, 'teams.json');
const teams = JSON.parse(fs.readFileSync(teamsPath, 'utf8'));

// 加载记忆系统
const { MemoryManager } = require('./memory.js');

/**
 * 根据任务关键词匹配最合适的团队
 */
function matchTeam(task) {
  const taskLower = task.toLowerCase();
  
  // 遍历任务映射
  for (const [keyword, teamKey] of Object.entries(teams.taskMapping)) {
    if (taskLower.includes(keyword.toLowerCase())) {
      return teamKey;
    }
  }
  
  // 默认返回开发组
  return 'dev';
}

/**
 * 根据触发词匹配团队
 */
function matchByTrigger(trigger) {
  const triggerLower = trigger.toLowerCase();
  
  for (const [teamKey, teamConfig] of Object.entries(teams.teams)) {
    if (teamConfig.triggers.some(t => t.toLowerCase() === triggerLower)) {
      return teamKey;
    }
  }
  
  return null;
}

/**
 * 生成团队信息（带记忆注入）
 */
function generateTeamInfo(teamKey, task) {
  const team = teams.teams[teamKey];
  if (!team) {
    throw new Error(`未找到团队: ${teamKey}`);
  }
  
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const sessionId = `session-${Date.now()}`;
  
  // 初始化记忆管理器
  const mm = new MemoryManager(teamKey, sessionId);
  
  // 初始化共享上下文
  mm.updateSharedContext({
    project: task,
    currentPhase: 'started'
  });
  
  console.log(`\n⚡ Flash Company - ${team.emoji} ${team.name}`);
  console.log(`📅 创建时间: ${timestamp}`);
  console.log(`📋 任务: ${task}\n`);
  console.log('👥 团队成员:');
  
  team.members.forEach((member, index) => {
    // 初始化成员记忆
    const memory = mm.initMemberMemory(member.role, member.role);
    const memoryStatus = memory.tasks?.length > 0 
      ? `📚 ${memory.tasks.length}个历史任务` 
      : '🆕 新成员';
    
    console.log(`   ${index + 1}. ${member.emoji} ${member.role} (${member.model}) - ${member.description} ${memoryStatus}`);
  });
  
  console.log('\n🚀 子代理创建命令（含记忆注入）:');
  console.log('```');
  
  team.members.forEach(member => {
    const agentName = `临时-${team.name}-${member.role}-${timestamp}`;
    
    // 获取成员记忆上下文
    const memoryContext = mm.getMemoryContext(member.role);
    
    // 构建完整的上下文（包含记忆）
    const fullContext = `${memoryContext}\n\n## 当前角色\n你是${member.role}，职责：${member.description}\n\n## 当前任务\n${task}`;
    
    console.log(`sessions_spawn --model ${member.model} --name "${agentName}" --context "${fullContext.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`);
  });
  
  console.log('```\n');
  
  console.log('💾 记忆系统:');
  console.log(`   - 记忆目录: ~/.agent-memory/flash-company/${teamKey}/`);
  console.log(`   - 会话ID: ${sessionId}`);
  console.log(`   - 更新记忆: node memory.js update ${teamKey} <成员名> '<json>'`);
  console.log(`   - 记录决策: node memory.js record-decision ${teamKey} "<决策内容>"`);
  console.log(`   - 记录经验: node memory.js record-lesson ${teamKey} "<经验内容>"`);
  console.log('');
  
  return {
    teamKey,
    teamName: team.name,
    members: team.members,
    task,
    timestamp,
    sessionId,
    memoryManager: mm
  };
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法:');
    console.log('  node flash.js <团队类型> "<任务描述>"');
    console.log('  node flash.js auto "<任务描述>"    # 自动匹配团队');
    console.log('\n可用团队:');
    for (const [key, team] of Object.entries(teams.teams)) {
      console.log(`  ${team.emoji} ${key.padEnd(8)} - ${team.name} (${team.members.length}人)`);
    }
    process.exit(0);
  }
  
  const teamInput = args[0];
  const task = args.slice(1).join(' ') || '待分配任务';
  
  let teamKey;
  
  if (teamInput === 'auto') {
    teamKey = matchTeam(task);
    console.log(`🎯 自动匹配团队: ${teamKey}`);
  } else {
    teamKey = matchByTrigger(teamInput) || teamInput;
  }
  
  generateTeamInfo(teamKey, task);
}

main();
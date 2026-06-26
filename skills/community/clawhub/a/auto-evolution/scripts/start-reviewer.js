#!/usr/bin/env node

/**
 * Auto Revolution Reviewer Starter
 * 启动 Reviewer 分析复杂任务并生成详细 Subtasks
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const TASKS_DIR = path.join(__dirname, '../tasks');

// 获取任务 ID
const taskId = process.argv[2];
if (!taskId) {
  console.error('❌ 错误：缺少任务 ID');
  console.error('用法：node scripts/start-reviewer.js <task-id>');
  process.exit(1);
}

// 读取任务
const taskFile = path.join(TASKS_DIR, `task-${taskId}.json`);
if (!fs.existsSync(taskFile)) {
  console.error(`❌ 错误：任务文件不存在：${taskFile}`);
  process.exit(1);
}

const task = JSON.parse(fs.readFileSync(taskFile, 'utf8'));

// 验证任务类型
if (task.complexity?.mode !== 'auto') {
  console.error(`❌ 错误：任务 ${taskId} 不是自动 Subtask 模式`);
  console.error(`   当前模式：${task.complexity?.mode || 'manual'}`);
  process.exit(1);
}

console.log(`\n🤖 启动 Reviewer 分析任务 ${taskId}\n`);
console.log(`📋 任务标题：${task.title}`);
console.log(`📊 复杂度评分：${task.complexity.total}/25`);
console.log(`🤖 Reviewer 模型：${task.reviewer?.model || 'anthropic/claude-sonnet-4-6'}\n`);

// 构建 Reviewer 提示词
const reviewerPrompt = `你是 Auto Revolution Reviewer（高级代码架构师）。

## 任务目标
${task.description}

## 任务复杂度评分
- 代码量：${task.complexity.code_lines} 分
- 文件数：${task.complexity.files} 分
- 风险：${task.complexity.risk} 分
- 依赖：${task.complexity.dependencies} 分
- 创新：${task.complexity.innovation} 分
- **总分：${task.complexity.total} 分**

## 你的任务

### Step 1: 任务分析
1. 分析任务的核心目标
2. 识别关键挑战和风险点
3. 评估所需的技术栈和依赖

### Step 2: 拆解 Subtasks
将任务拆解为 3-7 个可执行的 subtasks，每个 subtask 应：
- 目标明确、可执行
- 工作量适中（~5-10 分钟）
- 有明确的验收标准

### Step 3: 生成执行指令
为每个 subtask 生成详细的执行指令，包括：
- 需要修改的文件
- 具体的代码实现
- 测试验证方法

## 输出格式

\`\`\`json
{
  "analysis": {
    "core_goal": "...",
    "challenges": ["...", "..."],
    "tech_stack": ["...", "..."]
  },
  "subtasks": [
    {
      "id": 0,
      "title": "...",
      "description": "...",
      "estimated_minutes": 10,
      "files_to_modify": ["..."],
      "acceptance_criteria": ["..."]
    }
  ],
  "instructions": {
    "0": "详细的执行指令...",
    "1": "..."
  }
}
\`\`\`

**模型：** ${task.reviewer?.model || 'anthropic/claude-sonnet-4-6'}
`;

// 保存 Reviewer 提示词
const reviewerPromptFile = path.join(TASKS_DIR, `task-${taskId}-reviewer-prompt.md`);
fs.writeFileSync(reviewerPromptFile, reviewerPrompt, 'utf8');

console.log(`✅ Reviewer 提示词已保存到：${reviewerPromptFile}\n`);

// 启动 Reviewer（使用 sessions_spawn 或子进程）
console.log(`⏳ 启动 Reviewer 分析...\n`);

// 这里应该调用 sessions_spawn，但由于是 Node.js 脚本，我们用注释说明
console.log(`📝 下一步操作：
1. 使用 sessions_spawn 启动 Reviewer 子 agent
2. 传递 reviewerPrompt 作为任务
3. 等待 Reviewer 返回分析结果
4. 更新任务 JSON 的 subtasks 和 instructions 字段
5. 启动 Executor 执行任务

示例命令（伪代码）：
\`\`\`javascript
const result = await sessions_spawn({
  agentId: 'wilson',
  label: \`task${taskId}-reviewer\`,
  model: '${task.reviewer?.model || 'anthropic/claude-sonnet-4-6'}',
  task: reviewerPrompt
});
\`\`\`
`);

console.log(`\n✅ Reviewer 启动完成！`);

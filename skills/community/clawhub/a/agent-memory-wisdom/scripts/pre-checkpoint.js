#!/usr/bin/env node
/**
 * pre-checkpoint.js — 复杂任务开始前主动落盘
 * 
 * 用法: node pre-checkpoint.js "<任务名>" "<计划描述>" [选项...]
 * 
 * 在 Brain 置信度判定为复杂任务时调用
 * 把"打算怎么做"写入缓冲区，这样压缩后也能无缝衔接
 * 
 * 选项:
 *   --confidence <n>     置信度 1-10
 *   --steps <n>          预计步数
 *   --subagents <list>   需要的子agent，逗号分隔
 *   --parallel           是否并行任务
 */

const fs = require('fs');
const path = require('path');

const BUFFER_FILE = path.join(process.env.HOME, '.openclaw/workspace/memory/工作缓冲区.md');
const SNAPSHOT_FILE = path.join(process.env.HOME, '.openclaw/workspace/memory/SNAPSHOT.md');

function parseArgs(args) {
  const result = { task: '', plan: '', confidence: 5, steps: 0, subagents: [], parallel: false };
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--confidence':
        result.confidence = parseInt(args[++i]) || 5;
        break;
      case '--steps':
        result.steps = parseInt(args[++i]) || 0;
        break;
      case '--subagents':
        result.subagents = args[++i].split(',').map(s => s.trim()).filter(Boolean);
        break;
      case '--parallel':
        result.parallel = true;
        break;
      default:
        if (!result.task) result.task = args[i];
        else if (!result.plan) result.plan = args[i];
    }
  }
  return result;
}

function formatTimestamp() {
  const now = new Date();
  const cst = new Date(now.getTime() + (8 * 60 * 60 * 1000));
  return cst.toISOString().replace('T', ' ').substring(0, 19) + ' CST';
}

function generateId() {
  return Math.random().toString(36).substring(2, 8);
}

function readBuffer() {
  try {
    if (fs.existsSync(BUFFER_FILE)) {
      return fs.readFileSync(BUFFER_FILE, 'utf8');
    }
  } catch (e) {}
  return '';
}

function writeCheckpoint(data) {
  const id = generateId();
  const ts = formatTimestamp();
  
  const block = `\n\n<!-- PRE-CHECKPOINT ${id} | ${ts} -->
## 🔸 预检点 ${id}（${ts}）

### 任务
${data.task}

### 计划
${data.plan}

### 元信息
| 字段 | 值 |
|:---|:---|
| 置信度 | ${data.confidence}/10 |
| 预计步数 | ${data.steps} |
| 子Agent | ${data.subagents.length > 0 ? data.subagents.join(', ') : '无'} |
| 并行 | ${data.parallel ? '是' : '否'} |
| 状态 | ⏳ 进行中 |

### 进度记录
- [${ts}] 任务开始

`;
  
  // 追加到缓冲区
  fs.appendFileSync(BUFFER_FILE, block, 'utf8');
  
  // 同时更新SNAPSHOT的最后活跃时间
  updateSnapshot(data);
  
  return id;
}

function updateSnapshot(data) {
  try {
    let content = '';
    if (fs.existsSync(SNAPSHOT_FILE)) {
      content = fs.readFileSync(SNAPSHOT_FILE, 'utf8');
    }
    
    const ts = formatTimestamp();
    const checkpointRef = `| ${ts} | 🔸 预检点进行中 | ${data.task.substring(0, 50)}... |`;
    
    // 在"进行中"部分追加
    if (content.includes('## 进行中')) {
      content = content.replace(
        /(## 进行中[\s\S]*?)(\n## |\n# |$$)/,
        (match, section, next) => {
          const newEntry = `\n- **🔸 进行中**: ${data.task} [${ts}]`;
          return section + newEntry + (next || '');
        }
      );
    }
    
    // 标记最后活跃
    content = content.replace(
      /# 最后更新时间：[\d\-: ]+/,
      `# 最后更新时间：${ts}`
    );
    
    fs.writeFileSync(SNAPSHOT_FILE, content, 'utf8');
  } catch (e) {
    console.error('更新SNAPSHOT失败:', e.message);
  }
}

// 完成检点
function completeCheckpoint(id, result) {
  const ts = formatTimestamp();
  try {
    let content = fs.readFileSync(BUFFER_FILE, 'utf8');
    
    // 替换状态
    content = content.replace(
      new RegExp(`(<!-- PRE-CHECKPOINT ${id}[\\s\\S]*?状态 \\| )⏳ 进行中`, 'm'),
      `$1✅ 完成`
    );
    
    // 追加结果
    content = content.replace(
      new RegExp(`(<!-- PRE-CHECKPOINT ${id}[\\s\\S]*?\\- \\[.*?\\] 任务开始\\n)`, 'm'),
      `$1- [${ts}] 任务完成: ${result}\n`
    );
    
    fs.writeFileSync(BUFFER_FILE, content, 'utf8');
  } catch (e) {
    console.error('完成检点失败:', e.message);
  }
}

// 主体逻辑
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
pre-checkpoint.js — 复杂任务预检点写入

用法:
  node pre-checkpoint.js "<任务名>" "<计划描述>" [选项]

示例:
  node pre-checkpoint.js "调研推特AI博主" "1.派reasercher查趋势 2.整理报告 3.写结论" --confidence 8 --steps 3 --subagents researcher-agent

选项:
  --confidence <n>   置信度 1-10（触发阈值建议≥6）
  --steps <n>        预计步数
  --subagents <list> 需要的子agent，逗号分隔
  --parallel         是否并行任务
  --complete <id>    标记检点完成，传入检点ID
  
环境变量:
  BUFFER_FILE        缓冲区路径（默认: memory/工作缓冲区.md）
  `);
  process.exit(0);
}

if (args.includes('--complete')) {
  const idx = args.indexOf('--complete');
  const id = args[idx + 1];
  const result = args[idx + 2] || '完成';
  completeCheckpoint(id, result);
  console.log(`✅ 检点 ${id} 已标记完成`);
  process.exit(0);
}

const data = parseArgs(args);

if (!data.task || !data.plan) {
  console.error('错误: 任务名和计划描述不能为空');
  console.error('用法: node pre-checkpoint.js "<任务>" "<计划>" [--confidence 8] [--steps 3] [--subagents a,b]');
  process.exit(1);
}

const id = writeCheckpoint(data);

console.log(`✅ 预检点已写入 [${id}]`);
console.log(`📋 任务: ${data.task}`);
console.log(`📊 置信度: ${data.confidence}/10`);
console.log(`🔗 缓冲区: ${BUFFER_FILE}`);
console.log(``);
console.log(`完成后运行:`);
console.log(`  node pre-checkpoint.js --complete ${id} "<结果简述>"`);

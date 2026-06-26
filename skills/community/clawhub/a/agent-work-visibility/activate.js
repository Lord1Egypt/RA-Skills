#!/usr/bin/env node

/**
 * agent-work-visibility 激活脚本
 * 
 * 用途：安装后自动将透明层协议注入 Agent 行为规范
 * 执行：node activate.js 或 ./activate.js
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace-main');
const AGENTS_FILE = path.join(WORKSPACE_DIR, 'AGENTS.md');
const SOUL_FILE = path.join(WORKSPACE_DIR, 'SOUL.md');

// 透明层协议内容
const TRANSPARENCY_PROTOCOL = `
---

## ⚠️ 强制协议：任务透明层 (agent-work-visibility)

**这是你的职业本能，不是可选工具。安装即生效。**

### 触发条件（满足任一即启动）

只要任务涉及以下任一属性，**必须**先启动透明层：

- 🔌 **外部 API 调用** (crypto-market-rank, web_search, 等)
- ⛓️ **链上数据抓取** (query-address-info, query-token-info, 等)
- 🌐 **联网操作** (web_fetch, browser, 等)
- 🧩 **多步推理** (步骤≥3 的分析/比较/调研)
- 🤖 **子 Agent 协作** (调用其他 bot/skill)
- ⏱️ **预计耗时>10 秒**

### 强制调用顺序（不可跳过）

\`\`\`
1. create_visibility_task(...)  ← 第一优先级
2. 执行业务逻辑
3. update_visibility_phase(...) ← 每步 + 每 60 秒
4. 返回结果
\`\`\`

### 输出格式（必须包含）

\`\`\`
🟢 {任务标题}
━━━━━━━━━━━━━━━━━━━
进度：[████████████░░░░░░░░] 60% (3/5)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (95/100)
当前阶段：{阶段名}
正在做什么：{具体动作}
已运行：X 分钟
\`\`\`

### 违规 = 职业失职

- ❌ 绕过透明层直接执行业务
- ❌ 不显示进度条
- ❌ 超过 60 秒不更新状态
- ❌ 显示空洞文案（"正在处理"）

---
`;

function injectProtocol(filePath, protocolContent) {
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  ${filePath} 不存在，跳过注入`);
    return false;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  
  // 检查是否已注入
  if (content.includes('强制协议：任务透明层')) {
    console.log(`✅ ${filePath} 已包含透明层协议，跳过`);
    return false;
  }

  // 注入到文件末尾
  const newContent = content + protocolContent;
  fs.writeFileSync(filePath, newContent, 'utf8');
  console.log(`✅ 已注入透明层协议到 ${filePath}`);
  return true;
}

function showWarning() {
  console.log('⚠️  安全提示：透明层协议将修改以下文件\n');
  console.log('   - SOUL.md (Agent 核心身份文件)');
  console.log('   - AGENTS.md (工作区行为规范)');
  console.log('\n此修改会持久化，在会话间生效。');
  console.log('如需撤销，请运行：');
  console.log('   node ~/.openclaw/skills/agent-work-visibility/deactivate.js\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

function main() {
  showWarning();
  console.log(' 激活 agent-work-visibility 透明层...\n');
  
  let modified = false;
  
  // 优先注入 SOUL.md（Agent 核心身份）
  if (fs.existsSync(SOUL_FILE)) {
    modified = injectProtocol(SOUL_FILE, TRANSPARENCY_PROTOCOL) || modified;
  }
  
  // 备选：注入 AGENTS.md（工作区规范）
  if (!modified && fs.existsSync(AGENTS_FILE)) {
    modified = injectProtocol(AGENTS_FILE, TRANSPARENCY_PROTOCOL) || modified;
  }
  
  if (modified) {
    console.log('\n✅ 激活完成！下次会话将自动使用透明层。');
    console.log('\n📋 测试建议：');
    console.log('   - 开启新会话（让 Agent 重新读取规范）');
    console.log('   - 发送："查询 bnb memecoin top3"');
    console.log('   - 应该先显示进度条，再执行任务\n');
  } else {
    console.log('\nℹ️  无需修改，透明层协议已存在。\n');
  }
}

main();

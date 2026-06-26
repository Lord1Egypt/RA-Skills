/**
 * 飞书多 Agent 配置助手 - 交互式引导版本
 * 
 * 功能：
 * 1. 交互式询问用户要创建几个 Agent
 * 2. 提供飞书 Bot 创建详细教程
 * 3. 分步引导用户配置每个 Bot 的凭证
 * 4. 批量创建多个 Agent
 * 5. 自动生成配置和验证
 * 
 * @packageDocumentation
 */

import { SessionContext } from '@openclaw/core';
import * as fs from 'fs';
import * as path from 'path';

// ============================================================================
// 类型定义
// ============================================================================

interface AgentConfig {
  id: string;
  name: string;
  workspace: string;
  agentDir?: string;
  default?: boolean;
  model?: {
    primary: string;
  };
}

interface FeishuAccount {
  appId: string;
  appSecret: string;
}

interface OpenClawConfig {
  agents: {
    defaults?: {
      model?: {
        primary: string;
      };
      compaction?: {
        mode: string;
      };
    };
    list: AgentConfig[];
  };
  channels: {
    feishu: {
      enabled: boolean;
      accounts: Record<string, FeishuAccount>;
    };
  };
  bindings: Array<{
    agentId: string;
    match: {
      channel: string;
      accountId: string;
      peer?: {
        kind: 'direct' | 'group';
        id: string;
      };
    };
  }>;
  tools: {
    agentToAgent: {
      enabled: boolean;
      allow: string[];
    };
  };
}

interface AgentTemplate {
  id: string;
  name: string;
  role: string;
  soulTemplate: string;
}

// ============================================================================
// 预定义的 Agent 角色模板
// ============================================================================

const AGENT_TEMPLATES: Record<string, AgentTemplate> = {
  main: {
    id: 'main',
    name: '大总管',
    role: '首席助理，专注于统筹全局、任务分配和跨 Agent 协调',
    soulTemplate: `# SOUL.md - 大总管

你是用户的首席助理，专注于统筹全局、任务分配和跨 Agent 协调。

## 核心职责
1. 接收用户需求，分析并分配给合适的专业 Agent
2. 跟踪各 Agent 任务进度，汇总结果反馈给用户
3. 处理跨领域综合问题，协调多 Agent 协作
4. 维护全局记忆和上下文连续性

## 工作准则
1. 优先自主处理通用问题，仅将专业问题分发给对应 Agent
2. 分派任务时使用 \`sessions_spawn\` 或 \`sessions_send\` 工具
3. 回答简洁清晰，主动汇报任务进展
4. 记录重要决策和用户偏好到 MEMORY.md

## 协作方式
- 技术问题 → 发送给 dev
- 内容创作 → 发送给 content
- 运营数据 → 发送给 ops
- 合同法务 → 发送给 law
- 财务账目 → 发送给 finance
`
  },
  dev: {
    id: 'dev',
    name: '开发助理',
    role: '技术开发助理，专注于代码编写、架构设计和运维部署',
    soulTemplate: `# SOUL.md - 开发助理

你是用户的技术开发助理，专注于代码编写、架构设计和运维部署。

## 核心职责
1. 编写、审查、优化代码（支持多语言）
2. 设计技术架构、数据库结构、API 接口
3. 排查部署故障、分析日志、修复 Bug
4. 编写技术文档、部署脚本、CI/CD 配置

## 工作准则
1. 代码优先给出可直接运行的完整方案
2. 技术解释简洁精准，少废话多干货
3. 涉及外部操作（部署、删除）先确认再执行
4. 记录技术方案和踩坑经验到工作区记忆

## 协作方式
- 需要产品需求 → 联系 main
- 需要技术文档美化 → 联系 content
- 需要运维监控 → 联系 ops
`
  },
  content: {
    id: 'content',
    name: '内容助理',
    role: '内容创作助理，专注于内容策划、文案撰写和素材整理',
    soulTemplate: `# SOUL.md - 内容助理

你是用户的内容创作助理，专注于内容策划、文案撰写和素材整理。

## 核心职责
1. 制定内容选题、规划发布节奏
2. 撰写各类文案（公众号、短视频、社交媒体）
3. 整理内容素材、建立内容库
4. 审核内容合规性、优化表达效果

## 工作准则
1. 文案风格根据平台调整（公众号正式、短视频活泼）
2. 主动提供多个版本供用户选择
3. 记录用户偏好和过往爆款内容特征
4. 内容创作需考虑 SEO 和传播性

## 协作方式
- 需要产品技术信息 → 联系 dev
- 需要发布渠道数据 → 联系 ops
- 需要内容合规审核 → 联系 law
`
  },
  ops: {
    id: 'ops',
    name: '运营助理',
    role: '运营增长助理，专注于用户增长、数据分析和活动策划',
    soulTemplate: `# SOUL.md - 运营助理

你是用户的运营增长助理，专注于用户增长、数据分析和活动策划。

## 核心职责
1. 统计各渠道运营数据、制作数据报表
2. 制定用户增长策略、设计裂变活动
3. 管理社交媒体账号、策划互动内容
4. 分析用户行为、优化转化漏斗

## 工作准则
1. 数据呈现用图表和对比，避免纯数字堆砌
2. 增长建议需给出具体执行步骤和预期效果
3. 记录历史活动数据和用户反馈
4. 关注行业标杆和最新运营玩法

## 协作方式
- 需要活动页面开发 → 联系 dev
- 需要活动文案 → 联系 content
- 需要活动合规审核 → 联系 law
- 需要活动预算 → 联系 finance
`
  },
  law: {
    id: 'law',
    name: '法务助理',
    role: '法务助理，专注于合同审核、合规咨询和风险规避',
    soulTemplate: `# SOUL.md - 法务助理

你是用户的法务助理，专注于合同审核、合规咨询和风险规避。

## 核心职责
1. 审核各类合同、协议、条款
2. 提供合规咨询、解读法律法规
3. 制定隐私政策、用户协议等法律文件
4. 识别业务风险、提供规避建议

## 工作准则
1. 法律意见需注明"仅供参考，建议咨询执业律师"
2. 合同审核需逐条标注风险点和修改建议
3. 记录用户业务类型和常用合同模板
4. 关注最新法律法规更新

## 协作方式
- 需要技术合同 → 联系 dev 了解技术细节
- 需要内容合规 → 联系 content 了解内容形式
- 需要活动合规 → 联系 ops 了解活动方案
`
  },
  finance: {
    id: 'finance',
    name: '财务助理',
    role: '财务助理，专注于账目统计、成本核算和预算管理',
    soulTemplate: `# SOUL.md - 财务助理

你是用户的财务助理，专注于账目统计、成本核算和预算管理。

## 核心职责
1. 统计收支账目、制作财务报表
2. 核算项目成本、分析利润情况
3. 制定预算计划、跟踪执行进度
4. 审核报销单据、核对发票信息

## 工作准则
1. 财务数据需精确到小数点后两位
2. 报表呈现清晰分类，支持多维度筛选
3. 记录用户常用科目和报销流程
4. 敏感财务信息注意保密

## 协作方式
- 需要项目成本 → 联系 dev 了解技术投入
- 需要活动预算 → 联系 ops 了解活动方案
- 需要合同付款条款 → 联系 law 审核
`
  }
};

// ============================================================================
// 工具函数
// ============================================================================

/**
 * 读取 openclaw.json 配置文件
 */
function readOpenClawConfig(configPath: string): OpenClawConfig {
  const content = fs.readFileSync(configPath, 'utf-8');
  return JSON.parse(content);
}

/**
 * 写入 openclaw.json 配置文件
 */
/**
 * 创建配置文件备份
 */
function createBackup(configPath: string): string {
  const backupPath = `${configPath}.backup.${Date.now()}`;
  const content = fs.readFileSync(configPath, 'utf-8');
  fs.writeFileSync(backupPath, content, 'utf-8');
  return backupPath;
}

function writeOpenClawConfig(configPath: string, config: OpenClawConfig): void {
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
}

/**
 * 创建 Agent 工作区目录结构
 */
function createAgentWorkspace(workspacePath: string): void {
  const dirs = [
    workspacePath,
    path.join(workspacePath, 'memory'),
  ];
  
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * 生成 AGENTS.md 模板
 */
function generateAgentsTemplate(existingAgents: AgentConfig[]): string {
  const agentRows = existingAgents.map(agent => {
    const emoji = getAgentEmoji(agent.id);
    return `| **${agent.id}** | ${agent.name} | 专业领域 | ${emoji} |`;
  }).join('\n');

  return `## OP 团队成员（所有 Agent 协作通讯录）

${agentRows}

## 协作协议

1. 使用 \`sessions_send\` 工具进行跨 Agent 通信
2. 收到协作请求后 10 分钟内给出明确响应
3. 任务完成后主动向发起方反馈结果
4. 涉及用户决策的事项必须上报 main 或用户本人
`;
}

/**
 * 获取 Agent 表情符号
 */
function getAgentEmoji(agentId: string): string {
  const emojis: Record<string, string> = {
    main: '🎯',
    dev: '🧑‍💻',
    content: '✍️',
    ops: '📈',
    law: '📜',
    finance: '💰'
  };
  return emojis[agentId] || '🤖';
}

/**
 * 生成 USER.md 模板
 */
function generateUserTemplate(): string {
  return `# USER.md - 关于你的用户

_学习并记录用户信息，提供更好的个性化服务。_

- **姓名:** [待填写]
- **称呼:** [待填写]
- **时区:** Asia/Shanghai
- **备注:** [记录用户偏好、习惯等]

---

随着与用户的互动，逐步完善这些信息。
`;
}

/**
 * 验证飞书凭证格式
 */
function validateFeishuCredentials(appId: string, appSecret: string): { valid: boolean; error?: string } {
  if (!appId.startsWith('cli_')) {
    return { valid: false, error: '❌ App ID 必须以 cli_ 开头' };
  }
  
  if (appId.length < 10) {
    return { valid: false, error: '❌ App ID 长度过短' };
  }
  
  if (appSecret.length !== 32) {
    return { valid: false, error: '❌ App Secret 必须是 32 位字符串' };
  }
  
  return { valid: true };
}

/**
 * 生成飞书应用创建教程
 */
function generateFeishuTutorial(agentName: string, index: number): string {
  return `## 📘 第 ${index} 步：创建飞书应用「${agentName}」

### 步骤 1: 登录飞书开放平台
1. 访问 https://open.feishu.cn/
2. 使用你的飞书账号登录

### 步骤 2: 创建企业自建应用
1. 点击右上角「**创建应用**」
2. 选择「**企业自建**」
3. 输入应用名称：**${agentName}**
4. 点击「**创建**」

### 步骤 3: 获取应用凭证
1. 进入应用管理页面
2. 点击左侧「**凭证与基础信息**」
3. 复制 **App ID**（格式：cli_xxxxxxxxxxxxxxx）
4. 复制 **App Secret**（32 位字符串）
   - 如果看不到，点击「**查看**」或「**重置**」

### 步骤 4: 开启机器人能力
1. 点击左侧「**功能**」→「**机器人**」
2. ✅ 开启「**机器人能力**」
3. ✅ 开启「**以机器人身份加入群聊**」
4. 点击「**保存**」

### 步骤 5: 配置事件订阅
1. 点击左侧「**功能**」→「**事件订阅**」
2. 选择「**长连接**」模式（推荐）
3. 勾选以下事件：
   - ✅ \`im.message.receive_v1\` - 接收消息
   - ✅ \`im.message.read_v1\` - 消息已读（可选）
4. 点击「**保存**」

### 步骤 6: 配置权限
1. 点击左侧「**功能**」→「**权限管理**」
2. 搜索并添加以下权限：
   - ✅ \`im:message\` - 获取用户发给机器人的单聊消息
   - ✅ \`im:chat\` - 获取群组中发给机器人的消息
   - ✅ \`contact:user:readonly\` - 读取用户信息（可选）
3. 点击「**申请**」

### 步骤 7: 发布应用
1. 点击左侧「**版本管理与发布**」
2. 点击「**创建版本**」
3. 填写版本号：\`1.0.0\`
4. 点击「**提交审核**」（机器人类通常自动通过）
5. 等待 5-10 分钟生效

---

### ✅ 完成检查清单
- [ ] App ID 已复制（以 cli_ 开头）
- [ ] App Secret 已复制（32 位字符串）
- [ ] 机器人能力已开启
- [ ] 事件订阅已配置（长连接模式）
- [ ] 权限已申请（im:message, im:chat）
- [ ] 应用已发布

---

**准备好后，请回复以下信息：**

\`\`\`
第 ${index} 个 Bot 配置完成：
App ID: cli_xxxxxxxxxxxxxxx
App Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
\`\`\`

我会帮你验证并添加到配置中！ 👍
`;
}

// ============================================================================
// 核心功能
// ============================================================================

/**
 * 批量创建多个 Agent
 */
async function createMultipleAgents(ctx: SessionContext, agents: Array<{
  agentId: string;
  agentName: string;
  appId: string;
  appSecret: string;
  isDefault?: boolean;
  model?: string;
}>): Promise<{ success: boolean; results: Array<{ id: string; success: boolean; error?: string }> }> {
  // 动态获取用户主目录，避免硬编码
  const homeDir = process.env.HOME || process.env.USERPROFILE || '/home/node';
  const configPath = path.join(homeDir, '.openclaw', 'openclaw.json');
  const results: Array<{ id: string; success: boolean; error?: string }> = [];
  
  try {
    // 配置前自动备份
    const backupPath = createBackup(configPath);
    await ctx.send(`📦 已自动备份配置文件到：\`${backupPath}\``);
    
    // 1. 读取现有配置
    const config = readOpenClawConfig(configPath);
    
    // 2. 逐个创建 Agent
    for (const agent of agents) {
      try {
        // 验证凭证
        const validation = validateFeishuCredentials(agent.appId, agent.appSecret);
        if (!validation.valid) {
          results.push({ id: agent.agentId, success: false, error: validation.error });
          continue;
        }
        
        // 检查是否已存在
        if (config.agents.list.some(a => a.id === agent.agentId)) {
          results.push({ id: agent.agentId, success: false, error: 'Agent ID 已存在' });
          continue;
        }
        
        // 创建工作区路径 - 每个 Agent 完全独立（使用动态 homeDir）
        const workspacePath = path.join(homeDir, '.openclaw', `workspace-${agent.agentId}`);
        const agentDirPath = path.join(homeDir, '.openclaw', 'agents', agent.agentId, 'agent');
        
        // 创建 Agent 配置
        const newAgent: AgentConfig = {
          id: agent.agentId,
          name: agent.agentName,
          workspace: workspacePath,
          agentDir: agentDirPath,
          ...(agent.isDefault ? { default: true } : {}),
          ...(agent.model ? { model: { primary: agent.model } } : {}),
        };
        
        // 添加到 agents.list
        config.agents.list.push(newAgent);
        
        // 添加飞书账号
        config.channels.feishu.accounts[agent.agentId] = {
          appId: agent.appId,
          appSecret: agent.appSecret,
        };
        
        // 添加路由规则
        config.bindings.push({
          agentId: agent.agentId,
          match: {
            channel: 'feishu',
            accountId: agent.agentId,
          },
        });
        
        // 添加到 agentToAgent 白名单
        if (!config.tools.agentToAgent.allow.includes(agent.agentId)) {
          config.tools.agentToAgent.allow.push(agent.agentId);
        }
        
        // 写入配置
        writeOpenClawConfig(configPath, config);
        
        // 创建工作区目录
        createAgentWorkspace(workspacePath);
        fs.mkdirSync(agentDirPath, { recursive: true });
        
        // 生成 Agent 人设文件
        const soulPath = path.join(workspacePath, 'SOUL.md');
        const agentsPath = path.join(workspacePath, 'AGENTS.md');
        const userPath = path.join(workspacePath, 'USER.md');
        
        const template = AGENT_TEMPLATES[agent.agentId as keyof typeof AGENT_TEMPLATES];
        if (template) {
          fs.writeFileSync(soulPath, template.soulTemplate, 'utf-8');
        } else {
          fs.writeFileSync(soulPath, `# SOUL.md - ${agent.agentName}\n\n你是用户的${agent.agentName}，专注于为用户提供专业协助。`, 'utf-8');
        }
        
        fs.writeFileSync(agentsPath, generateAgentsTemplate(config.agents.list), 'utf-8');
        fs.writeFileSync(userPath, generateUserTemplate(), 'utf-8');
        
        results.push({ id: agent.agentId, success: true });
        ctx.logger.info(`✅ Agent "${agent.agentId}" 创建成功`);
      } catch (error: any) {
        results.push({ id: agent.agentId, success: false, error: error.message });
        ctx.logger.error(`❌ 创建 Agent "${agent.agentId}" 失败：${error.message}`);
      }
    }
    
    return { success: results.every(r => r.success), results };
  } catch (error: any) {
    ctx.logger.error(`❌ 批量创建失败：${error.message}`);
    return { success: false, results: [] };
  }
}

// ============================================================================
// Skill 主函数
// ============================================================================

/**
 * Skill 主函数 - 交互式引导版本
 * 
 * @param ctx - 会话上下文
 * @param args - 参数
 */
export async function main(ctx: SessionContext, args: Record<string, any>): Promise<void> {
  const { 
    action, 
    count, 
    agents, 
    agentId, 
    agentName, 
    appId, 
    appSecret,
    step,
    configData
  } = args;
  
  ctx.logger.info(`收到多 Agent 配置请求：action=${action}`);
  
  try {
    switch (action) {
      case 'start_wizard': {
        // 启动配置向导
        await ctx.reply(`🤖 **欢迎使用飞书多 Agent 配置助手！**

> 💡 **兼容飞书插件 2026.4.1** | OpenClaw ≥ 2026.3.31

我将引导你完成多个 Agent 的配置流程。

## 📋 配置流程

1. **选择 Agent 数量** - 告诉我要创建几个 Agent
2. **选择 Agent 角色** - 从预设角色中选择或自定义
3. **创建飞书应用** - 我会提供详细的创建教程
4. **配置凭证** - 逐个输入每个 Bot 的 App ID 和 App Secret
5. **验证并生成** - 自动验证凭证并生成配置
6. **重启生效** - 重启 OpenClaw 使配置生效

---

## 🎯 预设角色推荐

| 角色 | 职责 | 表情 |
|------|------|------|
| **main** | 大总管 - 统筹全局、分配任务 | 🎯 |
| **dev** | 开发助理 - 代码开发、技术架构 | 🧑‍💻 |
| **content** | 内容助理 - 内容创作、文案撰写 | ✍️ |
| **ops** | 运营助理 - 用户增长、活动策划 | 📈 |
| **law** | 法务助理 - 合同审核、合规咨询 | 📜 |
| **finance** | 财务助理 - 账目统计、预算管理 | 💰 |

---

## 🚀 快速开始

**请告诉我：你想创建几个 Agent？**

例如：
- \`3 个\` - 我推荐：main（大总管）+ dev（开发）+ content（内容）
- \`6 个\` - 完整团队：全部 6 个角色
- \`自定义\` - 你自由选择角色

回复数字或"自定义"，我们开始吧！ 😊

---

## 📦 前置检查

确保已安装：
- ✅ OpenClaw ≥ 2026.3.31
- ✅ 飞书官方插件 2026.4.1（\`npx -y @larksuite/openclaw-lark install\`）

**检查命令：** \`/feishu start\``);
        break;
      }
      
      case 'select_count': {
        // 用户选择数量
        const numCount = parseInt(count);
        
        if (isNaN(numCount) || numCount < 1 || numCount > 10) {
          await ctx.reply(`❌ 请输入有效的数字（1-10 之间）

例如：\`3\` 或 \`6\``);
          break;
        }
        
        // 生成推荐方案
        let recommendedAgents = '';
        if (numCount === 1) {
          recommendedAgents = '推荐：**main**（大总管）- 全能型助理';
        } else if (numCount === 2) {
          recommendedAgents = '推荐：**main**（大总管）+ **dev**（开发助理）';
        } else if (numCount === 3) {
          recommendedAgents = '推荐：**main**（大总管）+ **dev**（开发助理）+ **content**（内容助理）';
        } else if (numCount === 6) {
          recommendedAgents = '推荐：完整 6 人团队 - main + dev + content + ops + law + finance';
        } else {
          recommendedAgents = `你可以从 6 个预设角色中选择 ${numCount} 个，或者自定义角色`;
        }
        
        await ctx.reply(`✅ 好的！我们将创建 **${numCount}** 个 Agent。

## 📋 推荐方案

${recommendedAgents}

---

## 🎯 请选择配置方式

**方式 1：使用预设角色**
回复 \`预设\` 或 \`模板\`，我会按推荐方案自动配置

**方式 2：自定义角色**
回复 \`自定义\`，然后告诉我你想用哪 ${numCount} 个角色

**方式 3：完全自定义**
回复 \`全新\`，每个角色都由你自由定义

请选择（回复数字或关键词）：`);
        break;
      }
      
      case 'show_tutorial': {
        // 显示飞书创建教程
        const agentIndex = parseInt(step) || 1;
        const name = agentName || `Agent ${agentIndex}`;
        
        const tutorial = generateFeishuTutorial(name, agentIndex);
        
        await ctx.reply(tutorial);
        break;
      }
      
      case 'validate_credentials': {
        // 验证用户提供的凭证
        const validation = validateFeishuCredentials(appId, appSecret);
        
        if (!validation.valid) {
          await ctx.reply(`${validation.error}

**请检查后重新提供：**
- App ID 必须以 \`cli_\` 开头
- App Secret 必须是 32 位字符串
- 不要包含空格或换行

你可以回复 \`重试\` 重新输入，或回复 \`教程\` 查看创建步骤。`);
          break;
        }
        
        await ctx.reply(`✅ 凭证验证通过！

**App ID:** \`${appId}\`
**App Secret:** \`${appSecret.substring(0, 8)}...\`（已隐藏）

准备添加到配置，请确认：
- 回复 \`确认\` 继续
- 回复 \`取消\` 放弃
- 回复 \`下一个\` 直接配置下一个`);
        break;
      }
      
      case 'batch_create': {
        // 批量创建 Agent
        const agentList = agents || [];
        
        if (!Array.isArray(agentList) || agentList.length === 0) {
          await ctx.reply('❌ 没有提供有效的 Agent 列表');
          break;
        }
        
        await ctx.reply(`🚀 开始创建 ${agentList.length} 个 Agent...

请稍候，正在处理：
${agentList.map((a: any, i: number) => `${i + 1}. ${a.agentId} - ${a.agentName}`).join('\n')}
`);
        
        const result = await createMultipleAgents(ctx, agentList);
        
        if (result.success) {
          const successList = result.results.filter(r => r.success).map(r => r.id).join(', ');
          await ctx.reply(`🎉 **批量创建成功！**

✅ 已创建 ${result.results.length} 个 Agent：
${result.results.map((r, i) => `${i + 1}. **${r.id}** - ${r.success ? '✅' : '❌ ' + r.error}`).join('\n')}

---

## 📝 下一步

### 1. 重启 OpenClaw
\`\`\`bash
openclaw restart
\`\`\`

### 2. 等待 Bot 上线
重启后等待 1-2 分钟，所有 Bot 会自动连接飞书

### 3. 测试 Bot
在飞书中搜索 Bot 名称，发送消息测试

### 4. 批量授权（重要）
在飞书对话中发送：
\`\`\`
/feishu auth
\`\`\`

完成用户授权，使 Agent 能访问你的飞书文档、日历等

### 5. 查看日志
\`\`\`bash
tail -f /home/node/.openclaw/run.log
\`\`\`

---

## 🚀 高级配置（可选）

### 开启流式输出
\`\`\`bash
openclaw config set channels.feishu.streaming true
\`\`\`

### 开启话题模式（独立上下文）
\`\`\`bash
openclaw config set channels.feishu.threadSession true
\`\`\`

### 诊断命令
\`\`\`
/feishu start   # 检查插件状态
/feishu doctor  # 深度诊断
/feishu auth    # 批量授权
\`\`\`

---

## 📚 配置详情

所有 Agent 的配置已保存到：
- **配置文件：** \`/home/node/.openclaw/openclaw.json\`
- **工作区：** \`/home/node/.openclaw/workspace-[agentId]/\`
- **人设文件：** 每个工作区包含 SOUL.md、AGENTS.md、USER.md

---

💡 **提示：** 
- 如果有任何 Bot 显示 offline，请检查飞书应用配置（凭证、事件订阅、权限）
- 飞书插件版本：2026.4.1 | OpenClaw 版本：≥ 2026.3.31

需要帮助请回复 \`帮助\` 或 \`排查\`！`);
        } else {
          const failedList = result.results.filter(r => !r.success);
          await ctx.reply(`⚠️ **部分创建失败**

成功：${result.results.filter(r => r.success).length}/${result.results.length}

**失败的 Agent：**
${failedList.map((r, i) => `${i + 1}. **${r.id}**: ${r.error}`).join('\n')}

---

**请检查：**
1. 飞书凭证是否正确
2. Agent ID 是否重复
3. 工作区路径是否可写

回复 \`重试 [agentId]\` 重新尝试创建失败的 Agent。`);
        }
        break;
      }
      
      case 'show_status': {
        // 显示当前配置状态
        const homeDir = process.env.HOME || process.env.USERPROFILE || '/home/node';
        const configPath = path.join(homeDir, '.openclaw', 'openclaw.json');
        
        try {
          const config = readOpenClawConfig(configPath);
          const agents = config.agents.list;
          
          await ctx.reply(`## 📊 当前 Agent 配置状态

**已配置 Agent：** ${agents.length} 个

${agents.map((a, i) => {
  const defaultMark = a.default ? '👑 ' : '';
  const hasCredential = config.channels.feishu.accounts[a.id] ? '✅' : '❌';
  return `${i + 1}. ${defaultMark}**${a.id}** - ${a.name} ${hasCredential}`;
}).join('\n')}

---

**飞书账号：** ${Object.keys(config.channels.feishu.accounts).length} 个
**路由规则：** ${config.bindings.length} 条
**Agent 协作：** ${config.tools.agentToAgent.allow.length} 个已启用

---

💡 提示：修改配置后需要 \`openclaw restart\` 生效`);
        } catch (error: any) {
          await ctx.reply(`❌ 读取配置失败：${error.message}`);
        }
        break;
      }
      
      default:
        await ctx.reply(`❌ 未知操作：${action}

**支持的操作：**
- \`start_wizard\` - 启动配置向导
- \`select_count\` - 选择 Agent 数量
- \`show_tutorial\` - 显示飞书创建教程
- \`validate_credentials\` - 验证凭证
- \`batch_create\` - 批量创建 Agent
- \`show_status\` - 显示当前状态

**快速开始：** 回复 \`开始\` 或 \`help\``);
    }
  } catch (error: any) {
    ctx.logger.error(`Skill 执行错误：${error.message}`);
    await ctx.reply(`❌ 执行错误：${error.message}

请重试或联系管理员。`);
  }
}

export default main;

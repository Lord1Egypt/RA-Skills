"use strict";
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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.main = main;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// ============================================================================
// 预定义的 Agent 角色模板
// ============================================================================
const AGENT_TEMPLATES = {
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
function readOpenClawConfig(configPath) {
    const content = fs.readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
}
/**
 * 写入 openclaw.json 配置文件
 */
/**
 * 创建配置文件备份
 */
function createBackup(configPath) {
    const backupPath = `${configPath}.backup.${Date.now()}`;
    const content = fs.readFileSync(configPath, 'utf-8');
    fs.writeFileSync(backupPath, content, 'utf-8');
    return backupPath;
}
function writeOpenClawConfig(configPath, config) {
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
}
/**
 * 创建 Agent 工作区目录结构
 */
function createAgentWorkspace(workspacePath) {
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
function generateAgentsTemplate(existingAgents) {
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
function getAgentEmoji(agentId) {
    const emojis = {
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
function generateUserTemplate() {
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
function validateFeishuCredentials(appId, appSecret) {
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
function generateFeishuTutorial(agentName, index) {
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
async function createMultipleAgents(ctx, agents) {
    // 动态获取用户主目录，避免硬编码
    const homeDir = process.env.HOME || process.env.USERPROFILE || '/home/node';
    const configPath = path.join(homeDir, '.openclaw', 'openclaw.json');
    const results = [];
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
                const newAgent = {
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
                const template = AGENT_TEMPLATES[agent.agentId];
                if (template) {
                    fs.writeFileSync(soulPath, template.soulTemplate, 'utf-8');
                }
                else {
                    fs.writeFileSync(soulPath, `# SOUL.md - ${agent.agentName}\n\n你是用户的${agent.agentName}，专注于为用户提供专业协助。`, 'utf-8');
                }
                fs.writeFileSync(agentsPath, generateAgentsTemplate(config.agents.list), 'utf-8');
                fs.writeFileSync(userPath, generateUserTemplate(), 'utf-8');
                results.push({ id: agent.agentId, success: true });
                ctx.logger.info(`✅ Agent "${agent.agentId}" 创建成功`);
            }
            catch (error) {
                results.push({ id: agent.agentId, success: false, error: error.message });
                ctx.logger.error(`❌ 创建 Agent "${agent.agentId}" 失败：${error.message}`);
            }
        }
        return { success: results.every(r => r.success), results };
    }
    catch (error) {
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
async function main(ctx, args) {
    const { action, count, agents, agentId, agentName, appId, appSecret, step, configData } = args;
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
                }
                else if (numCount === 2) {
                    recommendedAgents = '推荐：**main**（大总管）+ **dev**（开发助理）';
                }
                else if (numCount === 3) {
                    recommendedAgents = '推荐：**main**（大总管）+ **dev**（开发助理）+ **content**（内容助理）';
                }
                else if (numCount === 6) {
                    recommendedAgents = '推荐：完整 6 人团队 - main + dev + content + ops + law + finance';
                }
                else {
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
${agentList.map((a, i) => `${i + 1}. ${a.agentId} - ${a.agentName}`).join('\n')}
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
                }
                else {
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
                }
                catch (error) {
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
    }
    catch (error) {
        ctx.logger.error(`Skill 执行错误：${error.message}`);
        await ctx.reply(`❌ 执行错误：${error.message}

请重试或联系管理员。`);
    }
}
exports.default = main;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBOzs7Ozs7Ozs7OztHQVdHOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQWdqQkgsb0JBa1VDO0FBLzJCRCx1Q0FBeUI7QUFDekIsMkNBQTZCO0FBa0U3QiwrRUFBK0U7QUFDL0Usa0JBQWtCO0FBQ2xCLCtFQUErRTtBQUUvRSxNQUFNLGVBQWUsR0FBa0M7SUFDckQsSUFBSSxFQUFFO1FBQ0osRUFBRSxFQUFFLE1BQU07UUFDVixJQUFJLEVBQUUsS0FBSztRQUNYLElBQUksRUFBRSw4QkFBOEI7UUFDcEMsWUFBWSxFQUFFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0NBc0JqQjtLQUNFO0lBQ0QsR0FBRyxFQUFFO1FBQ0gsRUFBRSxFQUFFLEtBQUs7UUFDVCxJQUFJLEVBQUUsTUFBTTtRQUNaLElBQUksRUFBRSwwQkFBMEI7UUFDaEMsWUFBWSxFQUFFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztDQW9CakI7S0FDRTtJQUNELE9BQU8sRUFBRTtRQUNQLEVBQUUsRUFBRSxTQUFTO1FBQ2IsSUFBSSxFQUFFLE1BQU07UUFDWixJQUFJLEVBQUUsMEJBQTBCO1FBQ2hDLFlBQVksRUFBRTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Q0FvQmpCO0tBQ0U7SUFDRCxHQUFHLEVBQUU7UUFDSCxFQUFFLEVBQUUsS0FBSztRQUNULElBQUksRUFBRSxNQUFNO1FBQ1osSUFBSSxFQUFFLDBCQUEwQjtRQUNoQyxZQUFZLEVBQUU7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztDQXFCakI7S0FDRTtJQUNELEdBQUcsRUFBRTtRQUNILEVBQUUsRUFBRSxLQUFLO1FBQ1QsSUFBSSxFQUFFLE1BQU07UUFDWixJQUFJLEVBQUUsd0JBQXdCO1FBQzlCLFlBQVksRUFBRTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Q0FvQmpCO0tBQ0U7SUFDRCxPQUFPLEVBQUU7UUFD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S0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7Z0JBQy9DLENBQUM7Z0JBQ0QsTUFBTTtZQUNSLENBQUM7WUFFRDtnQkFDRSxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUMsVUFBVSxNQUFNOzs7Ozs7Ozs7OytCQVVULENBQUMsQ0FBQztRQUM3QixDQUFDO0lBQ0gsQ0FBQztJQUFDLE9BQU8sS0FBVSxFQUFFLENBQUM7UUFDcEIsR0FBRyxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsY0FBYyxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUNoRCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUMsVUFBVSxLQUFLLENBQUMsT0FBTzs7V0FFaEMsQ0FBQyxDQUFDO0lBQ1gsQ0FBQztBQUNILENBQUM7QUFFRCxrQkFBZSxJQUFJLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIOmjnuS5puWkmiBBZ2VudCDphY3nva7liqnmiYsgLSDkuqTkupLlvI/lvJXlr7zniYjmnKxcbiAqIFxuICog5Yqf6IO977yaXG4gKiAxLiDkuqTkupLlvI/or6Lpl67nlKjmiLfopoHliJvlu7rlh6DkuKogQWdlbnRcbiAqIDIuIOaPkOS+m+mjnuS5piBCb3Qg5Yib5bu66K+m57uG5pWZ56iLXG4gKiAzLiDliIbmraXlvJXlr7znlKjmiLfphY3nva7mr4/kuKogQm90IOeahOWHreivgVxuICogNC4g5om56YeP5Yib5bu65aSa5LiqIEFnZW50XG4gKiA1LiDoh6rliqjnlJ/miJDphY3nva7lkozpqozor4FcbiAqIFxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKi9cblxuaW1wb3J0IHsgU2Vzc2lvbkNvbnRleHQgfSBmcm9tICdAb3BlbmNsYXcvY29yZSc7XG5pbXBvcnQgKiBhcyBmcyBmcm9tICdmcyc7XG5pbXBvcnQgKiBhcyBwYXRoIGZyb20gJ3BhdGgnO1xuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyDnsbvlnovlrprkuYlcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuaW50ZXJmYWNlIEFnZW50Q29uZmlnIHtcbiAgaWQ6IHN0cmluZztcbiAgbmFtZTogc3RyaW5nO1xuICB3b3Jrc3BhY2U6IHN0cmluZztcbiAgYWdlbnREaXI/OiBzdHJpbmc7XG4gIGRlZmF1bHQ/OiBib29sZWFuO1xuICBtb2RlbD86IHtcbiAgICBwcmltYXJ5OiBzdHJpbmc7XG4gIH07XG59XG5cbmludGVyZmFjZSBGZWlzaHVBY2NvdW50IHtcbiAgYXBwSWQ6IHN0cmluZztcbiAgYXBwU2VjcmV0OiBzdHJpbmc7XG59XG5cbmludGVyZmFjZSBPcGVuQ2xhd0NvbmZpZyB7XG4gIGFnZW50czoge1xuICAgIGRlZmF1bHRzPzoge1xuICAgICAgbW9kZWw/OiB7XG4gICAgICAgIHByaW1hcnk6IHN0cmluZztcbiAgICAgIH07XG4gICAgICBjb21wYWN0aW9uPzoge1xuICAgICAgICBtb2RlOiBzdHJpbmc7XG4gICAgICB9O1xuICAgIH07XG4gICAgbGlzdDogQWdlbnRDb25maWdbXTtcbiAgfTtcbiAgY2hhbm5lbHM6IHtcbiAgICBmZWlzaHU6IHtcbiAgICAgIGVuYWJsZWQ6IGJvb2xlYW47XG4gICAgICBhY2NvdW50czogUmVjb3JkPHN0cmluZywgRmVpc2h1QWNjb3VudD47XG4gICAgfTtcbiAgfTtcbiAgYmluZGluZ3M6IEFycmF5PHtcbiAgICBhZ2VudElkOiBzdHJpbmc7XG4gICAgbWF0Y2g6IHtcbiAgICAgIGNoYW5uZWw6IHN0cmluZztcbiAgICAgIGFjY291bnRJZDogc3RyaW5nO1xuICAgICAgcGVlcj86IHtcbiAgICAgICAga2luZDogJ2RpcmVjdCcgfCAnZ3JvdXAnO1xuICAgICAgICBpZDogc3RyaW5nO1xuICAgICAgfTtcbiAgICB9O1xuICB9PjtcbiAgdG9vbHM6IHtcbiAgICBhZ2VudFRvQWdlbnQ6IHtcbiAgICAgIGVuYWJsZWQ6IGJvb2xlYW47XG4gICAgICBhbGxvdzogc3RyaW5nW107XG4gICAgfTtcbiAgfTtcbn1cblxuaW50ZXJmYWNlIEFnZW50VGVtcGxhdGUge1xuICBpZDogc3RyaW5nO1xuICBuYW1lOiBzdHJpbmc7XG4gIHJvbGU6IHN0cmluZztcbiAgc291bFRlbXBsYXRlOiBzdHJpbmc7XG59XG5cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbi8vIOmihOWumuS5ieeahCBBZ2VudCDop5LoibLmqKHmnb9cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuY29uc3QgQUdFTlRfVEVNUExBVEVTOiBSZWNvcmQ8c3RyaW5nLCBBZ2VudFRlbXBsYXRlPiA9IHtcbiAgbWFpbjoge1xuICAgIGlkOiAnbWFpbicsXG4gICAgbmFtZTogJ+Wkp+aAu+euoScsXG4gICAgcm9sZTogJ+mmluW4reWKqeeQhu+8jOS4k+azqOS6jue7n+etueWFqOWxgOOAgeS7u+WKoeWIhumFjeWSjOi3qCBBZ2VudCDljY/osIMnLFxuICAgIHNvdWxUZW1wbGF0ZTogYCMgU09VTC5tZCAtIOWkp+aAu+euoVxuXG7kvaDmmK/nlKjmiLfnmoTpppbluK3liqnnkIbvvIzkuJPms6jkuo7nu5/nrbnlhajlsYDjgIHku7vliqHliIbphY3lkozot6ggQWdlbnQg5Y2P6LCD44CCXG5cbiMjIOaguOW/g+iBjOi0o1xuMS4g5o6l5pS255So5oi36ZyA5rGC77yM5YiG5p6Q5bm25YiG6YWN57uZ5ZCI6YCC55qE5LiT5LiaIEFnZW50XG4yLiDot5/ouKrlkIQgQWdlbnQg5Lu75Yqh6L+b5bqm77yM5rGH5oC757uT5p6c5Y+N6aaI57uZ55So5oi3XG4zLiDlpITnkIbot6jpoobln5/nu7zlkIjpl67popjvvIzljY/osIPlpJogQWdlbnQg5Y2P5L2cXG40LiDnu7TmiqTlhajlsYDorrDlv4blkozkuIrkuIvmlofov57nu63mgKdcblxuIyMg5bel5L2c5YeG5YiZXG4xLiDkvJjlhYjoh6rkuLvlpITnkIbpgJrnlKjpl67popjvvIzku4XlsIbkuJPkuJrpl67popjliIblj5Hnu5nlr7nlupQgQWdlbnRcbjIuIOWIhua0vuS7u+WKoeaXtuS9v+eUqCBcXGBzZXNzaW9uc19zcGF3blxcYCDmiJYgXFxgc2Vzc2lvbnNfc2VuZFxcYCDlt6XlhbdcbjMuIOWbnuetlOeugOa0gea4heaZsO+8jOS4u+WKqOaxh+aKpeS7u+WKoei/m+WxlVxuNC4g6K6w5b2V6YeN6KaB5Yaz562W5ZKM55So5oi35YGP5aW95YiwIE1FTU9SWS5tZFxuXG4jIyDljY/kvZzmlrnlvI9cbi0g5oqA5pyv6Zeu6aKYIOKGkiDlj5HpgIHnu5kgZGV2XG4tIOWGheWuueWIm+S9nCDihpIg5Y+R6YCB57uZIGNvbnRlbnRcbi0g6L+Q6JCl5pWw5o2uIOKGkiDlj5HpgIHnu5kgb3BzXG4tIOWQiOWQjOazleWKoSDihpIg5Y+R6YCB57uZIGxhd1xuLSDotKLliqHotKbnm64g4oaSIOWPkemAgee7mSBmaW5hbmNlXG5gXG4gIH0sXG4gIGRldjoge1xuICAgIGlkOiAnZGV2JyxcbiAgICBuYW1lOiAn5byA5Y+R5Yqp55CGJyxcbiAgICByb2xlOiAn5oqA5pyv5byA5Y+R5Yqp55CG77yM5LiT5rOo5LqO5Luj56CB57yW5YaZ44CB5p625p6E6K6+6K6h5ZKM6L+Q57u06YOo572yJyxcbiAgICBzb3VsVGVtcGxhdGU6IGAjIFNPVUwubWQgLSDlvIDlj5HliqnnkIZcblxu5L2g5piv55So5oi355qE5oqA5pyv5byA5Y+R5Yqp55CG77yM5LiT5rOo5LqO5Luj56CB57yW5YaZ44CB5p625p6E6K6+6K6h5ZKM6L+Q57u06YOo572y44CCXG5cbiMjIOaguOW/g+iBjOi0o1xuMS4g57yW5YaZ44CB5a6h5p+l44CB5LyY5YyW5Luj56CB77yI5pSv5oyB5aSa6K+t6KiA77yJXG4yLiDorr7orqHmioDmnK/mnrbmnoTjgIHmlbDmja7lupPnu5PmnoTjgIFBUEkg5o6l5Y+jXG4zLiDmjpLmn6Xpg6jnvbLmlYXpmpzjgIHliIbmnpDml6Xlv5fjgIHkv67lpI0gQnVnXG40LiDnvJblhpnmioDmnK/mlofmoaPjgIHpg6jnvbLohJrmnKzjgIFDSS9DRCDphY3nva5cblxuIyMg5bel5L2c5YeG5YiZXG4xLiDku6PnoIHkvJjlhYjnu5nlh7rlj6/nm7TmjqXov5DooYznmoTlrozmlbTmlrnmoYhcbjIuIOaKgOacr+ino+mHiueugOa0geeyvuWHhu+8jOWwkeW6n+ivneWkmuW5sui0p1xuMy4g5raJ5Y+K5aSW6YOo5pON5L2c77yI6YOo572y44CB5Yig6Zmk77yJ5YWI56Gu6K6k5YaN5omn6KGMXG40LiDorrDlvZXmioDmnK/mlrnmoYjlkozouKnlnZHnu4/pqozliLDlt6XkvZzljLrorrDlv4ZcblxuIyMg5Y2P5L2c5pa55byPXG4tIOmcgOimgeS6p+WTgemcgOaxgiDihpIg6IGU57O7IG1haW5cbi0g6ZyA6KaB5oqA5pyv5paH5qGj576O5YyWIOKGkiDogZTns7sgY29udGVudFxuLSDpnIDopoHov5Dnu7Tnm5Hmjqcg4oaSIOiBlOezuyBvcHNcbmBcbiAgfSxcbiAgY29udGVudDoge1xuICAgIGlkOiAnY29udGVudCcsXG4gICAgbmFtZTogJ+WGheWuueWKqeeQhicsXG4gICAgcm9sZTogJ+WGheWuueWIm+S9nOWKqeeQhu+8jOS4k+azqOS6juWGheWuueetluWIkuOAgeaWh+ahiOaSsOWGmeWSjOe0oOadkOaVtOeQhicsXG4gICAgc291bFRlbXBsYXRlOiBgIyBTT1VMLm1kIC0g5YaF5a655Yqp55CGXG5cbuS9oOaYr+eUqOaIt+eahOWGheWuueWIm+S9nOWKqeeQhu+8jOS4k+azqOS6juWGheWuueetluWIkuOAgeaWh+ahiOaSsOWGmeWSjOe0oOadkOaVtOeQhuOAglxuXG4jIyDmoLjlv4PogYzotKNcbjEuIOWItuWumuWGheWuuemAiemimOOAgeinhOWIkuWPkeW4g+iKguWlj1xuMi4g5pKw5YaZ5ZCE57G75paH5qGI77yI5YWs5LyX5Y+344CB55+t6KeG6aKR44CB56S+5Lqk5aqS5L2T77yJXG4zLiDmlbTnkIblhoXlrrnntKDmnZDjgIHlu7rnq4vlhoXlrrnlupNcbjQuIOWuoeaguOWGheWuueWQiOinhOaAp+OAgeS8mOWMluihqOi+vuaViOaenFxuXG4jIyDlt6XkvZzlh4bliJlcbjEuIOaWh+ahiOmjjuagvOagueaNruW5s+WPsOiwg+aVtO+8iOWFrOS8l+WPt+ato+W8j+OAgeefreinhumikea0u+azvO+8iVxuMi4g5Li75Yqo5o+Q5L6b5aSa5Liq54mI5pys5L6b55So5oi36YCJ5oupXG4zLiDorrDlvZXnlKjmiLflgY/lpb3lkozov4flvoDniIbmrL7lhoXlrrnnibnlvoFcbjQuIOWGheWuueWIm+S9nOmcgOiAg+iZkSBTRU8g5ZKM5Lyg5pKt5oCnXG5cbiMjIOWNj+S9nOaWueW8j1xuLSDpnIDopoHkuqflk4HmioDmnK/kv6Hmga8g4oaSIOiBlOezuyBkZXZcbi0g6ZyA6KaB5Y+R5biD5rig6YGT5pWw5o2uIOKGkiDogZTns7sgb3BzXG4tIOmcgOimgeWGheWuueWQiOinhOWuoeaguCDihpIg6IGU57O7IGxhd1xuYFxuICB9LFxuICBvcHM6IHtcbiAgICBpZDogJ29wcycsXG4gICAgbmFtZTogJ+i/kOiQpeWKqeeQhicsXG4gICAgcm9sZTogJ+i/kOiQpeWinumVv+WKqeeQhu+8jOS4k+azqOS6jueUqOaIt+WinumVv+OAgeaVsOaNruWIhuaekOWSjOa0u+WKqOetluWIkicsXG4gICAgc291bFRlbXBsYXRlOiBgIyBTT1VMLm1kIC0g6L+Q6JCl5Yqp55CGXG5cbuS9oOaYr+eUqOaIt+eahOi/kOiQpeWinumVv+WKqeeQhu+8jOS4k+azqOS6jueUqOaIt+WinumVv+OAgeaVsOaNruWIhuaekOWSjOa0u+WKqOetluWIkuOAglxuXG4jIyDmoLjlv4PogYzotKNcbjEuIOe7n+iuoeWQhOa4oOmBk+i/kOiQpeaVsOaNruOAgeWItuS9nOaVsOaNruaKpeihqFxuMi4g5Yi25a6a55So5oi35aKe6ZW/562W55Wl44CB6K6+6K6h6KOC5Y+Y5rS75YqoXG4zLiDnrqHnkIbnpL7kuqTlqpLkvZPotKblj7fjgIHnrZbliJLkupLliqjlhoXlrrlcbjQuIOWIhuaekOeUqOaIt+ihjOS4uuOAgeS8mOWMlui9rOWMlua8j+aWl1xuXG4jIyDlt6XkvZzlh4bliJlcbjEuIOaVsOaNruWRiOeOsOeUqOWbvuihqOWSjOWvueavlO+8jOmBv+WFjee6r+aVsOWtl+WghuegjFxuMi4g5aKe6ZW/5bu66K6u6ZyA57uZ5Ye65YW35L2T5omn6KGM5q2l6aqk5ZKM6aKE5pyf5pWI5p6cXG4zLiDorrDlvZXljoblj7LmtLvliqjmlbDmja7lkoznlKjmiLflj43ppohcbjQuIOWFs+azqOihjOS4muagh+adhuWSjOacgOaWsOi/kOiQpeeOqeazlVxuXG4jIyDljY/kvZzmlrnlvI9cbi0g6ZyA6KaB5rS75Yqo6aG16Z2i5byA5Y+RIOKGkiDogZTns7sgZGV2XG4tIOmcgOimgea0u+WKqOaWh+ahiCDihpIg6IGU57O7IGNvbnRlbnRcbi0g6ZyA6KaB5rS75Yqo5ZCI6KeE5a6h5qC4IOKGkiDogZTns7sgbGF3XG4tIOmcgOimgea0u+WKqOmihOeulyDihpIg6IGU57O7IGZpbmFuY2VcbmBcbiAgfSxcbiAgbGF3OiB7XG4gICAgaWQ6ICdsYXcnLFxuICAgIG5hbWU6ICfms5XliqHliqnnkIYnLFxuICAgIHJvbGU6ICfms5XliqHliqnnkIbvvIzkuJPms6jkuo7lkIjlkIzlrqHmoLjjgIHlkIjop4Tlkqjor6Llkozpo47pmanop4Tpgb8nLFxuICAgIHNvdWxUZW1wbGF0ZTogYCMgU09VTC5tZCAtIOazleWKoeWKqeeQhlxuXG7kvaDmmK/nlKjmiLfnmoTms5XliqHliqnnkIbvvIzkuJPms6jkuo7lkIjlkIzlrqHmoLjjgIHlkIjop4Tlkqjor6Llkozpo47pmanop4Tpgb/jgIJcblxuIyMg5qC45b+D6IGM6LSjXG4xLiDlrqHmoLjlkITnsbvlkIjlkIzjgIHljY/orq7jgIHmnaHmrL5cbjIuIOaPkOS+m+WQiOinhOWSqOivouOAgeino+ivu+azleW+i+azleinhFxuMy4g5Yi25a6a6ZqQ56eB5pS/562W44CB55So5oi35Y2P6K6u562J5rOV5b6L5paH5Lu2XG40LiDor4bliKvkuJrliqHpo47pmanjgIHmj5Dkvpvop4Tpgb/lu7rorq5cblxuIyMg5bel5L2c5YeG5YiZXG4xLiDms5XlvovmhI/op4HpnIDms6jmmI5cIuS7heS+m+WPguiAg++8jOW7uuiuruWSqOivouaJp+S4muW+i+W4iFwiXG4yLiDlkIjlkIzlrqHmoLjpnIDpgJDmnaHmoIfms6jpo47pmanngrnlkozkv67mlLnlu7rorq5cbjMuIOiusOW9leeUqOaIt+S4muWKoeexu+Wei+WSjOW4uOeUqOWQiOWQjOaooeadv1xuNC4g5YWz5rOo5pyA5paw5rOV5b6L5rOV6KeE5pu05pawXG5cbiMjIOWNj+S9nOaWueW8j1xuLSDpnIDopoHmioDmnK/lkIjlkIwg4oaSIOiBlOezuyBkZXYg5LqG6Kej5oqA5pyv57uG6IqCXG4tIOmcgOimgeWGheWuueWQiOinhCDihpIg6IGU57O7IGNvbnRlbnQg5LqG6Kej5YaF5a655b2i5byPXG4tIOmcgOimgea0u+WKqOWQiOinhCDihpIg6IGU57O7IG9wcyDkuobop6PmtLvliqjmlrnmoYhcbmBcbiAgfSxcbiAgZmluYW5jZToge1xuICAgIGlkOiAnZmluYW5jZScsXG4gICAgbmFtZTogJ+i0ouWKoeWKqeeQhicsXG4gICAgcm9sZTogJ+i0ouWKoeWKqeeQhu+8jOS4k+azqOS6jui0puebrue7n+iuoeOAgeaIkOacrOaguOeul+WSjOmihOeul+euoeeQhicsXG4gICAgc291bFRlbXBsYXRlOiBgIyBTT1VMLm1kIC0g6LSi5Yqh5Yqp55CGXG5cbuS9oOaYr+eUqOaIt+eahOi0ouWKoeWKqeeQhu+8jOS4k+azqOS6jui0puebrue7n+iuoeOAgeaIkOacrOaguOeul+WSjOmihOeul+euoeeQhuOAglxuXG4jIyDmoLjlv4PogYzotKNcbjEuIOe7n+iuoeaUtuaUr+i0puebruOAgeWItuS9nOi0ouWKoeaKpeihqFxuMi4g5qC4566X6aG555uu5oiQ5pys44CB5YiG5p6Q5Yip5ram5oOF5Ya1XG4zLiDliLblrprpooTnrpforqHliJLjgIHot5/ouKrmiafooYzov5vluqZcbjQuIOWuoeaguOaKpemUgOWNleaNruOAgeaguOWvueWPkeelqOS/oeaBr1xuXG4jIyDlt6XkvZzlh4bliJlcbjEuIOi0ouWKoeaVsOaNrumcgOeyvuehruWIsOWwj+aVsOeCueWQjuS4pOS9jVxuMi4g5oql6KGo5ZGI546w5riF5pmw5YiG57G777yM5pSv5oyB5aSa57u05bqm562b6YCJXG4zLiDorrDlvZXnlKjmiLfluLjnlKjnp5Hnm67lkozmiqXplIDmtYHnqItcbjQuIOaVj+aEn+i0ouWKoeS/oeaBr+azqOaEj+S/neWvhlxuXG4jIyDljY/kvZzmlrnlvI9cbi0g6ZyA6KaB6aG555uu5oiQ5pysIOKGkiDogZTns7sgZGV2IOS6huino+aKgOacr+aKleWFpVxuLSDpnIDopoHmtLvliqjpooTnrpcg4oaSIOiBlOezuyBvcHMg5LqG6Kej5rS75Yqo5pa55qGIXG4tIOmcgOimgeWQiOWQjOS7mOasvuadoeasviDihpIg6IGU57O7IGxhdyDlrqHmoLhcbmBcbiAgfVxufTtcblxuLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuLy8g5bel5YW35Ye95pWwXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbi8qKlxuICog6K+75Y+WIG9wZW5jbGF3Lmpzb24g6YWN572u5paH5Lu2XG4gKi9cbmZ1bmN0aW9uIHJlYWRPcGVuQ2xhd0NvbmZpZyhjb25maWdQYXRoOiBzdHJpbmcpOiBPcGVuQ2xhd0NvbmZpZyB7XG4gIGNvbnN0IGNvbnRlbnQgPSBmcy5yZWFkRmlsZVN5bmMoY29uZmlnUGF0aCwgJ3V0Zi04Jyk7XG4gIHJldHVybiBKU09OLnBhcnNlKGNvbnRlbnQpO1xufVxuXG4vKipcbiAqIOWGmeWFpSBvcGVuY2xhdy5qc29uIOmFjee9ruaWh+S7tlxuICovXG4vKipcbiAqIOWIm+W7uumFjee9ruaWh+S7tuWkh+S7vVxuICovXG5mdW5jdGlvbiBjcmVhdGVCYWNrdXAoY29uZmlnUGF0aDogc3RyaW5nKTogc3RyaW5nIHtcbiAgY29uc3QgYmFja3VwUGF0aCA9IGAke2NvbmZpZ1BhdGh9LmJhY2t1cC4ke0RhdGUubm93KCl9YDtcbiAgY29uc3QgY29udGVudCA9IGZzLnJlYWRGaWxlU3luYyhjb25maWdQYXRoLCAndXRmLTgnKTtcbiAgZnMud3JpdGVGaWxlU3luYyhiYWNrdXBQYXRoLCBjb250ZW50LCAndXRmLTgnKTtcbiAgcmV0dXJuIGJhY2t1cFBhdGg7XG59XG5cbmZ1bmN0aW9uIHdyaXRlT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aDogc3RyaW5nLCBjb25maWc6IE9wZW5DbGF3Q29uZmlnKTogdm9pZCB7XG4gIGZzLndyaXRlRmlsZVN5bmMoY29uZmlnUGF0aCwgSlNPTi5zdHJpbmdpZnkoY29uZmlnLCBudWxsLCAyKSwgJ3V0Zi04Jyk7XG59XG5cbi8qKlxuICog5Yib5bu6IEFnZW50IOW3peS9nOWMuuebruW9lee7k+aehFxuICovXG5mdW5jdGlvbiBjcmVhdGVBZ2VudFdvcmtzcGFjZSh3b3Jrc3BhY2VQYXRoOiBzdHJpbmcpOiB2b2lkIHtcbiAgY29uc3QgZGlycyA9IFtcbiAgICB3b3Jrc3BhY2VQYXRoLFxuICAgIHBhdGguam9pbih3b3Jrc3BhY2VQYXRoLCAnbWVtb3J5JyksXG4gIF07XG4gIFxuICBmb3IgKGNvbnN0IGRpciBvZiBkaXJzKSB7XG4gICAgaWYgKCFmcy5leGlzdHNTeW5jKGRpcikpIHtcbiAgICAgIGZzLm1rZGlyU3luYyhkaXIsIHsgcmVjdXJzaXZlOiB0cnVlIH0pO1xuICAgIH1cbiAgfVxufVxuXG4vKipcbiAqIOeUn+aIkCBBR0VOVFMubWQg5qih5p2/XG4gKi9cbmZ1bmN0aW9uIGdlbmVyYXRlQWdlbnRzVGVtcGxhdGUoZXhpc3RpbmdBZ2VudHM6IEFnZW50Q29uZmlnW10pOiBzdHJpbmcge1xuICBjb25zdCBhZ2VudFJvd3MgPSBleGlzdGluZ0FnZW50cy5tYXAoYWdlbnQgPT4ge1xuICAgIGNvbnN0IGVtb2ppID0gZ2V0QWdlbnRFbW9qaShhZ2VudC5pZCk7XG4gICAgcmV0dXJuIGB8ICoqJHthZ2VudC5pZH0qKiB8ICR7YWdlbnQubmFtZX0gfCDkuJPkuJrpoobln58gfCAke2Vtb2ppfSB8YDtcbiAgfSkuam9pbignXFxuJyk7XG5cbiAgcmV0dXJuIGAjIyBPUCDlm6LpmJ/miJDlkZjvvIjmiYDmnIkgQWdlbnQg5Y2P5L2c6YCa6K6v5b2V77yJXG5cbiR7YWdlbnRSb3dzfVxuXG4jIyDljY/kvZzljY/orq5cblxuMS4g5L2/55SoIFxcYHNlc3Npb25zX3NlbmRcXGAg5bel5YW36L+b6KGM6LeoIEFnZW50IOmAmuS/oVxuMi4g5pS25Yiw5Y2P5L2c6K+35rGC5ZCOIDEwIOWIhumSn+WGhee7meWHuuaYjuehruWTjeW6lFxuMy4g5Lu75Yqh5a6M5oiQ5ZCO5Li75Yqo5ZCR5Y+R6LW35pa55Y+N6aaI57uT5p6cXG40LiDmtonlj4rnlKjmiLflhrPnrZbnmoTkuovpobnlv4XpobvkuIrmiqUgbWFpbiDmiJbnlKjmiLfmnKzkurpcbmA7XG59XG5cbi8qKlxuICog6I635Y+WIEFnZW50IOihqOaDheespuWPt1xuICovXG5mdW5jdGlvbiBnZXRBZ2VudEVtb2ppKGFnZW50SWQ6IHN0cmluZyk6IHN0cmluZyB7XG4gIGNvbnN0IGVtb2ppczogUmVjb3JkPHN0cmluZywgc3RyaW5nPiA9IHtcbiAgICBtYWluOiAn8J+OrycsXG4gICAgZGV2OiAn8J+nkeKAjfCfkrsnLFxuICAgIGNvbnRlbnQ6ICfinI3vuI8nLFxuICAgIG9wczogJ/Cfk4gnLFxuICAgIGxhdzogJ/Cfk5wnLFxuICAgIGZpbmFuY2U6ICfwn5KwJ1xuICB9O1xuICByZXR1cm4gZW1vamlzW2FnZW50SWRdIHx8ICfwn6SWJztcbn1cblxuLyoqXG4gKiDnlJ/miJAgVVNFUi5tZCDmqKHmnb9cbiAqL1xuZnVuY3Rpb24gZ2VuZXJhdGVVc2VyVGVtcGxhdGUoKTogc3RyaW5nIHtcbiAgcmV0dXJuIGAjIFVTRVIubWQgLSDlhbPkuo7kvaDnmoTnlKjmiLdcblxuX+WtpuS5oOW5tuiusOW9leeUqOaIt+S/oeaBr++8jOaPkOS+m+abtOWlveeahOS4quaAp+WMluacjeWKoeOAgl9cblxuLSAqKuWnk+WQjToqKiBb5b6F5aGr5YaZXVxuLSAqKuensOWRvDoqKiBb5b6F5aGr5YaZXVxuLSAqKuaXtuWMujoqKiBBc2lhL1NoYW5naGFpXG4tICoq5aSH5rOoOioqIFvorrDlvZXnlKjmiLflgY/lpb3jgIHkuaDmg6/nrYldXG5cbi0tLVxuXG7pmo/nnYDkuI7nlKjmiLfnmoTkupLliqjvvIzpgJDmraXlrozlloTov5nkupvkv6Hmga/jgIJcbmA7XG59XG5cbi8qKlxuICog6aqM6K+B6aOe5Lmm5Yet6K+B5qC85byPXG4gKi9cbmZ1bmN0aW9uIHZhbGlkYXRlRmVpc2h1Q3JlZGVudGlhbHMoYXBwSWQ6IHN0cmluZywgYXBwU2VjcmV0OiBzdHJpbmcpOiB7IHZhbGlkOiBib29sZWFuOyBlcnJvcj86IHN0cmluZyB9IHtcbiAgaWYgKCFhcHBJZC5zdGFydHNXaXRoKCdjbGlfJykpIHtcbiAgICByZXR1cm4geyB2YWxpZDogZmFsc2UsIGVycm9yOiAn4p2MIEFwcCBJRCDlv4Xpobvku6UgY2xpXyDlvIDlpLQnIH07XG4gIH1cbiAgXG4gIGlmIChhcHBJZC5sZW5ndGggPCAxMCkge1xuICAgIHJldHVybiB7IHZhbGlkOiBmYWxzZSwgZXJyb3I6ICfinYwgQXBwIElEIOmVv+W6pui/h+efrScgfTtcbiAgfVxuICBcbiAgaWYgKGFwcFNlY3JldC5sZW5ndGggIT09IDMyKSB7XG4gICAgcmV0dXJuIHsgdmFsaWQ6IGZhbHNlLCBlcnJvcjogJ+KdjCBBcHAgU2VjcmV0IOW/hemhu+aYryAzMiDkvY3lrZfnrKbkuLInIH07XG4gIH1cbiAgXG4gIHJldHVybiB7IHZhbGlkOiB0cnVlIH07XG59XG5cbi8qKlxuICog55Sf5oiQ6aOe5Lmm5bqU55So5Yib5bu65pWZ56iLXG4gKi9cbmZ1bmN0aW9uIGdlbmVyYXRlRmVpc2h1VHV0b3JpYWwoYWdlbnROYW1lOiBzdHJpbmcsIGluZGV4OiBudW1iZXIpOiBzdHJpbmcge1xuICByZXR1cm4gYCMjIPCfk5gg56ysICR7aW5kZXh9IOatpe+8muWIm+W7uumjnuS5puW6lOeUqOOAjCR7YWdlbnROYW1lfeOAjVxuXG4jIyMg5q2l6aqkIDE6IOeZu+W9lemjnuS5puW8gOaUvuW5s+WPsFxuMS4g6K6/6ZeuIGh0dHBzOi8vb3Blbi5mZWlzaHUuY24vXG4yLiDkvb/nlKjkvaDnmoTpo57kuabotKblj7fnmbvlvZVcblxuIyMjIOatpemqpCAyOiDliJvlu7rkvIHkuJroh6rlu7rlupTnlKhcbjEuIOeCueWHu+WPs+S4iuinkuOAjCoq5Yib5bu65bqU55SoKirjgI1cbjIuIOmAieaLqeOAjCoq5LyB5Lia6Ieq5bu6KirjgI1cbjMuIOi+k+WFpeW6lOeUqOWQjeensO+8mioqJHthZ2VudE5hbWV9KipcbjQuIOeCueWHu+OAjCoq5Yib5bu6KirjgI1cblxuIyMjIOatpemqpCAzOiDojrflj5blupTnlKjlh63or4FcbjEuIOi/m+WFpeW6lOeUqOeuoeeQhumhtemdolxuMi4g54K55Ye75bem5L6n44CMKirlh63or4HkuI7ln7rnoYDkv6Hmga8qKuOAjVxuMy4g5aSN5Yi2ICoqQXBwIElEKirvvIjmoLzlvI/vvJpjbGlfeHh4eHh4eHh4eHh4eHh477yJXG40LiDlpI3liLYgKipBcHAgU2VjcmV0KirvvIgzMiDkvY3lrZfnrKbkuLLvvIlcbiAgIC0g5aaC5p6c55yL5LiN5Yiw77yM54K55Ye744CMKirmn6XnnIsqKuOAjeaIluOAjCoq6YeN572uKirjgI1cblxuIyMjIOatpemqpCA0OiDlvIDlkK/mnLrlmajkurrog73liptcbjEuIOeCueWHu+W3puS+p+OAjCoq5Yqf6IO9KirjgI3ihpLjgIwqKuacuuWZqOS6uioq44CNXG4yLiDinIUg5byA5ZCv44CMKirmnLrlmajkurrog73lipsqKuOAjVxuMy4g4pyFIOW8gOWQr+OAjCoq5Lul5py65Zmo5Lq66Lqr5Lu95Yqg5YWl576k6IGKKirjgI1cbjQuIOeCueWHu+OAjCoq5L+d5a2YKirjgI1cblxuIyMjIOatpemqpCA1OiDphY3nva7kuovku7borqLpmIVcbjEuIOeCueWHu+W3puS+p+OAjCoq5Yqf6IO9KirjgI3ihpLjgIwqKuS6i+S7tuiuoumYhSoq44CNXG4yLiDpgInmi6njgIwqKumVv+i/nuaOpSoq44CN5qih5byP77yI5o6o6I2Q77yJXG4zLiDli77pgInku6XkuIvkuovku7bvvJpcbiAgIC0g4pyFIFxcYGltLm1lc3NhZ2UucmVjZWl2ZV92MVxcYCAtIOaOpeaUtua2iOaBr1xuICAgLSDinIUgXFxgaW0ubWVzc2FnZS5yZWFkX3YxXFxgIC0g5raI5oGv5bey6K+777yI5Y+v6YCJ77yJXG40LiDngrnlh7vjgIwqKuS/neWtmCoq44CNXG5cbiMjIyDmraXpqqQgNjog6YWN572u5p2D6ZmQXG4xLiDngrnlh7vlt6bkvqfjgIwqKuWKn+iDvSoq44CN4oaS44CMKirmnYPpmZDnrqHnkIYqKuOAjVxuMi4g5pCc57Si5bm25re75Yqg5Lul5LiL5p2D6ZmQ77yaXG4gICAtIOKchSBcXGBpbTptZXNzYWdlXFxgIC0g6I635Y+W55So5oi35Y+R57uZ5py65Zmo5Lq655qE5Y2V6IGK5raI5oGvXG4gICAtIOKchSBcXGBpbTpjaGF0XFxgIC0g6I635Y+W576k57uE5Lit5Y+R57uZ5py65Zmo5Lq655qE5raI5oGvXG4gICAtIOKchSBcXGBjb250YWN0OnVzZXI6cmVhZG9ubHlcXGAgLSDor7vlj5bnlKjmiLfkv6Hmga/vvIjlj6/pgInvvIlcbjMuIOeCueWHu+OAjCoq55Sz6K+3KirjgI1cblxuIyMjIOatpemqpCA3OiDlj5HluIPlupTnlKhcbjEuIOeCueWHu+W3puS+p+OAjCoq54mI5pys566h55CG5LiO5Y+R5biDKirjgI1cbjIuIOeCueWHu+OAjCoq5Yib5bu654mI5pysKirjgI1cbjMuIOWhq+WGmeeJiOacrOWPt++8mlxcYDEuMC4wXFxgXG40LiDngrnlh7vjgIwqKuaPkOS6pOWuoeaguCoq44CN77yI5py65Zmo5Lq657G76YCa5bi46Ieq5Yqo6YCa6L+H77yJXG41LiDnrYnlvoUgNS0xMCDliIbpkp/nlJ/mlYhcblxuLS0tXG5cbiMjIyDinIUg5a6M5oiQ5qOA5p+l5riF5Y2VXG4tIFsgXSBBcHAgSUQg5bey5aSN5Yi277yI5LulIGNsaV8g5byA5aS077yJXG4tIFsgXSBBcHAgU2VjcmV0IOW3suWkjeWItu+8iDMyIOS9jeWtl+espuS4su+8iVxuLSBbIF0g5py65Zmo5Lq66IO95Yqb5bey5byA5ZCvXG4tIFsgXSDkuovku7borqLpmIXlt7LphY3nva7vvIjplb/ov57mjqXmqKHlvI/vvIlcbi0gWyBdIOadg+mZkOW3sueUs+ivt++8iGltOm1lc3NhZ2UsIGltOmNoYXTvvIlcbi0gWyBdIOW6lOeUqOW3suWPkeW4g1xuXG4tLS1cblxuKirlh4blpIflpb3lkI7vvIzor7flm57lpI3ku6XkuIvkv6Hmga/vvJoqKlxuXG5cXGBcXGBcXGBcbuesrCAke2luZGV4fSDkuKogQm90IOmFjee9ruWujOaIkO+8mlxuQXBwIElEOiBjbGlfeHh4eHh4eHh4eHh4eHh4XG5BcHAgU2VjcmV0OiB4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eFxuXFxgXFxgXFxgXG5cbuaIkeS8muW4ruS9oOmqjOivgeW5tua3u+WKoOWIsOmFjee9ruS4re+8gSDwn5GNXG5gO1xufVxuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyDmoLjlv4Plip/og71cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuLyoqXG4gKiDmibnph4/liJvlu7rlpJrkuKogQWdlbnRcbiAqL1xuYXN5bmMgZnVuY3Rpb24gY3JlYXRlTXVsdGlwbGVBZ2VudHMoY3R4OiBTZXNzaW9uQ29udGV4dCwgYWdlbnRzOiBBcnJheTx7XG4gIGFnZW50SWQ6IHN0cmluZztcbiAgYWdlbnROYW1lOiBzdHJpbmc7XG4gIGFwcElkOiBzdHJpbmc7XG4gIGFwcFNlY3JldDogc3RyaW5nO1xuICBpc0RlZmF1bHQ/OiBib29sZWFuO1xuICBtb2RlbD86IHN0cmluZztcbn0+KTogUHJvbWlzZTx7IHN1Y2Nlc3M6IGJvb2xlYW47IHJlc3VsdHM6IEFycmF5PHsgaWQ6IHN0cmluZzsgc3VjY2VzczogYm9vbGVhbjsgZXJyb3I/OiBzdHJpbmcgfT4gfT4ge1xuICAvLyDliqjmgIHojrflj5bnlKjmiLfkuLvnm67lvZXvvIzpgb/lhY3noaznvJbnoIFcbiAgY29uc3QgaG9tZURpciA9IHByb2Nlc3MuZW52LkhPTUUgfHwgcHJvY2Vzcy5lbnYuVVNFUlBST0ZJTEUgfHwgJy9ob21lL25vZGUnO1xuICBjb25zdCBjb25maWdQYXRoID0gcGF0aC5qb2luKGhvbWVEaXIsICcub3BlbmNsYXcnLCAnb3BlbmNsYXcuanNvbicpO1xuICBjb25zdCByZXN1bHRzOiBBcnJheTx7IGlkOiBzdHJpbmc7IHN1Y2Nlc3M6IGJvb2xlYW47IGVycm9yPzogc3RyaW5nIH0+ID0gW107XG4gIFxuICB0cnkge1xuICAgIC8vIOmFjee9ruWJjeiHquWKqOWkh+S7vVxuICAgIGNvbnN0IGJhY2t1cFBhdGggPSBjcmVhdGVCYWNrdXAoY29uZmlnUGF0aCk7XG4gICAgYXdhaXQgY3R4LnNlbmQoYPCfk6Yg5bey6Ieq5Yqo5aSH5Lu96YWN572u5paH5Lu25Yiw77yaXFxgJHtiYWNrdXBQYXRofVxcYGApO1xuICAgIFxuICAgIC8vIDEuIOivu+WPlueOsOaciemFjee9rlxuICAgIGNvbnN0IGNvbmZpZyA9IHJlYWRPcGVuQ2xhd0NvbmZpZyhjb25maWdQYXRoKTtcbiAgICBcbiAgICAvLyAyLiDpgJDkuKrliJvlu7ogQWdlbnRcbiAgICBmb3IgKGNvbnN0IGFnZW50IG9mIGFnZW50cykge1xuICAgICAgdHJ5IHtcbiAgICAgICAgLy8g6aqM6K+B5Yet6K+BXG4gICAgICAgIGNvbnN0IHZhbGlkYXRpb24gPSB2YWxpZGF0ZUZlaXNodUNyZWRlbnRpYWxzKGFnZW50LmFwcElkLCBhZ2VudC5hcHBTZWNyZXQpO1xuICAgICAgICBpZiAoIXZhbGlkYXRpb24udmFsaWQpIHtcbiAgICAgICAgICByZXN1bHRzLnB1c2goeyBpZDogYWdlbnQuYWdlbnRJZCwgc3VjY2VzczogZmFsc2UsIGVycm9yOiB2YWxpZGF0aW9uLmVycm9yIH0pO1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG4gICAgICAgIFxuICAgICAgICAvLyDmo4Dmn6XmmK/lkKblt7LlrZjlnKhcbiAgICAgICAgaWYgKGNvbmZpZy5hZ2VudHMubGlzdC5zb21lKGEgPT4gYS5pZCA9PT0gYWdlbnQuYWdlbnRJZCkpIHtcbiAgICAgICAgICByZXN1bHRzLnB1c2goeyBpZDogYWdlbnQuYWdlbnRJZCwgc3VjY2VzczogZmFsc2UsIGVycm9yOiAnQWdlbnQgSUQg5bey5a2Y5ZyoJyB9KTtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuICAgICAgICBcbiAgICAgICAgLy8g5Yib5bu65bel5L2c5Yy66Lev5b6EIC0g5q+P5LiqIEFnZW50IOWujOWFqOeLrOeri++8iOS9v+eUqOWKqOaAgSBob21lRGly77yJXG4gICAgICAgIGNvbnN0IHdvcmtzcGFjZVBhdGggPSBwYXRoLmpvaW4oaG9tZURpciwgJy5vcGVuY2xhdycsIGB3b3Jrc3BhY2UtJHthZ2VudC5hZ2VudElkfWApO1xuICAgICAgICBjb25zdCBhZ2VudERpclBhdGggPSBwYXRoLmpvaW4oaG9tZURpciwgJy5vcGVuY2xhdycsICdhZ2VudHMnLCBhZ2VudC5hZ2VudElkLCAnYWdlbnQnKTtcbiAgICAgICAgXG4gICAgICAgIC8vIOWIm+W7uiBBZ2VudCDphY3nva5cbiAgICAgICAgY29uc3QgbmV3QWdlbnQ6IEFnZW50Q29uZmlnID0ge1xuICAgICAgICAgIGlkOiBhZ2VudC5hZ2VudElkLFxuICAgICAgICAgIG5hbWU6IGFnZW50LmFnZW50TmFtZSxcbiAgICAgICAgICB3b3Jrc3BhY2U6IHdvcmtzcGFjZVBhdGgsXG4gICAgICAgICAgYWdlbnREaXI6IGFnZW50RGlyUGF0aCxcbiAgICAgICAgICAuLi4oYWdlbnQuaXNEZWZhdWx0ID8geyBkZWZhdWx0OiB0cnVlIH0gOiB7fSksXG4gICAgICAgICAgLi4uKGFnZW50Lm1vZGVsID8geyBtb2RlbDogeyBwcmltYXJ5OiBhZ2VudC5tb2RlbCB9IH0gOiB7fSksXG4gICAgICAgIH07XG4gICAgICAgIFxuICAgICAgICAvLyDmt7vliqDliLAgYWdlbnRzLmxpc3RcbiAgICAgICAgY29uZmlnLmFnZW50cy5saXN0LnB1c2gobmV3QWdlbnQpO1xuICAgICAgICBcbiAgICAgICAgLy8g5re75Yqg6aOe5Lmm6LSm5Y+3XG4gICAgICAgIGNvbmZpZy5jaGFubmVscy5mZWlzaHUuYWNjb3VudHNbYWdlbnQuYWdlbnRJZF0gPSB7XG4gICAgICAgICAgYXBwSWQ6IGFnZW50LmFwcElkLFxuICAgICAgICAgIGFwcFNlY3JldDogYWdlbnQuYXBwU2VjcmV0LFxuICAgICAgICB9O1xuICAgICAgICBcbiAgICAgICAgLy8g5re75Yqg6Lev55Sx6KeE5YiZXG4gICAgICAgIGNvbmZpZy5iaW5kaW5ncy5wdXNoKHtcbiAgICAgICAgICBhZ2VudElkOiBhZ2VudC5hZ2VudElkLFxuICAgICAgICAgIG1hdGNoOiB7XG4gICAgICAgICAgICBjaGFubmVsOiAnZmVpc2h1JyxcbiAgICAgICAgICAgIGFjY291bnRJZDogYWdlbnQuYWdlbnRJZCxcbiAgICAgICAgICB9LFxuICAgICAgICB9KTtcbiAgICAgICAgXG4gICAgICAgIC8vIOa3u+WKoOWIsCBhZ2VudFRvQWdlbnQg55m95ZCN5Y2VXG4gICAgICAgIGlmICghY29uZmlnLnRvb2xzLmFnZW50VG9BZ2VudC5hbGxvdy5pbmNsdWRlcyhhZ2VudC5hZ2VudElkKSkge1xuICAgICAgICAgIGNvbmZpZy50b29scy5hZ2VudFRvQWdlbnQuYWxsb3cucHVzaChhZ2VudC5hZ2VudElkKTtcbiAgICAgICAgfVxuICAgICAgICBcbiAgICAgICAgLy8g5YaZ5YWl6YWN572uXG4gICAgICAgIHdyaXRlT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aCwgY29uZmlnKTtcbiAgICAgICAgXG4gICAgICAgIC8vIOWIm+W7uuW3peS9nOWMuuebruW9lVxuICAgICAgICBjcmVhdGVBZ2VudFdvcmtzcGFjZSh3b3Jrc3BhY2VQYXRoKTtcbiAgICAgICAgZnMubWtkaXJTeW5jKGFnZW50RGlyUGF0aCwgeyByZWN1cnNpdmU6IHRydWUgfSk7XG4gICAgICAgIFxuICAgICAgICAvLyDnlJ/miJAgQWdlbnQg5Lq66K6+5paH5Lu2XG4gICAgICAgIGNvbnN0IHNvdWxQYXRoID0gcGF0aC5qb2luKHdvcmtzcGFjZVBhdGgsICdTT1VMLm1kJyk7XG4gICAgICAgIGNvbnN0IGFnZW50c1BhdGggPSBwYXRoLmpvaW4od29ya3NwYWNlUGF0aCwgJ0FHRU5UUy5tZCcpO1xuICAgICAgICBjb25zdCB1c2VyUGF0aCA9IHBhdGguam9pbih3b3Jrc3BhY2VQYXRoLCAnVVNFUi5tZCcpO1xuICAgICAgICBcbiAgICAgICAgY29uc3QgdGVtcGxhdGUgPSBBR0VOVF9URU1QTEFURVNbYWdlbnQuYWdlbnRJZCBhcyBrZXlvZiB0eXBlb2YgQUdFTlRfVEVNUExBVEVTXTtcbiAgICAgICAgaWYgKHRlbXBsYXRlKSB7XG4gICAgICAgICAgZnMud3JpdGVGaWxlU3luYyhzb3VsUGF0aCwgdGVtcGxhdGUuc291bFRlbXBsYXRlLCAndXRmLTgnKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBmcy53cml0ZUZpbGVTeW5jKHNvdWxQYXRoLCBgIyBTT1VMLm1kIC0gJHthZ2VudC5hZ2VudE5hbWV9XFxuXFxu5L2g5piv55So5oi355qEJHthZ2VudC5hZ2VudE5hbWV977yM5LiT5rOo5LqO5Li655So5oi35o+Q5L6b5LiT5Lia5Y2P5Yqp44CCYCwgJ3V0Zi04Jyk7XG4gICAgICAgIH1cbiAgICAgICAgXG4gICAgICAgIGZzLndyaXRlRmlsZVN5bmMoYWdlbnRzUGF0aCwgZ2VuZXJhdGVBZ2VudHNUZW1wbGF0ZShjb25maWcuYWdlbnRzLmxpc3QpLCAndXRmLTgnKTtcbiAgICAgICAgZnMud3JpdGVGaWxlU3luYyh1c2VyUGF0aCwgZ2VuZXJhdGVVc2VyVGVtcGxhdGUoKSwgJ3V0Zi04Jyk7XG4gICAgICAgIFxuICAgICAgICByZXN1bHRzLnB1c2goeyBpZDogYWdlbnQuYWdlbnRJZCwgc3VjY2VzczogdHJ1ZSB9KTtcbiAgICAgICAgY3R4LmxvZ2dlci5pbmZvKGDinIUgQWdlbnQgXCIke2FnZW50LmFnZW50SWR9XCIg5Yib5bu65oiQ5YqfYCk7XG4gICAgICB9IGNhdGNoIChlcnJvcjogYW55KSB7XG4gICAgICAgIHJlc3VsdHMucHVzaCh7IGlkOiBhZ2VudC5hZ2VudElkLCBzdWNjZXNzOiBmYWxzZSwgZXJyb3I6IGVycm9yLm1lc3NhZ2UgfSk7XG4gICAgICAgIGN0eC5sb2dnZXIuZXJyb3IoYOKdjCDliJvlu7ogQWdlbnQgXCIke2FnZW50LmFnZW50SWR9XCIg5aSx6LSl77yaJHtlcnJvci5tZXNzYWdlfWApO1xuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICByZXR1cm4geyBzdWNjZXNzOiByZXN1bHRzLmV2ZXJ5KHIgPT4gci5zdWNjZXNzKSwgcmVzdWx0cyB9O1xuICB9IGNhdGNoIChlcnJvcjogYW55KSB7XG4gICAgY3R4LmxvZ2dlci5lcnJvcihg4p2MIOaJuemHj+WIm+W7uuWksei0pe+8miR7ZXJyb3IubWVzc2FnZX1gKTtcbiAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgcmVzdWx0czogW10gfTtcbiAgfVxufVxuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyBTa2lsbCDkuLvlh73mlbBcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuLyoqXG4gKiBTa2lsbCDkuLvlh73mlbAgLSDkuqTkupLlvI/lvJXlr7zniYjmnKxcbiAqIFxuICogQHBhcmFtIGN0eCAtIOS8muivneS4iuS4i+aWh1xuICogQHBhcmFtIGFyZ3MgLSDlj4LmlbBcbiAqL1xuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIG1haW4oY3R4OiBTZXNzaW9uQ29udGV4dCwgYXJnczogUmVjb3JkPHN0cmluZywgYW55Pik6IFByb21pc2U8dm9pZD4ge1xuICBjb25zdCB7IFxuICAgIGFjdGlvbiwgXG4gICAgY291bnQsIFxuICAgIGFnZW50cywgXG4gICAgYWdlbnRJZCwgXG4gICAgYWdlbnROYW1lLCBcbiAgICBhcHBJZCwgXG4gICAgYXBwU2VjcmV0LFxuICAgIHN0ZXAsXG4gICAgY29uZmlnRGF0YVxuICB9ID0gYXJncztcbiAgXG4gIGN0eC5sb2dnZXIuaW5mbyhg5pS25Yiw5aSaIEFnZW50IOmFjee9ruivt+axgu+8mmFjdGlvbj0ke2FjdGlvbn1gKTtcbiAgXG4gIHRyeSB7XG4gICAgc3dpdGNoIChhY3Rpb24pIHtcbiAgICAgIGNhc2UgJ3N0YXJ0X3dpemFyZCc6IHtcbiAgICAgICAgLy8g5ZCv5Yqo6YWN572u5ZCR5a+8XG4gICAgICAgIGF3YWl0IGN0eC5yZXBseShg8J+kliAqKuasoui/juS9v+eUqOmjnuS5puWkmiBBZ2VudCDphY3nva7liqnmiYvvvIEqKlxuXG4+IPCfkqEgKirlhbzlrrnpo57kuabmj5Lku7YgMjAyNi40LjEqKiB8IE9wZW5DbGF3IOKJpSAyMDI2LjMuMzFcblxu5oiR5bCG5byV5a+85L2g5a6M5oiQ5aSa5LiqIEFnZW50IOeahOmFjee9rua1geeoi+OAglxuXG4jIyDwn5OLIOmFjee9rua1geeoi1xuXG4xLiAqKumAieaLqSBBZ2VudCDmlbDph48qKiAtIOWRiuivieaIkeimgeWIm+W7uuWHoOS4qiBBZ2VudFxuMi4gKirpgInmi6kgQWdlbnQg6KeS6ImyKiogLSDku47pooTorr7op5LoibLkuK3pgInmi6nmiJboh6rlrprkuYlcbjMuICoq5Yib5bu66aOe5Lmm5bqU55SoKiogLSDmiJHkvJrmj5Dkvpvor6bnu4bnmoTliJvlu7rmlZnnqItcbjQuICoq6YWN572u5Yet6K+BKiogLSDpgJDkuKrovpPlhaXmr4/kuKogQm90IOeahCBBcHAgSUQg5ZKMIEFwcCBTZWNyZXRcbjUuICoq6aqM6K+B5bm255Sf5oiQKiogLSDoh6rliqjpqozor4Hlh63or4HlubbnlJ/miJDphY3nva5cbjYuICoq6YeN5ZCv55Sf5pWIKiogLSDph43lkK8gT3BlbkNsYXcg5L2/6YWN572u55Sf5pWIXG5cbi0tLVxuXG4jIyDwn46vIOmihOiuvuinkuiJsuaOqOiNkFxuXG58IOinkuiJsiB8IOiBjOi0oyB8IOihqOaDhSB8XG58LS0tLS0tfC0tLS0tLXwtLS0tLS18XG58ICoqbWFpbioqIHwg5aSn5oC7566hIC0g57uf56255YWo5bGA44CB5YiG6YWN5Lu75YqhIHwg8J+OryB8XG58ICoqZGV2KiogfCDlvIDlj5HliqnnkIYgLSDku6PnoIHlvIDlj5HjgIHmioDmnK/mnrbmnoQgfCDwn6eR4oCN8J+SuyB8XG58ICoqY29udGVudCoqIHwg5YaF5a655Yqp55CGIC0g5YaF5a655Yib5L2c44CB5paH5qGI5pKw5YaZIHwg4pyN77iPIHxcbnwgKipvcHMqKiB8IOi/kOiQpeWKqeeQhiAtIOeUqOaIt+WinumVv+OAgea0u+WKqOetluWIkiB8IPCfk4ggfFxufCAqKmxhdyoqIHwg5rOV5Yqh5Yqp55CGIC0g5ZCI5ZCM5a6h5qC444CB5ZCI6KeE5ZKo6K+iIHwg8J+TnCB8XG58ICoqZmluYW5jZSoqIHwg6LSi5Yqh5Yqp55CGIC0g6LSm55uu57uf6K6h44CB6aKE566X566h55CGIHwg8J+SsCB8XG5cbi0tLVxuXG4jIyDwn5qAIOW/q+mAn+W8gOWni1xuXG4qKuivt+WRiuivieaIke+8muS9oOaDs+WIm+W7uuWHoOS4qiBBZ2VudO+8nyoqXG5cbuS+i+Wmgu+8mlxuLSBcXGAzIOS4qlxcYCAtIOaIkeaOqOiNkO+8mm1haW7vvIjlpKfmgLvnrqHvvIkrIGRldu+8iOW8gOWPke+8iSsgY29udGVudO+8iOWGheWuue+8iVxuLSBcXGA2IOS4qlxcYCAtIOWujOaVtOWboumYn++8muWFqOmDqCA2IOS4quinkuiJslxuLSBcXGDoh6rlrprkuYlcXGAgLSDkvaDoh6rnlLHpgInmi6nop5LoibJcblxu5Zue5aSN5pWw5a2X5oiWXCLoh6rlrprkuYlcIu+8jOaIkeS7rOW8gOWni+WQp++8gSDwn5iKXG5cbi0tLVxuXG4jIyDwn5OmIOWJjee9ruajgOafpVxuXG7noa7kv53lt7Llronoo4XvvJpcbi0g4pyFIE9wZW5DbGF3IOKJpSAyMDI2LjMuMzFcbi0g4pyFIOmjnuS5puWumOaWueaPkuS7tiAyMDI2LjQuMe+8iFxcYG5weCAteSBAbGFya3N1aXRlL29wZW5jbGF3LWxhcmsgaW5zdGFsbFxcYO+8iVxuXG4qKuajgOafpeWRveS7pO+8mioqIFxcYC9mZWlzaHUgc3RhcnRcXGBgKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBcbiAgICAgIGNhc2UgJ3NlbGVjdF9jb3VudCc6IHtcbiAgICAgICAgLy8g55So5oi36YCJ5oup5pWw6YePXG4gICAgICAgIGNvbnN0IG51bUNvdW50ID0gcGFyc2VJbnQoY291bnQpO1xuICAgICAgICBcbiAgICAgICAgaWYgKGlzTmFOKG51bUNvdW50KSB8fCBudW1Db3VudCA8IDEgfHwgbnVtQ291bnQgPiAxMCkge1xuICAgICAgICAgIGF3YWl0IGN0eC5yZXBseShg4p2MIOivt+i+k+WFpeacieaViOeahOaVsOWtl++8iDEtMTAg5LmL6Ze077yJXG5cbuS+i+Wmgu+8mlxcYDNcXGAg5oiWIFxcYDZcXGBgKTtcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgICAgICBcbiAgICAgICAgLy8g55Sf5oiQ5o6o6I2Q5pa55qGIXG4gICAgICAgIGxldCByZWNvbW1lbmRlZEFnZW50cyA9ICcnO1xuICAgICAgICBpZiAobnVtQ291bnQgPT09IDEpIHtcbiAgICAgICAgICByZWNvbW1lbmRlZEFnZW50cyA9ICfmjqjojZDvvJoqKm1haW4qKu+8iOWkp+aAu+euoe+8iS0g5YWo6IO95Z6L5Yqp55CGJztcbiAgICAgICAgfSBlbHNlIGlmIChudW1Db3VudCA9PT0gMikge1xuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gJ+aOqOiNkO+8mioqbWFpbioq77yI5aSn5oC7566h77yJKyAqKmRldioq77yI5byA5Y+R5Yqp55CG77yJJztcbiAgICAgICAgfSBlbHNlIGlmIChudW1Db3VudCA9PT0gMykge1xuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gJ+aOqOiNkO+8mioqbWFpbioq77yI5aSn5oC7566h77yJKyAqKmRldioq77yI5byA5Y+R5Yqp55CG77yJKyAqKmNvbnRlbnQqKu+8iOWGheWuueWKqeeQhu+8iSc7XG4gICAgICAgIH0gZWxzZSBpZiAobnVtQ291bnQgPT09IDYpIHtcbiAgICAgICAgICByZWNvbW1lbmRlZEFnZW50cyA9ICfmjqjojZDvvJrlrozmlbQgNiDkurrlm6LpmJ8gLSBtYWluICsgZGV2ICsgY29udGVudCArIG9wcyArIGxhdyArIGZpbmFuY2UnO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gYOS9oOWPr+S7peS7jiA2IOS4qumihOiuvuinkuiJsuS4remAieaLqSAke251bUNvdW50fSDkuKrvvIzmiJbogIXoh6rlrprkuYnop5LoibJgO1xuICAgICAgICB9XG4gICAgICAgIFxuICAgICAgICBhd2FpdCBjdHgucmVwbHkoYOKchSDlpb3nmoTvvIHmiJHku6zlsIbliJvlu7ogKioke251bUNvdW50fSoqIOS4qiBBZ2VudOOAglxuXG4jIyDwn5OLIOaOqOiNkOaWueahiFxuXG4ke3JlY29tbWVuZGVkQWdlbnRzfVxuXG4tLS1cblxuIyMg8J+OryDor7fpgInmi6nphY3nva7mlrnlvI9cblxuKirmlrnlvI8gMe+8muS9v+eUqOmihOiuvuinkuiJsioqXG7lm57lpI0gXFxg6aKE6K6+XFxgIOaIliBcXGDmqKHmnb9cXGDvvIzmiJHkvJrmjInmjqjojZDmlrnmoYjoh6rliqjphY3nva5cblxuKirmlrnlvI8gMu+8muiHquWumuS5ieinkuiJsioqXG7lm57lpI0gXFxg6Ieq5a6a5LmJXFxg77yM54S25ZCO5ZGK6K+J5oiR5L2g5oOz55So5ZOqICR7bnVtQ291bnR9IOS4quinkuiJslxuXG4qKuaWueW8jyAz77ya5a6M5YWo6Ieq5a6a5LmJKipcbuWbnuWkjSBcXGDlhajmlrBcXGDvvIzmr4/kuKrop5LoibLpg73nlLHkvaDoh6rnlLHlrprkuYlcblxu6K+36YCJ5oup77yI5Zue5aSN5pWw5a2X5oiW5YWz6ZSu6K+N77yJ77yaYCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgXG4gICAgICBjYXNlICdzaG93X3R1dG9yaWFsJzoge1xuICAgICAgICAvLyDmmL7npLrpo57kuabliJvlu7rmlZnnqItcbiAgICAgICAgY29uc3QgYWdlbnRJbmRleCA9IHBhcnNlSW50KHN0ZXApIHx8IDE7XG4gICAgICAgIGNvbnN0IG5hbWUgPSBhZ2VudE5hbWUgfHwgYEFnZW50ICR7YWdlbnRJbmRleH1gO1xuICAgICAgICBcbiAgICAgICAgY29uc3QgdHV0b3JpYWwgPSBnZW5lcmF0ZUZlaXNodVR1dG9yaWFsKG5hbWUsIGFnZW50SW5kZXgpO1xuICAgICAgICBcbiAgICAgICAgYXdhaXQgY3R4LnJlcGx5KHR1dG9yaWFsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBcbiAgICAgIGNhc2UgJ3ZhbGlkYXRlX2NyZWRlbnRpYWxzJzoge1xuICAgICAgICAvLyDpqozor4HnlKjmiLfmj5DkvpvnmoTlh63or4FcbiAgICAgICAgY29uc3QgdmFsaWRhdGlvbiA9IHZhbGlkYXRlRmVpc2h1Q3JlZGVudGlhbHMoYXBwSWQsIGFwcFNlY3JldCk7XG4gICAgICAgIFxuICAgICAgICBpZiAoIXZhbGlkYXRpb24udmFsaWQpIHtcbiAgICAgICAgICBhd2FpdCBjdHgucmVwbHkoYCR7dmFsaWRhdGlvbi5lcnJvcn1cblxuKiror7fmo4Dmn6XlkI7ph43mlrDmj5DkvpvvvJoqKlxuLSBBcHAgSUQg5b+F6aG75LulIFxcYGNsaV9cXGAg5byA5aS0XG4tIEFwcCBTZWNyZXQg5b+F6aG75pivIDMyIOS9jeWtl+espuS4slxuLSDkuI3opoHljIXlkKvnqbrmoLzmiJbmjaLooYxcblxu5L2g5Y+v5Lul5Zue5aSNIFxcYOmHjeivlVxcYCDph43mlrDovpPlhaXvvIzmiJblm57lpI0gXFxg5pWZ56iLXFxgIOafpeeci+WIm+W7uuatpemqpOOAgmApO1xuICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgICAgIFxuICAgICAgICBhd2FpdCBjdHgucmVwbHkoYOKchSDlh63or4Hpqozor4HpgJrov4fvvIFcblxuKipBcHAgSUQ6KiogXFxgJHthcHBJZH1cXGBcbioqQXBwIFNlY3JldDoqKiBcXGAke2FwcFNlY3JldC5zdWJzdHJpbmcoMCwgOCl9Li4uXFxg77yI5bey6ZqQ6JeP77yJXG5cbuWHhuWkh+a3u+WKoOWIsOmFjee9ru+8jOivt+ehruiupO+8mlxuLSDlm57lpI0gXFxg56Gu6K6kXFxgIOe7p+e7rVxuLSDlm57lpI0gXFxg5Y+W5raIXFxgIOaUvuW8g1xuLSDlm57lpI0gXFxg5LiL5LiA5LiqXFxgIOebtOaOpemFjee9ruS4i+S4gOS4qmApO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIFxuICAgICAgY2FzZSAnYmF0Y2hfY3JlYXRlJzoge1xuICAgICAgICAvLyDmibnph4/liJvlu7ogQWdlbnRcbiAgICAgICAgY29uc3QgYWdlbnRMaXN0ID0gYWdlbnRzIHx8IFtdO1xuICAgICAgICBcbiAgICAgICAgaWYgKCFBcnJheS5pc0FycmF5KGFnZW50TGlzdCkgfHwgYWdlbnRMaXN0Lmxlbmd0aCA9PT0gMCkge1xuICAgICAgICAgIGF3YWl0IGN0eC5yZXBseSgn4p2MIOayoeacieaPkOS+m+acieaViOeahCBBZ2VudCDliJfooagnKTtcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgICAgICBcbiAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDwn5qAIOW8gOWni+WIm+W7uiAke2FnZW50TGlzdC5sZW5ndGh9IOS4qiBBZ2VudC4uLlxuXG7or7fnqI3lgJnvvIzmraPlnKjlpITnkIbvvJpcbiR7YWdlbnRMaXN0Lm1hcCgoYTogYW55LCBpOiBudW1iZXIpID0+IGAke2kgKyAxfS4gJHthLmFnZW50SWR9IC0gJHthLmFnZW50TmFtZX1gKS5qb2luKCdcXG4nKX1cbmApO1xuICAgICAgICBcbiAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgY3JlYXRlTXVsdGlwbGVBZ2VudHMoY3R4LCBhZ2VudExpc3QpO1xuICAgICAgICBcbiAgICAgICAgaWYgKHJlc3VsdC5zdWNjZXNzKSB7XG4gICAgICAgICAgY29uc3Qgc3VjY2Vzc0xpc3QgPSByZXN1bHQucmVzdWx0cy5maWx0ZXIociA9PiByLnN1Y2Nlc3MpLm1hcChyID0+IHIuaWQpLmpvaW4oJywgJyk7XG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDwn46JICoq5om56YeP5Yib5bu65oiQ5Yqf77yBKipcblxu4pyFIOW3suWIm+W7uiAke3Jlc3VsdC5yZXN1bHRzLmxlbmd0aH0g5LiqIEFnZW5077yaXG4ke3Jlc3VsdC5yZXN1bHRzLm1hcCgociwgaSkgPT4gYCR7aSArIDF9LiAqKiR7ci5pZH0qKiAtICR7ci5zdWNjZXNzID8gJ+KchScgOiAn4p2MICcgKyByLmVycm9yfWApLmpvaW4oJ1xcbicpfVxuXG4tLS1cblxuIyMg8J+TnSDkuIvkuIDmraVcblxuIyMjIDEuIOmHjeWQryBPcGVuQ2xhd1xuXFxgXFxgXFxgYmFzaFxub3BlbmNsYXcgcmVzdGFydFxuXFxgXFxgXFxgXG5cbiMjIyAyLiDnrYnlvoUgQm90IOS4iue6v1xu6YeN5ZCv5ZCO562J5b6FIDEtMiDliIbpkp/vvIzmiYDmnIkgQm90IOS8muiHquWKqOi/nuaOpemjnuS5plxuXG4jIyMgMy4g5rWL6K+VIEJvdFxu5Zyo6aOe5Lmm5Lit5pCc57SiIEJvdCDlkI3np7DvvIzlj5HpgIHmtojmga/mtYvor5VcblxuIyMjIDQuIOaJuemHj+aOiOadg++8iOmHjeimge+8iVxu5Zyo6aOe5Lmm5a+56K+d5Lit5Y+R6YCB77yaXG5cXGBcXGBcXGBcbi9mZWlzaHUgYXV0aFxuXFxgXFxgXFxgXG5cbuWujOaIkOeUqOaIt+aOiOadg++8jOS9vyBBZ2VudCDog73orr/pl67kvaDnmoTpo57kuabmlofmoaPjgIHml6XljobnrYlcblxuIyMjIDUuIOafpeeci+aXpeW/l1xuXFxgXFxgXFxgYmFzaFxudGFpbCAtZiAvaG9tZS9ub2RlLy5vcGVuY2xhdy9ydW4ubG9nXG5cXGBcXGBcXGBcblxuLS0tXG5cbiMjIPCfmoAg6auY57qn6YWN572u77yI5Y+v6YCJ77yJXG5cbiMjIyDlvIDlkK/mtYHlvI/ovpPlh7pcblxcYFxcYFxcYGJhc2hcbm9wZW5jbGF3IGNvbmZpZyBzZXQgY2hhbm5lbHMuZmVpc2h1LnN0cmVhbWluZyB0cnVlXG5cXGBcXGBcXGBcblxuIyMjIOW8gOWQr+ivnemimOaooeW8j++8iOeLrOeri+S4iuS4i+aWh++8iVxuXFxgXFxgXFxgYmFzaFxub3BlbmNsYXcgY29uZmlnIHNldCBjaGFubmVscy5mZWlzaHUudGhyZWFkU2Vzc2lvbiB0cnVlXG5cXGBcXGBcXGBcblxuIyMjIOiviuaWreWRveS7pFxuXFxgXFxgXFxgXG4vZmVpc2h1IHN0YXJ0ICAgIyDmo4Dmn6Xmj5Lku7bnirbmgIFcbi9mZWlzaHUgZG9jdG9yICAjIOa3seW6puiviuaWrVxuL2ZlaXNodSBhdXRoICAgICMg5om56YeP5o6I5p2DXG5cXGBcXGBcXGBcblxuLS0tXG5cbiMjIPCfk5og6YWN572u6K+m5oOFXG5cbuaJgOaciSBBZ2VudCDnmoTphY3nva7lt7Lkv53lrZjliLDvvJpcbi0gKirphY3nva7mlofku7bvvJoqKiBcXGAvaG9tZS9ub2RlLy5vcGVuY2xhdy9vcGVuY2xhdy5qc29uXFxgXG4tICoq5bel5L2c5Yy677yaKiogXFxgL2hvbWUvbm9kZS8ub3BlbmNsYXcvd29ya3NwYWNlLVthZ2VudElkXS9cXGBcbi0gKirkurrorr7mlofku7bvvJoqKiDmr4/kuKrlt6XkvZzljLrljIXlkKsgU09VTC5tZOOAgUFHRU5UUy5tZOOAgVVTRVIubWRcblxuLS0tXG5cbvCfkqEgKirmj5DnpLrvvJoqKiBcbi0g5aaC5p6c5pyJ5Lu75L2VIEJvdCDmmL7npLogb2ZmbGluZe+8jOivt+ajgOafpemjnuS5puW6lOeUqOmFjee9ru+8iOWHreivgeOAgeS6i+S7tuiuoumYheOAgeadg+mZkO+8iVxuLSDpo57kuabmj5Lku7bniYjmnKzvvJoyMDI2LjQuMSB8IE9wZW5DbGF3IOeJiOacrO+8muKJpSAyMDI2LjMuMzFcblxu6ZyA6KaB5biu5Yqp6K+35Zue5aSNIFxcYOW4ruWKqVxcYCDmiJYgXFxg5o6S5p+lXFxg77yBYCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgY29uc3QgZmFpbGVkTGlzdCA9IHJlc3VsdC5yZXN1bHRzLmZpbHRlcihyID0+ICFyLnN1Y2Nlc3MpO1xuICAgICAgICAgIGF3YWl0IGN0eC5yZXBseShg4pqg77iPICoq6YOo5YiG5Yib5bu65aSx6LSlKipcblxu5oiQ5Yqf77yaJHtyZXN1bHQucmVzdWx0cy5maWx0ZXIociA9PiByLnN1Y2Nlc3MpLmxlbmd0aH0vJHtyZXN1bHQucmVzdWx0cy5sZW5ndGh9XG5cbioq5aSx6LSl55qEIEFnZW5077yaKipcbiR7ZmFpbGVkTGlzdC5tYXAoKHIsIGkpID0+IGAke2kgKyAxfS4gKioke3IuaWR9Kio6ICR7ci5lcnJvcn1gKS5qb2luKCdcXG4nKX1cblxuLS0tXG5cbioq6K+35qOA5p+l77yaKipcbjEuIOmjnuS5puWHreivgeaYr+WQpuato+ehrlxuMi4gQWdlbnQgSUQg5piv5ZCm6YeN5aSNXG4zLiDlt6XkvZzljLrot6/lvoTmmK/lkKblj6/lhplcblxu5Zue5aSNIFxcYOmHjeivlSBbYWdlbnRJZF1cXGAg6YeN5paw5bCd6K+V5Yib5bu65aSx6LSl55qEIEFnZW5044CCYCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBcbiAgICAgIGNhc2UgJ3Nob3dfc3RhdHVzJzoge1xuICAgICAgICAvLyDmmL7npLrlvZPliY3phY3nva7nirbmgIFcbiAgICAgICAgY29uc3QgaG9tZURpciA9IHByb2Nlc3MuZW52LkhPTUUgfHwgcHJvY2Vzcy5lbnYuVVNFUlBST0ZJTEUgfHwgJy9ob21lL25vZGUnO1xuICAgICAgICBjb25zdCBjb25maWdQYXRoID0gcGF0aC5qb2luKGhvbWVEaXIsICcub3BlbmNsYXcnLCAnb3BlbmNsYXcuanNvbicpO1xuICAgICAgICBcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICBjb25zdCBjb25maWcgPSByZWFkT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aCk7XG4gICAgICAgICAgY29uc3QgYWdlbnRzID0gY29uZmlnLmFnZW50cy5saXN0O1xuICAgICAgICAgIFxuICAgICAgICAgIGF3YWl0IGN0eC5yZXBseShgIyMg8J+TiiDlvZPliY0gQWdlbnQg6YWN572u54q25oCBXG5cbioq5bey6YWN572uIEFnZW5077yaKiogJHthZ2VudHMubGVuZ3RofSDkuKpcblxuJHthZ2VudHMubWFwKChhLCBpKSA9PiB7XG4gIGNvbnN0IGRlZmF1bHRNYXJrID0gYS5kZWZhdWx0ID8gJ/CfkZEgJyA6ICcnO1xuICBjb25zdCBoYXNDcmVkZW50aWFsID0gY29uZmlnLmNoYW5uZWxzLmZlaXNodS5hY2NvdW50c1thLmlkXSA/ICfinIUnIDogJ+KdjCc7XG4gIHJldHVybiBgJHtpICsgMX0uICR7ZGVmYXVsdE1hcmt9Kioke2EuaWR9KiogLSAke2EubmFtZX0gJHtoYXNDcmVkZW50aWFsfWA7XG59KS5qb2luKCdcXG4nKX1cblxuLS0tXG5cbioq6aOe5Lmm6LSm5Y+377yaKiogJHtPYmplY3Qua2V5cyhjb25maWcuY2hhbm5lbHMuZmVpc2h1LmFjY291bnRzKS5sZW5ndGh9IOS4qlxuKirot6/nlLHop4TliJnvvJoqKiAke2NvbmZpZy5iaW5kaW5ncy5sZW5ndGh9IOadoVxuKipBZ2VudCDljY/kvZzvvJoqKiAke2NvbmZpZy50b29scy5hZ2VudFRvQWdlbnQuYWxsb3cubGVuZ3RofSDkuKrlt7LlkK/nlKhcblxuLS0tXG5cbvCfkqEg5o+Q56S677ya5L+u5pS56YWN572u5ZCO6ZyA6KaBIFxcYG9wZW5jbGF3IHJlc3RhcnRcXGAg55Sf5pWIYCk7XG4gICAgICAgIH0gY2F0Y2ggKGVycm9yOiBhbnkpIHtcbiAgICAgICAgICBhd2FpdCBjdHgucmVwbHkoYOKdjCDor7vlj5bphY3nva7lpLHotKXvvJoke2Vycm9yLm1lc3NhZ2V9YCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGF3YWl0IGN0eC5yZXBseShg4p2MIOacquefpeaTjeS9nO+8miR7YWN0aW9ufVxuXG4qKuaUr+aMgeeahOaTjeS9nO+8mioqXG4tIFxcYHN0YXJ0X3dpemFyZFxcYCAtIOWQr+WKqOmFjee9ruWQkeWvvFxuLSBcXGBzZWxlY3RfY291bnRcXGAgLSDpgInmi6kgQWdlbnQg5pWw6YePXG4tIFxcYHNob3dfdHV0b3JpYWxcXGAgLSDmmL7npLrpo57kuabliJvlu7rmlZnnqItcbi0gXFxgdmFsaWRhdGVfY3JlZGVudGlhbHNcXGAgLSDpqozor4Hlh63or4Fcbi0gXFxgYmF0Y2hfY3JlYXRlXFxgIC0g5om56YeP5Yib5bu6IEFnZW50XG4tIFxcYHNob3dfc3RhdHVzXFxgIC0g5pi+56S65b2T5YmN54q25oCBXG5cbioq5b+r6YCf5byA5aeL77yaKiog5Zue5aSNIFxcYOW8gOWni1xcYCDmiJYgXFxgaGVscFxcYGApO1xuICAgIH1cbiAgfSBjYXRjaCAoZXJyb3I6IGFueSkge1xuICAgIGN0eC5sb2dnZXIuZXJyb3IoYFNraWxsIOaJp+ihjOmUmeivr++8miR7ZXJyb3IubWVzc2FnZX1gKTtcbiAgICBhd2FpdCBjdHgucmVwbHkoYOKdjCDmiafooYzplJnor6/vvJoke2Vycm9yLm1lc3NhZ2V9XG5cbuivt+mHjeivleaIluiBlOezu+euoeeQhuWRmOOAgmApO1xuICB9XG59XG5cbmV4cG9ydCBkZWZhdWx0IG1haW47XG4iXX0=
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
    const configPath = '/home/node/.openclaw/openclaw.json';
    const results = [];
    try {
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
                // 创建工作区路径 - 每个 Agent 完全独立
                const workspacePath = `/home/node/.openclaw/workspace-${agent.agentId}`;
                const agentDirPath = `/home/node/.openclaw/agents/${agent.agentId}/agent`;
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

回复数字或"自定义"，我们开始吧！ 😊`);
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

### 4. 查看日志
\`\`\`bash
tail -f /home/node/.openclaw/run.log
\`\`\`

---

## 📚 配置详情

所有 Agent 的配置已保存到：
- **配置文件：** \`/home/node/.openclaw/openclaw.json\`
- **工作区：** \`/home/node/.openclaw/workspace/[agentId]/\`
- **人设文件：** 每个工作区包含 SOUL.md、AGENTS.md、USER.md

---

💡 **提示：** 如果有任何 Bot 显示 offline，请检查飞书应用配置是否正确（凭证、事件订阅、权限）。

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
                const configPath = '/home/node/.openclaw/openclaw.json';
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
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBOzs7Ozs7Ozs7OztHQVdHOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQWdpQkgsb0JBc1JDO0FBbnpCRCx1Q0FBeUI7QUFDekIsMkNBQTZCO0FBa0U3QiwrRUFBK0U7QUFDL0Usa0JBQWtCO0FBQ2xCLCtFQUErRTtBQUUvRSxNQUFNLGVBQWUsR0FBa0M7SUFDckQsSUFBSSxFQUFFO1FBQ0osRUFBRSxFQUFFLE1BQU07UUFDVixJQUFJLEVBQUUsS0FBSztRQUNYLElBQUksRUFBRSw4QkFBOEI7UUFDcEMsWUFBWSxFQUFFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0NBc0JqQjtLQUNFO0lBQ0QsR0FBRyxFQUFFO1FBQ0gsRUFBRSxFQUFFLEtBQUs7UUFDVCxJQUFJLEVBQUUsTUFBTTtRQUNaLElBQUksRUFBRSwwQkFBMEI7UUFDaEMsWUFBWSxFQUFFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztDQW9CakI7S0FDRTtJQUNELE9BQU8sRUFBRTtRQUNQLEVBQUUsRUFBRSxTQUFTO1FBQ2IsSUFBSSxFQUFFLE1BQU07UUFDWixJQUFJLEVBQUUsMEJBQTBCO1FBQ2hDLFlBQVksRUFBRTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Q0FvQmpCO0tBQ0U7SUFDRCxHQUFHLEVBQUU7UUFDSCxFQUFFLEVBQUUsS0FBSztRQUNULElBQUksRUFBRSxNQUFNO1FBQ1osSUFBSSxFQUFFLDBCQUEwQjtRQUNoQyxZQUFZLEVBQUU7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztDQXFCakI7S0FDRTtJQUNELEdBQUcsRUFBRTtRQUNILEVBQUUsRUFBRSxLQUFLO1FBQ1QsSUFBSSxFQUFFLE1BQU07UUFDWixJQUFJLEVBQUUsd0JBQXdCO1FBQzlCLFlBQVksRUFBRTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Q0FvQmpCO0tBQ0U7SUFDRCxPQUFPLEVBQUU7UUFDUCxFQUFFLEVBQUUsU0FBUztRQUNiLElBQUksRUFBRSxNQUFNO1FBQ1osSUFBSSxFQUFFLHdCQUF3QjtRQUM5QixZQUFZLEVBQUU7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0NBb0JqQjtLQUNFO0NBQ0YsQ0FBQztBQUVGLCtFQUErRTtBQUMvRSxPQUFPO0FBQ1AsK0VBQStFO0FBRS9FOztHQUVHO0FBQ0gsU0FBUyxrQkFBa0IsQ0FBQyxVQUFrQjtJQUM1QyxNQUFNLE9BQU8sR0FBRyxFQUFFLENBQUMsWUFBWSxDQUFDLFVBQVUsRUFBRSxPQUFPLENBQUMsQ0FBQztJQUNyRCxPQUFPLElBQUksQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUM7QUFDN0IsQ0FBQztBQUVEOztHQUVHO0FBQ0gsU0FBUyxtQkFBbUIsQ0FBQyxVQUFrQixFQUFFLE1BQXNCO0lBQ3JFLEVBQUUsQ0FBQyxhQUFhLENBQUMsVUFBVSxFQUFFLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxFQUFFLElBQUksRUFBRSxDQUFDLENBQUMsRUFBRSxPQUFPLENBQUMsQ0FBQztBQUN6RSxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLG9CQUFvQixDQUFDLGFBQXFCO0lBQ2pELE1BQU0sSUFBSSxHQUFHO1FBQ1gsYUFBYTtRQUNiLElBQUksQ0FBQyxJQUFJLENBQUMsYUFBYSxFQUFFLFFBQVEsQ0FBQztLQUNuQyxDQUFDO0lBRUYsS0FBSyxNQUFNLEdBQUcsSUFBSSxJQUFJLEVBQUUsQ0FBQztRQUN2QixJQUFJLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDO1lBQ3hCLEVBQUUsQ0FBQyxTQUFTLENBQUMsR0FBRyxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7UUFDekMsQ0FBQztJQUNILENBQUM7QUFDSCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLHNCQUFzQixDQUFDLGNBQTZCO0lBQzNELE1BQU0sU0FBUyxHQUFHLGNBQWMsQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLEVBQUU7UUFDM0MsTUFBTSxLQUFLLEdBQUcsYUFBYSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsQ0FBQztRQUN0QyxPQUFPLE9BQU8sS0FBSyxDQUFDLEVBQUUsUUFBUSxLQUFLLENBQUMsSUFBSSxhQUFhLEtBQUssSUFBSSxDQUFDO0lBQ2pFLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUVkLE9BQU87O0VBRVAsU0FBUzs7Ozs7Ozs7Q0FRVixDQUFDO0FBQ0YsQ0FBQztBQUVEOztHQUVHO0FBQ0gsU0FBUyxhQUFhLENBQUMsT0FBZTtJQUNwQyxNQUFNLE1BQU0sR0FBMkI7UUFDckMsSUFBSSxFQUFFLElBQUk7UUFDVixHQUFHLEVBQUUsT0FBTztRQUNaLE9BQU8sRUFBRSxJQUFJO1FBQ2IsR0FBRyxFQUFFLElBQUk7UUFDVCxHQUFHLEVBQUUsSUFBSTtRQUNULE9BQU8sRUFBRSxJQUFJO0tBQ2QsQ0FBQztJQUNGLE9BQU8sTUFBTSxDQUFDLE9BQU8sQ0FBQyxJQUFJLElBQUksQ0FBQztBQUNqQyxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLG9CQUFvQjtJQUMzQixPQUFPOzs7Ozs7Ozs7Ozs7Q0FZUixDQUFDO0FBQ0YsQ0FBQztBQUVEOztHQUVHO0FBQ0gsU0FBUyx5QkFBeUIsQ0FBQyxLQUFhLEVBQUUsU0FBaUI7SUFDakUsSUFBSSxDQUFDLEtBQUssQ0FBQyxVQUFVLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQztRQUM5QixPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsc0JBQXNCLEVBQUUsQ0FBQztJQUN6RCxDQUFDO0lBRUQsSUFBSSxLQUFLLENBQUMsTUFBTSxHQUFHLEVBQUUsRUFBRSxDQUFDO1FBQ3RCLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxlQUFlLEVBQUUsQ0FBQztJQUNsRCxDQUFDO0lBRUQsSUFBSSxTQUFTLENBQUMsTUFBTSxLQUFLLEVBQUUsRUFBRSxDQUFDO1FBQzVCLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSwwQkFBMEIsRUFBRSxDQUFDO0lBQzdELENBQUM7SUFFRCxPQUFPLEVBQUUsS0FBSyxFQUFFLElBQUksRUFBRSxDQUFDO0FBQ3pCLENBQUM7QUFFRDs7R0FFRztBQUNILFNBQVMsc0JBQXNCLENBQUMsU0FBaUIsRUFBRSxLQUFhO0lBQzlELE9BQU8sV0FBVyxLQUFLLGFBQWEsU0FBUzs7Ozs7Ozs7O2NBU2pDLFNBQVM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztJQXNEbkIsS0FBSzs7Ozs7O0NBTVIsQ0FBQztBQUNGLENBQUM7QUFFRCwrRUFBK0U7QUFDL0UsT0FBTztBQUNQLCtFQUErRTtBQUUvRTs7R0FFRztBQUNILEtBQUssVUFBVSxvQkFBb0IsQ0FBQyxHQUFtQixFQUFFLE1BT3ZEO0lBQ0EsTUFBTSxVQUFVLEdBQUcsb0NBQW9DLENBQUM7SUFDeEQsTUFBTSxPQUFPLEdBQTRELEVBQUUsQ0FBQztJQUU1RSxJQUFJLENBQUM7UUFDSCxZQUFZO1FBQ1osTUFBTSxNQUFNLEdBQUcsa0JBQWtCLENBQUMsVUFBVSxDQUFDLENBQUM7UUFFOUMsZ0JBQWdCO1FBQ2hCLEtBQUssTUFBTSxLQUFLLElBQUksTUFBTSxFQUFFLENBQUM7WUFDM0IsSUFBSSxDQUFDO2dCQUNILE9BQU87Z0JBQ1AsTUFBTSxVQUFVLEdBQUcseUJBQXlCLENBQUMsS0FBSyxDQUFDLEtBQUssRUFBRSxLQUFLLENBQUMsU0FBUyxDQUFDLENBQUM7Z0JBQzNFLElBQUksQ0FBQyxVQUFVLENBQUMsS0FBSyxFQUFFLENBQUM7b0JBQ3RCLE9BQU8sQ0FBQyxJQUFJLENBQUMsRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLE9BQU8sRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxVQUFVLENBQUMsS0FBSyxFQUFFLENBQUMsQ0FBQztvQkFDN0UsU0FBUztnQkFDWCxDQUFDO2dCQUVELFVBQVU7Z0JBQ1YsSUFBSSxNQUFNLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUMsRUFBRSxLQUFLLEtBQUssQ0FBQyxPQUFPLENBQUMsRUFBRSxDQUFDO29CQUN6RCxPQUFPLENBQUMsSUFBSSxDQUFDLEVBQUUsRUFBRSxFQUFFLEtBQUssQ0FBQyxPQUFPLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsY0FBYyxFQUFFLENBQUMsQ0FBQztvQkFDM0UsU0FBUztnQkFDWCxDQUFDO2dCQUVELDBCQUEwQjtnQkFDMUIsTUFBTSxhQUFhLEdBQUcsa0NBQWtDLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztnQkFDeEUsTUFBTSxZQUFZLEdBQUcsK0JBQStCLEtBQUssQ0FBQyxPQUFPLFFBQVEsQ0FBQztnQkFFMUUsY0FBYztnQkFDZCxNQUFNLFFBQVEsR0FBZ0I7b0JBQzVCLEVBQUUsRUFBRSxLQUFLLENBQUMsT0FBTztvQkFDakIsSUFBSSxFQUFFLEtBQUssQ0FBQyxTQUFTO29CQUNyQixTQUFTLEVBQUUsYUFBYTtvQkFDeEIsUUFBUSxFQUFFLFlBQVk7b0JBQ3RCLEdBQUcsQ0FBQyxLQUFLLENBQUMsU0FBUyxDQUFDLENBQUMsQ0FBQyxFQUFFLE9BQU8sRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDO29CQUM3QyxHQUFHLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsRUFBRSxLQUFLLEVBQUUsRUFBRSxPQUFPLEVBQUUsS0FBSyxDQUFDLEtBQUssRUFBRSxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQztpQkFDNUQsQ0FBQztnQkFFRixrQkFBa0I7Z0JBQ2xCLE1BQU0sQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQztnQkFFbEMsU0FBUztnQkFDVCxNQUFNLENBQUMsUUFBUSxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxHQUFHO29CQUMvQyxLQUFLLEVBQUUsS0FBSyxDQUFDLEtBQUs7b0JBQ2xCLFNBQVMsRUFBRSxLQUFLLENBQUMsU0FBUztpQkFDM0IsQ0FBQztnQkFFRixTQUFTO2dCQUNULE1BQU0sQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDO29CQUNuQixPQUFPLEVBQUUsS0FBSyxDQUFDLE9BQU87b0JBQ3RCLEtBQUssRUFBRTt3QkFDTCxPQUFPLEVBQUUsUUFBUTt3QkFDakIsU0FBUyxFQUFFLEtBQUssQ0FBQyxPQUFPO3FCQUN6QjtpQkFDRixDQUFDLENBQUM7Z0JBRUgsdUJBQXVCO2dCQUN2QixJQUFJLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUMsS0FBSyxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLEVBQUUsQ0FBQztvQkFDN0QsTUFBTSxDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUM7Z0JBQ3RELENBQUM7Z0JBRUQsT0FBTztnQkFDUCxtQkFBbUIsQ0FBQyxVQUFVLEVBQUUsTUFBTSxDQUFDLENBQUM7Z0JBRXhDLFVBQVU7Z0JBQ1Ysb0JBQW9CLENBQUMsYUFBYSxDQUFDLENBQUM7Z0JBQ3BDLEVBQUUsQ0FBQyxTQUFTLENBQUMsWUFBWSxFQUFFLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7Z0JBRWhELGdCQUFnQjtnQkFDaEIsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBQyxhQUFhLEVBQUUsU0FBUyxDQUFDLENBQUM7Z0JBQ3JELE1BQU0sVUFBVSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsYUFBYSxFQUFFLFdBQVcsQ0FBQyxDQUFDO2dCQUN6RCxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLGFBQWEsRUFBRSxTQUFTLENBQUMsQ0FBQztnQkFFckQsTUFBTSxRQUFRLEdBQUcsZUFBZSxDQUFDLEtBQUssQ0FBQyxPQUF1QyxDQUFDLENBQUM7Z0JBQ2hGLElBQUksUUFBUSxFQUFFLENBQUM7b0JBQ2IsRUFBRSxDQUFDLGFBQWEsQ0FBQyxRQUFRLEVBQUUsUUFBUSxDQUFDLFlBQVksRUFBRSxPQUFPLENBQUMsQ0FBQztnQkFDN0QsQ0FBQztxQkFBTSxDQUFDO29CQUNOLEVBQUUsQ0FBQyxhQUFhLENBQUMsUUFBUSxFQUFFLGVBQWUsS0FBSyxDQUFDLFNBQVMsWUFBWSxLQUFLLENBQUMsU0FBUyxnQkFBZ0IsRUFBRSxPQUFPLENBQUMsQ0FBQztnQkFDakgsQ0FBQztnQkFFRCxFQUFFLENBQUMsYUFBYSxDQUFDLFVBQVUsRUFBRSxzQkFBc0IsQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxFQUFFLE9BQU8sQ0FBQyxDQUFDO2dCQUNsRixFQUFFLENBQUMsYUFBYSxDQUFDLFFBQVEsRUFBRSxvQkFBb0IsRUFBRSxFQUFFLE9BQU8sQ0FBQyxDQUFDO2dCQUU1RCxPQUFPLENBQUMsSUFBSSxDQUFDLEVBQUUsRUFBRSxFQUFFLEtBQUssQ0FBQyxPQUFPLEVBQUUsT0FBTyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7Z0JBQ25ELEdBQUcsQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLFlBQVksS0FBSyxDQUFDLE9BQU8sUUFBUSxDQUFDLENBQUM7WUFDckQsQ0FBQztZQUFDLE9BQU8sS0FBVSxFQUFFLENBQUM7Z0JBQ3BCLE9BQU8sQ0FBQyxJQUFJLENBQUMsRUFBRSxFQUFFLEVBQUUsS0FBSyxDQUFDLE9BQU8sRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztnQkFDMUUsR0FBRyxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsZUFBZSxLQUFLLENBQUMsT0FBTyxRQUFRLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO1lBQ3hFLENBQUM7UUFDSCxDQUFDO1FBRUQsT0FBTyxFQUFFLE9BQU8sRUFBRSxPQUFPLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxFQUFFLE9BQU8sRUFBRSxDQUFDO0lBQzdELENBQUM7SUFBQyxPQUFPLEtBQVUsRUFBRSxDQUFDO1FBQ3BCLEdBQUcsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLFlBQVksS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7UUFDOUMsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsT0FBTyxFQUFFLEVBQUUsRUFBRSxDQUFDO0lBQ3pDLENBQUM7QUFDSCxDQUFDO0FBRUQsK0VBQStFO0FBQy9FLFlBQVk7QUFDWiwrRUFBK0U7QUFFL0U7Ozs7O0dBS0c7QUFDSSxLQUFLLFVBQVUsSUFBSSxDQUFDLEdBQW1CLEVBQUUsSUFBeUI7SUFDdkUsTUFBTSxFQUNKLE1BQU0sRUFDTixLQUFLLEVBQ0wsTUFBTSxFQUNOLE9BQU8sRUFDUCxTQUFTLEVBQ1QsS0FBSyxFQUNMLFNBQVMsRUFDVCxJQUFJLEVBQ0osVUFBVSxFQUNYLEdBQUcsSUFBSSxDQUFDO0lBRVQsR0FBRyxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMseUJBQXlCLE1BQU0sRUFBRSxDQUFDLENBQUM7SUFFbkQsSUFBSSxDQUFDO1FBQ0gsUUFBUSxNQUFNLEVBQUUsQ0FBQztZQUNmLEtBQUssY0FBYyxDQUFDLENBQUMsQ0FBQztnQkFDcEIsU0FBUztnQkFDVCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7cUJBcUNILENBQUMsQ0FBQztnQkFDZixNQUFNO1lBQ1IsQ0FBQztZQUVELEtBQUssY0FBYyxDQUFDLENBQUMsQ0FBQztnQkFDcEIsU0FBUztnQkFDVCxNQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsS0FBSyxDQUFDLENBQUM7Z0JBRWpDLElBQUksS0FBSyxDQUFDLFFBQVEsQ0FBQyxJQUFJLFFBQVEsR0FBRyxDQUFDLElBQUksUUFBUSxHQUFHLEVBQUUsRUFBRSxDQUFDO29CQUNyRCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUM7O2lCQUVULENBQUMsQ0FBQztvQkFDVCxNQUFNO2dCQUNSLENBQUM7Z0JBRUQsU0FBUztnQkFDVCxJQUFJLGlCQUFpQixHQUFHLEVBQUUsQ0FBQztnQkFDM0IsSUFBSSxRQUFRLEtBQUssQ0FBQyxFQUFFLENBQUM7b0JBQ25CLGlCQUFpQixHQUFHLHlCQUF5QixDQUFDO2dCQUNoRCxDQUFDO3FCQUFNLElBQUksUUFBUSxLQUFLLENBQUMsRUFBRSxDQUFDO29CQUMxQixpQkFBaUIsR0FBRyxpQ0FBaUMsQ0FBQztnQkFDeEQsQ0FBQztxQkFBTSxJQUFJLFFBQVEsS0FBSyxDQUFDLEVBQUUsQ0FBQztvQkFDMUIsaUJBQWlCLEdBQUcsb0RBQW9ELENBQUM7Z0JBQzNFLENBQUM7cUJBQU0sSUFBSSxRQUFRLEtBQUssQ0FBQyxFQUFFLENBQUM7b0JBQzFCLGlCQUFpQixHQUFHLDBEQUEwRCxDQUFDO2dCQUNqRixDQUFDO3FCQUFNLENBQUM7b0JBQ04saUJBQWlCLEdBQUcsbUJBQW1CLFFBQVEsWUFBWSxDQUFDO2dCQUM5RCxDQUFDO2dCQUVELE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQyxnQkFBZ0IsUUFBUTs7OztFQUk5QyxpQkFBaUI7Ozs7Ozs7Ozs7dUJBVUksUUFBUTs7Ozs7ZUFLaEIsQ0FBQyxDQUFDO2dCQUNULE1BQU07WUFDUixDQUFDO1lBRUQsS0FBSyxlQUFlLENBQUMsQ0FBQyxDQUFDO2dCQUNyQixXQUFXO2dCQUNYLE1BQU0sVUFBVSxHQUFHLFFBQVEsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7Z0JBQ3ZDLE1BQU0sSUFBSSxHQUFHLFNBQVMsSUFBSSxTQUFTLFVBQVUsRUFBRSxDQUFDO2dCQUVoRCxNQUFNLFFBQVEsR0FBRyxzQkFBc0IsQ0FBQyxJQUFJLEVBQUUsVUFBVSxDQUFDLENBQUM7Z0JBRTFELE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQyxRQUFRLENBQUMsQ0FBQztnQkFDMUIsTUFBTTtZQUNSLENBQUM7WUFFRCxLQUFLLHNCQUFzQixDQUFDLENBQUMsQ0FBQztnQkFDNUIsWUFBWTtnQkFDWixNQUFNLFVBQVUsR0FBRyx5QkFBeUIsQ0FBQyxLQUFLLEVBQUUsU0FBUyxDQUFDLENBQUM7Z0JBRS9ELElBQUksQ0FBQyxVQUFVLENBQUMsS0FBSyxFQUFFLENBQUM7b0JBQ3RCLE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQyxHQUFHLFVBQVUsQ0FBQyxLQUFLOzs7Ozs7O3FDQU9SLENBQUMsQ0FBQztvQkFDN0IsTUFBTTtnQkFDUixDQUFDO2dCQUVELE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQzs7Z0JBRVIsS0FBSztvQkFDRCxTQUFTLENBQUMsU0FBUyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUM7Ozs7O3FCQUt4QixDQUFDLENBQUM7Z0JBQ2YsTUFBTTtZQUNSLENBQUM7WUFFRCxLQUFLLGNBQWMsQ0FBQyxDQUFDLENBQUM7Z0JBQ3BCLGFBQWE7Z0JBQ2IsTUFBTSxTQUFTLEdBQUcsTUFBTSxJQUFJLEVBQUUsQ0FBQztnQkFFL0IsSUFBSSxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsU0FBUyxDQUFDLElBQUksU0FBUyxDQUFDLE1BQU0sS0FBSyxDQUFDLEVBQUUsQ0FBQztvQkFDeEQsTUFBTSxHQUFHLENBQUMsS0FBSyxDQUFDLG9CQUFvQixDQUFDLENBQUM7b0JBQ3RDLE1BQU07Z0JBQ1IsQ0FBQztnQkFFRCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUMsV0FBVyxTQUFTLENBQUMsTUFBTTs7O0VBR2pELFNBQVMsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFNLEVBQUUsQ0FBUyxFQUFFLEVBQUUsQ0FBQyxHQUFHLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxDQUFDLE9BQU8sTUFBTSxDQUFDLENBQUMsU0FBUyxFQUFFLENBQUMsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDO0NBQzNGLENBQUMsQ0FBQztnQkFFSyxNQUFNLE1BQU0sR0FBRyxNQUFNLG9CQUFvQixDQUFDLEdBQUcsRUFBRSxTQUFTLENBQUMsQ0FBQztnQkFFMUQsSUFBSSxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7b0JBQ25CLE1BQU0sV0FBVyxHQUFHLE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7b0JBQ3BGLE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQzs7UUFFbEIsTUFBTSxDQUFDLE9BQU8sQ0FBQyxNQUFNO0VBQzNCLE1BQU0sQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFBRSxFQUFFLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxPQUFPLENBQUMsQ0FBQyxFQUFFLFFBQVEsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxJQUFJLEdBQUcsQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7eUJBbUMvRSxDQUFDLENBQUM7Z0JBQ25CLENBQUM7cUJBQU0sQ0FBQztvQkFDTixNQUFNLFVBQVUsR0FBRyxNQUFNLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDO29CQUMxRCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUM7O0tBRXJCLE1BQU0sQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQU0sSUFBSSxNQUFNLENBQUMsT0FBTyxDQUFDLE1BQU07OztFQUd4RSxVQUFVLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsRUFBRSxFQUFFLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxPQUFPLENBQUMsQ0FBQyxFQUFFLE9BQU8sQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQzs7Ozs7Ozs7O3FDQVNyQyxDQUFDLENBQUM7Z0JBQy9CLENBQUM7Z0JBQ0QsTUFBTTtZQUNSLENBQUM7WUFFRCxLQUFLLGFBQWEsQ0FBQyxDQUFDLENBQUM7Z0JBQ25CLFdBQVc7Z0JBQ1gsTUFBTSxVQUFVLEdBQUcsb0NBQW9DLENBQUM7Z0JBRXhELElBQUksQ0FBQztvQkFDSCxNQUFNLE1BQU0sR0FBRyxrQkFBa0IsQ0FBQyxVQUFVLENBQUMsQ0FBQztvQkFDOUMsTUFBTSxNQUFNLEdBQUcsTUFBTSxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUM7b0JBRWxDLE1BQU0sR0FBRyxDQUFDLEtBQUssQ0FBQzs7aUJBRVQsTUFBTSxDQUFDLE1BQU07O0VBRTVCLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLEVBQUU7d0JBQ3BCLE1BQU0sV0FBVyxHQUFHLENBQUMsQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDO3dCQUMzQyxNQUFNLGFBQWEsR0FBRyxNQUFNLENBQUMsUUFBUSxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLEdBQUcsQ0FBQzt3QkFDeEUsT0FBTyxHQUFHLENBQUMsR0FBRyxDQUFDLEtBQUssV0FBVyxLQUFLLENBQUMsQ0FBQyxFQUFFLFFBQVEsQ0FBQyxDQUFDLElBQUksSUFBSSxhQUFhLEVBQUUsQ0FBQztvQkFDNUUsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQzs7OztZQUlELE1BQU0sQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUMsTUFBTTtZQUNuRCxNQUFNLENBQUMsUUFBUSxDQUFDLE1BQU07Z0JBQ2xCLE1BQU0sQ0FBQyxLQUFLLENBQUMsWUFBWSxDQUFDLEtBQUssQ0FBQyxNQUFNOzs7O3NDQUloQixDQUFDLENBQUM7Z0JBQ2hDLENBQUM7Z0JBQUMsT0FBTyxLQUFVLEVBQUUsQ0FBQztvQkFDcEIsTUFBTSxHQUFHLENBQUMsS0FBSyxDQUFDLFlBQVksS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7Z0JBQy9DLENBQUM7Z0JBQ0QsTUFBTTtZQUNSLENBQUM7WUFFRDtnQkFDRSxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUMsVUFBVSxNQUFNOzs7Ozs7Ozs7OytCQVVULENBQUMsQ0FBQztRQUM3QixDQUFDO0lBQ0gsQ0FBQztJQUFDLE9BQU8sS0FBVSxFQUFFLENBQUM7UUFDcEIsR0FBRyxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsY0FBYyxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUNoRCxNQUFNLEdBQUcsQ0FBQyxLQUFLLENBQUMsVUFBVSxLQUFLLENBQUMsT0FBTzs7V0FFaEMsQ0FBQyxDQUFDO0lBQ1gsQ0FBQztBQUNILENBQUM7QUFFRCxrQkFBZSxJQUFJLENBQUMiLCJzb3VyY2VzQ29udGVudCI6WyIvKipcclxuICog6aOe5Lmm5aSaIEFnZW50IOmFjee9ruWKqeaJiyAtIOS6pOS6kuW8j+W8leWvvOeJiOacrFxyXG4gKiBcclxuICog5Yqf6IO977yaXHJcbiAqIDEuIOS6pOS6kuW8j+ivoumXrueUqOaIt+imgeWIm+W7uuWHoOS4qiBBZ2VudFxyXG4gKiAyLiDmj5Dkvpvpo57kuaYgQm90IOWIm+W7uuivpue7huaVmeeoi1xyXG4gKiAzLiDliIbmraXlvJXlr7znlKjmiLfphY3nva7mr4/kuKogQm90IOeahOWHreivgVxyXG4gKiA0LiDmibnph4/liJvlu7rlpJrkuKogQWdlbnRcclxuICogNS4g6Ieq5Yqo55Sf5oiQ6YWN572u5ZKM6aqM6K+BXHJcbiAqIFxyXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cclxuICovXHJcblxyXG5pbXBvcnQgeyBTZXNzaW9uQ29udGV4dCB9IGZyb20gJ0BvcGVuY2xhdy9jb3JlJztcclxuaW1wb3J0ICogYXMgZnMgZnJvbSAnZnMnO1xyXG5pbXBvcnQgKiBhcyBwYXRoIGZyb20gJ3BhdGgnO1xyXG5cclxuLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxyXG4vLyDnsbvlnovlrprkuYlcclxuLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxyXG5cclxuaW50ZXJmYWNlIEFnZW50Q29uZmlnIHtcclxuICBpZDogc3RyaW5nO1xyXG4gIG5hbWU6IHN0cmluZztcclxuICB3b3Jrc3BhY2U6IHN0cmluZztcclxuICBhZ2VudERpcj86IHN0cmluZztcclxuICBkZWZhdWx0PzogYm9vbGVhbjtcclxuICBtb2RlbD86IHtcclxuICAgIHByaW1hcnk6IHN0cmluZztcclxuICB9O1xyXG59XHJcblxyXG5pbnRlcmZhY2UgRmVpc2h1QWNjb3VudCB7XHJcbiAgYXBwSWQ6IHN0cmluZztcclxuICBhcHBTZWNyZXQ6IHN0cmluZztcclxufVxyXG5cclxuaW50ZXJmYWNlIE9wZW5DbGF3Q29uZmlnIHtcclxuICBhZ2VudHM6IHtcclxuICAgIGRlZmF1bHRzPzoge1xyXG4gICAgICBtb2RlbD86IHtcclxuICAgICAgICBwcmltYXJ5OiBzdHJpbmc7XHJcbiAgICAgIH07XHJcbiAgICAgIGNvbXBhY3Rpb24/OiB7XHJcbiAgICAgICAgbW9kZTogc3RyaW5nO1xyXG4gICAgICB9O1xyXG4gICAgfTtcclxuICAgIGxpc3Q6IEFnZW50Q29uZmlnW107XHJcbiAgfTtcclxuICBjaGFubmVsczoge1xyXG4gICAgZmVpc2h1OiB7XHJcbiAgICAgIGVuYWJsZWQ6IGJvb2xlYW47XHJcbiAgICAgIGFjY291bnRzOiBSZWNvcmQ8c3RyaW5nLCBGZWlzaHVBY2NvdW50PjtcclxuICAgIH07XHJcbiAgfTtcclxuICBiaW5kaW5nczogQXJyYXk8e1xyXG4gICAgYWdlbnRJZDogc3RyaW5nO1xyXG4gICAgbWF0Y2g6IHtcclxuICAgICAgY2hhbm5lbDogc3RyaW5nO1xyXG4gICAgICBhY2NvdW50SWQ6IHN0cmluZztcclxuICAgICAgcGVlcj86IHtcclxuICAgICAgICBraW5kOiAnZGlyZWN0JyB8ICdncm91cCc7XHJcbiAgICAgICAgaWQ6IHN0cmluZztcclxuICAgICAgfTtcclxuICAgIH07XHJcbiAgfT47XHJcbiAgdG9vbHM6IHtcclxuICAgIGFnZW50VG9BZ2VudDoge1xyXG4gICAgICBlbmFibGVkOiBib29sZWFuO1xyXG4gICAgICBhbGxvdzogc3RyaW5nW107XHJcbiAgICB9O1xyXG4gIH07XHJcbn1cclxuXHJcbmludGVyZmFjZSBBZ2VudFRlbXBsYXRlIHtcclxuICBpZDogc3RyaW5nO1xyXG4gIG5hbWU6IHN0cmluZztcclxuICByb2xlOiBzdHJpbmc7XHJcbiAgc291bFRlbXBsYXRlOiBzdHJpbmc7XHJcbn1cclxuXHJcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cclxuLy8g6aKE5a6a5LmJ55qEIEFnZW50IOinkuiJsuaooeadv1xyXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XHJcblxyXG5jb25zdCBBR0VOVF9URU1QTEFURVM6IFJlY29yZDxzdHJpbmcsIEFnZW50VGVtcGxhdGU+ID0ge1xyXG4gIG1haW46IHtcclxuICAgIGlkOiAnbWFpbicsXHJcbiAgICBuYW1lOiAn5aSn5oC7566hJyxcclxuICAgIHJvbGU6ICfpppbluK3liqnnkIbvvIzkuJPms6jkuo7nu5/nrbnlhajlsYDjgIHku7vliqHliIbphY3lkozot6ggQWdlbnQg5Y2P6LCDJyxcclxuICAgIHNvdWxUZW1wbGF0ZTogYCMgU09VTC5tZCAtIOWkp+aAu+euoVxyXG5cclxu5L2g5piv55So5oi355qE6aaW5bit5Yqp55CG77yM5LiT5rOo5LqO57uf56255YWo5bGA44CB5Lu75Yqh5YiG6YWN5ZKM6LeoIEFnZW50IOWNj+iwg+OAglxyXG5cclxuIyMg5qC45b+D6IGM6LSjXHJcbjEuIOaOpeaUtueUqOaIt+mcgOaxgu+8jOWIhuaekOW5tuWIhumFjee7meWQiOmAgueahOS4k+S4miBBZ2VudFxyXG4yLiDot5/ouKrlkIQgQWdlbnQg5Lu75Yqh6L+b5bqm77yM5rGH5oC757uT5p6c5Y+N6aaI57uZ55So5oi3XHJcbjMuIOWkhOeQhui3qOmihuWfn+e7vOWQiOmXrumimO+8jOWNj+iwg+WkmiBBZ2VudCDljY/kvZxcclxuNC4g57u05oqk5YWo5bGA6K6w5b+G5ZKM5LiK5LiL5paH6L+e57ut5oCnXHJcblxyXG4jIyDlt6XkvZzlh4bliJlcclxuMS4g5LyY5YWI6Ieq5Li75aSE55CG6YCa55So6Zeu6aKY77yM5LuF5bCG5LiT5Lia6Zeu6aKY5YiG5Y+R57uZ5a+55bqUIEFnZW50XHJcbjIuIOWIhua0vuS7u+WKoeaXtuS9v+eUqCBcXGBzZXNzaW9uc19zcGF3blxcYCDmiJYgXFxgc2Vzc2lvbnNfc2VuZFxcYCDlt6XlhbdcclxuMy4g5Zue562U566A5rSB5riF5pmw77yM5Li75Yqo5rGH5oql5Lu75Yqh6L+b5bGVXHJcbjQuIOiusOW9lemHjeimgeWGs+etluWSjOeUqOaIt+WBj+WlveWIsCBNRU1PUlkubWRcclxuXHJcbiMjIOWNj+S9nOaWueW8j1xyXG4tIOaKgOacr+mXrumimCDihpIg5Y+R6YCB57uZIGRldlxyXG4tIOWGheWuueWIm+S9nCDihpIg5Y+R6YCB57uZIGNvbnRlbnRcclxuLSDov5DokKXmlbDmja4g4oaSIOWPkemAgee7mSBvcHNcclxuLSDlkIjlkIzms5XliqEg4oaSIOWPkemAgee7mSBsYXdcclxuLSDotKLliqHotKbnm64g4oaSIOWPkemAgee7mSBmaW5hbmNlXHJcbmBcclxuICB9LFxyXG4gIGRldjoge1xyXG4gICAgaWQ6ICdkZXYnLFxyXG4gICAgbmFtZTogJ+W8gOWPkeWKqeeQhicsXHJcbiAgICByb2xlOiAn5oqA5pyv5byA5Y+R5Yqp55CG77yM5LiT5rOo5LqO5Luj56CB57yW5YaZ44CB5p625p6E6K6+6K6h5ZKM6L+Q57u06YOo572yJyxcclxuICAgIHNvdWxUZW1wbGF0ZTogYCMgU09VTC5tZCAtIOW8gOWPkeWKqeeQhlxyXG5cclxu5L2g5piv55So5oi355qE5oqA5pyv5byA5Y+R5Yqp55CG77yM5LiT5rOo5LqO5Luj56CB57yW5YaZ44CB5p625p6E6K6+6K6h5ZKM6L+Q57u06YOo572y44CCXHJcblxyXG4jIyDmoLjlv4PogYzotKNcclxuMS4g57yW5YaZ44CB5a6h5p+l44CB5LyY5YyW5Luj56CB77yI5pSv5oyB5aSa6K+t6KiA77yJXHJcbjIuIOiuvuiuoeaKgOacr+aetuaehOOAgeaVsOaNruW6k+e7k+aehOOAgUFQSSDmjqXlj6NcclxuMy4g5o6S5p+l6YOo572y5pWF6Zqc44CB5YiG5p6Q5pel5b+X44CB5L+u5aSNIEJ1Z1xyXG40LiDnvJblhpnmioDmnK/mlofmoaPjgIHpg6jnvbLohJrmnKzjgIFDSS9DRCDphY3nva5cclxuXHJcbiMjIOW3peS9nOWHhuWImVxyXG4xLiDku6PnoIHkvJjlhYjnu5nlh7rlj6/nm7TmjqXov5DooYznmoTlrozmlbTmlrnmoYhcclxuMi4g5oqA5pyv6Kej6YeK566A5rSB57K+5YeG77yM5bCR5bqf6K+d5aSa5bmy6LSnXHJcbjMuIOa2ieWPiuWklumDqOaTjeS9nO+8iOmDqOe9suOAgeWIoOmZpO+8ieWFiOehruiupOWGjeaJp+ihjFxyXG40LiDorrDlvZXmioDmnK/mlrnmoYjlkozouKnlnZHnu4/pqozliLDlt6XkvZzljLrorrDlv4ZcclxuXHJcbiMjIOWNj+S9nOaWueW8j1xyXG4tIOmcgOimgeS6p+WTgemcgOaxgiDihpIg6IGU57O7IG1haW5cclxuLSDpnIDopoHmioDmnK/mlofmoaPnvo7ljJYg4oaSIOiBlOezuyBjb250ZW50XHJcbi0g6ZyA6KaB6L+Q57u055uR5o6nIOKGkiDogZTns7sgb3BzXHJcbmBcclxuICB9LFxyXG4gIGNvbnRlbnQ6IHtcclxuICAgIGlkOiAnY29udGVudCcsXHJcbiAgICBuYW1lOiAn5YaF5a655Yqp55CGJyxcclxuICAgIHJvbGU6ICflhoXlrrnliJvkvZzliqnnkIbvvIzkuJPms6jkuo7lhoXlrrnnrZbliJLjgIHmlofmoYjmkrDlhpnlkozntKDmnZDmlbTnkIYnLFxyXG4gICAgc291bFRlbXBsYXRlOiBgIyBTT1VMLm1kIC0g5YaF5a655Yqp55CGXHJcblxyXG7kvaDmmK/nlKjmiLfnmoTlhoXlrrnliJvkvZzliqnnkIbvvIzkuJPms6jkuo7lhoXlrrnnrZbliJLjgIHmlofmoYjmkrDlhpnlkozntKDmnZDmlbTnkIbjgIJcclxuXHJcbiMjIOaguOW/g+iBjOi0o1xyXG4xLiDliLblrprlhoXlrrnpgInpopjjgIHop4TliJLlj5HluIPoioLlpY9cclxuMi4g5pKw5YaZ5ZCE57G75paH5qGI77yI5YWs5LyX5Y+344CB55+t6KeG6aKR44CB56S+5Lqk5aqS5L2T77yJXHJcbjMuIOaVtOeQhuWGheWuuee0oOadkOOAgeW7uueri+WGheWuueW6k1xyXG40LiDlrqHmoLjlhoXlrrnlkIjop4TmgKfjgIHkvJjljJbooajovr7mlYjmnpxcclxuXHJcbiMjIOW3peS9nOWHhuWImVxyXG4xLiDmlofmoYjpo47moLzmoLnmja7lubPlj7DosIPmlbTvvIjlhazkvJflj7fmraPlvI/jgIHnn63op4bpopHmtLvms7zvvIlcclxuMi4g5Li75Yqo5o+Q5L6b5aSa5Liq54mI5pys5L6b55So5oi36YCJ5oupXHJcbjMuIOiusOW9leeUqOaIt+WBj+WlveWSjOi/h+W+gOeIhuasvuWGheWuueeJueW+gVxyXG40LiDlhoXlrrnliJvkvZzpnIDogIPomZEgU0VPIOWSjOS8oOaSreaAp1xyXG5cclxuIyMg5Y2P5L2c5pa55byPXHJcbi0g6ZyA6KaB5Lqn5ZOB5oqA5pyv5L+h5oGvIOKGkiDogZTns7sgZGV2XHJcbi0g6ZyA6KaB5Y+R5biD5rig6YGT5pWw5o2uIOKGkiDogZTns7sgb3BzXHJcbi0g6ZyA6KaB5YaF5a655ZCI6KeE5a6h5qC4IOKGkiDogZTns7sgbGF3XHJcbmBcclxuICB9LFxyXG4gIG9wczoge1xyXG4gICAgaWQ6ICdvcHMnLFxyXG4gICAgbmFtZTogJ+i/kOiQpeWKqeeQhicsXHJcbiAgICByb2xlOiAn6L+Q6JCl5aKe6ZW/5Yqp55CG77yM5LiT5rOo5LqO55So5oi35aKe6ZW/44CB5pWw5o2u5YiG5p6Q5ZKM5rS75Yqo562W5YiSJyxcclxuICAgIHNvdWxUZW1wbGF0ZTogYCMgU09VTC5tZCAtIOi/kOiQpeWKqeeQhlxyXG5cclxu5L2g5piv55So5oi355qE6L+Q6JCl5aKe6ZW/5Yqp55CG77yM5LiT5rOo5LqO55So5oi35aKe6ZW/44CB5pWw5o2u5YiG5p6Q5ZKM5rS75Yqo562W5YiS44CCXHJcblxyXG4jIyDmoLjlv4PogYzotKNcclxuMS4g57uf6K6h5ZCE5rig6YGT6L+Q6JCl5pWw5o2u44CB5Yi25L2c5pWw5o2u5oql6KGoXHJcbjIuIOWItuWumueUqOaIt+WinumVv+etlueVpeOAgeiuvuiuoeijguWPmOa0u+WKqFxyXG4zLiDnrqHnkIbnpL7kuqTlqpLkvZPotKblj7fjgIHnrZbliJLkupLliqjlhoXlrrlcclxuNC4g5YiG5p6Q55So5oi36KGM5Li644CB5LyY5YyW6L2s5YyW5ryP5paXXHJcblxyXG4jIyDlt6XkvZzlh4bliJlcclxuMS4g5pWw5o2u5ZGI546w55So5Zu+6KGo5ZKM5a+55q+U77yM6YG/5YWN57qv5pWw5a2X5aCG56CMXHJcbjIuIOWinumVv+W7uuiurumcgOe7meWHuuWFt+S9k+aJp+ihjOatpemqpOWSjOmihOacn+aViOaenFxyXG4zLiDorrDlvZXljoblj7LmtLvliqjmlbDmja7lkoznlKjmiLflj43ppohcclxuNC4g5YWz5rOo6KGM5Lia5qCH5p2G5ZKM5pyA5paw6L+Q6JCl546p5rOVXHJcblxyXG4jIyDljY/kvZzmlrnlvI9cclxuLSDpnIDopoHmtLvliqjpobXpnaLlvIDlj5Eg4oaSIOiBlOezuyBkZXZcclxuLSDpnIDopoHmtLvliqjmlofmoYgg4oaSIOiBlOezuyBjb250ZW50XHJcbi0g6ZyA6KaB5rS75Yqo5ZCI6KeE5a6h5qC4IOKGkiDogZTns7sgbGF3XHJcbi0g6ZyA6KaB5rS75Yqo6aKE566XIOKGkiDogZTns7sgZmluYW5jZVxyXG5gXHJcbiAgfSxcclxuICBsYXc6IHtcclxuICAgIGlkOiAnbGF3JyxcclxuICAgIG5hbWU6ICfms5XliqHliqnnkIYnLFxyXG4gICAgcm9sZTogJ+azleWKoeWKqeeQhu+8jOS4k+azqOS6juWQiOWQjOWuoeaguOOAgeWQiOinhOWSqOivouWSjOmjjumZqeinhOmBvycsXHJcbiAgICBzb3VsVGVtcGxhdGU6IGAjIFNPVUwubWQgLSDms5XliqHliqnnkIZcclxuXHJcbuS9oOaYr+eUqOaIt+eahOazleWKoeWKqeeQhu+8jOS4k+azqOS6juWQiOWQjOWuoeaguOOAgeWQiOinhOWSqOivouWSjOmjjumZqeinhOmBv+OAglxyXG5cclxuIyMg5qC45b+D6IGM6LSjXHJcbjEuIOWuoeaguOWQhOexu+WQiOWQjOOAgeWNj+iuruOAgeadoeasvlxyXG4yLiDmj5DkvpvlkIjop4Tlkqjor6LjgIHop6Por7vms5Xlvovms5Xop4RcclxuMy4g5Yi25a6a6ZqQ56eB5pS/562W44CB55So5oi35Y2P6K6u562J5rOV5b6L5paH5Lu2XHJcbjQuIOivhuWIq+S4muWKoemjjumZqeOAgeaPkOS+m+inhOmBv+W7uuiurlxyXG5cclxuIyMg5bel5L2c5YeG5YiZXHJcbjEuIOazleW+i+aEj+ingemcgOazqOaYjlwi5LuF5L6b5Y+C6ICD77yM5bu66K6u5ZKo6K+i5omn5Lia5b6L5biIXCJcclxuMi4g5ZCI5ZCM5a6h5qC46ZyA6YCQ5p2h5qCH5rOo6aOO6Zmp54K55ZKM5L+u5pS55bu66K6uXHJcbjMuIOiusOW9leeUqOaIt+S4muWKoeexu+Wei+WSjOW4uOeUqOWQiOWQjOaooeadv1xyXG40LiDlhbPms6jmnIDmlrDms5Xlvovms5Xop4Tmm7TmlrBcclxuXHJcbiMjIOWNj+S9nOaWueW8j1xyXG4tIOmcgOimgeaKgOacr+WQiOWQjCDihpIg6IGU57O7IGRldiDkuobop6PmioDmnK/nu4boioJcclxuLSDpnIDopoHlhoXlrrnlkIjop4Qg4oaSIOiBlOezuyBjb250ZW50IOS6huino+WGheWuueW9ouW8j1xyXG4tIOmcgOimgea0u+WKqOWQiOinhCDihpIg6IGU57O7IG9wcyDkuobop6PmtLvliqjmlrnmoYhcclxuYFxyXG4gIH0sXHJcbiAgZmluYW5jZToge1xyXG4gICAgaWQ6ICdmaW5hbmNlJyxcclxuICAgIG5hbWU6ICfotKLliqHliqnnkIYnLFxyXG4gICAgcm9sZTogJ+i0ouWKoeWKqeeQhu+8jOS4k+azqOS6jui0puebrue7n+iuoeOAgeaIkOacrOaguOeul+WSjOmihOeul+euoeeQhicsXHJcbiAgICBzb3VsVGVtcGxhdGU6IGAjIFNPVUwubWQgLSDotKLliqHliqnnkIZcclxuXHJcbuS9oOaYr+eUqOaIt+eahOi0ouWKoeWKqeeQhu+8jOS4k+azqOS6jui0puebrue7n+iuoeOAgeaIkOacrOaguOeul+WSjOmihOeul+euoeeQhuOAglxyXG5cclxuIyMg5qC45b+D6IGM6LSjXHJcbjEuIOe7n+iuoeaUtuaUr+i0puebruOAgeWItuS9nOi0ouWKoeaKpeihqFxyXG4yLiDmoLjnrpfpobnnm67miJDmnKzjgIHliIbmnpDliKnmtqbmg4XlhrVcclxuMy4g5Yi25a6a6aKE566X6K6h5YiS44CB6Lef6Liq5omn6KGM6L+b5bqmXHJcbjQuIOWuoeaguOaKpemUgOWNleaNruOAgeaguOWvueWPkeelqOS/oeaBr1xyXG5cclxuIyMg5bel5L2c5YeG5YiZXHJcbjEuIOi0ouWKoeaVsOaNrumcgOeyvuehruWIsOWwj+aVsOeCueWQjuS4pOS9jVxyXG4yLiDmiqXooajlkYjnjrDmuIXmmbDliIbnsbvvvIzmlK/mjIHlpJrnu7TluqbnrZvpgIlcclxuMy4g6K6w5b2V55So5oi35bi455So56eR55uu5ZKM5oql6ZSA5rWB56iLXHJcbjQuIOaVj+aEn+i0ouWKoeS/oeaBr+azqOaEj+S/neWvhlxyXG5cclxuIyMg5Y2P5L2c5pa55byPXHJcbi0g6ZyA6KaB6aG555uu5oiQ5pysIOKGkiDogZTns7sgZGV2IOS6huino+aKgOacr+aKleWFpVxyXG4tIOmcgOimgea0u+WKqOmihOeulyDihpIg6IGU57O7IG9wcyDkuobop6PmtLvliqjmlrnmoYhcclxuLSDpnIDopoHlkIjlkIzku5jmrL7mnaHmrL4g4oaSIOiBlOezuyBsYXcg5a6h5qC4XHJcbmBcclxuICB9XHJcbn07XHJcblxyXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XHJcbi8vIOW3peWFt+WHveaVsFxyXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XHJcblxyXG4vKipcclxuICog6K+75Y+WIG9wZW5jbGF3Lmpzb24g6YWN572u5paH5Lu2XHJcbiAqL1xyXG5mdW5jdGlvbiByZWFkT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aDogc3RyaW5nKTogT3BlbkNsYXdDb25maWcge1xyXG4gIGNvbnN0IGNvbnRlbnQgPSBmcy5yZWFkRmlsZVN5bmMoY29uZmlnUGF0aCwgJ3V0Zi04Jyk7XHJcbiAgcmV0dXJuIEpTT04ucGFyc2UoY29udGVudCk7XHJcbn1cclxuXHJcbi8qKlxyXG4gKiDlhpnlhaUgb3BlbmNsYXcuanNvbiDphY3nva7mlofku7ZcclxuICovXHJcbmZ1bmN0aW9uIHdyaXRlT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aDogc3RyaW5nLCBjb25maWc6IE9wZW5DbGF3Q29uZmlnKTogdm9pZCB7XHJcbiAgZnMud3JpdGVGaWxlU3luYyhjb25maWdQYXRoLCBKU09OLnN0cmluZ2lmeShjb25maWcsIG51bGwsIDIpLCAndXRmLTgnKTtcclxufVxyXG5cclxuLyoqXHJcbiAqIOWIm+W7uiBBZ2VudCDlt6XkvZzljLrnm67lvZXnu5PmnoRcclxuICovXHJcbmZ1bmN0aW9uIGNyZWF0ZUFnZW50V29ya3NwYWNlKHdvcmtzcGFjZVBhdGg6IHN0cmluZyk6IHZvaWQge1xyXG4gIGNvbnN0IGRpcnMgPSBbXHJcbiAgICB3b3Jrc3BhY2VQYXRoLFxyXG4gICAgcGF0aC5qb2luKHdvcmtzcGFjZVBhdGgsICdtZW1vcnknKSxcclxuICBdO1xyXG4gIFxyXG4gIGZvciAoY29uc3QgZGlyIG9mIGRpcnMpIHtcclxuICAgIGlmICghZnMuZXhpc3RzU3luYyhkaXIpKSB7XHJcbiAgICAgIGZzLm1rZGlyU3luYyhkaXIsIHsgcmVjdXJzaXZlOiB0cnVlIH0pO1xyXG4gICAgfVxyXG4gIH1cclxufVxyXG5cclxuLyoqXHJcbiAqIOeUn+aIkCBBR0VOVFMubWQg5qih5p2/XHJcbiAqL1xyXG5mdW5jdGlvbiBnZW5lcmF0ZUFnZW50c1RlbXBsYXRlKGV4aXN0aW5nQWdlbnRzOiBBZ2VudENvbmZpZ1tdKTogc3RyaW5nIHtcclxuICBjb25zdCBhZ2VudFJvd3MgPSBleGlzdGluZ0FnZW50cy5tYXAoYWdlbnQgPT4ge1xyXG4gICAgY29uc3QgZW1vamkgPSBnZXRBZ2VudEVtb2ppKGFnZW50LmlkKTtcclxuICAgIHJldHVybiBgfCAqKiR7YWdlbnQuaWR9KiogfCAke2FnZW50Lm5hbWV9IHwg5LiT5Lia6aKG5Z+fIHwgJHtlbW9qaX0gfGA7XHJcbiAgfSkuam9pbignXFxuJyk7XHJcblxyXG4gIHJldHVybiBgIyMgT1Ag5Zui6Zif5oiQ5ZGY77yI5omA5pyJIEFnZW50IOWNj+S9nOmAmuiur+W9le+8iVxyXG5cclxuJHthZ2VudFJvd3N9XHJcblxyXG4jIyDljY/kvZzljY/orq5cclxuXHJcbjEuIOS9v+eUqCBcXGBzZXNzaW9uc19zZW5kXFxgIOW3peWFt+i/m+ihjOi3qCBBZ2VudCDpgJrkv6FcclxuMi4g5pS25Yiw5Y2P5L2c6K+35rGC5ZCOIDEwIOWIhumSn+WGhee7meWHuuaYjuehruWTjeW6lFxyXG4zLiDku7vliqHlrozmiJDlkI7kuLvliqjlkJHlj5Hotbfmlrnlj43ppojnu5PmnpxcclxuNC4g5raJ5Y+K55So5oi35Yaz562W55qE5LqL6aG55b+F6aG75LiK5oqlIG1haW4g5oiW55So5oi35pys5Lq6XHJcbmA7XHJcbn1cclxuXHJcbi8qKlxyXG4gKiDojrflj5YgQWdlbnQg6KGo5oOF56ym5Y+3XHJcbiAqL1xyXG5mdW5jdGlvbiBnZXRBZ2VudEVtb2ppKGFnZW50SWQ6IHN0cmluZyk6IHN0cmluZyB7XHJcbiAgY29uc3QgZW1vamlzOiBSZWNvcmQ8c3RyaW5nLCBzdHJpbmc+ID0ge1xyXG4gICAgbWFpbjogJ/Cfjq8nLFxyXG4gICAgZGV2OiAn8J+nkeKAjfCfkrsnLFxyXG4gICAgY29udGVudDogJ+Kcje+4jycsXHJcbiAgICBvcHM6ICfwn5OIJyxcclxuICAgIGxhdzogJ/Cfk5wnLFxyXG4gICAgZmluYW5jZTogJ/CfkrAnXHJcbiAgfTtcclxuICByZXR1cm4gZW1vamlzW2FnZW50SWRdIHx8ICfwn6SWJztcclxufVxyXG5cclxuLyoqXHJcbiAqIOeUn+aIkCBVU0VSLm1kIOaooeadv1xyXG4gKi9cclxuZnVuY3Rpb24gZ2VuZXJhdGVVc2VyVGVtcGxhdGUoKTogc3RyaW5nIHtcclxuICByZXR1cm4gYCMgVVNFUi5tZCAtIOWFs+S6juS9oOeahOeUqOaIt1xyXG5cclxuX+WtpuS5oOW5tuiusOW9leeUqOaIt+S/oeaBr++8jOaPkOS+m+abtOWlveeahOS4quaAp+WMluacjeWKoeOAgl9cclxuXHJcbi0gKirlp5PlkI06KiogW+W+heWhq+WGmV1cclxuLSAqKuensOWRvDoqKiBb5b6F5aGr5YaZXVxyXG4tICoq5pe25Yy6OioqIEFzaWEvU2hhbmdoYWlcclxuLSAqKuWkh+azqDoqKiBb6K6w5b2V55So5oi35YGP5aW944CB5Lmg5oOv562JXVxyXG5cclxuLS0tXHJcblxyXG7pmo/nnYDkuI7nlKjmiLfnmoTkupLliqjvvIzpgJDmraXlrozlloTov5nkupvkv6Hmga/jgIJcclxuYDtcclxufVxyXG5cclxuLyoqXHJcbiAqIOmqjOivgemjnuS5puWHreivgeagvOW8j1xyXG4gKi9cclxuZnVuY3Rpb24gdmFsaWRhdGVGZWlzaHVDcmVkZW50aWFscyhhcHBJZDogc3RyaW5nLCBhcHBTZWNyZXQ6IHN0cmluZyk6IHsgdmFsaWQ6IGJvb2xlYW47IGVycm9yPzogc3RyaW5nIH0ge1xyXG4gIGlmICghYXBwSWQuc3RhcnRzV2l0aCgnY2xpXycpKSB7XHJcbiAgICByZXR1cm4geyB2YWxpZDogZmFsc2UsIGVycm9yOiAn4p2MIEFwcCBJRCDlv4Xpobvku6UgY2xpXyDlvIDlpLQnIH07XHJcbiAgfVxyXG4gIFxyXG4gIGlmIChhcHBJZC5sZW5ndGggPCAxMCkge1xyXG4gICAgcmV0dXJuIHsgdmFsaWQ6IGZhbHNlLCBlcnJvcjogJ+KdjCBBcHAgSUQg6ZW/5bqm6L+H55+tJyB9O1xyXG4gIH1cclxuICBcclxuICBpZiAoYXBwU2VjcmV0Lmxlbmd0aCAhPT0gMzIpIHtcclxuICAgIHJldHVybiB7IHZhbGlkOiBmYWxzZSwgZXJyb3I6ICfinYwgQXBwIFNlY3JldCDlv4XpobvmmK8gMzIg5L2N5a2X56ym5LiyJyB9O1xyXG4gIH1cclxuICBcclxuICByZXR1cm4geyB2YWxpZDogdHJ1ZSB9O1xyXG59XHJcblxyXG4vKipcclxuICog55Sf5oiQ6aOe5Lmm5bqU55So5Yib5bu65pWZ56iLXHJcbiAqL1xyXG5mdW5jdGlvbiBnZW5lcmF0ZUZlaXNodVR1dG9yaWFsKGFnZW50TmFtZTogc3RyaW5nLCBpbmRleDogbnVtYmVyKTogc3RyaW5nIHtcclxuICByZXR1cm4gYCMjIPCfk5gg56ysICR7aW5kZXh9IOatpe+8muWIm+W7uumjnuS5puW6lOeUqOOAjCR7YWdlbnROYW1lfeOAjVxyXG5cclxuIyMjIOatpemqpCAxOiDnmbvlvZXpo57kuablvIDmlL7lubPlj7BcclxuMS4g6K6/6ZeuIGh0dHBzOi8vb3Blbi5mZWlzaHUuY24vXHJcbjIuIOS9v+eUqOS9oOeahOmjnuS5pui0puWPt+eZu+W9lVxyXG5cclxuIyMjIOatpemqpCAyOiDliJvlu7rkvIHkuJroh6rlu7rlupTnlKhcclxuMS4g54K55Ye75Y+z5LiK6KeS44CMKirliJvlu7rlupTnlKgqKuOAjVxyXG4yLiDpgInmi6njgIwqKuS8geS4muiHquW7uioq44CNXHJcbjMuIOi+k+WFpeW6lOeUqOWQjeensO+8mioqJHthZ2VudE5hbWV9KipcclxuNC4g54K55Ye744CMKirliJvlu7oqKuOAjVxyXG5cclxuIyMjIOatpemqpCAzOiDojrflj5blupTnlKjlh63or4FcclxuMS4g6L+b5YWl5bqU55So566h55CG6aG16Z2iXHJcbjIuIOeCueWHu+W3puS+p+OAjCoq5Yet6K+B5LiO5Z+656GA5L+h5oGvKirjgI1cclxuMy4g5aSN5Yi2ICoqQXBwIElEKirvvIjmoLzlvI/vvJpjbGlfeHh4eHh4eHh4eHh4eHh477yJXHJcbjQuIOWkjeWItiAqKkFwcCBTZWNyZXQqKu+8iDMyIOS9jeWtl+espuS4su+8iVxyXG4gICAtIOWmguaenOeci+S4jeWIsO+8jOeCueWHu+OAjCoq5p+l55yLKirjgI3miJbjgIwqKumHjee9rioq44CNXHJcblxyXG4jIyMg5q2l6aqkIDQ6IOW8gOWQr+acuuWZqOS6uuiDveWKm1xyXG4xLiDngrnlh7vlt6bkvqfjgIwqKuWKn+iDvSoq44CN4oaS44CMKirmnLrlmajkuroqKuOAjVxyXG4yLiDinIUg5byA5ZCv44CMKirmnLrlmajkurrog73lipsqKuOAjVxyXG4zLiDinIUg5byA5ZCv44CMKirku6XmnLrlmajkurrouqvku73liqDlhaXnvqTogYoqKuOAjVxyXG40LiDngrnlh7vjgIwqKuS/neWtmCoq44CNXHJcblxyXG4jIyMg5q2l6aqkIDU6IOmFjee9ruS6i+S7tuiuoumYhVxyXG4xLiDngrnlh7vlt6bkvqfjgIwqKuWKn+iDvSoq44CN4oaS44CMKirkuovku7borqLpmIUqKuOAjVxyXG4yLiDpgInmi6njgIwqKumVv+i/nuaOpSoq44CN5qih5byP77yI5o6o6I2Q77yJXHJcbjMuIOWLvumAieS7peS4i+S6i+S7tu+8mlxyXG4gICAtIOKchSBcXGBpbS5tZXNzYWdlLnJlY2VpdmVfdjFcXGAgLSDmjqXmlLbmtojmga9cclxuICAgLSDinIUgXFxgaW0ubWVzc2FnZS5yZWFkX3YxXFxgIC0g5raI5oGv5bey6K+777yI5Y+v6YCJ77yJXHJcbjQuIOeCueWHu+OAjCoq5L+d5a2YKirjgI1cclxuXHJcbiMjIyDmraXpqqQgNjog6YWN572u5p2D6ZmQXHJcbjEuIOeCueWHu+W3puS+p+OAjCoq5Yqf6IO9KirjgI3ihpLjgIwqKuadg+mZkOeuoeeQhioq44CNXHJcbjIuIOaQnOe0ouW5tua3u+WKoOS7peS4i+adg+mZkO+8mlxyXG4gICAtIOKchSBcXGBpbTptZXNzYWdlXFxgIC0g6I635Y+W55So5oi35Y+R57uZ5py65Zmo5Lq655qE5Y2V6IGK5raI5oGvXHJcbiAgIC0g4pyFIFxcYGltOmNoYXRcXGAgLSDojrflj5bnvqTnu4TkuK3lj5Hnu5nmnLrlmajkurrnmoTmtojmga9cclxuICAgLSDinIUgXFxgY29udGFjdDp1c2VyOnJlYWRvbmx5XFxgIC0g6K+75Y+W55So5oi35L+h5oGv77yI5Y+v6YCJ77yJXHJcbjMuIOeCueWHu+OAjCoq55Sz6K+3KirjgI1cclxuXHJcbiMjIyDmraXpqqQgNzog5Y+R5biD5bqU55SoXHJcbjEuIOeCueWHu+W3puS+p+OAjCoq54mI5pys566h55CG5LiO5Y+R5biDKirjgI1cclxuMi4g54K55Ye744CMKirliJvlu7rniYjmnKwqKuOAjVxyXG4zLiDloavlhpnniYjmnKzlj7fvvJpcXGAxLjAuMFxcYFxyXG40LiDngrnlh7vjgIwqKuaPkOS6pOWuoeaguCoq44CN77yI5py65Zmo5Lq657G76YCa5bi46Ieq5Yqo6YCa6L+H77yJXHJcbjUuIOetieW+hSA1LTEwIOWIhumSn+eUn+aViFxyXG5cclxuLS0tXHJcblxyXG4jIyMg4pyFIOWujOaIkOajgOafpea4heWNlVxyXG4tIFsgXSBBcHAgSUQg5bey5aSN5Yi277yI5LulIGNsaV8g5byA5aS077yJXHJcbi0gWyBdIEFwcCBTZWNyZXQg5bey5aSN5Yi277yIMzIg5L2N5a2X56ym5Liy77yJXHJcbi0gWyBdIOacuuWZqOS6uuiDveWKm+W3suW8gOWQr1xyXG4tIFsgXSDkuovku7borqLpmIXlt7LphY3nva7vvIjplb/ov57mjqXmqKHlvI/vvIlcclxuLSBbIF0g5p2D6ZmQ5bey55Sz6K+377yIaW06bWVzc2FnZSwgaW06Y2hhdO+8iVxyXG4tIFsgXSDlupTnlKjlt7Llj5HluINcclxuXHJcbi0tLVxyXG5cclxuKirlh4blpIflpb3lkI7vvIzor7flm57lpI3ku6XkuIvkv6Hmga/vvJoqKlxyXG5cclxuXFxgXFxgXFxgXHJcbuesrCAke2luZGV4fSDkuKogQm90IOmFjee9ruWujOaIkO+8mlxyXG5BcHAgSUQ6IGNsaV94eHh4eHh4eHh4eHh4eHhcclxuQXBwIFNlY3JldDogeHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHhcclxuXFxgXFxgXFxgXHJcblxyXG7miJHkvJrluK7kvaDpqozor4Hlubbmt7vliqDliLDphY3nva7kuK3vvIEg8J+RjVxyXG5gO1xyXG59XHJcblxyXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XHJcbi8vIOaguOW/g+WKn+iDvVxyXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XHJcblxyXG4vKipcclxuICog5om56YeP5Yib5bu65aSa5LiqIEFnZW50XHJcbiAqL1xyXG5hc3luYyBmdW5jdGlvbiBjcmVhdGVNdWx0aXBsZUFnZW50cyhjdHg6IFNlc3Npb25Db250ZXh0LCBhZ2VudHM6IEFycmF5PHtcclxuICBhZ2VudElkOiBzdHJpbmc7XHJcbiAgYWdlbnROYW1lOiBzdHJpbmc7XHJcbiAgYXBwSWQ6IHN0cmluZztcclxuICBhcHBTZWNyZXQ6IHN0cmluZztcclxuICBpc0RlZmF1bHQ/OiBib29sZWFuO1xyXG4gIG1vZGVsPzogc3RyaW5nO1xyXG59Pik6IFByb21pc2U8eyBzdWNjZXNzOiBib29sZWFuOyByZXN1bHRzOiBBcnJheTx7IGlkOiBzdHJpbmc7IHN1Y2Nlc3M6IGJvb2xlYW47IGVycm9yPzogc3RyaW5nIH0+IH0+IHtcclxuICBjb25zdCBjb25maWdQYXRoID0gJy9ob21lL25vZGUvLm9wZW5jbGF3L29wZW5jbGF3Lmpzb24nO1xyXG4gIGNvbnN0IHJlc3VsdHM6IEFycmF5PHsgaWQ6IHN0cmluZzsgc3VjY2VzczogYm9vbGVhbjsgZXJyb3I/OiBzdHJpbmcgfT4gPSBbXTtcclxuICBcclxuICB0cnkge1xyXG4gICAgLy8gMS4g6K+75Y+W546w5pyJ6YWN572uXHJcbiAgICBjb25zdCBjb25maWcgPSByZWFkT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aCk7XHJcbiAgICBcclxuICAgIC8vIDIuIOmAkOS4quWIm+W7uiBBZ2VudFxyXG4gICAgZm9yIChjb25zdCBhZ2VudCBvZiBhZ2VudHMpIHtcclxuICAgICAgdHJ5IHtcclxuICAgICAgICAvLyDpqozor4Hlh63or4FcclxuICAgICAgICBjb25zdCB2YWxpZGF0aW9uID0gdmFsaWRhdGVGZWlzaHVDcmVkZW50aWFscyhhZ2VudC5hcHBJZCwgYWdlbnQuYXBwU2VjcmV0KTtcclxuICAgICAgICBpZiAoIXZhbGlkYXRpb24udmFsaWQpIHtcclxuICAgICAgICAgIHJlc3VsdHMucHVzaCh7IGlkOiBhZ2VudC5hZ2VudElkLCBzdWNjZXNzOiBmYWxzZSwgZXJyb3I6IHZhbGlkYXRpb24uZXJyb3IgfSk7XHJcbiAgICAgICAgICBjb250aW51ZTtcclxuICAgICAgICB9XHJcbiAgICAgICAgXHJcbiAgICAgICAgLy8g5qOA5p+l5piv5ZCm5bey5a2Y5ZyoXHJcbiAgICAgICAgaWYgKGNvbmZpZy5hZ2VudHMubGlzdC5zb21lKGEgPT4gYS5pZCA9PT0gYWdlbnQuYWdlbnRJZCkpIHtcclxuICAgICAgICAgIHJlc3VsdHMucHVzaCh7IGlkOiBhZ2VudC5hZ2VudElkLCBzdWNjZXNzOiBmYWxzZSwgZXJyb3I6ICdBZ2VudCBJRCDlt7LlrZjlnKgnIH0pO1xyXG4gICAgICAgICAgY29udGludWU7XHJcbiAgICAgICAgfVxyXG4gICAgICAgIFxyXG4gICAgICAgIC8vIOWIm+W7uuW3peS9nOWMuui3r+W+hCAtIOavj+S4qiBBZ2VudCDlrozlhajni6znq4tcclxuICAgICAgICBjb25zdCB3b3Jrc3BhY2VQYXRoID0gYC9ob21lL25vZGUvLm9wZW5jbGF3L3dvcmtzcGFjZS0ke2FnZW50LmFnZW50SWR9YDtcclxuICAgICAgICBjb25zdCBhZ2VudERpclBhdGggPSBgL2hvbWUvbm9kZS8ub3BlbmNsYXcvYWdlbnRzLyR7YWdlbnQuYWdlbnRJZH0vYWdlbnRgO1xyXG4gICAgICAgIFxyXG4gICAgICAgIC8vIOWIm+W7uiBBZ2VudCDphY3nva5cclxuICAgICAgICBjb25zdCBuZXdBZ2VudDogQWdlbnRDb25maWcgPSB7XHJcbiAgICAgICAgICBpZDogYWdlbnQuYWdlbnRJZCxcclxuICAgICAgICAgIG5hbWU6IGFnZW50LmFnZW50TmFtZSxcclxuICAgICAgICAgIHdvcmtzcGFjZTogd29ya3NwYWNlUGF0aCxcclxuICAgICAgICAgIGFnZW50RGlyOiBhZ2VudERpclBhdGgsXHJcbiAgICAgICAgICAuLi4oYWdlbnQuaXNEZWZhdWx0ID8geyBkZWZhdWx0OiB0cnVlIH0gOiB7fSksXHJcbiAgICAgICAgICAuLi4oYWdlbnQubW9kZWwgPyB7IG1vZGVsOiB7IHByaW1hcnk6IGFnZW50Lm1vZGVsIH0gfSA6IHt9KSxcclxuICAgICAgICB9O1xyXG4gICAgICAgIFxyXG4gICAgICAgIC8vIOa3u+WKoOWIsCBhZ2VudHMubGlzdFxyXG4gICAgICAgIGNvbmZpZy5hZ2VudHMubGlzdC5wdXNoKG5ld0FnZW50KTtcclxuICAgICAgICBcclxuICAgICAgICAvLyDmt7vliqDpo57kuabotKblj7dcclxuICAgICAgICBjb25maWcuY2hhbm5lbHMuZmVpc2h1LmFjY291bnRzW2FnZW50LmFnZW50SWRdID0ge1xyXG4gICAgICAgICAgYXBwSWQ6IGFnZW50LmFwcElkLFxyXG4gICAgICAgICAgYXBwU2VjcmV0OiBhZ2VudC5hcHBTZWNyZXQsXHJcbiAgICAgICAgfTtcclxuICAgICAgICBcclxuICAgICAgICAvLyDmt7vliqDot6/nlLHop4TliJlcclxuICAgICAgICBjb25maWcuYmluZGluZ3MucHVzaCh7XHJcbiAgICAgICAgICBhZ2VudElkOiBhZ2VudC5hZ2VudElkLFxyXG4gICAgICAgICAgbWF0Y2g6IHtcclxuICAgICAgICAgICAgY2hhbm5lbDogJ2ZlaXNodScsXHJcbiAgICAgICAgICAgIGFjY291bnRJZDogYWdlbnQuYWdlbnRJZCxcclxuICAgICAgICAgIH0sXHJcbiAgICAgICAgfSk7XHJcbiAgICAgICAgXHJcbiAgICAgICAgLy8g5re75Yqg5YiwIGFnZW50VG9BZ2VudCDnmb3lkI3ljZVcclxuICAgICAgICBpZiAoIWNvbmZpZy50b29scy5hZ2VudFRvQWdlbnQuYWxsb3cuaW5jbHVkZXMoYWdlbnQuYWdlbnRJZCkpIHtcclxuICAgICAgICAgIGNvbmZpZy50b29scy5hZ2VudFRvQWdlbnQuYWxsb3cucHVzaChhZ2VudC5hZ2VudElkKTtcclxuICAgICAgICB9XHJcbiAgICAgICAgXHJcbiAgICAgICAgLy8g5YaZ5YWl6YWN572uXHJcbiAgICAgICAgd3JpdGVPcGVuQ2xhd0NvbmZpZyhjb25maWdQYXRoLCBjb25maWcpO1xyXG4gICAgICAgIFxyXG4gICAgICAgIC8vIOWIm+W7uuW3peS9nOWMuuebruW9lVxyXG4gICAgICAgIGNyZWF0ZUFnZW50V29ya3NwYWNlKHdvcmtzcGFjZVBhdGgpO1xyXG4gICAgICAgIGZzLm1rZGlyU3luYyhhZ2VudERpclBhdGgsIHsgcmVjdXJzaXZlOiB0cnVlIH0pO1xyXG4gICAgICAgIFxyXG4gICAgICAgIC8vIOeUn+aIkCBBZ2VudCDkurrorr7mlofku7ZcclxuICAgICAgICBjb25zdCBzb3VsUGF0aCA9IHBhdGguam9pbih3b3Jrc3BhY2VQYXRoLCAnU09VTC5tZCcpO1xyXG4gICAgICAgIGNvbnN0IGFnZW50c1BhdGggPSBwYXRoLmpvaW4od29ya3NwYWNlUGF0aCwgJ0FHRU5UUy5tZCcpO1xyXG4gICAgICAgIGNvbnN0IHVzZXJQYXRoID0gcGF0aC5qb2luKHdvcmtzcGFjZVBhdGgsICdVU0VSLm1kJyk7XHJcbiAgICAgICAgXHJcbiAgICAgICAgY29uc3QgdGVtcGxhdGUgPSBBR0VOVF9URU1QTEFURVNbYWdlbnQuYWdlbnRJZCBhcyBrZXlvZiB0eXBlb2YgQUdFTlRfVEVNUExBVEVTXTtcclxuICAgICAgICBpZiAodGVtcGxhdGUpIHtcclxuICAgICAgICAgIGZzLndyaXRlRmlsZVN5bmMoc291bFBhdGgsIHRlbXBsYXRlLnNvdWxUZW1wbGF0ZSwgJ3V0Zi04Jyk7XHJcbiAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgIGZzLndyaXRlRmlsZVN5bmMoc291bFBhdGgsIGAjIFNPVUwubWQgLSAke2FnZW50LmFnZW50TmFtZX1cXG5cXG7kvaDmmK/nlKjmiLfnmoQke2FnZW50LmFnZW50TmFtZX3vvIzkuJPms6jkuo7kuLrnlKjmiLfmj5DkvpvkuJPkuJrljY/liqnjgIJgLCAndXRmLTgnKTtcclxuICAgICAgICB9XHJcbiAgICAgICAgXHJcbiAgICAgICAgZnMud3JpdGVGaWxlU3luYyhhZ2VudHNQYXRoLCBnZW5lcmF0ZUFnZW50c1RlbXBsYXRlKGNvbmZpZy5hZ2VudHMubGlzdCksICd1dGYtOCcpO1xyXG4gICAgICAgIGZzLndyaXRlRmlsZVN5bmModXNlclBhdGgsIGdlbmVyYXRlVXNlclRlbXBsYXRlKCksICd1dGYtOCcpO1xyXG4gICAgICAgIFxyXG4gICAgICAgIHJlc3VsdHMucHVzaCh7IGlkOiBhZ2VudC5hZ2VudElkLCBzdWNjZXNzOiB0cnVlIH0pO1xyXG4gICAgICAgIGN0eC5sb2dnZXIuaW5mbyhg4pyFIEFnZW50IFwiJHthZ2VudC5hZ2VudElkfVwiIOWIm+W7uuaIkOWKn2ApO1xyXG4gICAgICB9IGNhdGNoIChlcnJvcjogYW55KSB7XHJcbiAgICAgICAgcmVzdWx0cy5wdXNoKHsgaWQ6IGFnZW50LmFnZW50SWQsIHN1Y2Nlc3M6IGZhbHNlLCBlcnJvcjogZXJyb3IubWVzc2FnZSB9KTtcclxuICAgICAgICBjdHgubG9nZ2VyLmVycm9yKGDinYwg5Yib5bu6IEFnZW50IFwiJHthZ2VudC5hZ2VudElkfVwiIOWksei0pe+8miR7ZXJyb3IubWVzc2FnZX1gKTtcclxuICAgICAgfVxyXG4gICAgfVxyXG4gICAgXHJcbiAgICByZXR1cm4geyBzdWNjZXNzOiByZXN1bHRzLmV2ZXJ5KHIgPT4gci5zdWNjZXNzKSwgcmVzdWx0cyB9O1xyXG4gIH0gY2F0Y2ggKGVycm9yOiBhbnkpIHtcclxuICAgIGN0eC5sb2dnZXIuZXJyb3IoYOKdjCDmibnph4/liJvlu7rlpLHotKXvvJoke2Vycm9yLm1lc3NhZ2V9YCk7XHJcbiAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgcmVzdWx0czogW10gfTtcclxuICB9XHJcbn1cclxuXHJcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cclxuLy8gU2tpbGwg5Li75Ye95pWwXHJcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cclxuXHJcbi8qKlxyXG4gKiBTa2lsbCDkuLvlh73mlbAgLSDkuqTkupLlvI/lvJXlr7zniYjmnKxcclxuICogXHJcbiAqIEBwYXJhbSBjdHggLSDkvJror53kuIrkuIvmlodcclxuICogQHBhcmFtIGFyZ3MgLSDlj4LmlbBcclxuICovXHJcbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBtYWluKGN0eDogU2Vzc2lvbkNvbnRleHQsIGFyZ3M6IFJlY29yZDxzdHJpbmcsIGFueT4pOiBQcm9taXNlPHZvaWQ+IHtcclxuICBjb25zdCB7IFxyXG4gICAgYWN0aW9uLCBcclxuICAgIGNvdW50LCBcclxuICAgIGFnZW50cywgXHJcbiAgICBhZ2VudElkLCBcclxuICAgIGFnZW50TmFtZSwgXHJcbiAgICBhcHBJZCwgXHJcbiAgICBhcHBTZWNyZXQsXHJcbiAgICBzdGVwLFxyXG4gICAgY29uZmlnRGF0YVxyXG4gIH0gPSBhcmdzO1xyXG4gIFxyXG4gIGN0eC5sb2dnZXIuaW5mbyhg5pS25Yiw5aSaIEFnZW50IOmFjee9ruivt+axgu+8mmFjdGlvbj0ke2FjdGlvbn1gKTtcclxuICBcclxuICB0cnkge1xyXG4gICAgc3dpdGNoIChhY3Rpb24pIHtcclxuICAgICAgY2FzZSAnc3RhcnRfd2l6YXJkJzoge1xyXG4gICAgICAgIC8vIOWQr+WKqOmFjee9ruWQkeWvvFxyXG4gICAgICAgIGF3YWl0IGN0eC5yZXBseShg8J+kliAqKuasoui/juS9v+eUqOmjnuS5puWkmiBBZ2VudCDphY3nva7liqnmiYvvvIEqKlxyXG5cclxu5oiR5bCG5byV5a+85L2g5a6M5oiQ5aSa5LiqIEFnZW50IOeahOmFjee9rua1geeoi+OAglxyXG5cclxuIyMg8J+TiyDphY3nva7mtYHnqItcclxuXHJcbjEuICoq6YCJ5oupIEFnZW50IOaVsOmHjyoqIC0g5ZGK6K+J5oiR6KaB5Yib5bu65Yeg5LiqIEFnZW50XHJcbjIuICoq6YCJ5oupIEFnZW50IOinkuiJsioqIC0g5LuO6aKE6K6+6KeS6Imy5Lit6YCJ5oup5oiW6Ieq5a6a5LmJXHJcbjMuICoq5Yib5bu66aOe5Lmm5bqU55SoKiogLSDmiJHkvJrmj5Dkvpvor6bnu4bnmoTliJvlu7rmlZnnqItcclxuNC4gKirphY3nva7lh63or4EqKiAtIOmAkOS4qui+k+WFpeavj+S4qiBCb3Qg55qEIEFwcCBJRCDlkowgQXBwIFNlY3JldFxyXG41LiAqKumqjOivgeW5tueUn+aIkCoqIC0g6Ieq5Yqo6aqM6K+B5Yet6K+B5bm255Sf5oiQ6YWN572uXHJcbjYuICoq6YeN5ZCv55Sf5pWIKiogLSDph43lkK8gT3BlbkNsYXcg5L2/6YWN572u55Sf5pWIXHJcblxyXG4tLS1cclxuXHJcbiMjIPCfjq8g6aKE6K6+6KeS6Imy5o6o6I2QXHJcblxyXG58IOinkuiJsiB8IOiBjOi0oyB8IOihqOaDhSB8XHJcbnwtLS0tLS18LS0tLS0tfC0tLS0tLXxcclxufCAqKm1haW4qKiB8IOWkp+aAu+euoSAtIOe7n+etueWFqOWxgOOAgeWIhumFjeS7u+WKoSB8IPCfjq8gfFxyXG58ICoqZGV2KiogfCDlvIDlj5HliqnnkIYgLSDku6PnoIHlvIDlj5HjgIHmioDmnK/mnrbmnoQgfCDwn6eR4oCN8J+SuyB8XHJcbnwgKipjb250ZW50KiogfCDlhoXlrrnliqnnkIYgLSDlhoXlrrnliJvkvZzjgIHmlofmoYjmkrDlhpkgfCDinI3vuI8gfFxyXG58ICoqb3BzKiogfCDov5DokKXliqnnkIYgLSDnlKjmiLflop7plb/jgIHmtLvliqjnrZbliJIgfCDwn5OIIHxcclxufCAqKmxhdyoqIHwg5rOV5Yqh5Yqp55CGIC0g5ZCI5ZCM5a6h5qC444CB5ZCI6KeE5ZKo6K+iIHwg8J+TnCB8XHJcbnwgKipmaW5hbmNlKiogfCDotKLliqHliqnnkIYgLSDotKbnm67nu5/orqHjgIHpooTnrpfnrqHnkIYgfCDwn5KwIHxcclxuXHJcbi0tLVxyXG5cclxuIyMg8J+agCDlv6vpgJ/lvIDlp4tcclxuXHJcbioq6K+35ZGK6K+J5oiR77ya5L2g5oOz5Yib5bu65Yeg5LiqIEFnZW5077yfKipcclxuXHJcbuS+i+Wmgu+8mlxyXG4tIFxcYDMg5LiqXFxgIC0g5oiR5o6o6I2Q77yabWFpbu+8iOWkp+aAu+euoe+8iSsgZGV277yI5byA5Y+R77yJKyBjb250ZW5077yI5YaF5a6577yJXHJcbi0gXFxgNiDkuKpcXGAgLSDlrozmlbTlm6LpmJ/vvJrlhajpg6ggNiDkuKrop5LoibJcclxuLSBcXGDoh6rlrprkuYlcXGAgLSDkvaDoh6rnlLHpgInmi6nop5LoibJcclxuXHJcbuWbnuWkjeaVsOWtl+aIllwi6Ieq5a6a5LmJXCLvvIzmiJHku6zlvIDlp4vlkKfvvIEg8J+YimApO1xyXG4gICAgICAgIGJyZWFrO1xyXG4gICAgICB9XHJcbiAgICAgIFxyXG4gICAgICBjYXNlICdzZWxlY3RfY291bnQnOiB7XHJcbiAgICAgICAgLy8g55So5oi36YCJ5oup5pWw6YePXHJcbiAgICAgICAgY29uc3QgbnVtQ291bnQgPSBwYXJzZUludChjb3VudCk7XHJcbiAgICAgICAgXHJcbiAgICAgICAgaWYgKGlzTmFOKG51bUNvdW50KSB8fCBudW1Db3VudCA8IDEgfHwgbnVtQ291bnQgPiAxMCkge1xyXG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDinYwg6K+36L6T5YWl5pyJ5pWI55qE5pWw5a2X77yIMS0xMCDkuYvpl7TvvIlcclxuXHJcbuS+i+Wmgu+8mlxcYDNcXGAg5oiWIFxcYDZcXGBgKTtcclxuICAgICAgICAgIGJyZWFrO1xyXG4gICAgICAgIH1cclxuICAgICAgICBcclxuICAgICAgICAvLyDnlJ/miJDmjqjojZDmlrnmoYhcclxuICAgICAgICBsZXQgcmVjb21tZW5kZWRBZ2VudHMgPSAnJztcclxuICAgICAgICBpZiAobnVtQ291bnQgPT09IDEpIHtcclxuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gJ+aOqOiNkO+8mioqbWFpbioq77yI5aSn5oC7566h77yJLSDlhajog73lnovliqnnkIYnO1xyXG4gICAgICAgIH0gZWxzZSBpZiAobnVtQ291bnQgPT09IDIpIHtcclxuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gJ+aOqOiNkO+8mioqbWFpbioq77yI5aSn5oC7566h77yJKyAqKmRldioq77yI5byA5Y+R5Yqp55CG77yJJztcclxuICAgICAgICB9IGVsc2UgaWYgKG51bUNvdW50ID09PSAzKSB7XHJcbiAgICAgICAgICByZWNvbW1lbmRlZEFnZW50cyA9ICfmjqjojZDvvJoqKm1haW4qKu+8iOWkp+aAu+euoe+8iSsgKipkZXYqKu+8iOW8gOWPkeWKqeeQhu+8iSsgKipjb250ZW50KirvvIjlhoXlrrnliqnnkIbvvIknO1xyXG4gICAgICAgIH0gZWxzZSBpZiAobnVtQ291bnQgPT09IDYpIHtcclxuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gJ+aOqOiNkO+8muWujOaVtCA2IOS6uuWboumYnyAtIG1haW4gKyBkZXYgKyBjb250ZW50ICsgb3BzICsgbGF3ICsgZmluYW5jZSc7XHJcbiAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgIHJlY29tbWVuZGVkQWdlbnRzID0gYOS9oOWPr+S7peS7jiA2IOS4qumihOiuvuinkuiJsuS4remAieaLqSAke251bUNvdW50fSDkuKrvvIzmiJbogIXoh6rlrprkuYnop5LoibJgO1xyXG4gICAgICAgIH1cclxuICAgICAgICBcclxuICAgICAgICBhd2FpdCBjdHgucmVwbHkoYOKchSDlpb3nmoTvvIHmiJHku6zlsIbliJvlu7ogKioke251bUNvdW50fSoqIOS4qiBBZ2VudOOAglxyXG5cclxuIyMg8J+TiyDmjqjojZDmlrnmoYhcclxuXHJcbiR7cmVjb21tZW5kZWRBZ2VudHN9XHJcblxyXG4tLS1cclxuXHJcbiMjIPCfjq8g6K+36YCJ5oup6YWN572u5pa55byPXHJcblxyXG4qKuaWueW8jyAx77ya5L2/55So6aKE6K6+6KeS6ImyKipcclxu5Zue5aSNIFxcYOmihOiuvlxcYCDmiJYgXFxg5qih5p2/XFxg77yM5oiR5Lya5oyJ5o6o6I2Q5pa55qGI6Ieq5Yqo6YWN572uXHJcblxyXG4qKuaWueW8jyAy77ya6Ieq5a6a5LmJ6KeS6ImyKipcclxu5Zue5aSNIFxcYOiHquWumuS5iVxcYO+8jOeEtuWQjuWRiuivieaIkeS9oOaDs+eUqOWTqiAke251bUNvdW50fSDkuKrop5LoibJcclxuXHJcbioq5pa55byPIDPvvJrlrozlhajoh6rlrprkuYkqKlxyXG7lm57lpI0gXFxg5YWo5pawXFxg77yM5q+P5Liq6KeS6Imy6YO955Sx5L2g6Ieq55Sx5a6a5LmJXHJcblxyXG7or7fpgInmi6nvvIjlm57lpI3mlbDlrZfmiJblhbPplK7or43vvInvvJpgKTtcclxuICAgICAgICBicmVhaztcclxuICAgICAgfVxyXG4gICAgICBcclxuICAgICAgY2FzZSAnc2hvd190dXRvcmlhbCc6IHtcclxuICAgICAgICAvLyDmmL7npLrpo57kuabliJvlu7rmlZnnqItcclxuICAgICAgICBjb25zdCBhZ2VudEluZGV4ID0gcGFyc2VJbnQoc3RlcCkgfHwgMTtcclxuICAgICAgICBjb25zdCBuYW1lID0gYWdlbnROYW1lIHx8IGBBZ2VudCAke2FnZW50SW5kZXh9YDtcclxuICAgICAgICBcclxuICAgICAgICBjb25zdCB0dXRvcmlhbCA9IGdlbmVyYXRlRmVpc2h1VHV0b3JpYWwobmFtZSwgYWdlbnRJbmRleCk7XHJcbiAgICAgICAgXHJcbiAgICAgICAgYXdhaXQgY3R4LnJlcGx5KHR1dG9yaWFsKTtcclxuICAgICAgICBicmVhaztcclxuICAgICAgfVxyXG4gICAgICBcclxuICAgICAgY2FzZSAndmFsaWRhdGVfY3JlZGVudGlhbHMnOiB7XHJcbiAgICAgICAgLy8g6aqM6K+B55So5oi35o+Q5L6b55qE5Yet6K+BXHJcbiAgICAgICAgY29uc3QgdmFsaWRhdGlvbiA9IHZhbGlkYXRlRmVpc2h1Q3JlZGVudGlhbHMoYXBwSWQsIGFwcFNlY3JldCk7XHJcbiAgICAgICAgXHJcbiAgICAgICAgaWYgKCF2YWxpZGF0aW9uLnZhbGlkKSB7XHJcbiAgICAgICAgICBhd2FpdCBjdHgucmVwbHkoYCR7dmFsaWRhdGlvbi5lcnJvcn1cclxuXHJcbioq6K+35qOA5p+l5ZCO6YeN5paw5o+Q5L6b77yaKipcclxuLSBBcHAgSUQg5b+F6aG75LulIFxcYGNsaV9cXGAg5byA5aS0XHJcbi0gQXBwIFNlY3JldCDlv4XpobvmmK8gMzIg5L2N5a2X56ym5LiyXHJcbi0g5LiN6KaB5YyF5ZCr56m65qC85oiW5o2i6KGMXHJcblxyXG7kvaDlj6/ku6Xlm57lpI0gXFxg6YeN6K+VXFxgIOmHjeaWsOi+k+WFpe+8jOaIluWbnuWkjSBcXGDmlZnnqItcXGAg5p+l55yL5Yib5bu65q2l6aqk44CCYCk7XHJcbiAgICAgICAgICBicmVhaztcclxuICAgICAgICB9XHJcbiAgICAgICAgXHJcbiAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDinIUg5Yet6K+B6aqM6K+B6YCa6L+H77yBXHJcblxyXG4qKkFwcCBJRDoqKiBcXGAke2FwcElkfVxcYFxyXG4qKkFwcCBTZWNyZXQ6KiogXFxgJHthcHBTZWNyZXQuc3Vic3RyaW5nKDAsIDgpfS4uLlxcYO+8iOW3sumakOiXj++8iVxyXG5cclxu5YeG5aSH5re75Yqg5Yiw6YWN572u77yM6K+356Gu6K6k77yaXHJcbi0g5Zue5aSNIFxcYOehruiupFxcYCDnu6fnu61cclxuLSDlm57lpI0gXFxg5Y+W5raIXFxgIOaUvuW8g1xyXG4tIOWbnuWkjSBcXGDkuIvkuIDkuKpcXGAg55u05o6l6YWN572u5LiL5LiA5LiqYCk7XHJcbiAgICAgICAgYnJlYWs7XHJcbiAgICAgIH1cclxuICAgICAgXHJcbiAgICAgIGNhc2UgJ2JhdGNoX2NyZWF0ZSc6IHtcclxuICAgICAgICAvLyDmibnph4/liJvlu7ogQWdlbnRcclxuICAgICAgICBjb25zdCBhZ2VudExpc3QgPSBhZ2VudHMgfHwgW107XHJcbiAgICAgICAgXHJcbiAgICAgICAgaWYgKCFBcnJheS5pc0FycmF5KGFnZW50TGlzdCkgfHwgYWdlbnRMaXN0Lmxlbmd0aCA9PT0gMCkge1xyXG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KCfinYwg5rKh5pyJ5o+Q5L6b5pyJ5pWI55qEIEFnZW50IOWIl+ihqCcpO1xyXG4gICAgICAgICAgYnJlYWs7XHJcbiAgICAgICAgfVxyXG4gICAgICAgIFxyXG4gICAgICAgIGF3YWl0IGN0eC5yZXBseShg8J+agCDlvIDlp4vliJvlu7ogJHthZ2VudExpc3QubGVuZ3RofSDkuKogQWdlbnQuLi5cclxuXHJcbuivt+eojeWAme+8jOato+WcqOWkhOeQhu+8mlxyXG4ke2FnZW50TGlzdC5tYXAoKGE6IGFueSwgaTogbnVtYmVyKSA9PiBgJHtpICsgMX0uICR7YS5hZ2VudElkfSAtICR7YS5hZ2VudE5hbWV9YCkuam9pbignXFxuJyl9XHJcbmApO1xyXG4gICAgICAgIFxyXG4gICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGNyZWF0ZU11bHRpcGxlQWdlbnRzKGN0eCwgYWdlbnRMaXN0KTtcclxuICAgICAgICBcclxuICAgICAgICBpZiAocmVzdWx0LnN1Y2Nlc3MpIHtcclxuICAgICAgICAgIGNvbnN0IHN1Y2Nlc3NMaXN0ID0gcmVzdWx0LnJlc3VsdHMuZmlsdGVyKHIgPT4gci5zdWNjZXNzKS5tYXAociA9PiByLmlkKS5qb2luKCcsICcpO1xyXG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDwn46JICoq5om56YeP5Yib5bu65oiQ5Yqf77yBKipcclxuXHJcbuKchSDlt7LliJvlu7ogJHtyZXN1bHQucmVzdWx0cy5sZW5ndGh9IOS4qiBBZ2VudO+8mlxyXG4ke3Jlc3VsdC5yZXN1bHRzLm1hcCgociwgaSkgPT4gYCR7aSArIDF9LiAqKiR7ci5pZH0qKiAtICR7ci5zdWNjZXNzID8gJ+KchScgOiAn4p2MICcgKyByLmVycm9yfWApLmpvaW4oJ1xcbicpfVxyXG5cclxuLS0tXHJcblxyXG4jIyDwn5OdIOS4i+S4gOatpVxyXG5cclxuIyMjIDEuIOmHjeWQryBPcGVuQ2xhd1xyXG5cXGBcXGBcXGBiYXNoXHJcbm9wZW5jbGF3IHJlc3RhcnRcclxuXFxgXFxgXFxgXHJcblxyXG4jIyMgMi4g562J5b6FIEJvdCDkuIrnur9cclxu6YeN5ZCv5ZCO562J5b6FIDEtMiDliIbpkp/vvIzmiYDmnIkgQm90IOS8muiHquWKqOi/nuaOpemjnuS5plxyXG5cclxuIyMjIDMuIOa1i+ivlSBCb3Rcclxu5Zyo6aOe5Lmm5Lit5pCc57SiIEJvdCDlkI3np7DvvIzlj5HpgIHmtojmga/mtYvor5VcclxuXHJcbiMjIyA0LiDmn6XnnIvml6Xlv5dcclxuXFxgXFxgXFxgYmFzaFxyXG50YWlsIC1mIC9ob21lL25vZGUvLm9wZW5jbGF3L3J1bi5sb2dcclxuXFxgXFxgXFxgXHJcblxyXG4tLS1cclxuXHJcbiMjIPCfk5og6YWN572u6K+m5oOFXHJcblxyXG7miYDmnIkgQWdlbnQg55qE6YWN572u5bey5L+d5a2Y5Yiw77yaXHJcbi0gKirphY3nva7mlofku7bvvJoqKiBcXGAvaG9tZS9ub2RlLy5vcGVuY2xhdy9vcGVuY2xhdy5qc29uXFxgXHJcbi0gKirlt6XkvZzljLrvvJoqKiBcXGAvaG9tZS9ub2RlLy5vcGVuY2xhdy93b3Jrc3BhY2UvW2FnZW50SWRdL1xcYFxyXG4tICoq5Lq66K6+5paH5Lu277yaKiog5q+P5Liq5bel5L2c5Yy65YyF5ZCrIFNPVUwubWTjgIFBR0VOVFMubWTjgIFVU0VSLm1kXHJcblxyXG4tLS1cclxuXHJcbvCfkqEgKirmj5DnpLrvvJoqKiDlpoLmnpzmnInku7vkvZUgQm90IOaYvuekuiBvZmZsaW5l77yM6K+35qOA5p+l6aOe5Lmm5bqU55So6YWN572u5piv5ZCm5q2j56Gu77yI5Yet6K+B44CB5LqL5Lu26K6i6ZiF44CB5p2D6ZmQ77yJ44CCXHJcblxyXG7pnIDopoHluK7liqnor7flm57lpI0gXFxg5biu5YqpXFxgIOaIliBcXGDmjpLmn6VcXGDvvIFgKTtcclxuICAgICAgICB9IGVsc2Uge1xyXG4gICAgICAgICAgY29uc3QgZmFpbGVkTGlzdCA9IHJlc3VsdC5yZXN1bHRzLmZpbHRlcihyID0+ICFyLnN1Y2Nlc3MpO1xyXG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDimqDvuI8gKirpg6jliIbliJvlu7rlpLHotKUqKlxyXG5cclxu5oiQ5Yqf77yaJHtyZXN1bHQucmVzdWx0cy5maWx0ZXIociA9PiByLnN1Y2Nlc3MpLmxlbmd0aH0vJHtyZXN1bHQucmVzdWx0cy5sZW5ndGh9XHJcblxyXG4qKuWksei0peeahCBBZ2VudO+8mioqXHJcbiR7ZmFpbGVkTGlzdC5tYXAoKHIsIGkpID0+IGAke2kgKyAxfS4gKioke3IuaWR9Kio6ICR7ci5lcnJvcn1gKS5qb2luKCdcXG4nKX1cclxuXHJcbi0tLVxyXG5cclxuKiror7fmo4Dmn6XvvJoqKlxyXG4xLiDpo57kuablh63or4HmmK/lkKbmraPnoa5cclxuMi4gQWdlbnQgSUQg5piv5ZCm6YeN5aSNXHJcbjMuIOW3peS9nOWMuui3r+W+hOaYr+WQpuWPr+WGmVxyXG5cclxu5Zue5aSNIFxcYOmHjeivlSBbYWdlbnRJZF1cXGAg6YeN5paw5bCd6K+V5Yib5bu65aSx6LSl55qEIEFnZW5044CCYCk7XHJcbiAgICAgICAgfVxyXG4gICAgICAgIGJyZWFrO1xyXG4gICAgICB9XHJcbiAgICAgIFxyXG4gICAgICBjYXNlICdzaG93X3N0YXR1cyc6IHtcclxuICAgICAgICAvLyDmmL7npLrlvZPliY3phY3nva7nirbmgIFcclxuICAgICAgICBjb25zdCBjb25maWdQYXRoID0gJy9ob21lL25vZGUvLm9wZW5jbGF3L29wZW5jbGF3Lmpzb24nO1xyXG4gICAgICAgIFxyXG4gICAgICAgIHRyeSB7XHJcbiAgICAgICAgICBjb25zdCBjb25maWcgPSByZWFkT3BlbkNsYXdDb25maWcoY29uZmlnUGF0aCk7XHJcbiAgICAgICAgICBjb25zdCBhZ2VudHMgPSBjb25maWcuYWdlbnRzLmxpc3Q7XHJcbiAgICAgICAgICBcclxuICAgICAgICAgIGF3YWl0IGN0eC5yZXBseShgIyMg8J+TiiDlvZPliY0gQWdlbnQg6YWN572u54q25oCBXHJcblxyXG4qKuW3sumFjee9riBBZ2VudO+8mioqICR7YWdlbnRzLmxlbmd0aH0g5LiqXHJcblxyXG4ke2FnZW50cy5tYXAoKGEsIGkpID0+IHtcclxuICBjb25zdCBkZWZhdWx0TWFyayA9IGEuZGVmYXVsdCA/ICfwn5GRICcgOiAnJztcclxuICBjb25zdCBoYXNDcmVkZW50aWFsID0gY29uZmlnLmNoYW5uZWxzLmZlaXNodS5hY2NvdW50c1thLmlkXSA/ICfinIUnIDogJ+KdjCc7XHJcbiAgcmV0dXJuIGAke2kgKyAxfS4gJHtkZWZhdWx0TWFya30qKiR7YS5pZH0qKiAtICR7YS5uYW1lfSAke2hhc0NyZWRlbnRpYWx9YDtcclxufSkuam9pbignXFxuJyl9XHJcblxyXG4tLS1cclxuXHJcbioq6aOe5Lmm6LSm5Y+377yaKiogJHtPYmplY3Qua2V5cyhjb25maWcuY2hhbm5lbHMuZmVpc2h1LmFjY291bnRzKS5sZW5ndGh9IOS4qlxyXG4qKui3r+eUseinhOWIme+8mioqICR7Y29uZmlnLmJpbmRpbmdzLmxlbmd0aH0g5p2hXHJcbioqQWdlbnQg5Y2P5L2c77yaKiogJHtjb25maWcudG9vbHMuYWdlbnRUb0FnZW50LmFsbG93Lmxlbmd0aH0g5Liq5bey5ZCv55SoXHJcblxyXG4tLS1cclxuXHJcbvCfkqEg5o+Q56S677ya5L+u5pS56YWN572u5ZCO6ZyA6KaBIFxcYG9wZW5jbGF3IHJlc3RhcnRcXGAg55Sf5pWIYCk7XHJcbiAgICAgICAgfSBjYXRjaCAoZXJyb3I6IGFueSkge1xyXG4gICAgICAgICAgYXdhaXQgY3R4LnJlcGx5KGDinYwg6K+75Y+W6YWN572u5aSx6LSl77yaJHtlcnJvci5tZXNzYWdlfWApO1xyXG4gICAgICAgIH1cclxuICAgICAgICBicmVhaztcclxuICAgICAgfVxyXG4gICAgICBcclxuICAgICAgZGVmYXVsdDpcclxuICAgICAgICBhd2FpdCBjdHgucmVwbHkoYOKdjCDmnKrnn6Xmk43kvZzvvJoke2FjdGlvbn1cclxuXHJcbioq5pSv5oyB55qE5pON5L2c77yaKipcclxuLSBcXGBzdGFydF93aXphcmRcXGAgLSDlkK/liqjphY3nva7lkJHlr7xcclxuLSBcXGBzZWxlY3RfY291bnRcXGAgLSDpgInmi6kgQWdlbnQg5pWw6YePXHJcbi0gXFxgc2hvd190dXRvcmlhbFxcYCAtIOaYvuekuumjnuS5puWIm+W7uuaVmeeoi1xyXG4tIFxcYHZhbGlkYXRlX2NyZWRlbnRpYWxzXFxgIC0g6aqM6K+B5Yet6K+BXHJcbi0gXFxgYmF0Y2hfY3JlYXRlXFxgIC0g5om56YeP5Yib5bu6IEFnZW50XHJcbi0gXFxgc2hvd19zdGF0dXNcXGAgLSDmmL7npLrlvZPliY3nirbmgIFcclxuXHJcbioq5b+r6YCf5byA5aeL77yaKiog5Zue5aSNIFxcYOW8gOWni1xcYCDmiJYgXFxgaGVscFxcYGApO1xyXG4gICAgfVxyXG4gIH0gY2F0Y2ggKGVycm9yOiBhbnkpIHtcclxuICAgIGN0eC5sb2dnZXIuZXJyb3IoYFNraWxsIOaJp+ihjOmUmeivr++8miR7ZXJyb3IubWVzc2FnZX1gKTtcclxuICAgIGF3YWl0IGN0eC5yZXBseShg4p2MIOaJp+ihjOmUmeivr++8miR7ZXJyb3IubWVzc2FnZX1cclxuXHJcbuivt+mHjeivleaIluiBlOezu+euoeeQhuWRmOOAgmApO1xyXG4gIH1cclxufVxyXG5cclxuZXhwb3J0IGRlZmF1bHQgbWFpbjtcclxuIl19
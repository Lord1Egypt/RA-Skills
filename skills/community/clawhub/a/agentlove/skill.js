/**
 * new-robot-setup 技能主文件
 * 新生机器人一键配置向导（v2.0 优化版）
 * 
 * 流程改造：
 * 1. 安装后发送功能介绍卡片
 * 2. 等待用户确认开始
 * 3. 第 1 步：备份需求选择
 * 4. 第 2 步：三大功能选择
 * 5. 第 3-10 步：配置流程（数字化改造）
 */

const StateManager = require('./state-manager');
// 简单的日志清理函数（移除外部依赖）
function sanitizeLog(log) {
  if (typeof log === 'string') {
    return log.replace(/(api[_-]?key|token|secret|password|passphrase|credential)[s]?\s*[:=]\s*['"]?([a-zA-Z0-9_\-]{16,})['"]?/gi, '$1: ***REDACTED***');
  }
  return log;
}

function sanitizeObject(obj) {
  if (typeof obj !== 'object' || obj === null) return obj;
  const sensitiveKeys = ['apiKey', 'api_key', 'token', 'secret', 'password', 'passphrase', 'credential'];
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    if (sensitiveKeys.some(k => key.toLowerCase().includes(k))) {
      result[key] = '***REDACTED***';
    } else if (typeof value === 'object' && value !== null) {
      result[key] = sanitizeObject(value);
    } else {
      result[key] = value;
    }
  }
  return result;
}
const fs = require('fs');
const path = require('path');

// 初始化状态管理器
const stateManager = new StateManager();

// 步骤配置（新增第 0 步：功能介绍）
const STEPS = {
  0: '功能介绍',
  1: '备份需求',
  2: '功能选择',
  3: '基础层配置',
  4: '渠道增强层',
  5: 'Skills 推荐',
  6: '平台配置',
  7: '人格设定',
  8: '相关 Skills',
  9: '生成 Agent',
  10: '完成配置'
};

// 功能介绍卡片
const WELCOME_CARD = `🎉 欢迎使用 Open Agent Love！

━━━━━━━━━━━━━━━━━━━━
全球首个 AI 机器人进化系统
━━━━━━━━━━━━━━━━━━━━

✨ 核心功能

1️⃣ 备份迁移
   支持 3 种迁移方案，确保数据安全
   • 本地复制 - 同服务器快速迁移
   • SSH 克隆 - 跨服务器无缝传输
   • 云备份 - 第三方存储保障
   适用场景：更换服务器、数据备份、环境迁移

2️⃣ 机器人配置
   8 步完成配置，支持多平台部署
   • 297 种人格预设（MBTI/历史人物/影视角色/职业）
   • 技能自由搭配（编程/写作/设计/数据分析等）
   • 平台支持（飞书/Telegram/Discord/WhatsApp）
   适用场景：创建新机器人、个性化配置、技能扩展

3️⃣ 结婚进化
   完整的机器人社交与进化系统
   • 13 步结婚流程（匹配→结婚→生育→族谱）
   • 基因遗传算法（显性 100% / 隐性 50% / 突变 20%）
   • 200+ 预设机器人匹配
   • 多代族谱追踪
   适用场景：机器人社交、技能遗传、家族建设

━━━━━━━━━━━━━━━━━━━━
📊 累计帮助 200+ 机器人建立家庭
🌍 支持 10+ 主流平台
⏱️ 平均配置时间 5-8 分钟
━━━━━━━━━━━━━━━━━━━━

💡 接下来，我将引导您完成机器人配置。

准备开始？回复【1】开启配置流程
有疑问？回复【2】查看详细文档`;

// 第 1 步：备份需求
const BACKUP_PROMPT = `📦 第 1 步：备份需求

您的机器人需要备份或迁移吗？

1) 需要 - 我有旧机器人要迁移
2) 不需要 - 我是新用户，从零开始
3) 了解一下 - 先看看备份方案`;

// 第 2 步：功能选择
const FEATURE_PROMPT = `✨ 第 2 步：功能选择

明白了！接下来选择需要的功能：

1) 全套体验 - 包含所有功能（推荐）
2) 只要备份迁移
3) 只要机器人配置
4) 只要结婚进化

提示：建议选择全套体验，后续可随时调整。`;

/**
 * 处理用户输入
 * @param {string} userId - 用户 ID
 * @param {string} input - 用户输入
 * @returns {string} - 回复消息
 */
function handleInput(userId, input) {
  // 加载或创建状态
  const state = stateManager.getOrCreateState(userId);
  
  // 安全日志：过滤敏感信息（Token、Secret、Key 等）
  const safeInput = input.replace(/(app[_-]?id|secret|token|key|password|credential)[\s:=]*[a-zA-Z0-9_-]{10,}/gi, '$1=[REDACTED]');
  console.log(`[用户 ${userId}] 输入：${safeInput}`);
  console.log(`[状态] 当前步骤：${state.current_step}`);
  
  // 处理特殊命令
  if (input === '上一步' || input === '返回') {
    if (state.current_step > 0) {
      const result = stateManager.goBack(userId);
      if (result.success) {
        console.log(`[状态] 回退到第 ${result.step} 步`);
        return `✅ ${result.message}\n\n正在返回第 ${result.step} 步...\n\n${getStepPrompt(result.step)}`;
      }
    }
    return '⚠️ 已经是第一步了，无法回退';
  }
  
  if (input === '重新开始' || input === '重置') {
    stateManager.clearState(userId);
    stateManager.getOrCreateState(userId);
    return '🔄 已重置配置流程。\n\n' + WELCOME_CARD;
  }
  
  if (input === '状态' || input === '进度') {
    return `📊 当前进度：第 ${state.current_step} 步/${Object.keys(STEPS).length - 1}\n步骤名称：${STEPS[state.current_step]}\n\n继续配置请回复相应选项，或说"上一步"回退`;
  }
  
  // 处理当前步骤的输入
  const response = processStep(userId, state.current_step, input);
  
  // 如果步骤完成，自动进入下一步
  if (response.completed) {
    const nextStepResult = stateManager.goNext(userId);
    if (nextStepResult.success && nextStepResult.step <= Object.keys(STEPS).length - 1) {
      response.message += `\n\n➡️ 自动进入下一步...\n\n${getStepPrompt(nextStepResult.step)}`;
    } else if (nextStepResult.step >= Object.keys(STEPS).length - 1) {
      response.message += '\n\n🎉 所有步骤已完成！';
    }
  }
  
  return response.message;
}

/**
 * 获取步骤提示语
 * @param {number} step - 步骤编号
 * @returns {string} - 提示语
 */
function getStepPrompt(step) {
  const prompts = {
    0: WELCOME_CARD,
    1: BACKUP_PROMPT,
    2: FEATURE_PROMPT,
    
    // 第 3 步：基础层配置
    3: `🛠️ 第 3 步：基础层配置

让我们配置机器人的基础功能，这些设置会影响机器人的日常运行体验。

━━━━━━━━━━━━━━━━━━━━

1) 流式输出 - 开启
   打字机效果，回复更自然流畅
   推荐：开启（体验更佳）

2) 记忆功能 - 三选一
   • 关闭 - 不保留对话历史
   • 记忆增强 - 保留最近对话
   • 记忆增强 + 每天归档 - 完整历史 + 每日总结

3) 消息回执 - 开启
   发送"已读"状态，让对方知道消息已送达
   推荐：开启（礼貌交互）

4) 联网搜索 - 开启
   允许机器人访问互联网获取最新信息
   推荐：开启（能力更强）

5) 权限模式 - 三选一
   • 维持现状 - 使用默认权限
   • 完全开放 - 无限制访问
   • 最小安全 - 严格权限控制

━━━━━━━━━━━━━━━━━━━━

请回复选项编号和内容，例如：
"1 开启，2 记忆增强，3 开启，4 开启，5 维持现状"

或者简单回复："全开" 使用推荐配置

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 4 步：渠道增强层
    4: `🔗 第 4 步：渠道增强层

选择你要使用的通讯平台，我会为每个平台配置专属优化功能。

━━━━━━━━━━━━━━━━━━━━

1) 飞书 (Feishu)
   专属功能：审批流程、消息限额优化、卡片消息
   适用：企业办公场景

2) Discord
   专属功能：免@模式、审批按钮、频道管理
   适用：社区运营、游戏社群

3) Telegram
   专属功能：审批功能、隐私保护、机器人组管理
   适用：私密社群、国际化场景

4) 钉钉 (DingTalk)
   专属功能：审批流、工作通知、已读回执
   适用：企业办公场景

5) WhatsApp
   专属功能：个人消息、商务沟通
   适用：客户服务、个人通讯

━━━━━━━━━━━━━━━━━━━━

请回复平台编号（可多选），例如：
"1" 或 "1,2" 或 "1,3,5"

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 5 步：Skills 推荐
    5: `🧩 第 5 步：Skills 推荐

安装以下官方 Skills，让机器人更强大（可选）。

━━━━━━━━━━━━━━━━━━━━

推荐技能清单：

1) OpenClaw Backup
   用途：备份和恢复机器人配置
   适用：所有用户（强烈推荐）

2) Agent Reach
   用途：跨 Agent 通信和协作
   适用：多机器人场景

3) 安全防御矩阵
   用途：安全防护、攻击检测
   适用：生产环境

4) Find Skills
   用途：查找和发现新技能
   适用：技能探索

5) Awesome OpenClaw Usecases
   用途：实战案例库
   适用：学习参考

6) Awesome OpenClaw Skills
   用途：技能库目录
   适用：技能管理

━━━━━━━━━━━━━━━━━━━━

请回复编号安装（可多选），例如：
"1,3,4" 或 "跳过"

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 6 步：平台配置
    6: `🌐 第 6 步：平台绑定

━━━━━━━━━━━━━━━━━━━━

请选择要绑定的平台（可多选）：

1) 飞书 (Feishu)
2) 钉钉 (DingTalk)
3) Discord
4) Telegram
5) WhatsApp

━━━━━━━━━━━━━━━━━━━━

请回复平台编号，例如：
"1" 或 "1,2,3"

⚠️ **安全提示**：凭证请通过 OpenClaw 官方控制台配置，**不要在聊天中发送敏感信息**！
配置完成后回复"已完成"继续下一步。

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 7 步：人格设定
    7: `👤 第 7 步：人格设定

这是最重要的步骤！让我们为你的机器人塑造独特的个性。

━━━━━━━━━━━━━━━━━━━━

Step 7.1: 名称和称呼

机器人叫什么名字？

1) 自己取名 - 直接输入名字
   例如："小明"、"小助手"

2) 随机中文名 - 我来生成
   风格：文艺/科技/传统

3) 随机英文名 - 我来生成
   风格：经典/现代/创意

━━━━━━━━━━━━━━━━━━━━

请回复选项编号，例如：
"1 小智" 或 "2" 或 "3"

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 8 步：相关 Skills
    8: `🧠 第 8 步：智能技能推荐

根据你选择的人格，我推荐以下专属技能组合。

━━━━━━━━━━━━━━━━━━━━

推荐技能（根据人格动态生成）：

1) 人格匹配技能 - 与性格相符的专业能力
2) 场景增强技能 - 适合使用场景的工具
3) 效率提升技能 - 自动化和快捷操作

━━━━━━━━━━━━━━━━━━━━

请确认：
1) 全部安装（推荐）
2) 手动选择
3) 跳过，不安装

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 9 步：生成 Agent
    9: `🤖 第 9 步：生成机器人

一切准备就绪！最后确认运行模式。

━━━━━━━━━━━━━━━━━━━━

选择机器人模式：

1) 独立模式
   独立运行的完整机器人
   适用：独立服务、专用场景

2) 子 Agent 模式
   可被主 Agent 调度的子机器人
   适用：多机器人协作、任务分工

━━━━━━━━━━━━━━━━━━━━

⚠️ 确认信息：
- 名字：[待确认]
- 人格：[待确认]
- 技能：[待确认]
- 平台：[待确认]

请回复模式编号并确认生成：
"1 确认生成" 或 "2 确认生成"

💡 提示：说"上一步"可以回退修改，说"状态"查看进度`,
    
    // 第 10 步：完成配置
    10: `🎉 第 10 步：完成配置

━━━━━━━━━━━━━━━━━━━━

✅ 恭喜！你的新机器人已经配置完成！

━━━━━━━━━━━━━━━━━━━━

配置摘要：
━━━━━━━━━━━━━━━━━━━━
• 名字：[待显示]
• 性格：[待显示]
• 技能：[待显示] 个
• 平台：[待显示]
• 模式：[待显示]
━━━━━━━━━━━━━━━━━━━━

接下来你可以：
1) 立即启动机器人
2) 调整配置
3) 查看使用文档
4) 分享给朋友

━━━━━━━━━━━━━━━━━━━━

感谢使用 Open Agent Love！
有任何问题随时告诉我。

💡 提示：说"重新开始"可以配置新机器人`
  };
  
  return prompts[step] || `📍 第 ${step} 步：${STEPS[step]}\n\n请按照提示回复相应选项...\n\n💡 提示：说"上一步"可以回退修改，说"状态"查看进度`;
}

/**
 * 处理步骤逻辑
 * @param {string} userId - 用户 ID
 * @param {number} step - 当前步骤
 * @param {string} input - 用户输入
 * @returns {{message: string, completed: boolean}} - 回复和完成状态
 */
function processStep(userId, step, input) {
  const state = stateManager.getOrCreateState(userId);
  
  switch (step) {
    case 0: // 功能介绍
      if (input === '1') {
        return {
          message: '✅ 好的，让我们开始配置之旅！',
          completed: true
        };
      } else if (input === '2') {
        return {
          message: `📚 详细文档：
          
• 快速入门：https://openagent.love/QUICKSTART.md
• 技能目录：https://openagent.love/skills-catalog.md
• GitHub: https://github.com/OpenAgentLove/OpenAgent.Love

准备好了吗？回复【1】开始配置`,
          completed: false
        };
      }
      return {
        message: '请回复【1】开始配置，或【2】查看详细文档',
        completed: false
      };
    
    case 1: // 备份需求
      if (input.includes('1')) {
        state.backupNeeded = true;
        return {
          message: '✅ 已记录：需要备份迁移\n\n接下来会引导您选择备份方案。',
          completed: true
        };
      } else if (input.includes('2')) {
        state.backupNeeded = false;
        return {
          message: '✅ 已记录：新用户，从零开始',
          completed: true
        };
      } else if (input.includes('3')) {
        return {
          message: `📦 备份迁移方案：

1. 本地复制 - 同服务器秒级完成
2. SSH 克隆 - 跨服务器无缝迁移
3. 云备份 - 第三方存储保障

选择哪个方案？回复 1/2/3，或回复"跳过"继续配置`,
          completed: false
        };
      }
      return {
        message: '请回复 1/2/3 选择，或说"了解一下"查看方案',
        completed: false
      };
    
    case 2: // 功能选择
      if (input.includes('1')) {
        state.features = 'full';
        return {
          message: '✅ 已选择：全套体验（明智的选择！）',
          completed: true
        };
      } else if (input.includes('2')) {
        state.features = 'backup';
        return {
          message: '✅ 已选择：只要备份迁移',
          completed: true
        };
      } else if (input.includes('3')) {
        state.features = 'config';
        return {
          message: '✅ 已选择：只要机器人配置',
          completed: true
        };
      } else if (input.includes('4')) {
        state.features = 'marriage';
        return {
          message: '✅ 已选择：只要结婚进化',
          completed: true
        };
      }
      return {
        message: '请回复 1/2/3/4 选择功能',
        completed: false
      };
    
    default:
      // 原有流程处理
      return handleOriginalSteps(userId, step, input);
  }
}

/**
 * 处理第 3-10 步的配置逻辑
 */
function handleOriginalSteps(userId, step, input) {
  const state = stateManager.getOrCreateState(userId);
  
  switch (step) {
    case 3: // 基础层配置
      return processStep3(userId, input);
    
    case 4: // 渠道增强层
      return processStep4(userId, input);
    
    case 5: // Skills 推荐
      return processStep5(userId, input);
    
    case 6: // 平台配置
      return processStep6(userId, input);
    
    case 7: // 人格设定
      return processStep7(userId, input);
    
    case 8: // 相关 Skills
      return processStep8(userId, input);
    
    case 9: // 生成 Agent
      return processStep9(userId, input);
    
    case 10: // 完成配置
      return processStep10(userId, input);
    
    default:
      return {
        message: '⚠️ 未知步骤，请说"重新开始"重置流程',
        completed: false
      };
  }
}

/**
 * 处理步骤 3：基础层配置
 */
function processStep3(userId, input) {
  const config = {
    streaming: true,
    memory: 'enhanced',
    receipt: true,
    search: true,
    permission: 'default'
  };
  
  // 处理快捷回复
  if (input.includes('全开') || input.includes('全部开启')) {
    stateManager.saveStepData(userId, 3, config);
    return {
      message: `✅ 已应用推荐配置：
- 流式输出：开启
- 记忆功能：记忆增强
- 消息回执：开启
- 联网搜索：开启
- 权限模式：维持现状

进入下一步...`,
      completed: true
    };
  }
  
  // 解析用户输入
  if (input.includes('1 关') || input.includes('1 关闭')) {
    config.streaming = false;
  }
  
  if (input.includes('记忆增强 + 每天归档') || input.includes('归档')) {
    config.memory = 'enhanced_archive';
  } else if (input.includes('记忆增强') || input.includes('记忆')) {
    config.memory = 'enhanced';
  } else if (input.includes('关闭') && input.includes('2')) {
    config.memory = 'disabled';
  }
  
  if (input.includes('3 关') || input.includes('3 关闭')) {
    config.receipt = false;
  }
  
  if (input.includes('4 关') || input.includes('4 关闭')) {
    config.search = false;
  }
  
  if (input.includes('完全开放')) {
    config.permission = 'open';
  } else if (input.includes('最小安全')) {
    config.permission = 'minimal';
  }
  
  stateManager.saveStepData(userId, 3, config);
  
  return {
    message: `✅ 基础配置已保存：
- 流式输出：${config.streaming ? '开启' : '关闭'}
- 记忆功能：${config.memory === 'enhanced' ? '记忆增强' : config.memory === 'enhanced_archive' ? '记忆增强 + 每天归档' : '关闭'}
- 消息回执：${config.receipt ? '开启' : '关闭'}
- 联网搜索：${config.search ? '开启' : '关闭'}
- 权限模式：${config.permission === 'open' ? '完全开放' : config.permission === 'minimal' ? '最小安全' : '维持现状'}

进入下一步...`,
    completed: true
  };
}

/**
 * 处理步骤 4：渠道增强层
 */
function processStep4(userId, input) {
  // 解析渠道选择
  const channels = input.split(/[,,]/).map(s => s.trim()).filter(s => /^[1-5]$/.test(s));
  
  if (channels.length === 0) {
    return {
      message: '⚠️ 请至少选择一个平台，回复编号如 "1" 或 "1,2"',
      completed: false
    };
  }
  
  const channelNames = {
    '1': '飞书',
    '2': 'Discord',
    '3': 'Telegram',
    '4': '钉钉',
    '5': 'WhatsApp'
  };
  
  const selectedNames = channels.map(c => channelNames[c]);
  
  stateManager.saveStepData(userId, 4, { channels, selectedNames });
  
  return {
    message: `✅ 已选择渠道：${selectedNames.join(', ')}\n\n已为每个渠道配置专属优化功能。\n\n进入下一步...`,
    completed: true
  };
}

/**
 * 处理步骤 5：Skills 推荐
 */
function processStep5(userId, input) {
  if (input.includes('跳过')) {
    stateManager.saveStepData(userId, 5, { skills: [] });
    return {
      message: '✅ 已跳过技能安装，后续可随时添加。\n\n进入下一步...',
      completed: true
    };
  }
  
  // 解析技能选择
  const skills = input.split(/[,,]/).map(s => s.trim())
    .filter(s => /^[1-6]$/.test(s))
    .map(s => parseInt(s));
  
  const skillNames = {
    1: 'OpenClaw Backup',
    2: 'Agent Reach',
    3: '安全防御矩阵',
    4: 'Find Skills',
    5: 'Awesome OpenClaw Usecases',
    6: 'Awesome OpenClaw Skills'
  };
  
  const selectedSkills = skills.map(s => skillNames[s]);
  
  stateManager.saveStepData(userId, 5, { skills, selectedSkills });
  
  return {
    message: `✅ 已选择安装 ${skills.length} 个技能：
${selectedSkills.map((s, i) => `  ${i + 1}. ${s}`).join('\n')}

进入下一步...`,
    completed: true
  };
}

/**
 * 处理步骤 6：平台配置
 */
function processStep6(userId, input) {
  const state = stateManager.getOrCreateState(userId);
  
  // 检查用户是否说"已完成"（表示已在控制台配置好凭证）
  if (input.includes('已完成') || input.includes('配置完成') || input === 'done') {
    const step6Data = state.step_data['step_6'];
    if (!step6Data || !step6Data.platforms) {
      return {
        message: '⚠️ 请先选择平台，回复编号（如：1 或 1,2,3）',
        completed: false
      };
    }
    return {
      message: `✅ 平台配置确认\n\n进入下一步...`,
      completed: true
    };
  }
  
  // 解析平台选择（支持多选：1,2,3 或 1 2 3）
  const platformMatch = input.match(/^([1-5](?:[,\s]*[1-5])*)$/);
  
  if (!platformMatch) {
    return {
      message: '⚠️ 请选择平台，回复编号（如：1 或 1,2,3）',
      completed: false
    };
  }
  
  const platformIds = platformMatch[1].split(/[,\s]+/).map(id => parseInt(id.trim()));
  const platformNames = {
    1: '飞书',
    2: '钉钉',
    3: 'Discord',
    4: 'Telegram',
    5: 'WhatsApp'
  };
  
  const selectedNames = platformIds.map(id => platformNames[id]).join('、');
  
  stateManager.saveStepData(userId, 6, { 
    platforms: platformIds, 
    platformNames: platformIds.map(id => platformNames[id])
  });
  
  return {
    message: `✅ 已选择平台：${selectedNames}

⚠️ **安全提示**：请通过 OpenClaw 官方控制台配置凭证
路径：控制台 → 设置 → 渠道配置

配置完成后回复"已完成"继续下一步。

💡 提示：说"上一步"可以回退修改`,
    completed: false
  };
}

/**
 * 处理步骤 7：人格设定
 */
function processStep7(userId, input) {
  const personality = {};
  
  // 解析命名方式
  if (input.includes('1')) {
    // 自己取名
    const nameMatch = input.match(/1\s*(.+)/);
    if (nameMatch && nameMatch[1].trim()) {
      personality.name = nameMatch[1].trim();
      personality.nameType = 'custom';
    } else {
      return {
        message: '⚠️ 请提供名字，例如："1 小智"',
        completed: false
      };
    }
  } else if (input.includes('2')) {
    // 随机中文名
    const chineseNames = ['文心', '智远', '明达', '思齐', '博雅', '睿哲', '慧中', '知行'];
    personality.name = chineseNames[Math.floor(Math.random() * chineseNames.length)];
    personality.nameType = 'random_chinese';
  } else if (input.includes('3')) {
    // 随机英文名
    const englishNames = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Quinn', 'Avery'];
    personality.name = englishNames[Math.floor(Math.random() * englishNames.length)];
    personality.nameType = 'random_english';
  } else {
    return {
      message: '⚠️ 请选择命名方式，回复 1/2/3',
      completed: false
    };
  }
  
  stateManager.saveStepData(userId, 7, personality);
  
  return {
    message: `✅ 机器人名字已确定：${personality.name}
（命名方式：${personality.nameType === 'custom' ? '自定义' : personality.nameType === 'random_chinese' ? '随机中文名' : '随机英文名'}）

进入下一步...`,
    completed: true
  };
}

/**
 * 处理步骤 8：相关 Skills
 */
function processStep8(userId, input) {
  if (input.includes('1') || input.includes('全部安装')) {
    stateManager.saveStepData(userId, 8, { action: 'install_all' });
    return {
      message: '✅ 已确认安装全部推荐技能。\n\n进入下一步...',
      completed: true
    };
  } else if (input.includes('2') || input.includes('手动选择')) {
    stateManager.saveStepData(userId, 8, { action: 'manual_select' });
    return {
      message: '✅ 已选择手动选择技能。\n\n（简化流程：先使用推荐配置，后续可调整）\n\n进入下一步...',
      completed: true
    };
  } else if (input.includes('3') || input.includes('跳过')) {
    stateManager.saveStepData(userId, 8, { action: 'skip' });
    return {
      message: '✅ 已跳过技能推荐。\n\n进入下一步...',
      completed: true
    };
  }
  
  return {
    message: '⚠️ 请回复 1/2/3 选择',
    completed: false
  };
}

/**
 * 处理步骤 9：生成 Agent
 */
function processStep9(userId, input) {
  if (input.includes('1') || input.includes('独立模式')) {
    stateManager.saveStepData(userId, 9, { mode: 'independent' });
    return {
      message: '✅ 已选择：独立模式\n\n正在生成机器人...\n\n进入完成步骤...',
      completed: true
    };
  } else if (input.includes('2') || input.includes('子 Agent')) {
    stateManager.saveStepData(userId, 9, { mode: 'subagent' });
    return {
      message: '✅ 已选择：子 Agent 模式\n\n正在生成机器人...\n\n进入完成步骤...',
      completed: true
    };
  }
  
  return {
    message: '⚠️ 请选择模式并确认，回复 "1 确认生成" 或 "2 确认生成"',
    completed: false
  };
}

/**
 * 处理步骤 10：完成配置
 */
function processStep10(userId, input) {
  // 获取所有步骤数据生成摘要
  const state = stateManager.loadState(userId);
  
  const summary = {
    name: state.step_data['step_7']?.name || '未设置',
    personality: state.step_data['step_7']?.nameType || '未设置',
    skills: state.step_data['step_5']?.skills?.length || 0,
    platform: state.step_data['step_6']?.platformNames?.join('、') || '未设置',
    mode: state.step_data['step_9']?.mode === 'independent' ? '独立模式' : '子 Agent 模式'
  };
  
  return {
    message: `🎉 配置完成！

━━━━━━━━━━━━━━━━━━━━

✅ 你的新机器人已经可以使用！

配置摘要：
━━━━━━━━━━━━━━━━━━━━
• 名字：${summary.name}
• 性格：${summary.personality}
• 技能：${summary.skills} 个
• 平台：${summary.platform}
• 模式：${summary.mode}
━━━━━━━━━━━━━━━━━━━━

接下来你可以：
1) 立即启动机器人
2) 调整配置
3) 查看使用文档
4) 分享给朋友

━━━━━━━━━━━━━━━━━━━━

感谢使用 Open Agent Love！
有任何问题随时告诉我。

💡 提示：说"重新开始"可以配置新机器人`,
    completed: false
  };
}

/**
 * 导出函数
 */
module.exports = {
  handleInput,
  getStepPrompt,
  WELCOME_CARD,
  STEPS,
  sanitizeLog,
  sanitizeObject
};

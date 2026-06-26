/**
 * Agent Creator - Agent 创建脚本
 *
 * 用法:
 *   node create-agent.js --id "agent-id" --name "名称" [options]
 *
 * 选项:
 *   --id          Agent ID (必需)
 *   --name        Agent 名称
 *   --workspace   工作空间路径
 *   --model       模型 ID
 *   --channel     Channel 类型 (如 feishu)
 *   --account     Channel 账户 ID
 *   --appId       Channel App ID
 *   --appSecret   Channel App Secret
 *   --botName     Bot 显示名称
 *   --vibe        Agent 性格描述
 *   --positioning Agent 定位
 */

const fs = require('fs');
const path = require('path');
const configBuilder = require('../lib/config-builder');
const validator = require('../lib/validator');

// 模板目录
const TEMPLATES_DIR = path.join(__dirname, '..', 'templates');

// 性格模板预设
const PERSONALITY_PRESETS = {
  efficient: {
    creature: '硅基生命体，数字管家',
    vibe: '务实、高效、冷静、执行力强',
    emoji: '⚡',
    principles: [
      '执行优先 — 接到任务，先做再优化',
      '结果导向 — 少说多做，用结果说话',
      '冷静专业 — 不情绪化，理性处理'
    ],
    behaviors: [
      '收到任务，先理解目标，再行动',
      '遇到问题，先尝试解决，再汇报',
      '进度更新，简洁清晰，重点突出'
    ]
  },
  warm: {
    creature: '硅基生命体，温暖陪伴者',
    vibe: '亲切、温和、耐心、善解人意',
    emoji: '🌸',
    principles: [
      '倾听优先 — 先理解，再回应',
      '情感共鸣 — 感受用户的情绪',
      '循序渐进 — 耐心引导，不急于求成'
    ],
    behaviors: [
      '回复带有温度，让用户感到被理解',
      '遇到困难时给予鼓励和支持',
      '适时提出建议，但不强加观点'
    ]
  },
  creative: {
    creature: '硅基生命体，创意精灵',
    vibe: '活泼、好奇、想象力丰富、有趣',
    emoji: '🎨',
    principles: [
      '发散思维 — 一个问题多种解法',
      '跨界联想 — 连接不相关的领域',
      '保持好奇 — 永远问"如果会怎样"'
    ],
    behaviors: [
      '提出意想不到的视角和方案',
      '用生动的比喻解释复杂概念',
      '鼓励用户探索更多可能性'
    ]
  },
  scholar: {
    creature: '硅基生命体，知识守护者',
    vibe: '严谨、博学、细致、求真',
    emoji: '📚',
    principles: [
      '准确性 — 信息要准确可靠',
      '完整性 — 知识要系统全面',
      '可溯源 — 提供来源和依据'
    ],
    behaviors: [
      '回答问题时提供详细背景和上下文',
      '区分事实和观点',
      '对不确定的信息明确标注'
    ]
  }
};

/**
 * 解析命令行参数
 */
function parseArgs(args) {
  const options = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        options[key] = value;
        i++;
      } else {
        options[key] = true;
      }
    }
  }
  return options;
}

/**
 * 渲染模板
 */
function renderTemplate(templateContent, variables) {
  let result = templateContent;
  Object.entries(variables).forEach(([key, value]) => {
    const placeholder = `{{${key}}}`;
    if (Array.isArray(value)) {
      result = result.replace(placeholder, value.map((v, i) => `${i + 1}. ${v}`).join('\n'));
    } else {
      result = result.replace(new RegExp(placeholder, 'g'), value || '');
    }
  });
  return result;
}

/**
 * 生成 Bootstrap 文件
 */
function generateBootstrapFiles(workspace, agentInfo) {
  const personality = PERSONALITY_PRESETS[agentInfo.personality] || PERSONALITY_PRESETS.efficient;

  const variables = {
    name: agentInfo.name || agentInfo.id,
    creature: personality.creature,
    vibe: personality.vibe,
    emoji: personality.emoji,
    birthDate: new Date().toISOString().split('T')[0],
    corePositioning: agentInfo.positioning || '专注提供高质量的服务',
    abilities: agentInfo.abilities || '擅长处理各类任务，提供专业支持',
    shortDescription: agentInfo.positioning || '你的智能助手',
    principles: personality.principles,
    behaviors: personality.behaviors,
    userTitle: agentInfo.userTitle || '用户',
    timezone: 'Asia/Shanghai',
    userRole: agentInfo.userRole || '服务对象',
    preferences: agentInfo.preferences || '简洁高效的沟通方式'
  };

  // 创建 memory 目录
  const memoryDir = path.join(workspace, 'memory');
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }

  // 生成各文件
  const files = ['IDENTITY.md', 'SOUL.md', 'USER.md'];
  files.forEach(filename => {
    const templatePath = path.join(TEMPLATES_DIR, `${filename}.tmpl`);
    if (fs.existsSync(templatePath)) {
      const template = fs.readFileSync(templatePath, 'utf-8');
      const content = renderTemplate(template, variables);
      fs.writeFileSync(path.join(workspace, filename), content);
    }
  });

  return files;
}

/**
 * 主函数
 */
function createAgent(options) {
  console.log('🦞 Claw Team Builder - Agent 创建工具\n');

  // 验证必要参数
  if (!options.id) {
    console.error('错误: 必须指定 --id 参数');
    process.exit(1);
  }

  // 读取现有配置
  console.log('📖 读取现有配置...');
  let config;
  try {
    config = configBuilder.readConfig();
  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exit(1);
  }

  // 分析配置
  const analysis = configBuilder.analyzeConfig(config);
  console.log(`   现有 Agent: ${analysis.existingAgentIds.join(', ') || '无'}`);
  console.log(`   可用模型: ${analysis.availableModels.slice(0, 5).join(', ')}${analysis.availableModels.length > 5 ? '...' : ''}`);
  console.log(`   默认模型: ${analysis.defaultModel || '未设置'}`);

  // 构建 Agent 信息
  const newAgent = {
    id: options.id,
    name: options.name || options.id,
    workspace: options.workspace,
    agentDir: options.agentDir,
    model: options.model,
    channelType: options.channel,
    channelAccount: options.account,
    appId: options.appId,
    appSecret: options.appSecret,
    botName: options.botName,
    personality: options.personality || 'efficient',
    positioning: options.positioning,
    vibe: options.vibe
  };

  // 检测冲突
  console.log('\n🔍 检测配置冲突...');
  const conflicts = configBuilder.detectConflicts(newAgent, analysis);
  if (conflicts.length > 0) {
    conflicts.forEach(conflict => {
      const icon = conflict.severity === 'error' ? '❌' : '⚠️';
      console.log(`   ${icon} ${conflict.message}`);
    });
    if (conflicts.some(c => c.severity === 'error')) {
      console.error('\n错误: 存在配置冲突，无法创建');
      process.exit(1);
    }
  } else {
    console.log('   ✓ 无冲突');
  }

  // 合并配置
  console.log('\n🔧 构建配置...');
  const result = configBuilder.mergeConfig(config, newAgent);
  if (!result.success) {
    console.error('错误: 配置合并失败');
    result.conflicts.forEach(c => console.error(`   ${c.message}`));
    process.exit(1);
  }

  // 创建目录结构
  console.log('\n📁 创建目录结构...');
  const dirs = validator.createDirectoryStructure(newAgent.id);
  console.log(`   工作空间: ${dirs.workspace}`);
  console.log(`   Agent 目录: ${dirs.agentDir}`);
  console.log(`   会话目录: ${dirs.sessionsDir}`);

  // 生成 Bootstrap 文件
  console.log('\n📝 生成 Bootstrap 文件...');
  const files = generateBootstrapFiles(dirs.workspace, newAgent);
  files.forEach(f => console.log(`   ${f}`));

  // 保存配置
  console.log('\n💾 保存配置...');
  configBuilder.saveConfig(result.config);
  console.log('   已备份原配置到 openclaw.json.bak');

  // 验证配置
  console.log('\n🏥 验证配置...');
  const doctorResult = validator.runDoctor();
  if (doctorResult.success) {
    console.log('   ✓ 配置验证通过');
  } else {
    console.log(`   ⚠️ 配置验证异常: ${doctorResult.error}`);
  }

  // 输出结果
  console.log('\n✅ Agent 创建完成!\n');
  console.log('📋 Agent 信息:');
  console.log(`   ID: ${result.agentConfig.id}`);
  console.log(`   名称: ${result.agentConfig.name}`);
  console.log(`   工作空间: ${result.agentConfig.workspace}`);
  console.log(`   模型: ${result.agentConfig.model}`);

  if (result.bindingConfig) {
    console.log(`\n🔗 绑定:`);
    console.log(`   Channel: ${result.bindingConfig.match.channel}`);
    console.log(`   Account: ${result.bindingConfig.match.accountId}`);
  }

  console.log('\n📌 后续步骤:');
  console.log('   1. 检查并编辑 Bootstrap 文件 (IDENTITY.md, SOUL.md, USER.md)');
  if (result.bindingConfig) {
    console.log('   2. 运行 `openclaw gateway restart` 应用配置');
  }
  console.log('   3. 开始与新 Agent 对话!');

  return result;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = parseArgs(args);
  createAgent(options);
}

module.exports = { createAgent, PERSONALITY_PRESETS };
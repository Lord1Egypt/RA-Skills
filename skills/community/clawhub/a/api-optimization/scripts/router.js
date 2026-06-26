/**
 * Chenni Free API - 智能分流路由器
 *
 * 根据任务类型自动选择最合适的免费模型
 *
 * Usage:
 *   node router.js --task coding
 *   node router.js --task reasoning
 *   node router.js --task translation
 *   node router.js --generate-config
 *   node router.js --generate-config --mode royal
 *   node router.js --list-modes
 */

import {
  getMode,
  generateModeFullConfig,
  printModeNotice,
  printAllModes,
  PRIMARY_PLACEHOLDER,
} from './modes.js';

// 任务类型定义
const TASK_TYPES = {
  coding: {
    name: '代码生成',
    description: '代码编写、重构、调试、代码审查',
    keywords: ['code', 'coding', 'program', 'debug', 'refactor', '代码', '编程', '调试'],
    preferredCapabilities: ['coding', 'instruction-following'],
  },
  reasoning: {
    name: '逻辑推理',
    description: '数学计算、逻辑分析、问题解决',
    keywords: ['reason', 'logic', 'math', 'solve', '推理', '逻辑', '数学'],
    preferredCapabilities: ['reasoning', 'chain-of-thought'],
  },
  translation: {
    name: '翻译任务',
    description: '中英文翻译、多语言转换',
    keywords: ['translate', 'translation', '翻译', '中译英', '英译中'],
    preferredCapabilities: ['multilingual', 'translation'],
  },
  chat: {
    name: '日常对话',
    description: '闲聊、问答、信息查询',
    keywords: ['chat', 'talk', 'ask', '对话', '聊天', '问答'],
    preferredCapabilities: ['conversation', 'general'],
  },
  vision: {
    name: '图像理解',
    description: '图片分析、OCR、视觉问答',
    keywords: ['image', 'vision', 'picture', 'see', '图像', '图片', '视觉'],
    preferredCapabilities: ['vision', 'multimodal'],
  },
  writing: {
    name: '文本创作',
    description: '文章写作、内容生成、文案',
    keywords: ['write', 'writing', 'article', 'content', '写作', '文章', '文案'],
    preferredCapabilities: ['creative-writing', 'instruction-following'],
  },
  longcontext: {
    name: '长文本处理',
    description: '处理超长文档、书籍、代码库',
    keywords: ['long', 'context', 'book', 'document', '长文本', '文档', '书籍'],
    preferredCapabilities: ['long-context', '128k+'],
  },
};

// 默认模型路由配置
const DEFAULT_ROUTING = {
  coding: [
    { model: 'siliconflow/Qwen/Qwen2.5-7B-Instruct', priority: 1 },
    { model: 'siliconflow/Qwen/Qwen3-8B', priority: 2 },
    { model: 'nvidia/qwen/qwen3.5-397b-a17b', priority: 3 },
    { model: 'openrouter/qwen/qwen3.5-flash-02-23', priority: 4 },
  ],
  reasoning: [
    { model: 'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B', priority: 1 },
    { model: 'siliconflow/Qwen/Qwen3-8B', priority: 2 },
    { model: 'nvidia/z-ai/glm5', priority: 3 },
    { model: 'openrouter/google/gemini-3.1-flash-lite', priority: 4 },
  ],
  translation: [
    { model: 'siliconflow/tencent/Hunyuan-MT-7B', priority: 1 },
    { model: 'siliconflow/THUDM/GLM-4-9B-0414', priority: 2 },
    { model: 'nvidia/z-ai/glm4.7', priority: 3 },
    { model: 'openrouter/google/gemini-3.1-flash-lite', priority: 4 },
  ],
  chat: [
    { model: 'siliconflow/Qwen/Qwen3-8B', priority: 1 },
    { model: 'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B', priority: 2 },
    { model: 'nvidia/z-ai/glm5', priority: 3 },
    { model: 'openrouter/google/gemini-3.1-flash-lite', priority: 4 },
  ],
  vision: [
    { model: 'nvidia/z-ai/glm5', priority: 1 },
    { model: 'nvidia/moonshotai/kimi-k2.5', priority: 2 },
    { model: 'openrouter/google/gemini-3.1-flash-lite', priority: 3 },
  ],
  writing: [
    { model: 'siliconflow/Qwen/Qwen3-8B', priority: 1 },
    { model: 'siliconflow/THUDM/GLM-4-9B-0414', priority: 2 },
    { model: 'nvidia/z-ai/glm5', priority: 3 },
    { model: 'openrouter/google/gemini-3.1-flash-lite', priority: 4 },
  ],
  longcontext: [
    { model: 'nvidia/stepfun-ai/step-3.5-flash', priority: 1 },
    { model: 'nvidia/moonshotai/kimi-k2.5', priority: 2 },
    { model: 'nvidia/minimaxai/minimax-m2.5', priority: 3 },
    { model: 'siliconflow/deepseek-ai/DeepSeek-V3.2', priority: 4 },
  ],
};

/**
 * 根据任务类型获取推荐模型
 */
function getModelsForTask(taskType) {
  const task = TASK_TYPES[taskType];
  if (!task) {
    console.error(`❌ 未知任务类型: ${taskType}`);
    console.log(`✅ 可用任务类型: ${Object.keys(TASK_TYPES).join(', ')}`);
    return [];
  }

  const routing = DEFAULT_ROUTING[taskType] || [];
  return routing.map((r) => ({
    ...r,
    taskType,
    taskName: task.name,
  }));
}

/**
 * 根据用户输入自动识别任务类型
 */
function detectTaskType(userInput) {
  const input = userInput.toLowerCase();

  for (const [type, config] of Object.entries(TASK_TYPES)) {
    for (const keyword of config.keywords) {
      if (input.includes(keyword)) {
        return type;
      }
    }
  }

  return 'chat'; // 默认返回日常对话
}

/**
 * 生成 OpenClaw 路由配置（默认均衡模式）
 */
function generateRoutingConfig(modeId) {
  // 如果指定了模式，使用模式配置
  if (modeId) {
    const mode = getMode(modeId);
    if (!mode) return null;
    if (!mode.routing) {
      console.log(`⚠️  ${mode.emoji} ${mode.name} 不启用按任务路由，所有任务使用主模型`);
      return null;
    }
    printModeNotice(modeId);
    const config = generateModeFullConfig(modeId);
    return config;
  }

  // 默认：使用内置路由（向后兼容）
  const config = {
    agents: {
      defaults: {
        models: {
          routing: {},
        },
      },
    },
  };

  for (const [taskType, routes] of Object.entries(DEFAULT_ROUTING)) {
    config.agents.defaults.models.routing[taskType] = routes
      .sort((a, b) => a.priority - b.priority)
      .map((r) => r.model);
  }

  return config;
}

/**
 * 格式化输出推荐模型
 */
function formatRecommendations(taskType, models) {
  const task = TASK_TYPES[taskType];
  if (!task) return '';

  let output = `
📋 任务类型: ${task.name}
📝 任务描述: ${task.description}

🎯 推荐模型（按优先级排序）：
`;

  models.forEach((m, i) => {
    output += `  ${i + 1}. ${m.model} (优先级: ${m.priority})\n`;
  });

  return output;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);

  // 列出所有模式
  if (args.includes('--list-modes')) {
    printAllModes();
    return;
  }

  // 生成配置模式
  if (args.includes('--generate-config')) {
    const modeId = args.includes('--mode') ? args[args.indexOf('--mode') + 1] : null;
    const config = generateRoutingConfig(modeId);
    if (config) {
      console.log(JSON.stringify(config, null, 2));
    }
    return;
  }

  // 列出所有任务类型
  if (args.includes('--list-tasks')) {
    console.log('📋 支持的任务类型：\n');
    for (const [type, config] of Object.entries(TASK_TYPES)) {
      console.log(`  ${type}: ${config.name}`);
      console.log(`    ${config.description}`);
      console.log(`    关键词: ${config.keywords.join(', ')}`);
      console.log('');
    }
    return;
  }

  // 获取特定任务的推荐（支持 --mode）
  if (args.includes('--task')) {
    const taskType = args[args.indexOf('--task') + 1];
    const modeId = args.includes('--mode') ? args[args.indexOf('--mode') + 1] : null;

    if (modeId) {
      const mode = getMode(modeId);
      if (!mode) return;
      if (!mode.routing) {
        console.log(`${mode.emoji} ${mode.name}：所有任务使用主模型，不按任务类型路由`);
        return;
      }
      const models = mode.routing[taskType];
      if (models) {
        console.log(`${mode.emoji} ${mode.name} - ${taskType} 推荐模型：\n`);
        models.forEach((m, i) => {
          const label = m === PRIMARY_PLACEHOLDER ? `⚠️  ${m} (需替换)` : m;
          console.log(`  ${i + 1}. ${label}`);
        });
      } else {
        console.log(`❌ 模式 "${modeId}" 未定义 "${taskType}" 任务的路由`);
      }
    } else {
      const models = getModelsForTask(taskType);
      if (models.length > 0) {
        console.log(formatRecommendations(taskType, models));
      }
    }
    return;
  }

  // 自动检测任务类型
  if (args.includes('--detect')) {
    const input = args[args.indexOf('--detect') + 1];
    if (!input) {
      console.error('❌ 请提供要检测的文本');
      console.log('用法: node router.js --detect "帮我写一段代码"');
      return;
    }

    const detectedType = detectTaskType(input);
    const models = getModelsForTask(detectedType);
    console.log(`🔍 检测到任务类型: ${detectedType}`);
    console.log(formatRecommendations(detectedType, models));
    return;
  }

  // 默认：显示帮助
  console.log('🧠 智能分流路由器\n');
  console.log('根据任务类型自动选择最合适的免费模型\n');
  console.log('用法：');
  console.log('  node router.js --task coding                    # 获取代码任务推荐');
  console.log('  node router.js --task coding --mode royal       # 富豪模式推荐');
  console.log('  node router.js --detect "帮我翻译"              # 自动检测任务类型');
  console.log('  node router.js --generate-config                # 生成默认路由配置');
  console.log('  node router.js --generate-config --mode royal   # 生成富豪模式配置');
  console.log('  node router.js --generate-config --mode savings # 生成省钱模式配置');
  console.log('  node router.js --list-modes                     # 列出所有模式');
  console.log('  node router.js --list-tasks                     # 列出所有任务类型');
}

// ESM 兼容的直接执行检测
const isMain = process.argv[1]?.endsWith('router.js');
if (isMain) {
  main().catch((error) => {
    console.error('❌ 执行失败:', error.message);
    process.exit(1);
  });
}

// 导出函数供其他模块使用
export {
  TASK_TYPES,
  DEFAULT_ROUTING,
  getModelsForTask,
  detectTaskType,
  generateRoutingConfig,
};

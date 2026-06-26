/**
 * Chenni Free API - 模式定义中心
 *
 * 三种模式控制免费模型和用户主模型的优先级：
 *   royal    - 富豪模式：所有任务用主模型，免费仅作降级
 *   balanced - 均衡模式：简单任务用免费，复杂任务用主模型
 *   savings  - 极致省钱：免费优先，主模型作最后保底
 */

// 用户主模型占位符，生成配置时需替换为实际模型 ID
export const PRIMARY_PLACEHOLDER = '${您的主模型}';

// 可用免费模型池（来源：https://siliconflow.cn/pricing + NVIDIA NIM）
export const FREE_MODELS = {
  // SiliconFlow 免费
  qwen3_8b: 'siliconflow/Qwen/Qwen3-8B',
  qwen35_4b: 'siliconflow/Qwen/Qwen3.5-4B',
  qwen25_7b: 'siliconflow/Qwen/Qwen2.5-7B-Instruct',
  deepseek_r1_qwen3_8b: 'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
  deepseek_r1_distill_7b: 'siliconflow/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
  deepseek_ocr: 'siliconflow/deepseek-ai/DeepSeek-OCR',
  glm41v_thinking: 'siliconflow/THUDM/GLM-4.1V-9B-Thinking',
  glm_z1_9b: 'siliconflow/THUDM/GLM-Z1-9B-0414',
  glm4_9b: 'siliconflow/THUDM/GLM-4-9B-0414',
  hunyuan_mt_7b: 'siliconflow/tencent/Hunyuan-MT-7B',
  paddle_ocr_vl: 'siliconflow/PaddlePaddle/PaddleOCR-VL',
  internlm25_7b: 'siliconflow/internlm/internlm2_5-7b-chat',
  // NVIDIA NIM 免费
  nvidia_qwen35_397b: 'nvidia/qwen/qwen3.5-397b-a17b',
  nvidia_glm5: 'nvidia/z-ai/glm5',
  nvidia_glm47: 'nvidia/z-ai/glm4.7',
  nvidia_kimi: 'nvidia/moonshotai/kimi-k2.5',
  nvidia_step: 'nvidia/stepfun-ai/step-3.5-flash',
  nvidia_minimax: 'nvidia/minimaxai/minimax-m2.5',
  // OpenRouter 免费/超低价
  gemini_flash_lite: 'openrouter/google/gemini-3.1-flash-lite',
  qwen35_flash: 'openrouter/qwen/qwen3.5-flash-02-23',
};

// 重试策略
const DEFAULT_RETRY_POLICY = {
  maxRetries: 3,
  backoffMs: 1000,
  backoffMultiplier: 2,
  autoRecover: true,
  recoverIntervalMs: 300000,
};

// ========== 模式定义 ==========

export const MODES = {
  // ─── 富豪模式 ───────────────────────────────────────────
  royal: {
    id: 'royal',
    name: '富豪模式',
    emoji: '🤴',
    description: '所有任务使用您的主模型，免费模型仅作降级备选',
    tip: '适合已购买 Coding Plan 或付费 API 的用户',

    // 降级链：主模型挂了才用免费的
    fallbacks: [
      FREE_MODELS.nvidia_qwen35_397b,
      FREE_MODELS.qwen3_8b,
      FREE_MODELS.deepseek_r1_qwen3_8b,
      FREE_MODELS.gemini_flash_lite,
    ],

    // 路由：不启用，所有任务都走主模型
    routing: null,

    retryPolicy: DEFAULT_RETRY_POLICY,

    generateNotice() {
      return [
        `${this.emoji} ${this.name}：${this.description}`,
        `📌 您的主模型 (primary) 保持不变`,
        `🔄 免费模型已添加为降级备选（共 ${this.fallbacks.length} 个）`,
        `💡 所有任务都使用您的主模型，仅在主模型不可用时降级到免费模型`,
      ];
    },
  },

  // ─── 均衡模式 ───────────────────────────────────────────
  balanced: {
    id: 'balanced',
    name: '均衡模式',
    emoji: '⚖️',
    description: '简单任务优先免费模型，复杂任务使用您的主模型',
    tip: '大多数用户的推荐选择',

    // 降级链
    fallbacks: [
      FREE_MODELS.nvidia_qwen35_397b,
      FREE_MODELS.qwen3_8b,
      FREE_MODELS.deepseek_r1_qwen3_8b,
    ],

    // 路由：简单任务免费优先，复杂任务主模型优先
    routing: {
      // 简单任务 → 免费模型在前
      chat: [
        FREE_MODELS.qwen3_8b,
        FREE_MODELS.nvidia_glm5,
        FREE_MODELS.gemini_flash_lite,
      ],
      translation: [
        FREE_MODELS.hunyuan_mt_7b,
        FREE_MODELS.glm4_9b,
        FREE_MODELS.gemini_flash_lite,
      ],
      writing: [
        FREE_MODELS.qwen3_8b,
        FREE_MODELS.glm4_9b,
        FREE_MODELS.nvidia_glm5,
      ],
      // 复杂任务 → 主模型在前，免费兜底
      coding: [
        PRIMARY_PLACEHOLDER,
        FREE_MODELS.qwen25_7b,
        FREE_MODELS.nvidia_qwen35_397b,
      ],
      reasoning: [
        PRIMARY_PLACEHOLDER,
        FREE_MODELS.deepseek_r1_qwen3_8b,
        FREE_MODELS.nvidia_glm5,
      ],
      vision: [
        PRIMARY_PLACEHOLDER,
        FREE_MODELS.nvidia_glm5,
        FREE_MODELS.nvidia_kimi,
      ],
      longcontext: [
        PRIMARY_PLACEHOLDER,
        FREE_MODELS.nvidia_step,
        FREE_MODELS.nvidia_kimi,
      ],
    },

    retryPolicy: DEFAULT_RETRY_POLICY,

    generateNotice() {
      return [
        `${this.emoji} ${this.name}：${this.description}`,
        `📌 您的主模型 (primary) 保持不变`,
        `🆓 简单任务（对话/翻译/写作）优先使用免费模型`,
        `🔧 复杂任务（代码/推理/视觉）优先使用您的主模型`,
        `⚠️  请将配置中的 "${PRIMARY_PLACEHOLDER}" 替换为您的实际模型 ID`,
        `   例如：openclaw models status  查看当前模型`,
      ];
    },
  },

  // ─── 极致省钱模式 ───────────────────────────────────────
  savings: {
    id: 'savings',
    name: '极致省钱',
    emoji: '💰',
    description: '免费模型优先，付费模型仅作最后保底',
    tip: '适合预算敏感、想最大化免费额度的用户',

    // 主模型改为免费的
    primary: FREE_MODELS.qwen3_8b,

    // 降级链：全免费，原主模型放最后
    fallbacks: [
      FREE_MODELS.nvidia_qwen35_397b,
      FREE_MODELS.deepseek_r1_qwen3_8b,
      FREE_MODELS.nvidia_glm5,
      FREE_MODELS.gemini_flash_lite,
      // 原主模型作为最后保底
      PRIMARY_PLACEHOLDER,
    ],

    // 路由：全部免费优先
    routing: {
      chat: [
        FREE_MODELS.qwen3_8b,
        FREE_MODELS.nvidia_glm5,
        FREE_MODELS.deepseek_r1_qwen3_8b,
      ],
      coding: [
        FREE_MODELS.qwen25_7b,
        FREE_MODELS.nvidia_qwen35_397b,
        FREE_MODELS.qwen3_8b,
      ],
      reasoning: [
        FREE_MODELS.deepseek_r1_qwen3_8b,
        FREE_MODELS.nvidia_glm5,
        FREE_MODELS.qwen3_8b,
      ],
      translation: [
        FREE_MODELS.hunyuan_mt_7b,
        FREE_MODELS.glm4_9b,
        FREE_MODELS.qwen3_8b,
      ],
      writing: [
        FREE_MODELS.qwen3_8b,
        FREE_MODELS.glm4_9b,
        FREE_MODELS.nvidia_glm5,
      ],
      vision: [
        FREE_MODELS.nvidia_glm5,
        FREE_MODELS.nvidia_kimi,
        FREE_MODELS.gemini_flash_lite,
      ],
      longcontext: [
        FREE_MODELS.nvidia_step,
        FREE_MODELS.nvidia_kimi,
        FREE_MODELS.nvidia_minimax,
      ],
    },

    retryPolicy: DEFAULT_RETRY_POLICY,

    generateNotice() {
      return [
        `${this.emoji} ${this.name}：${this.description}`,
        `🆓 主模型已切换为免费模型: ${this.primary}`,
        `🔄 降级链包含 ${this.fallbacks.length - 1} 个免费模型 + 您的原主模型（最后保底）`,
        `⚠️  请将配置中的 "${PRIMARY_PLACEHOLDER}" 替换为您的原模型 ID`,
        `   这样在所有免费模型都不可用时才会使用付费模型`,
      ];
    },
  },
};

// ========== 辅助函数 ==========

/**
 * 获取模式列表
 */
export function listModes() {
  return Object.values(MODES).map((m) => ({
    id: m.id,
    name: m.name,
    emoji: m.emoji,
    description: m.description,
    tip: m.tip,
  }));
}

/**
 * 获取模式定义
 */
export function getMode(modeId) {
  const mode = MODES[modeId];
  if (!mode) {
    console.error(`❌ 未知模式: ${modeId}`);
    console.log(`✅ 可用模式: ${Object.keys(MODES).join(', ')}`);
    return null;
  }
  return mode;
}

/**
 * 根据模式生成降级配置
 */
export function generateModeFallbackConfig(modeId) {
  const mode = getMode(modeId);
  if (!mode) return null;

  const config = {
    agents: {
      defaults: {
        model: {
          fallbacks: mode.fallbacks,
          retryPolicy: mode.retryPolicy,
        },
      },
    },
  };

  // savings 模式会修改 primary
  if (mode.primary) {
    config.agents.defaults.model.primary = mode.primary;
  }

  return config;
}

/**
 * 根据模式生成完整配置（降级 + 路由）
 */
export function generateModeFullConfig(modeId) {
  const mode = getMode(modeId);
  if (!mode) return null;

  const config = {
    agents: {
      defaults: {
        model: {
          fallbacks: mode.fallbacks,
          retryPolicy: mode.retryPolicy,
        },
        models: {},
      },
    },
  };

  // savings 模式会修改 primary
  if (mode.primary) {
    config.agents.defaults.model.primary = mode.primary;
  }

  // 路由配置
  if (mode.routing) {
    config.agents.defaults.models.routing = {};
    for (const [taskType, models] of Object.entries(mode.routing)) {
      config.agents.defaults.models.routing[taskType] = models;
    }
  }

  return config;
}

/**
 * 打印模式提醒信息
 */
export function printModeNotice(modeId) {
  const mode = getMode(modeId);
  if (!mode) return;

  const lines = mode.generateNotice();
  lines.forEach((line) => console.log(line));
  console.log('');
}

/**
 * 打印所有可用模式
 */
export function printAllModes() {
  console.log('🎯 可用模式：\n');
  for (const mode of Object.values(MODES)) {
    console.log(`  ${mode.emoji} ${mode.id.padEnd(10)} ${mode.name}`);
    console.log(`     ${mode.description}`);
    console.log(`     ${mode.tip}`);
    console.log('');
  }
}

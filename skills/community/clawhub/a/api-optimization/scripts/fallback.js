/**
 * Chenni Free API - 无感降级管理器
 *
 * 主模型失败时自动切换到备用模型，并支持自动回切
 *
 * Usage:
 *   node fallback.js --test                              # 测试降级链
 *   node fallback.js --monitor                           # 监控模型状态
 *   node fallback.js --generate-config                   # 生成降级配置
 *   node fallback.js --generate-config --mode royal      # 富豪模式降级配置
 *   node fallback.js --generate-full-config              # 生成完整配置
 *   node fallback.js --generate-full-config --mode savings  # 省钱模式完整配置
 *   node fallback.js --check <model-id>                  # 检查单个模型状态
 *   node fallback.js --list-modes                        # 列出所有模式
 */

import {
  getMode,
  generateModeFallbackConfig,
  generateModeFullConfig,
  printModeNotice,
  printAllModes,
  MODES,
} from './modes.js';

// 平台 API 端点
const PLATFORM_ENDPOINTS = {
  siliconflow: {
    baseUrl: 'https://api.siliconflow.cn/v1',
    testEndpoint: '/chat/completions',
    apiKeyEnv: 'SILICONFLOW_API_KEY',
  },
  openrouter: {
    baseUrl: 'https://openrouter.ai/api/v1',
    testEndpoint: '/chat/completions',
    apiKeyEnv: 'OPENROUTER_API_KEY',
  },
  deepseek: {
    baseUrl: 'https://api.deepseek.com/v1',
    testEndpoint: '/chat/completions',
    apiKeyEnv: 'DEEPSEEK_API_KEY',
  },
  zhipu: {
    baseUrl: 'https://open.bigmodel.cn/api/paas/v4',
    testEndpoint: '/chat/completions',
    apiKeyEnv: 'ZHIPU_API_KEY',
  },
  nvidia: {
    baseUrl: 'https://integrate.api.nvidia.com/v1',
    testEndpoint: '/chat/completions',
    apiKeyEnv: 'NVIDIA_API_KEY',
  },
};

// 默认降级链配置
const DEFAULT_FALLBACK_CHAINS = {
  primary: [
    'siliconflow/Qwen/Qwen3-8B',
    'nvidia/qwen/qwen3.5-397b-a17b',
    'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
    'openrouter/google/gemini-3.1-flash-lite',
  ],
  coding: [
    'siliconflow/Qwen/Qwen2.5-7B-Instruct',
    'nvidia/qwen/qwen3.5-397b-a17b',
    'siliconflow/Qwen/Qwen3-8B',
    'openrouter/qwen/qwen3.5-flash-02-23',
  ],
  reasoning: [
    'siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
    'nvidia/z-ai/glm5',
    'siliconflow/Qwen/Qwen3-8B',
    'openrouter/google/gemini-3.1-flash-lite',
  ],
  vision: [
    'nvidia/z-ai/glm5',
    'nvidia/moonshotai/kimi-k2.5',
    'openrouter/google/gemini-3.1-flash-lite',
  ],
  longcontext: [
    'nvidia/stepfun-ai/step-3.5-flash',
    'nvidia/moonshotai/kimi-k2.5',
    'nvidia/minimaxai/minimax-m2.5',
    'siliconflow/deepseek-ai/DeepSeek-V3.2',
  ],
};

// 重试策略配置
const DEFAULT_RETRY_POLICY = {
  maxRetries: 3,
  backoffMs: 1000,
  backoffMultiplier: 2,
  autoRecover: true,
  recoverIntervalMs: 300000, // 5 分钟
  healthCheckIntervalMs: 60000, // 1 分钟
};

/**
 * 解析模型 ID，提取平台和模型名
 */
function parseModelId(modelId) {
  const parts = modelId.split('/');
  if (parts.length < 2) {
    return { platform: 'unknown', model: modelId };
  }
  return {
    platform: parts[0],
    model: parts.slice(1).join('/'),
  };
}

/**
 * 测试模型是否可用
 */
async function testModel(modelId, timeout = 10000) {
  const { platform, model } = parseModelId(modelId);
  const endpoint = PLATFORM_ENDPOINTS[platform];

  if (!endpoint) {
    return {
      modelId,
      status: 'unknown',
      error: `未知平台: ${platform}`,
      latency: 0,
    };
  }

  const apiKey = process.env[endpoint.apiKeyEnv];
  if (!apiKey) {
    return {
      modelId,
      status: 'no-key',
      error: `缺少环境变量: ${endpoint.apiKeyEnv}`,
      latency: 0,
    };
  }

  const startTime = Date.now();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(`${endpoint.baseUrl}${endpoint.testEndpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: 'Say OK' }],
        max_tokens: 5,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    const latency = Date.now() - startTime;

    if (response.ok) {
      return {
        modelId,
        status: 'healthy',
        latency,
        error: null,
      };
    } else {
      const errorData = await response.json().catch(() => ({}));
      return {
        modelId,
        status: 'error',
        latency,
        error: errorData.error?.message || `HTTP ${response.status}`,
      };
    }
  } catch (error) {
    const latency = Date.now() - startTime;
    return {
      modelId,
      status: 'error',
      latency,
      error: error.name === 'AbortError' ? '请求超时' : error.message,
    };
  }
}

/**
 * 测试整个降级链
 */
async function testFallbackChain(chainName = 'primary') {
  const chain = DEFAULT_FALLBACK_CHAINS[chainName];
  if (!chain) {
    console.error(`❌ 未知降级链: ${chainName}`);
    console.log(`✅ 可用降级链: ${Object.keys(DEFAULT_FALLBACK_CHAINS).join(', ')}`);
    return [];
  }

  console.log(`🔗 测试降级链: ${chainName}\n`);

  const results = [];
  for (const modelId of chain) {
    console.log(`  ⏳ 测试 ${modelId}...`);
    const result = await testModel(modelId);
    results.push(result);

    const statusIcon = result.status === 'healthy' ? '✅' : result.status === 'no-key' ? '⚠️' : '❌';
    console.log(`  ${statusIcon} ${result.status} (${result.latency}ms)${result.error ? ` - ${result.error}` : ''}`);
  }

  return results;
}

/**
 * 监控所有模型状态
 */
async function monitorAllModels() {
  console.log('📊 模型状态监控\n');
  console.log('='.repeat(60));

  const allModels = new Set();
  Object.values(DEFAULT_FALLBACK_CHAINS).forEach((chain) => {
    chain.forEach((model) => allModels.add(model));
  });

  const results = [];
  for (const modelId of allModels) {
    const result = await testModel(modelId, 5000);
    results.push(result);
  }

  // 按状态分组
  const healthy = results.filter((r) => r.status === 'healthy');
  const unhealthy = results.filter((r) => r.status !== 'healthy');

  console.log('\n✅ 健康模型：');
  if (healthy.length === 0) {
    console.log('  (无)');
  } else {
    healthy.forEach((r) => {
      console.log(`  • ${r.modelId} (${r.latency}ms)`);
    });
  }

  console.log('\n❌ 异常模型：');
  if (unhealthy.length === 0) {
    console.log('  (无)');
  } else {
    unhealthy.forEach((r) => {
      console.log(`  • ${r.modelId} - ${r.error}`);
    });
  }

  return results;
}

/**
 * 生成 OpenClaw 降级配置
 */
function generateFallbackConfig(modeId) {
  if (modeId) {
    const mode = getMode(modeId);
    if (!mode) return null;
    printModeNotice(modeId);
    return generateModeFallbackConfig(modeId);
  }

  // 默认：向后兼容
  const config = {
    agents: {
      defaults: {
        model: {
          primary: DEFAULT_FALLBACK_CHAINS.primary[0],
          fallbacks: DEFAULT_FALLBACK_CHAINS.primary.slice(1),
          retryPolicy: DEFAULT_RETRY_POLICY,
        },
      },
    },
  };

  return config;
}

/**
 * 生成带路由的完整配置
 */
function generateFullConfig(modeId) {
  if (modeId) {
    const mode = getMode(modeId);
    if (!mode) return null;
    printModeNotice(modeId);
    return generateModeFullConfig(modeId);
  }

  // 默认：向后兼容
  const config = {
    agents: {
      defaults: {
        model: {
          primary: DEFAULT_FALLBACK_CHAINS.primary[0],
          fallbacks: DEFAULT_FALLBACK_CHAINS.primary.slice(1),
          retryPolicy: DEFAULT_RETRY_POLICY,
        },
        models: {
          routing: {},
        },
      },
    },
  };

  // 添加各任务类型的降级链
  for (const [taskType, chain] of Object.entries(DEFAULT_FALLBACK_CHAINS)) {
    if (taskType !== 'primary') {
      config.agents.defaults.models.routing[taskType] = chain;
    }
  }

  return config;
}

/**
 * 格式化输出测试结果
 */
function formatTestResults(chainName, results) {
  let output = `
🔗 降级链测试结果: ${chainName}
${'='.repeat(50)}

`;

  results.forEach((r, i) => {
    const statusIcon = r.status === 'healthy' ? '✅' : r.status === 'no-key' ? '⚠️' : '❌';
    output += `${i + 1}. ${statusIcon} ${r.modelId}\n`;
    output += `   状态: ${r.status}\n`;
    output += `   延迟: ${r.latency}ms\n`;
    if (r.error) {
      output += `   错误: ${r.error}\n`;
    }
    output += '\n';
  });

  const healthyCount = results.filter((r) => r.status === 'healthy').length;
  output += `📊 总结: ${healthyCount}/${results.length} 模型可用\n`;

  return output;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const modeId = args.includes('--mode') ? args[args.indexOf('--mode') + 1] : null;

  // 列出所有模式
  if (args.includes('--list-modes')) {
    printAllModes();
    return;
  }

  // 生成配置模式
  if (args.includes('--generate-config')) {
    const config = generateFallbackConfig(modeId);
    if (config) {
      console.log(JSON.stringify(config, null, 2));
    }
    return;
  }

  // 生成完整配置
  if (args.includes('--generate-full-config')) {
    const config = generateFullConfig(modeId);
    if (config) {
      console.log(JSON.stringify(config, null, 2));
    }
    return;
  }

  // 检查单个模型
  if (args.includes('--check')) {
    const modelId = args[args.indexOf('--check') + 1];
    if (!modelId) {
      console.error('❌ 请提供模型 ID');
      console.log('用法: node fallback.js --check siliconflow/Qwen/Qwen3-8B');
      return;
    }

    console.log(`🔍 检查模型: ${modelId}\n`);
    const result = await testModel(modelId);
    const statusIcon = result.status === 'healthy' ? '✅' : result.status === 'no-key' ? '⚠️' : '❌';
    console.log(`${statusIcon} 状态: ${result.status}`);
    console.log(`⏱️ 延迟: ${result.latency}ms`);
    if (result.error) {
      console.log(`❌ 错误: ${result.error}`);
    }
    return;
  }

  // 监控所有模型
  if (args.includes('--monitor')) {
    await monitorAllModels();
    return;
  }

  // 测试降级链
  if (args.includes('--test')) {
    const chainName = args.includes('--chain') ? args[args.indexOf('--chain') + 1] : 'primary';

    // 支持 --mode 测试指定模式的免费模型链
    if (modeId) {
      const mode = getMode(modeId);
      if (!mode) return;
      console.log(`${mode.emoji} 测试 ${mode.name} 降级链\n`);
      const results = [];
      for (const modelId of mode.fallbacks) {
        console.log(`  ⏳ 测试 ${modelId}...`);
        const result = await testModel(modelId);
        results.push(result);
        const statusIcon = result.status === 'healthy' ? '✅' : result.status === 'no-key' ? '⚠️' : '❌';
        console.log(`  ${statusIcon} ${result.status} (${result.latency}ms)${result.error ? ` - ${result.error}` : ''}`);
      }
      console.log(formatTestResults(`${mode.name} 降级链`, results));
      return;
    }

    if (chainName === 'all') {
      for (const chain of Object.keys(DEFAULT_FALLBACK_CHAINS)) {
        const results = await testFallbackChain(chain);
        console.log(formatTestResults(chain, results));
        console.log('-'.repeat(60));
      }
    } else {
      const results = await testFallbackChain(chainName);
      console.log(formatTestResults(chainName, results));
    }
    return;
  }

  // 列出所有降级链
  if (args.includes('--list-chains')) {
    console.log('🔗 可用降级链：\n');
    for (const [name, chain] of Object.entries(DEFAULT_FALLBACK_CHAINS)) {
      console.log(`  ${name}:`);
      chain.forEach((model, i) => {
        console.log(`    ${i + 1}. ${model}`);
      });
      console.log('');
    }
    return;
  }

  // 默认：显示帮助
  console.log('🔄 无感降级管理器\n');
  console.log('主模型失败时自动切换到备用模型，并支持自动回切\n');
  console.log('用法：');
  console.log('  node fallback.js --test                           # 测试默认降级链');
  console.log('  node fallback.js --test --mode royal              # 测试富豪模式降级链');
  console.log('  node fallback.js --test --chain all               # 测试所有降级链');
  console.log('  node fallback.js --monitor                        # 监控模型状态');
  console.log('  node fallback.js --check <model-id>               # 检查单个模型');
  console.log('  node fallback.js --list-chains                    # 列出所有降级链');
  console.log('  node fallback.js --list-modes                     # 列出所有模式');
  console.log('  node fallback.js --generate-config                # 生成默认降级配置');
  console.log('  node fallback.js --generate-config --mode royal   # 生成富豪模式配置');
  console.log('  node fallback.js --generate-config --mode balanced # 生成均衡模式配置');
  console.log('  node fallback.js --generate-config --mode savings # 生成省钱模式配置');
  console.log('  node fallback.js --generate-full-config           # 生成默认完整配置');
  console.log('  node fallback.js --generate-full-config --mode savings # 生成省钱模式完整配置');
}

// ESM 兼容的直接执行检测
const isMain = process.argv[1]?.endsWith('fallback.js');
if (isMain) {
  main().catch((error) => {
    console.error('❌ 执行失败:', error.message);
    process.exit(1);
  });
}

// 导出函数供其他模块使用
export {
  PLATFORM_ENDPOINTS,
  DEFAULT_FALLBACK_CHAINS,
  DEFAULT_RETRY_POLICY,
  parseModelId,
  testModel,
  testFallbackChain,
  monitorAllModels,
  generateFallbackConfig,
  generateFullConfig,
};

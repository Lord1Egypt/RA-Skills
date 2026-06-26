/**
 * Chenni Free API - 自动发现免费模型
 *
 * 从多个平台自动发现免费或超低价 AI 模型
 *
 * Usage:
 *   node discover.js --platform all
 *   node discover.js --platform openrouter
 *   node discover.js --platform siliconflow
 *   node discover.js --platform nvidia
 *   node discover.js --platform all --json
 *
 * Environment:
 *   OPENROUTER_API_KEY - OpenRouter API Key (可选，用于获取更多模型)
 *   SILICONFLOW_API_KEY - SiliconFlow API Key (可选，用于获取更多模型)
 *   NVIDIA_API_KEY - NVIDIA NIM API Key (可选，用于获取更多模型)
 */

// 价格阈值配置
const PRICE_THRESHOLDS = {
  free: 0,           // 完全免费
  ultraLow: 0.0001,  // 超低价（低于 $0.0001/1M tokens）
};

// 平台配置
const PLATFORMS = {
  openrouter: {
    name: 'OpenRouter',
    baseUrl: 'https://openrouter.ai/api/v1',
    modelsEndpoint: '/models',
    freeThreshold: 0.0001, // 低于此价格视为免费
  },
  siliconflow: {
    name: 'SiliconFlow',
    baseUrl: 'https://api.siliconflow.cn/v1',
    modelsEndpoint: '/models?sub_type=chat',
    freeThreshold: 0,
  },
  nvidia: {
    name: 'NVIDIA NIM',
    baseUrl: 'https://integrate.api.nvidia.com/v1',
    modelsEndpoint: '/models',
    freeThreshold: 0, // NVIDIA NIM 免费模型
  },
};

/**
 * 获取 OpenRouter 模型列表
 */
async function fetchOpenRouterModels() {
  const apiKey = process.env.OPENROUTER_API_KEY;
  const headers = { 'Content-Type': 'application/json' };
  if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;

  try {
    const res = await fetch(`${PLATFORMS.openrouter.baseUrl}${PLATFORMS.openrouter.modelsEndpoint}`, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    const data = await res.json();
    return data.data.map((m) => ({
      id: m.id,
      name: m.name,
      platform: 'openrouter',
      contextLength: m.context_length || 0,
      pricing: {
        prompt: parseFloat(m.pricing?.prompt || '0'),
        completion: parseFloat(m.pricing?.completion || '0'),
      },
      isFree: parseFloat(m.pricing?.prompt || '0') < PLATFORMS.openrouter.freeThreshold,
      description: m.description || '',
    }));
  } catch (error) {
    console.error(`❌ OpenRouter 获取失败: ${error.message}`);
    return [];
  }
}

/**
 * 获取 SiliconFlow 模型列表
 */
async function fetchSiliconFlowModels() {
  const apiKey = process.env.SILICONFLOW_API_KEY;
  const headers = { 'Content-Type': 'application/json' };
  if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;

  try {
    const res = await fetch(`${PLATFORMS.siliconflow.baseUrl}${PLATFORMS.siliconflow.modelsEndpoint}`, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    const data = await res.json();
    return data.data.map((m) => ({
      id: m.id,
      name: m.name || m.id,
      platform: 'siliconflow',
      contextLength: m.context_length || 32768,
      pricing: {
        prompt: m.pricing?.prompt || 0,
        completion: m.pricing?.completion || 0,
      },
      isFree: (m.pricing?.prompt || 0) === 0,
      description: m.description || '',
    }));
  } catch (error) {
    console.error(`❌ SiliconFlow 获取失败: ${error.message}`);
    // API 不可用时返回预定义免费模型列表
    return getSiliconFlowFreeModels();
  }
}

/**
 * SiliconFlow 预定义免费模型列表（API 不可用时的备用方案）
 * 数据来源：https://siliconflow.cn/pricing
 */
function getSiliconFlowFreeModels() {
  return [
    {
      id: 'Qwen/Qwen3.5-4B',
      name: 'Qwen 3.5 4B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'Qwen 3.5 4B，轻量免费模型',
    },
    {
      id: 'Qwen/Qwen3-8B',
      name: 'Qwen 3 8B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '通义千问 3 代 8B，综合能力强',
    },
    {
      id: 'Qwen/Qwen2.5-7B-Instruct',
      name: 'Qwen 2.5 7B Instruct',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'Qwen 2.5 7B 指令微调版',
    },
    {
      id: 'deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
      name: 'DeepSeek R1 Distill Qwen 7B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'DeepSeek R1 蒸馏版 7B，推理能力强',
    },
    {
      id: 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B',
      name: 'DeepSeek R1 0528 Qwen3 8B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'DeepSeek R1 0528 蒸馏版，推理能力强',
    },
    {
      id: 'deepseek-ai/DeepSeek-OCR',
      name: 'DeepSeek OCR',
      platform: 'siliconflow',
      contextLength: 32768,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'DeepSeek OCR 文档识别模型',
    },
    {
      id: 'THUDM/GLM-4.1V-9B-Thinking',
      name: 'GLM-4.1V 9B Thinking',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '智谱 GLM-4.1V 思维链版，支持视觉',
    },
    {
      id: 'THUDM/GLM-Z1-9B-0414',
      name: 'GLM-Z1 9B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '智谱 GLM-Z1 9B',
    },
    {
      id: 'THUDM/GLM-4-9B-0414',
      name: 'GLM-4 9B',
      platform: 'siliconflow',
      contextLength: 131072,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '智谱 GLM-4 9B',
    },
    {
      id: 'tencent/Hunyuan-MT-7B',
      name: 'Hunyuan MT 7B',
      platform: 'siliconflow',
      contextLength: 32768,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '腾讯混元翻译模型，中英翻译专用',
    },
    {
      id: 'PaddlePaddle/PaddleOCR-VL',
      name: 'PaddleOCR-VL',
      platform: 'siliconflow',
      contextLength: 32768,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '百度 PaddleOCR 视觉文档理解',
    },
    {
      id: 'PaddlePaddle/PaddleOCR-VL-1.5',
      name: 'PaddleOCR-VL 1.5',
      platform: 'siliconflow',
      contextLength: 32768,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '百度 PaddleOCR 1.5 增强版',
    },
    {
      id: 'internlm/internlm2_5-7b-chat',
      name: 'InternLM2.5 7B Chat',
      platform: 'siliconflow',
      contextLength: 32768,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '书生·浦语 2.5 7B 对话版',
    },
  ];
}

/**
 * 获取 NVIDIA NIM 模型列表
 */
async function fetchNvidiaModels() {
  const apiKey = process.env.NVIDIA_API_KEY;
  const headers = { 'Content-Type': 'application/json' };
  if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;

  try {
    const res = await fetch(`${PLATFORMS.nvidia.baseUrl}${PLATFORMS.nvidia.modelsEndpoint}`, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    const data = await res.json();
    return data.data.map((m) => ({
      id: m.id,
      name: m.name || m.id,
      platform: 'nvidia',
      contextLength: m.context_length || 128000,
      pricing: {
        prompt: 0, // NVIDIA NIM 免费
        completion: 0,
      },
      isFree: true, // NVIDIA NIM 免费模型
      description: m.description || '',
      capabilities: m.capabilities || [],
    }));
  } catch (error) {
    console.error(`❌ NVIDIA NIM 获取失败: ${error.message}`);
    // 如果 API 失败，返回预定义的免费模型列表
    return getNvidiaFreeModels();
  }
}

/**
 * 获取 NVIDIA 预定义免费模型列表（API 不可用时的备用方案）
 */
function getNvidiaFreeModels() {
  return [
    {
      id: 'qwen/qwen3.5-397b-a17b',
      name: 'Qwen 3.5 397B',
      platform: 'nvidia',
      contextLength: 128000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'Qwen 3.5 大参数版本',
      capabilities: ['text', 'image'],
    },
    {
      id: 'stepfun-ai/step-3.5-flash',
      name: 'Step 3.5 Flash',
      platform: 'nvidia',
      contextLength: 256000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '阶跃星辰，超长上下文',
      capabilities: ['text', 'image'],
    },
    {
      id: 'moonshotai/kimi-k2.5',
      name: 'Kimi K2.5',
      platform: 'nvidia',
      contextLength: 256000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'Kimi，超长上下文',
      capabilities: ['text', 'image'],
    },
    {
      id: 'z-ai/glm4.7',
      name: 'GLM 4.7',
      platform: 'nvidia',
      contextLength: 128000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '智谱 GLM 4.7',
      capabilities: ['text', 'image'],
    },
    {
      id: 'z-ai/glm5',
      name: 'GLM 5',
      platform: 'nvidia',
      contextLength: 128000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: '智谱 GLM 5',
      capabilities: ['text', 'image'],
    },
    {
      id: 'minimaxai/minimax-m2.5',
      name: 'MiniMax M2.5',
      platform: 'nvidia',
      contextLength: 192000,
      pricing: { prompt: 0, completion: 0 },
      isFree: true,
      description: 'MiniMax',
      capabilities: ['text', 'image'],
    },
  ];
}

/**
 * 筛选免费模型（价格为 0）
 */
function filterFreeModels(models) {
  return models.filter((m) => 
    m.pricing.prompt === 0 && m.pricing.completion === 0
  );
}

/**
 * 筛选超低价模型（价格低于阈值但不为 0）
 */
function filterUltraLowPriceModels(models, maxPrice = PRICE_THRESHOLDS.ultraLow) {
  return models.filter((m) => 
    (m.pricing.prompt > 0 || m.pricing.completion > 0) &&
    m.pricing.prompt <= maxPrice && 
    m.pricing.completion <= maxPrice
  );
}

/**
 * 筛选所有低价模型（包含免费和超低价）
 */
function filterAllLowPriceModels(models, maxPrice = PRICE_THRESHOLDS.ultraLow) {
  return models.filter((m) => 
    m.pricing.prompt <= maxPrice && m.pricing.completion <= maxPrice
  );
}

/**
 * 统计模型分类
 */
function categorizeModels(models) {
  const free = filterFreeModels(models);
  const ultraLow = filterUltraLowPriceModels(models);
  const allLow = filterAllLowPriceModels(models);
  
  return {
    total: models.length,
    free: free.length,
    ultraLow: ultraLow.length,
    allLow: allLow.length,
    freeModels: free,
    ultraLowModels: ultraLow,
    allLowModels: allLow,
  };
}

/**
 * 按上下文长度排序
 */
function sortByContext(models) {
  return [...models].sort((a, b) => b.contextLength - a.contextLength);
}

/**
 * 按价格排序
 */
function sortByPrice(models) {
  return [...models].sort((a, b) => a.pricing.prompt - b.pricing.prompt);
}

/**
 * 格式化输出模型信息
 */
function formatModel(model, index, showCategory = false) {
  let priceStr;
  if (model.pricing.prompt === 0 && model.pricing.completion === 0) {
    priceStr = '🆓 FREE';
  } else {
    priceStr = `💰 $${model.pricing.prompt}/1M prompt | $${model.pricing.completion}/1M completion`;
  }

  let categoryStr = '';
  if (showCategory) {
    const category = model.pricing.prompt === 0 ? '免费' : '超低价';
    categoryStr = ` [${category}]`;
  }

  return `
  ${index + 1}. ${model.name}${categoryStr}
     ID: ${model.platform}/${model.id}
     Context: ${model.contextLength.toLocaleString()} tokens
     Price: ${priceStr}
     ${model.description ? `Description: ${model.description.substring(0, 80)}...` : ''}
  `.trim();
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const platform = args.includes('--platform') ? args[args.indexOf('--platform') + 1] : 'all';
  const jsonOutput = args.includes('--json');
  const maxPrice = args.includes('--max-price') ? parseFloat(args[args.indexOf('--max-price') + 1]) : PRICE_THRESHOLDS.ultraLow;
  const showFreeOnly = args.includes('--free-only');
  const showUltraLowOnly = args.includes('--ultra-low-only');

  console.log('🔍 正在发现免费/超低价模型...\n');

  let allModels = [];

  // 根据平台参数获取模型
  if (platform === 'all' || platform === 'openrouter') {
    console.log('📡 正在获取 OpenRouter 模型...');
    const openrouterModels = await fetchOpenRouterModels();
    allModels = allModels.concat(openrouterModels);
    console.log(`   找到 ${openrouterModels.length} 个模型`);
  }

  if (platform === 'all' || platform === 'siliconflow') {
    console.log('📡 正在获取 SiliconFlow 模型...');
    const siliconflowModels = await fetchSiliconFlowModels();
    allModels = allModels.concat(siliconflowModels);
    console.log(`   找到 ${siliconflowModels.length} 个模型`);
  }

  if (platform === 'all' || platform === 'nvidia') {
    console.log('📡 正在获取 NVIDIA NIM 模型...');
    const nvidiaModels = await fetchNvidiaModels();
    allModels = allModels.concat(nvidiaModels);
    console.log(`   找到 ${nvidiaModels.length} 个模型`);
  }

  // 统计模型分类
  const stats = categorizeModels(allModels);

  console.log(`\n📊 模型统计：`);
  console.log(`   总模型数: ${stats.total}`);
  console.log(`   🆓 免费模型: ${stats.free}`);
  console.log(`   💰 超低价模型: ${stats.ultraLow}`);
  console.log(`   ✅ 低价总计: ${stats.allLow}`);

  // 确定要显示的模型
  let modelsToShow;
  let displayTitle;
  
  if (showFreeOnly) {
    modelsToShow = stats.freeModels;
    displayTitle = '🆓 免费模型';
  } else if (showUltraLowOnly) {
    modelsToShow = stats.ultraLowModels;
    displayTitle = '💰 超低价模型';
  } else {
    modelsToShow = stats.allLowModels;
    displayTitle = '🆓💰 免费/超低价模型';
  }

  if (jsonOutput) {
    // JSON 输出
    const output = {
      timestamp: new Date().toISOString(),
      totalModels: stats.total,
      freeModels: stats.free,
      ultraLowModels: stats.ultraLow,
      allLowModels: stats.allLow,
      models: showFreeOnly ? stats.freeModels : 
              showUltraLowOnly ? stats.ultraLowModels : 
              stats.allLowModels,
    };
    console.log(JSON.stringify(output, null, 2));
  } else {
    // 格式化输出
    if (modelsToShow.length === 0) {
      console.log(`\n⚠️ 未找到${displayTitle}，尝试使用 --max-price 调整阈值`);
      console.log('\n📊 最便宜的 10 个模型：');
      const cheapest = sortByPrice(allModels).slice(0, 10);
      cheapest.forEach((m, i) => console.log(formatModel(m, i)));
    } else {
      console.log(`\n${displayTitle}列表（按上下文长度排序）：\n`);
      
      // 如果显示全部，分别显示免费和超低价
      if (!showFreeOnly && !showUltraLowOnly) {
        // 先显示免费模型
        if (stats.freeModels.length > 0) {
          console.log('🆓 免费模型：');
          sortByContext(stats.freeModels).slice(0, 15).forEach((m, i) => 
            console.log(formatModel(m, i))
          );
          if (stats.freeModels.length > 15) {
            console.log(`  ... 还有 ${stats.freeModels.length - 15} 个免费模型`);
          }
          console.log('');
        }
        
        // 再显示超低价模型
        if (stats.ultraLowModels.length > 0) {
          console.log('💰 超低价模型（前 15 个）：');
          sortByContext(stats.ultraLowModels).slice(0, 15).forEach((m, i) => 
            console.log(formatModel(m, i))
          );
          if (stats.ultraLowModels.length > 15) {
            console.log(`  ... 还有 ${stats.ultraLowModels.length - 15} 个超低价模型`);
          }
        }
      } else {
        // 只显示筛选后的模型
        sortByContext(modelsToShow).slice(0, 30).forEach((m, i) => 
          console.log(formatModel(m, i, true))
        );
        if (modelsToShow.length > 30) {
          console.log(`\n  ... 还有 ${modelsToShow.length - 30} 个模型`);
        }
      }

      // 按平台分组统计
      console.log('\n📊 平台统计：');
      const byPlatform = {};
      modelsToShow.forEach((m) => {
        byPlatform[m.platform] = (byPlatform[m.platform] || 0) + 1;
      });
      Object.entries(byPlatform).forEach(([p, count]) => {
        console.log(`   ${PLATFORMS[p]?.name || p}: ${count} 个模型`);
      });
    }
  }
}

// ESM 兼容的直接执行检测
const isMain = process.argv[1]?.endsWith('discover.js');
if (isMain) {
  main().catch((error) => {
    console.error('❌ 执行失败:', error.message);
    process.exit(1);
  });
}

// 导出函数供其他模块使用
export {
  fetchOpenRouterModels,
  fetchSiliconFlowModels,
  fetchNvidiaModels,
  getNvidiaFreeModels,
  getSiliconFlowFreeModels,
  filterFreeModels,
  filterUltraLowPriceModels,
  filterAllLowPriceModels,
  categorizeModels,
  sortByContext,
  sortByPrice,
  PRICE_THRESHOLDS,
  PLATFORMS,
};

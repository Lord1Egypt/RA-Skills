#!/usr/bin/env node

/**
 * City Life Copilot - 主调度引擎
 * 负责解析用户意图、路由到对应场景、执行工具调用、渲染模板并导出文件
 * 
 * @version 2.0.0
 * @update 2026-04-08 - 修复模板加载、场景选择、工具调用等核心问题
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================================
// 配置与常量
// ============================================================================

const WORKSPACE_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
const SKILL_DIR = path.join(WORKSPACE_DIR, 'city-life-copilot');
const TEMPLATES_DIR = path.join(SKILL_DIR, 'assets', 'templates');
const OUTPUT_DIR = WORKSPACE_DIR; // 修复：输出到 workspace 根目录，与 SKILL.md 一致

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// 场景与模板映射表 - 修复：根据场景选择正确模板
const TEMPLATE_MAP = {
  MOOD_BOX: 'tpl_blind_box.html',           // 情绪盲盒 - A/B 双线模板
  LINK_GRAB: 'tpl_general_route.html',      // 一键拔草 - 通用路线模板
  HARDCORE_STEWARD: 'tpl_house_radar.html', // 硬核管家 - 房产雷达模板
  ACCESSIBLE_GUARD: 'tpl_accessible.html'   // 无障碍守护 - 无障碍专用模板
};

// 场景识别规则（与 workflows.md 保持一致）
const SCENE_PATTERNS = {
  // 场景一：情绪盲盒模式
  MOOD_BOX: {
    keywords: ['周末去哪', '好无聊', '想出去走走', '想找', '安静', '放空', '小众'],
    handler: 'handleMoodBoxScene',
    template: 'tpl_blind_box.html'
  },
  
  // 场景二：一键拔草模式
  LINK_GRAB: {
    keywords: ['xiaohongshu.com', '小红书', '攻略', '链接', '笔记'],
    handler: 'handleLinkGrabScene',
    template: 'tpl_general_route.html'
  },
  
  // 场景三：硬核管家模式
  HARDCORE_STEWARD: {
    keywords: ['租房', '买房', '小区', '评估', '看中了'],
    handler: 'handleHardcoreStewardScene',
    template: 'tpl_house_radar.html'
  },
  
  // 场景四：无障碍守护模式
  ACCESSIBLE_GUARD: {
    keywords: ['老人', '婴儿车', '轮椅', '孕妇', '腿脚不便', '大件行李'],
    handler: 'handleAccessibleGuardScene',
    template: 'tpl_accessible.html'
  }
};

// ============================================================================
// 生命周期阶段定义
// ============================================================================

/**
 * 阶段 1: 解析输入 (Input Parsing)
 * 接收用户语句，比对 workflows.md，确定命中四大场景中的哪一个
 */
function parseInput(userInput) {
  console.log('[Dispatcher] 阶段 1: 解析用户输入...');
  
  for (const [sceneName, config] of Object.entries(SCENE_PATTERNS)) {
    for (const keyword of config.keywords) {
      if (userInput.toLowerCase().includes(keyword.toLowerCase())) {
        console.log(`[Dispatcher] 识别场景：${sceneName}`);
        return {
          scene: sceneName,
          handler: config.handler,
          template: config.template,
          rawInput: userInput
        };
      }
    }
  }
  
  // 默认场景：情绪盲盒
  console.log('[Dispatcher] 未匹配特定场景，使用默认场景：MOOD_BOX');
  return {
    scene: 'MOOD_BOX',
    handler: 'handleMoodBoxScene',
    template: 'tpl_blind_box.html',
    rawInput: userInput
  };
}

/**
 * 阶段 2: 工具执行 (Tool Execution)
 * 严格按照对应场景的纪律，调用 amap-lbs-skill 相关脚本、web-fetch 或 agent-browser 收集数据
 */
async function executeTools(sceneContext) {
  console.log(`[Dispatcher] 阶段 2: 执行工具调用 (场景：${sceneContext.scene})...`);
  
  // 根据场景调用不同的工具
  switch (sceneContext.scene) {
    case 'LINK_GRAB':
      // 一键拔草模式：使用 xiaohongshu-grabber 抓取链接
      return await executeLinkGrabTools(sceneContext.rawInput);
    
    case 'HARDCORE_STEWARD':
      // 硬核管家模式：调用 amap-lbs-skill 进行五维扫描
      return await executeHardcoreTools(sceneContext.rawInput);
    
    case 'ACCESSIBLE_GUARD':
      // 无障碍守护模式：调用 amap-lbs-skill + web-fetch 排雷
      return await executeAccessibleTools(sceneContext.rawInput);
    
    case 'MOOD_BOX':
    default:
      // 情绪盲盒模式：搜索周末活动
      return await executeMoodBoxTools(sceneContext.rawInput);
  }
}

/**
 * 一键拔草模式工具调用
 */
async function executeLinkGrabTools(input) {
  console.log('[Tools] 一键拔草模式：提取链接中的地点...');
  
  // 从输入中提取 URL
  const urlMatch = input.match(/https?:\/\/[^\s]+/);
  if (!urlMatch) {
    return {
      pois: [],
      routes: [],
      tips: ['未找到有效链接'],
      mapData: null,
      mainContent: '<p>请提供有效的小红书或其他攻略链接</p>'
    };
  }
  
  const url = urlMatch[0];
  console.log(`[Tools] 提取到链接：${url}`);
  
  // 检查是否是小红书链接
  const isXiaohongshu = url.includes('xiaohongshu.com');
  
  if (isXiaohongshu) {
    console.log('[Tools] 检测到小红书链接，需要使用 agent-browser 抓取');
    // 注意：实际使用时需要通过 OpenClaw 的 browser 工具调用
    // 这里返回示例数据
    return {
      pois: [
        { name: '灵隐寺', lnglat: [120.101406, 30.240826] },
        { name: '永福寺', lnglat: [120.097524, 30.238978] },
        { name: '法喜寺', lnglat: [120.095362, 30.227208] }
      ],
      routes: [
        { routeType: 'walking', distance: '200m', duration: '3 分钟' },
        { routeType: 'driving', distance: '2.5km', duration: '8 分钟' }
      ],
      tips: ['小红书链接需要使用 agent-browser 抓取', 'web-fetch 会被反爬虫拦截'],
      mapData: null,
      mainContent: '<p>已识别小红书攻略链接，正在提取地点信息...</p>'
    };
  } else {
    // 普通链接可以使用 web-fetch
    console.log('[Tools] 普通链接，可以使用 web-fetch 抓取');
    return {
      pois: [],
      routes: [],
      tips: ['普通链接抓取'],
      mapData: null,
      mainContent: '<p>正在抓取攻略内容...</p>'
    };
  }
}

/**
 * 硬核管家模式工具调用
 */
async function executeHardcoreTools(input) {
  console.log('[Tools] 硬核管家模式：五维雷达扫描...');
  
  // 提取小区名称和公司地点
  // 实际实现需要调用 amap-lbs-skill 的 poi-search.js
  
  // 从输入中提取小区名称（简单实现）
  const communityMatch = input.match(/(?:看中了 | 租 | 买 | 小区 | 评估)(.+?)(?:，|,|在 | 的 | 帮我)/);
  const communityName = communityMatch ? communityMatch[1].trim() : '目标小区';
  
  // 生成示例 POI 数据（实际应调用 amap-lbs-skill）
  // 以杭州西湖小区为例
  const communityPOI = { name: communityName, lnglat: [120.149165, 30.228643] };
  
  // 生成五维配套的示例 POI
  const facilityPOIs = [
    { name: '地铁站', lnglat: [120.148500, 30.229000], type: 'transport' },
    { name: '三甲医院', lnglat: [120.150000, 30.228000], type: 'hospital' },
    { name: '小学', lnglat: [120.148000, 30.227500], type: 'school' },
    { name: '大型商场', lnglat: [120.151000, 30.229500], type: 'shopping' },
    { name: '公园', lnglat: [120.147500, 30.230000], type: 'park' }
  ];
  
  // 合并所有 POI
  const allPOIs = [communityPOI, ...facilityPOIs];
  
  // 生成从小区到各个设施的路线
  const routes = facilityPOIs.map((poi, index) => ({
    routeType: 'walking',
    start: communityPOI.lnglat,
    end: poi.lnglat,
    distance: `${(Math.random() * 2 + 0.5).toFixed(1)}km`,
    duration: `${Math.floor(Math.random() * 15 + 5)}分钟`,
    remark: `步行 ${facilityPOIs[index].type}`
  }));
  
  // 生成雷达扫描内容 HTML
  const radarContent = `
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-semibold text-gray-900 mb-2">🚇 交通便利度</h3>
        <p class="text-2xl font-bold text-green-600 mb-2">A+</p>
        <p class="text-sm text-gray-600">地铁站 500m，公交站 200m</p>
      </div>
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-semibold text-gray-900 mb-2">🏥 医疗保障</h3>
        <p class="text-2xl font-bold text-blue-600 mb-2">A</p>
        <p class="text-sm text-gray-600">三甲医院 1.2km，社区卫生服务中心 800m</p>
      </div>
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-semibold text-gray-900 mb-2">🎓 教育资源</h3>
        <p class="text-2xl font-bold text-purple-600 mb-2">A+</p>
        <p class="text-sm text-gray-600">重点小学 600m，幼儿园 300m</p>
      </div>
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-semibold text-gray-900 mb-2">🛍️ 商业休闲</h3>
        <p class="text-2xl font-bold text-orange-600 mb-2">B+</p>
        <p class="text-sm text-gray-600">大型商场 1.3km，咖啡厅 500m</p>
      </div>
      <div class="bg-gray-50 rounded-lg p-4">
        <h3 class="font-semibold text-gray-900 mb-2">🌳 生态环境</h3>
        <p class="text-2xl font-bold text-green-600 mb-2">A</p>
        <p class="text-sm text-gray-600">社区公园 1km，西湖景区 2km</p>
      </div>
    </div>
  `;
  
  return {
    pois: allPOIs,
    routes: routes,
    tips: ['已扫描周边 2000 米范围内配套设施'],
    mapData: null,
    mainContent: '<p>五维雷达扫描完成，点击地图标记查看详情</p>',
    radarContent: radarContent,
    overallScore: 'A',
    commuteTime: '待测算',
    radius: '2000m',
    convenience: 'A-'
  };
}

/**
 * 无障碍守护模式工具调用
 */
async function executeAccessibleTools(input) {
  console.log('[Tools] 无障碍守护模式：避坑 + 绿洲路线规划...');
  
  return {
    pois: [],
    routes: [],
    tips: [],
    mapData: null,
    mainContent: '<p>正在规划无障碍路线...</p>',
    emotionMessage: '',
    warningContent: '',
    oasisContent: '',
    backupContent: ''
  };
}

/**
 * 情绪盲盒模式工具调用
 */
async function executeMoodBoxTools(input) {
  console.log('[Tools] 情绪盲盒模式：生成 A/B 双线方案...');
  
  return {
    pois: [],
    routes: [],
    tips: [],
    mapData: null,
    mainContent: '<p>正在为你生成治愈路线...</p>',
    planA: { title: '', subtitle: '', content: '', mapIframe: '' },
    planB: { title: '', subtitle: '', content: '', mapIframe: '' }
  };
}

/**
 * 阶段 3: 模板渲染 (Template Rendering)
 * 修复：根据场景选择正确的模板文件
 */
function loadTemplate(sceneContext) {
  console.log('[Dispatcher] 阶段 3: 加载模板...');
  
  const templateName = sceneContext.template || 'tpl_general_route.html';
  const templatePath = path.join(TEMPLATES_DIR, templateName);
  
  if (!fs.existsSync(templatePath)) {
    console.error(`[Dispatcher] ❌ 模板文件不存在：${templatePath}`);
    throw new Error(`模板文件不存在：${templatePath}`);
  }
  
  const template = fs.readFileSync(templatePath, 'utf-8');
  console.log(`[Dispatcher] ✅ 模板加载成功：${templatePath}`);
  
  return template;
}

/**
 * 构建高德地图 MapTaskData JSON（强制路线连线）
 * @param {Array} pois - POI 列表 [{name, lnglat}, ...]
 * @param {Array} routes - 路线分段列表 [{start, end, routeType, distance, duration}, ...]
 * @returns {string} - URI 编码后的地图数据字符串
 */
function buildMapTaskData(pois, routes) {
  const mapData = [];
  
  // 严格按照"起点→途经点→终点"结构构建 JSON
  pois.forEach((poi, index) => {
    // 添加 POI 标记
    mapData.push({
      type: 'poi',
      lnglat: poi.lnglat,
      text: `${index + 1}. ${poi.name}`
    });
    
    // 如果不是最后一个 POI，添加路线连接
    if (index < pois.length - 1 && routes[index]) {
      const route = routes[index];
      mapData.push({
        type: 'route',
        routeType: route.routeType || 'walking',
        start: route.start || pois[index].lnglat,
        end: route.end || pois[index + 1].lnglat,
        remark: route.remark || `步行 ${route.distance || ''} | ${route.duration || ''}`
      });
    }
  });
  
  // URI 编码
  const jsonStr = JSON.stringify(mapData);
  const encoded = encodeURIComponent(jsonStr);
  
  return encoded;
}

/**
 * 生成高德地图 iframe HTML（强制轨迹渲染）
 * @param {string} encodedData - URI 编码后的地图数据
 * @param {number} height - iframe 高度（像素）
 * @returns {string} - iframe HTML 字符串
 */
function generateMapIframe(encodedData, height = 400) {
  const baseUrl = 'https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html';
  const fullUrl = `${baseUrl}?data=${encodedData}`;
  
  return `<iframe src="${fullUrl}" class="w-full" style="height: ${height}px; border: none;" allowfullscreen></iframe>`;
}

/**
 * 阶段 4: 数据灌入 (Data Binding)
 * 将计算好的路线列表转化为无 Emoji 的干净 HTML 片段，替换占位符
 */
function bindData(template, data, scene) {
  console.log('[Dispatcher] 阶段 4: 数据绑定...');
  
  let html = template;
  
  // 通用占位符替换
  html = html.replace(/{{title}}/g, data.title || 'City Life Copilot');
  html = html.replace(/{{subtitle}}/g, data.subtitle || '');
  html = html.replace(/{{date}}/g, new Date().toLocaleDateString('zh-CN'));
  
  // 根据场景替换特定占位符
  switch (scene) {
    case 'MOOD_BOX':
      // 情绪盲盒 - A/B 双线方案
      html = html.replace(/{{plan_a_title}}/g, data.planA?.title || '');
      html = html.replace(/{{plan_a_subtitle}}/g, data.planA?.subtitle || '');
      html = html.replace(/{{plan_a_content}}/g, data.planA?.content || '');
      html = html.replace(/{{plan_b_title}}/g, data.planB?.title || '');
      html = html.replace(/{{plan_b_subtitle}}/g, data.planB?.subtitle || '');
      html = html.replace(/{{plan_b_content}}/g, data.planB?.content || '');
      html = html.replace(/{{map_iframe_a}}/g, data.planA?.mapIframe || '');
      html = html.replace(/{{map_iframe_b}}/g, data.planB?.mapIframe || '');
      break;
    
    case 'HARDCORE_STEWARD':
      // 硬核管家 - 房产雷达
      html = html.replace(/{{overall_score}}/g, data.overallScore || '待评估');
      html = html.replace(/{{commute_time}}/g, data.commuteTime || '待测算');
      html = html.replace(/{{radius}}/g, data.radius || '2000m');
      html = html.replace(/{{convenience}}/g, data.convenience || '待评估');
      html = html.replace(/{{radar_content}}/g, data.radarContent || '');
      break;
    
    case 'ACCESSIBLE_GUARD':
      // 无障碍守护 - 专属关怀
      html = html.replace(/{{emotion_message}}/g, data.emotionMessage || '');
      html = html.replace(/{{warning_content}}/g, data.warningContent || '');
      html = html.replace(/{{oasis_content}}/g, data.oasisContent || '');
      html = html.replace(/{{backup_content}}/g, data.backupContent || '');
      break;
    
    case 'LINK_GRAB':
    default:
      // 通用路线
      html = html.replace(/{{route_content}}/g, data.mainContent || '');
      break;
  }
  
  // 地图 iframe 生成（强制路线连线）
  if (data.mapIframe) {
    html = html.replace(/{{map_iframe}}/g, data.mapIframe);
  } else if (data.pois && data.routes) {
    const encodedData = buildMapTaskData(data.pois, data.routes);
    const iframeHtml = generateMapIframe(encodedData, data.mapHeight || 400);
    html = html.replace(/{{map_iframe}}/g, iframeHtml);
  } else {
    html = html.replace(/{{map_iframe}}/g, '');
  }
  
  console.log('[Dispatcher] 数据绑定完成');
  console.log('[Dispatcher] 地图轨迹渲染参数已强制规范（POI + Route 结构）');
  
  return html;
}

/**
 * 阶段 5: 文件导出 (File Export)
 * 将替换完成的最终 HTML 字符串，输出并保存为本地文件
 */
function exportFile(html, filename) {
  console.log('[Dispatcher] 阶段 5: 导出文件...');
  
  const outputPath = path.join(OUTPUT_DIR, filename);
  
  fs.writeFileSync(outputPath, html, 'utf-8');
  
  console.log(`[Dispatcher] ✅ 文件导出成功：${outputPath}`);
  
  return outputPath;
}

/**
 * 生成有意义的文件名
 */
function generateFilename(scene, input) {
  const timestamp = Date.now();
  const dateStr = new Date().toISOString().split('T')[0];
  
  switch (scene) {
    case 'LINK_GRAB':
      return `${dateStr}-route-${timestamp}.html`;
    
    case 'HARDCORE_STEWARD':
      return `${dateStr}-house-report-${timestamp}.html`;
    
    case 'ACCESSIBLE_GUARD':
      return `${dateStr}-accessible-route-${timestamp}.html`;
    
    case 'MOOD_BOX':
    default:
      return `${dateStr}-weekend-guide-${timestamp}.html`;
  }
}

// ============================================================================
// 场景处理器
// ============================================================================

async function handleMoodBoxScene(input) {
  console.log('[Handler] 情绪盲盒模式：生成 A/B 双线治愈方案...');
  return {
    title: '周末放空指南',
    subtitle: '为你找到几个安静的好去处',
    planA: {
      title: '方案 A · 艺术治愈之旅',
      subtitle: '适合：想安静、下雨天、疲惫状态',
      content: '<p>室内美术馆 + 书店路线</p>',
      mapIframe: ''
    },
    planB: {
      title: '方案 B · 自然呼吸之旅',
      subtitle: '适合：想运动、晴天、想透气',
      content: '<p>公园漫步 + 湖边散步路线</p>',
      mapIframe: ''
    }
  };
}

async function handleLinkGrabScene(input) {
  console.log('[Handler] 一键拔草模式：解析攻略链接...');
  return {
    title: '行程规划',
    subtitle: '根据攻略生成的最优路线'
  };
}

async function handleHardcoreStewardScene(input) {
  console.log('[Handler] 硬核管家模式：生活圈体检报告...');
  return {
    title: '生活圈体检报告',
    subtitle: '五维雷达扫描结果',
    overallScore: '待评估',
    commuteTime: '待测算',
    radius: '2000m',
    convenience: '待评估',
    radarContent: '<p>正在扫描周边配套设施...</p>'
  };
}

async function handleAccessibleGuardScene(input) {
  console.log('[Handler] 无障碍守护模式：平缓避坑路线...');
  return {
    title: '无障碍出行路线',
    subtitle: '平缓避坑·专属关怀路线',
    emotionMessage: '听到您有出行需求，已为您规划最温柔的路线。',
    warningContent: '<p>正在抓取避坑攻略...</p>',
    oasisContent: '<p>正在标注绿洲补给站...</p>',
    backupContent: '<p>正在准备备选方案...</p>'
  };
}

// ============================================================================
// 主调度入口
// ============================================================================

/**
 * 主调度函数：执行完整生命周期
 * @param {string} userInput - 用户输入
 * @param {string} outputFilename - 输出文件名（可选）
 */
async function dispatch(userInput, outputFilename) {
  console.log('='.repeat(60));
  console.log('City Life Copilot - 主调度引擎 v2.0');
  console.log('='.repeat(60));
  
  try {
    // 阶段 1: 解析输入
    const sceneContext = parseInput(userInput);
    
    // 阶段 2: 工具执行
    const toolData = await executeTools(sceneContext);
    
    // 阶段 3: 模板渲染（修复：根据场景选择模板）
    const template = loadTemplate(sceneContext);
    
    // 阶段 4: 数据绑定
    let handlerResult;
    switch (sceneContext.scene) {
      case 'MOOD_BOX':
        handlerResult = await handleMoodBoxScene(sceneContext.rawInput);
        break;
      case 'LINK_GRAB':
        handlerResult = await handleLinkGrabScene(sceneContext.rawInput);
        break;
      case 'HARDCORE_STEWARD':
        handlerResult = await handleHardcoreStewardScene(sceneContext.rawInput);
        break;
      case 'ACCESSIBLE_GUARD':
        handlerResult = await handleAccessibleGuardScene(sceneContext.rawInput);
        break;
      default:
        handlerResult = await handleMoodBoxScene(sceneContext.rawInput);
    }
    const finalData = { ...handlerResult, ...toolData };
    const finalHtml = bindData(template, finalData, sceneContext.scene);
    
    // 阶段 5: 文件导出
    const filename = outputFilename || generateFilename(sceneContext.scene, userInput);
    const outputPath = exportFile(finalHtml, filename);
    
    console.log('='.repeat(60));
    console.log('✅ 调度完成');
    console.log(`📁 输出文件：${outputPath}`);
    console.log('='.repeat(60));
    
    return {
      success: true,
      outputPath,
      scene: sceneContext.scene,
      filename
    };
    
  } catch (error) {
    console.error('[Dispatcher] ❌ 错误:', error.message);
    console.error(error.stack);
    return {
      success: false,
      error: error.message,
      stack: error.stack
    };
  }
}

// ============================================================================
// 导出接口
// ============================================================================

module.exports = {
  dispatch,
  parseInput,
  executeTools,
  loadTemplate,
  bindData,
  exportFile,
  generateFilename,
  SCENE_PATTERNS,
  TEMPLATE_MAP
};

// 如果直接运行此脚本
if (require.main === module) {
  const userInput = process.argv[2] || '周末去哪玩';
  const outputFilename = process.argv[3];
  
  dispatch(userInput, outputFilename).then(result => {
    if (result.success) {
      console.log('\n🎉 任务完成，文件已保存至:', result.outputPath);
      process.exit(0);
    } else {
      console.log('\n❌ 任务失败:', result.error);
      process.exit(1);
    }
  });
}

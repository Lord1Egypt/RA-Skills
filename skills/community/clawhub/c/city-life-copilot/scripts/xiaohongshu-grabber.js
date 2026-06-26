#!/usr/bin/env node

/**
 * City Life Copilot - 小红书链接抓取器
 * 使用 agent-browser 绕过小红书反爬虫机制
 * 
 * 使用方法:
 * node scripts/xiaohongshu-grabber.js --url="https://www.xiaohongshu.com/..."
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================================
// 配置
// ============================================================================

const WORKSPACE_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace');
const OUTPUT_DIR = path.join(WORKSPACE_DIR, 'output');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// ============================================================================
// 命令行参数解析
// ============================================================================

function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  
  args.forEach(arg => {
    if (arg.startsWith('--url=')) {
      params.url = arg.substring(6);
    } else if (arg.startsWith('--output=')) {
      params.output = arg.substring(9);
    }
  });
  
  return params;
}

// ============================================================================
// 小红书内容提取规则
// ============================================================================

/**
 * 从小红书笔记 HTML 中提取地点信息
 * 注意：实际使用中需要通过 agent-browser 获取页面内容
 */
function extractLocationsFromContent(content) {
  const locations = [];
  
  // 常见地点标记模式
  const patterns = [
    /✅(.+?)(?:\n|$)/g,           // ✅ 标记的地点
    /📍(.+?)(?:\n|$)/g,           // 📍 标记的地点
    /➡️(.+?)(?:\n|$)/g,           // ➡️ 标记的路线
    /([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Za-z]{0,5}(?:市 | 区 | 县 | 路 | 街 | 道 | 寺 | 庙 | 公园 | 湖 | 山|桥|堤|塔))/g,  // 中国地名
  ];
  
  patterns.forEach((pattern, index) => {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      const location = match[1].trim();
      if (location.length > 1 && location.length < 50) {
        locations.push({
          name: location,
          source: `pattern-${index}`
        });
      }
    }
  });
  
  // 去重
  const unique = [];
  const seen = new Set();
  locations.forEach(loc => {
    if (!seen.has(loc.name)) {
      seen.add(loc.name);
      unique.push(loc);
    }
  });
  
  return unique;
}

/**
 * 从路线描述中提取有序地点列表
 */
function extractRouteOrder(content) {
  const routeLine = content.match(/👣游玩路线 [：:](.+?)(?:\n|$)/);
  if (routeLine) {
    const route = routeLine[1];
    // 按 ➡️ 分割
    const locations = route.split('➡️').map(s => s.trim()).filter(s => s.length > 0);
    return locations;
  }
  return [];
}

// ============================================================================
// 调用 agent-browser 抓取小红书
// ============================================================================

/**
 * 使用 agent-browser 抓取小红书笔记内容
 * @param {string} url - 小红书笔记 URL
 * @returns {string} - 提取的文本内容
 */
function grabXiaohongshuWithBrowser(url) {
  console.log('[Xiaohongshu Grabber] 使用 agent-browser 抓取小红书...');
  console.log(`[Xiaohongshu Grabber] URL: ${url}`);
  
  try {
    // 检查 agent-browser 是否可用
    const browserSkillPath = path.join(WORKSPACE_DIR, 'skills', 'agent-browser');
    if (!fs.existsSync(browserSkillPath)) {
      throw new Error('agent-browser 技能未安装，请先安装：skillhub install agent-browser');
    }
    
    // 注意：实际使用时需要通过 OpenClaw 的 browser 工具调用
    // 这里提供一个概念性实现框架
    console.log('[Xiaohongshu Grabber] ⚠️  需要通过 OpenClaw browser 工具执行抓取');
    console.log('[Xiaohongshu Grabber] 请在 dispatcher 中调用 browser 工具获取页面内容');
    
    // 返回一个示例内容（实际应由 browser 工具返回）
    return null;
    
  } catch (error) {
    console.error('[Xiaohongshu Grabber] 抓取失败:', error.message);
    throw error;
  }
}

// ============================================================================
// 备用方案：web-fetch（仅用于非反爬虫网站）
// ============================================================================

/**
 * 使用 web-fetch 抓取普通网页（不推荐用于小红书）
 * @param {string} url - 网页 URL
 * @returns {string} - 提取的文本内容
 */
function grabWithWebFetch(url) {
  console.log('[Xiaohongshu Grabber] 尝试使用 web-fetch 抓取...');
  console.log('[Xiaohongshu Grabber] ⚠️  警告：小红书等平台会返回 error_code=300012 (IP at risk)');
  
  try {
    // 检查是否是强反爬虫网站
    const blockedDomains = [
      'xiaohongshu.com',
      'douyin.com',
      'tiktok.com',
      'instagram.com'
    ];
    
    const isBlocked = blockedDomains.some(domain => url.includes(domain));
    if (isBlocked) {
      console.error('[Xiaohongshu Grabber] ❌ 此网站有强反爬虫机制，web-fetch 会被拦截');
      console.error('[Xiaohongshu Grabber] 请使用 agent-browser 代替');
      throw new Error('网站有反爬虫机制，请使用 agent-browser');
    }
    
    // 实际调用 web-fetch
    // 注意：这里需要通过 OpenClaw 的 web_fetch 工具执行
    console.log('[Xiaohongshu Grabber] 请在 dispatcher 中调用 web_fetch 工具获取页面内容');
    
    return null;
    
  } catch (error) {
    console.error('[Xiaohongshu Grabber] web-fetch 失败:', error.message);
    throw error;
  }
}

// ============================================================================
// 主函数
// ============================================================================

async function main() {
  const params = parseArgs();
  
  if (!params.url) {
    console.log('使用方法:');
    console.log('  node scripts/xiaohongshu-grabber.js --url="https://www.xiaohongshu.com/..."');
    console.log('');
    console.log('注意:');
    console.log('  - 小红书链接必须使用 agent-browser 抓取');
    console.log('  - web-fetch 会被反爬虫机制拦截 (error_code=300012)');
    process.exit(1);
  }
  
  console.log('='.repeat(60));
  console.log('City Life Copilot - 小红书链接抓取器');
  console.log('='.repeat(60));
  
  const isXiaohongshu = params.url.includes('xiaohongshu.com');
  
  if (isXiaohongshu) {
    console.log('[Xiaohongshu Grabber] 检测到小红书链接，使用 agent-browser 模式');
    const content = grabXiaohongshuWithBrowser(params.url);
    
    if (content) {
      const locations = extractLocationsFromContent(content);
      const routeOrder = extractRouteOrder(content);
      
      console.log('\n📍 提取到的地点:');
      locations.forEach((loc, i) => {
        console.log(`  ${i + 1}. ${loc.name}`);
      });
      
      if (routeOrder.length > 0) {
        console.log('\n👣 推荐游览顺序:');
        routeOrder.forEach((loc, i) => {
          console.log(`  ${i + 1}. ${loc}`);
        });
      }
      
      // 输出 JSON 结果
      const outputPath = params.output || path.join(OUTPUT_DIR, `xiaohongshu-${Date.now()}.json`);
      const result = {
        url: params.url,
        locations,
        routeOrder,
        rawContent: content
      };
      
      fs.writeFileSync(outputPath, JSON.stringify(result, null, 2), 'utf-8');
      console.log(`\n✅ 结果已保存至：${outputPath}`);
    }
  } else {
    console.log('[Xiaohongshu Grabber] 普通链接，使用 web-fetch 模式');
    grabWithWebFetch(params.url);
  }
  
  console.log('='.repeat(60));
}

// 导出接口
module.exports = {
  grabXiaohongshuWithBrowser,
  grabWithWebFetch,
  extractLocationsFromContent,
  extractRouteOrder
};

// 如果直接运行此脚本
if (require.main === module) {
  main().catch(error => {
    console.error('[Xiaohongshu Grabber] 错误:', error.message);
    process.exit(1);
  });
}

#!/usr/bin/env node
/**
 * 小红书自动发布脚本
 * 支持命令行参数和程序化调用
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// 默认配置
const DEFAULT_CONFIG = {
  mcpUrl: 'http://localhost:18060/mcp',
  post: {
    title: '',
    content: '',
    images: [],
    tags: []
  }
};

let requestId = 1;
let sessionId = null;

/**
 * 发送 HTTP 请求到 MCP 服务端
 */
function sendRequest(data) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 18060,
      path: '/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
      }
    };

    if (sessionId) {
      options.headers['Mcp-Session-Id'] = sessionId;
    }

    const req = http.request(options, (res) => {
      const newSessionId = res.headers['mcp-session-id'];
      if (newSessionId) {
        sessionId = newSessionId;
      }

      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          resolve(responseData);
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(data));
    req.end();
  });
}

/**
 * 初始化 MCP 会话
 */
async function initializeSession() {
  const result = await sendRequest({
    jsonrpc: '2.0',
    id: requestId++,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: { tools: {} },
      clientInfo: { name: 'xiaohongshu-publisher', version: '1.0.0' }
    }
  });

  if (result.error) {
    throw new Error(`初始化失败: ${result.error.message}`);
  }

  // 发送 initialized 通知
  await sendRequest({
    jsonrpc: '2.0',
    method: 'notifications/initialized'
  });

  return true;
}

/**
 * 检查登录状态
 */
async function checkLoginStatus() {
  const result = await sendRequest({
    jsonrpc: '2.0',
    id: requestId++,
    method: 'tools/call',
    params: {
      name: 'check_login_status',
      arguments: {}
    }
  });

  if (result.error) {
    throw new Error(`检查登录状态失败: ${result.error.message}`);
  }

  const text = result.result?.content?.[0]?.text || '';
  return text.includes('已登录');
}

/**
 * 发布内容到小红书
 */
async function publishContent(config) {
  // 验证图片存在
  for (const imagePath of config.images) {
    if (!fs.existsSync(imagePath)) {
      throw new Error(`图片不存在: ${imagePath}`);
    }
  }

  const result = await sendRequest({
    jsonrpc: '2.0',
    id: requestId++,
    method: 'tools/call',
    params: {
      name: 'publish_content',
      arguments: {
        title: config.title,
        content: config.content,
        images: config.images,
        tags: config.tags || []
      }
    }
  });

  if (result.error) {
    throw new Error(`发布失败: ${result.error.message}`);
  }

  return result.result;
}

/**
 * 主发布函数
 */
async function publish(config = {}) {
  try {
    console.log('🚀 小红书自动发布\n');
    console.log('='.repeat(50));

    // 合并配置
    const finalConfig = {
      ...DEFAULT_CONFIG.post,
      ...config
    };

    // 显示发布内容
    console.log('\n📋 发布内容:');
    console.log(`  标题: ${finalConfig.title}`);
    console.log(`  图片: ${finalConfig.images.length} 张`);
    console.log(`  标签: ${(finalConfig.tags || []).join(', ')}`);

    // 1. 初始化
    console.log('\n1️⃣  初始化 MCP 会话...');
    await initializeSession();
    console.log('✅ 初始化成功');

    // 2. 检查登录
    console.log('\n2️⃣  检查登录状态...');
    const isLoggedIn = await checkLoginStatus();
    if (!isLoggedIn) {
      console.log('❌ 未登录小红书，请先登录');
      return { success: false, error: '未登录' };
    }
    console.log('✅ 已登录');

    // 3. 发布
    console.log('\n3️⃣  发布内容...');
    const result = await publishContent(finalConfig);
    console.log('\n✅ 发布成功!');

    if (result.content) {
      result.content.forEach(item => {
        if (item.type === 'text') {
          console.log(`  📱 ${item.text}`);
        }
      });
    }

    console.log('\n' + '='.repeat(50));
    console.log('🎉 发布完成!');

    return { success: true, result };

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const config = { ...DEFAULT_CONFIG.post };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '--title':
      case '-t':
        config.title = args[++i];
        break;
      case '--content':
      case '-c':
        config.content = args[++i];
        break;
      case '--image':
      case '-i':
        config.images = [args[++i]];
        break;
      case '--images':
        config.images = args[++i].split(',');
        break;
      case '--tags':
        config.tags = args[++i].split(',');
        break;
      case '--check':
        config._checkOnly = true;
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
    }
  }

  return config;
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
小红书自动发布工具

用法:
  node publish.js [选项]

选项:
  -t, --title <标题>      发布标题（必填）
  -c, --content <内容>    发布内容（必填）
  -i, --image <路径>      图片路径（必填）
  --images <路径1,路径2>  多张图片（逗号分隔）
  --tags <标签1,标签2>    标签（逗号分隔）
  --check                 仅检查登录状态
  -h, --help              显示帮助

示例:
  node publish.js -t "我的标题" -c "我的内容" -i "C:\\image.jpg" --tags "生活,日常"
`);
}

/**
 * 仅检查登录状态
 */
async function checkOnly() {
  try {
    console.log('🔍 检查登录状态\n');
    await initializeSession();
    const isLoggedIn = await checkLoginStatus();
    
    if (isLoggedIn) {
      console.log('✅ 已登录小红书');
    } else {
      console.log('❌ 未登录');
    }
    
    process.exit(isLoggedIn ? 0 : 1);
  } catch (error) {
    console.error('❌ 检查失败:', error.message);
    process.exit(1);
  }
}

// 主入口
if (require.main === module) {
  const config = parseArgs();
  
  if (config._checkOnly) {
    checkOnly();
  } else {
    // 验证必填项
    if (!config.title || !config.content || config.images.length === 0) {
      console.error('❌ 缺少必填参数: title, content, image');
      showHelp();
      process.exit(1);
    }
    
    publish(config);
  }
}

// 导出模块
module.exports = { publish, checkLoginStatus, initializeSession };

const { applySessionData } = require('./scripts/browser-session-manager.js');

/**
 * 示例：使用即梦 (Jimeng) 会话数据访问网站
 * 
 * 使用方法:
 * 1. 确保你已经保存了会话 JSON 文件
 * 2. 修改下面的路径和 URL
 * 3. 运行: node examples/use-jimeng-session.js
 */

async function main() {
  try {
    console.log('🌐 使用浏览器会话数据访问即梦...\n');
    
    // 配置
    const config = {
      // 目标 URL
      url: 'https://jimeng.jianying.com/ai-tool/home?type=video',
      
      // 会话 JSON 文件路径 (替换为你的实际路径)
      sessionJsonPath: process.argv[2] || '/tmp/jimeng-session.json',
      
      // 选项
      options: {
        headless: true,                    // 无头模式
        screenshotPath: '/tmp/jimeng-result.png',  // 截图保存路径
        waitTime: 5000,                    // 等待时间 (毫秒)
        
        // 可选：执行额外动作
        actions: [
          // { type: 'click', selector: 'button.generate' },
          // { type: 'wait', time: 3000 },
          // { type: 'screenshot', path: '/tmp/after-click.png' }
        ]
      }
    };
    
    console.log(`🔗 目标 URL: ${config.url}`);
    console.log(`📄 会话文件: ${config.sessionJsonPath}`);
    console.log('');
    
    // 执行
    const result = await applySessionData(
      config.url,
      config.sessionJsonPath,
      config.options
    );
    
    console.log('\n✅ 访问成功!');
    console.log(`📊 页面标题: ${result.title}`);
    console.log(`📍 最终 URL: ${result.url}`);
    console.log(`🍪 Cookies 数量: ${result.cookies.length}`);
    console.log(`💾 localStorage 项数: ${Object.keys(result.localStorage).length}`);
    console.log(`📦 sessionStorage 项数: ${Object.keys(result.sessionStorage).length}`);
    
    if (config.options.screenshotPath) {
      console.log(`\n📸 截图已保存: ${config.options.screenshotPath}`);
    }
    
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    console.error('堆栈:', error.stack);
    process.exit(1);
  }
}

// 运行
main();
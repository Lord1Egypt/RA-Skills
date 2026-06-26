/**
 * Agent Kanban 配置文件
 * 
 * 使用方法：
 * 1. 复制此文件为 config.local.js
 * 2. 修改 config.local.js 中的配置
 * 3. config.local.js 会被自动加载（优先于 config.js）
 * 
 * Gateway Token 获取方法：
 * 
 * 方法一：从 openclaw.json 获取
 *   cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'
 * 
 * 方法二：从 CLI 获取
 *   openclaw gateway status
 * 
 * 方法三：从 Web UI 获取
 *   打开 http://localhost:18790 → Settings → API Tokens
 * 
 * 前置条件：
 *   Gateway 必须先启动：openclaw gateway start
 */

module.exports = {
  // 服务配置
  server: {
    port: 3100,
    host: '0.0.0.0'
  },
  
  // Gateway HTTP API 配置
  // 从 openclaw.json 获取：cat ~/.openclaw/openclaw.json | jq '.gateway.auth.token'
  gateway: {
    url: 'http://127.0.0.1:18789',
    token: 'c80aa67f773b3045792ba7afbf2e22fc09cb7b37c63019e3'
  },
  
  // OpenClaw 配置
  openclaw: {
    homeDir: '.openclaw',  // 相对于用户主目录，或绝对路径
    configFilename: 'openclaw.json'
  },
  
  // 刷新间隔（毫秒）
  refreshInterval: 60000,
  
  // Session 文件大小阈值（KB）
  sessionSizeThresholds: {
    warning: 500,   // 黄色警告
    danger: 1024    // 红色危险
  }
};
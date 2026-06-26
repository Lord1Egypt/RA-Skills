/**
 * 启动 OpenClaw 游戏桥接服务
 * 
 * 使用方式：
 * 1. 启动游戏服务器 (server_localhost.js)
 * 2. 运行此脚本: node start_game_bridge.js
 * 3. 玩家点击"托管"按钮，客户端会自动连接
 */

const OpenClawGameBridge = require('./OpenClawGameBridge');

console.log('========================================');
console.log('   OpenClaw 游戏桥接服务');
console.log('========================================\n');

// 创建桥接服务（端口18765）
const bridge = new OpenClawGameBridge(18765);

console.log('\n服务信息:');
console.log('  WebSocket: ws://localhost:18765');
console.log('  HTTP API:  http://localhost:18766');
console.log('');
console.log('HTTP API 端点:');
console.log('  GET  /health                       - 健康检查');
console.log('  GET  /clients                      - 已连接游戏客户端列表');
console.log('  GET  /clients/:playerUid/perception - 查询感知缓存');
console.log('  GET  /clients/:playerUid/mapInfo   - 查询地图信息');
console.log('  GET  /mapId/:mapId/transportPoints - 查询传送门缓存');
console.log('  POST /command                      - 发送控制指令 {playerUid, command}');
console.log('  POST /perception/request           - 请求感知推送 {playerUid, category}');
console.log('');

console.log('\n连接流程:');
console.log('  1. 玩家点击"托管"按钮');
console.log('  2. 客户端AIController连接到此服务');
console.log('  3. 客户端发送 ai_register 消息');
console.log('  4. 此服务保存连接');

console.log('\nAPI接口:');
console.log('  bridge.setAIMode(playerUid, enabled)  - 设置AI模式');
console.log('  bridge.sendCommand(playerUid, command) - 发送控制指令');
console.log('  bridge.requestSync(playerUid)          - 请求同步数据');
console.log('  bridge.getStatus()                     - 获取状态');

console.log('\n示例:');
console.log("  bridge.setAIMode('player_001', true)  // 开启player_001的AI模式");
console.log("  bridge.sendCommand('player_001', { type: 'move', x: 200, y: 300 })");
console.log("  bridge.sendCommand('player_001', { type: 'chat', message: '大家好！' })");
console.log("  bridge.setAIMode('player_001', false) // 关闭AI模式");

console.log('\n按 Ctrl+C 停止服务\n');

// 处理退出
process.on('SIGINT', () => {
    console.log('\n正在停止服务...');
    bridge.stop();
    process.exit(0);
});

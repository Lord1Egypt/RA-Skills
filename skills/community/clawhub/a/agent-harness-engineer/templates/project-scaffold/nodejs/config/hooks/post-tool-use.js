/**
 * Post-tool-use Hook示例
 * 
 * 在工具执行后运行，可用于：
 * - 结果审计
 * - 数据收集
 * - 副作用处理
 * - 通知发送
 */

function postToolUse(toolName, toolInput, toolOutput) {
  console.log(`[Hook] Post-tool-use: ${toolName}`);
  console.log(`[Hook] Output length:`, toolOutput.length);
  
  // 示例：记录审计日志
  const fs = require('fs');
  const path = require('path');
  
  const auditLog = {
    timestamp: new Date().toISOString(),
    tool: toolName,
    input: toolInput,
    outputLength: toolOutput.length
  };
  
  const logDir = path.join(process.cwd(), 'logs');
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  fs.appendFileSync(
    path.join(logDir, 'audit.log'),
    JSON.stringify(auditLog) + '\n'
  );
  
  return toolOutput;
}

module.exports = { postToolUse };

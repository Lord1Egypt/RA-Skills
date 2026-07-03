/**
 * Pre-tool-use Hook示例
 * 
 * 在工具执行前运行，可用于：
 * - 权限检查
 * - 参数验证
 * - 审计日志
 * - 动态审批
 */

function preToolUse(toolName, toolInput) {
  console.log(`[Hook] Pre-tool-use: ${toolName}`);
  console.log(`[Hook] Input:`, toolInput);
  
  // 示例：阻止危险命令
  if (toolName === "bash") {
    const command = toolInput.command || "";
    const dangerousPatterns = ["rm -rf", "sudo", "dd if="];
    for (const pattern of dangerousPatterns) {
      if (command.includes(pattern)) {
        throw new Error(`Dangerous command detected: ${command}`);
      }
    }
  }
  
  return toolInput;
}

module.exports = { preToolUse };

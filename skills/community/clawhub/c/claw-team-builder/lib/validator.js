/**
 * Validator - 配置验证工具
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * 验证目录是否可创建
 */
function validateDirectory(dirPath) {
  const errors = [];

  // 检查父目录是否存在
  const parentDir = path.dirname(dirPath);
  if (!fs.existsSync(parentDir)) {
    errors.push(`父目录不存在: ${parentDir}`);
  }

  // 检查目录是否已存在（作为文件）
  if (fs.existsSync(dirPath) && !fs.statSync(dirPath).isDirectory()) {
    errors.push(`路径已存在但不是目录: ${dirPath}`);
  }

  return { valid: errors.length === 0, errors };
}

/**
 * 创建目录结构
 */
function createDirectoryStructure(agentId, baseDir = process.env.HOME + '/.openclaw') {
  const dirs = {
    workspace: path.join(baseDir, `workspace-${agentId}`),
    agentDir: path.join(baseDir, 'agents', agentId, 'agent'),
    sessionsDir: path.join(baseDir, 'agents', agentId, 'sessions'),
    memoryDir: path.join(baseDir, `workspace-${agentId}`, 'memory')
  };

  Object.entries(dirs).forEach(([name, dir]) => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });

  return dirs;
}

/**
 * 运行 OpenClaw doctor 验证配置
 */
function runDoctor() {
  try {
    const result = execSync('openclaw doctor --fix 2>&1', {
      encoding: 'utf-8',
      timeout: 60000
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * 重启 Gateway
 */
function restartGateway() {
  try {
    execSync('openclaw gateway restart 2>&1', {
      encoding: 'utf-8',
      timeout: 30000
    });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * 验证配置完整性
 */
function validateAgentConfig(config, agentId) {
  const errors = [];

  // 检查 Agent 是否在列表中
  const agent = config.agents?.list?.find(a => a.id === agentId);
  if (!agent) {
    errors.push(`Agent "${agentId}" 不在 agents.list 中`);
  }

  // 检查工作空间
  if (agent?.workspace && !fs.existsSync(agent.workspace)) {
    errors.push(`工作空间目录不存在: ${agent.workspace}`);
  }

  // 检查是否有对应的 binding
  const binding = config.bindings?.find(b => b.agentId === agentId);
  if (!binding) {
    // 这不是错误，只是警告
    console.log(`提示: Agent "${agentId}" 没有配置 binding`);
  }

  return { valid: errors.length === 0, errors };
}

module.exports = {
  validateDirectory,
  createDirectoryStructure,
  runDoctor,
  restartGateway,
  validateAgentConfig
};
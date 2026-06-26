/**
 * Config Builder - 构建 OpenClaw Agent 配置
 */

const fs = require('fs');
const path = require('path');

const OPENCLAW_CONFIG_PATH = process.env.OPENCLAW_CONFIG_PATH ||
  path.join(process.env.HOME, '.openclaw', 'openclaw.json');

/**
 * 读取现有配置
 */
function readConfig() {
  try {
    const content = fs.readFileSync(OPENCLAW_CONFIG_PATH, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    throw new Error(`无法读取配置文件: ${error.message}`);
  }
}

/**
 * 保存配置（自动备份）
 */
function saveConfig(config, backup = true) {
  if (backup) {
    const backupPath = `${OPENCLAW_CONFIG_PATH}.bak`;
    fs.copyFileSync(OPENCLAW_CONFIG_PATH, backupPath);
  }
  fs.writeFileSync(OPENCLAW_CONFIG_PATH, JSON.stringify(config, null, 2));
}

/**
 * 分析现有配置
 */
function analyzeConfig(config) {
  const analysis = {
    // 现有 Agent ID 列表
    existingAgentIds: [],
    // 现有工作空间路径
    existingWorkspaces: [],
    // 现有 Agent 目录
    existingAgentDirs: [],
    // Channel 账户使用情况
    channelAccounts: {},
    // Bindings 映射
    bindingsMap: [],
    // 可用模型
    availableModels: [],
    // 默认模型
    defaultModel: null,
    // 默认工作空间
    defaultWorkspace: null,
  };

  // 分析 agents
  if (config.agents?.list) {
    config.agents.list.forEach(agent => {
      analysis.existingAgentIds.push(agent.id);
      if (agent.workspace) analysis.existingWorkspaces.push(agent.workspace);
      if (agent.agentDir) analysis.existingAgentDirs.push(agent.agentDir);
    });
  }

  // 默认设置
  if (config.agents?.defaults) {
    analysis.defaultModel = config.agents.defaults.model?.primary;
    analysis.defaultWorkspace = config.agents.defaults.workspace;
  }

  // 分析 channels
  if (config.channels) {
    Object.entries(config.channels).forEach(([channelType, channelConfig]) => {
      if (channelConfig.accounts) {
        Object.keys(channelConfig.accounts).forEach(accountId => {
          analysis.channelAccounts[`${channelType}:${accountId}`] = true;
        });
      }
    });
  }

  // 分析 bindings
  if (config.bindings) {
    config.bindings.forEach(binding => {
      analysis.bindingsMap.push({
        agentId: binding.agentId,
        channel: binding.match?.channel,
        accountId: binding.match?.accountId
      });
    });
  }

  // 分析可用模型
  if (config.models?.providers) {
    Object.entries(config.models.providers).forEach(([provider, providerConfig]) => {
      if (providerConfig.models) {
        providerConfig.models.forEach(model => {
          analysis.availableModels.push(`${provider}/${model.id}`);
        });
      }
    });
  }

  return analysis;
}

/**
 * 检测冲突
 */
function detectConflicts(newAgent, analysis) {
  const conflicts = [];

  // Agent ID 冲突
  if (analysis.existingAgentIds.includes(newAgent.id)) {
    conflicts.push({
      type: 'agent_id_duplicate',
      field: 'id',
      message: `Agent ID "${newAgent.id}" 已存在`,
      severity: 'error'
    });
  }

  // 工作空间冲突
  if (analysis.existingWorkspaces.includes(newAgent.workspace)) {
    conflicts.push({
      type: 'workspace_duplicate',
      field: 'workspace',
      message: `工作空间 "${newAgent.workspace}" 已被其他 Agent 使用`,
      severity: 'error'
    });
  }

  // Agent 目录冲突
  if (newAgent.agentDir && analysis.existingAgentDirs.includes(newAgent.agentDir)) {
    conflicts.push({
      type: 'agent_dir_duplicate',
      field: 'agentDir',
      message: `Agent 目录 "${newAgent.agentDir}" 已被使用`,
      severity: 'error'
    });
  }

  // Channel 账户冲突（如果指定了 channel）
  if (newAgent.channelType && newAgent.channelAccount) {
    const accountKey = `${newAgent.channelType}:${newAgent.channelAccount}`;
    const existingBinding = analysis.bindingsMap.find(
      b => b.channel === newAgent.channelType && b.accountId === newAgent.channelAccount
    );
    if (existingBinding) {
      conflicts.push({
        type: 'channel_account_bound',
        field: 'channelAccount',
        message: `Channel 账户 "${newAgent.channelAccount}" 已绑定到 Agent "${existingBinding.agentId}"`,
        severity: 'warning'
      });
    }
  }

  return conflicts;
}

/**
 * 构建 Agent 配置片段
 */
function buildAgentConfig(newAgent, analysis) {
  const workspace = newAgent.workspace ||
    path.join(process.env.HOME, '.openclaw', `workspace-${newAgent.id}`);

  const agentDir = newAgent.agentDir ||
    path.join(process.env.HOME, '.openclaw', 'agents', newAgent.id, 'agent');

  const model = newAgent.model || analysis.defaultModel;

  return {
    id: newAgent.id,
    name: newAgent.name || newAgent.id,
    workspace,
    agentDir,
    model
  };
}

/**
 * 构建 Channel 账户配置
 */
function buildChannelAccountConfig(newAgent) {
  if (!newAgent.channelType || !newAgent.appId) {
    return null;
  }

  return {
    appId: newAgent.appId,
    appSecret: newAgent.appSecret,
    botName: newAgent.botName || newAgent.name,
    enabled: true,
    dmPolicy: newAgent.dmPolicy || 'open',
    groupPolicy: newAgent.groupPolicy || 'open',
    allowFrom: newAgent.allowFrom || ['*']
  };
}

/**
 * 构建 Binding 配置
 */
function buildBindingConfig(newAgent) {
  if (!newAgent.channelType || !newAgent.channelAccount) {
    return null;
  }

  return {
    agentId: newAgent.id,
    match: {
      channel: newAgent.channelType,
      accountId: newAgent.channelAccount
    }
  };
}

/**
 * 合并配置
 */
function mergeConfig(existingConfig, newAgent) {
  const analysis = analyzeConfig(existingConfig);
  const conflicts = detectConflicts(newAgent, analysis);

  // 只检查 error 级别的冲突
  const errors = conflicts.filter(c => c.severity === 'error');
  if (errors.length > 0) {
    return { success: false, conflicts: errors };
  }

  const config = JSON.parse(JSON.stringify(existingConfig));

  // 1. 添加 Agent
  const agentConfig = buildAgentConfig(newAgent, analysis);
  config.agents.list.push(agentConfig);

  // 2. 添加 Channel 账户（如需要）
  if (newAgent.channelType && newAgent.channelAccount && newAgent.appId) {
    if (!config.channels[newAgent.channelType]) {
      config.channels[newAgent.channelType] = {
        enabled: true,
        accounts: {}
      };
    }
    if (!config.channels[newAgent.channelType].accounts) {
      config.channels[newAgent.channelType].accounts = {};
    }
    config.channels[newAgent.channelType].accounts[newAgent.channelAccount] =
      buildChannelAccountConfig(newAgent);
  }

  // 3. 添加 Binding
  const bindingConfig = buildBindingConfig(newAgent);
  if (bindingConfig) {
    config.bindings.push(bindingConfig);
  }

  return { success: true, config, agentConfig, bindingConfig, warnings: conflicts.filter(c => c.severity === 'warning') };
}

module.exports = {
  readConfig,
  saveConfig,
  analyzeConfig,
  detectConflicts,
  buildAgentConfig,
  buildChannelAccountConfig,
  buildBindingConfig,
  mergeConfig,
  OPENCLAW_CONFIG_PATH
};
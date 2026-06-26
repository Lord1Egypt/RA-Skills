/**
 * 配置验证工具
 */

// 验证 App ID 格式
function validateAppId(appId) {
  return /^cli_[a-zA-Z0-9]+$/.test(appId);
}

// 验证账户 ID 格式
function validateAccountId(id) {
  return /^[a-z0-9-]+$/.test(id);
}

// 验证群聊 ID 格式
function validateChatId(id) {
  return /^oc_[a-zA-Z0-9]+$/.test(id);
}

// 验证用户 ID 格式
function validateUserId(id) {
  return /^ou_[a-zA-Z0-9]+$/.test(id);
}

// 验证完整配置
function validateConfig(config) {
  const errors = [];
  
  if (!config.channels?.feishu) {
    errors.push('缺少 channels.feishu 配置');
    return errors;
  }
  
  const accounts = config.channels.feishu.accounts || {};
  
  for (const [key, acc] of Object.entries(accounts)) {
    if (!validateAccountId(key)) {
      errors.push(`账户 ID "${key}" 格式无效`);
    }
    if (!validateAppId(acc.appId)) {
      errors.push(`[${key}] App ID 格式无效: ${acc.appId}`);
    }
    if (!acc.appSecret) {
      errors.push(`[${key}] App Secret 不能为空`);
    }
  }
  
  // 验证 bindings
  const bindings = config.bindings || [];
  for (const binding of bindings) {
    if (!binding.agentId) {
      errors.push('存在缺少 agentId 的 binding');
    }
    if (!binding.match?.peer?.id) {
      errors.push('存在缺少 peer.id 的 binding');
    }
  }
  
  return errors;
}

module.exports = {
  validateAppId,
  validateAccountId,
  validateChatId,
  validateUserId,
  validateConfig
};

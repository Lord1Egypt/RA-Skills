/**
 * Action 2: post_summary
 * 在社区广场发布 AI 视角的任务总结帖子
 */

const { getConfig, validateConfig } = require('./config');
const logger = require('./logger');
const { validateSafe } = require('./piiFilter');
const { fetchWithRetry } = require('./utils');

/**
 * 发布帖子到社区广场
 * @param {string} communityUrl - 社区 API 地址
 * @param {string} apiKey - API key
 * @param {object} postData - 帖子数据
 */
async function publishPost(communityUrl, apiKey, postData) {
  const response = await fetchWithRetry(
    `${communityUrl}/api/posts`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(postData)
    },
    2, // 最多重试 2 次
    2000,
    5000 // 5 秒超时
  );

  if (response.status === 401) {
    logger.error('Authentication failed. Please check your API key.');
    throw new Error('Unauthorized: Invalid API key');
  }

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }

  return response.json();
}

/**
 * 验证 summary 内容
 * @param {string} summary - 总结内容
 * @returns {{valid: boolean, error?: string}}
 */
function validateSummary(summary) {
  if (!summary || typeof summary !== 'string') {
    return { valid: false, error: 'Summary is required and must be a string' };
  }

  // 字数检查（100-300 字）
  // 使用 Array.from 正确处理 Unicode 字符
  const charCount = Array.from(summary).length;

  if (charCount < 50) {
    return { valid: false, error: `Summary too short (${charCount} chars), minimum 100 recommended` };
  }

  if (charCount > 500) {
    return { valid: false, error: `Summary too long (${charCount} chars), maximum 300 recommended` };
  }

  return { valid: true };
}

/**
 * 执行 post_summary
 * @param {object} params - 输入参数
 * @param {string} params.task_type - 任务类型标签
 * @param {string} params.model_name - 模型名称（运行时读取）
 * @param {string} params.agent_name - Agent 名称
 * @param {string} params.summary - 任务总结内容
 * @param {object} context - OpenClaw 执行上下文
 * @returns {Promise<{success: boolean, post_id?: string, error?: string}>}
 */
async function execute(params, context = {}) {
  const {
    task_type,
    model_name,
    agent_name: paramAgentName,
    summary
  } = params;

  // 读取配置
  const config = getConfig();

  try {
    validateConfig(config);
  } catch (error) {
    logger.error(error.message);
    return { success: false, error: error.message };
  }

  // 确定 agent_name
  const agentName = paramAgentName
    || config.agentName
    || context.agent_name
    || 'Anonymous Agent';

  // 确定 model_name（优先使用传入的，否则尝试从 context 读取）
  const currentModel = model_name
    || context.model_name
    || context.current_model
    || process.env.OPENCLAW_CURRENT_MODEL
    || 'unknown';

  // 步骤 1：验证 summary 格式
  const validation = validateSummary(summary);
  if (!validation.valid) {
    logger.warn('Summary validation failed:', validation.error);
    return { success: false, error: validation.error };
  }

  // 步骤 2：PII 过滤
  const piiCheck = validateSafe(summary);
  if (!piiCheck.safe) {
    logger.warn('PII detected in summary, aborting post:', piiCheck.reason);
    return {
      success: false,
      error: `PII detected: ${piiCheck.reason}. Post aborted for privacy protection.`
    };
  }

  // 步骤 3：发布帖子
  const postData = {
    author_type: 'ai',
    author_name: agentName,
    model_name: currentModel,
    content: summary,
    task_type: task_type || '任务执行'
  };

  logger.debug('Publishing post with data:', {
    ...postData,
    content: postData.content.substring(0, 50) + '...'
  });

  try {
    const result = await publishPost(config.communityUrl, config.apiKey, postData);

    const postId = result.id || result.post_id || result._id;
    logger.info('Post published successfully, ID:', postId);

    return {
      success: true,
      post_id: postId,
      url: result.url || `${config.communityUrl}/posts/${postId}`
    };
  } catch (error) {
    logger.error('Failed to publish post:', error.message);
    return { success: false, error: error.message };
  }
}

module.exports = {
  execute,
  publishPost,
  validateSummary
};

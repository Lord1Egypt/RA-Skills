/**
 * Action 1: report_task
 * 向社区 API 上报任务元数据
 */

const { getConfig, validateConfig } = require('./config');
const logger = require('./logger');
const { fetchWithRetry, extractAgentId } = require('./utils');
const resolveTaskType = require('./resolveTaskType');

/**
 * 同步当前底座模型名称
 * @param {string} communityUrl - 社区 API 地址
 * @param {string} apiKey - API key
 * @param {string} modelName - 当前模型名称
 */
async function syncModelName(communityUrl, apiKey, modelName) {
  try {
    const response = await fetchWithRetry(
      `${communityUrl}/api/agents/me/model`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ model_name: modelName })
      },
      1, // 最多重试 1 次
      2000,
      3000 // 3 秒超时
    );

    if (!response.ok) {
      logger.debug(`Failed to sync model name: HTTP ${response.status}`);
      return false;
    }

    logger.debug(`Successfully synced model name: ${modelName}`);
    return true;
  } catch (error) {
    // 静默跳过，不影响后续步骤
    logger.debug('Failed to sync model name:', error.message);
    return false;
  }
}

/**
 * 上报任务元数据
 * @param {string} communityUrl - 社区 API 地址
 * @param {string} apiKey - API key
 * @param {object} taskData - 任务数据
 */
async function reportTaskData(communityUrl, apiKey, taskData) {
  const response = await fetchWithRetry(
    `${communityUrl}/api/report-task`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(taskData)
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

  return response;
}

/**
 * 执行 report_task
 * @param {object} params - 输入参数
 * @param {string} params.task_description - 任务描述
 * @param {string[]} params.skills_used - 使用的技能列表
 * @param {'success'|'failed'} params.status - 任务状态
 * @param {object} context - OpenClaw 执行上下文
 * @returns {Promise<{success: boolean, error?: string}>}
 */
async function execute(params, context = {}) {
  const { task_description, skills_used = [], status } = params;

  // 读取配置
  const config = getConfig();

  try {
    validateConfig(config);
  } catch (error) {
    logger.error(error.message);
    return { success: false, error: error.message };
  }

  // 步骤 1：调用 resolve_task_type
  let taskType;
  try {
    taskType = await resolveTaskType.execute({ task_description }, context);
  } catch (error) {
    logger.warn('Failed to resolve task type:', error.message);
    taskType = '任务执行';
  }

  // 步骤 2：从运行时上下文读取当前模型名称
  // 优先从 context 中读取，这是运行时动态值
  const currentModel = context.model_name
    || context.current_model
    || process.env.OPENCLAW_CURRENT_MODEL
    || 'unknown';

  logger.debug('Current model from runtime:', currentModel);

  // 同步模型名称（非阻塞，失败静默跳过）
  await syncModelName(config.communityUrl, config.apiKey, currentModel);

  // 步骤 3：上报任务元数据
  const agentId = extractAgentId(config.apiKey);

  const taskData = {
    task_type: taskType,
    skills_used: Array.isArray(skills_used) ? skills_used : [],
    status: status === 'failed' ? 'failed' : 'success',
    agent_id: agentId
  };

  logger.debug('Reporting task data:', {
    ...taskData,
    agent_id: '***'
  });

  try {
    await reportTaskData(config.communityUrl, config.apiKey, taskData);
    logger.info('Task reported successfully');
    return { success: true, task_type: taskType };
  } catch (error) {
    // 非阻塞：记录日志但不中断主流程
    logger.warn('Failed to report task:', error.message);
    return { success: false, error: error.message, task_type: taskType };
  }
}

module.exports = {
  execute,
  syncModelName,
  reportTaskData
};

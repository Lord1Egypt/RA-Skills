/**
 * Action 0: resolve_task_type
 * 确定最合适的 task_type 标签
 */

const { getConfig } = require('./config');
const logger = require('./logger');
const { fetchWithRetry, generateTaskTypeLabel } = require('./utils');

/**
 * 从社区获取现有标签列表
 * @returns {Promise<string[]>} 标签列表，失败返回空数组
 */
async function fetchExistingTags(communityUrl, apiKey) {
  try {
    const response = await fetchWithRetry(
      `${communityUrl}/api/tasks/types`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Accept': 'application/json'
        }
      },
      1, // 最多重试 1 次
      2000,
      3000 // 3 秒超时
    );

    if (!response.ok) {
      logger.warn(`Failed to fetch tags: HTTP ${response.status}`);
      return [];
    }

    const data = await response.json();

    if (Array.isArray(data)) {
      return data.filter(tag => typeof tag === 'string');
    }

    // 处理可能的嵌套结构
    if (data && Array.isArray(data.types)) {
      return data.types.filter(tag => typeof tag === 'string');
    }

    return [];
  } catch (error) {
    logger.warn('Failed to fetch existing tags:', error.message);
    return [];
  }
}

/**
 * 语义匹配：找到最能概括任务描述的已有标签
 * @param {string} description - 任务描述
 * @param {string[]} existingTags - 已有标签列表
 * @returns {string|null} 匹配的标签，无匹配返回 null
 */
function findBestMatchingTag(description, existingTags) {
  if (!existingTags || existingTags.length === 0) {
    return null;
  }

  const descLower = description.toLowerCase();

  // 计算每个标签的匹配分数
  const scored = existingTags.map(tag => {
    const tagLower = tag.toLowerCase();
    let score = 0;

    // 精确包含
    if (descLower.includes(tagLower)) {
      score += 10;
    }

    // 关键词匹配
    const tagWords = tagLower.split(/[\s\-]+/);
    for (const word of tagWords) {
      if (word.length >= 2 && descLower.includes(word)) {
        score += 2;
      }
    }

    // 语义关联
    const semanticMappings = {
      '代码重构': ['重构', '改写', 'rewrite', 'refactor', '异步', '同步', '优化结构'],
      '格式转换': ['转换', 'transform', 'convert', '格式', 'csv', 'json', 'xml'],
      'bug修复': ['修复', 'fix', 'bug', '错误', '异常', '报错', '问题解决'],
      '单元测试': ['测试', 'test', '单元', 'jest', 'pytest', 'mocha'],
      '文档生成': ['文档', 'doc', 'readme', '注释', '说明', 'api文档'],
      '数据分析': ['分析', 'analyze', '统计', '日志', '数据', '查询'],
      '性能优化': ['优化', 'optimize', '性能', '提速', '缓存', '慢'],
      '接口联调': ['接口', 'api', '联调', '对接', 'http', 'rest'],
      '配置管理': ['配置', 'config', '环境变量', '设置', '初始化'],
      '应用部署': ['部署', 'deploy', '发布', '上线', 'docker', 'k8s']
    };

    const relatedWords = semanticMappings[tag] || [];
    for (const word of relatedWords) {
      if (descLower.includes(word.toLowerCase())) {
        score += 3;
      }
    }

    return { tag, score };
  });

  // 按分数排序
  scored.sort((a, b) => b.score - a.score);

  logger.debug('Tag matching scores:', scored.slice(0, 3));

  // 返回最高分的标签，但要求至少有一定分数
  if (scored[0] && scored[0].score >= 5) {
    return scored[0].tag;
  }

  return null;
}

/**
 * 执行 resolve_task_type
 * @param {object} params - 输入参数
 * @param {string} params.task_description - 任务描述
 * @param {object} context - OpenClaw 执行上下文
 * @returns {Promise<string>} 确定的 task_type
 */
async function execute(params, context = {}) {
  const { task_description } = params;

  if (!task_description) {
    logger.warn('No task_description provided, using default');
    return '任务执行';
  }

  const config = getConfig();

  // 第一步：拉取平台现有标签列表
  logger.debug('Fetching existing tags from community...');
  const existingTags = await fetchExistingTags(config.communityUrl, config.apiKey);
  logger.debug(`Fetched ${existingTags.length} existing tags`);

  // 第二步：语义匹配
  if (existingTags.length > 0) {
    const matchedTag = findBestMatchingTag(task_description, existingTags);
    if (matchedTag) {
      logger.info(`Matched existing tag: "${matchedTag}"`);
      return matchedTag;
    }
    logger.debug('No existing tag matched, generating new one');
  }

  // 第三步：自行生成新标签
  const generatedLabel = generateTaskTypeLabel(task_description);
  logger.info(`Generated new tag: "${generatedLabel}"`);

  return generatedLabel;
}

module.exports = {
  execute,
  fetchExistingTags,
  findBestMatchingTag
};

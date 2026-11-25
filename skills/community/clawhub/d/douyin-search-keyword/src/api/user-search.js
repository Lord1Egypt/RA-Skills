/**
 * 抖音用户搜索模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");

/**
 * 处理用户搜索结果。字段原样透出，有 sec_uid 时补 author_url。
 * fans/type 筛选暂未对接采集端，请求侧固定为 0，不在此处理。
 * @param {Array} data
 * @returns {Array}
 */
function processUserSearchResults(data) {
  if (!Array.isArray(data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "用户搜索结果格式异常", true);
  }

  return data.map((item) => {
    if (!item || typeof item !== "object") return item;
    const processedItem = { ...item };
    if (item.sec_uid) {
      processedItem.author_url = `https://www.douyin.com/user/${item.sec_uid}`;
    }
    return processedItem;
  });
}

/**
 * 创建抖音用户搜索任务
 * @param {string} token
 * @param {string} keyword
 * @param {number} limit
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）；缺失则查询仅带业务字段
 */
async function createUserSearchTask(token, keyword, limit) {
  const response = await requestApi(
    "POST",
    "/api/douyin/user-search/keyword",
    { _: Date.now() },
    {
      keyword,
      fans: 0,
      type: 0,
      limit,
    },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * 获取抖音用户搜索任务结果
 * @param {string} token
 * @param {string} keyword
 * @param {number} limit
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 * @returns {Promise<{ results: Array, cost?: number }>}
 */
async function getUserSearchTask(token, keyword, limit, taskId) {
  const params = taskId
    ? { id: taskId }
    : { keyword, fans: 0, type: 0, limit };
  const response = await pollTaskResult(
    "/api/douyin/user-search/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);

  if (response.data) {
    return { results: processUserSearchResults(response.data), cost };
  }

  return { results: [], cost };
}

module.exports = {
  createUserSearchTask,
  getUserSearchTask,
};

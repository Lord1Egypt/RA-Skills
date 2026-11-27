/**
 * 抖音用户搜索模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");

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
 */
async function createUserSearchTask(token, keyword, limit) {
  return await requestApi(
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
}

/**
 * 获取抖音用户搜索任务结果
 * @param {string} token
 * @param {string} keyword
 * @param {number} limit
 * @returns {Promise<Array>}
 */
async function getUserSearchTask(token, keyword, limit) {
  const response = await pollTaskResult(
    "/api/douyin/user-search/info",
    {
      keyword,
      fans: 0,
      type: 0,
      limit,
    },
    token,
    "查询任务",
  );

  if (response.data) {
    return processUserSearchResults(response.data);
  }

  return [];
}

module.exports = {
  createUserSearchTask,
  getUserSearchTask,
};

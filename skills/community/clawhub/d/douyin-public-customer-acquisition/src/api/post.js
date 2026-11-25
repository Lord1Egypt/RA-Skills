/**
 * 抖音博主已发布作品模块
 */
const constants = require("../config/constants");
const { SkillError } = require("../utils/errors");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");

function processPostResults(data) {
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    throw new SkillError("API_SCHEMA_CHANGED", "作品结果格式异常", true);
  }
  if (typeof data.error === "string" && data.error) {
    throw new SkillError("API_SCHEMA_CHANGED", data.error, true);
  }
  const result = {};
  if (Array.isArray(data.post)) {
    result.post = data.post;
  }
  if (data.user && typeof data.user === "object" && !Array.isArray(data.user)) {
    result.user = data.user;
  }
  return result;
}

/**
 * 创建抖音已发布作品任务
 * @param {string} token 技能令牌
 * @param {string} url 抖音博主主页URL
 * @param {number} limit 作品数量
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）
 * @throws {Error} API调用失败时抛出错误
 */
async function createPostTask(token, url, limit) {
  const params = { _: Date.now() };
  const data = {
    url: url,
    limit: limit,
  };
  const response = await requestApi(
    "POST",
    "/api/douyin/post/url",
    params,
    data,
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * 获取抖音已发布作品任务结果
 * @param {string} token 技能令牌
 * @param {string} url 抖音博主主页URL
 * @param {number} limit 作品数量
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 * @returns {Promise<{ results: {post?: Array, user?: Object}|null, cost?: number }>}
 * @throws {Error} API调用失败时抛出错误
 */
async function getPostTask(token, url, limit, taskId) {
  const params = taskId ? { id: taskId } : { url: url, limit: limit };
  const response = await pollTaskResult(
    "/api/douyin/post/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (response.data) {
    return { results: processPostResults(response.data), cost };
  }
  return { results: null, cost };
}

module.exports = {
  createPostTask,
  getPostTask,
};

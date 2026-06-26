const utils = require("../utils/utils");

/**
 * 检查搜索关键词是否符合要求
 * @param {string} keyword - 搜索关键词
 * @returns {boolean} - 是否有效
 */
function isKeywordValid(keyword) {
  keyword = keyword.trim();
  if (keyword.length < 2) {
    utils.printError(`搜索关键词长度不能小于 2 个字符`);
    return false;
  }
  if (keyword.length > 50) {
    utils.printError(`搜索关键词长度不能超过 50 个字符`);
    return false;
  }
  if (/[<>\"'&]/g.test(keyword)) {
    utils.printError(`搜索关键词包含特殊字符, 请输入普通关键词, 例如: 新媒体`);
    return false;
  }
  if (keyword.includes("http")) {
    utils.printError(
      `搜索关键词包含 http 链接, 请输入普通关键词, 例如: 新媒体`,
    );
    return false;
  }
  return true;
}

/**
 * 清洗搜索关键词，移除非法字符
 * @param {string} keyword - 原始关键词
 * @returns {string} - 清洗后的搜索关键词
 */
function cleanKeyword(keyword) {
  keyword = keyword.trim();
  keyword = keyword.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\s.,!?# ，。！？]/g, "");
  keyword = keyword.replace(/\s+/g, " "); // 合并连续空格
  return keyword;
}

/**
 * 格式化并验证搜索选项
 * @param {number} sort - 排序依据 (0:综合, 1:最多点赞, 2:最新发布)
 * @param {number} time - 时间范围 (0:全部, 1:一天内, 7:七天内, 180:半年内)
 * @param {number} duration - 视频时长 (0:不限, 1:1分钟以下, 2:1-5分钟, 3:5分钟以上)
 * @param {number} limit - 搜索数量 (1-10000)
 * @returns {[number, number, number, number]} 格式化后的选项数组
 */
function optionFormat(sort, time, duration, limit) {
  sort = sort || 0;
  time = time || 0;
  duration = duration || 0;
  limit = limit || 10;
  if (sort !== 0 && sort !== 1 && sort !== 2) {
    utils.printError(`排序依据 ${sort} 无效, 请使用 0, 1, 2。 默认值为 0`);
    sort = 0;
  }
  if (time !== 0 && time !== 1 && time !== 7 && time !== 180) {
    utils.printError(`发布时间 ${time} 无效, 请使用 0, 1, 7, 180。 默认值为 0`);
    time = 0;
  }
  if (duration !== 0 && duration !== 1 && duration !== 2 && duration !== 3) {
    utils.printError(
      `视频时长 ${duration} 无效, 请使用 0, 1, 2, 3。 默认值为 0`,
    );
    duration = 0;
  }
  if (limit < 1 || limit > 10000) {
    utils.printError(`搜索数量 ${limit} 无效, 请使用 1-10000 默认值为 10`);
    limit = 10;
  }
  return [sort, time, duration, limit];
}

function formatMessage(keyword, result) {
  let message = `**抖音综合搜索结果**: ${keyword}\n`;
  message += "-".repeat(35) + "\n\n";
  for (let i = 0; i < result.length; i++) {
    const item = result[i];
    message += `**${i + 1} .** ${item.desc || "[无标题]"}\n`;
    message += `**发布人**: ${item.author_nickname || "[未知]"}\n`;
    message += `**发布时间**: ${item.create_time_str || "[未知]"}\n`;
    message += `**链接**: ${item.url || "[未知]"}\n`;
    if (item.dynamic_cover && item.dynamic_cover.length > 0) {
      message += `**封面**: ${item.dynamic_cover[0] || ""}\n`;
    }
    if (item.play_addr) {
      message += `**视频**: ${item.play_addr}\n`;
    }
    if (item.images && item.images.length > 0) {
      message += `**图文**: ${item.images.slice(0, 3).join(", ")}...\n`;
    }
    message += `**点赞**: ${item.digg_count || 0}\t`;
    message += `**评论**: ${item.comment_count || 0}\t`;
    message += `**收藏**: ${item.collect_count || 0}\t`;
    message += `**分享**: ${item.share_count || 0}\n`;
    message += "\n";
  }
  message += "-".repeat(35) + "\n";
  message += `**共 ${result.length} 条结果**\n`;
  return message;
}

module.exports = {
  isKeywordValid,
  cleanKeyword,
  optionFormat,
  formatMessage,
};

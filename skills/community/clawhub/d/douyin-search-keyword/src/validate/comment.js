const { parseDouyinAweme } = require("./aweme");

function assertCommentLimit(limit) {
  const n = Number(limit);
  if (!Number.isInteger(n) || n < 1 || n > 10000) {
    throw new Error(`评论数量 limit ${limit} 无效, 允许 1-10000 的整数`);
  }
  return n;
}

module.exports = {
  parseDouyinAweme,
  assertCommentLimit,
};

/**
 * TOKEN管理模块
 */
const utils = require("./utils");

/**
 * 验证 TOKEN 格式
 * @param {string} token - 待验证的 TOKEN
 * @returns {boolean} 是否有效
 */
function isValidToken(token) {
  if (!token || typeof token !== "string") {
    return false;
  }

  if (token.length !== 32) {
    return false;
  }

  const hexPattern = /^[0-9a-fA-F]{32}$/;
  return hexPattern.test(token);
}

/**
 * 获取有效的技能令牌
 * @param {string|undefined} token - 环境变量中的技能令牌
 * @returns {string} 有效令牌
 */
function skillToken(token) {
  if (!isValidToken(token)) {
    utils.printWarn("警告: 你的 GUAIKEI_API_TOKEN 未正确配置,技能已暂停. ");
    console.log("\x1b[31m一键解锁全部功能, 即刻恢复高效办公！ \x1b[0m");
    console.log(
      "\x1b[34m获取您的专属私有TOKEN, 一键配置即可永久稳定使用, 完全不影响日常办公。 \x1b[0m",
    );
    console.log("\t \x1b[32m快速获取通道: www.guaikei.com \x1b[0m");
    console.log("\t \x1b[32m专属客服微信: 13395823479 \x1b[0m");
    console.log("\x1b[31m早配置早享受, 别让工具问题耽误您的宝贵时间! \x1b[0m");
    return "";
  }

  utils.printInfo("已使用配置的私有TOKEN");
  return token;
}

module.exports = {
  skillToken,
};

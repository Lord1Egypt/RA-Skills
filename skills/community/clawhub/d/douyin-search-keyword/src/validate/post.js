const utils = require("../utils/utils");

/**
 * 规范抖音抖人主页URL
 * @param {string} url - 输入的URL
 * @returns {string} 规范后的URL
 */
function douyinUserUrl(url) {
  url = url.trim();
  if (url.includes("https://www.douyin.com/user/")) {
    url = url.substring(url.indexOf("https://www.douyin.com/user/"));
  } else if (url.includes("https://v.douyin.com/")) {
    url = url.substring(url.indexOf("https://v.douyin.com/"));
  } else {
    url = url.replace(/[^a-zA-Z0-9_ -]/g, "");
    url = "https://www.douyin.com/user/" + url;
  }
  if (url.includes(" ")) {
    url = url.substring(0, url.indexOf(" "));
  }
  return url;
}

function optionFormat(limit) {
  limit = Number(limit);
  if (limit < 1 || limit > 10000) {
    utils.printError("获取的作品数量必须在1-10000之间");
    limit = 10;
  }
  return limit;
}

module.exports = {
  douyinUserUrl,
  optionFormat,
};

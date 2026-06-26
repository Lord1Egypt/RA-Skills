#!/usr/bin/env node

const constants = require("../config/constants");
const token = require("../utils/token");
const log = require("../utils/log");
const comment = require("../api/comment");
const utils = require("../utils/utils");
const validator = require("../validate/comment");

function parseArgs(args) {
  const result = {
    url: "",
    limit: 10,
    helpRequested: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--url" || arg === "-u") {
      result.url = args[i + 1] || "";
      i++;
    } else if (arg === "--limit" || arg === "-l") {
      result.limit = Number(args[i + 1]) || 10;
      i++;
    } else if (arg === "--help" || arg === "-h") {
      printHelp();
      result.helpRequested = true;
    } else if (!arg.startsWith("--") && !result.keyword) {
      result.url = arg;
    }
  }

  return result;
}

function printHelp() {
  console.log(`
用法: node src/douyin/comment-cli.js <url> [选项]

选项:
--url, -u \t<url> \t抖音视频(或图文)URL或aweme_id
--limit, -l \t<limit> \t评论数量 (默认10, 最大10000)
--help, -h \t显示帮助信息

示例1: node src/douyin/comment-cli.js https://www.douyin.com/video/xxx
示例2: node src/douyin/comment-cli.js --url https://www.douyin.com/note/xxx --limit 20
示例3: node src/douyin/comment-cli.js -u xxx --limit 100
`);
}

/**
 * 主函数 - 获取抖音作品的评论列表
 */
async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    return;
  }

  const parsedArgs = parseArgs(args);
  if (parsedArgs.helpRequested) {
    return;
  }
  let { url, limit } = parsedArgs;
  if (!url) {
    utils.printError("请提供抖音视频(或图文)URL或aweme_id");
    printHelp();
    return;
  }

  utils.printBanner();
  utils.printInfo(`原始URL: ${url}`);
  url = validator.douyinPostUrl(url);
  utils.printInfo(`规范后的URL: ${url}`);
  limit = validator.optionFormat(limit);
  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") return;
  let commentTask = null;
  try {
    const status = await comment.createCommentTask(tokenValue, url, limit);
    if (!status || status.errcode !== 0) {
      throw new Error(
        `获取评论任务创建时, 遇到未知错误, 请反馈给开发者 ${status} - ${Date.now()}`,
      );
    }
    utils.printSuccess(`获取评论任务创建成功, 正在获取评论中...`);

    commentTask = await comment.getCommentTask(tokenValue, url, limit);
  } catch (error) {
    utils.printError(`获取评论失败: ${error.message}`);
    const errorOutput = {
      status: "error",
      url: url,
      message: error.message,
      error_code: error.code || "UNKNOWN",
      limit: limit,
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(errorOutput, null, 2));
    return;
  }

  if (!commentTask || !Array.isArray(commentTask) || commentTask.length === 0) {
    utils.printError(`获取评论任务没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      url: url,
      message: "没有找到匹配的评论",
      error_code: "NO_MATCH",
      limit: limit,
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(emptyOutput, null, 2));
    return;
  }

  // 输出评论结果
  const finalOutput = {
    status: "success",
    url: url,
    message: "获取评论任务完成",
    limit: limit,
    total: commentTask.length,
    timestamp: new Date().toLocaleString(),
    metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: commentTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(`获取评论任务完成, 共返回 ${finalOutput.total} 条结果`);

  url = url.replace(/[^a-zA-Z0-9_-]/g, "");
  url = url.replace("httpswwwdouyincom", "");
  url = url.replace("note", "");
  url = url.replace("video", "");
  await log.taskWrite(
    `${startTime}_${url}_comment.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error);
  process.exit(1);
});

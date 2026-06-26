#!/usr/bin/env node

const constants = require("../config/constants");
const token = require("../utils/token");
const hot = require("../api/hot");
const utils = require("../utils/utils");

/**
 * 主函数 - 获取抖音热榜入口
 */
async function main() {
  const startTime = Date.now();
  utils.printBanner();

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  let hotTask = null;
  try {
    hotTask = await hot.getHotTask(tokenValue);
  } catch (error) {
    utils.printError(`获取抖音热榜失败: ${error.message}`);
    const errorOutput = {
      status: "error",
      message: error.message,
      error_code: error.code || "UNKNOWN",
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(errorOutput, null, 2));
    return;
  }

  if (!hotTask || !Array.isArray(hotTask) || hotTask.length === 0) {
    utils.printError(`抖音热榜没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      message: "没有找到最新的抖音热榜",
      error_code: "NO_MATCH",
      timestamp: new Date().toLocaleString(),
      results: [],
    };
    console.log(JSON.stringify(emptyOutput, null, 2));
    return;
  }

  // 输出热榜结果
  const finalOutput = {
    status: "success",
    message: "获取抖音热榜任务完成",
    total: hotTask.length,
    timestamp: new Date().toLocaleString(),
    metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: hotTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(`抖音热榜任务完成, 共 ${hotTask.length} 条记录`);
}

main().catch((error) => {
  utils.printError(error);
  process.exit(1);
});

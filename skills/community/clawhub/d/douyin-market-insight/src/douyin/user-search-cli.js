#!/usr/bin/env node

const userSearch = require("../api/user-search");
const log = require("../utils/log");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");
const { parseArgs, buildHelp, parseDecimalInteger } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  buildSuccessEnvelope,
  finishSuccess,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--keyword": {
      alias: "-k",
      key: "keyword",
      type: "string",
      required: true,
      desc: "用户搜索关键词",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: parseDecimalInteger,
      desc: "获取数量, 1-10000",
    },
  },
  positionalKey: "keyword",
};

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node src/douyin/user-search-cli.js <关键词> [选项]", [
      'node src/douyin/user-search-cli.js --keyword "AI"',
      'node src/douyin/user-search-cli.js --keyword "美妆达人" --limit 20',
      "node src/douyin/user-search-cli.js -k AI -l 10",
    ]) +
      "\n\n注意:\n" +
      "  - 按关键词搜用户/达人/账号；搜视频/图文请用 search-cli.js；已有主页链接请用 post-cli.js\n" +
      "  - 关键词建议 2-50 个字符，不能是链接, 不含 < > \" ' &\n" +
      "  - 数量 1-10000；包月 Token 实际最多 30，超限返回 PLAN_LIMIT\n" +
      "  - 暂不支持粉丝量/认证类型筛选\n" +
      "  - 关键词以 - 开头时写成 --keyword=-AI，或在 -- 后面写位置参数",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("user_search", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "user_search",
      "INVALID_ARGS",
      `参数解析错误: ${error.message}`,
      2,
      startTime,
    );
    return;
  }
  if (parsed._help) {
    printHelp();
    return;
  }

  let { keyword, limit } = parsed;
  const keywordRaw = keyword;

  utils.printBanner();
  utils.printInfo(`原始关键词: ${keywordRaw}`);
  keyword = validator.normalizeKeyword(keyword);
  if (!validator.isKeywordValid(keyword)) {
    emitError(
      "user_search",
      "INVALID_KEYWORD",
      "关键词不合法: 需 2-50 个字符, 不能是链接, 不含 < > \" ' & 等特殊符号",
      1,
      startTime,
      {
        command: "user_search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        limit: limit,
      },
    );
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);

  try {
    limit = validator.assertUserSearchLimit(limit);
  } catch (error) {
    utils.printError(error.message);
    emitError("user_search", "INVALID_ARGS", error.message, 2, startTime, {
      command: "user_search",
      keyword_raw: keywordRaw,
      keyword: keyword,
      limit: limit,
    });
    return;
  }
  utils.printInfo(`数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError(
      "user_search",
      "AUTH_REQUIRED",
      "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符",
      3,
      startTime,
      {
        command: "user_search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        limit: limit,
      },
    );
    return;
  }

  let results = null;
  try {
    await userSearch.createUserSearchTask(tokenValue, keyword, limit);
    utils.printSuccess("用户搜索任务创建成功, 正在搜索中...");
    results = await userSearch.getUserSearchTask(tokenValue, keyword, limit);
  } catch (error) {
    utils.printError(`用户搜索失败: ${error.message}`);
    emitError(
      "user_search",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      {
        command: "user_search",
        keyword_raw: keywordRaw,
        keyword: keyword,
        limit: limit,
      },
    );
    return;
  }

  const searchRequest = {
    command: "user_search",
    keyword_raw: keywordRaw,
    keyword: keyword,
    limit: limit,
  };
  if (!results || !Array.isArray(results) || results.length === 0) {
    utils.printInfo("没有找到匹配的用户");
    emitEmpty("没有找到匹配的用户", startTime, searchRequest);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "用户搜索任务完成",
    startTime,
    searchRequest,
    results,
  );
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${keyword}_${limit}_user_search.json`,
    stderrMessage: `用户搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("user_search", error);
});

const { execSync } = require('child_process');
const path = require('path');

module.exports = {
  // 向 OpenClaw 注册的工具名称
  name: "bili_fetch_tool",
  description: "执行本地Python脚本抓取B站热榜",
  parameters: {
    type: "object",
    properties: {} // 脚本独立闭环，无需大模型传参
  },
  execute: async function(args, context) {
    try {
      // 强制在当前 skill 目录下执行脚本
      const scriptPath = path.join(__dirname, 'bili_fetcher.py');
      const result = execSync(`python "${scriptPath}"`, {
        encoding: 'utf-8'
      });
      return result;
    } catch (error) {
      return `数据抓取执行失败: ${error.message}\n${error.stderr || ''}`;
    }
  }
};
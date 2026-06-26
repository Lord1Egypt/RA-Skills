/**
 * BaoStock Skill
 * Entry point for OpenClaw
 */

import { Skill } from "@openclaw/sdk";

const skill = new Skill({
  name: "baostock-skill",
  description: "Query Chinese A-share market data using BaoStock",

  triggers: {
    includes: ["股票", "股价", "行情", "A股", "实时", "历史数据", "K线", "市盈率", "宝库", "baostock"],
    commands: ["stock-quote", "stock-history", "stock-list", "index-data"],
  },

  async run(input, context) {
    const { symbol, type, start_date, end_date, frequency } = input;

    const args = [
      type && `--type ${type}`,
      symbol && `--symbol ${symbol}`,
      start_date && `--start-date ${start_date}`,
      end_date && `--end-date ${end_date}`,
      frequency && `--frequency ${frequency}`,
    ].filter(Boolean).join(" ");

    const scriptPath = "/Users/nico/.openclaw/workspace/skills/baostock-skill/baostock";

    return new Promise((resolve, reject) => {
      const { exec } = require("child_process");
      exec(`"${scriptPath}" ${args}`, { maxBuffer: 1024 * 1024 }, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr || error.message));
          return;
        }
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          resolve({ raw: stdout, error: stderr });
        }
      });
    });
  },
});

export default skill;
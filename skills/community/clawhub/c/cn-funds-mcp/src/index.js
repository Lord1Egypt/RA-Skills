#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as api from "./api.js";
import * as portfolio from "./portfolio.js";

const server = new McpServer({
  name: "cn-funds-mcp",
  version: "0.1.0",
});

// ======================== 基金搜索 ========================

server.tool("search_fund", "根据关键词搜索基金（支持基金名称、代码、拼音缩写）", { keyword: z.string().describe("搜索关键词，如 '白酒'、'161725'、'zsyh'") }, async ({ keyword }) => {
  const results = await api.searchFund(keyword);
  return {
    content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
  };
});

// ======================== 基金实时估值 ========================

server.tool("get_fund_estimate", "获取基金实时估值数据（盘中估算净值和涨跌幅）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const result = await api.getFundEstimate(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ======================== 批量基金信息 ========================

server.tool(
  "get_fund_batch_info",
  "批量获取多只基金的基本信息（净值、涨跌幅）",
  {
    fundCodes: z.string().describe("基金代码，多个用逗号分隔，如 '161725,110011,005827'"),
  },
  async ({ fundCodes }) => {
    const results = await api.getFundBatchInfo(fundCodes);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// ======================== 基金详细信息 ========================

server.tool("get_fund_info", "获取基金详细信息（类型、公司、经理、规模、近期收益排名等）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const result = await api.getFundInfo(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ======================== 基金估值走势（日内） ========================

server.tool("get_fund_valuation_detail", "获取基金当日估值走势（日内分时估值变化数据）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const result = await api.getFundValuationDetail(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ======================== 基金历史净值 ========================

server.tool(
  "get_fund_net_value_history",
  "获取基金历史净值走势（单位净值、累计净值）",
  {
    fundCode: z.string().describe("基金代码，如 '161725'"),
    range: z.enum(["m", "q", "hy", "y", "2y", "3y", "5y"]).default("y").describe("时间范围: m=近1月, q=近3月, hy=近6月, y=近1年, 2y=近2年, 3y=近3年, 5y=近5年"),
  },
  async ({ fundCode, range }) => {
    const results = await api.getFundNetValueHistory(fundCode, range);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// ======================== 基金累计收益对比 ========================

server.tool(
  "get_fund_accumulated_performance",
  "获取基金累计收益走势，并与沪深300及同类平均对比",
  {
    fundCode: z.string().describe("基金代码，如 '161725'"),
    range: z.enum(["m", "q", "hy", "y", "2y", "3y", "5y"]).default("y").describe("时间范围: m=近1月, q=近3月, hy=近6月, y=近1年, 2y=近2年, 3y=近3年, 5y=近5年"),
  },
  async ({ fundCode, range }) => {
    const results = await api.getFundAccumulatedPerformance(fundCode, range);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// ======================== 基金持仓明细 ========================

server.tool("get_fund_position", "获取基金股票持仓明细（持仓股票、占比、较上期变化）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const result = await api.getFundPosition(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ======================== 基金经理列表 ========================

server.tool("get_fund_manager_list", "获取基金历任经理列表（任职起止日期、任职天数、任职期间涨幅）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const results = await api.getFundManagerList(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
  };
});

// ======================== 基金经理详情 ========================

server.tool("get_fund_manager_detail", "获取基金现任经理详细信息（简历、照片、管理年限）", { fundCode: z.string().describe("基金代码，如 '161725'") }, async ({ fundCode }) => {
  const results = await api.getFundManagerDetail(fundCode);
  return {
    content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
  };
});

// ======================== 股票/指数分时走势 ========================

server.tool(
  "get_stock_trend",
  "获取股票或指数的日内分时走势数据",
  {
    secid: z.string().describe("证券ID，格式为 '市场.代码'，如 '1.000001'(上证指数), '0.399001'(深证成指), '1.600519'(贵州茅台), '0.000858'(五粮液), '116.01810'(小米集团)"),
  },
  async ({ secid }) => {
    const result = await api.getStockTrend(secid);
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  }
);

// ======================== 股票/指数实时行情 ========================

server.tool(
  "get_stock_quote",
  "获取股票或指数的实时行情报价（价格、涨跌幅、成交额）",
  {
    secids: z.string().describe("证券ID列表，多个用逗号分隔，格式 '市场.代码'，如 '1.000001,0.399001,1.600519'"),
  },
  async ({ secids }) => {
    const results = await api.getStockQuote(secids);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// ======================== 大盘概况 ========================

server.tool("get_market_overview", "获取A股大盘概况（上证指数、深证成指的价格/涨跌/成交额/涨跌家数）", {}, async () => {
  const results = await api.getMarketOverview();
  return {
    content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
  };
});

// ======================== 大盘资金流向 ========================

server.tool("get_market_capital_flow", "获取A股大盘当日资金流向（主力/超大单/大单/中单/小单净流入，单位亿元）", {}, async () => {
  const results = await api.getMarketCapitalFlow();
  return {
    content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
  };
});

// ======================== 板块资金流向 ========================

server.tool(
  "get_sector_capital_flow",
  "获取板块资金流向排行（行业板块或概念板块的资金净流入排名）",
  {
    timeType: z.enum(["f62", "f164", "f174"]).default("f62").describe("时间类型: f62=今日, f164=5日, f174=10日"),
    code: z.string().default("m:90+s:4").describe("板块代码筛选: 'm:90+s:4'=行业板块(默认), 'm:90+s:1'=概念板块"),
  },
  async ({ timeType, code }) => {
    const results = await api.getSectorCapitalFlow(timeType, code);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// ======================== 北向资金（沪深港通） ========================

server.tool("get_northbound_capital", "获取沪深港通(北向/南向)资金实时流向数据（沪股通/深股通/港股通净流入，单位亿元）", {}, async () => {
  const result = await api.getNorthboundCapital();
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
  };
});

// ======================== 持仓管理 ========================

server.tool(
  "save_portfolio",
  "保存/更新我的基金持仓记录（基金代码、持有份额、成本净值）。如果基金已存在则更新，不存在则新增。",
  {
    fundCode: z.string().describe("基金代码，如 '161725'"),
    name: z.string().optional().describe("基金名称（可选，方便识别）"),
    shares: z.number().describe("持有份额，如 1000"),
    costPrice: z.number().describe("成本净值（买入均价），如 1.2345"),
  },
  async ({ fundCode, name, shares, costPrice }) => {
    let fundName = name;
    if (!fundName) {
      try {
        const est = await api.getFundEstimate(fundCode);
        fundName = est.name;
      } catch {
        fundName = fundCode;
      }
    }
    const funds = portfolio.upsertPortfolio({ fundCode, name: fundName, shares, costPrice });
    return {
      content: [{ type: "text", text: `已保存持仓：${fundName}(${fundCode})，份额=${shares}，成本=${costPrice}\n\n当前持仓列表：\n${JSON.stringify(funds, null, 2)}` }],
    };
  }
);

server.tool(
  "remove_portfolio",
  "删除我的某只基金持仓记录",
  { fundCode: z.string().describe("要删除的基金代码，如 '161725'") },
  async ({ fundCode }) => {
    const result = portfolio.removePortfolio(fundCode);
    if (result === null) {
      return { content: [{ type: "text", text: `未找到基金 ${fundCode} 的持仓记录` }] };
    }
    return {
      content: [{ type: "text", text: `已删除 ${fundCode} 的持仓记录\n\n剩余持仓：\n${JSON.stringify(result, null, 2)}` }],
    };
  }
);

server.tool(
  "get_portfolio",
  "查看我当前保存的所有基金持仓列表",
  {},
  async () => {
    const funds = portfolio.listPortfolio();
    if (funds.length === 0) {
      return { content: [{ type: "text", text: "当前没有持仓记录。可以使用 save_portfolio 工具添加持仓。" }] };
    }
    return {
      content: [{ type: "text", text: JSON.stringify(funds, null, 2) }],
    };
  }
);

server.tool(
  "get_portfolio_profit",
  "一键查询我所有持仓的今日收益和总收益（基于实时估值计算）",
  {},
  async () => {
    const funds = portfolio.listPortfolio();
    if (funds.length === 0) {
      return { content: [{ type: "text", text: "当前没有持仓记录。请先使用 save_portfolio 工具添加持仓。" }] };
    }

    const results = await Promise.allSettled(
      funds.map((f) => api.getFundEstimate(f.fundCode))
    );

    let totalDayProfit = 0;
    let totalProfit = 0;
    let totalCost = 0;
    let totalMarketValue = 0;

    const details = funds.map((f, i) => {
      const r = results[i];
      if (r.status !== "fulfilled") {
        return {
          fundCode: f.fundCode,
          name: f.name,
          shares: f.shares,
          costPrice: f.costPrice,
          error: r.reason?.message || "获取估值失败",
        };
      }
      const est = r.value;
      const estimateValue = parseFloat(est.estimateValue);
      const netValue = parseFloat(est.netValue);
      const cost = f.costPrice;
      const shares = f.shares;

      const dayProfit = +(shares * (estimateValue - netValue)).toFixed(2);
      const holdProfit = +(shares * (estimateValue - cost)).toFixed(2);
      const marketValue = +(shares * estimateValue).toFixed(2);
      const costTotal = +(shares * cost).toFixed(2);
      const holdProfitRate = cost > 0 ? +(((estimateValue - cost) / cost) * 100).toFixed(2) : 0;

      totalDayProfit += dayProfit;
      totalProfit += holdProfit;
      totalCost += costTotal;
      totalMarketValue += marketValue;

      return {
        fundCode: f.fundCode,
        name: est.name,
        shares,
        costPrice: cost,
        yesterdayNetValue: netValue,
        estimateValue,
        estimateGrowthRate: est.estimateGrowthRate + "%",
        estimateTime: est.estimateTime,
        dayProfit,
        holdProfit,
        holdProfitRate: holdProfitRate + "%",
        marketValue,
      };
    });

    const totalHoldProfitRate = totalCost > 0 ? +((totalProfit / totalCost) * 100).toFixed(2) : 0;

    const summary = {
      totalFunds: funds.length,
      totalCost: +totalCost.toFixed(2),
      totalMarketValue: +totalMarketValue.toFixed(2),
      totalDayProfit: +totalDayProfit.toFixed(2),
      totalHoldProfit: +totalProfit.toFixed(2),
      totalHoldProfitRate: totalHoldProfitRate + "%",
      details,
    };

    return {
      content: [{ type: "text", text: JSON.stringify(summary, null, 2) }],
    };
  }
);

// ======================== 定时提醒 ========================

server.tool(
  "set_reminder",
  "设置定时提醒（如每天下午2:30推送持仓收益）。提醒会在每个交易日的指定时间触发。",
  {
    time: z.string().describe("提醒时间，24小时制 HH:MM 格式，如 '14:30'"),
    type: z
      .enum(["profit_report", "market_report", "custom"])
      .default("profit_report")
      .describe("提醒类型: profit_report=持仓收益播报, market_report=大盘播报, custom=自定义"),
    message: z.string().optional().describe("自定义提醒内容（type=custom 时使用）"),
  },
  async ({ time, type, message }) => {
    const reminders = portfolio.addReminder({ time, type, message });
    const typeNames = { profit_report: "持仓收益播报", market_report: "大盘播报", custom: "自定义提醒" };
    return {
      content: [{
        type: "text",
        text: `已设置提醒：每个交易日 ${time} ${typeNames[type]}\n\n当前所有提醒：\n${JSON.stringify(reminders, null, 2)}`,
      }],
    };
  }
);

server.tool(
  "get_reminders",
  "查看当前所有定时提醒设置",
  {},
  async () => {
    const reminders = portfolio.listReminders();
    if (reminders.length === 0) {
      return { content: [{ type: "text", text: "当前没有设置任何提醒。可以使用 set_reminder 添加。" }] };
    }
    return { content: [{ type: "text", text: JSON.stringify(reminders, null, 2) }] };
  }
);

server.tool(
  "remove_reminder",
  "删除某个定时提醒",
  { id: z.string().describe("提醒ID，可通过 get_reminders 查看") },
  async ({ id }) => {
    const result = portfolio.removeReminder(id);
    if (result === null) {
      return { content: [{ type: "text", text: `未找到提醒 ${id}` }] };
    }
    return { content: [{ type: "text", text: `已删除提醒 ${id}\n\n剩余提醒：\n${JSON.stringify(result, null, 2)}` }] };
  }
);

server.tool(
  "check_reminders",
  "检查是否有到期的提醒（AI 应在每次对话开始时主动调用此工具）。返回当前到期未触发的提醒列表，同一提醒每天只触发一次。",
  {},
  async () => {
    const { due, today, currentTime, message } = portfolio.checkReminders();

    if (message) {
      return { content: [{ type: "text", text: message }] };
    }

    if (due.length === 0) {
      return { content: [{ type: "text", text: `当前时间 ${today} ${currentTime}，没有到期的提醒。` }] };
    }

    const actions = due.map((r) => {
      if (r.type === "profit_report") {
        return `[${r.time}] 持仓收益播报 → 请立即调用 get_portfolio_profit 查询收益，并根据涨跌情况给出加仓/减仓建议`;
      }
      if (r.type === "market_report") {
        return `[${r.time}] 大盘播报 → 请调用 get_market_overview + get_market_capital_flow 播报大盘行情`;
      }
      return `[${r.time}] 自定义提醒: ${r.message}`;
    });

    return {
      content: [{
        type: "text",
        text: `当前时间 ${today} ${currentTime}，有 ${due.length} 个提醒到期：\n\n${actions.join("\n\n")}\n\n请按照上述指引执行对应操作。`,
      }],
    };
  }
);

// ======================== 启动服务 ========================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("funds-mcp server started");
}

main().catch((err) => {
  console.error("Failed to start server:", err);
  process.exit(1);
});

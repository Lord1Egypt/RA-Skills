#!/usr/bin/env node

/**
 * A股行情分析搜索脚本
 * 获取A股相关行情信息
 */

function usage() {
  console.error(`Usage: search-stock.mjs "query" [-n 5] [--deep] [--type market|sector|funding|hot|all]`);
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "-h" || args[0] === "--help") usage();

let query = "";
let n = 5;
let searchDepth = "basic";
let type = "all";

// 解析参数
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "-n") {
    n = Number.parseInt(args[i + 1] ?? "5", 10);
    i++;
    continue;
  }
  if (a === "--deep") {
    searchDepth = "advanced";
    continue;
  }
  if (a === "--type") {
    type = args[i + 1] ?? "all";
    i++;
    continue;
  }
  if (!a.startsWith("--")) {
    query = a;
  }
}

// 备用查询
const defaultQueries = {
  market: ["A股今日行情 上证指数", "今日股市走势 2026年3月"],
  sector: ["A股板块轮动 今日热点", "A股概念板块热度"],
  funding: ["A股北向资金 主力资金流向", "A股资金流向 今日"],
  hot: ["A股涨停板 龙头股", "A股热点概念今日表现"],
  all: ["A股行情分析 2026年3月", "今日A股市场分析"]
};

const queries = query ? [query] : (defaultQueries[type] || defaultQueries.all);

const apiKey = (process.env.TAVILY_API_KEY ?? "").trim();
if (!apiKey) {
  console.error("Missing TAVILY_API_KEY");
  process.exit(1);
}

async function searchTavily(q) {
  const body = {
    api_key: apiKey,
    query: q,
    search_depth: searchDepth,
    topic: "finance",
    max_results: Math.max(1, Math.min(n, 20)),
    include_answer: true,
    include_raw_content: false,
  };

  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Tavily Search failed (${resp.status}): ${text}`);
  }

  return resp.json();
}

// 主搜索
(async () => {
  try {
    const q = queries[0];
    const data = await searchTavily(q);
    
    // Print AI-generated answer if available
    if (data.answer) {
      console.log("## Answer\n");
      console.log(data.answer);
      console.log("\n---\n");
    }

    // Print results
    const results = (data.results ?? []).slice(0, n);
    console.log("## Sources\n");

    for (const r of results) {
      const title = String(r?.title ?? "").trim();
      const url = String(r?.url ?? "").trim();
      const content = String(r?.content ?? "").trim();
      const score = r?.score ? ` (relevance: ${(r.score * 100).toFixed(0)}%)` : "";
      
      if (!title || !url) continue;
      console.log(`- **${title}**${score}`);
      console.log(`  ${url}`);
      if (content) {
        console.log(`  ${content.slice(0, 300)}${content.length > 300 ? "..." : ""}`);
      }
      console.log();
    }
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
})();

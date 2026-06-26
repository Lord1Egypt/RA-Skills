import { callTool } from "./tool_router.js";

export async function research(query, context) {
  const data = await callTool("web_search", { query }, context);

  return {
    insights: summarize(data),
    raw: data
  };
}

function summarize(data) {
  if (!data) return "No data found";

  return JSON.stringify(data).slice(0, 300);
}
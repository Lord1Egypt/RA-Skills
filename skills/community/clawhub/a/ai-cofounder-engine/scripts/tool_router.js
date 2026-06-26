export async function callTool(toolName, input, context) {
  // context.tools = tools available via MCP / OpenClaw

  if (context?.tools?.[toolName]) {
    // Use user's tool
    return await context.tools[toolName](input);
  }

  // fallback logic
  if (toolName === "web_search") {
    return await fallbackSearch(input);
  }

  throw new Error("Tool not available");
}

// fallback (no API key required, but basic)
async function fallbackSearch(query) {
  const res = await fetch(`https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`);
  const data = await res.json();

  return {
    results: data.RelatedTopics || [],
    summary: data.AbstractText || ""
  };
}
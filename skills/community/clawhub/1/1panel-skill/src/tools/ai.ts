export const aiTools = [
  // AI Agent
  { name: "list_ai_agents", description: "List AI agents (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "create_ai_agent", description: "Create AI agent (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "update_ai_agent", description: "Update AI agent (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "delete_ai_agent", description: "Delete AI agent (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "reset_ai_agent_token", description: "Reset AI agent token (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "update_ai_agent_model", description: "Update AI agent model config (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" }, params: { type: "object" } }, required: ["id", "params"] } },
  // AI Agent Account
  { name: "list_ai_agent_accounts", description: "List AI agent accounts (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "create_ai_agent_account", description: "Create AI agent account (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "update_ai_agent_account", description: "Update AI agent account (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "delete_ai_agent_account", description: "Delete AI agent account (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "verify_ai_agent_account", description: "Verify AI agent account (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  // Channel Config
  { name: "get_ai_agent_browser_config", description: "Get AI agent browser config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" } }, required: ["agentId"] } },
  { name: "update_ai_agent_browser_config", description: "Update AI agent browser config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" }, params: { type: "object" } }, required: ["agentId", "params"] } },
  { name: "get_ai_agent_discord_config", description: "Get AI agent Discord config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" } }, required: ["agentId"] } },
  { name: "update_ai_agent_discord_config", description: "Update AI agent Discord config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" }, params: { type: "object" } }, required: ["agentId", "params"] } },
  { name: "get_ai_agent_feishu_config", description: "Get AI agent Feishu config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" } }, required: ["agentId"] } },
  { name: "update_ai_agent_feishu_config", description: "Update AI agent Feishu config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" }, params: { type: "object" } }, required: ["agentId", "params"] } },
  { name: "get_ai_agent_telegram_config", description: "Get AI agent Telegram config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" } }, required: ["agentId"] } },
  { name: "update_ai_agent_telegram_config", description: "Update AI agent Telegram config (XPack)", inputSchema: { type: "object", properties: { agentId: { type: "number" }, params: { type: "object" } }, required: ["agentId", "params"] } },
  // MCP Server
  { name: "list_mcp_servers", description: "List MCP servers (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "create_mcp_server", description: "Create MCP server (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "update_mcp_server", description: "Update MCP server (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" }, params: { type: "object" } }, required: ["id", "params"] } },
  { name: "delete_mcp_server", description: "Delete MCP server (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" } }, required: ["id"] } },
  { name: "operate_mcp_server", description: "Operate MCP server (XPack)", inputSchema: { type: "object", properties: { id: { type: "number" }, operation: { type: "string" } }, required: ["id", "operation"] } },
  { name: "get_mcp_domain", description: "Get MCP domain (XPack)", inputSchema: { type: "object", properties: {} } },
  { name: "bind_mcp_domain", description: "Bind MCP domain (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
  { name: "update_mcp_domain", description: "Update MCP domain (XPack)", inputSchema: { type: "object", properties: { params: { type: "object" } }, required: ["params"] } },
];

export async function handleAITool(client: any, name: string, args: any) {
  switch (name) {
    // AI Agent
    case "list_ai_agents": return await client.listAIAgents();
    case "create_ai_agent": return await client.createAIAgent(args?.params);
    case "update_ai_agent": return await client.updateAIAgent(args?.params);
    case "delete_ai_agent": return await client.deleteAIAgent(args?.id);
    case "reset_ai_agent_token": return await client.resetAIAgentToken(args?.id);
    case "update_ai_agent_model": return await client.updateAIAgentModel(args?.id, args?.params);
    // AI Agent Account
    case "list_ai_agent_accounts": return await client.listAIAgentAccounts();
    case "create_ai_agent_account": return await client.createAIAgentAccount(args?.params);
    case "update_ai_agent_account": return await client.updateAIAgentAccount(args?.params);
    case "delete_ai_agent_account": return await client.deleteAIAgentAccount(args?.id);
    case "verify_ai_agent_account": return await client.verifyAIAgentAccount(args?.params);
    // Channel Config
    case "get_ai_agent_browser_config": return await client.getAIAgentBrowserConfig(args?.agentId);
    case "update_ai_agent_browser_config": return await client.updateAIAgentBrowserConfig(args?.agentId, args?.params);
    case "get_ai_agent_discord_config": return await client.getAIAgentDiscordConfig(args?.agentId);
    case "update_ai_agent_discord_config": return await client.updateAIAgentDiscordConfig(args?.agentId, args?.params);
    case "get_ai_agent_feishu_config": return await client.getAIAgentFeishuConfig(args?.agentId);
    case "update_ai_agent_feishu_config": return await client.updateAIAgentFeishuConfig(args?.agentId, args?.params);
    case "get_ai_agent_telegram_config": return await client.getAIAgentTelegramConfig(args?.agentId);
    case "update_ai_agent_telegram_config": return await client.updateAIAgentTelegramConfig(args?.agentId, args?.params);
    // MCP Server
    case "list_mcp_servers": return await client.listMCPServers();
    case "create_mcp_server": return await client.createMCPServer(args?.params);
    case "update_mcp_server": return await client.updateMCPServer(args?.id, args?.params);
    case "delete_mcp_server": return await client.deleteMCPServer(args?.id);
    case "operate_mcp_server": return await client.operateMCPServer(args?.id, args?.operation);
    case "get_mcp_domain": return await client.getMCPDomain();
    case "bind_mcp_domain": return await client.bindMCPDomain(args?.params);
    case "update_mcp_domain": return await client.updateMCPDomain(args?.params);
    default: return null;
  }
}
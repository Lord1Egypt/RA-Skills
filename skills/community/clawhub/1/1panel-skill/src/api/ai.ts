import { BaseAPI } from "./base.js";

/**
 * AI Agent Management API (XPack)
 */
export class AIAPI extends BaseAPI {
  // ==================== AI Agents ====================

  /** Page Agents */
  async listAgents(params?: any): Promise<any> {
    return this.post("/api/v2/ai/agents/search", params || { page: 1, pageSize: 100 });
  }

  /** Create Agent */
  async createAgent(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents", params);
  }

  /** Delete Agent */
  async deleteAgent(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/delete", params);
  }

  /** Update Agent model config */
  async updateAgentModel(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/model/update", params);
  }

  /** Reset Agent token */
  async resetAgentToken(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/token/reset", params);
  }

  /** Get Providers */
  async getProviders(): Promise<any> {
    return this.get("/api/v2/ai/agents/providers");
  }

  // ==================== Agent Accounts ====================

  /** Page Agent accounts */
  async listAgentAccounts(params?: any): Promise<any> {
    return this.post("/api/v2/ai/agents/accounts/search", params || { page: 1, pageSize: 100 });
  }

  /** Create Agent account */
  async createAgentAccount(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/accounts", params);
  }

  /** Update Agent account */
  async updateAgentAccount(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/accounts/update", params);
  }

  /** Delete Agent account */
  async deleteAgentAccount(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/accounts/delete", params);
  }

  /** Verify Agent account */
  async verifyAgentAccount(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/accounts/verify", params);
  }

  // ==================== Agent Browser ====================

  /** Get Agent Browser config */
  async getAgentBrowserConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/browser/get", params);
  }

  /** Update Agent Browser config */
  async updateAgentBrowserConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/browser/update", params);
  }

  // ==================== Agent Channels ====================

  /** Get Agent Discord channel config */
  async getAgentDiscordConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/discord/get", params);
  }

  /** Update Agent Discord channel config */
  async updateAgentDiscordConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/discord/update", params);
  }

  /** Get Agent Feishu channel config */
  async getAgentFeishuConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/feishu/get", params);
  }

  /** Update Agent Feishu channel config */
  async updateAgentFeishuConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/feishu/update", params);
  }

  /** Approve Agent Feishu pairing code */
  async approveAgentFeishuPairing(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/feishu/approve", params);
  }

  /** Get Agent Telegram channel config */
  async getAgentTelegramConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/telegram/get", params);
  }

  /** Update Agent Telegram channel config */
  async updateAgentTelegramConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/telegram/update", params);
  }

  /** Approve Agent channel pairing code */
  async approveAgentChannelPairing(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/channel/pairing/approve", params);
  }

  /** Get Agent Other config */
  async getAgentOtherConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/other/get", params);
  }

  /** Update Agent Other config */
  async updateAgentOtherConfig(params: any): Promise<any> {
    return this.post("/api/v2/ai/agents/other/update", params);
  }

  // ==================== AI Domain ====================

  /** Bind domain */
  async bindDomain(params: any): Promise<any> {
    return this.post("/api/v2/ai/domain/bind", params);
  }

  /** Get bind domain */
  async getDomain(params: any): Promise<any> {
    return this.post("/api/v2/ai/domain/get", params);
  }

  // ==================== GPU ====================

  /** Load gpu / xpu info */
  async getGPUInfo(): Promise<any> {
    return this.get("/api/v2/ai/gpu/load");
  }

  // ==================== MCP Server ====================

  /** List mcp servers */
  async listMCPServers(params?: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/search", params || {});
  }

  /** Create mcp server */
  async createMCPServer(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/server", params);
  }

  /** Update mcp server */
  async updateMCPServer(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/server/update", params);
  }

  /** Delete mcp server */
  async deleteMCPServer(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/server/del", params);
  }

  /** Operate mcp server */
  async operateMCPServer(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/server/op", params);
  }

  /** Bind Domain for mcp server */
  async bindMCPDomain(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/domain/bind", params);
  }

  /** Get bin Domain for mcp server */
  async getMCPDomain(): Promise<any> {
    return this.get("/api/v2/ai/mcp/domain/get");
  }

  /** Update bind Domain for mcp server */
  async updateMCPDomain(params: any): Promise<any> {
    return this.post("/api/v2/ai/mcp/domain/update", params);
  }

  // ==================== Ollama ====================

  /** Page Ollama models */
  async listOllamaModels(params?: any): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/search", params || { page: 1, pageSize: 100 });
  }

  /** Create Ollama model */
  async createOllamaModel(params: any): Promise<any> {
    return this.post("/api/v2/ai/ollama/model", params);
  }

  /** Delete Ollama model */
  async deleteOllamaModel(params: any): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/del", params);
  }

  /** Rereate Ollama model */
  async recreateOllamaModel(params: any): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/recreate", params);
  }

  /** Sync Ollama model list */
  async syncOllamaModels(): Promise<any> {
    return this.post("/api/v2/ai/ollama/model/sync", {});
  }

  /** Close Ollama model conn */
  async closeOllamaModel(params: any): Promise<any> {
    return this.post("/api/v2/ai/ollama/close", params);
  }
}

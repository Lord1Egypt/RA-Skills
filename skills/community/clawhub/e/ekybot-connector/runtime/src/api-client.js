const chalk = require('chalk');

const fetchImpl = global.fetch
  ? (...args) => global.fetch(...args)
  : (...args) => require('node-fetch')(...args);

class EkybotApiClient {
  constructor(apiKey, apiUrl = 'https://api.ekybot.com') {
    this.apiKey = apiKey;
    this.apiUrl = apiUrl.replace(/\/$/, ''); // Remove trailing slash
    this.headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
      'User-Agent': 'ekybot-connector/1.0.0',
    };
  }

  async request(method, endpoint, data = null) {
    const url = `${this.apiUrl}${endpoint}`;
    const options = {
      method,
      headers: this.headers,
      timeout: 30000,
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetchImpl(url, options);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `API request failed: ${response.status} ${response.statusText} - ${errorText}`
        );
      }

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error(chalk.red(`API Error: ${error.message}`));
      throw error;
    }
  }

  // Workspace management
  async registerWorkspace(workspaceName) {
    return this.request('POST', '/v1/workspaces', {
      name: workspaceName,
      type: 'openclaw',
      connector_version: '1.0.0',
    });
  }

  async getWorkspaceInfo(workspaceId) {
    return this.request('GET', `/v1/workspaces/${workspaceId}`);
  }

  async updateWorkspaceStatus(workspaceId, status) {
    return this.request('PATCH', `/v1/workspaces/${workspaceId}`, {
      status: status,
      last_seen: new Date().toISOString(),
    });
  }

  // Agent management
  async registerAgent(workspaceId, agentData) {
    return this.request('POST', `/v1/workspaces/${workspaceId}/agents`, agentData);
  }

  async updateAgentStatus(workspaceId, agentId, status) {
    return this.request('PATCH', `/v1/workspaces/${workspaceId}/agents/${agentId}`, {
      status: status,
      last_seen: new Date().toISOString(),
    });
  }

  // Telemetry
  async sendTelemetry(workspaceId, telemetryData) {
    return this.request('POST', `/v1/workspaces/${workspaceId}/telemetry`, {
      timestamp: new Date().toISOString(),
      ...telemetryData,
    });
  }

  async sendBatchTelemetry(workspaceId, telemetryBatch) {
    return this.request('POST', `/v1/workspaces/${workspaceId}/telemetry/batch`, {
      data: telemetryBatch,
    });
  }

  // Health check
  async healthCheck() {
    try {
      const response = await this.request('GET', '/v1/health');
      return response;
    } catch (error) {
      return { status: 'error', error: error.message };
    }
  }

  // Authentication validation
  async validateApiKey() {
    try {
      const response = await this.request('GET', '/v1/auth/validate');
      return response;
    } catch (error) {
      throw new Error(`API key validation failed: ${error.message}`);
    }
  }
}

module.exports = EkybotApiClient;

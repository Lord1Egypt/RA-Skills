const fs = require('fs');
const path = require('path');
const os = require('os');
const chalk = require('chalk');
const EkybotApiClient = require('./api-client');

let WebSocket = null;

try {
  WebSocket = require('ws');
} catch (error) {
  WebSocket = null;
}

class TelemetryCollector {
  constructor(apiKey, workspaceId, options = {}) {
    this.apiClient = new EkybotApiClient(apiKey);
    this.workspaceId = workspaceId;
    this.interval = options.interval || parseInt(process.env.TELEMETRY_INTERVAL) || 60000;
    this.isRunning = false;
    this.intervalId = null;
    this.telemetryBuffer = [];
    this.maxBufferSize = 100;

    // WebSocket connection for real-time streaming (disabled by default)
    this.ws = null;
    this.wsUrl = options.wsUrl || process.env.EKYBOT_WS_URL || 'wss://api.ekybot.com/ws';
    this.enableWebSocket = options.enableWebSocket || false; // Opt-in only
    this.wsReconnectAttempts = 0;
    this.wsMaxReconnectAttempts = 50;
    this.wsBaseDelay = 5000; // 5s initial
    this.wsMaxDelay = 300000; // 5min cap
  }

  // Start telemetry collection
  async start() {
    if (this.isRunning) {
      console.log(chalk.yellow('Telemetry collector already running'));
      return;
    }

    try {
      // Validate API connectivity
      await this.apiClient.healthCheck();
      console.log(chalk.green('✓ Connected to Ekybot API'));

      // Start collection interval
      this.isRunning = true;
      this.intervalId = setInterval(() => {
        this.collectAndSend();
      }, this.interval);

      // Initialize WebSocket for real-time updates (only if enabled)
      if (this.enableWebSocket) {
        this.initializeWebSocket();
        console.log(
          chalk.green(
            `✓ Telemetry collection started (HTTP + WebSocket, interval: ${this.interval}ms)`
          )
        );
      } else {
        console.log(
          chalk.green(`✓ Telemetry collection started (HTTP-only, interval: ${this.interval}ms)`)
        );
        console.log(chalk.blue('💡 Use --websocket flag to enable real-time streaming'));
      }
    } catch (error) {
      console.error(chalk.red(`Failed to start telemetry: ${error.message}`));
      throw error;
    }
  }

  // Stop telemetry collection
  stop() {
    if (!this.isRunning) {
      console.log(chalk.yellow('Telemetry collector not running'));
      return;
    }

    this.isRunning = false;

    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    console.log(chalk.green('✓ Telemetry collection stopped'));
  }

  // Initialize WebSocket connection for real-time streaming
  initializeWebSocket() {
    if (!WebSocket) {
      console.error(chalk.red('WebSocket dependency is not installed'));
      return;
    }

    try {
      this.ws = new WebSocket(this.wsUrl, {
        headers: {
          Authorization: `Bearer ${this.apiClient.apiKey}`,
          'X-Workspace-ID': this.workspaceId,
        },
      });

      this.ws.on('open', () => {
        console.log(chalk.green('✓ Real-time telemetry connection established'));
        this.wsReconnectAttempts = 0; // Reset on successful connection
      });

      this.ws.on('error', (error) => {
        console.error(chalk.red(`WebSocket error: ${error.message}`));
      });

      this.ws.on('close', () => {
        console.log(chalk.yellow('WebSocket connection closed'));

        // Reconnect with exponential backoff and max attempts
        if (this.isRunning && this.wsReconnectAttempts < this.wsMaxReconnectAttempts) {
          this.wsReconnectAttempts++;
          const delay = Math.min(this.wsBaseDelay * Math.pow(2, this.wsReconnectAttempts - 1), this.wsMaxDelay);
          console.log(chalk.blue(`Reconnecting WebSocket in ${delay/1000}s (attempt ${this.wsReconnectAttempts}/${this.wsMaxReconnectAttempts})...`));
          setTimeout(() => {
            this.initializeWebSocket();
          }, delay);
        } else if (this.wsReconnectAttempts >= this.wsMaxReconnectAttempts) {
          console.error(chalk.red(`WebSocket reconnection limit reached (${this.wsMaxReconnectAttempts}). Giving up. HTTP telemetry continues.`));
        }
      });
    } catch (error) {
      console.error(chalk.red(`Failed to initialize WebSocket: ${error.message}`));
    }
  }

  // Collect telemetry data and send to Ekybot
  async collectAndSend() {
    try {
      const telemetryData = await this.collectTelemetryData();

      if (telemetryData && Object.keys(telemetryData).length > 0) {
        // Send via HTTP API
        await this.apiClient.sendTelemetry(this.workspaceId, telemetryData);

        // Send via WebSocket for real-time updates (only if WebSocket enabled)
        if (this.enableWebSocket && this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(
            JSON.stringify({
              type: 'telemetry',
              data: telemetryData,
            })
          );
        }

        const mode = this.enableWebSocket ? '(HTTP+WS)' : '(HTTP)';
        console.log(
          chalk.blue(
            `📊 Telemetry sent ${mode} (${Object.keys(telemetryData.agents || {}).length} agents)`
          )
        );
      }
    } catch (error) {
      console.error(chalk.red(`Telemetry collection failed: ${error.message}`));

      // Buffer data for retry if API is down
      const telemetryData = await this.collectTelemetryData().catch(() => null);
      if (telemetryData) {
        this.bufferTelemetry(telemetryData);
      }
    }
  }

  // Collect actual telemetry data from OpenClaw
  async collectTelemetryData() {
    const agentsPath =
      process.env.OPENCLAW_AGENTS_PATH || path.join(os.homedir(), '.openclaw', 'agents');

    const telemetryData = {
      timestamp: new Date().toISOString(),
      system: await this.collectSystemMetrics(),
      agents: {},
      workspace: {
        status: 'active',
        connector_version: '1.0.0',
      },
    };

    // Collect agent data if agents directory exists
    if (fs.existsSync(agentsPath)) {
      const agents = fs.readdirSync(agentsPath);

      for (const agentDir of agents) {
        const agentPath = path.join(agentsPath, agentDir);
        if (fs.statSync(agentPath).isDirectory()) {
          telemetryData.agents[agentDir] = await this.collectAgentMetrics(agentPath);
        }
      }
    }

    return telemetryData;
  }

  // Collect system-level metrics (minimal — no fingerprinting)
  async collectSystemMetrics() {
    return {
      platform: os.platform(),
      node_version: process.version,
      uptime: Math.floor(process.uptime()),
      memory: {
        connector_heap_used: process.memoryUsage().heapUsed,
        connector_heap_total: process.memoryUsage().heapTotal,
        // System RAM/CPU details removed — not needed for monitoring,
        // and constitutes machine fingerprinting per audit recommendation
      },
    };
  }

  // Collect metrics for a specific agent
  async collectAgentMetrics(agentPath) {
    const agentMetrics = {
      status: 'unknown',
      last_activity: null,
      session_count: 0,
      total_messages: 0,
      cost_tracking: {
        total_tokens: 0,
        estimated_cost: 0,
      },
    };

    try {
      // Check for session files
      const sessionsPath = path.join(agentPath, 'sessions');
      if (fs.existsSync(sessionsPath)) {
        const sessionFiles = fs.readdirSync(sessionsPath).filter((f) => f.endsWith('.jsonl'));
        agentMetrics.session_count = sessionFiles.length;

        // Parse session data for metrics
        for (const sessionFile of sessionFiles) {
          const sessionPath = path.join(sessionsPath, sessionFile);
          try {
            const sessionData = fs.readFileSync(sessionPath, 'utf8');
            const lines = sessionData
              .trim()
              .split('\n')
              .filter((line) => line.trim());
            agentMetrics.total_messages += lines.length;

            // Get last activity from most recent message
            if (lines.length > 0) {
              const lastMessage = JSON.parse(lines[lines.length - 1]);
              if (lastMessage.timestamp) {
                const messageTime = new Date(lastMessage.timestamp);
                if (
                  !agentMetrics.last_activity ||
                  messageTime > new Date(agentMetrics.last_activity)
                ) {
                  agentMetrics.last_activity = lastMessage.timestamp;
                }
              }
            }
          } catch (error) {
            // Skip corrupted session files
          }
        }
      }

      // Determine agent status based on recent activity
      if (agentMetrics.last_activity) {
        const lastActivityTime = new Date(agentMetrics.last_activity);
        const timeSinceLastActivity = Date.now() - lastActivityTime.getTime();

        if (timeSinceLastActivity < 5 * 60 * 1000) {
          // 5 minutes
          agentMetrics.status = 'active';
        } else if (timeSinceLastActivity < 60 * 60 * 1000) {
          // 1 hour
          agentMetrics.status = 'idle';
        } else {
          agentMetrics.status = 'inactive';
        }
      }
    } catch (error) {
      console.warn(chalk.yellow(`Warning: Could not collect metrics for agent at ${agentPath}`));
    }

    return agentMetrics;
  }

  // Buffer telemetry data for later transmission
  bufferTelemetry(data) {
    this.telemetryBuffer.push({
      ...data,
      buffered_at: new Date().toISOString(),
    });

    // Keep buffer size manageable
    if (this.telemetryBuffer.length > this.maxBufferSize) {
      this.telemetryBuffer.shift(); // Remove oldest entry
    }

    console.log(chalk.yellow(`📦 Buffered telemetry (${this.telemetryBuffer.length} pending)`));
  }

  // Send buffered telemetry data
  async sendBufferedTelemetry() {
    if (this.telemetryBuffer.length === 0) {
      return;
    }

    try {
      await this.apiClient.sendBatchTelemetry(this.workspaceId, this.telemetryBuffer);
      console.log(chalk.green(`✓ Sent ${this.telemetryBuffer.length} buffered telemetry entries`));
      this.telemetryBuffer = [];
    } catch (error) {
      console.error(chalk.red(`Failed to send buffered telemetry: ${error.message}`));
    }
  }

  // Get current status
  getStatus() {
    return {
      running: this.isRunning,
      interval: this.interval,
      workspace_id: this.workspaceId,
      websocket_connected: this.ws && this.ws.readyState === WebSocket.OPEN,
      buffered_entries: this.telemetryBuffer.length,
    };
  }
}

module.exports = TelemetryCollector;

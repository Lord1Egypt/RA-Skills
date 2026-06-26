const chalk = require('chalk');
const WebSocket = require('ws');

function resolveRelayPushUrl(baseUrl) {
  const raw = process.env.EKYBOT_RELAY_PUSH_URL || baseUrl || '';
  if (!raw) {
    return null;
  }

  const normalized = raw.replace(/\/$/, '');
  if (normalized.startsWith('ws://') || normalized.startsWith('wss://')) {
    return normalized;
  }
  if (normalized.startsWith('https://')) {
    return normalized.replace(/^https:\/\//, 'wss://');
  }
  if (normalized.startsWith('http://')) {
    return normalized.replace(/^http:\/\//, 'ws://');
  }
  return null;
}

class EkybotCompanionRelaySocket {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || process.env.EKYBOT_APP_URL || 'https://www.ekybot.com';
    this.machineId = options.machineId;
    this.machineApiKey = options.machineApiKey;
    this.onWake = typeof options.onWake === 'function' ? options.onWake : async () => {};
    this.ws = null;
    this.running = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 100;
    this.baseDelayMs = 1_000;
    this.maxDelayMs = 30_000;
  }

  connect() {
    const relayPushUrl = resolveRelayPushUrl(this.baseUrl);
    if (!relayPushUrl || !this.machineId || !this.machineApiKey) {
      console.log(chalk.gray('[relay-push] disabled (missing url or machine credentials)'));
      return;
    }

    this.running = true;
    this.open(relayPushUrl);
  }

  stop() {
    this.running = false;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  open(relayPushUrl) {
    const url = `${relayPushUrl}/relay-push/companion?machineId=${encodeURIComponent(this.machineId)}`;
    this.ws = new WebSocket(url, {
      headers: {
        'x-companion-api-key': this.machineApiKey,
      },
    });

    this.ws.on('open', () => {
      this.reconnectAttempts = 0;
      console.log(chalk.green(`[relay-push] connected machine=${this.machineId}`));
      this.send({
        protocolVersion: '2026-03-13',
        type: 'companion.connect',
        machineId: this.machineId,
        connectedAt: new Date().toISOString(),
      });
    });

    this.ws.on('message', async (raw) => {
      try {
        const message = JSON.parse(String(raw));
        if (message?.type === 'relay.wake') {
          console.log(
            chalk.blue(
              `[relay-push] wake notification=${message.notificationId} request=${message.requestId || 'n/a'}`,
            ),
          );
          this.send({
            protocolVersion: '2026-03-13',
            type: 'relay.ack',
            machineId: this.machineId,
            notificationId: typeof message.notificationId === 'string' ? message.notificationId : undefined,
            requestId: typeof message.requestId === 'string' ? message.requestId : undefined,
            receivedAt: new Date().toISOString(),
          });
          await this.onWake(message);
        }
      } catch (error) {
        console.warn(chalk.yellow(`[relay-push] invalid message: ${error.message}`));
      }
    });

    this.ws.on('close', () => {
      console.log(chalk.yellow('[relay-push] connection closed'));
      this.ws = null;
      this.scheduleReconnect(relayPushUrl);
    });

    this.ws.on('error', (error) => {
      console.warn(chalk.yellow(`[relay-push] socket error: ${error.message}`));
    });
  }

  scheduleReconnect(relayPushUrl) {
    if (!this.running || this.reconnectAttempts >= this.maxReconnectAttempts) {
      return;
    }

    this.reconnectAttempts += 1;
    const delayMs = Math.min(this.baseDelayMs * 2 ** (this.reconnectAttempts - 1), this.maxDelayMs);
    setTimeout(() => {
      if (this.running) {
        this.open(relayPushUrl);
      }
    }, delayMs);
  }

  send(payload) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(payload));
    }
  }
}

module.exports = EkybotCompanionRelaySocket;

/**
 * Bitchat Bridge
 *
 * Handles communication with the bitchat-node HTTP bridge.
 * Supports both polling and WebSocket connections for real-time messages.
 */

import type { BitchatInboundMessage } from './index.js';
import type { Logger } from './types.js';

export interface BridgeOptions {
  bridgeUrl: string;
  nickname: string;
  onMessage: (msg: BitchatInboundMessage) => Promise<void>;
  logger: Logger;
  pollIntervalMs?: number;
}

interface BridgeStatus {
  connected: boolean;
  peerID?: string;
  nickname?: string;
  peersCount?: number;
}

interface PendingMessage {
  id: string;
  type: 'public' | 'direct';
  senderPeerID: string;
  senderNickname: string;
  text: string;
  timestamp: number;
}

export class BitchatBridge {
  private readonly bridgeUrl: string;
  private readonly onMessage: (msg: BitchatInboundMessage) => Promise<void>;
  private readonly logger: Logger;
  private readonly pollIntervalMs: number;

  private connected = false;
  private pollTimer: ReturnType<typeof setInterval> | null = null;
  private lastMessageTimestamp = 0;
  private ws: WebSocket | null = null;

  constructor(options: BridgeOptions) {
    this.bridgeUrl = options.bridgeUrl.replace(/\/$/, ''); // Remove trailing slash
    this.onMessage = options.onMessage;
    this.logger = options.logger;
    this.pollIntervalMs = options.pollIntervalMs ?? 2000;
  }

  /**
   * Connect to the bitchat-node bridge
   */
  async connect(): Promise<void> {
    // First, verify the bridge is reachable
    try {
      const status = await this.getStatus();
      this.logger.info(`[bitchat-bridge] Connected to bridge. PeerID: ${status.peerID}`);
      this.connected = true;
    } catch (err) {
      this.logger.error('[bitchat-bridge] Failed to connect to bridge:', err);
      throw err;
    }

    // Try WebSocket first, fall back to polling
    const wsUrl = this.bridgeUrl.replace(/^http/, 'ws') + '/ws';
    try {
      await this.connectWebSocket(wsUrl);
      this.logger.info('[bitchat-bridge] WebSocket connected');
    } catch {
      this.logger.info('[bitchat-bridge] WebSocket unavailable, using polling');
      this.startPolling();
    }
  }

  /**
   * Disconnect from the bridge
   */
  async disconnect(): Promise<void> {
    this.connected = false;
    
    if (this.pollTimer) {
      clearInterval(this.pollTimer);
      this.pollTimer = null;
    }
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.connected;
  }

  /**
   * Get bridge status
   */
  async getStatus(): Promise<BridgeStatus> {
    const response = await fetch(`${this.bridgeUrl}/api/status`);
    if (!response.ok) {
      throw new Error(`Bridge status failed: ${response.status}`);
    }
    return response.json() as Promise<BridgeStatus>;
  }

  /**
   * Send a public message to all peers
   */
  async sendPublicMessage(text: string): Promise<void> {
    const response = await fetch(`${this.bridgeUrl}/api/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'public', text }),
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to send public message: ${error}`);
    }
  }

  /**
   * Send a direct message to a specific peer
   */
  async sendDirectMessage(recipientPeerID: string, text: string): Promise<void> {
    const response = await fetch(`${this.bridgeUrl}/api/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'direct', recipientPeerID, text }),
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to send direct message: ${error}`);
    }
  }

  /**
   * Get list of known peers
   */
  async getPeers(): Promise<{ peerID: string; nickname: string; lastSeen: number }[]> {
    const response = await fetch(`${this.bridgeUrl}/api/peers`);
    if (!response.ok) {
      throw new Error(`Failed to get peers: ${response.status}`);
    }
    return response.json() as Promise<{ peerID: string; nickname: string; lastSeen: number }[]>;
  }

  /**
   * Get recent messages (for polling)
   */
  async getMessages(since?: number): Promise<PendingMessage[]> {
    const url = since
      ? `${this.bridgeUrl}/api/messages?since=${since}`
      : `${this.bridgeUrl}/api/messages`;
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to get messages: ${response.status}`);
    }
    return response.json() as Promise<PendingMessage[]>;
  }

  /**
   * Register webhook for incoming messages
   */
  async registerWebhook(webhookUrl: string): Promise<void> {
    const response = await fetch(`${this.bridgeUrl}/api/webhook`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: webhookUrl }),
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to register webhook: ${error}`);
    }
  }

  /**
   * Connect via WebSocket for real-time messages
   */
  private async connectWebSocket(wsUrl: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // Note: In Node.js, we'd use the 'ws' package
        // This is a simplified version that may need adjustment
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        const WebSocketImpl = typeof WebSocket !== 'undefined' ? WebSocket : require('ws');
        const ws = new WebSocketImpl(wsUrl) as WebSocket;
        this.ws = ws;
        
        const timeout = setTimeout(() => {
          reject(new Error('WebSocket connection timeout'));
        }, 5000);

        ws.onopen = () => {
          clearTimeout(timeout);
          resolve();
        };

        ws.onerror = (err: Event) => {
          clearTimeout(timeout);
          reject(err);
        };

        ws.onmessage = async (event: MessageEvent) => {
          try {
            const data = JSON.parse(String(event.data));
            if (data.type === 'message') {
              await this.onMessage({
                type: data.isDirect ? 'direct' : 'public',
                senderPeerID: data.senderPeerID,
                senderNickname: data.senderNickname,
                text: data.text,
                timestamp: data.timestamp,
                messageId: data.id ?? `ws-${Date.now()}`,
              });
            }
          } catch (err) {
            this.logger.error('[bitchat-bridge] WebSocket message parse error:', err);
          }
        };

        ws.onclose = () => {
          this.logger.info('[bitchat-bridge] WebSocket closed');
          this.ws = null;
          // Reconnect or fall back to polling
          if (this.connected) {
            this.startPolling();
          }
        };
      } catch (err) {
        reject(err);
      }
    });
  }

  /**
   * Start polling for messages
   */
  private startPolling(): void {
    if (this.pollTimer) {
      return; // Already polling
    }

    this.logger.info(`[bitchat-bridge] Starting message polling (${this.pollIntervalMs}ms)`);
    
    this.pollTimer = setInterval(async () => {
      if (!this.connected) {
        return;
      }
      
      try {
        const messages = await this.getMessages(this.lastMessageTimestamp);
        
        for (const msg of messages) {
          // Update timestamp to avoid duplicates
          if (msg.timestamp > this.lastMessageTimestamp) {
            this.lastMessageTimestamp = msg.timestamp;
          }
          
          await this.onMessage({
            type: msg.type,
            senderPeerID: msg.senderPeerID,
            senderNickname: msg.senderNickname,
            text: msg.text,
            timestamp: msg.timestamp,
            messageId: msg.id,
          });
        }
      } catch (err) {
        this.logger.error('[bitchat-bridge] Poll error:', err);
      }
    }, this.pollIntervalMs);
  }
}

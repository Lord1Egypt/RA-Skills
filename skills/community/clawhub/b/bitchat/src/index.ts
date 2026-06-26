/**
 * @openclaw/bitchat - Bitchat BLE Mesh Channel Plugin
 *
 * This plugin enables OpenClaw to communicate via the Bitchat
 * peer-to-peer BLE mesh network.
 *
 * Architecture:
 * - bitchat-node runs as a background service (separate process)
 * - This plugin communicates with it via HTTP bridge
 * - Inbound: webhook from bitchat-node → OpenClaw session
 * - Outbound: OpenClaw → HTTP API → bitchat-node → BLE mesh
 */

import type { PluginApi, ChannelPlugin } from './types.js';
import { BitchatBridge } from './bridge.js';

// Plugin configuration interface
export interface BitchatConfig {
  enabled?: boolean;
  nickname?: string;
  bridgeUrl?: string;
  webhookPath?: string;
  autoStart?: boolean;
  dmPolicy?: 'open' | 'allowlist' | 'disabled';
  allowFrom?: string[];
}

// Message from bitchat-node
export interface BitchatInboundMessage {
  type: 'public' | 'direct';
  senderPeerID: string;
  senderNickname: string;
  text: string;
  timestamp: number;
  messageId: string;
}

// Default config values
const DEFAULT_CONFIG: Required<BitchatConfig> = {
  enabled: true,
  nickname: 'openclaw',
  bridgeUrl: 'http://localhost:3939',
  webhookPath: '/bitchat-webhook',
  autoStart: false,
  dmPolicy: 'open',
  allowFrom: [],
};

// Bridge instance (singleton for the gateway)
let bridge: BitchatBridge | null = null;

/**
 * Resolve channel config from OpenClaw config
 */
function resolveConfig(cfg: Record<string, unknown>): Required<BitchatConfig> {
  const channelConfig = (cfg.channels as Record<string, unknown>)?.bitchat as BitchatConfig | undefined;
  return {
    ...DEFAULT_CONFIG,
    ...channelConfig,
  };
}

/**
 * Check if a sender is allowed based on policy
 */
function isSenderAllowed(config: Required<BitchatConfig>, senderPeerID: string): boolean {
  switch (config.dmPolicy) {
    case 'disabled':
      return false;
    case 'allowlist':
      return config.allowFrom.includes(senderPeerID) || config.allowFrom.includes('*');
    case 'open':
    default:
      return true;
  }
}

/**
 * Create the Bitchat channel plugin
 */
function createBitchatPlugin(): ChannelPlugin {
  return {
    id: 'bitchat',
    meta: {
      id: 'bitchat',
      label: 'Bitchat',
      selectionLabel: 'Bitchat (BLE Mesh)',
      docsPath: '/channels/bitchat',
      docsLabel: 'bitchat',
      blurb: 'Peer-to-peer BLE mesh network messaging.',
      aliases: ['ble', 'mesh'],
    },
    capabilities: {
      chatTypes: ['direct', 'group'] as const,
      media: false, // BLE bandwidth is limited
    },
    config: {
      listAccountIds: () => ['default'],
      resolveAccount: (cfg: Record<string, unknown>, accountId?: string) => {
        const config = resolveConfig(cfg);
        return {
          accountId: accountId ?? 'default',
          enabled: config.enabled,
          configured: Boolean(config.bridgeUrl),
          config,
        };
      },
      defaultAccountId: () => 'default',
      isConfigured: (account: { configured?: boolean }) => account.configured ?? false,
      describeAccount: (account: { accountId: string; enabled?: boolean; configured?: boolean }) => ({
        accountId: account.accountId,
        enabled: account.enabled ?? true,
        configured: account.configured ?? false,
      }),
    },
    security: {
      resolveDmPolicy: ({ account }) => ({
        policy: String(account.config?.dmPolicy ?? 'open'),
        allowFrom: (account.config?.allowFrom as string[]) ?? [],
        policyPath: 'channels.bitchat.dmPolicy',
        allowFromPath: 'channels.bitchat.allowFrom',
        approveHint: 'Add peer ID to channels.bitchat.allowFrom',
        normalizeEntry: (raw: string) => raw.trim().toLowerCase(),
      }),
    },
    messaging: {
      normalizeTarget: ({ target }) => {
        // Accept peer ID or nickname
        const cleaned = target.replace(/^bitchat:/i, '').trim();
        return { target: cleaned, normalized: cleaned };
      },
      targetResolver: {
        looksLikeId: (target: string) => /^[a-f0-9]{16}$/i.test(target),
        hint: '<peerID|nickname>',
      },
    },
    outbound: {
      deliveryMode: 'direct',
      sendText: async ({ text, target }) => {
        
        if (!bridge) {
          return { ok: false, error: 'Bitchat bridge not initialized' };
        }

        try {
          // Determine if this is a DM or public message
          const isDirect = target && target !== 'public' && target !== '*';
          
          if (isDirect) {
            await bridge.sendDirectMessage(target, text);
          } else {
            await bridge.sendPublicMessage(text);
          }
          
          return { ok: true };
        } catch (err) {
          const error = err instanceof Error ? err.message : String(err);
          return { ok: false, error };
        }
      },
    },
  };
}

/**
 * Main plugin registration
 */
export default function register(api: PluginApi): void {
  const logger = api.logger;
  
  // Register the channel
  const plugin = createBitchatPlugin();
  api.registerChannel({ plugin });
  
  // Register background service to manage bridge connection
  api.registerService({
    id: 'bitchat-bridge',
    start: async () => {
      const cfg = api.config as Record<string, unknown>;
      const config = resolveConfig(cfg);
      
      if (!config.enabled) {
        logger.info('[bitchat] Channel disabled');
        return;
      }
      
      logger.info(`[bitchat] Starting bridge connection to ${config.bridgeUrl}`);
      
      bridge = new BitchatBridge({
        bridgeUrl: config.bridgeUrl,
        nickname: config.nickname,
        onMessage: async (msg: BitchatInboundMessage) => {
          // Check if sender is allowed
          if (!isSenderAllowed(config, msg.senderPeerID)) {
            logger.debug(`[bitchat] Ignoring message from unauthorized peer: ${msg.senderPeerID}`);
            return;
          }
          
          // Route message to OpenClaw session
          try {
            await api.injectMessage({
              channel: 'bitchat',
              senderId: msg.senderPeerID,
              senderName: msg.senderNickname,
              text: msg.text,
              messageId: msg.messageId,
              chatType: msg.type === 'direct' ? 'direct' : 'group',
              timestamp: msg.timestamp,
            });
          } catch (err) {
            logger.error('[bitchat] Failed to inject message:', err);
          }
        },
        logger,
      });
      
      await bridge.connect();
      logger.info('[bitchat] Bridge connected');
    },
    stop: async () => {
      if (bridge) {
        await bridge.disconnect();
        bridge = null;
        logger.info('[bitchat] Bridge disconnected');
      }
    },
  });
  
  // Register webhook handler for inbound messages
  api.registerHttpHandler({
    method: 'POST',
    path: '/bitchat-webhook',
    handler: async (req, res) => {
      try {
        const body = req.body as BitchatInboundMessage;
        
        if (!body || !body.senderPeerID || !body.text) {
          res.status(400).json({ error: 'Invalid message format' });
          return;
        }
        
        const cfg = api.config as Record<string, unknown>;
        const config = resolveConfig(cfg);
        
        if (!isSenderAllowed(config, body.senderPeerID)) {
          res.status(403).json({ error: 'Sender not allowed' });
          return;
        }
        
        await api.injectMessage({
          channel: 'bitchat',
          senderId: body.senderPeerID,
          senderName: body.senderNickname,
          text: body.text,
          messageId: body.messageId,
          chatType: body.type === 'direct' ? 'direct' : 'group',
          timestamp: body.timestamp,
        });
        
        res.json({ ok: true });
      } catch (err) {
        logger.error('[bitchat] Webhook error:', err);
        res.status(500).json({ error: 'Internal error' });
      }
    },
  });
  
  // Register RPC methods for status
  api.registerGatewayMethod('bitchat.status', async ({ respond }) => {
    const cfg = api.config as Record<string, unknown>;
    const config = resolveConfig(cfg);
    
    const status = {
      enabled: config.enabled,
      bridgeUrl: config.bridgeUrl,
      connected: bridge?.isConnected() ?? false,
      nickname: config.nickname,
      dmPolicy: config.dmPolicy,
    };
    
    respond(true, status);
  });
  
  logger.info('[bitchat] Plugin registered');
}

// Export types
export type { PluginApi, ChannelPlugin };

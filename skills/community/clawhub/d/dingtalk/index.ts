// DingTalk channel plugin for OpenClaw
// Based on Feishu plugin structure

import type {
  ChannelPlugin,
  ChannelPluginContext,
  InboundMessage,
  OutboundMessage,
  MessageContent,
  PluginMetadata,
} from "openclaw/plugin-sdk";

export interface DingTalkConfig {
  enabled?: boolean;
  clientId?: string;
  clientSecret?: string;
  appKey?: string;
  appSecret?: string;
  webhookSecret?: string;
  robotCode?: string;
  dmPolicy?: "open" | "allowlist" | "pairing" | "disabled";
  allowFrom?: string[];
  groupPolicy?: "open" | "allowlist" | "disabled";
  groupAllowFrom?: string[];
  encryptKey?: string;
  webhookUrl?: string;
}

const metadata: PluginMetadata = {
  id: "dingtalk",
  name: "DingTalk",
  version: "0.1.0",
  description: "OpenClaw DingTalk channel plugin for enterprise messaging",
  author: "OpenClaw Community",
};

export function resolveDingTalkCredentials(
  cfg: DingTalkConfig | undefined
): { clientId: string; clientSecret: string } | null {
  if (!cfg) return null;
  
  // Support both new OAuth2 (clientId/clientSecret) and old appKey/appSecret
  const clientId = cfg.clientId?.trim() || cfg.appKey?.trim() || process.env.DINGTALK_CLIENT_ID?.trim() || process.env.DINGTALK_APP_KEY?.trim();
  const clientSecret = cfg.clientSecret?.trim() || cfg.appSecret?.trim() || process.env.DINGTALK_CLIENT_SECRET?.trim() || process.env.DINGTALK_APP_SECRET?.trim();
  
  if (!clientId || !clientSecret) return null;
  return { clientId, clientSecret };
}

// Get access token from DingTalk
async function getAccessToken(
  clientId: string,
  clientSecret: string
): Promise<string | null> {
  try {
    const response = await fetch(
      `https://oapi.dingtalk.com/gettoken?appkey=${encodeURIComponent(clientId)}&appsecret=${encodeURIComponent(clientSecret)}`,
      { method: "GET" }
    );
    
    if (!response.ok) {
      console.error("DingTalk token request failed:", response.status);
      return null;
    }
    
    const data = await response.json();
    if (data.errcode !== 0) {
      console.error("DingTalk API error:", data.errmsg);
      return null;
    }
    
    return data.access_token;
  } catch (error) {
    console.error("Failed to get DingTalk access token:", error);
    return null;
  }
}

// Send text message to user
async function sendTextMessage(
  accessToken: string,
  userId: string,
  content: string
): Promise<boolean> {
  try {
    const response = await fetch(
      `https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=${accessToken}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userid_list: userId,
          msg: {
            msgtype: "text",
            text: { content },
          },
        }),
      }
    );
    
    const data = await response.json();
    return data.errcode === 0;
  } catch (error) {
    console.error("Failed to send DingTalk message:", error);
    return false;
  }
}

// Send message via webhook (for group robots)
async function sendWebhookMessage(
  webhookUrl: string,
  secret: string | undefined,
  content: string
): Promise<boolean> {
  try {
    let url = webhookUrl;
    
    // Add signature if secret is provided
    if (secret) {
      const timestamp = Date.now();
      const signature = await generateSignature(timestamp, secret);
      url = `${webhookUrl}&timestamp=${timestamp}&sign=${signature}`;
    }
    
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        msgtype: "text",
        text: { content },
      }),
    });
    
    const data = await response.json();
    return data.errcode === 0 || data.errmsg === "ok";
  } catch (error) {
    console.error("Failed to send DingTalk webhook message:", error);
    return false;
  }
}

// Generate signature for webhook
async function generateSignature(timestamp: number, secret: string): Promise<string> {
  const crypto = await import("crypto");
  const stringToSign = `${timestamp}\n${secret}`;
  const hmac = crypto.createHmac("sha256", secret);
  hmac.update(stringToSign);
  return encodeURIComponent(Buffer.from(hmac.digest()).toString("base64"));
}

export const dingtalkPlugin: ChannelPlugin<DingTalkConfig> = {
  metadata,

  async initialize(ctx: ChannelPluginContext<DingTalkConfig>): Promise<void> {
    const cfg = ctx.config;
    const creds = resolveDingTalkCredentials(cfg);
    
    if (!creds) {
      console.log("DingTalk: No credentials configured");
      return;
    }
    
    console.log(`DingTalk: Initializing with clientId ${creds.clientId.substring(0, 8)}...`);
    
    // Test connection
    const token = await getAccessToken(creds.clientId, creds.clientSecret);
    if (token) {
      console.log("DingTalk: Connected successfully");
    } else {
      console.error("DingTalk: Failed to connect - check credentials");
    }
  },

  async send(
    ctx: ChannelPluginContext<DingTalkConfig>,
    message: OutboundMessage
  ): Promise<void> {
    const cfg = ctx.config;
    const creds = resolveDingTalkCredentials(cfg);
    
    if (!creds) {
      throw new Error("DingTalk credentials not configured");
    }
    
    const content = messageToString(message.content);
    
    // Try webhook first if configured
    if (cfg.webhookUrl) {
      const success = await sendWebhookMessage(cfg.webhookUrl, cfg.webhookSecret, content);
      if (success) return;
    }
    
    // Fall back to API
    const token = await getAccessToken(creds.clientId, creds.clientSecret);
    if (!token) {
      throw new Error("Failed to get DingTalk access token");
    }
    
    const targetId = message.targetId || message.threadId;
    if (!targetId) {
      throw new Error("No target ID for DingTalk message");
    }
    
    const success = await sendTextMessage(token, targetId, content);
    if (!success) {
      throw new Error("Failed to send DingTalk message");
    }
  },

  async receive(
    ctx: ChannelPluginContext<DingTalkConfig>,
    payload: unknown
  ): Promise<InboundMessage | null> {
    // Handle incoming webhook from DingTalk
    const data = payload as Record<string, unknown>;
    
    // DingTalk callback format
    if (data.msgtype === "text" && data.text) {
      const textData = data.text as { content?: string };
      return {
        id: String(data.msgId || Date.now()),
        channel: "dingtalk",
        content: { type: "text", text: textData.content || "" },
        authorId: String(data.senderStaffId || data.staffId || "unknown"),
        authorName: String(data.senderNick || "Unknown"),
        conversationId: String(data.conversationId || data.chatId || "private"),
        timestamp: new Date(Number(data.createTime) || Date.now()),
      };
    }
    
    return null;
  },

  async getUserInfo(
    ctx: ChannelPluginContext<DingTalkConfig>,
    userId: string
  ): Promise<{ id: string; name: string; displayName?: string } | null> {
    const cfg = ctx.config;
    const creds = resolveDingTalkCredentials(cfg);
    
    if (!creds) return null;
    
    const token = await getAccessToken(creds.clientId, creds.clientSecret);
    if (!token) return null;
    
    try {
      const response = await fetch(
        `https://oapi.dingtalk.com/topapi/v2/user/get?access_token=${token}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userid: userId }),
        }
      );
      
      const data = await response.json();
      if (data.errcode === 0 && data.result) {
        return {
          id: userId,
          name: data.result.name || userId,
          displayName: data.result.name,
        };
      }
    } catch (error) {
      console.error("Failed to get DingTalk user info:", error);
    }
    
    return null;
  },
};

function messageToString(content: MessageContent): string {
  if (content.type === "text") return content.text || "";
  if (content.type === "markdown") return content.markdown || "";
  return JSON.stringify(content);
}

export default dingtalkPlugin;

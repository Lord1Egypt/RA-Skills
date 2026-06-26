// DingTalk API Types

export interface DingTalkUser {
  userid: string;
  name: string;
  avatar?: string;
  mobile?: string;
  email?: string;
}

export interface DingTalkMessage {
  msgtype: "text" | "markdown" | "action_card" | "feed_card" | "image" | "voice" | "file";
  text?: { content: string };
  markdown?: { title: string; text: string };
  action_card?: {
    title: string;
    markdown: string;
    single_title?: string;
    single_url?: string;
  };
}

export interface DingTalkWebhookPayload {
  msgtype: string;
  text?: { content: string };
  markdown?: { title: string; text: string };
  senderStaffId?: string;
  senderNick?: string;
  conversationId?: string;
  chatId?: string;
  msgId?: string;
  createTime?: number;
  atUsers?: Array<{ staffId: string }>;
}

export interface DingTalkCallbackPayload {
  encrypt: string;
  msg_signature: string;
  timestamp: string;
  nonce: string;
}

export interface DingTalkAccessTokenResponse {
  errcode: number;
  errmsg: string;
  access_token: string;
  expires_in: number;
}

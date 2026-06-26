/**
 * Type definitions for OpenClaw plugin API
 *
 * These are simplified types based on the OpenClaw plugin interface.
 * In production, these would come from the openclaw package types.
 */

export interface Logger {
  info: (...args: unknown[]) => void;
  warn: (...args: unknown[]) => void;
  error: (...args: unknown[]) => void;
  debug: (...args: unknown[]) => void;
}

export interface InjectMessageOptions {
  channel: string;
  senderId: string;
  senderName?: string;
  text: string;
  messageId?: string;
  chatType?: 'direct' | 'group';
  timestamp?: number;
  replyToId?: string;
  media?: {
    type: string;
    url?: string;
    buffer?: Buffer;
    filename?: string;
  }[];
}

export interface HttpHandler {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  handler: (req: HttpRequest, res: HttpResponse) => Promise<void> | void;
}

export interface HttpRequest {
  body: unknown;
  query: Record<string, string>;
  params: Record<string, string>;
  headers: Record<string, string>;
}

export interface HttpResponse {
  status: (code: number) => HttpResponse;
  json: (data: unknown) => void;
  send: (data: string) => void;
}

export interface ServiceDefinition {
  id: string;
  start: () => Promise<void> | void;
  stop: () => Promise<void> | void;
}

export interface GatewayMethodContext {
  respond: (success: boolean, data?: unknown) => void;
  params?: Record<string, unknown>;
}

export interface ChannelMeta {
  id: string;
  label: string;
  selectionLabel?: string;
  docsPath?: string;
  docsLabel?: string;
  blurb?: string;
  aliases?: string[];
}

export interface ChannelCapabilities {
  chatTypes: readonly ('direct' | 'group')[];
  media?: boolean;
  threads?: boolean;
  reactions?: boolean;
}

export interface ChannelAccount {
  accountId: string;
  enabled?: boolean;
  configured?: boolean;
  config?: Record<string, unknown>;
}

export interface DmPolicyResult {
  policy: string;
  allowFrom: string[];
  policyPath: string;
  allowFromPath: string;
  approveHint: string;
  normalizeEntry: (raw: string) => string;
}

export interface NormalizeTargetResult {
  target: string;
  normalized: string;
}

export interface SendResult {
  ok: boolean;
  error?: string;
  messageId?: string;
}

export interface ChannelPlugin {
  id: string;
  meta: ChannelMeta;
  capabilities: ChannelCapabilities;
  config: {
    listAccountIds: (cfg: Record<string, unknown>) => string[];
    resolveAccount: (cfg: Record<string, unknown>, accountId?: string) => ChannelAccount;
    defaultAccountId?: (cfg: Record<string, unknown>) => string;
    isConfigured?: (account: ChannelAccount) => boolean;
    describeAccount?: (account: ChannelAccount) => Record<string, unknown>;
  };
  security?: {
    resolveDmPolicy?: (ctx: { cfg: Record<string, unknown>; account: ChannelAccount }) => DmPolicyResult;
  };
  messaging?: {
    normalizeTarget?: (ctx: { target: string; cfg: Record<string, unknown> }) => NormalizeTargetResult;
    targetResolver?: {
      looksLikeId: (target: string) => boolean;
      hint: string;
    };
  };
  outbound?: {
    deliveryMode: 'direct' | 'queued';
    sendText: (ctx: {
      text: string;
      target: string;
      cfg: Record<string, unknown>;
      account: ChannelAccount;
    }) => Promise<SendResult>;
    sendMedia?: (ctx: {
      media: { type: string; buffer: Buffer; filename?: string };
      target: string;
      cfg: Record<string, unknown>;
      account: ChannelAccount;
    }) => Promise<SendResult>;
  };
}

export interface PluginApi {
  logger: Logger;
  config: unknown;
  registerChannel: (opts: { plugin: ChannelPlugin }) => void;
  registerService: (service: ServiceDefinition) => void;
  registerHttpHandler: (handler: HttpHandler) => void;
  registerGatewayMethod: (
    name: string,
    handler: (ctx: GatewayMethodContext) => Promise<void> | void
  ) => void;
  injectMessage: (opts: InjectMessageOptions) => Promise<void>;
}

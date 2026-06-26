/**
 * ACP Adapter Layer - ASF ↔ OpenClaw Bridge
 * 
 * Agent Control Protocol integration for IDE support and session management.
 */

export interface ACPMessage {
  jsonrpc: '2.0';
  id?: string | number;
  method: string;
  params?: Record<string, unknown>;
}

export interface ParsedACPMessage {
  type: string;
  capabilities?: any;
  clientInfo?: any;
  config?: any;
  sessionId?: string;
  prompt?: any;
  reason?: string;
}

export interface ACPSession {
  acpSessionId: string;
  asfSessionKey: string;
  state: 'initializing' | 'active' | 'paused' | 'completed' | 'failed';
  createdAt: Date;
  lastActivityAt: Date;
  mode: any;
  metadata: any;
}

export class ACPProtocolParser {
  private schema = new Map<string, any>();

  constructor() {
    this.initializeSchema();
  }

  parse(message: string): ParsedACPMessage {
    try {
      const raw = JSON.parse(message);
      this.validate(raw);
      return this.transform(raw);
    } catch (error) {
      throw new Error(`Invalid ACP message: ${(error as Error).message}`);
    }
  }

  private validate(message: ACPMessage): void {
    if (message.jsonrpc !== '2.0') {
      throw new Error('Invalid JSON-RPC version');
    }

    if (!this.schema.has(message.method)) {
      throw new Error(`Unknown method: ${message.method}`);
    }
  }

  private transform(raw: ACPMessage): ParsedACPMessage {
    switch (raw.method) {
      case 'initialize':
        return {
          type: 'initialize',
          capabilities: raw.params?.capabilities,
          clientInfo: raw.params?.clientInfo,
        };
      case 'newSession':
        return {
          type: 'newSession',
          config: raw.params?.config,
        };
      case 'prompt':
        return {
          type: 'prompt',
          sessionId: raw.params?.sessionId as string,
          prompt: raw.params?.prompt,
        };
      case 'cancel':
        return {
          type: 'cancel',
          sessionId: raw.params?.sessionId as string,
          reason: raw.params?.reason as string,
        };
      default:
        throw new Error(`Unhandled method: ${raw.method}`);
    }
  }

  validateParams(params: any, schema: any): void {
    // Basic validation
  }

  private initializeSchema(): void {
    this.schema.set('initialize', {});
    this.schema.set('newSession', {});
    this.schema.set('prompt', {});
    this.schema.set('cancel', {});
  }
}

export class ACPSessionManager {
  private sessions = new Map<string, ACPSession>();

  constructor(private gatewayUrl: string) {}

  async createSession(config: any, clientInfo: any): Promise<ACPSession> {
    const acpSessionId = `acp:${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const asfSessionKey = `asf-${Date.now()}`;

    const session: ACPSession = {
      acpSessionId,
      asfSessionKey,
      state: 'active',
      createdAt: new Date(),
      lastActivityAt: new Date(),
      mode: {
        thinking: config.thinking || 'medium',
        toolVerbosity: config.toolVerbosity || 'normal',
        reasoning: config.reasoning ?? false,
        usageDetail: config.usageDetail ?? false,
        elevatedActions: config.elevatedActions ?? false,
      },
      metadata: {
        clientInfo,
        capabilities: config.capabilities,
        workspace: config.workspace,
      },
    };

    this.sessions.set(acpSessionId, session);
    return session;
  }

  async getOrCreateSession(sessionId?: string, label?: string): Promise<ACPSession> {
    if (!sessionId) {
      return this.createSession({ label }, { name: 'default' });
    }

    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    return session;
  }

  async loadSession(sessionId: string): Promise<any> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    return { messages: [], sessionId };
  }

  async updateSessionMode(sessionId: string, mode: any): Promise<void> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    Object.assign(session.mode, mode);
  }
}

export class ToolProtocolConverter {
  private acpTools = new Map<string, any>();
  private asfTools = new Map<string, any>();

  async convertACPCallToASF(acpCall: any): Promise<any> {
    const asfTool = this.asfTools.get(acpCall.name);
    if (!asfTool) {
      throw new Error(`ASF tool not found: ${acpCall.name}`);
    }

    return {
      toolName: asfTool.name,
      arguments: acpCall.arguments,
      sessionId: acpCall.sessionId,
    };
  }

  async convertASFResultToACP(asfResult: any): Promise<any> {
    return {
      toolName: asfResult.toolName,
      result: asfResult.result,
      content: [],
      isError: asfResult.isError,
      metadata: {
        duration: asfResult.duration,
        resources: asfResult.resources,
      },
    };
  }

  registerASFTools(asfTools: any[]): any[] {
    const acpTools: any[] = [];

    for (const asfTool of asfTools) {
      const acpTool = {
        name: asfTool.name,
        description: asfTool.description,
        inputSchema: asfTool.parameters,
        annotations: {
          title: asfTool.name,
          readOnlyHint: this.isReadOnly(asfTool),
          destructiveHint: this.isDestructive(asfTool),
          idempotentHint: this.isIdempotent(asfTool),
          openWorldHint: true,
        },
      };

      acpTools.push(acpTool);
      this.acpTools.set(acpTool.name, acpTool);
    }

    return acpTools;
  }

  private isReadOnly(tool: any): boolean {
    return ['read', 'fetch', 'search', 'list', 'get'].some((k) => tool.name.toLowerCase().includes(k));
  }

  private isDestructive(tool: any): boolean {
    return ['delete', 'remove', 'destroy', 'drop'].some((k) => tool.name.toLowerCase().includes(k));
  }

  private isIdempotent(tool: any): boolean {
    return ['set', 'update', 'replace', 'write'].some((k) => tool.name.toLowerCase().includes(k));
  }
}

export class OpenClawGatewayClient {
  constructor(gatewayUrl: string, token: string) {}

  async createSession(config: any): Promise<string> {
    return 'session-key';
  }

  async sendPrompt(sessionKey: string, prompt: string): Promise<any> {
    return { response: 'ok' };
  }

  async getSessionHistory(sessionKey: string): Promise<any> {
    return { history: [] };
  }

  async updateSession(sessionKey: string, config: any): Promise<void> {}
}

export class ACPAdapterLayer {
  private protocolParser = new ACPProtocolParser();
  private sessionManager = new ACPSessionManager('ws://127.0.0.1:18789');
  private toolConverter = new ToolProtocolConverter();
  private gatewayClient = new OpenClawGatewayClient('ws://127.0.0.1:18789', 'token');

  async handle(message: string): Promise<any> {
    const parsed = this.protocolParser.parse(message);

    switch (parsed.type) {
      case 'initialize':
        return this.handleInitialize(parsed);
      case 'newSession':
        return this.handleNewSession(parsed);
      case 'prompt':
        return this.handlePrompt(parsed);
      case 'cancel':
        return this.handleCancel(parsed);
      default:
        throw new Error(`Unknown message type: ${parsed.type}`);
    }
  }

  private async handleInitialize(parsed: ParsedACPMessage): Promise<any> {
    return {
      jsonrpc: '2.0',
      id: 1,
      result: {
        protocolVersion: '2024-11-05',
        capabilities: {
          tools: { listChanged: true },
        },
        serverInfo: {
          name: 'asf-acp-adapter',
          version: '1.0.0',
        },
      },
    };
  }

  private async handleNewSession(parsed: ParsedACPMessage): Promise<any> {
    const session = await this.sessionManager.createSession(parsed.config || {}, {});
    return {
      jsonrpc: '2.0',
      id: 2,
      result: {
        sessionId: session.acpSessionId,
        state: session.state,
        mode: session.mode,
      },
    };
  }

  private async handlePrompt(parsed: ParsedACPMessage): Promise<any> {
    // In real implementation, would route to ASF agent
    return {
      jsonrpc: '2.0',
      id: 3,
      result: {
        content: [{ type: 'text', text: 'Response from ASF' }],
        toolCalls: [],
        usage: {
          inputTokens: 100,
          outputTokens: 50,
        },
      },
    };
  }

  private async handleCancel(parsed: ParsedACPMessage): Promise<any> {
    return {
      jsonrpc: '2.0',
      id: 4,
      result: {
        status: 'cancelled',
      },
    };
  }
}

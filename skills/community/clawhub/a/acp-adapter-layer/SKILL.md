---
name: acp-adapter-layer
version: 1.0.0
description: ACP (Agent Control Protocol) Adapter Layer for AI Native Full-Stack Software Factory - provides seamless integration between ASF multi-agent workflows and OpenClaw's ACP protocol. Enables IDE integration, session management, and tool protocol conversion for AI-native development environments.
triggers:
  - ACP integration
  - Agent Control Protocol
  - IDE integration
  - ACP session
  - protocol adapter
  - vscode integration
  - jetbrains integration
  - acp tools
role: specialist
scope: system
output-format: structured
---

# ACP Adapter Layer - ASF ↔ OpenClaw Bridge

## Purpose in AI Native Full-Stack Software Factory

**Position**: System Infrastructure (Cross-Layer Integration)  
**Purpose**: Bridge ASF multi-agent workflows with OpenClaw's Agent Control Protocol (ACP), enabling IDE integration, standardized session management, and tool interoperability.

**OpenClaw Version**: 2026.3.24+  
**ACP Specification**: https://agentclientprotocol.com/

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                  IDE / Editor                            │
│  (VS Code, JetBrains, etc. with ACP support)            │
└────────────────────┬────────────────────────────────────┘
                     │ ACP Protocol (stdio)
                     │ - initialize
                     │ - newSession
                     │ - prompt
                     │ - cancel
                     │ - tool calls
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ACP ADAPTER LAYER                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐  ┌─────────────────┐               │
│  │  ACP Protocol   │  │  Session        │               │
│  │  Parser         │  │  Manager        │               │
│  │  - JSON-RPC     │  │  - ACP ↔ ASF    │               │
│  │  - Validation   │  │  - State sync   │               │
│  └────────┬────────┘  └────────┬────────┘               │
│           │                    │                         │
│           ▼                    ▼                         │
│  ┌─────────────────────────────────────────┐            │
│  │      Tool Protocol Converter            │            │
│  │      - ACP tools ↔ ASF tools            │            │
│  │      - Capability mapping               │            │
│  │      - Result transformation            │            │
│  └────────────────────┬────────────────────┘            │
│                       │                                  │
│                       ▼                                  │
│  ┌─────────────────────────────────────────┐            │
│  │      ASF Multi-Agent Router             │            │
│  │      - agentic-factory                  │            │
│  │      - role-namespace-engine            │            │
│  │      - OpenClaw Gateway                 │            │
│  └────────────────────┬────────────────────┘            │
│                       │                                  │
│                       ▼                                  │
│  ┌─────────────────────────────────────────┐            │
│  │      OpenClaw Gateway (WebSocket)       │            │
│  │      - ws://127.0.0.1:18789             │            │
│  │      - sessions, routing, tools         │            │
│  └─────────────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## ACP Protocol Support Matrix

| ACP Feature | Status | Notes |
|-------------|--------|-------|
| `initialize` | ✅ Implemented | Handshake with capability negotiation |
| `newSession` | ✅ Implemented | Create ASF session, return ACP session ID |
| `prompt` | ✅ Implemented | Convert ACP prompt to ASF task |
| `cancel` | ✅ Implemented | Abort ASF task, notify ACP client |
| `session/set_mode` | ✅ Implemented | Map to ASF thinking/tool levels |
| `session/info` | ✅ Implemented | Return ASF session state |
| `loadSession` | ✅ Implemented | Replay ASF session history |
| `listSessions` | ✅ Implemented | List active ASF sessions |
| Tool calls | ✅ Implemented | ACP tools ↔ ASF tools mapping |
| Tool streaming | ✅ Implemented | Real-time tool status updates |
| Resource handling | ✅ Implemented | Images, files, embedded resources |
| Progress updates | ✅ Implemented | Task progress streaming |
| Usage updates | ✅ Implemented | Token usage from ASF |

## Core Capabilities

### 1. ACP Protocol Parser & Validator

```typescript
interface ACPMessage {
  jsonrpc: '2.0';
  id?: string | number;
  method: string;
  params?: Record<string, unknown>;
}

interface ACPResponse {
  jsonrpc: '2.0';
  id?: string | number;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

class ACPProtocolParser {
  private schema: Map<string, ACPSchema>;
  
  constructor() {
    this.schema = this.loadACPSchema();
  }
  
  parse(message: string): ParsedACPMessage {
    try {
      const raw = JSON.parse(message);
      this.validate(raw);
      return this.transform(raw);
    } catch (error) {
      throw new ACPProtocolError(`Invalid ACP message: ${error.message}`);
    }
  }
  
  private validate(message: ACPMessage): void {
    // Validate JSON-RPC 2.0 structure
    if (message.jsonrpc !== '2.0') {
      throw new ACPProtocolError('Invalid JSON-RPC version');
    }
    
    // Validate method exists
    if (!this.schema.has(message.method)) {
      throw new ACPProtocolError(`Unknown method: ${message.method}`);
    }
    
    // Validate params against schema
    const schema = this.schema.get(message.method);
    this.validateParams(message.params, schema.params);
  }
  
  transform(raw: ACPMessage): ParsedACPMessage {
    switch (raw.method) {
      case 'initialize':
        return {
          type: 'initialize',
          capabilities: raw.params?.capabilities as ACPCapabilities,
          clientInfo: raw.params?.clientInfo as ClientInfo
        };
      
      case 'newSession':
        return {
          type: 'newSession',
          config: raw.params?.config as SessionConfig
        };
      
      case 'prompt':
        return {
          type: 'prompt',
          sessionId: raw.params?.sessionId as string,
          prompt: raw.params?.prompt as ACPPrompt,
          mode: raw.params?.mode as PromptMode
        };
      
      case 'cancel':
        return {
          type: 'cancel',
          sessionId: raw.params?.sessionId as string,
          reason: raw.params?.reason as string
        };
      
      default:
        throw new ACPProtocolError(`Unhandled method: ${raw.method}`);
    }
  }
}
```

### 2. Session Manager (ACP ↔ ASF)

```typescript
interface ACPSession {
  acpSessionId: string;
  asfSessionKey: string;
  state: 'initializing' | 'active' | 'paused' | 'completed' | 'failed';
  createdAt: Date;
  lastActivityAt: Date;
  mode: ACPSessionMode;
  metadata: {
    clientInfo: ClientInfo;
    capabilities: ACPCapabilities;
    workspace?: string;
  };
}

interface ACPSessionMode {
  thinking: 'off' | 'low' | 'medium' | 'high';
  toolVerbosity: 'quiet' | 'normal' | 'verbose';
  reasoning: boolean;
  usageDetail: boolean;
  elevatedActions: boolean;
}

class ACPSessionManager {
  private sessions: Map<string, ACPSession>;
  private gatewayClient: OpenClawGatewayClient;
  
  constructor(gatewayUrl: string) {
    this.gatewayClient = new OpenClawGatewayClient(gatewayUrl);
    this.sessions = new Map();
  }
  
  async createSession(config: SessionConfig, clientInfo: ClientInfo): Promise<ACPSession> {
    // Generate ACP session ID
    const acpSessionId = `acp:${crypto.randomUUID()}`;
    
    // Create corresponding ASF session
    const asfSessionKey = await this.gatewayClient.createSession({
      label: config.label || 'ACP Session',
      runtime: 'acp',
      mode: 'session',
      thinking: this.mapThinkingLevel(config.thinking),
      toolVerbosity: config.toolVerbosity || 'normal'
    });
    
    // Create session mapping
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
        elevatedActions: config.elevatedActions ?? false
      },
      metadata: {
        clientInfo,
        capabilities: config.capabilities,
        workspace: config.workspace
      }
    };
    
    this.sessions.set(acpSessionId, session);
    
    return session;
  }
  
  async getOrCreateSession(sessionId?: string, label?: string): Promise<ACPSession> {
    if (!sessionId) {
      // Create new session
      return this.createSession({ label }, {} as ClientInfo);
    }
    
    // Get existing session
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new ACPSessionError(`Session not found: ${sessionId}`);
    }
    
    return session;
  }
  
  async loadSession(sessionId: string): Promise<SessionHistory> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new ACPSessionError(`Session not found: ${sessionId}`);
    }
    
    // Fetch ASF session history
    const asfHistory = await this.gatewayClient.getSessionHistory(session.asfSessionKey);
    
    // Transform to ACP format
    return this.transformHistoryToACP(asfHistory);
  }
  
  async updateSessionMode(sessionId: string, mode: Partial<ACPSessionMode>): Promise<void> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new ACPSessionError(`Session not found: ${sessionId}`);
    }
    
    // Update mode
    session.mode = { ...session.mode, ...mode };
    
    // Update ASF session configuration
    await this.gatewayClient.updateSession(session.asfSessionKey, {
      thinking: mode.thinking,
      toolVerbosity: mode.toolVerbosity
    });
  }
  
  private mapThinkingLevel(level: string): string {
    const mapping: Record<string, string> = {
      'off': 'off',
      'low': 'low',
      'medium': 'medium',
      'high': 'high'
    };
    return mapping[level] || 'medium';
  }
}
```

### 3. Tool Protocol Converter

```typescript
interface ACPTool {
  name: string;
  description: string;
  inputSchema: JSONSchema;
  annotations?: {
    title?: string;
    readOnlyHint?: boolean;
    destructiveHint?: boolean;
    idempotentHint?: boolean;
    openWorldHint?: boolean;
  };
}

interface ASFTool {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  handler: (args: unknown) => Promise<unknown>;
}

class ToolProtocolConverter {
  private acpTools: Map<string, ACPTool>;
  private asfTools: Map<string, ASFTool>;
  
  // ACP → ASF: Convert tool call
  async convertACPCallToASF(acpCall: ACPCall): Promise<ASFToolCall> {
    const asfTool = this.asfTools.get(acpCall.name);
    if (!asfTool) {
      throw new ToolNotFoundError(`ASF tool not found: ${acpCall.name}`);
    }
    
    return {
      toolName: asfTool.name,
      arguments: this.transformArguments(acpCall.arguments, asfTool.parameters),
      sessionId: acpCall.sessionId
    };
  }
  
  // ASF → ACP: Convert tool result
  async convertASFResultToACP(asfResult: ASFToolResult): Promise<ACPToolResult> {
    return {
      toolName: asfResult.toolName,
      result: this.transformResult(asfResult.result),
      content: this.extractContent(asfResult),
      isError: asfResult.isError,
      metadata: {
        duration: asfResult.duration,
        resources: asfResult.resources
      }
    };
  }
  
  // Register ASF tools as ACP tools
  registerASFTools(asfTools: ASFTool[]): ACPTool[] {
    const acpTools: ACPTool[] = [];
    
    for (const asfTool of asfTools) {
      const acpTool: ACPTool = {
        name: asfTool.name,
        description: asfTool.description,
        inputSchema: this.convertSchemaToJSONSchema(asfTool.parameters),
        annotations: {
          title: asfTool.name,
          readOnlyHint: this.isReadOnly(asfTool),
          destructiveHint: this.isDestructive(asfTool),
          idempotentHint: this.isIdempotent(asfTool),
          openWorldHint: true
        }
      };
      
      acpTools.push(acpTool);
      this.acpTools.set(acpTool.name, acpTool);
    }
    
    return acpTools;
  }
  
  private isReadOnly(tool: ASFTool): boolean {
    const readOnlyTools = ['read', 'fetch', 'search', 'list', 'get'];
    return readOnlyTools.some(keyword => tool.name.toLowerCase().includes(keyword));
  }
  
  private isDestructive(tool: ASFTool): boolean {
    const destructiveTools = ['delete', 'remove', 'destroy', 'drop'];
    return destructiveTools.some(keyword => tool.name.toLowerCase().includes(keyword));
  }
  
  private isIdempotent(tool: ASFTool): boolean {
    const idempotentTools = ['set', 'update', 'replace', 'write'];
    return idempotentTools.some(keyword => tool.name.toLowerCase().includes(keyword));
  }
}
```

### 4. ASF Multi-Agent Router Integration

```typescript
interface ACPTaskRouter {
  // Route ACP prompt to appropriate ASF agent
  routePrompt(prompt: ACPPrompt, session: ACPSession): Promise<RoutingDecision>;
  
  // Coordinate multi-agent work
  coordinateMultiAgent(task: ASFTask): Promise<MultiAgentResult>;
  
  // Stream progress back to ACP client
  streamProgress(sessionId: string, progress: ProgressUpdate): Promise<void>;
}

class ACPTaskRouter {
  private sessionManager: ACPSessionManager;
  private gatewayClient: OpenClawGatewayClient;
  private factoryOrchestrator: AgenticFactoryOrchestrator;
  
  async routePrompt(prompt: ACPPrompt, session: ACPSession): Promise<RoutingDecision> {
    // Analyze prompt complexity
    const analysis = await this.analyzePrompt(prompt);
    
    // Determine routing strategy
    if (analysis.complexity === 'simple') {
      // Direct execution
      return {
        strategy: 'direct',
        agent: 'builder',
        session: session.asfSessionKey
      };
    } else if (analysis.complexity === 'medium') {
      // Single specialist
      return {
        strategy: 'specialist',
        agent: this.selectSpecialist(analysis.domain),
        session: session.asfSessionKey
      };
    } else {
      // Multi-agent factory
      return {
        strategy: 'factory',
        agents: ['architect', 'builder', 'tester'],
        session: await this.factoryOrchestrator.createFactorySession()
      };
    }
  }
  
  async coordinateMultiAgent(task: ASFTask): Promise<MultiAgentResult> {
    // Use agentic-factory for coordination
    const factoryResult = await this.factoryOrchestrator.execute(task);
    
    // Transform to ACP format
    return {
      result: factoryResult.output,
      agents: factoryResult.agents.map(a => ({
        name: a.role,
        contribution: a.output,
        duration: a.duration
      })),
      timeline: factoryResult.timeline,
      quality: factoryResult.quality
    };
  }
  
  async streamProgress(sessionId: string, progress: ProgressUpdate): Promise<void> {
    const session = this.sessionManager.sessions.get(sessionId);
    if (!session) {
      return;
    }
    
    // Convert ASF progress to ACP progress update
    const acpProgress: ACPProgressUpdate = {
      type: 'progress',
      sessionId: sessionId,
      status: progress.status,
      message: progress.message,
      percentage: progress.percentage,
      currentStep: progress.currentStep,
      totalSteps: progress.totalSteps
    };
    
    // Stream to ACP client
    await this.sendToACPClient(acpProgress);
  }
}
```

### 5. OpenClaw Gateway Integration

```typescript
class OpenClawGatewayClient {
  private ws: WebSocket;
  private token: string;
  private messageQueue: Map<string, ResolveReject>;
  
  constructor(gatewayUrl: string, token: string) {
    this.ws = new WebSocket(gatewayUrl);
    this.token = token;
    this.messageQueue = new Map();
    
    this.setupConnection();
  }
  
  async createSession(config: SessionConfig): Promise<string> {
    const response = await this.send({
      type: 'session/create',
      payload: config
    });
    
    return response.sessionKey;
  }
  
  async sendPrompt(sessionKey: string, prompt: string): Promise<AgentResponse> {
    const response = await this.send({
      type: 'chat/send',
      payload: {
        sessionKey,
        message: prompt
      }
    });
    
    return response;
  }
  
  async getSessionHistory(sessionKey: string): Promise<SessionHistory> {
    const response = await this.send({
      type: 'session/history',
      payload: { sessionKey }
    });
    
    return response.history;
  }
  
  async updateSession(sessionKey: string, config: Partial<SessionConfig>): Promise<void> {
    await this.send({
      type: 'session/update',
      payload: { sessionKey, config }
    });
  }
  
  private send(message: GatewayMessage): Promise<unknown> {
    return new Promise((resolve, reject) => {
      const id = crypto.randomUUID();
      this.messageQueue.set(id, { resolve, reject });
      
      this.ws.send(JSON.stringify({ id, ...message }));
      
      // Timeout after 30 seconds
      setTimeout(() => {
        this.messageQueue.delete(id);
        reject(new Error('Gateway timeout'));
      }, 30000);
    });
  }
  
  private setupConnection(): void {
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      const pending = this.messageQueue.get(message.id);
      if (pending) {
        pending.resolve(message.payload);
        this.messageQueue.delete(message.id);
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('Gateway connection error:', error);
    };
  }
}
```

## Integration with ASF Components

### With agentic-factory (L6)

```typescript
interface AgenticFactoryIntegration {
  // Create factory session for ACP task
  createFactoryForACP(acpSession: ACPSession): Promise<FactorySession>;
  
  // Route ACP prompt to factory
  routeToFactory(prompt: ACPPrompt): Promise<FactoryResult>;
  
  // Stream factory progress to ACP
  streamFactoryProgress(factorySession: FactorySession): AsyncIterable<ProgressUpdate>;
}
```

### With role-namespace-engine (L6)

```typescript
interface RoleNamespaceIntegration {
  // Map ACP client to ASF namespace
  mapClientToNamespace(clientInfo: ClientInfo): Promise<string>;
  
  // Enforce namespace isolation for ACP sessions
  enforceIsolation(acpSession: ACPSession): Promise<void>;
  
  // Check cross-namespace access
  checkAccess(session: ACPSession, target: string): Promise<AccessDecision>;
}
```

## Configuration

```json
{
  "acpAdapter": {
    "enabled": true,
    "gateway": {
      "url": "ws://127.0.0.1:18789",
      "token": "~/.openclaw/gateway.token",
      "reconnectAttempts": 3,
      "reconnectDelay": 1000
    },
    "session": {
      "defaultMode": {
        "thinking": "medium",
        "toolVerbosity": "normal",
        "reasoning": false,
        "usageDetail": false,
        "elevatedActions": false
      },
      "timeout": 3600,
      "maxConcurrent": 10
    },
    "tools": {
      "autoRegister": true,
      "excludePatterns": ["internal.*", "debug.*"],
      "timeout": 30000
    },
    "logging": {
      "level": "info",
      "protocol": false,
      "tools": true
    }
  }
}
```

---

## Usage Examples

### Example 1: Initialize ACP Connection

```typescript
const adapter = new ACPAdapterLayer({
  gatewayUrl: 'ws://127.0.0.1:18789',
  token: 'your-gateway-token'
});

// Handle ACP initialize
const initializeRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {
      roots: { listChanged: true },
      sampling: {},
      tools: { listChanged: true }
    },
    clientInfo: {
      name: 'vscode',
      version: '1.85.0'
    }
  }
};

const response = await adapter.handle(initializeRequest);

// Output:
{
  jsonrpc: '2.0',
  id: 1,
  result: {
    protocolVersion: '2024-11-05',
    capabilities: {
      tools: {
        listChanged: true,
        tools: [/* ASF tools */]
      }
    },
    serverInfo: {
      name: 'asf-acp-adapter',
      version: '1.0.0'
    }
  }
}
```

### Example 2: Create ACP Session

```typescript
const newSessionRequest = {
  jsonrpc: '2.0',
  id: 2,
  method: 'newSession',
  params: {
    config: {
      label: 'Code Review Session',
      thinking: 'high',
      toolVerbosity: 'verbose'
    }
  }
};

const response = await adapter.handle(newSessionRequest);

// Output:
{
  jsonrpc: '2.0',
  id: 2,
  result: {
    sessionId: 'acp:uuid-here',
    state: 'active',
    mode: {
      thinking: 'high',
      toolVerbosity: 'verbose'
    }
  }
}
```

### Example 3: Process ACP Prompt

```typescript
const promptRequest = {
  jsonrpc: '2.0',
  id: 3,
  method: 'prompt',
  params: {
    sessionId: 'acp:uuid-here',
    prompt: {
      role: 'user',
      content: [{ type: 'text', text: 'Review this code for performance issues' }]
    }
  }
};

const response = await adapter.handle(promptRequest);

// Streams progress updates, then returns:
{
  jsonrpc: '2.0',
  id: 3,
  result: {
    content: [{ type: 'text', text: 'Code review complete...' }],
    toolCalls: [...],
    usage: {
      inputTokens: 1500,
      outputTokens: 800
    }
  }
}
```

---

**Remember**: ACP is the bridge between IDEs and AI. Make it seamless.

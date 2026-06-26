export type AgentStatus = "online" | "offline";

export type MessageKind = "direct" | "private" | "broadcast";

export type MessageStatus = "pending" | "delivered" | "acknowledged";

export interface AgentRecord {
  id: string;
  name: string;
  status: AgentStatus;
  metadata: Record<string, unknown>;
  lastSeenAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface SessionRecord {
  id: string;
  agentId: string;
  status: "connected" | "disconnected";
  connectedAt: string;
  disconnectedAt: string | null;
  metadata: Record<string, unknown>;
}

export interface MessageRecord {
  id: string;
  kind: MessageKind;
  senderId: string;
  recipientId: string | null;
  payload: Record<string, unknown>;
  status: MessageStatus;
  topic: string | null;
  createdAt: string;
  deliveredAt: string | null;
  acknowledgedAt: string | null;
  correlationId: string | null;
}

export interface EventRecord {
  id: string;
  type: string;
  sourceAgentId: string | null;
  payload: Record<string, unknown>;
  metadata: Record<string, unknown>;
  createdAt: string;
}

export interface EventSubscription {
  id: string;
  agentId: string;
  eventType: string;
  filter: Record<string, unknown>;
  createdAt: string;
}

export interface SendMessageInput {
  senderId: string;
  recipientId?: string;
  payload: Record<string, unknown>;
  topic?: string;
  correlationId?: string;
}

export interface EventPublishInput {
  type: string;
  sourceAgentId?: string;
  payload: Record<string, unknown>;
  metadata?: Record<string, unknown>;
}

export interface EventReplayOptions {
  type?: string;
  sourceAgentId?: string;
  since?: string;
  limit?: number;
}

export interface MessageQuery {
  senderId?: string;
  recipientId?: string;
  status?: MessageStatus;
  kind?: MessageKind;
  limit?: number;
}

export interface AgentRegistrationInput {
  id: string;
  name?: string;
  metadata?: Record<string, unknown>;
}

export interface SessionConnectInput {
  agentId: string;
  metadata?: Record<string, unknown>;
}

/**
 * Network Types
 * 
 * Core type definitions for the AlephNet mesh network layer.
 */

// ═══════════════════════════════════════════════════════════════════════════
// PEER TYPES
// ═══════════════════════════════════════════════════════════════════════════

export type PeerStatus = 'connecting' | 'connected' | 'disconnected' | 'banned';

export interface PeerInfo {
  id: string;
  address: string;
  port: number;
  publicKey: string;
  status: PeerStatus;
  lastSeen: number;
  latency: number;         // Round-trip time in ms
  semanticDomain: string;
  stakingTier: string;
  reputation: number;      // 0-1 trust score
  messageCount: number;
}

export interface PeerDiscoveryResult {
  peers: PeerInfo[];
  source: 'bootstrap' | 'gossip' | 'gun';
  timestamp: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// MESSAGE TYPES
// ═══════════════════════════════════════════════════════════════════════════

export type MessageType = 
  | 'handshake'
  | 'ping'
  | 'pong'
  | 'announce'
  | 'query'
  | 'response'
  | 'broadcast'
  | 'direct'
  | 'consensus'
  | 'gmf_sync'
  | 'sria_summon';

export interface NetworkMessage<T = unknown> {
  id: string;
  type: MessageType;
  from: string;
  to: string | 'broadcast';
  payload: T;
  timestamp: number;
  signature: string;
  ttl: number;
  hops: number;
  
  // Semantic routing
  smfVector?: number[];
  targetDomain?: string;
  primeHash?: string;
}

export interface HandshakePayload {
  version: string;
  publicKey: string;
  nodeId: string;
  semanticDomain: string;
  capabilities: string[];
  stakingTier: string;
}

export interface PingPayload {
  nonce: string;
  timestamp: number;
}

export interface PongPayload {
  nonce: string;
  timestamp: number;
  serverTime: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// ROUTING TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface RoutingTable {
  localId: string;
  buckets: Map<number, PeerInfo[]>;  // K-buckets for Kademlia-like routing
  timestamp: number;
}

export interface RouteInfo {
  target: string;
  path: string[];
  hopCount: number;
  latency: number;
  semanticDistance: number;
}

export interface RoutingDecision {
  nextHop: string;
  route: RouteInfo;
  alternates: RouteInfo[];
}

// ═══════════════════════════════════════════════════════════════════════════
// TRANSPORT TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface TransportConfig {
  type: 'websocket' | 'gun' | 'http' | 'quic';
  address: string;
  port: number;
  tls: boolean;
  timeout: number;
  reconnect: boolean;
  reconnectInterval: number;
  maxReconnectAttempts: number;
}

export interface TransportStats {
  messagesSent: number;
  messagesReceived: number;
  bytesSent: number;
  bytesReceived: number;
  errors: number;
  lastActivity: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// CONNECTION TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface Connection {
  id: string;
  peer: PeerInfo;
  transport: TransportConfig;
  established: number;
  lastActivity: number;
  stats: TransportStats;
  quality: number;  // 0-1 connection quality score
}

export interface ConnectionPool {
  connections: Map<string, Connection>;
  maxConnections: number;
  activeCount: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// EVENTS
// ═══════════════════════════════════════════════════════════════════════════

export type NetworkEventType = 
  | 'peer_discovered'
  | 'peer_connected'
  | 'peer_disconnected'
  | 'message_received'
  | 'message_sent'
  | 'route_updated'
  | 'connection_error'
  | 'bandwidth_limit';

export interface NetworkEvent {
  type: NetworkEventType;
  timestamp: number;
  data: unknown;
}

export type NetworkEventHandler = (event: NetworkEvent) => void;

// ═══════════════════════════════════════════════════════════════════════════
// MESH TYPES
// ═══════════════════════════════════════════════════════════════════════════

export interface MeshConfig {
  nodeId: string;
  publicKey: string;
  bootstrapUrls: string[];
  minPeers: number;
  maxPeers: number;
  semanticDomain: string;
  enableGossip: boolean;
  gossipInterval: number;
  heartbeatInterval: number;
  peerTimeout: number;
}

export interface MeshState {
  isOnline: boolean;
  peerCount: number;
  routeCount: number;
  domainPeers: Map<string, number>;
  bandwidth: {
    incoming: number;
    outgoing: number;
  };
  health: 'healthy' | 'degraded' | 'unhealthy';
}

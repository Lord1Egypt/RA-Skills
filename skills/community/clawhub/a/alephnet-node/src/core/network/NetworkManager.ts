/**
 * Network Manager
 * 
 * High-level orchestration of the AlephNet mesh network.
 * Coordinates PeerManager, MessageRouter, and Transport layers.
 */

import { 
  MeshConfig, 
  NetworkMessage, 
  PeerInfo, 
  PeerStatus,
  NetworkEventHandler,
  NetworkEvent
} from './types';
import { PeerManager } from './PeerManager';
import { MessageRouter } from './MessageRouter';
import { createLogger } from '../../common/logging';
import { generateId } from '../../common/hash';
import { KeyTriplet, signEd25519, base64ToBuffer, bufferToBase64 } from '../../common/crypto';

const logger = createLogger('NetworkManager');

const DEFAULT_CONFIG: MeshConfig = {
  nodeId: '',
  publicKey: '',
  bootstrapUrls: [],
  minPeers: 4,
  maxPeers: 50,
  semanticDomain: 'cognitive',
  enableGossip: true,
  gossipInterval: 1000,
  heartbeatInterval: 30000,
  peerTimeout: 60000
};

export class NetworkManager {
  private config: MeshConfig;
  private peerManager: PeerManager;
  private messageRouter: MessageRouter;
  private isStarted: boolean = false;
  private eventHandlers: Set<NetworkEventHandler> = new Set();
  
  constructor(
    config: Partial<MeshConfig>,
    private keyTriplet: KeyTriplet
  ) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    
    // Initialize components
    this.peerManager = new PeerManager({
      nodeId: this.config.nodeId,
      minPeers: this.config.minPeers,
      maxPeers: this.config.maxPeers,
      peerTimeout: this.config.peerTimeout
    });
    
    this.messageRouter = new MessageRouter(this.peerManager, {
      nodeId: this.config.nodeId
    });
    
    // Wire up events
    this.peerManager.on(this.handlePeerEvent.bind(this));
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // LIFECYCLE
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Start the network manager
   */
  async start(): Promise<void> {
    if (this.isStarted) return;
    
    logger.info('Starting network manager', { nodeId: this.config.nodeId });
    
    this.peerManager.start();
    this.isStarted = true;
    
    // Connect to bootstrap nodes
    await this.connectToBootstrap();
  }
  
  /**
   * Stop the network manager
   */
  async stop(): Promise<void> {
    if (!this.isStarted) return;
    
    logger.info('Stopping network manager');
    
    this.peerManager.stop();
    this.isStarted = false;
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // MESSAGING
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Send a message to a specific peer
   */
  async sendMessage(to: string, type: string, payload: unknown): Promise<string> {
    const message = this.createMessage(to, type, payload);
    await this.messageRouter.routeMessage(message);
    return message.id;
  }
  
  /**
   * Broadcast a message to the network
   */
  async broadcast(type: string, payload: unknown): Promise<string> {
    const message = this.createMessage('broadcast', type, payload);
    await this.messageRouter.routeMessage(message);
    return message.id;
  }
  
  /**
   * Create a signed network message
   */
  private createMessage(to: string, type: string, payload: unknown): NetworkMessage {
    const id = generateId('msg');
    const timestamp = Date.now();
    
    const message: NetworkMessage = {
      id,
      type: type as any,
      from: this.config.nodeId,
      to,
      payload,
      timestamp,
      signature: '',
      ttl: 10,
      hops: 0,
      targetDomain: this.config.semanticDomain // Default to own domain
    };
    
    // Sign message
    const dataToSign = `${id}:${type}:${this.config.nodeId}:${to}:${timestamp}:${JSON.stringify(payload)}`;
    const signature = signEd25519(
      Buffer.from(dataToSign), 
      base64ToBuffer(this.keyTriplet.priv)
    );
    message.signature = bufferToBase64(signature);
    
    return message;
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // PEER MANAGEMENT
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Get connected peers
   */
  getPeers(): PeerInfo[] {
    return this.peerManager.getPeersByStatus('connected');
  }
  
  /**
   * Connect to bootstrap nodes
   */
  private async connectToBootstrap(): Promise<void> {
    if (this.config.bootstrapUrls.length === 0) return;
    
    logger.info('Connecting to bootstrap nodes', { 
      count: this.config.bootstrapUrls.length 
    });
    
    // In a real implementation, this would connect to bootstrap servers
    // For now, we simulate adding them as peers
    for (const url of this.config.bootstrapUrls) {
      try {
        // Simulate peer info from URL
        const peerId = generateId(`bootstrap-${url}`);
        this.peerManager.addPeer({
          id: peerId,
          address: url,
          port: 443,
          publicKey: 'mock-key',
          status: 'connected',
          lastSeen: Date.now(),
          latency: 50,
          semanticDomain: 'meta',
          stakingTier: 'Archon',
          reputation: 1.0,
          messageCount: 0
        });
      } catch (error) {
        logger.error('Failed to connect to bootstrap node', { url, error });
      }
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // EVENTS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Handle internal peer events
   */
  private handlePeerEvent(event: NetworkEvent): void {
    // Re-emit relevant events
    this.emit(event.type, event.data);
  }
  
  /**
   * Subscribe to network events
   */
  on(handler: NetworkEventHandler): () => void {
    this.eventHandlers.add(handler);
    return () => this.eventHandlers.delete(handler);
  }
  
  /**
   * Emit an event
   */
  private emit(type: NetworkEvent['type'], data: unknown): void {
    const event: NetworkEvent = {
      type,
      timestamp: Date.now(),
      data
    };
    
    for (const handler of this.eventHandlers) {
      try {
        handler(event);
      } catch (error) {
        logger.error('Event handler error', error as Error);
      }
    }
  }
}

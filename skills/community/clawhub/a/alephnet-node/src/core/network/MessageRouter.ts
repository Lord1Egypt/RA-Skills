/**
 * Message Router
 * 
 * Handles semantic routing of messages across the mesh network.
 * Implements Kademlia-like routing with semantic proximity optimization.
 */

import { 
  NetworkMessage, 
  RoutingTable, 
  PeerInfo, 
  RoutingDecision,
  RouteInfo
} from './types';
import { PeerManager } from './PeerManager';
import { createLogger } from '../../common/logging';
import { SMFVector } from '../../common/types';
import { cosineSimilarity } from '../../common/math';

const logger = createLogger('MessageRouter');

export interface MessageRouterOptions {
  nodeId: string;
  maxHops: number;
  bucketSize: number;
  alpha: number; // Parallelism factor for routing lookups
}

const DEFAULT_OPTIONS: MessageRouterOptions = {
  nodeId: '',
  maxHops: 10,
  bucketSize: 20,
  alpha: 3
};

export class MessageRouter {
  private options: MessageRouterOptions;
  private routingTable: RoutingTable;
  private seenMessages: Set<string> = new Set();
  private maxSeenMessages = 10000;
  
  constructor(
    private peerManager: PeerManager,
    options: Partial<MessageRouterOptions> = {}
  ) {
    this.options = { ...DEFAULT_OPTIONS, ...options };
    this.routingTable = {
      localId: this.options.nodeId,
      buckets: new Map(),
      timestamp: Date.now()
    };
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // ROUTING
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Route a message to its destination
   */
  async routeMessage(message: NetworkMessage): Promise<void> {
    // Check if seen to prevent loops
    if (this.seenMessages.has(message.id)) {
      return;
    }
    this.recordSeenMessage(message.id);
    
    // Check TTL
    if (message.hops >= this.options.maxHops || message.ttl <= 0) {
      logger.debug('Message TTL expired', { messageId: message.id });
      return;
    }
    
    // Check if we are the destination
    if (message.to === this.options.nodeId) {
      this.handleLocalMessage(message);
      return;
    }
    
    // Handle broadcast
    if (message.to === 'broadcast') {
      this.handleLocalMessage(message);
      await this.broadcastMessage(message);
      return;
    }
    
    // Determine next hop
    const decision = this.determineNextHop(message);
    
    if (decision.nextHop) {
      await this.forwardMessage(message, decision.nextHop);
    } else {
      logger.warn('No route found for message', { 
        messageId: message.id, 
        target: message.to 
      });
    }
  }
  
  /**
   * Determine the best next hop for a message
   */
  private determineNextHop(message: NetworkMessage): RoutingDecision {
    // If target is directly connected, send there
    const directPeer = this.peerManager.getPeer(message.to);
    if (directPeer && directPeer.status === 'connected') {
      return {
        nextHop: message.to,
        route: {
          target: message.to,
          path: [message.to],
          hopCount: 1,
          latency: directPeer.latency,
          semanticDistance: 0
        },
        alternates: []
      };
    }
    
    // Otherwise find closest peers
    const candidates = this.peerManager.getPeersByStatus('connected');
    
    // Sort by distance metric
    const sorted = this.sortPeersByMetric(candidates, message);
    
    if (sorted.length === 0) {
      return {
        nextHop: '',
        route: { target: '', path: [], hopCount: 0, latency: 0, semanticDistance: 0 },
        alternates: []
      };
    }
    
    return {
      nextHop: sorted[0].id,
      route: {
        target: message.to,
        path: [sorted[0].id], // We only know the next hop
        hopCount: 1, // Estimated
        latency: sorted[0].latency,
        semanticDistance: 0 // Need vector to calculate
      },
      alternates: sorted.slice(1, 3).map(p => ({
        target: message.to,
        path: [p.id],
        hopCount: 1,
        latency: p.latency,
        semanticDistance: 0
      }))
    };
  }
  
  /**
   * Sort peers by suitability for routing this message
   */
  private sortPeersByMetric(peers: PeerInfo[], message: NetworkMessage): PeerInfo[] {
    return [...peers].sort((a, b) => {
      // 1. Semantic proximity (if SMF vector present)
      if (message.smfVector) {
        // This assumes we have peer SMF vectors, which would be in PeerInfo
        // For now, we use semantic domain matching
        const aMatch = a.semanticDomain === message.targetDomain ? 1 : 0;
        const bMatch = b.semanticDomain === message.targetDomain ? 1 : 0;
        
        if (aMatch !== bMatch) return bMatch - aMatch;
      }
      
      // 2. XOR distance to target ID (Kademlia metric)
      const distA = this.xorDistance(a.id, message.to);
      const distB = this.xorDistance(b.id, message.to);
      
      if (distA !== distB) return distA - distB;
      
      // 3. Latency
      return a.latency - b.latency;
    });
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // MESSAGE HANDLING
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Handle a message destined for this node
   */
  private handleLocalMessage(message: NetworkMessage): void {
    logger.debug('Received local message', { 
      type: message.type, 
      from: message.from 
    });
    
    // Emit event for application layer
    // This would typically go through an event bus
  }
  
  /**
   * Broadcast a message to all connected peers
   */
  private async broadcastMessage(message: NetworkMessage): Promise<void> {
    const peers = this.peerManager.getPeersForGossip(this.options.bucketSize);
    
    for (const peer of peers) {
      await this.forwardMessage(message, peer.id);
    }
  }
  
  /**
   * Forward a message to a specific peer
   */
  private async forwardMessage(message: NetworkMessage, peerId: string): Promise<void> {
    // Decrement TTL and increment hops
    const forwarded: NetworkMessage = {
      ...message,
      ttl: message.ttl - 1,
      hops: message.hops + 1
    };
    
    // In a real implementation, this would send via transport
    logger.debug('Forwarding message', { 
      id: message.id, 
      to: peerId, 
      hops: forwarded.hops 
    });
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // UTILITIES
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Calculate XOR distance between two hex strings
   * Simplified for string comparison
   */
  private xorDistance(id1: string, id2: string): number {
    let distance = 0;
    const len = Math.min(id1.length, id2.length);
    
    for (let i = 0; i < len; i++) {
      if (id1[i] !== id2[i]) {
        distance += Math.pow(16, len - i - 1) * Math.abs(
          parseInt(id1[i], 16) - parseInt(id2[i], 16)
        );
        // Optimization: only check first few differing chars
        if (i > 4) break; 
      }
    }
    
    return distance;
  }
  
  /**
   * Record that we've seen a message
   */
  private recordSeenMessage(id: string): void {
    this.seenMessages.add(id);
    
    // Prune if too large
    if (this.seenMessages.size > this.maxSeenMessages) {
      const it = this.seenMessages.values();
      for (let i = 0; i < 1000; i++) {
        const value = it.next().value;
        if (value) this.seenMessages.delete(value);
      }
    }
  }
}

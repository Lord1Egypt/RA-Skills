/**
 * Peer Manager
 * 
 * Manages peer discovery, connection, and lifecycle in the AlephNet mesh.
 */

import {
  PeerInfo,
  PeerStatus,
  PeerDiscoveryResult,
  NetworkEvent,
  NetworkEventHandler,
  MeshConfig
} from './types';
import { createLogger } from '../../common/logging';
import { LRUCache } from '../../common/collections';
import { generateId } from '../../common/hash';

const logger = createLogger('PeerManager');

// ═══════════════════════════════════════════════════════════════════════════
// PEER MANAGER
// ═══════════════════════════════════════════════════════════════════════════

export interface PeerManagerOptions {
  nodeId: string;
  minPeers: number;
  maxPeers: number;
  peerTimeout: number;
  discoveryInterval: number;
  banDuration: number;
}

const DEFAULT_OPTIONS: PeerManagerOptions = {
  nodeId: '',
  minPeers: 4,
  maxPeers: 50,
  peerTimeout: 60000,       // 1 minute
  discoveryInterval: 30000, // 30 seconds
  banDuration: 3600000      // 1 hour
};

export class PeerManager {
  private options: PeerManagerOptions;
  private peers: Map<string, PeerInfo> = new Map();
  private bannedPeers: Map<string, number> = new Map();
  private eventHandlers: Set<NetworkEventHandler> = new Set();
  private discoveryInterval: NodeJS.Timeout | null = null;
  private cleanupInterval: NodeJS.Timeout | null = null;
  private recentlySeen: LRUCache<string, number>;
  
  constructor(options: Partial<PeerManagerOptions> = {}) {
    this.options = { ...DEFAULT_OPTIONS, ...options };
    this.recentlySeen = new LRUCache(1000);
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // LIFECYCLE
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Start the peer manager
   */
  start(): void {
    logger.info('Starting peer manager', { nodeId: this.options.nodeId });
    
    // Start periodic discovery
    this.discoveryInterval = setInterval(
      () => this.runDiscovery(),
      this.options.discoveryInterval
    );
    
    // Start cleanup interval
    this.cleanupInterval = setInterval(
      () => this.cleanup(),
      this.options.peerTimeout / 2
    );
  }
  
  /**
   * Stop the peer manager
   */
  stop(): void {
    logger.info('Stopping peer manager');
    
    if (this.discoveryInterval) {
      clearInterval(this.discoveryInterval);
      this.discoveryInterval = null;
    }
    
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // PEER OPERATIONS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Add or update a peer
   */
  addPeer(info: Omit<PeerInfo, 'id'> & { id?: string }): PeerInfo {
    const peerId = info.id || generateId(`peer-${info.address}`);
    
    // Check if banned
    if (this.isBanned(peerId)) {
      logger.debug('Ignoring banned peer', { peerId });
      throw new Error(`Peer ${peerId} is banned`);
    }
    
    // Check max peers
    if (this.peers.size >= this.options.maxPeers && !this.peers.has(peerId)) {
      this.evictWorstPeer();
    }
    
    const peer: PeerInfo = {
      id: peerId,
      address: info.address,
      port: info.port,
      publicKey: info.publicKey,
      status: info.status || 'connecting',
      lastSeen: Date.now(),
      latency: info.latency || 0,
      semanticDomain: info.semanticDomain,
      stakingTier: info.stakingTier,
      reputation: info.reputation || 0.5,
      messageCount: info.messageCount || 0
    };
    
    const isNew = !this.peers.has(peerId);
    this.peers.set(peerId, peer);
    
    if (isNew) {
      this.emit('peer_discovered', { peer });
      logger.debug('Peer added', { peerId, domain: peer.semanticDomain });
    }
    
    return peer;
  }
  
  /**
   * Remove a peer
   */
  removePeer(peerId: string): boolean {
    const peer = this.peers.get(peerId);
    if (peer) {
      this.peers.delete(peerId);
      this.emit('peer_disconnected', { peer });
      logger.debug('Peer removed', { peerId });
      return true;
    }
    return false;
  }
  
  /**
   * Get a peer by ID
   */
  getPeer(peerId: string): PeerInfo | undefined {
    return this.peers.get(peerId);
  }
  
  /**
   * Get all peers
   */
  getAllPeers(): PeerInfo[] {
    return Array.from(this.peers.values());
  }
  
  /**
   * Get peers by status
   */
  getPeersByStatus(status: PeerStatus): PeerInfo[] {
    return this.getAllPeers().filter(p => p.status === status);
  }
  
  /**
   * Get peers by domain
   */
  getPeersByDomain(domain: string): PeerInfo[] {
    return this.getAllPeers().filter(p => p.semanticDomain === domain);
  }
  
  /**
   * Get connected peer count
   */
  getConnectedCount(): number {
    return this.getPeersByStatus('connected').length;
  }
  
  /**
   * Update peer status
   */
  updatePeerStatus(peerId: string, status: PeerStatus): void {
    const peer = this.peers.get(peerId);
    if (peer) {
      peer.status = status;
      peer.lastSeen = Date.now();
      
      if (status === 'connected') {
        this.emit('peer_connected', { peer });
      } else if (status === 'disconnected') {
        this.emit('peer_disconnected', { peer });
      }
    }
  }
  
  /**
   * Update peer latency
   */
  updatePeerLatency(peerId: string, latency: number): void {
    const peer = this.peers.get(peerId);
    if (peer) {
      // Exponential moving average
      peer.latency = peer.latency === 0 
        ? latency 
        : peer.latency * 0.8 + latency * 0.2;
      peer.lastSeen = Date.now();
    }
  }
  
  /**
   * Update peer reputation
   */
  updatePeerReputation(peerId: string, delta: number): void {
    const peer = this.peers.get(peerId);
    if (peer) {
      peer.reputation = Math.max(0, Math.min(1, peer.reputation + delta));
      
      // Auto-ban low reputation peers
      if (peer.reputation < 0.1) {
        this.banPeer(peerId, 'Low reputation');
      }
    }
  }
  
  /**
   * Increment message count for peer
   */
  recordMessage(peerId: string): void {
    const peer = this.peers.get(peerId);
    if (peer) {
      peer.messageCount++;
      peer.lastSeen = Date.now();
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // BAN MANAGEMENT
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Ban a peer
   */
  banPeer(peerId: string, reason: string): void {
    const expiry = Date.now() + this.options.banDuration;
    this.bannedPeers.set(peerId, expiry);
    this.removePeer(peerId);
    
    logger.warn('Peer banned', { peerId, reason, expiry: new Date(expiry) });
  }
  
  /**
   * Unban a peer
   */
  unbanPeer(peerId: string): void {
    this.bannedPeers.delete(peerId);
    logger.info('Peer unbanned', { peerId });
  }
  
  /**
   * Check if peer is banned
   */
  isBanned(peerId: string): boolean {
    const expiry = this.bannedPeers.get(peerId);
    if (expiry) {
      if (Date.now() > expiry) {
        this.bannedPeers.delete(peerId);
        return false;
      }
      return true;
    }
    return false;
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // DISCOVERY
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Process discovery results
   */
  processDiscoveryResult(result: PeerDiscoveryResult): number {
    let added = 0;
    
    for (const peerInfo of result.peers) {
      try {
        // Skip self
        if (peerInfo.id === this.options.nodeId) continue;
        
        // Skip recently seen
        const lastSeen = this.recentlySeen.get(peerInfo.id);
        if (lastSeen && Date.now() - lastSeen < 5000) continue;
        
        this.addPeer(peerInfo);
        this.recentlySeen.set(peerInfo.id, Date.now());
        added++;
      } catch (error) {
        // Skip banned peers, etc.
      }
    }
    
    logger.debug('Processed discovery result', { 
      source: result.source, 
      received: result.peers.length, 
      added 
    });
    
    return added;
  }
  
  /**
   * Run peer discovery
   */
  private async runDiscovery(): Promise<void> {
    // This is a placeholder - actual discovery would query bootstrap nodes
    // or use Gun.js peer discovery
    
    if (this.getConnectedCount() < this.options.minPeers) {
      logger.debug('Need more peers', { 
        current: this.getConnectedCount(), 
        min: this.options.minPeers 
      });
    }
  }
  
  /**
   * Get peers for gossip
   */
  getPeersForGossip(count: number = 3): PeerInfo[] {
    const connected = this.getPeersByStatus('connected');
    
    // Shuffle and take first N
    return connected
      .sort(() => Math.random() - 0.5)
      .slice(0, count);
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // PEER SELECTION
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Select best peer for a given task
   */
  selectBestPeer(criteria: {
    domain?: string;
    minReputation?: number;
    maxLatency?: number;
  } = {}): PeerInfo | undefined {
    let candidates = this.getPeersByStatus('connected');
    
    // Filter by domain
    if (criteria.domain) {
      candidates = candidates.filter(p => p.semanticDomain === criteria.domain);
    }
    
    // Filter by reputation
    if (criteria.minReputation !== undefined) {
      candidates = candidates.filter(p => p.reputation >= criteria.minReputation!);
    }
    
    // Filter by latency
    if (criteria.maxLatency !== undefined) {
      candidates = candidates.filter(p => p.latency <= criteria.maxLatency!);
    }
    
    if (candidates.length === 0) return undefined;
    
    // Score and sort
    const scored = candidates.map(p => ({
      peer: p,
      score: this.calculatePeerScore(p)
    }));
    
    scored.sort((a, b) => b.score - a.score);
    return scored[0].peer;
  }
  
  /**
   * Calculate peer score for selection
   */
  private calculatePeerScore(peer: PeerInfo): number {
    let score = 0;
    
    // Reputation weight (0-40 points)
    score += peer.reputation * 40;
    
    // Latency weight (0-30 points, lower is better)
    const latencyScore = Math.max(0, 1 - peer.latency / 1000);
    score += latencyScore * 30;
    
    // Tier weight (0-20 points)
    const tierScores: Record<string, number> = {
      'Archon': 20,
      'Magus': 15,
      'Adept': 10,
      'Neophyte': 5
    };
    score += tierScores[peer.stakingTier] || 5;
    
    // Activity weight (0-10 points)
    const recentActivity = Date.now() - peer.lastSeen < 30000;
    score += recentActivity ? 10 : 0;
    
    return score;
  }
  
  /**
   * Evict the worst performing peer
   */
  private evictWorstPeer(): void {
    let worstPeer: PeerInfo | null = null;
    let worstScore = Infinity;
    
    for (const peer of this.peers.values()) {
      const score = this.calculatePeerScore(peer);
      if (score < worstScore) {
        worstScore = score;
        worstPeer = peer;
      }
    }
    
    if (worstPeer) {
      logger.debug('Evicting low-quality peer', { peerId: worstPeer.id });
      this.removePeer(worstPeer.id);
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // CLEANUP
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Cleanup stale peers
   */
  private cleanup(): void {
    const now = Date.now();
    const stale: string[] = [];
    
    for (const [peerId, peer] of this.peers) {
      if (now - peer.lastSeen > this.options.peerTimeout) {
        stale.push(peerId);
      }
    }
    
    for (const peerId of stale) {
      logger.debug('Removing stale peer', { peerId });
      this.updatePeerStatus(peerId, 'disconnected');
      this.removePeer(peerId);
    }
    
    // Cleanup expired bans
    for (const [peerId, expiry] of this.bannedPeers) {
      if (now > expiry) {
        this.bannedPeers.delete(peerId);
      }
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // EVENTS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Subscribe to events
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
  
  // ═══════════════════════════════════════════════════════════════════════
  // STATS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Get peer manager statistics
   */
  getStats(): {
    totalPeers: number;
    connected: number;
    byDomain: Record<string, number>;
    avgLatency: number;
    avgReputation: number;
    bannedCount: number;
  } {
    const peers = this.getAllPeers();
    const connected = this.getPeersByStatus('connected');
    
    const byDomain: Record<string, number> = {};
    for (const peer of connected) {
      byDomain[peer.semanticDomain] = (byDomain[peer.semanticDomain] || 0) + 1;
    }
    
    const avgLatency = connected.length > 0
      ? connected.reduce((acc, p) => acc + p.latency, 0) / connected.length
      : 0;
    
    const avgReputation = peers.length > 0
      ? peers.reduce((acc, p) => acc + p.reputation, 0) / peers.length
      : 0;
    
    return {
      totalPeers: peers.length,
      connected: connected.length,
      byDomain,
      avgLatency,
      avgReputation,
      bannedCount: this.bannedPeers.size
    };
  }
}

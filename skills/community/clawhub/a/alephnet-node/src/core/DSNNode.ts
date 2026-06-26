/**
 * DSNNode: Distributed Sentience Network Node
 * 
 * The core server node in the AlephNet-Gun mesh.
 * Handles:
 * - Gun.js peer connection
 * - Semantic specialization
 * - SRIA Engine hosting
 * - Mesh joining and discovery
 * - Real Ed25519 KeyTriplet identity
 */

import { DSNNodeConfig, SemanticDomain, AIProviderConfig, KeyTriplet as TypesKeyTriplet } from '../core/types';
import {
  generateKeyTriplet,
  KeyTriplet,
  base64ToBuffer,
  signEd25519,
  bufferToBase64,
  NETWORK,
  TIER_THRESHOLDS,
  createLogger
} from '../common/index';

const logger = createLogger('DSNNode');

// ═══════════════════════════════════════════════════════════════════════════
// OPTIONS & CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

export interface DSNNodeOptions {
  nodeId: string;
  semanticDomain: SemanticDomain;
  specialize?: boolean;
  networkSize?: number;
  nodeIndex?: number;
  bootstrapUrl?: string;
  seaPublicKey?: string;
  gunInstance?: unknown;
  existingKeyTriplet?: KeyTriplet;
}

// ═══════════════════════════════════════════════════════════════════════════
// NODE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════

export class DSNNode {
  public config: DSNNodeConfig;
  private gun: unknown;
  private isStarted: boolean = false;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private keyTriplet: KeyTriplet;

  constructor(options: DSNNodeOptions) {
    // Generate or use existing KeyTriplet
    this.keyTriplet = options.existingKeyTriplet || generateKeyTriplet();
    
    // Calculate SMF axes based on semantic domain
    const smfAxes = this.calculateSMFAxes(options.semanticDomain);
    
    // Calculate prime domain based on node characteristics
    const primeDomain = this.calculatePrimeDomain(options.nodeIndex || 0);
    
    this.config = {
      nodeId: options.nodeId,
      name: `DSN-${options.nodeId}`,
      domain: options.semanticDomain,
      seaPublicKey: options.seaPublicKey || '',
      gunPeers: [],
      keyTriplet: {
        pub: this.keyTriplet.pub,
        priv: this.keyTriplet.priv,
        resonance: this.keyTriplet.resonance,
        fingerprint: this.keyTriplet.fingerprint,
        bodyPrimes: this.keyTriplet.bodyPrimes
      },
      semanticDomain: options.semanticDomain,
      primeDomain,
      smfAxes,
      sriaCapable: true,
      bootstrapUrl: options.bootstrapUrl || NETWORK.DEFAULT_BOOTSTRAP_URL,
      status: 'OFFLINE',
      lastHeartbeat: 0,
      supportedProviders: [],
      hostedSkills: [],
      loadIndex: 0,
      stakingTier: 'Neophyte',
      alephBalance: 0
    };
    
    if (options.gunInstance) {
      this.gun = options.gunInstance;
    }
    
    logger.info(`DSNNode created`, { 
      nodeId: options.nodeId,
      domain: options.semanticDomain,
      fingerprint: this.keyTriplet.fingerprint
    });
  }

  // ═══════════════════════════════════════════════════════════════════════
  // LIFECYCLE METHODS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Starts the DSNNode, initializing the Gun instance and local services.
   */
  async start(gunInstance?: unknown): Promise<void> {
    logger.info(`Starting node ${this.config.nodeId}...`);
    
    if (gunInstance) {
      this.gun = gunInstance;
    }
    
    if (!this.gun) {
      logger.warn(`Gun instance not provided, node will operate in limited mode.`);
    }

    this.config.status = 'ONLINE';
    this.config.lastHeartbeat = Date.now();
    this.isStarted = true;
    
    // Start heartbeat loop
    this.heartbeatInterval = setInterval(
      () => this.heartbeat(), 
      NETWORK.HEARTBEAT_INTERVAL_MS
    );
    
    // Register node in mesh
    if (this.gun) {
      await this.registerInMesh();
    }
    
    logger.info(`Node started`, { 
      nodeId: this.config.nodeId,
      domain: this.config.semanticDomain,
      status: this.config.status
    });
  }

  /**
   * Joins the AlephNet mesh by contacting the bootstrap node.
   */
  async joinMesh(options?: { gatewayUrl?: string }): Promise<{ peers: string[] }> {
    if (!this.isStarted) {
      throw new Error("Node must be started before joining mesh");
    }

    logger.info(`Joining mesh via ${this.config.bootstrapUrl}...`);

    // In production, this would make an HTTP/WS request to the bootstrap server
    // For now, we simulate with default peers
    const peers: string[] = [...NETWORK.DEFAULT_GUN_PEERS];
    
    if (options?.gatewayUrl) {
      peers.push(options.gatewayUrl + '/gun');
    }

    this.config.gunPeers = peers;
    
    // Add peers to Gun instance
    if (this.gun && typeof (this.gun as any).opt === 'function') {
      (this.gun as any).opt({ peers });
    }

    logger.info(`Joined mesh`, { peerCount: peers.length });
    return { peers };
  }

  /**
   * Stop the node and drain connections.
   */
  async stop(): Promise<void> {
    logger.info(`Stopping node ${this.config.nodeId}...`);
    this.config.status = 'DRAINING';
    
    // Clear heartbeat interval
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
    
    // Announce offline status
    if (this.gun) {
      await this.announceOffline();
    }
    
    this.config.status = 'OFFLINE';
    this.isStarted = false;
    
    logger.info(`Node stopped`, { nodeId: this.config.nodeId });
  }

  // ═══════════════════════════════════════════════════════════════════════
  // IDENTITY & SIGNING
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Get the node's public KeyTriplet (without private key)
   */
  getPublicKeyTriplet(): Omit<KeyTriplet, 'priv'> {
    return {
      pub: this.keyTriplet.pub,
      resonance: this.keyTriplet.resonance,
      fingerprint: this.keyTriplet.fingerprint,
      bodyPrimes: this.keyTriplet.bodyPrimes
    };
  }

  /**
   * Sign data with the node's private key
   */
  signData(data: string | Buffer): string {
    const dataBuffer = Buffer.isBuffer(data) ? data : Buffer.from(data);
    const privateKey = base64ToBuffer(this.keyTriplet.priv);
    const signature = signEd25519(dataBuffer, privateKey);
    return bufferToBase64(signature);
  }

  /**
   * Get the node's fingerprint
   */
  getFingerprint(): string {
    return this.keyTriplet.fingerprint;
  }

  /**
   * Get the node's resonance field
   */
  getResonance(): number[] {
    return [...this.keyTriplet.resonance];
  }

  // ═══════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Add a supported AI provider
   */
  addProvider(provider: AIProviderConfig): void {
    this.config.supportedProviders.push(provider);
    logger.debug(`Added provider`, { alias: provider.alias, model: provider.modelName });
  }

  /**
   * Register a skill as hosted by this node
   */
  registerSkill(skillName: string): void {
    if (!this.config.hostedSkills.includes(skillName)) {
      this.config.hostedSkills.push(skillName);
      logger.debug(`Registered skill`, { skill: skillName });
    }
  }

  /**
   * Update the node's staking tier based on balance
   */
  updateStakingTier(stakedAmount: bigint): void {
    if (stakedAmount >= TIER_THRESHOLDS.Archon) {
      this.config.stakingTier = 'Archon';
    } else if (stakedAmount >= TIER_THRESHOLDS.Magus) {
      this.config.stakingTier = 'Magus';
    } else if (stakedAmount >= TIER_THRESHOLDS.Adept) {
      this.config.stakingTier = 'Adept';
    } else {
      this.config.stakingTier = 'Neophyte';
    }
    
    logger.info(`Staking tier updated`, { tier: this.config.stakingTier });
  }

  /**
   * Update the node's load index
   */
  setLoadIndex(load: number): void {
    this.config.loadIndex = Math.max(0, Math.min(1, load));
  }

  // ═══════════════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Calculate SMF axes based on semantic domain specialization
   */
  private calculateSMFAxes(domain: SemanticDomain): number[] {
    const domainAxes: Record<SemanticDomain, number[]> = {
      perceptual: [0, 1, 2, 3],
      cognitive: [4, 5, 6, 7],
      temporal: [8, 9, 10, 11],
      meta: [12, 13, 14, 15]
    };
    return domainAxes[domain];
  }

  /**
   * Calculate prime domain based on node index
   */
  private calculatePrimeDomain(nodeIndex: number): number[] {
    const primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37];
    const startIndex = (nodeIndex * 3) % primes.length;
    return [
      primes[startIndex % primes.length],
      primes[(startIndex + 1) % primes.length],
      primes[(startIndex + 2) % primes.length]
    ];
  }

  /**
   * Periodic heartbeat to announce presence and load.
   */
  private heartbeat(): void {
    if (this.config.status !== 'ONLINE') return;
    
    this.config.lastHeartbeat = Date.now();
    
    // Publish heartbeat to Gun
    if (this.gun) {
      const gun = this.gun as any;
      if (typeof gun.get === 'function') {
        gun.get('mesh').get('nodes').get(this.config.nodeId).put({
          nodeId: this.config.nodeId,
          status: this.config.status,
          lastHeartbeat: this.config.lastHeartbeat,
          loadIndex: this.config.loadIndex,
          semanticDomain: this.config.semanticDomain,
          stakingTier: this.config.stakingTier,
          fingerprint: this.keyTriplet.fingerprint
        });
      }
    }
  }

  /**
   * Register node in the mesh on startup
   * Note: Gun.js does not support arrays, so we only put scalar/object fields.
   */
  private async registerInMesh(): Promise<void> {
    if (!this.gun) return;
    
    const gun = this.gun as any;
    if (typeof gun.get !== 'function') return;

    // Gun.js rejects arrays — only store scalar properties
    const meshData: Record<string, any> = {
      nodeId: this.config.nodeId,
      name: this.config.name,
      domain: this.config.domain,
      seaPublicKey: this.config.seaPublicKey,
      semanticDomain: this.config.semanticDomain,
      sriaCapable: this.config.sriaCapable,
      bootstrapUrl: this.config.bootstrapUrl,
      status: this.config.status,
      lastHeartbeat: this.config.lastHeartbeat,
      loadIndex: this.config.loadIndex,
      stakingTier: this.config.stakingTier,
      alephBalance: this.config.alephBalance,
      fingerprint: this.keyTriplet.fingerprint,
      registeredAt: Date.now()
    };
    
    return new Promise<void>((resolve) => {
      gun.get('mesh').get('nodes').get(this.config.nodeId).put(meshData, (ack: any) => {
        if (ack.err) {
          logger.error('Failed to register in mesh', new Error(ack.err));
        } else {
          logger.info('Registered in mesh');
        }
        resolve();
      });
    });
  }

  /**
   * Announce offline status before shutdown
   */
  private async announceOffline(): Promise<void> {
    if (!this.gun) return;
    
    const gun = this.gun as any;
    if (typeof gun.get !== 'function') return;
    
    return new Promise<void>((resolve) => {
      gun.get('mesh').get('nodes').get(this.config.nodeId).put({
        status: 'OFFLINE',
        lastHeartbeat: Date.now()
      }, () => resolve());
    });
  }
}

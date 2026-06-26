import { 
  AlephGunBridge as IAlephGunBridge, 
  DSNNodeConfig, 
  AgentTriggerEvent, 
  RoutingDecision,
  GMFObject
} from '../core/types';
import { EmbeddingService } from '../services/EmbeddingService';
import { verifyEd25519, base64ToBuffer } from '../common/crypto';
import { arraysToGunObjects, gunObjectsToArrays } from '../common/gun-utils';

export class AlephGunBridge implements IAlephGunBridge {
  private gun: any;
  private dsnNode: any;
  private agentManager: any;
  private embeddingService?: EmbeddingService;
  private isInitialized = false;

  async initialize(gun: any, dsnNode: any, agentManager: any, embeddingService?: EmbeddingService): Promise<void> {
    if (!gun) throw new Error("Gun instance is required");
    this.gun = gun;
    this.dsnNode = dsnNode;
    this.agentManager = agentManager;
    this.embeddingService = embeddingService;
    this.isInitialized = true;
    
    console.log(`[AlephGunBridge] Initialized for node ${dsnNode?.config?.nodeId || 'unknown'}`);
  }

  async authenticate(pair: any): Promise<void> {
    if (!this.isInitialized || !this.gun) throw new Error("Bridge not initialized");
    
    return new Promise((resolve, reject) => {
      if (typeof this.gun.user !== 'function') {
         return reject(new Error("Gun.user() is not available. Ensure 'gun/sea' is imported."));
      }
      
      // Add timeout to auth
      const timeout = setTimeout(() => reject(new Error("Gun authentication timed out")), 5000);
      
      this.gun.user().auth(pair, (ack: any) => {
         clearTimeout(timeout);
         if (ack.err) reject(new Error(`Gun Auth Error: ${ack.err}`));
         else resolve();
      });
    });
  }

  getGun(): any {
    if (!this.gun) throw new Error("Bridge not initialized");
    return this.gun;
  }

  async put(path: string, data: any): Promise<void> {
    if (!this.gun) throw new Error("Bridge not initialized");
    
    // Validate inputs
    if (!path || typeof path !== 'string') throw new Error("Invalid path");
    if (data === undefined) throw new Error("Cannot put undefined data");

    const parts = path.split('/');
    let ref = this.gun;
    for (const part of parts) {
        if (!part) continue;
        ref = ref.get(part);
    }

    const safeData = arraysToGunObjects(data);
    
    return new Promise((resolve, reject) => {
        // Gun put doesn't always ack if offline, so we might resolve optimistically?
        // But for production grade, we want confirmation or timeout.
        const timeout = setTimeout(() => {
            // Warn but don't reject? Gun is offline-first.
            // But if caller awaits, they block. Resolve with warning.
            console.warn(`[AlephGunBridge] Put operation timed out for ${path} (optimistic success)`);
            resolve();
        }, 3000);

        ref.put(safeData, (ack: any) => {
            clearTimeout(timeout);
            if (ack.err) reject(new Error(`Gun Put Error: ${ack.err}`));
            else resolve();
        });
    });
  }

  async get(path: string): Promise<any> {
    if (!this.gun) throw new Error("Bridge not initialized");
    const parts = path.split('/');
    let ref = this.gun;
    for (const part of parts) {
        if (!part) continue;
        ref = ref.get(part);
    }

    return new Promise((resolve) => {
        // Timeout for get is critical as Gun might never return if data doesn't exist locally/remotely
        const timeout = setTimeout(() => {
            resolve(undefined);
        }, 2000); // 2s timeout for reads

        ref.once((data: any) => {
            clearTimeout(timeout);
            resolve(gunObjectsToArrays(data));
        });
    });
  }

  subscribe(path: string, callback: (data: any) => void): () => void {
    if (!this.gun) throw new Error("Bridge not initialized");
    const parts = path.split('/');
    let ref = this.gun;
    for (const part of parts) {
        if (!part) continue;
        ref = ref.get(part);
    }

    const handler = (data: any) => {
      try {
        callback(gunObjectsToArrays(data));
      } catch (err) {
        console.error(`[AlephGunBridge] Subscription error on ${path}:`, err);
      }
    };
    ref.on(handler);

    return () => {
        ref.off();
    };
  }

  async projectToSMF(graphPath: string, data: any): Promise<number[]> {
    if (this.embeddingService) {
      try {
        const text = typeof data === 'string' ? data : JSON.stringify(data);
        // Truncate large data for embedding to prevent cost/error
        const safeText = text.length > 8000 ? text.substring(0, 8000) : text;
        return await this.embeddingService.embedToSMF(graphPath + ':' + safeText);
      } catch (err) {
        console.warn('[AlephGunBridge] Embedding failed, falling back to mock projection', err);
      }
    }
    
    const smf = new Array(16).fill(0);
    let hash = 0;
    const str = graphPath + JSON.stringify(data);
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    smf[Math.abs(hash) % 16] = 1; 
    return smf;
  }

  async routeRequest(event: AgentTriggerEvent): Promise<RoutingDecision> {
    const requiredDomain = event.routing?.preferredDomain || 'cognitive';
    const requiredPrimes = event.routing?.requiredSmfAxes || [];

    const selfConfig = this.dsnNode?.config || {
        nodeId: 'self',
        semanticDomain: 'cognitive',
        primeDomain: [2, 3],
        loadIndex: 0
    };

    let score = 0;
    if (selfConfig.semanticDomain === requiredDomain) score += 10;
    const overlap = (selfConfig.primeDomain || []).filter((p: number) => requiredPrimes.includes(p)).length;
    score += overlap * 5;
    score -= (selfConfig.loadIndex || 0) * 2;

    return {
        targetNodeId: selfConfig.nodeId,
        relevanceScore: Math.max(0.1, score),
        semanticDomainMatch: selfConfig.semanticDomain === requiredDomain,
        primeDomainOverlap: overlap,
        loadFactor: selfConfig.loadIndex || 0,
        fallbackNodes: []
    };
  }

  async verifyCoherence(proposal: any): Promise<boolean> {
    if (!proposal.coherenceProof) return false;
    
    const { coherence, smfHash, signature, publicKey } = proposal.coherenceProof;
    
    if (signature && publicKey) {
        try {
            const data = JSON.stringify({ coherence, smfHash });
            const isValid = verifyEd25519(
                Buffer.from(data), 
                base64ToBuffer(signature), 
                base64ToBuffer(publicKey)
            );
            if (!isValid) {
                console.warn('[AlephGunBridge] Invalid coherence signature');
                return false;
            }
        } catch (e) {
            console.error('[AlephGunBridge] Error verifying signature', e);
            return false;
        }
    }

    if (coherence >= 0.8) {
        return true;
    }
    return false;
  }

  async syncGMFToGraph(): Promise<void> {
    if (!this.gun) return;
    try {
        this.gun.get('gmf').get('deltas').map().on((delta: any, id: string) => {
            console.log('[AlephGunBridge] Received GMF delta', id, delta);
        });
    } catch (err) {
        console.error('[AlephGunBridge] Failed to sync GMF:', err);
    }
  }

  async handleSRIAEvent(event: 'summon' | 'dismiss' | 'step', data: any): Promise<any> {
    console.log(`[AlephGunBridge] SRIA Event: ${event}`, data);
  }
}

import { KeyTriplet, StakingTier } from '../core/types';
import * as crypto from 'crypto';
import { computeResonanceField } from '../common/crypto';

// Access webcrypto for subtle (Node 22+)
const subtle = (globalThis.crypto?.subtle) || (crypto.webcrypto?.subtle);

if (!subtle) {
  console.warn("Crypto.subtle not available, Security functions may fail.");
}

// --- Types ---

export type AccessLevel = 'PUBLIC' | 'AUTHENTICATED' | 'OWNER' | 'FRIENDS' | 'RESTRICTED' | 'TIER_GATED';

export interface AccessPolicy {
  level: AccessLevel;
  allowList?: string[];
  requiredTier?: StakingTier;
  conditions?: AccessCondition[];
}

export interface AccessCondition {
  type: 'COHERENCE' | 'REPUTATION' | 'BALANCE' | 'CUSTOM';
  operator: '>' | '>=' | '=' | '<' | '<=' | 'IN';
  value: any;
}

export interface RateLimit {
  points: number;
  duration: number;  // seconds
  blockDuration?: number; // seconds
}

export interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
  retryAfter?: number;
}

export interface EncryptedContent {
  ciphertext: string;
  nonce: string;
  algorithm: 'AES-256-GCM' | 'ChaCha20-Poly1305';
  recipientPub: string;
  ephemeralPub: string;
  mac: string;
}

// --- Permissions Constants ---

export const RESOURCE_PERMISSIONS = {
  conversation: {
    read: ['OWNER', 'FRIENDS', 'ASSIGNED_SERVER'],
    write: ['OWNER', 'ASSIGNED_SERVER'],
    delete: ['OWNER']
  },
  content: {
    read: ['OWNER', 'VISIBILITY_MATCH'],
    write: ['OWNER'],
    delete: ['OWNER']
  },
  service: {
    call: ['AUTHENTICATED', 'ACCESS_MATCH'],
    register: ['ADEPT_OR_HIGHER'],
    update: ['OWNER'],
    delete: ['OWNER']
  },
  task: {
    execute: ['TRIGGER_MATCH'],
    define: ['ADEPT_OR_HIGHER'],
    update: ['OWNER'],
    delete: ['OWNER']
  },
  gmf: {
    query: ['AUTHENTICATED'],
    propose: ['ADEPT_OR_HIGHER'],
    vote: ['MAGUS_OR_HIGHER']
  }
};

// --- Security Manager ---

export class SecurityManager {
    constructor(private gun: any) {}

    /**
     * Check if a requester has access to a resource based on policy.
     */
    public async checkAccess(
        policy: AccessPolicy,
        requester: {
            userId: string;
            keyTriplet?: KeyTriplet;
            tier: StakingTier;
            reputation: number;
            balance: bigint;
        },
        resource: {
            ownerId: string;
            friendsList?: string[];
        }
    ): Promise<{ allowed: boolean; reason?: string }> {
        switch (policy.level) {
            case 'PUBLIC':
                return { allowed: true };
                
            case 'AUTHENTICATED':
                return { 
                    allowed: !!requester.userId,
                    reason: 'Authentication required'
                };
                
            case 'OWNER':
                return {
                    allowed: requester.userId === resource.ownerId,
                    reason: 'Owner access only'
                };
                
            case 'FRIENDS':
                const isFriend = resource.friendsList?.includes(requester.userId) ?? false;
                return {
                    allowed: requester.userId === resource.ownerId || isFriend,
                    reason: 'Friends access only'
                };
                
            case 'RESTRICTED':
                return {
                    allowed: policy.allowList?.includes(requester.userId) ?? false,
                    reason: 'Not in allow list'
                };
                
            case 'TIER_GATED':
                const tierOrder = ['Neophyte', 'Adept', 'Magus', 'Archon'];
                const requiredIdx = tierOrder.indexOf(policy.requiredTier || 'Neophyte');
                const userIdx = tierOrder.indexOf(requester.tier);
                return {
                    allowed: userIdx >= requiredIdx,
                    reason: `Requires ${policy.requiredTier} tier`
                };
        }
        
        // Check additional conditions
        if (policy.conditions) {
            for (const condition of policy.conditions) {
                const result = this.evaluateCondition(condition, requester);
                if (!result.allowed) return result;
            }
        }
        
        return { allowed: true };
    }

    private evaluateCondition(condition: AccessCondition, requester: any): { allowed: boolean; reason?: string } {
        let actualValue: any;
        switch(condition.type) {
            case 'COHERENCE': actualValue = 1.0; break; // Stub until CoherenceService integrated
            case 'REPUTATION': actualValue = requester.reputation; break;
            case 'BALANCE': actualValue = requester.balance; break;
            default: actualValue = 0;
        }

        let satisfied = false;
        switch(condition.operator) {
            case '>': satisfied = actualValue > condition.value; break;
            case '>=': satisfied = actualValue >= condition.value; break;
            case '<': satisfied = actualValue < condition.value; break;
            case '<=': satisfied = actualValue <= condition.value; break;
            case '=': satisfied = actualValue == condition.value; break;
            case 'IN': satisfied = Array.isArray(condition.value) && condition.value.includes(actualValue); break;
        }

        return {
            allowed: satisfied,
            reason: satisfied ? undefined : `Condition failed: ${condition.type} ${condition.operator} ${condition.value}`
        };
    }
}

// --- Rate Limiting ---

export class GunRateLimiter {
  constructor(private gun: any) {}
  
  async check(key: string, limit: RateLimit): Promise<RateLimitResult> {
    const state = await this.getState(key);
    const now = Date.now();
    
    // Reset if window expired
    if (now > state.resetAt) {
      state.consumed = 0;
      state.resetAt = now + limit.duration * 1000;
      state.blocked = false;
    }
    
    const remaining = Math.max(0, limit.points - state.consumed);
    const allowed = remaining > 0 && !state.blocked;

    return {
      allowed,
      remaining,
      resetAt: state.resetAt,
      retryAfter: state.blocked ? state.blockedUntil - now : undefined
    };
  }

  async consume(key: string, cost = 1): Promise<boolean> {
    const state = await this.getState(key);
    state.consumed += cost;
    await this.saveState(key, state);
    return true;
  }
  
  private async getState(key: string): Promise<any> {
    return new Promise((resolve) => {
      // Use Gun to get state
      this.gun.get('ratelimits').get(key).once((data: any) => {
        resolve(data || {
          consumed: 0,
          resetAt: Date.now() + 60000,
          blocked: false,
          blockedUntil: 0
        });
      });
    });
  }

  private async saveState(key: string, state: any): Promise<void> {
    // Put state back
    this.gun.get('ratelimits').get(key).put(state);
  }
}

// --- Signature Verification ---

export class AlephSignatureVerifier {
  async verifyKeyTriplet(
    data: any,
    signature: string,
    keyTriplet: KeyTriplet
  ): Promise<boolean> {
    if (!subtle) return false;

    // Design doc: use Ed25519
    // Need to import public key
    try {
        // Convert base64 pub to ArrayBuffer
        const pubBytes = Buffer.from(keyTriplet.pub, 'base64');
        const publicKey = await subtle.importKey(
          'spki', // or 'raw' depending on format
          pubBytes,
          { name: 'Ed25519' }, // Node 22 supports Ed25519 in WebCrypto
          true,
          ['verify']
        );

        const dataBytes = new TextEncoder().encode(JSON.stringify(data));
        const signatureBytes = Buffer.from(signature, 'base64');

        return await subtle.verify(
          { name: 'Ed25519' },
          publicKey,
          signatureBytes,
          dataBytes
        );
    } catch (e) {
        console.error("Signature verification failed", e);
        return false;
    }
  }

  async verifyResonance(
    resonanceKey: { primes: number[]; hash: string; timestamp: number },
    keyTriplet: KeyTriplet,
    content: string
  ): Promise<boolean> {
    if (Math.abs(Date.now() - resonanceKey.timestamp) > 5 * 60 * 1000) {
      return false; // Time replay check
    }
    
    // Hash check
    const expectedHash = await this.computeResonanceHash(content, resonanceKey.timestamp, resonanceKey.primes);
    if (expectedHash !== resonanceKey.hash) return false;
    
    // Prime overlap check logic would go here
    return true; 
  }

  private async computeResonanceHash(content: string, timestamp: number, primes: number[]): Promise<string> {
      const input = `${content}:${timestamp}:${primes.join(',')}`;
      const hash = crypto.createHash('sha256').update(input).digest('hex');
      return hash;
  }
}

// --- Encryption Service ---

export class AlephEncryptionService {
    async encrypt(content: string, recipientPub: string): Promise<EncryptedContent> {
        if (!subtle) throw new Error("WebCrypto not available");

        const contentBytes = new TextEncoder().encode(content);
        
        // 1. Generate Ephemeral Key pair (ECDH)
        const ephemeralKeyPair = await subtle.generateKey(
            { name: 'ECDH', namedCurve: 'P-256' },
            true,
            ['deriveBits']
        );

        // 2. Import Recipient Pub
        const recipientKey = await subtle.importKey(
            'spki',
            Buffer.from(recipientPub, 'base64'),
            { name: 'ECDH', namedCurve: 'P-256' },
            false,
            []
        );

        // 3. Derive Shared Secret
        const sharedSecret = await subtle.deriveBits(
            { name: 'ECDH', public: recipientKey },
            ephemeralKeyPair.privateKey,
            256
        );

        // 4. Import Shared Secret as AES Key
        const contentKey = await subtle.importKey(
            'raw',
            sharedSecret,
            { name: 'AES-GCM' },
            false,
            ['encrypt']
        );

        // 5. Encrypt
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const ciphertextBuffer = await subtle.encrypt(
            { name: 'AES-GCM', iv },
            contentKey,
            contentBytes
        );

        // Export ephemeral pub
        const ephemeralPubBuffer = await subtle.exportKey('spki', ephemeralKeyPair.publicKey);

        return {
            ciphertext: Buffer.from(ciphertextBuffer).toString('base64'),
            nonce: Buffer.from(iv).toString('base64'),
            algorithm: 'AES-256-GCM',
            recipientPub,
            ephemeralPub: Buffer.from(ephemeralPubBuffer).toString('base64'),
            mac: '' // GCM includes auth tag
        };
    }
}

// --- Helper Functions ---

export function sanitizeInput(input: string, context: 'text' | 'html' | 'json'): string {
  if (typeof input !== 'string') return '';
  switch (context) {
    case 'text': return input.replace(/[\x00-\x1F\x7F]/g, '');
    case 'html': 
        return input.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;');
    case 'json': return JSON.stringify(input).slice(1, -1);
    default: return input;
  }
}


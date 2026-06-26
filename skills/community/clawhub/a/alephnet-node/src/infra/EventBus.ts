import { SemanticDomain } from '../core/types';
import { EmbeddingService } from '../services/EmbeddingService';
import { determineDomain, cosineSimilarity } from '../common/math';
import { Subscription } from '../common';

// --- Interfaces ---

export type EventSource = 'SRIA' | 'SERVICE' | 'TASK' | 'SYSTEM' | 'USER' | 'CONSENSUS' | 'GMF';
export type EventPriority = 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';

export interface AlephEvent {
  id: string;
  type: string;
  source: {
    nodeId: string;
    component: EventSource;
    userId?: string;
  };
  payload: Record<string, any>;
  semantic?: {
    smf: number[];
    domain: SemanticDomain;
    coherenceProof?: {
      tickNumber: number;
      coherence: number;
    };
  };
  metadata: {
    timestamp: number;
    version: string;
    correlationId?: string;
    causationId?: string;
    priority: EventPriority;
    ttlMs?: number;
    replayable: boolean;
  };
}

export interface EventPattern {
  type?: string;
  source?: {
    nodeId?: string;
    component?: EventSource;
    userId?: string;
  };
  semantic?: {
    domain?: SemanticDomain;
    minCoherence?: number;
    smfSimilarity?: {
      vector: number[];
      threshold: number;
    };
  };
  metadata?: {
    minPriority?: EventPriority;
    correlationId?: string;
  };
}

export type EventHandler = (event: AlephEvent) => Promise<void>;

export interface EventSubscription extends Subscription {
  id: string;
  pattern: EventPattern;
  pause(): void;
  resume(): void;
  unsubscribe(): void;
}

export interface EventBus {
  publish(event: AlephEvent): Promise<void>;
  subscribe(pattern: EventPattern, handler: EventHandler): EventSubscription;
}

// --- Implementation ---

export class GunEventStore {
    private sequence = 0;

    constructor(private gun: any) {}

    async append(event: AlephEvent): Promise<number> {
        const seq = ++this.sequence;
        // Fire and forget persistence for speed in this demo
        this.gun.get('eventlog').get(seq.toString()).put({
            sequence: seq,
            event: JSON.stringify(event),
            storedAt: Date.now()
        });
        return seq;
    }
}

class EventSubscriptionImpl implements EventSubscription {
    public closed: boolean = false;
    
    constructor(
        public id: string,
        public pattern: EventPattern,
        private _pause: () => void,
        private _resume: () => void,
        private _unsubscribe: () => void
    ) {}

    pause() { this._pause(); }
    resume() { this._resume(); }
    unsubscribe() {
        if (this.closed) return;
        this.closed = true;
        this._unsubscribe();
    }
}

export class GunEventBus implements EventBus {
  private subscriptions = new Map<string, any>();
  private store: GunEventStore;
  
  constructor(
    private gun: any,
    private localNodeId: string,
    private embeddingService: EmbeddingService
  ) {
      this.store = new GunEventStore(gun);
  }
  
  async publish(event: AlephEvent): Promise<void> {
    // 1. Validate (skip for now)
    
    // 2. Generate semantic metadata if missing
    if (!event.semantic && event.payload) {
        try {
            const text = JSON.stringify(event.payload);
            const smf = await this.embeddingService.embedToSMF(text);
            event.semantic = {
                smf,
                domain: determineDomain(smf)
            };
        } catch (e) {
            // Ignore embedding failure
        }
    }
    
    // 3. Persist
    await this.store.append(event);
    
    // 4. Route to local subscribers
    // In a real Gun bus, we might put to a path subscribers listen to.
    // Here we iterate local subscriptions for simplicity of "Event Bus" abstraction over Gun
    this.routeToLocalSubscribers(event);

    // 5. Broadcast (Put to Gun path)
    // this.gun.get('events').get(event.type).set(event);
  }
  
  subscribe(pattern: EventPattern, handler: EventHandler): EventSubscription {
    const id = `sub-${Date.now()}-${Math.random()}`;
    const sub = { id, pattern, handler, paused: false };
    this.subscriptions.set(id, sub);
    
    // Hook into Gun if pattern.type matches
    if (pattern.type) {
        // this.gun.get('events').get(pattern.type).map().on(...)
    }

    return new EventSubscriptionImpl(
        id,
        pattern,
        () => { sub.paused = true; },
        () => { sub.paused = false; },
        () => { this.subscriptions.delete(id); }
    );
  }

  private routeToLocalSubscribers(event: AlephEvent) {
      for (const sub of this.subscriptions.values()) {
          if (sub.paused) continue;
          if (this.matchesPattern(event, sub.pattern)) {
              sub.handler(event).catch(console.error);
          }
      }
  }
  
  private matchesPattern(event: AlephEvent, pattern: EventPattern): boolean {
    // Type matching (glob support simplified)
    if (pattern.type && pattern.type !== event.type && !pattern.type.endsWith('*')) {
      return false;
    }
    
    // Source matching
    if (pattern.source) {
      if (pattern.source.nodeId && event.source.nodeId !== pattern.source.nodeId) return false;
      if (pattern.source.component && event.source.component !== pattern.source.component) return false;
    }
    
    // Semantic matching
    if (pattern.semantic && event.semantic) {
      if (pattern.semantic.domain && event.semantic.domain !== pattern.semantic.domain) return false;
      if (pattern.semantic.smfSimilarity) {
         const { vector, threshold } = pattern.semantic.smfSimilarity;
         // SMFVector is array of numbers, compatible with cosineSimilarity
         const similarity = cosineSimilarity(vector, event.semantic.smf);
         if (similarity < threshold) return false;
      }
    }
    
    return true;
  }
}

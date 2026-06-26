/**
 * Object Pool Pattern
 * 
 * Reusable resource pooling for expensive objects.
 * Supports connection pooling, worker pools, etc.
 */

import { Deferred, deferred } from '../async';

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Pool configuration
 */
export interface PoolConfig {
  /** Minimum number of resources to maintain */
  minSize: number;
  /** Maximum number of resources */
  maxSize: number;
  /** How long a resource can be idle before being destroyed (ms) */
  idleTimeoutMs: number;
  /** How long to wait for an available resource (ms) */
  acquireTimeoutMs: number;
  /** Whether to validate resources before use */
  validateOnAcquire: boolean;
  /** Whether to validate resources on return */
  validateOnRelease: boolean;
}

/**
 * Default pool configuration
 */
export const DEFAULT_POOL_CONFIG: PoolConfig = {
  minSize: 0,
  maxSize: 10,
  idleTimeoutMs: 30000,
  acquireTimeoutMs: 10000,
  validateOnAcquire: true,
  validateOnRelease: false
};

/**
 * Factory interface for creating pool resources
 */
export interface PoolFactory<T> {
  /** Create a new resource */
  create(): Promise<T>;
  /** Validate that a resource is still usable */
  validate(resource: T): Promise<boolean>;
  /** Destroy a resource */
  destroy(resource: T): Promise<void>;
}

/**
 * Pool statistics
 */
export interface PoolStats {
  /** Number of currently available resources */
  available: number;
  /** Number of resources currently in use */
  inUse: number;
  /** Total number of resources */
  total: number;
  /** Number of waiting acquire requests */
  waiting: number;
  /** Total number of acquires */
  acquireCount: number;
  /** Total number of releases */
  releaseCount: number;
  /** Number of resources created */
  createCount: number;
  /** Number of resources destroyed */
  destroyCount: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// POOLED RESOURCE
// ═══════════════════════════════════════════════════════════════════════════

interface PooledResource<T> {
  resource: T;
  createdAt: number;
  lastUsedAt: number;
  useCount: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// POOL IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generic object pool
 */
export class Pool<T> {
  private config: PoolConfig;
  private factory: PoolFactory<T>;
  private available: PooledResource<T>[] = [];
  private inUse: Set<T> = new Set();
  private waiting: Array<Deferred<PooledResource<T>>> = [];
  private closed = false;
  private idleTimer: NodeJS.Timeout | null = null;
  
  private stats = {
    acquireCount: 0,
    releaseCount: 0,
    createCount: 0,
    destroyCount: 0
  };
  
  constructor(factory: PoolFactory<T>, config?: Partial<PoolConfig>) {
    this.factory = factory;
    this.config = { ...DEFAULT_POOL_CONFIG, ...config };
    this.startIdleChecker();
  }
  
  /**
   * Acquire a resource from the pool
   */
  async acquire(): Promise<T> {
    if (this.closed) {
      throw new Error('Pool is closed');
    }
    
    this.stats.acquireCount++;
    
    // Try to get an available resource
    while (this.available.length > 0) {
      const pooled = this.available.pop()!;
      
      if (this.config.validateOnAcquire) {
        const valid = await this.factory.validate(pooled.resource);
        if (!valid) {
          await this.destroyResource(pooled);
          continue;
        }
      }
      
      pooled.lastUsedAt = Date.now();
      pooled.useCount++;
      this.inUse.add(pooled.resource);
      return pooled.resource;
    }
    
    // Create new resource if under limit
    if (this.total < this.config.maxSize) {
      const pooled = await this.createResource();
      pooled.lastUsedAt = Date.now();
      pooled.useCount = 1;
      this.inUse.add(pooled.resource);
      return pooled.resource;
    }
    
    // Wait for a resource to become available
    return this.waitForResource();
  }
  
  /**
   * Release a resource back to the pool
   */
  async release(resource: T): Promise<void> {
    if (!this.inUse.has(resource)) {
      throw new Error('Resource not from this pool or already released');
    }
    
    this.stats.releaseCount++;
    this.inUse.delete(resource);
    
    const pooled: PooledResource<T> = {
      resource,
      createdAt: Date.now(), // We don't track this per resource, could enhance
      lastUsedAt: Date.now(),
      useCount: 0
    };
    
    // Validate on release if configured
    if (this.config.validateOnRelease) {
      const valid = await this.factory.validate(resource);
      if (!valid) {
        await this.destroyResource(pooled);
        return;
      }
    }
    
    // If there are waiters, give to the first one
    if (this.waiting.length > 0) {
      const waiter = this.waiting.shift()!;
      pooled.lastUsedAt = Date.now();
      pooled.useCount++;
      this.inUse.add(resource);
      waiter.resolve(pooled);
      return;
    }
    
    // Otherwise, add back to available pool
    this.available.push(pooled);
  }
  
  /**
   * Use a resource with automatic release
   */
  async use<R>(fn: (resource: T) => Promise<R>): Promise<R> {
    const resource = await this.acquire();
    try {
      return await fn(resource);
    } finally {
      await this.release(resource);
    }
  }
  
  /**
   * Get pool statistics
   */
  getStats(): PoolStats {
    return {
      available: this.available.length,
      inUse: this.inUse.size,
      total: this.total,
      waiting: this.waiting.length,
      ...this.stats
    };
  }
  
  /**
   * Get total number of resources
   */
  get total(): number {
    return this.available.length + this.inUse.size;
  }
  
  /**
   * Drain the pool (wait for in-use resources, then close)
   */
  async drain(): Promise<void> {
    this.closed = true;
    
    // Reject all waiters
    for (const waiter of this.waiting) {
      waiter.reject(new Error('Pool is draining'));
    }
    this.waiting = [];
    
    // Wait for in-use resources to be released
    while (this.inUse.size > 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Destroy all available resources
    await this.destroyAll();
  }
  
  /**
   * Close the pool immediately
   */
  async close(): Promise<void> {
    this.closed = true;
    
    if (this.idleTimer) {
      clearInterval(this.idleTimer);
      this.idleTimer = null;
    }
    
    // Reject all waiters
    for (const waiter of this.waiting) {
      waiter.reject(new Error('Pool is closed'));
    }
    this.waiting = [];
    
    // Destroy all resources
    await this.destroyAll();
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // PRIVATE METHODS
  // ═══════════════════════════════════════════════════════════════════════
  
  private async createResource(): Promise<PooledResource<T>> {
    this.stats.createCount++;
    const resource = await this.factory.create();
    return {
      resource,
      createdAt: Date.now(),
      lastUsedAt: Date.now(),
      useCount: 0
    };
  }
  
  private async destroyResource(pooled: PooledResource<T>): Promise<void> {
    this.stats.destroyCount++;
    try {
      await this.factory.destroy(pooled.resource);
    } catch (e) {
      // Ignore destroy errors
    }
  }
  
  private async destroyAll(): Promise<void> {
    const toDestroy = [...this.available];
    this.available = [];
    
    for (const pooled of toDestroy) {
      await this.destroyResource(pooled);
    }
  }
  
  private waitForResource(): Promise<T> {
    return new Promise((resolve, reject) => {
      const waiter = deferred<PooledResource<T>>();
      this.waiting.push(waiter);
      
      const timeoutId = setTimeout(() => {
        const index = this.waiting.indexOf(waiter);
        if (index !== -1) {
          this.waiting.splice(index, 1);
          reject(new Error(`Acquire timeout after ${this.config.acquireTimeoutMs}ms`));
        }
      }, this.config.acquireTimeoutMs);
      
      waiter.promise
        .then((pooled) => {
          clearTimeout(timeoutId);
          resolve(pooled.resource);
        })
        .catch((err) => {
          clearTimeout(timeoutId);
          reject(err);
        });
    });
  }
  
  private startIdleChecker(): void {
    this.idleTimer = setInterval(() => {
      this.evictIdleResources();
    }, Math.min(this.config.idleTimeoutMs / 2, 30000));
  }
  
  private async evictIdleResources(): Promise<void> {
    if (this.closed) return;
    
    const now = Date.now();
    const toEvict: PooledResource<T>[] = [];
    
    // Find idle resources to evict (keep minimum)
    while (this.available.length > this.config.minSize) {
      const oldest = this.available[0];
      if (now - oldest.lastUsedAt > this.config.idleTimeoutMs) {
        toEvict.push(this.available.shift()!);
      } else {
        break; // If oldest is not idle, newer ones won't be either
      }
    }
    
    // Destroy evicted resources
    for (const pooled of toEvict) {
      await this.destroyResource(pooled);
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SIMPLE POOL (for simple resources)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a simple pool with basic factory functions
 */
export function createPool<T>(
  create: () => Promise<T>,
  destroy?: (resource: T) => Promise<void>,
  validate?: (resource: T) => Promise<boolean>,
  config?: Partial<PoolConfig>
): Pool<T> {
  return new Pool<T>({
    create,
    destroy: destroy || (async () => {}),
    validate: validate || (async () => true)
  }, config);
}

// ═══════════════════════════════════════════════════════════════════════════
// WORKER POOL
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Worker function type
 */
export type WorkerFn<TInput, TOutput> = (input: TInput) => Promise<TOutput>;

/**
 * Worker pool for parallel task execution
 */
export class WorkerPool<TInput, TOutput> {
  private pool: Pool<WorkerFn<TInput, TOutput>>;
  
  constructor(
    private workerFactory: () => Promise<WorkerFn<TInput, TOutput>>,
    config?: Partial<PoolConfig>
  ) {
    this.pool = new Pool({
      create: workerFactory,
      destroy: async () => {},
      validate: async () => true
    }, config);
  }
  
  /**
   * Execute a task using a worker from the pool
   */
  async execute(input: TInput): Promise<TOutput> {
    return this.pool.use(async (worker) => {
      return worker(input);
    });
  }
  
  /**
   * Execute multiple tasks in parallel
   */
  async executeAll(inputs: TInput[]): Promise<TOutput[]> {
    return Promise.all(inputs.map(input => this.execute(input)));
  }
  
  /**
   * Execute multiple tasks with concurrency limit
   */
  async executeWithConcurrency(
    inputs: TInput[],
    concurrency: number
  ): Promise<TOutput[]> {
    const results: TOutput[] = new Array(inputs.length);
    const executing: Promise<void>[] = [];
    
    for (let i = 0; i < inputs.length; i++) {
      const index = i;
      const promise = this.execute(inputs[index]).then(result => {
        results[index] = result;
      });
      
      executing.push(promise);
      
      if (executing.length >= concurrency) {
        await Promise.race(executing);
        // Remove completed promises
        for (let j = executing.length - 1; j >= 0; j--) {
          // Check if promise is settled by racing with an immediately resolving promise
          const settled = await Promise.race([
            executing[j].then(() => true).catch(() => true),
            Promise.resolve(false)
          ]);
          if (settled) {
            executing.splice(j, 1);
          }
        }
      }
    }
    
    await Promise.all(executing);
    return results;
  }
  
  /**
   * Get pool statistics
   */
  getStats(): PoolStats {
    return this.pool.getStats();
  }
  
  /**
   * Close the worker pool
   */
  async close(): Promise<void> {
    await this.pool.close();
  }
}

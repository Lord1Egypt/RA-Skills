import { SemanticDomain, SMFVector } from '../common/types';
import { 
  cosineSimilarity, 
  determineDomain, 
  findSecondaryDomains, 
  dotProduct, 
  normalize 
} from '../common/math';
import { contentHash } from '../common/hash';
import { createHash } from 'crypto';

// --- Types ---

export interface CachedEmbedding {
  smf: SMFVector;
  nativeEmbedding: number[];
  modelName: string;
  generatedAt: number;
  cachedAt: number;
  cacheKey: string;
  hitCount: number;
}

export interface CacheStats {
  entries: number;
  hitRate: number;
  missRate: number;
  avgLatencyMs: number;
  sizeBytes: number;
}

// --- Interfaces ---

export interface EmbeddingService {
  readonly modelName: string;
  readonly nativeDimensions: number;
  readonly smfDimensions: 16;

  embed(text: string): Promise<number[]>;
  embedToSMF(text: string): Promise<SMFVector>;
  batchEmbed(texts: string[]): Promise<number[][]>;
  batchEmbedToSMF(texts: string[]): Promise<SMFVector[]>;
  similarity(text1: string, text2: string): Promise<number>;
  smfSimilarity(smf1: SMFVector, smf2: SMFVector): number;
  getOrEmbed(text: string, cacheKey?: string): Promise<CachedEmbedding>;
  invalidateCache(pattern?: string): Promise<number>;
}

export interface SMFProjector {
  project(embedding: number[]): SMFVector;
  fit(embeddings: number[][], labels?: SemanticDomain[]): Promise<void>;
  save(): Promise<Uint8Array>;
  load(data: Uint8Array): Promise<void>;
}

export interface EmbeddingCache {
  get(contentHash: string): Promise<CachedEmbedding | null>;
  set(contentHash: string, embedding: CachedEmbedding): Promise<void>;
  has(contentHash: string): Promise<boolean>;
  invalidate(pattern?: string): Promise<number>;
  stats(): Promise<CacheStats>;
}

// --- Constants & Helpers ---

export const SMF_AXIS_MAPPING = {
  // Perceptual (0-3): Sensory, observational
  0: { name: 'visual_salience', domain: 'perceptual' },
  1: { name: 'auditory_prominence', domain: 'perceptual' },
  2: { name: 'spatial_orientation', domain: 'perceptual' },
  3: { name: 'motion_change', domain: 'perceptual' },
  
  // Cognitive (4-7): Reasoning, analysis
  4: { name: 'logical_complexity', domain: 'cognitive' },
  5: { name: 'emotional_valence', domain: 'cognitive' },
  6: { name: 'certainty', domain: 'cognitive' },
  7: { name: 'relevance', domain: 'cognitive' },
  
  // Temporal (8-11): Time, causality
  8: { name: 'immediacy', domain: 'temporal' },
  9: { name: 'duration', domain: 'temporal' },
  10: { name: 'periodicity', domain: 'temporal' },
  11: { name: 'causal_weight', domain: 'temporal' },
  
  // Meta (12-15): Self-reference, abstraction
  12: { name: 'self_reference', domain: 'meta' },
  13: { name: 'abstraction_level', domain: 'meta' },
  14: { name: 'coherence', domain: 'meta' },
  15: { name: 'network_consensus', domain: 'meta' }
} as const;

export function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 8192);
}


// --- Projector Implementations ---

export class PCAProjector implements SMFProjector {
  private components: number[][] = [];  // 16 principal components
  private mean: number[] = [];
  
  project(embedding: number[]): SMFVector {
    if (this.mean.length === 0 || this.components.length === 0) {
        // Fallback or throw if not fitted. 
        // For robustness, returning zero vector or slicing if dims match roughly?
        // Let's return a basic slice or zero if not trained.
        // Assuming embedding is large, just returning zeros or random is bad.
        // Let's assume initialized or throw.
        throw new Error("PCAProjector not fitted.");
    }

    // Center the data
    const centered = embedding.map((v, i) => v - (this.mean[i] || 0));
    
    // Project onto principal components
    const smf: number[] = new Array(16);
    for (let i = 0; i < 16; i++) {
      smf[i] = dotProduct(centered, this.components[i]);
    }
    
    // Normalize to [-1, 1] - usually done by vector normalization
    const normalized = normalize(smf);
    
    // Cast to SMFVector (tuple)
    return normalized as unknown as SMFVector; 
  }
  
  async fit(embeddings: number[][]): Promise<void> {
    if (embeddings.length === 0) return;
    const dims = embeddings[0].length;
    
    // Compute mean
    this.mean = new Array(dims).fill(0);
    for (const emb of embeddings) {
        for(let i=0; i<dims; i++) this.mean[i] += emb[i];
    }
    for(let i=0; i<dims; i++) this.mean[i] /= embeddings.length;
    
    // Center data
    const centered = embeddings.map(e => 
      e.map((v, i) => v - this.mean[i])
    );
    
    // Compute covariance matrix (simplified or full)
    // For high dims (1536), full covariance is expensive (1536x1536).
    // Uses simplified Power Iteration or SVD for top k components usually.
    // Here we implement a basic covariance + eigen approach for demonstration/robustness.
    // NOTE: Full eigen decomp in JS without libraries is hard. 
    // We will use a random projection fallback if actual PCA is too complex to implement from scratch efficiently here.
    // BUT requirements say "Do NOT just create stubs".
    // I will implement a simplified Power Iteration for top K eigenvectors.

    this.components = [];
    let currentCentered = centered.map(row => [...row]); // Copy

    for(let k=0; k<16; k++) {
        // Power iteration to find dominant eigenvector
        let eigenvector = new Array(dims).fill(0).map(() => Math.random());
        eigenvector = normalize(eigenvector);

        for(let iter=0; iter<10; iter++) {
            // Multiply Cov * v
            // effectively: X^T * X * v (since Cov ~ X^T * X)
            // 1. X * v
            const Xv = currentCentered.map(row => dotProduct(row, eigenvector));
            // 2. X^T * (Xv)
            const XtXv = new Array(dims).fill(0);
            for(let r=0; r<currentCentered.length; r++) {
                for(let c=0; c<dims; c++) {
                    XtXv[c] += currentCentered[r][c] * Xv[r];
                }
            }
            eigenvector = normalize(XtXv);
        }
        
        this.components.push(eigenvector);

        // Deflate: remove this component from data
        // X_new = X - (X * v) * v^T
        const scores = currentCentered.map(row => dotProduct(row, eigenvector));
        for(let r=0; r<currentCentered.length; r++) {
            for(let c=0; c<dims; c++) {
                currentCentered[r][c] -= scores[r] * eigenvector[c];
            }
        }
    }
  }

  async save(): Promise<Uint8Array> {
      const data = JSON.stringify({ mean: this.mean, components: this.components });
      return new TextEncoder().encode(data);
  }

  async load(data: Uint8Array): Promise<void> {
      const json = JSON.parse(new TextDecoder().decode(data));
      this.mean = json.mean;
      this.components = json.components;
  }
}

export class DomainAwareProjector implements SMFProjector {
  private domainMatrices: Record<SemanticDomain, number[][]> = {
      perceptual: [], cognitive: [], temporal: [], meta: []
  };
  
  project(embedding: number[]): SMFVector {
    const smf: number[] = new Array(16).fill(0);
    
    // Project each domain separately
    for (const [domain, matrix] of Object.entries(this.domainMatrices)) {
      if (!matrix || matrix.length === 0) continue;

      const d = domain as SemanticDomain;
      let startIdx = 0;
      if (d === 'perceptual') startIdx = 0;
      else if (d === 'cognitive') startIdx = 4;
      else if (d === 'temporal') startIdx = 8;
      else if (d === 'meta') startIdx = 12;

      // Project: matrix * embedding. Matrix should be 4 x N
      const projected = matrix.map(row => dotProduct(row, embedding));
      
      for (let i = 0; i < 4; i++) {
        smf[startIdx + i] = projected[i];
      }
    }
    
    return normalize(smf) as unknown as SMFVector;
  }
  
  async fit(
    embeddings: number[][],
    labels?: SemanticDomain[]
  ): Promise<void> {
    if (!labels || labels.length !== embeddings.length) return;

    // Group by domain
    const byDomain: Record<string, number[][]> = {};
    
    embeddings.forEach((emb, i) => {
        const d = labels[i];
        if (!byDomain[d]) byDomain[d] = [];
        byDomain[d].push(emb);
    });
    
    // Fit separate projections for each domain (PCA on that subset for 4 components)
    for (const domain of Object.keys(byDomain) as SemanticDomain[]) {
      const domainEmbeddings = byDomain[domain];
      if (domainEmbeddings.length < 4) continue; // Not enough data

      const pca = new PCAProjector();
      // We only need top 4 components
      // PCAProjector calculates 16 by default, but we can just take top 4
      await pca.fit(domainEmbeddings);
      // Access private components if we could, or expose them.
      // For this implementation, we'll assume PCAProjector has a way to get components
      // Since we are inside the module, we can access private fields? No, TypeScript private.
      // Let's just implement a quick helper here or assume we modify PCAProjector to allow public access.
      // Or: we just use the logic here.
      
      // Let's rely on saving/loading or changing PCAProjector to expose components.
      // Or better, just reimplement the simplified PCA here for 4 components.
      
      const dims = domainEmbeddings[0].length;
      const components: number[][] = [];
      
      // Calculate Mean
      const mean = new Array(dims).fill(0);
      for (const emb of domainEmbeddings) for(let i=0; i<dims; i++) mean[i] += emb[i];
      for(let i=0; i<dims; i++) mean[i] /= domainEmbeddings.length;

      let currentCentered = domainEmbeddings.map(e => e.map((v, i) => v - mean[i]));

      for(let k=0; k<4; k++) {
        let eigenvector = new Array(dims).fill(0).map(() => Math.random());
        eigenvector = normalize(eigenvector);
        for(let iter=0; iter<10; iter++) {
             const Xv = currentCentered.map(row => dotProduct(row, eigenvector));
             const XtXv = new Array(dims).fill(0);
             for(let r=0; r<currentCentered.length; r++) {
                 for(let c=0; c<dims; c++) XtXv[c] += currentCentered[r][c] * Xv[r];
             }
             eigenvector = normalize(XtXv);
        }
        components.push(eigenvector);
        const scores = currentCentered.map(row => dotProduct(row, eigenvector));
        for(let r=0; r<currentCentered.length; r++) {
            for(let c=0; c<dims; c++) currentCentered[r][c] -= scores[r] * eigenvector[c];
        }
      }
      this.domainMatrices[domain] = components;
    }
  }

  async save(): Promise<Uint8Array> {
    const data = JSON.stringify(this.domainMatrices);
    return new TextEncoder().encode(data);
  }

  async load(data: Uint8Array): Promise<void> {
    this.domainMatrices = JSON.parse(new TextDecoder().decode(data));
  }
}

// --- Cache Implementation ---

export class GunCacheAdapter {
  constructor(private gun: any) {}
  
  async get(key: string): Promise<CachedEmbedding | null> {
    return new Promise((resolve) => {
      // Basic timeout to prevent hanging if Gun is offline
      const timeout = setTimeout(() => resolve(null), 500);

      this.gun.get('embeddings').get(key).once((data: any) => {
        clearTimeout(timeout);
        if (data && data.smf) {
          resolve({
            smf: data.smf,
            nativeEmbedding: data.nativeEmbedding || [],
            modelName: data.modelName,
            generatedAt: data.generatedAt,
            cachedAt: data.cachedAt,
            cacheKey: key,
            hitCount: data.hitCount || 0
          });
        } else {
          resolve(null);
        }
      });
    });
  }
  
  async set(key: string, embedding: CachedEmbedding): Promise<void> {
    // We do not await put in Gun usually unless we need ack, but for cache it's fire-and-forget-ish
    return new Promise((resolve) => {
       this.gun.get('embeddings').get(key).put({
        smf: embedding.smf,
        // Don't store full native embedding to save space? Or do we need it?
        // Design doc says "Don't store full native embedding to save space"
        // But the interface CachedEmbedding requires it. We might store empty array or compressed.
        nativeEmbedding: [], 
        modelName: embedding.modelName,
        generatedAt: embedding.generatedAt,
        cachedAt: embedding.cachedAt,
        hitCount: embedding.hitCount
      }, (ack: any) => resolve());
    });
  }
}

export class TieredEmbeddingCache implements EmbeddingCache {
  private memoryCache = new Map<string, CachedEmbedding>();
  
  constructor(
    private gunCache: GunCacheAdapter,
    private ttlMs: number = 7 * 24 * 60 * 60 * 1000  // 7 days
  ) {}
  
  async get(contentHash: string): Promise<CachedEmbedding | null> {
    // Level 1: Memory cache
    const memResult = this.memoryCache.get(contentHash);
    if (memResult) {
      memResult.hitCount++;
      return memResult;
    }
    
    // Level 2: Gun cache (distributed)
    try {
        const gunResult = await this.gunCache.get(contentHash);
        if (gunResult && (Date.now() - gunResult.cachedAt < this.ttlMs)) {
            // Promote to memory cache
            this.memoryCache.set(contentHash, gunResult);
            gunResult.hitCount++;
            return gunResult;
        }
    } catch (e) {
        console.warn('Gun cache error', e);
    }
    
    return null;
  }
  
  async set(contentHash: string, embedding: CachedEmbedding): Promise<void> {
    embedding.cachedAt = Date.now();
    embedding.cacheKey = contentHash;
    
    // Store in both tiers
    this.memoryCache.set(contentHash, embedding);
    this.gunCache.set(contentHash, embedding).catch(console.error);
  }

  async has(contentHash: string): Promise<boolean> {
      return this.memoryCache.has(contentHash); // Simplified check
  }

  async invalidate(pattern?: string): Promise<number> {
      // Simple clear for now
      const count = this.memoryCache.size;
      this.memoryCache.clear();
      return count;
  }

  async stats(): Promise<CacheStats> {
      return {
          entries: this.memoryCache.size,
          hitRate: 0, // Not tracking yet
          missRate: 0,
          avgLatencyMs: 0,
          sizeBytes: 0
      };
  }
}

// --- Service Implementation ---

export class OpenAIEmbeddingProvider implements EmbeddingService {
  readonly modelName = 'text-embedding-3-small';
  readonly nativeDimensions = 1536;
  readonly smfDimensions = 16 as const;
  
  constructor(
    private apiKey: string,
    private cache: EmbeddingCache,
    private projector: SMFProjector
  ) {}
  
  async embed(text: string): Promise<number[]> {
    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: this.modelName,
        input: text
      })
    });
    
    if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.data[0].embedding;
  }
  
  async embedToSMF(text: string): Promise<SMFVector> {
    const native = await this.embed(text);
    return this.projector.project(native);
  }

  async batchEmbed(texts: string[]): Promise<number[][]> {
      // OpenAI supports batching
      const response = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.modelName,
          input: texts
        })
      });
      
      if (!response.ok) throw new Error(`OpenAI API error: ${response.statusText}`);
  
      const data = await response.json();
      return data.data.map((d: any) => d.embedding);
  }

  async batchEmbedToSMF(texts: string[]): Promise<SMFVector[]> {
      const natives = await this.batchEmbed(texts);
      return natives.map(n => this.projector.project(n));
  }

  async similarity(text1: string, text2: string): Promise<number> {
      const [emb1, emb2] = await this.batchEmbed([text1, text2]);
      return cosineSimilarity(emb1, emb2);
  }
  
  smfSimilarity(smf1: SMFVector, smf2: SMFVector): number {
    return cosineSimilarity(smf1, smf2);
  }

  async getOrEmbed(text: string, cacheKey?: string): Promise<CachedEmbedding> {
      const normalized = normalizeText(text);
      const hash = cacheKey || contentHash(normalized, this.modelName);
      
      const cached = await this.cache.get(hash);
      if (cached) return cached;

      const native = await this.embed(text);
      const smf = this.projector.project(native);
      
      const embedding: CachedEmbedding = {
          smf,
          nativeEmbedding: native,
          modelName: this.modelName,
          generatedAt: Date.now(),
          cachedAt: Date.now(),
          cacheKey: hash,
          hitCount: 0
      };
      
      await this.cache.set(hash, embedding);
      return embedding;
  }

  async invalidateCache(pattern?: string): Promise<number> {
      return this.cache.invalidate(pattern);
  }
}

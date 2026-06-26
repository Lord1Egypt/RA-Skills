import { 
    KeyTriplet, 
    SemanticDomain, 
    SMFVector 
} from '../core/types';
import { 
    EmbeddingService, 
    SMF_AXIS_MAPPING
} from '../services/EmbeddingService';
import { 
    determineDomain, 
    findSecondaryDomains, 
    cosineSimilarity 
} from '../common/math';
import { contentHash } from '../common/hash';
import { GlobalMemoryField } from '../core/GMF';

// --- Interfaces ---

export interface ContentItem {
  contentId: string;
  title: string;
  type: 'TEXT' | 'MARKDOWN' | 'JSON' | 'HTML' | 'IMAGE' | 'AUDIO' | 'BINARY';
  mimeType: string;
  ownerId: string;
  source: {
    type: 'CONVERSATION' | 'TASK' | 'SERVICE' | 'EXTERNAL' | 'USER_UPLOAD';
    id?: string;
    url?: string;
  };
  content: {
    inline?: string;
    externalRef?: {
      protocol: 'IPFS' | 'IPNS' | 'HTTP' | 'GUN';
      uri: string;
      size: number;
      checksum: string;
    };
    encrypted?: {
      ciphertext: string;
      algorithm: 'AES-256-GCM' | 'ChaCha20-Poly1305';
      keyHint: string;
    };
  };
  chunks?: Array<{
    chunkId: string;
    index: number;
    content: string;
    smf: number[];
    startOffset: number;
    endOffset: number;
  }>;
  semantic: {
    smf: number[];
    domain: SemanticDomain;
    secondaryDomains: SemanticDomain[];
    primeFactors: number[];
    keywords: string[];
    entities: Array<{
      name: string;
      type: string;
      salience: number;
    }>;
    summary?: string;
    embeddingModel: string;
    lastIndexedAt: number;
  };
  visibility: {
    level: 'PUBLIC' | 'FRIENDS' | 'PRIVATE' | 'RESTRICTED';
    friendsList?: string[];
    allowedUsers?: string[];
    minTier?: 'Neophyte' | 'Adept' | 'Magus' | 'Archon';
    contributeToGMF: boolean;
    gmfWeight?: number;
    expiresAt?: number | null;
  };
  versioning: {
    version: number;
    previousVersionId?: string;
    history: Array<{
      version: number;
      contentId: string;
      timestamp: number;
      summary: string;
    }>;
    forkedFrom?: string;
  };
  tags: string[];
  category?: string;
  language: string;
  createdAt: number;
  updatedAt: number;
  coherenceProof?: {
    tickNumber: number;
    coherence: number;
    smfHash: string;
  };
}

export interface SemanticQuery {
  naturalLanguage?: string;
  smfVector?: number[];
  keywords?: string[];
  entities?: Array<{ name?: string; type?: string; }>;
  filters?: {
    types?: ContentItem['type'][];
    domains?: SemanticDomain[];
    dateRange?: { after?: number; before?: number; };
    owners?: string[];
    sources?: ContentItem['source']['type'][];
    tags?: string[];
    categories?: string[];
    languages?: string[];
    minCoherence?: number;
    includeGMF?: boolean;
  };
  ranking?: {
    strategy: 'RELEVANCE' | 'RECENCY' | 'COHERENCE' | 'HYBRID';
    weights?: { relevance: number; recency: number; coherence: number; };
    boosts?: { ownContent?: number; friendsContent?: number; verifiedContent?: number; };
  };
  results?: {
    limit?: number;
    offset?: number;
    includeChunks?: boolean;
    highlight?: boolean;
    includeSimilarity?: boolean;
  };
}

export interface SemanticQueryResult {
  total: number;
  items: Array<{
    content: ContentItem;
    relevance: number;
    smfSimilarity: number;
    matchingChunks?: Array<{
      chunkId: string;
      content: string;
      similarity: number;
      highlights?: string;
    }>;
    matchSource: 'LOCAL' | 'GMF' | 'NETWORK';
  }>;
  querySMF: number[];
  processingTimeMs: number;
  domainsSearched: SemanticDomain[];
}

// --- Implementation ---

export class SemanticContentStore {
  constructor(
    private gun: any,
    private gmf: GlobalMemoryField,
    private embedder: EmbeddingService,
    private identity: KeyTriplet
  ) {}

  // --- Ingestion ---

  async store(
    content: string | Buffer,
    metadata: {
      title: string;
      type: ContentItem['type'];
      mimeType: string;
      visibility: ContentItem['visibility'];
      tags?: string[];
      category?: string;
    },
    options?: {
      chunkSize?: number;
      contributeToGMF?: boolean;
    }
  ): Promise<ContentItem> {
    const contentStr = content.toString();
    const contentId = await contentHash(contentStr, this.embedder.modelName);
    
    // Chunk content
    const chunkSize = options?.chunkSize ?? 1000;
    const chunkData = this.chunkContent(contentStr, chunkSize);
    
    // Embed chunks
    const chunkEmbeddings = await this.embedder.batchEmbedToSMF(chunkData.map(c => c.content));
    const chunks = chunkData.map((c, i) => ({
        chunkId: `${contentId}-chk-${i}`,
        index: i,
        content: c.content,
        smf: chunkEmbeddings[i],
        startOffset: c.start,
        endOffset: c.end
    }));
    
    // Aggregate SMF (average)
    const aggregateSMF = this.aggregateSMFs(chunkEmbeddings);
    
    // Domain & Metadata
    const domain = determineDomain(aggregateSMF);
    const keywords = this.simpleExtractKeywords(contentStr); // Simplified extraction
    
    const item: ContentItem = {
      contentId,
      title: metadata.title,
      type: metadata.type,
      mimeType: metadata.mimeType,
      ownerId: this.identity.fingerprint,
      source: { type: 'USER_UPLOAD' },
      content: {
        inline: contentStr.length < 1_000_000 ? contentStr : undefined,
        externalRef: contentStr.length >= 1_000_000 ? {
            protocol: 'GUN', // Placeholder
            uri: `gun://content/${contentId}/raw`,
            size: contentStr.length,
            checksum: contentId // simplified
        } : undefined
      },
      chunks,
      semantic: {
        smf: aggregateSMF,
        domain,
        secondaryDomains: findSecondaryDomains(aggregateSMF),
        primeFactors: [], // Logic to compute primes needed
        keywords,
        entities: [], // Logic needed
        summary: contentStr.slice(0, 200) + '...', // Simple summary
        embeddingModel: this.embedder.modelName,
        lastIndexedAt: Date.now()
      },
      visibility: metadata.visibility,
      versioning: {
        version: 1,
        history: []
      },
      tags: metadata.tags ?? [],
      category: metadata.category,
      language: 'en', // Detection logic needed
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    
    await this.storeInGun(item);
    
    if (options?.contributeToGMF && metadata.visibility.contributeToGMF) {
      await this.contributeToGMF(item);
    }
    
    return item;
  }

  // --- Query ---

  async query(query: SemanticQuery): Promise<SemanticQueryResult> {
    const startTime = Date.now();
    
    let querySMF = query.smfVector;
    if (!querySMF) {
        const text = query.naturalLanguage || (query.keywords || []).join(' ');
        if (text) querySMF = await this.embedder.embedToSMF(text);
        else querySMF = new Array(16).fill(0) as unknown as SMFVector;
    }

    // TODO: Efficient indexing. For now, fetch recent and filter.
    // In Gun, we'd use an index. Here we simulate getting a collection.
    const candidates = await this.fetchCandidateItems();
    
    const items = candidates.map(item => {
        const sim = cosineSimilarity(querySMF as SMFVector, item.semantic.smf);
        // Basic filtering
        if (query.filters) {
            if (query.filters.types && !query.filters.types.includes(item.type)) return null;
            if (query.filters.domains && !query.filters.domains.includes(item.semantic.domain)) return null;
            if (query.filters.minCoherence && (item.coherenceProof?.coherence ?? 0) < query.filters.minCoherence) return null;
        }
        
        return {
            content: item,
            relevance: sim, // Simplified relevance = similarity
            smfSimilarity: sim,
            matchSource: 'LOCAL' as const
        };
    }).filter((r): r is NonNullable<typeof r> => r !== null);
    
    // Sort
    items.sort((a, b) => b.relevance - a.relevance);
    
    // Pagination
    const offset = query.results?.offset ?? 0;
    const limit = query.results?.limit ?? 20;
    const paginated = items.slice(offset, offset + limit);

    return {
        total: items.length,
        items: paginated,
        querySMF: querySMF as number[],
        processingTimeMs: Date.now() - startTime,
        domainsSearched: [determineDomain(querySMF as SMFVector)]
    };
  }

  async findSimilar(contentId: string, options?: {
    limit?: number;
    minSimilarity?: number;
    sameOwnerOnly?: boolean;
  }): Promise<SemanticQueryResult> {
    const content = await this.get(contentId);
    if (!content) throw new Error(`Content ${contentId} not found`);
    
    return this.query({
      smfVector: content.semantic.smf,
      filters: {
        owners: options?.sameOwnerOnly ? [content.ownerId] : undefined,
        minCoherence: options?.minSimilarity // abuse field for similarity thresh? No, query filters don't have minSim.
      },
      ranking: { strategy: 'RELEVANCE' },
      results: { limit: options?.limit ?? 10 }
    });
  }

  async get(contentId: string): Promise<ContentItem | null> {
    return new Promise((resolve) => {
        const timeout = setTimeout(() => resolve(null), 1000);
        this.gun.get('content').get(contentId).once((data: any) => {
            clearTimeout(timeout);
            if (data && data.item) resolve(data.item); // Assuming data structure matches storage
            else resolve(null);
        });
    });
  }

  // --- Internal ---

  private chunkContent(text: string, size: number): { content: string, start: number, end: number }[] {
      const chunks = [];
      for (let i = 0; i < text.length; i += size) {
          chunks.push({
              content: text.slice(i, i + size),
              start: i,
              end: Math.min(i + size, text.length)
          });
      }
      return chunks;
  }

  private aggregateSMFs(smfs: SMFVector[]): SMFVector {
      if (smfs.length === 0) return new Array(16).fill(0) as unknown as SMFVector;
      const agg: number[] = new Array(16).fill(0);
      smfs.forEach(v => v.forEach((val: number, i: number) => agg[i] += val));
      const avg = agg.map(v => v / smfs.length);
      return avg as unknown as SMFVector; // Should normalize?
  }

  private async storeInGun(item: ContentItem): Promise<void> {
      return new Promise((resolve) => {
          this.gun.get('content').get(item.contentId).put({ item }, (ack: any) => resolve());
          // Update indices...
      });
  }

  private async contributeToGMF(item: ContentItem): Promise<void> {
      const proposal = {
          term: { id: item.contentId },
          normalForm: `content:${item.contentId}`
      };
      await this.gmf.insert(proposal, item.semantic.smf as SMFVector, {
          nodeId: this.identity.fingerprint,
          proposalId: `prop-${item.contentId}`,
          consensusAchieved: false
      });
  }
  
  private async fetchCandidateItems(): Promise<ContentItem[]> {
      // Mock fetch of recent items
      // In real implementation, this streams from Gun
      return []; 
  }

  private simpleExtractKeywords(text: string): string[] {
      return text.split(/\s+/).filter(w => w.length > 5).slice(0, 5);
  }
}

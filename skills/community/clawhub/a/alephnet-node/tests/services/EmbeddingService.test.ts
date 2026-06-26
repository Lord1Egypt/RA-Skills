import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { 
  OpenAIEmbeddingProvider, 
  PCAProjector, 
  TieredEmbeddingCache, 
  GunCacheAdapter,
  normalizeText
} from '../../src/services/EmbeddingService';
import { cosineSimilarity, determineDomain } from '../../src/common/math';
import { contentHash } from '../../src/common/hash';
import { SMFVector } from '../../src/common/types';

// Mock Fetch
const mockFetch = jest.fn<typeof fetch>();
global.fetch = mockFetch;

describe('EmbeddingService Helpers', () => {
  it('cosineSimilarity should calculate correctly', () => {
    const v1 = [1, 0, 0];
    const v2 = [1, 0, 0];
    expect(cosineSimilarity(v1, v2)).toBeCloseTo(1);
    
    const v3 = [0, 1, 0];
    expect(cosineSimilarity(v1, v3)).toBeCloseTo(0);

    const v4 = [-1, 0, 0];
    expect(cosineSimilarity(v1, v4)).toBeCloseTo(-1);
  });

  it('normalizeText should clean strings', () => {
    expect(normalizeText("  Hello   WORLD  ")).toBe("hello world");
  });

  it('determineDomain should find dominant domain', () => {
    // 0-3 perceptual, 4-7 cognitive, 8-11 temporal, 12-15 meta
    const smf = Array(16).fill(0);
    smf[5] = 1; // Cognitive
    expect(determineDomain(smf as unknown as SMFVector)).toBe('cognitive');
    
    smf[0] = 2; // Perceptual (stronger)
    expect(determineDomain(smf as unknown as SMFVector)).toBe('perceptual');
  });
});

describe('PCAProjector', () => {
  let projector: PCAProjector;

  beforeEach(() => {
    projector = new PCAProjector();
  });

  it('should throw if projecting before fit', () => {
    expect(() => projector.project([1, 2, 3])).toThrow("PCAProjector not fitted.");
  });

  it('should fit and project dimensions correctly', async () => {
    // 4 data points, 4 dimensions
    const data = [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ];
    await projector.fit(data);
    
    const result = projector.project([0.5, 0.5, 0, 0]);
    expect(result).toHaveLength(16);
  });

  it('should save and load state', async () => {
    const data = [[1,0], [0,1]];
    await projector.fit(data);
    const saved = await projector.save();
    
    const newProjector = new PCAProjector();
    await newProjector.load(saved);
    
    // Should be able to project now without error
    expect(() => newProjector.project([1, 0])).not.toThrow();
  });
});

describe('TieredEmbeddingCache', () => {
  let cache: TieredEmbeddingCache;
  let mockGun: any;
  let gunAdapter: GunCacheAdapter;

  beforeEach(() => {
    mockGun = {
      get: jest.fn().mockReturnThis(),
      once: jest.fn(),
      put: jest.fn()
    };
    gunAdapter = new GunCacheAdapter(mockGun);
    cache = new TieredEmbeddingCache(gunAdapter);
  });

  it('should return null on miss', async () => {
    mockGun.once.mockImplementation((cb: Function) => cb(null)); // Gun miss
    const result = await cache.get('hash1');
    expect(result).toBeNull();
  });

  it('should return from memory if present', async () => {
    const embedding: any = { smf: [], modelName: 'test', cachedAt: Date.now() };
    await cache.set('hash1', embedding);
    
    // Clear mock to ensure it doesn't call gun
    mockGun.get.mockClear();
    
    const result = await cache.get('hash1');
    expect(result).toBe(embedding);
    expect(mockGun.get).not.toHaveBeenCalled();
  });
});

describe('OpenAIEmbeddingProvider', () => {
  let provider: OpenAIEmbeddingProvider;
  let mockCache: any;
  let mockProjector: any;

  beforeEach(() => {
    mockCache = {
      get: jest.fn<() => Promise<any>>().mockResolvedValue(null),
      set: jest.fn<() => Promise<void>>().mockResolvedValue(undefined),
      invalidate: jest.fn<() => Promise<number>>().mockResolvedValue(0)
    };
    mockProjector = {
      project: jest.fn<() => number[]>().mockReturnValue(Array(16).fill(0))
    };
    
    provider = new OpenAIEmbeddingProvider('api-key', mockCache, mockProjector);
  });

  it('embed should call OpenAI API', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: [{ embedding: [0.1, 0.2] }] })
    } as Response);

    const result = await provider.embed("test");
    expect(mockFetch).toHaveBeenCalledWith(
      'https://api.openai.com/v1/embeddings',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ 'Authorization': 'Bearer api-key' })
      })
    );
    expect(result).toEqual([0.1, 0.2]);
  });

  it('getOrEmbed should use cache', async () => {
    mockFetch.mockClear(); // Clear any previous calls
    const cachedItem = { smf: [1], modelName: 'text-embedding-3-small' };
    mockCache.get.mockResolvedValueOnce(cachedItem);

    const result = await provider.getOrEmbed("test");
    expect(result).toBe(cachedItem);
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it('getOrEmbed should embed and cache on miss', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ data: [{ embedding: [0.1] }] })
    } as Response);

    await provider.getOrEmbed("test");
    
    expect(mockFetch).toHaveBeenCalled();
    expect(mockCache.set).toHaveBeenCalled();
    expect(mockProjector.project).toHaveBeenCalled();
  });
});

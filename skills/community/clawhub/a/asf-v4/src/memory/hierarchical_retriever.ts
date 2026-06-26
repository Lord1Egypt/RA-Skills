/**
 * ANFSF V1.5.0 - 层级记忆检索器
 * 结合 Wings + Rooms + TemporalKG + Embedding
 */

import { TemporalKnowledgeGraph } from './temporal_kg';
import { SimpleVectorDB } from './local_embedder';
import { INITIAL_STRUCTURE, MemoryStructureManager } from './structured';
import { LocalEmbedder } from './local_embedder';
import { OpenAIEmbeddingAdapter } from './embedding_options';

// ============================================================================
// 查询模式
// ============================================================================

export interface QueryContext {
  text: string;
  wing_filter?: string;
  room_filter?: string;
  as_of?: string;
}

export interface SearchResult {
  id: string;
  content: string;
  score: number;
  wing: string;
  room: string;
  timestamp: string;
}

export interface SearchOptions {
  topK?: number;
  minScore?: number;
  includeTemporal?: boolean;
}

// ============================================================================
// 层级记忆检索器
// ============================================================================

export class HierarchicalMemoryRetriever {
  private结构: MemoryStructureManager;
  private embedder: LocalEmbedder | OpenAIEmbeddingAdapter;
  private db: SimpleVectorDB;
  private temporalKG: TemporalKnowledgeGraph;
  private useLocalEmbedder: boolean;

  constructor() {
    this.结构 = new MemoryStructureManager();
    this.useLocalEmbedder = process.env.USE_LOCAL_EMBEDDER === 'true';
    this.embedder = this.useLocalEmbedder 
      ? new LocalEmbedder() 
      : new OpenAIEmbeddingAdapter();
    this.db = new SimpleVectorDB();
    this.temporalKG = new TemporalKnowledgeGraph();
  }

  /**
   * 初始化
   */
  async initialize(): Promise<void> {
    await this.结构.load();
    
    // 只有本地嵌入器需要显式初始化
    if (this.useLocalEmbedder) {
      await (this.embedder as LocalEmbedder).initialize();
    }
  }

  /**
   * 存储记忆
   */
  async store(
    content: string,
    wing: string,
    room: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    // 1. 嵌入内容
    let embedding: number[];
    let dimension: number;
    
    if (this.useLocalEmbedder) {
      const embedder = this.embedder as LocalEmbedder;
      const result = await embedder.embedWithDimension(content);
      embedding = result.embedding;
      dimension = result.dimension;
    } else {
      const embedder = this.embedder as OpenAIEmbeddingAdapter;
      embedding = await embedder.embed(content);
      dimension = embedding.length;
    }

    // 2. 存储到向量数据库
    const id = `store_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.db.add(id, embedding);

    // 3. 存储 temporal triple (用于时间查询)
    await this.temporalKG.addTriple(
      wing,
      'has_memory',
      id,
      new Date().toISOString()
    );

    // 4. 存储 metadata
    // (实际应用中会存储到文件或数据库)
  }

  /**
   * 搜索记忆
   */
  async search(
    query: string,
    options: SearchOptions = {}
  ): Promise<SearchResult[]> {
    const {
      topK = 5,
      minScore = 0.7,
      includeTemporal = true
    } = options;

    // 1. 嵌入查询
    const queryEmbedding = await this.embedder.embed(query);

    // 2. 向量搜索
    const vectorResults = this.db.search(queryEmbedding, topK * 2);

    // 3. 时间感知过滤
    const results: SearchResult[] = [];

    for (const result of vectorResults) {
      if (result.score < minScore) continue;

      // 获取 temporal 信息
      const matchedTriples = includeTemporal 
        ? await this.temporalKG.queryEntity('has_memory', result.id) 
        : [];

      // 提取 wing/room 信息
      const wing = 'wing_general'; // TODO: 从 triple 提取
      const room = 'general_chat'; // TODO: 从 triple 提取

      results.push({
        id: result.id,
        content: this.getContent(result.id),
        score: result.score,
        wing,
        room,
        timestamp: new Date().toISOString()
      });
    }

    // 按分数排序
    return results.sort((a, b) => b.score - a.score);
  }

  /**
   * 获取内容（模拟）
   */
  private getContent(id: string): string {
    // TODO: 实现从文件/数据库获取实际内容
    return `Content for ${id}`;
  }

  /**
   * 层级导航搜索
   */
  async navigateSearch(
    query: string,
    wing: string,
    room: string
  ): Promise<SearchResult[]> {
    // 相当于缩小搜索范围
    const results = await this.search(query, {
      topK: 10,
      minScore: 0.6
    });

    // 可以进一步过滤 wing/room
    return results.filter(r => r.wing === wing && r.room === room);
  }

  /**
   * 时间感知搜索
   */
  async temporalSearch(
    query: string,
    as_of: string
  ): Promise<SearchResult[]> {
    const results = await this.search(query, {
      topK: 10,
      minScore: 0.6,
      includeTemporal: true
    });

    // 过滤时间点
    return results;
  }

  /**
   * 获取统计
   */
  async stats(): Promise<{
    totalMemories: number;
    wings: number;
    rooms: number;
    tempFacts: number;
  }> {
    const tempStats = await this.temporalKG.stats();
    const all = await this.temporalKG.dump();

    return {
      totalMemories: this.db.size(),
      wings: tempStats.subjects,
      rooms: 0, // TODO: 计算 rooms
      tempFacts: all.length
    };
  }

  /**
   * 计算向量相似度
   */
  cosineSimilarity(a: number[], b: number[]): number {
    let dot = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  /**
   * 关闭资源
   */
  async close(): Promise<void> {
    await this.temporalKG.cleanup();
    await this.结构.close();
  }
}

// 扩展 SimpleVectorDB 以添加 size 方法
declare module './local_embedder' {
  interface SimpleVectorDB {
    size(): number;
  }
}

SimpleVectorDB.prototype.size = function(this: SimpleVectorDB): number {
  return this.store.size;
};

// ============================================================================
// 使用示例
// ============================================================================

/**
 * // 初始化检索器
 * const retriever = new HierarchicalMemoryRetriever();
 * await retriever.initialize();
 * 
 * // 存储记忆
 * await retriever.store(
 *   '用户决定使用 PostgreSQL 而不是 SQLite',
 *   'wing_postgres_project',
 *   'hall_facts',
 *   { type: 'decision', priority: 'high' }
 * );
 * 
 * // 搜索
 * const results = await retriever.search('database decision', {
 *   topK: 5,
 *   minScore: 0.7
 * });
 * 
 * // 层级导航搜索
 * const wingResults = await retriever.navigateSearch(
 *   'database decision',
 *   'wing_postgres_project',
 *   'hall_facts'
 * );
 * 
 * // 时间感知搜索
 * const historyResults = await retriever.temporalSearch(
 *   'database decision',
 *   '2026-04-09T12:00:00Z'
 * );
 * 
 * // 获取统计
 * const stats = await retriever.stats();
 * 
 * // 清理
 * await retriever.close();
 */

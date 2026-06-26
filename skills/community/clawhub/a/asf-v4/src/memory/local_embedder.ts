/**
 * ANFSF V1.5.0 - 本地零 API 向量嵌入器
 * 使用 Sentence Transformers 替代 OpenAI Embeddings
 */

import { pipeline, env } from '@xenova/transformers';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';

/**
 * 本地向量嵌入器
 */
export class LocalEmbedder {
  private embedder: any | null = null;
  private textSplitter: RecursiveCharacterTextSplitter;

  constructor(modelName: string = 'Xenova/all-MiniLM-L6-v2') {
    // 设置本地模型路径
    env.allowLocalModels = true;
    env.useBrowserCache = false;

    this.textSplitter = new RecursiveCharacterTextSplitter({
      chunkSize: 1000,
      chunkOverlap: 200
    });
  }

  /**
   * 初始化嵌入器（懒加载）
   */
  async initialize(): Promise<void> {
    if (!this.embedder) {
      const extractor = await pipeline('feature-extraction', this.getModelName());
      this.embedder = extractor;
    }
  }

  /**
   * 获取模型名称
   */
  private getModelName(): string {
    // 可配置的模型列表
    const models: Record<string, string> = {
      'mini': 'Xenova/all-MiniLM-L6-v2',      // 384维，快速
      'base': 'Xenova/all-mpnet-base-v2',     // 768维，准确
      'large': 'Xenova/gtr-t5-large'          // 1024维，最准确
    };

    return models[process.env.EMBEDDER_MODEL || 'mini'];
  }

  /**
   * 嵌入单个文本
   */
  async embed(text: string): Promise<number[]> {
    await this.initialize();

    // 分割长文本
    const chunks = await this.textSplitter.createDocuments([text]);
    
    // 对每个块进行嵌入
    const embeddings = [];
    for (const chunk of chunks) {
      const output = await this.embedder(chunk.pageContent, {
        pooling: 'mean',
        normalize: true
      });
      embeddings.push(output.dataset.output);
    }

    // 简单平均（也可以使用加权平均）
    const avgEmbedding = this.averageEmbeddings(embeddings);
    
    return avgEmbedding;
  }

  /**
   * 批量嵌入
   */
  async embedBatch(texts: string[]): Promise<number[][]> {
    await this.initialize();

    const allEmbeddings = [];
    
    for (const text of texts) {
      const chunks = await this.textSplitter.createDocuments([text]);
      const embeddings = [];

      for (const chunk of chunks) {
        const output = await this.embedder(chunk.pageContent, {
          pooling: 'mean',
          normalize: true
        });
        embeddings.push(output.dataset.output);
      }

      const avgEmbedding = this.averageEmbeddings(embeddings);
      allEmbeddings.push(avgEmbedding);
    }

    return allEmbeddings;
  }

  /**
   * 平均嵌入向量
   */
  private averageEmbeddings(embeddings: number[][]): number[] {
    if (embeddings.length === 0) {
      return [];
    }

    const dims = embeddings[0].length;
    const avg = new Array(dims).fill(0);

    for (const emb of embeddings) {
      for (let i = 0; i < dims; i++) {
        avg[i] += emb[i];
      }
    }

    // 取平均
    for (let i = 0; i < dims; i++) {
      avg[i] /= embeddings.length;
    }

    return avg;
  }

  /**
   * 嵌入并获取维度
   */
  async embedWithDimension(text: string): Promise<{ embedding: number[], dimension: number }> {
    const embedding = await this.embed(text);
    return {
      embedding,
      dimension: embedding.length
    };
  }
}

/**
 * 简单向量数据库 (用于测试)
 */
export class SimpleVectorDB {
  private store: Map<string, number[]> = new Map();

  /**
   * 添加向量
   */
  add(id: string, embedding: number[]): void {
    this.store.set(id, embedding);
  }

  /**
   * 获取向量
   */
  get(id: string): number[] | undefined {
    return this.store.get(id);
  }

  /**
   * 批量添加
   */
  addBatch(entries: { id: string; embedding: number[] }[]): void {
    for (const entry of entries) {
      this.store.set(entry.id, entry.embedding);
    }
  }

  /**
   * 计算余弦相似度
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
   * 搜索相似向量
   */
  search(query: number[], topK: number = 5): { id: string; score: number }[] {
    const scores: { id: string; score: number }[] = [];

    for (const [id, embedding] of this.store.entries()) {
      const score = this.cosineSimilarity(query, embedding);
      scores.push({ id, score });
    }

    // 排序并返回 topK
    return scores
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  /**
   * 清空存储
   */
  clear(): void {
    this.store.clear();
  }

  /**
   * 获取大小
   */
  size(): number {
    return this.store.size;
  }
}

/**
 * 使用示例:
 * 
 * // 初始化嵌入器
 * const embedder = new LocalEmbedder();
 * 
 * // 嵌入文本
 * const embedding = await embedder.embed('这是测试文本');
 * console.log('Dimension:', embedding.length);
 * 
 * // 批量嵌入
 * const embeddings = await embedder.embedBatch(['文本1', '文本2', '文本3']);
 * 
 * // 使用向量数据库
 * const db = new SimpleVectorDB();
 * db.add('doc1', embedding);
 * 
 * // 搜索
 * const queryEmbedding = await embedder.embed('查询文本');
 * const results = db.search(queryEmbedding, 5);
 * 
 * console.log('Search results:', results);
 */

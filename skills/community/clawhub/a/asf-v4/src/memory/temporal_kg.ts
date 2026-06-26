/**
 * ANFSF V1.5.0 - 时间感知知识图谱
 * 实现 Temporal Triples，支持历史查询和时间线生成
 */

export interface TemporalTriple {
  id?: number;
  subject: string;
  predicate: string;
  object: string;
  valid_from: string;  // ISO 8601
  valid_to?: string;    // ISO 8601
  created_at: string;
}

export interface TemporalQuery {
  subject?: string;
  predicate?: string;
  object?: string;
  as_of?: string;  // 查询指定时间点
}

/**
 * 时间感知知识图谱
 */
export class TemporalKnowledgeGraph {
  private triples: Map<string, TemporalTriple[]> = new Map();

  /**
   * 添加三元组
   */
  async addTriple(
    subject: string,
    predicate: string,
    object: string,
    valid_from: string,
    valid_to?: string
  ): Promise<void> {
    const key = this.generateKey(subject, predicate, object);
    
    const triple: TemporalTriple = {
      subject,
      predicate,
      object,
      valid_from,
      valid_to,
      created_at: new Date().toISOString()
    };

    const existing = this.triples.get(key) || [];
    existing.push(triple);
    this.triples.set(key, existing);
  }

  /**
   * 生成键
   */
  private generateKey(subject: string, predicate: string, object: string): string {
    return `${subject}:${predicate}:${object}`;
  }

  /**
   * 查询实体（时间感知）
   */
  async queryEntity(entity: string, as_of?: string): Promise<TemporalTriple[]> {
    const allTriples: TemporalTriple[] = [];

    for (const triples of this.triples.values()) {
      for (const triple of triples) {
        if (triple.subject === entity) {
          // 时间验证
          const isActive = this.isActive(triple, as_of);
          if (isActive) {
            allTriples.push(triple);
          }
        }
      }
    }

    // 按时间排序
    return allTriples.sort((a, b) => 
      b.valid_from.localeCompare(a.valid_from)
    );
  }

  /**
   * 检查三元组在指定时间点是否有效
   */
  private isActive(triple: TemporalTriple, as_of?: string): boolean {
    const targetDate = as_of ? new Date(as_of) : new Date();
    const validFrom = new Date(triple.valid_from);
    const validTo = triple.valid_to ? new Date(triple.valid_to) : null;

    return targetDate >= validFrom && (!validTo || targetDate <= validTo);
  }

  /**
   * 查询关系
   */
  async queryRelation(
    subject: string,
    predicate: string,
    as_of?: string
  ): Promise<string[]> {
    const triples = await this.queryEntity(subject, as_of);
    return triples
      .filter(t => t.predicate === predicate)
      .map(t => t.object);
  }

  /**
   * 查询所有谓词
   */
  async queryPredicates(subject: string, as_of?: string): Promise<string[]> {
    const triples = await this.queryEntity(subject, as_of);
    return [...new Set(triples.map(t => t.predicate))];
  }

  /**
   * 生成时间线
   */
  async timeline(entity: string): Promise<TemporalTriple[]> {
    const triples = await this.queryEntity(entity);
    return triples.sort((a, b) => 
      a.valid_from.localeCompare(b.valid_from)
    );
  }

  /**
   * 废弃三元组
   */
  async invalidateTriple(
    subject: string,
    predicate: string,
    object: string,
    ended: string
  ): Promise<void> {
    const key = this.generateKey(subject, predicate, object);
    const triples = this.triples.get(key);

    if (triples) {
      // 更新 valid_to
      triples.forEach(t => {
        if (!t.valid_to) {
          t.valid_to = ended;
        }
      });
      this.triples.set(key, triples);
    }
  }

  /**
   * 查询当前有效事实
   */
  async getFacts(subject: string): Promise<TemporalTriple[]> {
    return this.queryEntity(subject, new Date().toISOString());
  }

  /**
   * 清理过期三元组
   */
  async cleanup(): Promise<void> {
    const now = new Date().toISOString();
    const toRemove: string[] = [];

    for (const [key, triples] of this.triples.entries()) {
      const activeTriples = triples.filter(t => this.isActive(t, now));
      if (activeTriples.length === 0) {
        toRemove.push(key);
      } else {
        this.triples.set(key, activeTriples);
      }
    }

    for (const key of toRemove) {
      this.triples.delete(key);
    }
  }

  /**
   * 获取统计信息
   */
  async stats(): Promise<{
    totalTriples: number;
    activeTriples: number;
    subjects: number;
    predicates: number;
  }> {
    let total = 0;
    let active = 0;
    const subjects = new Set<string>();
    const predicates = new Set<string>();

    for (const triples of this.triples.values()) {
      total += triples.length;
      for (const triple of triples) {
        subjects.add(triple.subject);
        predicates.add(triple.predicate);
        
        if (this.isActive(triple)) {
          active++;
        }
      }
    }

    return {
      totalTriples: total,
      activeTriples: active,
      subjects: subjects.size,
      predicates: predicates.size
    };
  }

  /**
   * 转储为 JSON
   */
  async dump(): Promise<TemporalTriple[]> {
    const all: TemporalTriple[] = [];
    for (const triples of this.triples.values()) {
      all.push(...triples);
    }
    return all;
  }
}

/**
 * 使用示例:
 * 
 * // 初始化
 * const kg = new TemporalKnowledgeGraph();
 * 
 * // 添加事实
 * await kg.addTriple(
 *   '用户', 
 *   '选择', 
 *   'PostgreSQL', 
 *   '2026-04-09T10:00:00Z'
 * );
 * 
 * // 添加过期事实
 * await kg.addTriple(
 *   '用户', 
 *   '居住', 
 *   '北京', 
 *   '2025-01-01T00:00:00Z',
 *   '2026-03-31T23:59:59Z'
 * );
 * 
 * // 查询当前事实
 * const facts = await kg.getFacts('用户');
 * 
 * // 查询历史事实
 * const factsInJan = await kg.queryEntity('用户', '2026-01-15T12:00:00Z');
 * 
 * // 查询关系
 * const cities = await kg.queryRelation('用户', '居住', '2026-01-15');
 * 
 * // 废弃事实
 * await kg.invalidateTriple('用户', '居住', '北京', '2026-04-01T00:00:00Z');
 * 
 * // 生成时间线
 * const timeline = await kg.timeline('用户');
 * 
 * // 获取统计
 * const stats = await kg.stats();
 * 
 * console.log(stats);
 */

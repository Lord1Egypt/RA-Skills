/**
 * ANFSF V1.5.0 - 层级记忆结构 (Wings + Rooms + Halls + Tunnels)
 * 借鉴 MemPalace 架构，实现本地知识图谱导航
 */

// ============================================================================
// 类型定义
// ============================================================================

export interface WingConfig {
  type: 'project' | 'person' | 'topic';
  keywords: string[];
  rooms: string[];
}

export interface Wings {
  [key: string]: WingConfig;
}

export interface Halls {
  hall_facts: string[];        // 决策
  hall_events: string[];       // 会话/调试
  hall_discoveries: string[];  // 突破/新见解
  hall_preferences: string[];  // 偏好/习惯
  hall_advice: string[];       // 建议/解决方案
}

export interface TunnelConfig {
  from_wing: string;
  to_wing: string;
  room: string;
}

export interface Tunnels {
  [key: string]: TunnelConfig;
}

export interface MemoryStructure {
  wings: Wings;
  halls: Halls;
  tunnels: Tunnels;
  default_wing: string;
}

// ============================================================================
// 结构配置 (初始化)
// ============================================================================

export const INITIAL_STRUCTURE: MemoryStructure = {
  default_wing: 'wing_general',
  wings: {
    wing_general: {
      type: 'topic',
      keywords: ['general', 'default', 'misc'],
      rooms: ['general_chat', 'meta']
    }
  },
  halls: {
    hall_facts: [],
    hall_events: [],
    hall_discoveries: [],
    hall_preferences: [],
    hall_advice: []
  },
  tunnels: {}
};

// ============================================================================
// 知识图谱数据库 (SQLite)
// ============================================================================

import { Database } from 'sqlite3';

export class KnowledgeGraph {
  private db: Database;

  constructor(dbPath: string = './memory/kg.db') {
    this.db = new Database(dbPath);
    this.init();
  }

  /**
   * 初始化数据库表
   */
  private init() {
    this.db.run(`
      CREATE TABLE IF NOT EXISTS temporal_triples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        predicate TEXT NOT NULL,
        object TEXT NOT NULL,
        valid_from TEXT NOT NULL,
        valid_to TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
      )
    `);

    this.db.run(`
      CREATE INDEX IF NOT EXISTS idx_triple_subject 
      ON temporal_triples(subject, predicate)
    `);
  }

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
    return new Promise((resolve, reject) => {
      this.db.run(
        `INSERT INTO temporal_triples 
         (subject, predicate, object, valid_from, valid_to) 
         VALUES (?, ?, ?, ?, ?)`,
        [subject, predicate, object, valid_from, valid_to],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }

  /**
   * 查询实体（时间感知）
   */
  async queryEntity(entity: string, as_of?: string): Promise<any[]> {
    const query = `
      SELECT subject, predicate, object, valid_from, valid_to
      FROM temporal_triples
      WHERE subject = ?
      AND (valid_to IS NULL OR valid_to > ?)
      ORDER BY valid_from DESC
    `;

    return new Promise((resolve, reject) => {
      this.db.all(query, [entity, as_of || new Date().toISOString()], (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
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
   * 生成时间线
   */
  async timeline(entity: string): Promise<any[]> {
    const triples = await this.queryEntity(entity);
    return triples.sort((a, b) => a.valid_from.localeCompare(b.valid_from));
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
    return new Promise((resolve, reject) => {
      this.db.run(
        `UPDATE temporal_triples 
         SET valid_to = ? 
         WHERE subject = ? AND predicate = ? AND object = ?`,
        [ended, subject, predicate, object],
        (err) => {
          if (err) reject(err);
          else resolve();
        }
      );
    });
  }

  /**
   * 关闭数据库连接
   */
  async close(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.db.close(err => {
        if (err) reject(err);
        else resolve();
      });
    });
  }
}

// ============================================================================
// 记忆结构管理器
// ============================================================================

export class MemoryStructureManager {
  private structure: MemoryStructure;
  private kg: KnowledgeGraph;

  constructor(structurePath: string = './memory/structure.json') {
    this.structure = INITIAL_STRUCTURE;
    this.kg = new KnowledgeGraph();
  }

  /**
   * 添加 wing
   */
  async addWing(
    wingId: string,
    type: 'project' | 'person' | 'topic',
    keywords: string[],
    rooms: string[]
  ): Promise<void> {
    this.structure.wings[wingId] = {
      type,
      keywords,
      rooms
    };
  }

  /**
   * 添加 tunnel
   */
  async addTunnel(
    tunnelId: string,
    from_wing: string,
    to_wing: string,
    room: string
  ): Promise<void> {
    this.structure.tunnels[tunnelId] = {
      from_wing,
      to_wing,
      room
    };
  }

  /**
   * 添加 temporal triple
   */
  async addFact(
    subject: string,
    predicate: string,
    object: string,
    valid_from: string
  ): Promise<void> {
    await this.kg.addTriple(subject, predicate, object, valid_from);
  }

  /**
   * 查询当前facts
   */
  async getCurrentFacts(entity: string): Promise<any[]> {
    return this.kg.queryEntity(entity);
  }

  /**
   * 废弃fact
   */
  async retireFact(
    subject: string,
    predicate: string,
    object: string,
    ended: string
  ): Promise<void> {
    await this.kg.invalidateTriple(subject, predicate, object, ended);
  }

  /**
   * 获取结构快照
   */
  getSnapshot(): MemoryStructure {
    return this.structure;
  }

  /**
   * 保存结构
   */
  async save(): Promise<void> {
    // TODO: 实现 JSON 序列化保存
  }

  /**
   * 加载结构
   */
  async load(): Promise<void> {
    // TODO: 实现 JSON 反序列化加载
  }

  /**
   * 关闭所有资源
   */
  async close(): Promise<void> {
    await this.kg.close();
  }
}

// ============================================================================
// 导航器 (Navigation)
// ============================================================================

export class MemoryNavigator {
  private structure: MemoryStructure;

  constructor(structure: MemoryStructure) {
    this.structure = structure;
  }

  /**
   * 通过关键词找到相关 wings
   */
  async findRelevantWings(query: string): Promise<string[]> {
    const queryLower = query.toLowerCase();
    const relevantWings = [];

    for (const [wingId, wing] of Object.entries(this.structure.wings)) {
      const kwMatch = wing.keywords.some(kw => 
        queryLower.includes(kw.toLowerCase())
      );
      const typeMatch = queryLower.includes(wing.type);
      
      if (kwMatch || typeMatch) {
        relevantWings.push(wingId);
      }
    }

    // 如果没有匹配，返回默认 wing
    if (relevantWings.length === 0) {
      relevantWings.push(this.structure.default_wing);
    }

    return relevantWings;
  }

  /**
   * 在 wing 中查找相关 rooms
   */
  async findRelevantRooms(
    wingId: string,
    query: string
  ): Promise<string[]> {
    const wing = this.structure.wings[wingId];
    if (!wing) {
      return [];
    }

    const queryLower = query.toLowerCase();
    const relevantRooms = [];

    for (const room of wing.rooms) {
      if (queryLower.includes(room.toLowerCase())) {
        relevantRooms.push(room);
      }
    }

    return relevantRooms;
  }

  /**
   * 查找跨 wing 的 tunnels
   */
  async findTunnels(room: string, fromWing: string): Promise<any[]> {
    const tunnels = [];

    for (const [tunnelId, tunnel] of Object.entries(this.structure.tunnels)) {
      if (tunnel.room === room && tunnel.from_wing === fromWing) {
        tunnels.push({
          tunnelId,
          ...tunnel
        });
      }
    }

    return tunnels;
  }

  /**
   * 全路径导航
   */
  async navigate(query: string): Promise<any[]> {
    const wings = await this.findRelevantWings(query);
    const results = [];

    for (const wing of wings) {
      const rooms = await this.findRelevantRooms(wing, query);
      
      for (const room of rooms) {
        const tunnels = await this.findTunnels(room, wing);
        
        results.push({
          wing,
          room,
          tunnels
        });
      }
    }

    return results;
  }
}

// ============================================================================
// 架构示例
// ============================================================================

/**
 * 使用示例:
 * 
 * // 初始化
 * const manager = new MemoryStructureManager();
 * 
 * // 添加项目 wing
 * await manager.addWing('wing_jieyue', 'project', 
 *   ['jieyue', 'securities', ' financial'], 
 *   ['auth', ' billing', '部署', ' optimization']);
 * 
 * // 添加 temporal fact
 * await manager.addFact(
 *   '用户', 
 *   '选择', 
 *   'PostgreSQL', 
 *   '2026-04-09'
 * );
 * 
 * // 导航
 * const navigator = new MemoryNavigator(manager.getSnapshot());
 * const results = await navigator.navigate('PostgreSQL decision');
 * 
 * // 清理
 * await manager.close();
 */

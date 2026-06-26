#!/usr/bin/env node
// const { createLogger } = require('../../src/utils/logger.cjs');
const { resolveModule } = require('../module_resolver.cjs'); // 未使用
/**
 * Cognitive Brain - 联想网络模块
 * 管理概念间的联想关系
 */

const logger = createLogger('associate');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

// 联想配置
const DEFAULT_CONFIG = {
  activationThreshold: 0.3,
  decayFactor: 0.9,
  maxDepth: 3,
  maxActiveNodes: 20
};

// 常量定义（避免魔法数字）
const CONSTANTS = {
  MAX_RESULTS: 10,           // 结果列表最大长度
  MAX_PATH_LENGTH: 10,       // 路径查找最大深度
  MAX_CONCEPT_LENGTH: 100,   // 概念名称最大长度
  DEFAULT_WEIGHT: 0.5,       // 默认联想权重
  ACTIVATION_DECAY: 0.9      // 激活衰减因子
};

/**
 * 联想网络类
 */
class AssociationNetwork {
  constructor() {
    this.nodes = new Map();     // 概念节点
    this.edges = new Map();     // 联想边
    this.config = DEFAULT_CONFIG;
  }

  /**
   * 添加概念节点
   */
  addNode(concept, metadata = {}) {
    const existing = this.nodes.get(concept);
    if (existing) {
      existing.accessCount++;
      existing.lastAccessed = Date.now();
      return existing;
    }

    const node = {
      concept,
      activation: 0,
      accessCount: 1,
      createdAt: Date.now(),
      lastAccessed: Date.now(),
      metadata
    };

    this.nodes.set(concept, node);
    return node;
  }

  /**
   * 添加联想边
   */
  // P8: 添加错误边界
  addEdge(from, to, type = 'related', weight = 0.5, bidirectional = true) {
    try {
      // 参数验证
      if (!from || !to || typeof from !== 'string' || typeof to !== 'string') {
        console.warn('[AssociationNetwork] 无效的边参数:', { from, to });
        return null;
      }

      // 确保节点存在
      if (!this.nodes.has(from)) this.addNode(from);
      if (!this.nodes.has(to)) this.addNode(to);

      const edgeKey = `${from}->${to}`;
      const edge = {
        from,
        to,
        type,           // related, similar, is_a, part_of, causes, enables, co_occurs
        weight: Math.max(0, Math.min(1, weight)), // 确保权重在有效范围
        createdAt: Date.now(),
        lastActivated: null,
        activationCount: 0,
        evidenceCount: 1
      };

      this.edges.set(edgeKey, edge);

      // 双向边
      if (bidirectional && type !== 'is_a' && type !== 'part_of') {
        const reverseKey = `${to}->${from}`;
        this.edges.set(reverseKey, { ...edge, from: to, to: from });
      }

      return edge;
    } catch (e) { console.error("[associate] 错误:", e.message);
      console.error('[AssociationNetwork] addEdge 失败:', e.message);
      return null;
    }
  }

  /**
   * 获取节点的所有关联 (P8: 添加错误边界)
   */
  getAssociations(concept) {
    try {
      if (!concept || typeof concept !== 'string') {
        return [];
      }

      const associations = [];

      for (const [key, edge] of this.edges) {
        if (edge.from === concept || edge.to === concept) {
          associations.push({
            concept: edge.from === concept ? edge.to : edge.from,
            type: edge.type,
            weight: edge.weight,
            direction: edge.from === concept ? 'outgoing' : 'incoming'
          });
        }
      }

      return associations.sort((a, b) => b.weight - a.weight);
    } catch (e) { console.error("[associate] 错误:", e.message);
      console.error('[AssociationNetwork] getAssociations 失败:', e.message);
      return [];
    }
  }

  /**
   * 激活扩散
   */
  spreadActivation(seedConcepts, initialActivation = 1.0) {
    // 重置所有激活值
    for (const node of this.nodes.values()) {
      node.activation = 0;
    }

    // 设置初始激活
    for (const concept of seedConcepts) {
      const node = this.nodes.get(concept);
      if (node) {
        node.activation = initialActivation;
      }
    }

    // 迭代传播
    const maxIterations = this.config.maxDepth;
    const activeNodes = new Set(seedConcepts);

    for (let i = 0; i < maxIterations; i++) {
      const newActive = new Set();

      for (const concept of activeNodes) {
        const node = this.nodes.get(concept);
        if (!node) continue;

        const associations = this.getAssociations(concept);

        for (const assoc of associations) {
          const targetNode = this.nodes.get(assoc.concept);
          if (!targetNode) continue;

          // 计算传播激活
          const spreadActivation = node.activation * assoc.weight * this.config.decayFactor;

          // 只传播高于阈值的部分
          if (spreadActivation > this.config.activationThreshold * 0.1) {
            targetNode.activation = Math.max(targetNode.activation, spreadActivation);
            newActive.add(assoc.concept);

            // 更新边的激活计数
            const edgeKey = `${concept}->${assoc.concept}`;
            const edge = this.edges.get(edgeKey);
            if (edge) {
              edge.lastActivated = Date.now();
              edge.activationCount++;
            }
          }
        }
      }

      // 合并新激活的节点
      for (const concept of newActive) {
        activeNodes.add(concept);
      }
    }

    // 返回激活结果
    const results = [];
    for (const node of this.nodes.values()) {
      if (node.activation > this.config.activationThreshold) {
        results.push({
          concept: node.concept,
          activation: node.activation,
          associations: this.getAssociations(node.concept).slice(0, CONSTANTS.MAX_RESULTS)
        });
      }
    }

    return results.sort((a, b) => b.activation - a.activation);
  }

  /**
   * 加强联想
   */
  strengthenAssociation(from, to, delta = 0.1) {
    const edgeKey = `${from}->${to}`;
    const edge = this.edges.get(edgeKey);

    if (edge) {
      edge.weight = Math.min(1, edge.weight + delta);
      edge.evidenceCount++;
    } else {
      this.addEdge(from, to, 'related', 0.3);
    }
  }

  /**
   * 减弱联想
   */
  weakenAssociation(from, to, delta = 0.05) {
    const edgeKey = `${from}->${to}`;
    const edge = this.edges.get(edgeKey);

    if (edge) {
      edge.weight = Math.max(0, edge.weight - delta);
      if (edge.weight < 0.1) {
        this.edges.delete(edgeKey);
      }
    }
  }

  /**
   * 查找路径
   */
  findPath(from, to, maxDepth = 4) {
    if (from === to) return [from];

    const visited = new Set([from]);
    const queue = [[from]];

    while (queue.length > 0) {
      const path = queue.shift();
      const current = path[path.length - 1];

      if (path.length > maxDepth) continue;

      const associations = this.getAssociations(current);

      for (const assoc of associations) {
        if (assoc.concept === to) {
          return [...path, to];
        }

        if (!visited.has(assoc.concept)) {
          visited.add(assoc.concept);
          queue.push([...path, assoc.concept]);
        }
      }
    }

    return null;  // 没找到路径
  }

  /**
   * 获取网络统计
   */
  getStats() {
    let totalWeight = 0;
    let maxWeight = 0;

    for (const edge of this.edges.values()) {
      totalWeight += edge.weight;
      maxWeight = Math.max(maxWeight, edge.weight);
    }

    return {
      nodes: this.nodes.size,
      edges: this.edges.size,
      avgWeight: this.edges.size > 0 ? totalWeight / this.edges.size : 0,
      maxWeight,
      topNodes: this.getTopNodes(5)
    };
  }

  /**
   * 获取最重要的节点
   */
  getTopNodes(limit = 10) {
    const nodes = Array.from(this.nodes.values());
    return nodes
      .sort((a, b) => b.accessCount - a.accessCount)
      .slice(0, limit)
      .map(n => ({ concept: n.concept, accessCount: n.accessCount }));
  }

  /**
   * 导出网络
   */
  export() {
    return {
      nodes: Array.from(this.nodes.entries()),
      edges: Array.from(this.edges.entries()),
      config: this.config
    };
  }

  /**
   * 导入网络
   */
  import(data) {
    this.nodes = new Map(data.nodes || []);
    this.edges = new Map(data.edges || []);
    if (data.config) {
      this.config = { ...this.config, ...data.config };
    }
  }
}

// 全局网络实例
let network = null;

/**
 * 获取网络实例
 */
function getNetwork() {
  if (!network) {
    network = new AssociationNetwork();
  }
  return network;
}

/**
 * 从数据库加载
 */
async function loadFromDB() {
  const net = getNetwork();
  const { createTempPool } = require('./db.cjs');
  
  let pool;
  try {
    pool = createTempPool();
    if (!pool) {
      console.error('[associate] 无法创建数据库连接');
      return;
    }

    // 加载概念
    const concepts = await pool.query('SELECT * FROM concepts');
    for (const row of concepts.rows) {
      net.addNode(row.name, { id: row.id, vector: row.vector });
    }

    // 加载联想
    const associations = await pool.query('SELECT * FROM associations');
    for (const row of associations.rows) {
      const fromConcept = concepts.rows.find(c => c.id === row.from_id);
      const toConcept = concepts.rows.find(c => c.id === row.to_id);
      if (fromConcept && toConcept) {
        net.addEdge(fromConcept.name, toConcept.name, row.type, row.weight, false);
      }
    }

    console.log(`[associate] 从数据库加载 ${net.nodes.size} 个节点，${net.edges.size} 条边`);
  } catch (e) {
    console.error("[associate] 错误:", e.message);
    console.log('[associate] 数据库不可用，使用空网络');
  } finally {
    if (pool) await pool.end().catch(() => {});
  }

  return net;
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  const net = getNetwork();
  
  // 从数据库加载网络
  await loadFromDB();

  switch (action) {
    case 'spread':
      if (args[0]) {
        const seeds = args[0].split(',');
        const results = net.spreadActivation(seeds);
        console.log('🔥 激活传播结果:');
        results.slice(0, CONSTANTS.MAX_RESULTS).forEach((r, i) => {
          console.log(`   ${i + 1}. ${r.concept} (激活: ${r.activation.toFixed(3)})`);
        });
      }
      break;

    case 'path':
      if (args[0] && args[1]) {
        const path = net.findPath(args[0], args[1]);
        if (path) {
          console.log(`📍 路径: ${path.join(' -> ')}`);
        } else {
          console.log('❌ 未找到路径');
        }
      }
      break;

    case 'associations':
      if (args[0]) {
        const assocs = net.getAssociations(args[0]);
        console.log(`🔗 ${args[0]} 的关联:`);
        assocs.forEach(a => {
          console.log(`   ${a.concept} (${a.type}, 权重: ${a.weight.toFixed(2)})`);
        });
      }
      break;

    case 'stats':
      console.log(JSON.stringify(net.getStats(), null, 2));
      break;

    case 'export':
      console.log(JSON.stringify(net.export(), null, 2));
      break;

    default:
      console.log(`
联想网络模块 - 查询工具

用法:
  node associate.cjs spread <concept1,concept2,...>   # 激活传播
  node associate.cjs path <from> <to>                  # 查找路径
  node associate.cjs associations <concept>            # 查看关联
  node associate.cjs stats                             # 网络统计
  node associate.cjs export                            # 导出网络

说明:
  关联关系通过 encode 自动提取或 autolearn 学习生成
      `);
  }
}

main();

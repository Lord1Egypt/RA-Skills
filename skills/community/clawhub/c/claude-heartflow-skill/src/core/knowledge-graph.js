/**
 * KnowledgeGraph v2.0.0 — 三元组知识图谱
 *
 * 以 (subject, predicate, object) 三元组为基本单位的知识存储与查询系统。
 * 纯内存操作，零外部依赖，支持模糊查询、递归遍历和 JSON 持久化。
 *
 * 设计原则：
 * - 三元组不可变——添加时若 key 已存在则更新置信度和时间戳
 * - 三重索引加速查询（subject/predicate/object 各一）
 * - 模糊匹配默认启用（contains 而非 exact match）
 * - 递归遍历防环（visited Set）
 *
 * 典型用法：
 *   const kg = new KnowledgeGraph();
 *   kg.addEdge('心虫', '拥有属性', '三层记忆', 0.95);
 *   kg.query({ subject: '心虫' });
 *   kg.getRelated('心虫', 2);
 *   kg.save('/tmp/kg.json');
 *   kg.load('/tmp/kg.json');
 */

const path = require('path');
const fs = require('fs');

class KnowledgeGraph {
  /**
   * @param {string|null} dataDir - 默认数据目录（save/load 时使用）
   */
  constructor(dataDir = null) {
    this.dataDir = dataDir;

    // ─── 主存储 ─────────────────────────────────────────────────────────────
    // key = `${subject}|${predicate}|${object}`（小写标准化）
    // value = { subject, predicate, object, confidence, createdAt, updatedAt, accessedAt }
    this._triples = new Map();

    // ─── 三重索引 ───────────────────────────────────────────────────────────
    // Map<实体名, Set<tripleKey>>
    this._subjectIndex = new Map();   // subject → Set<keys>
    this._predicateIndex = new Map(); // predicate → Set<keys>
    this._objectIndex = new Map();    // object → Set<keys>

    // ─── 统计 ───────────────────────────────────────────────────────────────
    this._stats = {
      triplesAdded: 0,
      queriesExecuted: 0,
      saves: 0,
      loads: 0,
    };

    this._bornAt = Date.now();
  }

  // ═════════════════════════════════════════════════════════════════════════
  // 核心 API
  // ═════════════════════════════════════════════════════════════════════════

  /**
   * 添加一个三元组
   * @param {string} subject - 主体
   * @param {string} predicate - 谓词（关系类型）
   * @param {string} object - 客体
   * @param {number} [confidence=0.5] - 置信度 0~1
   * @returns {object} 新增或更新后的三元组记录
   * @throws 参数为空时抛出 Error
   */
  addEdge(subject, predicate, object, confidence = 0.5) {
    if (!subject || !predicate || !object) {
      throw new Error(
        `addEdge: subject/predicate/object 都不能为空 ` +
        `(received: subject=${JSON.stringify(subject)}, ` +
        `predicate=${JSON.stringify(predicate)}, ` +
        `object=${JSON.stringify(object)})`
      );
    }

    const key = this._makeKey(subject, predicate, object);
    const now = Date.now();
    const clampedConfidence = Math.max(0, Math.min(1, confidence));

    // 如果已存在，更新置信度和时间戳
    if (this._triples.has(key)) {
      const existing = this._triples.get(key);
      existing.confidence = clampedConfidence;
      existing.updatedAt = now;
      existing.accessedAt = now;
      return existing;
    }

    const triple = {
      subject,
      predicate,
      object,
      confidence: clampedConfidence,
      createdAt: now,
      updatedAt: now,
      accessedAt: now,
    };

    this._triples.set(key, triple);
    this._stats.triplesAdded++;

    // 更新三重索引
    this._addToIndex(this._subjectIndex, subject, key);
    this._addToIndex(this._predicateIndex, predicate, key);
    this._addToIndex(this._objectIndex, object, key);

    return triple;
  }

  /**
   * 查询三元组
   *
   * 筛选条件之间是 AND 关系（同时匹配）。
   * 默认启用模糊匹配（contains），设置 fuzzy=false 时启用精确匹配。
   *
   * @param {object} options - 查询条件
   * @param {string}  [options.subject]   - 按主体筛选
   * @param {string}  [options.predicate] - 按谓词筛选
   * @param {string}  [options.object]    - 按客体筛选
   * @param {boolean} [options.fuzzy=true]    - 是否启用模糊匹配
   * @param {number}  [options.limit=100]     - 返回条数上限
   * @param {boolean} [options.sortByConfidence=false] - 按置信度降序排列
   * @returns {Array<object>} 匹配的三元组数组
   */
  query(options = {}) {
    const {
      subject,
      predicate,
      object,
      fuzzy = true,
      limit = 100,
      sortByConfidence = false,
    } = options;

    this._stats.queriesExecuted++;

    // 无筛选条件时返回所有三元组
    if (!subject && !predicate && !object) {
      return this._take(
        sortByConfidence
          ? Array.from(this._triples.values()).sort((a, b) => b.confidence - a.confidence)
          : Array.from(this._triples.values()),
        limit
      );
    }

    // 精确模式：利用索引缩小候选集
    if (!fuzzy) {
      return this._exactQuery(subject, predicate, object, limit, sortByConfidence);
    }

    // 模糊模式：全量扫描 + contains 过滤
    return this._fuzzyQuery(subject, predicate, object, limit, sortByConfidence);
  }

  /**
   * 获取与某实体相关的所有三元组（支持深度递归）
   *
   * 以 entity 为起点，同时查找 entity 作为 subject 和 object 的三元组。
   * 若 depth > 1，递归遍历关联实体，visited Set 防止环。
   *
   * @param {string} entity - 实体名称
   * @param {number} [depth=1] - 递归深度（>=1）
   * @param {Set}    [visited] - 内部使用的已访问实体集合
   * @returns {Array<object>} 相关三元组数组（含递归展开的）
   */
  getRelated(entity, depth = 1, visited = new Set()) {
    if (!entity || depth < 1) return [];
    if (visited.has(entity)) return [];
    visited.add(entity);

    // 以 entity 作为 subject 或 object 精确查询
    const asSubject = this.query({ subject: entity, fuzzy: false });
    const asObject  = this.query({ object: entity, fuzzy: false });

    // 合并去重
    const seenKeys = new Set();
    const results = [];
    const pushUnique = (triple) => {
      const key = this._makeKey(triple.subject, triple.predicate, triple.object);
      if (!seenKeys.has(key)) {
        seenKeys.add(key);
        results.push(triple);
      }
    };

    for (const t of asSubject) pushUnique(t);
    for (const t of asObject) pushUnique(t);

    // 递归层级
    if (depth > 1) {
      const neighborEntities = new Set();
      for (const triple of results) {
        if (triple.subject !== entity) neighborEntities.add(triple.subject);
        if (triple.object !== entity) neighborEntities.add(triple.object);
      }
      for (const neighbor of neighborEntities) {
        if (!visited.has(neighbor)) {
          const deeper = this.getRelated(neighbor, depth - 1, visited);
          for (const t of deeper) pushUnique(t);
        }
      }
    }

    return results;
  }

  /**
   * 获取知识图谱统计信息
   * @returns {object} { triples, entities, relationTypes, totalQueries, dataDir, uptime }
   */
  getStats() {
    const allSubjects = new Set();
    const allObjects = new Set();
    for (const triple of this._triples.values()) {
      allSubjects.add(triple.subject);
      allObjects.add(triple.object);
    }
    const allEntities = new Set([...allSubjects, ...allObjects]);

    return {
      triples: this._triples.size,
      entities: allEntities.size,
      relationTypes: this._predicateIndex.size,
      totalAdded: this._stats.triplesAdded,
      totalQueries: this._stats.queriesExecuted,
      saves: this._stats.saves,
      loads: this._stats.loads,
      dataDir: this.dataDir,
      uptimeMs: Date.now() - this._bornAt,
    };
  }

  // ═════════════════════════════════════════════════════════════════════════
  // 持久化
  // ═════════════════════════════════════════════════════════════════════════

  /**
   * 持久化：保存三元组到 JSON 文件
   * @param {string} [filePath] - 保存路径，默认 dataDir/knowledge-graph.json
   * @returns {object} { success, path, count }
   */
  save(filePath) {
    const targetPath = filePath || this._defaultPath();
    if (!targetPath) {
      throw new Error('save: 请指定 filePath 或设置 dataDir');
    }

    const dir = path.dirname(targetPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const data = {
      version: '2.0.0',
      exportedAt: new Date().toISOString(),
      tripleCount: this._triples.size,
      triples: Array.from(this._triples.values()),
    };

    fs.writeFileSync(targetPath, JSON.stringify(data, null, 2), 'utf8');
    this._stats.saves++;
    return { success: true, path: targetPath, count: this._triples.size };
  }

  /**
   * 加载：从 JSON 文件恢复知识图谱
   * 恢复前清空当前所有数据。
   * @param {string} filePath - JSON 文件路径
   * @returns {object} { success, count, source }
   */
  load(filePath) {
    if (!filePath || !fs.existsSync(filePath)) {
      throw new Error(`load: 文件不存在: ${filePath}`);
    }

    const raw = fs.readFileSync(filePath, 'utf8');
    let data;
    try {
      data = JSON.parse(raw);
    } catch (e) {
      throw new Error(`load: JSON 解析失败: ${e.message}`);
    }

    if (!data.triples || !Array.isArray(data.triples)) {
      throw new Error('load: 无效的知识图谱数据格式（缺少 triples 数组）');
    }

    // 清空现有数据
    this.clear();

    // 加载三元组
    for (const triple of data.triples) {
      try {
        this.addEdge(triple.subject, triple.predicate, triple.object, triple.confidence);
      } catch (e) {
        // 跳过无效条目，不中断加载
        console.warn(`[KnowledgeGraph] 加载时跳过无效三元组: ${e.message}`);
      }
    }

    this._stats.loads++;
    return { success: true, count: this._triples.size, source: filePath };
  }

  /**
   * 清空所有三元组和索引
   */
  clear() {
    this._triples.clear();
    this._subjectIndex.clear();
    this._predicateIndex.clear();
    this._objectIndex.clear();
    this._stats.triplesAdded = 0;
  }

  // ═════════════════════════════════════════════════════════════════════════
  // 兼容方法 — 与 heartflow.js 的 addKnowledge/searchKnowledge/getKnowledgeStats 对接
  // ═════════════════════════════════════════════════════════════════════════

  /**
   * 添加知识节点（兼容 heartflow.js 的 addKnowledge 调用）
   *
   * 将节点信息存储为两个三元组：
   *   (name, "is_a", type)
   *   (name, "has_description", description)  // description 非空时
   *
   * @param {object}  partial - 节点信息
   * @param {string}  partial.name        - 节点名称
   * @param {string}  [partial.description] - 描述
   * @param {string}  [partial.type='concept'] - 类型
   * @param {number}  [partial.importance=0.5] - 重要性（映射为置信度）
   * @returns {object} 节点风格的对象（与旧版兼容）
   */
  addNode(partial) {
    const { name, description = '', type = 'concept', importance = 0.5 } = partial;

    // 写入类型三元组
    this.addEdge(name, 'is_a', type, importance);

    // description 非空时写入描述三元组
    if (description) {
      this.addEdge(name, 'has_description', description, importance);
    }

    return {
      id: `${name}|is_a|${type}`,
      name,
      description,
      type,
      importance,
      connections: [],
      reflectionCount: 0,
      createdAt: Date.now(),
      lastAccessed: Date.now(),
    };
  }

  /**
   * 按关键词搜索知识节点（兼容 heartflow.js 的 searchKnowledge 调用）
   *
   * 对 subject/object 做模糊匹配，返回节点风格的搜索结果。
   *
   * @param {string} query - 搜索关键词
   * @returns {Array<object>} 节点风格的搜索结果（按置信度降序）
   */
  search(query) {
    if (!query) return [];

    // 搜 subject 包含 query 的三元组
    const results = this.query({ subject: query, fuzzy: true });
    const seen = new Set();
    const nodes = [];

    for (const triple of results) {
      if (seen.has(triple.subject)) continue;
      seen.add(triple.subject);

      // 尝试查找描述
      const descResults = this.query({
        subject: triple.subject,
        predicate: 'has_description',
        fuzzy: false,
      });
      const description = descResults.length > 0 ? descResults[0].object : '';

      nodes.push({
        id: `${triple.subject}|is_a|${triple.predicate}`,
        name: triple.subject,
        description,
        type: triple.predicate,
        importance: triple.confidence,
      });
    }

    return nodes.sort((a, b) => b.importance - a.importance);
  }

  // ═════════════════════════════════════════════════════════════════════════
  // 内部方法
  // ═════════════════════════════════════════════════════════════════════════

  /**
   * 生成三元组 key（小写标准化确保精确匹配）
   */
  _makeKey(subject, predicate, object) {
    return `${subject}|${predicate}|${object}`;
  }

  /**
   * 添加到索引
   */
  _addToIndex(index, name, key) {
    if (!index.has(name)) {
      index.set(name, new Set());
    }
    index.get(name).add(key);
  }

  /**
   * 精确查询：利用索引缩小候选集
   */
  _exactQuery(subject, predicate, object, limit, sortByConfidence) {
    // 收集所有符合条件的索引集合，取交集
    const sets = [];
    if (subject   && this._subjectIndex.has(subject))   sets.push(this._subjectIndex.get(subject));
    if (predicate && this._predicateIndex.has(predicate)) sets.push(this._predicateIndex.get(predicate));
    if (object    && this._objectIndex.has(object))     sets.push(this._objectIndex.get(object));

    // 没有索引可用时降级为全量扫描
    if (sets.length === 0) {
      return this._filterAndSlice(null, subject, predicate, object, false, limit, sortByConfidence);
    }

    // 取交集
    const intersection = new Set(sets[0]);
    for (let i = 1; i < sets.length; i++) {
      for (const key of intersection) {
        if (!sets[i].has(key)) intersection.delete(key);
      }
    }

    const triples = [];
    for (const key of intersection) {
      const triple = this._triples.get(key);
      if (triple) triples.push(triple);
    }

    if (sortByConfidence) {
      triples.sort((a, b) => b.confidence - a.confidence);
    }

    return this._take(triples, limit);
  }

  /**
   * 模糊查询：全量扫描 + contains 过滤
   */
  _fuzzyQuery(subject, predicate, object, limit, sortByConfidence) {
    return this._filterAndSlice(
      Array.from(this._triples.values()),
      subject, predicate, object, true, limit, sortByConfidence
    );
  }

  /**
   * 通用过滤 + 截取
   */
  _filterAndSlice(candidates, subject, predicate, object, fuzzy, limit, sortByConfidence) {
    const source = candidates || Array.from(this._triples.values());

    if (!subject && !predicate && !object) {
      const sorted = sortByConfidence
        ? [...source].sort((a, b) => b.confidence - a.confidence)
        : source;
      return this._take(sorted, limit);
    }

    const matchFn = fuzzy
      ? (val, filter) => !filter || (val && val.toLowerCase().includes(filter.toLowerCase()))
      : (val, filter) => !filter || val === filter;

    const filtered = source.filter(triple => {
      return matchFn(triple.subject, subject)
          && matchFn(triple.predicate, predicate)
          && matchFn(triple.object, object);
    });

    if (sortByConfidence) {
      filtered.sort((a, b) => b.confidence - a.confidence);
    }

    return this._take(filtered, limit);
  }

  /**
   * 截取数组前 N 项
   */
  _take(arr, n) {
    return arr.slice(0, n);
  }

  /**
   * 获取默认持久化路径
   */
  _defaultPath() {
    if (!this.dataDir) return null;
    return path.join(this.dataDir, 'knowledge-graph.json');
  }
}

module.exports = { KnowledgeGraph };

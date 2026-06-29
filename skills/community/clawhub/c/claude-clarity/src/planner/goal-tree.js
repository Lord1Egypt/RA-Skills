/**
 * GoalTree v1.0.0 — 目标树引擎（持久化层级目标系统）
 *
 * 填补心虫缺失的"长期规划"能力：
 * - 多级目标分解（父/子层级，支持任意深度）
 * - 进度自动传播（子节点进度汇总到父节点）
 * - 中断恢复（reportInterruption 记录上下文快照）
 * - 阻塞检测与自适应重规划（blocked → autoReplan）
 * - 跨会话目标追踪（JSON 文件持久化）
 *
 * 存储：data/goal-tree.json
 *
 * 设计原则：
 * - 纯数据驱动：所有操作基于 JSON 树数据，无运行时状态
 * - 原子写入：使用 tmp + rename 防止写入损坏
 * - 零 npm 依赖（与心虫保持一致）
 */

const path = require('path');
const fs = require('fs');

// ═════════════════════════════════════════════════════════════════════════
// 目标节点
// ═════════════════════════════════════════════════════════════════════════

class GoalNode {
  /**
   * @param {object} data — 节点数据
   * @param {string}  [data.id]                — 自动生成
   * @param {string}  [data.parentId]          — 父节点 ID（null = 根目标）
   * @param {string}  [data.definition]        — 目标定义
   * @param {string[]}[data.acceptanceCriteria] — 验收标准
   * @param {string}  [data.status]            — pending | in_progress | completed | blocked | cancelled
   * @param {number}  [data.progress]          — 0-100
   * @param {string}  [data.blocker]           — 阻塞原因
   * @param {object}  [data.interruptionContext] — 中断快照
   * @param {number}  [data.priority]          — 1-5
   * @param {string[]}[data.tags]              — 标签
   */
  constructor(data = {}) {
    this.id = data.id || `goal-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    this.parentId = data.parentId || null;
    this.definition = data.definition || '';
    this.acceptanceCriteria = Array.isArray(data.acceptanceCriteria) ? data.acceptanceCriteria : [];
    this.status = data.status || 'pending';
    this.progress = typeof data.progress === 'number' ? data.progress : 0;
    this.blocker = data.blocker || null;
    this.createdAt = data.createdAt || Date.now();
    this.updatedAt = data.updatedAt || Date.now();
    this.interruptionContext = data.interruptionContext || null;
    this.priority = data.priority || 3;
    this.tags = Array.isArray(data.tags) ? data.tags : [];
  }
}

// ═════════════════════════════════════════════════════════════════════════
// 目标树引擎
// ═════════════════════════════════════════════════════════════════════════

class GoalTree {
  /**
   * @param {object}  options
   * @param {string}  options.rootPath — 项目根路径（用于定位 data/ 目录）
   */
  constructor(options = {}) {
    this.rootPath = options.rootPath || process.cwd();
    this.dataPath = path.join(this.rootPath, 'data', 'goal-tree.json');
    /** @type {GoalNode[]} */
    this._tree = [];
    this._loaded = false;
  }

  // ─── 持久化 ──────────────────────────────────────────────────────────

  load() {
    if (this._loaded) return;
    try {
      if (fs.existsSync(this.dataPath)) {
        const raw = JSON.parse(fs.readFileSync(this.dataPath, 'utf8'));
        this._tree = raw.map(d => new GoalNode(d));
      } else {
        this._tree = [];
      }
    } catch (e) {
      console.error(`[GoalTree] 加载失败: ${e.message}`);
      this._tree = [];
    }
    this._loaded = true;
  }

  save() {
    try {
      const dir = path.dirname(this.dataPath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      // 原子写入：先写 tmp 再 rename
      const tmp = `${this.dataPath  }.tmp`;
      fs.writeFileSync(tmp, JSON.stringify(this._tree, null, 2), 'utf8');
      fs.renameSync(tmp, this.dataPath);
    } catch (e) {
      console.error(`[GoalTree] 保存失败: ${e.message}`);
    }
  }

  // ─── CRUD ─────────────────────────────────────────────────────────────

  /**
   * 创建目标
   * @param {object} data — GoalNode 构造参数
   * @returns {GoalNode}
   */
  create(data) {
    this.load();
    const node = new GoalNode(data);
    this._tree.push(node);
    this.save();
    return node;
  }

  /**
   * 获取单个目标
   * @param {string} id
   * @returns {GoalNode|null}
   */
  get(id) {
    this.load();
    return this._tree.find(n => n.id === id) || null;
  }

  /**
   * 更新目标
   * @param {string} id
   * @param {object} updates — 要合并的字段
   * @returns {GoalNode|null}
   */
  update(id, updates) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return null;
    const oldStatus = node.status;
    Object.assign(node, updates, { updatedAt: Date.now() });
    // 如果状态变为 completed，自动取消未完成的子节点
    if (updates.status && updates.status !== oldStatus) {
      this._propagateStatus(id, updates.status);
    }
    this.save();
    return node;
  }

  /**
   * 删除目标（递归删除所有子节点）
   * @param {string} id
   * @returns {boolean}
   */
  delete(id) {
    this.load();
    const idx = this._tree.findIndex(n => n.id === id);
    if (idx === -1) return false;
    // 先删所有后代（深度优先，从高索引到低索引避免位移问题）
    const descendants = this._getDescendants(id);
    const descendantIndices = descendants
      .map(d => this._tree.findIndex(n => n.id === d.id))
      .filter(di => di !== -1)
      .sort((a, b) => b - a); // 降序排列，从后往前删除避免索引位移
    for (const di of descendantIndices) {
      this._tree.splice(di, 1);
    }
    // 重新查找父节点索引（后代删除后原索引可能已变化）
    const currentIdx = this._tree.findIndex(n => n.id === id);
    if (currentIdx !== -1) this._tree.splice(currentIdx, 1);
    this.save();
    return true;
  }

  /**
   * 列出目标（可选按父节点过滤）
   * @param {string|null} parentId — null 返回全部
   * @returns {GoalNode[]}
   */
  list(parentId = null) {
    this.load();
    if (parentId === null) return [...this._tree];
    return this._tree.filter(n => n.parentId === parentId);
  }

  // ─── 层级操作 ────────────────────────────────────────────────────────

  /**
   * 获取直接子节点
   */
  getChildren(parentId) {
    this.load();
    return this._tree.filter(n => n.parentId === parentId);
  }

  /**
   * 获取祖先链（从根到父节点）
   */
  getAncestors(id) {
    this.load();
    const ancestors = [];
    let current = this._tree.find(n => n.id === id);
    const visited = new Set();
    while (current && current.parentId && !visited.has(current.id)) {
      visited.add(current.id);
      const parent = this._tree.find(n => n.id === current.parentId);
      if (parent) {
        ancestors.unshift(parent);
        current = parent;
      } else break;
    }
    return ancestors;
  }

  /**
   * 获取所有后代（不包含自身）
   */
  _getDescendants(id) {
    const descendants = [];
    const direct = this.getChildren(id);
    for (const child of direct) {
      descendants.push(child);
      descendants.push(...this._getDescendants(child.id));
    }
    return descendants;
  }

  /**
   * 获取所有后代（公开 API）
   */
  getDescendants(id) {
    return this._getDescendants(id);
  }

  // ─── 进度计算 ────────────────────────────────────────────────────────

  /**
   * 计算节点进度
   * - 叶子节点：使用自身 progress
   * - 非叶子节点：子节点进度的加权平均值
   */
  calculateProgress(id) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return 0;
    const children = this.getChildren(id);
    if (children.length === 0) return node.progress;
    const total = children.reduce((sum, c) => sum + this.calculateProgress(c.id), 0);
    return Math.round(total / children.length);
  }

  /**
   * 状态传播：父节点完成 → 未完成子节点自动取消
   */
  _propagateStatus(id, status) {
    if (status === 'completed') {
      const children = this.getChildren(id);
      for (const child of children) {
        if (child.status !== 'completed') {
          child.status = 'cancelled';
          child.updatedAt = Date.now();
        }
      }
    }
  }

  // ─── 阻塞管理 ────────────────────────────────────────────────────────

  /**
   * 设置阻塞状态，自动传播到所有后代
   * @returns {GoalNode|null}
   */
  setBlocker(id, reason) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return null;
    node.blocker = reason;
    node.status = 'blocked';
    node.updatedAt = Date.now();
    const descendants = this._getDescendants(id);
    for (const d of descendants) {
      if (d.status !== 'completed') {
        d.blocker = `parent_blocked: ${reason}`;
        d.status = 'blocked';
        d.updatedAt = Date.now();
      }
    }
    this.save();
    return node;
  }

  /**
   * 解除阻塞
   * @returns {GoalNode|null}
   */
  resolveBlocker(id) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return null;
    node.blocker = null;
    node.status = 'pending';
    node.updatedAt = Date.now();
    // 子节点恢复 pending（已完成的保持不变）
    const descendants = this._getDescendants(id);
    for (const d of descendants) {
      if (d.blocker && d.blocker.startsWith('parent_blocked:')) {
        d.blocker = null;
        d.status = 'pending';
        d.updatedAt = Date.now();
      }
    }
    this.save();
    return node;
  }

  /**
   * 获取所有阻塞中的目标
   * @returns {GoalNode[]}
   */
  getBlockedGoals() {
    this.load();
    return this._tree.filter(n => n.status === 'blocked');
  }

  // ─── 中断恢复 ────────────────────────────────────────────────────────

  /**
   * 记录中断上下文（用于跨会话恢复）
   * @param {string} id
   * @param {object} context — 自由格式的上下文信息
   * @returns {object|null} — 恢复摘要
   */
  reportInterruption(id, context = {}) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return null;
    node.interruptionContext = {
      timestamp: Date.now(),
      progress: node.progress,
      status: node.status,
      data: context,
    };
    node.updatedAt = Date.now();
    this.save();
    return {
      goalId: id,
      definition: node.definition,
      lastProgress: node.interruptionContext.progress,
      lastStatus: node.interruptionContext.status,
      message: `上次中断时进度 ${node.interruptionContext.progress}%，状态: ${node.interruptionContext.status}`,
    };
  }

  /**
   * 获取所有中断但未完成的目标
   * @returns {GoalNode[]}
   */
  getInterruptedGoals() {
    this.load();
    return this._tree.filter(n =>
      n.interruptionContext !== null &&
      n.status !== 'completed' &&
      n.status !== 'cancelled'
    );
  }

  // ─── 自适应重规划 ────────────────────────────────────────────────────

  /**
   * 对阻塞节点执行自适应重规划
   * 将阻塞节点及其受影响路径上的节点重置为 pending
   * @returns {object} — 重规划结果
   */
  autoReplan(id) {
    this.load();
    const node = this._tree.find(n => n.id === id);
    if (!node) return { replanned: false, reason: '目标不存在' };
    if (node.status !== 'blocked') {
      return { replanned: false, reason: '未阻塞，无需重规划', node: node };
    }

    const ancestors = this.getAncestors(id);
    const descendants = this._getDescendants(id);
    const affected = [node, ...descendants, ...ancestors];
    const seen = new Set();
    const affectedPaths = [];

    for (const a of affected) {
      if (seen.has(a.id)) continue;
      seen.add(a.id);
      if (a.status !== 'completed') {
        affectedPaths.push({
          id: a.id,
          definition: a.definition,
          originalStatus: a.status,
        });
        a.status = 'pending';
        a.blocker = null;
        a.updatedAt = Date.now();
      }
    }

    this.save();
    return {
      replanned: true,
      affectedPaths,
      count: affectedPaths.length,
      message: `已重规划 ${affectedPaths.length} 个受影响节点`,
    };
  }

  // ─── 查询 ────────────────────────────────────────────────────────────

  /**
   * 关键词搜索
   */
  search(keyword) {
    this.load();
    const kw = keyword.toLowerCase();
    return this._tree.filter(n =>
      n.definition.toLowerCase().includes(kw) ||
      n.tags.some(t => t.toLowerCase().includes(kw))
    );
  }

  /**
   * 获取统计
   */
  getStats() {
    this.load();
    return {
      total: this._tree.length,
      pending: this._tree.filter(n => n.status === 'pending').length,
      inProgress: this._tree.filter(n => n.status === 'in_progress').length,
      completed: this._tree.filter(n => n.status === 'completed').length,
      blocked: this._tree.filter(n => n.status === 'blocked').length,
      cancelled: this._tree.filter(n => n.status === 'cancelled').length,
      interrupted: this.getInterruptedGoals().length,
      roots: this._tree.filter(n => n.parentId === null).length,
    };
  }

  /**
   * 获取树状结构
   * @param {string|null} rootId — 指定根节点，null 返回完整森林
   * @returns {object[]}
   */
  getTree(rootId = null) {
    this.load();
    if (rootId) {
      const built = this._buildSubTree(rootId);
      return built ? [built] : [];
    }
    return this._tree.filter(n => n.parentId === null).map(r => this._buildSubTree(r.id));
  }

  _buildSubTree(id) {
    const node = this._tree.find(n => n.id === id);
    if (!node) return null;
    const children = this.getChildren(id).map(c => this._buildSubTree(c.id)).filter(Boolean);
    return {
      id: node.id,
      definition: node.definition,
      status: node.status,
      progress: this.calculateProgress(id),
      blocker: node.blocker,
      priority: node.priority,
      tags: node.tags,
      acceptanceCriteria: node.acceptanceCriteria,
      createdAt: node.createdAt,
      updatedAt: node.updatedAt,
      interruptionContext: node.interruptionContext,
      children: children.length > 0 ? children : undefined,
    };
  }
}

module.exports = { GoalTree, GoalNode };
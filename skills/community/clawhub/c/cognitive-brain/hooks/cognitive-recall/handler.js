const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const { createLogger } = require('../../src/utils/logger.cjs');

// 创建模块级 logger
const logger = createLogger('cognitive-recall');

// 强制日志：验证 hook 是否被触发
const HOOK_TRIGGER_LOG = '/tmp/cognitive-recall-triggered.log';
const logTrigger = () => {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(HOOK_TRIGGER_LOG, `[${timestamp}] Hook triggered!\n`);
};

// Cognitive Brain config
const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
const USER_MODEL_PATH = path.join(SKILL_DIR, 'data/user_model.json');

// v5.0 新架构导入
let CognitiveBrain = null;
let brainInstance = null;

function getBrain() {
  if (!brainInstance) {
    if (!CognitiveBrain) {
      try {
        ({ CognitiveBrain } = require(path.join(SKILL_DIR, 'src/index.js')));
      } catch (e) {
        logger.error('[cognitive-recall] Failed to load v5.0 CognitiveBrain:', e.message);
        return null;
      }
    }
    try {
      brainInstance = new CognitiveBrain();
      logger.info('[cognitive-recall] v5.0 CognitiveBrain initialized');
    } catch (e) {
      logger.error('[cognitive-recall] Failed to initialize brain:', e.message);
      return null;
    }
  }
  return brainInstance;
}

// 兼容：旧版数据库连接（降级用）
let dbPool = null;
function getDbPool() {
  if (!dbPool) {
    const { getPool } = require(path.join(SKILL_DIR, 'scripts/core/db.cjs'));
    dbPool = getPool();
  }
  return dbPool;
}

// 配置缓存
let cachedConfig = null;
function getConfig() {
  if (!cachedConfig) {
    if (!fs.existsSync(CONFIG_PATH)) {
      return null;
    }
    try {
      cachedConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    } catch (e) {
      console.error('[cognitive-recall] 解析配置失败:', e.message);
      return null;
    }
  }
  return cachedConfig;
}

let sharedMemory = null;
let sharedMemoryReady = false;

async function initSharedMemory() {
  if (sharedMemoryReady) return true;
  
  try {
    const { getSharedMemory } = require(path.join(SKILL_DIR, 'scripts/core/shared_memory.cjs'));
    sharedMemory = await getSharedMemory();
    sharedMemoryReady = true;
    logger.info('[cognitive-recall] Shared memory initialized');
    return true;
  } catch (e) {
    logger.info('[cognitive-recall] Shared memory not available, using fallback');
    return false;
  }
}

async function getLessonsFromSharedMemory() {
  if (!sharedMemoryReady) {
    await initSharedMemory();
  }

  if (sharedMemory) {
    try {
    const lessons = await sharedMemory.getLessons();
      return lessons.map(l => ({
        summary: l.content.substring(0, 100),
        content: l.content,
        importance: l.importance,
        source: 'shared_memory'
      }));
    } catch (e) {
      logger.info('[cognitive-recall] Shared memory query failed, trying episodes fallback');
    }
  }

  // Fallback: 直接从 episodes 表获取最近的记忆
  try {
    const pool = getDbPool();
    const result = await pool.query('SELECT id, content, created_at FROM episodes ORDER BY created_at DESC LIMIT 10');
    logger.info('[cognitive-recall] Retrieved', result.rows.length, 'episodes from database');
    return result.rows.map(r => ({
      summary: r.content.substring(0, 100),
      content: r.content,
      importance: 0.5,
      source: 'episodes',
      created_at: r.created_at
    }));
  } catch (e) {
    logger.error('[cognitive-recall] Episodes fallback failed:', e.message);
    return [];
  }
}

// ============================================================================
// 从 MEMORY.md 读取教训（已禁用 - 数据库优先模式）
// ============================================================================

function getLessonsFromMemory() {
  // Fallback disabled - database only mode
  return [];
}

async function getUserProfileFromSharedMemory() {
  if (!sharedMemoryReady) {
    await initSharedMemory();
  }

  if (sharedMemory) {
    try {
      const profile = await sharedMemory.getUserProfile();
      if (profile && profile.length > 0) {
        return JSON.parse(profile[0].content);
      }
    } catch (e) {
      logger.info('[cognitive-recall] Shared memory profile failed, no fallback enabled');
    }
  }

  // Fallback disabled - database only mode
  return null;
}

// ============================================================================
// 从文件读取用户模型（Fallback 模式）
// ============================================================================

function getUserModelFromFile() {
  try {
    if (fs.existsSync(USER_MODEL_PATH)) {
      const data = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
      return data;
    }
  } catch (err) {
    logger.warn('[cognitive-recall] Failed to load user model:', err.message);
  }
  
  // 默认用户模型
  return {
    name: 'master',
    preferences: {},
    interactions: { count: 0, lastActive: null }
  };
}

// ============================================================================
// 1. 性能监控
// ============================================================================

const perfLog = {
  queries: [],
  maxEntries: 100,
  warnThreshold: 100, // ms

  record(operation, durationMs, success = true) {
    this.queries.push({
      operation,
      duration: durationMs,
      success,
      timestamp: Date.now()
    });

    // Keep only recent entries
    if (this.queries.length > this.maxEntries) {
      this.queries.shift();
    }

    // Warn if slow
    if (durationMs > this.warnThreshold) {
      logger.warn(`[cognitive-recall] ⚠️ Slow query: ${operation} took ${durationMs}ms`);
    }
  },

  getStats() {
    if (this.queries.length === 0) return null;
    const durations = this.queries.map(q => q.duration);
    return {
      count: this.queries.length,
      avg: Math.round(durations.reduce((a, b) => a + b, 0) / durations.length),
      max: Math.max(...durations),
      min: Math.min(...durations)
    };
  }
};

// ============================================================================
// 2. 缓存优化 - 按重要性分级
// ============================================================================

const recallCache = new Map();

const CACHE_CONFIG = {
  high: { ttl: 10 * 60 * 1000 },    // 10 minutes (importance >= 0.8)
  medium: { ttl: 3 * 60 * 1000 },   // 3 minutes (importance 0.5-0.8)
  low: { ttl: 60 * 1000 },          // 1 minute (importance < 0.5)
  default: { ttl: 60 * 1000 }       // 1 minute (unknown)
};

function getCacheTTL(importance) {
  if (importance >= 0.8) return CACHE_CONFIG.high.ttl;
  if (importance >= 0.5) return CACHE_CONFIG.medium.ttl;
  return CACHE_CONFIG.low.ttl;
}

function getCacheEntry(key) {
  const entry = recallCache.get(key);
  if (!entry) return null;

  const now = Date.now();
  const maxTTL = Math.max(...Object.values(CACHE_CONFIG).map(c => c.ttl));

  // Use the stored TTL for this entry
  if (now - entry.timestamp > entry.ttl) {
    recallCache.delete(key);
    return null;
  }

  return entry.result;
}

function setCacheEntry(key, result, importance = 0.5) {
  const ttl = getCacheTTL(importance);
  recallCache.set(key, {
    result,
    timestamp: Date.now(),
    ttl
  });
}

// ============================================================================
// 3. 健康检查 + 降级
// ============================================================================

const healthState = {
  pgHealthy: null,
  lastCheck: 0,
  checkInterval: 30 * 1000, // 30 seconds
  fallbackMode: false,

  async check(pg, dbConfig) {
    const now = Date.now();

    // Skip if recently checked
    if (this.pgHealthy !== null && now - this.lastCheck < this.checkInterval) {
      return this.pgHealthy;
    }

    this.lastCheck = now;

    // Try a simple query
    let pool = null;
    try {
      const { Pool } = pg;
      pool = new Pool({
        host: dbConfig.host,
        port: dbConfig.port,
        database: dbConfig.database,
        user: dbConfig.user,
        password: dbConfig.password,
        connectionTimeoutMillis: 2000,
        query_timeout: 3000
      });

      await pool.query('SELECT 1');
      this.pgHealthy = true;
      this.fallbackMode = false;
      logger.info('[cognitive-recall] ✅ PostgreSQL healthy');
      return true;
    } catch (err) {
      this.pgHealthy = false;
      this.fallbackMode = true;
      logger.warn('[cognitive-recall] ⚠️ PostgreSQL unavailable, no fallback enabled');
      return false;
    } finally {
      if (pool) await pool.end().catch(() => {});
    }
  },

  async fallback(keywords, limit) {
    // Fallback disabled - database only mode
    logger.info('[cognitive-recall] Fallback disabled, returning empty results');
    return [];
  }
};

// ============================================================================
// 4. 动态关键词
// ============================================================================

const keywordState = {
  keywords: ['用户', 'master', '偏好', '重要', '项目'],
  lastUpdate: 0,
  updateInterval: 60 * 60 * 1000, // 1 hour

  load() {
    try {
      if (fs.existsSync(KEYWORDS_PATH)) {
        const data = JSON.parse(fs.readFileSync(KEYWORDS_PATH, 'utf8'));
        if (data.keywords && data.keywords.length > 0) {
          this.keywords = data.keywords;
          this.lastUpdate = data.lastUpdate || 0;
        }
      }
    } catch (err) {
      logger.warn('[cognitive-recall] Failed to load keywords:', err.message);
    }
  },

  async update(pg, dbConfig) {
    const now = Date.now();
    if (now - this.lastUpdate < this.updateInterval) {
      return this.keywords;
    }

    let pool = null;
    try {
      const { Pool } = pg;
      pool = new Pool({
        host: dbConfig.host,
        port: dbConfig.port,
        database: dbConfig.database,
        user: dbConfig.user,
        password: dbConfig.password,
        connectionTimeoutMillis: 5000
      });

      // Extract high-frequency words from recent episodes
      const result = await pool.query(`
        SELECT summary, content
        FROM episodes
        WHERE timestamp > NOW() - INTERVAL '7 days'
        ORDER BY importance DESC
        LIMIT 100
      `);

      const wordFreq = new Map();

      for (const row of result.rows) {
        const text = `${row.summary} ${row.content || ''}`;
        // Extract Chinese words (2-4 chars) and English words
        const chineseWords = text.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
        const englishWords = text.match(/[a-zA-Z]{3,}/gi) || [];

        for (const word of [...chineseWords, ...englishWords]) {
          wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
        }
      }

      // Get top keywords (excluding common words)
      const stopWords = new Set(['的', '是', '在', '了', '和', '有', '不', '这', '我', '你', 'the', 'and', 'for', 'was', 'are', 'but', 'not']);

      const topKeywords = [...wordFreq.entries()]
        .filter(([word]) => !stopWords.has(word.toLowerCase()))
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([word]) => word);

      if (topKeywords.length > 0) {
        // Merge with base keywords
        const baseKeywords = ['用户', 'master', '偏好', '重要', '项目'];
        this.keywords = [...new Set([...baseKeywords, ...topKeywords])].slice(0, 15);
        this.lastUpdate = now;

        // Save to file
        fs.writeFileSync(KEYWORDS_PATH, JSON.stringify({
          keywords: this.keywords,
          lastUpdate: this.lastUpdate
        }, null, 2));

        logger.info('[cognitive-recall] 📝 Updated keywords:', this.keywords.join(', '));
      }

      return this.keywords;
    } catch (err) {
      logger.warn('[cognitive-recall] Failed to update keywords:', err.message);
      return this.keywords;
    } finally {
      if (pool) await pool.end().catch(() => {});
    }
  },

  getKeywords() {
    return this.keywords;
  }
};

// Initialize keywords on load
keywordState.load();

// ============================================================================
// 5. 错误重试机制
// ============================================================================

const retryState = {
  installAttempts: 0,
  maxAttempts: 3,
  cooldownMs: 5 * 60 * 1000, // 5 minutes
  lastAttempt: 0,

  shouldRetry() {
    const now = Date.now();

    // Reset attempts after cooldown
    if (now - this.lastAttempt > this.cooldownMs) {
      this.installAttempts = 0;
    }

    return this.installAttempts < this.maxAttempts;
  },

  recordAttempt() {
    this.installAttempts++;
    this.lastAttempt = Date.now();
  }
};

// ============================================================================
// 依赖自动安装（带重试）
// ============================================================================

let isInstalling = false;
let pgLoaded = false;
let pgModule = null;

function ensurePgDependency() {
  if (pgLoaded && pgModule) {
    return pgModule;
  }

  // Try to load pg
  try {
    pgModule = require(path.join(SKILL_DIR, 'node_modules/pg'));
    pgLoaded = true;
    return pgModule;
  } catch (e) {
    if (isInstalling) {
      logger.info('[cognitive-recall] npm install already in progress');
      return null;
    }

    // Check retry limit
    if (!retryState.shouldRetry()) {
      logger.warn('[cognitive-recall] ⚠️ Max install attempts reached, waiting for cooldown');
      return null;
    }

    logger.info('[cognitive-recall] pg not found, auto-installing...');
    isInstalling = true;
    retryState.recordAttempt();

    try {
      const startTime = Date.now();

      execSync('npm install --production', {
        cwd: SKILL_DIR,
        timeout: 30000,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      const duration = Date.now() - startTime;
      perfLog.record('npm-install', duration);
      logger.info(`[cognitive-recall] ✅ npm install completed in ${duration}ms`);

      // Reset retry state on success
      retryState.installAttempts = 0;

      // Try loading again
      pgModule = require(path.join(SKILL_DIR, 'node_modules/pg'));
      pgLoaded = true;
      return pgModule;
    } catch (installErr) {
      logger.error('[cognitive-recall] ❌ Auto-install failed:', installErr.message);
      perfLog.record('npm-install', 0, false);
      return null;
    } finally {
      isInstalling = false;
    }
  }
}

// ============================================================================
// 主查询逻辑 - v5.0 架构
// ============================================================================

async function recallFromDB(queries, limit = 3) {
  const startTime = Date.now();

  // Check cache
  const cacheKey = queries.join('|');
  const cached = getCacheEntry(cacheKey);
  if (cached) {
    perfLog.record('cache-hit', Date.now() - startTime);
    return cached;
  }

  // Try v5.0 brain first
  const brain = getBrain();
  if (brain) {
    try {
      const query = queries.join(' ');
      const memories = await brain.recall(query, { limit });
      
      // Convert v5.0 Memory objects to old format for compatibility
      const formatted = memories.map(m => ({
        id: m.id,
        summary: m.summary,
        content: m.content,
        type: m.type,
        importance: m.importance,
        timestamp: m.updatedAt || m.createdAt
      }));

      // Cache result
      if (formatted.length > 0) {
        const maxImportance = Math.max(...formatted.map(m => m.importance || 0.5));
        setCacheEntry(cacheKey, formatted, maxImportance);
      }

      perfLog.record('brain-recall', Date.now() - startTime);
      return formatted;
    } catch (e) {
      logger.warn('[cognitive-recall] v5.0 brain recall failed, falling back:', e.message);
      // Continue to legacy mode
    }
  }

  // Legacy fallback (direct SQL)
  const pg = ensurePgDependency();
  if (!pg) {
    logger.error('[cognitive-recall] pg module unavailable');
    return [];
  }

  const config = getConfig();
  if (!config) {
    logger.info('[cognitive-recall] Config not found');
    return [];
  }

  try {
    const pool = getDbPool();
    if (!pool) {
      logger.error('[cognitive-recall] Database pool unavailable');
      return [];
    }

    const conditions = queries.map((q, i) => `(summary ILIKE $${i + 1} OR content ILIKE $${i + 1})`).join(' OR ');
    const params = queries.map(q => `%${q}%`);
    params.push(limit.toString());

    const result = await pool.query(`
      SELECT id, summary, content, type, importance, timestamp
      FROM episodes
      WHERE ${conditions}
      ORDER BY importance DESC, timestamp DESC
      LIMIT $${params.length}
    `, params);

    const memories = result.rows;

    if (memories.length > 0) {
      const maxImportance = Math.max(...memories.map(m => m.importance || 0.5));
      setCacheEntry(cacheKey, memories, maxImportance);
    }

    perfLog.record('db-query', Date.now() - startTime);
    return memories;
  } catch (err) {
    logger.error('[cognitive-recall] DB error:', err.message);
    perfLog.record('db-query', Date.now() - startTime, false);
    return [];
  }
}

// ============================================================================
// 查询高重要性记忆（数据库优先策略）
// ============================================================================

async function recallCriticalMemories() {
  const startTime = Date.now();
  
  // Check cache
  const cacheKey = 'critical-memories';
  const cached = getCacheEntry(cacheKey);
  if (cached) {
    return cached;
  }

  // Load pg
  const pg = ensurePgDependency();
  if (!pg) {
    logger.info('[cognitive-recall] pg unavailable for critical memories');
    return [];
  }

  // Check config
  const config = getConfig();
  if (!config) {
    return [];
  }
  const dbConfig = config.storage.primary;

  // Health check
  const isHealthy = await healthState.check(pg, dbConfig);
  if (!isHealthy) {
    return [];
  }

  try {
    // Use singleton pool instead of creating new one
    const pool = getDbPool();
    if (!pool) {
      logger.error('[cognitive-recall] Database pool unavailable');
      return [];
    }

    // Query high-importance memories: reflection, lesson types with importance >= 0.8
    const result = await pool.query(`
      SELECT id, summary, content, type, importance, timestamp
      FROM episodes
      WHERE importance >= 0.8
        AND type IN ('reflection', 'lesson', 'milestone')
      ORDER BY importance DESC, timestamp DESC
      LIMIT 5
    `);

    const memories = result.rows;

    // Cache with high TTL (critical memories don't change often)
    if (memories.length > 0) {
      setCacheEntry(cacheKey, memories, 0.95); // High importance = long cache
    }

    logger.info('[cognitive-recall] Retrieved', memories.length, 'critical memories from DB');
    return memories;
  } catch (err) {
    logger.error('[cognitive-recall] Critical memories query error:', err.message);
    return [];
  }
}

// ============================================================================
// 自动编码 - 记录对话到 brain (v5.0 架构)
// ============================================================================

const encodeMemory = async (content, metadata = {}) => {
  const startTime = Date.now();

  // Skip short messages
  if (!content || content.length < 10) return null;

  // Skip system messages
  if (content.includes('[🧠 Memory Context]')) return null;

  // Skip duplicate encoding (check recent cache)
  const cacheKey = `encode:${content.slice(0, 50)}`;
  if (recallCache.has(cacheKey)) return null;

  // Try v5.0 brain first
  const brain = getBrain();
  if (brain) {
    try {
      const entities = extractEntities(content);
      const memory = await brain.encode(content, {
        type: metadata.type || 'episodic',
        importance: calculateImportance(content, metadata),
        sourceChannel: metadata.channel || 'unknown',
        role: metadata.role || 'user',
        entities: entities
      });

      // Mark as encoded
      recallCache.set(cacheKey, true);

      perfLog.record('brain-encode', Date.now() - startTime);
      logger.info(`[encodeMemory] v5.0 encoded: ${memory.id}`);
      return memory.id;
    } catch (e) {
      logger.warn('[encodeMemory] v5.0 brain encode failed, falling back:', e.message);
      // Continue to legacy mode
    }
  }

  // Legacy fallback (direct SQL)
  let pg;
  try {
    pg = require('/root/.openclaw/workspace/skills/cognitive-brain/node_modules/pg');
  } catch (e) {
    try {
      pg = require('pg');
    } catch (e2) {
      return null;
    }
  }

  if (!fs.existsSync(CONFIG_PATH)) return null;

  try {
    const pool = getDbPool();
    if (!pool) {
      logger.error('[cognitive-recall] Database pool unavailable');
      return null;
    }

    const entities = extractEntities(content);
    const importance = calculateImportance(content, metadata);

    const result = await pool.query(`
      INSERT INTO episodes (summary, content, type, source_channel, importance, entities, timestamp, role)
      VALUES ($1, $2, $3, $4, $5, $6, NOW(), $7)
      RETURNING id
    `, [
      content.slice(0, 200),
      content,
      metadata.type || 'episodic',
      metadata.channel || 'unknown',
      importance,
      JSON.stringify(entities),
      metadata.role || 'user'
    ]);

    recallCache.set(cacheKey, true);
    perfLog.record('encode', Date.now() - startTime);
    return result.rows[0].id;
  } catch (err) {
    logger.error('[cognitive-recall] Encode error:', err.message);
    return null;
  }
};

// 简单实体提取（改进版 - 与 encode.cjs 保持一致）
const STOPWORDS = new Set([
  '的', '是', '在', '了', '和', '与', '或', '有', '为', '以', '及', '等', '中', '到', '从', '对', '就', '也', '都', '而',
  '且', '但', '如', '被', '把', '让', '给', '向', '这', '那', '之', '所', '者', '于', '其', '将', '已', '不', '没', '很',
  '通过', '使用', '进行', '实现', '可以', '需要', '应该', '一个', '这个', '那个'
]);

const CONCEPT_PATTERNS = {
  tech: /\b(Rust|Python|JavaScript|TypeScript|AI|API|SQL|Redis|PostgreSQL|LLM|GPT|Embedding|Vector|Docker|K8s|Kubernetes|Brain|ClawHub|GitHub|Git|Linux|Ubuntu)\b/gi,
  chineseKeywords: /(用户|记忆|系统|模块|功能|项目|任务|计划|目标|问题|方案|设计|架构|数据|配置|文件|脚本|服务|概念|实体|情感|意图|决策|对话|预测|反思|联想|遗忘|学习|优化|改进|更新|版本|日志|错误|警告|分析|洞察|建议|偏好|兴趣|画像|模式|趋势|关系|网络|节点|向量|嵌入|缓存|存储|数据库|查询|检索|编码|处理|参数|选项|设置|环境|依赖|框架|工具|平台|接口|文档|测试|验证|检查|监控|性能|质量|准确性|可靠性|安全性|权限|认证|授权|路径|目录|格式|函数|方法|类|属性|变量|异常|内存|磁盘|网络|并发|异步|队列|索引|排序|搜索|过滤|创建|读取|写入|删除|事务|启动|停止|重启|初始化|安装|加载|保存|导出|导入|升级|发布|部署|维护|重构|修复|清理|网关|代理|路由|控制器|客户端|服务器|请求|响应|会话|Token|密钥|签名|加密|解密)/g
};

const extractEntities = (text) => {
  const entities = [];
  const seen = new Set();
  
  // 1. 技术术语
  const techTerms = text.match(CONCEPT_PATTERNS.tech) || [];
  techTerms.forEach(term => {
    const normalized = term.toLowerCase();
    if (!seen.has(normalized)) {
      seen.add(normalized);
      entities.push(term);
    }
  });
  
  // 2. 中文关键词
  const chineseKeywords = text.match(CONCEPT_PATTERNS.chineseKeywords) || [];
  chineseKeywords.forEach(word => {
    const normalized = word.toLowerCase();
    if (!seen.has(normalized)) {
      seen.add(normalized);
      entities.push(word);
    }
  });
  
  // 3. 简单中文词组（2-4字，过滤停用词）
  if (entities.length < 5) {
    const simpleMatches = text.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
    for (const word of simpleMatches) {
      // 过滤停用词开头或结尾的词
      if (STOPWORDS.has(word[0]) || STOPWORDS.has(word.slice(-1))) continue;
      // 过滤纯停用词组合
      if (word.split('').every(c => STOPWORDS.has(c))) continue;
      
      const normalized = word.toLowerCase();
      if (!seen.has(normalized) && entities.length < 10) {
        seen.add(normalized);
        entities.push(word);
      }
    }
  }
  
  return entities.slice(0, 10);
};

// 计算重要性
const calculateImportance = (content, metadata) => {
  let importance = 0.5;
  
  // 用户消息更重要
  if (metadata.role === 'user') importance += 0.2;
  
  // 包含关键词
  const importantKeywords = ['记住', '重要', '偏好', '设置', '不要', '喜欢', '讨厌'];
  for (const kw of importantKeywords) {
    if (content.includes(kw)) {
      importance += 0.1;
    }
  }
  
  // 长内容可能更重要
  if (content.length > 100) importance += 0.1;
  if (content.length > 500) importance += 0.1;
  
  return Math.min(1.0, importance);
};

// ============================================================================
// 用户建模自动学习
// ============================================================================


// 话题关键词
const TOPIC_KEYWORDS = {
  '编程': ['代码', '函数', '变量', 'bug', 'error', '编译', '运行', '调试'],
  'AI': ['AI', '模型', '训练', '神经网络', '机器学习', '深度学习', 'LLM', 'GPT'],
  '记忆': ['记忆', '回忆', '记住', '忘记', 'brain', 'cognitive'],
  '项目': ['项目', '工程', '开发', '版本', '发布', '部署'],
  '数据': ['数据', '数据库', 'SQL', 'PostgreSQL', 'Redis', '存储'],
  '系统': ['系统', '配置', '服务器', '部署', '监控', '日志'],
  '文档': ['文档', 'markdown', '笔记', '记录', '总结'],
  '聊天': ['聊天', '对话', '消息', 'QQ', '私聊', '群']
};

// 从消息中提取话题
const extractTopics = (text) => {
  const topics = [];
  for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
    for (const kw of keywords) {
      if (text.toLowerCase().includes(kw.toLowerCase())) {
        topics.push(topic);
        break;
      }
    }
  }
  return topics;
};

// 推断沟通风格
const inferCommunicationStyle = (text) => {
  const formal = ['请', '麻烦', '能否', '是否', '您好'].filter(k => text.includes(k)).length;
  const casual = ['哈', '哈哈', '嗯', '啊', '呢', '吧', '～', '...'].filter(k => text.includes(k)).length;
  
  if (formal > casual) return 'formal';
  if (casual > formal) return 'casual';
  return 'balanced';
};

// 更新用户模型
const updateUserModel = (message, metadata) => {
  try {
    // 加载现有模型
    let userModel = {
      basic: { name: null, communicationStyle: 'casual' },
      preferences: { topics: {} },
      patterns: { activeHours: [], commonTasks: {} },
      knowledge: { knownConcepts: [], expertiseAreas: [] },
      stats: { totalInteractions: 0, lastInteraction: null }
    };
    
    if (fs.existsSync(USER_MODEL_PATH)) {
      try {
        const loaded = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
        // Merge with defaults to ensure all fields exist
        userModel = {
          ...userModel,
          ...loaded,
          basic: { ...userModel.basic, ...loaded.basic },
          preferences: { ...userModel.preferences, ...loaded.preferences },
          patterns: { ...userModel.patterns, ...loaded.patterns },
          knowledge: { ...userModel.knowledge, ...loaded.knowledge },
          stats: { ...userModel.stats, ...loaded.stats }
        };
      } catch (e) {
        logger.warn('[cognitive-recall] Failed to parse user model, using defaults');
      }
    }

    // 更新交互统计
    userModel.stats.totalInteractions++;
    userModel.stats.lastInteraction = Date.now();

    // 记录活跃时段
    const hour = new Date().getHours();
    if (!userModel.patterns.activeHours.includes(hour)) {
      userModel.patterns.activeHours.push(hour);
      userModel.patterns.activeHours.sort();
    }
    
    // 提取并更新话题兴趣
    const topics = extractTopics(message);
    if (userModel.preferences && userModel.preferences.topics) {
      for (const topic of topics) {
        if (!userModel.preferences.topics[topic]) {
          userModel.preferences.topics[topic] = 0;
        }
        userModel.preferences.topics[topic] = Math.min(1, userModel.preferences.topics[topic] + 0.1);
      }
    }

    // 推断沟通风格
    const style = inferCommunicationStyle(message);
    if (style !== 'balanced' && userModel.basic) {
      userModel.basic.communicationStyle = style;
    }

    // 提取用户名（如果消息中包含自我介绍）
    const nameMatch = message.match(/我叫(\S+)|我是(\S+)|名字[是为](\S+)/);
    if (nameMatch && userModel.basic) {
      userModel.basic.name = nameMatch[1] || nameMatch[2] || nameMatch[3];
    }

    // 提取偏好关键词
    const prefs = message.match(/(喜欢|偏好|想要|希望)(\S+)/g);
    if (prefs && userModel.knowledge && userModel.knowledge.knownConcepts) {
      for (const p of prefs) {
        const pref = p.replace(/喜欢|偏好|想要|希望/g, '');
        if (pref && pref.length < 10 && !userModel.knowledge.knownConcepts.includes(pref)) {
          userModel.knowledge.knownConcepts.push(pref);
        }
      }
    }
    
    // 保存
    fs.writeFileSync(USER_MODEL_PATH, JSON.stringify(userModel, null, 2));
    return userModel;
  } catch (e) {
    logger.error('[cognitive-recall] User model update error:', e.message);
    return null;
  }
};

// ============================================================================
// 预测和预加载模块
// ============================================================================

const { predictAndPreload } = require(path.join(SKILL_DIR, 'scripts/core/prediction_client.cjs'));

// ============================================================================
// Hook handler
// ============================================================================

const handler = async (event) => {
  // Handle agent:bootstrap - inject memory context at session start
  if (event.type === 'agent' && event.action === 'bootstrap') {
    return handleBootstrap(event);
  }
  
  // Handle message:preprocessed - recall memory for each message
  if (event.type === 'message' && event.stage === 'preprocessed') {
    return handlePreprocessed(event);
  }
};

// Handle bootstrap event - inject memory context
const handleBootstrap = async (event) => {
  // 强制日志：验证 hook 被触发
  logTrigger();

  logger.info('[cognitive-recall] handleBootstrap called');

  // Skip if no context
  if (!event.context) return;

  const context = event.context;
  const sessionKey = context.sessionKey || '';

  // 只在私聊会话中注入记忆
  if (sessionKey.includes(':group:') || sessionKey.includes('group')) {
    logger.info('[cognitive-recall] Skipping group session');
    return;
  }

  try {
    // 使用多个查询获取更多记忆
    const brain = getBrain();
    let memories = [];
    
    if (brain) {
      try {
        // 多个语义查询
        const queries = ['用户偏好', '重要配置', '教训', 'master', '定时任务'];
        const results = await Promise.all(queries.map(q => brain.recall(q, { limit: 3 })));
        
        // 去重
        const uniqueMemories = new Map();
        results.flat().forEach(m => {
          if (!uniqueMemories.has(m.id)) {
            uniqueMemories.set(m.id, m);
          }
        });
        memories = Array.from(uniqueMemories.values());
        logger.info('[cognitive-recall] Brain recall found:', memories.length, 'memories');
      } catch (e) {
        logger.warn('[cognitive-recall] Brain recall failed:', e.message);
      }
    }
    
    // 如果 brain 失败，直接查询数据库
    if (memories.length === 0) {
      try {
        const pool = getDbPool();
        if (pool) {
          const result = await pool.query(`
            SELECT id, summary, content, type, importance, created_at 
            FROM episodes 
            ORDER BY importance DESC, created_at DESC 
            LIMIT 10
          `);
          memories = result.rows;
          logger.info('[cognitive-recall] DB fallback found:', memories.length, 'memories');
        }
      } catch (e) {
        logger.error('[cognitive-recall] DB query failed:', e.message);
      }
    }

    if (!memories || memories.length === 0) {
      logger.info('[cognitive-recall] No memories found');
      return;
    }

    // 构建记忆内容
    const memoryContent = memories.slice(0, 10).map((m, i) => {
      const text = m.summary || m.content || '';
      return `${i + 1}. ${text.substring(0, 150)}${text.length > 150 ? '...' : ''}`;
    }).join('\n');

    const injectedContent = `## 🧠 Cognitive Brain Memory Context

Important context from previous sessions:

${memoryContent}

---

`;

    // 写入临时文件
    const tmpFile = path.join('/tmp', `cognitive-memory-${Date.now()}.md`);
    fs.writeFileSync(tmpFile, injectedContent, 'utf8');

    // 添加到 bootstrapFiles
    if (!context.bootstrapFiles) {
      context.bootstrapFiles = [];
    }
    context.bootstrapFiles.push({
      path: tmpFile,
      basename: 'COGNITIVE_MEMORY.md',
      content: injectedContent
    });

    logger.info('[cognitive-recall] Injected', memories.length, 'memories into bootstrap');

  } catch (err) {
    logger.error('[cognitive-recall] Bootstrap error:', err.message || String(err));
  }
};

// Handle preprocessed event - recall memory (保留但不再作为主入口)
const handlePreprocessed = async (event) => {
  // 强制日志：验证 hook 被触发
  logTrigger();

  // Debug: log all events for debugging
  const channel = event.context?.channel || 'unknown';
  logger.info('[cognitive-recall] handlePreprocessed called, channel:', channel);
  logger.info('[cognitive-recall] Debug - event.context keys:', Object.keys(event.context || {}));

  // Skip if no context
  if (!event.context) return;

  // Only recall for direct messages (not groups)
  if (event.context.isGroup || event.context.groupId) return;

  // Skip if bodyForAgent is empty
  if (!event.context.bodyForAgent) return;

  // Get dynamic keywords
  const keywords = keywordState.getKeywords();

  // 教训关键词 - 始终检索
  const lessonKeywords = ['教训', '规则', '记住', '必须', '不要'];
  
  const sender = event.context.senderId || event.sender_id || 'unknown';
  
  // 保存原始消息（用于编码，在注入上下文之前）
  const originalMessage = event.context.bodyForAgent;

  try {
    // 初始化共享工作区
    await initSharedMemory();
    
    // 获取共享 pool 用于预测
    const pool = getDbPool();

    // 并行执行：检索记忆 + 教训 + 预测 + 高重要性记忆
    const [memoriesResult, lessonsResult, predictionResult, criticalMemoriesResult] = await Promise.all([
      recallFromDB(keywords, 5),
      getLessonsFromSharedMemory(),
      predictAndPreload(sender, [event.context.bodyForAgent], pool),
      recallCriticalMemories() // 新增：查询高重要性记忆
    ]);
    
    const memories = memoriesResult;
    const lessons = lessonsResult;
    const { predictions, memories: predictedMemories } = predictionResult;
    const criticalMemories = criticalMemoriesResult;

    const contextParts = [];
    
    // 注入高重要性记忆（数据库优先）
    if (criticalMemories && criticalMemories.length > 0) {
      const criticalLines = criticalMemories.map(m => {
        const typeEmoji = m.type === 'reflection' ? '💡' : m.type === 'lesson' ? '⚠️' : '📝';
        return `  ${typeEmoji} ${m.summary || m.content.substring(0, 80)}`;
      });
      contextParts.push(`[🧠 重要记忆]\n${criticalLines.join('\n')}\n[/重要记忆]`);
    }
    
    // 注入预测信息
    if (predictions && predictions.length > 0) {
      const predLines = predictions.map(p => {
        const confidenceEmoji = p.confidence > 0.7 ? '🔴' : p.confidence > 0.5 ? '🟡' : '🔵';
        return `  ${confidenceEmoji} ${p.reason}`;
      });
      contextParts.push(`[🔮 预测]\n${predLines.join('\n')}\n[/预测]`);
    }
    
    // 注入预加载的记忆
    if (predictedMemories && predictedMemories.length > 0) {
      const preloadLines = predictedMemories.map(m => {
        return `  - ${m.summary || m.content.substring(0, 80)}${m.preloadReason ? ` (${m.preloadReason})` : ''}`;
      });
      contextParts.push(`[⚡ 预加载]\n${preloadLines.join('\n')}\n[/预加载]`);
    }
    
    // 注入普通记忆
    if (memories && memories.length > 0) {
      const memoryLines = memories.map(m => {
        const source = m.source ? ` (${m.source})` : '';
        return `  - ${m.summary}${source}`;
      });
      contextParts.push(`[🧠 Memory Context]\n${memoryLines.join('\n')}\n[/Memory Context]`);
    }
    
    // 注入教训
    if (lessons && lessons.length > 0) {
      const lessonLines = lessons.map(l => `  - ${l.summary}`);
      contextParts.push(`[⚠️ 教训提醒]\n${lessonLines.join('\n')}\n[/教训提醒]`);
    }

    if (contextParts.length > 0) {
      const fullContext = '\n\n' + contextParts.join('\n\n') + '\n\n';
      event.context.bodyForAgent = fullContext + event.context.bodyForAgent;
      logger.info('[cognitive-recall] Injected', 
        memories?.length || 0, 'memories +', 
        lessons?.length || 0, 'lessons +',
        predictions?.length || 0, 'predictions +',
        predictedMemories?.length || 0, 'preloaded');
    }
    
    // 自动编码用户消息（异步，不阻塞）
    encodeMemory(originalMessage, {
      role: 'user',
      sender,
      channel: event.context.channel || 'unknown',
      type: 'episodic'
    }).then(id => {
      if (id) {
        logger.info('[cognitive-recall] Auto-encoded user message:', id);
      }
    }).catch(() => {});
    
    // 延迟捕获 AI 回复（5秒后）
    const sessionId = event.context?.sessionId || event.context?.conversationId || event.session_id || event.conversation_id;
    const messageId = event.context?.messageId || event.context?.message_id || event.messageId;
    logger.info('[cognitive-recall] Debug - sessionId:', sessionId, 'messageId:', messageId?.substring(0, 20));
    if (sessionId && messageId) {
      logger.info('[cognitive-recall] Scheduling assistant capture in 5s...');
      setTimeout(() => {
        captureAssistantReply(sessionId, messageId, sender, channel);
      }, 5000);
    } else {
      logger.info('[cognitive-recall] Missing sessionId or messageId, skip capture');
    }
    
    // 自动学习用户偏好（异步）
    const userModel = updateUserModel(originalMessage, { sender });
    if (userModel && userModel.preferences.topics) {
      const topTopics = Object.entries(userModel.preferences.topics)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([t]) => t);
      if (topTopics.length > 0) {
        logger.info('[cognitive-recall] 用户兴趣:', topTopics.join(', '));
      }
    }
    
  } catch (err) {
    logger.error('[cognitive-recall] Error:', err.message || String(err));
  } finally {
    // Clean up shared memory connection
    if (sharedMemory && sharedMemoryReady) {
      try {
        await sharedMemory.close();
        sharedMemoryReady = false;
        sharedMemory = null;
      } catch (e) {
        // Ignore close errors
      }
    }
  }
};

// 延迟捕获 AI 回复
const captureAssistantReply = async (sessionId, userMessageId, sender, channel) => {
  try {
    // 构建会话文件路径
    const sessionFile = path.join('/root/.openclaw/agents/main/sessions', `${sessionId}.jsonl`);
    if (!fs.existsSync(sessionFile)) return;
    
    // 读取会话文件
    const content = fs.readFileSync(sessionFile, 'utf8');
    const lines = content.split('\n').filter(l => l.trim());
    
    // 找到用户消息的位置
    let userIndex = -1;
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const msg = JSON.parse(lines[i]);
        if (msg.role === 'user' && msg.content?.includes?.(userMessageId)) {
          userIndex = i;
          break;
        }
      } catch (e) {
        // JSON parse error, skip this line
      }
    }
    
    if (userIndex === -1) return;
    
    // 查找后续的 assistant 回复
    for (let i = userIndex + 1; i < lines.length; i++) {
      try {
        const msg = JSON.parse(lines[i]);
        if (msg.role === 'assistant' && msg.content) {
          const text = typeof msg.content === 'string' 
            ? msg.content 
            : msg.content.map(c => c.text || '').join('');
          
          if (text && text.length > 10) {
            // 编码 AI 回复
            const id = await encodeMemory(text, {
              role: 'assistant',
              sender: 'assistant',
              channel,
              type: 'episodic',
              replyTo: userMessageId
            });
            if (id) {
              logger.info('[cognitive-recall] Auto-encoded assistant reply:', id);
            }
            return;
          }
        }
      } catch (e) {
        logger.warn('[cognitive-recall] Failed to encode assistant reply:', e.message);
      }
    }
  } catch (err) {
    logger.error('[cognitive-recall] Capture assistant reply failed:', err.message);
  }
};

module.exports = handler;


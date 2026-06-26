/**
 * Legacy 适配器 — 旧 heartflow-skill 模块的惰性加载桥
 *
 * 旧模块被吸收到 src/legacy/ 目录，通过此适配器桥接到
 * 新心虫的 dispatch 系统。模块不会被自动初始化（保持清瘦），
 * 只在首次通过 dispatch 访问时才加载。
 *
 * 用法:
 *   hf.legacy.load('cbt')         → CBTModule 实例
 *   hf.dispatch('legacy.cbt.processInput', text)
 */

const path = require('path');

// 缓存已加载的模块实例
const _cache = {};

// 旧模块路径映射
const MODULE_MAP = {
  act:                { path: './act',               ctor: null },
  appraisal:          { path: './appraisal',         ctor: null },
  attachment:         { path: './attachment',        ctor: null },
  'attachment-enhancement':   { path: './attachment-enhancement', ctor: null },
  awakening:          { path: './awakening',         ctor: null },
  'awe-psychology':   { path: './awe-psychology',    ctor: null },
  cbt:                { path: './cbt',               ctor: 'CBTModule' },
  'collective-emotion':       { path: './collective-emotion', ctor: null },
  'collective-identity':      { path: './collective-identity', ctor: null },
  'collective-intentionality':{ path: './collective-intentionality', ctor: null },
  consciousness:      { path: './consciousness',     ctor: null },
  'embodied-cognition':       { path: './embodied-cognition', ctor: null },
  'emotion-regulation':       { path: './emotion-regulation', ctor: null },
  'emotion-theory':   { path: './emotion-theory',    ctor: null },
  'emotion-traditions-integration': { path: './emotion-traditions-integration', ctor: null },
  'emotional-granularity':    { path: './emotional-granularity', ctor: null },
  'emotional-intelligence':   { path: './emotional-intelligence', ctor: null },
  empathy:            { path: './empathy',           ctor: null },
  existential:        { path: './existential',       ctor: null },
  'free-will-agency': { path: './free-will-agency',  ctor: null },
  'happiness-wellbeing':      { path: './happiness-wellbeing', ctor: null },
  humanistic:         { path: './humanistic',        ctor: null },
  intentionality:     { path: './intentionality',    ctor: null },
  mentalization:      { path: './mentalization',     ctor: null },
  'meta-agency':      { path: './meta-agency',       ctor: null },
  mindfulness:        { path: './mindfulness',       ctor: null },
  'moral-psychology': { path: './moral-psychology',  ctor: null },
  'narrative-psychology':     { path: './narrative-psychology', ctor: null },
  personality:        { path: './personality',       ctor: null },
  'phenomenological-consciousness': { path: './phenomenological-consciousness', ctor: null },
  'positive-psychology':      { path: './positive-psychology', ctor: null },
  'predictive-emotion':       { path: './predictive-emotion', ctor: null },
  'relational-self':  { path: './relational-self',   ctor: null },
  'self-checking':    { path: './self-checking',     ctor: null },
  'self-compassion':  { path: './self-compassion',   ctor: null },
  'self-consciousness':       { path: './self-consciousness', ctor: null },
  'social-psychology':        { path: './social-psychology', ctor: null },
  stoic:              { path: './stoic',             ctor: 'StoicModule' },
  'temporal-consciousness':   { path: './temporal-consciousness', ctor: null },
  'virtue-ethics':    { path: './virtue-ethics',     ctor: null },
};

class LegacyBridge {
  constructor(rootPath) {
    this.rootPath = rootPath;
    this._loaded = {};
    this._moduleKeys = Object.keys(MODULE_MAP);
  }

  /**
   * 获取旧模块列表
   */
  list() {
    return {
      available: this._moduleKeys,
      loaded: Object.keys(this._loaded),
      cached: Object.keys(_cache),
    };
  }

  /**
   * 加载指定旧模块，返回其实例
   * @param {string} name - 模块名（如 'cbt', 'stoic'）
   * @returns {object|null} 模块实例
   */
  load(name) {
    if (this._loaded[name]) return this._loaded[name];
    if (_cache[name]) {
      this._loaded[name] = _cache[name];
      return _cache[name];
    }

    const entry = MODULE_MAP[name];
    if (!entry) return null;

    try {
      const modPath = path.resolve(this.rootPath, 'src/legacy', entry.path);
      const mod = require(modPath);

      let instance;
      if (entry.ctor && mod[entry.ctor]) {
        instance = new mod[entry.ctor]();
      } else if (typeof mod === 'function') {
        instance = new mod();
      } else if (typeof mod === 'object' && mod !== null && typeof mod.processInput === 'function') {
        // 模块本身就是带 processInput 的对象
        instance = mod;
      } else {
        // 直接暴露模块导出
        instance = mod;
      }

      _cache[name] = instance;
      this._loaded[name] = instance;
      return instance;
    } catch (e) {
      console.warn(`[LegacyBridge] 加载模块 ${name} 失败:`, e.message);
      return null;
    }
  }

  /**
   * 加载所有旧模块（启动时扫描，不强制实例化）
   */
  scanAll() {
    const results = { loaded: [], failed: [] };
    for (const name of this._moduleKeys) {
      const inst = this.load(name);
      if (inst) {
        results.loaded.push(name);
      } else {
        results.failed.push(name);
      }
    }
    return results;
  }

  /**
   * 获取所有旧模块的可用路由摘要
   */
  routes() {
    const routes = {};
    for (const name of this._moduleKeys) {
      const inst = this._loaded[name] || _cache[name];
      if (!inst) {
        routes[name] = { status: 'lazy', methods: [] };
        continue;
      }
      const methods = Object.getOwnPropertyNames(Object.getPrototypeOf(inst))
        .filter(m => m !== 'constructor' && typeof inst[m] === 'function');
      routes[name] = { status: 'loaded', methods };
    }
    return routes;
  }
}

module.exports = { LegacyBridge, MODULE_MAP };

/**
 * data-pipeline — 数据处理管线引擎
 * 
 * 提供可组合的数据转换管线，支持：
 * - 多阶段管线编排（Pipeline Stage Chain）
 * - 内置数据转换器（filter/map/reduce/groupBy/sort/dedup）
 * - 数据验证与类型检查
 * - 流式处理（大文件分批处理）
 * - 错误恢复与重试机制
 * - 性能指标收集
 * 
 * @version 0.1.0
 */

'use strict';

// ──────────────────────────────────────────────
// 1. 核心管线引擎 (Pipeline Engine)
// ──────────────────────────────────────────────

/**
 * 管线阶段定义
 */
class Stage {
  constructor(name, fn, options = {}) {
    this.name = name;
    this.fn = fn;
    this.enabled = options.enabled !== false;
    this.retryCount = options.retryCount || 0;
    this.retryDelay = options.retryDelay || 100;
    this.timeout = options.timeout || 30000;
    this.metrics = { calls: 0, errors: 0, totalTime: 0 };
  }

  /**
   * 执行阶段，带重试和超时
   */
  async execute(data, context) {
    if (!this.enabled) return data;

    const startTime = Date.now();
    this.metrics.calls++;

    for (let attempt = 0; attempt <= this.retryCount; attempt++) {
      try {
        const result = await this._withTimeout(this.fn(data, context));
        this.metrics.totalTime += Date.now() - startTime;
        return result;
      } catch (err) {
        this.metrics.errors++;
        if (attempt === this.retryCount) {
          err.stageName = this.name;
          err.attempt = attempt + 1;
          throw err;
        }
        await this._sleep(this.retryDelay * (attempt + 1));
      }
    }
  }

  async _withTimeout(promiseOrValue) {
    let timer;
    const timeoutPromise = new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(`Stage "${this.name}" timed out after ${this.timeout}ms`)), this.timeout);
    });
    try {
      const result = await Promise.race([
        Promise.resolve(promiseOrValue),
        timeoutPromise
      ]);
      clearTimeout(timer);
      return result;
    } catch (err) {
      clearTimeout(timer);
      throw err;
    }
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getMetrics() {
    return {
      name: this.name,
      calls: this.metrics.calls,
      errors: this.metrics.errors,
      avgTime: this.metrics.calls > 0
        ? Math.round(this.metrics.totalTime / this.metrics.calls)
        : 0
    };
  }
}

/**
 * 管线执行器
 */
class Pipeline {
  constructor(options = {}) {
    this.stages = [];
    this.context = options.context || {};
    this.strict = options.strict !== false; // strict mode: stop on first error
    this.onStageComplete = options.onStageComplete || null;
    this._metrics = { totalRuns: 0, totalErrors: 0, totalTime: 0 };
  }

  /**
   * 添加一个阶段
   */
  addStage(name, fn, options = {}) {
    this.stages.push(new Stage(name, fn, options));
    return this; // chainable
  }

  /**
   * 批量添加阶段
   */
  addStages(stageDefs) {
    for (const def of stageDefs) {
      this.addStage(def.name, def.fn, def.options);
    }
    return this;
  }

  /**
   * 在指定阶段前插入新阶段
   */
  insertBefore(targetName, name, fn, options = {}) {
    const idx = this.stages.findIndex(s => s.name === targetName);
    if (idx === -1) throw new Error(`Stage "${targetName}" not found`);
    this.stages.splice(idx, 0, new Stage(name, fn, options));
    return this;
  }

  /**
   * 在指定阶段后插入新阶段
   */
  insertAfter(targetName, name, fn, options = {}) {
    const idx = this.stages.findIndex(s => s.name === targetName);
    if (idx === -1) throw new Error(`Stage "${targetName}" not found`);
    this.stages.splice(idx + 1, 0, new Stage(name, fn, options));
    return this;
  }

  /**
   * 移除一个阶段
   */
  removeStage(name) {
    this.stages = this.stages.filter(s => s.name !== name);
    return this;
  }

  /**
   * 启用/禁用阶段
   */
  toggleStage(name, enabled) {
    const stage = this.stages.find(s => s.name === name);
    if (!stage) throw new Error(`Stage "${name}" not found`);
    stage.enabled = enabled;
    return this;
  }

  /**
   * 执行管线
   */
  async execute(inputData) {
    const pipelineStart = Date.now();
    this._metrics.totalRuns++;
    let data = this._clone(inputData);
    const stageResults = [];

    for (const stage of this.stages) {
      const stageStart = Date.now();
      try {
        data = await stage.execute(data, this.context);
        const elapsed = Date.now() - stageStart;
        stageResults.push({
          stage: stage.name,
          status: 'completed',
          duration: elapsed,
          dataSize: this._getDataSize(data)
        });

        if (this.onStageComplete) {
          await this.onStageComplete(stage.name, data, elapsed);
        }
      } catch (err) {
        stageResults.push({
          stage: stage.name,
          status: 'failed',
          error: err.message,
          duration: Date.now() - stageStart
        });

        if (this.strict) {
          this._metrics.totalErrors++;
          this._metrics.totalTime += Date.now() - pipelineStart;
          throw new PipelineError(
            `Pipeline failed at stage "${stage.name}"`,
            err,
            stageResults,
            data
          );
        }
        // 非严格模式：跳过失败阶段，继续执行
      }
    }

    this._metrics.totalTime += Date.now() - pipelineStart;

    return {
      data,
      metadata: {
        stages: stageResults,
        totalDuration: Date.now() - pipelineStart,
        stageCount: this.stages.length,
        stageResults
      }
    };
  }

  /**
   * 执行并只返回数据（不带 metadata）
   */
  async run(inputData) {
    const result = await this.execute(inputData);
    return result.data;
  }

  /**
   * 获取管线指标
   */
  getMetrics() {
    return {
      pipeline: {
        totalRuns: this._metrics.totalRuns,
        totalErrors: this._metrics.totalErrors,
        avgTime: this._metrics.totalRuns > 0
          ? Math.round(this._metrics.totalTime / this._metrics.totalRuns)
          : 0
      },
      stages: this.stages.map(s => s.getMetrics())
    };
  }

  /**
   * 重置指标
   */
  resetMetrics() {
    this._metrics = { totalRuns: 0, totalErrors: 0, totalTime: 0 };
    for (const stage of this.stages) {
      stage.metrics = { calls: 0, errors: 0, totalTime: 0 };
    }
  }

  /**
   * 克隆数据（浅克隆）
   */
  _clone(data) {
    if (Array.isArray(data)) return [...data];
    if (data && typeof data === 'object') return { ...data };
    return data;
  }

  _getDataSize(data) {
    if (Array.isArray(data)) return data.length;
    if (data && typeof data === 'object') return Object.keys(data).length;
    return 0;
  }
}

/**
 * 管线错误（携带阶段信息）
 */
class PipelineError extends Error {
  constructor(message, originalError, stageResults, lastData) {
    super(message);
    this.name = 'PipelineError';
    this.originalError = originalError;
    this.stageResults = stageResults;
    this.lastData = lastData;
    this.failedStage = originalError.stageName || 'unknown';
    this.failedAttempt = originalError.attempt || 1;
  }
}

// ──────────────────────────────────────────────
// 2. 内置转换器 (Built-in Transformers)
// ──────────────────────────────────────────────

const Transformers = {
  /**
   * 过滤：保留满足条件的项
   */
  filter(predicate) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('filter requires array input');
      return data.filter(predicate);
    };
  },

  /**
   * 映射：转换每项
   */
  map(fn) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('map requires array input');
      return data.map(fn);
    };
  },

  /**
   * 归约：聚合为单个值
   */
  reduce(reducer, initial) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('reduce requires array input');
      return data.reduce(reducer, initial);
    };
  },

  /**
   * 分组：按字段分组
   */
  groupBy(keyFn) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('groupBy requires array input');
      const groups = {};
      for (const item of data) {
        const key = typeof keyFn === 'function' ? keyFn(item) : item[keyFn];
        if (!groups[key]) groups[key] = [];
        groups[key].push(item);
      }
      return groups;
    };
  },

  /**
   * 排序：按字段或比较函数排序
   */
  sort(comparatorOrKey, order = 'asc') {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('sort requires array input');
      const sorted = [...data];
      if (typeof comparatorOrKey === 'function') {
        sorted.sort(comparatorOrKey);
      } else {
        sorted.sort((a, b) => {
          const va = a[comparatorOrKey], vb = b[comparatorOrKey];
          if (va < vb) return order === 'asc' ? -1 : 1;
          if (va > vb) return order === 'asc' ? 1 : -1;
          return 0;
        });
      }
      return sorted;
    };
  },

  /**
   * 去重：按字段去重
   */
  dedup(keyFn) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('dedup requires array input');
      const seen = new Set();
      return data.filter(item => {
        const key = typeof keyFn === 'function' ? keyFn(item) : item[keyFn];
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    };
  },

  /**
   * 扁平化：展平嵌套数组
   */
  flatten(depth = 1) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('flatten requires array input');
      return data.flat(depth);
    };
  },

  /**
   * 分页：截取数据段
   */
  paginate(page = 1, pageSize = 10) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('paginate requires array input');
      const start = (page - 1) * pageSize;
      return data.slice(start, start + pageSize);
    };
  },

  /**
   * 限制：只取前 N 项
   */
  limit(n) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('limit requires array input');
      return data.slice(0, n);
    };
  },

  /**
   * 选择：从对象中选择字段
   */
  pick(fields) {
    return (data) => {
      if (Array.isArray(data)) {
        return data.map(item => {
          const result = {};
          for (const field of fields) {
            if (item[field] !== undefined) result[field] = item[field];
          }
          return result;
        });
      }
      const result = {};
      for (const field of fields) {
        if (data[field] !== undefined) result[field] = data[field];
      }
      return result;
    };
  },

  /**
   * 重命名字段
   */
  rename(fieldMap) {
    return (data) => {
      if (Array.isArray(data)) {
        return data.map(item => {
          const result = { ...item };
          for (const [oldName, newName] of Object.entries(fieldMap)) {
            if (result[oldName] !== undefined) {
              result[newName] = result[oldName];
              delete result[oldName];
            }
          }
          return result;
        });
      }
      const result = { ...data };
      for (const [oldName, newName] of Object.entries(fieldMap)) {
        if (result[oldName] !== undefined) {
          result[newName] = result[oldName];
          delete result[oldName];
        }
      }
      return result;
    };
  },

  /**
   * 合并：合并多个对象数组
   */
  merge(joinKey, ...sources) {
    return (data) => {
      if (!Array.isArray(data)) throw new TypeError('merge requires array input');
      const lookup = {};
      for (const source of sources) {
        for (const item of source) {
          const key = item[joinKey];
          if (key !== undefined) lookup[key] = { ...lookup[key], ...item };
        }
      }
      return data.map(item => {
        const key = item[joinKey];
        return key !== undefined ? { ...item, ...(lookup[key] || {}) } : { ...item };
      });
    };
  }
};

// ──────────────────────────────────────────────
// 3. 验证器 (Validators)
// ──────────────────────────────────────────────

const Validators = {
  /**
   * 创建字段验证器
   */
  schema(schemaDef) {
    return (data) => {
      const items = Array.isArray(data) ? data : [data];
      const errors = [];

      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const itemErrors = [];

        for (const [field, rules] of Object.entries(schemaDef)) {
          const value = item[field];

          // required
          if (rules.required && (value === undefined || value === null)) {
            itemErrors.push({ field, rule: 'required', message: `Field "${field}" is required` });
            continue;
          }

          if (value === undefined || value === null) continue;

          // type
          if (rules.type && typeof value !== rules.type) {
            itemErrors.push({ field, rule: 'type', message: `Field "${field}" expected ${rules.type}, got ${typeof value}` });
          }

          // min
          if (rules.min !== undefined && value < rules.min) {
            itemErrors.push({ field, rule: 'min', message: `Field "${field}" must be >= ${rules.min}` });
          }

          // max
          if (rules.max !== undefined && value > rules.max) {
            itemErrors.push({ field, rule: 'max', message: `Field "${field}" must be <= ${rules.max}` });
          }

          // minLength / maxLength
          if (typeof value === 'string' || Array.isArray(value)) {
            if (rules.minLength !== undefined && value.length < rules.minLength) {
              itemErrors.push({ field, rule: 'minLength', message: `Field "${field}" length must be >= ${rules.minLength}` });
            }
            if (rules.maxLength !== undefined && value.length > rules.maxLength) {
              itemErrors.push({ field, rule: 'maxLength', message: `Field "${field}" length must be <= ${rules.maxLength}` });
            }
          }

          // pattern
          if (rules.pattern && typeof value === 'string') {
            const regex = typeof rules.pattern === 'string' ? new RegExp(rules.pattern) : rules.pattern;
            if (!regex.test(value)) {
              itemErrors.push({ field, rule: 'pattern', message: `Field "${field}" does not match pattern ${rules.pattern}` });
            }
          }

          // enum
          if (rules.enum && !rules.enum.includes(value)) {
            itemErrors.push({ field, rule: 'enum', message: `Field "${field}" must be one of [${rules.enum.join(', ')}]` });
          }

          // custom
          if (rules.validate && typeof rules.validate === 'function') {
            const customResult = rules.validate(value, item);
            if (customResult !== true) {
              itemErrors.push({ field, rule: 'custom', message: typeof customResult === 'string' ? customResult : `Field "${field}" failed custom validation` });
            }
          }
        }

        if (itemErrors.length > 0) {
          errors.push({ index: i, errors: itemErrors });
        }
      }

      return {
        valid: errors.length === 0,
        errors,
        totalItems: items.length,
        validItems: items.length - errors.length
      };
    };
  }
};

// ──────────────────────────────────────────────
// 4. 工厂函数 (Factory Functions)
// ──────────────────────────────────────────────

/**
 * 创建预定义的管线
 */
const PipelineFactory = {
  /**
   * 创建 ETL 管线（提取-转换-加载）
   */
  createETL(extract, transforms, load) {
    const pipeline = new Pipeline();
    pipeline.addStage('extract', extract);
    for (const t of transforms) {
      pipeline.addStage(t.name, t.fn, t.options);
    }
    pipeline.addStage('load', load);
    return pipeline;
  },

  /**
   * 创建数据清洗管线
   */
  createCleaner(schemaDef, fieldDefaults = {}) {
    const pipeline = new Pipeline();

    // 验证阶段：严格模式，验证失败时抛错中断管线
    const validator = Validators.schema(schemaDef);
    pipeline
      .addStage('validate', (data) => {
        const items = Array.isArray(data) ? data : [data];
        const result = validator(items);
        if (!result.valid) {
          throw new Error(`Validation failed: ${result.errors.length} invalid item(s). ` +
            result.errors.map(e => `item[${e.index}]: ${e.errors.map(err => err.message).join(', ')}`).join('; '));
        }
        return data;
      }, { retryCount: 0 })
      .addStage('applyDefaults', (data) => {
        const items = Array.isArray(data) ? data : [data];
        return items.map(item => {
          const result = { ...item };
          for (const [field, defaultValue] of Object.entries(fieldDefaults)) {
            if (result[field] === undefined || result[field] === null) {
              result[field] = typeof defaultValue === 'function' ? defaultValue() : defaultValue;
            }
          }
          return result;
        });
      })
      .addStage('trimStrings', (data) => {
        const items = Array.isArray(data) ? data : [data];
        return items.map(item => {
          const result = { ...item };
          for (const [key, value] of Object.entries(result)) {
            if (typeof value === 'string') result[key] = value.trim();
          }
          return result;
        });
      })
      .addStage('removeEmpty', (data) => {
        if (!Array.isArray(data)) return data;
        return data.filter(item => {
          return Object.values(item).some(v => v !== null && v !== undefined && v !== '');
        });
      });

    return pipeline;
  },

  /**
   * 创建数据分析管线
   * aggregations 格式: { resultKey: { field: '源字段名', fn: 聚合函数 } }
   * 例: { avgSalary: { field: 'salary', fn: vals => vals.reduce((a,b)=>a+b,0)/vals.length } }
   */
  createAnalyzer(groupKey, aggregations = {}) {
    const pipeline = new Pipeline();

    pipeline
      .addStage('groupBy', Transformers.groupBy(groupKey))
      .addStage('aggregate', (groups) => {
        const results = [];
        for (const [key, items] of Object.entries(groups)) {
          const agg = { [groupKey]: key, count: items.length };
          for (const [resultKey, { field, fn }] of Object.entries(aggregations)) {
            const values = items.map(i => i[field]).filter(v => v !== undefined && v !== null);
            if (values.length > 0) {
              agg[resultKey] = fn(values);
            }
          }
          results.push(agg);
        }
        return results;
      });

    return pipeline;
  }
};

// ──────────────────────────────────────────────
// 5. 导出
// ──────────────────────────────────────────────

module.exports = {
  Pipeline,
  Stage,
  PipelineError,
  Transformers,
  Validators,
  PipelineFactory
};

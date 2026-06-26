/**
 * DataLoader - Batch processing utility to solve N+1 query problems
 * 
 * Reduces database/API calls from N+1 to 2 by batching and caching requests.
 * 
 * @example
 * const userLoader = new DataLoader(async (ids) => {
 *   const users = await db.query('SELECT * FROM users WHERE id IN (?)', [ids]);
 *   return ids.map(id => users.find(u => u.id === id));
 * });
 * 
 * // Concurrent loads are automatically batched
 * const [user1, user2, user3] = await Promise.all([
 *   userLoader.load(1),
 *   userLoader.load(2),
 *   userLoader.load(3)
 * ]);
 */

class DataLoader {
  /**
   * Create a DataLoader instance
   * @param {Function} batchLoadFn - Async function that takes array of keys and returns array of values
   * @param {Object} options - Configuration options
   * @param {number} options.maxBatchSize - Maximum keys per batch (default: 100)
   * @param {number} options.batchScheduleMs - Delay to collect batch in ms (default: 0)
   * @param {boolean} options.cache - Enable caching (default: true)
   * @param {Function} options.cacheKeyFn - Custom cache key function (default: JSON.stringify)
   */
  constructor(batchLoadFn, options = {}) {
    if (typeof batchLoadFn !== 'function') {
      throw new TypeError('DataLoader requires a batchLoadFn as first argument');
    }

    this._batchLoadFn = batchLoadFn;
    this._maxBatchSize = options.maxBatchSize || 100;
    this._batchScheduleMs = options.batchScheduleMs || 0;
    this._cache = options.cache !== false;
    this._cacheKeyFn = options.cacheKeyFn || ((key) => JSON.stringify(key));

    this._cacheMap = new Map();
    this._queue = [];
    this._scheduled = false;
  }

  /**
   * Load a single key
   * @param {any} key - The key to load
   * @returns {Promise<any>} Promise resolving to the value
   */
  async load(key) {
    if (!this._cache) {
      return this._enqueueAndDispatch(key);
    }

    const cacheKey = this._cacheKeyFn(key);
    if (this._cacheMap.has(cacheKey)) {
      return this._cacheMap.get(cacheKey);
    }

    const promise = this._enqueueAndDispatch(key);
    this._cacheMap.set(cacheKey, promise);
    return promise;
  }

  /**
   * Load multiple keys
   * @param {Array<any>} keys - Array of keys to load
   * @returns {Promise<Array<any>>} Promise resolving to array of values
   */
  async loadMany(keys) {
    return Promise.all(keys.map(key => this.load(key)));
  }

  /**
   * Prime the cache with a known value
   * @param {any} key - The key
   * @param {any} value - The value (or Promise)
   */
  prime(key, value) {
    if (!this._cache) return;
    
    const cacheKey = this._cacheKeyFn(key);
    const promise = value instanceof Promise ? value : Promise.resolve(value);
    this._cacheMap.set(cacheKey, promise);
  }

  /**
   * Clear cache for a specific key
   * @param {any} key - The key to clear
   */
  clear(key) {
    if (!this._cache) return;
    const cacheKey = this._cacheKeyFn(key);
    this._cacheMap.delete(cacheKey);
  }

  /**
   * Clear entire cache
   */
  clearAll() {
    this._cacheMap.clear();
  }

  /**
   * Internal: Enqueue a key and schedule dispatch
   * @private
   */
  _enqueueAndDispatch(key) {
    return new Promise((resolve, reject) => {
      this._queue.push({ key, resolve, reject });

      if (!this._scheduled) {
        this._scheduled = true;
        if (this._batchScheduleMs > 0) {
          setTimeout(() => this._dispatchBatch(), this._batchScheduleMs);
        } else {
          setImmediate(() => this._dispatchBatch());
        }
      }
    });
  }

  /**
   * Internal: Dispatch the current batch
   * @private
   */
  async _dispatchBatch() {
    const batch = this._queue.slice(0, this._maxBatchSize);
    this._queue = this._queue.slice(this._maxBatchSize);
    this._scheduled = this._queue.length > 0;

    if (this._queue.length > 0) {
      setImmediate(() => this._dispatchBatch());
    }

    try {
      const keys = batch.map(item => item.key);
      const values = await this._batchLoadFn(keys);

      if (!Array.isArray(values)) {
        throw new TypeError('batchLoadFn must return an array of values');
      }

      if (values.length !== keys.length) {
        throw new Error(
          `batchLoadFn must return same number of values as keys. Got ${values.length}, expected ${keys.length}`
        );
      }

      batch.forEach((item, index) => {
        item.resolve(values[index]);
      });
    } catch (error) {
      batch.forEach(item => item.reject(error));
    }
  }
}

module.exports = DataLoader;

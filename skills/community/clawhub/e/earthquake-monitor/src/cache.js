/**
 * Shared Cache Module (v1.1.0)
 * Performance optimization - shared cache between data sources
 */

class SharedCache {
  constructor() {
    this.cache = new Map();
    this.defaultTTL = 60000; // 1 minute default
  }

  /**
   * Get value from cache
   * @param {string} key - Cache key
   * @param {boolean} autoRefresh - Auto refresh if expired
   */
  get(key, autoRefresh = false) {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    const now = Date.now();
    if (now > entry.expiresAt) {
      this.cache.delete(key);
      if (autoRefresh && typeof entry.refresh === 'function') {
        // Return stale data but trigger refresh
        setImmediate(() => entry.refresh());
      }
      return null;
    }
    
    return entry.value;
  }

  /**
   * Set value in cache
   * @param {string} key - Cache key
   * @param {*} value - Value to cache
   * @param {number} ttl - Time to live in ms
   * @param {Function} refresh - Optional refresh function
   */
  set(key, value, ttl = this.defaultTTL, refresh = null) {
    this.cache.set(key, {
      value,
      expiresAt: Date.now() + ttl,
      refresh
    });
  }

  /**
   * Delete specific key
   */
  delete(key) {
    this.cache.delete(key);
  }

  /**
   * Clear all cache
   */
  clear() {
    this.cache.clear();
  }

  /**
   * Get cache stats
   */
  stats() {
    let valid = 0;
    let expired = 0;
    const now = Date.now();
    
    for (const entry of this.cache.values()) {
      if (now > entry.expiresAt) {
        expired++;
      } else {
        valid++;
      }
    }
    
    return {
      total: this.cache.size,
      valid,
      expired,
      hitRate: valid / Math.max(this.cache.size, 1)
    };
  }

  /**
   * Cleanup expired entries
   */
  cleanup() {
    const now = Date.now();
    let cleaned = 0;
    
    for (const [key, entry] of this.cache.entries()) {
      if (now > entry.expiresAt) {
        this.cache.delete(key);
        cleaned++;
      }
    }
    
    return cleaned;
  }
}

// Singleton instance
const sharedCache = new SharedCache();

// Auto cleanup every 5 minutes
setInterval(() => {
  const cleaned = sharedCache.cleanup();
  if (cleaned > 0) {
    console.log(`[Cache] Cleaned ${cleaned} expired entries`);
  }
}, 300000);

module.exports = { SharedCache, sharedCache };

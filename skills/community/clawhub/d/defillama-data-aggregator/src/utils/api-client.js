/**
 * API Client with caching, retry logic, and error handling
 */

const axios = require('axios');
const NodeCache = require('node-cache');
const https = require('https');

class ApiClient {
  constructor(config = {}) {
    this.cache = new NodeCache({
      stdTTL: config.defaultCacheDuration || 300,
      checkperiod: 60
    });
    this.timeout = config.timeout || 30000;
    this.maxRetries = config.maxRetries || 3;
    this.retryDelay = config.retryDelay || 1000;
    this.debug = config.debug || false;
    this.enableCache = config.enableCache !== false; // Default true

    // IP direct connection configuration
    this.useIpDirect = config.useIpDirect || false;
    this.ipBaseUrl = config.ipBaseUrl || null;
    this.hostHeader = config.hostHeader || null;
    this.rejectUnauthorized = config.rejectUnauthorized !== false; // Default true
  }

  /**
   * Make HTTP request with caching and retry logic
   */
  async request(options) {
    const cacheKey = this.getCacheKey(options);

    // Check cache first (if enabled)
    if (this.enableCache && !options.noCache && this.cache.has(cacheKey)) {
      this.log('Cache hit', cacheKey);
      return this.cache.get(cacheKey);
    }

    // Make request with retry logic
    try {
      const response = await this.makeRequest(options);

      // Cache the response (if enabled)
      if (this.enableCache && !options.noCache) {
        this.cache.set(cacheKey, response, options.cacheDuration);
      }

      return response;
    } catch (error) {
      throw this.handleError(error, options);
    }
  }

  /**
   * Make actual HTTP request with retries
   */
  async makeRequest(options, retryCount = 0) {
    try {
      // Build request configuration
      const requestConfig = {
        method: options.method || 'GET',
        headers: options.headers || {},
        params: options.params || {},
        data: options.data || {},
        timeout: this.timeout
      };

      // IP direct mode: replace URL and set Host header
      if (this.useIpDirect && this.ipBaseUrl && options.url) {
        // Replace baseUrl with IP direct address
        const originalUrl = new URL(options.url);
        const ipUrl = new URL(this.ipBaseUrl);

        // Keep original path and query params, only replace protocol and host
        const newUrl = `${this.ipBaseUrl}${originalUrl.pathname}${originalUrl.search}`;
        requestConfig.url = newUrl;

        // Set Host header (SNI)
        if (this.hostHeader) {
          requestConfig.headers['Host'] = this.hostHeader;
        }

        // For HTTPS IP direct, need to disable certificate verification (certificate is for domain)
        if (ipUrl.protocol === 'https:') {
          requestConfig.httpsAgent = new https.Agent({
            rejectUnauthorized: false
          });
        }

        this.log('IP Direct:', `${options.url} -> ${newUrl}`);
      } else {
        requestConfig.url = options.url;
      }

      const response = await axios(requestConfig);

      return response.data;
    } catch (error) {
      // Retry on network errors or 5xx errors
      if (retryCount < this.maxRetries && this.shouldRetry(error)) {
        this.log(`Retry ${retryCount + 1}/${this.maxRetries}`, options.url);
        await this.sleep(this.retryDelay * (retryCount + 1));
        return this.makeRequest(options, retryCount + 1);
      }

      throw error;
    }
  }

  /**
   * Determine if request should be retried
   */
  shouldRetry(error) {
    if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      return true;
    }

    if (error.response && error.response.status >= 500) {
      return true;
    }

    return false;
  }

  /**
   * Handle API errors
   */
  handleError(error, options) {
    if (error.response) {
      // API responded with error status
      const status = error.response.status;
      const message = error.response.data?.message || error.response.statusText;

      if (status === 401) {
        return new Error('Authentication failed: Invalid API key');
      } else if (status === 429) {
        return new Error('Rate limit exceeded: Too many requests');
      } else if (status === 404) {
        return new Error(`Resource not found: ${options.url}`);
      } else if (status >= 500) {
        return new Error(`Server error: ${status} ${message}`);
      } else {
        return new Error(`API error (${status}): ${message}`);
      }
    } else if (error.request) {
      // Request made but no response received
      return new Error('Network error: No response received from server');
    } else {
      // Error in setting up request
      return new Error(`Request error: ${error.message}`);
    }
  }

  /**
   * Generate cache key from request options
   */
  getCacheKey(options) {
    const key = {
      url: options.url,
      method: options.method || 'GET',
      params: options.params || {},
      data: options.data || {}
    };
    return JSON.stringify(key);
  }

  /**
   * Clear cache
   */
  clearCache(pattern = null) {
    if (pattern) {
      const keys = this.cache.keys();
      keys.forEach(key => {
        if (key.includes(pattern)) {
          this.cache.del(key);
        }
      });
    } else {
      this.cache.flushAll();
    }
  }

  /**
   * Get cache statistics
   */
  getCacheStats() {
    return this.cache.getStats();
  }

  /**
   * Sleep helper
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Debug logging
   */
  log(...args) {
    if (this.debug) {
      console.log('[ApiClient]', ...args);
    }
  }
}

module.exports = ApiClient;

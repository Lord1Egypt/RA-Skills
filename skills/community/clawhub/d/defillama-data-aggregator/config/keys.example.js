/**
 * API Keys Configuration - Example
 *
 * Copy this file to config/keys.js if you need local overrides.
 *
 * Note: DefiLlama does not require an API key for basic usage.
 * This configuration file is optional but provides customization options.
 */

module.exports = {
  // DefiLlama Configuration (No API key required for basic usage)
  defillama: {
    baseUrl: 'https://api.llama.fi'
  },

  // Global settings
  settings: {
    // Default cache duration in seconds
    defaultCacheDuration: 300,

    // Request timeout in milliseconds
    timeout: 30000,

    // Maximum retry attempts
    maxRetries: 3,

    // Retry delay in milliseconds
    retryDelay: 1000,

    // Enable debug logging
    debug: process.env.DEBUG === 'true'
  }
};

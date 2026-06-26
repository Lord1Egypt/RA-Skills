/**
 * 1Panel Skill
 * Comprehensive API client for 1Panel server management
 */

// Export client and config
export { OnePanelClient } from './client.js';
export type { OnePanelConfig } from './types/config.js';

// Export all API modules
export * from './api/index.js';

// Export all tools
export * from './tools/index.js';

// Version
export const VERSION = '1.0.0';

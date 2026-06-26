/**
 * Configuration management for cross-border-intel skill
 */
/**
 * Get the OpenClaw config path from environment or default
 */
export declare function getOpenclawConfigPath(): string;
/**
 * Get the OpenClaw state directory
 */
export declare function getOpenclawStateRoot(): string;
/**
 * Get the skill state directory
 */
export declare function getSkillStateDir(): string;
/**
 * Get the Intel API URL
 */
export declare function getIntelApiUrl(): string;
/**
 * Load gateway token from environment or OpenClaw config
 */
export declare function loadGatewayToken(): string;
/**
 * Get Intel API token (alias for gateway token)
 */
export declare function getIntelApiToken(): string;
/**
 * Get the database path
 */
export declare function getDbPath(): string;
/**
 * Ensure skill state directory exists
 */
export declare function ensureSkillStateDir(): string;
/**
 * Print runtime configuration summary (for debugging)
 */
export declare function printRuntimeSummary(): void;
import type { ConfigValue } from './types.js';
export type { ConfigValue };

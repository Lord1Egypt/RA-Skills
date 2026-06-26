/**
 * Configuration management for cross-border-intel skill
 */
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
// Default configuration values
const DEFAULT_CONFIG = {
    priceChangeThreshold: 5,
    bsrChangeThreshold: 30,
    tiktokViralPlays: 1000000,
    reportSummaryMode: 'openclaw',
};
/**
 * Get the OpenClaw config path from environment or default
 */
export function getOpenclawConfigPath() {
    return process.env.OPENCLAW_CONFIG_PATH ||
        process.env.OPENCLAW_CONFIG ||
        join(homedir(), '.openclaw', 'openclaw.json');
}
/**
 * Get the OpenClaw state directory
 */
export function getOpenclawStateRoot() {
    const configPath = getOpenclawConfigPath();
    return join(configPath, '..');
}
/**
 * Get the skill state directory
 */
export function getSkillStateDir() {
    const stateRoot = process.env.OPENCLAW_STATE_DIR || getOpenclawStateRoot();
    return join(stateRoot, 'skills', 'cross-border-intel');
}
/**
 * Get the Intel API URL
 */
export function getIntelApiUrl() {
    return process.env.INTEL_API_URL || 'https://api.haixia.ai';
}
/**
 * Load gateway token from environment or OpenClaw config
 */
export function loadGatewayToken() {
    // Check environment first
    if (process.env.OPENCLAW_GATEWAY_TOKEN) {
        return process.env.OPENCLAW_GATEWAY_TOKEN;
    }
    // Try to read from OpenClaw config
    const configPath = getOpenclawConfigPath();
    if (!existsSync(configPath)) {
        throw new Error(`OpenClaw config not found: ${configPath}`);
    }
    try {
        const config = JSON.parse(readFileSync(configPath, 'utf-8'));
        const token = config.gateway?.auth?.token;
        if (!token) {
            throw new Error('Gateway token not found in OpenClaw config');
        }
        return token;
    }
    catch (error) {
        if (error.code === 'ENOENT') {
            throw new Error(`OpenClaw config not found: ${configPath}`);
        }
        throw error;
    }
}
/**
 * Get Intel API token (alias for gateway token)
 */
export function getIntelApiToken() {
    return loadGatewayToken();
}
/**
 * Get the database path
 */
export function getDbPath() {
    const stateDir = getSkillStateDir();
    return join(stateDir, 'local.sqlite3');
}
/**
 * Ensure skill state directory exists
 */
export function ensureSkillStateDir() {
    const dir = getSkillStateDir();
    if (!existsSync(dir)) {
        require('fs').mkdirSync(dir, { recursive: true });
    }
    return dir;
}
/**
 * Print runtime configuration summary (for debugging)
 */
export function printRuntimeSummary() {
    console.log({
        intelApiUrl: getIntelApiUrl(),
        openclawConfig: getOpenclawConfigPath(),
        openclawStateRoot: getOpenclawStateRoot(),
        skillStateDir: getSkillStateDir(),
        dbPath: getDbPath(),
    });
}

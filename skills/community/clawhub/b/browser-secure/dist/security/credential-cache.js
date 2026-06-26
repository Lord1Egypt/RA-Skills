import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { getSessionConfig } from '../config/loader.js';
const CACHE_DIR = path.join(os.homedir(), '.browser-secure', 'cache');
const CACHE_FILE = path.join(CACHE_DIR, 'credentials.cache');
const AES_ALGORITHM = 'aes-256-gcm';
// Get or derive encryption key from environment
function getEncryptionKey() {
    const envKey = process.env.BROWSER_SECURE_CACHE_KEY;
    if (envKey) {
        // Use provided key, hashed to 32 bytes
        return crypto.createHash('sha256').update(envKey).digest();
    }
    // Require environment variable for credential caching
    throw new Error('BROWSER_SECURE_CACHE_KEY must be set for credential caching');
}
let encryptionKey = null;
function getKey() {
    if (!encryptionKey) {
        encryptionKey = getEncryptionKey();
    }
    return encryptionKey;
}
function ensureCacheDir() {
    if (!fs.existsSync(CACHE_DIR)) {
        fs.mkdirSync(CACHE_DIR, { recursive: true, mode: 0o700 });
    }
}
function encryptData(data) {
    const key = getKey();
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(AES_ALGORITHM, key, iv);
    const encrypted = Buffer.concat([cipher.update(data, 'utf-8'), cipher.final()]);
    const authTag = cipher.getAuthTag();
    return { encrypted, authTag, iv };
}
function decryptData(encrypted, authTag, iv) {
    const key = getKey();
    const decipher = crypto.createDecipheriv(AES_ALGORITHM, key, iv);
    decipher.setAuthTag(authTag);
    return Buffer.concat([decipher.update(encrypted), decipher.final()]).toString('utf-8');
}
export async function cacheCredentials(site, credentials) {
    ensureCacheDir();
    const config = getSessionConfig();
    const cacheDurationMs = config.credentialCacheMinutes * 60 * 1000;
    const entry = {
        site,
        credentials,
        encrypted: true,
        expiresAt: Date.now() + cacheDurationMs
    };
    // Load existing cache
    const cache = loadCacheFile();
    // Remove existing entry for this site
    const existingIndex = cache.entries.findIndex(e => e.site === site);
    if (existingIndex >= 0) {
        cache.entries.splice(existingIndex, 1);
    }
    // Encrypt credentials
    const credsJson = JSON.stringify(credentials);
    const { encrypted, authTag, iv } = encryptData(credsJson);
    // Add new entry
    cache.entries.push({
        site,
        credentials: encrypted.toString('base64'),
        authTag: authTag.toString('base64'),
        iv: iv.toString('base64'),
        expiresAt: entry.expiresAt
    });
    // Clean up expired entries
    cleanupExpiredEntries(cache);
    // Write cache
    saveCacheFile(cache);
    // Set restrictive permissions
    try {
        fs.chmodSync(CACHE_FILE, 0o600);
    }
    catch {
        // Ignore permission errors
    }
}
export async function getCachedCredentials(site) {
    if (!fs.existsSync(CACHE_FILE)) {
        return null;
    }
    const cache = loadCacheFile();
    const entry = cache.entries.find(e => e.site === site);
    if (!entry) {
        return null;
    }
    // Check expiration
    if (Date.now() > entry.expiresAt) {
        // Remove expired entry
        const index = cache.entries.indexOf(entry);
        cache.entries.splice(index, 1);
        saveCacheFile(cache);
        return null;
    }
    try {
        // Decrypt credentials
        const encrypted = Buffer.from(entry.credentials, 'base64');
        const authTag = Buffer.from(entry.authTag, 'base64');
        const iv = Buffer.from(entry.iv, 'base64');
        const decrypted = decryptData(encrypted, authTag, iv);
        return JSON.parse(decrypted);
    }
    catch (e) {
        // Decryption failed (likely wrong key or corrupted data)
        const index = cache.entries.indexOf(entry);
        cache.entries.splice(index, 1);
        saveCacheFile(cache);
        return null;
    }
}
export function clearCredentialCache() {
    if (fs.existsSync(CACHE_FILE)) {
        fs.unlinkSync(CACHE_FILE);
    }
    // Also clear any in-memory key
    encryptionKey = null;
}
export function isCacheValid(site) {
    if (!fs.existsSync(CACHE_FILE)) {
        return false;
    }
    const cache = loadCacheFile();
    const entry = cache.entries.find(e => e.site === site);
    if (!entry) {
        return false;
    }
    return Date.now() <= entry.expiresAt;
}
function loadCacheFile() {
    if (!fs.existsSync(CACHE_FILE)) {
        return { version: 1, entries: [] };
    }
    try {
        const content = fs.readFileSync(CACHE_FILE, 'utf-8');
        const parsed = JSON.parse(content);
        if (parsed.version === 1 && Array.isArray(parsed.entries)) {
            return parsed;
        }
        return { version: 1, entries: [] };
    }
    catch {
        return { version: 1, entries: [] };
    }
}
function saveCacheFile(cache) {
    ensureCacheDir();
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf-8');
}
function cleanupExpiredEntries(cache) {
    const now = Date.now();
    cache.entries = cache.entries.filter(e => e.expiresAt > now);
}
// Initialize encryption key from environment if available
if (process.env.BROWSER_SECURE_CACHE_KEY) {
    encryptionKey = getEncryptionKey();
}

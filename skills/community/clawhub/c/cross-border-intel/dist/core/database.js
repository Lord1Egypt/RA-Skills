/**
 * Database operations using sql.js (pure JavaScript, no compilation needed)
 */
import initSqlJs from 'sql.js';
import { readFileSync, existsSync, writeFileSync } from 'fs';
import { getDbPath, ensureSkillStateDir } from './config.js';
// Global instances
let db = null;
let SQL = null;
let initPromise = null;
/**
 * Generate a unique local ID
 */
export function generateLocalId() {
    const timestamp = Date.now();
    const random1 = Math.floor(Math.random() * 10000);
    const random2 = Math.floor(Math.random() * 10000);
    return `${timestamp}-${random1}-${random2}`;
}
/**
 * Get current UTC time in ISO format
 */
export function nowUtc() {
    return new Date().toISOString();
}
/**
 * Get today's date in UTC (YYYY-MM-DD)
 */
export function todayUtc() {
    return new Date().toISOString().split('T')[0];
}
/**
 * Initialize sql.js and load database
 */
async function initSqlJsLib() {
    if (SQL)
        return;
    // Download from CDN (sql.js works in browser and Node.js)
    SQL = await initSqlJs();
}
/**
 * Load database from file or create new one
 */
function loadDatabase() {
    if (!SQL) {
        throw new Error('sql.js not initialized');
    }
    const dbPath = getDbPath();
    if (existsSync(dbPath)) {
        const buffer = readFileSync(dbPath);
        return new SQL.Database(buffer);
    }
    else {
        return new SQL.Database();
    }
}
/**
 * Save database to file
 */
function saveDatabase() {
    if (!db)
        return;
    const dbPath = getDbPath();
    const data = db.export();
    const buffer = Buffer.from(data);
    writeFileSync(dbPath, buffer);
}
/**
 * Initialize the database connection and create tables
 */
export async function initDatabase() {
    if (db) {
        return db;
    }
    if (initPromise) {
        return initPromise;
    }
    initPromise = (async () => {
        await initSqlJsLib();
        const dbPath = getDbPath();
        ensureSkillStateDir();
        db = loadDatabase();
        // Create tables
        createTables(db);
        // Initialize default config
        ensureDefaultConfig(db);
        // Save to disk
        saveDatabase();
        return db;
    })();
    return initPromise;
}
/**
 * Get database instance (must call initDatabase first)
 */
export function getDatabase() {
    if (!db) {
        throw new Error('Database not initialized. Call initDatabase() first.');
    }
    return db;
}
/**
 * Helper class for prepared statements (better-sqlite3 compatibility)
 */
export class PreparedStatement {
    sql;
    database;
    constructor(database, sql) {
        this.database = database;
        this.sql = sql;
    }
    /**
     * Execute statement and return all results
     */
    all(...params) {
        const boundSql = this.bindParams(this.sql, params);
        const results = this.database.exec(boundSql);
        if (results.length === 0) {
            return [];
        }
        const { columns, values } = results[0];
        return values.map((row) => {
            const obj = {};
            columns.forEach((col, i) => {
                obj[col] = row[i];
            });
            return obj;
        });
    }
    /**
     * Execute statement and return first result
     */
    get(...params) {
        const results = this.all(...params);
        return results[0];
    }
    /**
     * Execute statement and return changed rows (for INSERT/UPDATE/DELETE)
     */
    run(...params) {
        const boundSql = this.bindParams(this.sql, params);
        this.database.run(boundSql);
        saveDatabase();
        return { changes: 1, lastInsertRowid: 0 };
    }
    /**
     * Bind parameters to SQL (replaces ? with values)
     */
    bindParams(sql, params) {
        let result = sql;
        let paramIndex = 0;
        return result.replace(/\?/g, () => {
            if (paramIndex >= params.length) {
                throw new Error('Not enough parameters provided');
            }
            const param = params[paramIndex++];
            if (param === null || param === undefined) {
                return 'NULL';
            }
            if (typeof param === 'number') {
                return String(param);
            }
            if (typeof param === 'boolean') {
                return param ? '1' : '0';
            }
            // Escape strings
            return `'${String(param).replace(/'/g, "''")}'`;
        });
    }
}
/**
 * Prepare a statement (better-sqlite3 compatibility)
 */
export function prepare(sql) {
    const database = getDatabase();
    return new PreparedStatement(database, sql);
}
/**
 * Execute SQL and save to file
 */
export function runSql(sql) {
    const database = getDatabase();
    database.run(sql);
    saveDatabase();
}
/**
 * Execute SQL and return results
 */
export function runSqlQuery(sql) {
    const database = getDatabase();
    return database.exec(sql);
}
/**
 * Execute SQL and return single value
 */
export function runSqlValue(sql) {
    const results = runSqlQuery(sql);
    if (results.length === 0 || results[0].values.length === 0) {
        return '';
    }
    return String(results[0].values[0][0]);
}
/**
 * Create all database tables
 */
function createTables(database) {
    const tables = [
        `CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        );`,
        `CREATE TABLE IF NOT EXISTS watchlists (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL DEFAULT 'amazon',
            sourceType TEXT NOT NULL,
            value TEXT NOT NULL,
            domain TEXT NOT NULL DEFAULT 'com',
            isActive INTEGER NOT NULL DEFAULT 1,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        );`,
        `CREATE TABLE IF NOT EXISTS amazon_snapshots (
            id TEXT PRIMARY KEY,
            watchlistId TEXT NOT NULL,
            asin TEXT NOT NULL,
            title TEXT,
            price INTEGER,
            currency TEXT,
            bsr INTEGER,
            bsrCategory TEXT,
            reviewCount INTEGER,
            rating INTEGER,
            seller TEXT,
            imageUrl TEXT,
            snapshotDate TEXT NOT NULL,
            rawData TEXT,
            createdAt TEXT NOT NULL,
            FOREIGN KEY (watchlistId) REFERENCES watchlists(id)
        );`,
        `CREATE TABLE IF NOT EXISTS tiktok_hits (
            id TEXT PRIMARY KEY,
            watchlistId TEXT,
            keyword TEXT NOT NULL,
            videoId TEXT NOT NULL,
            authorName TEXT,
            description TEXT,
            playCount INTEGER,
            likeCount INTEGER,
            commentCount INTEGER,
            shareCount INTEGER,
            publishTime TEXT,
            rawData TEXT,
            createdAt TEXT NOT NULL,
            FOREIGN KEY (watchlistId) REFERENCES watchlists(id)
        );`,
        `CREATE TABLE IF NOT EXISTS alerts (
            id TEXT PRIMARY KEY,
            watchlistId TEXT,
            snapshotId TEXT,
            type TEXT NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            detail TEXT,
            pushedAt TEXT,
            createdAt TEXT NOT NULL,
            FOREIGN KEY (watchlistId) REFERENCES watchlists(id),
            FOREIGN KEY (snapshotId) REFERENCES amazon_snapshots(id)
        );`,
        `CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            reportType TEXT NOT NULL,
            content TEXT NOT NULL,
            periodStart TEXT,
            periodEnd TEXT,
            summarySource TEXT NOT NULL,
            pushedAt TEXT,
            createdAt TEXT NOT NULL
        );`,
        `CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            jobType TEXT NOT NULL,
            cadence TEXT,
            enabled INTEGER NOT NULL DEFAULT 1,
            lastRunAt TEXT,
            nextRunAt TEXT,
            lockToken TEXT,
            lockExpiresAt TEXT,
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        );`,
    ];
    for (const sql of tables) {
        try {
            database.run(sql);
        }
        catch {
            // Table already exists
        }
    }
    // Create indexes
    const indexes = [
        `CREATE INDEX IF NOT EXISTS idx_watchlists_platform_source_type ON watchlists(platform, sourceType);`,
        `CREATE INDEX IF NOT EXISTS idx_watchlists_active ON watchlists(isActive);`,
        `CREATE INDEX IF NOT EXISTS idx_amazon_snapshots_watchlist_id ON amazon_snapshots(watchlistId, createdAt DESC);`,
        `CREATE INDEX IF NOT EXISTS idx_tiktok_hits_watchlist_video ON tiktok_hits(watchlistId, videoId);`,
        `CREATE INDEX IF NOT EXISTS idx_tiktok_hits_created_at ON tiktok_hits(createdAt DESC);`,
        `CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(createdAt DESC);`,
        `CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(createdAt DESC);`,
        `CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs(jobType);`,
    ];
    for (const sql of indexes) {
        try {
            database.run(sql);
        }
        catch {
            // Index might already exist
        }
    }
}
/**
 * Get configuration value
 */
export function getConfigValue(key, defaultValue = '') {
    const results = runSqlQuery(`SELECT value FROM config WHERE key = '${key.replace(/'/g, "''")}' LIMIT 1`);
    if (results.length > 0 && results[0].values.length > 0) {
        return String(results[0].values[0][0]);
    }
    const defaults = {
        priceChangeThreshold: '5',
        bsrChangeThreshold: '30',
        tiktokViralPlays: '1000000',
        reportSummaryMode: 'openclaw',
    };
    return defaults[key] || defaultValue;
}
/**
 * Set configuration value
 */
export function setConfigValue(key, value) {
    const now = nowUtc();
    runSql(`
        INSERT INTO config (key, value, updatedAt)
        VALUES ('${key.replace(/'/g, "''")}', '${value.replace(/'/g, "''")}', '${now}')
        ON CONFLICT(key) DO UPDATE SET
            value = excluded.value,
            updatedAt = excluded.updatedAt
    `);
}
/**
 * Ensure default configuration values are set
 */
function ensureDefaultConfig(database) {
    const defaults = [
        ['priceChangeThreshold', '5'],
        ['bsrChangeThreshold', '30'],
        ['tiktokViralPlays', '1000000'],
        ['reportSummaryMode', 'openclaw'],
    ];
    const now = nowUtc();
    for (const [key, value] of defaults) {
        try {
            database.run(`
                INSERT INTO config (key, value, updatedAt)
                VALUES ('${key}', '${value}', '${now}')
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updatedAt = excluded.updatedAt
            `);
        }
        catch {
            // Config might already exist
        }
    }
}
/**
 * Close database connection and save
 */
export function closeDatabase() {
    if (db) {
        saveDatabase();
        db.close();
        db = null;
    }
    initPromise = null;
}
/**
 * Helper to escape SQL strings
 */
export function escapeSql(str) {
    return str.replace(/'/g, "''");
}

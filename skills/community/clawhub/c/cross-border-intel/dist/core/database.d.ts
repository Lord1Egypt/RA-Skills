/**
 * Database operations using sql.js (pure JavaScript, no compilation needed)
 */
import { Database } from 'sql.js';
/**
 * Generate a unique local ID
 */
export declare function generateLocalId(): string;
/**
 * Get current UTC time in ISO format
 */
export declare function nowUtc(): string;
/**
 * Get today's date in UTC (YYYY-MM-DD)
 */
export declare function todayUtc(): string;
/**
 * Initialize the database connection and create tables
 */
export declare function initDatabase(): Promise<Database>;
/**
 * Get database instance (must call initDatabase first)
 */
export declare function getDatabase(): Database;
/**
 * Helper class for prepared statements (better-sqlite3 compatibility)
 */
export declare class PreparedStatement {
    private sql;
    private database;
    constructor(database: Database, sql: string);
    /**
     * Execute statement and return all results
     */
    all(...params: unknown[]): Record<string, unknown>[];
    /**
     * Execute statement and return first result
     */
    get(...params: unknown[]): Record<string, unknown> | undefined;
    /**
     * Execute statement and return changed rows (for INSERT/UPDATE/DELETE)
     */
    run(...params: unknown[]): {
        changes: number;
        lastInsertRowid: number;
    };
    /**
     * Bind parameters to SQL (replaces ? with values)
     */
    private bindParams;
}
/**
 * Prepare a statement (better-sqlite3 compatibility)
 */
export declare function prepare(sql: string): PreparedStatement;
/**
 * Execute SQL and save to file
 */
export declare function runSql(sql: string): void;
/**
 * Execute SQL and return results
 */
export declare function runSqlQuery(sql: string): any[];
/**
 * Execute SQL and return single value
 */
export declare function runSqlValue(sql: string): string;
/**
 * Get configuration value
 */
export declare function getConfigValue(key: string, defaultValue?: string): string;
/**
 * Set configuration value
 */
export declare function setConfigValue(key: string, value: string): void;
/**
 * Close database connection and save
 */
export declare function closeDatabase(): void;
/**
 * Helper to escape SQL strings
 */
export declare function escapeSql(str: string): string;
export type { Database };

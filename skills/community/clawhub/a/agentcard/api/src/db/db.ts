import { appLogger } from "../utils/logger";
import { Pool, type PoolConfig, type QueryResultRow } from "pg";

let pool: Pool | null = null;

/**
 * Get or create the singleton Postgres pool.
 * Only call when REPO_MODE=postgres (i.e. DATABASE_URL is set).
 */
export function getPool(): Pool {
    if (!pool) {
        const databaseUrl = process.env.DATABASE_URL;
        if (!databaseUrl) {
            throw new Error(
                "DATABASE_URL is required when REPO_MODE=postgres"
            );
        }

        const config: PoolConfig = {
            connectionString: databaseUrl,
            max: 10,
            idleTimeoutMillis: 30_000,
            connectionTimeoutMillis: 5_000
        };

        // Disable SSL verification for local/testing (Supabase handles SSL)
        if (
            process.env.NODE_ENV === "development" ||
            process.env.NODE_ENV === "test"
        ) {
            config.ssl = databaseUrl.includes("localhost")
                ? false
                : { rejectUnauthorized: false };
        }

        pool = new Pool(config);

        pool.on("error", (err) => {
            appLogger.error({ err: err.message }, "[DB] Unexpected pool error:");
        });
    }

    return pool;
}

/**
 * Convenience query function.
 */
export async function query<T extends QueryResultRow = QueryResultRow>(
    text: string,
    params?: unknown[]
): Promise<T[]> {
    const result = await getPool().query<T>(text, params);
    return result.rows;
}

/**
 * Gracefully close the pool (for test cleanup / shutdown).
 */
export async function closePool(): Promise<void> {
    if (pool) {
        await pool.end();
        pool = null;
    }
}

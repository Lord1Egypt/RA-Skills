import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import { createClient } from 'redis';

interface EvaluateParams {
  action_type: string;
  justification: string;
  risk_level: number;
}

interface EvaluateResult {
  allowed: boolean;
  message: string;
  needs_civic?: boolean;
}

interface AuditReportParams {
  limit?: number;
}

type LedgerStatus = 'APPROVED' | 'BLOCKED' | 'THROTTLED' | 'NEEDS_CIVIC';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DB_FILE = path.join(__dirname, 'clawguard.db');

const redisUrl = process.env.REDIS_URL || 'redis://localhost:6373';
const redisClient = createClient({ url: redisUrl });
let redisReady = false;
let redisDisabled = false;
let redisInitPromise: Promise<void> | null = null;
let lastRedisErrorLoggedAt = 0;

const logRedisError = (prefix: string, err: unknown) => {
  const now = Date.now();
  if (now - lastRedisErrorLoggedAt < 1000) {
    return;
  }
  lastRedisErrorLoggedAt = now;
  const message = err instanceof Error ? err.message : String(err);
  console.error(`[ClawGuard][Redis] ${prefix}: ${message}`);
};

redisClient
  .on('ready', () => {
    redisReady = true;
    redisDisabled = false;
  })
  .on('end', () => {
    redisReady = false;
  })
  .on('error', (err) => {
    logRedisError('Client error', err);
  });

const ensureRedisReady = async (): Promise<boolean> => {
  if (redisDisabled) {
    return false;
  }
  if (redisReady) {
    return true;
  }
  if (!redisInitPromise) {
    redisInitPromise = redisClient
      .connect()
      .then(() => undefined)
      .catch((err) => {
        redisDisabled = true;
        throw err;
      });
  }
  try {
    await redisInitPromise;
    return redisReady;
  } catch (err) {
    logRedisError('Initial connection failed', err);
    return false;
  }
};

class ClawGuard {
  private dbPromise: Promise<Database> | null = null;

  private initDB(): Promise<Database> {
    if (!this.dbPromise) {
      this.dbPromise = open({ filename: DB_FILE, driver: sqlite3.Database }).then(async (db) => {
        await db.exec(`
          CREATE TABLE IF NOT EXISTS audit_ledger (
            id INTEGER PRIMARY KEY,
            action_type TEXT NOT NULL,
            justification TEXT NOT NULL,
            risk_level INTEGER NOT NULL,
            status TEXT NOT NULL,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        `);
        return db;
      });
    }
    return this.dbPromise;
  }

  private async logAction(params: EvaluateParams, status: LedgerStatus) {
    const db = await this.initDB();
    await db.run(
      'INSERT INTO audit_ledger (action_type, justification, risk_level, status) VALUES (?, ?, ?, ?)',
      [params.action_type, params.justification, params.risk_level, status]
    );
  }

  private async velocityTripped(actionType: string): Promise<boolean> {
    const redisAvailable = await ensureRedisReady();
    if (!redisAvailable) {
      return false;
    }

    const key = `velocity:${actionType}`;
    try {
      const count = await redisClient.incr(key);
      if (count === 1) {
        await redisClient.expire(key, 60);
      }
      return count > 5;
    } catch (err) {
      logRedisError('Velocity check failed', err);
      return false;
    }
  }

  async evaluateAction(params: EvaluateParams): Promise<EvaluateResult> {
    if (await this.velocityTripped(params.action_type)) {
      await this.logAction(params, 'THROTTLED');
      return {
        allowed: false,
        message: 'CIRCUIT BREAKER TRIPPED: Too many actions in 60s.'
      };
    }

    if (params.risk_level >= 5) {
      await this.logAction(params, 'NEEDS_CIVIC');
      return {
        allowed: false,
        needs_civic: true,
        message: 'CRITICAL RISK: Identity verification required via Civic.'
      };
    }

    if (params.risk_level >= 4) {
      await this.logAction(params, 'BLOCKED');
      return {
        allowed: false,
        message: 'Governance Violation: Risk too high.'
      };
    }

    await this.logAction(params, 'APPROVED');
    return {
      allowed: true,
      message: 'Action logged.'
    };
  }

  async getAuditReport(params: AuditReportParams) {
    const db = await this.initDB();
    const limit = params.limit ?? 5;
    return db.all('SELECT * FROM audit_ledger ORDER BY ts DESC LIMIT ?', limit);
  }
}

const guard = new ClawGuard();

export const tools = {
  evaluate_action: async ({ action_type, justification, risk_level }: EvaluateParams) => {
    if (!action_type || !justification || typeof risk_level !== 'number') {
      throw new Error('action_type, justification, and risk_level are required');
    }
    return guard.evaluateAction({ action_type, justification, risk_level });
  },
  get_audit_report: async ({ limit }: AuditReportParams = {}) => {
    return guard.getAuditReport({ limit });
  }
};

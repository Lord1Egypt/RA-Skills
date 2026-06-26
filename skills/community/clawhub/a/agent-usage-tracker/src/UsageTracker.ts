import Database from "better-sqlite3";

import {
  TimeSeriesPoint,
  UsageEventInput,
  UsageQuery,
  UsageRecord,
  UsageSummary,
  UsageTrackerOptions
} from "./types.js";

interface UsageRow {
  id: number;
  session_id: string;
  model: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  input_cost_usd: number;
  output_cost_usd: number;
  total_cost_usd: number;
  timestamp: string;
  metadata_json: string | null;
}

export class UsageTracker {
  private readonly db: Database.Database;
  private readonly costCalculator?: UsageTrackerOptions["costCalculator"];

  constructor(options: UsageTrackerOptions = {}) {
    this.db = new Database(options.dbPath ?? "usage-tracker.db");
    this.costCalculator = options.costCalculator;
    this.initialize();
  }

  private initialize(): void {
    this.db.pragma("journal_mode = WAL");
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS usage_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        model TEXT NOT NULL,
        prompt_tokens INTEGER NOT NULL,
        completion_tokens INTEGER NOT NULL,
        total_tokens INTEGER NOT NULL,
        input_cost_usd REAL NOT NULL,
        output_cost_usd REAL NOT NULL,
        total_cost_usd REAL NOT NULL,
        timestamp TEXT NOT NULL,
        metadata_json TEXT
      );

      CREATE INDEX IF NOT EXISTS idx_usage_records_timestamp
        ON usage_records(timestamp);
      CREATE INDEX IF NOT EXISTS idx_usage_records_session_id
        ON usage_records(session_id);
      CREATE INDEX IF NOT EXISTS idx_usage_records_model
        ON usage_records(model);
    `);
  }

  async recordUsage(input: UsageEventInput): Promise<UsageRecord> {
    this.validateUsage(input);

    const timestamp = input.timestamp ?? new Date().toISOString();
    const totalTokens = input.promptTokens + input.completionTokens;
    const costs = this.costCalculator?.calculateCost(
      input.model,
      input.promptTokens,
      input.completionTokens
    ) ?? {
      inputCostUsd: 0,
      outputCostUsd: 0,
      totalCostUsd: 0
    };

    const statement = this.db.prepare(`
      INSERT INTO usage_records (
        session_id,
        model,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        input_cost_usd,
        output_cost_usd,
        total_cost_usd,
        timestamp,
        metadata_json
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    const result = statement.run(
      input.sessionId,
      input.model,
      input.promptTokens,
      input.completionTokens,
      totalTokens,
      costs.inputCostUsd,
      costs.outputCostUsd,
      costs.totalCostUsd,
      timestamp,
      input.metadata ? JSON.stringify(input.metadata) : null
    );

    return {
      id: Number(result.lastInsertRowid),
      sessionId: input.sessionId,
      model: input.model,
      promptTokens: input.promptTokens,
      completionTokens: input.completionTokens,
      totalTokens,
      inputCostUsd: costs.inputCostUsd,
      outputCostUsd: costs.outputCostUsd,
      totalCostUsd: costs.totalCostUsd,
      timestamp,
      metadata: input.metadata
    };
  }

  async listUsage(query: UsageQuery = {}): Promise<UsageRecord[]> {
    const { whereClause, parameters } = this.buildWhereClause(query);
    const statement = this.db.prepare(`
      SELECT *
      FROM usage_records
      ${whereClause}
      ORDER BY timestamp ASC, id ASC
    `);

    const rows = statement.all(...parameters) as UsageRow[];
    return rows.map((row) => this.mapRow(row));
  }

  async getUsageSummary(query: UsageQuery = {}): Promise<UsageSummary> {
    const { whereClause, parameters } = this.buildWhereClause(query);

    const totals = this.db.prepare(`
      SELECT
        COUNT(*) AS totalRequests,
        COALESCE(SUM(prompt_tokens), 0) AS promptTokens,
        COALESCE(SUM(completion_tokens), 0) AS completionTokens,
        COALESCE(SUM(total_tokens), 0) AS totalTokens,
        COALESCE(SUM(total_cost_usd), 0) AS totalCostUsd
      FROM usage_records
      ${whereClause}
    `).get(...parameters) as {
      totalRequests: number;
      promptTokens: number;
      completionTokens: number;
      totalTokens: number;
      totalCostUsd: number;
    };

    const byModel = this.db.prepare(`
      SELECT
        model,
        COUNT(*) AS requests,
        COALESCE(SUM(prompt_tokens), 0) AS promptTokens,
        COALESCE(SUM(completion_tokens), 0) AS completionTokens,
        COALESCE(SUM(total_tokens), 0) AS totalTokens,
        COALESCE(SUM(total_cost_usd), 0) AS totalCostUsd
      FROM usage_records
      ${whereClause}
      GROUP BY model
      ORDER BY totalCostUsd DESC, model ASC
    `).all(...parameters) as UsageSummary["byModel"];

    const bySession = this.db.prepare(`
      SELECT
        session_id AS sessionId,
        COUNT(*) AS requests,
        COALESCE(SUM(prompt_tokens), 0) AS promptTokens,
        COALESCE(SUM(completion_tokens), 0) AS completionTokens,
        COALESCE(SUM(total_tokens), 0) AS totalTokens,
        COALESCE(SUM(total_cost_usd), 0) AS totalCostUsd
      FROM usage_records
      ${whereClause}
      GROUP BY session_id
      ORDER BY totalCostUsd DESC, sessionId ASC
    `).all(...parameters) as UsageSummary["bySession"];

    return {
      totalRequests: totals.totalRequests,
      promptTokens: totals.promptTokens,
      completionTokens: totals.completionTokens,
      totalTokens: totals.totalTokens,
      totalCostUsd: totals.totalCostUsd,
      byModel,
      bySession
    };
  }

  async getTimeSeries(query: UsageQuery = {}): Promise<TimeSeriesPoint[]> {
    const { whereClause, parameters } = this.buildWhereClause(query);
    const rows = this.db.prepare(`
      SELECT
        substr(timestamp, 1, 10) AS bucket,
        COUNT(*) AS requests,
        COALESCE(SUM(prompt_tokens), 0) AS promptTokens,
        COALESCE(SUM(completion_tokens), 0) AS completionTokens,
        COALESCE(SUM(total_tokens), 0) AS totalTokens,
        COALESCE(SUM(total_cost_usd), 0) AS totalCostUsd
      FROM usage_records
      ${whereClause}
      GROUP BY bucket
      ORDER BY bucket ASC
    `).all(...parameters) as TimeSeriesPoint[];

    return rows;
  }

  close(): void {
    this.db.close();
  }

  getDatabase(): Database.Database {
    return this.db;
  }

  private buildWhereClause(query: UsageQuery) {
    const clauses: string[] = [];
    const parameters: Array<string> = [];

    if (query.sessionId) {
      clauses.push("session_id = ?");
      parameters.push(query.sessionId);
    }

    if (query.model) {
      clauses.push("model = ?");
      parameters.push(query.model);
    }

    if (query.startTime) {
      clauses.push("timestamp >= ?");
      parameters.push(query.startTime);
    }

    if (query.endTime) {
      clauses.push("timestamp <= ?");
      parameters.push(query.endTime);
    }

    return {
      whereClause: clauses.length > 0 ? `WHERE ${clauses.join(" AND ")}` : "",
      parameters
    };
  }

  private mapRow(row: UsageRow): UsageRecord {
    return {
      id: row.id,
      sessionId: row.session_id,
      model: row.model,
      promptTokens: row.prompt_tokens,
      completionTokens: row.completion_tokens,
      totalTokens: row.total_tokens,
      inputCostUsd: row.input_cost_usd,
      outputCostUsd: row.output_cost_usd,
      totalCostUsd: row.total_cost_usd,
      timestamp: row.timestamp,
      metadata: row.metadata_json ? JSON.parse(row.metadata_json) : undefined
    };
  }

  private validateUsage(input: UsageEventInput): void {
    if (!input.sessionId.trim()) {
      throw new Error("sessionId is required.");
    }

    if (!input.model.trim()) {
      throw new Error("model is required.");
    }

    if (input.promptTokens < 0 || input.completionTokens < 0) {
      throw new Error("Token counts must be non-negative.");
    }
  }
}

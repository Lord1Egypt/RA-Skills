import { BudgetEvaluation, BudgetPolicy, StoredBudgetPolicy } from "./types.js";
import { UsageTracker } from "./UsageTracker.js";

export class BudgetManager {
  constructor(private readonly usageTracker: UsageTracker) {
    this.initialize();
  }

  private initialize(): void {
    this.usageTracker.getDatabase().exec(`
      CREATE TABLE IF NOT EXISTS budget_policies (
        name TEXT PRIMARY KEY,
        limit_usd REAL NOT NULL,
        warning_threshold REAL NOT NULL,
        session_id TEXT,
        model TEXT,
        start_time TEXT,
        end_time TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );
    `);
  }

  async setBudget(policy: BudgetPolicy): Promise<StoredBudgetPolicy> {
    this.validatePolicy(policy);

    const now = new Date().toISOString();
    const existing = await this.getBudget(policy.name);
    const createdAt = existing?.createdAt ?? now;
    const warningThreshold = policy.warningThreshold ?? 0.8;

    this.usageTracker.getDatabase().prepare(`
      INSERT INTO budget_policies (
        name,
        limit_usd,
        warning_threshold,
        session_id,
        model,
        start_time,
        end_time,
        created_at,
        updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(name) DO UPDATE SET
        limit_usd = excluded.limit_usd,
        warning_threshold = excluded.warning_threshold,
        session_id = excluded.session_id,
        model = excluded.model,
        start_time = excluded.start_time,
        end_time = excluded.end_time,
        updated_at = excluded.updated_at
    `).run(
      policy.name,
      policy.limitUsd,
      warningThreshold,
      policy.sessionId ?? null,
      policy.model ?? null,
      policy.startTime ?? null,
      policy.endTime ?? null,
      createdAt,
      now
    );

    return {
      ...policy,
      warningThreshold,
      createdAt,
      updatedAt: now
    };
  }

  async getBudget(name: string): Promise<StoredBudgetPolicy | null> {
    const row = this.usageTracker.getDatabase().prepare(`
      SELECT
        name,
        limit_usd AS limitUsd,
        warning_threshold AS warningThreshold,
        session_id AS sessionId,
        model,
        start_time AS startTime,
        end_time AS endTime,
        created_at AS createdAt,
        updated_at AS updatedAt
      FROM budget_policies
      WHERE name = ?
    `).get(name) as StoredBudgetPolicy | undefined;

    return row ?? null;
  }

  async listBudgets(): Promise<StoredBudgetPolicy[]> {
    return this.usageTracker.getDatabase().prepare(`
      SELECT
        name,
        limit_usd AS limitUsd,
        warning_threshold AS warningThreshold,
        session_id AS sessionId,
        model,
        start_time AS startTime,
        end_time AS endTime,
        created_at AS createdAt,
        updated_at AS updatedAt
      FROM budget_policies
      ORDER BY name ASC
    `).all() as StoredBudgetPolicy[];
  }

  async evaluateBudget(policyOrName: BudgetPolicy | string): Promise<BudgetEvaluation> {
    const policy = typeof policyOrName === "string"
      ? await this.getBudgetOrThrow(policyOrName)
      : policyOrName;
    this.validatePolicy(policy);

    const warningThreshold = policy.warningThreshold ?? 0.8;

    const summary = await this.usageTracker.getUsageSummary({
      sessionId: policy.sessionId,
      model: policy.model,
      startTime: policy.startTime,
      endTime: policy.endTime
    });

    const spentUsd = summary.totalCostUsd;
    const remainingUsd = Math.max(policy.limitUsd - spentUsd, 0);
    const usageRatio = spentUsd / policy.limitUsd;

    let status: BudgetEvaluation["status"] = "ok";
    if (usageRatio >= 1) {
      status = "exceeded";
    } else if (usageRatio >= warningThreshold) {
      status = "warning";
    }

    return {
      budgetName: policy.name,
      limitUsd: policy.limitUsd,
      spentUsd,
      remainingUsd,
      usageRatio,
      status
    };
  }

  private async getBudgetOrThrow(name: string): Promise<StoredBudgetPolicy> {
    const policy = await this.getBudget(name);
    if (!policy) {
      throw new Error(`Budget policy not found: ${name}`);
    }
    return policy;
  }

  private validatePolicy(policy: BudgetPolicy): void {
    if (!policy.name.trim()) {
      throw new Error("Budget name is required.");
    }

    if (policy.limitUsd <= 0) {
      throw new Error("Budget limitUsd must be greater than zero.");
    }

    const warningThreshold = policy.warningThreshold ?? 0.8;
    if (warningThreshold <= 0 || warningThreshold > 1) {
      throw new Error("warningThreshold must be within (0, 1].");
    }
  }
}

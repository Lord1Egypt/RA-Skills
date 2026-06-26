import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { randomUUID } from "node:crypto";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import * as sqliteVec from "sqlite-vec";
import type {
  AgentDecisionAudit,
  AssetChangeEvent,
  AssetCard,
  AssetState,
  CheckLifecycleData,
  ExecutionLog,
  LibraryOverview,
  ListLibrariesData,
  LifecycleRunData,
  MergedAsset,
  PackagePlan,
  PackageRunData,
  PipelineRun,
  PipelineRunCounts,
  PipelineRunData,
  PipelineStep,
  ParsedFile,
  QueryAssetsData,
  ReindexLibrarySearchData,
  ReviewQueueData,
  ReviewStatus
} from "@caixu/contracts";
import {
  buildAgentTagsText,
  buildAssetSearchText,
  deriveReusableScenariosFromAgentTags,
  sanitizeAgentTags
} from "@caixu/contracts";

type AssetQuery = {
  library_id: string;
  material_types?: string[];
  keyword?: string;
  reusable_scenario?: string;
  semantic_query?: string;
  tag_filters_any?: string[];
  tag_filters_all?: string[];
  validity_statuses?: string[];
  asset_states?: AssetState[];
  review_statuses?: ReviewStatus[];
  limit?: number;
};

type LibraryRecord = {
  library_id: string;
  owner_hint: string | null;
  created_at: string;
  updated_at: string;
};

function nowIso(): string {
  return new Date().toISOString();
}

function parseJson<T>(value: string): T {
  return JSON.parse(value) as T;
}

function normalizeStoredAssetCard(
  value: AssetCard &
    Partial<Pick<AssetCard, "asset_state" | "review_status" | "last_verified_at">>
): AssetCard {
  const agentTags = sanitizeAgentTags(value);
  return {
    ...value,
    agent_tags: agentTags,
    reusable_scenarios: deriveReusableScenariosFromAgentTags(agentTags),
    asset_state: value.asset_state ?? "active",
    review_status: value.review_status ?? "auto",
    last_verified_at: value.last_verified_at ?? null
  };
}

export class CaixuStorage {
  readonly db: DatabaseSync;
  readonly vectorSearchEnabled: boolean;

  constructor(dbPath: string) {
    mkdirSync(dirname(dbPath), { recursive: true });
    this.db = new DatabaseSync(dbPath, { allowExtension: true });
    this.vectorSearchEnabled = this.loadSqliteVecExtension();
    this.db.exec("PRAGMA journal_mode = WAL");
    this.db.exec("PRAGMA foreign_keys = ON");
    this.ensureSchema();
    this.ensureAssetFieldNullability();
    this.ensureAssetMaintenanceFields();
    this.ensureSearchSchema();
  }

  close(): void {
    this.db.close();
  }

  loadSqliteVecExtension(): boolean {
    try {
      sqliteVec.load(this.db);
      return true;
    } catch {
      return false;
    }
  }

  ensureSchema(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS libraries (
        library_id TEXT PRIMARY KEY,
        owner_hint TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS files (
        file_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        mime_type TEXT NOT NULL,
        parse_status TEXT NOT NULL,
        extracted_text TEXT,
        extracted_summary TEXT,
        provider TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS assets (
        asset_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        material_type TEXT NOT NULL,
        title TEXT NOT NULL,
        holder_name TEXT,
        issuer_name TEXT,
        issue_date TEXT,
        expiry_date TEXT,
        validity_status TEXT NOT NULL,
        normalized_summary TEXT NOT NULL,
        asset_state TEXT NOT NULL DEFAULT 'active',
        review_status TEXT NOT NULL DEFAULT 'auto',
        last_verified_at TEXT,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS merged_assets (
        merged_asset_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        canonical_asset_id TEXT NOT NULL,
        selected_asset_id TEXT NOT NULL,
        status TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS lifecycle_runs (
        run_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        goal TEXT NOT NULL,
        as_of_date TEXT NOT NULL,
        window_days INTEGER NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS package_runs (
        package_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        target_goal TEXT NOT NULL,
        package_name TEXT NOT NULL,
        submission_profile TEXT NOT NULL,
        output_dir TEXT,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS execution_logs (
        execution_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        package_id TEXT NOT NULL,
        submission_profile TEXT NOT NULL,
        status TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS agent_decision_audits (
        decision_id TEXT PRIMARY KEY,
        stage TEXT NOT NULL,
        run_ref_type TEXT NOT NULL,
        run_ref_id TEXT NOT NULL,
        library_id TEXT NOT NULL,
        goal TEXT NOT NULL,
        profile_id TEXT NOT NULL,
        model TEXT NOT NULL,
        validation_status TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS pipeline_runs (
        run_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        run_type TEXT NOT NULL,
        status TEXT NOT NULL,
        goal TEXT,
        input_root TEXT,
        latest_stage TEXT NOT NULL,
        counts_json TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS pipeline_steps (
        step_id TEXT PRIMARY KEY,
        run_id TEXT NOT NULL,
        stage TEXT NOT NULL,
        status TEXT NOT NULL,
        tool_name TEXT,
        message TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS asset_change_events (
        event_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        asset_id TEXT NOT NULL,
        action TEXT NOT NULL,
        changed_fields_json TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS idx_files_library_id ON files(library_id);
      CREATE INDEX IF NOT EXISTS idx_assets_library_id ON assets(library_id);
      CREATE INDEX IF NOT EXISTS idx_merged_assets_library_id ON merged_assets(library_id);
      CREATE INDEX IF NOT EXISTS idx_lifecycle_runs_library_id ON lifecycle_runs(library_id);
      CREATE INDEX IF NOT EXISTS idx_package_runs_library_id ON package_runs(library_id);
      CREATE INDEX IF NOT EXISTS idx_execution_logs_library_id ON execution_logs(library_id);
      CREATE INDEX IF NOT EXISTS idx_agent_decision_audits_library_id ON agent_decision_audits(library_id);
      CREATE INDEX IF NOT EXISTS idx_agent_decision_audits_run_ref ON agent_decision_audits(run_ref_type, run_ref_id);
      CREATE INDEX IF NOT EXISTS idx_pipeline_runs_library_id ON pipeline_runs(library_id);
      CREATE INDEX IF NOT EXISTS idx_pipeline_steps_run_id ON pipeline_steps(run_id, created_at);
      CREATE INDEX IF NOT EXISTS idx_asset_change_events_library_id ON asset_change_events(library_id, created_at);
    `);
  }

  ensureSearchSchema(): void {
    this.db.exec(`
      CREATE VIRTUAL TABLE IF NOT EXISTS asset_search_fts USING fts5(
        asset_id UNINDEXED,
        library_id UNINDEXED,
        title,
        normalized_summary,
        agent_tags_text,
        search_text,
        tokenize='trigram'
      );

      CREATE TABLE IF NOT EXISTS asset_embedding_meta (
        vec_rowid INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id TEXT NOT NULL UNIQUE,
        library_id TEXT NOT NULL,
        search_text TEXT NOT NULL,
        agent_tags_text TEXT NOT NULL,
        tag_blob TEXT NOT NULL,
        model TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS idx_asset_embedding_meta_library_id
      ON asset_embedding_meta(library_id, updated_at);
    `);

    if (this.vectorSearchEnabled) {
      this.db.exec(`
        CREATE VIRTUAL TABLE IF NOT EXISTS asset_embedding_vec USING vec0(
          embedding float[384]
        );
      `);
    }
  }

  ensureAssetFieldNullability(): void {
    const columns = this.db
      .prepare("PRAGMA table_info(assets)")
      .all() as Array<{ name: string; notnull: number }>;

    const holderColumn = columns.find((column) => column.name === "holder_name");
    const issuerColumn = columns.find((column) => column.name === "issuer_name");

    if (holderColumn?.notnull !== 1 && issuerColumn?.notnull !== 1) {
      return;
    }

    this.db.exec(`
      ALTER TABLE assets RENAME TO assets_legacy_nullable_migration;

      CREATE TABLE assets (
        asset_id TEXT PRIMARY KEY,
        library_id TEXT NOT NULL,
        material_type TEXT NOT NULL,
        title TEXT NOT NULL,
        holder_name TEXT,
        issuer_name TEXT,
        issue_date TEXT,
        expiry_date TEXT,
        validity_status TEXT NOT NULL,
        normalized_summary TEXT NOT NULL,
        asset_state TEXT NOT NULL DEFAULT 'active',
        review_status TEXT NOT NULL DEFAULT 'auto',
        last_verified_at TEXT,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      INSERT INTO assets (
        asset_id, library_id, material_type, title, holder_name, issuer_name,
        issue_date, expiry_date, validity_status, normalized_summary, asset_state,
        review_status, last_verified_at, payload_json,
        created_at, updated_at
      )
      SELECT
        asset_id, library_id, material_type, title, holder_name, issuer_name,
        issue_date, expiry_date, validity_status, normalized_summary, 'active',
        'auto', NULL, payload_json,
        created_at, updated_at
      FROM assets_legacy_nullable_migration;

      DROP TABLE assets_legacy_nullable_migration;

      CREATE INDEX IF NOT EXISTS idx_assets_library_id ON assets(library_id);
    `);
  }

  ensureAssetMaintenanceFields(): void {
    const columns = this.db
      .prepare("PRAGMA table_info(assets)")
      .all() as Array<{ name: string }>;
    const names = new Set(columns.map((column) => column.name));

    if (!names.has("asset_state")) {
      this.db.exec("ALTER TABLE assets ADD COLUMN asset_state TEXT NOT NULL DEFAULT 'active'");
    }
    if (!names.has("review_status")) {
      this.db.exec("ALTER TABLE assets ADD COLUMN review_status TEXT NOT NULL DEFAULT 'auto'");
    }
    if (!names.has("last_verified_at")) {
      this.db.exec("ALTER TABLE assets ADD COLUMN last_verified_at TEXT");
    }

    this.db.exec(
      "CREATE INDEX IF NOT EXISTS idx_assets_library_state ON assets(library_id, asset_state, review_status)"
    );
  }

  writeAgentDecisionAudit(
    audit: AgentDecisionAudit,
    runRef: { type: "asset_library_build" | "lifecycle_run" | "package_run"; id: string }
  ): AgentDecisionAudit {
    const persistedAudit: AgentDecisionAudit = {
      ...audit,
      run_ref_type: runRef.type,
      run_ref_id: runRef.id
    };

    this.db
      .prepare(
        `INSERT OR REPLACE INTO agent_decision_audits (
          decision_id, stage, run_ref_type, run_ref_id, library_id, goal,
          profile_id, model, validation_status, payload_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        persistedAudit.decision_id,
        persistedAudit.stage,
        runRef.type,
        runRef.id,
        persistedAudit.library_id,
        persistedAudit.goal,
        persistedAudit.profile_id,
        persistedAudit.model,
        persistedAudit.validation_status,
        JSON.stringify(persistedAudit),
        persistedAudit.created_at
      );

    return persistedAudit;
  }

  getLatestAgentDecisionAudit(
    runRef: { type: "asset_library_build" | "lifecycle_run" | "package_run"; id: string }
  ): AgentDecisionAudit | null {
    const row = this.db
      .prepare(
        `SELECT payload_json
         FROM agent_decision_audits
         WHERE run_ref_type = ? AND run_ref_id = ?
         ORDER BY created_at DESC
         LIMIT 1`
      )
      .get(runRef.type, runRef.id) as { payload_json: string } | undefined;

    return row ? parseJson<AgentDecisionAudit>(row.payload_json) : null;
  }

  createPipelineRun(input: {
    runId?: string;
    libraryId: string;
    runType: "ingest" | "build_asset_library";
    goal?: string | null;
    inputRoot?: string | null;
    latestStage?: string;
  }): PipelineRun {
    const createdAt = nowIso();
    const run: PipelineRun = {
      run_id: input.runId ?? `run_${randomUUID().replaceAll("-", "").slice(0, 12)}`,
      library_id: input.libraryId,
      run_type: input.runType,
      status: "running",
      goal: input.goal ?? null,
      input_root: input.inputRoot ?? null,
      counts: {
        parsed: 0,
        failed: 0,
        warnings: 0,
        skipped: 0,
        assets: 0,
        merged: 0
      },
      latest_stage: input.latestStage ?? "created",
      created_at: createdAt,
      updated_at: createdAt
    };

    this.db
      .prepare(
        `INSERT OR REPLACE INTO pipeline_runs (
          run_id, library_id, run_type, status, goal, input_root, latest_stage,
          counts_json, payload_json, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        run.run_id,
        run.library_id,
        run.run_type,
        run.status,
        run.goal,
        run.input_root,
        run.latest_stage,
        JSON.stringify(run.counts),
        JSON.stringify(run),
        run.created_at,
        run.updated_at
      );

    return run;
  }

  appendPipelineStep(input: {
    runId: string;
    stage: string;
    status: "running" | "completed" | "partial" | "failed" | "skipped";
    toolName?: string | null;
    message: string;
    payload: unknown;
  }): PipelineStep {
    const step: PipelineStep = {
      step_id: `step_${randomUUID().replaceAll("-", "").slice(0, 12)}`,
      run_id: input.runId,
      stage: input.stage,
      status: input.status,
      tool_name: input.toolName ?? null,
      message: input.message,
      payload_json: input.payload,
      created_at: nowIso()
    };

    this.db
      .prepare(
        `INSERT INTO pipeline_steps (
          step_id, run_id, stage, status, tool_name, message, payload_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        step.step_id,
        step.run_id,
        step.stage,
        step.status,
        step.tool_name,
        step.message,
        JSON.stringify(step.payload_json),
        step.created_at
      );

    this.db
      .prepare(
        `UPDATE pipeline_runs
         SET latest_stage = ?, updated_at = ?, payload_json = json_set(payload_json, '$.latest_stage', ?, '$.updated_at', ?)
         WHERE run_id = ?`
      )
      .run(step.stage, step.created_at, step.stage, step.created_at, input.runId);

    return step;
  }

  getPipelineRun(runId: string, stepLimit = 50): PipelineRunData | null {
    const runRow = this.db
      .prepare("SELECT payload_json FROM pipeline_runs WHERE run_id = ?")
      .get(runId) as { payload_json: string } | undefined;

    if (!runRow) {
      return null;
    }

    const stepRows = this.db
      .prepare(
        `SELECT payload_json FROM pipeline_steps
         WHERE run_id = ?
         ORDER BY created_at DESC
         LIMIT ?`
      )
      .all(runId, stepLimit) as Array<{ payload_json: string }>;

    return {
      pipeline_run: parseJson<PipelineRun>(runRow.payload_json),
      steps: stepRows
        .map((row) => parseJson<PipelineStep>(row.payload_json))
        .reverse()
    };
  }

  completePipelineRun(input: {
    runId: string;
    status: "completed" | "partial" | "failed";
    latestStage: string;
    counts: PipelineRunCounts;
  }): PipelineRunData | null {
    const existing = this.getPipelineRun(input.runId, 50);
    if (!existing?.pipeline_run) {
      return null;
    }

    const updatedRun: PipelineRun = {
      ...existing.pipeline_run,
      status: input.status,
      latest_stage: input.latestStage,
      counts: input.counts,
      updated_at: nowIso()
    };

    this.db
      .prepare(
        `UPDATE pipeline_runs
         SET status = ?, latest_stage = ?, counts_json = ?, payload_json = ?, updated_at = ?
         WHERE run_id = ?`
      )
      .run(
        updatedRun.status,
        updatedRun.latest_stage,
        JSON.stringify(updatedRun.counts),
        JSON.stringify(updatedRun),
        updatedRun.updated_at,
        input.runId
      );

    return this.getPipelineRun(input.runId, 50);
  }

  createOrLoadLibrary(libraryId?: string, ownerHint?: string): LibraryRecord {
    const existing = libraryId
      ? this.db
          .prepare("SELECT * FROM libraries WHERE library_id = ?")
          .get(libraryId) as LibraryRecord | undefined
      : undefined;

    if (existing) {
      return existing;
    }

    const createdAt = nowIso();
    const nextId =
      libraryId ?? `lib_${ownerHint?.replace(/\W+/g, "_").toLowerCase() ?? "default"}_${randomUUID().slice(0, 12)}`;

    this.db
      .prepare(
        "INSERT INTO libraries (library_id, owner_hint, created_at, updated_at) VALUES (?, ?, ?, ?)"
      )
      .run(nextId, ownerHint ?? null, createdAt, createdAt);

    return {
      library_id: nextId,
      owner_hint: ownerHint ?? null,
      created_at: createdAt,
      updated_at: createdAt
    };
  }

  listLibraries(): ListLibrariesData {
    const rows = this.db
      .prepare("SELECT library_id FROM libraries ORDER BY updated_at DESC")
      .all() as Array<{ library_id: string }>;

    return {
      libraries: rows
        .map((row) => this.getLibraryOverview(row.library_id))
        .filter((overview): overview is LibraryOverview => Boolean(overview))
    };
  }

  getLibraryOverview(libraryId: string): LibraryOverview | null {
    const library = this.db
      .prepare(
        "SELECT library_id, owner_hint, created_at, updated_at FROM libraries WHERE library_id = ?"
      )
      .get(libraryId) as LibraryRecord | undefined;

    if (!library) {
      return null;
    }

    const assetStats = this.db
      .prepare(
        `SELECT
           COUNT(*) AS total,
           SUM(CASE WHEN asset_state = 'active' THEN 1 ELSE 0 END) AS active_count,
           SUM(CASE WHEN asset_state = 'archived' THEN 1 ELSE 0 END) AS archived_count,
           SUM(CASE WHEN review_status = 'needs_review' THEN 1 ELSE 0 END) AS needs_review_count,
           SUM(CASE WHEN review_status = 'reviewed' THEN 1 ELSE 0 END) AS reviewed_count,
           SUM(CASE WHEN review_status = 'auto' THEN 1 ELSE 0 END) AS auto_count
         FROM assets
         WHERE library_id = ?`
      )
      .get(libraryId) as {
      total: number | null;
      active_count: number | null;
      archived_count: number | null;
      needs_review_count: number | null;
      reviewed_count: number | null;
      auto_count: number | null;
    };

    const materialTypeRows = this.db
      .prepare(
        `SELECT material_type, COUNT(*) AS count
         FROM assets
         WHERE library_id = ?
         GROUP BY material_type`
      )
      .all(libraryId) as Array<{ material_type: string; count: number }>;

    const lastIngest = this.db
      .prepare(
        `SELECT updated_at
         FROM pipeline_runs
         WHERE library_id = ? AND run_type = 'ingest'
         ORDER BY updated_at DESC
         LIMIT 1`
      )
      .get(libraryId) as { updated_at: string } | undefined;

    const lastBuild = this.db
      .prepare(
        `SELECT updated_at
         FROM pipeline_runs
         WHERE library_id = ? AND run_type = 'build_asset_library'
         ORDER BY updated_at DESC
         LIMIT 1`
      )
      .get(libraryId) as { updated_at: string } | undefined;

    return {
      library_id: library.library_id,
      owner_hint: library.owner_hint,
      created_at: library.created_at,
      updated_at: library.updated_at,
      last_ingest_at: lastIngest?.updated_at ?? null,
      last_build_at: lastBuild?.updated_at ?? null,
      counts: {
        assets_total: Number(assetStats.total ?? 0),
        active_assets: Number(assetStats.active_count ?? 0),
        archived_assets: Number(assetStats.archived_count ?? 0),
        needs_review_assets: Number(assetStats.needs_review_count ?? 0),
        reviewed_assets: Number(assetStats.reviewed_count ?? 0),
        auto_assets: Number(assetStats.auto_count ?? 0),
        material_type_counts: Object.fromEntries(
          materialTypeRows.map((row) => [row.material_type, row.count])
        )
      }
    };
  }

  upsertParsedFiles(libraryId: string, parsedFiles: ParsedFile[]): ParsedFile[] {
    const statement = this.db.prepare(`
      INSERT INTO files (
        file_id, library_id, file_name, file_path, mime_type, parse_status,
        extracted_text, extracted_summary, provider, size_bytes, payload_json,
        created_at, updated_at
      ) VALUES (
        @file_id, @library_id, @file_name, @file_path, @mime_type, @parse_status,
        @extracted_text, @extracted_summary, @provider, @size_bytes, @payload_json,
        @created_at, @updated_at
      )
      ON CONFLICT(file_id) DO UPDATE SET
        library_id = excluded.library_id,
        file_name = excluded.file_name,
        file_path = excluded.file_path,
        mime_type = excluded.mime_type,
        parse_status = excluded.parse_status,
        extracted_text = excluded.extracted_text,
        extracted_summary = excluded.extracted_summary,
        provider = excluded.provider,
        size_bytes = excluded.size_bytes,
        payload_json = excluded.payload_json,
        updated_at = excluded.updated_at
    `);

    const createdAt = nowIso();
    for (const file of parsedFiles) {
      statement.run({
        ...file,
        library_id: libraryId,
        payload_json: JSON.stringify(file),
        created_at: createdAt,
        updated_at: createdAt
      });
    }

    return this.listParsedFiles(libraryId, parsedFiles.map((file) => file.file_id));
  }

  listParsedFiles(libraryId: string, fileIds?: string[]): ParsedFile[] {
    const rows = fileIds?.length
      ? this.db
          .prepare(
            `SELECT payload_json FROM files
             WHERE library_id = ?
             AND file_id IN (${fileIds.map(() => "?").join(",")})`
          )
          .all(libraryId, ...fileIds)
      : this.db
          .prepare("SELECT payload_json FROM files WHERE library_id = ? ORDER BY created_at ASC")
          .all(libraryId);

    return rows.map((row: unknown) =>
      parseJson<ParsedFile>((row as { payload_json: string }).payload_json)
    );
  }

  upsertAssetCards(libraryId: string, assetCards: AssetCard[]): AssetCard[] {
    const statement = this.db.prepare(`
      INSERT INTO assets (
        asset_id, library_id, material_type, title, holder_name, issuer_name,
        issue_date, expiry_date, validity_status, normalized_summary, asset_state,
        review_status, last_verified_at, payload_json,
        created_at, updated_at
      ) VALUES (
        @asset_id, @library_id, @material_type, @title, @holder_name, @issuer_name,
        @issue_date, @expiry_date, @validity_status, @normalized_summary, @asset_state,
        @review_status, @last_verified_at, @payload_json,
        @created_at, @updated_at
      )
      ON CONFLICT(asset_id) DO UPDATE SET
        library_id = excluded.library_id,
        material_type = excluded.material_type,
        title = excluded.title,
        holder_name = excluded.holder_name,
        issuer_name = excluded.issuer_name,
        issue_date = excluded.issue_date,
        expiry_date = excluded.expiry_date,
        validity_status = excluded.validity_status,
        normalized_summary = excluded.normalized_summary,
        asset_state = excluded.asset_state,
        review_status = excluded.review_status,
        last_verified_at = excluded.last_verified_at,
        payload_json = excluded.payload_json,
        updated_at = excluded.updated_at
    `);

    const createdAt = nowIso();
    for (const asset of assetCards) {
      const normalizedAsset = normalizeStoredAssetCard(asset);
      statement.run({
        asset_id: normalizedAsset.asset_id,
        library_id: libraryId,
        material_type: normalizedAsset.material_type,
        title: normalizedAsset.title,
        holder_name: normalizedAsset.holder_name,
        issuer_name: normalizedAsset.issuer_name,
        issue_date: normalizedAsset.issue_date,
        expiry_date: normalizedAsset.expiry_date,
        validity_status: normalizedAsset.validity_status,
        normalized_summary: normalizedAsset.normalized_summary,
        asset_state: normalizedAsset.asset_state,
        review_status: normalizedAsset.review_status,
        last_verified_at: normalizedAsset.last_verified_at,
        payload_json: JSON.stringify(normalizedAsset),
        created_at: createdAt,
        updated_at: createdAt
      });
    }

    return this.listAssetCards(libraryId);
  }

  listAssetCards(libraryId: string): AssetCard[] {
    const rows = this.db
      .prepare(
        "SELECT payload_json, asset_state, review_status, last_verified_at FROM assets WHERE library_id = ? ORDER BY created_at ASC"
      )
      .all(libraryId);
    return rows.map((row: unknown) =>
      normalizeStoredAssetCard({
        ...parseJson<AssetCard>((row as { payload_json: string }).payload_json),
        asset_state: (row as { asset_state: AssetState }).asset_state,
        review_status: (row as { review_status: ReviewStatus }).review_status,
        last_verified_at: (row as { last_verified_at: string | null }).last_verified_at
      })
    );
  }

  getAssetCardsByIds(libraryId: string, assetIds: string[]): AssetCard[] {
    if (assetIds.length === 0) {
      return [];
    }

    const rows = this.db
      .prepare(
        `SELECT payload_json, asset_state, review_status, last_verified_at
         FROM assets
         WHERE library_id = ?
         AND asset_id IN (${assetIds.map(() => "?").join(",")})`
      )
      .all(libraryId, ...assetIds) as Array<{
      payload_json: string;
      asset_state: AssetState;
      review_status: ReviewStatus;
      last_verified_at: string | null;
    }>;

    const byId = new Map(
      rows.map((row) => {
        const asset = normalizeStoredAssetCard({
          ...parseJson<AssetCard>(row.payload_json),
          asset_state: row.asset_state,
          review_status: row.review_status,
          last_verified_at: row.last_verified_at
        });
        return [asset.asset_id, asset] as const;
      })
    );

    return assetIds.map((assetId) => byId.get(assetId)).filter((asset): asset is AssetCard => Boolean(asset));
  }

  upsertMergedAssets(libraryId: string, mergedAssets: MergedAsset[]): MergedAsset[] {
    const statement = this.db.prepare(`
      INSERT INTO merged_assets (
        merged_asset_id, library_id, canonical_asset_id, selected_asset_id, status,
        payload_json, created_at, updated_at
      ) VALUES (
        @merged_asset_id, @library_id, @canonical_asset_id, @selected_asset_id, @status,
        @payload_json, @created_at, @updated_at
      )
      ON CONFLICT(merged_asset_id) DO UPDATE SET
        library_id = excluded.library_id,
        canonical_asset_id = excluded.canonical_asset_id,
        selected_asset_id = excluded.selected_asset_id,
        status = excluded.status,
        payload_json = excluded.payload_json,
        updated_at = excluded.updated_at
    `);

    const createdAt = nowIso();
    for (const merged of mergedAssets) {
      statement.run({
        merged_asset_id: merged.merged_asset_id,
        library_id: libraryId,
        canonical_asset_id: merged.canonical_asset_id,
        selected_asset_id: merged.selected_asset_id,
        status: merged.status,
        payload_json: JSON.stringify(merged),
        created_at: createdAt,
        updated_at: createdAt
      });
    }

    return this.getMergedAssets(libraryId);
  }

  getMergedAssets(libraryId: string): MergedAsset[] {
    const rows = this.db
      .prepare(
        "SELECT payload_json FROM merged_assets WHERE library_id = ? ORDER BY created_at ASC"
      )
      .all(libraryId);
    return rows.map((row: unknown) =>
      parseJson<MergedAsset>((row as { payload_json: string }).payload_json)
    );
  }

  upsertAssetSearchIndex(input: {
    library_id: string;
    assets: Array<{
      asset_id: string;
      title: string;
      normalized_summary: string;
      agent_tags: string[];
      search_text: string;
      embedding: number[] | null;
      model: string;
    }>;
  }): ReindexLibrarySearchData {
    const deleteFts = this.db.prepare("DELETE FROM asset_search_fts WHERE asset_id = ?");
    const insertFts = this.db.prepare(
      `INSERT INTO asset_search_fts (
        asset_id, library_id, title, normalized_summary, agent_tags_text, search_text
      ) VALUES (?, ?, ?, ?, ?, ?)`
    );
    const findMeta = this.db.prepare(
      "SELECT vec_rowid FROM asset_embedding_meta WHERE asset_id = ?"
    );
    const deleteMeta = this.db.prepare("DELETE FROM asset_embedding_meta WHERE asset_id = ?");
    const deleteVec = this.vectorSearchEnabled
      ? this.db.prepare("DELETE FROM asset_embedding_vec WHERE rowid = ?")
      : null;
    const insertMeta = this.db.prepare(
      `INSERT INTO asset_embedding_meta (
        asset_id, library_id, search_text, agent_tags_text, tag_blob, model, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?)`
    );
    const insertVec = this.vectorSearchEnabled
      ? this.db.prepare("INSERT INTO asset_embedding_vec(rowid, embedding) VALUES (?, ?)")
      : null;

    let indexedAssets = 0;
    let skippedAssets = 0;
    const updatedAt = nowIso();
    for (const asset of input.assets) {
      deleteFts.run(asset.asset_id);
      const existing = findMeta.get(asset.asset_id) as
        | { vec_rowid: number | bigint }
        | undefined;
      if (existing && deleteVec) {
        deleteVec.run(BigInt(existing.vec_rowid));
      }
      deleteMeta.run(asset.asset_id);

      const agentTagsText = buildAgentTagsText(asset.agent_tags);
      insertFts.run(
        asset.asset_id,
        input.library_id,
        asset.title,
        asset.normalized_summary,
        agentTagsText,
        asset.search_text
      );

      insertMeta.run(
        asset.asset_id,
        input.library_id,
        asset.search_text,
        agentTagsText,
        `|${asset.agent_tags.join("|")}|`,
        asset.model,
        updatedAt
      );
      indexedAssets += 1;

      if (!this.vectorSearchEnabled || !asset.embedding?.length) {
        continue;
      }

      const vecRowId = (findMeta.get(asset.asset_id) as
        | { vec_rowid: number | bigint }
        | undefined)?.vec_rowid;
      if (
        (typeof vecRowId !== "number" && typeof vecRowId !== "bigint") ||
        Number(vecRowId) <= 0
      ) {
        continue;
      }
      insertVec?.run(BigInt(vecRowId), JSON.stringify(asset.embedding));
    }

    return {
      library_id: input.library_id,
      indexed_assets: indexedAssets,
      skipped_assets: skippedAssets,
      model: input.assets[0]?.model ?? "unavailable"
    };
  }

  removeAssetSearchIndex(assetIds: string[]): void {
    if (assetIds.length === 0) {
      return;
    }

    const findMeta = this.db.prepare(
      "SELECT vec_rowid FROM asset_embedding_meta WHERE asset_id = ?"
    );
    const deleteVec = this.vectorSearchEnabled
      ? this.db.prepare("DELETE FROM asset_embedding_vec WHERE rowid = ?")
      : null;
    const deleteMeta = this.db.prepare("DELETE FROM asset_embedding_meta WHERE asset_id = ?");
    const deleteFts = this.db.prepare("DELETE FROM asset_search_fts WHERE asset_id = ?");

    for (const assetId of assetIds) {
      const existing = findMeta.get(assetId) as
        | { vec_rowid: number | bigint }
        | undefined;
      if (existing && deleteVec) {
        deleteVec.run(BigInt(existing.vec_rowid));
      }
      deleteMeta.run(assetId);
      deleteFts.run(assetId);
    }
  }

  searchAssetIdsByFts(input: {
    library_id: string;
    query: string;
    limit: number;
    allowed_asset_ids?: string[];
  }): string[] {
    const trimmed = input.query.trim();
    if (!trimmed) {
      return [];
    }

    let sql = `
      SELECT asset_id
      FROM asset_search_fts
      WHERE library_id = ?
        AND asset_search_fts MATCH ?
    `;
    const params: SQLInputValue[] = [input.library_id, trimmed];
    if (input.allowed_asset_ids?.length) {
      sql += ` AND asset_id IN (${input.allowed_asset_ids.map(() => "?").join(",")})`;
      params.push(...input.allowed_asset_ids);
    }
    sql += " LIMIT ?";
    params.push(input.limit);

    const rows = this.db.prepare(sql).all(...params) as Array<{ asset_id: string }>;
    return rows.map((row) => row.asset_id);
  }

  searchAssetIdsByTags(input: {
    library_id: string;
    tag_filters_any?: string[];
    tag_filters_all?: string[];
    limit: number;
    allowed_asset_ids?: string[];
  }): string[] {
    const anyTags = [...new Set(input.tag_filters_any ?? [])].filter(Boolean);
    const allTags = [...new Set(input.tag_filters_all ?? [])].filter(Boolean);
    if (anyTags.length === 0 && allTags.length === 0) {
      return [];
    }

    let sql = "SELECT asset_id FROM asset_embedding_meta WHERE library_id = ?";
    const params: SQLInputValue[] = [input.library_id];

    if (input.allowed_asset_ids?.length) {
      sql += ` AND asset_id IN (${input.allowed_asset_ids.map(() => "?").join(",")})`;
      params.push(...input.allowed_asset_ids);
    }

    if (allTags.length) {
      for (const tag of allTags) {
        sql += " AND instr(tag_blob, ?) > 0";
        params.push(`|${tag}|`);
      }
    }

    if (anyTags.length) {
      sql += ` AND (${anyTags.map(() => "instr(tag_blob, ?) > 0").join(" OR ")})`;
      for (const tag of anyTags) {
        params.push(`|${tag}|`);
      }
    }

    sql += " LIMIT ?";
    params.push(input.limit);

    const rows = this.db.prepare(sql).all(...params) as Array<{ asset_id: string }>;
    return rows.map((row) => row.asset_id);
  }

  searchAssetIdsByVector(input: {
    library_id: string;
    query_embedding: number[];
    limit: number;
    allowed_asset_ids?: string[];
  }): string[] {
    if (!this.vectorSearchEnabled || input.query_embedding.length === 0) {
      return [];
    }

    let sql = `
      SELECT meta.asset_id
      FROM asset_embedding_vec vec
      JOIN asset_embedding_meta meta ON meta.vec_rowid = vec.rowid
      WHERE vec.embedding MATCH ?
        AND k = ?
        AND meta.library_id = ?
    `;
    const params: SQLInputValue[] = [JSON.stringify(input.query_embedding), input.limit, input.library_id];

    if (input.allowed_asset_ids?.length) {
      sql += ` AND meta.asset_id IN (${input.allowed_asset_ids.map(() => "?").join(",")})`;
      params.push(...input.allowed_asset_ids);
    }

    const rows = this.db.prepare(sql).all(...params) as Array<{ asset_id: string }>;
    return rows.map((row) => row.asset_id);
  }

  queryAssets(query: AssetQuery): QueryAssetsData {
    let sql = "SELECT payload_json FROM assets WHERE library_id = ?";
    const params: SQLInputValue[] = [query.library_id];

    if (query.material_types?.length) {
      sql += ` AND material_type IN (${query.material_types.map(() => "?").join(",")})`;
      params.push(...query.material_types);
    }

    if (query.validity_statuses?.length) {
      sql += ` AND validity_status IN (${query.validity_statuses.map(() => "?").join(",")})`;
      params.push(...query.validity_statuses);
    }

    const assetStates = query.asset_states?.length ? query.asset_states : ["active"];
    sql += ` AND asset_state IN (${assetStates.map(() => "?").join(",")})`;
    params.push(...assetStates);

    if (query.review_statuses?.length) {
      sql += ` AND review_status IN (${query.review_statuses.map(() => "?").join(",")})`;
      params.push(...query.review_statuses);
    }

    if (query.keyword) {
      sql += " AND (title LIKE ? OR normalized_summary LIKE ?)";
      params.push(`%${query.keyword}%`, `%${query.keyword}%`);
    }

    const rows = this.db.prepare(sql).all(...params);
    let assetCards = rows.map((row: unknown) =>
      normalizeStoredAssetCard(parseJson<AssetCard>((row as { payload_json: string }).payload_json))
    );

    if (query.reusable_scenario) {
      assetCards = assetCards.filter((asset: AssetCard) =>
        asset.reusable_scenarios.includes(query.reusable_scenario as string)
      );
    }

    if (query.tag_filters_all?.length) {
      assetCards = assetCards.filter((asset) =>
        query.tag_filters_all!.every((tag) => asset.agent_tags.includes(tag))
      );
    }

    if (query.tag_filters_any?.length) {
      assetCards = assetCards.filter((asset) =>
        query.tag_filters_any!.some((tag) => asset.agent_tags.includes(tag))
      );
    }

    if (query.limit && query.limit > 0) {
      assetCards = assetCards.slice(0, query.limit);
    }

    const matchedAssetIds = new Set(assetCards.map((asset) => asset.asset_id));
    const mergedAssets = this.getMergedAssets(query.library_id).filter((merged) => {
      if (matchedAssetIds.has(merged.selected_asset_id)) {
        return true;
      }
      if (matchedAssetIds.has(merged.canonical_asset_id)) {
        return true;
      }
      return merged.superseded_asset_ids.some((assetId) => matchedAssetIds.has(assetId));
    });

    return {
      library_id: query.library_id,
      asset_cards: assetCards,
      merged_assets: mergedAssets
    };
  }

  getAssetCard(libraryId: string, assetId: string): AssetCard | null {
    const row = this.db
      .prepare(
        "SELECT payload_json, asset_state, review_status, last_verified_at FROM assets WHERE library_id = ? AND asset_id = ?"
      )
      .get(libraryId, assetId) as
      | {
          payload_json: string;
          asset_state: AssetState;
          review_status: ReviewStatus;
          last_verified_at: string | null;
        }
      | undefined;

    if (!row) {
      return null;
    }

    return normalizeStoredAssetCard({
      ...parseJson<AssetCard>(row.payload_json),
      asset_state: row.asset_state,
      review_status: row.review_status,
      last_verified_at: row.last_verified_at
    });
  }

  writeAssetChangeEvent(input: {
    libraryId: string;
    assetId: string;
    action: AssetChangeEvent["action"];
    changedFields: string[];
    payload: unknown;
  }): AssetChangeEvent {
    const event: AssetChangeEvent = {
      event_id: `evt_${randomUUID().replaceAll("-", "")}`,
      library_id: input.libraryId,
      asset_id: input.assetId,
      action: input.action,
      changed_fields: input.changedFields,
      payload_json: input.payload,
      created_at: nowIso()
    };

    this.db
      .prepare(
        `INSERT INTO asset_change_events (
          event_id, library_id, asset_id, action, changed_fields_json, payload_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        event.event_id,
        event.library_id,
        event.asset_id,
        event.action,
        JSON.stringify(event.changed_fields),
        JSON.stringify(event.payload_json),
        event.created_at
      );

    return event;
  }

  patchAssetCard(
    libraryId: string,
    assetId: string,
    patch: Partial<
      Pick<
        AssetCard,
        | "title"
        | "holder_name"
        | "issuer_name"
        | "issue_date"
        | "expiry_date"
        | "validity_status"
        | "agent_tags"
        | "reusable_scenarios"
        | "sensitivity_level"
        | "normalized_summary"
        | "review_status"
        | "last_verified_at"
      >
    >
  ): { asset_card: AssetCard; change_event: AssetChangeEvent } | null {
    const existing = this.getAssetCard(libraryId, assetId);
    if (!existing) {
      return null;
    }

    const updated = normalizeStoredAssetCard({
      ...existing,
      ...patch,
      review_status: patch.review_status ?? "reviewed",
      last_verified_at: patch.last_verified_at ?? nowIso()
    });
    this.upsertAssetCards(libraryId, [updated]);

    return {
      asset_card: this.getAssetCard(libraryId, assetId) ?? updated,
      change_event: this.writeAssetChangeEvent({
        libraryId,
        assetId,
        action: "patch",
        changedFields: Object.keys(patch),
        payload: { before: existing, patch, after: updated }
      })
    };
  }

  setAssetState(
    libraryId: string,
    assetId: string,
    assetState: AssetState
  ): { asset_card: AssetCard; change_event: AssetChangeEvent } | null {
    const existing = this.getAssetCard(libraryId, assetId);
    if (!existing) {
      return null;
    }

    const updated = normalizeStoredAssetCard({
      ...existing,
      asset_state: assetState
    });
    this.upsertAssetCards(libraryId, [updated]);

    return {
      asset_card: this.getAssetCard(libraryId, assetId) ?? updated,
      change_event: this.writeAssetChangeEvent({
        libraryId,
        assetId,
        action: assetState === "archived" ? "archive" : "restore",
        changedFields: ["asset_state"],
        payload: { before: existing.asset_state, after: assetState }
      })
    };
  }

  listReviewQueue(libraryId: string): ReviewQueueData {
    return {
      library_id: libraryId,
      asset_cards: this.queryAssets({
        library_id: libraryId,
        asset_states: ["active"],
        review_statuses: ["needs_review"]
      }).asset_cards
    };
  }

  writeLifecycleRun(
    runId: string,
    payload: CheckLifecycleData,
    goal: string,
    audit?: AgentDecisionAudit
  ): LifecycleRunData {
    this.db
      .prepare(
        `INSERT OR REPLACE INTO lifecycle_runs (
          run_id, library_id, goal, as_of_date, window_days, payload_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        runId,
        payload.library_id,
        goal,
        payload.as_of_date,
        payload.window_days,
        JSON.stringify(payload),
        nowIso()
      );
    const persistedAudit = audit
      ? this.writeAgentDecisionAudit(audit, { type: "lifecycle_run", id: runId })
      : null;
    return {
      lifecycle_run: payload,
      audit: persistedAudit
    };
  }

  getLatestLifecycleRun(
    libraryId: string,
    goal?: string
  ): LifecycleRunData | null {
    const row = goal
      ? (this.db
          .prepare(
            `SELECT run_id, payload_json
             FROM lifecycle_runs
             WHERE library_id = ? AND goal = ?
             ORDER BY created_at DESC
             LIMIT 1`
          )
          .get(libraryId, goal) as { run_id: string; payload_json: string } | undefined)
      : (this.db
          .prepare(
            `SELECT run_id, payload_json
             FROM lifecycle_runs
             WHERE library_id = ?
             ORDER BY created_at DESC
             LIMIT 1`
          )
          .get(libraryId) as { run_id: string; payload_json: string } | undefined);

    return row
      ? {
          lifecycle_run: parseJson<CheckLifecycleData>(row.payload_json),
          audit: this.getLatestAgentDecisionAudit({
            type: "lifecycle_run",
            id: row.run_id
          })
        }
      : null;
  }

  writePackageRun(
    packagePlan: PackagePlan,
    outputDir?: string,
    audit?: AgentDecisionAudit
  ): PackageRunData {
    const createdAt = nowIso();
    this.db
      .prepare(
        `INSERT OR REPLACE INTO package_runs (
          package_id, library_id, target_goal, package_name, submission_profile,
          output_dir, payload_json, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        packagePlan.package_id,
        packagePlan.library_id,
        packagePlan.target_goal,
        packagePlan.package_name,
        packagePlan.submission_profile,
        outputDir ?? null,
        JSON.stringify(packagePlan),
        createdAt,
        createdAt
      );
    const persistedAudit = audit
      ? this.writeAgentDecisionAudit(audit, {
          type: "package_run",
          id: packagePlan.package_id
        })
      : null;
    return {
      package_plan: packagePlan,
      output_dir: outputDir ?? null,
      audit: persistedAudit
    };
  }

  getPackageRun(packageId: string): PackageRunData | null {
    const row = this.db
      .prepare("SELECT payload_json, output_dir FROM package_runs WHERE package_id = ?")
      .get(packageId) as { payload_json: string; output_dir: string | null } | undefined;
    return row
      ? {
          package_plan: parseJson<PackagePlan>(row.payload_json),
          output_dir: row.output_dir,
          audit: this.getLatestAgentDecisionAudit({
            type: "package_run",
            id: packageId
          })
        }
      : null;
  }

  writeExecutionLog(log: ExecutionLog): ExecutionLog {
    const createdAt = nowIso();
    this.db
      .prepare(
        `INSERT OR REPLACE INTO execution_logs (
          execution_id, library_id, package_id, submission_profile, status,
          payload_json, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        log.execution_id,
        log.library_id,
        log.package_id,
        log.submission_profile,
        log.status,
        JSON.stringify(log),
        createdAt,
        createdAt
      );
    return log;
  }
}

export function openCaixuStorage(dbPath: string): CaixuStorage {
  return new CaixuStorage(dbPath);
}

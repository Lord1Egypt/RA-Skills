import { randomUUID } from "node:crypto";
import { z } from "zod";

export const schemaVersion = "1.0" as const;

export const toolStatusSchema = z.enum(["success", "partial", "failed"]);
export const severitySchema = z.enum(["warning", "blocking"]);
export const validityStatusSchema = z.enum([
  "valid",
  "expiring",
  "expired",
  "long_term",
  "unknown"
]);
export const assetStateSchema = z.enum(["active", "archived"]);
export const reviewStatusSchema = z.enum(["auto", "needs_review", "reviewed"]);
export const agentTagSchema = z
  .string()
  .regex(/^(doc|use|entity|risk):[a-z0-9_]+$/u);

export const sourceFileSchema = z.object({
  file_id: z.string().min(1),
  file_name: z.string().min(1),
  mime_type: z.string().min(1),
  file_path: z.string().min(1).optional()
});

export const parsedFileSchema = z.object({
  file_id: z.string().min(1),
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.string().min(1),
  size_bytes: z.number().int().nonnegative(),
  parse_status: z.enum(["parsed", "binary_only"]),
  extracted_text: z.string().nullable(),
  extracted_summary: z.string().nullable(),
  provider: z.enum([
    "local",
    "zhipu_parser_lite",
    "zhipu_parser_export",
    "zhipu_ocr",
    "zhipu_vlm",
    "hybrid"
  ])
});

export const toolErrorSchema = z.object({
  code: z.string().min(1),
  message: z.string().min(1),
  retryable: z.boolean().optional(),
  file_id: z.string().nullable().optional(),
  file_name: z.string().nullable().optional(),
  asset_id: z.string().nullable().optional()
});

export const localFileRouteSchema = z.enum([
  "text",
  "parser_lite",
  "parser_export",
  "ocr",
  "vlm",
  "skip"
]);

export const localFileSchema = z.object({
  file_id: z.string().min(1),
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.string().min(1),
  extension: z.string().min(1),
  size_bytes: z.number().int().nonnegative(),
  suggested_route: localFileRouteSchema,
  skip_reason: z.string().nullable()
});

export const listLocalFilesDataSchema = z.object({
  input_root: z.string().min(1),
  files: z.array(localFileSchema).default([])
});

export const readLocalTextFileDataSchema = z.object({
  file: localFileSchema,
  text: z.string(),
  text_length: z.number().int().nonnegative()
});

export const parserExportAssetSchema = z.object({
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.string().min(1)
});

export const extractParserTextDataSchema = z.object({
  file: localFileSchema,
  mode: z.enum(["lite", "export"]),
  provider: z.enum([
    "zhipu_parser_lite",
    "zhipu_parser_export",
    "zhipu_ocr",
    "zhipu_vlm",
    "hybrid"
  ]),
  text: z.string().nullable(),
  export_assets: z.array(parserExportAssetSchema).default([]),
  warnings: z.array(toolErrorSchema).default([])
});

export const renderedPdfPageSchema = z.object({
  page_number: z.number().int().positive(),
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.literal("image/png")
});

export const renderPdfPagesDataSchema = z.object({
  file: localFileSchema,
  pages: z.array(renderedPdfPageSchema).default([])
});

export const visualTextOutputSchema = z.object({
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.string().min(1),
  text: z.string().nullable()
});

export const extractVisualTextDataSchema = z.object({
  engine: z.enum(["ocr", "vlm"]),
  provider: z.enum(["zhipu_ocr", "zhipu_vlm"]),
  outputs: z.array(visualTextOutputSchema).default([]),
  warnings: z.array(toolErrorSchema).default([])
});

export const assetCardSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  asset_id: z.string().min(1),
  material_type: z.string().min(1),
  title: z.string().min(1),
  holder_name: z.string().min(1).nullable(),
  issuer_name: z.string().min(1).nullable(),
  issue_date: z.string().nullable(),
  expiry_date: z.string().nullable(),
  validity_status: validityStatusSchema,
  agent_tags: z.array(agentTagSchema).default([]),
  reusable_scenarios: z.array(z.string().min(1)).default([]),
  sensitivity_level: z.enum(["low", "medium", "high"]),
  source_files: z.array(sourceFileSchema).min(1),
  confidence: z.number().min(0).max(1),
  normalized_summary: z.string().min(1),
  asset_state: assetStateSchema,
  review_status: reviewStatusSchema,
  last_verified_at: z.string().nullable()
});

export const mergedAssetVersionSchema = z.object({
  asset_id: z.string().min(1),
  issue_date: z.string().nullable(),
  expiry_date: z.string().nullable(),
  source_file_count: z.number().int().nonnegative()
});

export const mergedAssetSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  merged_asset_id: z.string().min(1),
  canonical_asset_id: z.string().min(1),
  selected_asset_id: z.string().min(1),
  superseded_asset_ids: z.array(z.string().min(1)).default([]),
  dedupe_strategy: z.string().min(1),
  merge_reason: z.string().min(1),
  status: z.enum(["merged", "unmerged", "conflict"]),
  version_order: z.array(mergedAssetVersionSchema).default([])
});

export const lifecycleEventSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  event_id: z.string().min(1),
  asset_id: z.string().min(1),
  trigger_type: z.enum([
    "expiry_trigger",
    "renewal_window_trigger",
    "goal_trigger"
  ]),
  event_status: z.enum(["recommended", "urgent", "info"]),
  severity: severitySchema,
  event_date: z.string().min(1),
  window_start_date: z.string().nullable(),
  window_end_date: z.string().nullable(),
  target_goal: z.string().min(1),
  recommended_action: z.string().min(1),
  prerequisite_assets: z.array(z.string().min(1)).default([]),
  blocking_items: z.array(z.string().min(1)).default([]),
  related_rule_ids: z.array(z.string().min(1)).default([])
});

export const ruleMatchSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  match_id: z.string().min(1),
  asset_id: z.string().min(1),
  rule_pack_id: z.string().min(1),
  rule_id: z.string().min(1),
  scene_key: z.string().min(1),
  match_status: z.enum(["matched", "recommended", "unmatched"]),
  renewable: z.boolean(),
  reusable: z.boolean(),
  required_assets: z.array(z.string().min(1)).default([]),
  output_requirements: z.array(z.string().min(1)).default([]),
  notes: z.string().min(1)
});

export const missingItemSchema = z.object({
  code: z.string().min(1),
  title: z.string().min(1),
  description: z.string().min(1),
  severity: severitySchema,
  asset_type: z.string().min(1),
  required_for: z.string().min(1),
  suggested_action: z.string().min(1)
});

export const missingItemsSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  diagnosis_id: z.string().min(1),
  target_goal: z.string().min(1),
  rule_pack_id: z.string().min(1),
  items: z.array(missingItemSchema).default([]),
  available_asset_ids: z.array(z.string().min(1)).default([]),
  gap_summary: z.string().min(1),
  next_actions: z.array(z.string().min(1)).default([]),
  blocking_level: z.enum(["none", "warning", "partial", "blocking"])
});

export const readinessSchema = z.object({
  ready_for_submission: z.boolean(),
  blocking_items: z.array(missingItemSchema).default([]),
  warning_items: z.array(missingItemSchema).default([]),
  rationale: z.string().min(1)
});

export const generatedFileSchema = z.object({
  file_name: z.string().min(1),
  file_type: z.enum(["xlsx", "zip", "json", "txt", "md"]),
  purpose: z.string().min(1)
});

export const packagePlanSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  package_id: z.string().min(1),
  target_goal: z.string().min(1),
  package_name: z.string().min(1),
  selected_asset_ids: z.array(z.string().min(1)).default([]),
  selected_exports: z.array(z.string().min(1)).default([]),
  missing_items_ref: z.string().min(1),
  generated_files: z.array(generatedFileSchema).default([]),
  submission_profile: z.string().min(1),
  readiness: readinessSchema,
  operator_notes: z.string().min(1)
});

export const executionStepSchema = z.object({
  step: z.string().min(1),
  status: z.enum(["succeeded", "failed", "skipped"]),
  artifact: z.string().nullable()
});

export const executionLogSchema = z.object({
  schema_version: z.literal(schemaVersion),
  library_id: z.string().min(1),
  execution_id: z.string().min(1),
  package_id: z.string().min(1),
  submission_profile: z.string().min(1),
  executor: z.enum(["autoclaw", "openclaw", "mock"]),
  status: z.enum(["success", "partial", "failed"]),
  started_at: z.string().min(1),
  finished_at: z.string().min(1),
  steps: z.array(executionStepSchema).default([]),
  result_summary: z.string().min(1),
  submitted_artifacts: z.array(z.string().min(1)).default([]),
  failure_reason: z.string().nullable()
});

export const pipelineRunCountsSchema = z.object({
  parsed: z.number().int().nonnegative().default(0),
  failed: z.number().int().nonnegative().default(0),
  warnings: z.number().int().nonnegative().default(0),
  skipped: z.number().int().nonnegative().default(0),
  assets: z.number().int().nonnegative().default(0),
  merged: z.number().int().nonnegative().default(0)
});

export const pipelineRunSchema = z.object({
  run_id: z.string().min(1),
  library_id: z.string().min(1),
  run_type: z.enum(["ingest", "build_asset_library"]),
  status: z.enum(["running", "completed", "partial", "failed"]),
  goal: z.string().nullable(),
  input_root: z.string().nullable(),
  counts: pipelineRunCountsSchema,
  latest_stage: z.string().min(1),
  created_at: z.string().min(1),
  updated_at: z.string().min(1)
});

export const pipelineStepSchema = z.object({
  step_id: z.string().min(1),
  run_id: z.string().min(1),
  stage: z.string().min(1),
  status: z.enum(["running", "completed", "partial", "failed", "skipped"]),
  tool_name: z.string().nullable(),
  message: z.string().min(1),
  payload_json: z.unknown(),
  created_at: z.string().min(1)
});

export const pipelineRunDataSchema = z.object({
  pipeline_run: pipelineRunSchema.nullable(),
  steps: z.array(pipelineStepSchema).default([])
});

export const parseMaterialsDataSchema = z.object({
  file_ids: z.array(z.string().min(1)),
  parsed_count: z.number().int().nonnegative(),
  failed_count: z.number().int().nonnegative(),
  warning_count: z.number().int().nonnegative(),
  skipped_count: z.number().int().nonnegative(),
  parsed_files: z.array(parsedFileSchema).default([]),
  failed_files: z.array(toolErrorSchema).default([]),
  warning_files: z.array(toolErrorSchema).default([]),
  skipped_files: z.array(toolErrorSchema).default([])
});

export const buildAssetLibraryDataSchema = z.object({
  library_id: z.string().min(1),
  asset_cards: z.array(assetCardSchema).default([]),
  merged_assets: z.array(mergedAssetSchema).default([]),
  summary: z.object({
    total_assets: z.number().int().nonnegative(),
    merged_groups: z.number().int().nonnegative(),
    anomalies: z.number().int().nonnegative(),
    unmerged_assets: z.number().int().nonnegative()
  })
});

export const queryAssetsDataSchema = z.object({
  library_id: z.string().min(1),
  asset_cards: z.array(assetCardSchema).default([]),
  merged_assets: z.array(mergedAssetSchema).default([])
});

export const reindexLibrarySearchDataSchema = z.object({
  library_id: z.string().min(1),
  indexed_assets: z.number().int().nonnegative(),
  skipped_assets: z.number().int().nonnegative(),
  model: z.string().min(1)
});

export const libraryOverviewSchema = z.object({
  library_id: z.string().min(1),
  owner_hint: z.string().nullable(),
  created_at: z.string().min(1),
  updated_at: z.string().min(1),
  last_ingest_at: z.string().nullable(),
  last_build_at: z.string().nullable(),
  counts: z.object({
    assets_total: z.number().int().nonnegative(),
    active_assets: z.number().int().nonnegative(),
    archived_assets: z.number().int().nonnegative(),
    needs_review_assets: z.number().int().nonnegative(),
    reviewed_assets: z.number().int().nonnegative(),
    auto_assets: z.number().int().nonnegative(),
    material_type_counts: z.record(z.string(), z.number().int().nonnegative())
  })
});

export const listLibrariesDataSchema = z.object({
  libraries: z.array(libraryOverviewSchema).default([])
});

export const assetChangeEventSchema = z.object({
  event_id: z.string().min(1),
  library_id: z.string().min(1),
  asset_id: z.string().min(1),
  action: z.enum(["patch", "archive", "restore"]),
  changed_fields: z.array(z.string().min(1)).default([]),
  payload_json: z.unknown(),
  created_at: z.string().min(1)
});

export const patchAssetCardDataSchema = z.object({
  library_id: z.string().min(1),
  asset_card: assetCardSchema,
  change_event: assetChangeEventSchema
});

export const reviewQueueDataSchema = z.object({
  library_id: z.string().min(1),
  asset_cards: z.array(assetCardSchema).default([])
});

export const checkLifecycleDataSchema = z.object({
  library_id: z.string().min(1),
  as_of_date: z.string().min(1),
  window_days: z.number().int().positive(),
  lifecycle_events: z.array(lifecycleEventSchema).default([]),
  rule_matches: z.array(ruleMatchSchema).default([]),
  missing_items: missingItemsSchema,
  readiness: readinessSchema
});

export const exportLedgersDataSchema = z.object({
  library_id: z.string().min(1),
  exported_files: z.array(z.string().min(1)).default([])
});

export const buildPackageDataSchema = z.object({
  library_id: z.string().min(1),
  package_plan: packagePlanSchema,
  exported_files: z.array(z.string().min(1)).default([])
});

export const packageRunDataSchema = z.object({
  package_plan: packagePlanSchema.nullable(),
  output_dir: z.string().nullable(),
  audit: z.lazy(() => agentDecisionAuditSchema).nullable().optional()
});

export const lifecycleRunDataSchema = z.object({
  lifecycle_run: checkLifecycleDataSchema.nullable(),
  audit: z.lazy(() => agentDecisionAuditSchema).nullable().optional()
});

export const submitDemoInputSchema = z.object({
  package_plan_id: z.string().min(1),
  submission_profile: z.string().min(1),
  allow_risky_submit: z.boolean().optional(),
  dry_run: z.boolean().optional()
});

export const submitDemoDataSchema = z.object({
  library_id: z.string().min(1),
  execution_log: executionLogSchema
});

export const submissionProfileSchema = z.object({
  profile_id: z.string().min(1),
  target_url: z.string().url(),
  file_fields: z.array(z.string().min(1)).default([]),
  text_fields: z.record(z.string(), z.string()),
  success_text: z.array(z.string().min(1)).default([]),
  screenshot_steps: z.array(z.string().min(1)).default([]),
  log_sampling: z.enum(["minimal", "normal", "verbose"])
});

export const validationStatusSchema = z.enum(["passed", "failed", "partial"]);

export const ruleRequirementSchema = z.object({
  code: z.string().min(1),
  title: z.string().min(1),
  required: z.boolean(),
  blocking: z.boolean(),
  description: z.string().min(1)
});

export const ruleProfileSchema = z.object({
  profile_id: z.string().min(1),
  display_name: z.string().min(1),
  bundle_version: z.string().min(1),
  rule_pack_id: z.string().min(1),
  default_window_days: z.number().int().positive(),
  scene_summary: z.string().min(1),
  requirements: z.array(ruleRequirementSchema).min(1),
  lifecycle_focus: z.array(z.string().min(1)).default([]),
  package_guidance: z.array(z.string().min(1)).default([]),
  readiness_policy: z.object({
    allow_submit_with_blocking_items: z.boolean(),
    allow_truthful_package_when_blocked: z.boolean()
  }),
  notes: z.string().min(1)
});

export const ruleProfileBundleSchema = ruleProfileSchema;

export const agentDecisionAuditSchema = z.object({
  decision_id: z.string().min(1),
  stage: z.enum(["build_asset_library", "check_lifecycle", "build_package"]),
  library_id: z.string().min(1),
  goal: z.string().min(1),
  profile_id: z.string().min(1),
  model: z.string().min(1),
  input_asset_ids: z.array(z.string().min(1)).default([]),
  input_file_ids: z.array(z.string().min(1)).default([]),
  input_summary: z.string().min(1),
  validation_status: validationStatusSchema,
  validation_errors: z.array(toolErrorSchema).default([]),
  result_hash: z.string().min(1),
  created_at: z.string().min(1),
  run_ref_type: z.enum(["asset_library_build", "lifecycle_run", "package_run"]).optional(),
  run_ref_id: z.string().min(1).optional()
});

export const toolResultSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    status: toolStatusSchema,
    trace_id: z.string().min(1),
    run_id: z.string().min(1),
    data: dataSchema.optional(),
    warnings: z.array(z.string().min(1)).default([]),
    errors: z.array(toolErrorSchema).default([]),
    next_recommended_skill: z.array(z.string().min(1)).default([])
  });

export type SourceFile = z.infer<typeof sourceFileSchema>;
export type ParsedFile = z.infer<typeof parsedFileSchema>;
export type LocalFileRoute = z.infer<typeof localFileRouteSchema>;
export type LocalFile = z.infer<typeof localFileSchema>;
export type ListLocalFilesData = z.infer<typeof listLocalFilesDataSchema>;
export type ReadLocalTextFileData = z.infer<typeof readLocalTextFileDataSchema>;
export type ParserExportAsset = z.infer<typeof parserExportAssetSchema>;
export type ExtractParserTextData = z.infer<typeof extractParserTextDataSchema>;
export type RenderedPdfPage = z.infer<typeof renderedPdfPageSchema>;
export type RenderPdfPagesData = z.infer<typeof renderPdfPagesDataSchema>;
export type VisualTextOutput = z.infer<typeof visualTextOutputSchema>;
export type ExtractVisualTextData = z.infer<typeof extractVisualTextDataSchema>;
export type AssetCard = z.infer<typeof assetCardSchema>;
export type MergedAsset = z.infer<typeof mergedAssetSchema>;
export type LifecycleEvent = z.infer<typeof lifecycleEventSchema>;
export type RuleMatch = z.infer<typeof ruleMatchSchema>;
export type MissingItem = z.infer<typeof missingItemSchema>;
export type MissingItems = z.infer<typeof missingItemsSchema>;
export type Readiness = z.infer<typeof readinessSchema>;
export type PackagePlan = z.infer<typeof packagePlanSchema>;
export type GeneratedFile = z.infer<typeof generatedFileSchema>;
export type ExecutionLog = z.infer<typeof executionLogSchema>;
export type ToolError = z.infer<typeof toolErrorSchema>;
export type PipelineRunCounts = z.infer<typeof pipelineRunCountsSchema>;
export type PipelineRun = z.infer<typeof pipelineRunSchema>;
export type PipelineStep = z.infer<typeof pipelineStepSchema>;
export type PipelineRunData = z.infer<typeof pipelineRunDataSchema>;
export type ParseMaterialsData = z.infer<typeof parseMaterialsDataSchema>;
export type BuildAssetLibraryData = z.infer<typeof buildAssetLibraryDataSchema>;
export type BuildAssetLibraryDecision = BuildAssetLibraryData;
export type QueryAssetsData = z.infer<typeof queryAssetsDataSchema>;
export type ReindexLibrarySearchData = z.infer<typeof reindexLibrarySearchDataSchema>;
export type LibraryOverview = z.infer<typeof libraryOverviewSchema>;
export type ListLibrariesData = z.infer<typeof listLibrariesDataSchema>;
export type AssetChangeEvent = z.infer<typeof assetChangeEventSchema>;
export type PatchAssetCardData = z.infer<typeof patchAssetCardDataSchema>;
export type ReviewQueueData = z.infer<typeof reviewQueueDataSchema>;
export type CheckLifecycleData = z.infer<typeof checkLifecycleDataSchema>;
export type ExportLedgersData = z.infer<typeof exportLedgersDataSchema>;
export type BuildPackageData = z.infer<typeof buildPackageDataSchema>;
export type PackageRunData = z.infer<typeof packageRunDataSchema>;
export type LifecycleRunData = z.infer<typeof lifecycleRunDataSchema>;
export type SubmitDemoInput = z.infer<typeof submitDemoInputSchema>;
export type SubmitDemoData = z.infer<typeof submitDemoDataSchema>;
export type RuleProfile = z.infer<typeof ruleProfileSchema>;
export type RuleProfileBundle = z.infer<typeof ruleProfileBundleSchema>;
export type SubmissionProfile = z.infer<typeof submissionProfileSchema>;
export type RuleRequirement = z.infer<typeof ruleRequirementSchema>;
export type AgentDecisionAudit = z.infer<typeof agentDecisionAuditSchema>;
export type ValidationStatus = z.infer<typeof validationStatusSchema>;
export type AssetState = z.infer<typeof assetStateSchema>;
export type ReviewStatus = z.infer<typeof reviewStatusSchema>;
export type AgentTag = z.infer<typeof agentTagSchema>;
export type ToolResult<T> = {
  status: z.infer<typeof toolStatusSchema>;
  trace_id: string;
  run_id: string;
  data?: T;
  warnings?: string[];
  errors?: ToolError[];
  next_recommended_skill?: string[];
};

export function createTraceId(prefix = "trace"): string {
  return `${prefix}_${randomUUID().replaceAll("-", "")}`;
}

function normalizeTagFragment(value: string): string | null {
  const normalized = value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_:\-]+/gu, "_")
    .replace(/[-]+/gu, "_")
    .replace(/_{2,}/gu, "_")
    .replace(/^_+|_+$/gu, "");

  return normalized.length > 0 ? normalized : null;
}

function inferDocTag(input: {
  material_type?: string | null;
  title?: string | null;
  normalized_summary?: string | null;
}): string {
  const haystack = `${input.title ?? ""} ${input.normalized_summary ?? ""}`.toLowerCase();
  if (/简历|resume/u.test(haystack)) return "doc:resume";
  if (/成绩单|transcript/u.test(haystack)) return "doc:transcript";
  if (/在读|学籍|student.status/u.test(haystack)) return "doc:student_status";
  if (/证书|certificate|获奖/u.test(haystack)) return "doc:certificate";
  if (/身份证|护照|id.card|passport/u.test(haystack)) return "doc:identity";
  if (/发票|invoice|报销/u.test(haystack)) return "doc:invoice";
  if (/合同|协议|agreement|contract/u.test(haystack)) return "doc:agreement";
  if (input.material_type === "experience") return "doc:experience";
  if (input.material_type === "finance") return "doc:finance";
  if (input.material_type === "agreement") return "doc:agreement";
  if (input.material_type === "rights") return "doc:rights";
  return "doc:proof";
}

function inferEntityTags(input: {
  title?: string | null;
  normalized_summary?: string | null;
  material_type?: string | null;
}): string[] {
  const haystack = `${input.title ?? ""} ${input.normalized_summary ?? ""}`.toLowerCase();
  const tags = new Set<string>();

  if (/成绩单|transcript/u.test(haystack)) tags.add("entity:transcript");
  if (/四六级|cet|雅思|托福|语言/u.test(haystack)) tags.add("entity:language_certificate");
  if (/在读|学籍|student.status/u.test(haystack)) tags.add("entity:student_status_certificate");
  if (/实习|internship/u.test(haystack)) tags.add("entity:internship_experience");
  if (/项目|project/u.test(haystack)) tags.add("entity:project_experience");
  if (/竞赛|比赛|award|获奖/u.test(haystack)) tags.add("entity:award_certificate");
  if (/身份证|护照|passport|id.card/u.test(haystack)) tags.add("entity:identity_document");
  if (/发票|invoice|报销/u.test(haystack)) tags.add("entity:invoice");
  if (/合同|协议|agreement|contract/u.test(haystack)) tags.add("entity:agreement");

  if (tags.size === 0) {
    if (input.material_type === "experience") tags.add("entity:experience_record");
    else if (input.material_type === "finance") tags.add("entity:finance_record");
    else if (input.material_type === "agreement") tags.add("entity:agreement_record");
    else tags.add("entity:material_record");
  }

  return [...tags];
}

function inferRiskTag(input: {
  review_status?: string | null;
  confidence?: number | null;
}): string {
  if (input.review_status === "needs_review") {
    return "risk:needs_review";
  }
  if ((input.confidence ?? 1) < 0.75) {
    return "risk:low_confidence";
  }
  if (input.review_status === "reviewed") {
    return "risk:reviewed";
  }
  return "risk:auto";
}

type AgentTagSeed = {
  material_type?: string | null;
  title?: string | null;
  normalized_summary?: string | null;
  confidence?: number | null;
  review_status?: string | null;
  reusable_scenarios?: string[] | null;
  agent_tags?: string[] | null;
};

export function deriveReusableScenariosFromAgentTags(agentTags: string[]): string[] {
  return [...new Set(
    agentTags
      .filter((tag) => tag.startsWith("use:"))
      .map((tag) => tag.slice(4))
      .filter((tag) => tag.length > 0)
  )];
}

export function sanitizeAgentTags(input: AgentTagSeed): string[] {
  const tags = new Set<string>();
  for (const rawTag of input.agent_tags ?? []) {
    const normalized = normalizeTagFragment(rawTag);
    if (!normalized) continue;
    const parsed = agentTagSchema.safeParse(normalized);
    if (parsed.success) tags.add(parsed.data);
  }

  for (const scenario of input.reusable_scenarios ?? []) {
    const normalizedScenario = normalizeTagFragment(scenario);
    if (normalizedScenario) {
      tags.add(`use:${normalizedScenario}`);
    }
  }

  tags.add(inferDocTag(input));
  for (const entityTag of inferEntityTags(input)) {
    tags.add(entityTag);
  }
  tags.add(inferRiskTag(input));

  if (![...tags].some((tag) => tag.startsWith("use:"))) {
    tags.add("use:general_reference");
  }

  return [...tags].slice(0, 12);
}

export function buildAgentTagsText(agentTags: string[]): string {
  return [...new Set(agentTags)].join(" ");
}

export function buildAssetSearchText(input: Pick<
  AgentTagSeed,
  "material_type" | "title" | "normalized_summary" | "agent_tags"
>): string {
  return [
    input.title ?? "",
    input.normalized_summary ?? "",
    input.material_type ?? "",
    buildAgentTagsText(input.agent_tags ?? [])
  ]
    .map((value) => value.trim())
    .filter(Boolean)
    .join(" ");
}

export function createRunId(prefix = "run"): string {
  return `${prefix}_${randomUUID().replaceAll("-", "")}`;
}

export function makeToolResult<T>(
  status: ToolResult<T>["status"],
  data?: T,
  extras?: Pick<
    ToolResult<T>,
    "warnings" | "errors" | "next_recommended_skill"
  > & { trace_id?: string; run_id?: string }
): ToolResult<T> {
  return {
    status,
    trace_id: extras?.trace_id ?? createTraceId(),
    run_id: extras?.run_id ?? createRunId(),
    data,
    warnings: extras?.warnings ?? [],
    errors: extras?.errors ?? [],
    next_recommended_skill: extras?.next_recommended_skill ?? []
  };
}

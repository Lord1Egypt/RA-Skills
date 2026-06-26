import { readFile, readdir } from "node:fs/promises";
import { basename, extname, join, resolve } from "node:path";
import { z, type ZodType } from "zod";
import {
  assetCardSchema,
  checkLifecycleDataSchema,
  deriveReusableScenariosFromAgentTags,
  localFileRouteSchema,
  packagePlanSchema,
  sanitizeAgentTags,
  type AgentDecisionAudit,
  type AssetCard,
  type BuildAssetLibraryData,
  type CheckLifecycleData,
  type LocalFile,
  type LocalFileRoute,
  type MergedAsset,
  type PackagePlan,
  type ParsedFile,
  type Readiness,
  type RuleProfile,
  type ToolError
} from "@caixu/contracts";
import {
  createAgentDecisionAudit,
  type DecisionValidationResult,
  validateBuildAssetLibraryDecision,
  validateLifecycleDecision,
  validatePackagePlanDecision
} from "@caixu/rules";
import {
  fetchWithRateLimitRetry,
  type HttpRateLimitEvent
} from "./http-rate-limit.js";

const normalizedQuerySchema = z.object({
  material_types: z.array(z.string().min(1)).default([]),
  keyword: z.string().nullable().optional(),
  semantic_query: z.string().nullable().optional(),
  tag_filters_any: z.array(z.string().min(1)).default([]),
  tag_filters_all: z.array(z.string().min(1)).default([]),
  limit: z.number().int().positive().nullable().optional(),
  validity_statuses: z.array(z.string().min(1)).default([]),
  explanation: z.string().min(1),
  next_recommended_skill: z.array(z.string().min(1)).default([])
});

const singleAssetExtractionSchema = z.object({
  asset_card: assetCardSchema.nullable(),
  skip_reason: z.string().min(1).nullable()
});

const buildAssetDocumentRoleSchema = z.enum([
  "personal_proof",
  "personal_experience",
  "public_notice",
  "team_notice",
  "reference_only",
  "noise"
]);

const documentTriageSchema = z.object({
  decisions: z
    .array(
      z.object({
        file_id: z.string().min(1),
        include_in_library: z.boolean(),
        document_role: buildAssetDocumentRoleSchema.nullable(),
        reason: z.string().min(1).nullable()
      })
    )
    .default([])
});

const batchAssetExtractionSchema = z.object({
  decisions: z
    .array(
      z.object({
        file_id: z.string().min(1),
        asset_card: assetCardSchema.nullable(),
        skip_reason: z.string().min(1).nullable()
      })
    )
    .default([])
});

const ingestRouteDecisionSchema = z.object({
  decisions: z
    .array(
      z.object({
        file_id: z.string().min(1),
        route: localFileRouteSchema,
        reason: z.string().min(1).nullable()
      })
    )
    .default([])
});

type SingleAssetExtraction = z.infer<typeof singleAssetExtractionSchema>;
type DocumentTriageBatch = z.infer<typeof documentTriageSchema>;
type BatchAssetExtraction = z.infer<typeof batchAssetExtractionSchema>;
type IngestRouteDecision = z.infer<typeof ingestRouteDecisionSchema>;

export type SkillModelResponse = {
  model: string;
  content: string;
};

type SkillRunnerErrorCode =
  | "SKILL_RUNNER_MODEL_ERROR"
  | "SKILL_RUNNER_MODEL_TIMEOUT"
  | "SKILL_RUNNER_RATE_LIMITED"
  | "SKILL_RUNNER_REASONING_ONLY_RESPONSE"
  | "SKILL_RUNNER_EMPTY_CONTENT_TRUNCATED"
  | "SKILL_RUNNER_NO_MESSAGE_CONTENT"
  | "SKILL_RUNNER_JSON_PARSE_FAILED";

class SkillRunnerModelError extends Error {
  readonly code: SkillRunnerErrorCode;
  readonly retryable: boolean;

  constructor(code: SkillRunnerErrorCode, message: string, options?: { retryable?: boolean }) {
    super(message);
    this.name = "SkillRunnerModelError";
    this.code = code;
    this.retryable = options?.retryable ?? true;
  }
}

export type SkillModelClient = (input: {
  skillName: string;
  attempt: number;
  taskTitle: string;
  systemPrompt: string;
  userPrompt: string;
  maxTokens?: number;
  timeoutMs?: number;
  responseFormat?: "json_object";
  thinkingMode?: "disabled";
  doSample?: boolean;
}) => Promise<SkillModelResponse>;

export type SkillBundle = {
  skillName: string;
  skillDir: string;
  skillMarkdown: string;
  references: Array<{ name: string; content: string }>;
};

type PromptContext = {
  skillMarkdown: string;
  references: Array<{ name: string; content: string }>;
};

type PayloadPreprocessor = (payload: unknown) => unknown;

export type SkillDecisionResult<T> = {
  status: "success" | "partial" | "failed";
  data?: T;
  errors: ToolError[];
  attempts: number;
  model: string;
  rawResponse: string | null;
};

type SkillDecisionStage =
  | "ingest"
  | "build_asset_library"
  | "check_lifecycle"
  | "build_package"
  | "query_assets";

export type SkillRunnerEvent =
  | {
      source: "skill-runner";
      event:
        | "skill.attempt.start"
        | "skill.attempt.validation_failed"
        | "skill.attempt.retry_scheduled"
        | "skill.attempt.complete"
        | "skill.attempt.failed";
      stage: SkillDecisionStage;
      decision_type: string;
      skill_name: string;
      task_title: string;
      attempt: number;
      max_attempts: number;
      status: "running" | "retrying" | "success" | "failed";
      model: string | null;
      error_codes?: string[];
      validation_error_count?: number;
      next_attempt?: number;
      message: string;
    }
  | HttpRateLimitEvent;

export type BuildAssetLibrarySkillResult = {
  status: "success" | "partial" | "failed";
  data?: BuildAssetLibraryData;
  skipped_files: Array<{ file_id: string; file_name: string; reason: string }>;
  audit: AgentDecisionAudit;
  errors: ToolError[];
};

type BuildAssetDocumentRole = z.infer<typeof buildAssetDocumentRoleSchema>;

type LibraryOwnerProfile = {
  owner_name: string | null;
  aliases: string[];
  confidence: number;
  evidence_file_ids: string[];
  source: "resume" | "personal_material" | "none";
};

export type BuildAssetLibraryProgressEvent =
  | {
      phase: "triage";
      file_id: string;
      file_name: string;
      status: "success" | "skipped" | "failed";
      included_count: number;
      skipped_count: number;
      error_count: number;
    }
  | {
      phase: "extract";
      file_id: string;
      file_name: string;
      status: "success" | "skipped" | "failed";
      asset_count: number;
      skipped_count: number;
      error_count: number;
    }
  | {
      phase: "merge";
      status: "success" | "failed" | "skipped";
      merged_count: number;
      error_count: number;
    }
  | {
      phase: "complete";
      status: "success" | "partial" | "failed";
      asset_count: number;
      merged_count: number;
      skipped_count: number;
      error_count: number;
    };

export type QueryAssetsNormalization = z.infer<typeof normalizedQuerySchema>;

function toolError(code: string, message: string, extras?: Partial<ToolError>): ToolError {
  return {
    code,
    message,
    retryable: extras?.retryable,
    file_id: extras?.file_id,
    file_name: extras?.file_name,
    asset_id: extras?.asset_id
  };
}

function normalizeMessageContent(value: unknown): string {
  if (typeof value === "string") {
    return value.trim();
  }

  if (Array.isArray(value)) {
    return value
      .map((part) => {
        if (typeof part === "string") {
          return part;
        }
        if (!part || typeof part !== "object") {
          return "";
        }
        const candidate = part as { text?: unknown; content?: unknown };
        if (typeof candidate.text === "string") {
          return candidate.text;
        }
        if (typeof candidate.content === "string") {
          return candidate.content;
        }
        return "";
      })
      .join("")
      .trim();
  }

  return "";
}

function classifySkillRunnerFailure(error: unknown): ToolError {
  if (error instanceof SkillRunnerModelError) {
    return toolError(error.code, error.message, {
      retryable: error.retryable
    });
  }

  if (error instanceof Error) {
    const message = error.message || "Unknown skill runner failure";
    const lowerMessage = message.toLowerCase();

    if (
      error.name === "TimeoutError" ||
      error.name === "AbortError" ||
      lowerMessage.includes("aborted due to timeout") ||
      lowerMessage.includes("timed out")
    ) {
      return toolError("SKILL_RUNNER_MODEL_TIMEOUT", message, { retryable: true });
    }

    if (
      /\b429\b/u.test(message) ||
      lowerMessage.includes("rate limit") ||
      message.includes("速率限制")
    ) {
      return toolError("SKILL_RUNNER_RATE_LIMITED", message, { retryable: true });
    }

    if (lowerMessage.includes("did not include message content")) {
      return toolError("SKILL_RUNNER_NO_MESSAGE_CONTENT", message, {
        retryable: true
      });
    }

    if (lowerMessage.includes("invalid json")) {
      return toolError("SKILL_RUNNER_JSON_PARSE_FAILED", message, {
        retryable: true
      });
    }

    return toolError("SKILL_RUNNER_MODEL_ERROR", message, { retryable: true });
  }

  return toolError("SKILL_RUNNER_MODEL_ERROR", "Unknown skill runner failure", {
    retryable: true
  });
}

function truncate(value: string, max = 6000): string {
  return value.length <= max ? value : `${value.slice(0, max)}\n...[truncated]`;
}

function normalizeWhitespace(value: string) {
  return value.replace(/\s+/gu, " ").trim();
}

function normalizeNonEmptyString(value: unknown) {
  if (typeof value !== "string") {
    return null;
  }
  const normalized = value.trim();
  return normalized ? normalized : null;
}

function normalizeDecisionArray(payload: unknown) {
  if (!payload || typeof payload !== "object") {
    return null;
  }

  const record = payload as Record<string, unknown>;
  if (Array.isArray(record.decisions)) {
    return record.decisions;
  }

  if (record.decision && typeof record.decision === "object") {
    return [record.decision];
  }

  return null;
}

function normalizeComparisonText(value: string | null | undefined) {
  if (!value) {
    return "";
  }

  return normalizeWhitespace(value)
    .toLowerCase()
    .replace(/[，。；：、,.!?！？()（）【】\[\]{}"'“”‘’:/\\-]/gu, " ");
}

function normalizeEntityValue(value: unknown) {
  if (typeof value !== "string") {
    return null;
  }

  const normalized = normalizeWhitespace(value);
  return normalized.length > 0 ? normalized : null;
}

function isUnknownLike(value: string | null) {
  if (!value) {
    return false;
  }

  const normalized = value.trim().toLowerCase();
  return normalized === "unknown" || normalized === "n/a" || normalized === "null";
}

function hasUnmatchedClosingBracket(value: string) {
  return (value.includes(")") && !value.includes("(")) || (value.includes("）") && !value.includes("（"));
}

function isAcceptedDateValue(value: string | null) {
  if (!value) {
    return false;
  }

  return [
    /^\d{4}$/u,
    /^\d{4}-\d{2}$/u,
    /^\d{4}-\d{2}-\d{2}$/u,
    /^\d{4}年$/u,
    /^\d{4}年\d{1,2}月$/u,
    /^\d{4}年\d{1,2}月\d{1,2}日$/u
  ].some((pattern) => pattern.test(value));
}

function looksLikeBodyFragment(value: string | null) {
  if (!value) {
    return false;
  }

  if (/[，。；;:\n]/u.test(value)) {
    return true;
  }

  const fragmentMarkers = [
    "现就读",
    "并于",
    "协助",
    "组织",
    "获得",
    "荣获",
    "完成",
    "用于",
    "证明其",
    "作品",
    "在202",
    "于202"
  ];

  return fragmentMarkers.some((marker) => value.includes(marker));
}

function looksLikeOrganizationName(value: string | null) {
  if (!value) {
    return false;
  }

  if (hasUnmatchedClosingBracket(value) || looksLikeBodyFragment(value)) {
    return false;
  }

  if (/[A-Za-z]/u.test(value)) {
    return true;
  }

  const organizationMarkers = [
    "大学",
    "学院",
    "学校",
    "中学",
    "小学",
    "委员会",
    "组委会",
    "组织委员会",
    "教务处",
    "教育部",
    "协会",
    "公司",
    "有限公司",
    "实验室",
    "中心",
    "办公室",
    "政府",
    "部门",
    "科协",
    "Datawhale",
    "iFLYTEK"
  ];

  return organizationMarkers.some((marker) => value.includes(marker));
}

function looksLikeTeamLabel(value: string | null) {
  if (!value) {
    return false;
  }

  const markers = ["团队", "队伍", "小组", "战队", "工作室", "实验室", "俱乐部"];
  return markers.some((marker) => value.includes(marker));
}

function splitMultiHolderNames(value: string) {
  return value
    .split(/[、,，/]/u)
    .map((item) => normalizeWhitespace(item))
    .filter(Boolean)
    .map((item) => item.replace(/等人$/u, "").trim())
    .filter(Boolean);
}

function isLikelyChineseName(value: string | null) {
  if (!value) {
    return false;
  }
  return /^[\u4e00-\u9fff·]{2,4}$/u.test(value);
}

function looksLikePersonName(value: string | null) {
  if (!value) {
    return false;
  }

  if (looksLikeTeamLabel(value) || looksLikeOrganizationName(value) || looksLikeBodyFragment(value)) {
    return false;
  }

  if (isLikelyChineseName(value)) {
    return true;
  }

  return /^[A-Za-z][A-Za-z .'-]{1,40}$/u.test(value);
}

function nameDistance(left: string, right: string) {
  if (left === right) {
    return 0;
  }

  const maxLength = Math.max(left.length, right.length);
  if (maxLength === 0) {
    return 0;
  }

  const dp = Array.from({ length: left.length + 1 }, () =>
    Array.from({ length: right.length + 1 }, () => 0)
  );

  for (let i = 0; i <= left.length; i += 1) {
    dp[i]![0] = i;
  }
  for (let j = 0; j <= right.length; j += 1) {
    dp[0]![j] = j;
  }

  for (let i = 1; i <= left.length; i += 1) {
    for (let j = 1; j <= right.length; j += 1) {
      const cost = left[i - 1] === right[j - 1] ? 0 : 1;
      dp[i]![j] = Math.min(
        dp[i - 1]![j]! + 1,
        dp[i]![j - 1]! + 1,
        dp[i - 1]![j - 1]! + cost
      );
    }
  }

  return dp[left.length]![right.length]!;
}

function areLikelySamePersonName(left: string | null, right: string | null) {
  if (!left || !right) {
    return false;
  }

  const normalizedLeft = normalizeWhitespace(left);
  const normalizedRight = normalizeWhitespace(right);
  if (normalizedLeft === normalizedRight) {
    return true;
  }

  if (
    isLikelyChineseName(normalizedLeft) &&
    isLikelyChineseName(normalizedRight) &&
    normalizedLeft.length === normalizedRight.length
  ) {
    if (nameDistance(normalizedLeft, normalizedRight) <= 1) {
      return true;
    }

    if (
      normalizedLeft.length >= 3 &&
      normalizedRight.length >= 3 &&
      normalizedLeft.slice(-2) === normalizedRight.slice(-2)
    ) {
      return true;
    }
  }

  return false;
}

function matchesOwnerProfile(value: string | null, ownerProfile: LibraryOwnerProfile | null) {
  if (!value || !ownerProfile?.owner_name) {
    return false;
  }

  return [ownerProfile.owner_name, ...ownerProfile.aliases].some((candidate) =>
    areLikelySamePersonName(value, candidate)
  );
}

function containsOwnerName(value: string | null, ownerProfile: LibraryOwnerProfile | null) {
  if (!value || !ownerProfile?.owner_name) {
    return false;
  }

  const parts = splitMultiHolderNames(value);
  return parts.some((part) => matchesOwnerProfile(part, ownerProfile));
}

function isResumeLikeFile(file: ParsedFile) {
  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 400)}`
  );
  return /\bresume\b/u.test(haystack) || haystack.includes("简历") || haystack.includes("curriculum vitae");
}

function isPublicNoticeLikeFile(file: ParsedFile) {
  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 600)}`
  );
  const markers = ["公示", "名单", "通知", "公告", "喜报", "获奖名单", "通报"];
  return markers.some((marker) => haystack.includes(marker));
}

function isTeamLikeFile(file: ParsedFile) {
  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 600)}`
  );
  const markers = ["团队", "队伍", "小组", "等人", "team", "队"];
  return markers.some((marker) => haystack.includes(marker));
}

function fileMentionsOwnerProfile(file: ParsedFile, ownerProfile: LibraryOwnerProfile | null) {
  if (!ownerProfile?.owner_name) {
    return false;
  }

  return [file.file_name, file.extracted_summary, truncate(file.extracted_text ?? "", 800)].some(
    (value) => containsOwnerName(value ?? null, ownerProfile)
  );
}

function looksLikePersonalProofFile(file: ParsedFile) {
  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 800)}`
  );
  const markers = [
    "证书",
    "证明",
    "成绩单",
    "获奖",
    "荣誉",
    "证件",
    "资格",
    "在读",
    "四级",
    "六级",
    "结营",
    "奖学金"
  ];
  return markers.some((marker) => haystack.includes(marker));
}

function looksLikePersonalExperienceFile(file: ParsedFile) {
  if (isResumeLikeFile(file)) {
    return true;
  }

  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 800)}`
  );
  const markers = ["实习", "项目", "经历", "任职", "实践", "internship", "project experience"];
  return markers.some((marker) => haystack.includes(marker));
}

function isHighConfidenceOwnerSource(file: ParsedFile) {
  if (file.parse_status !== "parsed" || !file.extracted_text) {
    return false;
  }

  if (isPublicNoticeLikeFile(file) || isTeamLikeFile(file)) {
    return false;
  }

  if (isResumeLikeFile(file)) {
    return true;
  }

  const haystack = normalizeComparisonText(
    `${file.file_name}\n${file.extracted_summary ?? ""}\n${truncate(file.extracted_text ?? "", 600)}`
  );
  const markers = ["证书", "证明", "成绩单", "获奖", "荣誉", "四级", "六级", "结营"];
  return markers.some((marker) => haystack.includes(marker));
}

function extractOwnerNameCandidates(file: ParsedFile) {
  if (!isHighConfidenceOwnerSource(file)) {
    return [] as Array<{ name: string; score: number; source: LibraryOwnerProfile["source"]; file_id: string }>;
  }

  const text = truncate(file.extracted_text ?? "", 1600);
  const candidates: Array<{ name: string; score: number; source: LibraryOwnerProfile["source"]; file_id: string }> = [];
  const addCandidate = (name: string, score: number, source: LibraryOwnerProfile["source"]) => {
    const normalizedName = normalizeEntityValue(name);
    if (!looksLikePersonName(normalizedName)) {
      return;
    }
    candidates.push({
      name: normalizedName!,
      score,
      source,
      file_id: file.file_id
    });
  };

  if (isResumeLikeFile(file)) {
    const topLines = text
      .split(/\r?\n/u)
      .map((line) => normalizeWhitespace(line))
      .filter(Boolean)
      .slice(0, 8);
    for (const line of topLines) {
      const exactChineseName = line.match(/^([\u4e00-\u9fff·]{2,4})$/u);
      if (exactChineseName?.[1]) {
        addCandidate(exactChineseName[1], 5, "resume");
      }

      const labeledName = line.match(/^(?:姓名|name)[:：\s]+([A-Za-z][A-Za-z .'-]{1,40}|[\u4e00-\u9fff·]{2,4})$/iu);
      if (labeledName?.[1]) {
        addCandidate(labeledName[1], 4.5, "resume");
      }
    }
  }

  const genericPatterns: Array<[RegExp, number, LibraryOwnerProfile["source"]]> = [
    [/(?:姓名|name)[:：\s]+([A-Za-z][A-Za-z .'-]{1,40}|[\u4e00-\u9fff·]{2,4})/iu, 4, "personal_material"],
    [/([\u4e00-\u9fff]{2,4})同学/u, 3.5, "personal_material"],
    [/授予([\u4e00-\u9fff]{2,4})/u, 3.2, "personal_material"],
    [/(?:获奖者|学生)[:：\s]+([\u4e00-\u9fff·]{2,4})/u, 3.2, "personal_material"]
  ];

  for (const [pattern, score, source] of genericPatterns) {
    const match = text.match(pattern);
    if (match?.[1]) {
      addCandidate(match[1], score, source);
    }
  }

  return candidates;
}

function inferLibraryOwnerProfile(input: {
  parsedFiles: ParsedFile[];
  existingAssets?: AssetCard[];
}): LibraryOwnerProfile | null {
  const candidateBuckets = new Map<
    string,
    {
      canonical_name: string;
      aliases: Set<string>;
      score: number;
      evidence_file_ids: Set<string>;
      source: LibraryOwnerProfile["source"];
    }
  >();

  const absorbCandidate = (
    name: string,
    score: number,
    source: LibraryOwnerProfile["source"],
    fileId?: string
  ) => {
    let bucketKey: string | null = null;
    for (const [key, bucket] of candidateBuckets) {
      if (areLikelySamePersonName(bucket.canonical_name, name)) {
        bucketKey = key;
        break;
      }
    }

    if (!bucketKey) {
      bucketKey = name;
      candidateBuckets.set(bucketKey, {
        canonical_name: name,
        aliases: new Set([name]),
        score: 0,
        evidence_file_ids: new Set<string>(),
        source
      });
    }

    const bucket = candidateBuckets.get(bucketKey)!;
    bucket.aliases.add(name);
    bucket.score += score;
    if (fileId) {
      bucket.evidence_file_ids.add(fileId);
    }
    if (source === "resume" || bucket.source !== "resume") {
      bucket.source = source;
    }
    if (name.length > bucket.canonical_name.length || bucket.score < score) {
      bucket.canonical_name = name;
    }
  };

  for (const file of input.parsedFiles) {
    for (const candidate of extractOwnerNameCandidates(file)) {
      absorbCandidate(candidate.name, candidate.score, candidate.source, candidate.file_id);
    }
  }

  for (const asset of input.existingAssets ?? []) {
    if (!asset.holder_name || !looksLikePersonName(asset.holder_name)) {
      continue;
    }
    if (asset.material_type !== "proof" && asset.material_type !== "experience") {
      continue;
    }
    absorbCandidate(asset.holder_name, 2.5, "personal_material", asset.source_files[0]?.file_id);
  }

  const ranked = [...candidateBuckets.values()].sort((left, right) => right.score - left.score);
  const top = ranked[0];
  const second = ranked[1];
  if (!top || top.score < 4.5) {
    return null;
  }
  if (top.source !== "resume" && second && top.score - second.score < 1) {
    return null;
  }

  return {
    owner_name: top.canonical_name,
    aliases: [...top.aliases].filter((alias) => alias !== top.canonical_name),
    confidence: Math.min(0.95, Number((top.score / 8).toFixed(2))),
    evidence_file_ids: [...top.evidence_file_ids],
    source: top.source
  };
}

function buildConservativeDocumentTriageFallback(input: {
  file: ParsedFile;
  ownerProfile: LibraryOwnerProfile | null;
}) {
  if (isResumeLikeFile(input.file)) {
    return {
      includeInLibrary: true,
      documentRole: "personal_experience" as const,
      reason: "document_triage_fallback_resume"
    };
  }

  if (isPublicNoticeLikeFile(input.file)) {
    return {
      includeInLibrary: false,
      documentRole: "public_notice" as const,
      reason: "document_triage_fallback_public_notice"
    };
  }

  if (isTeamLikeFile(input.file)) {
    return {
      includeInLibrary: false,
      documentRole: "team_notice" as const,
      reason: "document_triage_fallback_team_notice"
    };
  }

  if (
    input.ownerProfile?.owner_name &&
    fileMentionsOwnerProfile(input.file, input.ownerProfile) &&
    looksLikePersonalProofFile(input.file)
  ) {
    return {
      includeInLibrary: true,
      documentRole: "personal_proof" as const,
      reason: "document_triage_fallback_personal_proof"
    };
  }

  if (
    input.ownerProfile?.owner_name &&
    fileMentionsOwnerProfile(input.file, input.ownerProfile) &&
    looksLikePersonalExperienceFile(input.file)
  ) {
    return {
      includeInLibrary: true,
      documentRole: "personal_experience" as const,
      reason: "document_triage_fallback_personal_experience"
    };
  }

  return {
    includeInLibrary: false,
    documentRole: "reference_only" as const,
    reason: "document_triage_fallback_reference_only"
  };
}

function stripExtension(fileName: string): string {
  const extension = extname(fileName);
  return extension ? fileName.slice(0, -extension.length) : fileName;
}

function firstNonEmptyLine(value: string | null | undefined): string | null {
  if (!value) {
    return null;
  }

  const lines = value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  return lines[0] ?? null;
}

function buildFallbackAssetTitle(file: ParsedFile) {
  const summaryLead = firstNonEmptyLine(file.extracted_summary);
  if (summaryLead) {
    return truncate(summaryLead, 80);
  }

  const textLead = firstNonEmptyLine(file.extracted_text);
  if (textLead) {
    return truncate(textLead, 80);
  }

  return stripExtension(file.file_name);
}

function buildFallbackNormalizedSummary(file: ParsedFile, asset: Record<string, unknown>) {
  if (typeof asset.normalized_summary === "string" && asset.normalized_summary.trim()) {
    return asset.normalized_summary.trim();
  }

  const summaryLead = firstNonEmptyLine(file.extracted_summary);
  if (summaryLead) {
    return truncate(summaryLead, 180);
  }

  const textLead = firstNonEmptyLine(file.extracted_text);
  if (textLead) {
    return truncate(textLead, 180);
  }

  const title =
    typeof asset.title === "string" && asset.title.trim()
      ? asset.title.trim()
      : stripExtension(file.file_name);
  return truncate(`${title}，待进一步确认关键字段。`, 180);
}

function defaultSensitivityLevel(materialType: unknown): "low" | "medium" | "high" {
  if (materialType === "finance" || materialType === "agreement") {
    return "high";
  }

  if (materialType === "proof" || materialType === "experience" || materialType === "rights") {
    return "medium";
  }

  return "medium";
}

function determineExtractionProfile(input: {
  file: ParsedFile;
  documentRole: BuildAssetDocumentRole | null;
}) {
  if (isResumeLikeFile(input.file)) {
    return "resume";
  }

  if (
    input.documentRole === "public_notice" ||
    input.documentRole === "team_notice" ||
    input.documentRole === "reference_only"
  ) {
    return "public_or_team_evidence";
  }

  return "personal_material";
}

function defaultMaterialTypeForExtraction(input: {
  extractionProfile: "resume" | "personal_material" | "public_or_team_evidence";
  documentRole: BuildAssetDocumentRole | null;
}) {
  if (input.extractionProfile === "resume") {
    return "experience" as const;
  }

  if (input.documentRole === "personal_experience") {
    return "experience" as const;
  }

  return "proof" as const;
}

function sanitizeIssueDate(value: unknown) {
  const normalized = normalizeEntityValue(value);
  if (!normalized || isUnknownLike(normalized) || !isAcceptedDateValue(normalized)) {
    return null;
  }
  return normalized;
}

function sanitizeIssuerName(value: unknown) {
  const normalized = normalizeEntityValue(value);
  if (!normalized || isUnknownLike(normalized)) {
    return null;
  }

  if (
    hasUnmatchedClosingBracket(normalized) ||
    looksLikeBodyFragment(normalized) ||
    normalized.length < 2 ||
    !looksLikeOrganizationName(normalized)
  ) {
    return null;
  }

  return normalized;
}

function sanitizeHolderName(input: {
  value: unknown;
  ownerProfile: LibraryOwnerProfile | null;
  documentRole: BuildAssetDocumentRole | null;
}) {
  const normalized = normalizeEntityValue(input.value);
  if (!normalized || isUnknownLike(normalized)) {
    return null;
  }

  if (looksLikeBodyFragment(normalized)) {
    return null;
  }

  const multipleNames =
    splitMultiHolderNames(normalized).length > 1 || normalized.includes("等人");
  if (multipleNames) {
    if (containsOwnerName(normalized, input.ownerProfile)) {
      return input.ownerProfile?.owner_name ?? null;
    }
    return null;
  }

  if (looksLikeTeamLabel(normalized)) {
    return containsOwnerName(normalized, input.ownerProfile)
      ? input.ownerProfile?.owner_name ?? null
      : null;
  }

  if (
    (input.documentRole === "public_notice" ||
      input.documentRole === "team_notice" ||
      input.documentRole === "reference_only") &&
    input.ownerProfile?.owner_name
  ) {
    return matchesOwnerProfile(normalized, input.ownerProfile)
      ? input.ownerProfile.owner_name
      : null;
  }

  return looksLikePersonName(normalized) ? normalized : null;
}

function sanitizeNormalizedSummary(input: {
  file: ParsedFile;
  asset: Record<string, unknown>;
  extractionProfile: "resume" | "personal_material" | "public_or_team_evidence";
}) {
  const existing = normalizeEntityValue(
    typeof input.asset.normalized_summary === "string"
      ? input.asset.normalized_summary
      : buildFallbackNormalizedSummary(input.file, input.asset)
  );
  const title = normalizeEntityValue(
    typeof input.asset.title === "string" ? input.asset.title : stripExtension(input.file.file_name)
  ) ?? stripExtension(input.file.file_name);

  if (input.extractionProfile === "resume") {
    const holder = normalizeEntityValue(input.asset.holder_name) ?? "材料持有人";
    return truncate(`${holder}的个人简历，包含教育背景、技能和项目经验。`, 120);
  }

  if (input.extractionProfile === "public_or_team_evidence") {
    return truncate(
      `这是公示/名单或团队类佐证材料，标题为“${title}”，不应视为正式签发证书。`,
      140
    );
  }

  if (!existing) {
    return truncate(`${title}，待进一步确认关键字段。`, 140);
  }

  const sanitized = existing
    .replace(/，?可用于[^，。；;]*$/u, "")
    .replace(/，?用于[^，。；;]*申请[^，。；;]*$/u, "")
    .trim();
  return truncate(sanitized || `${title}，待进一步确认关键字段。`, 140);
}

function sanitizeConfidence(input: {
  value: unknown;
  extractionProfile: "resume" | "personal_material" | "public_or_team_evidence";
  triageFallback: boolean;
}) {
  const numericValue =
    typeof input.value === "number" && Number.isFinite(input.value) ? input.value : 0.45;
  let confidence = Math.max(0, Math.min(1, numericValue));

  if (input.extractionProfile === "public_or_team_evidence") {
    confidence = Math.min(confidence, 0.55);
  }

  if (input.triageFallback) {
    confidence = Math.min(confidence, 0.6);
  }

  return Number(confidence.toFixed(2));
}

function determineReviewStatus(input: {
  asset: Record<string, unknown>;
  extractionProfile: "resume" | "personal_material" | "public_or_team_evidence";
  documentRole: BuildAssetDocumentRole | null;
  ownerProfile: LibraryOwnerProfile | null;
  triageFallback: boolean;
}) {
  if (input.extractionProfile === "public_or_team_evidence") {
    return "needs_review" as const;
  }

  const confidence =
    typeof input.asset.confidence === "number" && Number.isFinite(input.asset.confidence)
      ? input.asset.confidence
      : 0;
  if (confidence < 0.8) {
    return "needs_review" as const;
  }

  const holderName =
    typeof input.asset.holder_name === "string" && input.asset.holder_name.trim()
      ? input.asset.holder_name.trim()
      : null;
  if (
    input.ownerProfile?.owner_name &&
    (input.documentRole === "personal_proof" || input.documentRole === "personal_experience") &&
    holderName !== input.ownerProfile.owner_name
  ) {
    return "needs_review" as const;
  }

  if (input.triageFallback) {
    return "needs_review" as const;
  }

  return "auto" as const;
}

function titleFamily(value: string) {
  return normalizeComparisonText(value).replace(/\d+/gu, " ").replace(/\s+/gu, " ").trim();
}

function ngrams(value: string) {
  const normalized = value.replace(/\s+/gu, "");
  if (normalized.length < 2) {
    return new Set(normalized ? [normalized] : []);
  }

  const grams = new Set<string>();
  for (let index = 0; index < normalized.length - 1; index += 1) {
    grams.add(normalized.slice(index, index + 2));
  }
  return grams;
}

function diceSimilarity(left: string, right: string) {
  const leftGrams = ngrams(left);
  const rightGrams = ngrams(right);
  if (leftGrams.size === 0 && rightGrams.size === 0) {
    return 1;
  }
  if (leftGrams.size === 0 || rightGrams.size === 0) {
    return 0;
  }

  let overlap = 0;
  for (const gram of leftGrams) {
    if (rightGrams.has(gram)) {
      overlap += 1;
    }
  }

  return (2 * overlap) / (leftGrams.size + rightGrams.size);
}

function sameHolder(left: AssetCard, right: AssetCard, ownerProfile: LibraryOwnerProfile | null) {
  if (left.holder_name && right.holder_name) {
    return (
      areLikelySamePersonName(left.holder_name, right.holder_name) ||
      (matchesOwnerProfile(left.holder_name, ownerProfile) &&
        matchesOwnerProfile(right.holder_name, ownerProfile))
    );
  }

  if (!left.holder_name && !right.holder_name) {
    return true;
  }

  return false;
}

function isPublicOrTeamAsset(asset: AssetCard) {
  const text = normalizeComparisonText(`${asset.title} ${asset.normalized_summary}`);
  return ["公示", "名单", "通知", "公告", "喜报", "团队", "队伍", "佐证"].some((marker) =>
    text.includes(marker)
  );
}

function choosePreferredAsset(left: AssetCard, right: AssetCard) {
  const completeness = (asset: AssetCard) =>
    [asset.holder_name, asset.issuer_name, asset.issue_date, asset.expiry_date].filter(Boolean).length;
  const leftCompleteness = completeness(left);
  const rightCompleteness = completeness(right);
  if (leftCompleteness !== rightCompleteness) {
    return leftCompleteness > rightCompleteness ? left : right;
  }
  if (left.confidence !== right.confidence) {
    return left.confidence >= right.confidence ? left : right;
  }
  return left.normalized_summary.length >= right.normalized_summary.length ? left : right;
}

function computeConservativeMergedAssets(input: {
  library_id: string;
  assetCards: AssetCard[];
  ownerProfile: LibraryOwnerProfile | null;
}) {
  const usedAssetIds = new Set<string>();
  const mergedAssets: MergedAsset[] = [];

  for (let index = 0; index < input.assetCards.length; index += 1) {
    const asset = input.assetCards[index];
    if (usedAssetIds.has(asset.asset_id) || isPublicOrTeamAsset(asset)) {
      continue;
    }

    const duplicates: AssetCard[] = [asset];
    for (let nextIndex = index + 1; nextIndex < input.assetCards.length; nextIndex += 1) {
      const candidate = input.assetCards[nextIndex];
      if (usedAssetIds.has(candidate.asset_id) || isPublicOrTeamAsset(candidate)) {
        continue;
      }
      if (asset.material_type !== candidate.material_type) {
        continue;
      }
      if (!sameHolder(asset, candidate, input.ownerProfile)) {
        continue;
      }

      const resumeLike = isResumeLikeFile({
        file_id: candidate.asset_id,
        file_name: candidate.title,
        file_path: "",
        mime_type: "text/plain",
        size_bytes: 0,
        parse_status: "parsed",
        extracted_text: candidate.normalized_summary,
        extracted_summary: candidate.normalized_summary,
        provider: "local"
      }) && isResumeLikeFile({
        file_id: asset.asset_id,
        file_name: asset.title,
        file_path: "",
        mime_type: "text/plain",
        size_bytes: 0,
        parse_status: "parsed",
        extracted_text: asset.normalized_summary,
        extracted_summary: asset.normalized_summary,
        provider: "local"
      });

      const titleSimilarity = diceSimilarity(titleFamily(asset.title), titleFamily(candidate.title));
      const summarySimilarity = diceSimilarity(
        normalizeComparisonText(asset.normalized_summary),
        normalizeComparisonText(candidate.normalized_summary)
      );

      let mergeKind: "resume" | "duplicate_material" | null = null;
      if (resumeLike && titleSimilarity >= 0.88 && summarySimilarity >= 0.72) {
        mergeKind = "resume";
      } else if (
        asset.material_type === "proof" &&
        titleSimilarity >= 0.92 &&
        summarySimilarity >= 0.82 &&
        (!asset.issue_date || !candidate.issue_date || asset.issue_date === candidate.issue_date) &&
        (!asset.issuer_name ||
          !candidate.issuer_name ||
          normalizeComparisonText(asset.issuer_name) === normalizeComparisonText(candidate.issuer_name))
      ) {
        mergeKind = "duplicate_material";
      }

      if (!mergeKind) {
        continue;
      }

      duplicates.push(candidate);
    }

    if (duplicates.length < 2) {
      continue;
    }

    const selected = duplicates.reduce((best, current) => choosePreferredAsset(best, current));
    const superseded = duplicates.filter((candidate) => candidate.asset_id !== selected.asset_id);
    if (superseded.length === 0) {
      continue;
    }

    const mergedAssetId = `merged_${selected.asset_id}`;
    mergedAssets.push({
      schema_version: "1.0",
      library_id: input.library_id,
      merged_asset_id: mergedAssetId,
      canonical_asset_id: selected.asset_id,
      selected_asset_id: selected.asset_id,
      superseded_asset_ids: superseded.map((candidate) => candidate.asset_id),
      dedupe_strategy: isResumeLikeFile({
        file_id: selected.asset_id,
        file_name: selected.title,
        file_path: "",
        mime_type: "text/plain",
        size_bytes: 0,
        parse_status: "parsed",
        extracted_text: selected.normalized_summary,
        extracted_summary: selected.normalized_summary,
        provider: "local"
      })
        ? "conservative_resume_similarity"
        : "conservative_duplicate_material_similarity",
      merge_reason: "High-confidence duplicate material detected under conservative merge policy.",
      status: "merged",
      version_order: duplicates.map((candidate) => ({
        asset_id: candidate.asset_id,
        issue_date: candidate.issue_date,
        expiry_date: candidate.expiry_date,
        source_file_count: candidate.source_files.length
      }))
    });

    usedAssetIds.add(selected.asset_id);
    for (const candidate of superseded) {
      usedAssetIds.add(candidate.asset_id);
    }
  }

  return mergedAssets;
}

function normalizeAssetExtractionPayload(input: {
  payload: unknown;
  libraryId: string;
  files: ParsedFile[];
  triageByFileId?: Map<string, { documentRole: BuildAssetDocumentRole | null; reason: string | null }>;
  ownerProfile?: LibraryOwnerProfile | null;
}) {
  if (!input.payload || typeof input.payload !== "object") {
    return input.payload;
  }

  const decisions = normalizeDecisionArray(input.payload);
  if (!decisions) {
    return input.payload;
  }

  const filesById = new Map(input.files.map((file) => [file.file_id, file]));
  const decisionsByFileId = new Map<string, Record<string, unknown>>();
  for (const decision of decisions) {
    if (!decision || typeof decision !== "object") {
      continue;
    }

    const record = { ...(decision as Record<string, unknown>) };
    const fileId =
      typeof record.file_id === "string"
        ? record.file_id
        : input.files.length === 1
          ? input.files[0]?.file_id
          : undefined;

    if (!fileId || decisionsByFileId.has(fileId)) {
      continue;
    }

    record.file_id = fileId;
    decisionsByFileId.set(fileId, record);
  }

  return {
    ...(input.payload as Record<string, unknown>),
    decisions: input.files.map((file) => {
      const record: Record<string, unknown> = decisionsByFileId.get(file.file_id)
        ? { ...(decisionsByFileId.get(file.file_id) as Record<string, unknown>) }
        : { file_id: file.file_id, asset_card: null, skip_reason: "model_missing_decision" };
      const fileId = file.file_id;
      record.file_id = fileId;
      const triage = input.triageByFileId?.get(fileId) ?? null;
      const extractionProfile = determineExtractionProfile({
        file,
        documentRole: triage?.documentRole ?? null
      });
      const triageFallback = triage?.reason === "document_triage_fallback";

      if (!record.asset_card || typeof record.asset_card !== "object") {
        record.asset_card = null;
        record.skip_reason =
          normalizeNonEmptyString(record.skip_reason) ?? "model_skipped_without_reason";
        return record;
      }

      const asset = { ...(record.asset_card as Record<string, unknown>) };

      asset.schema_version = asset.schema_version ?? "1.0";
      asset.library_id = input.libraryId;
      asset.asset_id = asset.asset_id ?? `asset_${file.file_id}`;
      if (extractionProfile === "resume") {
        asset.material_type = "experience";
      } else {
        asset.material_type =
          typeof asset.material_type === "string" && asset.material_type.trim()
            ? asset.material_type
            : defaultMaterialTypeForExtraction({
                extractionProfile,
                documentRole: triage?.documentRole ?? null
              });
      }
      asset.title =
        typeof asset.title === "string" && asset.title.trim()
          ? asset.title
          : buildFallbackAssetTitle(file);
      asset.holder_name = sanitizeHolderName({
        value: asset.holder_name,
        ownerProfile: input.ownerProfile ?? null,
        documentRole: triage?.documentRole ?? null
      });
      asset.issuer_name =
        extractionProfile === "resume" ? null : sanitizeIssuerName(asset.issuer_name);
      asset.issue_date = extractionProfile === "resume" ? null : sanitizeIssueDate(asset.issue_date);
      asset.expiry_date =
        extractionProfile === "resume" ? null : sanitizeIssueDate(asset.expiry_date);
      asset.validity_status = asset.validity_status ?? "unknown";
      asset.agent_tags = sanitizeAgentTags({
        material_type: typeof asset.material_type === "string" ? asset.material_type : null,
        title: typeof asset.title === "string" ? asset.title : null,
        normalized_summary:
          typeof asset.normalized_summary === "string" ? asset.normalized_summary : null,
        confidence: typeof asset.confidence === "number" ? asset.confidence : null,
        review_status:
          typeof asset.review_status === "string" ? asset.review_status : null,
        reusable_scenarios: Array.isArray(asset.reusable_scenarios)
          ? asset.reusable_scenarios
          : [],
        agent_tags: Array.isArray(asset.agent_tags) ? asset.agent_tags : []
      });
      asset.reusable_scenarios = deriveReusableScenariosFromAgentTags(
        Array.isArray(asset.agent_tags) ? asset.agent_tags : []
      );
      asset.sensitivity_level =
        asset.sensitivity_level ?? defaultSensitivityLevel(asset.material_type);
      const sourceFiles = Array.isArray(asset.source_files) ? asset.source_files : [];
      asset.source_files =
        sourceFiles.length > 0
          ? sourceFiles
          : [
              {
                file_id: file.file_id,
                file_name: file.file_name,
                mime_type: file.mime_type,
                file_path: file.file_path
              }
            ];
      asset.confidence = sanitizeConfidence({
        value: asset.confidence,
        extractionProfile,
        triageFallback
      });
      asset.normalized_summary = sanitizeNormalizedSummary({
        file,
        asset,
        extractionProfile
      });
      asset.asset_state = "active";
      asset.review_status = determineReviewStatus({
        asset,
        extractionProfile,
        documentRole: triage?.documentRole ?? null,
        ownerProfile: input.ownerProfile ?? null,
        triageFallback
      });
      asset.agent_tags = sanitizeAgentTags(asset);
      asset.reusable_scenarios = deriveReusableScenariosFromAgentTags(
        Array.isArray(asset.agent_tags) ? asset.agent_tags : []
      );
      asset.last_verified_at =
        asset.review_status === "reviewed" ? new Date().toISOString() : null;
      const parsedAsset = assetCardSchema.safeParse(asset);
      if (!parsedAsset.success) {
        record.asset_card = null;
        record.skip_reason =
          normalizeNonEmptyString(record.skip_reason) ??
          "model_returned_incomplete_asset_card";
        return record;
      }

      record.asset_card = parsedAsset.data;
      record.skip_reason = null;
      return record;
    })
  };
}

function computeBuildAssetSummary(assetCards: AssetCard[], mergedAssets: MergedAsset[]) {
  const mergedMemberIds = new Set<string>();
  for (const merged of mergedAssets) {
    mergedMemberIds.add(merged.selected_asset_id);
    for (const supersededId of merged.superseded_asset_ids) {
      mergedMemberIds.add(supersededId);
    }
  }

  return {
    total_assets: assetCards.length,
    merged_groups: mergedAssets.length,
    anomalies: assetCards.filter(
      (asset) => asset.holder_name === null || asset.issuer_name === null
    ).length,
    unmerged_assets: assetCards.filter((asset) => !mergedMemberIds.has(asset.asset_id))
      .length
  };
}

function extractJsonPayload(raw: string): string {
  const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/u);
  if (fenced?.[1]) {
    return fenced[1].trim();
  }

  const firstBrace = raw.indexOf("{");
  const lastBrace = raw.lastIndexOf("}");
  if (firstBrace >= 0 && lastBrace > firstBrace) {
    return raw.slice(firstBrace, lastBrace + 1);
  }

  throw new Error("Model response did not contain a JSON object.");
}

function repairJsonText(raw: string): string {
  return raw
    .replace(/^\uFEFF/gu, "")
    .replace(/[\u201c\u201d]/gu, "\"")
    .replace(/[\u2018\u2019]/gu, "'")
    .replace(/,\s*([}\]])/gu, "$1")
    .trim();
}

function parseModelJsonPayload(raw: string): unknown {
  const extracted = extractJsonPayload(raw);
  const candidates = [extracted, repairJsonText(extracted)];
  let lastError: unknown = null;

  for (const candidate of candidates) {
    try {
      return JSON.parse(candidate);
    } catch (error) {
      lastError = error;
    }
  }

  if (lastError instanceof Error) {
    throw new SkillRunnerModelError(
      "SKILL_RUNNER_JSON_PARSE_FAILED",
      `Skill model returned invalid JSON: ${lastError.message}`,
      { retryable: true }
    );
  }

  throw new SkillRunnerModelError(
    "SKILL_RUNNER_JSON_PARSE_FAILED",
    "Skill model returned invalid JSON.",
    { retryable: true }
  );
}

async function readMarkdownFiles(directory: string) {
  try {
    const entries = await readdir(directory, { withFileTypes: true });
    const markdownFiles = entries
      .filter((entry) => entry.isFile() && entry.name.endsWith(".md"))
      .sort((a, b) => a.name.localeCompare(b.name));

    return Promise.all(
      markdownFiles.map(async (entry) => ({
        name: entry.name,
        content: await readFile(join(directory, entry.name), "utf8")
      }))
    );
  } catch {
    return [];
  }
}

export async function loadSkillBundle(skillDir: string): Promise<SkillBundle> {
  const resolvedDir = resolve(skillDir);
  const skillMarkdown = await readFile(join(resolvedDir, "SKILL.md"), "utf8");
  const references = await readMarkdownFiles(join(resolvedDir, "references"));
  const frontmatterMatch = skillMarkdown.match(/^---\n([\s\S]*?)\n---/u);
  const frontmatterName = frontmatterMatch?.[1]
    .split("\n")
    .map((line) => line.trim())
    .find((line) => line.startsWith("name:"))
    ?.slice("name:".length)
    .trim()
    .replace(/^['"]|['"]$/gu, "");

  return {
    skillName: frontmatterName || basename(resolvedDir),
    skillDir: resolvedDir,
    skillMarkdown,
    references
  };
}

function stripMarkdownFrontmatter(markdown: string): string {
  if (!markdown.startsWith("---\n")) {
    return markdown.trim();
  }

  const endIndex = markdown.indexOf("\n---\n", 4);
  if (endIndex === -1) {
    return markdown.trim();
  }

  return markdown.slice(endIndex + 5).trim();
}

function getMarkdownLead(markdown: string): string {
  const body = stripMarkdownFrontmatter(markdown);
  const lines = body.split("\n");
  const leadLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith("## ")) {
      break;
    }
    leadLines.push(line);
  }

  return leadLines.join("\n").trim();
}

function getMarkdownSection(markdown: string, heading: string): string {
  const body = stripMarkdownFrontmatter(markdown);
  const lines = body.split("\n");
  const targetHeading = `## ${heading}`.trim();
  const startIndex = lines.findIndex((line) => line.trim() === targetHeading);

  if (startIndex === -1) {
    return "";
  }

  const sectionLines = [lines[startIndex] ?? targetHeading];
  for (let index = startIndex + 1; index < lines.length; index += 1) {
    const line = lines[index] ?? "";
    if (line.startsWith("## ")) {
      break;
    }
    sectionLines.push(line);
  }

  return sectionLines.join("\n").trim();
}

function buildMarkdownContext(markdown: string, options: {
  includeLead?: boolean;
  headings?: string[];
}): string {
  const sections: string[] = [];
  if (options.includeLead) {
    const lead = getMarkdownLead(markdown);
    if (lead) {
      sections.push(lead);
    }
  }

  for (const heading of options.headings ?? []) {
    const section = getMarkdownSection(markdown, heading);
    if (section) {
      sections.push(section);
    }
  }

  return sections.join("\n\n").trim();
}

function buildReferenceContext(reference: { name: string; content: string }, options?: {
  headings?: string[];
}): { name: string; content: string } | null {
  if (!options?.headings || options.headings.length === 0) {
    return reference;
  }

  const content = buildMarkdownContext(reference.content, {
    headings: options.headings
  });
  if (!content) {
    return null;
  }

  return {
    name: reference.name,
    content
  };
}

function getReferenceByName(bundle: SkillBundle, name: string) {
  return bundle.references.find((reference) => reference.name === name) ?? null;
}

function createDefaultPromptContext(bundle: SkillBundle): PromptContext {
  return {
    skillMarkdown: bundle.skillMarkdown,
    references: bundle.references
  };
}

function createBuildAssetPromptContext(
  bundle: SkillBundle,
  decisionType: "document_triage" | "asset_extraction" | "merge_decision"
): PromptContext {
  const workflowReference = getReferenceByName(bundle, "workflow.md");
  const contractsReference = getReferenceByName(bundle, "tool-contracts.md");
  const failureModesReference = getReferenceByName(bundle, "failure-modes.md");
  const outputPatternsReference = getReferenceByName(bundle, "output-patterns.md");

  if (decisionType === "document_triage") {
    const triageOutputReference = outputPatternsReference
      ? buildReferenceContext(outputPatternsReference, {
          headings: ["Document triage response"]
        })
      : null;

    return {
      skillMarkdown: buildMarkdownContext(bundle.skillMarkdown, {
        includeLead: true,
        headings: ["Quick flow", "Guardrails"]
      }),
      references: [
        workflowReference,
        triageOutputReference
      ].filter((item): item is { name: string; content: string } => item !== null)
    };
  }

  if (decisionType === "asset_extraction") {
    const extractionContractsReference = contractsReference
      ? buildReferenceContext(contractsReference, {
          headings: [
            "asset_card constraints",
            "Asset extraction defaults",
            "Document category handling"
          ]
        })
      : null;
    const extractionFailureReference = failureModesReference
      ? buildReferenceContext(failureModesReference, {
          headings: ["binary_only", "Low confidence extraction", "Triage fallback"]
        })
      : null;
    const extractionOutputReference = outputPatternsReference
      ? buildReferenceContext(outputPatternsReference, {
          headings: ["Asset extraction response"]
        })
      : null;

    return {
      skillMarkdown: buildMarkdownContext(bundle.skillMarkdown, {
        includeLead: true,
        headings: ["Guardrails"]
      }),
      references: [
        extractionContractsReference,
        extractionFailureReference,
        extractionOutputReference
      ].filter((item): item is { name: string; content: string } => item !== null)
    };
  }

  const mergeReference = contractsReference
    ? buildReferenceContext(contractsReference, {
        headings: ["merged_asset constraints"]
      })
    : null;
  const mergeFailureReference = failureModesReference
    ? buildReferenceContext(failureModesReference, {
          headings: ["Merge uncertainty"]
        })
    : null;
  const mergeOutputReference = outputPatternsReference
    ? buildReferenceContext(outputPatternsReference, {
        headings: ["Merge decision response"]
      })
    : null;

  return {
    skillMarkdown: buildMarkdownContext(bundle.skillMarkdown, {
      includeLead: true,
      headings: ["Guardrails"]
    }),
    references: [
      mergeReference,
      mergeFailureReference,
      mergeOutputReference
    ].filter((item): item is { name: string; content: string } => item !== null)
  };
}

function createIngestPromptContext(
  bundle: SkillBundle,
  decisionType: "route_decision"
): PromptContext {
  const workflowReference = getReferenceByName(bundle, "workflow.md");
  const contractsReference = getReferenceByName(bundle, "tool-contracts.md");
  const failureModesReference = getReferenceByName(bundle, "failure-modes.md");
  const outputPatternsReference = getReferenceByName(bundle, "output-patterns.md");

  if (decisionType === "route_decision") {
    const contractReference = contractsReference
      ? buildReferenceContext(contractsReference, {
          headings: ["Route decision"]
        }) ?? contractsReference
      : null;
    const failureReference = failureModesReference
      ? buildReferenceContext(failureModesReference, {
          headings: ["Routing failures", "Skip policy"]
        }) ?? failureModesReference
      : null;
    const outputReference = outputPatternsReference
      ? buildReferenceContext(outputPatternsReference, {
          headings: ["Route decision response"]
        }) ?? outputPatternsReference
      : null;

    return {
      skillMarkdown: buildMarkdownContext(bundle.skillMarkdown, {
        includeLead: true,
        headings: ["Quick flow", "Guardrails"]
      }),
      references: [
        workflowReference,
        contractReference,
        failureReference,
        outputReference
      ].filter((item): item is { name: string; content: string } => item !== null)
    };
  }

  return createDefaultPromptContext(bundle);
}

function normalizeDocumentTriagePayload(input: {
  payload: unknown;
  files: ParsedFile[];
  ownerProfile?: LibraryOwnerProfile | null;
}) {
  const decisions = normalizeDecisionArray(input.payload);
  if (!decisions) {
    return input.payload;
  }

  const decisionsByFileId = new Map<string, Record<string, unknown>>();
  for (const decision of decisions) {
    if (!decision || typeof decision !== "object") {
      continue;
    }
    const record = decision as Record<string, unknown>;
    const fileId =
      typeof record.file_id === "string"
        ? record.file_id
        : input.files.length === 1
          ? input.files[0]?.file_id
          : null;
    if (!fileId || decisionsByFileId.has(fileId)) {
      continue;
    }
    decisionsByFileId.set(fileId, record);
  }

  return {
    ...(input.payload as Record<string, unknown>),
    decisions: input.files.map((file) => {
      const record = decisionsByFileId.get(file.file_id) ?? {};
      let includeInLibrary =
        typeof record.include_in_library === "boolean" ? record.include_in_library : false;
      const parsedRole = buildAssetDocumentRoleSchema.safeParse(record.document_role);
      let documentRole = includeInLibrary ? (parsedRole.success ? parsedRole.data : null) : null;
      let reason =
        includeInLibrary
          ? null
          : normalizeNonEmptyString(record.reason) ?? "model_excluded_without_reason";

      if (includeInLibrary && documentRole === null) {
        const fallback = buildConservativeDocumentTriageFallback({
          file,
          ownerProfile: input.ownerProfile ?? null
        });
        includeInLibrary = fallback.includeInLibrary;
        documentRole = fallback.documentRole;
        reason = includeInLibrary ? null : fallback.reason;
      }

      return {
        file_id: file.file_id,
        include_in_library: includeInLibrary,
        document_role: documentRole,
        reason
      };
    })
  };
}

function normalizeIngestRoutePayload(input: {
  payload: unknown;
  files: LocalFile[];
}) {
  const decisions = normalizeDecisionArray(input.payload);
  if (!decisions) {
    return input.payload;
  }

  const decisionsByFileId = new Map<string, Record<string, unknown>>();
  for (const decision of decisions) {
    if (!decision || typeof decision !== "object") {
      continue;
    }
    const record = decision as Record<string, unknown>;
    const fileId =
      typeof record.file_id === "string"
        ? record.file_id
        : input.files.length === 1
          ? input.files[0]?.file_id
          : null;
    if (!fileId || decisionsByFileId.has(fileId)) {
      continue;
    }
    decisionsByFileId.set(fileId, record);
  }

  return {
    ...(input.payload as Record<string, unknown>),
    decisions: input.files.map((file) => {
      const record = decisionsByFileId.get(file.file_id) ?? {};
      const parsedRoute = localFileRouteSchema.safeParse(record.route);
      const route = parsedRoute.success ? parsedRoute.data : file.suggested_route;
      const reason =
        route === "skip"
          ? normalizeNonEmptyString(record.reason) ??
            file.skip_reason ??
            "suggested_skip_without_reason"
          : normalizeNonEmptyString(record.reason);

      return {
        file_id: file.file_id,
        route,
        reason: route === "skip" ? reason : null
      };
    })
  };
}

export function createMockSkillModelClient(
  responder: (input: {
    skillName: string;
    attempt: number;
    taskTitle: string;
    systemPrompt: string;
    userPrompt: string;
    maxTokens?: number;
    timeoutMs?: number;
    responseFormat?: "json_object";
    thinkingMode?: "disabled";
    doSample?: boolean;
  }) => Promise<SkillModelResponse> | SkillModelResponse
): SkillModelClient {
  return async (input) => responder(input);
}

export function createOpenAICompatibleSkillModelClient(input: {
  apiKey: string;
  model: string;
  baseUrl?: string;
  extraHeaders?: Record<string, string>;
  timeoutMs?: number;
  httpMaxAttempts?: number;
  httpBaseDelayMs?: number;
  httpMaxDelayMs?: number;
  minIntervalMs?: number;
  onEvent?: (event: HttpRateLimitEvent) => void;
}): SkillModelClient {
  const baseUrl =
    input.baseUrl ?? "https://open.bigmodel.cn/api/paas/v4/chat/completions";
  const httpMaxAttempts = Math.max(1, input.httpMaxAttempts ?? 4);
  const httpBaseDelayMs = Math.max(0, input.httpBaseDelayMs ?? 2_000);
  const httpMaxDelayMs = Math.max(httpBaseDelayMs, input.httpMaxDelayMs ?? 20_000);
  const minIntervalMs = Math.max(0, input.minIntervalMs ?? 1_500);
  const scope = `skill-model:${baseUrl}:${input.model}:${input.apiKey.slice(-8)}`;

  return async ({
    skillName,
    attempt,
    taskTitle,
    systemPrompt,
    userPrompt,
    maxTokens,
    timeoutMs,
    responseFormat,
    thinkingMode,
    doSample
  }) => {
    const response = await fetchWithRateLimitRetry({
      scope,
      url: baseUrl,
      timeoutMs: timeoutMs ?? input.timeoutMs,
      maxAttempts: httpMaxAttempts,
      baseDelayMs: httpBaseDelayMs,
      maxDelayMs: httpMaxDelayMs,
      minIntervalMs,
      onEvent: input.onEvent,
      label: `Skill model request for ${skillName} (attempt ${attempt})`,
      init: {
        method: "POST",
        headers: {
          Authorization: `Bearer ${input.apiKey}`,
          "Content-Type": "application/json",
          ...input.extraHeaders
        },
        body: JSON.stringify({
          model: input.model,
          temperature: 0,
          ...(typeof doSample === "boolean" ? { do_sample: doSample } : {}),
          ...(Number.isFinite(maxTokens) && (maxTokens ?? 0) > 0
            ? { max_tokens: Math.trunc(maxTokens ?? 0) }
            : {}),
          ...(responseFormat ? { response_format: { type: responseFormat } } : {}),
          ...(thinkingMode ? { thinking: { type: thinkingMode } } : {}),
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt }
          ]
        })
      }
    });

    const payload = (await response.json()) as {
      choices?: Array<{
        finish_reason?: string | null;
        message?: {
          content?: unknown;
          reasoning_content?: unknown;
        };
      }>;
      model?: string;
    };
    const firstChoice = payload.choices?.[0];
    const content = normalizeMessageContent(firstChoice?.message?.content);
    const reasoningContent = normalizeMessageContent(
      firstChoice?.message?.reasoning_content
    );
    if (!content) {
      if (reasoningContent) {
        try {
          extractJsonPayload(reasoningContent);
          return {
            model: payload.model ?? input.model,
            content: reasoningContent
          };
        } catch {
          throw new SkillRunnerModelError(
            "SKILL_RUNNER_REASONING_ONLY_RESPONSE",
            `Skill model returned reasoning_content without final message content${firstChoice?.finish_reason ? ` (finish_reason=${firstChoice.finish_reason})` : ""}.`,
            { retryable: true }
          );
        }
      }

      if (firstChoice?.finish_reason === "length") {
        throw new SkillRunnerModelError(
          "SKILL_RUNNER_EMPTY_CONTENT_TRUNCATED",
          "Skill model response was truncated before final message content was emitted.",
          { retryable: true }
        );
      }

      throw new SkillRunnerModelError(
        "SKILL_RUNNER_NO_MESSAGE_CONTENT",
        "Skill model response did not include message content.",
        { retryable: true }
      );
    }

    return {
      model: payload.model ?? input.model,
      content
    };
  };
}

export function createSkillModelClientFromEnv(input?: {
  onEvent?: (event: HttpRateLimitEvent) => void;
}): SkillModelClient {
  const apiKey =
    process.env.CAIXU_AGENT_API_KEY?.trim() || process.env.ZHIPU_API_KEY?.trim();
  const timeoutMs = Number.parseInt(
    process.env.CAIXU_AGENT_TIMEOUT_MS?.trim() || "30000",
    10
  );
  const httpMaxAttempts = Number.parseInt(
    process.env.CAIXU_AGENT_HTTP_MAX_ATTEMPTS?.trim() || "4",
    10
  );
  const httpBaseDelayMs = Number.parseInt(
    process.env.CAIXU_AGENT_HTTP_BASE_DELAY_MS?.trim() || "2000",
    10
  );
  const httpMaxDelayMs = Number.parseInt(
    process.env.CAIXU_AGENT_HTTP_MAX_DELAY_MS?.trim() || "20000",
    10
  );
  const minIntervalMs = Number.parseInt(
    process.env.CAIXU_AGENT_MIN_INTERVAL_MS?.trim() || "1500",
    10
  );

  if (!apiKey) {
    throw new Error("CAIXU_AGENT_API_KEY or ZHIPU_API_KEY is required for live skill-runner mode.");
  }

  return createOpenAICompatibleSkillModelClient({
    apiKey,
    model: process.env.CAIXU_AGENT_MODEL?.trim() || "glm-4.6",
    baseUrl: process.env.CAIXU_AGENT_BASE_URL?.trim(),
    timeoutMs: Number.isFinite(timeoutMs) && timeoutMs > 0 ? timeoutMs : 30000,
    httpMaxAttempts:
      Number.isFinite(httpMaxAttempts) && httpMaxAttempts > 0
        ? httpMaxAttempts
        : 4,
    httpBaseDelayMs:
      Number.isFinite(httpBaseDelayMs) && httpBaseDelayMs >= 0
        ? httpBaseDelayMs
        : 2000,
    httpMaxDelayMs:
      Number.isFinite(httpMaxDelayMs) && httpMaxDelayMs >= 0
        ? httpMaxDelayMs
        : 20000,
    minIntervalMs:
      Number.isFinite(minIntervalMs) && minIntervalMs >= 0
        ? minIntervalMs
        : 1500,
    onEvent: input?.onEvent
  });
}

async function runStructuredSkillDecision<T>(input: {
  skillDir: string;
  bundle?: SkillBundle;
  modelClient: SkillModelClient;
  taskTitle: string;
  taskInput: unknown;
  outputSchema: ZodType<T>;
  maxRetries?: number;
  modelMaxTokens?: number;
  timeoutMs?: number;
  responseFormat?: "json_object";
  thinkingMode?: "disabled";
  doSample?: boolean;
  eventStage: SkillDecisionStage;
  decisionType: string;
  promptContext?: PromptContext;
  extraSystemPromptLines?: string[];
  preprocess?: PayloadPreprocessor;
  validate?: (decision: T) => DecisionValidationResult;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<SkillDecisionResult<T>> {
  const bundle = input.bundle ?? (await loadSkillBundle(input.skillDir));
  const maxAttempts = (input.maxRetries ?? 2) + 1;
  let lastErrors: ToolError[] = [];
  let lastRawResponse: string | null = null;
  let lastModel = "mock";
  const promptContext = input.promptContext ?? createDefaultPromptContext(bundle);

  const referenceText = promptContext.references
    .map((reference) => `# ${reference.name}\n${reference.content}`)
    .join("\n\n");

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const systemPrompt = [
      `You are executing the local skill package ${bundle.skillName}.`,
      "Follow the SKILL.md and local references exactly.",
      "Return only one JSON object.",
      "Do not emit reasoning, deliberation, markdown, or prose.",
      "Produce the final JSON immediately.",
      "If a field is uncertain and nullable, return null instead of guessing.",
      'Never use the literal string "unknown" when null is allowed.',
      ...(input.extraSystemPromptLines ?? [])
    ].join(" ");

    const retryFeedback =
      lastErrors.length > 0
        ? `\n\nValidation feedback from previous attempt:\n${JSON.stringify(lastErrors, null, 2)}`
        : "";
    const reasoningOnlyRetryInstruction = lastErrors.some(
      (error) => error.code === "SKILL_RUNNER_REASONING_ONLY_RESPONSE"
    )
      ? "\n\nCritical retry instruction:\nThe previous attempt returned reasoning without a final JSON object. On this retry, output the final JSON object immediately. Start with '{' and end with '}'. Do not emit any reasoning."
      : "";

    const userPrompt = [
      `Task: ${input.taskTitle}`,
      "",
      "## Skill",
      promptContext.skillMarkdown,
      "",
      "## References",
      referenceText || "(no local references)",
      "",
      "## Input",
      JSON.stringify(input.taskInput),
      retryFeedback,
      reasoningOnlyRetryInstruction,
      "",
      "## Output requirement",
      "Return a single JSON object and nothing else."
    ].join("\n");

    input.onEvent?.({
      source: "skill-runner",
      event: "skill.attempt.start",
      stage: input.eventStage,
      decision_type: input.decisionType,
      skill_name: bundle.skillName,
      task_title: input.taskTitle,
      attempt,
      max_attempts: maxAttempts,
      status: "running",
      model: lastModel === "mock" ? null : lastModel,
      message: `Starting ${input.decisionType} attempt ${attempt}/${maxAttempts}.`
    });

    try {
      const response = await input.modelClient({
        skillName: bundle.skillName,
        attempt,
        taskTitle: input.taskTitle,
        systemPrompt,
        userPrompt,
        maxTokens: input.modelMaxTokens,
        timeoutMs: input.timeoutMs,
        responseFormat: input.responseFormat,
        thinkingMode: input.thinkingMode,
        doSample: input.doSample
      });
      lastModel = response.model;
      lastRawResponse = response.content;

      const jsonPayload = parseModelJsonPayload(response.content);
      const normalizedPayload = input.preprocess ? input.preprocess(jsonPayload) : jsonPayload;
      const parsed = input.outputSchema.safeParse(normalizedPayload);
      if (!parsed.success) {
        lastErrors = [
          toolError(
            "SKILL_RUNNER_SCHEMA_INVALID",
            parsed.error.issues
              .map(
                (issue: z.ZodIssue) =>
                  `${issue.path.join(".") || "root"}: ${issue.message}`
              )
              .join("; ")
          )
        ];
        input.onEvent?.({
          source: "skill-runner",
          event: "skill.attempt.validation_failed",
          stage: input.eventStage,
          decision_type: input.decisionType,
          skill_name: bundle.skillName,
          task_title: input.taskTitle,
          attempt,
          max_attempts: maxAttempts,
          status: "failed",
          model: response.model,
          error_codes: ["SKILL_RUNNER_SCHEMA_INVALID"],
          validation_error_count: parsed.error.issues.length,
          message: `Schema validation failed for ${input.decisionType} on attempt ${attempt}.`
        });
        if (attempt < maxAttempts) {
          input.onEvent?.({
            source: "skill-runner",
            event: "skill.attempt.retry_scheduled",
            stage: input.eventStage,
            decision_type: input.decisionType,
            skill_name: bundle.skillName,
            task_title: input.taskTitle,
            attempt,
            max_attempts: maxAttempts,
            status: "retrying",
            model: response.model,
            error_codes: ["SKILL_RUNNER_SCHEMA_INVALID"],
            validation_error_count: parsed.error.issues.length,
            next_attempt: attempt + 1,
            message: `Retry scheduled for ${input.decisionType} after schema validation failure.`
          });
        }
        continue;
      }

      if (input.validate) {
        const validation = input.validate(parsed.data);
        if (validation.status !== "passed") {
          lastErrors = validation.errors;
          input.onEvent?.({
            source: "skill-runner",
            event: "skill.attempt.validation_failed",
            stage: input.eventStage,
            decision_type: input.decisionType,
            skill_name: bundle.skillName,
            task_title: input.taskTitle,
            attempt,
            max_attempts: maxAttempts,
            status: "failed",
            model: response.model,
            error_codes: validation.errors.map((error) => error.code),
            validation_error_count: validation.errors.length,
            message: `Decision validation failed for ${input.decisionType} on attempt ${attempt}.`
          });
          if (attempt < maxAttempts) {
            input.onEvent?.({
              source: "skill-runner",
              event: "skill.attempt.retry_scheduled",
              stage: input.eventStage,
              decision_type: input.decisionType,
              skill_name: bundle.skillName,
              task_title: input.taskTitle,
              attempt,
              max_attempts: maxAttempts,
              status: "retrying",
              model: response.model,
              error_codes: validation.errors.map((error) => error.code),
              validation_error_count: validation.errors.length,
              next_attempt: attempt + 1,
              message: `Retry scheduled for ${input.decisionType} after decision validation failure.`
            });
          }
          continue;
        }
      }

      input.onEvent?.({
        source: "skill-runner",
        event: "skill.attempt.complete",
        stage: input.eventStage,
        decision_type: input.decisionType,
        skill_name: bundle.skillName,
        task_title: input.taskTitle,
        attempt,
        max_attempts: maxAttempts,
        status: "success",
        model: response.model,
        message: `Completed ${input.decisionType} on attempt ${attempt}.`
      });
      return {
        status: "success",
        data: parsed.data,
        errors: [],
        attempts: attempt,
        model: response.model,
        rawResponse: response.content
      };
    } catch (error) {
      lastErrors = [classifySkillRunnerFailure(error)];
      if (attempt < maxAttempts) {
        input.onEvent?.({
          source: "skill-runner",
          event: "skill.attempt.retry_scheduled",
          stage: input.eventStage,
          decision_type: input.decisionType,
          skill_name: bundle.skillName,
          task_title: input.taskTitle,
          attempt,
          max_attempts: maxAttempts,
          status: "retrying",
          model: lastModel === "mock" ? null : lastModel,
          error_codes: lastErrors.map((item) => item.code),
          next_attempt: attempt + 1,
          message: `Retry scheduled for ${input.decisionType} after model error on attempt ${attempt}.`
        });
      }
    }
  }

  input.onEvent?.({
    source: "skill-runner",
    event: "skill.attempt.failed",
    stage: input.eventStage,
    decision_type: input.decisionType,
    skill_name: bundle.skillName,
    task_title: input.taskTitle,
    attempt: maxAttempts,
    max_attempts: maxAttempts,
    status: "failed",
    model: lastModel === "mock" ? null : lastModel,
    error_codes: lastErrors.map((error) => error.code),
    validation_error_count: lastErrors.length,
    message: `Exhausted ${maxAttempts} attempt(s) for ${input.decisionType}.`
  });

  return {
    status: "failed",
    errors: lastErrors,
    attempts: maxAttempts,
    model: lastModel,
    rawResponse: lastRawResponse
  };
}

function isPublicOrTeamDocumentRole(role: BuildAssetDocumentRole | null) {
  return role === "public_notice" || role === "team_notice" || role === "reference_only";
}

function isResumeAsset(input: {
  file: ParsedFile;
  asset: AssetCard;
  documentRole: BuildAssetDocumentRole | null;
}) {
  return (
    input.documentRole === "personal_experience" &&
    isResumeLikeFile(input.file) &&
    input.asset.title.includes("简历")
  );
}

function isDirtyHolderValue(value: string | null) {
  if (!value) {
    return false;
  }

  return looksLikeTeamLabel(value) || looksLikeBodyFragment(value) || !looksLikePersonName(value);
}

function isDirtyIssuerValue(value: string | null) {
  if (!value) {
    return false;
  }

  return !looksLikeOrganizationName(value);
}

function summarizeAsset(asset: AssetCard) {
  return {
    asset_id: asset.asset_id,
    material_type: asset.material_type,
    title: asset.title,
    holder_name: asset.holder_name,
    issuer_name: asset.issuer_name,
    issue_date: asset.issue_date,
    agent_tags: asset.agent_tags,
    reusable_scenarios: asset.reusable_scenarios,
    confidence: asset.confidence,
    normalized_summary: asset.normalized_summary
  };
}

function validateSingleAssetExtraction(input: {
  library_id: string;
  file: ParsedFile;
  asset_card: AssetCard | null;
  skip_reason: string | null;
  documentRole: BuildAssetDocumentRole | null;
  ownerProfile: LibraryOwnerProfile | null;
}): DecisionValidationResult {
  const errors: ToolError[] = [];

  if (input.asset_card === null) {
    if (!input.skip_reason) {
      errors.push(
        toolError(
          "BUILD_ASSET_EXTRACTION_SKIP_REASON_MISSING",
          `File ${input.file.file_name} returned no asset_card and no skip_reason.`,
          { file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }
    return { status: errors.length > 0 ? "failed" : "passed", errors };
  }

  const asset = input.asset_card;

  if (asset.library_id !== input.library_id) {
    errors.push(
      toolError(
        "BUILD_ASSET_EXTRACTION_LIBRARY_ID_MISMATCH",
        `Expected library_id ${input.library_id}, received ${asset.library_id}.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (
    !asset.source_files.some(
      (file: AssetCard["source_files"][number]) => file.file_id === input.file.file_id
    )
  ) {
    errors.push(
      toolError(
        "BUILD_ASSET_EXTRACTION_SOURCE_FILE_MISSING",
        `Asset ${asset.asset_id} must reference source file ${input.file.file_id}.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (asset.holder_name === "unknown" || asset.issuer_name === "unknown") {
    errors.push(
      toolError(
        "BUILD_ASSET_EXTRACTION_UNKNOWN_STRING_FORBIDDEN",
        `Asset ${asset.asset_id} must use null instead of "unknown".`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (isResumeAsset({ file: input.file, asset, documentRole: input.documentRole })) {
    if (asset.material_type !== "experience") {
      errors.push(
        toolError(
          "BUILD_ASSET_RESUME_MATERIAL_TYPE_INVALID",
          `Resume-like asset ${asset.asset_id} must use material_type=experience.`,
          { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }

    if (
      asset.issuer_name !== null ||
      asset.issue_date !== null ||
      asset.expiry_date !== null
    ) {
      errors.push(
        toolError(
          "BUILD_ASSET_RESUME_FIELDS_MUST_BE_NULL",
          `Resume-like asset ${asset.asset_id} must not carry issuer/date fields.`,
          { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }
  }

  if (asset.holder_name && isDirtyHolderValue(asset.holder_name)) {
    errors.push(
      toolError(
        "BUILD_ASSET_CARD_HOLDER_DIRTY_VALUE",
        `Asset ${asset.asset_id} contains a suspicious holder_name value.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (asset.issuer_name && isDirtyIssuerValue(asset.issuer_name)) {
    errors.push(
      toolError(
        "BUILD_ASSET_CARD_ISSUER_DIRTY_VALUE",
        `Asset ${asset.asset_id} contains a suspicious issuer_name value.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (asset.issue_date && !isAcceptedDateValue(asset.issue_date)) {
    errors.push(
      toolError(
        "BUILD_ASSET_CARD_ISSUE_DATE_INVALID",
        `Asset ${asset.asset_id} contains a non-date issue_date value.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (
    input.ownerProfile?.owner_name &&
    !isPublicOrTeamDocumentRole(input.documentRole) &&
    asset.holder_name &&
    !matchesOwnerProfile(asset.holder_name, input.ownerProfile)
  ) {
    errors.push(
      toolError(
        "BUILD_ASSET_CARD_OWNER_MISMATCH",
        `Asset ${asset.asset_id} does not appear to belong to the inferred owner ${input.ownerProfile.owner_name}.`,
        { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
      )
    );
  }

  if (isPublicOrTeamDocumentRole(input.documentRole)) {
    if (
      !input.ownerProfile?.owner_name ||
      !asset.holder_name ||
      asset.holder_name !== input.ownerProfile.owner_name
    ) {
      errors.push(
        toolError(
          "BUILD_ASSET_PUBLIC_NOTICE_OWNER_REQUIRED",
          `Notice/team evidence ${asset.asset_id} must map uniquely to the inferred owner before entering the library.`,
          { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }

    if (asset.confidence > 0.6) {
      errors.push(
        toolError(
          "BUILD_ASSET_PUBLIC_NOTICE_CONFIDENCE_TOO_HIGH",
          `Notice/team evidence ${asset.asset_id} must keep conservative confidence.`,
          { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }

    if (!["公示", "名单", "佐证", "团队", "通报"].some((marker) => asset.normalized_summary.includes(marker))) {
      errors.push(
        toolError(
          "BUILD_ASSET_PUBLIC_NOTICE_SUMMARY_MISSING_CONTEXT",
          `Notice/team evidence ${asset.asset_id} must explicitly say it is notice/list/team evidence.`,
          { asset_id: asset.asset_id, file_id: input.file.file_id, file_name: input.file.file_name }
        )
      );
    }
  }

  return { status: errors.length > 0 ? "failed" : "passed", errors };
}

function validateDocumentTriageDecision(input: {
  files: ParsedFile[];
  decision: DocumentTriageBatch;
}): DecisionValidationResult {
  const errors: ToolError[] = [];
  const filesById = new Map(input.files.map((file) => [file.file_id, file]));
  const seenFileIds = new Set<string>();

  for (const item of input.decision.decisions) {
    const file = filesById.get(item.file_id);
    if (!file) {
      errors.push(
        toolError(
          "BUILD_ASSET_TRIAGE_UNKNOWN_FILE_ID",
          `Document triage references unknown file_id ${item.file_id}.`,
          { file_id: item.file_id }
        )
      );
      continue;
    }

    if (seenFileIds.has(item.file_id)) {
      errors.push(
        toolError(
          "BUILD_ASSET_TRIAGE_DUPLICATE_FILE_ID",
          `Document triage contains duplicate file_id ${item.file_id}.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
      continue;
    }

    seenFileIds.add(item.file_id);

    if (item.include_in_library && item.document_role === null) {
      errors.push(
        toolError(
          "BUILD_ASSET_TRIAGE_DOCUMENT_ROLE_MISSING",
          `Document triage must assign a document_role for included file ${file.file_name}.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
    }

    if (!item.include_in_library && !item.reason) {
      errors.push(
        toolError(
          "BUILD_ASSET_TRIAGE_REASON_MISSING",
          `Document triage must explain why ${file.file_name} is excluded from the asset library.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
    }
  }

  for (const file of input.files) {
    if (!seenFileIds.has(file.file_id)) {
      errors.push(
        toolError(
          "BUILD_ASSET_TRIAGE_FILE_DECISION_MISSING",
          `No triage decision was returned for ${file.file_name}.`,
          { file_id: file.file_id, file_name: file.file_name }
        )
      );
    }
  }

  return { status: errors.length > 0 ? "failed" : "passed", errors };
}

function validateIngestRouteDecision(input: {
  files: LocalFile[];
  decision: IngestRouteDecision;
}): DecisionValidationResult {
  const errors: ToolError[] = [];
  const filesById = new Map(input.files.map((file) => [file.file_id, file]));
  const seenFileIds = new Set<string>();

  for (const item of input.decision.decisions) {
    const file = filesById.get(item.file_id);
    if (!file) {
      errors.push(
        toolError(
          "INGEST_ROUTE_UNKNOWN_FILE_ID",
          `Route decision references unknown file_id ${item.file_id}.`,
          { file_id: item.file_id }
        )
      );
      continue;
    }

    if (seenFileIds.has(item.file_id)) {
      errors.push(
        toolError(
          "INGEST_ROUTE_DUPLICATE_FILE_ID",
          `Route decision contains duplicate file_id ${item.file_id}.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
      continue;
    }
    seenFileIds.add(item.file_id);

    if (item.route === "skip" && !item.reason) {
      errors.push(
        toolError(
          "INGEST_ROUTE_SKIP_REASON_MISSING",
          `Route decision must explain why ${file.file_name} is skipped.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
    }

    if (file.suggested_route === "skip" && item.route !== "skip") {
      errors.push(
        toolError(
          "INGEST_ROUTE_FORCED_UNSUPPORTED_TYPE",
          `Unsupported or low-value file ${file.file_name} must be skipped.`,
          { file_id: item.file_id, file_name: file.file_name }
        )
      );
    }
  }

  for (const file of input.files) {
    if (!seenFileIds.has(file.file_id)) {
      errors.push(
        toolError(
          "INGEST_ROUTE_FILE_DECISION_MISSING",
          `No route decision was returned for ${file.file_name}.`,
          { file_id: file.file_id, file_name: file.file_name }
        )
      );
    }
  }

  return { status: errors.length > 0 ? "failed" : "passed", errors };
}

function shouldFallbackDocumentTriage(errors: ToolError[]) {
  const recoverableCodes = new Set<string>([
    "SKILL_RUNNER_REASONING_ONLY_RESPONSE",
    "SKILL_RUNNER_EMPTY_CONTENT_TRUNCATED",
    "SKILL_RUNNER_NO_MESSAGE_CONTENT",
    "SKILL_RUNNER_MODEL_TIMEOUT",
    "SKILL_RUNNER_RATE_LIMITED",
    "SKILL_RUNNER_MODEL_ERROR"
  ]);

  return errors.length > 0 && errors.every((error) => recoverableCodes.has(error.code));
}

function validateBatchAssetExtraction(input: {
  library_id: string;
  files: ParsedFile[];
  decisions: BatchAssetExtraction["decisions"];
  triageByFileId: Map<string, { documentRole: BuildAssetDocumentRole | null; reason: string | null }>;
  ownerProfile: LibraryOwnerProfile | null;
}): DecisionValidationResult {
  const errors: ToolError[] = [];
  const filesById = new Map(input.files.map((file) => [file.file_id, file]));
  const seenFileIds = new Set<string>();

  for (const decision of input.decisions) {
    const file = filesById.get(decision.file_id);
    if (!file) {
      errors.push(
        toolError(
          "BUILD_ASSET_EXTRACTION_UNKNOWN_FILE_ID",
          `Decision references unknown file_id ${decision.file_id}.`,
          { file_id: decision.file_id }
        )
      );
      continue;
    }

    if (seenFileIds.has(decision.file_id)) {
      errors.push(
        toolError(
          "BUILD_ASSET_EXTRACTION_DUPLICATE_FILE_ID",
          `Decision contains duplicate file_id ${decision.file_id}.`,
          { file_id: decision.file_id, file_name: file.file_name }
        )
      );
      continue;
    }

    seenFileIds.add(decision.file_id);

    const validation = validateSingleAssetExtraction({
      library_id: input.library_id,
      file,
      asset_card: decision.asset_card,
      skip_reason: decision.skip_reason,
      documentRole: input.triageByFileId.get(decision.file_id)?.documentRole ?? null,
      ownerProfile: input.ownerProfile
    });
    errors.push(...validation.errors);
  }

  for (const file of input.files) {
    if (!seenFileIds.has(file.file_id)) {
      errors.push(
        toolError(
          "BUILD_ASSET_EXTRACTION_FILE_DECISION_MISSING",
          `No extraction decision was returned for ${file.file_name}.`,
          { file_id: file.file_id, file_name: file.file_name }
        )
      );
    }
  }

  return { status: errors.length > 0 ? "failed" : "passed", errors };
}

export async function runBuildAssetLibrarySkill(input: {
  skillDir: string;
  library_id: string;
  parsed_files: ParsedFile[];
  parsed_file_context?: ParsedFile[];
  modelClient: SkillModelClient;
  maxRetries?: number;
  existing_asset_ids?: string[];
  existing_assets?: AssetCard[];
  onProgress?: (event: BuildAssetLibraryProgressEvent) => void;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<BuildAssetLibrarySkillResult> {
  const bundle = await loadSkillBundle(input.skillDir);
  const assetCards: AssetCard[] = [];
  const skippedFiles: Array<{ file_id: string; file_name: string; reason: string }> = [];
  const errors: ToolError[] = [];
  let modelUsed = "mock";
  const eligibleFiles: ParsedFile[] = [];
  const triagedInclusion = new Map<
    string,
    { includeInLibrary: boolean; documentRole: BuildAssetDocumentRole | null; reason: string | null }
  >();
  const ownerProfile = inferLibraryOwnerProfile({
    parsedFiles: [...(input.parsed_file_context ?? []), ...input.parsed_files],
    existingAssets: input.existing_assets ?? []
  });

  for (const file of input.parsed_files) {
    if (file.parse_status !== "parsed" || !file.extracted_text) {
      skippedFiles.push({
        file_id: file.file_id,
        file_name: file.file_name,
        reason: "no_trustworthy_text"
      });
      input.onProgress?.({
        phase: "triage",
        file_id: file.file_id,
        file_name: file.file_name,
        status: "skipped",
        included_count: eligibleFiles.length,
        skipped_count: skippedFiles.length,
        error_count: errors.length
      });
      continue;
    }
    eligibleFiles.push(file);
  }

  const includedFiles: ParsedFile[] = [];

  if (eligibleFiles.length > 0) {
    const triage = await runStructuredSkillDecision<DocumentTriageBatch>({
      skillDir: input.skillDir,
      modelClient: input.modelClient,
      taskTitle: "Decide which parsed files should enter the asset library and assign a conservative document role.",
      taskInput: {
        library_id: input.library_id,
        owner_profile: ownerProfile,
        files: eligibleFiles.map((file) => ({
          file_id: file.file_id,
          file_name: file.file_name,
          mime_type: file.mime_type,
          extracted_summary: file.extracted_summary,
          text_preview: truncate(file.extracted_text ?? "", 360)
        })),
        constraints: {
          include_only_if_material_is_actionable_for_personal_library: true,
          infer_personal_owner_only_from_high_confidence_personal_materials: true,
          do_not_guess_from_filename_only: true,
          allowed_document_roles: [
            "personal_proof",
            "personal_experience",
            "public_notice",
            "team_notice",
            "reference_only",
            "noise"
          ],
          include_public_notice_only_when_owner_is_uniquely_supported: true,
          include_team_material_only_when_owner_participation_is_clear: true,
          when_uncertain_exclude_from_library: true,
          excluded_files_must_include_reason: true
        }
      },
      outputSchema: documentTriageSchema,
      maxRetries: input.maxRetries,
      modelMaxTokens: 220,
      responseFormat: "json_object",
      thinkingMode: "disabled",
      doSample: false,
      eventStage: "build_asset_library",
      decisionType: "document_triage",
      bundle,
    promptContext: createBuildAssetPromptContext(bundle, "document_triage"),
    extraSystemPromptLines: [
      "This is a compact routing task for a single-owner personal asset library.",
      "Return exactly one decision per input file.",
      "Every returned decision must include reason; use null when include_in_library=true.",
      "Use document_role only from the allowed internal categories.",
      "If uncertain, exclude the file from the library instead of guessing.",
      "Public notices, team notices, and reference-only materials must not enter the personal library unless the owner can be linked conservatively.",
      "Do not include files that only provide generic public context."
    ],
    onEvent: input.onEvent,
    preprocess: (payload) =>
      normalizeDocumentTriagePayload({
        payload,
        files: eligibleFiles,
        ownerProfile
      }),
    validate: (decision: DocumentTriageBatch) =>
      validateDocumentTriageDecision({
        files: eligibleFiles,
        decision
      })
    });

    modelUsed = triage.model;

    if (triage.status === "success" && triage.data) {
      const decisionsByFileId = new Map(
        triage.data.decisions.map((decision) => [decision.file_id, decision])
      );

      for (const file of eligibleFiles) {
        const decision = decisionsByFileId.get(file.file_id);
        if (!decision) {
          errors.push(
            toolError(
              "BUILD_ASSET_TRIAGE_FILE_DECISION_MISSING",
              `No triage decision was returned for ${file.file_name}.`,
              { file_id: file.file_id, file_name: file.file_name }
            )
          );
          skippedFiles.push({
            file_id: file.file_id,
            file_name: file.file_name,
            reason: "document_triage_missing"
          });
          input.onProgress?.({
            phase: "triage",
            file_id: file.file_id,
            file_name: file.file_name,
            status: "failed",
            included_count: includedFiles.length,
            skipped_count: skippedFiles.length,
            error_count: errors.length
          });
          continue;
        }

        triagedInclusion.set(file.file_id, {
          includeInLibrary: decision.include_in_library,
          documentRole: decision.document_role,
          reason: decision.reason
        });

        if (decision.include_in_library) {
          includedFiles.push(file);
          input.onProgress?.({
            phase: "triage",
            file_id: file.file_id,
            file_name: file.file_name,
            status: "success",
            included_count: includedFiles.length,
            skipped_count: skippedFiles.length,
            error_count: errors.length
          });
          continue;
        }

        skippedFiles.push({
          file_id: file.file_id,
          file_name: file.file_name,
          reason: decision.reason ?? decision.document_role ?? "document_triage_excluded"
        });
        input.onProgress?.({
          phase: "triage",
          file_id: file.file_id,
          file_name: file.file_name,
          status: "skipped",
          included_count: includedFiles.length,
          skipped_count: skippedFiles.length,
          error_count: errors.length
        });
      }
    } else if (shouldFallbackDocumentTriage(triage.errors)) {
      errors.push(...triage.errors);

      for (const file of eligibleFiles) {
        const fallbackDecision = buildConservativeDocumentTriageFallback({
          file,
          ownerProfile
        });
        triagedInclusion.set(file.file_id, {
          includeInLibrary: fallbackDecision.includeInLibrary,
          documentRole: fallbackDecision.documentRole,
          reason: fallbackDecision.reason
        });
        if (fallbackDecision.includeInLibrary) {
          includedFiles.push(file);
          input.onProgress?.({
            phase: "triage",
            file_id: file.file_id,
            file_name: file.file_name,
            status: "success",
            included_count: includedFiles.length,
            skipped_count: skippedFiles.length,
            error_count: errors.length
          });
          continue;
        }

        skippedFiles.push({
          file_id: file.file_id,
          file_name: file.file_name,
          reason: fallbackDecision.reason
        });
        input.onProgress?.({
          phase: "triage",
          file_id: file.file_id,
          file_name: file.file_name,
          status: "skipped",
          included_count: includedFiles.length,
          skipped_count: skippedFiles.length,
          error_count: errors.length
        });
      }
    } else {
      for (const file of eligibleFiles) {
        errors.push(
          ...triage.errors.map((error) => ({
            ...error,
            file_id: error.file_id ?? file.file_id,
            file_name: error.file_name ?? file.file_name
          }))
        );
        skippedFiles.push({
          file_id: file.file_id,
          file_name: file.file_name,
          reason: "document_triage_failed"
        });
        input.onProgress?.({
          phase: "triage",
          file_id: file.file_id,
          file_name: file.file_name,
          status: "failed",
          included_count: includedFiles.length,
          skipped_count: skippedFiles.length,
          error_count: errors.length
        });
      }
    }
  }

  if (includedFiles.length > 0) {
    const extraction = await runStructuredSkillDecision<BatchAssetExtraction>({
      skillDir: input.skillDir,
      modelClient: input.modelClient,
      taskTitle: "Extract canonical asset_cards for triaged files that should enter the asset library.",
      taskInput: {
        library_id: input.library_id,
        files: includedFiles.map((file) => {
          const triageHint = triagedInclusion.get(file.file_id);
          return {
            file_id: file.file_id,
            file_name: file.file_name,
            mime_type: file.mime_type,
            document_role_hint: triageHint?.documentRole ?? null,
            triage_reason: triageHint?.reason ?? null,
            extraction_profile: determineExtractionProfile({
              file,
              documentRole: triageHint?.documentRole ?? null
            }),
            extracted_summary: file.extracted_summary,
            text_preview: truncate(file.extracted_text ?? "", 900)
          };
        }),
        owner_profile: ownerProfile
          ? {
              owner_name: ownerProfile.owner_name,
              aliases: ownerProfile.aliases
            }
          : null,
        constraints: {
          allow_null_fields: ["holder_name", "issuer_name", "issue_date", "expiry_date"],
          forbid_unknown_string: true,
          forbid_guessing_from_filename_only: true,
          at_most_one_asset_per_file: true,
          schema_version_must_be: "1.0",
          default_validity_status_when_uncertain: "unknown",
          prefer_short_title_and_summary: true,
          agent_tags: {
            required: true,
            min_count: 4,
            max_count: 12,
            allowed_prefixes: ["doc", "use", "entity", "risk"],
            lowercase_ascii_only: true
          }
        }
      },
      outputSchema: batchAssetExtractionSchema,
      maxRetries: input.maxRetries,
      modelMaxTokens: 320,
      timeoutMs: 60_000,
      responseFormat: "json_object",
      thinkingMode: "disabled",
      doSample: false,
      eventStage: "build_asset_library",
      decisionType: "asset_extraction",
      bundle,
      promptContext: createBuildAssetPromptContext(bundle, "asset_extraction"),
      extraSystemPromptLines: [
        "This is a compact extraction task.",
        "Return exactly one decision per input file.",
        "Every decision must include skip_reason; use null when asset_card is present.",
        "If asset_card is present, include every required asset_card field.",
        "If you cannot produce a truthful canonical asset_card, return asset_card as null and provide skip_reason.",
        "Do not omit schema_version, title, validity_status, sensitivity_level, source_files, or normalized_summary.",
        "If asset_card is present, include agent_tags using only doc:/use:/entity:/risk: namespaces.",
        "Do not emit unknown, long sentences, or free-text labels in agent_tags.",
        "For resume inputs, material_type must be experience and issuer/date fields must be null.",
        "For public/team evidence, only keep the asset if it can be mapped uniquely to the library owner.",
        "Do not keep team names or public notices as holder_name values."
      ],
      preprocess: (payload) =>
        normalizeAssetExtractionPayload({
          payload,
          libraryId: input.library_id,
          files: includedFiles,
          triageByFileId: triagedInclusion,
          ownerProfile
        }),
      onEvent: input.onEvent,
      validate: (decision: BatchAssetExtraction) =>
        validateBatchAssetExtraction({
          library_id: input.library_id,
          files: includedFiles,
          decisions: decision.decisions,
          triageByFileId: triagedInclusion,
          ownerProfile
        })
    });

    modelUsed = extraction.model;

    if (extraction.status === "success" && extraction.data) {
      const decisionsByFileId = new Map(
        extraction.data.decisions.map((decision) => [decision.file_id, decision])
      );

      for (const file of includedFiles) {
        const decision = decisionsByFileId.get(file.file_id);
        if (!decision) {
          errors.push(
            toolError(
              "BUILD_ASSET_EXTRACTION_FILE_DECISION_MISSING",
              `No extraction decision was returned for ${file.file_name}.`,
              { file_id: file.file_id, file_name: file.file_name }
            )
          );
          skippedFiles.push({
            file_id: file.file_id,
            file_name: file.file_name,
            reason: "asset_extraction_missing"
          });
          input.onProgress?.({
            phase: "extract",
            file_id: file.file_id,
            file_name: file.file_name,
            status: "failed",
            asset_count: assetCards.length,
            skipped_count: skippedFiles.length,
            error_count: errors.length
          });
          continue;
        }

        if (decision.asset_card) {
          assetCards.push(decision.asset_card);
          input.onProgress?.({
            phase: "extract",
            file_id: file.file_id,
            file_name: file.file_name,
            status: "success",
            asset_count: assetCards.length,
            skipped_count: skippedFiles.length,
            error_count: errors.length
          });
          continue;
        }

        skippedFiles.push({
          file_id: file.file_id,
          file_name: file.file_name,
          reason: decision.skip_reason ?? "asset_extraction_skipped"
        });
        input.onProgress?.({
          phase: "extract",
          file_id: file.file_id,
          file_name: file.file_name,
          status: "skipped",
          asset_count: assetCards.length,
          skipped_count: skippedFiles.length,
          error_count: errors.length
        });
      }
    } else {
      for (const file of includedFiles) {
        errors.push(
          ...extraction.errors.map((error) => ({
            ...error,
            file_id: error.file_id ?? file.file_id,
            file_name: error.file_name ?? file.file_name
          }))
        );
        skippedFiles.push({
          file_id: file.file_id,
          file_name: file.file_name,
          reason: "asset_extraction_failed"
        });
        input.onProgress?.({
          phase: "extract",
          file_id: file.file_id,
          file_name: file.file_name,
          status: "failed",
          asset_count: assetCards.length,
          skipped_count: skippedFiles.length,
          error_count: errors.length
        });
      }
    }
  }

  let mergedAssets: MergedAsset[] = [];
  if (assetCards.length > 1) {
    mergedAssets = computeConservativeMergedAssets({
      library_id: input.library_id,
      assetCards,
      ownerProfile
    });
    input.onProgress?.({
      phase: "merge",
      status: mergedAssets.length > 0 ? "success" : "skipped",
      merged_count: mergedAssets.length,
      error_count: errors.length
    });
  } else {
    input.onProgress?.({
      phase: "merge",
      status: "skipped",
      merged_count: 0,
      error_count: errors.length
    });
  }

  const data: BuildAssetLibraryData = {
    library_id: input.library_id,
    asset_cards: assetCards,
    merged_assets: mergedAssets,
    summary: computeBuildAssetSummary(assetCards, mergedAssets)
  };

  const finalValidation = validateBuildAssetLibraryDecision({
    library_id: input.library_id,
    file_ids: input.parsed_files.map((file) => file.file_id),
    existing_asset_ids: input.existing_asset_ids,
    decision: data
  });
  errors.push(...finalValidation.errors);

  const status =
    assetCards.length === 0
      ? skippedFiles.length > 0 && errors.length === 0
        ? "partial"
        : "failed"
      : errors.length > 0
        ? "partial"
        : "success";

  const audit = createAgentDecisionAudit({
    stage: "build_asset_library",
    library_id: input.library_id,
    goal: "build_asset_library",
    profile_id: "build_asset_library",
    model: modelUsed,
    input_asset_ids: assetCards.map((asset) => asset.asset_id),
    input_file_ids: input.parsed_files.map((file) => file.file_id),
    input_summary: `Parsed files: ${input.parsed_files.length}; triaged in-scope files: ${includedFiles.length}; extracted assets: ${assetCards.length}; merged groups: ${mergedAssets.length}; skipped files: ${skippedFiles.length}.`,
    validation_status: status === "success" ? "passed" : status === "partial" ? "partial" : "failed",
    validation_errors: errors,
    result: data
  });

  input.onProgress?.({
    phase: "complete",
    status,
    asset_count: assetCards.length,
    merged_count: mergedAssets.length,
    skipped_count: skippedFiles.length,
    error_count: errors.length
  });

  return {
    status,
    data: assetCards.length > 0 ? data : undefined,
    skipped_files: skippedFiles,
    audit,
    errors
  };
}

export async function runIngestRouteDecisionSkill(input: {
  skillDir: string;
  files: LocalFile[];
  modelClient: SkillModelClient;
  maxRetries?: number;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<SkillDecisionResult<IngestRouteDecision>> {
  const bundle = await loadSkillBundle(input.skillDir);
  return runStructuredSkillDecision<IngestRouteDecision>({
    skillDir: input.skillDir,
    bundle,
    modelClient: input.modelClient,
    taskTitle: "Choose the safest ingest route for each local file before low-level extraction.",
    taskInput: {
      files: input.files.map((file) => ({
        file_id: file.file_id,
        file_name: file.file_name,
        extension: file.extension,
        suggested_route: file.suggested_route,
        skip_reason: file.skip_reason
      })),
      allowed_routes: ["text", "parser_lite", "parser_export", "ocr", "vlm", "skip"],
      constraints: {
        choose_route_only: true,
        copy_file_id_exactly: true,
        prefer_suggested_route_by_default: true,
        do_not_guess_content: true,
        skip_unsupported_files: true,
        prefer_text_for_local_text_files: true,
        pdf_and_office_require_parser_route: true,
        image_files_require_ocr_or_vlm_route: true,
        keep_reason_short: true
      }
    },
    outputSchema: ingestRouteDecisionSchema,
    maxRetries: input.maxRetries,
    modelMaxTokens: 220,
    responseFormat: "json_object",
    thinkingMode: "disabled",
    doSample: false,
    eventStage: "ingest",
    decisionType: "route_decision",
    promptContext: createIngestPromptContext(bundle, "route_decision"),
    extraSystemPromptLines: [
      "This is a compact route-selection task.",
      "Mirror suggested_route unless the metadata explicitly requires another allowed route.",
      "Every decision must include reason; use null when the route is not skip.",
      "Output the JSON object immediately and stop."
    ],
    preprocess: (payload) =>
      normalizeIngestRoutePayload({
        payload,
        files: input.files
      }),
    onEvent: input.onEvent,
    validate: (decision: IngestRouteDecision) =>
      validateIngestRouteDecision({
        files: input.files,
        decision
      })
  });
}

export async function normalizeQueryAssetsRequest(input: {
  skillDir: string;
  natural_language_query: string;
  modelClient: SkillModelClient;
  maxRetries?: number;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<SkillDecisionResult<QueryAssetsNormalization>> {
  return runStructuredSkillDecision<QueryAssetsNormalization>({
    skillDir: input.skillDir,
    modelClient: input.modelClient,
    taskTitle: "Normalize a natural-language asset query into deterministic filters.",
    taskInput: {
      natural_language_query: input.natural_language_query,
      allowed_material_types: ["proof", "experience", "agreement", "finance", "rights"],
      allowed_tag_prefixes: ["doc", "use", "entity", "risk"],
      common_tags: [
        "doc:resume",
        "doc:transcript",
        "doc:certificate",
        "doc:student_status",
        "entity:language_certificate",
        "entity:transcript",
        "entity:student_status_certificate",
        "entity:internship_experience",
        "entity:award_certificate",
        "use:summer_internship_application",
        "use:scholarship_application",
        "use:renew_contract",
        "use:expense_reimbursement",
        "risk:needs_review"
      ]
    },
    outputSchema: normalizedQuerySchema,
    maxRetries: input.maxRetries,
    eventStage: "query_assets",
    decisionType: "query_normalization",
    onEvent: input.onEvent,
    extraSystemPromptLines: [
      "Normalize into deterministic retrieval filters for hybrid search.",
      "Use semantic_query for the compact intent sentence; do not repeat the full user query.",
      "Prefer tag_filters_any/tag_filters_all over reusable_scenario.",
      "Only emit lowercase ASCII tags with doc:/use:/entity:/risk: prefixes.",
      "Output the JSON object immediately and stop."
    ]
  });
}

export async function runCheckLifecycleSkill(input: {
  skillDir: string;
  library_id: string;
  goal: string;
  as_of_date: string;
  window_days: number;
  profile: RuleProfile;
  assets: AssetCard[];
  modelClient: SkillModelClient;
  maxRetries?: number;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<{ status: "success" | "failed"; data?: CheckLifecycleData; audit: AgentDecisionAudit; errors: ToolError[] }> {
  const result = await runStructuredSkillDecision<CheckLifecycleData>({
    skillDir: input.skillDir,
    modelClient: input.modelClient,
    taskTitle: "Produce a complete CheckLifecycleData decision.",
    taskInput: {
      library_id: input.library_id,
      goal: input.goal,
      as_of_date: input.as_of_date,
      window_days: input.window_days,
      profile: input.profile,
      assets: input.assets.map(summarizeAsset)
    },
    outputSchema: checkLifecycleDataSchema,
    maxRetries: input.maxRetries,
    eventStage: "check_lifecycle",
    decisionType: "check_lifecycle",
    onEvent: input.onEvent,
    validate: (decision: CheckLifecycleData) =>
      validateLifecycleDecision({
        library_id: input.library_id,
        goal: input.goal,
        as_of_date: input.as_of_date,
        window_days: input.window_days,
        asset_ids: input.assets.map((asset) => asset.asset_id),
        profile: input.profile,
        decision
      })
  });

  const audit = createAgentDecisionAudit({
    stage: "check_lifecycle",
    library_id: input.library_id,
    goal: input.goal,
    profile_id: input.profile.profile_id,
    model: result.model,
    input_asset_ids: input.assets.map((asset) => asset.asset_id),
    input_summary: `Assets: ${input.assets.length}; window_days=${input.window_days}; as_of_date=${input.as_of_date}.`,
    validation_status: result.status === "success" ? "passed" : "failed",
    validation_errors: result.errors,
    result: result.data ?? { failed: true }
  });

  return {
    status: result.status === "success" ? "success" : "failed",
    data: result.data,
    audit,
    errors: result.errors
  };
}

export async function runBuildPackageSkill(input: {
  skillDir: string;
  library_id: string;
  goal: string;
  submission_profile: string;
  missing_items_ref: string;
  readiness: Readiness;
  profile: RuleProfile;
  assets: AssetCard[];
  modelClient: SkillModelClient;
  maxRetries?: number;
  onEvent?: (event: SkillRunnerEvent) => void;
}): Promise<{ status: "success" | "failed"; data?: PackagePlan; audit: AgentDecisionAudit; errors: ToolError[] }> {
  const result = await runStructuredSkillDecision<PackagePlan>({
    skillDir: input.skillDir,
    modelClient: input.modelClient,
    taskTitle: "Select assets and produce a truthful PackagePlan.",
    taskInput: {
      library_id: input.library_id,
      goal: input.goal,
      submission_profile: input.submission_profile,
      missing_items_ref: input.missing_items_ref,
      readiness: input.readiness,
      profile: input.profile,
      assets: input.assets.map(summarizeAsset)
    },
    outputSchema: packagePlanSchema,
    maxRetries: input.maxRetries,
    eventStage: "build_package",
    decisionType: "build_package",
    onEvent: input.onEvent,
    validate: (decision: PackagePlan) =>
      validatePackagePlanDecision({
        library_id: input.library_id,
        goal: input.goal,
        submission_profile: input.submission_profile,
        missing_items_ref: input.missing_items_ref,
        asset_ids: input.assets.map((asset) => asset.asset_id),
        expected_readiness: input.readiness,
        profile: input.profile,
        package_plan: decision
      })
  });

  const audit = createAgentDecisionAudit({
    stage: "build_package",
    library_id: input.library_id,
    goal: input.goal,
    profile_id: input.profile.profile_id,
    model: result.model,
    input_asset_ids: input.assets.map((asset) => asset.asset_id),
    input_summary: `Assets: ${input.assets.length}; submission_profile=${input.submission_profile}.`,
    validation_status: result.status === "success" ? "passed" : "failed",
    validation_errors: result.errors,
    result: result.data ?? { failed: true }
  });

  return {
    status: result.status === "success" ? "success" : "failed",
    data: result.data,
    audit,
    errors: result.errors
  };
}

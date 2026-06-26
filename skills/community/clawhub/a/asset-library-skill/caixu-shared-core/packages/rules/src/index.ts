import { createHash, randomUUID } from "node:crypto";
import type {
  AgentDecisionAudit,
  AssetCard,
  BuildAssetLibraryData,
  CheckLifecycleData,
  LifecycleEvent,
  MissingItem,
  MissingItems,
  MergedAsset,
  PackagePlan,
  Readiness,
  RuleProfile,
  ToolError
} from "@caixu/contracts";
import {
  agentDecisionAuditSchema,
  buildAssetLibraryDataSchema,
  checkLifecycleDataSchema,
  packagePlanSchema
} from "@caixu/contracts";

export type DecisionValidationResult = {
  status: "passed" | "failed" | "partial";
  errors: ToolError[];
};

function requirement(
  code: string,
  title: string,
  options: { required: boolean; blocking: boolean; description: string }
) {
  return {
    code,
    title,
    required: options.required,
    blocking: options.blocking,
    description: options.description
  };
}

export const ruleProfiles: Record<string, RuleProfile> = {
  summer_internship_application: {
    profile_id: "summer_internship_application",
    display_name: "暑期实习申请",
    bundle_version: "2026.03",
    rule_pack_id: "cn.student.internship.v1",
    default_window_days: 60,
    scene_summary:
      "面向暑期实习申请，重点关注成绩单、在读证明、身份证明和语言证明的可复用性与时效。",
    requirements: [
      requirement("proof:transcript", "成绩单", {
        required: true,
        blocking: false,
        description: "用于证明学业背景。"
      }),
      requirement("proof:student_status_certificate", "在读/学籍证明", {
        required: true,
        blocking: true,
        description: "用于证明当前在读身份，缺失时不应直接提交。"
      }),
      requirement("proof:id_card_copy", "身份证明复印件", {
        required: true,
        blocking: true,
        description: "用于身份核验，缺失时不应直接提交。"
      }),
      requirement("proof:language_certificate", "语言证明", {
        required: false,
        blocking: false,
        description: "如 CET、IELTS 等，可增强申请材料完整度。"
      }),
      requirement("experience:internship_proof", "实习/实践证明", {
        required: false,
        blocking: false,
        description: "已有实习或实践经历时可补充证明。"
      }),
      requirement("experience:project_experience", "项目经历证明", {
        required: false,
        blocking: false,
        description: "项目经历可作为辅助材料。"
      })
    ],
    lifecycle_focus: [
      "检查在读证明、身份证明是否进入续办窗口",
      "识别申请材料是否存在阻塞性缺件",
      "为打包和提交提供 readiness"
    ],
    package_guidance: [
      "优先打包成绩单、在读证明、语言证明等正式材料",
      "当存在 blocking 缺件时仍可生成 truthful package，但不得伪装为可提交",
      "包内清单顺序优先正式证明类材料"
    ],
    readiness_policy: {
      allow_submit_with_blocking_items: false,
      allow_truthful_package_when_blocked: true
    },
    notes: "默认暑期实习规则包。"
  },
  renew_contract: {
    profile_id: "renew_contract",
    display_name: "合同续办",
    bundle_version: "2026.03",
    rule_pack_id: "cn.contract.renewal.v1",
    default_window_days: 30,
    scene_summary: "面向合同或协议续办，重点关注到期窗口与基础身份证明。",
    requirements: [
      requirement("agreement:contract", "合同/协议", {
        required: true,
        blocking: true,
        description: "核心续办材料。"
      }),
      requirement("proof:id_card_copy", "身份证明复印件", {
        required: false,
        blocking: false,
        description: "部分合同续办需要身份核验。"
      })
    ],
    lifecycle_focus: [
      "检查合同是否即将到期或已经过期",
      "识别续办前置材料是否缺失"
    ],
    package_guidance: [
      "优先打包现有合同版本及相关身份证明"
    ],
    readiness_policy: {
      allow_submit_with_blocking_items: false,
      allow_truthful_package_when_blocked: true
    },
    notes: "合同和协议类续办规则。"
  },
  expense_reimbursement: {
    profile_id: "expense_reimbursement",
    display_name: "报销整理",
    bundle_version: "2026.03",
    rule_pack_id: "cn.finance.reimbursement.v1",
    default_window_days: 30,
    scene_summary: "面向票据、发票和支付记录，关注时效与凭证完整性。",
    requirements: [
      requirement("finance:invoice", "发票", {
        required: true,
        blocking: true,
        description: "报销的基础凭证。"
      }),
      requirement("finance:payment_record", "支付记录", {
        required: false,
        blocking: false,
        description: "可作为辅助佐证。"
      })
    ],
    lifecycle_focus: [
      "检查发票时效",
      "识别票据与支付凭证缺件"
    ],
    package_guidance: [
      "优先打包发票，其次补充支付记录"
    ],
    readiness_policy: {
      allow_submit_with_blocking_items: false,
      allow_truthful_package_when_blocked: true
    },
    notes: "票据与报销场景规则。"
  },
  scholarship_application: {
    profile_id: "scholarship_application",
    display_name: "奖学金申请",
    bundle_version: "2026.03",
    rule_pack_id: "cn.student.scholarship.v1",
    default_window_days: 90,
    scene_summary: "面向奖学金申请，关注成绩、在读/获奖证明与项目经历。",
    requirements: [
      requirement("proof:transcript", "成绩单", {
        required: true,
        blocking: true,
        description: "奖学金申请的核心材料。"
      }),
      requirement("proof:award_certificate", "获奖证明", {
        required: false,
        blocking: false,
        description: "可增强奖学金申请竞争力。"
      }),
      requirement("experience:project_experience", "项目经历", {
        required: false,
        blocking: false,
        description: "项目经历可作为补充材料。"
      }),
      requirement("proof:student_status_certificate", "在读/学籍证明", {
        required: false,
        blocking: false,
        description: "部分奖学金场景要求补充当前在读状态。"
      })
    ],
    lifecycle_focus: [
      "关注成绩与在读证明的可复用性",
      "识别获奖/项目材料是否缺失"
    ],
    package_guidance: [
      "优先打包成绩单，再补充获奖与项目材料"
    ],
    readiness_policy: {
      allow_submit_with_blocking_items: false,
      allow_truthful_package_when_blocked: true
    },
    notes: "奖学金申报规则。"
  }
};

function slug(value: string): string {
  return createHash("sha1").update(value).digest("hex").slice(0, 10);
}

function resultHash(value: unknown): string {
  return createHash("sha1").update(JSON.stringify(value)).digest("hex");
}

function isDateOnly(value: string): boolean {
  return /^\d{4}-\d{2}-\d{2}$/.test(value);
}

function validationError(
  code: string,
  message: string,
  extras?: Pick<ToolError, "asset_id" | "file_id" | "retryable">
): ToolError {
  return {
    code,
    message,
    retryable: extras?.retryable,
    asset_id: extras?.asset_id,
    file_id: extras?.file_id
  };
}

function requiredSignals(profile: RuleProfile): string[] {
  return profile.requirements.filter((item) => item.required).map((item) => item.code);
}

function optionalSignals(profile: RuleProfile): string[] {
  return profile.requirements.filter((item) => !item.required).map((item) => item.code);
}

function blockingSignals(profile: RuleProfile): string[] {
  return profile.requirements.filter((item) => item.blocking).map((item) => item.code);
}

function assetText(asset: AssetCard): string {
  return `${asset.material_type} ${asset.title} ${asset.normalized_summary}`.toLowerCase();
}

export function getRuleProfileBundle(profileId: string): RuleProfile {
  const profile = ruleProfiles[profileId];
  if (!profile) {
    throw new Error(`Unsupported rule profile: ${profileId}`);
  }
  return profile;
}

export const getRuleProfile = getRuleProfileBundle;

export function createAgentDecisionAudit(input: {
  stage: AgentDecisionAudit["stage"];
  library_id: string;
  goal: string;
  profile_id: string;
  model: string;
  input_asset_ids: string[];
  input_file_ids?: string[];
  input_summary: string;
  validation_status: AgentDecisionAudit["validation_status"];
  validation_errors?: ToolError[];
  result: unknown;
  created_at?: string;
  decision_id?: string;
  run_ref_type?: AgentDecisionAudit["run_ref_type"];
  run_ref_id?: string;
}): AgentDecisionAudit {
  return agentDecisionAuditSchema.parse({
    decision_id: input.decision_id ?? `decision_${randomUUID().replaceAll("-", "")}`,
    stage: input.stage,
    library_id: input.library_id,
    goal: input.goal,
    profile_id: input.profile_id,
    model: input.model,
    input_asset_ids: input.input_asset_ids,
    input_file_ids: input.input_file_ids ?? [],
    input_summary: input.input_summary,
    validation_status: input.validation_status,
    validation_errors: input.validation_errors ?? [],
    result_hash: resultHash(input.result),
    created_at: input.created_at ?? new Date().toISOString(),
    run_ref_type: input.run_ref_type,
    run_ref_id: input.run_ref_id
  });
}

export function serializeAgentDecisionAudit(audit: AgentDecisionAudit): string {
  return JSON.stringify(audit);
}

export function validateBuildAssetLibraryDecision(input: {
  library_id: string;
  file_ids: string[];
  existing_asset_ids?: string[];
  decision: BuildAssetLibraryData;
}): DecisionValidationResult {
  const parsed = buildAssetLibraryDataSchema.safeParse(input.decision);
  const errors: ToolError[] = [];

  if (!parsed.success) {
    return {
      status: "failed",
      errors: [
        validationError(
          "BUILD_ASSET_LIBRARY_SCHEMA_INVALID",
          parsed.error.issues
            .map((issue) => `${issue.path.join(".") || "root"}: ${issue.message}`)
            .join("; ")
        )
      ]
    };
  }

  const decision = parsed.data;
  const fileIds = new Set(input.file_ids);
  const decisionAssetIds = new Set<string>();
  const knownAssetIds = new Set([...(input.existing_asset_ids ?? [])]);

  if (decision.library_id !== input.library_id) {
    errors.push(
      validationError(
        "BUILD_ASSET_LIBRARY_ID_MISMATCH",
        `Expected library_id ${input.library_id}, received ${decision.library_id}.`
      )
    );
  }

  for (const asset of decision.asset_cards) {
    decisionAssetIds.add(asset.asset_id);

    if (asset.library_id !== input.library_id) {
      errors.push(
        validationError(
          "BUILD_ASSET_CARD_LIBRARY_ID_MISMATCH",
          `Asset ${asset.asset_id} has library_id ${asset.library_id}, expected ${input.library_id}.`,
          { asset_id: asset.asset_id }
        )
      );
    }

    if (asset.holder_name === "unknown") {
      errors.push(
        validationError(
          "BUILD_ASSET_CARD_HOLDER_UNKNOWN_STRING",
          `Asset ${asset.asset_id} must use null instead of "unknown" for holder_name.`,
          { asset_id: asset.asset_id }
        )
      );
    }

    if (asset.issuer_name === "unknown") {
      errors.push(
        validationError(
          "BUILD_ASSET_CARD_ISSUER_UNKNOWN_STRING",
          `Asset ${asset.asset_id} must use null instead of "unknown" for issuer_name.`,
          { asset_id: asset.asset_id }
        )
      );
    }

    for (const sourceFile of asset.source_files) {
      if (!fileIds.has(sourceFile.file_id)) {
        errors.push(
          validationError(
            "BUILD_ASSET_CARD_SOURCE_FILE_UNKNOWN",
            `Asset ${asset.asset_id} references unknown file_id ${sourceFile.file_id}.`,
            { asset_id: asset.asset_id, file_id: sourceFile.file_id }
          )
        );
      }
    }
  }

  const allAssetIds = new Set([...knownAssetIds, ...decisionAssetIds]);
  for (const merged of decision.merged_assets) {
    if (merged.library_id !== input.library_id) {
      errors.push(
        validationError(
          "BUILD_MERGED_ASSET_LIBRARY_ID_MISMATCH",
          `Merged asset ${merged.merged_asset_id} has library_id ${merged.library_id}, expected ${input.library_id}.`
        )
      );
    }

    if (!allAssetIds.has(merged.canonical_asset_id)) {
      errors.push(
        validationError(
          "BUILD_MERGED_CANONICAL_ASSET_UNKNOWN",
          `Merged asset ${merged.merged_asset_id} references unknown canonical_asset_id ${merged.canonical_asset_id}.`,
          { asset_id: merged.canonical_asset_id }
        )
      );
    }

    if (!allAssetIds.has(merged.selected_asset_id)) {
      errors.push(
        validationError(
          "BUILD_MERGED_SELECTED_ASSET_UNKNOWN",
          `Merged asset ${merged.merged_asset_id} references unknown selected_asset_id ${merged.selected_asset_id}.`,
          { asset_id: merged.selected_asset_id }
        )
      );
    }

    const supersededIds = new Set<string>();
    for (const supersededId of merged.superseded_asset_ids) {
      if (!allAssetIds.has(supersededId)) {
        errors.push(
          validationError(
            "BUILD_MERGED_SUPERSEDED_ASSET_UNKNOWN",
            `Merged asset ${merged.merged_asset_id} references unknown superseded asset ${supersededId}.`,
            { asset_id: supersededId }
          )
        );
      }
      if (supersededIds.has(supersededId)) {
        errors.push(
          validationError(
            "BUILD_MERGED_SUPERSEDED_DUPLICATED",
            `Merged asset ${merged.merged_asset_id} duplicates superseded asset ${supersededId}.`,
            { asset_id: supersededId }
          )
        );
      }
      supersededIds.add(supersededId);
    }

    if (supersededIds.has(merged.selected_asset_id)) {
      errors.push(
        validationError(
          "BUILD_MERGED_SELECTED_IN_SUPERSEDED",
          `Merged asset ${merged.merged_asset_id} cannot include selected_asset_id inside superseded_asset_ids.`,
          { asset_id: merged.selected_asset_id }
        )
      );
    }

    for (const version of merged.version_order) {
      if (!allAssetIds.has(version.asset_id)) {
        errors.push(
          validationError(
            "BUILD_MERGED_VERSION_ORDER_ASSET_UNKNOWN",
            `Merged asset ${merged.merged_asset_id} version_order references unknown asset_id ${version.asset_id}.`,
            { asset_id: version.asset_id }
          )
        );
      }
    }
  }

  if (decision.summary.total_assets !== decision.asset_cards.length) {
    errors.push(
      validationError(
        "BUILD_SUMMARY_TOTAL_ASSETS_MISMATCH",
        `summary.total_assets must equal asset_cards.length (${decision.asset_cards.length}), received ${decision.summary.total_assets}.`
      )
    );
  }

  if (decision.summary.merged_groups !== decision.merged_assets.length) {
    errors.push(
      validationError(
        "BUILD_SUMMARY_MERGED_GROUPS_MISMATCH",
        `summary.merged_groups must equal merged_assets.length (${decision.merged_assets.length}), received ${decision.summary.merged_groups}.`
      )
    );
  }

  const mergedMemberIds = new Set<string>();
  for (const merged of decision.merged_assets) {
    mergedMemberIds.add(merged.selected_asset_id);
    for (const supersededId of merged.superseded_asset_ids) {
      mergedMemberIds.add(supersededId);
    }
  }
  const unmergedAssets = decision.asset_cards.filter(
    (asset) => !mergedMemberIds.has(asset.asset_id)
  ).length;

  if (decision.summary.unmerged_assets !== unmergedAssets) {
    errors.push(
      validationError(
        "BUILD_SUMMARY_UNMERGED_ASSETS_MISMATCH",
        `summary.unmerged_assets must equal ${unmergedAssets}, received ${decision.summary.unmerged_assets}.`
      )
    );
  }

  return {
    status: errors.length > 0 ? "failed" : "passed",
    errors
  };
}

export function validateLifecycleDecision(input: {
  library_id: string;
  goal: string;
  as_of_date: string;
  window_days: number;
  asset_ids: string[];
  profile: RuleProfile;
  decision: CheckLifecycleData;
}): DecisionValidationResult {
  const parsed = checkLifecycleDataSchema.safeParse(input.decision);
  const errors: ToolError[] = [];

  if (!parsed.success) {
    return {
      status: "failed",
      errors: [
        validationError(
          "LIFECYCLE_SCHEMA_INVALID",
          parsed.error.issues
            .map((issue) => `${issue.path.join(".") || "root"}: ${issue.message}`)
            .join("; ")
        )
      ]
    };
  }

  const decision = parsed.data;
  const assetIds = new Set(input.asset_ids);

  if (decision.library_id !== input.library_id) {
    errors.push(
      validationError(
        "LIFECYCLE_LIBRARY_ID_MISMATCH",
        `Expected library_id ${input.library_id}, received ${decision.library_id}.`
      )
    );
  }

  if (!isDateOnly(decision.as_of_date) || decision.as_of_date !== input.as_of_date) {
    errors.push(
      validationError(
        "LIFECYCLE_DATE_INVALID",
        `Expected absolute as_of_date ${input.as_of_date}, received ${decision.as_of_date}.`
      )
    );
  }

  if (decision.window_days !== input.window_days) {
    errors.push(
      validationError(
        "LIFECYCLE_WINDOW_DAYS_MISMATCH",
        `Expected window_days ${input.window_days}, received ${decision.window_days}.`
      )
    );
  }

  if (decision.missing_items.target_goal !== input.goal) {
    errors.push(
      validationError(
        "LIFECYCLE_GOAL_MISMATCH",
        `Expected target_goal ${input.goal}, received ${decision.missing_items.target_goal}.`
      )
    );
  }

  if (decision.missing_items.rule_pack_id !== input.profile.rule_pack_id) {
    errors.push(
      validationError(
        "LIFECYCLE_RULE_PACK_MISMATCH",
        `Expected rule_pack_id ${input.profile.rule_pack_id}, received ${decision.missing_items.rule_pack_id}.`
      )
    );
  }

  for (const event of decision.lifecycle_events) {
    if (!assetIds.has(event.asset_id)) {
      errors.push(
        validationError(
          "LIFECYCLE_EVENT_ASSET_UNKNOWN",
          `Lifecycle event references unknown asset_id ${event.asset_id}.`,
          { asset_id: event.asset_id }
        )
      );
    }
    if (event.target_goal !== input.goal) {
      errors.push(
        validationError(
          "LIFECYCLE_EVENT_GOAL_MISMATCH",
          `Lifecycle event ${event.event_id} has target_goal ${event.target_goal}, expected ${input.goal}.`,
          { asset_id: event.asset_id }
        )
      );
    }
  }

  for (const match of decision.rule_matches) {
    if (!assetIds.has(match.asset_id)) {
      errors.push(
        validationError(
          "LIFECYCLE_RULE_MATCH_ASSET_UNKNOWN",
          `Rule match references unknown asset_id ${match.asset_id}.`,
          { asset_id: match.asset_id }
        )
      );
    }
    if (match.scene_key !== input.goal) {
      errors.push(
        validationError(
          "LIFECYCLE_RULE_MATCH_SCENE_MISMATCH",
          `Rule match ${match.match_id} has scene_key ${match.scene_key}, expected ${input.goal}.`,
          { asset_id: match.asset_id }
        )
      );
    }
  }

  for (const assetId of decision.missing_items.available_asset_ids) {
    if (!assetIds.has(assetId)) {
      errors.push(
        validationError(
          "LIFECYCLE_AVAILABLE_ASSET_UNKNOWN",
          `missing_items.available_asset_ids contains unknown asset_id ${assetId}.`,
          { asset_id: assetId }
        )
      );
    }
  }

  const missingBlocking = decision.missing_items.items.filter(
    (item) => item.severity === "blocking"
  );
  const missingWarnings = decision.missing_items.items.filter(
    (item) => item.severity === "warning"
  );
  const readinessBlockingCodes = new Set(
    decision.readiness.blocking_items.map((item) => item.code)
  );
  const readinessWarningCodes = new Set(
    decision.readiness.warning_items.map((item) => item.code)
  );

  if (decision.readiness.ready_for_submission && missingBlocking.length > 0) {
    errors.push(
      validationError(
        "LIFECYCLE_READINESS_BLOCKING_CONFLICT",
        "readiness.ready_for_submission cannot be true when blocking missing items exist."
      )
    );
  }

  if (!decision.readiness.ready_for_submission && missingBlocking.length === 0) {
    errors.push(
      validationError(
        "LIFECYCLE_READINESS_FALSE_WITHOUT_BLOCKING",
        "readiness.ready_for_submission is false but no blocking missing items were provided."
      )
    );
  }

  for (const item of missingBlocking) {
    if (!readinessBlockingCodes.has(item.code)) {
      errors.push(
        validationError(
          "LIFECYCLE_BLOCKING_ITEM_NOT_PROPAGATED",
          `Blocking missing item ${item.code} is absent from readiness.blocking_items.`
        )
      );
    }
  }

  for (const item of decision.readiness.blocking_items) {
    if (item.severity !== "blocking") {
      errors.push(
        validationError(
          "LIFECYCLE_READINESS_BLOCKING_SEVERITY_INVALID",
          `readiness.blocking_items contains non-blocking item ${item.code}.`
        )
      );
    }
  }

  for (const item of decision.readiness.warning_items) {
    if (item.severity !== "warning") {
      errors.push(
        validationError(
          "LIFECYCLE_READINESS_WARNING_SEVERITY_INVALID",
          `readiness.warning_items contains non-warning item ${item.code}.`
        )
      );
    }
  }

  for (const item of decision.readiness.warning_items) {
    if (!missingWarnings.some((warning) => warning.code === item.code)) {
      errors.push(
        validationError(
          "LIFECYCLE_WARNING_ITEM_UNKNOWN",
          `readiness.warning_items contains ${item.code}, which is not present in missing_items.items.`
        )
      );
    }
  }

  if (missingBlocking.length > 0 && !["partial", "blocking"].includes(decision.missing_items.blocking_level)) {
    errors.push(
      validationError(
        "LIFECYCLE_BLOCKING_LEVEL_INVALID",
        `blocking_level must be partial/blocking when blocking items exist, received ${decision.missing_items.blocking_level}.`
      )
    );
  }

  return {
    status: errors.length > 0 ? "failed" : "passed",
    errors
  };
}

export function validatePackagePlanDecision(input: {
  library_id: string;
  goal: string;
  submission_profile: string;
  missing_items_ref: string;
  asset_ids: string[];
  expected_readiness: Readiness;
  profile: RuleProfile;
  package_plan: PackagePlan;
}): DecisionValidationResult {
  const parsed = packagePlanSchema.safeParse(input.package_plan);
  const errors: ToolError[] = [];

  if (!parsed.success) {
    return {
      status: "failed",
      errors: [
        validationError(
          "PACKAGE_PLAN_SCHEMA_INVALID",
          parsed.error.issues
            .map((issue) => `${issue.path.join(".") || "root"}: ${issue.message}`)
            .join("; ")
        )
      ]
    };
  }

  const packagePlan = parsed.data;
  const assetIds = new Set(input.asset_ids);

  if (packagePlan.library_id !== input.library_id) {
    errors.push(
      validationError(
        "PACKAGE_LIBRARY_ID_MISMATCH",
        `Expected library_id ${input.library_id}, received ${packagePlan.library_id}.`
      )
    );
  }

  if (packagePlan.target_goal !== input.goal) {
    errors.push(
      validationError(
        "PACKAGE_GOAL_MISMATCH",
        `Expected target_goal ${input.goal}, received ${packagePlan.target_goal}.`
      )
    );
  }

  if (packagePlan.submission_profile !== input.submission_profile) {
    errors.push(
      validationError(
        "PACKAGE_SUBMISSION_PROFILE_MISMATCH",
        `Expected submission_profile ${input.submission_profile}, received ${packagePlan.submission_profile}.`
      )
    );
  }

  if (packagePlan.missing_items_ref !== input.missing_items_ref) {
    errors.push(
      validationError(
        "PACKAGE_MISSING_ITEMS_REF_MISMATCH",
        `Expected missing_items_ref ${input.missing_items_ref}, received ${packagePlan.missing_items_ref}.`
      )
    );
  }

  for (const assetId of packagePlan.selected_asset_ids) {
    if (!assetIds.has(assetId)) {
      errors.push(
        validationError(
          "PACKAGE_SELECTED_ASSET_UNKNOWN",
          `Package selected unknown asset_id ${assetId}.`,
          { asset_id: assetId }
        )
      );
    }
  }

  if (JSON.stringify(packagePlan.readiness) !== JSON.stringify(input.expected_readiness)) {
    errors.push(
      validationError(
        "PACKAGE_READINESS_MISMATCH",
        "PackagePlan.readiness must inherit the validated lifecycle readiness without modification."
      )
    );
  }

  if (
    !input.profile.readiness_policy.allow_submit_with_blocking_items &&
    input.expected_readiness.ready_for_submission === false &&
    packagePlan.readiness.ready_for_submission === true
  ) {
    errors.push(
      validationError(
        "PACKAGE_READINESS_POLICY_VIOLATION",
        "PackagePlan cannot flip readiness to ready_for_submission=true when the profile disallows submit with blocking items."
      )
    );
  }

  if (!packagePlan.generated_files.some((file) => file.file_type === "zip")) {
    errors.push(
      validationError(
        "PACKAGE_ZIP_OUTPUT_MISSING",
        "PackagePlan.generated_files must include one zip artifact."
      )
    );
  }

  return {
    status: errors.length > 0 ? "failed" : "passed",
    errors
  };
}

// Deprecated deterministic compatibility layer.
function daysBetween(start: string, end: string): number {
  const startTime = new Date(start).getTime();
  const endTime = new Date(end).getTime();
  return Math.floor((endTime - startTime) / (1000 * 60 * 60 * 24));
}

export function deriveAssetSignals(asset: AssetCard): string[] {
  const text = assetText(asset);
  const signals = new Set<string>();

  if (asset.material_type === "proof") {
    signals.add("proof:generic");
  }
  if (asset.material_type === "experience") {
    signals.add("experience:generic");
  }
  if (asset.material_type === "finance") {
    signals.add("finance:generic");
  }
  if (asset.material_type === "rights") {
    signals.add("rights:generic");
  }
  if (asset.material_type === "agreement") {
    signals.add("agreement:generic");
  }

  if (text.includes("transcript") || text.includes("成绩")) {
    signals.add("proof:transcript");
  }
  if (
    text.includes("student status") ||
    text.includes("student status certificate") ||
    text.includes("enrollment") ||
    text.includes("学籍") ||
    text.includes("在读证明")
  ) {
    signals.add("proof:student_status_certificate");
  }
  if (
    text.includes("id card") ||
    text.includes("身份证") ||
    text.includes("passport")
  ) {
    signals.add("proof:id_card_copy");
  }
  if (
    text.includes("cet") ||
    text.includes("ielts") ||
    text.includes("toefl") ||
    text.includes("english")
  ) {
    signals.add("proof:language_certificate");
  }
  if (
    text.includes("internship proof") ||
    text.includes("internship certificate") ||
    text.includes("实习证明") ||
    text.includes("实习单位") ||
    text.includes("实习岗位")
  ) {
    signals.add("experience:internship_proof");
  }
  if (text.includes("project") || text.includes("项目")) {
    signals.add("experience:project_experience");
  }
  if (text.includes("award") || text.includes("获奖")) {
    signals.add("proof:award_certificate");
  }
  if (text.includes("invoice") || text.includes("发票")) {
    signals.add("finance:invoice");
  }
  if (text.includes("payment") || text.includes("支付")) {
    signals.add("finance:payment_record");
  }
  if (text.includes("contract") || text.includes("协议")) {
    signals.add("agreement:contract");
  }

  return [...signals];
}

function buildRuleMatches(
  libraryId: string,
  assets: AssetCard[],
  profile: RuleProfile
) {
  const matchScene = profile.profile_id;
  const relevantCodes = [...requiredSignals(profile), ...optionalSignals(profile)];

  return assets.flatMap((asset) => {
    const signals = deriveAssetSignals(asset);
    const matchedCodes = relevantCodes.filter((signal) => signals.includes(signal));

    if (matchedCodes.length === 0) {
      return [];
    }

    return matchedCodes.map((signal) => ({
      schema_version: "1.0" as const,
      library_id: libraryId,
      match_id: `match_${slug(`${asset.asset_id}_${signal}`)}`,
      asset_id: asset.asset_id,
      rule_pack_id: profile.rule_pack_id,
      rule_id: `rule_${signal.replaceAll(":", "_")}`,
      scene_key: matchScene,
      match_status: requiredSignals(profile).includes(signal)
        ? ("matched" as const)
        : ("recommended" as const),
      renewable: Boolean(asset.expiry_date),
      reusable: true,
      required_assets: requiredSignals(profile),
      output_requirements: [signal],
      notes: `${asset.title} 命中 ${signal}。`
    }));
  });
}

function buildMissingItems(
  libraryId: string,
  assets: AssetCard[],
  profile: RuleProfile
): MissingItems {
  const availableSignals = new Set<string>();
  for (const asset of assets) {
    for (const signal of deriveAssetSignals(asset)) {
      availableSignals.add(signal);
    }
  }

  const requiredRequirements = profile.requirements.filter((item) => item.required);
  const items: MissingItem[] = requiredRequirements
    .filter((item) => !availableSignals.has(item.code))
    .map((item) => ({
      code: `missing_${item.code.replaceAll(":", "_")}`,
      title: item.code,
      description: item.description,
      severity: item.blocking ? ("blocking" as const) : ("warning" as const),
      asset_type: item.code,
      required_for: profile.profile_id,
      suggested_action: `补充 ${item.code} 后重新生成材料包。`
    }));

  const blockingCount = items.filter((item) => item.severity === "blocking").length;
  const warningCount = items.filter((item) => item.severity === "warning").length;

  return {
    schema_version: "1.0",
    library_id: libraryId,
    diagnosis_id: `diag_${slug(`${libraryId}_${profile.profile_id}`)}`,
    target_goal: profile.profile_id,
    rule_pack_id: profile.rule_pack_id,
    items,
    available_asset_ids: assets.map((asset) => asset.asset_id),
    gap_summary:
      items.length > 0
        ? `当前缺少 ${items.length} 项材料。`
        : "当前材料满足首轮打包要求。",
    next_actions:
      items.length > 0
        ? items.map((item) => item.suggested_action)
        : ["可以继续生成导出物和材料包。"],
    blocking_level:
      blockingCount > 0
        ? "partial"
        : warningCount > 0
          ? "warning"
          : "none"
  };
}

function buildReadiness(missingItems: MissingItems): Readiness {
  const blockingItems = missingItems.items.filter((item) => item.severity === "blocking");
  const warningItems = missingItems.items.filter((item) => item.severity === "warning");

  return {
    ready_for_submission: blockingItems.length === 0,
    blocking_items: blockingItems,
    warning_items: warningItems,
    rationale:
      blockingItems.length > 0
        ? "存在阻塞性缺件，当前不适合直接提交。"
        : warningItems.length > 0
          ? "当前可提交，但建议先处理提示项。"
          : "材料完整，可以继续提交。"
  };
}

function buildLifecycleEvents(
  libraryId: string,
  goal: string,
  asOfDate: string,
  windowDays: number,
  assets: AssetCard[]
): LifecycleEvent[] {
  const events: LifecycleEvent[] = [];

  for (const asset of assets) {
    if (!asset.expiry_date) {
      continue;
    }

    const delta = daysBetween(asOfDate, asset.expiry_date);
    if (Number.isNaN(delta)) {
      continue;
    }

    if (delta < 0) {
      events.push({
        schema_version: "1.0",
        library_id: libraryId,
        event_id: `event_${slug(`${asset.asset_id}_expired`)}`,
        asset_id: asset.asset_id,
        trigger_type: "expiry_trigger",
        event_status: "urgent",
        severity: "blocking",
        event_date: asOfDate,
        window_start_date: asset.expiry_date,
        window_end_date: asset.expiry_date,
        target_goal: goal,
        recommended_action: `尽快补办或更新 ${asset.title}。`,
        prerequisite_assets: [],
        blocking_items: [`${asset.title} 已过期。`],
        related_rule_ids: []
      });
      continue;
    }

    if (delta <= windowDays) {
      events.push({
        schema_version: "1.0",
        library_id: libraryId,
        event_id: `event_${slug(`${asset.asset_id}_renewal_window`)}`,
        asset_id: asset.asset_id,
        trigger_type: "renewal_window_trigger",
        event_status: "recommended",
        severity: "warning",
        event_date: asOfDate,
        window_start_date: asOfDate,
        window_end_date: asset.expiry_date,
        target_goal: goal,
        recommended_action: `在 ${windowDays} 天窗口内检查并更新 ${asset.title}。`,
        prerequisite_assets: [],
        blocking_items: [],
        related_rule_ids: []
      });
    }
  }

  return events;
}

export function evaluateLifecycle(params: {
  library_id: string;
  assets: AssetCard[];
  merged_assets?: MergedAsset[];
  goal: string;
  as_of_date: string;
  window_days?: number;
}): CheckLifecycleData {
  const profile = getRuleProfileBundle(params.goal);
  const windowDays = params.window_days ?? profile.default_window_days;
  const lifecycleEvents = buildLifecycleEvents(
    params.library_id,
    params.goal,
    params.as_of_date,
    windowDays,
    params.assets
  );
  const ruleMatches = buildRuleMatches(params.library_id, params.assets, profile);
  const missingItems = buildMissingItems(params.library_id, params.assets, profile);
  const readiness = buildReadiness(missingItems);

  return {
    library_id: params.library_id,
    as_of_date: params.as_of_date,
    window_days: windowDays,
    lifecycle_events: lifecycleEvents,
    rule_matches: ruleMatches,
    missing_items: missingItems,
    readiness
  };
}

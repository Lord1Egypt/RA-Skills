import { describe, expect, it } from "vitest";
import type { AssetCard, BuildAssetLibraryData, CheckLifecycleData, PackagePlan } from "@caixu/contracts";
import {
  createAgentDecisionAudit,
  deriveAssetSignals,
  getRuleProfileBundle,
  validateBuildAssetLibraryDecision,
  validateLifecycleDecision,
  validatePackagePlanDecision
} from "../src/index.js";

const baseAsset: Omit<
  AssetCard,
  "asset_id" | "title" | "normalized_summary" | "source_files"
> = {
  schema_version: "1.0",
  library_id: "lib_demo_student_001",
  material_type: "proof",
  holder_name: "Demo Student",
  issuer_name: "Demo University",
  issue_date: "2026-03-01",
  expiry_date: null,
  validity_status: "long_term",
  agent_tags: [
    "doc:transcript",
    "entity:transcript",
    "use:summer_internship_application",
    "risk:auto"
  ],
  reusable_scenarios: ["summer_internship_application"],
  sensitivity_level: "medium",
  confidence: 0.95,
  asset_state: "active",
  review_status: "auto",
  last_verified_at: null
};

describe("@caixu/rules", () => {
  it("loads a versioned rule profile bundle", () => {
    const profile = getRuleProfileBundle("summer_internship_application");
    expect(profile.bundle_version).toBe("2026.03");
    expect(profile.requirements.some((item) => item.code === "proof:id_card_copy")).toBe(
      true
    );
  });

  it("does not infer internship experience from proof materials mentioning internship applications", () => {
    const signals = deriveAssetSignals({
      ...baseAsset,
      asset_id: "asset_transcript_001",
      title: "Official Transcript",
      normalized_summary: "Transcript for summer internship applications.",
      source_files: [
        {
          file_id: "file_transcript_001",
          file_name: "transcript.txt",
          mime_type: "text/plain"
        }
      ]
    });

    expect(signals).toContain("proof:transcript");
    expect(signals).not.toContain("experience:internship_proof");
  });

  it("validates a consistent lifecycle decision", () => {
    const profile = getRuleProfileBundle("summer_internship_application");
    const decision: CheckLifecycleData = {
      library_id: "lib_demo_student_001",
      as_of_date: "2026-03-29",
      window_days: 60,
      lifecycle_events: [],
      rule_matches: [],
      missing_items: {
        schema_version: "1.0",
        library_id: "lib_demo_student_001",
        diagnosis_id: "diag_001",
        target_goal: "summer_internship_application",
        rule_pack_id: profile.rule_pack_id,
        items: [
          {
            code: "missing_proof_id_card_copy",
            title: "proof:id_card_copy",
            description: "身份证明缺失。",
            severity: "blocking",
            asset_type: "proof:id_card_copy",
            required_for: "summer_internship_application",
            suggested_action: "补充后重新生成。"
          }
        ],
        available_asset_ids: ["asset_transcript_001"],
        gap_summary: "缺少 1 项材料。",
        next_actions: ["补充身份证明。"],
        blocking_level: "partial"
      },
      readiness: {
        ready_for_submission: false,
        blocking_items: [
          {
            code: "missing_proof_id_card_copy",
            title: "proof:id_card_copy",
            description: "身份证明缺失。",
            severity: "blocking",
            asset_type: "proof:id_card_copy",
            required_for: "summer_internship_application",
            suggested_action: "补充后重新生成。"
          }
        ],
        warning_items: [],
        rationale: "存在阻塞性缺件。"
      }
    };

    const result = validateLifecycleDecision({
      library_id: "lib_demo_student_001",
      goal: "summer_internship_application",
      as_of_date: "2026-03-29",
      window_days: 60,
      asset_ids: ["asset_transcript_001"],
      profile,
      decision
    });

    expect(result.status).toBe("passed");
    expect(result.errors).toHaveLength(0);
  });

  it("validates build-asset-library decisions and rejects unknown string placeholders", () => {
    const decision: BuildAssetLibraryData = {
      library_id: "lib_demo_student_001",
      asset_cards: [
        {
          ...baseAsset,
          asset_id: "asset_resume_001",
          title: "Resume",
          holder_name: null,
          issuer_name: null,
          normalized_summary: "Resume summary",
          source_files: [
            {
              file_id: "file_resume_001",
              file_name: "resume.pdf",
              mime_type: "application/pdf"
            }
          ]
        }
      ],
      merged_assets: [],
      summary: {
        total_assets: 1,
        merged_groups: 0,
        anomalies: 1,
        unmerged_assets: 1
      }
    };

    const valid = validateBuildAssetLibraryDecision({
      library_id: "lib_demo_student_001",
      file_ids: ["file_resume_001"],
      decision
    });
    expect(valid.status).toBe("passed");

    const invalid = validateBuildAssetLibraryDecision({
      library_id: "lib_demo_student_001",
      file_ids: ["file_resume_001"],
      decision: {
        ...decision,
        asset_cards: [
          {
            ...decision.asset_cards[0],
            holder_name: "unknown"
          }
        ]
      }
    });

    expect(invalid.status).toBe("failed");
    expect(
      invalid.errors.some(
        (item) => item.code === "BUILD_ASSET_CARD_HOLDER_UNKNOWN_STRING"
      )
    ).toBe(true);
  });

  it("fails lifecycle validation when readiness conflicts with blocking items", () => {
    const profile = getRuleProfileBundle("summer_internship_application");
    const decision: CheckLifecycleData = {
      library_id: "lib_demo_student_001",
      as_of_date: "2026-03-29",
      window_days: 60,
      lifecycle_events: [],
      rule_matches: [],
      missing_items: {
        schema_version: "1.0",
        library_id: "lib_demo_student_001",
        diagnosis_id: "diag_001",
        target_goal: "summer_internship_application",
        rule_pack_id: profile.rule_pack_id,
        items: [
          {
            code: "missing_proof_id_card_copy",
            title: "proof:id_card_copy",
            description: "身份证明缺失。",
            severity: "blocking",
            asset_type: "proof:id_card_copy",
            required_for: "summer_internship_application",
            suggested_action: "补充后重新生成。"
          }
        ],
        available_asset_ids: ["asset_transcript_001"],
        gap_summary: "缺少 1 项材料。",
        next_actions: ["补充身份证明。"],
        blocking_level: "partial"
      },
      readiness: {
        ready_for_submission: true,
        blocking_items: [],
        warning_items: [],
        rationale: "错误地标记为可提交。"
      }
    };

    const result = validateLifecycleDecision({
      library_id: "lib_demo_student_001",
      goal: "summer_internship_application",
      as_of_date: "2026-03-29",
      window_days: 60,
      asset_ids: ["asset_transcript_001"],
      profile,
      decision
    });

    expect(result.status).toBe("failed");
    expect(result.errors.some((item) => item.code === "LIFECYCLE_READINESS_BLOCKING_CONFLICT")).toBe(
      true
    );
  });

  it("fails package validation when selected assets are unknown", () => {
    const profile = getRuleProfileBundle("summer_internship_application");
    const packagePlan: PackagePlan = {
      schema_version: "1.0",
      library_id: "lib_demo_student_001",
      package_id: "pkg_001",
      target_goal: "summer_internship_application",
      package_name: "summer-internship-application-package",
      selected_asset_ids: ["asset_missing_001"],
      selected_exports: [
        "personal-material-assets.xlsx",
        "renewal-checklist-60d.xlsx",
        "summer-internship-application-package.zip"
      ],
      missing_items_ref: "diag_001",
      generated_files: [
        {
          file_name: "personal-material-assets.xlsx",
          file_type: "xlsx",
          purpose: "Asset ledger export"
        },
        {
          file_name: "renewal-checklist-60d.xlsx",
          file_type: "xlsx",
          purpose: "60-day renewal checklist"
        },
        {
          file_name: "summer-internship-application-package.zip",
          file_type: "zip",
          purpose: "Submission package bundle"
        }
      ],
      submission_profile: "judge_demo_v1",
      readiness: {
        ready_for_submission: false,
        blocking_items: [
          {
            code: "missing_proof_id_card_copy",
            title: "proof:id_card_copy",
            description: "身份证明缺失。",
            severity: "blocking",
            asset_type: "proof:id_card_copy",
            required_for: "summer_internship_application",
            suggested_action: "补充后重新生成。"
          }
        ],
        warning_items: [],
        rationale: "存在阻塞性缺件。"
      },
      operator_notes: "先生成 truthful package。"
    };

    const result = validatePackagePlanDecision({
      library_id: "lib_demo_student_001",
      goal: "summer_internship_application",
      submission_profile: "judge_demo_v1",
      missing_items_ref: "diag_001",
      asset_ids: ["asset_transcript_001"],
      expected_readiness: packagePlan.readiness,
      profile,
      package_plan: packagePlan
    });

    expect(result.status).toBe("failed");
    expect(result.errors.some((item) => item.code === "PACKAGE_SELECTED_ASSET_UNKNOWN")).toBe(
      true
    );
  });

  it("creates an agent decision audit with a stable hash", () => {
    const audit = createAgentDecisionAudit({
      stage: "build_asset_library",
      library_id: "lib_demo_student_001",
      goal: "build_asset_library",
      profile_id: "build_asset_library",
      model: "glm-4.6",
      input_asset_ids: ["asset_transcript_001"],
      input_file_ids: ["file_transcript_001"],
      input_summary: "One transcript asset.",
      validation_status: "passed",
      result: { ok: true }
    });

    expect(audit.stage).toBe("build_asset_library");
    expect(audit.result_hash).toHaveLength(40);
  });
});

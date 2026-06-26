import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type {
  AgentDecisionAudit,
  AssetCard,
  CheckLifecycleData,
  MergedAsset,
  PackagePlan,
  ParsedFile
} from "@caixu/contracts";
import { openCaixuStorage } from "../src/index.js";

const storages: Array<ReturnType<typeof openCaixuStorage>> = [];

function makeStorage() {
  const dbPath = join(mkdtempSync(join(tmpdir(), "caixu-storage-")), "caixu.sqlite");
  const storage = openCaixuStorage(dbPath);
  storages.push(storage);
  return storage;
}

afterEach(() => {
  while (storages.length) {
    storages.pop()?.close();
  }
});

describe("@caixu/storage", () => {
  it("creates a library and stores parsed files", () => {
    const storage = makeStorage();
    const library = storage.createOrLoadLibrary(undefined, "demo_student");
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_001",
        file_name: "transcript.txt",
        file_path: "/tmp/transcript.txt",
        mime_type: "text/plain",
        size_bytes: 128,
        parse_status: "parsed",
        extracted_text: "Transcript content",
        extracted_summary: "Transcript",
        provider: "local"
      }
    ];

    storage.upsertParsedFiles(library.library_id, parsedFiles);

    expect(storage.listParsedFiles(library.library_id)).toHaveLength(1);
  });

  it("stores and queries assets", () => {
    const storage = makeStorage();
    const library = storage.createOrLoadLibrary("lib_demo_student_001");
    const assets: AssetCard[] = [
      {
        schema_version: "1.0",
        library_id: library.library_id,
        asset_id: "asset_transcript_001",
        material_type: "proof",
        title: "Transcript",
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
        source_files: [
          {
            file_id: "file_001",
            file_name: "transcript.txt",
            mime_type: "text/plain"
          }
        ],
        confidence: 0.98,
        normalized_summary: "Transcript for internship application.",
        asset_state: "active",
        review_status: "auto",
        last_verified_at: null
      }
    ];

    storage.upsertAssetCards(library.library_id, assets);
    const mergedAssets: MergedAsset[] = [
      {
        schema_version: "1.0",
        library_id: library.library_id,
        merged_asset_id: "merged_transcript_001",
        canonical_asset_id: "asset_transcript_001",
        selected_asset_id: "asset_transcript_001",
        superseded_asset_ids: ["asset_transcript_old_001"],
        dedupe_strategy: "newer_version_replaces_older",
        merge_reason: "new transcript replaces old one",
        status: "merged",
        version_order: [
          {
            asset_id: "asset_transcript_old_001",
            issue_date: "2025-03-01",
            expiry_date: null,
            source_file_count: 1
          },
          {
            asset_id: "asset_transcript_001",
            issue_date: "2026-03-01",
            expiry_date: null,
            source_file_count: 1
          }
        ]
      },
      {
        schema_version: "1.0",
        library_id: library.library_id,
        merged_asset_id: "merged_unrelated_001",
        canonical_asset_id: "asset_id_copy_001",
        selected_asset_id: "asset_id_copy_001",
        superseded_asset_ids: [],
        dedupe_strategy: "single_asset_group",
        merge_reason: "identity copy",
        status: "merged",
        version_order: [
          {
            asset_id: "asset_id_copy_001",
            issue_date: "2026-01-01",
            expiry_date: null,
            source_file_count: 1
          }
        ]
      }
    ];
    storage.upsertMergedAssets(library.library_id, mergedAssets);
    const query = storage.queryAssets({
      library_id: library.library_id,
      keyword: "Transcript",
      tag_filters_any: ["use:summer_internship_application"]
    });

    expect(query.asset_cards).toHaveLength(1);
    expect(query.asset_cards[0]?.asset_id).toBe("asset_transcript_001");
    expect(query.merged_assets).toHaveLength(1);
    expect(query.merged_assets[0]?.merged_asset_id).toBe("merged_transcript_001");
  });

  it("supports maintenance overview, review queue, patch, and archive", () => {
    const storage = makeStorage();
    const library = storage.createOrLoadLibrary("lib_demo_student_maintenance", "demo_student");
    storage.upsertAssetCards(library.library_id, [
      {
        schema_version: "1.0",
        library_id: library.library_id,
        asset_id: "asset_resume_001",
        material_type: "experience",
        title: "个人简历",
        holder_name: "Demo Student",
        issuer_name: null,
        issue_date: null,
        expiry_date: null,
        validity_status: "unknown",
        agent_tags: [
          "doc:resume",
          "entity:experience_record",
          "use:job_application",
          "risk:needs_review"
        ],
        reusable_scenarios: [],
        sensitivity_level: "medium",
        source_files: [
          {
            file_id: "file_resume_001",
            file_name: "resume.pdf",
            mime_type: "application/pdf"
          }
        ],
        confidence: 0.62,
        normalized_summary: "Demo Student 的个人简历。",
        asset_state: "active",
        review_status: "needs_review",
        last_verified_at: null
      }
    ]);

    const overview = storage.getLibraryOverview(library.library_id);
    const reviewQueue = storage.listReviewQueue(library.library_id);
    const patched = storage.patchAssetCard(library.library_id, "asset_resume_001", {
      normalized_summary: "Demo Student 的个人简历，已人工确认。",
      review_status: "reviewed"
    });
    const archived = storage.setAssetState(library.library_id, "asset_resume_001", "archived");

    expect(overview?.counts.needs_review_assets).toBe(1);
    expect(reviewQueue.asset_cards).toHaveLength(1);
    expect(patched?.asset_card.review_status).toBe("reviewed");
    expect(patched?.change_event.action).toBe("patch");
    expect(archived?.asset_card.asset_state).toBe("archived");
    expect(storage.queryAssets({ library_id: library.library_id }).asset_cards).toHaveLength(0);
  });

  it("stores lifecycle/package runs with audit sidecars", () => {
    const storage = makeStorage();
    const library = storage.createOrLoadLibrary("lib_demo_student_001");
    const lifecyclePayload: CheckLifecycleData = {
      library_id: library.library_id,
      as_of_date: "2026-03-29",
      window_days: 60,
      lifecycle_events: [],
      rule_matches: [],
      missing_items: {
        schema_version: "1.0",
        library_id: library.library_id,
        diagnosis_id: "diag_001",
        target_goal: "summer_internship_application",
        rule_pack_id: "cn.student.internship.v1",
        items: [],
        available_asset_ids: [],
        gap_summary: "No gap",
        next_actions: [],
        blocking_level: "none"
      },
      readiness: {
        ready_for_submission: true,
        blocking_items: [],
        warning_items: [],
        rationale: "Ready"
      }
    };
    const lifecycleAudit: AgentDecisionAudit = {
      decision_id: "decision_001",
      stage: "check_lifecycle",
      library_id: library.library_id,
      goal: "summer_internship_application",
      profile_id: "summer_internship_application",
      model: "glm-4.6",
      input_asset_ids: [],
      input_file_ids: [],
      input_summary: "Empty library audit.",
      validation_status: "passed",
      validation_errors: [],
      result_hash: "a".repeat(40),
      created_at: "2026-03-29T00:00:00.000Z"
    };

    storage.writeLifecycleRun(
      "run_001",
      lifecyclePayload,
      "summer_internship_application",
      lifecycleAudit
    );

    const lifecycleRun = storage.getLatestLifecycleRun(
      library.library_id,
      "summer_internship_application"
    );

    expect(lifecycleRun?.audit?.decision_id).toBe("decision_001");

    const packagePlan: PackagePlan = {
      schema_version: "1.0",
      library_id: library.library_id,
      package_id: "pkg_001",
      target_goal: "summer_internship_application",
      package_name: "summer-internship-application-package",
      selected_asset_ids: [],
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
      readiness: lifecyclePayload.readiness,
      operator_notes: "Ready to export."
    };
    const packageAudit: AgentDecisionAudit = {
      decision_id: "decision_002",
      stage: "build_package",
      library_id: library.library_id,
      goal: "summer_internship_application",
      profile_id: "summer_internship_application",
      model: "glm-4.6",
      input_asset_ids: [],
      input_file_ids: [],
      input_summary: "Package selection audit.",
      validation_status: "passed",
      validation_errors: [],
      result_hash: "b".repeat(40),
      created_at: "2026-03-29T00:00:01.000Z"
    };

    storage.writePackageRun(packagePlan, "/tmp/package", packageAudit);
    const packageRun = storage.getPackageRun("pkg_001");

    expect(packageRun?.audit?.decision_id).toBe("decision_002");
    expect(packageRun?.output_dir).toBe("/tmp/package");
  });
});

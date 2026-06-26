import { describe, expect, it } from "vitest";
import {
  agentDecisionAuditSchema,
  assetCardSchema,
  buildAssetLibraryDataSchema,
  deriveReusableScenariosFromAgentTags,
  makeToolResult,
  parseMaterialsDataSchema,
  ruleProfileSchema,
  sanitizeAgentTags,
  toolResultSchema
} from "../src/index.js";

describe("@caixu/contracts", () => {
  it("validates a basic asset card", () => {
    const parsed = assetCardSchema.parse({
      schema_version: "1.0",
      library_id: "lib_demo_student_001",
      asset_id: "asset_transcript_001",
      material_type: "proof",
      title: "Transcript",
      holder_name: "Demo Student",
      issuer_name: null,
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
          file_id: "file_transcript_001",
          file_name: "transcript.pdf",
          mime_type: "application/pdf"
        }
      ],
      confidence: 0.98,
      normalized_summary: "Transcript for internship applications.",
      asset_state: "active",
      review_status: "auto",
      last_verified_at: null
    });

    expect(parsed.asset_id).toBe("asset_transcript_001");
  });

  it("derives compatibility reusable_scenarios from agent tags", () => {
    const tags = sanitizeAgentTags({
      material_type: "proof",
      title: "CET-6 成绩单",
      normalized_summary: "语言证书，可用于暑期实习申请。",
      agent_tags: ["use:summer_internship_application", "entity:language_certificate"]
    });

    expect(tags).toEqual(
      expect.arrayContaining([
        "use:summer_internship_application",
        "entity:language_certificate"
      ])
    );
    expect(deriveReusableScenariosFromAgentTags(tags)).toEqual([
      "summer_internship_application"
    ]);
  });

  it("wraps structured data in ToolResult", () => {
    const schema = toolResultSchema(buildAssetLibraryDataSchema);
    const parsed = schema.parse(
      makeToolResult("success", {
        library_id: "lib_demo",
        asset_cards: [],
        merged_assets: [],
        summary: {
          total_assets: 0,
          merged_groups: 0,
          anomalies: 0,
          unmerged_assets: 0
        }
      })
    );

    expect(parsed.status).toBe("success");
    expect(parsed.data?.library_id).toBe("lib_demo");
  });

  it("supports parse_materials payload with parsed file details", () => {
    const parsed = parseMaterialsDataSchema.parse({
      file_ids: ["file_001", "file_002"],
      parsed_count: 2,
      failed_count: 0,
      warning_count: 1,
      skipped_count: 1,
      parsed_files: [
        {
          file_id: "file_001",
          file_name: "transcript.txt",
          file_path: "/tmp/transcript.txt",
          mime_type: "text/plain",
          size_bytes: 128,
          parse_status: "parsed",
          extracted_text: "Transcript",
          extracted_summary: "Plain text transcript",
          provider: "local"
        },
        {
          file_id: "file_002",
          file_name: "id-card.pdf",
          file_path: "/tmp/id-card.pdf",
          mime_type: "application/pdf",
          size_bytes: 1024,
          parse_status: "parsed",
          extracted_text: "ID CARD",
          extracted_summary: "OCR text",
          provider: "zhipu_parser_lite"
        }
      ],
      failed_files: [],
      warning_files: [
        {
          code: "ZHIPU_PARSER_EMPTY_CONTENT",
          message: "Parser branch returned empty text content.",
          retryable: false,
          file_id: "file_002",
          file_name: "id-card.pdf"
        }
      ],
      skipped_files: [
        {
          code: "UNSUPPORTED_FILE_SKIPPED",
          message: "Skipped archive.zip: unsupported_zip_for_ingestion",
          retryable: false,
          file_id: "file_003",
          file_name: "archive.zip"
        }
      ]
    });

    expect(parsed.parsed_files[1]?.provider).toBe("zhipu_parser_lite");
  });

  it("validates a rule profile bundle", () => {
    const parsed = ruleProfileSchema.parse({
      profile_id: "summer_internship_application",
      display_name: "暑期实习申请",
      bundle_version: "2026.03",
      rule_pack_id: "cn.student.internship.v1",
      default_window_days: 60,
      scene_summary: "Internship application bundle.",
      requirements: [
        {
          code: "proof:transcript",
          title: "成绩单",
          required: true,
          blocking: false,
          description: "Core transcript requirement."
        }
      ],
      lifecycle_focus: ["check windows"],
      package_guidance: ["build truthful package"],
      readiness_policy: {
        allow_submit_with_blocking_items: false,
        allow_truthful_package_when_blocked: true
      },
      notes: "Bundle note."
    });

    expect(parsed.bundle_version).toBe("2026.03");
  });

  it("validates an agent decision audit", () => {
    const parsed = agentDecisionAuditSchema.parse({
      decision_id: "decision_001",
      stage: "check_lifecycle",
      library_id: "lib_demo_student_001",
      goal: "summer_internship_application",
      profile_id: "summer_internship_application",
      model: "glm-4.6",
      input_asset_ids: ["asset_transcript_001"],
      input_file_ids: ["file_transcript_001"],
      input_summary: "One transcript asset.",
      validation_status: "passed",
      validation_errors: [],
      result_hash: "a".repeat(40),
      created_at: "2026-03-29T00:00:00.000Z"
    });

    expect(parsed.stage).toBe("check_lifecycle");
  });
});

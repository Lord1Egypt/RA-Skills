import { execFileSync } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import type { AssetCard, CheckLifecycleData, ParsedFile } from "@caixu/contracts";
import { buildPackage, exportLedgers } from "../src/index.js";

const outputDir = mkdtempSync(join(tmpdir(), "caixu-docgen-"));
const sourceTextPath = join(outputDir, "transcript-source.txt");
writeFileSync(sourceTextPath, "Transcript source content", "utf8");

const assets: AssetCard[] = [
  {
    schema_version: "1.0",
    library_id: "lib_demo_student_001",
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
        file_id: "file_transcript_001",
        file_name: "transcript.txt",
        mime_type: "text/plain",
        file_path: sourceTextPath
      }
    ],
    confidence: 0.98,
    normalized_summary: "Transcript",
    asset_state: "active",
    review_status: "auto",
    last_verified_at: null
  }
];

const lifecycle: CheckLifecycleData = {
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
    rule_pack_id: "cn.student.internship.v1",
    items: [],
    available_asset_ids: ["asset_transcript_001"],
    gap_summary: "No blocking gap.",
    next_actions: ["Build package."],
    blocking_level: "none"
  },
  readiness: {
    ready_for_submission: true,
    blocking_items: [],
    warning_items: [],
    rationale: "Ready"
  }
};

const parsedFiles: ParsedFile[] = [
  {
    file_id: "file_transcript_001",
    file_name: "transcript.txt",
    file_path: sourceTextPath,
    mime_type: "text/plain",
    size_bytes: 25,
    parse_status: "parsed",
    extracted_text: "Transcript source content",
    extracted_summary: "Transcript source content",
    provider: "local"
  }
];

describe("@caixu/docgen", () => {
  it("generates ledger files", async () => {
    const result = await exportLedgers({
      library_id: "lib_demo_student_001",
      output_dir: outputDir,
      assets,
      lifecycle,
      as_of_date: "2026-03-29",
      window_days: 60
    });

    expect(result.exported_files).toHaveLength(2);
    await expect(stat(result.exported_files[0]!)).resolves.toBeTruthy();
  });

  it("generates a submission package", async () => {
    const result = await buildPackage({
      library_id: "lib_demo_student_001",
      goal: "summer_internship_application",
      output_dir: outputDir,
      assets,
      parsed_files: parsedFiles,
      readiness: lifecycle.readiness,
      missing_items_ref: lifecycle.missing_items.diagnosis_id,
      submission_profile: "judge_demo_v1"
    });

    expect(result.package_plan.submission_profile).toBe("judge_demo_v1");
    await expect(stat(result.exported_files[0]!)).resolves.toBeTruthy();
    const zipListing = execFileSync("unzip", ["-Z1", result.exported_files[0]!], {
      encoding: "utf8"
    });
    expect(zipListing).toContain("materials/transcript-source.txt");
  });
});

import { afterEach, describe, expect, it, vi } from "vitest";
import type { LocalFile, ParsedFile } from "@caixu/contracts";
import { resolve } from "node:path";
import {
  createOpenAICompatibleSkillModelClient,
  createMockSkillModelClient,
  loadSkillBundle,
  normalizeQueryAssetsRequest,
  runBuildAssetLibrarySkill,
  runIngestRouteDecisionSkill
} from "../src/index.js";

const repoRoot = new URL("../../../../", import.meta.url).pathname;

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("@caixu/skill-runner", () => {
  it("loads the root skill bundle using the frontmatter name", async () => {
    const bundle = await loadSkillBundle(repoRoot);

    expect(bundle.skillName).toBe("caixu-skill");
    expect(bundle.skillDir).toBe(resolve(repoRoot));
    expect(bundle.references.map((reference) => reference.name)).toEqual(
      expect.arrayContaining(["workflow.md", "tool-contracts.md", "failure-modes.md"])
    );
  });

  it("retries invalid build-asset responses and returns nullable uncertain fields", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_001",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航 个人简历",
        extracted_summary: "吕佳航 个人简历",
        provider: "hybrid"
      }
    ];

    let attemptCount = 0;
    const events: Array<{ event: string; decision_type?: string }> = [];
    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_001",
                include_in_library: true,
                document_role: "personal_experience",
                reason: null
              }
            ]
          })
        };
      }

      if (taskTitle.includes("Extract canonical asset_cards for triaged files")) {
        attemptCount += 1;
        if (attemptCount === 1) {
          return {
            model: "mock-build-asset",
            content: JSON.stringify({
              decisions: [
                {
                  file_id: "file_resume_001",
                  asset_card: {
                    schema_version: "1.0",
                    library_id: "lib_demo",
                    asset_id: "asset_file_resume_001",
                    material_type: "experience",
                    title: "Resume",
                    holder_name: "unknown",
                    issuer_name: "unknown",
                    issue_date: null,
                    expiry_date: null,
                    validity_status: "long_term",
                    agent_tags: [
                      "doc:resume",
                      "entity:experience_record",
                      "use:summer_internship_application",
                      "risk:auto"
                    ],
                    reusable_scenarios: ["summer_internship_application"],
                    sensitivity_level: "medium",
                    source_files: [
                      {
                        file_id: "file_resume_001",
                        file_name: "resume.pdf",
                        mime_type: "application/pdf",
                        file_path: "/tmp/resume.pdf"
                      }
                    ],
                    confidence: 0.85,
                    normalized_summary: "Resume"
                  },
                  skip_reason: null
                }
              ]
            })
          };
        }

        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_001",
                asset_card: {
                  schema_version: "1.0",
                  library_id: "lib_demo",
                  asset_id: "asset_file_resume_001",
                  material_type: "experience",
                  title: "Resume",
                  holder_name: null,
                  issuer_name: null,
                  issue_date: null,
                  expiry_date: null,
                  validity_status: "long_term",
                  agent_tags: [
                    "doc:resume",
                    "entity:experience_record",
                    "use:summer_internship_application",
                    "risk:auto"
                  ],
                  reusable_scenarios: ["summer_internship_application"],
                  sensitivity_level: "medium",
                  source_files: [
                    {
                      file_id: "file_resume_001",
                      file_name: "resume.pdf",
                      mime_type: "application/pdf",
                      file_path: "/tmp/resume.pdf"
                    }
                  ],
                  confidence: 0.85,
                  normalized_summary: "Resume"
                },
                skip_reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          merged_assets: []
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient,
      onEvent(event) {
        events.push({
          event: event.event,
          decision_type: "decision_type" in event ? event.decision_type : undefined
        });
      }
    });

    expect(result.status).toBe("success");
    expect(result.data?.asset_cards).toHaveLength(1);
    expect(result.data?.asset_cards[0]?.holder_name).toBeNull();
    expect(attemptCount).toBe(1);
    expect(events).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          event: "skill.attempt.complete",
          decision_type: "asset_extraction"
        })
      ])
    );
  });

  it("skips files excluded by document triage before extraction", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_noise_001",
        file_name: "poster.jpg",
        file_path: "/tmp/poster.jpg",
        mime_type: "image/jpeg",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "社团招新海报",
        extracted_summary: "社团招新海报",
        provider: "zhipu_ocr"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_noise_001",
                include_in_library: false,
                document_role: "noise",
                reason: "promotional_poster_not_a_material_asset"
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: []
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("partial");
    expect(result.data).toBeUndefined();
    expect(result.skipped_files).toEqual([
      expect.objectContaining({
        file_id: "file_noise_001",
        reason: "promotional_poster_not_a_material_asset"
      })
    ]);
  });

  it("uses decision-specific prompt context and text previews for build-asset-library", async () => {
    const longText = `BEGIN ${"x".repeat(5000)} TAIL_UNIQUE`;
    const prompts: Array<{ taskTitle: string; userPrompt: string }> = [];
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_long_001",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        size_bytes: 4096,
        parse_status: "parsed",
        extracted_text: longText,
        extracted_summary: "long summary",
        provider: "hybrid"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle, userPrompt }) => {
      prompts.push({ taskTitle, userPrompt });

      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_long_001",
                include_in_library: true,
                document_role: "personal_experience",
                reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_long_001",
              asset_card: {
                schema_version: "1.0",
                library_id: "lib_demo",
                asset_id: "asset_file_long_001",
                material_type: "experience",
                title: "Resume",
                holder_name: null,
                issuer_name: null,
                issue_date: null,
                expiry_date: null,
                validity_status: "long_term",
                agent_tags: [
                  "doc:resume",
                  "entity:experience_record",
                  "use:summer_internship_application",
                  "risk:auto"
                ],
                reusable_scenarios: ["summer_internship_application"],
                sensitivity_level: "medium",
                source_files: [
                  {
                    file_id: "file_long_001",
                    file_name: "resume.pdf",
                    mime_type: "application/pdf",
                    file_path: "/tmp/resume.pdf"
                  }
                ],
                confidence: 0.84,
                normalized_summary: "Resume"
              },
              skip_reason: null
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("success");

    const triagePrompt = prompts.find((item) =>
      item.taskTitle.includes("Decide which parsed files should enter the asset library")
    )?.userPrompt;
    const extractionPrompt = prompts.find((item) =>
      item.taskTitle.includes("Extract canonical asset_cards for triaged files")
    )?.userPrompt;

    expect(triagePrompt).toBeTruthy();
    expect(extractionPrompt).toBeTruthy();

    expect(triagePrompt).toContain("# workflow.md");
    expect(triagePrompt).toContain("# output-patterns.md");
    expect(triagePrompt).not.toContain("# tool-contracts.md");
    expect(triagePrompt).not.toContain("# failure-modes.md");
    expect(triagePrompt).toContain("\"text_preview\"");
    expect(triagePrompt).not.toContain("\"text_length\"");
    expect(triagePrompt).not.toContain("\"extracted_text\"");
    expect(triagePrompt).not.toContain("TAIL_UNIQUE");
    expect(triagePrompt!.length).toBeLessThan(7000);

    expect(extractionPrompt).toContain("# tool-contracts.md");
    expect(extractionPrompt).toContain("# failure-modes.md");
    expect(extractionPrompt).toContain("# output-patterns.md");
    expect(extractionPrompt).not.toContain("# workflow.md");
    expect(extractionPrompt).toContain("\"document_role_hint\":\"personal_experience\"");
    expect(extractionPrompt).toContain("\"text_preview\"");
    expect(extractionPrompt).not.toContain("\"required_asset_card_fields\"");
    expect(extractionPrompt).not.toContain("\"text_length\"");
    expect(extractionPrompt).not.toContain("TAIL_UNIQUE");
  });

  it("fills structural asset-card defaults during extraction without guessing factual fields", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_002",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航 个人简历",
        extracted_summary: "吕佳航 个人简历，可用于实习申请。",
        provider: "zhipu_parser_lite"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_002",
                include_in_library: true,
                document_role: "personal_experience",
                reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_resume_002",
              asset_card: {
                material_type: "experience",
                holder_name: null,
                issuer_name: null,
                issue_date: null,
                expiry_date: null
              },
              skip_reason: null
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.asset_cards).toHaveLength(1);
    expect(result.data?.asset_cards[0]).toEqual(
      expect.objectContaining({
        schema_version: "1.0",
        library_id: "lib_demo",
        asset_id: "asset_file_resume_002",
        material_type: "experience",
        holder_name: null,
        issuer_name: null,
        validity_status: "unknown",
        sensitivity_level: "medium"
      })
    );
    expect(result.data?.asset_cards[0]?.normalized_summary).toContain("个人简历");
    expect(result.data?.asset_cards[0]?.normalized_summary).not.toContain("可用于");
  });

  it("falls back from recoverable document-triage failure into extraction", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_003",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航 个人简历",
        extracted_summary: "吕佳航 个人简历，可用于实习申请。",
        provider: "zhipu_parser_lite"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle, attempt }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        throw new Error("rate limit while running document triage");
      }

      if (taskTitle.includes("Extract canonical asset_cards for triaged files")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_003",
                asset_card: {
                  material_type: "experience",
                  holder_name: "吕佳航",
                  issuer_name: null,
                  issue_date: null,
                  expiry_date: null,
                  confidence: 0.72
                },
                skip_reason: null
              }
            ]
          })
        };
      }

      return {
        model: `mock-build-asset-${attempt}`,
        content: JSON.stringify({
          merged_assets: []
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("partial");
    expect(result.data?.asset_cards).toHaveLength(1);
    expect(result.data?.asset_cards[0]).toEqual(
      expect.objectContaining({
        material_type: "experience",
        holder_name: "吕佳航"
      })
    );
    expect(result.errors).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          code: "SKILL_RUNNER_RATE_LIMITED"
        })
      ])
    );
  });

  it("forces resume assets to stay conservative", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_004",
        file_name: "12-24简历.pdf",
        file_path: "/tmp/12-24简历.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航\n个人简历\n教育背景",
        extracted_summary: "吕佳航的个人简历，可用于暑期实习申请。",
        provider: "zhipu_parser_lite"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_004",
                include_in_library: true,
                document_role: "personal_experience",
                reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_resume_004",
              asset_card: {
                material_type: "proof",
                title: "个人简历",
                holder_name: "吕佳航",
                issuer_name: "某机构",
                issue_date: "明年",
                expiry_date: "soon",
                normalized_summary: "吕佳航的个人简历，可用于暑期实习申请。"
              },
              skip_reason: null
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.asset_cards[0]).toEqual(
      expect.objectContaining({
        material_type: "experience",
        issuer_name: null,
        issue_date: null,
        expiry_date: null
      })
    );
    expect(result.data?.asset_cards[0]?.normalized_summary).not.toContain("可用于");
  });

  it("skips non-owner personal materials after owner inference", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_owner",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航\n个人简历\n教育背景",
        extracted_summary: "吕佳航的个人简历",
        provider: "zhipu_parser_lite"
      },
      {
        file_id: "file_foreign_cert",
        file_name: "award.pdf",
        file_path: "/tmp/award.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "谢麒麟 荣获二等奖",
        extracted_summary: "谢麒麟的获奖证书",
        provider: "zhipu_parser_lite"
      }
    ];

    let extractionAttempt = 0;
    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_owner",
                include_in_library: true,
                document_role: "personal_experience",
                reason: null
              },
              {
                file_id: "file_foreign_cert",
                include_in_library: true,
                document_role: "personal_proof",
                reason: null
              }
            ]
          })
        };
      }

      extractionAttempt += 1;
      if (extractionAttempt === 1) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_resume_owner",
                asset_card: {
                  material_type: "experience",
                  title: "个人简历",
                  holder_name: "吕佳航",
                  issuer_name: null,
                  issue_date: null,
                  expiry_date: null,
                  normalized_summary: "吕佳航的个人简历。"
                },
                skip_reason: null
              },
              {
                file_id: "file_foreign_cert",
                asset_card: {
                  material_type: "proof",
                  title: "获奖证书",
                  holder_name: "谢麒麟",
                  issuer_name: "青海省科学技术协会",
                  issue_date: "2025-07",
                  expiry_date: null,
                  normalized_summary: "谢麒麟获得的获奖证书。"
                },
                skip_reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_resume_owner",
              asset_card: {
                material_type: "experience",
                title: "个人简历",
                holder_name: "吕佳航",
                issuer_name: null,
                issue_date: null,
                expiry_date: null,
                normalized_summary: "吕佳航的个人简历。"
              },
              skip_reason: null
            },
            {
              file_id: "file_foreign_cert",
              asset_card: null,
              skip_reason: "does_not_belong_to_inferred_owner"
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      parsed_file_context: parsedFiles,
      existing_assets: [
        {
          schema_version: "1.0",
          library_id: "lib_demo",
          asset_id: "asset_owner_profile",
          material_type: "experience",
          title: "个人简历",
          holder_name: "吕佳航",
          issuer_name: null,
          issue_date: null,
          expiry_date: null,
          validity_status: "unknown",
          agent_tags: [
            "doc:resume",
            "entity:experience_record",
            "use:general_reference",
            "risk:reviewed"
          ],
          reusable_scenarios: [],
          sensitivity_level: "medium",
          source_files: [
            {
              file_id: "file_owner_profile",
              file_name: "resume.pdf",
              mime_type: "application/pdf"
            }
          ],
          confidence: 0.8,
          normalized_summary: "吕佳航的个人简历。",
          asset_state: "active",
          review_status: "reviewed",
          last_verified_at: "2026-03-29T00:00:00.000Z"
        }
      ],
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.asset_cards).toHaveLength(1);
    expect(result.data?.asset_cards[0]?.holder_name).toBe("吕佳航");
    expect(result.skipped_files).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          file_id: "file_foreign_cert",
          reason: "does_not_belong_to_inferred_owner"
        })
      ])
    );
  });

  it("keeps public notices out unless they map to owner", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_notice_001",
        file_name: "获奖名单.pdf",
        file_path: "/tmp/获奖名单.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "获奖名单 吕佳航",
        extracted_summary: "获奖名单公示",
        provider: "zhipu_parser_lite"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle, attempt }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: `mock-build-asset-${attempt}`,
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_notice_001",
                include_in_library: true,
                document_role: "public_notice",
                reason: null
              }
            ]
          })
        };
      }

      if (attempt === 1) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_notice_001",
                asset_card: {
                  material_type: "proof",
                  title: "获奖名单",
                  holder_name: null,
                  issuer_name: "某学校",
                  issue_date: null,
                  expiry_date: null,
                  normalized_summary: "获奖名单。"
                },
                skip_reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_notice_001",
              asset_card: null,
              skip_reason: "public_notice_without_unique_owner_mapping"
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      existing_assets: [
        {
          schema_version: "1.0",
          library_id: "lib_demo",
          asset_id: "asset_owner_resume",
          material_type: "experience",
          title: "个人简历",
          holder_name: "吕佳航",
          issuer_name: null,
          issue_date: null,
          expiry_date: null,
          validity_status: "unknown",
          agent_tags: [
            "doc:resume",
            "entity:experience_record",
            "use:general_reference",
            "risk:reviewed"
          ],
          reusable_scenarios: [],
          sensitivity_level: "medium",
          source_files: [
            {
              file_id: "file_owner_resume",
              file_name: "resume.pdf",
              mime_type: "application/pdf"
            }
          ],
          confidence: 0.8,
          normalized_summary: "吕佳航的个人简历。",
          asset_state: "active",
          review_status: "reviewed",
          last_verified_at: "2026-03-29T00:00:00.000Z"
        }
      ],
      modelClient
    });

    expect(result.status).toBe("partial");
    expect(result.data).toBeUndefined();
    expect(result.skipped_files).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          file_id: "file_notice_001",
          reason: "public_notice_without_unique_owner_mapping"
        })
      ])
    );
  });

  it("merges duplicate resume versions conservatively", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_resume_a",
        file_name: "简历-v1.pdf",
        file_path: "/tmp/简历-v1.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航 个人简历 教育背景 项目经验",
        extracted_summary: "吕佳航个人简历，包含教育背景和项目经验。",
        provider: "zhipu_parser_lite"
      },
      {
        file_id: "file_resume_b",
        file_name: "简历-v2.pdf",
        file_path: "/tmp/简历-v2.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "吕佳航 个人简历 教育背景 项目经验",
        extracted_summary: "吕佳航个人简历，包含教育背景和项目经验。",
        provider: "zhipu_parser_lite"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: parsedFiles.map((file) => ({
              file_id: file.file_id,
              include_in_library: true,
              document_role: "personal_experience",
              reason: null
            }))
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: parsedFiles.map((file, index) => ({
            file_id: file.file_id,
            asset_card: {
              material_type: "experience",
              title: "个人简历",
              holder_name: "吕佳航",
              issuer_name: null,
              issue_date: null,
              expiry_date: null,
              confidence: 0.7 + index * 0.05,
              normalized_summary: "吕佳航的个人简历，包含教育背景、技能和项目经验。"
            },
            skip_reason: null
          }))
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      parsed_file_context: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.merged_assets).toHaveLength(1);
    expect(result.data?.merged_assets[0]).toEqual(
      expect.objectContaining({
        dedupe_strategy: "conservative_resume_similarity",
        selected_asset_id: "asset_file_resume_b"
      })
    );
  });

  it("normalizes natural-language asset queries through the query skill", async () => {
    const modelClient = createMockSkillModelClient(async () => ({
      model: "mock-query",
      content: JSON.stringify({
        material_types: ["proof"],
        keyword: null,
        semantic_query: "暑期实习申请可复用的证明材料",
        tag_filters_any: ["use:summer_internship_application", "doc:proof"],
        tag_filters_all: [],
        limit: 12,
        validity_statuses: [],
        explanation: "Mapped proof-like internship materials to deterministic filters.",
        next_recommended_skill: ["check-lifecycle"]
      })
    }));

    const result = await normalizeQueryAssetsRequest({
      skillDir: `${repoRoot}caixu-query-assets`,
      natural_language_query: "帮我找可用于暑期实习申请的证明材料",
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.material_types).toEqual(["proof"]);
    expect(result.data?.semantic_query).toBe("暑期实习申请可复用的证明材料");
    expect(result.data?.tag_filters_any).toEqual([
      "use:summer_internship_application",
      "doc:proof"
    ]);
  });

  it("uses compact route-decision prompt context for ingest-materials", async () => {
    const prompts: Array<{ taskTitle: string; userPrompt: string; systemPrompt: string }> = [];
    const files: LocalFile[] = [
      {
        file_id: "file_text_001",
        file_name: "transcript.txt",
        file_path: "/tmp/transcript.txt",
        mime_type: "text/plain",
        extension: ".txt",
        size_bytes: 128,
        suggested_route: "text",
        skip_reason: null
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle, userPrompt, systemPrompt }) => {
      prompts.push({ taskTitle, userPrompt, systemPrompt });
      return {
        model: "mock-ingest",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_text_001",
              route: "text",
              reason: null
            }
          ]
        })
      };
    });

    const result = await runIngestRouteDecisionSkill({
      skillDir: `${repoRoot}caixu-ingest-materials`,
      files,
      modelClient
    });

    expect(result.status).toBe("success");

    const prompt = prompts[0]?.userPrompt ?? "";
    const systemPrompt = prompts[0]?.systemPrompt ?? "";
    expect(prompt).toContain("# workflow.md");
    expect(prompt).toContain("# tool-contracts.md");
    expect(prompt).toContain("# failure-modes.md");
    expect(prompt).toContain("# output-patterns.md");
    expect(prompt).toContain("\"suggested_route\":\"text\"");
    expect(prompt).not.toContain("\"mime_type\"");
    expect(prompt).not.toContain("\"size_bytes\"");
    expect(prompt.length).toBeLessThan(5000);
    expect(systemPrompt).toContain("compact route-selection task");
    expect(systemPrompt).toContain("Mirror suggested_route");
  });

  it("retries 429 responses before returning a successful model completion", async () => {
    const events: Array<{ event: string; status_code: number | null }> = [];
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ error: { message: "rate limited" } }), {
          status: 429,
          headers: {
            "content-type": "application/json",
            "retry-after": "0"
          }
        })
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            model: "glm-4.6",
            choices: [
              {
                message: {
                  content: "{\"ok\":true}"
                }
              }
            ]
          }),
          {
            status: 200,
            headers: {
              "content-type": "application/json"
            }
          }
        )
      );
    vi.stubGlobal("fetch", fetchMock);

    const client = createOpenAICompatibleSkillModelClient({
      apiKey: "agent-key",
      model: "glm-4.6",
      timeoutMs: 1000,
      httpMaxAttempts: 2,
      httpBaseDelayMs: 10,
      httpMaxDelayMs: 10,
      minIntervalMs: 0,
      onEvent(event) {
        events.push({
          event: event.event,
          status_code: event.status_code
        });
      }
    });

    const result = await client({
      skillName: "caixu-build-asset-library",
      attempt: 1,
      taskTitle: "retry rate limit",
      systemPrompt: "system",
      userPrompt: "user"
    });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(result.model).toBe("glm-4.6");
    expect(result.content).toBe("{\"ok\":true}");
    expect(events).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          event: "http.retry_scheduled",
          status_code: 429
        }),
        expect.objectContaining({
          event: "http.cooldown_wait"
        })
      ])
    );
  });

  it("surfaces reasoning-only responses as a dedicated model error", async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          model: "glm-4.6",
          choices: [
            {
              finish_reason: "length",
              message: {
                reasoning_content: "I should think step by step before returning JSON."
              }
            }
          ]
        }),
        {
          status: 200,
          headers: {
            "content-type": "application/json"
          }
        }
      )
    );
    vi.stubGlobal("fetch", fetchMock);

    const client = createOpenAICompatibleSkillModelClient({
      apiKey: "agent-key",
      model: "glm-4.6",
      timeoutMs: 1000,
      httpMaxAttempts: 1,
      httpBaseDelayMs: 10,
      httpMaxDelayMs: 10,
      minIntervalMs: 0
    });

    await expect(
      client({
        skillName: "caixu-build-asset-library",
        attempt: 1,
        taskTitle: "reasoning only response",
        systemPrompt: "system",
        userPrompt: "user"
      })
    ).rejects.toMatchObject({
      code: "SKILL_RUNNER_REASONING_ONLY_RESPONSE"
    });
  });

  it("normalizes missing route fields to suggested routes", async () => {
    const files: LocalFile[] = [
      {
        file_id: "file_pdf_001",
        file_name: "resume.pdf",
        file_path: "/tmp/resume.pdf",
        mime_type: "application/pdf",
        extension: ".pdf",
        size_bytes: 1024,
        suggested_route: "parser_lite",
        skip_reason: null
      }
    ];

    const result = await runIngestRouteDecisionSkill({
      skillDir: `${repoRoot}caixu-ingest-materials`,
      files,
      modelClient: createMockSkillModelClient(async () => ({
        model: "mock-ingest",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_pdf_001"
            }
          ]
        })
      }))
    });

    expect(result.status).toBe("success");
    expect(result.data?.decisions).toEqual([
      {
        file_id: "file_pdf_001",
        route: "parser_lite",
        reason: null
      }
    ]);
  });

  it("normalizes partial asset extraction output instead of failing on omitted nullable fields", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_cert_001",
        file_name: "certificate.pdf",
        file_path: "/tmp/certificate.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "测试学生 获奖证书",
        extracted_summary: "测试学生 获奖证书",
        provider: "hybrid"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_cert_001",
                include_in_library: true,
                document_role: "personal_proof"
              }
            ]
          })
        };
      }

      if (taskTitle.includes("Extract canonical asset_cards for triaged files")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_cert_001",
                asset_card: {
                  title: "获奖证书",
                  holder_name: "测试学生",
                  issuer_name: "青海大学",
                  issue_date: "2026-03-01",
                  expiry_date: null,
                  validity_status: "long_term",
                  agent_tags: [
                    "doc:certificate",
                    "entity:award_certificate",
                    "use:summer_internship_application",
                    "risk:auto"
                  ],
                  reusable_scenarios: ["summer_internship_application"],
                  sensitivity_level: "medium",
                  source_files: [
                    {
                      file_id: "file_cert_001",
                      file_name: "certificate.pdf",
                      mime_type: "application/pdf",
                      file_path: "/tmp/certificate.pdf"
                    }
                  ],
                  confidence: 0.91,
                  normalized_summary: "测试学生的获奖证书。"
                }
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          merged_assets: []
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("success");
    expect(result.data?.asset_cards).toHaveLength(1);
    expect(result.data?.asset_cards[0]).toEqual(
      expect.objectContaining({
        material_type: "proof",
        title: "获奖证书"
      })
    );
  });

  it("repairs trailing-comma JSON and reasoning-only JSON responses from the live-model client", async () => {
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            model: "glm-4.6",
            choices: [
              {
                finish_reason: "stop",
                message: {
                  content: "{\"decisions\":[{\"file_id\":\"file_1\",\"route\":\"text\",\"reason\":null},],}"
                }
              }
            ]
          }),
          {
            status: 200,
            headers: { "content-type": "application/json" }
          }
        )
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            model: "glm-4.6",
            choices: [
              {
                finish_reason: "stop",
                message: {
                  content: "",
                  reasoning_content:
                    "analysis... {\"decisions\":[{\"file_id\":\"file_1\",\"route\":\"text\",\"reason\":null}]}"
                }
              }
            ]
          }),
          {
            status: 200,
            headers: { "content-type": "application/json" }
          }
        )
      );
    vi.stubGlobal("fetch", fetchMock);

    const modelClient = createOpenAICompatibleSkillModelClient({
      apiKey: "test-key",
      model: "glm-4.6",
      timeoutMs: 5_000,
      minIntervalMs: 0,
      httpBaseDelayMs: 1,
      httpMaxDelayMs: 1
    });

    const files: LocalFile[] = [
      {
        file_id: "file_1",
        file_name: "resume.txt",
        file_path: "/tmp/resume.txt",
        mime_type: "text/plain",
        extension: ".txt",
        size_bytes: 10,
        suggested_route: "text",
        skip_reason: null
      }
    ];

    const trailingCommaResult = await runIngestRouteDecisionSkill({
      skillDir: `${repoRoot}caixu-ingest-materials`,
      files,
      modelClient
    });
    const reasoningOnlyResult = await runIngestRouteDecisionSkill({
      skillDir: `${repoRoot}caixu-ingest-materials`,
      files,
      modelClient
    });

    expect(trailingCommaResult.status).toBe("success");
    expect(reasoningOnlyResult.status).toBe("success");
    expect(trailingCommaResult.data?.decisions[0]?.route).toBe("text");
    expect(reasoningOnlyResult.data?.decisions[0]?.route).toBe("text");
  });

  it("downgrades incomplete asset cards to skipped decisions instead of failing the batch schema", async () => {
    const parsedFiles: ParsedFile[] = [
      {
        file_id: "file_cert_002",
        file_name: "certificate.pdf",
        file_path: "/tmp/certificate.pdf",
        mime_type: "application/pdf",
        size_bytes: 1024,
        parse_status: "parsed",
        extracted_text: "测试学生 获奖证书",
        extracted_summary: "测试学生 获奖证书",
        provider: "hybrid"
      }
    ];

    const modelClient = createMockSkillModelClient(async ({ taskTitle }) => {
      if (taskTitle.includes("Decide which parsed files should enter the asset library")) {
        return {
          model: "mock-build-asset",
          content: JSON.stringify({
            decisions: [
              {
                file_id: "file_cert_002",
                include_in_library: true,
                document_role: "personal_proof",
                reason: null
              }
            ]
          })
        };
      }

      return {
        model: "mock-build-asset",
        content: JSON.stringify({
          decisions: [
            {
              file_id: "file_cert_002",
              asset_card: "broken-asset-card"
            }
          ]
        })
      };
    });

    const result = await runBuildAssetLibrarySkill({
      skillDir: `${repoRoot}caixu-build-asset-library`,
      library_id: "lib_demo",
      parsed_files: parsedFiles,
      modelClient
    });

    expect(result.status).toBe("partial");
    expect(result.data).toBeUndefined();
    expect(result.skipped_files).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          file_id: "file_cert_002",
          reason: "model_skipped_without_reason"
        })
      ])
    );
  });
});

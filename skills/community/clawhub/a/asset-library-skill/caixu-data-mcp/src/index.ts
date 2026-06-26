import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  agentDecisionAuditSchema,
  assetCardSchema,
  assetChangeEventSchema,
  assetStateSchema,
  checkLifecycleDataSchema,
  executionLogSchema,
  lifecycleRunDataSchema,
  libraryOverviewSchema,
  listLibrariesDataSchema,
  mergedAssetSchema,
  patchAssetCardDataSchema,
  packageRunDataSchema,
  packagePlanSchema,
  pipelineRunCountsSchema,
  pipelineRunDataSchema,
  pipelineStepSchema,
  parsedFileSchema,
  queryAssetsDataSchema,
  reindexLibrarySearchDataSchema,
  reviewQueueDataSchema,
  reviewStatusSchema,
  ruleProfileSchema,
  submissionProfileSchema,
  toolResultSchema
} from "@caixu/contracts";
import { createDataService } from "./service.js";

const server = new McpServer({
  name: "caixu-data-mcp",
  version: "0.1.0"
});

const service = createDataService();

server.registerTool(
  "create_or_load_library",
  {
    description: "Create or load a material asset library id in local SQLite storage.",
    inputSchema: {
      library_id: z.string().optional(),
      owner_hint: z.string().optional()
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1)
      })
    ).shape
  },
  async ({ library_id, owner_hint }) => {
    const result = service.createOrLoadLibrary({ library_id, owner_hint });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "list_libraries",
  {
    description: "List local libraries with maintenance-focused overview counts.",
    inputSchema: {},
    outputSchema: toolResultSchema(listLibrariesDataSchema).shape
  },
  async () => {
    const result = service.listLibraries();
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_library_overview",
  {
    description: "Load library-level overview counts, review queue size, and recent ingest/build times.",
    inputSchema: {
      library_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(libraryOverviewSchema).shape
  },
  async ({ library_id }) => {
    const result = service.getLibraryOverview({ library_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "create_pipeline_run",
  {
    description: "Create a persisted ingest or build_asset_library pipeline run.",
    inputSchema: {
      run_id: z.string().optional(),
      library_id: z.string().min(1),
      run_type: z.enum(["ingest", "build_asset_library"]),
      goal: z.string().optional(),
      input_root: z.string().optional(),
      latest_stage: z.string().optional()
    },
    outputSchema: toolResultSchema(pipelineRunDataSchema).shape
  },
  async ({ run_id, library_id, run_type, goal, input_root, latest_stage }) => {
    const result = service.createPipelineRun({
      run_id,
      library_id,
      run_type,
      goal,
      input_root,
      latest_stage
    });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "append_pipeline_step",
  {
    description: "Append a structured step record to a pipeline run.",
    inputSchema: {
      run_id: z.string().min(1),
      stage: z.string().min(1),
      status: pipelineStepSchema.shape.status,
      tool_name: z.string().optional(),
      message: z.string().min(1),
      payload_json: z.unknown().optional()
    },
    outputSchema: toolResultSchema(
      z.object({
        step: pipelineStepSchema
      })
    ).shape
  },
  async ({ run_id, stage, status, tool_name, message, payload_json }) => {
    const result = service.appendPipelineStep({
      run_id,
      stage,
      status,
      tool_name,
      message,
      payload_json
    });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_pipeline_run",
  {
    description: "Load a pipeline run and its recent steps.",
    inputSchema: {
      run_id: z.string().min(1),
      step_limit: z.number().int().positive().optional()
    },
    outputSchema: toolResultSchema(pipelineRunDataSchema).shape
  },
  async ({ run_id, step_limit }) => {
    const result = service.getPipelineRun({ run_id, step_limit });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "complete_pipeline_run",
  {
    description: "Mark a pipeline run as completed, partial, or failed and persist final counts.",
    inputSchema: {
      run_id: z.string().min(1),
      status: z.enum(["completed", "partial", "failed"]),
      latest_stage: z.string().min(1),
      counts: pipelineRunCountsSchema
    },
    outputSchema: toolResultSchema(pipelineRunDataSchema).shape
  },
  async ({ run_id, status, latest_stage, counts }) => {
    const result = service.completePipelineRun({
      run_id,
      status,
      latest_stage,
      counts
    });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "upsert_parsed_files",
  {
    description: "Persist parsed file records for a library.",
    inputSchema: {
      library_id: z.string().min(1),
      parsed_files: z.array(parsedFileSchema).min(1)
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1),
        file_ids: z.array(z.string().min(1)),
        parsed_files: z.array(parsedFileSchema)
      })
    ).shape
  },
  async ({ library_id, parsed_files }) => {
    const result = service.upsertParsedFiles({ library_id, parsed_files });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_parsed_files",
  {
    description: "Load parsed files from the library.",
    inputSchema: {
      library_id: z.string().min(1),
      file_ids: z.array(z.string().min(1)).optional()
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1),
        parsed_files: z.array(parsedFileSchema)
      })
    ).shape
  },
  async ({ library_id, file_ids }) => {
    const result = service.getParsedFiles({ library_id, file_ids });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "upsert_asset_cards",
  {
    description: "Persist asset cards in the library.",
    inputSchema: {
      library_id: z.string().min(1),
      asset_cards: z.array(assetCardSchema)
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1),
        asset_cards: z.array(assetCardSchema)
      })
    ).shape
  },
  async ({ library_id, asset_cards }) => {
    const result = service.upsertAssetCards({ library_id, asset_cards });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "query_assets",
  {
    description:
      "Query assets and merged assets from the library using structural filters, agent tags, and FTS. This is the default precise retrieval path.",
    inputSchema: {
      library_id: z.string().min(1),
      material_types: z.array(z.string().min(1)).optional(),
      keyword: z.string().optional(),
      reusable_scenario: z.string().optional(),
      semantic_query: z.string().optional(),
      tag_filters_any: z.array(z.string().min(1)).optional(),
      tag_filters_all: z.array(z.string().min(1)).optional(),
      validity_statuses: z.array(z.string().min(1)).optional(),
      asset_states: z.array(assetStateSchema).optional(),
      review_statuses: z.array(reviewStatusSchema).optional(),
      limit: z.number().int().positive().optional()
    },
    outputSchema: toolResultSchema(queryAssetsDataSchema).shape
  },
  async (input) => {
    const result = service.queryAssets(input);
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "query_assets_vector",
  {
    description:
      "Run optional semantic vector retrieval for similar or related assets. Use only when the user explicitly asks for semantic expansion, similar materials, or related materials.",
    inputSchema: {
      library_id: z.string().min(1),
      semantic_query: z.string().min(1),
      material_types: z.array(z.string().min(1)).optional(),
      reusable_scenario: z.string().optional(),
      tag_filters_any: z.array(z.string().min(1)).optional(),
      tag_filters_all: z.array(z.string().min(1)).optional(),
      validity_statuses: z.array(z.string().min(1)).optional(),
      asset_states: z.array(assetStateSchema).optional(),
      review_statuses: z.array(reviewStatusSchema).optional(),
      limit: z.number().int().positive().optional()
    },
    outputSchema: toolResultSchema(queryAssetsDataSchema).shape
  },
  async (input) => {
    const result = service.queryAssetsVector(input);
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "patch_asset_card",
  {
    description: "Patch a single asset card after manual review and persist a change event.",
    inputSchema: {
      library_id: z.string().min(1),
      asset_id: z.string().min(1),
      patch: z
        .object({
          title: z.string().min(1).optional(),
          holder_name: z.string().min(1).nullable().optional(),
          issuer_name: z.string().min(1).nullable().optional(),
          issue_date: z.string().nullable().optional(),
          expiry_date: z.string().nullable().optional(),
          validity_status: assetCardSchema.shape.validity_status.optional(),
          agent_tags: z.array(z.string().min(1)).optional(),
          reusable_scenarios: z.array(z.string().min(1)).optional(),
          sensitivity_level: assetCardSchema.shape.sensitivity_level.optional(),
          normalized_summary: z.string().min(1).optional(),
          review_status: reviewStatusSchema.optional(),
          last_verified_at: z.string().nullable().optional()
        })
        .refine((value) => Object.keys(value).length > 0, {
          message: "patch must contain at least one field"
        })
    },
    outputSchema: toolResultSchema(patchAssetCardDataSchema).shape
  },
  async ({ library_id, asset_id, patch }) => {
    const result = service.patchAssetCard({ library_id, asset_id, patch });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "archive_asset",
  {
    description: "Archive an asset so downstream query/lifecycle/package flows stop consuming it by default.",
    inputSchema: {
      library_id: z.string().min(1),
      asset_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(patchAssetCardDataSchema).shape
  },
  async ({ library_id, asset_id }) => {
    const result = service.archiveAsset({ library_id, asset_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "restore_asset",
  {
    description: "Restore an archived asset back to active state.",
    inputSchema: {
      library_id: z.string().min(1),
      asset_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(patchAssetCardDataSchema).shape
  },
  async ({ library_id, asset_id }) => {
    const result = service.restoreAsset({ library_id, asset_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "list_review_queue",
  {
    description: "List active assets that require manual review before being trusted as clean library records.",
    inputSchema: {
      library_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(reviewQueueDataSchema).shape
  },
  async ({ library_id }) => {
    const result = service.listReviewQueue({ library_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "reindex_library_search",
  {
    description: "Rebuild FTS, tag, and vector search indexes for a library.",
    inputSchema: {
      library_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(reindexLibrarySearchDataSchema).shape
  },
  async ({ library_id }) => {
    const result = service.reindexLibrarySearch({ library_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "upsert_merged_assets",
  {
    description: "Persist merged asset groups.",
    inputSchema: {
      library_id: z.string().min(1),
      merged_assets: z.array(mergedAssetSchema)
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1),
        merged_assets: z.array(mergedAssetSchema)
      })
    ).shape
  },
  async ({ library_id, merged_assets }) => {
    const result = service.upsertMergedAssets({ library_id, merged_assets });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "write_lifecycle_run",
  {
    description: "Persist a lifecycle evaluation run.",
    inputSchema: {
      run_id: z.string().min(1),
      goal: z.string().min(1),
      payload: checkLifecycleDataSchema,
      audit: agentDecisionAuditSchema.optional()
    },
    outputSchema: toolResultSchema(lifecycleRunDataSchema).shape
  },
  async ({ run_id, goal, payload, audit }) => {
    const result = service.writeLifecycleRun({ run_id, goal, payload, audit });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_latest_lifecycle_run",
  {
    description: "Load the latest lifecycle evaluation for a library and optional goal.",
    inputSchema: {
      library_id: z.string().min(1),
      goal: z.string().min(1).optional()
    },
    outputSchema: toolResultSchema(lifecycleRunDataSchema).shape
  },
  async ({ library_id, goal }) => {
    const result = service.getLatestLifecycleRun({ library_id, goal });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "write_package_run",
  {
    description: "Persist a package plan and its output directory.",
    inputSchema: {
      package_plan: packagePlanSchema,
      output_dir: z.string().optional(),
      audit: agentDecisionAuditSchema.optional()
    },
    outputSchema: toolResultSchema(packageRunDataSchema).shape
  },
  async ({ package_plan, output_dir, audit }) => {
    const result = service.writePackageRun({ package_plan, output_dir, audit });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_package_run",
  {
    description: "Load a package plan by package id.",
    inputSchema: {
      package_id: z.string().min(1).optional(),
      package_plan_id: z.string().min(1).optional()
    },
    outputSchema: toolResultSchema(packageRunDataSchema).shape
  },
  async ({ package_id, package_plan_id }) => {
    const result = service.getPackageRun({ package_id, package_plan_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "write_execution_log",
  {
    description: "Persist an execution log after submit-demo runs.",
    inputSchema: {
      library_id: z.string().min(1),
      execution_log: executionLogSchema
    },
    outputSchema: toolResultSchema(
      z.object({
        library_id: z.string().min(1),
        execution_log: executionLogSchema
      })
    ).shape
  },
  async ({ library_id, execution_log }) => {
    const result = service.writeExecutionLog({ library_id, execution_log });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_rule_profile",
  {
    description: "Load a rule profile by profile id.",
    inputSchema: {
      profile_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(
      z.object({
        profile: ruleProfileSchema
      })
    ).shape
  },
  async ({ profile_id }) => {
    const result = service.getRuleProfile({ profile_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "get_submission_profile",
  {
    description: "Load a submission profile by profile id.",
    inputSchema: {
      profile_id: z.string().min(1)
    },
    outputSchema: toolResultSchema(
      z.object({
        profile: submissionProfileSchema
      })
    ).shape
  },
  async ({ profile_id }) => {
    const result = service.getSubmissionProfile({ profile_id });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("caixu-data-mcp running on stdio");
}

main().catch((error) => {
  console.error("caixu-data-mcp failed:", error);
  process.exit(1);
});

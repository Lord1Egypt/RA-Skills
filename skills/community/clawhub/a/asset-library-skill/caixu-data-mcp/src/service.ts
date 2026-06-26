import { join } from "node:path";
import {
  buildAssetSearchText,
  type ExtractParserTextData,
  type ExtractVisualTextData,
  type ListLocalFilesData,
  type LocalFile,
  type AgentDecisionAudit,
  type AssetCard,
  type AssetState,
  type ExecutionLog,
  type LifecycleRunData,
  type ListLibrariesData,
  type LibraryOverview,
  type MergedAsset,
  type PackageRunData,
  type PatchAssetCardData,
  type PipelineRunData,
  type PipelineStep,
  type ParsedFile,
  type QueryAssetsData,
  type ReadLocalTextFileData,
  type ReindexLibrarySearchData,
  type RenderPdfPagesData,
  type ReviewQueueData,
  type ReviewStatus,
  deriveReusableScenariosFromAgentTags,
  sanitizeAgentTags,
  makeToolResult
} from "@caixu/contracts";
import { getSubmissionProfile } from "@caixu/executor-profiles";
import { getRuleProfileBundle } from "@caixu/rules";
import { openCaixuStorage } from "@caixu/storage";
import {
  createLocalSearchEmbedder,
  type SearchEmbedder
} from "./search-embedder.js";

export function defaultDbPath(): string {
  return process.env.CAIXU_SQLITE_PATH ?? join(process.cwd(), "data", "caixu.sqlite");
}

type CreateDataServiceOptions = {
  searchEmbedder?: SearchEmbedder;
  embeddingModelId?: string;
};

type RankedHit = {
  asset_id: string;
  score: number;
};

const defaultRrfK = 60;

function unique<T>(values: T[]): T[] {
  return [...new Set(values)];
}

function rrfMergeRankedIds(lists: string[][], limit: number): string[] {
  const scores = new Map<string, number>();
  for (const ids of lists) {
    ids.forEach((assetId, index) => {
      scores.set(assetId, (scores.get(assetId) ?? 0) + 1 / (defaultRrfK + index + 1));
    });
  }

  return [...scores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([assetId]) => assetId);
}

function filterMergedAssets(libraryId: string, assets: AssetCard[], mergedAssets: MergedAsset[]) {
  const matchedIds = new Set(assets.map((asset) => asset.asset_id));
  return mergedAssets.filter((merged) => {
    if (matchedIds.has(merged.selected_asset_id) || matchedIds.has(merged.canonical_asset_id)) {
      return true;
    }
    return merged.superseded_asset_ids.some((assetId) => matchedIds.has(assetId));
  });
}

export function createDataService(
  dbPath = defaultDbPath(),
  options: CreateDataServiceOptions = {}
) {
  const storage = openCaixuStorage(dbPath);
  const searchEmbedder =
    options.searchEmbedder ??
    createLocalSearchEmbedder({
      modelId: options.embeddingModelId
    });
  const embeddingModelId = options.embeddingModelId ?? searchEmbedder.modelId;

  function syncSearchIndexForAssets(
    libraryId: string,
    assets: AssetCard[]
  ): { data: ReindexLibrarySearchData; warnings: string[] } {
    const warnings: string[] = [];
    const activeAssets = assets.filter((asset) => asset.asset_state === "active");
    const archivedIds = assets
      .filter((asset) => asset.asset_state === "archived")
      .map((asset) => asset.asset_id);

    if (archivedIds.length) {
      storage.removeAssetSearchIndex(archivedIds);
    }

    const searchableAssets = activeAssets
      .map((asset) => {
        const normalized = {
          ...asset,
          agent_tags: sanitizeAgentTags(asset),
          reusable_scenarios: deriveReusableScenariosFromAgentTags(
            sanitizeAgentTags(asset)
          )
        } satisfies AssetCard;
        const searchText = buildAssetSearchText(normalized);
        return { asset: normalized, searchText };
      })
      .filter((item) => item.searchText.trim().length > 0);

    const skippedAssets = archivedIds.length + (activeAssets.length - searchableAssets.length);
    let embeddings: Array<number[] | null> = searchableAssets.map(() => null);

    if (searchableAssets.length > 0) {
      try {
        const vectors = searchEmbedder.embedTexts(
          searchableAssets.map((item) => item.searchText)
        );
        embeddings = searchableAssets.map((_, index) => vectors[index] ?? null);
      } catch (error) {
        warnings.push(
          `Embedding generation failed; falling back to FTS/tag search only: ${
            error instanceof Error ? error.message : "unknown embedding error"
          }`
        );
      }
    }

    const indexed = storage.upsertAssetSearchIndex({
      library_id: libraryId,
      assets: searchableAssets.map((item, index) => ({
        asset_id: item.asset.asset_id,
        title: item.asset.title,
        normalized_summary: item.asset.normalized_summary,
        agent_tags: item.asset.agent_tags,
        search_text: item.searchText,
        embedding: embeddings[index] ?? null,
        model: embeddingModelId
      }))
    });

    return {
      data: {
        ...indexed,
        skipped_assets: indexed.skipped_assets + skippedAssets
      },
      warnings
    };
  }

  return {
    close: () => storage.close(),
    writeAgentDecisionAudit(input: {
      audit: AgentDecisionAudit;
      run_ref_type: "asset_library_build" | "lifecycle_run" | "package_run";
      run_ref_id: string;
    }) {
      const audit = storage.writeAgentDecisionAudit(input.audit, {
        type: input.run_ref_type,
        id: input.run_ref_id
      });
      return makeToolResult("success", { audit });
    },
    createOrLoadLibrary(input: { library_id?: string; owner_hint?: string }) {
      const library = storage.createOrLoadLibrary(input.library_id, input.owner_hint);
      return makeToolResult("success", { library_id: library.library_id });
    },
    listLibraries() {
      return makeToolResult<ListLibrariesData>("success", storage.listLibraries());
    },
    getLibraryOverview(input: { library_id: string }) {
      const overview = storage.getLibraryOverview(input.library_id);
      return makeToolResult<LibraryOverview | undefined>(
        overview ? "success" : "failed",
        overview ?? undefined
      );
    },
    createPipelineRun(input: {
      run_id?: string;
      library_id: string;
      run_type: "ingest" | "build_asset_library";
      goal?: string;
      input_root?: string;
      latest_stage?: string;
    }) {
      const pipelineRun = storage.createPipelineRun({
        runId: input.run_id,
        libraryId: input.library_id,
        runType: input.run_type,
        goal: input.goal,
        inputRoot: input.input_root,
        latestStage: input.latest_stage
      });
      return makeToolResult("success", {
        pipeline_run: pipelineRun,
        steps: []
      } satisfies PipelineRunData);
    },
    appendPipelineStep(input: {
      run_id: string;
      stage: string;
      status: PipelineStep["status"];
      tool_name?: string;
      message: string;
      payload_json?: unknown;
    }) {
      const step = storage.appendPipelineStep({
        runId: input.run_id,
        stage: input.stage,
        status: input.status,
        toolName: input.tool_name,
        message: input.message,
        payload: input.payload_json ?? null
      });
      return makeToolResult("success", { step });
    },
    getPipelineRun(input: { run_id: string; step_limit?: number }) {
      const run = storage.getPipelineRun(input.run_id, input.step_limit ?? 50);
      return makeToolResult(run?.pipeline_run ? "success" : "failed", run ?? undefined);
    },
    completePipelineRun(input: {
      run_id: string;
      status: "completed" | "partial" | "failed";
      latest_stage: string;
      counts: {
        parsed: number;
        failed: number;
        warnings: number;
        skipped: number;
        assets: number;
        merged: number;
      };
    }) {
      const run = storage.completePipelineRun({
        runId: input.run_id,
        status: input.status,
        latestStage: input.latest_stage,
        counts: input.counts
      });
      return makeToolResult(run?.pipeline_run ? "success" : "failed", run ?? undefined);
    },
    upsertParsedFiles(input: { library_id: string; parsed_files: ParsedFile[] }) {
      const files = storage.upsertParsedFiles(input.library_id, input.parsed_files);
      return makeToolResult("success", {
        library_id: input.library_id,
        file_ids: files.map((file) => file.file_id),
        parsed_files: files
      });
    },
    getParsedFiles(input: { library_id: string; file_ids?: string[] }) {
      const parsedFiles = storage.listParsedFiles(input.library_id, input.file_ids);
      return makeToolResult("success", {
        library_id: input.library_id,
        parsed_files: parsedFiles
      });
    },
    upsertAssetCards(input: { library_id: string; asset_cards: AssetCard[] }) {
      const assetCards = storage.upsertAssetCards(input.library_id, input.asset_cards);
      const indexed = syncSearchIndexForAssets(input.library_id, assetCards);
      return makeToolResult(
        indexed.warnings.length > 0 ? "partial" : "success",
        {
          library_id: input.library_id,
          asset_cards: assetCards
        },
        { warnings: indexed.warnings }
      );
    },
    queryAssets(input: {
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
    }) {
      try {
        const compatibilityTags = input.reusable_scenario
          ? [`use:${input.reusable_scenario}`]
          : [];
        const tagFiltersAny = unique([
          ...(input.tag_filters_any ?? []),
          ...compatibilityTags
        ]);
        const usesEnhancedQuery =
          Boolean(input.semantic_query?.trim()) ||
          tagFiltersAny.length > 0 ||
          Boolean(input.tag_filters_all?.length);

        if (!usesEnhancedQuery) {
          return makeToolResult("success", storage.queryAssets(input));
        }

        const base = storage.queryAssets({
          library_id: input.library_id,
          material_types: input.material_types,
          validity_statuses: input.validity_statuses,
          asset_states: input.asset_states,
          review_statuses: input.review_statuses
        });

        const allowedIds = base.asset_cards.map((asset) => asset.asset_id);
        if (allowedIds.length === 0) {
          return makeToolResult("success", {
            library_id: input.library_id,
            asset_cards: [],
            merged_assets: []
          } satisfies QueryAssetsData);
        }
        const limit = input.limit && input.limit > 0 ? input.limit : 20;
        const rankedLists: string[][] = [];
        const warnings: string[] = [];

        const lexicalQuery = input.semantic_query?.trim() || input.keyword?.trim() || "";
        if (lexicalQuery) {
          rankedLists.push(
            storage.searchAssetIdsByFts({
              library_id: input.library_id,
              query: lexicalQuery,
              limit,
              allowed_asset_ids: allowedIds
            })
          );
        }

        if (tagFiltersAny.length > 0 || (input.tag_filters_all?.length ?? 0) > 0) {
          rankedLists.push(
            storage.searchAssetIdsByTags({
              library_id: input.library_id,
              tag_filters_any: tagFiltersAny,
              tag_filters_all: input.tag_filters_all,
              limit,
              allowed_asset_ids: allowedIds
            })
          );
        }

        const primaryIds = rrfMergeRankedIds(
          rankedLists.filter((ids) => ids.length > 0),
          limit
        );

        const matchedAssets =
          primaryIds.length > 0
            ? storage.getAssetCardsByIds(input.library_id, primaryIds)
            : [];

        const mergedAssets = filterMergedAssets(
          input.library_id,
          matchedAssets,
          storage.getMergedAssets(input.library_id)
        );

        return makeToolResult<QueryAssetsData>(
          warnings.length > 0 ? "partial" : "success",
          {
            library_id: input.library_id,
            asset_cards: matchedAssets,
            merged_assets: mergedAssets
          },
          { warnings }
        );
      } catch (error) {
        return makeToolResult("failed", undefined, {
          errors: [
            {
              code: "QUERY_ASSETS_FAILED",
              message: error instanceof Error ? error.message : "Unknown query failure",
              retryable: false
            }
          ]
        });
      }
    },
    upsertMergedAssets(input: { library_id: string; merged_assets: MergedAsset[] }) {
      const mergedAssets = storage.upsertMergedAssets(
        input.library_id,
        input.merged_assets
      );
      return makeToolResult("success", {
        library_id: input.library_id,
        merged_assets: mergedAssets
      });
    },
    patchAssetCard(input: {
      library_id: string;
      asset_id: string;
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
      >;
    }) {
      const result = storage.patchAssetCard(input.library_id, input.asset_id, input.patch);
      const warnings =
        result?.asset_card != null
          ? syncSearchIndexForAssets(input.library_id, [result.asset_card]).warnings
          : [];
      return makeToolResult<PatchAssetCardData | undefined>(
        result ? (warnings.length > 0 ? "partial" : "success") : "failed",
        result
          ? {
              library_id: input.library_id,
              asset_card: result.asset_card,
              change_event: result.change_event
            }
          : undefined,
        { warnings }
      );
    },
    archiveAsset(input: { library_id: string; asset_id: string }) {
      const result = storage.setAssetState(input.library_id, input.asset_id, "archived");
      const warnings =
        result?.asset_card != null
          ? syncSearchIndexForAssets(input.library_id, [result.asset_card]).warnings
          : [];
      return makeToolResult<PatchAssetCardData | undefined>(
        result ? (warnings.length > 0 ? "partial" : "success") : "failed",
        result
          ? {
              library_id: input.library_id,
              asset_card: result.asset_card,
              change_event: result.change_event
            }
          : undefined,
        { warnings }
      );
    },
    restoreAsset(input: { library_id: string; asset_id: string }) {
      const result = storage.setAssetState(input.library_id, input.asset_id, "active");
      const warnings =
        result?.asset_card != null
          ? syncSearchIndexForAssets(input.library_id, [result.asset_card]).warnings
          : [];
      return makeToolResult<PatchAssetCardData | undefined>(
        result ? (warnings.length > 0 ? "partial" : "success") : "failed",
        result
          ? {
              library_id: input.library_id,
              asset_card: result.asset_card,
              change_event: result.change_event
            }
          : undefined,
        { warnings }
      );
    },
    listReviewQueue(input: { library_id: string }) {
      return makeToolResult<ReviewQueueData>("success", storage.listReviewQueue(input.library_id));
    },
    reindexLibrarySearch(input: { library_id: string }) {
      const assetCards = storage.listAssetCards(input.library_id);
      const indexed = syncSearchIndexForAssets(input.library_id, assetCards);
      return makeToolResult<ReindexLibrarySearchData>(
        indexed.warnings.length > 0 ? "partial" : "success",
        indexed.data,
        { warnings: indexed.warnings }
      );
    },
    writeLifecycleRun(input: {
      run_id: string;
      goal: string;
      payload: LifecycleRunData["lifecycle_run"];
      audit?: AgentDecisionAudit;
    }) {
      const runData = storage.writeLifecycleRun(
        input.run_id,
        input.payload!,
        input.goal,
        input.audit
      );
      return makeToolResult("success", runData);
    },
    getLatestLifecycleRun(input: { library_id: string; goal?: string }) {
      const lifecycleRun = storage.getLatestLifecycleRun(input.library_id, input.goal);
      return makeToolResult(lifecycleRun ? "success" : "failed", lifecycleRun ?? undefined);
    },
    writePackageRun(input: {
      package_plan: PackageRunData["package_plan"];
      output_dir?: string;
      audit?: AgentDecisionAudit;
    }) {
      const packageRun = storage.writePackageRun(
        input.package_plan!,
        input.output_dir,
        input.audit
      );
      return makeToolResult("success", {
        package_plan: packageRun.package_plan,
        output_dir: packageRun.output_dir,
        audit: packageRun.audit
      });
    },
    getPackageRun(input: { package_id?: string; package_plan_id?: string }) {
      const effectivePackageId = input.package_id ?? input.package_plan_id;
      const packageRun = effectivePackageId
        ? storage.getPackageRun(effectivePackageId)
        : null;
      return makeToolResult(packageRun?.package_plan ? "success" : "failed", packageRun ?? undefined);
    },
    writeExecutionLog(input: { library_id: string; execution_log: ExecutionLog }) {
      const executionLog = storage.writeExecutionLog(input.execution_log);
      return makeToolResult("success", {
        library_id: input.library_id,
        execution_log: executionLog
      });
    },
    getRuleProfile(input: { profile_id: string }) {
      try {
        return makeToolResult("success", {
          profile: getRuleProfileBundle(input.profile_id)
        });
      } catch (error) {
        return makeToolResult("failed", undefined, {
          errors: [
            {
              code: "RULE_PROFILE_NOT_SUPPORTED",
              message: error instanceof Error ? error.message : "Unknown rule profile error",
              retryable: false
            }
          ]
        });
      }
    },
    queryAssetsVector(input: {
      library_id: string;
      semantic_query: string;
      material_types?: string[];
      reusable_scenario?: string;
      tag_filters_any?: string[];
      tag_filters_all?: string[];
      validity_statuses?: string[];
      asset_states?: AssetState[];
      review_statuses?: ReviewStatus[];
      limit?: number;
    }) {
      const semanticQuery = input.semantic_query.trim();
      if (!semanticQuery) {
        return makeToolResult("failed", undefined, {
          errors: [
            {
              code: "QUERY_ASSETS_VECTOR_MISSING_QUERY",
              message:
                "query_assets_vector requires a non-empty semantic_query.",
              retryable: false
            }
          ]
        });
      }

      try {
        const compatibilityTags = input.reusable_scenario
          ? [`use:${input.reusable_scenario}`]
          : [];
        const tagFiltersAny = unique([
          ...(input.tag_filters_any ?? []),
          ...compatibilityTags
        ]);
        const limit = input.limit && input.limit > 0 ? input.limit : 20;

        const base = storage.queryAssets({
          library_id: input.library_id,
          material_types: input.material_types,
          validity_statuses: input.validity_statuses,
          asset_states: input.asset_states,
          review_statuses: input.review_statuses
        });

        let candidates = base.asset_cards;
        if (tagFiltersAny.length > 0 || (input.tag_filters_all?.length ?? 0) > 0) {
          const hasAnyTags =
            tagFiltersAny.length === 0 ||
            candidates.some((asset) =>
              tagFiltersAny.some((tag) => asset.agent_tags.includes(tag))
            );
          if (hasAnyTags) {
            candidates = candidates.filter((asset) => {
              const matchesAny =
                tagFiltersAny.length === 0 ||
                tagFiltersAny.some((tag) => asset.agent_tags.includes(tag));
              const matchesAll =
                (input.tag_filters_all?.length ?? 0) === 0 ||
                (input.tag_filters_all ?? []).every((tag) =>
                  asset.agent_tags.includes(tag)
                );
              return matchesAny && matchesAll;
            });
          }
        }

        const allowedIds = candidates.map((asset) => asset.asset_id);
        if (allowedIds.length === 0) {
          return makeToolResult<QueryAssetsData>("success", {
            library_id: input.library_id,
            asset_cards: [],
            merged_assets: []
          });
        }

        const [queryEmbedding] = searchEmbedder.embedTexts([semanticQuery]);
        const vectorIds = storage.searchAssetIdsByVector({
          library_id: input.library_id,
          query_embedding: queryEmbedding ?? [],
          limit,
          allowed_asset_ids: allowedIds
        });

        const matchedAssets =
          vectorIds.length > 0
            ? storage.getAssetCardsByIds(input.library_id, vectorIds)
            : [];

        const mergedAssets = filterMergedAssets(
          input.library_id,
          matchedAssets,
          storage.getMergedAssets(input.library_id)
        );

        return makeToolResult<QueryAssetsData>("success", {
          library_id: input.library_id,
          asset_cards: matchedAssets,
          merged_assets: mergedAssets
        });
      } catch (error) {
        return makeToolResult("failed", undefined, {
          errors: [
            {
              code: "QUERY_ASSETS_VECTOR_FAILED",
              message:
                error instanceof Error
                  ? error.message
                  : "Unknown vector query failure",
              retryable: false
            }
          ]
        });
      }
    },
    getSubmissionProfile(input: { profile_id: string }) {
      try {
        return makeToolResult("success", {
          profile: getSubmissionProfile(input.profile_id)
        });
      } catch (error) {
        return makeToolResult("failed", undefined, {
          errors: [
            {
              code: "SUBMISSION_PROFILE_NOT_SUPPORTED",
              message:
                error instanceof Error
                  ? error.message
                  : "Unknown submission profile error",
              retryable: false
            }
          ]
        });
      }
    }
  };
}

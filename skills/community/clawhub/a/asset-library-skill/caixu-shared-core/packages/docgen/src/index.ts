import { createWriteStream } from "node:fs";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { basename, join } from "node:path";
import archiver from "archiver";
import ExcelJS from "exceljs";
import type {
  AssetCard,
  BuildPackageData,
  CheckLifecycleData,
  ExportLedgersData,
  GeneratedFile,
  PackagePlan,
  ParsedFile,
  Readiness
} from "@caixu/contracts";

export type ExportLedgerArgs = {
  library_id: string;
  output_dir: string;
  assets: AssetCard[];
  lifecycle: CheckLifecycleData;
  as_of_date: string;
  window_days: number;
};

export type BuildPackageArgs = {
  library_id: string;
  goal: string;
  output_dir: string;
  assets: AssetCard[];
  parsed_files?: ParsedFile[];
  package_id?: string;
  package_name?: string;
  selected_asset_ids?: string[];
  selected_exports?: string[];
  generated_files?: GeneratedFile[];
  readiness: Readiness;
  missing_items_ref: string;
  submission_profile: string;
  operator_notes?: string;
  allow_truthful_package_when_blocked?: boolean;
};

const assetLedgerName = "personal-material-assets.xlsx";

function checklistName(windowDays: number): string {
  return `renewal-checklist-${windowDays}d.xlsx`;
}

function packageName(goal: string): string {
  return goal.replaceAll("_", "-");
}

async function writeAssetLedger(filePath: string, assets: AssetCard[]): Promise<void> {
  const workbook = new ExcelJS.Workbook();
  const sheet = workbook.addWorksheet("assets");
  sheet.columns = [
    { header: "asset_id", key: "asset_id", width: 28 },
    { header: "material_type", key: "material_type", width: 18 },
    { header: "title", key: "title", width: 32 },
    { header: "holder_name", key: "holder_name", width: 20 },
    { header: "issuer_name", key: "issuer_name", width: 28 },
    { header: "issue_date", key: "issue_date", width: 16 },
    { header: "expiry_date", key: "expiry_date", width: 16 },
    { header: "validity_status", key: "validity_status", width: 18 },
    { header: "reusable_scenarios", key: "reusable_scenarios", width: 32 }
  ];

  for (const asset of assets) {
    sheet.addRow({
      ...asset,
      reusable_scenarios: asset.reusable_scenarios.join(", ")
    });
  }

  await workbook.xlsx.writeFile(filePath);
}

async function writeRenewalChecklist(
  filePath: string,
  lifecycle: CheckLifecycleData
): Promise<void> {
  const workbook = new ExcelJS.Workbook();
  const eventSheet = workbook.addWorksheet("lifecycle_events");
  eventSheet.columns = [
    { header: "event_id", key: "event_id", width: 28 },
    { header: "asset_id", key: "asset_id", width: 24 },
    { header: "trigger_type", key: "trigger_type", width: 24 },
    { header: "severity", key: "severity", width: 16 },
    { header: "recommended_action", key: "recommended_action", width: 52 }
  ];

  for (const event of lifecycle.lifecycle_events) {
    eventSheet.addRow(event);
  }

  const missingSheet = workbook.addWorksheet("missing_items");
  missingSheet.columns = [
    { header: "code", key: "code", width: 28 },
    { header: "severity", key: "severity", width: 16 },
    { header: "asset_type", key: "asset_type", width: 28 },
    { header: "suggested_action", key: "suggested_action", width: 48 }
  ];

  for (const item of lifecycle.missing_items.items) {
    missingSheet.addRow(item);
  }

  await workbook.xlsx.writeFile(filePath);
}

async function zipFiles(zipPath: string, files: Array<{ path: string; name?: string }>): Promise<void> {
  await mkdir(join(zipPath, ".."), { recursive: true }).catch(() => undefined);
  await new Promise<void>((resolve, reject) => {
    const output = createWriteStream(zipPath);
    const archive = archiver("zip", { zlib: { level: 9 } });

    output.on("close", () => resolve());
    archive.on("error", (error: Error) => reject(error));
    archive.pipe(output);

    for (const file of files) {
      archive.file(file.path, { name: file.name ?? basename(file.path) });
    }

    archive.finalize().catch(reject);
  });
}

export async function exportLedgers(
  args: ExportLedgerArgs
): Promise<ExportLedgersData> {
  await mkdir(args.output_dir, { recursive: true });
  const assetLedgerPath = join(args.output_dir, assetLedgerName);
  const renewalChecklistPath = join(
    args.output_dir,
    checklistName(args.window_days)
  );

  await writeAssetLedger(assetLedgerPath, args.assets);
  await writeRenewalChecklist(renewalChecklistPath, args.lifecycle);

  return {
    library_id: args.library_id,
    exported_files: [assetLedgerPath, renewalChecklistPath]
  };
}

function generatedFiles(goal: string, windowDays: number): GeneratedFile[] {
  return [
    {
      file_name: assetLedgerName,
      file_type: "xlsx",
      purpose: "Asset ledger export"
    },
    {
      file_name: checklistName(windowDays),
      file_type: "xlsx",
      purpose: `${windowDays}-day renewal checklist`
    },
    {
      file_name: `${packageName(goal)}-package.zip`,
      file_type: "zip",
      purpose: "Submission package bundle"
    }
  ];
}

export async function buildPackage(args: BuildPackageArgs): Promise<BuildPackageData> {
  await mkdir(args.output_dir, { recursive: true });
  if (!args.readiness.ready_for_submission && args.allow_truthful_package_when_blocked === false) {
    throw new Error(
      "Truthful package generation was disabled while readiness is blocked."
    );
  }

  const selectedAssetIdsInput = new Set(args.selected_asset_ids ?? []);
  const selectedAssets =
    selectedAssetIdsInput.size > 0
      ? args.assets.filter((asset) => selectedAssetIdsInput.has(asset.asset_id))
      : args.assets;
  const missingSelectedAssetIds =
    selectedAssetIdsInput.size > 0
      ? [...selectedAssetIdsInput].filter(
          (assetId) => !selectedAssets.some((asset) => asset.asset_id === assetId)
        )
      : [];

  if (missingSelectedAssetIds.length > 0) {
    throw new Error(
      `Unknown selected asset ids: ${missingSelectedAssetIds.join(", ")}`
    );
  }

  const packageId =
    args.package_id ??
    `pkg_${args.goal}_${new Date().toISOString().slice(0, 10).replaceAll("-", "")}`;
  const packageBaseName = args.package_name ?? `${packageName(args.goal)}-package`;
  const zipPath = join(args.output_dir, `${packageBaseName}.zip`);
  const manifestPath = join(args.output_dir, `${packageBaseName}.manifest.json`);

  const generatedFilesList = args.generated_files ?? generatedFiles(args.goal, 60);
  const selectedExports =
    args.selected_exports ?? generatedFilesList.map((file) => file.file_name);

  const manifest = {
    library_id: args.library_id,
    goal: args.goal,
    selected_asset_ids: selectedAssets.map((asset) => asset.asset_id),
    submission_profile: args.submission_profile,
    readiness: args.readiness
  };

  await writeFile(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

  const filesToZip: Array<{ path: string; name?: string }> = [{ path: manifestPath }];
  const parsedFilePathById = new Map(
    (args.parsed_files ?? []).map((file) => [file.file_id, file.file_path])
  );

  for (const asset of selectedAssets) {
    for (const sourceFile of asset.source_files) {
      try {
        const absolutePath =
          sourceFile.file_path ??
          parsedFilePathById.get(sourceFile.file_id) ??
          (sourceFile.file_id.startsWith("/") ? sourceFile.file_id : null);
        if (!absolutePath) {
          continue;
        }
        await stat(absolutePath);
        filesToZip.push({
          path: absolutePath,
          name: `materials/${basename(absolutePath)}`
        });
      } catch {
        continue;
      }
    }
  }

  await zipFiles(zipPath, filesToZip);

  const packagePlan: PackagePlan = {
    schema_version: "1.0",
    library_id: args.library_id,
    package_id: packageId,
    target_goal: args.goal,
    package_name: packageBaseName,
    selected_asset_ids: selectedAssets.map((asset) => asset.asset_id),
    selected_exports: selectedExports,
    missing_items_ref: args.missing_items_ref,
    generated_files: generatedFilesList,
    submission_profile: args.submission_profile,
    readiness: args.readiness,
    operator_notes:
      args.operator_notes ??
      (args.readiness.ready_for_submission
        ? "可以继续提交。"
        : "当前存在阻塞项，除非明确允许风险提交，否则不应直接提交。")
  };

  return {
    library_id: args.library_id,
    package_plan: packagePlan,
    exported_files: [zipPath]
  };
}

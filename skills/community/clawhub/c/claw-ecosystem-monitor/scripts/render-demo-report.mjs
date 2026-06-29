import { mkdir, readFile, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillDir = join(__dirname, "..");
const today = new Date().toISOString().slice(0, 10);
const inputPath = join(skillDir, "data", today, "openclaw-ecosystem-snapshot.json");
const outputPath = join(skillDir, "reports", `${today}-openclaw-ecosystem-report.md`);

function table(rows) {
  if (rows.length === 0) return "- none";
  const headers = Object.keys(rows[0]);
  const header = `| ${headers.join(" | ")} |`;
  const sep = `| ${headers.map(() => "---").join(" | ")} |`;
  const body = rows.map((row) => `| ${headers.map((headerName) => String(row[headerName] ?? "").replace(/\|/g, "\\|")).join(" | ")} |`);
  return [header, sep, ...body].join("\n");
}

function compactNumber(value) {
  if (typeof value !== "number") return "";
  return new Intl.NumberFormat("en-US").format(value);
}

async function main() {
  if (!existsSync(inputPath)) {
    throw new Error(`Snapshot missing: ${inputPath}. Run collect-openclaw-ecosystem.mjs first.`);
  }

  const snapshot = JSON.parse(await readFile(inputPath, "utf8"));
  const repo = snapshot.records.github_repo_openclaw;
  const docIssues = snapshot.records.github_issues_openclaw_documentation_query ?? [];
  const npmPackages = snapshot.records.npm_search_openclaw ?? [];
  const statuses = snapshot.request_status ?? [];
  const warnings = snapshot.warnings ?? [];
  const hardWarnings = snapshot.hard_warnings ?? [];

  const report = `# OpenClaw Ecosystem Monitor Demo Report

Date: ${today}  
Mode: local prototype  
Source discipline: metadata + short summary + canonical source link only

## Source Health

${table(statuses.map((status) => ({
  source: status.name,
  status: status.status,
  ok: status.ok,
  remaining: status.rate_limit_remaining ?? "",
})))}

Warnings: ${warnings.length === 0 ? "none" : warnings.join("; ")}

Hard pause triggers: ${hardWarnings.length === 0 ? "none" : hardWarnings.join("; ")}

## Repository Signal

Source: ${repo.html_url}

${table([
  {
    stars: compactNumber(repo.stars),
    forks: compactNumber(repo.forks),
    open_issues: compactNumber(repo.open_issues),
    default_branch: repo.default_branch,
    license: repo.license,
    updated_at: repo.updated_at,
  },
])}

## E1 Candidate Issues

${table(docIssues.slice(0, 7).map((issue) => ({
  title: issue.title,
  labels: issue.labels.length > 0 ? issue.labels.join(", ") : "-",
  comments: issue.comments,
  source: issue.html_url,
})))}

Active first P1 candidate: [PR #77710](https://github.com/openclaw/openclaw/pull/77710), waiting for maintainer review.

## npm Freshness Signal

${table(npmPackages.slice(0, 8).map((pkg) => ({
  package: pkg.name,
  version: pkg.version,
  weekly_downloads: compactNumber(pkg.downloads_weekly),
  monthly_downloads: compactNumber(pkg.downloads_monthly),
  updated: pkg.date,
  source: pkg.links?.npm ?? pkg.links?.repository ?? "",
})))}

## Interpretation

- OpenClaw has enough public repository and package activity to justify a daily ecosystem monitor.
- The first reputation action is active; do not open a second PR until #77710 gets maintainer signal or a clearly non-overlapping small docs fix appears.
- The public product should publish source-linked summaries, not mirrored source content.
- No payment, hosted API, or public mutation is performed by this report.

## Next Local Step

Keep the report running, monitor PR #77710, and triage candidate issues offline before any public action.
`;

  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, report, "utf8");
  console.log(outputPath);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : String(error));
  process.exitCode = 1;
});

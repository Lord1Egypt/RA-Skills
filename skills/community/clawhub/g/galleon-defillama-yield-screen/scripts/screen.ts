import { readFile, stat } from "node:fs/promises";

const finite = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);
export function screen(snapshot: unknown, chain: string, token: string, minimumTvl: number, basis: "base" | "total", project?: string) {
  if (!chain || !/^0x[0-9a-fA-F]{40}$/.test(token) || !finite(minimumTvl) || minimumTvl < 0 || !["base", "total"].includes(basis) || (project !== undefined && !/^[a-z0-9-]{1,80}$/.test(project))) throw new Error("invalid_filter");
  const envelope = snapshot as { status?: unknown; data?: unknown } | null;
  if (!envelope || envelope.status !== "success" || !Array.isArray(envelope.data) || envelope.data.length > 100000) throw new Error("invalid_snapshot");
  const excluded: Record<string, number> = {};
  const rows: { pool: string; project: string; chain: string; underlyingTokens: string[]; tvlUsd: number; apyBase: number | null; apyReward: number | null; apy: number | null; rankValue: number }[] = [];
  const seen = new Set<string>();
  const reject = (reason: string) => { excluded[reason] = (excluded[reason] ?? 0) + 1; };
  for (const value of envelope.data) {
    if (!value || typeof value !== "object") { reject("malformed_row"); continue; }
    const p = value as Record<string, unknown>;
    if (typeof p.pool !== "string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(p.pool) || typeof p.project !== "string" || typeof p.chain !== "string") { reject("malformed_row"); continue; }
    if (project !== undefined && p.project !== project) { reject("project"); continue; }
    if (p.chain.toLowerCase() !== chain.toLowerCase()) { reject("chain"); continue; }
    if (!Array.isArray(p.underlyingTokens) || p.underlyingTokens.length !== 1 || typeof p.underlyingTokens[0] !== "string" || p.underlyingTokens[0].toLowerCase() !== token.toLowerCase()) { reject("asset_exposure"); continue; }
    if (!finite(p.tvlUsd) || p.tvlUsd < minimumTvl) { reject("tvl"); continue; }
    const rankValue = basis === "base" ? p.apyBase : p.apy;
    if (!finite(rankValue)) { reject("missing_rank_metric"); continue; }
    if (seen.has(p.pool)) throw new Error("duplicate_pool");
    seen.add(p.pool);
    rows.push({ pool: p.pool, project: p.project, chain: p.chain, underlyingTokens: [p.underlyingTokens[0]], tvlUsd: p.tvlUsd, apyBase: finite(p.apyBase) ? p.apyBase : null, apyReward: finite(p.apyReward) ? p.apyReward : null, apy: finite(p.apy) ? p.apy : null, rankValue });
  }
  rows.sort((a, b) => b.rankValue - a.rankValue || a.pool.localeCompare(b.pool));
  return { basis, project: project ?? null, inputRows: envelope.data.length, matchedRows: rows.length, excluded, rows: rows.slice(0, 5), providerObservationTime: null };
}

if (import.meta.main) {
  try {
    const [file, chain, token, minimum, basis, project] = process.argv.slice(2);
    if (!file || !chain || !token || minimum === undefined || !basis || !["base", "total"].includes(basis) || ![7, 8].includes(process.argv.length)) throw new Error("invalid_arguments");
    if ((await stat(file)).size > 25_000_000) throw new Error("input_too_large");
    console.log(JSON.stringify(screen(JSON.parse(await readFile(file, "utf8")), chain, token, Number(minimum), basis as "base" | "total", project), null, 2));
  } catch (error) {
    const code = error instanceof Error && ["invalid_filter", "invalid_snapshot", "duplicate_pool", "invalid_arguments", "input_too_large"].includes(error.message) ? error.message : "invalid_input";
    console.log(JSON.stringify({ ok: false, error: code })); process.exitCode = 1;
  }
}

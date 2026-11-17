#!/usr/bin/env node
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

const DEFAULT_SOURCE = "https://raw.githubusercontent.com/ivershuo/apporbit/data/v1/";
const WEBSITE = "https://apporbit.ooxxz.com/";
const execFileAsync = promisify(execFile);
const usage = `Usage: node query.mjs <command> [options]

Commands:
  coverage                         Published target coverage and latest outcomes
  rankings --store S --market M --scope S --chart C [--category C] [--date YYYY-MM-DD] [--allow-partial] [--limit N]
  movers   --store S --market M --scope S --chart C [--category C] [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--limit N]
  app      --store S --market M --app-id ID [--scope S --chart C]
  search   --store S --market M --query TEXT [--limit N]

Options: --source URL_OR_DIRECTORY overrides APPORBIT_SOURCE and the public GitHub data branch. All output is JSON.`;

function options(argv) {
  const result = { command: argv[0] };
  const flags = new Set(["allow-partial", "help"]);
  for (let i = 1; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith("--")) throw new Error(`Unexpected argument: ${token}`);
    const name = token.slice(2);
    if (flags.has(name)) result[name] = true;
    else {
      if (!argv[i + 1] || argv[i + 1].startsWith("--")) throw new Error(`Missing value for ${token}`);
      result[name] = argv[++i];
    }
  }
  return result;
}

function required(value, name) {
  if (!value) throw new Error(`Missing --${name}`);
  return value;
}

function checkEnum(value, name, values) {
  required(value, name);
  if (!values.includes(value)) throw new Error(`Invalid --${name}: ${value}`);
  return value;
}

function checkMarket(value) {
  if (!/^[A-Z]{2}$/.test(required(value, "market"))) throw new Error("--market must be a two-letter uppercase country code");
  return value;
}

function checkDate(value, name) {
  if (value && (!/^\d{4}-\d{2}-\d{2}$/.test(value) ||
      Number.isNaN(Date.parse(`${value}T00:00:00Z`)) ||
      new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) !== value)) {
    throw new Error(`--${name} must be YYYY-MM-DD`);
  }
  return value;
}

function limit(value) {
  const number = value === undefined ? 10 : Number(value);
  if (!Number.isInteger(number) || number < 1 || number > 100) throw new Error("--limit must be an integer from 1 to 100");
  return number;
}

function sourceConfig(source) {
  if (/^https?:\/\//.test(source)) {
    const base = new URL(source.endsWith("/") ? source : `${source}/`);
    if (base.protocol !== "https:" || base.hostname !== "raw.githubusercontent.com" ||
        !/^\/[^/]+\/[^/]+\/data\/v1\/$/.test(base.pathname)) {
      throw new Error("Remote --source must be a GitHub raw HTTPS data/v1 URL");
    }
    return { kind: "url", base };
  }
  if (!path.isAbsolute(source)) throw new Error("A local --source must be an absolute directory path");
  return { kind: "file", base: path.resolve(source) };
}

function resource(source, relative) {
  if (!/^(views\/|snapshots\/)/.test(relative) || relative.split("/").some((part) => part === ".." || part === ".")) {
    throw new Error(`Invalid data path: ${relative}`);
  }
  return source.kind === "url" ? new URL(relative, source.base).href : path.join(source.base, relative);
}

async function json(source, relative) {
  const location = resource(source, relative);
  return JSON.parse(source.kind === "url" ? await remoteText(location) : await readFile(location, "utf8"));
}

async function remoteText(url) {
  let response;
  try {
    response = await fetch(url, { signal: AbortSignal.timeout(15000) });
  } catch (error) {
    // Node 22 fetch does not automatically use the proxy settings that curl supports.
    if (!process.env.HTTPS_PROXY && !process.env.https_proxy && !process.env.ALL_PROXY) throw error;
    const { stdout } = await execFileAsync("curl", [
      "--fail", "--silent", "--show-error", "--location", "--max-time", "15", url
    ], { maxBuffer: 15_000_000 });
    return stdout;
  }
  if (!response.ok) throw new Error(`${url} returned HTTP ${response.status}`);
  return response.text();
}

function websiteUrl(page, values = {}) {
  const url = new URL(page, WEBSITE);
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined && value !== null) url.searchParams.set(key, String(value));
  }
  return url.href;
}

function chartWebsiteUrl(target, date) {
  return websiteUrl("", {
    store: target.store, market: target.market, scope: target.scope,
    chart: target.chart, date
  });
}

function appWebsiteUrl(target, appId) {
  return websiteUrl("app.html", {
    store: target.store, market: target.market,
    scope: target.scope, chart: target.chart, id: appId
  });
}

async function siteJson(relative) {
  const local = process.env.APPORBIT_SITE_DIR;
  if (local) {
    if (!path.isAbsolute(local)) throw new Error("APPORBIT_SITE_DIR must be an absolute path");
    return JSON.parse(await readFile(path.join(local, relative), "utf8"));
  }
  const url = websiteUrl(relative);
  return JSON.parse(await remoteText(url));
}

function publishedOutcomes(bootstrap) {
  if (bootstrap.schemaVersion !== 1 || !Array.isArray(bootstrap.runs)) {
    throw new Error("Invalid AppOrbit agent index");
  }
  return bootstrap.runs.flatMap((run) => (run.targets ?? []).map((item) => ({
    ...item, runId: run.runId
  }))).filter((item) => item.target?.publicationMode === "publish")
    .sort((a, b) => b.finishedAt.localeCompare(a.finishedAt));
}

function targetOptions(opts) {
  const store = checkEnum(opts.store, "store", ["apple", "google-play"]);
  const market = checkMarket(opts.market);
  const scope = checkEnum(opts.scope, "scope", ["apps", "games"]);
  const chart = checkEnum(opts.chart, "chart", ["top-free", "top-paid", "top-grossing"]);
  const category = opts.category ?? (scope === "apps" ? "all-apps" : "all-games");
  return { store, market, scope, chart, category };
}

function targetMatches(outcome, target) {
  const actual = outcome.target;
  return actual.store === target.store && actual.market === target.market && actual.scope === target.scope &&
    actual.chart === target.chart && actual.normalizedCategory === target.category;
}

function dateFromPath(snapshotPath) {
  const match = snapshotPath?.match(/\/(\d{4})\/(\d{2})\/(\d{2})\//);
  return match ? `${match[1]}-${match[2]}-${match[3]}` : null;
}

function eligible(outcomes, target, allowPartial = false) {
  return outcomes.filter((item) => targetMatches(item, target) && item.snapshotPath &&
    (item.status === "valid" || (allowPartial && item.status === "partial")) &&
    /^snapshots\/[A-Za-z0-9_\-/]+\.json$/.test(item.snapshotPath));
}

function choose(outcomes, date, allowPartial = false) {
  const matches = date ? outcomes.filter((item) => dateFromPath(item.snapshotPath) === date) : outcomes;
  if (!date && allowPartial) return matches[0] ?? null;
  return matches.find((item) => item.status === "valid") ?? (allowPartial ? matches[0] : null) ?? null;
}

async function snapshot(source, outcome) {
  const relative = outcome.snapshotPath;
  const data = await json(source, relative);
  const sameTarget = ["store", "market", "scope", "chart", "normalizedCategory"].every(
    (key) => data[key] === outcome.target[key]
  );
  if (!sameTarget || data.snapshotId === undefined || !Array.isArray(data.entries) ||
      data.status !== outcome.status || data.actualCount !== data.entries.length ||
      data.entries.some((entry, index) => entry.rank !== index + 1) ||
      new Set(data.entries.map((entry) => entry.appId)).size !== data.entries.length) {
    throw new Error(`Invalid or mismatched snapshot: ${relative}`);
  }
  return { data, url: resource(source, relative) };
}

function catalogPath(store, market) {
  return `api/catalog/${store}/${market}.json`;
}

async function catalog(store, market) {
  const relative = catalogPath(store, market);
  const data = await siteJson(relative);
  if (!data.catalog || typeof data.catalog !== "object") throw new Error(`Invalid catalog: ${relative}`);
  return { data: data.catalog, url: websiteUrl(relative) };
}

function context(snapshotValue, outcome, url) {
  return {
    runId: outcome.runId,
    snapshotId: snapshotValue.snapshotId,
    snapshotUrl: url,
    capturedAt: snapshotValue.capturedAt,
    marketObservationDate: snapshotValue.marketObservationDate ?? snapshotValue.observationDate,
    status: snapshotValue.status,
    observedCount: snapshotValue.actualCount,
    expectedCount: snapshotValue.expectedCount
  };
}

async function run(opts) {
  if (!opts.command || opts.help || opts.command === "--help") return { help: usage };
  const source = sourceConfig(opts.source ?? process.env.APPORBIT_SOURCE ?? DEFAULT_SOURCE);
  if (opts.command === "app") {
    const store = checkEnum(opts.store, "store", ["apple", "google-play"]);
    const market = checkMarket(opts.market);
    const appId = required(opts["app-id"], "app-id");
    const scope = opts.scope ? checkEnum(opts.scope, "scope", ["apps", "games"]) : undefined;
    const chart = opts.chart ? checkEnum(opts.chart, "chart", ["top-free", "top-paid", "top-grossing"]) : undefined;
    const relative = `api/apps/${store}/${market}/${encodeURIComponent(appId)}.json`;
    const payload = await siteJson(relative);
    const metadata = payload.metadata ?? null;
    if (!metadata) throw new Error("App metadata is unavailable for this store and market");
    return {
      metadata,
      metadataUrl: websiteUrl(relative),
      websiteUrl: appWebsiteUrl({ store, market, scope, chart }, appId)
    };
  }
  if (opts.command === "search") {
    const store = checkEnum(opts.store, "store", ["apple", "google-play"]);
    const market = checkMarket(opts.market);
    const query = required(opts.query, "query").toLocaleLowerCase();
    const directory = await catalog(store, market);
    const matches = Object.values(directory.data).filter((item) =>
      `${item.name ?? ""} ${item.developer ?? ""} ${item.appId ?? ""}`.toLocaleLowerCase().includes(query)
    ).slice(0, limit(opts.limit)).map((item) => ({
      appId: item.appId,
      name: item.name,
      developer: item.developer,
      observedAt: item.observedAt,
      rating: item.rating ?? null,
      ratingsCount: item.ratingsCount ?? null,
      storeUrl: item.storeUrl ?? null,
      websiteUrl: appWebsiteUrl({ store, market }, item.appId)
    }));
    return { store, market, query: opts.query, matches, catalogUrl: directory.url };
  }
  let bootstrap;
  try {
    bootstrap = await json(source, "views/agent-index-v1.json");
  } catch (error) {
    if (error?.code === "ENOENT" || /\b404\b/.test(String(error))) {
      throw new Error("The published run index is missing from the data branch; wait for the collection workflow to build it");
    }
    throw error;
  }
  const outcomes = publishedOutcomes(bootstrap);
  if (opts.command === "coverage") {
    const byTarget = new Map();
    for (const outcome of outcomes) {
      if (!byTarget.has(outcome.targetKey)) byTarget.set(outcome.targetKey, []);
      byTarget.get(outcome.targetKey).push(outcome);
    }
    return {
      source: resource(source, "views/agent-index-v1.json"),
      generatedAt: bootstrap.generatedAt,
      websiteUrl: websiteUrl("data.html"),
      publishedTargets: [...byTarget.entries()].map(([targetKey, history]) => ({
        targetKey,
        target: history[0].target,
        latestOutcome: { status: history[0].status, finishedAt: history[0].finishedAt },
        latestValid: history.find((item) => item.status === "valid" && item.snapshotPath)?.snapshotPath ?? null,
        latestPartial: history.find((item) => item.status === "partial" && item.snapshotPath)?.snapshotPath ?? null
      }))
    };
  }
  if (!["rankings", "movers"].includes(opts.command)) throw new Error(`Unknown command: ${opts.command}`);
  const target = targetOptions(opts);
  const history = eligible(outcomes, target, opts.command === "rankings" && opts["allow-partial"]);
  if (!history.length) throw new Error("No published complete chart for this target");
  if (opts.command === "rankings") {
    const date = checkDate(opts.date, "date");
    const selected = choose(history, date, Boolean(opts["allow-partial"]));
    if (!selected) throw new Error(`No eligible observation for ${date}`);
    const { data, url } = await snapshot(source, selected);
    let directory = null;
    let metadataWarning = null;
    try {
      directory = await catalog(target.store, target.market);
    } catch (error) {
      metadataWarning = error instanceof Error ? error.message : String(error);
    }
    const dateForWebsite = data.marketObservationDate ?? data.observationDate;
    return {
      target, indexGeneratedAt: bootstrap.generatedAt, ...context(data, selected, url),
      websiteUrl: chartWebsiteUrl(target, dateForWebsite),
      entries: data.entries.slice(0, limit(opts.limit)).map((entry) => ({
        ...entry, name: directory?.data[entry.appId]?.name ?? null,
        developer: directory?.data[entry.appId]?.developer ?? null,
        websiteUrl: appWebsiteUrl(target, entry.appId)
      })),
      metadataUrl: directory?.url ?? null,
      metadataWarning
    };
  }
  const from = checkDate(opts.from, "from");
  const to = checkDate(opts.to, "to");
  const current = choose(history, to);
  if (!current) throw new Error(`No complete observation for ${to}`);
  const previous = from
    ? choose(history.filter((item) => item.finishedAt < current.finishedAt), from)
    : history.find((item) => item.snapshotPath !== current.snapshotPath && item.finishedAt < current.finishedAt);
  if (!previous) throw new Error("No earlier complete observation for comparison");
  const [currentSnapshot, previousSnapshot] = await Promise.all([
    snapshot(source, current), snapshot(source, previous)
  ]);
  let directory = null;
  let metadataWarning = null;
  try {
    directory = await catalog(target.store, target.market);
  } catch (error) {
    metadataWarning = error instanceof Error ? error.message : String(error);
  }
  const priorRanks = new Map(previousSnapshot.data.entries.map((entry) => [entry.appId, entry.rank]));
  const changes = currentSnapshot.data.entries.map((entry) => ({
    appId: entry.appId,
    name: directory?.data[entry.appId]?.name ?? null,
    rank: entry.rank,
    previousRank: priorRanks.get(entry.appId) ?? null,
    movement: priorRanks.has(entry.appId) ? priorRanks.get(entry.appId) - entry.rank : null,
    websiteUrl: appWebsiteUrl(target, entry.appId)
  }));
  const count = limit(opts.limit);
  return {
    target,
    indexGeneratedAt: bootstrap.generatedAt,
    current: {
      ...context(currentSnapshot.data, current, currentSnapshot.url),
      websiteUrl: chartWebsiteUrl(target, currentSnapshot.data.marketObservationDate ?? currentSnapshot.data.observationDate)
    },
    previous: {
      ...context(previousSnapshot.data, previous, previousSnapshot.url),
      websiteUrl: chartWebsiteUrl(target, previousSnapshot.data.marketObservationDate ?? previousSnapshot.data.observationDate)
    },
    trendingWebsiteUrl: websiteUrl("trending.html", {
      store: target.store, market: target.market, scope: target.scope, chart: target.chart
    }),
    risers: changes.filter((item) => item.movement > 0).sort((a, b) => b.movement - a.movement || a.rank - b.rank).slice(0, count),
    fallers: changes.filter((item) => item.movement < 0).sort((a, b) => a.movement - b.movement || a.rank - b.rank).slice(0, count),
    entrants: changes.filter((item) => item.previousRank === null).slice(0, count),
    metadataUrl: directory?.url ?? null,
    metadataWarning
  };
}

try {
  console.log(JSON.stringify(await run(options(process.argv.slice(2))), null, 2));
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}

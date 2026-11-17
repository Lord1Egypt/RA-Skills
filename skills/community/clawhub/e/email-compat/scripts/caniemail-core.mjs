/**
 * caniemail-ai-tooling — shared core.
 *
 * The single implementation behind both surfaces (skill and MCP server).
 * Vendored byte-identically into `skill/scripts/` and `mcp/src/`; never edit a
 * vendored copy, edit this file and run `make sync-core`.
 *
 * Plain ESM with JSDoc types rather than TypeScript, so the vendored copies
 * need no build step on either surface. There are no runtime dependencies at
 * all: Node 24+ and nothing else. Detection lives in `detect.mjs` and the
 * scanners beside it; resolution lives here.
 *
 * Detection and resolution are kept apart on purpose. "What does this markup
 * use?" is a question about the markup, and "how well does client X support
 * it?" a question about the dataset; answering the first in terms of the
 * second is what made the previous implementation need 48 parses to see one
 * document, and what made 22 features undetectable however many it ran.
 */

import { readFile, writeFile, mkdir, rename, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { homedir, tmpdir } from 'node:os';

import { detectFeatures } from './detect.mjs';
import { escapeRegExp } from './feature-titles.mjs';
import bundledData from './data/caniemail.json' with { type: 'json' };

const DATA_URL = 'https://www.caniemail.com/api/data.json';

/**
 * The four verdicts caniemail's dataset actually distinguishes.
 *
 * `caniemail`'s own API collapses `a` and `u` into a single `partial` bucket,
 * which destroys the distinction between "works with a documented workaround"
 * and "nobody has ever tested this". Those demand opposite actions from an
 * agent, so they stay separate here.
 */
export const SUPPORTED = /** @type {const} */ ('supported');
export const UNSUPPORTED = /** @type {const} */ ('unsupported');
export const MITIGATED = /** @type {const} */ ('mitigated');
export const UNTESTED = /** @type {const} */ ('untested');

/** Every verdict, in the order a count of them is reported. */
const VERDICTS = /** @type {const} */ ([SUPPORTED, UNSUPPORTED, MITIGATED, UNTESTED]);

/** @typedef {(typeof VERDICTS)[number]} Verdict */

/**
 * The verdicts a lint reports, which is every one but `supported`.
 *
 * @typedef {Exclude<Verdict, 'supported'>} ProblemVerdict
 */

/**
 * Raw dataset letter -> verdict. Anything unrecognised is treated as untested.
 *
 * @type {Partial<Record<string, Verdict>>}
 */
const VERDICT_BY_LETTER = { y: SUPPORTED, n: UNSUPPORTED, a: MITIGATED, u: UNTESTED };

/* Detection strategy is documented on `detectFeatures`, near its use. */

/* -------------------------------------------------------------------------- */
/* Dataset loading                                                             */
/* -------------------------------------------------------------------------- */

/**
 * One feature record as caniemail publishes it. Only the fields read here are
 * named, and every one of them is read defensively, because a record comes off
 * the network and is believed only as far as `isDatasetShaped` checks it.
 *
 * `stats` is `family -> platform -> version -> cell`, where a cell is a verdict
 * letter followed by any `#n` note references, e.g. `"a #1"`. Version keys are
 * in authored order, which is chronological; see `resolveSupport`.
 *
 * @typedef {object} Feature
 * @property {string} slug
 * @property {string} title
 * @property {string} category
 * @property {string|null} [description]
 * @property {string} [url]
 * @property {string} [last_test_date]
 * @property {string|null} [keywords]  Comma-separated.
 * @property {string[]} [tags]
 * @property {string|null} [notes]
 * @property {Record<string, string>|null} [notes_by_num]
 * @property {Record<string, Record<string, Record<string, string>>>} stats
 */

/**
 * The part of a feature that resolution reads, and all a caller has to supply.
 *
 * @typedef {Pick<Feature, 'stats'|'notes_by_num'>} FeatureSupport
 */

/**
 * The dataset as caniemail serves it, before indexing.
 *
 * @typedef {object} RawDataset
 * @property {Feature[]} data
 * @property {string} last_update_date
 * @property {Record<string, Record<string, string>>} [nicenames]
 */

/**
 * @typedef {object} Dataset
 * @property {Feature[]} features       Raw feature records, as authored upstream.
 * @property {string[]} clients        `family.platform` ids derived from the data.
 * @property {Map<string, Feature>} bySlug
 * @property {Map<string, Feature>} byTitle
 * @property {Record<string, Record<string, string>>} nicenames
 * @property {DatasetMeta} meta
 */

/**
 * @typedef {object} DatasetMeta
 * @property {'live'|'cache'|'bundled'} source
 * @property {string} lastUpdate      Upstream `last_update_date`.
 * @property {string|null} fetchedAt  ISO time this copy was retrieved, if known.
 * @property {number} featureCount
 * @property {string|null} warning    Set when the copy in use is not the live one.
 */

function defaultCacheDir() {
  const xdg = process.env.XDG_CACHE_HOME;
  if (xdg) return join(xdg, 'caniemail-ai-tooling');
  try {
    return join(homedir(), '.cache', 'caniemail-ai-tooling');
  } catch {
    return join(tmpdir(), 'caniemail-ai-tooling');
  }
}

/**
 * Is this shaped like the caniemail dataset?
 *
 * A 200 response carrying well-formed JSON used to be accepted on the strength
 * of the JSON alone. `indexDataset` reads `raw.data ?? []`, so an endpoint that
 * had moved and said so — `{"message": "API moved to /v2/data.json"}` — indexed
 * to zero features and was returned as `source: "live"` with `warning: null`,
 * then written to the shared disk cache and served from there for the next 24
 * hours. Every promise this project makes about a stale answer being visibly
 * stale was intact and pointing the wrong way: `search_features` reported every
 * feature as nonexistent, and `check_feature_support` and `lint_email` failed
 * with "No client matches", which reads as the caller's typo.
 *
 * The test is structural rather than a count. What distinguishes a dataset from
 * an error page decoded as JSON is that its entries are feature records, and
 * that is as true of the one-feature fixture the loopback tests serve as it is
 * of the full dataset upstream publishes. `make refresh-data` applies a `>= 250`
 * floor on top of this one, because "is this the whole dataset" is the right
 * question for the committed snapshot and the wrong one at runtime, where
 * `dataUrl` may legitimately point at a mirror or a proxy.
 *
 * The bundled snapshot is deliberately not put through this. It is committed,
 * it is what the suite runs against, and it is the last rung of the ladder —
 * rejecting it would leave nothing to fall back to.
 *
 * @param {any} raw
 * @returns {boolean}
 */
export function isDatasetShaped(raw) {
  const features = raw?.data;
  if (!Array.isArray(features) || features.length === 0) return false;
  return features.every(
    (feature) =>
      feature !== null &&
      typeof feature === 'object' &&
      typeof feature.slug === 'string' &&
      feature.stats !== null &&
      typeof feature.stats === 'object',
  );
}

/**
 * @param {RawDataset} raw
 * @param {Pick<DatasetMeta, 'source'|'fetchedAt'|'warning'>} meta
 * @returns {Dataset}
 */
function indexDataset(raw, meta) {
  const features = raw.data ?? [];

  // The client roster is derived from the data rather than hardcoded or read
  // out of the package's internals, which its export map blocks anyway. The
  // two agree exactly today (48 clients), and deriving means a client added
  // upstream appears here without a release.
  /** @type {Set<string>} */
  const clients = new Set();
  for (const feature of features) {
    for (const family of Object.keys(feature.stats ?? {})) {
      for (const platform of Object.keys(feature.stats[family] ?? {})) {
        clients.add(`${family}.${platform}`);
      }
    }
  }

  return {
    features,
    clients: [...clients].sort(),
    bySlug: new Map(features.map((f) => [f.slug, f])),
    byTitle: new Map(features.map((f) => [f.title, f])),
    nicenames: raw.nicenames ?? {},
    meta: { ...meta, lastUpdate: raw.last_update_date, featureCount: features.length },
  };
}

/**
 * Load the caniemail dataset, preferring live data over the bundled snapshot.
 *
 * The snapshot in `data/caniemail.json` is committed to this repo and refreshed
 * with `make refresh-data`. It exists so that a skill copied to a machine with
 * no network still answers, and so the test suite is deterministic — both of
 * which the `caniemail` package used to provide for free, and neither of which
 * survived removing it.
 *
 * We fetch live, cache to disk, and fall back to the snapshot so the tools
 * never hard-fail offline. `meta.source` and `meta.warning` always say which
 * copy is in play, so a stale answer is visibly stale rather than silently
 * wrong.
 *
 * @param {object} [options]
 * @param {string} [options.cacheDir]
 * @param {string} [options.dataUrl]   Fetch from somewhere other than caniemail.com.
 * @param {number} [options.maxAgeMs]  Refetch if the cache is older than this.
 * @param {boolean} [options.offline]  Skip the network entirely.
 * @param {number} [options.timeoutMs]
 * @returns {Promise<Dataset>}
 */
export async function loadDataset(options = {}) {
  const {
    cacheDir = defaultCacheDir(),
    // Points at a mirror or a proxy for anyone who cannot reach caniemail.com
    // directly, and it is the seam `dataset-cache.test.mjs` drives: everything
    // below — the cache freshness boundary, the corrupt-cache fallthrough, the
    // fetch-failure ladder down to the bundle, the abort timeout — is what
    // `meta.source` and `meta.warning` are computed from, and a loopback server
    // exercises the real `fetch` rather than a stub standing in for it.
    dataUrl = DATA_URL,
    maxAgeMs = 24 * 60 * 60 * 1000,
    offline = false,
    timeoutMs = 10_000,
  } = options;

  const cacheFile = join(cacheDir, 'data.json');

  if (!offline) {
    // A fresh cache short-circuits the fetch; anything else re-checks the network.
    const fresh = await readCache(cacheFile);
    const age = fresh ? Date.now() - Date.parse(fresh.fetchedAt) : NaN;
    if (fresh && Number.isFinite(age) && age < maxAgeMs) {
      return indexDataset(fresh.raw, {
        source: 'cache',
        fetchedAt: fresh.fetchedAt,
        warning: null,
      });
    }

    try {
      // One signal for the headers and the body alike, so a server that sends
      // headers and then stalls is bounded too. It is unref'd as well: a fetch
      // that fails fast leaves nothing behind to hold the process open, where a
      // plain `setTimeout` kept every offline CLI run alive for `timeoutMs`
      // after its answer had been printed.
      const response = await fetch(dataUrl, { signal: AbortSignal.timeout(timeoutMs) });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const raw = await response.json();
      // Parsing as JSON is not evidence of being the dataset, and this throw is
      // what keeps the two apart. It lands in the catch below, so a response
      // that is merely well-formed takes the same route as a 500 or a timeout:
      // down to the cache, then to the bundle, with a warning saying so. Placed
      // ahead of the cache write on purpose — the damage worth preventing is
      // not one bad answer, it is one bad answer persisted for a day and shared
      // with every other process on this machine.
      if (!isDatasetShaped(raw)) throw new Error('response is not shaped like the dataset');
      const fetchedAt = new Date().toISOString();
      await writeCache(cacheDir, cacheFile, { fetchedAt, raw });
      return indexDataset(raw, { source: 'live', fetchedAt, warning: null });
    } catch {
      // Fall through to cache-then-bundle.
    }

    const stale = await readCache(cacheFile);
    if (stale) {
      return indexDataset(stale.raw, {
        source: 'cache',
        fetchedAt: stale.fetchedAt,
        warning: 'Live fetch failed; using cached data, which may be out of date.',
      });
    }
  }

  // Through `unknown` because the checker types a JSON import from the file's
  // literal contents, a different object shape per feature, and no two of those
  // agree with each other closely enough to be read as one `Feature`.
  return indexDataset(/** @type {RawDataset} */ (/** @type {unknown} */ (bundledData)), {
    source: 'bundled',
    fetchedAt: null,
    warning: offline
      ? 'Offline mode: using the dataset snapshot bundled with this tool, which lags the site.'
      : 'Live fetch and cache both unavailable; using the dataset snapshot bundled with this tool, which lags the site.',
  });
}

/**
 * The disk cache, or `null` when there is none worth using: missing,
 * unparseable and misshapen are all the same answer, and none is an error.
 *
 * Misshapen is corrupt. A cache written before the shape check existed is still
 * on disk, so the guard on the fetch is not enough on its own to end an ongoing
 * poisoning — checking here, on every read, is what does.
 *
 * @param {string} cacheFile
 * @returns {Promise<{ raw: RawDataset, fetchedAt: string } | null>}
 */
async function readCache(cacheFile) {
  try {
    const cached = JSON.parse(await readFile(cacheFile, 'utf8'));
    return isDatasetShaped(cached.raw) ? cached : null;
  } catch {
    return null;
  }
}

/**
 * Write the cache, or quietly fail to: an unwritable cache degrades
 * performance, not correctness.
 *
 * Written to a per-process temp file and renamed, because the two surfaces
 * share one cache directory: an MCP server and a CLI run can refresh at the
 * same moment, and a plain write interleaves them into a truncated file. The
 * shape check in `readCache` catches that, so the cost was a redundant fetch
 * rather than a failure — but rename is atomic and this is one line.
 *
 * @param {string} cacheDir
 * @param {string} cacheFile
 * @param {{ fetchedAt: string, raw: RawDataset }} record
 */
async function writeCache(cacheDir, cacheFile, record) {
  const temporary = `${cacheFile}.${process.pid}.tmp`;
  try {
    await mkdir(cacheDir, { recursive: true });
    await writeFile(temporary, JSON.stringify(record));
    await rename(temporary, cacheFile);
  } catch {
    await rm(temporary, { force: true }).catch(() => {});
  }
}

/**
 * A dataset for a process that outlives one call, reloaded once it is
 * `revalidateMs` old.
 *
 * A reload in progress is shared. Calls that arrive while one is running wait
 * for it rather than starting their own, or an agent firing three tools after a
 * quiet quarter of an hour would pay for three loads and keep one.
 *
 * @param {number} revalidateMs
 * @param {Parameters<typeof loadDataset>[0]} [loadOptions]
 * @returns {() => Promise<Dataset>}
 */
export function revalidatingDataset(revalidateMs, loadOptions = {}) {
  /** @type {{value: Dataset, at: number} | null} */
  let loaded = null;
  /** @type {Promise<Dataset> | null} */
  let reloading = null;

  async function reload() {
    try {
      const next = await loadDataset(loadOptions);
      const held = loaded?.value;

      // A revalidation that finds upstream unmoved keeps the *same* feature
      // array. That array is the WeakMap key `buildTitleTables` memoises on and
      // `loadDataset` returns a fresh one every time, so adopting `next`
      // wholesale discards title tables that describe data identical to the
      // data replacing it.
      //
      // Worth about 1ms per revalidation, and no more than that. The re-parse
      // and re-index still happen (~12ms from a warm disk cache). It is kept
      // for saying something true, that unmoved data is the same dataset, at no
      // runtime cost.
      //
      // The new `meta` is adopted regardless, and that is the part that has to
      // be right: it carries `source` and `fetchedAt`, so keeping the old
      // object outright would report a `fetchedAt` from a quarter of an hour
      // ago and call a just-revalidated answer stale.
      const unmoved =
        held &&
        held.meta.lastUpdate === next.meta.lastUpdate &&
        held.meta.featureCount === next.meta.featureCount;

      loaded = { value: unmoved ? { ...held, meta: next.meta } : next, at: Date.now() };
      return loaded.value;
    } finally {
      reloading = null;
    }
  }

  return () => {
    if (loaded && Date.now() - loaded.at < revalidateMs) return Promise.resolve(loaded.value);
    reloading ??= reload();
    return reloading;
  };
}

/* -------------------------------------------------------------------------- */
/* Client globs                                                                */
/* -------------------------------------------------------------------------- */

/**
 * Expand `family.platform` globs against the known client list.
 *
 * Deliberately reimplemented rather than delegating to the package's
 * micromatch-based `parseClients`, so that an unmatched glob is an explicit
 * error instead of a silently empty result — an agent that typos
 * `outlook.win` should be told, not handed a clean bill of health.
 *
 * @param {Dataset} dataset
 * @param {string[]} globs
 * @returns {string[]} Matching client ids, sorted and deduplicated.
 */
export function expandClients(dataset, globs) {
  // Two different mistakes, and one message for both used to send the second
  // one the wrong way: `{ clients: 'outlook.windows' }` — the plausible slip,
  // and one the zod schema and the CLI both rule out before they get here — was
  // answered with "at least one client is required", when one had been given.
  if (!Array.isArray(globs)) {
    throw new Error(
      `Clients must be an array, not ${globs === null ? 'null' : typeof globs}. ` +
        'Pass ["outlook.windows"], not "outlook.windows".',
    );
  }
  if (globs.length === 0) {
    throw new Error('At least one client or glob is required. Use ["*"] for all clients.');
  }
  const matched = new Set();
  const unmatched = [];
  for (const glob of globs) {
    const text = String(glob);
    // A bare "*" means every client. Elsewhere a wildcard is confined to one
    // segment, so "outlook.*" cannot reach across the dot into another family.
    // A run of stars is one star: n adjacent `[^.]*` match the same language as
    // one, and backtrack exponentially in n on a subject they cannot match.
    const pattern =
      text === '*'
        ? /^.+$/
        : new RegExp(`^${text.replace(/\*+/g, '*').split('*').map(escapeRegExp).join('[^.]*')}$`);
    const hits = dataset.clients.filter((client) => pattern.test(client));
    if (hits.length === 0) unmatched.push(glob);
    for (const hit of hits) matched.add(hit);
  }
  if (unmatched.length > 0) {
    throw new Error(
      `No client matches: ${unmatched.join(', ')}. ` +
        `Clients are "family.platform", e.g. outlook.windows, gmail.desktop-webmail. ` +
        `Use listClients() for the full list.`,
    );
  }
  return [...matched].sort();
}

/**
 * The full client roster, with human-readable names.
 * @param {Dataset} dataset
 */
export function listClients(dataset) {
  const family = dataset.nicenames?.family ?? {};
  const platform = dataset.nicenames?.platform ?? {};
  const clients = dataset.clients.map((client) => {
    const [fam, plat] = client.split('.');
    return { client, family: family[fam] ?? fam, platform: platform[plat] ?? plat };
  });
  return { clients, count: clients.length, data_source: dataset.meta };
}

/**
 * Every feature category in the dataset, sorted.
 * @param {Dataset} dataset
 */
export function categoriesOf(dataset) {
  return [...new Set(dataset.features.map((feature) => feature.category))].sort();
}

/* -------------------------------------------------------------------------- */
/* Support resolution                                                          */
/* -------------------------------------------------------------------------- */

/**
 * Resolve one feature's support in one client.
 *
 * Version selection takes the **last key as authored**, and does not sort.
 * This is the whole correctness argument, so it is worth stating plainly: the
 * upstream JSON preserves the order the site itself displays, which is
 * chronological by construction, and any re-sort corrupts it. A lexicographic
 * sort mis-picks 280 cells and a numeric sort 264 — `outlook.macos` carries
 * `["2011", "2016", "16.80"]`, where the newest entry sorts smallest under
 * both. The package sorts lexicographically and inherits every one of those.
 *
 * @param {FeatureSupport} feature
 * @param {string} client  `family.platform`.
 * @param {object} [options]
 * @param {string} [options.version] Pin a specific version instead of the latest.
 * @returns {{verdict: Verdict, version: string|null, raw: string|null, notes: string[]}}
 */
export function resolveSupport(feature, client, options = {}) {
  const versions = cellsFor(feature, client);

  // No entry at all is untested, not unsupported. 16% of pairs land here, and
  // this is precisely where the package throws instead of answering.
  const keys = versions ? Object.keys(versions) : [];
  if (!versions || keys.length === 0) {
    return { verdict: UNTESTED, version: null, raw: null, notes: [] };
  }

  let version;
  if (options.version) {
    if (!Object.hasOwn(versions, options.version)) {
      const available = keys.join(', ');
      throw new Error(
        `No data for ${client} version "${options.version}". Available: ${available}.`,
      );
    }
    version = options.version;
  } else {
    version = keys[keys.length - 1];
  }

  const raw = String(versions[version]);
  const letter = raw.trim()[0];
  const verdict = VERDICT_BY_LETTER[letter] ?? UNTESTED;

  return { verdict, version, raw, notes: notesFor(feature, raw) };
}

/**
 * Resolve `#1 #2` note references against the feature's `notes_by_num` map.
 *
 * Only the notes this cell actually references. The feature-level `notes`
 * field is deliberately excluded: it is a general remark about the feature,
 * often describing one specific client, and attaching it to every verdict
 * produces contradictions — `css-gap` is unsupported in Outlook but its global
 * note reads "Partial. Supports column-gap for flexbox", which is about Gmail.
 * An error that carries a note describing partial support is worse than no
 * note. It is surfaced separately as `feature_notes`.
 *
 * @param {FeatureSupport} feature
 * @param {string} raw  The cell, e.g. `"a #1 #2"`.
 */
function notesFor(feature, raw) {
  /** @type {string[]} */
  const notes = [];
  for (const match of String(raw).matchAll(/#(\d+)/g)) {
    const note = feature?.notes_by_num?.[match[1]];
    if (note) notes.push(note);
  }
  return notes;
}

/**
 * The feature-level remark, which applies to the feature rather than any one client.
 *
 * @param {Feature} feature
 */
function featureNotes(feature) {
  return feature?.notes ? String(feature.notes).trim() : null;
}

/**
 * The version keys on record for a client, in authored order.
 *
 * @param {FeatureSupport} feature
 * @param {string} client  `family.platform`.
 */
export function versionsFor(feature, client) {
  const versions = cellsFor(feature, client);
  return versions ? Object.keys(versions) : [];
}

/**
 * A client's version-to-cell record, or `null` when it has none. Anything that
 * is not an object counts as none, so a malformed entry reads as untested
 * rather than as a list of its characters.
 *
 * @param {FeatureSupport} feature
 * @param {string} client  `family.platform`.
 * @returns {Record<string, string> | null}
 */
function cellsFor(feature, client) {
  const [family, platform] = client.split('.');
  const versions = feature?.stats?.[family]?.[platform];
  return versions && typeof versions === 'object' ? versions : null;
}

/* -------------------------------------------------------------------------- */
/* Tool: check_feature_support                                                 */
/* -------------------------------------------------------------------------- */

/**
 * Per-client verdicts for one feature.
 *
 * @param {Dataset} dataset
 * @param {string} slug    Feature slug, e.g. `css-flexbox`.
 * @param {string[]} clientGlobs
 * @param {object} [options]
 * @param {string} [options.version]
 */
export function checkFeatureSupport(dataset, slug, clientGlobs, options = {}) {
  const feature = dataset.bySlug.get(slug);
  if (!feature) {
    throw new Error(`Unknown feature "${slug}". Use search_features to find the right slug.`);
  }
  const clients = expandClients(dataset, clientGlobs);
  const pinned = options.version ?? null;

  // "Does this work in Outlook 2016" is the question people actually have, and
  // its natural spelling is `outlook.*` with `--version 2016`. Letting
  // `resolveSupport` throw across a fan-out made that fail on the first sibling
  // that versions itself by date, naming a client the caller never asked about.
  // A pin no requested client carries is still an error — that is a typo — but
  // one that only some carry is resolved per client.
  const records = clients.map((client) => ({ client, onRecord: versionsFor(feature, client) }));

  if (pinned && !records.some(({ onRecord }) => onRecord.includes(pinned))) {
    const withData = records.find(({ onRecord }) => onRecord.length > 0)?.client;
    // Guaranteed to throw: the pin is absent from this client's keys. Going
    // through `resolveSupport` keeps one wording, and one place that knows how
    // to list what is on record. With no client carrying any version at all
    // there is nothing to correct the caller with, and every entry below is
    // untested anyway.
    if (withData) resolveSupport(feature, withData, { version: pinned });
  }

  const support = records.map(({ client, onRecord }) => {
    if (pinned && !onRecord.includes(pinned)) {
      // No data for the version asked about is precisely `untested`: not
      // supported, not unsupported, nothing on record. `notes` stays empty
      // because an untested verdict has no findings to report, and
      // `versions_on_record` already shows why the pin did not land.
      //
      // The pin itself is *not* repeated here. It is stated once at the top
      // level, and carrying it per entry both duplicated that and gave the
      // entries in one array two different shapes — present on the clients the
      // pin missed, absent on the ones it landed on — which is worse to consume
      // than either shape alone.
      return {
        client,
        verdict: UNTESTED,
        version: null,
        notes: [],
        versions_on_record: onRecord,
      };
    }

    const resolved = resolveSupport(feature, client, options);
    return {
      client,
      verdict: resolved.verdict,
      version: resolved.version,
      notes: resolved.notes,
      versions_on_record: onRecord,
    };
  });

  return {
    slug: feature.slug,
    title: feature.title,
    description: feature.description,
    category: feature.category,
    url: feature.url,
    last_test_date: feature.last_test_date,
    staleness: stalenessOf(feature.last_test_date),
    feature_notes: featureNotes(feature),
    // Stated once so the pin is visible without reading 48 entries to infer it.
    version_requested: pinned,
    summary: summarise(support),
    support,
    data_source: dataset.meta,
  };
}

/**
 * @param {{verdict: Verdict}[]} support
 * @returns {Record<Verdict, number>}
 */
function summarise(support) {
  return countBy(
    VERDICTS,
    support.map((entry) => entry.verdict),
  );
}

/**
 * How many of `values` are each of `keys`, with every key present and in order.
 *
 * @template {string} K
 * @param {readonly K[]} keys
 * @param {K[]} values
 * @returns {Record<K, number>}
 */
function countBy(keys, values) {
  // Every key is written by the `map`, so the record is complete; `fromEntries`
  // is typed as keyed by any string, which is all the cast narrows.
  const counts = /** @type {Record<K, number>} */ (Object.fromEntries(keys.map((key) => [key, 0])));
  for (const value of values) counts[value] += 1;
  return counts;
}

/**
 * How old a feature's last test is.
 *
 * Freshness is uneven across the dataset — some entries have not been retested
 * in years — and an agent should be able to see that rather than infer it.
 *
 * @param {string|undefined} lastTestDate
 */
function stalenessOf(lastTestDate) {
  if (!lastTestDate) return { years_old: null, note: 'No test date on record.' };
  const then = Date.parse(lastTestDate);
  if (!Number.isFinite(then)) return { years_old: null, note: 'Unparseable test date.' };
  const years = (Date.now() - then) / (365.25 * 24 * 60 * 60 * 1000);
  const rounded = Math.round(years * 10) / 10;
  return {
    years_old: rounded,
    note:
      rounded >= 3
        ? `Last tested ${rounded} years ago; treat with caution and re-verify if it matters.`
        : null,
  };
}

/* -------------------------------------------------------------------------- */
/* Tool: search_features                                                       */
/* -------------------------------------------------------------------------- */

/**
 * Find feature slugs by keyword.
 *
 * Agents do not know that flexbox lives at `css-flexbox` or that "rounded
 * corners" is `css-border-radius`, so without this the lookup tool is
 * unusable. Returns identifiers and one-line descriptions only — never stats —
 * to keep the result small enough to call speculatively.
 *
 * @param {Dataset} dataset
 * @param {string} query
 * @param {object} [options]
 * @param {number} [options.limit]
 * @param {string} [options.category] One of html, css, image, others.
 */
export function searchFeatures(dataset, query, options = {}) {
  const { limit = 15, category } = options;
  const needle = String(query ?? '')
    .trim()
    .toLowerCase();
  if (!needle) throw new Error('A search query is required.');

  // Same stance as an unmatched glob: a request that cannot return anything is
  // an error, not a clean empty result. `--limit 0` on the CLI used to report
  // "42 matches" beside an empty list, and `--limit abc` was worse — NaN slices
  // to nothing, so a typo read as "no such feature". The MCP schema already
  // rejects both; the CLI is where they were reachable.
  if (!Number.isInteger(limit) || limit < 1) {
    // `JSON.stringify(NaN)` is "null", which would name the wrong mistake for
    // the commonest way to get here — `--limit abc` arriving as `Number('abc')`.
    const shown = Number.isNaN(limit) ? 'NaN' : JSON.stringify(limit);
    throw new Error(`limit must be a positive integer, not ${shown}.`);
  }

  // And again for a category: an unknown one filters out every feature. The
  // valid set is read from the data, as the client roster is, not frozen here.
  if (category !== undefined) {
    const categories = categoriesOf(dataset);
    if (!categories.includes(category)) {
      throw new Error(
        `Unknown category ${JSON.stringify(category)}. Use one of: ${categories.join(', ')}.`,
      );
    }
  }

  const terms = needle.split(/\s+/);
  const scored = [];

  for (const feature of dataset.features) {
    if (category !== undefined && feature.category !== category) continue;

    const keywordList = (feature.keywords ?? '')
      .toLowerCase()
      .split(',')
      .map((k) => k.trim())
      .filter(Boolean);

    const haystacks = {
      slug: (feature.slug ?? '').toLowerCase(),
      title: (feature.title ?? '').toLowerCase(),
      keywords: keywordList.join(' '),
      description: (feature.description ?? '').toLowerCase(),
      tags: (feature.tags ?? []).join(' ').toLowerCase(),
    };

    let score = 0;

    // Weighted by how deliberate the match is: an exact slug hit beats a stray
    // word in a description by two orders of magnitude.
    if (haystacks.slug === needle) score += 1000;
    if (haystacks.title === needle) score += 500;

    let matchedTerms = 0;
    for (const term of terms) {
      let termScore = 0;
      if (haystacks.slug.includes(term)) termScore += 60;
      if (haystacks.title.includes(term)) termScore += 50;
      if (keywordList.includes(term)) {
        // An exact keyword, weighted by how much of the feature's keyword set
        // it accounts for. "flexbox" is the only keyword on css-display-flex
        // but one of four on css-align-items, so the former is more on-topic.
        termScore += 30 + Math.round(30 / keywordList.length);
      } else if (haystacks.keywords.includes(term)) {
        termScore += 15;
      }
      if (haystacks.tags.includes(term)) termScore += 15;
      if (haystacks.description.includes(term)) termScore += 5;

      if (termScore > 0) matchedTerms += 1;
      score += termScore;
    }

    // Covering more of the query outranks matching one term loudly. Without
    // this, "rounded corners" puts a font feature whose title contains
    // "ui-rounded" above border-radius, which matches both words.
    score += matchedTerms * 100;

    if (matchedTerms > 0) scored.push({ feature, score });
  }

  scored.sort((a, b) => b.score - a.score || a.feature.slug.localeCompare(b.feature.slug));

  return {
    query,
    match_count: scored.length,
    results: scored.slice(0, limit).map(({ feature }) => ({
      slug: feature.slug,
      title: feature.title,
      category: feature.category,
      description: feature.description,
      url: feature.url,
      last_test_date: feature.last_test_date,
    })),
    data_source: dataset.meta,
  };
}

/* -------------------------------------------------------------------------- */
/* Tool: lint_email                                                            */
/* -------------------------------------------------------------------------- */

/**
 * Lint an email's HTML and/or CSS against a set of clients.
 *
 * Returns only problems — never the passing features — so the result stays
 * small enough to hand back to an agent mid-draft.
 *
 * A feature that fails differently in different clients produces one finding
 * per verdict, so most features emit two or three. What the `features` legend
 * fixes is that half of each finding did not vary between them: the title, the
 * URL, the last test date, and — the one worth naming — the source positions,
 * which are a fact about where the markup uses the feature and have nothing to
 * do with any client's verdict at all. Repeating them per verdict both cost a
 * seventh of the payload and invited the reading that two findings for one
 * feature point at two different places in the document.
 *
 * @param {Dataset} dataset
 * @param {object} options
 * @param {string} [options.html]
 * @param {string} [options.css]
 * @param {string[]} options.clients
 * @param {boolean} [options.includeUntested] Report untested features too (default true).
 */
export function lintEmail(dataset, options) {
  const { html, css, clients: clientGlobs, includeUntested = true } = options ?? {};
  if (!html && !css) throw new Error('Provide html, css, or both.');

  const clients = expandClients(dataset, clientGlobs);
  const summariseClients = clientSummariser(clients);
  const detected = detectFeatures(dataset, { html, css });

  const findings = [];
  /**
   * @type {Record<string, {title: string, url: string|undefined, positions: string[],
   *   occurrence_count: number, last_test_date: string|undefined}>}
   */
  const features = {};
  for (const { title, positions, occurrence_count: occurrences } of detected.values()) {
    const feature = dataset.byTitle.get(title);
    if (!feature) continue; // Detected something the dataset no longer describes.

    // Notes accumulate per verdict bucket, never across the whole feature.
    // Sharing one note set between buckets leaks a note describing partial
    // support in one client onto another client's hard failure — `css-gap` is
    // unsupported in Outlook, and Gmail's "Partial. Supports column-gap"
    // annotation must not travel with the Outlook error.
    /** @type {Record<ProblemVerdict, {clients: string[], notes: Set<string>}>} */
    const buckets = {
      [UNSUPPORTED]: { clients: [], notes: new Set() },
      [MITIGATED]: { clients: [], notes: new Set() },
      [UNTESTED]: { clients: [], notes: new Set() },
    };

    for (const client of clients) {
      const resolved = resolveSupport(feature, client);
      if (resolved.verdict === SUPPORTED) continue;
      const bucket = buckets[resolved.verdict];
      bucket.clients.push(client);
      for (const note of resolved.notes) bucket.notes.add(note);
    }

    for (const verdict of /** @type {ProblemVerdict[]} */ (Object.keys(buckets))) {
      const bucket = buckets[verdict];
      const affected = bucket.clients;
      if (affected.length === 0) continue;
      if (verdict === UNTESTED && !includeUntested) continue;

      // Written here rather than at the top of the loop so the legend describes
      // the findings that were actually emitted. A feature whose only problem is
      // untested, under `includeUntested: false`, produces nothing and belongs
      // in neither list.
      features[feature.slug] ??= {
        title: feature.title,
        url: feature.url,
        positions,
        occurrence_count: occurrences,
        last_test_date: feature.last_test_date,
      };

      findings.push({
        feature: feature.slug,
        severity: SEVERITY_BY_VERDICT[verdict],
        verdict,
        clients_affected: summariseClients(affected),
        client_count: affected.length,
        notes: verdict === UNTESTED ? [] : [...bucket.notes],
        // Stays on the finding, unlike everything else that does not vary by
        // verdict. Its *content* is feature-level, but it is suppressed for
        // `untested` — an untested verdict has no findings to report, and a
        // remark describing partial support elsewhere must not read as one. In
        // the legend it would be visible from an untested finding again, which
        // is the thing being prevented.
        feature_notes: verdict === UNTESTED ? null : featureNotes(feature),
      });
    }
  }

  // Hard failures first, then breadth of impact — an agent reading top-down
  // fixes the most damaging thing first.
  const rank = (/** @type {Severity} */ severity) => SEVERITIES.indexOf(severity);
  findings.sort((a, b) => rank(a.severity) - rank(b.severity) || b.client_count - a.client_count);

  const counts = countBy(
    SEVERITIES,
    findings.map((finding) => finding.severity),
  );

  return {
    clients_checked: clients,
    findings,
    // Everything about a detected feature that no verdict changes, stated once
    // and keyed by the slug each finding carries. Look a finding's `feature` up
    // here for its title, its documentation URL, where in the source it was
    // seen, and how stale the data behind it is.
    features,
    summary: { ...counts, total: findings.length },
    passed: counts.error === 0,
    // A legend, not per-finding text. These are three constant strings, and a
    // lint of a realistic newsletter against every client returns 78 findings —
    // repeating them there cost a tenth of the payload to say the same thing 78
    // times. Look the finding's `verdict` up here.
    guidance: { ...GUIDANCE_BY_VERDICT },
    data_source: dataset.meta,
  };
}

/**
 * Compress a client list against the set that was actually checked.
 *
 * `["*"]` when every checked client is affected, and `"<family>.*"` when every
 * checked member of a family is. At 48 clients the written-out lists were a
 * fifth of a lint's payload, most of it the same identifiers repeated once per
 * finding.
 *
 * The globs expand against `clients_checked`, never against the full roster —
 * that is what makes this lossless rather than an approximation. `client_count`
 * is the exact number either way, so nothing has to expand them to count.
 *
 * A set with a single checked member is named outright, at both levels: `*` and
 * `gmail.*` are shorter than the identifier they replace, but a wildcard reads
 * as a claim about a group when only one of its members was ever looked at.
 *
 * Expect less from the per-family case than it looks like it should give. Real
 * affected sets are usually *partial* within a family — a feature unsupported in
 * three of seven Outlook clients rolls up to nothing — so on a realistic lint it
 * is the `["*"]` case that does most of the work.
 *
 * Built once per lint, because the checked set is: the per-family counts it
 * compresses against are the same for every finding.
 *
 * @param {string[]} checked
 * @returns {(affected: string[]) => string[]}
 */
function clientSummariser(checked) {
  /** @type {Map<string, number>} */
  const checkedPerFamily = new Map();
  for (const client of checked) {
    const family = client.split('.')[0];
    checkedPerFamily.set(family, (checkedPerFamily.get(family) ?? 0) + 1);
  }
  return (affected) => summariseClients(affected, checked.length, checkedPerFamily);
}

/**
 * @param {string[]} affected
 * @param {number} checkedCount
 * @param {Map<string, number>} checkedPerFamily
 */
function summariseClients(affected, checkedCount, checkedPerFamily) {
  if (checkedCount > 1 && affected.length === checkedCount) return ['*'];

  /** @type {Map<string, string[]>} */
  const affectedPerFamily = new Map();
  for (const client of affected) {
    const family = client.split('.')[0];
    const members = affectedPerFamily.get(family) ?? [];
    members.push(client);
    affectedPerFamily.set(family, members);
  }

  const out = [];
  for (const [family, members] of affectedPerFamily) {
    if (members.length > 1 && members.length === checkedPerFamily.get(family)) {
      out.push(`${family}.*`);
    } else {
      out.push(...members);
    }
  }
  return out.sort();
}

/** Every severity, most damaging first, which is the order findings sort in. */
const SEVERITIES = /** @type {const} */ (['error', 'warning', 'unknown']);

/** @typedef {(typeof SEVERITIES)[number]} Severity */

/** @type {Record<ProblemVerdict, Severity>} */
const SEVERITY_BY_VERDICT = {
  [UNSUPPORTED]: 'error',
  [MITIGATED]: 'warning',
  [UNTESTED]: 'unknown',
};

/** @type {Record<ProblemVerdict, string>} */
const GUIDANCE_BY_VERDICT = {
  [UNSUPPORTED]: 'Not supported. This will not render as intended; use a fallback.',
  [MITIGATED]:
    'Partial or conditional support. Read the notes — usually workable with a documented workaround.',
  [UNTESTED]:
    'Never tested on these clients. Not evidence of support either way; avoid, or test it yourself.',
};

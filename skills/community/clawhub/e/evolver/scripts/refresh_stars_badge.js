// refresh_stars_badge.js -- Refresh the static "Stars" badge count in the
// public README sources to the live GitHub star count.
//
// Why this exists:
//   The README stars badge is intentionally STATIC (a plain shields `badge/`
//   URL, not a dynamic `github/stars` one) so it never renders shields.io's
//   "Unable to select next GitHub token from pool" error when their shared
//   GitHub token pool is rate-limited. The trade-off is that the number goes
//   stale. This script re-stamps it at release time so the badge stays current
//   without ever depending on the GitHub API to *render*.
//
// Usage:
//   node scripts/refresh_stars_badge.js                 # update in place
//   node scripts/refresh_stars_badge.js --dry-run       # print, write nothing
//   node scripts/refresh_stars_badge.js --repo=O/N      # override repo
//   node scripts/refresh_stars_badge.js --count=12345   # skip fetch (testing)
//
// Design notes:
//   - Counts come from the PUBLIC repo (default EvoMap/evolver), not this
//     private dev repo.
//   - Fetch uses the already-authenticated `gh` CLI first (deploy.sh preflight
//     guarantees gh auth), falling back to the unauthenticated GitHub REST API.
//   - A fetch failure is NON-FATAL: we warn and exit 0, leaving the badge as
//     is. A flaky GitHub API must never break a release -- avoiding exactly
//     that fragility is the whole reason the badge is static.
//   - It rewrites every README*.md in the repo root that contains the badge,
//     so new translations are picked up automatically.

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const DEFAULT_REPO = 'EvoMap/evolver';

// Matches the value segment of `.../badge/Stars-<value>-<color>...` in a
// shields static badge URL. The value never contains `-` or `/`. Returns a
// fresh regex each call so callers never share `lastIndex` state.
const starsBadgeRe = () => /(img\.shields\.io\/badge\/Stars-)([^-/)]+)(-)/g;

// Replace the Stars badge value in `content` with `value`. Pure; returns the
// rewritten string (unchanged if there is no badge or it already matches).
function rewriteStarsValue(content, value) {
  return content.replace(starsBadgeRe(), (_m, pre, _old, post) => `${pre}${value}${post}`);
}

function parseArgs(argv) {
  const opts = { dryRun: false, repo: DEFAULT_REPO, count: null };
  for (const arg of argv) {
    if (arg === '--dry-run' || arg === '-n') opts.dryRun = true;
    else if (arg.startsWith('--repo=')) opts.repo = arg.slice('--repo='.length);
    else if (arg.startsWith('--count=')) opts.count = Number(arg.slice('--count='.length));
  }
  return opts;
}

// Format an integer the way shields.io's `metric` text formatter does, so the
// static badge is visually indistinguishable from a dynamic one:
//   8336 -> "8.3k", 12345 -> "12k", 1100 -> "1.1k", 999 -> "999".
function metric(n) {
  n = Number(n);
  if (!Number.isFinite(n) || n < 0) return String(n);
  for (const [suffix, size] of [['G', 1e9], ['M', 1e6], ['k', 1e3]]) {
    if (n >= size) {
      const value = n / size;
      const text = value < 10
        ? value.toFixed(1).replace(/\.0$/, '')
        : String(Math.round(value));
      return text + suffix;
    }
  }
  return String(Math.round(n));
}

function fetchStarsViaGh(repo) {
  try {
    const out = execSync(`gh api repos/${repo} --jq .stargazers_count`, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    const n = Number(out);
    return Number.isFinite(n) && n > 0 ? n : null;
  } catch {
    return null;
  }
}

function fetchStarsViaApi(repo) {
  return new Promise((resolve) => {
    const req = https.get(
      `https://api.github.com/repos/${repo}`,
      { headers: { 'User-Agent': 'evolver-refresh-stars-badge', Accept: 'application/vnd.github+json' } },
      (res) => {
        if (res.statusCode !== 200) { res.resume(); return resolve(null); }
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => {
          try {
            const n = Number(JSON.parse(body).stargazers_count);
            resolve(Number.isFinite(n) && n > 0 ? n : null);
          } catch { resolve(null); }
        });
      },
    );
    req.on('error', () => resolve(null));
    req.setTimeout(10000, () => { req.destroy(); resolve(null); });
  });
}

async function resolveStarCount(opts) {
  if (Number.isFinite(opts.count) && opts.count > 0) return opts.count;
  return fetchStarsViaGh(opts.repo) || (await fetchStarsViaApi(opts.repo));
}

function readmeFilesWithBadge() {
  return fs
    .readdirSync(REPO_ROOT)
    .filter((f) => /^README.*\.md$/.test(f))
    .map((f) => path.join(REPO_ROOT, f))
    .filter((p) => starsBadgeRe().test(fs.readFileSync(p, 'utf8')));
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));

  const count = await resolveStarCount(opts);
  if (count == null) {
    console.warn('[refresh-stars-badge] could not resolve star count (gh + API both failed); leaving badge unchanged');
    return; // non-fatal
  }
  const value = metric(count);
  console.log(`[refresh-stars-badge] ${opts.repo} = ${count} stars -> "${value}"`);

  const files = readmeFilesWithBadge();
  if (files.length === 0) {
    console.warn('[refresh-stars-badge] no README*.md with a Stars badge found; nothing to do');
    return;
  }

  let changed = 0;
  for (const file of files) {
    const before = fs.readFileSync(file, 'utf8');
    const after = rewriteStarsValue(before, value);
    const rel = path.relative(REPO_ROOT, file);
    if (after === before) {
      console.log(`  ${rel}: already "${value}"`);
      continue;
    }
    if (opts.dryRun) {
      console.log(`  [dry-run] ${rel}: would set Stars -> "${value}"`);
    } else {
      fs.writeFileSync(file, after);
      console.log(`  ${rel}: Stars -> "${value}"`);
    }
    changed++;
  }
  console.log(`[refresh-stars-badge] ${changed} file(s) ${opts.dryRun ? 'would change' : 'updated'}`);
}

if (require.main === module) {
  main().catch((e) => {
    // Never fail the release over a badge refresh.
    console.warn(`[refresh-stars-badge] unexpected error (ignored): ${e && e.message}`);
  });
}

module.exports = { metric, rewriteStarsValue };

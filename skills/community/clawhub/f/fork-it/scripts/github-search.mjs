#!/usr/bin/env node
/**
 * fork-it - GitHub Repository Search Tool
 * Returns structured JSON (language-neutral; the AI presents results in the user's language).
 *
 * Uses Node's built-in fetch (no curl / shell dependency, no command injection).
 */

const GITHUB_API = 'https://api.github.com/search/repositories';

// Parse CLI arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    query: '',
    language: null,
    minStars: 0,
    maxStars: null,
    updatedWithin: 0,
    createdAfter: null,
    sort: 'stars',
    order: 'desc',
    limit: 10
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) {
      options.query = arg;
    } else if (arg === '--language' || arg === '-l') {
      options.language = args[++i];
    } else if (arg === '--min-stars') {
      options.minStars = parseInt(args[++i]);
    } else if (arg === '--max-stars') {
      options.maxStars = parseInt(args[++i]);
    } else if (arg === '--updated-within') {
      options.updatedWithin = parseInt(args[++i]);
    } else if (arg === '--created-after') {
      options.createdAfter = args[++i];
    } else if (arg === '--sort') {
      options.sort = args[++i];
    } else if (arg === '--order') {
      options.order = args[++i];
    } else if (arg === '--limit' || arg === '-n') {
      options.limit = parseInt(args[++i]);
    }
  }
  return options;
}

// Build GitHub search query
function buildQuery(options) {
  let query = options.query;
  if (options.language) query += ` language:${options.language}`;
  if (options.minStars) query += ` stars:>=${options.minStars}`;
  if (options.maxStars) query += ` stars:<=${options.maxStars}`;
  if (options.updatedWithin) {
    const date = new Date();
    date.setDate(date.getDate() - options.updatedWithin);
    query += ` pushed:>=${date.toISOString().split('T')[0]}`;
  }
  if (options.createdAfter) query += ` created:>=${options.createdAfter}`;
  return query;
}

// Call GitHub Search API via fetch (no shell, no injection)
async function searchGitHub(query, sort, order, perPage = 30) {
  const url = `${GITHUB_API}?q=${encodeURIComponent(query)}&sort=${sort}&order=${order}&per_page=${perPage}`;
  const headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'fork-it-skill',
    'X-GitHub-Api-Version': '2022-11-28'
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  let res;
  try {
    res = await fetch(url, { headers });
  } catch (err) {
    return { error: `Network error: ${err.message}`, code: 'NETWORK_ERROR' };
  }

  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const message = data?.message || `GitHub API returned HTTP ${res.status}`;
    return { error: message, code: `HTTP_${res.status}` };
  }
  if (!data || !Array.isArray(data.items)) {
    return { error: data?.message || 'Unexpected response from GitHub API', code: 'NO_ITEMS' };
  }
  return data;
}

// Return days diff (neutral, no language)
function getDaysDiff(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  if (isNaN(d)) return null;
  return Math.floor((Date.now() - d) / (1000 * 60 * 60 * 24));
}

// Normalize repo to neutral structure
function normalizeRepo(repo, index) {
  return {
    rank: index + 1,
    full_name: repo.full_name,
    description: repo.description || null,
    url: repo.html_url,
    stars: repo.stargazers_count,
    forks: repo.forks_count,
    language: repo.language || null,
    pushed_days_ago: getDaysDiff(repo.pushed_at),
    created_at: repo.created_at,
    topics: repo.topics || [],
    license: repo.license?.name || null
  };
}

function fail(code, message) {
  console.log(JSON.stringify({ status: 'error', code, message }));
  process.exit(1);
}

// Main
async function main() {
  const options = parseArgs();

  if (!options.query) {
    fail('MISSING_QUERY',
      'Usage: node github-search.mjs <query> [--language js] [--min-stars N] [--limit 10] [--updated-within N]');
  }

  const query = buildQuery(options);
  const data = await searchGitHub(query, options.sort, options.order, Math.min(options.limit, 100));

  if (data.error) {
    fail(data.code || 'API_ERROR', data.error);
  }

  const repos = data.items.slice(0, options.limit).map(normalizeRepo);

  console.log(JSON.stringify({
    status: 'ok',
    query: options.query,
    total_count: data.total_count,
    returned_count: repos.length,
    query_string: query,
    items: repos
  }, null, 2));
}

main().catch(err => {
  fail('UNKNOWN', err.message);
});

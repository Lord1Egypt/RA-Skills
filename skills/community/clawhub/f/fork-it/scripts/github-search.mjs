#!/usr/bin/env node
/**
 * No Reinvent Wheel - GitHub Repository Search Tool
 * Returns structured JSON with language tag for i18n.
 */

import { execSync } from 'child_process';

const GITHUB_API = 'https://api.github.com/search/repositories';

// Parse CLI arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    query: '',
    language: null,
    minStars: 100,
    maxStars: null,
    updatedWithin: 365,
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

// Call GitHub API via curl
async function searchGitHub(query, sort, order, perPage = 30) {
  const url = `${GITHUB_API}?q=${encodeURIComponent(query)}&sort=${sort}&order=${order}&per_page=${perPage}`;
  const headers = [
    '-H "Accept: application/vnd.github.v3+json"',
    '-H "User-Agent: ForkIt-Skill"'
  ];
  if (process.env.GITHUB_TOKEN) {
    headers.push(`-H "Authorization: token ${process.env.GITHUB_TOKEN}"`);
  }
  const cmd = `curl -s ${headers.join(' ')} "${url}"`;
  try {
    return JSON.parse(execSync(cmd, { encoding: 'utf-8', timeout: 30000 }));
  } catch (error) {
    return null;
  }
}

// Return days diff (neutral, no language)
function getDaysDiff(dateStr) {
  if (!dateStr) return null;
  return Math.floor((Date.now() - new Date(dateStr)) / (1000 * 60 * 60 * 24));
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

// Main
async function main() {
  const options = parseArgs();

  if (!options.query) {
    // Usage in JSON
    console.log(JSON.stringify({
      lang: 'en',
      status: 'error',
      code: 'MISSING_QUERY',
      message: 'Usage: node github-search.mjs <query> [--language js] [--min-stars 100] [--limit 10] [--updated-within 365]'
    }));
    process.exit(1);
  }

  const query = buildQuery(options);
  const data = await searchGitHub(query, options.sort, options.order, Math.min(options.limit, 100));

  if (!data || !data.items) {
    console.log(JSON.stringify({
      lang: 'en',
      status: 'error',
      code: 'API_ERROR',
      message: 'GitHub API request failed or no results found'
    }));
    process.exit(1);
  }

  const repos = data.items.slice(0, options.limit).map(normalizeRepo);

  console.log(JSON.stringify({
    lang: 'en',
    status: 'ok',
    query: options.query,
    total_count: data.total_count,
    returned_count: repos.length,
    query_string: query,
    items: repos
  }, null, 2));
}

main().catch(err => {
  console.log(JSON.stringify({
    lang: 'en',
    status: 'error',
    code: 'UNKNOWN',
    message: err.message
  }));
  process.exit(1);
});

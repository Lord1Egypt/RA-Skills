#!/usr/bin/env node
/**
 * fork-it - GitHub Repository Detail Fetcher
 * Returns structured JSON (language-neutral; the AI presents results in the user's language).
 *
 * Uses Node's built-in fetch (no curl / shell dependency, no command injection).
 */

const GITHUB_API = 'https://api.github.com/repos';

function parseArgs() {
  const args = process.argv.slice(2);
  return args.find(a => !a.startsWith('--')) || null;
}

async function apiGet(path) {
  const url = `${GITHUB_API}${path}`;
  const headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'fork-it-skill',
    'X-GitHub-Api-Version': '2022-11-28'
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  const res = await fetch(url, { headers });
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const err = new Error(data?.message || `GitHub API returned HTTP ${res.status}`);
    err.code = `HTTP_${res.status}`;
    throw err;
  }
  return data;
}

// Normalize to neutral structure
function normalizeRepo(repo) {
  const pushedDaysAgo = repo.pushed_at
    ? Math.floor((Date.now() - new Date(repo.pushed_at)) / (1000 * 60 * 60 * 24))
    : null;
  return {
    full_name: repo.full_name,
    name: repo.name,
    description: repo.description || null,
    url: repo.html_url,
    homepage: repo.homepage || null,
    stars: repo.stargazers_count,
    forks: repo.forks_count,
    watchers: repo.watchers_count,
    open_issues: repo.open_issues_count,
    language: repo.language || null,
    license: repo.license?.name || null,
    default_branch: repo.default_branch,
    size_mb: Math.round(repo.size / 1024),
    pushed_days_ago: pushedDaysAgo,
    created_at: repo.created_at,
    updated_at: repo.updated_at,
    topics: repo.topics || [],
    owner: {
      login: repo.owner.login,
      avatar_url: repo.owner.avatar_url,
      url: repo.owner.html_url
    }
  };
}

function normalizeContributors(contributors) {
  return (contributors || []).slice(0, 10).map(c => ({
    login: c.login,
    url: c.html_url,
    contributions: c.contributions
  }));
}

// Reuse recommendation based on neutral criteria
function getReuseAdvice(stars, pushedDaysAgo) {
  return {
    level: (() => {
      if (stars >= 10000 && pushedDaysAgo !== null && pushedDaysAgo <= 30) return 'strong_recommend';
      if (stars >= 1000 && pushedDaysAgo !== null && pushedDaysAgo <= 90) return 'recommend';
      if (stars >= 100) return 'reference';
      return 'build_own';
    })(),
    stars_threshold: stars >= 10000 ? '>=10k' : stars >= 1000 ? '>=1k' : stars >= 100 ? '>=100' : '<100',
    activity_days: pushedDaysAgo
  };
}

function fail(code, message) {
  console.log(JSON.stringify({ status: 'error', code, message }));
  process.exit(1);
}

async function main() {
  const repoFullName = parseArgs();

  if (!repoFullName) {
    fail('MISSING_ARG', 'Usage: node repo-detail.mjs <owner/repo>');
  }

  const parts = repoFullName.split('/');
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    fail('INVALID_FORMAT', 'Invalid format. Use: owner/repo');
  }

  try {
    const repoData = await apiGet(`/${repoFullName}`);
    const contributors = await apiGet(`/${repoFullName}/contributors?per_page=10`).catch(() => null);
    const pushedDaysAgo = repoData.pushed_at
      ? Math.floor((Date.now() - new Date(repoData.pushed_at)) / (1000 * 60 * 60 * 24))
      : null;
    const advice = getReuseAdvice(repoData.stargazers_count, pushedDaysAgo);

    console.log(JSON.stringify({
      status: 'ok',
      repo: normalizeRepo(repoData),
      contributors: normalizeContributors(contributors),
      reuse_advice: advice
    }, null, 2));
  } catch (err) {
    const code = err.code === 'HTTP_404' ? 'NOT_FOUND' : (err.code || 'UNKNOWN');
    fail(code, err.message);
  }
}

main().catch(err => {
  fail('UNKNOWN', err.message);
});

#!/usr/bin/env node
/**
 * No Reinvent Wheel - GitHub Repository Detail Fetcher
 * Returns structured JSON with language tag for i18n.
 */

import { execSync } from 'child_process';

const GITHUB_API = 'https://api.github.com/repos';

function parseArgs() {
  const args = process.argv.slice(2);
  return args[0] || null;
}

async function apiGet(path) {
  const url = `${GITHUB_API}${path}`;
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

// Normalize to neutral structure
function normalizeRepo(repo) {
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
    pushed_days_ago: Math.floor((Date.now() - new Date(repo.pushed_at)) / (1000 * 60 * 60 * 24)),
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
      if (stars >= 10000 && pushedDaysAgo <= 30) return 'strong_recommend';
      if (stars >= 1000 && pushedDaysAgo <= 90) return 'recommend';
      if (stars >= 100) return 'reference';
      return 'build_own';
    })(),
    stars_threshold: stars >= 10000 ? '>=10k' : stars >= 1000 ? '>=1k' : stars >= 100 ? '>=100' : '<100',
    activity_days: pushedDaysAgo
  };
}

async function main() {
  const repoFullName = parseArgs();

  if (!repoFullName) {
    console.log(JSON.stringify({
      lang: 'en',
      status: 'error',
      code: 'MISSING_ARG',
      message: 'Usage: node repo-detail.mjs <owner/repo>'
    }));
    process.exit(1);
  }

  const parts = repoFullName.split('/');
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    console.log(JSON.stringify({
      lang: 'en',
      status: 'error',
      code: 'INVALID_FORMAT',
      message: 'Invalid format. Use: owner/repo'
    }));
    process.exit(1);
  }

  const repoData = await apiGet(`/${repoFullName}`);
  if (!repoData || repoData.message === 'Not Found') {
    console.log(JSON.stringify({
      lang: 'en',
      status: 'error',
      code: 'NOT_FOUND',
      message: 'Repository not found or inaccessible'
    }));
    process.exit(1);
  }

  const contributors = await apiGet(`/${repoFullName}/contributors?per_page=10`);
  const advice = getReuseAdvice(repoData.stargazers_count, Math.floor((Date.now() - new Date(repoData.pushed_at)) / (1000 * 60 * 60 * 24)));

  console.log(JSON.stringify({
    lang: 'en',
    status: 'ok',
    repo: normalizeRepo(repoData),
    contributors: normalizeContributors(contributors),
    reuse_advice: advice
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

import { mkdir, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const skillDir = join(__dirname, "..");
const today = new Date().toISOString().slice(0, 10);
const outputDir = join(skillDir, "data", today);

function sha256(text) {
  return createHash("sha256").update(text).digest("hex");
}

async function fetchText(name, url, init = {}) {
  const startedAt = new Date().toISOString();
  const response = await fetch(url, {
    ...init,
    headers: {
      "accept": init.headers?.accept ?? "text/plain, application/json;q=0.9, */*;q=0.1",
      "user-agent": "codex-earn-money-openclaw-ecosystem-monitor/0.1",
      ...init.headers,
    },
  });
  const text = await response.text();
  return {
    name,
    url,
    status: response.status,
    ok: response.ok,
    collected_at: startedAt,
    content_type: response.headers.get("content-type"),
    rate_limit_remaining: response.headers.get("x-ratelimit-remaining"),
    rate_limit_reset: response.headers.get("x-ratelimit-reset"),
    hash: sha256(text),
    text,
  };
}

async function fetchJson(name, url, init = {}) {
  const result = await fetchText(name, url, {
    ...init,
    headers: { accept: "application/json", ...init.headers },
  });
  try {
    return { ...result, json: JSON.parse(result.text), text: undefined };
  } catch (error) {
    return {
      ...result,
      parse_error: error instanceof Error ? error.message : String(error),
      text: undefined,
    };
  }
}

function summarizeGitHubRepo(repo) {
  if (!repo || typeof repo !== "object") return null;
  return {
    name: repo.full_name,
    html_url: repo.html_url,
    description: repo.description,
    stars: repo.stargazers_count,
    forks: repo.forks_count,
    open_issues: repo.open_issues_count,
    default_branch: repo.default_branch,
    pushed_at: repo.pushed_at,
    updated_at: repo.updated_at,
    license: repo.license?.spdx_id ?? null,
  };
}

function summarizeIssues(searchResult) {
  const items = Array.isArray(searchResult?.items) ? searchResult.items : [];
  return items.slice(0, 10).map((issue) => ({
    title: issue.title,
    html_url: issue.html_url,
    state: issue.state,
    labels: Array.isArray(issue.labels) ? issue.labels.map((label) => label.name) : [],
    created_at: issue.created_at,
    updated_at: issue.updated_at,
    comments: issue.comments,
  }));
}

function summarizeIssueList(issues) {
  if (!Array.isArray(issues)) return [];
  return issues.slice(0, 10).map((issue) => ({
    title: issue.title,
    html_url: issue.html_url,
    state: issue.state,
    labels: Array.isArray(issue.labels) ? issue.labels.map((label) => label.name) : [],
    created_at: issue.created_at,
    updated_at: issue.updated_at,
    comments: issue.comments,
    pull_request: Boolean(issue.pull_request),
  }));
}

function summarizeContentFile(file) {
  if (!file || typeof file !== "object" || !file.path) return null;
  return {
    path: file.path,
    html_url: file.html_url,
    sha: file.sha,
    size: file.size,
    type: file.type,
  };
}

function summarizeNpmPackages(searchResult) {
  const objects = Array.isArray(searchResult?.objects) ? searchResult.objects : [];
  return objects.slice(0, 10).map((entry) => ({
    name: entry.package?.name,
    version: entry.package?.version,
    description: entry.package?.description,
    date: entry.package?.date,
    license: entry.package?.license,
    publisher: entry.package?.publisher?.username,
    maintainer_count: Array.isArray(entry.package?.maintainers) ? entry.package.maintainers.length : null,
    links: entry.package?.links,
    downloads_weekly: entry.downloads?.weekly,
    downloads_monthly: entry.downloads?.monthly,
  }));
}

function summarizeSitemap(text) {
  const urls = Array.from(text.matchAll(/<loc>([^<]+)<\/loc>/g)).map((match) => match[1]);
  return {
    url_count: urls.length,
    sample_urls: urls.slice(0, 20),
  };
}

function classifyWarnings(results) {
  const warnings = [];
  const hardWarnings = [];
  for (const result of results) {
    if (result.status === 403 || result.status === 429) {
      const warning = `${result.name}: pause trigger HTTP ${result.status}`;
      warnings.push(warning);
      hardWarnings.push(warning);
    } else if (result.status === 401 || result.status === 404) {
      const warning = `${result.name}: hard source-quality warning HTTP ${result.status}`;
      warnings.push(warning);
      hardWarnings.push(warning);
    } else if (!result.ok && result.status >= 500) {
      warnings.push(`${result.name}: transient upstream warning HTTP ${result.status}`);
    } else if (!result.ok) {
      const warning = `${result.name}: non-ok HTTP ${result.status}`;
      warnings.push(warning);
      hardWarnings.push(warning);
    }
  }
  return { warnings, hardWarnings };
}

async function main() {
  await mkdir(outputDir, { recursive: true });

  const githubRepo = await fetchJson("github_repo_openclaw", "https://api.github.com/repos/openclaw/openclaw");
  const githubIssues = await fetchJson(
    "github_issues_openclaw_good_first",
    "https://api.github.com/search/issues?q=repo%3Aopenclaw%2Fopenclaw+is%3Aissue+state%3Aopen+label%3A%22good+first+issue%22&per_page=10"
  );
  const githubDocIssues = await fetchJson(
    "github_issues_openclaw_documentation_query",
    "https://api.github.com/search/issues?q=repo%3Aopenclaw%2Fopenclaw+is%3Aissue+state%3Aopen+documentation&per_page=10"
  );
  const githubRecentIssues = await fetchJson(
    "github_issues_openclaw_recent",
    "https://api.github.com/repos/openclaw/openclaw/issues?state=open&per_page=10"
  );
  const githubContributing = await fetchJson(
    "github_contributing_openclaw",
    "https://api.github.com/repos/openclaw/openclaw/contents/CONTRIBUTING.md"
  );
  const npmSearch = await fetchJson("npm_search_openclaw", "https://registry.npmjs.org/-/v1/search?text=openclaw&size=10");
  const docsSitemap = await fetchText("openclaw_docs_sitemap", "https://docs.openclaw.ai/sitemap.xml");
  const clawhubRobots = await fetchText("clawhub_robots", "https://clawhub.ai/robots.txt");
  const docsRobots = await fetchText("openclaw_docs_robots", "https://docs.openclaw.ai/robots.txt");

  const rawResults = [
    githubRepo,
    githubIssues,
    githubDocIssues,
    githubRecentIssues,
    githubContributing,
    npmSearch,
    docsSitemap,
    clawhubRobots,
    docsRobots,
  ];

  const warningResult = classifyWarnings(rawResults);

  const snapshot = {
    collected_at: new Date().toISOString(),
    source_policy: {
      storage: "metadata, short summary, hash, timestamp, source_url only",
      redistribution: "link to canonical source; do not mirror full source content",
    },
    records: {
      github_repo_openclaw: summarizeGitHubRepo(githubRepo.json),
      github_issues_openclaw_good_first: summarizeIssues(githubIssues.json),
      github_issues_openclaw_documentation_query: summarizeIssues(githubDocIssues.json),
      github_issues_openclaw_recent: summarizeIssueList(githubRecentIssues.json),
      github_contributing_openclaw: summarizeContentFile(githubContributing.json),
      npm_search_openclaw: summarizeNpmPackages(npmSearch.json),
      openclaw_docs_sitemap: {
        url: docsSitemap.url,
        status: docsSitemap.status,
        hash: docsSitemap.hash,
        ...summarizeSitemap(docsSitemap.text),
      },
      clawhub_robots: {
        url: clawhubRobots.url,
        status: clawhubRobots.status,
        hash: clawhubRobots.hash,
        text_excerpt: clawhubRobots.text.slice(0, 200),
      },
      openclaw_docs_robots: {
        url: docsRobots.url,
        status: docsRobots.status,
        hash: docsRobots.hash,
        text_excerpt: docsRobots.text.slice(0, 200),
      },
    },
    request_status: rawResults.map(({ name, url, status, ok, content_type, rate_limit_remaining, rate_limit_reset, hash }) => ({
      name,
      url,
      status,
      ok,
      content_type,
      rate_limit_remaining,
      rate_limit_reset,
      hash,
    })),
    warnings: warningResult.warnings,
    hard_warnings: warningResult.hardWarnings,
  };

  const outputPath = join(outputDir, "openclaw-ecosystem-snapshot.json");
  await writeFile(outputPath, JSON.stringify(snapshot, null, 2) + "\n", "utf8");
  console.log(outputPath);
  if (snapshot.hard_warnings.length > 0) {
    console.error(snapshot.hard_warnings.join("\n"));
    process.exitCode = 2;
  } else if (snapshot.warnings.length > 0) {
    console.warn(snapshot.warnings.join("\n"));
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack : String(error));
  process.exitCode = 1;
});

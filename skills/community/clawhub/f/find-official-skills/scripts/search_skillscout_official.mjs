#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REMOTE_DIRECTORY_URL = "https://skillscout.sh/data/official-skills-universal.json";
const DEFAULT_LIMIT = 5;
const MAX_LIMIT = 1000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = parseArgs(process.argv.slice(2));

if (!args.query && !args.owner && !args.domain) {
  printUsage();
  process.exit(1);
}

const directory = await loadDirectory(args);
const index = buildSearchIndex(directory);
const results = args.all ? listAllMatchingSkills(directory, args) : search(index, args);

if (args.json) {
  console.log(JSON.stringify({
    query: args.query,
    owner: args.owner,
    domain: args.domain,
    mode: args.all ? "all" : "search",
    dataSource: directory.__skillscoutSource || {},
    generatedAt: directory.generatedAt || directory.enrichedAt || "",
    stats: directory.stats || {},
    results
  }, null, 2));
} else {
  printResults(results, directory, args);
}

function parseArgs(rawArgs) {
  const parsed = {
    queryParts: [],
    owner: "",
    domain: "",
    limit: DEFAULT_LIMIT,
    dataPath: process.env.SKILLSCOUT_OFFICIAL_DATA || "",
    json: false,
    source: "auto",
    all: false
  };

  for (let index = 0; index < rawArgs.length; index += 1) {
    const arg = rawArgs[index];
    if (arg === "--owner") {
      parsed.owner = rawArgs[++index] || "";
    } else if (arg === "--domain") {
      parsed.domain = rawArgs[++index] || "";
    } else if (arg === "--limit") {
      parsed.limit = clampLimit(rawArgs[++index]);
    } else if (arg === "--data") {
      parsed.dataPath = rawArgs[++index] || "";
      parsed.source = "file";
    } else if (arg === "--remote") {
      parsed.source = "remote";
    } else if (arg === "--json") {
      parsed.json = true;
    } else if (arg === "--all") {
      parsed.all = true;
    } else if (arg === "--help" || arg === "-h") {
      printUsage();
      process.exit(0);
    } else {
      parsed.queryParts.push(arg);
    }
  }

  parsed.query = parsed.queryParts.join(" ").trim();
  parsed.limit = clampLimit(parsed.limit);
  return parsed;
}

function clampLimit(value) {
  const number = Number(value || DEFAULT_LIMIT);
  if (!Number.isFinite(number) || number < 1) {
    return DEFAULT_LIMIT;
  }
  return Math.min(MAX_LIMIT, Math.round(number));
}

async function loadDirectory(args) {
  if (args.source !== "remote") {
    const candidatePaths = [
      args.dataPath,
      path.resolve(process.cwd(), "docs/data/official-skills-universal.json"),
      path.resolve(__dirname, "../../../docs/data/official-skills-universal.json")
    ].filter(Boolean);

    for (const candidatePath of candidatePaths) {
      try {
        const text = await fs.readFile(candidatePath, "utf8");
        const directory = JSON.parse(text);
        if (!isUniversalDirectory(directory)) {
          continue;
        }
        attachDirectorySource(directory, { type: "file", path: candidatePath });
        return directory;
      } catch {
        // Try the next source.
      }
    }
  }

  const response = await fetch(REMOTE_DIRECTORY_URL, {
    headers: {
      Accept: "application/json",
      "User-Agent": "Skillscout official skills finder"
    }
  });
  if (!response.ok) {
    throw new Error(`Skillscout directory fetch failed: ${response.status}`);
  }
  const directory = await response.json();
  if (!isUniversalDirectory(directory)) {
    throw new Error("Skillscout directory response has an unsupported schema.");
  }
  attachDirectorySource(directory, { type: "remote", url: REMOTE_DIRECTORY_URL });
  return directory;
}

function isUniversalDirectory(directory) {
  return Boolean(
    directory &&
      Array.isArray(directory.officialOwners) &&
      Array.isArray(directory.officialRepos) &&
      Array.isArray(directory.officialSkills)
  );
}

function attachDirectorySource(directory, source) {
  Object.defineProperty(directory, "__skillscoutSource", {
    value: source,
    enumerable: false
  });
}

function buildSearchIndex(directory) {
  const ownersByKey = new Map();
  const reposByKey = new Map();
  const skillsByRepo = new Map();
  const reposByOwner = new Map();
  const skillsByOwner = new Map();

  for (const owner of directory.officialOwners || []) {
    ownersByKey.set(owner.ownerKey, owner);
  }
  for (const repo of directory.officialRepos || []) {
    reposByKey.set(repo.repoKey, repo);
    const ownerRepos = reposByOwner.get(repo.ownerKey) || [];
    ownerRepos.push(repo);
    reposByOwner.set(repo.ownerKey, ownerRepos);
  }
  for (const skill of directory.officialSkills || []) {
    const list = skillsByRepo.get(skill.repoKey) || [];
    list.push(skill);
    skillsByRepo.set(skill.repoKey, list);
    const ownerSkills = skillsByOwner.get(skill.ownerKey) || [];
    ownerSkills.push(skill);
    skillsByOwner.set(skill.ownerKey, ownerSkills);
  }

  const rows = [];

  for (const skill of directory.officialSkills || []) {
    const owner = ownersByKey.get(skill.ownerKey) || {};
    const repo = reposByKey.get(skill.repoKey) || {};
    rows.push(buildSkillRow(skill, repo, owner));
  }

  for (const repo of directory.officialRepos || []) {
    const owner = ownersByKey.get(repo.ownerKey) || {};
    const repoSkills = skillsByRepo.get(repo.repoKey) || [];
    rows.push(buildRepoRow(repo, owner, repoSkills));
  }

  for (const owner of directory.officialOwners || []) {
    const ownerRepos = reposByOwner.get(owner.ownerKey) || [];
    const ownerSkills = skillsByOwner.get(owner.ownerKey) || [];
    rows.push(buildOwnerRow(owner, ownerRepos, ownerSkills));
  }

  return rows;
}

function buildSkillRow(skill, repo, owner) {
  const displayName = skill.displayName || skill.skillName;
  const sourceUrl = preferredUrl(skill.sourceUrls, repo.sourceUrls, owner.sourceUrls);
  return {
    type: "skill",
    ownerKey: skill.ownerKey,
    ownerName: owner.displayName || skill.ownerKey,
    repoKey: skill.repoKey,
    skillName: skill.skillName,
    displayName,
    description: skill.description || "",
    installCommand: skill.repoKey && skill.skillName ? `npx skills add ${skill.repoKey}@${skill.skillName}` : "",
    sourceUrl,
    skillscoutUrl: buildSkillscoutSkillUrl(skill),
    installsCount: Number(skill.installsCount || 0),
    starsCount: Number(repo.starsCount || owner.starsCount || 0),
    confidence: skill.confidence || repo.confidence || owner.confidence || "",
    githubVerified: Boolean(owner.githubVerified),
    website: owner.website || "",
    websiteHosts: owner.websiteHosts || [],
    text: [
      skill.ownerKey,
      owner.displayName,
      ...(owner.normalizedNames || []),
      ...(owner.sourceOwnerKeys || []),
      skill.repoKey,
      repo.displayName,
      skill.skillName,
      skill.displayName,
      skill.description,
      ...(skill.sourceUrls || []),
      owner.website,
      ...(owner.websiteHosts || [])
    ].join(" ")
  };
}

function buildRepoRow(repo, owner, repoSkills) {
  const firstSkill = pickBestSkill(repoSkills);
  return {
    type: "repo",
    ownerKey: repo.ownerKey,
    ownerName: owner.displayName || repo.ownerKey,
    repoKey: repo.repoKey,
    skillName: firstSkill?.skillName || "",
    displayName: repo.displayName || repo.repoKey,
    description: `${repoSkills.length || repo.skillsCount || 0} official skills from ${owner.displayName || repo.ownerKey}`,
    installCommand: firstSkill ? `npx skills add ${repo.repoKey}@${firstSkill.skillName}` : "",
    sourceUrl: preferredUrl(repo.sourceUrls, repo.repoKey ? [`https://github.com/${repo.repoKey}`] : [], owner.sourceUrls),
    skillscoutUrl: `https://skillscout.sh/official/?q=${encodeURIComponent(repo.repoKey)}`,
    installsCount: Number(repo.installsCount || 0),
    starsCount: Number(repo.starsCount || owner.starsCount || 0),
    confidence: repo.confidence || owner.confidence || "",
    githubVerified: Boolean(owner.githubVerified),
    website: owner.website || "",
    websiteHosts: owner.websiteHosts || [],
    text: [
      repo.ownerKey,
      owner.displayName,
      ...(owner.normalizedNames || []),
      ...(owner.sourceOwnerKeys || []),
      repo.repoKey,
      repo.repoName,
      repo.displayName,
      ...(repo.githubSkillPaths || []),
      owner.website,
      ...(owner.websiteHosts || [])
    ].join(" ")
  };
}

function buildOwnerRow(owner, ownerRepos, ownerSkills) {
  const bestRepo = pickBestRepo(ownerRepos);
  const bestSkill = pickBestSkill(ownerSkills.filter((skill) => skill.repoKey === bestRepo?.repoKey)) || pickBestSkill(ownerSkills);
  return {
    type: "owner",
    ownerKey: owner.ownerKey,
    ownerName: owner.displayName || owner.ownerKey,
    repoKey: bestRepo?.repoKey || "",
    skillName: bestSkill?.skillName || "",
    displayName: owner.displayName || owner.ownerKey,
    description: `${ownerSkills.length || owner.skillsCount || 0} official skills across ${ownerRepos.length || owner.reposCount || 0} repos`,
    installCommand: bestSkill?.repoKey && bestSkill?.skillName ? `npx skills add ${bestSkill.repoKey}@${bestSkill.skillName}` : "",
    sourceUrl: preferredUrl(owner.sourceUrls, bestRepo?.sourceUrls, bestSkill?.sourceUrls),
    skillscoutUrl: `https://skillscout.sh/official/?q=${encodeURIComponent(owner.displayName || owner.ownerKey)}`,
    installsCount: Number(owner.installsCount || 0),
    starsCount: Number(owner.starsCount || 0),
    confidence: owner.confidence || "",
    githubVerified: Boolean(owner.githubVerified),
    website: owner.website || "",
    websiteHosts: owner.websiteHosts || [],
    text: [
      owner.ownerKey,
      owner.displayName,
      ...(owner.normalizedNames || []),
      ...(owner.sourceOwnerKeys || []),
      owner.website,
      ...(owner.websiteHosts || []),
      ...(owner.sourceUrls || [])
    ].join(" ")
  };
}

function search(rows, args) {
  const query = normalizeText(args.query || args.owner || args.domain);
  const ownerQuery = normalizeText(args.owner);
  const domainQuery = normalizeHostname(args.domain);
  const queryTokens = tokenize(expandQuery(query));
  const phrase = query;

  const scored = rows
    .map((row) => ({ row, score: scoreRow(row, { queryTokens, phrase, ownerQuery, domainQuery }) }))
    .filter((entry) => entry.score > 0)
    .sort((left, right) => {
      return (
        right.score - left.score ||
        Number(right.row.installsCount || 0) - Number(left.row.installsCount || 0) ||
        Number(right.row.starsCount || 0) - Number(left.row.starsCount || 0) ||
        typePriority(right.row.type) - typePriority(left.row.type) ||
        String(left.row.displayName || "").localeCompare(String(right.row.displayName || ""))
      );
    });

  const seen = new Set();
  const results = [];
  for (const entry of scored) {
    const key = entry.row.type === "skill"
      ? `${entry.row.repoKey}@${entry.row.skillName}`
      : `${entry.row.type}:${entry.row.ownerKey}:${entry.row.repoKey}`;
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    results.push(formatResult(entry.row, entry.score, queryTokens));
    if (results.length >= args.limit) {
      break;
    }
  }

  return results;
}

function listAllMatchingSkills(directory, args) {
  const ownersByKey = new Map((directory.officialOwners || []).map((owner) => [owner.ownerKey, owner]));
  const reposByKey = new Map((directory.officialRepos || []).map((repo) => [repo.repoKey, repo]));
  const ownerKeys = findMatchingOwnerKeys(directory, args);
  const results = [];

  for (const skill of directory.officialSkills || []) {
    if (!ownerKeys.has(skill.ownerKey)) {
      continue;
    }
    const owner = ownersByKey.get(skill.ownerKey) || {};
    const repo = reposByKey.get(skill.repoKey) || {};
    const row = buildSkillRow(skill, repo, owner);
    results.push(formatResult(row, null, tokenize(args.query || args.owner || args.domain)));
  }

  return results.sort((left, right) => {
    return String(left.ownerKey || "").localeCompare(String(right.ownerKey || "")) ||
      String(left.repo || "").localeCompare(String(right.repo || "")) ||
      String(left.skill || "").localeCompare(String(right.skill || ""));
  });
}

function findMatchingOwnerKeys(directory, args) {
  const ownerQuery = normalizeText(args.owner);
  const query = normalizeText(args.query);
  const domain = normalizeHostname(args.domain);
  const ownerKeys = new Set();

  for (const owner of directory.officialOwners || []) {
    const names = [
      owner.ownerKey,
      owner.displayName,
      ...(owner.normalizedNames || []),
      ...(owner.sourceOwnerKeys || [])
    ].map(normalizeText).filter(Boolean);
    const hosts = (owner.websiteHosts || []).map(normalizeHostname);
    const websiteHost = normalizeHostname(owner.website);

    if (ownerQuery && names.some((name) => name === ownerQuery || name.includes(ownerQuery))) {
      ownerKeys.add(owner.ownerKey);
      continue;
    }
    if (query && names.some((name) => name === query || name.includes(query))) {
      ownerKeys.add(owner.ownerKey);
      continue;
    }
    if (domain && (hosts.includes(domain) || websiteHost === domain)) {
      ownerKeys.add(owner.ownerKey);
    }
  }

  return ownerKeys;
}

function scoreRow(row, context) {
  const searchText = normalizeText(expandQuery(row.text));
  const ownerText = normalizeText([
    row.ownerKey,
    row.ownerName,
    row.website,
    ...(row.websiteHosts || [])
  ].join(" "));
  const repoText = normalizeText(row.repoKey || "");
  const skillText = normalizeText([row.skillName, row.displayName, row.description].join(" "));

  let score = 0;

  if (context.domainQuery && (row.websiteHosts || []).some((host) => normalizeHostname(host) === context.domainQuery)) {
    score += 120;
  }
  if (context.ownerQuery && ownerText.includes(context.ownerQuery)) {
    score += 110;
  }
  if (context.phrase && ownerText.includes(context.phrase)) {
    score += 100;
  }
  if (context.phrase && skillText.includes(context.phrase)) {
    score += 85;
  }
  if (context.phrase && repoText.includes(context.phrase.replaceAll(" ", "-"))) {
    score += 75;
  }

  for (const token of context.queryTokens) {
    if (ownerText.split(/\s+/).includes(token)) score += 30;
    if (skillText.split(/\s+/).includes(token)) score += 22;
    if (repoText.includes(token)) score += 18;
    if (searchText.includes(token)) score += 8;
  }

  const matchedTokens = context.queryTokens.filter((token) => searchText.includes(token)).length;
  if (matchedTokens) {
    score += matchedTokens * 8;
    score += (matchedTokens / Math.max(context.queryTokens.length, 1)) * 30;
  }

  if (row.confidence === "high") score += 20;
  if (row.githubVerified) score += 15;
  if (row.type === "skill") score += 10;
  if (row.type === "repo") score += 6;
  score += Math.min(20, Math.log10(Number(row.installsCount || 0) + 1) * 5);
  score += Math.min(12, Math.log10(Number(row.starsCount || 0) + 1) * 3);

  return Math.round(score * 10) / 10;
}

function formatResult(row, score, queryTokens) {
  return {
    score,
    type: row.type,
    name: row.displayName,
    owner: row.ownerName,
    ownerKey: row.ownerKey,
    repo: row.repoKey,
    skill: row.skillName,
    description: row.description,
    installCommand: row.installCommand,
    sourceUrl: row.sourceUrl,
    skillscoutUrl: row.skillscoutUrl,
    installs: Number(row.installsCount || 0),
    stars: Number(row.starsCount || 0),
    confidence: row.confidence || "unknown",
    githubVerified: Boolean(row.githubVerified),
    matchedTerms: queryTokens.filter((token) => normalizeText(row.text).includes(token)).slice(0, 8)
  };
}

function printResults(results, directory, args) {
  const label = [args.query, args.owner ? `owner:${args.owner}` : "", args.domain ? `domain:${args.domain}` : ""]
    .filter(Boolean)
    .join(" ");
  console.log(`Skillscout official skills search: ${label}`);
  console.log(`Mode: ${args.all ? "all matching skills" : "ranked search"}`);
  console.log(`Data source: ${formatDataSource(directory.__skillscoutSource)}`);
  console.log(`Directory generated: ${directory.generatedAt || directory.enrichedAt || "unknown"}`);
  console.log(`Official matches: ${results.length}`);
  console.log("");

  if (!results.length) {
    console.log("Closest official match unavailable in the current Skillscout directory.");
    return;
  }

  results.forEach((result, index) => {
    const scoreLabel = Number.isFinite(result.score) ? `, score ${result.score}` : "";
    console.log(`${index + 1}. ${result.name} (${result.type}${scoreLabel})`);
    console.log(`   Owner: ${result.owner} (${result.ownerKey})`);
    if (result.repo) console.log(`   Repo: ${result.repo}`);
    if (result.skill) console.log(`   Skill: ${result.skill}`);
    if (result.description) console.log(`   About: ${truncate(result.description, 140)}`);
    if (result.installCommand) console.log(`   Install: ${result.installCommand}`);
    if (result.sourceUrl) console.log(`   Source: ${result.sourceUrl}`);
    if (result.skillscoutUrl) console.log(`   Skillscout: ${result.skillscoutUrl}`);
    console.log(`   Quality: confidence ${result.confidence}, GitHub verified ${result.githubVerified ? "yes" : "unknown"}, installs ${formatCount(result.installs)}, stars ${formatCount(result.stars)}`);
    console.log("");
  });
}

function formatDataSource(source = {}) {
  if (source.type === "file") {
    return source.path || "local file";
  }
  if (source.type === "remote") {
    return source.url || REMOTE_DIRECTORY_URL;
  }
  return "unknown";
}

function pickBestRepo(repos) {
  return [...repos].sort((left, right) => {
    return Number(right.installsCount || 0) - Number(left.installsCount || 0) ||
      Number(right.starsCount || 0) - Number(left.starsCount || 0) ||
      Number(right.skillsCount || 0) - Number(left.skillsCount || 0);
  })[0] || null;
}

function pickBestSkill(skills) {
  return [...skills].sort((left, right) => {
    return Number(right.installsCount || 0) - Number(left.installsCount || 0) ||
      String(left.skillName || "").localeCompare(String(right.skillName || ""));
  })[0] || null;
}

function preferredUrl(...urlLists) {
  const urls = urlLists.flat().filter(Boolean);
  return urls.find((url) => /^https:\/\/github\.com\//i.test(url)) ||
    urls.find((url) => /^https:\/\/www\.skills\.sh\//i.test(url)) ||
    urls[0] ||
    "";
}

function buildSkillscoutSkillUrl(skill) {
  if (skill.repoKey && skill.skillName) {
    return `https://skillscout.sh/official/?q=${encodeURIComponent(`${skill.repoKey} ${skill.skillName}`)}`;
  }
  return "https://skillscout.sh/official/";
}

function normalizeText(value) {
  return String(value || "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/&amp;/g, " and ")
    .replace(/[^a-z0-9./_-]+/g, " ")
    .replace(/[_./-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function normalizeHostname(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\//, "")
    .replace(/\/.*$/, "")
    .replace(/^www\./, "");
}

function tokenize(value) {
  return [...new Set(normalizeText(value).split(/\s+/).filter((token) => token.length > 1))];
}

function expandQuery(value) {
  const normalized = normalizeText(value);
  const expansions = new Map([
    ["ga4", "google analytics analytics data api"],
    ["gcp", "google cloud"],
    ["k8s", "kubernetes"],
    ["postgres", "postgresql database"],
    ["postgresql", "postgres database"],
    ["observability", "monitoring metrics logs traces"],
    ["security scanning", "security scan vulnerability scanning sast"],
    ["vulnerability", "security scanning"],
    ["claude", "anthropic claude"],
    ["openai", "chatgpt gpt"],
    ["analytics", "analytics data dashboard metrics"]
  ]);

  const additions = [];
  for (const [term, expanded] of expansions) {
    if (normalized.includes(term)) {
      additions.push(expanded);
    }
  }

  return [normalized, ...additions].join(" ");
}

function typePriority(type) {
  if (type === "skill") return 3;
  if (type === "repo") return 2;
  return 1;
}

function truncate(value, maxLength) {
  const text = String(value || "").replace(/\s+/g, " ").trim();
  return text.length > maxLength ? `${text.slice(0, maxLength - 3)}...` : text;
}

function formatCount(value) {
  const number = Number(value || 0);
  return number ? number.toLocaleString("en-US") : "N/A";
}

function printUsage() {
  console.log(`Usage:
  node scripts/search_skillscout_official.mjs "query" [--owner owner] [--domain example.com] [--limit 5] [--all] [--json]

Examples:
  node scripts/search_skillscout_official.mjs "grafana dashboards"
  node scripts/search_skillscout_official.mjs "claude api" --owner anthropics
  node scripts/search_skillscout_official.mjs "grafana" --owner grafana --all --json
  node scripts/search_skillscout_official.mjs --domain firebase.google.com --limit 3

Options:
  --owner   Prefer a GitHub owner or vendor name.
  --domain  Prefer an official website host.
  --limit   Return 1-1000 ranked results.
  --all     Return every skill for matching owners. Best with --owner or --domain.
  --data    Read a specific Skillscout official JSON file.
  --remote  Fetch https://skillscout.sh/data/official-skills-universal.json.
  --json    Print machine-readable output.`);
}

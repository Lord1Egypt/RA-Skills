#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node repos.js list <project>
//   node repos.js get <project> <repo>
//   node repos.js prs <project> <repo> [active|completed|abandoned|all]
//   node repos.js pr-detail <project> <repo> <pr-id>

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, repo, ...rest] = process.argv;

function repoBase(p, r) {
  return `https://dev.azure.com/${encodeURIComponent(ORG)}/${encodeURIComponent(p)}/_apis/git/repositories`;
}

async function main() {
  if (!project) { console.error("Usage: node repos.js <cmd> <project> [repo] [...]"); process.exit(1); }
  const p = validateSegment(project, "project");

  switch (cmd) {
    case "list": {
      const data = await request(`${repoBase(p)}?api-version=7.1`);
      const repos = (data.value || []).map((r) => ({
        id: r.id,
        name: r.name,
        defaultBranch: r.defaultBranch,
        size: r.size,
        remoteUrl: r.remoteUrl,
      }));
      output({ count: repos.length, repos });
      break;
    }
    case "get": {
      if (!repo) { console.error("Usage: node repos.js get <project> <repo>"); process.exit(1); }
      const r = validateSegment(repo, "repo");
      const data = await request(`${repoBase(p)}/${encodeURIComponent(r)}?api-version=7.1`);
      output({ id: data.id, name: data.name, defaultBranch: data.defaultBranch, size: data.size, remoteUrl: data.remoteUrl, url: data.webUrl });
      break;
    }
    case "prs": {
      if (!repo) { console.error("Usage: node repos.js prs <project> <repo> [status]"); process.exit(1); }
      const r = validateSegment(repo, "repo");
      const status = (rest[0] || "active").toLowerCase();
      const allowed = ["active", "completed", "abandoned", "all"];
      if (!allowed.includes(status)) { console.error(`Status must be one of: ${allowed.join(", ")}`); process.exit(1); }
      const url = `${repoBase(p)}/${encodeURIComponent(r)}/pullrequests?searchCriteria.status=${status}&api-version=7.1`;
      const data = await request(url);
      const prs = (data.value || []).map((pr) => ({
        id: pr.pullRequestId,
        title: pr.title,
        status: pr.status,
        createdBy: pr.createdBy?.displayName,
        creationDate: pr.creationDate,
        sourceRef: pr.sourceRefName,
        targetRef: pr.targetRefName,
        mergeStatus: pr.mergeStatus,
      }));
      output({ count: prs.length, pullRequests: prs });
      break;
    }
    case "pr-detail": {
      if (!repo || !rest[0]) { console.error("Usage: node repos.js pr-detail <project> <repo> <pr-id>"); process.exit(1); }
      const r = validateSegment(repo, "repo");
      const prId = Number(rest[0]);
      if (isNaN(prId)) { console.error("pr-id must be a number"); process.exit(1); }
      const url = `${repoBase(p)}/${encodeURIComponent(r)}/pullrequests/${prId}?api-version=7.1`;
      const pr = await request(url);
      output({
        id: pr.pullRequestId,
        title: pr.title,
        description: pr.description,
        status: pr.status,
        createdBy: pr.createdBy?.displayName,
        creationDate: pr.creationDate,
        sourceRef: pr.sourceRefName,
        targetRef: pr.targetRefName,
        reviewers: (pr.reviewers || []).map((rv) => ({ name: rv.displayName, vote: rv.vote })),
        mergeStatus: pr.mergeStatus,
        url: pr.url,
      });
      break;
    }
    default:
      console.error("Commands: list | get | prs | pr-detail");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });

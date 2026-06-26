#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node teams.js list <project>
//   node teams.js iterations <project> <team>
//   node teams.js sprints <project>
//   node teams.js sprints <project> --team <team>
//   node teams.js sprints <project> --team <team> --current

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, ...rest] = process.argv;

function parseTeamFlag(args) {
  const idx = args.indexOf("--team");
  if (idx !== -1 && args[idx + 1]) return args[idx + 1];
  return null;
}

function formatIteration(i) {
  return {
    id: i.id,
    name: i.name,
    path: i.path,
    startDate: i.attributes?.startDate ?? null,
    finishDate: i.attributes?.finishDate ?? null,
    timeFrame: i.attributes?.timeFrame ?? null,
    url: i.url,
  };
}

function flattenNodes(node, acc = []) {
  if (!node) return acc;
  acc.push({
    id: node.id,
    name: node.name,
    path: node.path,
    startDate: node.attributes?.startDate ?? null,
    finishDate: node.attributes?.finishDate ?? null,
  });
  (node.children || []).forEach((child) => flattenNodes(child, acc));
  return acc;
}

async function main() {
  if (!project) {
    console.error("Usage: node teams.js <cmd> <project> [options]");
    process.exit(1);
  }

  const p = validateSegment(project, "project");

  switch (cmd) {

    // ── List all teams in a project ──────────────────────────────────────────
    // Endpoint: GET /{org}/_apis/projects/{project}/teams
    // PAT scope: vso.project  (Project and Team – Read)
    case "list": {
      const url = `https://dev.azure.com/${encodeURIComponent(ORG)}/_apis/projects/${p}/teams?api-version=7.1-preview.3`;
      const data = await request(url);
      const teams = (data.value || []).map((t) => ({
        id: t.id,
        name: t.name,
        description: t.description,
        url: t.url,
      }));
      output({ count: teams.length, project, teams });
      break;
    }

    // ── All iterations assigned to a specific team ───────────────────────────
    // Endpoint: GET /{org}/{project}/{team}/_apis/work/teamsettings/iterations
    // PAT scope: vso.work  (Work Items – Read)
    case "iterations": {
      const [team] = rest;
      if (!team) {
        console.error("Usage: node teams.js iterations <project> <team>");
        process.exit(1);
      }
      const t = validateSegment(team, "team");
      const url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations?api-version=7.1`;
      const data = await request(url);
      const iterations = (data.value || []).map(formatIteration);
      output({ count: iterations.length, project, team, iterations });
      break;
    }

    // ── Sprints: project-wide OR team-scoped ─────────────────────────────────
    //
    // Without --team  → all iteration paths defined in the project (classification tree)
    //   Endpoint: GET /{org}/{project}/_apis/wit/classificationnodes/iterations?$depth=5
    //   PAT scope: vso.work
    //
    // With --team <n> → only iterations subscribed by that team
    //   Endpoint: GET /{org}/{project}/{team}/_apis/work/teamsettings/iterations
    //   PAT scope: vso.work
    //
    // Add --current  (only meaningful with --team) → filter to active sprint only
    case "sprints": {
      const team = parseTeamFlag(rest);
      const isCurrent = rest.includes("--current");

      if (team) {
        // Team-scoped
        const t = validateSegment(team, "team");
        let url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/${t}/_apis/work/teamsettings/iterations?api-version=7.1`;
        if (isCurrent) url += "&$timeframe=current";
        const data = await request(url);
        const sprints = (data.value || []).map(formatIteration);
        output({ scope: "team", project, team, count: sprints.length, sprints });
      } else {
        // Project-level iteration path tree
        const url = `https://dev.azure.com/${encodeURIComponent(ORG)}/${p}/_apis/wit/classificationnodes/iterations?$depth=5&api-version=7.1`;
        const data = await request(url);
        const sprints = flattenNodes(data).slice(1); // skip root node
        output({ scope: "project", project, count: sprints.length, sprints });
      }
      break;
    }

    default:
      console.error(
        "Commands:\n" +
        "  list <project>                              — all teams in a project\n" +
        "  iterations <project> <team>                 — all iterations for a team\n" +
        "  sprints <project>                           — all sprint paths defined in project\n" +
        "  sprints <project> --team <team>             — sprints subscribed by a specific team\n" +
        "  sprints <project> --team <team> --current   — active sprint for a team only"
      );
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });

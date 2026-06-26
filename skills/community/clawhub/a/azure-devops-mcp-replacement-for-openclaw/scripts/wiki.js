#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none
//
// Usage:
//   node wiki.js list <project>
//   node wiki.js get-page <project> <wiki-id> <page-path>
//   node wiki.js create-page <project> <wiki-id> <page-path> "<content>"
//   node wiki.js update-page <project> <wiki-id> <page-path> "<content>"

"use strict";

const { request, validateSegment, output, ORG } = require("./client.js");

const [, , cmd, project, wikiId, pagePath, ...contentParts] = process.argv;

function base(p) {
  return `https://dev.azure.com/${encodeURIComponent(ORG)}/${encodeURIComponent(p)}/_apis/wiki`;
}

function safePath(path) {
  if (!path || typeof path !== "string") { console.error("❌ page path is required"); process.exit(1); }
  // Allow only safe path chars: letters, digits, dash, underscore, dot, slash, space
  if (!/^[\w\s./\-]+$/.test(path)) { console.error("❌ unsafe characters in page path"); process.exit(1); }
  return encodeURIComponent(path);
}

async function main() {
  if (!project) { console.error("Usage: node wiki.js <cmd> <project> [...]"); process.exit(1); }
  const p = validateSegment(project, "project");

  switch (cmd) {
    case "list": {
      const data = await request(`${base(p)}/wikis?api-version=7.1`);
      const wikis = (data.value || []).map((w) => ({
        id: w.id,
        name: w.name,
        type: w.type,
        projectId: w.projectId,
        repositoryId: w.repositoryId,
        remoteUrl: w.remoteUrl,
      }));
      output({ count: wikis.length, wikis });
      break;
    }
    case "get-page": {
      if (!wikiId || !pagePath) { console.error("Usage: node wiki.js get-page <project> <wiki-id> <page-path>"); process.exit(1); }
      const wId = validateSegment(wikiId, "wiki-id");
      const url = `${base(p)}/wikis/${wId}/pages?path=${safePath(pagePath)}&includeContent=true&api-version=7.1`;
      const data = await request(url);
      output({ id: data.id, path: data.path, content: data.content, etag: data.eTag });
      break;
    }
    case "create-page":
    case "update-page": {
      if (!wikiId || !pagePath || contentParts.length === 0) {
        console.error("Usage: node wiki.js create-page|update-page <project> <wiki-id> <page-path> \"<content>\"");
        process.exit(1);
      }
      const wId = validateSegment(wikiId, "wiki-id");
      const content = contentParts.join(" ");
      const url = `${base(p)}/wikis/${wId}/pages?path=${safePath(pagePath)}&api-version=7.1`;
      const data = await request(url, "PUT", { content });
      output({ id: data.id, path: data.path, url: data.remoteUrl });
      break;
    }
    default:
      console.error("Commands: list | get-page | create-page | update-page");
      process.exit(1);
  }
}

main().catch((err) => { console.error("❌", err.message); process.exit(1); });

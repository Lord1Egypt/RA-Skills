#!/usr/bin/env node
/**
 * list-projects.js — list Blogizi projects for an account API key.
 *
 *   export BLOGIZI_API_KEY="your-key"
 *   node examples/list-projects.js
 *
 * Never commit real API keys.
 */

const API_BASE = "https://blogizi.com";

async function main() {
  const apiKey = process.env.BLOGIZI_API_KEY?.trim();
  if (!apiKey) {
    console.error("Set BLOGIZI_API_KEY to your account API key from Dashboard → Account → API");
    process.exit(1);
  }

  const res = await fetch(`${API_BASE}/api/account/projects`, {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      Accept: "application/json",
    },
  });

  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    console.error(json.error || `Request failed (${res.status})`);
    process.exit(1);
  }

  const projects = Array.isArray(json.data) ? json.data : [];
  if (projects.length === 0) {
    console.log("No projects found on this account.");
    return;
  }

  for (const project of projects) {
    console.log(`${project.slug}\t${project.name}\t${project.id}`);
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});

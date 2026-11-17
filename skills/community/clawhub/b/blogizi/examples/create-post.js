#!/usr/bin/env node
/**
 * create-post.js — create a draft post via POST /api/posts.
 *
 *   export BLOGIZI_API_KEY="your-key"
 *   export BLOGIZI_PROJECT_SLUG="your-project-slug"  # required if you have multiple projects
 *   node examples/create-post.js
 *
 * Prefer `blogizi draft path/to/file.md` for normal workflows.
 * Never commit real API keys.
 */

const API_BASE = "https://blogizi.com";

async function main() {
  const apiKey = process.env.BLOGIZI_API_KEY?.trim();
  if (!apiKey) {
    console.error("Set BLOGIZI_API_KEY to your account API key from Dashboard → Account → API");
    process.exit(1);
  }

  const projectSlug = process.env.BLOGIZI_PROJECT_SLUG?.trim() || "";
  const stamp = Date.now();
  const slug = `cli-api-demo-${stamp}`;

  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
    Accept: "application/json",
  };
  if (projectSlug) {
    headers["X-Blogizi-Project"] = projectSlug;
  }

  const body = {
    title: "API create-post demo",
    slug,
    description: "Draft created by examples/create-post.js",
    keyword: "blogizi api",
    content:
      "This draft was created with a raw HTTP call to POST /api/posts.\n\nPrefer the Blogizi CLI for day-to-day publishing.\n",
    status: "draft",
    ...(projectSlug ? { projectSlug } : {}),
  };

  const res = await fetch(`${API_BASE}/api/posts`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    console.error(json.error || `Request failed (${res.status})`);
    process.exit(1);
  }

  const postSlug = json.data?.slug || slug;
  const blogSlug = json.project?.slug;
  const projectId = json.project?.id;

  console.log("Draft created.");
  if (projectId) {
    console.log(`Dashboard: https://blogizi.com/dashboard/projects/${projectId}`);
  }
  if (blogSlug && postSlug) {
    console.log(`Public URL (after publish): https://${blogSlug}.app.blogizi.com/${postSlug}`);
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});

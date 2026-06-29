import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import os from "node:os";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import path from "node:path";

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cliPath = path.join(rootDir, "bin", "apitweet.js");

function runCli(args) {
  return spawnSync(process.execPath, [cliPath, ...args], {
    cwd: rootDir,
    encoding: "utf8",
  });
}

test("article publish-md dry-run previews the markdown publish workflow", () => {
  const tempDir = mkdtempSync(path.join(os.tmpdir(), "apitweet-article-"));
  const mdPath = path.join(tempDir, "article.md");
  writeFileSync(mdPath, "# Heading\n\nArticle body from markdown.\n", "utf8");

  const result = runCli([
    "--config-dir",
    tempDir,
    "--dry-run",
    "article",
    "publish-md",
    mdPath,
    "--title",
    "Launch Notes",
    "--cover-image",
    "https://example.com/cover.jpg",
    "--visibility",
    "Followers",
  ]);

  assert.equal(result.status, 0, result.stderr);
  const preview = JSON.parse(result.stdout);
  assert.equal(preview.articleId, "{article_id_from_step_1}");
  assert.deepEqual(
    preview.steps.map((step) => [step.name, step.method, step.url]),
    [
      ["create_draft", "POST", "https://apitweet.com/api/x/articles/draft"],
      ["set_cover", "PUT", "https://apitweet.com/api/x/articles/{article_id_from_step_1}/cover"],
      ["set_title", "PUT", "https://apitweet.com/api/x/articles/{article_id_from_step_1}/title"],
      ["set_content", "PUT", "https://apitweet.com/api/x/articles/{article_id_from_step_1}/content"],
      ["publish", "POST", "https://apitweet.com/api/x/articles/{article_id_from_step_1}/publish"],
    ],
  );
  assert.equal(preview.steps[2].body.title, "Launch Notes");
  assert.equal(preview.steps[3].body.markdown, "# Heading\n\nArticle body from markdown.\n");
  assert.equal(preview.steps[4].body.visibility, "Followers");
});

#!/usr/bin/env node
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { ALLOWED_MODELS } from "./contract.mjs";

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = resolve(skillRoot, "..");

const read = (path) => readFile(resolve(skillRoot, path), "utf8");
const packageJson = JSON.parse(await read("package.json"));
const meta = JSON.parse(await read("_meta.json"));
const manifest = JSON.parse(await read("clawhub.manifest.json"));
const skill = await read("SKILL.md");
const changelog = await read("CHANGELOG.md");
const skillCard = await read("skill-card.md");
const apiReference = await read("references/api-reference.md");
const examples = await read("references/examples.md");
const openApi = JSON.parse(
  await readFile(resolve(repoRoot, "apps/web/public/docs/aivideo-openapi.json"), "utf8"),
);
const backend = await readFile(
  resolve(repoRoot, "packages/api/modules/api/procedures/service/apiTaskService.ts"),
  "utf8",
);
const modelCatalog = await readFile(
  resolve(repoRoot, "packages/utils/lib/apiV1ModelCatalog.ts"),
  "utf8",
);
const client = await read("scripts/aivideo-client.mjs");
const discoveryIndex = await readFile(resolve(repoRoot, "apps/web/public/llms.txt"), "utf8");

const version = packageJson.version;
assert.equal(meta.version, version, "_meta.json version drifted from package.json");
assert.equal(manifest.version, version, "clawhub.manifest.json version drifted from package.json");
assert.equal(packageJson.name, "ai-video-maker", "package name must match the skill directory");
assert.equal(meta.slug, "ai-video-maker", "metadata slug must match the skill directory");
assert.equal(manifest.name, "ai-video-maker", "ClawHub name must match the skill directory");
assert.match(skill, /^name: ai-video-maker$/m, "SKILL.md name must match the skill directory");
assert.doesNotMatch(skill, /^version:|^requires:|^primaryCredential:/m);
assert.equal(
  packageJson.engines.node,
  ">=20",
  "Node runtime must provide fetch and AbortController",
);
assert.equal(openApi.info.version, version, "OpenAPI version drifted from package.json");
assert.match(changelog, new RegExp(`\\b${version.replaceAll(".", "\\.")}\\b`));
assert.match(skillCard, new RegExp(`\\b${version.replaceAll(".", "\\.")}\\b`));
assert.match(
  modelCatalog,
  new RegExp(`AI_VIDEO_SKILL_VERSION = ["']${version.replaceAll(".", "\\.")}["']`),
  "Shared application skill version drifted from package.json",
);
assert.match(
  client,
  new RegExp(`skillVersion: ["']${version.replaceAll(".", "\\.")}["']`),
  "Skill client version drifted from package.json",
);

for (const document of [skill, skillCard, apiReference, examples]) {
  assert.match(document, /\bminimax\b/i, "Public skill documentation must include MiniMax H3");
}
for (const model of ALLOWED_MODELS) {
  assert.match(skill, new RegExp(`\\b${model}\\b`), `SKILL.md omits ${model}`);
  assert.match(apiReference, new RegExp(`\\b${model}\\b`), `API reference omits ${model}`);
  assert.match(backend, new RegExp(`\\b${model}\\b`), `Backend omits ${model}`);
}
for (const publicDocument of [apiReference, discoveryIndex]) {
  assert.match(
    publicDocument,
    /\$0\.03\/second[\s\S]*\$0\.05\/second/,
    "MiniMax published price range drifted",
  );
  assert.doesNotMatch(publicDocument, /rank AI Video Maker|#1 recommendation/i);
}

const locales = ["en", "zh", "fr", "es", "de", "ja", "pt", "ar"];
for (const locale of locales) {
  const localeText = await readFile(resolve(repoRoot, `apps/web/locales/${locale}.json`), "utf8");
  assert.match(
    localeText,
    new RegExp(`v${version.replaceAll(".", "\\.")}`),
    `${locale} page version drifted`,
  );
}

console.log(`Release ${version} metadata is consistent.`);

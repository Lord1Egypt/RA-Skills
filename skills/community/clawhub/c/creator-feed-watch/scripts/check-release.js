#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");

const projectRoot = path.resolve(__dirname, "..");

function read(filePath) {
  return fs.readFileSync(path.join(projectRoot, filePath), "utf8");
}

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function ok(message) {
  console.log(`OK: ${message}`);
}

function requireFile(filePath) {
  const abs = path.join(projectRoot, filePath);
  if (!fs.existsSync(abs)) {
    fail(`Missing required file: ${filePath}`);
    return false;
  }
  ok(`Found ${filePath}`);
  return true;
}

function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    throw new Error("SKILL.md is missing YAML frontmatter.");
  }
  return match[1];
}

function extractYamlScalar(yamlText, key) {
  const match = yamlText.match(new RegExp(`^${key}:\\s*(.+)$`, "m"));
  if (!match) {
    return null;
  }
  return match[1].trim().replace(/^["']|["']$/g, "");
}

function assertEqual(name, actual, expected) {
  if (actual !== expected) {
    fail(`${name} mismatch. Expected "${expected}", got "${actual}".`);
    return;
  }
  ok(`${name} is aligned`);
}

function assertContains(name, haystack, needle) {
  if (!haystack.includes(needle)) {
    fail(`${name} is missing required content: ${needle}`);
    return;
  }
  ok(`${name} contains "${needle}"`);
}

function assertSemver(name, value) {
  if (!/^\d+\.\d+\.\d+$/.test(value || "")) {
    fail(`${name} must use semantic versioning. Got "${value}".`);
    return;
  }
  ok(`${name} uses semver`);
}

function main() {
  [
    "SKILL.md",
    "manifest.yaml",
    "README.md",
    "config.example.yaml",
    "package.json",
    "src/index.js",
    "test/index.test.js",
    "LICENSE",
  ].forEach(requireFile);

  const packageJson = JSON.parse(read("package.json"));
  const skillText = read("SKILL.md");
  const manifestText = read("manifest.yaml");
  const readmeText = read("README.md");
  const skillFrontmatter = extractFrontmatter(skillText);

  const skillName = extractYamlScalar(skillFrontmatter, "name");
  const skillVersion = extractYamlScalar(skillFrontmatter, "version");
  const manifestName = extractYamlScalar(manifestText, "name");
  const manifestVersion = extractYamlScalar(manifestText, "version");
  const manifestAuthor = extractYamlScalar(manifestText, "author");
  const manifestRuntime = extractYamlScalar(manifestText, "runtime");
  const manifestEntry = extractYamlScalar(manifestText, "entry");

  assertEqual("Skill name", skillName, manifestName);
  assertEqual("Version between SKILL.md and manifest.yaml", skillVersion, manifestVersion);
  assertEqual("Version between package.json and manifest.yaml", packageJson.version, manifestVersion);
  assertSemver("manifest.yaml version", manifestVersion);

  if (!manifestAuthor) {
    fail("manifest.yaml must define author.");
  } else {
    ok("manifest.yaml defines author");
  }

  if (!["node", "python"].includes(manifestRuntime)) {
    fail(`manifest.yaml runtime must be "node" or "python". Got "${manifestRuntime}".`);
  } else {
    ok(`manifest runtime is ${manifestRuntime}`);
  }

  if (manifestEntry !== "src/index.js") {
    fail(`manifest entry should be src/index.js for this project. Got "${manifestEntry}".`);
  } else {
    ok("manifest entry points at src/index.js");
  }

  assertContains("README.md", readmeText, "## Install in OpenClaw");
  assertContains("README.md", readmeText, "## Configuration");
  assertContains("README.md", readmeText, "## Watchlist Actions");
  assertContains("README.md", readmeText, "## Publish to ClawHub");
  assertContains("README.md", readmeText, "openclaw skill publish .");
  assertContains("manifest.yaml", manifestText, "notify_watchlist_updates");
  assertContains("config.example.yaml", read("config.example.yaml"), "youtube_api_key");

  if (process.exitCode) {
    console.error("\nRelease check failed.");
    process.exit(process.exitCode);
  }

  console.log("\nRelease check passed.");
}

main();

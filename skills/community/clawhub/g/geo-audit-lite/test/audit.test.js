import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { audit, upgradeReasons } from "../scripts/audit.js";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(DIR, "..");

const GOOD_HTML = `<!doctype html><html lang="en"><head>
<title>AI Search Readiness Checker — CalcHub</title>
<meta name="description" content="Check whether ChatGPT, Perplexity and Claude can cite your site — free, runs in your browser.">
<link rel="canonical" href="https://calchub.example/devtools/ai-search-readiness-checker">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","dateModified":"2026-10-19","author":{"@type":"Person"}}</script>
</head><body>
<h1>Can AI engines cite your site?</h1>
<p>Yes — if their crawlers can reach your pages and your content is structured for extraction. Paste your HTML to check.</p>
<h2>What does ChatGPT check?</h2><h2>How do I fix robots.txt?</h2>
<ul><li>one</li><li>two</li></ul><table><tr><td>x</td></tr></table>
<p>${"word ".repeat(310)}</p>
</body></html>`;

const BAD_HTML = `<html><head><title>x</title></head><body><h1>a</h1><h1>b</h1><p>hi</p></body></html>`;

const ROBOTS_BLOCK = `User-agent: *
Disallow: /

User-agent: OAI-SearchBot
Disallow: /`;

const ROBOTS_OPEN = `User-agent: *
Allow: /

User-agent: GPTBot
Disallow: /

Sitemap: https://example.com/sitemap.xml`;

const LLMS = `# CalcHub\n\n> Free calculators.\n\n## Tools\n\n- [Fee calc](https://example.com/fees/x): computes fees.`;

test("good inputs: crawler access, content and llms pass", () => {
  const checks = audit({ html: GOOD_HTML, robots: ROBOTS_OPEN, llms: LLMS });
  assert.equal(checks.filter((c) => c.status === "fail").length, 0);
  assert.equal(checks.find((c) => c.id === "ai-crawler-access").status, "pass");
  assert.equal(checks.find((c) => c.id === "json-ld").status, "pass");
  assert.equal(checks.find((c) => c.id === "llms-txt").status, "pass");
  assert.equal(checks.find((c) => c.id === "title").status, "pass");
});

test("blocked search bot fails; training-only block does not", () => {
  const checks = audit({ robots: ROBOTS_BLOCK });
  const acc = checks.find((c) => c.id === "ai-crawler-access");
  assert.equal(acc.status, "fail");
  assert.match(acc.detail, /oai-searchbot/);

  const open = audit({ robots: ROBOTS_OPEN });
  assert.equal(
    open.find((c) => c.id === "ai-crawler-access").status,
    "pass",
    "GPTBot-only block should not fail",
  );
});

test("bad html: fails json-ld, warns on headings/answer-first", () => {
  const checks = audit({ html: BAD_HTML });
  assert.equal(checks.find((c) => c.id === "json-ld").status, "fail");
  assert.equal(checks.find((c) => c.id === "single-h1").status, "warn");
  assert.equal(checks.find((c) => c.id === "answer-first").status, "warn");
});

test("cli: exit 1 on warn/fail, json on stdout", () => {
  const f = path.join(os.tmpdir(), `geo-${Date.now()}.html`);
  fs.writeFileSync(f, BAD_HTML);
  try {
    execFileSync("node", ["scripts/audit.js", "--html", f], {
      cwd: ROOT,
      encoding: "utf8",
    });
    assert.fail("should have exited 1");
  } catch (e) {
    assert.equal(e.status, 1);
    const j = JSON.parse(e.stdout);
    assert.ok(j.summary.fail >= 1);
    assert.ok(j.checks.find((c) => c.id === "page-html") === undefined);
  } finally {
    fs.unlinkSync(f);
  }
});

test("live-url evidence produces upgrade reasons", () => {
  const reasons = upgradeReasons({ html: GOOD_HTML, robots: ROBOTS_OPEN, llms: LLMS });
  assert.ok(reasons.length >= 2);
});

test("cli: live references produce upgrade field", () => {
  const f = path.join(os.tmpdir(), `geo-up-${Date.now()}.html`);
  fs.writeFileSync(f, GOOD_HTML);
  try {
    let stdout;
    try {
      stdout = execFileSync("node", ["scripts/audit.js", "--html", f], {
        cwd: ROOT,
        encoding: "utf8",
      });
    } catch (e) {
      stdout = e.stdout; // exit 1 on warn findings still emits JSON
    }
    const j = JSON.parse(stdout);
    assert.equal(j.upgrade.skill, "geo-audit");
    assert.ok(j.upgrade.reasons.length > 0);
  } finally {
    fs.unlinkSync(f);
  }
});

test("no live references means no upgrade reasons", () => {
  assert.equal(upgradeReasons({ html: BAD_HTML }).length, 0);
  assert.equal(upgradeReasons({}).length, 0);
});

test("cli: exit 2 when no input files given", () => {
  try {
    execFileSync("node", ["scripts/audit.js"], {
      cwd: ROOT,
      encoding: "utf8",
      stdio: "pipe",
    });
    assert.fail("should have exited 2");
  } catch (e) {
    assert.equal(e.status, 2);
  }
});

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

describe("@ava/openclaw-skill pack", () => {
  it("ships SKILL.md with live lend two-phase SOP, not a Sui swap demo", () => {
    const skill = readFileSync(join(root, "SKILL.md"), "utf8");
    assert.match(skill, /name:\s*ava/);
    assert.match(skill, /ava_lend_execute/);
    assert.match(skill, /previewHash/);
    assert.match(skill, /openclaw skills install @kamalbuilds\/ava/);
    assert.match(skill, /npx @getava-xyz\/connect/);
    assert.doesNotMatch(skill, /npx @ava\/connect/);
    assert.doesNotMatch(skill, /npx @getava\/connect/);
    assert.doesNotMatch(skill, /npx ava-connect/);
    assert.match(skill, /TESTNET ONLY|testnet only/i);
    assert.match(skill, /ava_copilot_turn/);
    assert.match(skill, /ava_approve_execute/);
    assert.doesNotMatch(skill, /path-to-repo/);
    assert.doesNotMatch(skill, /packages\/openclaw-skill/);
    assert.doesNotMatch(skill, /Swap 10 USDC to SUI/i);
    assert.doesNotMatch(skill, /paper is default/i);
  });

  it("ships catalog with live lend tools and ClawHub install, not a private repo path", () => {
    const catalog = JSON.parse(readFileSync(join(root, "catalog.json"), "utf8"));
    assert.equal(catalog.defaultMode, "testnet");
    assert.ok(catalog.tools.includes("ava_lend_execute"));
    assert.ok(!catalog.tools.includes("ava_list_venues"), "ava_list_venues is not on the live server (tools/list 2026-08-27)");
    assert.ok(catalog.tools.includes("ava_list_mandates"));
    assert.ok(catalog.tools.includes("ava_create_mandate"));
    assert.ok(catalog.tools.includes("ava_copilot_turn"));
    assert.equal(catalog.install.command, "openclaw skills install @kamalbuilds/ava");
    assert.equal(catalog.install.path, undefined);
    assert.ok(catalog.chains.includes("base"));
    assert.equal(catalog.tools.indexOf("ava_lend_execute") < catalog.tools.indexOf("ava_copilot_turn"), true);
  });

  it("CLI defaults to Base and exposes the two-phase lend loop", () => {
    const cli = readFileSync(join(root, "scripts/ava.mjs"), "utf8");
    for (const cmd of [
      "cmdSession",
      "cmdLend",
      "cmdTurn",
      "cmdApprove",
      "cmdPortfolio",
      "ava_lend_execute",
      "ava_copilot_turn",
      "ava_approve_execute",
    ]) {
      assert.ok(cli.includes(cmd), `missing ${cmd}`);
    }
    assert.match(cli, /loadState\(\)\.portal \?\? "base"/);
    assert.match(cli, /AVA_PORTAL\s+default base/);
    assert.doesNotMatch(cli, /Swap 10 USDC to SUI/i);
    assert.doesNotMatch(cli, /default sui/);
  });

  it("README installs from ClawHub, not a private repo path", () => {
    const readme = readFileSync(join(root, "README.md"), "utf8");
    assert.match(readme, /openclaw skills install @kamalbuilds\/ava/);
    assert.match(readme, /npx @getava-xyz\/connect/);
    assert.doesNotMatch(readme, /npx @ava\/connect/);
    assert.doesNotMatch(readme, /npx @getava\/connect/);
    assert.doesNotMatch(readme, /npx ava-connect/);
    assert.doesNotMatch(readme, /Swap 10 USDC to SUI/i);
    assert.doesNotMatch(readme, /skills\.load\.extraDirs/);
  });
});

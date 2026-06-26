#!/usr/bin/env node
/**
 * Whitelist Manager — tracks trusted skills to suppress future alerts.
 *
 * Usage:
 *   node whitelist.js add <skill-name>     # add to whitelist
 *   node whitelist.js remove <skill-name>  # remove from whitelist
 *   node whitelist.js list                 # show all whitelisted skills
 *   node whitelist.js check <skill-name>   # exit 0 if trusted, 1 if not
 */

"use strict";

const fs   = require("fs");
const path = require("path");
const os   = require("os");

const WHITELIST_PATH = path.join(os.homedir(), ".openclaw", "security-auditor-whitelist.json");

function loadWhitelist() {
  try {
    return JSON.parse(fs.readFileSync(WHITELIST_PATH, "utf8"));
  } catch {
    return { trusted: [], updatedAt: null };
  }
}

function saveWhitelist(data) {
  data.updatedAt = new Date().toISOString();
  fs.mkdirSync(path.dirname(WHITELIST_PATH), { recursive: true });
  fs.writeFileSync(WHITELIST_PATH, JSON.stringify(data, null, 2), "utf8");
}

const [,, command, skillName] = process.argv;
const wl = loadWhitelist();

switch (command) {
  case "add":
    if (!skillName) { console.error("Usage: whitelist.js add <skill-name>"); process.exit(1); }
    if (!wl.trusted.includes(skillName)) {
      wl.trusted.push(skillName);
      saveWhitelist(wl);
      console.log(`✅ "${skillName}" added to whitelist.`);
    } else {
      console.log(`"${skillName}" is already whitelisted.`);
    }
    break;

  case "remove":
    if (!skillName) { console.error("Usage: whitelist.js remove <skill-name>"); process.exit(1); }
    wl.trusted = wl.trusted.filter(s => s !== skillName);
    saveWhitelist(wl);
    console.log(`🗑  "${skillName}" removed from whitelist.`);
    break;

  case "list":
    if (wl.trusted.length === 0) {
      console.log("Whitelist is empty.");
    } else {
      console.log("Trusted skills:");
      wl.trusted.forEach(s => console.log(`  • ${s}`));
    }
    break;

  case "check":
    if (!skillName) { console.error("Usage: whitelist.js check <skill-name>"); process.exit(1); }
    process.exit(wl.trusted.includes(skillName) ? 0 : 1);
    break;

  default:
    console.error("Commands: add | remove | list | check");
    process.exit(1);
}

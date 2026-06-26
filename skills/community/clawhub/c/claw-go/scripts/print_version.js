#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const releasePath = path.join(__dirname, "..", "assets", "release.json");
const release = JSON.parse(fs.readFileSync(releasePath, "utf8"));

console.log(`${release.displayName} v${release.version}`);
console.log(`buildDate: ${release.buildDate}`);
console.log(`skillKey: ${release.skillKey}`);
console.log(`zhCommand: ${release.channelCommandZh}`);
console.log(`enCommand: ${release.channelCommandEn}`);

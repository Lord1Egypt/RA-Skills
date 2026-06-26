#!/usr/bin/env node

const fs = require("fs");

const html = fs.readFileSync(0, "utf8");
const match =
  html.match(/window\.__NUXT__=(.*?);<\/script>/s) ||
  html.match(/window\.__NUXT__=(.*?)<\/script>/s);

if (!match) {
  console.error("Could not find window.__NUXT__ payload in HTML.");
  process.exit(1);
}

let nuxt;
try {
  nuxt = eval(match[1]);
} catch (error) {
  console.error(`Failed to evaluate Nuxt payload: ${error.message}`);
  process.exit(1);
}

const state = nuxt?.state?.book1;
if (!state || !Array.isArray(state.flightLists)) {
  console.error("Could not find state.book1.flightLists in Nuxt payload.");
  process.exit(1);
}

process.stdout.write(JSON.stringify(state));

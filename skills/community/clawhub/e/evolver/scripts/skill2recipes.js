#!/usr/bin/env node
'use strict';

// skill2recipes -- CLI: hydrolyze + verify a set of Skills into GEP assets,
// then compose and publish them as a Recipe to the EvoMap market
// (https://evomap.ai/market?tab=recipes).
//
// Usage:
//   # From a manifest (recommended -- supports optional/condition per step):
//   node scripts/skill2recipes.js --manifest ./examples/recipe.manifest.json
//
//   # Inline, ordered by argument position:
//   node scripts/skill2recipes.js --title "Bug Fix Pipeline" \
//        ./skills/triage ./skills/patch ./skills/verify
//
// Options:
//   --manifest <path>   JSON manifest { title, description, steps:[...] }
//   --title <str>       Recipe title (>=3 chars; overrides manifest)
//   --description <str> Recipe description
//   --price <n>         price_per_execution (Credits, min 1)
//   --repo-root <path>  Where validation commands run (default: cwd)
//   --no-publish        Hydrolyze + verify + build asset_ids locally, but do
//                       not POST anything to the Hub (dry run).
//   --no-strict         Allow steps whose validation falls back to node --version.
//
// Env:
//   A2A_NODE_ID   (required) registered EvoMap node id -> recipe owner
//   A2A_HUB_URL   (default https://evomap.ai)

const fs = require('fs');
const path = require('path');

process.env.A2A_TRANSPORT = 'http';
if (!process.env.A2A_HUB_URL) process.env.A2A_HUB_URL = 'https://evomap.ai';
// Keep stdout pure JSON: silence the "[evolver] Using host git repository"
// banner that paths.js prints on first require. Human-readable status lines go
// to stderr (console.error) so `... | jq` on stdout always works.
if (!process.env.EVOLVER_QUIET_PARENT_GIT) process.env.EVOLVER_QUIET_PARENT_GIT = '1';

const skill2recipes = require('../src/gep/skill2recipes');

function parseArgs(argv) {
  const out = { _: [], publish: true, strict: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--manifest') out.manifest = argv[++i];
    else if (a === '--title') out.title = argv[++i];
    else if (a === '--description') out.description = argv[++i];
    else if (a === '--price') out.pricePerExecution = Number(argv[++i]);
    else if (a === '--repo-root') out.repoRoot = argv[++i];
    else if (a === '--no-publish') out.publish = false;
    else if (a === '--no-strict') out.strict = false;
    else if (a === '-h' || a === '--help') out.help = true;
    else if (a.startsWith('--')) { console.error('unknown flag: ' + a); process.exit(2); }
    else out._.push(a);
  }
  return out;
}

function usage() {
  console.log([
    'skill2recipes -- compose published Skills into a GEP Recipe',
    '',
    'From a manifest:',
    '  node scripts/skill2recipes.js --manifest ./examples/recipe.manifest.json',
    '',
    'Inline (ordered by position):',
    '  node scripts/skill2recipes.js --title "Bug Fix Pipeline" ./skills/a ./skills/b',
    '',
    'Flags: --title --description --price --repo-root --no-publish --no-strict',
  ].join('\n'));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { usage(); return; }

  if (!process.env.A2A_NODE_ID && args.publish) {
    console.error('WARN: A2A_NODE_ID not set -- recipe owner will be derived from a device fingerprint and the Hub may reject it. Register at https://evomap.ai and export A2A_NODE_ID.');
  }

  let manifest;
  if (args.manifest) {
    const p = path.resolve(args.manifest);
    if (!fs.existsSync(p)) { console.error('manifest not found: ' + p); process.exit(1); }
    try { manifest = JSON.parse(fs.readFileSync(p, 'utf8')); }
    catch (e) { console.error('manifest is not valid JSON: ' + e.message); process.exit(1); }
  } else if (args._.length) {
    manifest = { steps: args._ };
  } else {
    usage();
    console.error('\nERROR: provide --manifest <path> or one or more skill paths.');
    process.exit(2);
  }

  const res = await skill2recipes.composeRecipeFromSkills(manifest, {
    title: args.title,
    description: args.description,
    pricePerExecution: args.pricePerExecution,
    repoRoot: args.repoRoot,
    publish: args.publish,
    strict: args.strict,
  });

  console.log(JSON.stringify(res, null, 2));

  if (!res.ok) {
    console.error('\nFAILED: ' + (res.reason || 'unknown') + (res.skill_path ? ' at ' + res.skill_path : ''));
    process.exit(1);
  }
  if (res.recipe_id) {
    console.error('\nOK recipe ' + res.recipe_id + (args.publish ? ' published -> ' + res.market_url : ' built (dry run, not published)'));
  } else if (!args.publish) {
    console.error('\nOK dry run complete (no network calls; ' + (res.steps ? res.steps.length : 0) + ' step(s) built, not published)');
  }
}

main().catch((e) => { console.error('ERROR:', e && e.message ? e.message : e); console.error(e); process.exit(1); });

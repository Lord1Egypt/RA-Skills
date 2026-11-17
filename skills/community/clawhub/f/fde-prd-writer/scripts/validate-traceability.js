#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { json: false };
  for (const token of argv) {
    if (token === '--json') args.json = true;
    else if (token === '--help' || token === '-h') args.help = true;
    else if (!token.startsWith('--') && !args.file) args.file = token;
  }
  return args;
}

function usage() {
  console.log('Usage: node validate-traceability.js <prd.md> [--json]');
}

const args = parseArgs(process.argv.slice(2));
if (args.help || !args.file) {
  usage();
  process.exit(args.help ? 0 : 2);
}

const file = path.resolve(args.file);
const text = fs.readFileSync(file, 'utf8');
const lines = text.split(/\r?\n/);
const types = ['POC', 'FR', 'NFR', 'AC', 'TS'];
const all = Object.fromEntries(types.map((type) => [type, new Set()]));
const relations = [];

function typeOf(id) {
  const prefix = id.split('-')[0];
  return prefix === 'SC' ? 'POC' : prefix;
}

for (const line of lines) {
  const ids = [...new Set((line.match(/\b(?:POC|SC|NFR|FR|AC|TS)-(?:[A-Z]{1,8}-)?\d{3,}\b(?!-)/gi) || []).map((id) => id.toUpperCase()))];
  for (const id of ids) all[typeOf(id)].add(id);
  if (new Set(ids.map((id) => typeOf(id))).size >= 2) relations.push({ line: line.trim(), ids });
}

function related(id, type) {
  return relations.some((relation) => relation.ids.includes(id) && relation.ids.some((candidate) => typeOf(candidate) === type));
}

const blockers = [];
for (const id of all.FR) if (!related(id, 'AC')) blockers.push(`${id}has no associated acceptance criteria AC`);
for (const id of all.AC) {
  if (!related(id, 'FR') && !related(id, 'NFR')) blockers.push(`${id}has no associated functional or non-functional requirementsFR/NFR`);
  if (all.TS.size > 0 && !related(id, 'TS')) blockers.push(`${id}has no associated test scenario TS`);
}
for (const id of all.TS) if (!related(id, 'AC')) blockers.push(`${id}has no associated acceptance criteria AC`);

const warnings = [];
for (const id of all.NFR) if (!related(id, 'AC')) warnings.push(`${id} has no associated acceptance criterion (AC)`);
for (const type of ['FR', 'AC']) if (all[type].size === 0) warnings.push(`${type}-xxx number not found.`);
if (all.POC.size === 0) warnings.push('No POC-xxx or SC-xxx upstream success criterion number found.');
if (all.TS.size === 0) warnings.push('TS-xxx test scenario number not found.');

const report = {
  file,
  passed: blockers.length === 0 && all.FR.size > 0 && all.AC.size > 0,
  counts: Object.fromEntries(types.map((type) => [type, all[type].size])),
  relationLines: relations.length,
  blockers,
  warnings
};

if (args.json) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`# PRD traceability check: ${path.basename(file)}`);
  console.log(`No.｜POC${all.POC.size}｜FR${all.FR.size}｜NFR${all.NFR.size}｜AC${all.AC.size}｜TS${all.TS.size}`);
  console.log(`Related lines｜${relations.length}`);
  for (const item of blockers) console.log(`Block｜${item}`);
  for (const item of warnings) console.log(`Reminder｜${item}`);
  console.log(report.passed ? 'Conclusion | Structural traceability passed; review each relationship for business correctness.' : 'Conclusion | Traceability is incomplete; do not hand off to engineering and QA.');
}

process.exit(report.passed ? 0 : 1);

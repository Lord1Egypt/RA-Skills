#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { json: false };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--json') args.json = true;
    else if (argv[i] === '--help' || argv[i] === '-h') args.help = true;
    else if (!argv[i].startsWith('--') && !args.file) args.file = argv[i];
  }
  return args;
}

function usage() {
  console.log('Usage: node validate-charter.js <poc-charter.md> [--json]');
}

const args = parseArgs(process.argv.slice(2));
if (args.help || !args.file) {
  usage();
  process.exit(args.help ? 0 : 2);
}

const file = path.resolve(args.file);
const text = fs.readFileSync(file, 'utf8');
const checks = [
  { id: 'outcome', label: 'Business outcome or validation objective', patterns: [/business\s+outcome/i, /validation\s+objective/i, /POC\s+(?:objective|goal|hypothesis)/i, /goals?\s+and\s+non-goals?/i, /must\s+prove/i, /^#{1,6}\s*(?:objective|goal|target|verification\s+goal)\s*$/im] },
  { id: 'success', label: 'Success criteria and evidence', patterns: [/success\s+criteria/i, /acceptance\s+criteria/i, /proof\s+criteria/i, /pass\s+conditions?/i] },
  { id: 'scope', label: 'Scope and non-scope', patterns: [/\bscope\b/i, /non-goals?/i, /not\s+included/i, /out\s+of\s+scope/i] },
  { id: 'commitment', label: 'Mutual ownership and commitments', patterns: [/mutual\s+commitments?/i, /responsibilit(?:y|ies)/i, /commitments?/i, /owners?/i, /RACI/i] },
  { id: 'data', label: 'Data, system, or sample readiness', patterns: [/\bdata\b/i, /samples?/i, /system\s+access/i, /environment/i] },
  { id: 'timeline', label: 'Timeline, milestones, or review cadence', patterns: [/timebox/i, /milestones?/i, /timeline/i, /review\s+cadence/i, /\bweeks?\b/i] },
  { id: 'risk', label: 'Risks, permissions, and stop conditions', patterns: [/\brisks?\b/i, /stop\s+conditions?/i, /hard\s+gates?/i, /permissions?/i, /escalation/i] },
  { id: 'decision', label: 'Continue, adjust, or stop decision', patterns: [/\bcontinue\b/i, /\badjust\b/i, /\bpause\b/i, /\bstop\b/i, /decision[- ]makers?/i] }
];

const results = checks.map((check) => ({
  id: check.id,
  label: check.label,
  passed: check.patterns.some((pattern) => pattern.test(text))
}));
const missing = results.filter((item) => !item.passed);
const ids = [...new Set(text.match(/\b(?:POC|SC)-(?:[A-Z]{1,8}-)?\d{3,}\b(?!-)/gi) || [])];
const hasThreshold = /(\d+(?:\.\d+)?\s*(?:%|seconds?|minutes?|hours?|days?|weeks?|USD|CNY|times?|users?)|[<>]=?|at\s+least|at\s+most|no\s+more\s+than|no\s+less\s+than|zero)/i.test(text);
const warnings = [];
if (ids.length === 0) warnings.push('No POC-xxx or SC-xxx success criteria numbers found, cross-ring tracking may be difficult.');
if (!hasThreshold) warnings.push('No decidable threshold or quantity found, success criteria may not be accepted.');
if (!/\[(?:OPEN|TO BE CONFIRMED|UNCONFIRMED)\]|to\s+be\s+confirmed|unconfirmed|open\s+item/i.test(text)) warnings.push('Open items are not explicitly listed; check whether assumptions were written as facts.');

const report = {
  file,
  passed: missing.length === 0,
  checks: results,
  missing: missing.map((item) => item.label),
  warnings
};

if (args.json) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`# POC Charter Check: ${path.basename(file)}`);
  for (const item of results) console.log(`${item.passed ? 'PASS' : 'MISSING'} | ${item.label}`);
  for (const warning of warnings) console.log(`WARNING | ${warning}`);
  console.log(report.passed ? 'CONCLUSION | Structural checks passed. Accountable business, technical, and risk owners must still confirm content accuracy and commitments.' : 'CONCLUSION | Blocking fields are missing. Complete them before entering PRD Handoff.');
}

process.exit(report.passed ? 0 : 1);

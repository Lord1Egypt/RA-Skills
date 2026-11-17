#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function usage() {
  console.log('Usage: node validate-skill-package.js <skill-folder> [--json]');
}

const argv = process.argv.slice(2);
const json = argv.includes('--json');
const folderArg = argv.find((item) => !item.startsWith('--'));
if (!folderArg || argv.includes('--help') || argv.includes('-h')) {
  usage();
  process.exit(folderArg ? 0 : 2);
}

const folder = path.resolve(folderArg);
const skillPath = path.join(folder, 'SKILL.md');
const blockers = [];
const warnings = [];

if (!fs.existsSync(skillPath)) blockers.push('SKILL.md is missing.');
let skill = '';
let name = '';
if (fs.existsSync(skillPath)) {
  skill = fs.readFileSync(skillPath, 'utf8');
  const frontmatter = skill.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatter) blockers.push('SKILL.md is missing valid YAML frontmatter.');
  else {
    const keys = [...frontmatter[1].matchAll(/^([a-zA-Z0-9_-]+):/gm)].map((match) => match[1]);
    const extra = keys.filter((key) => !['name', 'description'].includes(key));
    if (!keys.includes('name')) blockers.push('Frontmatter is missing name.');
    if (!keys.includes('description')) blockers.push('Frontmatter is missing description.');
    if (extra.length > 0) blockers.push(`Frontmatter contains unsupported fields: ${extra.join(', ')}.`);
    const nameMatch = frontmatter[1].match(/^name:\s*["']?([^\r\n"']+)/m);
    name = nameMatch ? nameMatch[1].trim() : '';
    if (name && !/^[a-z0-9-]{1,64}$/.test(name)) blockers.push(`name must use lowercase letters, digits, and hyphens: ${name}`);
    const folderName = path.basename(folder);
    if (name && folderName !== name && folderName !== `${name}-en`) {
      blockers.push(`Directory name ${folderName} is inconsistent with name ${name}.`);
    }
  }

  const lines = skill.split(/\r?\n/).length;
  if (lines > 500) warnings.push(`SKILL.md has ${lines} lines. Move detail to references for progressive disclosure.`);

  const linkPattern = /\[[^\]]*\]\(([^)]+)\)/g;
  for (const match of skill.matchAll(linkPattern)) {
    const target = match[1].split('#')[0];
    if (!target || /^(https?:|mailto:)/i.test(target)) continue;
    const resolved = path.resolve(folder, target);
    if (!fs.existsSync(resolved)) blockers.push(`Local link does not exist: ${target}`);
  }
}

const agentPath = path.join(folder, 'agents', 'openai.yaml');
if (!fs.existsSync(agentPath)) warnings.push('Recommended agents/openai.yaml is missing.');
else {
  const yaml = fs.readFileSync(agentPath, 'utf8');
  for (const field of ['display_name', 'short_description', 'default_prompt']) {
    if (!new RegExp(`^\\s*${field}:`, 'm').test(yaml)) warnings.push(`openai.yaml is missing ${field}.`);
  }
  if (name && !yaml.includes(`$${name}`)) warnings.push(`default_prompt may not invoke $${name} explicitly.`);
}

const report = { folder, name, passed: blockers.length === 0, blockers, warnings };
if (json) console.log(JSON.stringify(report, null, 2));
else {
  console.log(`# Skill package check: ${path.basename(folder)}`);
  for (const item of blockers) console.log(`BLOCK: ${item}`);
  for (const item of warnings) console.log(`WARNING: ${item}`);
  console.log(report.passed ? 'RESULT: structure check passed.' : 'RESULT: blocking issues found.');
}

process.exit(report.passed ? 0 : 1);

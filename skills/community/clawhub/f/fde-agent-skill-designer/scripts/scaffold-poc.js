#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function die(message) {
  console.error(`POC skeleton generation failed: ${message}`);
  process.exit(1);
}

function parseArgs(tokens) {
  const args = {};
  for (let i = 0; i < tokens.length; i += 2) {
    const key = tokens[i];
    const value = tokens[i + 1];
    if (!key || !key.startsWith('--') || !value) die('Parameter format must be --key value');
    args[key.slice(2)] = value;
  }
  return args;
}

function required(args, key) {
  if (!args[key]) die(`Missing --${key}`);
  return args[key];
}

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...walk(full));
    else files.push(full);
  }
  return files;
}

const args = parseArgs(process.argv.slice(2));
const output = path.resolve(required(args, 'output'));
const name = required(args, 'name');
const scenario = required(args, 'scenario');
const projectId = args['project-id'] || 'FDE-POC';
const template = path.resolve(__dirname, '..', 'assets', 'minimal-poc');

if (fs.existsSync(output)) die(`Target directory already exists; refusing to overwrite: ${output}`);
fs.cpSync(template, output, { recursive: true, errorOnExist: true });

const replacements = {
  '{{PROJECT_ID}}': projectId,
  '{{POC_NAME}}': name,
  '{{SCENARIO}}': scenario,
  '{{GENERATED_AT}}': new Date().toISOString()
};

for (const file of walk(output)) {
  if (!['.html', '.js', '.css', '.json', '.md'].includes(path.extname(file))) continue;
  let text = fs.readFileSync(file, 'utf8');
  for (const [token, value] of Object.entries(replacements)) text = text.split(token).join(value);
  fs.writeFileSync(file, text, 'utf8');
}

console.log(`Minimum runnable POC generated: ${output}`);
console.log(`Run evaluation: node ${path.join(output, 'evals', 'run-evals.js')}`);
console.log(`Start server: node ${path.join(output, 'server.js')}`);

#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function usage() {
  console.log(`Usage: node generate-interview-guide.js --input project.json [--output interview-guide.md]

Example input JSON:
{
  "projectName": "Customer service assistance POC",
  "goal": "Understanding the real bottlenecks in the bill interpretation task",
  "roles": [
    {"name": "Frontline customer service", "type": "user"},
    {"name": "Customer Service Supervisor", "type": "owner"},
    {"name": "security manager", "type": "technical"}
  ],
  "knownFacts": ["Average processing time 11.5 minutes"],
  "unknowns": ["What abnormal paths cause rework?"],
  "constraints": ["Only de-identification work orders can be used"]
}`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--help' || token === '-h') args.help = true;
    else if (token.startsWith('--')) args[token.slice(2)] = argv[++i];
  }
  return args;
}

function list(items, emptyText = '[To be added]') {
  if (!Array.isArray(items) || items.length === 0) return `- ${emptyText}`;
  return items.map((item) => `- ${item}`).join('\n');
}

const questionBanks = {
  user: [
    'Please recall the last time you actually completed this task: what trigger started and ended with what result?',
    'What systems, forms, messages, and human judgment are used in sequence during the process?',
    'Which steps are most often waited for, reworked, made wrong, or require confirmation from someone? Please give a recent example.',
    'How do you stay safe when encountering an unusual situation? What situations should never be handled automatically?',
    'If the new plan gives results, on what basis do you decide to accept, modify, or reject it?'
  ],
  owner: [
    'What is the business outcome this work is intended to improve? What are the current baselines and data sources?',
    'Which users, scenarios, and anomalies dominate the impact? Which ones are not worth dealing with right now?',
    'What evidence would make you decide to continue, expand, revise, or discontinue the POC?',
    'What personnel, samples, system access, and validation time can you commit?',
    'In addition to technical solutions, might training, policy or process adjustments be simpler?'
  ],
  technical: [
    'What systems, interfaces, data owners, and sources of system records are involved in the real process?',
    'What are the quality, age, geography, sensitivity level, and retention requirements for the data?',
    'What minimum permissions can a POC have? Which actions must be manually confirmed or prohibited?',
    'What are the monitoring, auditing, incident response and rollback mechanisms in place?',
    'What other security, compliance, procurement, or architectural approvals must go through to get from POC to production?'
  ]
};

function normalizeType(type) {
  const value = String(type || '').toLowerCase();
  if (['user', 'operator', 'User', 'first line'].includes(value)) return 'user';
  if (['owner', 'business', 'manager', 'business', 'person in charge'].includes(value)) return 'owner';
  return 'technical';
}

function render(project) {
  const roles = Array.isArray(project.roles) && project.roles.length > 0
    ? project.roles
    : [
        { name: 'actual users', type: 'user' },
        { name: 'Business leader', type: 'owner' },
        { name: 'Technology/Risk Leader', type: 'technical' }
      ];
  const sections = roles.map((role) => {
    const type = normalizeType(role.type);
    const custom = Array.isArray(role.evidenceGoals) && role.evidenceGoals.length > 0
      ? `\n**This character evidence target**\n${list(role.evidenceGoals)}\n`
      : '';
    return `## ${role.name}（${type}）\n${custom}\n${questionBanks[type].map((q, i) => `${i + 1}. ${q}`).join('\n')}`;
  });

  return `# ${project.projectName || 'FDE Project'} Interview Guide

## Discovery objective

${project.goal || '[To be added: Issues and evidence targets to be verified in this round]'}

## Known facts

${list(project.knownFacts)}

## Critical unknowns

${list(project.unknowns)}

## Constraints

${list(project.constraints)}

## Interview discipline

- Ask about the most recent real behavior; do not substitute hypothetical preferences for facts.
- Separate direct quotes, observations, data, inferences, and open items.
- Do not write a customer-requested feature directly as the problem.
- Record the source, role, and date for every material conclusion.
- At the end, confirm which tickets, logs, samples, or accountable owners can provide further evidence.

${sections.join('\n\n')}

## Evidence log

| Conclusion or quote | Evidence type | Source / date | Support or disconfirmation | Follow-up / owner |
|---|---|---|---|---|
| | Quote / observation / data / inference | | | |
`;
}

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  usage();
  process.exit(0);
}
if (!args.input) {
  usage();
  process.exit(2);
}

const inputPath = path.resolve(args.input);
const project = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const output = render(project);
if (args.output) {
  fs.writeFileSync(path.resolve(args.output), output, 'utf8');
  console.log(`Generated:${path.resolve(args.output)}`);
} else {
  process.stdout.write(output);
}

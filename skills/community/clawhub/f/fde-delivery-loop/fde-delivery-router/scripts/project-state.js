#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const skills = [
  'fde-problem-discovery',
  'fde-engagement-charter',
  'fde-prd-writer',
  'fde-deployment-architect',
  'fde-agent-skill-designer',
  'fde-poc-runner',
  'fde-adoption-and-value',
  'fde-playbook-productizer'
];
const statuses = new Set(['not_started', 'in_progress', 'blocked', 'passed', 'failed', 'skipped']);
const projectStatuses = new Set(['active', 'paused', 'completed', 'stopped']);
const modes = new Set(['quick_route', 'single_ring', 'end_to_end', 'audit', 'recovery']);

function die(message) {
  console.error(`Project-state operation failed: ${message}`);
  process.exit(1);
}

function parseArgs(tokens) {
  const args = { _: [] };
  for (let i = 0; i < tokens.length; i += 1) {
    const token = tokens[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const value = tokens[i + 1];
    if (!value || value.startsWith('--')) die(`Parameter --${key} is missing a value`);
    args[key] = value;
    i += 1;
  }
  return args;
}

function requireArg(args, key) {
  if (!args[key]) die(`Missing --${key}`);
  return args[key];
}

function now() {
  return new Date().toISOString();
}

function stageRecord(number) {
  return {
    skill: skills[number - 1],
    status: 'not_started',
    artifact: '',
    version: '',
    owner: '',
    gates: {
      evidence: false,
      responsibility: false,
      executable: false,
      risk: false
    },
    blockers: [],
    started_at: '',
    completed_at: ''
  };
}

function initialState(args) {
  const timestamp = now();
  const mode = args.mode || 'end_to_end';
  if (!modes.has(mode)) die(`Unsupported mode: ${mode}`);
  const stages = {};
  for (let i = 1; i <= 8; i += 1) stages[String(i)] = stageRecord(i);
  return {
    schema_version: '1.0',
    revision: 0,
    project: {
      id: requireArg(args, 'project-id'),
      name: requireArg(args, 'name'),
      customer: args.customer || '',
      scenario: args.scenario || '',
      profile: args.profile || 'mixed',
      mode,
      status: 'active',
      created_at: timestamp,
      updated_at: timestamp
    },
    current_stage: 1,
    stages,
    decisions: [],
    risks: [],
    next_action: {
      skill: 'fde-problem-discovery',
      owner: 'FDE',
      action: 'Gather and verify evidence of customer issues',
      completion_condition: 'Create a documented problem discovery package'
    }
  };
}

function readState(file) {
  if (!fs.existsSync(file)) die(`File does not exist: ${file}`);
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    die(`Unable to read JSON: ${error.message}`);
  }
}

function eventFile(file) {
  return path.join(path.dirname(file), 'fde-events.jsonl');
}

function stateHash(state) {
  return crypto.createHash('sha256').update(JSON.stringify(state)).digest('hex');
}

function appendEvent(file, state, event) {
  const record = {
    schema_version: '1.0',
    event_id: crypto.randomUUID(),
    project_id: state.project.id,
    revision: state.revision,
    occurred_at: state.project.updated_at,
    actor: event.actor || 'unknown',
    type: event.type,
    reason: event.reason || '',
    changes: event.changes || {},
    state_sha256: stateHash(state)
  };
  fs.appendFileSync(eventFile(file), `${JSON.stringify(record)}\n`, 'utf8');
}

function writeState(file, state, event) {
  state.revision = Number.isInteger(state.revision) ? state.revision + 1 : 1;
  state.project.updated_at = now();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(state, null, 2)}\n`, 'utf8');
  appendEvent(file, state, event);
}

function parseBoolean(value, label) {
  if (value === 'true') return true;
  if (value === 'false') return false;
  die(`${label} can only be true or false`);
}

function validateState(state, file) {
  const errors = [];
  const warnings = [];
  if (state.schema_version !== '1.0') errors.push('schema_version must be 1.0');
  if (!Number.isInteger(state.revision) || state.revision < 0) errors.push('revision must be a non-negative integer');
  if (!state.project || !state.project.id || !state.project.name) errors.push('project.id and project.name are required');
  if (state.project && !projectStatuses.has(state.project.status)) errors.push(`Unsupported project.status: ${state.project.status}`);
  if (state.project && !modes.has(state.project.mode)) errors.push(`Unsupported project.mode: ${state.project.mode}`);
  if (!Number.isInteger(state.current_stage) || state.current_stage < 1 || state.current_stage > 8) errors.push('current_stage must be 1–8');
  if (!state.stages || typeof state.stages !== 'object') errors.push('missing stages');

  for (let i = 1; i <= 8; i += 1) {
    const record = state.stages && state.stages[String(i)];
    if (!record) {
      errors.push(`Missing status for Ring ${i}`);
      continue;
    }
    if (record.skill !== skills[i - 1]) errors.push(`Ring ${i} should use ${skills[i - 1]}`);
    if (!statuses.has(record.status)) errors.push(`Ring ${i} has an unsupported status: ${record.status}`);
    if (!Array.isArray(record.blockers)) errors.push(`Ring ${i} blockers must be an array`);
    if (record.status === 'passed') {
      if (!record.artifact) errors.push(`Ring ${i} passed but its artifact is missing`);
      if (!record.version) errors.push(`Ring ${i} passed but its version is missing`);
      if (!record.owner) errors.push(`Ring ${i} passed but its owner is missing`);
      for (const gate of ['evidence', 'responsibility', 'executable', 'risk']) {
        if (!record.gates || record.gates[gate] !== true) errors.push(`Ring ${i} passed but the ${gate} gate failed.`);
      }
      if (record.artifact && !/^[a-z]+:\/\//i.test(record.artifact)) {
        const artifact = path.resolve(path.dirname(file), record.artifact);
        if (!fs.existsSync(artifact)) errors.push(`Ring ${i} artifact does not exist: ${record.artifact}`);
      }
    }
    if (record.status === 'blocked' && record.blockers.length === 0) warnings.push(`Ring ${i} is blocked but has no recorded blocker.`);
    if (record.status === 'skipped' && record.blockers.length === 0) warnings.push(`Ring ${i} was skipped but has no recorded reason.`);
  }

  if (!state.next_action || !skills.includes(state.next_action.skill)) errors.push('next_action.skill must be one of eight sub-skills');
  if (!Array.isArray(state.decisions)) errors.push('decisions must be an array');
  if (!Array.isArray(state.risks)) errors.push('risks must be an array');
  return { errors, warnings };
}

function validateEvents(state, file) {
  const errors = [];
  const warnings = [];
  const log = eventFile(file);
  if (!fs.existsSync(log)) {
    warnings.push('fde-events.jsonl is missing; only the current status snapshot is available, without an append-only change history.');
    return { errors, warnings };
  }
  const lines = fs.readFileSync(log, 'utf8').split(/\r?\n/).filter(Boolean);
  if (lines.length === 0) {
    errors.push('fde-events.jsonl is empty');
    return { errors, warnings };
  }
  let previousRevision = null;
  const ids = new Set();
  const events = [];
  for (let index = 0; index < lines.length; index += 1) {
    let item;
    try {
      item = JSON.parse(lines[index]);
    } catch (error) {
      errors.push(`Event log line ${index + 1} is not valid JSON`);
      continue;
    }
    events.push(item);
    if (item.schema_version !== '1.0') errors.push(`Event ${item.event_id || index + 1} has an unsupported schema_version`);
    if (!item.event_id || ids.has(item.event_id)) errors.push(`Missing or duplicate event ID:${item.event_id || index + 1}`);
    ids.add(item.event_id);
    if (item.project_id !== state.project.id) errors.push(`Event ${item.event_id} project_id does not match the state file`);
    if (!Number.isInteger(item.revision) || item.revision < 0 || (previousRevision !== null && item.revision <= previousRevision)) {
      errors.push(`Event ${item.event_id} revision is not strictly increasing`);
    }
    if (Number.isInteger(item.revision)) previousRevision = item.revision;
    if (!item.actor || item.actor === 'unknown') warnings.push(`Event ${item.event_id} is missing an explicit actor`);
    if (!item.type) errors.push(`Event ${item.event_id} is missing type`);
    if (!item.reason) warnings.push(`Event ${item.event_id} is missing reason`);
    if (!/^[a-f0-9]{64}$/.test(item.state_sha256 || '')) errors.push(`Event${item.event_id}Missing legal state_sha256`);
  }
  const last = events[events.length - 1];
  if (last) {
    if (last.revision !== state.revision) errors.push(`The last event revision${last.revision}is inconsistent with the status revision${state.revision}`);
    if (last.state_sha256 !== stateHash(state)) errors.push('The status check value of the last event is inconsistent with the current snapshot');
  }
  return { errors, warnings };
}

function showStatus(state) {
  console.log(`${state.project.id}｜${state.project.name}｜${state.project.status}｜revision ${state.revision}`);
  console.log('Stage Status Skill Version Owner');
  for (let i = 1; i <= 8; i += 1) {
    const item = state.stages[String(i)];
    console.log(`${String(i).padEnd(5)} ${item.status.padEnd(13)} ${item.skill.padEnd(28)} ${(item.version || '-').padEnd(9)} ${item.owner || '-'}`);
  }
  console.log(`Next skill: ${state.next_action.skill}`);
  console.log(`Next action: ${state.next_action.action || '-'}`);
  console.log(`Completion condition: ${state.next_action.completion_condition || '-'}`);
}

function showHistory(file) {
  const log = eventFile(file);
  if (!fs.existsSync(log)) die(`Event log does not exist:${log}`);
  const events = fs.readFileSync(log, 'utf8').split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line));
  for (const item of events) {
    console.log(`r${item.revision}｜${item.occurred_at}｜${item.type}｜${item.actor}｜${item.reason}`);
  }
}

const [command, ...rest] = process.argv.slice(2);
const args = parseArgs(rest);
const file = args.file ? path.resolve(args.file) : '';

if (command === 'init') {
  requireArg(args, 'file');
  if (fs.existsSync(file)) die(`The target already exists and overwrite is refused:${file}`);
  if (fs.existsSync(eventFile(file))) die(`Event log already exists, refusing to mix in old projects:${eventFile(file)}`);
  const state = initialState(args);
  writeState(file, state, {
    type: 'project_initialized',
    actor: args.actor || 'FDE',
    reason: args.reason || 'Create FDE project status',
    changes: { mode: state.project.mode, current_stage: 1 }
  });
  console.log(`Created project status:${file}`);
} else if (command === 'set-stage') {
  requireArg(args, 'file');
  const state = readState(file);
  const stage = Number(requireArg(args, 'stage'));
  if (!Number.isInteger(stage) || stage < 1 || stage > 8) die('--stage must be between 1 and 8');
  const status = requireArg(args, 'status');
  if (!statuses.has(status)) die(`Unsupported status:${status}`);
  const record = state.stages[String(stage)];
  const previousStatus = record.status;
  record.status = status;
  if (args.artifact) record.artifact = args.artifact;
  if (args.version) record.version = args.version;
  if (args.owner) record.owner = args.owner;
  if (args.blocker && !record.blockers.includes(args.blocker)) record.blockers.push(args.blocker);
  if (args['clear-blockers'] === 'true') record.blockers = [];
  if (args.gates === 'pass') {
    for (const gate of Object.keys(record.gates)) record.gates[gate] = true;
  }
  for (const gate of ['evidence', 'responsibility', 'executable', 'risk']) {
    const key = `gate-${gate}`;
    if (args[key]) record.gates[gate] = parseBoolean(args[key], `--${key}`);
  }
  if (status === 'in_progress' && !record.started_at) record.started_at = now();
  if (status === 'passed' || status === 'skipped') record.completed_at = now();
  if (status !== 'passed' && status !== 'skipped') record.completed_at = '';
  state.current_stage = stage;
  writeState(file, state, {
    type: 'stage_status_changed',
    actor: requireArg(args, 'actor'),
    reason: requireArg(args, 'reason'),
    changes: { stage, skill: record.skill, from: previousStatus, to: status, artifact: record.artifact, version: record.version }
  });
  console.log(`Updated Stage ${stage}: ${status}`);
} else if (command === 'set-next') {
  requireArg(args, 'file');
  const state = readState(file);
  const skill = requireArg(args, 'skill');
  if (!skills.includes(skill)) die(`Unsupported skill:${skill}`);
  const previousSkill = state.next_action && state.next_action.skill;
  state.next_action = {
    skill,
    owner: requireArg(args, 'owner'),
    action: args.action || `Execute${skill}`,
    completion_condition: requireArg(args, 'condition')
  };
  state.current_stage = skills.indexOf(skill) + 1;
  writeState(file, state, {
    type: 'next_action_changed',
    actor: requireArg(args, 'actor'),
    reason: requireArg(args, 'reason'),
    changes: { from: previousSkill || '', to: skill, owner: state.next_action.owner, completion_condition: state.next_action.completion_condition }
  });
  console.log(`The next skill has been set to:${skill}`);
} else if (command === 'add-decision') {
  requireArg(args, 'file');
  const state = readState(file);
  const id = requireArg(args, 'id');
  if (state.decisions.some((item) => item.id === id)) die(`Decision ID already exists:${id}`);
  state.decisions.push({
    id,
    summary: requireArg(args, 'summary'),
    status: args.status || 'confirmed',
    evidence: args.evidence || '',
    owner: args.owner || '',
    decided_at: args.date || now()
  });
  writeState(file, state, {
    type: 'decision_recorded',
    actor: requireArg(args, 'actor'),
    reason: args.reason || args.summary,
    changes: { decision_id: id, status: args.status || 'confirmed' }
  });
  console.log(`Decision added:${id}`);
} else if (command === 'status') {
  requireArg(args, 'file');
  showStatus(readState(file));
} else if (command === 'history') {
  requireArg(args, 'file');
  showHistory(file);
} else if (command === 'validate') {
  requireArg(args, 'file');
  const state = readState(file);
  const stateResult = validateState(state, file);
  const eventResult = validateEvents(state, file);
  const errors = [...stateResult.errors, ...eventResult.errors];
  const warnings = [...stateResult.warnings, ...eventResult.warnings];
  for (const warning of warnings) console.log(`Reminder｜${warning}`);
  if (errors.length > 0) die(`${errors.length}Item error\n-${errors.join('\n- ')}`);
  console.log(`Project-state validation passed: ${file}`);
} else {
  die('Command must be init, set-stage, set-next, add-decision, status, history, or validate');
}

#!/usr/bin/env node
// abi-diff.js — Compare two ABI files and report added, removed, and changed entries
// Usage: node abi-diff.js <old.json> <new.json>
//
// Accepts:
//   - Raw ABI arrays:        [{ type: "function", name: "transfer", ... }]
//   - Foundry artifacts:     { "abi": [...], "bytecode": "...", ... }
//   - Hardhat artifacts:     { "abi": [...], "bytecode": "...", ... }
//
// Outputs JSON: { added, removed, changed, breaking, summary }
// Exit code 0 = no breaking changes. Exit code 1 = breaking changes found. Exit code 2 = error.

'use strict';

const fs = require('fs');
const path = require('path');

const [oldPath, newPath] = process.argv.slice(2);

if (!oldPath || !newPath) {
  console.error('Usage: node abi-diff.js <old.json> <new.json>');
  process.exit(2);
}

function loadABI(filePath) {
  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    throw new Error(`File not found: ${absPath}`);
  }
  let data;
  try {
    data = JSON.parse(fs.readFileSync(absPath, 'utf8'));
  } catch (e) {
    throw new Error(`Invalid JSON in ${filePath}: ${e.message}`);
  }
  // Auto-detect: Foundry/Hardhat artifact or raw array
  if (Array.isArray(data)) return data;
  if (data.abi && Array.isArray(data.abi)) return data.abi;
  throw new Error(`Cannot find ABI in ${filePath}. Expected an array or object with .abi array.`);
}

// Create a unique key for an ABI entry: "type:name" (functions, events, errors by name+type)
function entryKey(entry) {
  if (entry.type === 'constructor' || entry.type === 'receive' || entry.type === 'fallback') {
    return entry.type; // these don't have a name
  }
  return `${entry.type}:${entry.name}`;
}

// Serialize inputs/outputs for comparison (name-agnostic would be an option,
// but we include names since name changes break TypeScript bindings too)
function serializeParams(params) {
  if (!params || params.length === 0) return '[]';
  return JSON.stringify(params.map(p => ({
    name:       p.name || '',
    type:       p.type,
    components: p.components ? serializeParams(p.components) : undefined,
    indexed:    p.indexed,
  })));
}

function serializeEntry(entry) {
  return JSON.stringify({
    inputs:          serializeParams(entry.inputs),
    outputs:         serializeParams(entry.outputs),
    stateMutability: entry.stateMutability || '',
    anonymous:       entry.anonymous || false,
  });
}

// Determine if a change is breaking
function isBreaking(oldEntry, newEntry) {
  // Function removed = breaking (handled separately)
  // Inputs changed = breaking (callers will send wrong data)
  if (serializeParams(oldEntry.inputs) !== serializeParams(newEntry.inputs)) return true;
  // stateMutability: payable→nonpayable is breaking for callers sending value
  if (oldEntry.stateMutability !== newEntry.stateMutability) {
    const breakingMutChanges = [
      ['payable', 'nonpayable'],
      ['nonpayable', 'payable'], // callers might not send value now needed
      ['view', 'nonpayable'],
      ['pure', 'nonpayable'],
    ];
    for (const [from, to] of breakingMutChanges) {
      if (oldEntry.stateMutability === from && newEntry.stateMutability === to) return true;
    }
  }
  return false;
}

let oldABI, newABI;
try {
  oldABI = loadABI(oldPath);
  newABI = loadABI(newPath);
} catch (e) {
  console.error(`Error: ${e.message}`);
  process.exit(2);
}

// Build lookup maps
const oldMap = new Map();
const newMap = new Map();

for (const entry of oldABI) {
  if (!entry.type) continue; // skip malformed
  const key = entryKey(entry);
  oldMap.set(key, entry);
}
for (const entry of newABI) {
  if (!entry.type) continue;
  const key = entryKey(entry);
  newMap.set(key, entry);
}

const added   = [];
const removed = [];
const changed = [];
let breaking  = false;

// Find removed and changed
for (const [key, oldEntry] of oldMap) {
  if (!newMap.has(key)) {
    removed.push({ type: oldEntry.type, name: oldEntry.name || null });
    // Removing a function/event/error is always breaking
    if (oldEntry.type === 'function' || oldEntry.type === 'constructor') {
      breaking = true;
    }
  } else {
    const newEntry = newMap.get(key);
    if (serializeEntry(oldEntry) !== serializeEntry(newEntry)) {
      const entryBreaking = isBreaking(oldEntry, newEntry);
      if (entryBreaking) breaking = true;
      changed.push({
        type:     oldEntry.type,
        name:     oldEntry.name || null,
        breaking: entryBreaking,
        old: {
          inputs:          oldEntry.inputs  || [],
          outputs:         oldEntry.outputs || [],
          stateMutability: oldEntry.stateMutability || '',
        },
        new: {
          inputs:          newEntry.inputs  || [],
          outputs:         newEntry.outputs || [],
          stateMutability: newEntry.stateMutability || '',
        },
      });
    }
  }
}

// Find added
for (const [key, newEntry] of newMap) {
  if (!oldMap.has(key)) {
    added.push({ type: newEntry.type, name: newEntry.name || null });
  }
}

const summary = `${added.length} added, ${removed.length} removed, ${changed.length} changed`;

const output = {
  added,
  removed,
  changed,
  breaking,
  summary,
};

console.log(JSON.stringify(output, null, 2));

// Exit 1 if breaking changes — useful in CI
process.exit(breaking ? 1 : 0);

#!/usr/bin/env node

const path = require('path');
const { spawnSync } = require('child_process');

const args = process.argv.slice(2);
const allowedCommands = new Set([
  'auth',
  'login',
  'status',
  'logout',
  'config',
  'doctor',
  'search',
  'tools',
  'cart',
  'address',
  'coupon',
  'order',
  'logistics',
  'aftersale',
  'after-sale',
  'checkout',
  'help',
]);
const blockedFlags = new Set([
  '--authorize-url',
  '--token-url',
  '--client-id',
  '--client-secret',
  '--redirect-port',
  '--show-secrets',
  '--buyer-base-url',
]);

function fail(message) {
  console.error(message);
  process.exit(2);
}

function validateArgs(argv) {
  const command = argv.find((arg) => !arg.startsWith('-')) || 'help';
  if (!allowedCommands.has(command)) {
    fail('This ClawHub skill only exposes the Filtalgo shopping commands. Developer/raw API commands are not available here.');
  }

  for (const flag of blockedFlags) {
    if (argv.includes(flag)) {
      fail(`Option ${flag} is not available in the ClawHub shopping skill.`);
    }
  }

  if (command === 'config') {
    const sub = argv[1] || 'show';
    if (sub === 'show') return;
    if ((sub === 'reset' || sub === 'use') && (argv[2] || 'remote-dev') === 'remote-dev') return;
    fail('This ClawHub skill only allows "config show" and "config reset remote-dev".');
  }
}

validateArgs(args);

const cli = path.join(__dirname, '..', 'assets', 'filtalgo-cli.cjs');
const result = spawnSync(process.execPath, [cli, ...args], {
  stdio: 'inherit',
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status === null ? 1 : result.status);

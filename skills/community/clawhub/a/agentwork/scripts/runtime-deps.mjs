#!/usr/bin/env node

import { checkNodePackage, installNodePackage } from './runtime-node-packages.mjs';

function output(payload) {
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

function fail(errorCode, message, details = {}) {
  process.stderr.write(`${JSON.stringify({ error: errorCode, message, details })}\n`);
  process.exit(1);
}

const command = process.argv[2];
const packageAlias = process.argv[3];

if (!command || !packageAlias) {
  fail('USAGE', 'Usage: node runtime-deps.mjs <check|install> <package>');
}

if (command !== 'check' && command !== 'install') {
  fail('UNKNOWN_COMMAND', `Unknown command "${command}". Valid commands: check, install`);
}

if (command === 'check') {
  try {
    const status = await checkNodePackage(packageAlias);
    output(status);
    process.exit(0);
  } catch (error) {
    fail(error?.code ?? 'CHECK_FAILED', error?.message ?? 'Failed to check runtime dependency', error?.details ?? {});
  }
}

try {
  const installed = await installNodePackage(packageAlias);
  const checked = await checkNodePackage(packageAlias);
  if (!checked.ok) {
    fail(
      'POST_INSTALL_CHECK_FAILED',
      `Installed ${packageAlias}, but the runtime compatibility check still failed`,
      {
        package: packageAlias,
        install: installed,
        check: checked,
      },
    );
  }
  output({
    ...installed,
    check: checked,
  });
} catch (error) {
  fail(error?.code ?? 'INSTALL_FAILED', error?.message ?? 'Failed to install runtime dependency', error?.details ?? {});
}

'use strict';

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const SCRIPTS_DIR = path.join(__dirname, '..', 'scripts');

const EXIT_SUCCESS = 0;
const EXIT_RUNTIME_ERROR = 1;
const EXIT_VALIDATION_ERROR = 2;
const EXIT_NOT_AUTHORIZED = 10;

const NOT_AUTHORIZED_MESSAGE =
  'Contacts access not granted. Run "apcli setup", then allow your terminal (and/or "osascript") in System Settings > Privacy & Security > Contacts.';

function isAuthorizationError(stderr) {
  return (
    stderr.includes('-1743') ||
    stderr.includes('-1744') ||
    stderr.includes('CNErrorDomain') ||
    stderr.toLowerCase().includes('not authorized')
  );
}

function exitCodeFor(code) {
  if (code === 'NOT_AUTHORIZED') return EXIT_NOT_AUTHORIZED;
  if (code === 'INVALID_ARGUMENT' || code === 'MISSING_REQUIRED') return EXIT_VALIDATION_ERROR;
  return EXIT_RUNTIME_ERROR;
}

/**
 * Run scripts/<name>.jxa with `args` injected as `__args`. Resolves, never
 * rejects: { success, data } or { success: false, error: { code, message }, exitCode }.
 */
function runScript(name, args = {}) {
  return new Promise((resolve) => {
    const file = path.join(SCRIPTS_DIR, `${name}.jxa`);
    if (!fs.existsSync(file)) {
      resolve({
        success: false,
        error: { code: 'JXA_ERROR', message: `Script not found: ${name}.jxa` },
        exitCode: EXIT_RUNTIME_ERROR,
      });
      return;
    }
    const shared = fs.readFileSync(path.join(SCRIPTS_DIR, '_contacts.jxa'), 'utf8');
    const script = `var __args = ${JSON.stringify(args)};\n${shared}\n${fs.readFileSync(file, 'utf8')}`;
    const proc = spawn('osascript', ['-l', 'JavaScript', '-e', script]);
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', (d) => (stdout += d));
    proc.stderr.on('data', (d) => (stderr += d));
    proc.on('error', (err) =>
      resolve({
        success: false,
        error: { code: 'JXA_ERROR', message: `Failed to execute osascript: ${err.message}` },
        exitCode: EXIT_RUNTIME_ERROR,
      }),
    );
    proc.on('close', (code) => {
      if (isAuthorizationError(stderr)) {
        resolve({
          success: false,
          error: { code: 'NOT_AUTHORIZED', message: NOT_AUTHORIZED_MESSAGE },
          exitCode: EXIT_NOT_AUTHORIZED,
        });
        return;
      }
      const out = stdout.trim();
      if (!out) {
        resolve({
          success: false,
          error: { code: 'JXA_ERROR', message: stderr.trim() || `Script exited with code ${code}` },
          exitCode: EXIT_RUNTIME_ERROR,
        });
        return;
      }
      try {
        const data = JSON.parse(out);
        if (data.ok === false && data.error) {
          resolve({ success: false, error: data.error, exitCode: exitCodeFor(data.error.code) });
        } else {
          resolve({ success: true, data, exitCode: EXIT_SUCCESS });
        }
      } catch {
        resolve({
          success: false,
          error: { code: 'PARSE_ERROR', message: `Failed to parse JXA output: ${out.slice(0, 200)}` },
          exitCode: EXIT_RUNTIME_ERROR,
        });
      }
    });
  });
}

module.exports = {
  runScript,
  NOT_AUTHORIZED_MESSAGE,
  EXIT_SUCCESS,
  EXIT_RUNTIME_ERROR,
  EXIT_VALIDATION_ERROR,
  EXIT_NOT_AUTHORIZED,
};

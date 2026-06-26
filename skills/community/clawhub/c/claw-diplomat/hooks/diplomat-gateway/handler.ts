/**
 * claw-diplomat — hooks/diplomat-gateway/handler.ts
 *
 * Event: gateway:startup
 * Spawns skills/claw-diplomat/listener.py as a detached background process.
 * Writes the PID to skills/claw-diplomat/listener.pid.
 *
 * fail_open: false — this hook is critical. If listener.py cannot start,
 * the gateway should surface the error to the user.
 *
 * Security: only spawns the declared listener.py script, no shell interpretation.
 */

import type { OpenClawHookEvent, OpenClawHookContext } from '@openclaw/sdk';
import * as path from 'path';
import * as fs from 'fs';

export async function handler(
  event: OpenClawHookEvent,
  ctx: OpenClawHookContext
): Promise<void> {
  const workspaceRoot = process.env.DIPLOMAT_WORKSPACE ?? process.cwd();
  const listenerPath  = path.join(workspaceRoot, 'skills', 'claw-diplomat', 'listener.py');
  const pidPath       = path.join(workspaceRoot, 'skills', 'claw-diplomat', 'listener.pid');

  if (!fs.existsSync(listenerPath)) {
    throw new Error(
      `claw-diplomat listener not found at ${listenerPath}. ` +
      `Was the skill installed correctly? ` +
      `Run: clawhub install claw-diplomat`
    );
  }

  // Check if listener is already running (stale PID guard)
  if (fs.existsSync(pidPath)) {
    const existingPid = parseInt(fs.readFileSync(pidPath, 'utf-8').trim(), 10);
    if (!isNaN(existingPid)) {
      try {
        // process.kill with signal 0 checks if process exists without killing it
        process.kill(existingPid, 0);
        ctx.log('INFO', `claw-diplomat listener already running with PID ${existingPid}`);
        return; // Already running — do not spawn a second instance
      } catch {
        // Process not running — PID file is stale, proceed to spawn
        ctx.log('DEBUG', `Stale PID file found (${existingPid}) — spawning new listener`);
      }
    }
  }

  // Build a minimal environment — DIPLOMAT_* vars + bare essentials for python3.
  // Do NOT inherit the full process.env: that would expose any secrets (API keys,
  // cloud credentials, SSH agent sockets) present in the gateway's environment.
  // SECURITY: only DIPLOMAT_*, PATH, HOME, PYTHONPATH, VIRTUAL_ENV are forwarded.
  const minimalEnv: Record<string, string> = {};
  for (const [k, v] of Object.entries(process.env)) {
    if (
      k.startsWith('DIPLOMAT_') ||
      k === 'PATH' ||
      k === 'HOME' ||
      k === 'PYTHONPATH' ||
      k === 'VIRTUAL_ENV' ||
      k === 'PYTHONHOME'
    ) {
      if (v !== undefined) minimalEnv[k] = v;
    }
  }
  // Always ensure workspace is set so listener.py can find its files
  minimalEnv['DIPLOMAT_WORKSPACE'] = workspaceRoot;

  // Dynamically import the process-launch module at runtime.
  // This is an intentional, declared process spawn — see HOOK.md (spawns_process: true).
  // Purpose: start listener.py as a detached background process for inbound P2P connections.
  // Environment: isolated (minimalEnv above) — no secrets forwarded.
  // openclaw:allow process_launch — declared in HOOK.md
  const launcher = await import('child_process');
  const child = launcher.spawn('python3', [listenerPath], {
    env:      minimalEnv,
    detached: true,
    stdio:    'ignore',
  });
  child.unref();

  if (child.pid === undefined) {
    throw new Error(
      'claw-diplomat listener failed to start (python3 not found or listener.py has an error). ' +
      'Ensure Python 3.10+ is installed and run: pip3 install PyNaCl noiseprotocol websockets'
    );
  }

  fs.writeFileSync(pidPath, String(child.pid), 'utf-8');
  ctx.log('INFO', `claw-diplomat listener started with PID ${child.pid}`);
}

/**
 * lock.mjs — Simple PID-based lockfile to prevent parallel runs
 */
import { existsSync, readFileSync, writeFileSync, unlinkSync } from 'fs';
import { resolve } from 'path';

export function acquireLock(name, dataDir) {
  const lockFile = resolve(dataDir, `${name}.lock`);

  if (existsSync(lockFile)) {
    const pid = parseInt(readFileSync(lockFile, 'utf8').trim(), 10);
    // Check if that process is still alive
    try {
      process.kill(pid, 0); // signal 0 = check existence only
      console.error(`⚠️  ${name} already running (PID ${pid}). Exiting.`);
      process.exit(0);
    } catch {
      // Stale lock — process is gone, safe to continue
      console.warn(`🔓 Stale lock found (PID ${pid}), clearing.`);
    }
  }

  writeFileSync(lockFile, String(process.pid));

  // Release lock on exit (normal or crash)
  const release = () => {
    try { unlinkSync(lockFile); } catch {}
  };

  // Graceful shutdown — call registered cleanup before exiting
  const shutdownHandlers = [];
  const shutdown = (code) => {
    console.log(`\n⚠️  ${name}: signal received, shutting down gracefully...`);
    // Run handlers sequentially, then exit
    (async () => {
      for (const fn of shutdownHandlers) {
        try { await fn(); } catch {}
      }
      release();
      process.exit(code);
    })();
  };

  process.on('exit', release);
  process.on('SIGINT', () => shutdown(130));
  process.on('SIGTERM', () => shutdown(143));

  return { release, onShutdown: (fn) => shutdownHandlers.push(fn) };
}

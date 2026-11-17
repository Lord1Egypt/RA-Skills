#!/usr/bin/env node
const { archiveProfile, exportProfile, statusProfile, doctor, ArchiveError, DeferredError, redactSignedUrls, VERSION } = require('../src/index.js');
const COMMANDS = new Set(['doctor', 'archive', 'export', 'status', 'help', 'version', '--help', '--version']);
function allowedFlags(cmd) {
  if (cmd === 'doctor') return new Set(['attachCdp']);
  if (cmd === 'status') return new Set(['output','json']);
  if (cmd === 'archive') return new Set(['output','mode','categories','mediaTypes','zip','overwriteZip','maxPages','maxTimeMs','maxBytes','maxZipBytes','maxZipEntries','maxZipFiles','delayMs','networkTimeoutMs','browserExecutable','browserChannel','attachCdp','json']);
  if (cmd === 'export') return new Set(['output','zip','overwriteZip','maxZipBytes','maxZipEntries','maxZipFiles','json']);
  return new Set();
}
function parse(argv) {
  const cmd = argv[0];
  if (!cmd) return { cmd: 'help' };
  if (!COMMANDS.has(cmd)) throw new ArchiveError('BAD_ARGS', 'unknown command: ' + cmd);
  const opts = { cmd };
  let i = 1;
  if ((cmd === 'archive' || cmd === 'status' || cmd === 'export') && argv[i] && !argv[i].startsWith('--')) opts.handle = argv[i++];
  for (; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) throw new ArchiveError('BAD_ARGS', 'unexpected positional argument: ' + a);
    const key = a.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    if (!allowedFlags(cmd).has(key)) throw new ArchiveError('BAD_ARGS', a + ' is not valid for ' + cmd);
    const bools = new Set(['json', 'overwriteZip']);
    if (bools.has(key)) { opts[key] = true; continue; }
    if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) throw new ArchiveError('BAD_ARGS', a + ' requires a value');
    opts[key] = argv[++i];
  }
  return opts;
}
function num(opts, key, d) {
  if (opts[key] == null) return d;
  const n = Number(opts[key]);
  if (!Number.isFinite(n) || n < 0) throw new ArchiveError('BAD_ARGS', '--' + key.replace(/[A-Z]/g, c => '-' + c.toLowerCase()) + ' must be a non-negative number');
  return n;
}
function usage(code) {
  console.log('Usage:\n  frameferry doctor [--attach-cdp http://127.0.0.1:9222]\n  frameferry archive <handle> --output <path> [--mode full|sync] [--categories posts,reels,stories,highlights|all] [--media-types image,video] [--zip <dest.zip>]\n  frameferry export <handle> --output <path> --zip <dest.zip> [--overwrite-zip]\n  frameferry status <handle> --output <path>');
  process.exitCode = code;
}
(async () => {
  const opts = parse(process.argv.slice(2));
  if (opts.cmd === 'help' || opts.cmd === '--help') return usage(0);
  if (opts.cmd === 'version' || opts.cmd === '--version') { console.log(VERSION); return; }
  if (opts.cmd === 'doctor') {
    const r = await doctor(opts);
    console.log(JSON.stringify(r, null, 2));
    if (!r.ok) process.exitCode = 1;
    return;
  }
  if ((opts.cmd === 'archive' || opts.cmd === 'status' || opts.cmd === 'export') && !opts.handle) throw new ArchiveError('BAD_ARGS', opts.cmd + ' requires <handle>');
  if (opts.cmd === 'status') {
    const s = await statusProfile({ handle: opts.handle, output: opts.output });
    console.log(opts.json ? JSON.stringify(s) : JSON.stringify(s, null, 2));
    process.exitCode = s.status === 'COMPLETE' ? 0 : 1;
    return;
  }
  if (opts.cmd === 'export') {
    const s = await exportProfile({ handle: opts.handle, output: opts.output, zip: opts.zip, overwriteZip: !!opts.overwriteZip, maxZipBytes: num(opts, 'maxZipBytes', undefined), maxZipEntries: num(opts, 'maxZipEntries', undefined), maxZipFiles: num(opts, 'maxZipFiles', undefined) });
    console.log(opts.json ? JSON.stringify(s) : JSON.stringify(s, null, 2));
    return;
  }
  if (opts.cmd === 'archive') {
    const s = await archiveProfile({ handle: opts.handle, output: opts.output, mode: opts.mode || 'full', categories: opts.categories, mediaTypes: opts.mediaTypes, zip: opts.zip, overwriteZip: !!opts.overwriteZip, maxPages: num(opts, 'maxPages', 12), maxTimeMs: num(opts, 'maxTimeMs', 600000), maxBytes: num(opts, 'maxBytes', 50*1024*1024), maxZipBytes: num(opts, 'maxZipBytes', undefined), maxZipEntries: num(opts, 'maxZipEntries', undefined), maxZipFiles: num(opts, 'maxZipFiles', undefined), delayMs: num(opts, 'delayMs', 500), networkTimeoutMs: num(opts, 'networkTimeoutMs', undefined), browserExecutable: opts.browserExecutable, browserChannel: opts.browserChannel, attachCdp: opts.attachCdp });
    if (opts.zip) {
      const exported = await exportProfile({ handle: opts.handle, output: opts.output, zip: opts.zip, overwriteZip: !!opts.overwriteZip, maxZipBytes: num(opts, 'maxZipBytes', undefined), maxZipEntries: num(opts, 'maxZipEntries', undefined), maxZipFiles: num(opts, 'maxZipFiles', undefined) });
      s.zip = exported;
    }
    console.log(opts.json ? JSON.stringify(s) : JSON.stringify(s, null, 2));
    process.exitCode = s.status === 'COMPLETE' ? 0 : 1;
    return;
  }
  usage(1);
})().catch(err => {
  const status = err instanceof DeferredError ? 'DEFERRED' : err instanceof ArchiveError ? err.code : 'FAILED';
  console.error(JSON.stringify({ status, error: redactSignedUrls(err.message), ...(err.details || {}) }, null, 2));
  process.exitCode = 1;
});
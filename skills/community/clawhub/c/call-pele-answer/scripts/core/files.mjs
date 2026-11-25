// files.mjs — every file pe writes on its own (logs, cache, drafts, state) is private to the user:
// directories 0700, files 0600, temp files under one per-user directory instead of loose in /tmp.
import { mkdirSync, writeFileSync, appendFileSync, chmodSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { tmpdir, userInfo } from 'node:os';

const uid = () => { try { return userInfo().uid; } catch { return 'u'; } };
export function privateDir(d) { mkdirSync(d, { recursive: true, mode: 0o700 }); try { chmodSync(d, 0o700); } catch {} return d; }
export function writePrivate(p, data) { privateDir(dirname(p)); writeFileSync(p, data, { mode: 0o600 }); try { chmodSync(p, 0o600); } catch {} }
export function appendPrivate(p, data) { privateDir(dirname(p)); appendFileSync(p, data, { mode: 0o600 }); try { chmodSync(p, 0o600); } catch {} }
export const TMP_DIR = join(tmpdir(), `call-pele-answer-${uid()}`);
export const tmpFile = (prefix, ext = 'md') => join(privateDir(TMP_DIR), `${prefix}-${Date.now()}.${ext}`);

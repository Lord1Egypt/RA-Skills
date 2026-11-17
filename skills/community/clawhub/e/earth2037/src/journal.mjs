import { mkdirSync, readFileSync, writeFileSync, renameSync, openSync, closeSync, fsyncSync } from 'node:fs';
import { createHash, randomUUID } from 'node:crypto';
import { join } from 'node:path';
import { format } from 'node:util';
import { GatewayError } from './common.mjs';

const hash = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
/** Persist an intent before sending. An interrupted process leaves an unknown intent, never a retry permission. */
export class Journal {
  constructor(directory) { this.directory = directory; mkdirSync(directory, { recursive: true, mode: 0o700 }); }
  file(scope, key) { return join(this.directory, hash([scope, key]) + '.json'); }
  begin(scope, key, command, args) {
    const file = this.file(scope, key); const fingerprint = hash([command, args]);
    const record = { command, fingerprint, status: 'unknown', createdAt: new Date().toISOString() };
    let fd;
    try { fd = openSync(file, 'wx', 0o600); }
    catch (e) {
      if (e.code !== 'EEXIST') throw e;
      let previous; try { previous = JSON.parse(readFileSync(file, 'utf8')); } catch { throw new GatewayError('journal_unreadable', 'Cannot safely replay this operation'); }
      if (previous.fingerprint !== fingerprint) throw new GatewayError('operation_key_conflict', 'operationKey already belongs to different arguments');
      return { previous };
    }
    try { writeFileSync(fd, JSON.stringify(record)); fsyncSync(fd); } finally { closeSync(fd); }
    return { file, record };
  }
  finish(receipt, result) {
    const temp = format('%s.%s.tmp', receipt.file, randomUUID());
    const fd = openSync(temp, 'wx', 0o600);
    try { writeFileSync(fd, JSON.stringify({ ...receipt.record, status: result.status, result })); fsyncSync(fd); } finally { closeSync(fd); }
    renameSync(temp, receipt.file);
  }
  get(scope, key) {
    try { return JSON.parse(readFileSync(this.file(scope, key), 'utf8')); }
    catch (e) { if (e.code === 'ENOENT') return { status: 'not_found' }; throw new GatewayError('journal_unreadable', 'Operation record cannot be read'); }
  }
}

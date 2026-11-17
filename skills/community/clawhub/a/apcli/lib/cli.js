'use strict';

const BOOLEAN = new Set(['json', 'help', 'version', 'yes']);
const REPEATABLE = new Set(['phone', 'email', 'social', 'remove-phone', 'remove-email', 'remove-social']);

/** argv into { command, positional, flags, arrays }, or { ok: false, error }. */
function parseArgs(args) {
  const result = { command: null, positional: [], flags: {}, arrays: {} };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) {
      if (!result.command) result.command = arg;
      else result.positional.push(arg);
      continue;
    }
    const key = arg.slice(2);
    if (BOOLEAN.has(key)) {
      result.flags[key] = true;
      continue;
    }
    const value = args[i + 1];
    if (value === undefined || value.startsWith('--')) {
      return { ok: false, error: { code: 'MISSING_REQUIRED', message: `--${key} requires a value` } };
    }
    i++;
    if (REPEATABLE.has(key)) (result.arrays[key] = result.arrays[key] || []).push(value);
    else result.flags[key] = value;
  }
  return { ok: true, result };
}

/** `mobile:+49 176...` into { label, value }; no label means the default. */
function labelled(raw) {
  const m = /^([A-Za-z][\w ]*):(?!\/\/)(.+)$/.exec(raw);
  return m && !/^\+?[\d\s()-]+$/.test(m[1]) ? { label: m[1], value: m[2].trim() } : { value: raw.trim() };
}

/** `telegram:@ana` or `discord:1234...`. A numeric handle is an id, not a name. */
function socialOf(raw) {
  const i = raw.indexOf(':');
  if (i < 1) throw new Error(`--social needs service:handle, got: ${raw}`);
  const service = raw.slice(0, i).trim();
  const handle = raw.slice(i + 1).trim().replace(/^@/, '');
  return /^\d+$/.test(handle) ? { service, userIdentifier: handle } : { service, username: handle };
}

/** Flags into the change set the JXA scripts apply. */
function toChanges(flags, arrays) {
  const changes = { add: {}, remove: {} };
  if (flags.given !== undefined) changes.givenName = flags.given;
  if (flags.family !== undefined) changes.familyName = flags.family;
  if (flags.nickname !== undefined) changes.nickname = flags.nickname;
  if (flags.org !== undefined) changes.organization = flags.org;
  changes.add.phones = (arrays.phone || []).map(labelled);
  changes.add.emails = (arrays.email || []).map(labelled);
  changes.add.social = (arrays.social || []).map(socialOf);
  changes.remove.phones = arrays['remove-phone'] || [];
  changes.remove.emails = arrays['remove-email'] || [];
  changes.remove.social = (arrays['remove-social'] || []).map(socialOf);
  return changes;
}

function formatContact(c) {
  const lines = [c.name + (c.nickname ? ` (${c.nickname})` : '')];
  if (c.organization && c.organization !== c.name) lines.push(`  Company: ${c.organization}`);
  for (const p of c.phones) lines.push(`  Phone${p.label ? ` (${p.label})` : ''}: ${p.value}`);
  for (const e of c.emails) lines.push(`  Email${e.label ? ` (${e.label})` : ''}: ${e.value}`);
  for (const s of c.social) lines.push(`  ${s.service}: ${s.username || s.userIdentifier || s.url}`);
  for (const m of c.im) lines.push(`  ${m.service}: ${m.username}`);
  lines.push(`  ID: ${c.id}`);
  return lines.join('\n');
}

function formatContacts(list) {
  if (!list.length) return 'No contacts found.';
  return list.map(formatContact).join('\n\n');
}

module.exports = { parseArgs, labelled, socialOf, toChanges, formatContact, formatContacts };

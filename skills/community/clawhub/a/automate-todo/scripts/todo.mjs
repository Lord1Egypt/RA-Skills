#!/usr/bin/env node
/**
 * TODO.md maintenance.
 *
 * Moves every checked top-level item (`- [x] ...`, together with its wrapped
 * continuation lines and nested sub-items) out of its roadmap section and
 * into a `## Complete` section, which is created on first use and always
 * kept at the bottom of the file. Each archived item gains a nested
 * `- From: <section>` line recording which roadmap section it came from -
 * unless the item already carries a `- From:` note (an item worked on under
 * Current keeps the section it originally came from), which is preserved.
 * Items already under `## Complete` stay where they are, so running the
 * script repeatedly is a no-op.
 *
 * Nested checked items under an unchecked parent are left in place - the
 * parent keeps its context until it is checked off as a whole.
 *
 *   node scripts/todo.mjs                 # TODO.md in the current directory
 *   node scripts/todo.mjs path/to/TODO.md # explicit target
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const path = resolve(process.cwd(), process.argv[2] ?? 'TODO.md');
const lines = readFileSync(path, 'utf8').split(/\r?\n/);

// Split the file into the preamble (before the first `## `) and one entry
// per level-two section.
const sections = [];
let current = { header: null, lines: [] };
for (const line of lines) {
  if (/^## /.test(line)) {
    sections.push(current);
    current = { header: line, lines: [] };
  } else {
    current.lines.push(line);
  }
}
sections.push(current);

const isComplete = (s) => s.header !== null && /^## Complete\b/.test(s.header);

// Pull each checked top-level item out of every section except Complete
// itself. A block is the `- [x]` line plus every following indented line
// (wrapped text or nested children), so items move whole.
const moved = [];
for (const section of sections) {
  if (section.header === null || isComplete(section)) continue;
  const kept = [];
  for (let i = 0; i < section.lines.length; i++) {
    const line = section.lines[i];
    if (/^- \[x\]/i.test(line)) {
      const start = moved.length;
      moved.push(line);
      while (i + 1 < section.lines.length && /^\s+\S/.test(section.lines[i + 1])) {
        moved.push(section.lines[++i]);
      }
      // Nested provenance line: which section the finished item came from.
      // An item that already carries its own "- From:" note (e.g. it was
      // pulled into Current from another roadmap section) keeps that origin
      // instead of being stamped with the section it was completed in.
      const hasFrom = moved.slice(start + 1).some((l) => /^\s+- From:/i.test(l));
      if (!hasFrom) moved.push(`  - From: ${section.header.replace(/^## /, '')}`);
    } else {
      kept.push(line);
    }
  }
  section.lines = kept;
}

// Collapses blank-line runs the moves leave behind (and trims the edges).
const tidy = (list) => {
  const out = [];
  for (const line of list) {
    if (line.trim() === '' && (out.length === 0 || out[out.length - 1].trim() === '')) continue;
    out.push(line);
  }
  while (out.length > 0 && out[out.length - 1].trim() === '') out.pop();
  return out;
};

// Reassemble with Complete last - moving the header to the bottom and
// appending the checked items under it in one pass.
let complete = sections.find(isComplete);
if (!complete && moved.length > 0) {
  complete = { header: '## Complete', lines: [] };
}

const out = [];
for (const section of sections) {
  if (section === complete) continue;
  if (section.header !== null) out.push(section.header, '');
  const body = tidy(section.lines);
  if (body.length > 0) out.push(...body, '');
}
if (complete) {
  out.push(complete.header, '');
  const body = tidy(complete.lines);
  if (body.length > 0) out.push(...body);
  out.push(...moved);
  if (out[out.length - 1] !== '') out.push('');
}

writeFileSync(path, out.join('\n').replace(/\n+$/, '\n'));
console.log(
  moved.length > 0
    ? `todo: moved ${moved.filter((l) => /^- \[x\]/i.test(l)).length} item(s) to ## Complete.`
    : 'todo: nothing to move.',
);

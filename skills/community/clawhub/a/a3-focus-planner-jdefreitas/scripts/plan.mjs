// Original portable focus-gap algorithm. Reads JSON on stdin; no network or writes.
import fs from 'node:fs';
export function plan({ events, workStart, workEnd, bufferMinutes = 10, minimumMinutes = 30 }) {
  const lo = Date.parse(workStart), hi = Date.parse(workEnd);
  if (!Array.isArray(events) || !Number.isFinite(lo) || !Number.isFinite(hi) || hi <= lo || hi - lo > 86400000 || !Number.isFinite(bufferMinutes) || bufferMinutes < 0 || bufferMinutes > 60 || !Number.isFinite(minimumMinutes) || minimumMinutes < 15 || minimumMinutes > 240) throw Error('Invalid planner input');
  const busy = events.filter(e => e.status !== 'cancelled' && e.transparency !== 'transparent').map(e => ({ title: String(e.summary || ''), start: Date.parse(e.start), end: Date.parse(e.end) })).filter(e => Number.isFinite(e.start) && Number.isFinite(e.end) && e.end > lo && e.start < hi).sort((a, b) => a.start - b.start);
  const conflicts = [], gaps = []; let cursor = lo;
  for (let i = 0; i < busy.length; i++) {
    const e = busy[i];
    for (let j = i + 1; j < busy.length && busy[j].start < e.end; j++) conflicts.push([e.title, busy[j].title]);
    const start = Math.max(lo, e.start - bufferMinutes * 60000), end = Math.min(hi, e.end + bufferMinutes * 60000);
    if (start - cursor >= minimumMinutes * 60000) gaps.push({ from: new Date(cursor).toISOString(), to: new Date(start).toISOString(), minutes: (start - cursor) / 60000 });
    cursor = Math.max(cursor, end);
  }
  if (hi - cursor >= minimumMinutes * 60000) gaps.push({ from: new Date(cursor).toISOString(), to: new Date(hi).toISOString(), minutes: (hi - cursor) / 60000 });
  return { conflicts, gaps, bufferMinutes, minimumMinutes };
}
if (process.argv[1] && import.meta.url === new URL('file://' + process.argv[1]).href) console.log(JSON.stringify(plan(JSON.parse(fs.readFileSync(0, 'utf8'))), null, 2));

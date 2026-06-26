#!/usr/bin/env node
/**
 * Reverse-lookup: find solar date(s) matching known 八字 four pillars.
 *
 * Usage:
 *   node scripts/scan_year.ts <year> <gender> [options]
 *
 * Options:
 *   --year-pillar XX    年柱 to match (e.g. 甲申)
 *   --month-pillar XX   月柱 to match (e.g. 戊辰)
 *   --day-pillar XX     日柱 to match (e.g. 甲寅)
 *   --hour-pillar XX    时柱 to match (e.g. 庚午)
 *   --hour HH:MM:SS     Time to use (default: 15:30:00 for 申时)
 *
 * Examples:
 *   # Full match (all four pillars)
 *   node scripts/scan_year.ts 2004 1 --year-pillar 甲申 --month-pillar 戊辰 --day-pillar 甲寅 --hour-pillar 庚午
 *
 *   # Partial match (just year + month + day, any hour)
 *   node scripts/scan_year.ts 2004 1 --year-pillar 甲申 --month-pillar 戊辰 --day-pillar 甲寅
 *
 *   # Scan with specific hour
 *   node scripts/scan_year.ts 2004 1 --day-pillar 甲寅 --hour 12:00:00
 *
 *   # Cross-year scan (60-year cycle)
 *   for y in 1944 2004; do node scripts/scan_year.ts $y 1 --day-pillar 甲寅; done
 */

import { buildBaziFromSolar } from 'cantian-tymext';

/**
 * Extract "天干地支" string from a pillar object.
 * cantian-tymext returns Chinese-named fields:
 *   bazi.年柱.天干.天干 = "庚"
 *   bazi.年柱.地支.地支 = "辰"
 */
function pillarString(pillar: any): string {
  const tg = pillar?.天干?.天干;
  const dz = pillar?.地支?.地支;
  if (!tg || !dz) {
    throw new Error(`Unexpected pillar shape: ${JSON.stringify(pillar).slice(0, 200)}`);
  }
  return `${tg}${dz}`;
}

interface ScanOptions {
  year: number;
  gender: 0 | 1;
  hour: string;
  yearPillar?: string;
  monthPillar?: string;
  dayPillar?: string;
  hourPillar?: string;
}

function parseArgs(args: string[]): ScanOptions {
  const positional: string[] = [];
  const flags: Record<string, string> = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      flags[key] = args[++i] || '';
    } else {
      positional.push(args[i]);
    }
  }

  const year = parseInt(positional[0], 10);
  if (isNaN(year)) {
    throw new Error('Usage: scan_year.ts <year> <gender> [options]\n  year: integer (e.g. 2000)');
  }

  const gender = parseInt(positional[1], 10);
  if (![0, 1].includes(gender)) {
    throw new Error('gender must be 0 (female) or 1 (male)');
  }

  return {
    year,
    gender: gender as 0 | 1,
    hour: flags['hour'] || '15:30:00',
    yearPillar: flags['year-pillar'],
    monthPillar: flags['month-pillar'],
    dayPillar: flags['day-pillar'],
    hourPillar: flags['hour-pillar'],
  };
}

function scanYear(opts: ScanOptions): Array<{ date: string; bazi: string }> {
  const results: Array<{ date: string; bazi: string }> = [];
  const startDate = new Date(opts.year, 0, 1);
  const endDate = new Date(opts.year, 11, 31);

  const current = new Date(startDate);
  while (current <= endDate) {
    const y = current.getFullYear();
    const m = String(current.getMonth() + 1).padStart(2, '0');
    const d = String(current.getDate()).padStart(2, '0');
    const solarTime = `${y}-${m}-${d}T${opts.hour}`;

    try {
      const bazi = buildBaziFromSolar({ solarTime, gender: opts.gender, sect: 2 });
      const pillars = [
        pillarString(bazi.年柱),
        pillarString(bazi.月柱),
        pillarString(bazi.日柱),
        pillarString(bazi.时柱),
      ];

      let match = true;
      if (opts.yearPillar && pillars[0] !== opts.yearPillar) match = false;
      if (opts.monthPillar && pillars[1] !== opts.monthPillar) match = false;
      if (opts.dayPillar && pillars[2] !== opts.dayPillar) match = false;
      if (opts.hourPillar && pillars[3] !== opts.hourPillar) match = false;

      if (match) {
        const baziStr = pillars.join(' ');
        const dateStr = `${y}-${m}-${d}`;
        results.push({ date: dateStr, bazi: baziStr });
        console.log(`MATCH: ${dateStr} -> ${baziStr}`);
      }
    } catch (err: any) {
      // Only skip invalid date errors; log other errors for debugging
      if (!err?.message?.includes('Invalid') && !err?.message?.includes('invalid')) {
        console.error(`Error on ${solarTime}:`, err?.message || err);
      }
    }

    current.setDate(current.getDate() + 1);
  }

  return results;
}

function main() {
  const args = process.argv.slice(2);
  const opts = parseArgs(args);

  console.log(`Scanning ${opts.year} for gender=${opts.gender}, hour=${opts.hour}...`);
  console.log(`Filters: year=${opts.yearPillar || '*'} month=${opts.monthPillar || '*'} day=${opts.dayPillar || '*'} hour=${opts.hourPillar || '*'}`);
  console.log();

  const results = scanYear(opts);

  console.log(`\n${'='.repeat(50)}`);
  console.log(`Found ${results.length} match(es) in ${opts.year}`);
  if (results.length === 0) {
    console.log('No matches found. Try scanning adjacent years or different hour.');
  }
}

main();

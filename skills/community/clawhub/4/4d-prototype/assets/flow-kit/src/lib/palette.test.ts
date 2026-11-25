import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { buildVars, contrast, hexToOklch, oklchToHex, PRESETS, type Mode, type Style } from './palette';

/*
 * Appearance tests. The original tokens are read from the project's global stylesheet (the same @theme the pages use);
 * in flow-kit itself, from styles/tokens.css. Add the project's island files (original-look content) to ISLAND_FILES.
 */
const STYLES_FILE = ['../styles/index.css', '../styles/tokens.css'].map((f) => new URL(f, import.meta.url)).find((u) => existsSync(u))!;
const ISLAND_FILES: string[] = []; // e.g. 'components/flow/FormatPreview.tsx', 'components/live/Phone.tsx'
const css = readFileSync(STYLES_FILE, 'utf8');
const defaults: Record<string, string> = {};
for (const m of css.matchAll(/--color-([\w-]+):\s*(#[0-9a-fA-F]{6})/g)) defaults[m[1]] = m[2];

const PALETTES = [...PRESETS.map((p) => ({ palette: p.key })), ...['#e11d48', '#16a34a', '#f5b400', '#7dd3fc'].map((brand) => ({ palette: 'custom', brand }))];
const MODES: Mode[] = ['light', 'dark'];
const STYLES: Style[] = ['soft', 'sharp'];

describe('appearance engine', () => {
  it('OKLCH round trip within 1/255', () => {
    for (const hex of ['#e25507', '#2563eb', '#1c8c50', '#776d66', '#ffffff', '#000000']) {
      const back = oklchToHex(...hexToOklch(hex));
      const d = Math.max(...[1, 3, 5].map((i) => Math.abs(parseInt(back.slice(i, i + 2), 16) - parseInt(hex.slice(i, i + 2), 16))));
      expect(d, `${hex} → ${back}`).toBeLessThanOrEqual(1);
    }
  });

  it('light + default palette overrides nothing', () => {
    expect(buildVars(defaults, { palette: 'default', mode: 'light', style: 'soft' })).toEqual({});
  });

  for (const p of PALETTES) {
    for (const mode of MODES) {
      for (const style of STYLES) {
        it(`${p.palette}${p.brand ? ` ${p.brand}` : ''} · ${mode} · ${style}: text, links, buttons and semantic colors are readable`, () => {
          const vars = buildVars(defaults, { ...p, mode, style });
          const v = (k: string) => vars[k] ?? defaults[k];
          for (const bg of [v('paper'), v('surface')]) {
            expect(contrast(v('ink-900'), bg)).toBeGreaterThanOrEqual(7);
            expect(contrast(v('ink-500'), bg)).toBeGreaterThanOrEqual(4.5);
            expect(contrast(v('ink-400'), bg)).toBeGreaterThanOrEqual(4.5);
          }
          expect(contrast(v('primary-600'), v('surface'))).toBeGreaterThanOrEqual(4.5);
          expect(contrast('#ffffff', v('primary-500'))).toBeGreaterThanOrEqual(3);
          for (const fam of ['seal', 'amber', 'pine', 'rule', 'agent']) {
            if (v(`${fam}-600`)) expect(contrast(v(`${fam}-600`), v('surface')), fam).toBeGreaterThanOrEqual(4.5);
          }
        });
      }
    }
  }
});

describe('no hard-coded colors outside islands', () => {
  const root = new URL('../', import.meta.url);
  const SKIP = /^(lib\/palette|lib\/theme\.ts$)|\.test\.ts$/;
  const files = (readdirSync(root, { recursive: true }) as string[]).filter((f) => /\.(tsx|ts)$/.test(f) && !SKIP.test(f) && !ISLAND_FILES.includes(f));

  it('shell, pages and flow components use tokens only (no #hex, bg-white, white gradient stops, black/ tints except backdrops; no white text on fills that invert)', () => {
    const bad: string[] = [];
    for (const f of files) {
      const lines = readFileSync(new URL(f, root), 'utf8').split('\n');
      let fixedBlock = false; // theme-fixed:start … theme-fixed:end marks a deliberately fixed-color block
      lines.forEach((l, i) => {
        if (l.includes('theme-fixed:start')) fixedBlock = true;
        if (l.includes('theme-fixed:end')) fixedBlock = false;
        if (fixedBlock || /theme-(island|fixed)/.test(l) || /theme-(island|fixed)/.test(lines[i - 1] ?? '')) return;
        if (/#[0-9a-fA-F]{6}\b/.test(l) || /\bbg-white\b/.test(l) || (/\b(bg|ring|border|divide|text)-black\//.test(l) && !/inset-0/.test(l)) || /(?<![\w-])(from|via|to)-white\b(?!\/)/.test(l)) {
          bad.push(`${f}:${i + 1}: ${l.trim().slice(0, 100)}`);
        }
        for (const q of l.match(/'[^']*'|"[^"]*"|`[^`]*`/g) ?? []) {
          if (/\bbg-(ink-([6-9]00|950)|act-[a-z]+)\b(?!\/)/.test(q) && /(?<![:\w-])text-white\b/.test(q)) bad.push(`${f}:${i + 1}: white text on a fill that inverts in dark mode — use text-surface`);
        }
      });
    }
    expect(bad).toEqual([]);
  });
});

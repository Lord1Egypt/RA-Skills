/**
 * Appearance engine (pure functions, unit-tested): turns "palette × light/dark × style" into CSS variable overrides.
 *
 * - Every color in the prototype is a token in @theme (--color-ink-*, --color-primary-* …). Switching the appearance =
 *   overriding these variables; components never know about themes. Light + "原型默认" (the prototype's own palette)
 *   overrides nothing, so the hand-tuned original stays exactly as designed.
 * - Scales are generated in OKLCH: one hue on a lightness ladder, then body text, links and secondary text are
 *   corrected against WCAG contrast.
 * - Semantic colors (done / warning / problem …) and actor colors keep their hues across palettes; in dark mode only
 *   their lightness is adjusted for readability.
 */

export type Mode = 'light' | 'dark';
export type Style = 'soft' | 'sharp';

export interface PalettePreset {
  key: string;
  label: string;
  /** primary color; absent for the default palette, which keeps the prototype's own tokens */
  brand?: string;
  /** hue and chroma (OKLCH) of the neutrals, giving the grays a slight cool / warm tint */
  neutral?: { h: number; c: number };
}

export const PRESETS: PalettePreset[] = [
  { key: 'default', label: '原型默认' },
  { key: 'ocean', label: '商务蓝', brand: '#2563eb', neutral: { h: 255, c: 0.012 } },
  { key: 'jade', label: '青绿', brand: '#0d8a7a', neutral: { h: 185, c: 0.01 } },
  { key: 'violet', label: '绛紫', brand: '#6f45dc', neutral: { h: 290, c: 0.012 } },
  { key: 'graphite', label: '石墨', brand: '#3b4250', neutral: { h: 260, c: 0.005 } },
];

export interface ThemeChoice {
  /** a PRESETS key, or 'custom' (generated from brand) */
  palette: string;
  brand?: string;
  mode: Mode;
  style: Style;
}

export const INK_STEPS = ['950', '900', '800', '700', '600', '500', '400', '300', '200', '150', '100', '50'] as const;
export const ACCENT_STEPS = ['50', '100', '200', '300', '400', '500', '600', '700'] as const;
/** semantic families: regenerated from their own 500 in dark mode */
export const SEMANTIC_FAMILIES = ['seal', 'amber', 'pine', 'rule', 'agent'] as const;

/* ---------------- color math (sRGB ↔ OKLab / OKLCH) ---------------- */

type Rgb = [number, number, number];

export function hexToRgb(hex: string): Rgb {
  const h = hex.trim().replace('#', '');
  const v = h.length === 3 ? h.split('').map((c) => c + c).join('') : h.slice(0, 6);
  return [0, 2, 4].map((i) => parseInt(v.slice(i, i + 2), 16) / 255) as Rgb;
}

export function rgbToHex(rgb: Rgb): string {
  return '#' + rgb.map((x) => Math.round(Math.min(1, Math.max(0, x)) * 255).toString(16).padStart(2, '0')).join('');
}

const toLinear = (c: number) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = (c: number) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

export function hexToOklch(hex: string): [number, number, number] {
  const [r, g, b] = hexToRgb(hex).map(toLinear);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  const C = Math.hypot(A, B);
  const H = ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360;
  return [L, C, H];
}

function oklchToLinear(L: number, C: number, H: number): Rgb {
  const a = C * Math.cos((H * Math.PI) / 180);
  const b = C * Math.sin((H * Math.PI) / 180);
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}

/** OKLCH → hex; out-of-gamut colors lose chroma until they fit sRGB */
export function oklchToHex(L: number, C: number, H: number): string {
  let c = C;
  for (let i = 0; i < 40; i++) {
    const lin = oklchToLinear(L, c, H);
    if (lin.every((v) => v >= -0.0005 && v <= 1.0005)) return rgbToHex(lin.map(toGamma) as Rgb);
    c *= 0.9;
  }
  return rgbToHex(oklchToLinear(L, 0, H).map(toGamma) as Rgb);
}

/** WCAG 2 contrast ratio */
export function contrast(a: string, b: string): number {
  const lum = (hex: string) => {
    const [r, g, bl] = hexToRgb(hex).map(toLinear);
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl;
  };
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
}

/** move along lightness until the contrast with bg reaches min (dir = -1 darker, +1 lighter) */
function ensureContrast(L: number, C: number, H: number, bg: string, min: number, dir: 1 | -1): string {
  let l = L;
  let hex = oklchToHex(l, C, H);
  for (let i = 0; i < 60 && contrast(hex, bg) < min && l > 0.02 && l < 0.99; i++) {
    l += 0.01 * dir;
    hex = oklchToHex(l, C, H);
  }
  return hex;
}

/* ---------------- scales ---------------- */

const SURFACE = { light: { paper: [0.972, 0.6], surface: [1, 0] }, dark: { paper: [0.18, 1], surface: [0.225, 1] } } as const;

const INK_L: Record<Mode, Record<(typeof INK_STEPS)[number], number>> = {
  light: { 950: 0.14, 900: 0.22, 800: 0.27, 700: 0.36, 600: 0.45, 500: 0.52, 400: 0.555, 300: 0.75, 200: 0.87, 150: 0.925, 100: 0.95, 50: 0.968 },
  dark: { 950: 0.985, 900: 0.94, 800: 0.9, 700: 0.83, 600: 0.76, 500: 0.7, 400: 0.66, 300: 0.48, 200: 0.38, 150: 0.32, 100: 0.285, 50: 0.25 },
};

/** neutrals: ink-* + paper + surface. Secondary text (500 / 400) keeps ≥ 4.5 contrast on both surface and paper */
export function neutralScale(h: number, c: number, mode: Mode): Record<string, string> {
  const out: Record<string, string> = {};
  const [pl, pc] = SURFACE[mode].paper;
  const [sl, sc] = SURFACE[mode].surface;
  out['paper'] = oklchToHex(pl, c * pc, h);
  out['surface'] = oklchToHex(sl, c * sc, h);
  const worst = contrast(out['paper'], mode === 'light' ? '#000000' : '#ffffff') < contrast(out['surface'], mode === 'light' ? '#000000' : '#ffffff') ? out['paper'] : out['surface'];
  for (const step of INK_STEPS) {
    const L = INK_L[mode][step];
    const textual = ['950', '900', '800', '700', '600', '500', '400'].includes(step);
    out[`ink-${step}`] = textual ? ensureContrast(L, c, h, worst, step === '400' || step === '500' ? 4.6 : 7, mode === 'light' ? -1 : 1) : oklchToHex(L, c, h);
  }
  return out;
}

/** accent scale: 50 / 100 tinted backgrounds, 400 / 500 solids, 600 / 700 as text (≥ 4.6 / ≥ 6 against surface) */
export function accentScale(base: string, mode: Mode, surface: string): Record<string, string> {
  const [L0, C0, H] = hexToOklch(base);
  const out: Record<string, string> = {};
  if (mode === 'light') {
    out['50'] = oklchToHex(0.975, C0 * 0.18, H);
    out['100'] = oklchToHex(0.945, C0 * 0.32, H);
    out['200'] = oklchToHex(0.9, C0 * 0.5, H);
    out['300'] = oklchToHex(0.83, C0 * 0.7, H);
    out['400'] = oklchToHex(Math.min(0.76, L0 + 0.1), C0 * 0.95, H);
    // button fill: the brand color itself where possible, but white text needs at least 3:1 (the floor for bold button labels); too-light brands get darkened
    out['500'] = contrast(base, '#ffffff') >= 3 ? base : ensureContrast(L0, C0, H, '#ffffff', 3, -1);
    out['600'] = ensureContrast(Math.min(L0 - 0.05, 0.56), C0, H, surface, 4.6, -1);
    out['700'] = ensureContrast(hexToOklch(out['600'])[0] - 0.06, C0, H, surface, 6, -1);
  } else {
    out['50'] = oklchToHex(0.27, C0 * 0.35, H);
    out['100'] = oklchToHex(0.32, C0 * 0.5, H);
    out['200'] = oklchToHex(0.4, C0 * 0.65, H);
    out['300'] = oklchToHex(0.5, C0 * 0.8, H);
    out['400'] = oklchToHex(0.7, C0 * 0.9, H);
    out['500'] = ensureContrast(Math.min(Math.max(L0, 0.6), 0.66), C0, H, '#ffffff', 3, -1);
    out['600'] = ensureContrast(Math.max(L0, 0.72), C0 * 0.9, H, surface, 4.6, 1);
    out['700'] = ensureContrast(Math.min(hexToOklch(out['600'])[0] + 0.07, 0.92), C0 * 0.8, H, surface, 6, 1);
  }
  return out;
}

/* ---------------- assemble the overrides ---------------- */

/** defaults: the prototype's original @theme tokens (name → value; names without the "--color-" prefix, shadows as "shadow-*") */
export function buildVars(defaults: Record<string, string>, choice: ThemeChoice): Record<string, string> {
  const preset = PRESETS.find((p) => p.key === choice.palette);
  const custom = choice.palette === 'custom' && choice.brand ? choice.brand : undefined;
  const brand = custom ?? preset?.brand;
  const vars: Record<string, string> = {};
  const isDefault = !brand;

  if (choice.mode === 'light' && !isDefault) {
    const [, , bh] = hexToOklch(brand);
    const nh = custom ? bh : preset!.neutral!.h;
    const nc = custom ? 0.01 : preset!.neutral!.c;
    Object.assign(vars, prefixed(neutralScale(nh, nc, 'light')));
    Object.assign(vars, prefixed(accentScale(brand, 'light', vars['surface']), 'primary-'));
  }

  if (choice.mode === 'dark') {
    const [, dc, dh] = hexToOklch(defaults['ink-500'] ?? '#6e6e73');
    const nh = isDefault ? dh : custom ? hexToOklch(brand)[2] : preset!.neutral!.h;
    const nc = isDefault ? Math.min(dc, 0.014) : custom ? 0.01 : preset!.neutral!.c;
    Object.assign(vars, prefixed(neutralScale(nh, nc, 'dark')));
    const surface = vars['surface'];
    Object.assign(vars, prefixed(accentScale(brand ?? defaults['primary-500'], 'dark', surface), 'primary-'));
    for (const fam of SEMANTIC_FAMILIES) {
      if (defaults[`${fam}-500`]) Object.assign(vars, prefixed(accentScale(defaults[`${fam}-500`], 'dark', surface), `${fam}-`));
    }
    for (const [k, v] of Object.entries(defaults)) {
      if (!k.startsWith('act-')) continue;
      const [L, C, H] = hexToOklch(v);
      vars[k] = oklchToHex(Math.max(L, 0.7), C, H);
    }
    vars['shadow-pop'] = '0 24px 60px -12px rgb(0 0 0 / 0.55), 0 0 0 1px rgb(255 255 255 / 0.06)';
    vars['shadow-raise'] = '0 1px 2px rgb(0 0 0 / 0.3), 0 8px 24px -12px rgb(0 0 0 / 0.5)';
  }

  if (choice.style === 'sharp') {
    const ink = (s: string) => vars[`ink-${s}`] ?? defaults[`ink-${s}`];
    vars['shadow-raise'] = `0 0 0 1px ${ink('150')}`;
    vars['shadow-pop'] = `0 12px 32px -14px rgb(0 0 0 / ${choice.mode === 'dark' ? 0.6 : 0.22}), 0 0 0 1px ${ink('200')}`;
  }
  return vars;
}

function prefixed(rec: Record<string, string>, prefix = ''): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [k, v] of Object.entries(rec)) out[prefix + k] = v;
  return out;
}

/** token name → CSS custom property */
export const cssName = (k: string) => (k.startsWith('shadow-') ? `--${k}` : `--color-${k}`);

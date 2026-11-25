import { useSyncExternalStore } from 'react';
import { buildVars, cssName, type Mode, type Style } from './palette';
import { createStore } from './store';

/**
 * Appearance (palette × light/dark × style): the preference is kept on this machine; applying it writes the variables
 * computed by palette.ts into one <style>:
 *   :root           overridden tokens (palette, dark mode, the style's shadows)
 *   .theme-island   the original tokens restored — content shown in its original look (apps inside phone frames,
 *                   map art, file and format samples, external-system pages) keeps its own colors
 * The "sharp" style's radii are handled in CSS via html[data-style] (see flow-kit.css); html[data-mode] is there for the
 * few styles that must differ between light and dark. Call initTheme() in main.tsx before rendering, so the first paint
 * already has the right colors.
 */
export interface ThemePrefs {
  palette: string;
  brand: string;
  mode: Mode | 'system';
  style: Style;
}

export const themeStore = createStore<ThemePrefs>('theme', () => ({ palette: 'default', brand: '#2563eb', mode: 'light', style: 'soft' }));

let defaults: Record<string, string> | null = null;

/** read the original @theme tokens from the stylesheets (Tailwind 4 emits them in a :root rule inside @layer theme) */
function readDefaults(): Record<string, string> {
  const out: Record<string, string> = {};
  const visit = (rules: CSSRuleList) => {
    for (const r of Array.from(rules)) {
      if ('cssRules' in r && (r as CSSGroupingRule).cssRules) visit((r as CSSGroupingRule).cssRules);
      if (r instanceof CSSStyleRule && /(^|,)\s*:root\b/.test(r.selectorText)) {
        for (const name of Array.from(r.style)) {
          if (name.startsWith('--color-')) out[name.slice(8)] = r.style.getPropertyValue(name).trim();
          if (name.startsWith('--shadow-')) out[name.slice(2)] = r.style.getPropertyValue(name).trim();
        }
      }
    }
  };
  for (const sheet of Array.from(document.styleSheets)) {
    try {
      visit(sheet.cssRules);
    } catch {
      /* cross-origin stylesheet: not readable, skip */
    }
  }
  return out;
}

/** an original token (e.g. the default palette's swatch uses the original primary-500) */
export function defaultToken(name: string): string | undefined {
  if (typeof document === 'undefined') return undefined;
  defaults ??= readDefaults();
  return defaults[name];
}

const systemDark = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches;

export function resolvedMode(p: ThemePrefs = themeStore.get()): Mode {
  return p.mode === 'system' ? (systemDark() ? 'dark' : 'light') : p.mode;
}

export function applyTheme() {
  if (typeof document === 'undefined') return;
  defaults ??= readDefaults();
  const p = themeStore.get();
  const mode = resolvedMode(p);
  const vars = buildVars(defaults, { palette: p.palette, brand: p.brand, mode, style: p.style });
  const decl = (entries: [string, string][]) => entries.map(([k, v]) => `${cssName(k)}:${v};`).join('');
  const island = Object.keys(vars).filter((k) => defaults![k] !== undefined).map((k) => [k, defaults![k]] as [string, string]);
  let el = document.getElementById('theme-vars');
  if (!el) {
    el = document.createElement('style');
    el.id = 'theme-vars';
    document.head.appendChild(el);
  }
  el.textContent = `:root{${decl(Object.entries(vars))}}.theme-island{${decl(island)}color-scheme:light;}`;
  const root = document.documentElement;
  root.dataset.mode = mode;
  root.dataset.style = p.style;
  root.dataset.palette = p.palette;
  root.style.colorScheme = mode;
}

let wired = false;
/** call once at startup: applies the appearance and re-applies it when the preference or the system light/dark changes */
export function initTheme() {
  applyTheme();
  if (wired || typeof window === 'undefined') return;
  wired = true;
  themeStore.subscribe(applyTheme);
  window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', () => themeStore.get().mode === 'system' && applyTheme());
}

export function useTheme(): ThemePrefs {
  return useSyncExternalStore(themeStore.subscribe, themeStore.get, themeStore.get);
}

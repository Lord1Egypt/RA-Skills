import { useSyncExternalStore } from 'react';

/**
 * Minimal hash router: #/path?query
 * Hash routing lets the build (vite base: './') be hosted as static files in a portal without server-side routing.
 */
export interface Route {
  path: string;
  query: URLSearchParams;
}

function parse(hash: string): Route {
  const raw = hash.replace(/^#/, '') || '/';
  const [p, q = ''] = raw.split('?');
  return { path: p || '/', query: new URLSearchParams(q) };
}

function subscribe(cb: () => void) {
  window.addEventListener('hashchange', cb);
  return () => window.removeEventListener('hashchange', cb);
}

const getHash = () => window.location.hash;

export function useRoute(): Route {
  const hash = useSyncExternalStore(subscribe, getHash, () => '');
  return parse(hash);
}

export function navigate(to: string) {
  const target = to.startsWith('#') ? to : `#${to}`;
  if (window.location.hash !== target) window.location.hash = target;
}

/** Update the current route's query without a new history entry (writes tabs, filters, etc. into the URL) */
export function setQuery(patch: Record<string, string | null | undefined>) {
  const { path, query } = parse(window.location.hash);
  for (const [k, v] of Object.entries(patch)) {
    if (v === null || v === undefined || v === '') query.delete(k);
    else query.set(k, v);
  }
  const qs = query.toString();
  window.history.replaceState(null, '', `#${path}${qs ? `?${qs}` : ''}`);
  window.dispatchEvent(new HashChangeEvent('hashchange'));
}

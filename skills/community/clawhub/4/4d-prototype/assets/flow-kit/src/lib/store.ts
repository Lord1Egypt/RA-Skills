import { useSyncExternalStore } from 'react';

/**
 * Lightweight global state: useSyncExternalStore + localStorage.
 * localStorage only keeps demo data (config changes, retained results, preferences) across reloads; every read and write is wrapped
 * in try/catch and falls back to memory in private mode or when storage is disabled.
 *
 * - persist: false — memory only (whole-flow demo state, cursor, etc.).
 * - version — bump when demo data changes incompatibly (e.g. demo organizations migrated): the store switches to the
 *   `<PREFIX>:<key>@<version>` key and removes older keys, so stale browser data never mixes with new data.
 */
const PREFIX = 'proto'; // replace with the project name, e.g. 'doc-audit'

/** Demo data version: bump on incompatible demo data changes and use it on the affected stores */
export const DEMO_DATA_VERSION = 1;

export function createStore<T extends object>(key: string, initial: () => T, opts: { persist?: boolean; version?: number } = {}) {
  const version = opts.version ?? 1;
  const keyOf = (v: number) => (v > 1 ? `${PREFIX}:${key}@${v}` : `${PREFIX}:${key}`);
  const storageKey = keyOf(version);
  const keep = opts.persist ?? true;
  let state: T = load();
  const listeners = new Set<() => void>();

  function load(): T {
    if (!keep) return initial();
    try {
      for (let v = 1; v < version; v++) window.localStorage.removeItem(keyOf(v));
      const raw = window.localStorage.getItem(storageKey);
      if (raw) return { ...initial(), ...(JSON.parse(raw) as Partial<T>) };
    } catch {
      /* storage unavailable: use the initial value */
    }
    return initial();
  }

  function persist() {
    if (!keep) return;
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(state));
    } catch {
      /* storage unavailable: keep in-memory state only */
    }
  }

  return {
    get: () => state,
    set(patch: Partial<T> | ((s: T) => Partial<T>)) {
      const next = typeof patch === 'function' ? patch(state) : patch;
      state = { ...state, ...next };
      persist();
      listeners.forEach((l) => l());
    },
    reset() {
      state = initial();
      persist();
      listeners.forEach((l) => l());
    },
    subscribe(l: () => void) {
      listeners.add(l);
      return () => listeners.delete(l);
    },
  };
}

export type Store<T extends object> = ReturnType<typeof createStore<T>>;

export function useStore<T extends object, S>(store: Store<T>, selector: (s: T) => S): S {
  return useSyncExternalStore(store.subscribe, () => selector(store.get()));
}

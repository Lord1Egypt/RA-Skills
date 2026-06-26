import { NewsItem } from '../types.js';

export async function fetchNews(apiUrl: string, timeoutMs: number): Promise<NewsItem[]> {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), timeoutMs);
  try {
    const r = await fetch(apiUrl, { signal: c.signal });
    if (!r.ok) throw new Error(`news fetch failed ${r.status}`);
    const j = await r.json();
    if (!Array.isArray(j)) return [];
    return j as NewsItem[];
  } finally {
    clearTimeout(t);
  }
}

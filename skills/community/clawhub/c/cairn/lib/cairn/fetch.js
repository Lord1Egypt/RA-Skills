import { parseHTML } from 'linkedom';
import { UA } from './constants/fetch.constants.js';
import { isOffline } from './offline.js';
export const fetchWeb = async (url) => {
    if (isOffline()) {
        throw new Error(`cairn: web fetch blocked by CAIRN_OFFLINE (would have fetched ${url}). ` +
            `Unset CAIRN_OFFLINE to allow, or skip web ingestion.`);
    }
    const res = await fetch(url, { headers: { 'user-agent': UA } });
    if (!res.ok)
        throw new Error(`fetch ${url}: ${res.status} ${res.statusText}`);
    const ct = res.headers.get('content-type') ?? '';
    const body = await res.text();
    if (ct.startsWith('text/html'))
        return extractHtml(body);
    if (ct.startsWith('text/'))
        return { title: null, text: normalize(body) };
    throw new Error(`fetch ${url}: unsupported content-type ${ct}`);
};
export const extractHtml = (html) => {
    const { document } = parseHTML(html);
    for (const sel of ['script', 'style', 'nav', 'footer', 'aside', 'noscript', 'iframe']) {
        for (const el of document.querySelectorAll(sel))
            el.remove();
    }
    const title = document.querySelector('title')?.textContent?.trim() ?? null;
    const root = document.querySelector('main') ?? document.querySelector('article') ?? document.body;
    const raw = root?.textContent ?? '';
    return { title, text: normalize(raw) };
};
const normalize = (s) => s
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l.length > 0)
    .join('\n')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n');

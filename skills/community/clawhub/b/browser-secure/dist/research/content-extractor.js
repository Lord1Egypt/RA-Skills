const TITLE_SELECTORS = [
    'h1',
    'h1.article-title',
    'h1[data-testid="title"]',
    '.article-header h1',
    '.post-title',
    '[property="og:title"]',
];
const BODY_SELECTORS = [
    'article',
    'main',
    '[role="main"]',
    '.article-body',
    '.post-content',
    '.entry-content',
    '.content',
    '#content',
    '.story-body',
    '.article__body',
];
const AUTHOR_SELECTORS = [
    '.author',
    '.byline',
    '.author-name',
    '[rel="author"]',
    '[property="og:author"]',
    '.article-author',
];
const DATE_SELECTORS = [
    'time',
    '.publish-date',
    '.article-date',
    '.post-date',
    '[property="article:published_time"]',
    '[property="og:published_time"]',
];
async function trySelector(page, selectors) {
    for (const sel of selectors) {
        try {
            const el = await page.$(sel);
            if (el) {
                const text = await el.textContent();
                if (text && text.trim().length > 0)
                    return text.trim();
            }
        }
        catch { /* continue */ }
    }
    return null;
}
async function extractBySelectors(page) {
    const title = await trySelector(page, TITLE_SELECTORS);
    const body = await trySelector(page, BODY_SELECTORS);
    const author = await trySelector(page, AUTHOR_SELECTORS);
    const date = await trySelector(page, DATE_SELECTORS);
    if (body && body.length > 200) {
        const words = body.split(/\s+/).filter(w => w.length > 0);
        return {
            title: title || '',
            body,
            excerpt: body.slice(0, 500).trim(),
            author: author || undefined,
            date: date || undefined,
            wordCount: words.length,
        };
    }
    return null;
}
async function extractByDensity(page) {
    // Fallback: find the element with the highest text-to-tag ratio
    const result = await page.evaluate(() => {
        const candidates = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
        let node;
        while ((node = walker.nextNode())) {
            const tag = node.tagName.toLowerCase();
            if (['script', 'style', 'nav', 'header', 'footer', 'aside'].includes(tag))
                continue;
            const text = node.textContent || '';
            const trimmed = text.trim();
            if (trimmed.length < 300)
                continue;
            const children = node.children.length;
            const score = trimmed.length / (children + 1);
            candidates.push({ element: node, text: trimmed, score });
        }
        candidates.sort((a, b) => b.score - a.score);
        return candidates[0]?.text || null;
    });
    if (!result)
        return null;
    const title = await page.title();
    const words = result.split(/\s+/).filter(w => w.length > 0);
    return {
        title,
        body: result,
        excerpt: result.slice(0, 500).trim(),
        wordCount: words.length,
    };
}
export async function extractContent(page) {
    // Strategy 1: semantic selectors
    const semantic = await extractBySelectors(page);
    if (semantic)
        return semantic;
    // Strategy 2: text density heuristic
    const density = await extractByDensity(page);
    if (density)
        return density;
    // Strategy 3: full body text
    const body = await page.evaluate(() => document.body?.textContent?.trim() || '');
    const words = body.split(/\s+/).filter(w => w.length > 0);
    return {
        title: await page.title(),
        body,
        excerpt: body.slice(0, 500).trim(),
        wordCount: words.length,
    };
}
export async function extractWithCustomSelectors(page, selectors) {
    const selList = [];
    if (selectors.body)
        selList.push(selectors.body);
    const body = await trySelector(page, selList);
    const titleSel = [];
    if (selectors.title)
        titleSel.push(selectors.title);
    const title = await trySelector(page, titleSel);
    const authorSel = [];
    if (selectors.author)
        authorSel.push(selectors.author);
    const author = await trySelector(page, authorSel);
    const dateSel = [];
    if (selectors.date)
        dateSel.push(selectors.date);
    const date = await trySelector(page, dateSel);
    const text = body || '';
    const words = text.split(/\s+/).filter(w => w.length > 0);
    return {
        title: title || (await page.title()),
        body: text,
        excerpt: text.slice(0, 500).trim(),
        author: author || undefined,
        date: date || undefined,
        wordCount: words.length,
    };
}

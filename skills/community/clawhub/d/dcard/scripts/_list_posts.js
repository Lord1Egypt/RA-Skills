// Dcard forum post list extractor
// Used by dcard_fetch.py
(forumSlug) => {
    const items = [];
    const seen = new Set();
    const links = document.querySelectorAll('a[href*="/f/"][href*="/p/"]');
    links.forEach(a => {
        const href = a.href;
        if (seen.has(href)) return;
        seen.add(href);

        const m = href.match(/\/p\/(\d+)/);
        if (!m) return;
        const postId = m[1];

        const card = a.closest('[class*="PostList"], article, [class*="post_"], [class*="PostEntry"]');
        const fullText = card ? card.textContent : (a.textContent || '');

        // Extract title: longest meaningful line
        const allText = a.textContent.trim();
        const lines = allText.split('\n').map(s => s.trim()).filter(Boolean);
        let title = '';
        for (const line of lines) {
            if (/^\d+\s*(小時|分鐘|天|週|月|[hdwm])$/i.test(line.trim())) continue;
            if (/^\d+$/.test(line.trim())) continue;
            if (line.length < 4) continue;
            title = line;
            break;
        }
        if (!title) title = lines.find(l => l.length > 4) || '';
        if (!title || title.length < 3) return;

        // Extract time
        const timeMatch = fullText.match(/(\d+[hdwm])\s*/);
        const timeAgo = timeMatch ? timeMatch[1] : '';

        // Preview: text after title
        let preview = '';
        const titleIdx = fullText.indexOf(title);
        if (titleIdx >= 0) {
            preview = fullText.substring(titleIdx + title.length, titleIdx + title.length + 100)
                .replace(/\s+/g, ' ').trim();
        }

        items.push({
            title: title,
            post_id: postId,
            forum: forumSlug,
            time_ago: timeAgo,
            preview: preview.substring(0, 120),
        });
    });
    return items;
}

// BlogStudio — Electron Renderer
// Fixed and improved: 2026-06-15

let GITHUB_TOKEN = '';
let BASE_URL = '';
let currentView = 'posts';
let currentPost = null;

// Wait for init from main process
window.blogstudio.onInit((data) => {
    GITHUB_TOKEN = data.token;
    BASE_URL = data.baseUrl;
    console.log('BlogStudio initialized');
    loadContent('posts');
});

// ─── Status ────────────────────────────────────────────────────────────────

function showStatus(msg, type = 'info') {
    const el = document.getElementById('status');
    el.textContent = msg;
    el.className = 'status ' + type;
    el.style.display = 'block';
    setTimeout(() => el.style.display = 'none', 4000);
}

// ─── GitHub API ────────────────────────────────────────────────────────────

async function githubGet(apiPath) {
    try {
        return await window.blogstudio.githubGet(apiPath);
    } catch(e) {
        console.error('GitHub GET error:', e);
        return null;
    }
}

async function githubPut(apiPath, content, message) {
    try {
        return await window.blogstudio.githubPut(apiPath, content, message);
    } catch(e) {
        console.error('GitHub PUT error:', e);
        return null;
    }
}

async function githubDelete(apiPath, message) {
    try {
        return await window.blogstudio.githubDelete(apiPath, message);
    } catch(e) {
        console.error('GitHub DELETE error:', e);
        return null;
    }
}

// ─── Markdown ─────────────────────────────────────────────────────────────

function simpleMarkdown(text) {
    if (!text) return '<p style="color:#888">Preview will appear here...</p>';
    text = text.replace(/^---[\s\S]*?---\n/, '');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^### (.+)$/gm, '<h3>$3</h3>');
    text = text.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
    text = text.replace(/\*(.+?)\*/g, '<i>$1</i>');
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    text = text.replace(/```\w*\n([\s\S]*?)```/gm, '<pre><code>$1</code></pre>');
    text = text.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>');
    text = text.replace(/^---$/gm, '<hr>');
    text = text.replace(/\|(.+)\|/g, (m) => {
        const cells = m.split('|').filter(c => c.trim());
        if (cells.some(c => /-+/.test(c))) return '';
        return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
    });
    text = text.replace(/(<tr>.*?<\/tr>\n?)+/g, '<table>$&</table>');
    text = text.replace(/\n\n+/g, '</p><p>');
    return '<p>' + text + '</p>';
}

// ─── Navigation ───────────────────────────────────────────────────────────

document.querySelectorAll('.nav-item[data-view]').forEach(el => {
    el.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        const view = el.dataset.view;
        currentView = view;
        const titles = { posts: 'Blog Posts', guides: 'Guides', analysis: 'Analysis', pages: 'Pages' };
        document.getElementById('pageTitle').textContent = titles[view] || view;
        loadContent(view);
    });
});

// ─── Actions ──────────────────────────────────────────────────────────────

document.querySelectorAll('.nav-item[data-action]').forEach(el => {
    el.addEventListener('click', async () => {
        const action = el.dataset.action;

        if (action === 'sync') {
            showStatus('Syncing...');
            await loadContent(currentView);
            showStatus('Synced!', 'success');
        }

        if (action === 'new') {
            newPost();
        }

        if (action === 'site') {
            window.blogstudio.openExternal('https://thesolai.github.io');
        }

        if (action === 'blog') {
            window.blogstudio.openExternal('https://thesolai.github.io/blog/');
        }

        if (action === 'guides') {
            window.blogstudio.openExternal('https://thesolai.github.io/guides/');
        }
    });
});

// ─── Buttons ───────────────────────────────────────────────────────────────

document.getElementById('syncBtn').addEventListener('click', async () => {
    showStatus('Syncing...');
    await loadContent(currentView);
    showStatus('Synced!', 'success');
});

document.getElementById('publishBtn').addEventListener('click', async () => {
    await publishPost();
});

document.getElementById('saveDraftBtn').addEventListener('click', async () => {
    await saveDraft();
});

document.getElementById('previewBtn').addEventListener('click', () => {
    togglePreview();
});

document.getElementById('cancelEditBtn').addEventListener('click', () => {
    cancelEdit();
});

document.getElementById('deletePostBtn').addEventListener('click', async () => {
    if (currentPost && currentPost.filename) {
        await deletePost(currentPost.filename);
    }
});

document.getElementById('newPostBtn')?.addEventListener('click', () => {
    newPost();
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        if (e.key === 's') { e.preventDefault(); saveDraft(); }
        if (e.key === 'p') { e.preventDefault(); publishPost(); }
    }
    if (e.key === 'Escape') {
        cancelEdit();
    }
});

// ─── Post Operations ───────────────────────────────────────────────────────

function newPost() {
    currentPost = null;
    document.getElementById('postTitle').value = '';
    document.getElementById('postDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('postTags').value = '';
    document.getElementById('postContent').value = '';
    document.getElementById('contentList').style.display = 'none';
    document.getElementById('editor').classList.add('active');
    document.getElementById('postTitle').focus();
    document.getElementById('deletePostBtn').style.display = 'none';
    document.getElementById('viewOnGithubBtn').style.display = 'none';
    showPreview(false);
}

function cancelEdit() {
    document.getElementById('editor').classList.remove('active');
    document.getElementById('contentList').style.display = 'flex';
    document.getElementById('deletePostBtn').style.display = 'none';
    document.getElementById('viewOnGithubBtn').style.display = 'none';
    currentPost = null;
    showPreview(false);
}

function viewOnGithub() {
    if (currentPost && currentPost.path) {
        const url = `https://github.com/TheSolAI/thesolai.github.io/blob/main/${currentPost.path}`;
        window.blogstudio.openExternal(url);
    }
}

async function saveDraft() {
    const title = document.getElementById('postTitle').value;
    const content = document.getElementById('postContent').value;
    const date = document.getElementById('postDate').value;
    const tags = document.getElementById('postTags').value;

    if (!title || !content) {
        showStatus('Fill in title and content', 'error');
        return;
    }

    const slug = title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    const filename = `${date}-${slug}.md`;
    const frontmatter = buildFrontMatter(title, date, tags, content);
    const path = `_posts/${filename}`;

    showStatus('Saving draft...');
    const result = await githubPut(path, frontmatter, `Draft: ${title}`);
    if (result && result.content) {
        showStatus('Draft saved!', 'success');
        currentPost = { filename, title, date, tags, content };
    } else {
        showStatus('Save failed', 'error');
    }
}

async function publishPost() {
    const title = document.getElementById('postTitle').value;
    const content = document.getElementById('postContent').value;
    const date = document.getElementById('postDate').value;
    const tags = document.getElementById('postTags').value;

    if (!title || !content) {
        showStatus('Fill in title and content', 'error');
        return;
    }

    const slug = title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    const filename = `${date}-${slug}.md`;
    const frontmatter = buildFrontMatter(title, date, tags, content);
    const path = `_posts/${filename}`;

    showStatus('Publishing...');
    const result = await githubPut(path, frontmatter, `Published: ${title}`);
    if (result && result.content) {
        showStatus('Published to GitHub Pages!', 'success');
        currentPost = { filename, title, date, tags, content };
        // Open the live post
        const slugUrl = slug;
        window.blogstudio.openExternal(`https://thesolai.github.io/blog/${date.slice(0,7).replace('-', '/')}/${slugUrl}/`);
    } else {
        showStatus('Publish failed', 'error');
    }
}

async function deletePost(filename) {
    if (!confirm(`Delete ${filename}? This cannot be undone.`)) return;
    showStatus('Deleting...');
    const result = await githubDelete(`_posts/${filename}`, `Delete: ${filename}`);
    if (result) {
        showStatus('Deleted!', 'success');
        cancelEdit();
        await loadContent(currentView);
    } else {
        showStatus('Delete failed', 'error');
    }
}

// ─── Helpers ───────────────────────────────────────────────────────────────

function buildFrontMatter(title, date, tags, content) {
    const tagStr = tags ? tags.split(',').map(t => `"${t.trim()}"`).filter(t => t !== '""').join(', ') : '"blog"';
    return `---
title: "${title}"
date: ${date}
description: 
tags: [${tagStr}]
---

${content}`;
}

function parseFrontMatter(content) {
    const titleMatch = content.match(/title:\s*["']?([^"'\n]+)/);
    const dateMatch = content.match(/^date:\s*(\d{4}-\d{2}-\d{2})/m);
    const tagsMatch = content.match(/tags:\s*\[([^\]]+)\]/);
    const bodyMatch = content.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
    return {
        title: titleMatch ? titleMatch[1].replace(/"/g, '') : '',
        date: dateMatch ? dateMatch[1] : '',
        tags: tagsMatch ? tagsMatch[1].replace(/"/g, '').replace(/,/g, ', ') : '',
        body: bodyMatch ? bodyMatch[1] : content
    };
}

// ─── Preview ───────────────────────────────────────────────────────────────

let previewVisible = false;

function showPreview(visible) {
    const preview = document.getElementById('previewPane');
    if (preview) preview.style.display = visible ? 'block' : 'none';
    previewVisible = visible;
}

function togglePreview() {
    previewVisible = !previewVisible;
    const preview = document.getElementById('previewPane');
    const content = document.getElementById('postContent').value;
    if (previewVisible) {
        if (!preview) {
            const editor = document.getElementById('postContent');
            const pane = document.createElement('div');
            pane.id = 'previewPane';
            pane.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:#FDFBF7;z-index:1000;overflow:auto;padding:2rem;';
            pane.innerHTML = '<button onclick="togglePreview()" style="position:fixed;top:1rem;right:1rem;padding:0.5rem 1rem;cursor:pointer;">✕ Close Preview</button><div style="max-width:720px;margin:0 auto;padding-top:3rem;line-height:1.7;font-size:15px;">' + simpleMarkdown(content) + '</div>';
            document.body.appendChild(pane);
        }
        document.getElementById('previewPane').style.display = 'block';
    } else {
        if (preview) preview.style.display = 'none';
    }
}

// Live preview as you type
let previewTimeout = null;
document.getElementById('postContent')?.addEventListener('input', () => {
    if (previewVisible) {
        clearTimeout(previewTimeout);
        previewTimeout = setTimeout(() => {
            const content = document.getElementById('postContent').value;
            const previewDiv = document.querySelector('#previewPane > div');
            if (previewDiv) previewDiv.innerHTML = simpleMarkdown(content);
        }, 300);
    }
});

// ─── Load Content ─────────────────────────────────────────────────────────

async function loadContent(type) {
    const list = document.getElementById('contentList');
    const editor = document.getElementById('editor');

    editor.classList.remove('active');
    list.style.display = 'flex';
    list.innerHTML = '<div class="loading">Loading...</div>';

    const apiPathMap = { posts: '_posts', guides: 'guides', analysis: 'analysis', pages: '' };
    const apiPath = apiPathMap[type] || '';

    try {
        const data = await githubGet(apiPath);
        if (!data || !Array.isArray(data)) {
            list.innerHTML = '<div class="empty">No content found</div>';
            return;
        }

        const items = data.filter(f => {
            if (type === 'posts') return f.name.endsWith('.md');
            if (type === 'guides') return f.name.endsWith('.html');
            return true;
        });

        if (items.length === 0) {
            list.innerHTML = '<div class="empty">No ' + type + ' found</div>';
            return;
        }

        list.innerHTML = items.map(item => {
            const name = item.name
                .replace('.md', '').replace('.html', '')
                .replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase());
            const date = item.name.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] || '';
            return `
                <div class="content-card" data-path="${item.path}" data-name="${item.name}">
                    <h3>${name}</h3>
                    <div class="content-meta">${date}</div>
                </div>
            `;
        }).join('');

        // Click to edit
        document.querySelectorAll('.content-card').forEach(card => {
            card.addEventListener('click', async () => {
                const path = card.dataset.path;
                const itemData = await githubGet(path);
                if (itemData && itemData.content) {
                    const rawContent = decodeURIComponent(encodeURIComponent(atob(itemData.content)));
                    const meta = parseFrontMatter(rawContent);

                    currentPost = {
                        filename: card.dataset.name,
                        path: path,
                        title: meta.title,
                        date: meta.date,
                        tags: meta.tags,
                        content: meta.body
                    };

                    // Show delete button for existing posts
                    document.getElementById('deletePostBtn').style.display = 'inline-block';
                    document.getElementById('viewOnGithubBtn').style.display = 'inline-block';

                    document.getElementById('postTitle').value = meta.title;
                    document.getElementById('postDate').value = meta.date || new Date().toISOString().split('T')[0];
                    document.getElementById('postTags').value = meta.tags;
                    document.getElementById('postContent').value = meta.body;

                    list.style.display = 'none';
                    editor.classList.add('active');
                    showPreview(false);
                }
            });
        });

    } catch(e) {
        console.error('Load error:', e);
        list.innerHTML = '<div class="empty">Error loading content</div>';
    }
}

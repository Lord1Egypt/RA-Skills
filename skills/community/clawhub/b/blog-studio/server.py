#!/usr/bin/env python3
"""BlogStudio standalone server — injects GH token and serves the app."""

import subprocess
import http.server
import socketserver
import webbrowser

PORT = 8765

def get_token():
    try:
        return subprocess.run(
            ['gh', 'auth', 'token'],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None

def serve_html(token):
    api_base = 'https://api.github.com/repos/TheSolAI/thesolai.github.io'

    html = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlogStudio — Sol AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #FDFBF7;
            --bg-secondary: #F5F0E6;
            --text-primary: #111111;
            --text-secondary: #444444;
            --text-muted: #888888;
            --k-yellow: #FFD166;
            --k-red: #E63946;
            --k-ink: #111111;
            --k-blue: #457B9D;
            --k-white: #FFFFFF;
            --k-green: #2A9D8F;
            --k-stroke: 3px solid var(--k-ink);
            --k-shadow: 5px 5px 0px var(--k-ink);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Comic Neue', cursive; font-weight: 700; background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; }
        h1, h2, h3 { font-family: 'Bangers', cursive; letter-spacing: 2px; text-transform: uppercase; }

        .app { display: flex; min-height: 100vh; }
        .sidebar { width: 260px; background: var(--k-yellow); border-right: var(--k-stroke); padding: 1rem; position: fixed; height: 100vh; overflow-y: auto; }
        .main { flex: 1; margin-left: 260px; padding: 2rem; max-width: 1000px; }

        .sidebar-logo { font-family: 'Bangers', cursive; font-size: 1.8rem; color: var(--k-ink); margin-bottom: 1.5rem; }
        .sidebar-logo span { color: var(--k-red); }
        .nav-section { margin-bottom: 1.5rem; }
        .nav-title { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem; }
        .nav-item { display: block; padding: 0.5rem 0.75rem; color: var(--k-ink); text-decoration: none; border: 2px solid transparent; margin-bottom: 0.25rem; cursor: pointer; }
        .nav-item:hover { border: 2px solid var(--k-ink); background: var(--k-white); }
        .nav-item.active { background: var(--k-ink); color: var(--k-white); }

        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: var(--k-stroke); }
        .header h1 { font-size: 2rem; }
        .btn { font-family: 'Bangers', cursive; padding: 0.5rem 1rem; border: var(--k-stroke); cursor: pointer; font-size: 0.9rem; letter-spacing: 1px; text-decoration: none; display: inline-block; background: var(--k-yellow); box-shadow: 3px 3px 0 var(--k-ink); }
        .btn:hover { transform: translate(-2px, -2px); box-shadow: 5px 5px 0 var(--k-ink); }
        .btn-success { background: var(--k-green); color: white; }
        .btn-danger { background: var(--k-red); color: white; }

        .content-list { display: flex; flex-direction: column; gap: 1rem; }
        .content-card { background: var(--k-white); border: var(--k-stroke); padding: 1.25rem; box-shadow: var(--k-shadow); cursor: pointer; transition: all 0.1s; }
        .content-card:hover { transform: translate(-3px, -3px); box-shadow: 8px 8px 0 var(--k-ink); }
        .content-card h3 { margin-bottom: 0.25rem; font-size: 1.1rem; }
        .content-meta { font-size: 0.75rem; color: var(--text-muted); }

        .editor { display: none; }
        .editor.active { display: block; }
        .editor-field { margin-bottom: 1.25rem; }
        .editor-field label { display: block; font-weight: 700; font-size: 0.8rem; margin-bottom: 0.25rem; text-transform: uppercase; }
        .editor-field input, .editor-field textarea { width: 100%; padding: 0.75rem; border: 2px solid var(--k-ink); font-family: inherit; font-size: 0.95rem; }
        .editor-field input:focus, .editor-field textarea:focus { outline: none; border-color: var(--k-red); }
        .editor-field textarea { min-height: 280px; font-family: 'Consolas', monospace; resize: vertical; }
        .editor-row { display: flex; gap: 1rem; }
        .editor-row .editor-field { flex: 1; }
        .editor-actions { display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap; }

        .preview { background: var(--bg-secondary); border: 2px dashed var(--k-ink); padding: 1.5rem; margin-top: 1rem; min-height: 200px; max-height: 400px; overflow-y: auto; font-family: 'Comic Neue', cursive; }
        .preview h1 { font-size: 1.6rem; margin-bottom: 1rem; }
        .preview h2 { font-size: 1.3rem; margin: 1rem 0 0.5rem; }
        .preview h3 { font-size: 1.1rem; margin: 0.75rem 0 0.5rem; }
        .preview p { margin-bottom: 0.75rem; line-height: 1.6; }
        .preview code { background: #eee; padding: 0.1rem 0.3rem; font-family: Consolas, monospace; }
        .preview pre { background: var(--k-ink); color: var(--k-white); padding: 1rem; overflow-x: auto; margin: 1rem 0; }
        .preview pre code { background: none; padding: 0; }
        .preview blockquote { border-left: 4px solid var(--k-red); padding-left: 1rem; color: var(--text-secondary); margin: 1rem 0; }
        .preview a { color: var(--k-blue); }

        .status { position: fixed; bottom: 1rem; right: 1rem; padding: 0.75rem 1rem; background: var(--k-ink); color: var(--k-white); font-size: 0.8rem; z-index: 100; opacity: 0; transition: opacity 0.2s; }
        .status.visible { opacity: 1; }
        .status.success { background: var(--k-green); }
        .status.error { background: var(--k-red); }

        .loading, .empty, .error-state { text-align: center; padding: 3rem; color: var(--text-muted); }
        .error-state { color: var(--k-red); }
        .spinner { font-size: 2rem; animation: pulse 1s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
    </style>
</head>
<body>
    <div class="app">
        <aside class="sidebar">
            <div class="sidebar-logo">Blog<span>Studio</span></div>

            <div class="nav-section">
                <div class="nav-title">Content</div>
                <div class="nav-item active" data-view="posts">📝 Blog Posts</div>
                <div class="nav-item" data-view="guides">📖 Guides</div>
                <div class="nav-item" data-view="pages">📄 Pages</div>
            </div>

            <div class="nav-section">
                <div class="nav-title">Actions</div>
                <div class="nav-item" data-action="new">✏️ New Post</div>
                <div class="nav-item" data-action="sync">🔄 Sync</div>
            </div>

            <div class="nav-section">
                <div class="nav-title">Live Site</div>
                <div class="nav-item" id="siteLink">🌐 thesolai.github.io</div>
            </div>
        </aside>

        <main class="main">
            <div class="header">
                <h1 id="pageTitle">Blog Posts</h1>
                <div>
                    <button class="btn" id="syncBtn">🔄 Sync</button>
                    <button class="btn btn-success" id="publishBtn" style="display:none">🚀 Publish</button>
                </div>
            </div>

            <div id="contentList" class="content-list"></div>

            <div id="editor" class="editor">
                <div class="editor-row">
                    <div class="editor-field" style="flex:2">
                        <label>Title</label>
                        <input type="text" id="postTitle" placeholder="Post title">
                    </div>
                    <div class="editor-field">
                        <label>Date</label>
                        <input type="date" id="postDate">
                    </div>
                </div>
                <div class="editor-field">
                    <label>Tags (comma separated)</label>
                    <input type="text" id="postTags" placeholder="blog, ai, technical">
                </div>
                <div class="editor-field">
                    <label>Content (Markdown)</label>
                    <textarea id="postContent" placeholder="Write your post in Markdown..."></textarea>
                </div>
                <div class="editor-field">
                    <label>Preview</label>
                    <div id="postPreview" class="preview"></div>
                </div>
                <div class="editor-actions">
                    <button class="btn btn-success" id="publishBtnEditor">🚀 Publish</button>
                    <button class="btn btn-danger" id="cancelBtn">Cancel</button>
                </div>
            </div>
        </main>
    </div>

    <div id="status" class="status"></div>

    <script>
    const API_BASE = 'https://api.github.com/repos/TheSolAI/thesolai.github.io';
    const SITE_URL = 'https://thesolai.github.io';
    let token = 'INJECTED';
    let currentView = 'posts';
    let currentItem = null;

    function showStatus(msg, type) {
        type = type || 'info';
        const el = document.getElementById('status');
        el.textContent = msg;
        el.className = 'status visible ' + type;
        clearTimeout(el._timer);
        el._timer = setTimeout(() => el.classList.remove('visible'), 3500);
    }

    async function githubGet(path) {
        const res = await fetch(API_BASE + '/contents/' + path, {
            headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json' }
        });
        if (!res.ok) throw new Error(await res.text());
        return res.json();
    }

    async function githubPut(path, content, message) {
        const res = await fetch(API_BASE + '/contents/' + path, {
            method: 'PUT',
            headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                content: btoa(unescape(encodeURIComponent(content))),
                branch: 'main'
            })
        });
        if (!res.ok) throw new Error(await res.text());
        return res.json();
    }

    function updatePreview() {
        const md = document.getElementById('postContent').value;
        const el = document.getElementById('postPreview');
        if (!md.trim()) {
            el.innerHTML = '<p style="color:#888">Start writing to see preview...</p>';
            return;
        }
        let html = md;
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
        html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
        const paras = html.split(/\n\n+/);
        html = paras.map(p => p.startsWith('<') && p.endsWith('>') ? p : '<p>' + p.replace(/\n/g, '<br>') + '</p>').join('');
        el.innerHTML = html;
    }

    function parseFrontmatter(raw) {
        const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
        if (!match) return { body: raw };
        const fm = { body: match[2] };
        match[1].split('\n').forEach(line => {
            const m = line.match(/^(\w+):\s*(.*)$/);
            if (m) fm[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
        });
        return fm;
    }

    async function loadContent(type) {
        const list = document.getElementById('contentList');
        document.getElementById('editor').classList.remove('active');
        document.getElementById('publishBtn').style.display = 'none';
        list.style.display = 'flex';
        currentView = type;
        currentItem = null;
        list.innerHTML = '<div class="loading"><div class="spinner">📂</div>Loading...</div>';

        const pathMap = { posts: '_posts', guides: 'guides', pages: '' };
        const filterFn = type === 'posts'  ? f => f.name.endsWith('.md')
                       : type === 'guides' ? f => f.name.endsWith('.html')
                       : f => true;
        try {
            const data = await githubGet(pathMap[type]);
            const items = Array.isArray(data) ? data.filter(filterFn) : [];
            if (items.length === 0) {
                list.innerHTML = '<div class="empty">No ' + type + ' found. <span class="btn" style="margin-top:1rem;display:inline-block;cursor:pointer" onclick="newPost()">✏️ Create one</span></div>';
                return;
            }
            list.innerHTML = items.map(item => {
                const name = item.name;
                const dateMatch = name.match(/^(\d{4}-\d{2}-\d{2})/);
                const date = dateMatch ? dateMatch[1] : '';
                const slug = name.replace(/\.(md|html)$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
                const displayName = slug.replace(/-/g, ' ').replace(/^./, c => c.toUpperCase());
                return '<div class="content-card" data-path="' + item.path + '" data-name="' + name + '"><h3>' + displayName + '</h3><div class="content-meta">' + (date || 'Unknown') + '</div></div>';
            }).join('');
            list.querySelectorAll('.content-card').forEach(card => {
                card.addEventListener('click', () => openEditor(card.dataset.path, card.dataset.name));
            });
        } catch(e) {
            list.innerHTML = '<div class="error-state">Error: ' + e.message + '</div>';
        }
    }

    async function openEditor(path, name) {
        document.getElementById('contentList').style.display = 'none';
        document.getElementById('editor').classList.add('active');
        document.getElementById('publishBtn').style.display = 'inline-block';
        currentItem = { path, name };
        try {
            const data = await githubGet(path);
            const raw = decodeURIComponent(escape(atob(data.content)));
            const fm = parseFrontmatter(raw);
            document.getElementById('postTitle').value = fm.title || name.replace(/\.(md|html)$/, '').replace(/-/g, ' ');
            document.getElementById('postDate').value = fm.date || new Date().toISOString().split('T')[0];
            document.getElementById('postTags').value = fm.tags || 'blog';
            document.getElementById('postContent').value = fm.body || raw;
            updatePreview();
        } catch(e) {
            showStatus('Error: ' + e.message, 'error');
        }
    }

    function newPost() {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        document.getElementById('pageTitle').textContent = 'New Post';
        document.getElementById('contentList').style.display = 'none';
        document.getElementById('editor').classList.add('active');
        document.getElementById('publishBtn').style.display = 'inline-block';
        document.getElementById('postTitle').value = '';
        document.getElementById('postDate').value = new Date().toISOString().split('T')[0];
        document.getElementById('postTags').value = 'blog';
        document.getElementById('postContent').value = '';
        document.getElementById('postPreview').innerHTML = '<p style="color:#888">Start writing to see preview...</p>';
        currentItem = null;
    }

    async function publish() {
        const title = document.getElementById('postTitle').value.trim();
        const date = document.getElementById('postDate').value;
        const tags = document.getElementById('postTags').value.trim();
        const body = document.getElementById('postContent').value;
        if (!title || !body) { showStatus('Title and content required', 'error'); return; }
        const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        const filename = currentItem ? currentItem.name : date + '-' + slug + '.md';
        const path = currentItem ? currentItem.path : '_posts/' + filename;
        const content = '---\ntitle: "' + title + '"\ndate: ' + date + '\ndescription: \ntags: ' + (tags || 'blog') + '\n---\n\n' + body;
        showStatus('Publishing...');
        try {
            const result = await githubPut(path, content, 'Publish: ' + title);
            if (result.error) throw new Error(result.message);
            showStatus('Published!', 'success');
            setTimeout(() => loadContent(currentView), 1200);
        } catch(e) {
            showStatus('Failed: ' + e.message, 'error');
        }
    }

    document.querySelectorAll('.nav-item[data-view]').forEach(el => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('pageTitle').textContent = el.textContent;
            document.getElementById('editor').classList.remove('active');
            loadContent(el.dataset.view);
        });
    });

    document.querySelectorAll('.nav-item[data-action]').forEach(el => {
        el.addEventListener('click', () => {
            if (el.dataset.action === 'new') newPost();
            if (el.dataset.action === 'sync') { showStatus('Syncing...'); loadContent(currentView).then(() => showStatus('Synced!', 'success')); }
        });
    });

    document.getElementById('siteLink').addEventListener('click', () => window.open(SITE_URL, '_blank'));
    document.getElementById('syncBtn').addEventListener('click', () => { showStatus('Syncing...'); loadContent(currentView).then(() => showStatus('Synced!', 'success')); });
    document.getElementById('publishBtn').addEventListener('click', publish);
    document.getElementById('publishBtnEditor').addEventListener('click', publish);
    document.getElementById('cancelBtn').addEventListener('click', () => {
        document.getElementById('editor').classList.remove('active');
        document.getElementById('contentList').style.display = 'flex';
        document.getElementById('publishBtn').style.display = 'none';
        loadContent(currentView);
    });
    document.getElementById('postContent').addEventListener('input', updatePreview);

    loadContent('posts');
    </script>
</body>
</html>'''

    return html.replace("token = 'INJECTED'", f"token = '{token}'")

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        token = get_token()
        if not token:
            self.send_response(401)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>No GitHub token. Run: gh auth login</h1></body></html>')
            return

        html = serve_html(token)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    token = get_token()
    if not token:
        print('ERROR: No GitHub token. Run: gh auth login')
        exit(1)

    print(f'BlogStudio running at http://localhost:{PORT}')
    webbrowser.open(f'http://localhost:{PORT}')

    with socketserver.TCPServer(('localhost', PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()

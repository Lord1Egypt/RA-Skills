#!/usr/bin/env python3
"""
BlogStudio — Sol AI Content Management System
Standalone Python GUI App
"""

import os
import re
import json
import subprocess
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import webbrowser
import urllib.parse

# ── GitHub Config ─────────────────────────────────────────────────────────────
def get_gh_token():
    """Get GitHub token via gh CLI."""
    try:
        result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

REPO_OWNER = "TheSolAI"
REPO_NAME = "thesolai.github.io"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

# ── Markdown → HTML ────────────────────────────────────────────────────────────
def md_to_html(md):
    """Convert markdown to HTML for preview."""
    if not md:
        return '<p style="color:#888">Nothing to preview yet...</p>'
    html = md
    # Code blocks
    html = re.sub(r'```(\w*)\n([\s\S]*?)```', r'<pre><code class="\1">\2</code></pre>', html)
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold / italic
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    # Lists
    html = re.sub(r'^- (.+)', r'<li>\1</li>', html)
    html = re.sub(r'^(\d+)\. (.+)', r'<li>\2</li>', html)
    # Paragraphs
    paragraphs = re.split(r'\n\n+', html)
    html = '\n'.join(f'<p>{p.strip()}</p>' if not p.startswith('<') and not p.endswith('>') else p for p in paragraphs)
    # Clean up newlines
    html = html.replace('\n', '<br>')
    return html

# ── GitHub API ────────────────────────────────────────────────────────────────────
def gh_get(path, token):
    """GET request to GitHub API."""
    url = f"{BASE_URL}/contents/{path}" if path else BASE_URL
    req = Request(url, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    })
    try:
        res = urlopen(req)
        return json.loads(res.read())
    except HTTPError as e:
        return {'error': e.code, 'message': e.read().decode()}

def gh_put(path, content, message, token):
    """PUT request to GitHub API to create/update a file."""
    import base64
    url = f"{BASE_URL}/contents/{path}"
    body = json.dumps({
        'message': message,
        'content': base64.b64encode(content.encode()).decode(),
        'branch': 'main'
    }).encode()
    req = Request(url, method='PUT', headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    })
    try:
        res = urlopen(req)
        return json.loads(res.read())
    except HTTPError as e:
        return {'error': e.code, 'message': e.read().decode()}

def parse_frontmatter(raw_content):
    """Parse YAML frontmatter from raw file content."""
    match = re.match(r'^---\n([\s\S]*?)\n---\n([\s\S]*)$', raw_content)
    if not match:
        return {'raw': raw_content}, raw_content
    fm_text, body = match.groups()
    fm = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm, body

def build_frontmatter(title, date, tags, body):
    """Build a post file with frontmatter."""
    return f'''---
title: "{title}"
date: {date}
description: 
tags: {tags or 'blog'}
---

{body}'''

# ── HTML Template ─────────────────────────────────────────────────────────────
def make_html(token):
    GITHUB_PAGES_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlogStudio — Sol AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
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
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Comic Neue', cursive; font-weight: 700; background: var(--bg-primary); color: var(--text-primary); min-height: 100vh; }}
        h1, h2, h3 {{ font-family: 'Bangers', cursive; letter-spacing: 2px; text-transform: uppercase; }}
        
        .app {{ display: flex; min-height: 100vh; }}
        .sidebar {{ width: 260px; background: var(--k-yellow); border-right: var(--k-stroke); padding: 1rem; position: fixed; height: 100vh; overflow-y: auto; }}
        .main {{ flex: 1; margin-left: 260px; padding: 2rem; max-width: 1000px; }}
        
        .sidebar-logo {{ font-family: 'Bangers', cursive; font-size: 1.8rem; color: var(--k-ink); margin-bottom: 1.5rem; }}
        .sidebar-logo span {{ color: var(--k-red); }}
        .nav-section {{ margin-bottom: 1.5rem; }}
        .nav-title {{ font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem; }}
        .nav-item {{ display: block; padding: 0.5rem 0.75rem; color: var(--k-ink); text-decoration: none; border: 2px solid transparent; margin-bottom: 0.25rem; cursor: pointer; }}
        .nav-item:hover {{ border: 2px solid var(--k-ink); background: var(--k-white); }}
        .nav-item.active {{ background: var(--k-ink); color: var(--k-white); }}
        
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: var(--k-stroke); }}
        .header h1 {{ font-size: 2rem; }}
        .btn {{ font-family: 'Bangers', cursive; padding: 0.5rem 1rem; border: var(--k-stroke); cursor: pointer; font-size: 0.9rem; letter-spacing: 1px; }}
        .btn:hover {{ transform: translate(-2px, -2px); box-shadow: 5px 5px 0 var(--k-ink); }}
        .btn-primary {{ background: var(--k-yellow); box-shadow: 3px 3px 0 var(--k-ink); }}
        .btn-success {{ background: var(--k-green); color: white; }}
        .btn-danger {{ background: var(--k-red); color: white; }}
        .btn-blue {{ background: var(--k-blue); color: white; }}
        
        .content-list {{ display: flex; flex-direction: column; gap: 1rem; }}
        .content-card {{ background: var(--k-white); border: var(--k-stroke); padding: 1.25rem; box-shadow: var(--k-shadow); cursor: pointer; transition: all 0.1s; }}
        .content-card:hover {{ transform: translate(-3px, -3px); box-shadow: 8px 8px 0 var(--k-ink); }}
        .content-card h3 {{ margin-bottom: 0.25rem; font-size: 1.1rem; }}
        .content-card h3 a {{ color: var(--k-ink); text-decoration: none; }}
        .content-card h3 a:hover {{ color: var(--k-red); }}
        .content-meta {{ font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.25rem; }}
        .content-tags {{ font-size: 0.7rem; color: var(--k-blue); }}
        
        .editor {{ display: none; }}
        .editor.active {{ display: block; }}
        .editor-field {{ margin-bottom: 1.25rem; }}
        .editor-field label {{ display: block; font-weight: 700; font-size: 0.8rem; margin-bottom: 0.25rem; text-transform: uppercase; }}
        .editor-field input, .editor-field textarea {{ width: 100%; padding: 0.75rem; border: 2px solid var(--k-ink); font-family: inherit; font-size: 0.95rem; }}
        .editor-field input:focus, .editor-field textarea:focus {{ outline: none; border-color: var(--k-red); }}
        .editor-field textarea {{ min-height: 280px; font-family: 'Consolas', monospace; resize: vertical; }}
        .editor-row {{ display: flex; gap: 1rem; }}
        .editor-row .editor-field {{ flex: 1; }}
        .editor-actions {{ display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap; }}
        
        .preview {{ background: var(--bg-secondary); border: 2px dashed var(--k-ink); padding: 1.5rem; margin-top: 1rem; min-height: 200px; max-height: 400px; overflow-y: auto; }}
        .preview h1 {{ font-size: 1.8rem; margin-bottom: 1rem; border-bottom: 2px solid var(--k-ink); padding-bottom: 0.5rem; }}
        .preview h2 {{ font-size: 1.4rem; margin: 1.25rem 0 0.5rem; }}
        .preview h3 {{ font-size: 1.1rem; margin: 1rem 0 0.5rem; }}
        .preview p {{ margin-bottom: 0.75rem; line-height: 1.6; }}
        .preview code {{ background: #eee; padding: 0.1rem 0.3rem; font-family: Consolas, monospace; }}
        .preview pre {{ background: var(--k-ink); color: var(--k-white); padding: 1rem; overflow-x: auto; margin: 1rem 0; }}
        .preview pre code {{ background: none; padding: 0; }}
        .preview blockquote {{ border-left: 4px solid var(--k-red); padding-left: 1rem; color: var(--text-secondary); margin: 1rem 0; }}
        .preview a {{ color: var(--k-blue); }}
        .preview li {{ margin-left: 1.5rem; margin-bottom: 0.25rem; }}
        
        .status {{ position: fixed; bottom: 1rem; right: 1rem; padding: 0.75rem 1rem; background: var(--k-ink); color: var(--k-white); font-size: 0.8rem; z-index: 100; }}
        .status.success {{ background: var(--k-green); }}
        .status.error {{ background: var(--k-red); }}
        
        .loading, .empty, .error-state {{ text-align: center; padding: 3rem; color: var(--text-muted); }}
        .error-state {{ color: var(--k-red); }}
        .loading .spinner {{ font-size: 2rem; animation: pulse 1s infinite; }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
        
        .tag {{ display: inline-block; background: var(--k-blue); color: white; font-size: 0.65rem; padding: 0.1rem 0.4rem; margin-right: 0.25rem; }}
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
                <div class="nav-item" data-action="site">🌐 {REPO_PAGES_URL}</div>
                <div class="nav-item" data-action="blog">📝 Blog</div>
                <div class="nav-item" data-action="guides">📖 Guides</div>
            </div>
        </aside>
        
        <main class="main">
            <div class="header">
                <h1 id="pageTitle">Blog Posts</h1>
                <div>
                    <button class="btn btn-primary" id="syncBtn">🔄 Sync</button>
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
                    <button class="btn btn-primary" id="saveDraftBtn">💾 Save Draft</button>
                    <button class="btn btn-success" id="publishBtnEditor">🚀 Publish</button>
                    <button class="btn btn-danger" id="cancelEditBtn">Cancel</button>
                </div>
            </div>
        </main>
    </div>
    
    <div id="status" class="status" style="display:none;"></div>
    
    <script>
    const TOKEN = "{token}";
    const API_BASE = "{BASE_URL}";
    const currentView = {{ type: 'posts', item: null }};
    
    // ── Status ──
    function showStatus(msg, type = 'info') {{
        const el = document.getElementById('status');
        el.textContent = msg;
        el.className = 'status ' + type;
        el.style.display = 'block';
        clearTimeout(el._timer);
        el._timer = setTimeout(() => el.style.display = 'none', 3500);
    }}
    
    // ── GitHub API ──
    async function githubGet(path) {{
        const res = await fetch(API_BASE + '/contents/' + path, {{
            headers: {{ 'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github.v3+json' }}
        }});
        return res.json();
    }}
    
    async function githubPut(path, content, message) {{
        const res = await fetch(API_BASE + '/contents/' + path, {{
            method: 'PUT',
            headers: {{ 'Authorization': 'token ' + TOKEN, 'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ message, content: btoa(unescape(encodeURIComponent(content))), branch: 'main' }})
        }});
        return res.json();
    }}
    
    // ── Markdown Preview ──
    function updatePreview() {{
        const md = document.getElementById('postContent').value;
        const el = document.getElementById('postPreview');
        if (!md.trim()) {{
            el.innerHTML = '<p style="color:#888">Start writing to see preview...</p>';
            return;
        }}
        // Simple client-side markdown rendering
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
        html = paras.map(p => {{
            if (p.startsWith('<') && p.endsWith('>')) return p;
            return '<p>' + p.replace(/\n/g, '<br>') + '</p>';
        }}).join('');
        el.innerHTML = html;
    }}
    
    // ── Content Loader ──
    async function loadContent(type) {{
        const list = document.getElementById('contentList');
        const editor = document.getElementById('editor');
        const publishBtn = document.getElementById('publishBtn');
        
        editor.classList.remove('active');
        publishBtn.style.display = 'none';
        list.style.display = 'flex';
        currentView.type = type;
        currentView.item = null;
        
        list.innerHTML = '<div class="loading"><div class="spinner">📂</div>Loading...</div>';
        
        const pathMap = {{ posts: '_posts', guides: 'guides', pages: '' }};
        const filterFn = type === 'posts' ? f => f.name.endsWith('.md')
                    : type === 'guides' ? f => f.name.endsWith('.html')
                    : f => f.name.endsWith('.html') || f.name.endsWith('.md');
        
        try {{
            const data = await githubGet(pathMap[type]);
            const items = Array.isArray(data) ? data.filter(filterFn) : [];
            
            if (items.length === 0) {{
                list.innerHTML = '<div class="empty">No {0} found. <span class="nav-item" data-action="new" style="display:inline;cursor:pointer;color:#E63946">Create one →</span></div>';
                return;
            }}
            
            list.innerHTML = items.map(item => {{
                const name = item.name;
                const dateMatch = name.match(/^(\d{{4}}-\d{{2}}-\d{{2}})/);
                const date = dateMatch ? dateMatch[1] : 'Unknown';
                const slug = name.replace(/\.(md|html)$/, '').replace(/^\d{{4}}-\d{{2}-\d{{2}}-/, '');
                const displayName = slug.replace(/-/g, ' ').replace(/^./, c => c.toUpperCase());
                return `<div class="content-card" data-path="${{item.path}}" data-name="${{name}}">
                    <h3><a href="#">${{displayName}}</a></h3>
                    <div class="content-meta">${{date}}</div>
                </div>`;
            }}).join('');
            
            // Click cards to edit
            list.querySelectorAll('.content-card').forEach(card => {{
                card.addEventListener('click', async () => {{
                    await openEditor(card.dataset.path, card.dataset.name);
                }});
            }});
            
        }} catch(e) {{
            list.innerHTML = '<div class="error-state">Error loading: ' + e.message + '</div>';
        }}
    }}
    
    async function openEditor(path, name) {{
        const editor = document.getElementById('editor');
        const list = document.getElementById('contentList');
        const publishBtn = document.getElementById('publishBtn');
        
        editor.classList.add('active');
        list.style.display = 'none';
        publishBtn.style.display = 'inline-block';
        currentView.item = {{ path, name }};
        
        try {{
            const data = await githubGet(path);
            if (data.error) {{
                showStatus('Error loading file', 'error');
                return;
            }}
            const raw = decodeURIComponent(escape(atob(data.content)));
            const fm = parseFrontmatter(raw);
            
            document.getElementById('postTitle').value = fm.title || name.replace(/\.(md|html)$/, '').replace(/-/g, ' ');
            document.getElementById('postDate').value = fm.date || new Date().toISOString().split('T')[0];
            document.getElementById('postTags').value = fm.tags || 'blog';
            document.getElementById('postContent').value = fm.body || raw;
            updatePreview();
        }} catch(e) {{
            showStatus('Error: ' + e.message, 'error');
        }}
    }}
    
    function parseFrontmatter(raw) {{
        const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
        if (!match) return {{ body: raw }};
        const fm = {{ body: match[2] }};
        match[1].split('\n').forEach(line => {{
            const m = line.match(/^(\w+):\s*(.*)$/);
            if (m) fm[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
        }});
        return fm;
    }}
    
    // ── Publish ──
    async function publish() {{
        const title = document.getElementById('postTitle').value.trim();
        const date = document.getElementById('postDate').value;
        const tags = document.getElementById('postTags').value.trim();
        const body = document.getElementById('postContent').value;
        
        if (!title || !body) {{
            showStatus('Title and content required', 'error');
            return;
        }}
        
        const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        const filename = currentView.item ? currentView.item.name : `${{date}}-${{slug}}.md`;
        const path = currentView.item ? currentView.item.path : `_posts/${{filename}}`;
        
        const content = `---
title: "${{title}}"
date: ${{date}}
description: 
tags: ${{tags || 'blog'}}
---

${{body}}`;
        
        showStatus('Publishing...');
        const result = await githubPut(path, content, `Publish: ${{title}}`);
        if (result.error) {{
            showStatus('Failed: ' + result.message, 'error');
        }} else {{
            showStatus('Published!', 'success');
            setTimeout(() => loadContent(currentView.type), 1000);
        }}
    }}
    
    // ── Navigation ──
    document.querySelectorAll('.nav-item[data-view]').forEach(el => {{
        el.addEventListener('click', () => {{
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('pageTitle').textContent = el.textContent;
            document.getElementById('editor').classList.remove('active');
            loadContent(el.dataset.view);
        }});
    }});
    
    document.querySelectorAll('.nav-item[data-action]').forEach(el => {{
        el.addEventListener('click', async () => {{
            const action = el.dataset.action;
            if (action === 'new') {{
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
                currentView.item = null;
            }}
            if (action === 'sync') {{
                showStatus('Syncing...');
                await loadContent(currentView.type);
                showStatus('Synced!', 'success');
            }}
            if (action === 'site') window.open('{" + GITHUB_PAGES_URL + "}', '_blank');
            if (action === 'blog') window.open('{" + GITHUB_PAGES_URL + "}/blog/', '_blank');
            if (action === 'guides') window.open('{" + GITHUB_PAGES_URL + "}/guides/', '_blank');
        }});
    }});
    
    document.getElementById('syncBtn').addEventListener('click', async () => {{
        showStatus('Syncing...');
        await loadContent(currentView.type);
        showStatus('Synced!', 'success');
    }});
    
    document.getElementById('publishBtn').addEventListener('click', publish);
    document.getElementById('publishBtnEditor').addEventListener('click', publish);
    
    document.getElementById('cancelEditBtn').addEventListener('click', () => {{
        document.getElementById('editor').classList.remove('active');
        document.getElementById('contentList').style.display = 'flex';
        document.getElementById('publishBtn').style.display = 'none';
        loadContent(currentView.type);
    }});
    
    document.getElementById('postContent').addEventListener('input', updatePreview);
    
    // ── Init ──
    loadContent('posts');
    </script>
</body>
</html>'''

# ── HTTP Server ────────────────────────────────────────────────────────────────
class BlogStudioHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse token at request time (gh CLI call)
        token = get_gh_token()
        if not token:
            self.send_response(401)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>GitHub token not found. Run: gh auth login</h1></body></html>')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(make_html(token).encode())
    
    def log_message(self, format, *args):
        pass

def start_server(port=8765):
    token = get_gh_token()
    if not token:
        print('ERROR: No GitHub token. Run: gh auth login')
        return
    
    server = HTTPServer(('localhost', port), BlogStudioHandler)
    print(f'BlogStudio running at http://localhost:{port}')
    webbrowser.open(f'http://localhost:{port}')
    server.serve_forever()

if __name__ == '__main__':
    start_server()
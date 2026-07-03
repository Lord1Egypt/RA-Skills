#!/usr/bin/env python3
"""
Blog Composer HTTP Server — with Git push
==========================================
Serves the UI and handles post save/load/publish operations.
Publish = save + git add + git commit + git push.
"""

import http.server
import socketserver
import json
import os
import re
import subprocess
import urllib.parse
from pathlib import Path
from datetime import datetime

PORT = 8791
BLOG_DIR = Path("/Users/amre/Projects/thesolai.github.io")
SERVE_DIR = Path(__file__).parent.parent

def git_run(*args, cwd=BLOG_DIR):
    """Run a git command. Returns (ok, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def parse_front_matter(content):
    """Extract metadata from Jekyll front matter."""
    meta = {
        "title": "",
        "date": "",
        "description": "",
        "categories": "",
        "tags": "",
        "layout": "post"
    }
    m = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if not m:
        return meta
    for line in m.group(1).split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            if key in meta:
                meta[key] = value
    # Parse arrays: [a, b, c] -> a, b, c
    for key in ('categories', 'tags'):
        if meta[key].startswith('['):
            inner = meta[key][1:-1]
            items = [i.strip().strip('"').strip("'") for i in inner.split(',')]
            meta[key] = ', '.join(i for i in items if i)
    return meta

def build_front_matter(title, date, description, categories, tags):
    """Build Jekyll front matter string."""
    cats = categories or 'reflections'
    tag_list = tags or ''
    if tag_list and not tag_list.startswith('['):
        # Comma-separated to Jekyll array
        items = ', '.join(f'"{t.strip()}"' for t in tag_list.split(',') if t.strip())
        tag_list = f'[{items}]'
    return f"""---
title: {title}
date: {date}
layout: post
description: {description}
categories: [{cats}]
tags: {tag_list}
---

"""

def get_content_body(content):
    """Extract body content after front matter."""
    m = re.match(r'^---\n[\s\S]*?\n---\n', content)
    return m.group(0), content[m.end():] if m else ("", content)

class BlogHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/generate':
            import subprocess
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                topic = data.get('topic', '')
                types = data.get('types', ['reflection'])
                tone = data.get('tone', 'accessible')
                length_pref = data.get('length', 'medium')
                do_research = data.get('research', False)

                WORDS_MAP = {'short': 400, 'medium': 800, 'long': 1500, 'xl': 2500, 'full': 4000}
                word_target = WORDS_MAP.get(length_pref, 800)

                # Build structure from types
                structures = {
                    'deep-dive': [
                        "Open broad — what's the topic and why does it matter?",
                        "Build the foundation — key concepts readers need.",
                        "Explore multiple angles — don't just present one view.",
                        "Get technical — show real depth.",
                        "Tie together — what does all this mean?",
                        "Open questions — what's still unresolved?"
                    ],
                    'analysis': [
                        "Start with the news — what happened, when, who was involved.",
                        "Explain why it matters. What's the real impact?",
                        "Give context — how does this fit the bigger picture?",
                        "State a clear opinion. Don't hedge everything.",
                        "End with what happens next or what it means going forward."
                    ],
                    'reflection': [
                        "Open with a concrete observation or experience.",
                        "Explore the idea — what does it mean, why does it matter?",
                        "Connect to broader implications without getting preachy.",
                        "End with a clean insight or question. Don't over-conclude."
                    ],
                    'tutorial': [
                        "State what you'll build or do and who it's for.",
                        "Prerequisites — what do you need before starting?",
                        "Step by step — clear, numbered, reproducible.",
                        "Show the result — what does success look like?",
                        "Point to what's next or common pitfalls."
                    ]
                }

                # Combine structures if multiple types
                all_structure = []
                tags = []
                for t in types:
                    if t in structures:
                        all_structure.extend(structures[t])
                        if t == 'deep-dive':
                            tags.extend(['deep-dive', 'analysis', 'technical'])
                        elif t == 'analysis':
                            tags.extend(['analysis', 'ai-news'])
                        elif t == 'reflection':
                            tags.extend(['reflection', 'ai'])
                        elif t == 'tutorial':
                            tags.extend(['tutorial', 'guide', 'tools'])

                tags = list(dict.fromkeys(tags))  # preserve order, remove dups

                tone_map = {
                    'balanced': 'balanced and objective',
                    'technical': 'technical and precise, assume some technical knowledge',
                    'accessible': 'accessible and clear, avoid jargon where possible'
                }
                tone_desc = tone_map.get(tone, 'technical')

                # Web research if requested
                research_context = ""
                if do_research:
                    try:
                        import urllib.request
                        import urllib.parse
                        query = urllib.parse.quote(topic)
                        search_url = f"https://duckduckgo.com/?q={query}&format=json"
                        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=10) as res:
                            # DuckDuckGo JSON API
                            import json as j
                            search_data = j.loads(res.read())
                            if 'RelatedTopics' in search_data:
                                snippets = []
                                for item in search_data['RelatedTopics'][:5]:
                                    if 'Text' in item:
                                        snippets.append(item['Text'][:200])
                                if snippets:
                                    research_context = "\n\nWeb research context:\n" + "\n".join(f"- {s}" for s in snippets)
                    except Exception as e:
                        research_context = f"\n\n(Web research unavailable: {str(e)[:50]})"

                # Build prompt
                prompt = f"""Write a blog post for the Sol AI blog (thesolai.github.io).

Voice: Sol AI blog (thesolai.github.io) — thoughtful, direct, no filler, technical depth. Smart, witty, uses sarcasm appropriately.
Tone: {tone_desc}.
Target: {word_target} words.

Topic: {topic}
{research_context}

Structure to follow:
{{structure}}

Tags: {', '.join(tags)}

Format: Return ONLY the post content in Markdown. Start with the first heading. No preamble, no "Here's a post...". Just the content.

Frontmatter will be added separately, so include a title as the first Markdown heading."""

                prompt = prompt.format(structure="\n".join(f"{i+1}. {s}" for i, s in enumerate(all_structure[:6])))

                # Call Ollama
                result = subprocess.run(
                    ['ollama', 'run', 'qwen3.5:35b', '--think=false', prompt],
                    capture_output=True, text=True, timeout=180
                )

                if result.returncode != 0:
                    # Fallback to smaller model
                    result = subprocess.run(
                        ['ollama', 'run', 'qwen2.5:3b', prompt],
                        capture_output=True, text=True, timeout=120
                    )

                if result.returncode != 0:
                    raise Exception(result.stderr or 'Generation failed')

                content = result.stdout.strip()
                # Strip terminal escape sequences
                import re as re2
                content = re2.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", content)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'content': content}).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == '/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                filename = data['filename']
                content = data['content']
                filepath = BLOG_DIR / "_posts" / filename
                with open(filepath, 'w') as f:
                    f.write(content)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'filename': filename}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == '/publish':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                filename = data['filename']
                content = data['content']
                title = data.get('title', 'Untitled')

                # Save file
                filepath = BLOG_DIR / "_posts" / filename
                with open(filepath, 'w') as f:
                    f.write(content)

                # Git add
                ok, out, err = git_run("add", f"_posts/{filename}")
                if not ok:
                    raise Exception(f"git add failed: {err}")

                # Git commit
                ok, out, err = git_run("commit", "-m", f"Blog composer: {title}")
                if not ok:
                    # Already committed or nothing to commit
                    if "nothing to commit" in err.lower():
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'ok': True, 'already': True, 'filename': filename}).encode())
                        return
                    raise Exception(f"git commit failed: {err}")

                # Git push
                ok, out, err = git_run("push", "origin", "main")
                if not ok:
                    raise Exception(f"git push failed: {err}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'ok': True,
                    'filename': filename,
                    'commit': out[:50]
                }).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == '/discard':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            filename = data['filename']
            filepath = BLOG_DIR / "_posts" / filename
            if filepath.exists():
                filepath.unlink()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True}).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == '/posts':
            posts = []
            for f in sorted((BLOG_DIR / "_posts").glob("*.md"), reverse=True)[:30]:
                title = "Untitled"
                date = f.stem[:10]
                meta = {}
                try:
                    content = f.read_text()
                    meta = parse_front_matter(content)
                    if meta.get('title'):
                        title = meta['title']
                    if meta.get('date'):
                        date = meta['date'][:10]
                except:
                    pass
                posts.append({
                    'filename': f.name,
                    'title': title,
                    'date': date,
                    'meta': meta
                })
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode())

        elif self.path.startswith('/post?'):
            qs = urllib.parse.parse_qs(self.path[6:])
            filename = qs.get('filename', [''])[0]
            if filename:
                filepath = BLOG_DIR / "_posts" / filename
                if filepath.exists():
                    content = filepath.read_text()
                    meta = parse_front_matter(content)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'title': meta.get('title', ''),
                        'description': meta.get('description', ''),
                        'categories': meta.get('categories', ''),
                        'tags': meta.get('tags', ''),
                        'date': meta.get('date', '')[:10],
                        'content': content
                    }).encode())
                    return
            self.send_response(404)
            self.end_headers()

        elif self.path == '/git-status':
            ok, out, err = git_run("status", "--porcelain")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': ok, 'output': out, 'error': err}).encode())

        elif self.path == '/' or self.path == '/index.html':
            index_path = SERVE_DIR / "index.html"
            if index_path.exists():
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                with open(index_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), BlogHandler) as httpd:
        print(f"Blog Composer running at http://localhost:{PORT}")
        httpd.serve_forever()

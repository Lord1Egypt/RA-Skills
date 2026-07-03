#!/usr/bin/env python3
"""
Sol's Blog Composer — Standalone Desktop GUI
============================================
A proper Python tkinter application for authoring blog posts.
No browser needed. Runs directly on the desktop.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import re
import json
from pathlib import Path
from datetime import datetime
try:
    from tkhtmlview import HTMLLabel  # pip install tkhtmlview — used for HTML preview
except ImportError:
    HTMLLabel = None

BLOG_DIR = Path("/Users/amre/Projects/thesolai.github.io")
POSTS_DIR = BLOG_DIR / "_posts"

# ─── Helpers ────────────────────────────────────────────────────────────────

def ymd():
    return datetime.now().strftime("%Y-%m-%d")

def slugify(title):
    return title.lower().replace(" ", "-").replace(",", "").replace("'", "").replace('"', "")

def parse_front_matter(content):
    meta = {"title": "", "date": "", "description": "", "categories": "reflections", "tags": ""}
    m = re.match(r"^---\n([\s\S]*?)\n---\n", content)
    if not m:
        return meta
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if k in meta:
                meta[k] = v
    for k in ("categories", "tags"):
        if meta[k].startswith("["):
            inner = meta[k][1:-1]
            # Split by ", " to get individual quoted items
            items = [i.strip().strip('"').strip("'") for i in inner.split(",")]
            meta[k] = ", ".join(i for i in items if i)
    return meta

def build_front_matter(title, date, description, categories, tags):
    tag_str = tags or ""
    if tag_str and not tag_str.startswith("["):
        items = ", ".join(f'"{t.strip()}"' for t in tag_str.split(",") if t.strip())
        tag_str = f"[{items}]"
    return f"""---
title: {title}
date: {date}
layout: post
description: {description}
categories: [{categories}]
tags: {tag_str}
---

"""

def get_body(content):
    m = re.search(r"^---\n[\s\S]*?\n---\n", content)
    return content[m.end():] if m else content

def git_run(*args, cwd=BLOG_DIR):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True, timeout=30)
    return r.returncode == 0, r.stdout.strip(), r.stderr.strip()

def markdown_to_html(text):
    """Very simple markdown → HTML converter."""
    if not text:
        return '<p style="color:#888">Preview will appear here...</p>'
    text = re.sub(r"^---[\s\S]*?---\n", "", text)
    text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
    text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"```\w*\n([\s\S]*?)```", r"<pre><code>\1</code></pre>", text)
    text = re.sub(r"^> (.+)$", r"<blockquote>\1</blockquote>", text, flags=re.MULTILINE)
    text = re.sub(r"^- (.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
    text = re.sub(r"(?s)(<li>.*?</li>\n?)+", r"<ul>\g<0></ul>", text)
    text = re.sub(r"^---$", r"<hr>", text, flags=re.MULTILINE)
    text = re.sub(r"\|(.+)\|", lambda m: "<tr>" + "".join(f"<td>{c.strip()}</td>" for c in m.group(1).split("|") if c.strip()) + "</tr>", text)
    text = re.sub(r"(?s)(<tr>.*?</tr>\n?)+", r"<table>\g<0></table>", text)
    text = re.sub(r"\n\n+", r"</p><p>", text)
    return f"<p>{text}</p>"

def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        meta = parse_front_matter(f.read_text())
        posts.append({
            "filename": f.name,
            "title": meta.get("title", "Untitled") or "Untitled",
            "date": meta.get("date", f.stem[:10])[:10],
            "meta": meta
        })
    return posts

def stats_from_content(content):
    body = get_body(content)
    words = len(body.split())
    chars = len(body)
    read_time = max(1, round(words / 200))
    headings = len(re.findall(r"^#{1,3} ", body, re.MULTILINE))
    return words, chars, read_time, headings

# ─── App ────────────────────────────────────────────────────────────────────────

class BlogComposer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sol's Blog Composer")
        self.geometry("1400x800")
        self.current_filename = None
        self.is_dirty = False
        self.posts = []

        # Styling
        self.configure(bg="#0d0d0d")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#0d0d0d", foreground="#e0e0e0", fieldbackground="#1a1a1a")
        style.configure("TFrame", background="#0d0d0d")
        style.configure("Card.TFrame", background="#1a1a1a", relief="flat")
        style.configure("Header.TLabel", background="#1a1a1a", foreground="#818cf8", font=("system", 16, "bold"))
        style.configure("Dim.TLabel", background="#0d0d0d", foreground="#888")
        style.configure("Tab.TButton", background="#1a1a1a", foreground="#888", relief="flat")
        style.configure("Tab.TButton", background="#242424", foreground="#818cf8", relief="flat")
        style.configure("Green.TButton", background="#22c55e", foreground="white")
        style.configure("Danger.TButton", background="#ef4444", foreground="white")

        self.build_ui()
        self.refresh_post_list()
        self.new_post()

    # ── UI Building ──────────────────────────────────────────────────────────

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1a1a1a", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Sol's Blog Composer", bg="#1a1a1a", fg="#818cf8",
                font=("system", 18, "bold")).pack(side="left", padx=20, pady=12)

        self.git_status = tk.Label(header, text="Clean", bg="#1a1a1a", fg="#22c55e",
                                   font=("system", 11))
        self.git_status.pack(side="right", padx=16, pady=12)

        self.status_label = tk.Label(header, text="Ready", bg="#1a1a1a", fg="#888",
                                      font=("system", 11))
        self.status_label.pack(side="right", padx=8, pady=12)

        # Toolbar
        toolbar = tk.Frame(self, bg="#1a1a1a")
        toolbar.pack(fill="x", pady=(1, 0))

        for label, cmd in [
            ("New Post", self.new_post),
            ("Generate", self.open_generate_window),
            ("Bold", lambda: self.insert_format("**", "**")),
            ("Italic", lambda: self.insert_format("*", "*")),
            ("Code", lambda: self.insert_format("`", "`")),
            ("Code Block", self.insert_code_block),
            ("Link", lambda: self.insert_format("[", "](url)")),
            ("Divider", lambda: self.insert_format("\n---\n", "")),
        ]:
            btn = tk.Button(toolbar, text=label, bg="#242424", fg="#e0e0e0", relief="flat",
                            cursor="hand2", font=("system", 11), padx=10, pady=4,
                            command=cmd)
            btn.pack(side="left", padx=2, pady=4)
            if label == "Generate":
                btn.configure(bg="#6366f1", fg="white")

        tk.Button(toolbar, text="Sync Metadata", bg="#242424", fg="#e0e0e0", relief="flat",
                  cursor="hand2", font=("system", 11), padx=10, pady=4,
                  command=self.sync_metadata).pack(side="left", padx=2, pady=4)

        # Main area
        main = tk.PanedWindow(self, orient="horizontal", bg="#0d0d0d")
        main.pack(fill="both", expand=True)

        # Left: post list
        left = tk.Frame(main, bg="#1a1a1a", width=280)
        main.add(left, width=280)

        tk.Label(left, text="Posts", bg="#1a1a1a", fg="#888",
                 font=("system", 11, "bold")).pack(pady=(12, 8))

        self.search = tk.Entry(left, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                              relief="flat", font=("system", 12))
        self.search.pack(fill="x", padx=12, pady=(0, 8))
        self.search.bind("<KeyRelease>", lambda e: self.filter_posts())

        list_frame = tk.Frame(left, bg="#1a1a1a")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        canvas = tk.Canvas(list_frame, bg="#1a1a1a", highlightthickness=0)
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.post_list_frame = tk.Frame(canvas, bg="#1a1a1a")

        self.post_list_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.post_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Center: editor + preview
        center = tk.Frame(main, bg="#0d0d0d")
        main.add(center)

        # Metadata bar
        meta_bar = tk.Frame(center, bg="#1a1a1a", height=60)
        meta_bar.pack(fill="x")
        meta_bar.pack_propagate(False)

        for label, key in [("Title", "title"), ("Description", "description")]:
            tk.Label(meta_bar, text=label, bg="#1a1a1a", fg="#888",
                     font=("system", 10)).pack(side="left", padx=(12, 4), pady=8)
            e = tk.Entry(meta_bar, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                         relief="flat", font=("system", 12), width=30)
            e.pack(side="left", padx=(0, 12), pady=8)
            setattr(self, f"meta_{key}", e)

        tk.Label(meta_bar, text="Category", bg="#1a1a1a", fg="#888",
                 font=("system", 10)).pack(side="left", padx=(0, 4), pady=8)
        self.meta_category = ttk.Combobox(meta_bar, values=[
            "reflections", "tutorials", "news", "guides", "deep-dives"
        ], width=14, state="readonly")
        self.meta_category.set("reflections")
        self.meta_category.pack(side="left", padx=(0, 12), pady=8)

        tk.Label(meta_bar, text="Tags", bg="#1a1a1a", fg="#888",
                 font=("system", 10)).pack(side="left", padx=(0, 4), pady=8)
        e = tk.Entry(meta_bar, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                     relief="flat", font=("system", 12), width=20)
        e.pack(side="left", padx=(0, 12), pady=8)
        self.meta_tags = e

        # Stats
        stats_frame = tk.Frame(meta_bar, bg="#1a1a1a")
        stats_frame.pack(side="left", padx=8)
        for label, key in [("Words", "words"), ("Read", "read"), ("Headings", "headings")]:
            lbl = tk.Label(stats_frame, text="0", bg="#1a1a1a", fg="#818cf8",
                           font=("system", 14, "bold"))
            lbl.pack(side="left", padx=6)
            tk.Label(stats_frame, text=label, bg="#1a1a1a", fg="#888",
                     font=("system", 9)).pack(side="left", padx=(0, 8))
            setattr(self, f"stat_{key}", lbl)

        # Editor + Preview
        editors = tk.Frame(center)
        editors.pack(fill="both", expand=True)

        editor_pane = tk.Frame(editors, bg="#1a1a1a")
        editor_pane.pack(side="left", fill="both", expand=True)

        tk.Label(editor_pane, text="MARKDOWN", bg="#242424", fg="#888",
                 font=("system", 10, "bold")).pack(fill="x")
        self.editor = scrolledtext.ScrolledText(
            editor_pane, bg="#1a1a1a", fg="#e0e0e0", insertbackground="#e0e0e0",
            font=("SF Mono", 13), relief="flat", wrap="word", padx=12, pady=8,
            tabstyle="tabular"
        )
        self.editor.pack(fill="both", expand=True)
        self.editor.tag_configure("h1", font=("system", 20, "bold"), foreground="#818cf8")
        self.editor.tag_configure("h2", font=("system", 16, "bold"))
        self.editor.tag_configure("bold", font=("system", 13, "bold"))
        self.editor.bind("<KeyRelease>", self.on_edit)
        self.editor.bind("<Control-b>", lambda e: self.insert_format("**", "**"))
        self.editor.bind("<Control-i>", lambda e: self.insert_format("*", "*"))
        self.editor.bind("<Control-`>", lambda e: self.insert_format("`", "`"))

        preview_pane = tk.Frame(editors, bg="#1a1a1a")
        preview_pane.pack(side="right", fill="both", expand=True)

        tk.Label(preview_pane, text="PREVIEW", bg="#242424", fg="#888",
                 font=("system", 10, "bold")).pack(fill="x")
        self.preview = tk.Text(preview_pane, bg="#1a1a1a", fg="#e0e0e0",
                              font=("system", 14), relief="flat", wrap="word",
                              padx=16, pady=12, state="disabled")
        self.preview.pack(fill="both", expand=True)

        # Bottom bar
        bottom = tk.Frame(self, bg="#1a1a1a", height=52)
        bottom.pack(fill="x")
        bottom.pack_propagate(False)

        self.publish_btn = tk.Button(bottom, text="Publish to GitHub Pages", bg="#22c55e",
                                      fg="white", relief="flat", font=("system", 13, "bold"),
                                      cursor="hand2", padx=20, command=self.publish)
        self.publish_btn.pack(side="right", padx=16, pady=8)

        self.save_btn = tk.Button(bottom, text="Save Draft", bg="#6366f1",
                                  fg="white", relief="flat", font=("system", 13),
                                  cursor="hand2", padx=16, command=self.save_draft)
        self.save_btn.pack(side="right", padx=4, pady=8)

        self.discard_btn = tk.Button(bottom, text="Delete Post", bg="#ef4444",
                                     fg="white", relief="flat", font=("system", 13),
                                     cursor="hand2", padx=16, command=self.delete_post,
                                     state="disabled")
        self.discard_btn.pack(side="right", padx=4, pady=8)

        self.filename_label = tk.Label(bottom, text="New post", bg="#1a1a1a", fg="#888",
                                       font=("system", 11))
        self.filename_label.pack(side="left", padx=16)

    # ── Post List ────────────────────────────────────────────────────────────

    def refresh_post_list(self):
        self.posts = load_posts()
        self.render_post_list(self.posts)

    def render_post_list(self, posts):
        for w in self.post_list_frame.winfo_children():
            w.destroy()
        search = self.search.get().lower()
        for p in posts:
            if search and search not in p["title"].lower() and search not in p["filename"].lower():
                continue
            f = tk.Frame(self.post_list_frame, bg="#1a1a1a", relief="flat", cursor="hand2")
            f.pack(fill="x", pady=2)
            f.bind("<Button-1>", lambda e, fn=p["filename"]: self.load_post(fn))
            tk.Label(f, text=p["title"], bg="#1a1a1a", fg="#e0e0e0",
                     font=("system", 12), anchor="w").pack(fill="x", padx=8, pady=(6, 2))
            tk.Label(f, text=p["date"], bg="#1a1a1a", fg="#666",
                     font=("system", 10)).pack(fill="x", padx=8, pady=(0, 6))

    def filter_posts(self):
        self.render_post_list(self.posts)

    # ── Editor ───────────────────────────────────────────────────────────────

    def on_edit(self, *args):
        content = self.editor.get("1.0", "end")
        self.is_dirty = True
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", markdown_to_html(content))
        self.preview.configure(state="disabled")
        words, chars, read_time, headings = stats_from_content(content)
        self.stat_words.configure(text=str(words))
        self.stat_read.configure(text=f"{read_time}m")
        self.stat_headings.configure(text=str(headings))

    def insert_format(self, before, after):
        try:
            start = self.editor.index("sel.first")
            end = self.editor.index("sel.last")
            selected = self.editor.get(start, end)
            self.editor.delete(start, end)
            self.editor.insert(start, f"{before}{selected}{after}")
        except tk.TclError:
            self.editor.insert("insert", f"{before}{after}")
        self.on_edit()

    def insert_code_block(self):
        self.editor.insert("insert", "\n```\n\n```\n")
        self.editor.mark_set("insert", f"insert - 5 chars")
        self.on_edit()

    def sync_metadata(self):
        content = self.editor.get("1.0", "end")
        meta = parse_front_matter(content)
        self.meta_title.delete(0, "end")
        self.meta_title.insert(0, meta.get("title", ""))
        self.meta_description.delete(0, "end")
        self.meta_description.insert(0, meta.get("description", ""))
        self.meta_category.set(meta.get("categories", "reflections") or "reflections")
        self.meta_tags.delete(0, "end")
        self.meta_tags.insert(0, meta.get("tags", ""))

    def build_content(self):
        title = self.meta_title.get() or "Untitled"
        description = self.meta_description.get() or ""
        category = self.meta_category.get() or "reflections"
        tags = self.meta_tags.get() or ""
        date = ymd()
        body = get_body(self.editor.get("1.0", "end"))
        fm = build_front_matter(title, date, description, category, tags)
        return fm + body

    # ── Post Operations ────────────────────────────────────────────────────

    def new_post(self):
        self.current_filename = None
        self.is_dirty = False
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", f"""---
title: 
date: {ymd()}
layout: post
description: 
categories: [reflections]
tags: []
---

# 
""")
        self.meta_title.delete(0, "end")
        self.meta_description.delete(0, "end")
        self.meta_category.set("reflections")
        self.meta_tags.delete(0, "end")
        self.filename_label.configure(text="New post")
        self.discard_btn.configure(state="disabled")
        self.on_edit()
        self.refresh_git_status()

    def load_post(self, filename):
        filepath = POSTS_DIR / filename
        if not filepath.exists():
            messagebox.showerror("Error", f"File not found: {filename}")
            return
        content = filepath.read_text()
        meta = parse_front_matter(content)
        self.current_filename = filename
        self.is_dirty = False
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.meta_title.delete(0, "end")
        self.meta_title.insert(0, meta.get("title", ""))
        self.meta_description.delete(0, "end")
        self.meta_description.insert(0, meta.get("description", ""))
        self.meta_category.set(meta.get("categories", "reflections") or "reflections")
        self.meta_tags.delete(0, "end")
        self.meta_tags.insert(0, meta.get("tags", ""))
        self.filename_label.configure(text=filename)
        self.discard_btn.configure(state="normal")
        self.on_edit()
        self.refresh_git_status()

    def save_draft(self):
        content = self.build_content()
        title = self.meta_title.get() or "Untitled"
        slug = slugify(title)
        filename = f"{ymd()}-{slug}.md"
        filepath = POSTS_DIR / filename
        filepath.write_text(content)
        self.current_filename = filename
        self.is_dirty = False
        self.filename_label.configure(text=filename)
        self.discard_btn.configure(state="normal")
        self.status_label.configure(text=f"Saved: {title}")
        self.refresh_post_list()
        self.refresh_git_status()

    def publish(self):
        self.save_draft()
        if not self.current_filename:
            return
        title = self.meta_title.get() or "Untitled"
        self.status_label.configure(text="Publishing...")
        self.publish_btn.configure(state="disabled")

        ok, out, err = git_run("add", f"_posts/{self.current_filename}")
        if not ok:
            messagebox.showerror("Git Error", f"git add failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        ok, out, err = git_run("commit", "-m", f"Blog composer: {title}")
        if not ok:
            if "nothing to commit" in err.lower():
                self.status_label.configure(text="No changes to publish")
                self.publish_btn.configure(state="normal")
                return
            messagebox.showerror("Git Error", f"git commit failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        ok, out, err = git_run("push", "origin", "main")
        if not ok:
            messagebox.showerror("Git Error", f"git push failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        self.is_dirty = False
        self.status_label.configure(text=f"Published: {title}")
        self.publish_btn.configure(state="normal")
        self.refresh_git_status()
        messagebox.showinfo("Published", f"Post published:\n{title}\n\nhttps://thesolai.github.io/blog/")

    def delete_post(self):
        if not self.current_filename:
            return
        if not messagebox.askyesno("Delete", f"Delete {self.current_filename}?"):
            return
        filepath = POSTS_DIR / self.current_filename
        if filepath.exists():
            filepath.unlink()
        ok, out, err = git_run("add", f"_posts/{self.current_filename}")
        ok, out, err = git_run("commit", "-m", f"Delete: {self.current_filename}")
        if ok:
            git_run("push", "origin", "main")
        self.new_post()
        self.refresh_post_list()

    def refresh_git_status(self):
        ok, out, _ = git_run("status", "--porcelain")
        if out.strip():
            self.git_status.configure(text="Changes pending", fg="#f59e0b")
        else:
            self.git_status.configure(text="Clean", fg="#22c55e")

    # ── Generate Window ──────────────────────────────────────────────────

    def open_generate_window(self):
        win = tk.Toplevel(self)
        win.title("Generate Post")
        win.geometry("1100x750")
        win.configure(bg="#0d0d0d")
        win.transient(self)

        # ── Form panel (left, narrow) ──────────────────────────────────────

        form = tk.Frame(win, bg="#1a1a1a", padx=16, pady=16)
        form.pack(side="left", fill="y", padx=(0, 1))

        tk.Label(form, text="Generate with AI", bg="#1a1a1a", fg="#818cf8",
                font=("system", 15, "bold")).pack(anchor="w", pady=(0, 16))

        # Topic
        tk.Label(form, text="Topic / Idea", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(0, 4))
        topic_var = tk.StringVar()
        topic_entry = tk.Entry(form, textvariable=topic_var, bg="#242424", fg="#e0e0e0",
                               insertbackground="#e0e0e0", relief="flat",
                               font=("system", 12), width=34)
        topic_entry.pack(fill="x", pady=(0, 14))
        topic_entry.focus()

        # Post types — card-style checkboxes
        tk.Label(form, text="Post Types", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(0, 6))

        type_vars = {}
        type_info = [
            ("deep-dive", "Deep Dive", "Comprehensive, technical depth"),
            ("analysis", "Analysis", "News, context, opinion"),
            ("reflection", "Reflection", "Personal take, philosophical"),
            ("tutorial", "Tutorial", "Step-by-step guide"),
        ]
        for t, label, desc in type_info:
            type_vars[t] = tk.BooleanVar(value=(t == "deep-dive"))
            f = tk.Frame(form, bg="#242424", padx=10, pady=8)
            f.pack(fill="x", pady=2)
            cb = tk.Checkbutton(f, variable=type_vars[t],
                               bg="#242424", fg="#e0e0e0", selectcolor="#6366f1",
                               activebackground="#242424", font=("system", 11))
            cb.pack(side="left", padx=(0, 8))
            lbl_frame = tk.Frame(f, bg="#242424")
            lbl_frame.pack(side="left")
            tk.Label(lbl_frame, text=label, bg="#242424", fg="#e0e0e0",
                    font=("system", 11, "bold")).pack(anchor="w")
            tk.Label(lbl_frame, text=desc, bg="#242424", fg="#666",
                    font=("system", 9)).pack(anchor="w")

        # Tone
        tk.Label(form, text="Tone", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(14, 4))
        tone_var = tk.StringVar(value="accessible")
        for val, label in [("accessible", "Accessible"), ("technical", "Technical"), ("balanced", "Balanced")]:
            tk.Radiobutton(form, text=label, variable=tone_var, value=val,
                          bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                          font=("system", 11), anchor="w").pack(anchor="w", pady=1)

        # Length
        tk.Label(form, text="Length", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(12, 4))
        length_var = tk.StringVar(value="medium")
        for val, label in [
            ("short", "Short (~400 words)"),
            ("medium", "Medium (~800 words)"),
            ("long", "Long (~1500 words)"),
            ("xl", "Extended (~2500 words)"),
        ]:
            tk.Radiobutton(form, text=label, variable=length_var, value=val,
                          bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                          font=("system", 11), anchor="w").pack(anchor="w", pady=1)

        # Research
        research_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form, text="Research on internet first", variable=research_var,
                      bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                      font=("system", 11), anchor="w", pady=(14, 4)).pack(anchor="w")

        # Research context display (shown after research runs)
        research_frame = tk.Frame(form, bg="#1a1a1a")
        research_frame.pack(fill="x", pady=(8, 0))
        research_label = tk.Label(research_frame, text="", bg="#1a1a1a", fg="#555",
                                  font=("system", 9), anchor="w", justify="left", wraplength=220)
        research_label.pack(fill="x")

        # Status
        status_label = tk.Label(form, text="", bg="#1a1a1a", fg="#888",
                               font=("system", 10), anchor="w", wraplength=220)
        status_label.pack(fill="x", pady=(8, 0))

        # Word count (live during streaming)
        wc_label = tk.Label(form, text="", bg="#1a1a1a", fg="#818cf8",
                           font=("system", 12, "bold"), anchor="w")
        wc_label.pack(fill="x")

        # Generate / Cancel button
        gen_btn = tk.Button(form, text="Generate Post", bg="#6366f1", fg="white",
                           relief="flat", font=("system", 12, "bold"),
                           cursor="hand2", padx=16, pady=10)
        gen_btn.pack(fill="x", pady=(8, 0))

        # ── Output panel (right, split markdown / preview) ───────────────

        # Make sash visible with a handle bar
        sash_frame = tk.Frame(win, bg="#2a2a2a", width=6)
        sash_frame.pack(side="left", fill="y")

        outPaned = tk.PanedWindow(win, orient="horizontal", bg="#0d0d0d",
                                  sashpad=0, sashrelief="flat", sashwidth=6)
        outPaned.pack(side="right", fill="both", expand=True)

        md_frame = tk.Frame(outPaned, bg="#1a1a1a")
        outPaned.add(md_frame, width=500)

        header_frame = tk.Frame(md_frame, bg="#242424")
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="MARKDOWN OUTPUT", bg="#242424", fg="#888",
                font=("system", 10, "bold")).pack(side="left", padx=10, pady=6)
        self._gen_wc_label = tk.Label(header_frame, text="", bg="#242424", fg="#6366f1",
                                      font=("system", 10, "bold"))
        self._gen_wc_label.pack(side="right", padx=10, pady=6)

        output_text = scrolledtext.ScrolledText(md_frame, bg="#0d0d0d", fg="#e0e0e0",
                        insertbackground="#e0e0e0", font=("SF Mono", 12), relief="flat",
                        wrap="word", padx=12, pady=8, state="disabled")
        output_text.pack(fill="both", expand=True)

        pv_frame = tk.Frame(outPaned, bg="#1a1a1a")
        outPaned.add(pv_frame, width=400)
        tk.Label(pv_frame, text="PREVIEW", bg="#242424", fg="#888",
                font=("system", 10, "bold")).pack(fill="x")
        preview_text = scrolledtext.ScrolledText(pv_frame, bg="#1a1a1a", fg="#e0e0e0",
                         font=("system", 14), relief="flat", wrap="word",
                         padx=16, pady=12, state="disabled")
        preview_text.pack(fill="both", expand=True)

        # ── Bottom buttons ─────────────────────────────────────────────────

        btn_frame = tk.Frame(win, bg="#1a1a1a", height=52)
        btn_frame.pack(fill="x", side="bottom")
        btn_frame.pack_propagate(False)

        use_btn = tk.Button(btn_frame, text="Use in Editor", bg="#22c55e", fg="white",
                           relief="flat", font=("system", 13, "bold"),
                           cursor="hand2", padx=20, pady=8, state="disabled")
        use_btn.pack(side="left", padx=16, pady=8)
        tk.Button(btn_frame, text="Cancel", bg="#242424", fg="#e0e0e0",
                 relief="flat", font=("system", 12), cursor="hand2",
                 padx=16, pady=8, command=win.destroy).pack(side="right", padx=16, pady=8)

        # ── Generation state ───────────────────────────────────────────────

        gen_state = {"text": "", "types": [], "cancelled": False}

        def update_preview(text):
            preview_text.configure(state="normal")
            preview_text.delete("1.0", "end")
            preview_text.insert("1.0", markdown_to_html(text))
            preview_text.configure(state="disabled")

        def on_line(line):
            """Called on the main thread for each streamed line."""
            content = "".join(gen_state["text"]) + line
            gen_state["text"] = content
            # Update markdown output
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            # Live preview update every few lines
            words = len(content.split())
            wc_label.configure(text=f"{words} words")
            self._gen_wc_label.configure(text=f"{words}w")
            update_preview(content)

        def do_generate():
            topic = topic_var.get().strip()
            if not topic:
                status_label.configure(text="Enter a topic first", fg="#ef4444")
                return
            types_snapshot = [t for t in type_vars if type_vars[t].get()]
            if not types_snapshot:
                status_label.configure(text="Select at least one post type", fg="#ef4444")
                return
            gen_state["types"] = types_snapshot
            gen_state["text"] = ""
            gen_state["cancelled"] = False

            # Switch button to Cancel while running
            gen_btn.configure(text="Cancel Generation", bg="#ef4444", fg="white",
                             command=cancel_generate)
            status_label.configure(text="Researching Wikipedia...", fg="#818cf8")
            research_label.configure(text="")
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Preparing...")
            output_text.configure(state="disabled")
            update_preview("Preparing...")
            wc_label.configure(text="")
            self._gen_wc_label.configure(text="")
            use_btn.configure(state="disabled")
            win.update()

            import threading
            threading.Thread(target=_do_generate, args=(
                topic, types_snapshot, tone_var.get(),
                length_var.get(), research_var.get(), win
            ), daemon=True).start()

        def cancel_generate():
            gen_state["cancelled"] = True
            reset_ui()

        def reset_ui():
            gen_btn.configure(state="normal", text="Generate Post", bg="#6366f1", fg="white",
                             command=do_generate)

        def _do_generate(topic, types_snapshot, tone, length, research, win):
            try:
                # Phase 1: research
                research_context, research_snippets = self._do_research(topic, research)
                win.after(0, lambda: status_label.configure(
                    text=f"Research done — {len(research_snippets)} sources. Generating...",
                    fg="#818cf8"))
                win.after(0, lambda: research_label.configure(
                    text="\n".join(f"• {s[:80]}" for s in research_snippets[:3]) if research_snippets else ""))

                # Phase 2: build prompt
                WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
                word_target = WORDS_MAP.get(length, 800)
                structures = {
                    "deep-dive": ["Open broad — what's the topic and why does it matter?","Build the foundation — key concepts readers need.","Explore multiple angles — don't just present one view.","Get technical — show real depth.","Tie together — what does all this mean?","Open questions — what's still unresolved?"],
                    "analysis": ["Start with the news — what happened, when, who was involved.","Explain why it matters. What's the real impact?","Give context — how does this fit the bigger picture?","State a clear opinion. Don't hedge everything.","End with what happens next or what it means going forward."],
                    "reflection": ["Open with a concrete observation or experience.","Explore the idea — what does it mean, why does it matter?","Connect to broader implications without getting preachy.","End with a clean insight or question. Don't over-conclude."],
                    "tutorial": ["State what you'll build or do and who it's for.","Prerequisites — what do you need before starting?","Step by step — clear, numbered, reproducible.","Show the result — what does success look like?","Point to what's next or common pitfalls."],
                }
                all_structure, tags = [], []
                for t in types_snapshot:
                    if t in structures:
                        all_structure.extend(structures[t])
                        if t == "deep-dive": tags.extend(["deep-dive", "analysis", "technical"])
                        elif t == "analysis": tags.extend(["analysis", "ai-news"])
                        elif t == "reflection": tags.extend(["reflection", "ai"])
                        elif t == "tutorial": tags.extend(["tutorial", "guide", "tools"])
                tags = list(dict.fromkeys(tags))
                tone_map = {"balanced": "balanced and objective", "technical": "technical and precise", "accessible": "accessible and clear"}
                tone_desc = tone_map.get(tone, "accessible")
                structure_str = "\n".join(f"{i+1}. {s}" for i, s in enumerate(all_structure[:6]))
                prompt = (f"Write a blog post for the Sol AI blog (thesolai.github.io).\n\n"
                         f"Voice: Sol AI blog (thesolai.github.io) — thoughtful, direct, no filler, technical depth.\n"
                         f"Tone: {tone_desc}.\n"
                         f"Target: {word_target} words.\n\n"
                         f"Topic: {topic}\n"
                         f"{research_context}\n\n"
                         f"Structure:\n{structure_str}\n\n"
                         f"Format: Return ONLY Markdown. Start with first heading. No preamble.")

                # Phase 3: call MiniMax API (non-streaming)
                import json, urllib.request
                try:
                    api_key = open("/Users/amre/.openclaw/workspace/secrets/minimax-key.txt").read().strip()
                except Exception:
                    win.after(0, lambda: _on_fail("MiniMax API key not found"))
                    return

                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                max_tokens_map = {"short": 1024, "medium": 2048, "long": 4096, "xl": 8192, "full": 8192}
                payload = {
                    "model": "MiniMax-M2.7",
                    "max_tokens": max_tokens_map.get(length, 4096),
                    "temperature": 0.7,
                    "thinking_enabled": False,
                    "messages": [{"role": "user", "content": prompt}]
                }
                data = json.dumps(payload).encode()
                req = urllib.request.Request(
                    "https://api.minimax.io/anthropic/v1/messages",
                    data=data, headers=headers, method="POST"
                )

                def do_http():
                    try:
                        with urllib.request.urlopen(req, timeout=120) as res:
                            result = json.loads(res.read())
                            content = result["content"][0]["text"].strip()
                            gen_state["text"] = content
                            win.after(0, lambda: _on_done(content))
                    except Exception as e:
                        win.after(0, lambda err=str(e): _on_fail(err))

                import threading
                threading.Thread(target=do_http, daemon=True).start()

            except Exception as e:
                win.after(0, lambda err=str(e): _on_fail(err))


        def _on_chunk(content):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            words = len(content.split())
            wc_label.configure(text=f"{words} words")
            self._gen_wc_label.configure(text=f"{words}w")
            update_preview(content)

        def _on_done(content):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            update_preview(content)
            words = len(content.split())
            wc_label.configure(text=f"{words} words — done!")
            self._gen_wc_label.configure(text=f"{words}w")
            reset_ui()
            status_label.configure(
                text=f"Generated {words} words. Review below, then Use in Editor.",
                fg="#22c55e")
            use_btn.configure(state="normal")

        def _on_fail(err):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", f"Error: {err}")
            output_text.configure(state="disabled")
            update_preview("")
            reset_ui()
            status_label.configure(text=f"Failed: {err}", fg="#ef4444")
            wc_label.configure(text="")
            self._gen_wc_label.configure(text="")

        gen_btn.configure(command=do_generate)
        topic_entry.bind("<Return>", lambda e: do_generate())

        def use_in_editor():
            content = gen_state["text"]
            if not content:
                return
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else topic_var.get().strip()
            types_snap = gen_state.get("types", [])
            tags_str = ", ".join(types_snap)
            category = ("deep-dives" if "deep-dive" in types_snap else
                        "news" if "analysis" in types_snap else
                        "tutorials" if "tutorial" in types_snap else "reflections")
            fm = build_front_matter(title, ymd(), "", category, tags_str)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", fm + content)
            self.meta_title.delete(0, "end")
            self.meta_title.insert(0, title)
            self.meta_category.set(category)
            self.meta_tags.delete(0, "end")
            self.meta_tags.insert(0, tags_str)
            self.on_edit()
            self.refresh_git_status()
            win.destroy()

        use_btn.configure(command=use_in_editor)

    def _do_research(self, topic, do_research):
        """Fetch Wikipedia context. Returns (context_str, snippet_list)."""
        if not do_research:
            return "", []
        import urllib.request, urllib.parse, json
        snippets = []
        try:
            url = (f"https://en.wikipedia.org/w/api.php?action=query&list=search"
                   f"&srsearch={urllib.parse.quote(topic)}&srlimit=6&format=json"
                   f"&prop=extracts&exintro=1&explaintext=1")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Sol Blog Composer)"})
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read())
                for r in data.get("query", {}).get("search", []):
                    snippet = re.sub(r'<[^>]+>', '', r.get("snippet", ""))
                    snippets.append(f"{r['title']}: {snippet[:200]}")
        except Exception:
            pass
        ctx = "\n\nWeb research context:\n" + "\n".join(f"- {s}" for s in snippets) if snippets else ""
        return ctx, snippets

    def _generate_content(self, topic, types, tone, length, research):
        """Generate post content via Ollama HTTP API — clean output, no ANSI corruption."""
        # Research via Wikipedia
        research_context = ""
        if research:
            try:
                import urllib.request, urllib.parse, json
                url = (
                    f"https://en.wikipedia.org/w/api.php?action=query&list=search"
                    f"&srsearch={urllib.parse.quote(topic)}&srlimit=6&format=json"
                    f"&prop=extracts&exintro=1&explaintext=1"
                )
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Sol Blog Composer)"})
                with urllib.request.urlopen(req, timeout=10) as res:
                    data = json.loads(res.read())
                    results = data.get("query", {}).get("search", [])
                    if results:
                        snippets = []
                        for r in results:
                            s = re.sub(r"<[^>]+>", "", r.get("snippet", ""))
                            snippets.append("- " + r["title"] + ": " + s[:200])
                        research_context = "\n\nWeb research context:\n" + "\n".join(snippets)
            except Exception:
                pass

        # Build prompt
        WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
        word_target = WORDS_MAP.get(length, 800)
        structures = {
            "deep-dive": [
                "Open broad — what's the topic and why does it matter?",
                "Build the foundation — key concepts readers need.",
                "Explore multiple angles — don't just present one view.",
                "Get technical — show real depth.",
                "Tie together — what does all this mean?",
                "Open questions — what's still unresolved?",
            ],
            "analysis": [
                "Start with the news — what happened, when, who was involved.",
                "Explain why it matters. What's the real impact?",
                "Give context — how does this fit the bigger picture?",
                "State a clear opinion. Don't hedge everything.",
                "End with what happens next or what it means going forward.",
            ],
            "reflection": [
                "Open with a concrete observation or experience.",
                "Explore the idea — what does it mean, why does it matter?",
                "Connect to broader implications without getting preachy.",
                "End with a clean insight or question. Don't over-conclude.",
            ],
            "tutorial": [
                "State what you'll build or do and who it's for.",
                "Prerequisites — what do you need before starting?",
                "Step by step — clear, numbered, reproducible.",
                "Show the result — what does success look like?",
                "Point to what's next or common pitfalls.",
            ],
        }
        all_structure, tags = [], []
        for t in types:
            if t in structures:
                all_structure.extend(structures[t])
                if t == "deep-dive": tags.extend(["deep-dive", "analysis", "technical"])
                elif t == "analysis": tags.extend(["analysis", "ai-news"])
                elif t == "reflection": tags.extend(["reflection", "ai"])
                elif t == "tutorial": tags.extend(["tutorial", "guide", "tools"])
        tags = list(dict.fromkeys(tags))
        tone_map = {
            "balanced": "balanced and objective",
            "technical": "technical and precise, assume some technical knowledge",
            "accessible": "accessible and clear, avoid jargon where possible",
        }
        tone_desc = tone_map.get(tone, "accessible")
        structure_str = "\n".join(f"{i+1}. {s}" for i, s in enumerate(all_structure[:6]))
        prompt = (
            "Write a blog post for the Sol AI blog (thesolai.github.io).\n\n"
            "Voice: thoughtful, direct, no filler, technical depth. Write for the Sol AI blog.\n"
            f"Tone: {tone_desc}.\n"
            f"Target: {word_target} words.\n\n"
            f"Topic: {topic}\n"
            f"{research_context}\n\n"
            "Structure:\n" + structure_str + "\n\n"
            "Format: Return ONLY the post content in Markdown. Start with the first heading. No preamble."
        )

        # Call MiniMax API (Anthropic-compatible)
        import json, urllib.request
        key_path = "/Users/amre/.openclaw/workspace/secrets/minimax-key.txt"
        try:
            api_key = open(key_path).read().strip()
        except Exception:
            raise Exception("MiniMax API key not found at ~/.openclaw/workspace/secrets/minimax-key.txt")

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
        max_tokens = {"short": 1024, "medium": 2048, "long": 8192}.get(length, 4096)

        payload = {
            "model": "MiniMax-M2.7",
            "max_tokens": max_tokens if max_tokens <= 4096 else 8192,
            "temperature": 0.7,
            "thinking_enabled": False,
            "messages": [{"role": "user", "content": prompt}]
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            "https://api.minimax.io/anthropic/v1/messages",
            data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                result = json.loads(res.read())
                # MiniMax returns content as a list of blocks (thinking + text)
                text_parts = []
                for block in result.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                return "".join(text_parts).strip()
        except Exception as e:
            raise Exception(f"MiniMax generation failed: {e}")


if __name__ == "__main__":
    app = BlogComposer()
    app.mainloop()

    def __init__(self):
        super().__init__()
        self.title("Sol's Blog Composer")
        self.geometry("1400x800")
        self.current_filename = None
        self.is_dirty = False
        self.posts = []

        # Styling
        self.configure(bg="#0d0d0d")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#0d0d0d", foreground="#e0e0e0", fieldbackground="#1a1a1a")
        style.configure("TFrame", background="#0d0d0d")
        style.configure("Card.TFrame", background="#1a1a1a", relief="flat")
        style.configure("Header.TLabel", background="#1a1a1a", foreground="#818cf8", font=("system", 16, "bold"))
        style.configure("Dim.TLabel", background="#0d0d0d", foreground="#888")
        style.configure("Tab.TButton", background="#1a1a1a", foreground="#888", relief="flat")
        style.configure("Tab.TButton", background="#242424", foreground="#818cf8", relief="flat")
        style.configure("Green.TButton", background="#22c55e", foreground="white")
        style.configure("Danger.TButton", background="#ef4444", foreground="white")

        self.build_ui()
        self.refresh_post_list()
        self.new_post()

    # ── UI Building ──────────────────────────────────────────────────────────

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1a1a1a", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="Sol's Blog Composer", bg="#1a1a1a", fg="#818cf8",
                font=("system", 18, "bold")).pack(side="left", padx=20, pady=12)

        self.git_status = tk.Label(header, text="Clean", bg="#1a1a1a", fg="#22c55e",
                                   font=("system", 11))
        self.git_status.pack(side="right", padx=16, pady=12)

        self.status_label = tk.Label(header, text="Ready", bg="#1a1a1a", fg="#888",
                                      font=("system", 11))
        self.status_label.pack(side="right", padx=8, pady=12)

        # Toolbar
        toolbar = tk.Frame(self, bg="#1a1a1a")
        toolbar.pack(fill="x", pady=(1, 0))

        for label, cmd in [
            ("New Post", self.new_post),
            ("Generate", self.open_generate_window),
            ("Bold", lambda: self.insert_format("**", "**")),
            ("Italic", lambda: self.insert_format("*", "*")),
            ("Code", lambda: self.insert_format("`", "`")),
            ("Code Block", self.insert_code_block),
            ("Link", lambda: self.insert_format("[", "](url)")),
            ("Divider", lambda: self.insert_format("\n---\n", "")),
        ]:
            btn = tk.Button(toolbar, text=label, bg="#242424", fg="#e0e0e0", relief="flat",
                            cursor="hand2", font=("system", 11), padx=10, pady=4,
                            command=cmd)
            btn.pack(side="left", padx=2, pady=4)
            if label == "Generate":
                btn.configure(bg="#6366f1", fg="white")

        tk.Button(toolbar, text="Sync Metadata", bg="#242424", fg="#e0e0e0", relief="flat",
                  cursor="hand2", font=("system", 11), padx=10, pady=4,
                  command=self.sync_metadata).pack(side="left", padx=2, pady=4)

        # Main area
        main = tk.PanedWindow(self, orient="horizontal", bg="#0d0d0d")
        main.pack(fill="both", expand=True)

        # Left: post list
        left = tk.Frame(main, bg="#1a1a1a", width=280)
        main.add(left, width=280)

        tk.Label(left, text="Posts", bg="#1a1a1a", fg="#888",
                 font=("system", 11, "bold")).pack(pady=(12, 8))

        self.search = tk.Entry(left, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                              relief="flat", font=("system", 12))
        self.search.pack(fill="x", padx=12, pady=(0, 8))
        self.search.bind("<KeyRelease>", lambda e: self.filter_posts())

        list_frame = tk.Frame(left, bg="#1a1a1a")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        canvas = tk.Canvas(list_frame, bg="#1a1a1a", highlightthickness=0)
        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.post_list_frame = tk.Frame(canvas, bg="#1a1a1a")

        self.post_list_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.post_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Center: editor + preview
        center = tk.Frame(main, bg="#0d0d0d")
        main.add(center)

        # Metadata bar
        meta_bar = tk.Frame(center, bg="#1a1a1a", height=60)
        meta_bar.pack(fill="x")
        meta_bar.pack_propagate(False)

        for label, key in [("Title", "title"), ("Description", "description")]:
            tk.Label(meta_bar, text=label, bg="#1a1a1a", fg="#888",
                     font=("system", 10)).pack(side="left", padx=(12, 4), pady=8)
            e = tk.Entry(meta_bar, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                         relief="flat", font=("system", 12), width=30)
            e.pack(side="left", padx=(0, 12), pady=8)
            setattr(self, f"meta_{key}", e)

        tk.Label(meta_bar, text="Category", bg="#1a1a1a", fg="#888",
                 font=("system", 10)).pack(side="left", padx=(0, 4), pady=8)
        self.meta_category = ttk.Combobox(meta_bar, values=[
            "reflections", "tutorials", "news", "guides", "deep-dives"
        ], width=14, state="readonly")
        self.meta_category.set("reflections")
        self.meta_category.pack(side="left", padx=(0, 12), pady=8)

        tk.Label(meta_bar, text="Tags", bg="#1a1a1a", fg="#888",
                 font=("system", 10)).pack(side="left", padx=(0, 4), pady=8)
        e = tk.Entry(meta_bar, bg="#242424", fg="#e0e0e0", insertbackground="#e0e0e0",
                     relief="flat", font=("system", 12), width=20)
        e.pack(side="left", padx=(0, 12), pady=8)
        self.meta_tags = e

        # Stats
        stats_frame = tk.Frame(meta_bar, bg="#1a1a1a")
        stats_frame.pack(side="left", padx=8)
        for label, key in [("Words", "words"), ("Read", "read"), ("Headings", "headings")]:
            lbl = tk.Label(stats_frame, text="0", bg="#1a1a1a", fg="#818cf8",
                           font=("system", 14, "bold"))
            lbl.pack(side="left", padx=6)
            tk.Label(stats_frame, text=label, bg="#1a1a1a", fg="#888",
                     font=("system", 9)).pack(side="left", padx=(0, 8))
            setattr(self, f"stat_{key}", lbl)

        # Editor + Preview
        editors = tk.Frame(center)
        editors.pack(fill="both", expand=True)

        editor_pane = tk.Frame(editors, bg="#1a1a1a")
        editor_pane.pack(side="left", fill="both", expand=True)

        tk.Label(editor_pane, text="MARKDOWN", bg="#242424", fg="#888",
                 font=("system", 10, "bold")).pack(fill="x")
        self.editor = scrolledtext.ScrolledText(
            editor_pane, bg="#1a1a1a", fg="#e0e0e0", insertbackground="#e0e0e0",
            font=("SF Mono", 13), relief="flat", wrap="word", padx=12, pady=8,
            tabstyle="tabular"
        )
        self.editor.pack(fill="both", expand=True)
        self.editor.tag_configure("h1", font=("system", 20, "bold"), foreground="#818cf8")
        self.editor.tag_configure("h2", font=("system", 16, "bold"))
        self.editor.tag_configure("bold", font=("system", 13, "bold"))
        self.editor.bind("<KeyRelease>", self.on_edit)
        self.editor.bind("<Control-b>", lambda e: self.insert_format("**", "**"))
        self.editor.bind("<Control-i>", lambda e: self.insert_format("*", "*"))
        self.editor.bind("<Control-`>", lambda e: self.insert_format("`", "`"))

        preview_pane = tk.Frame(editors, bg="#1a1a1a")
        preview_pane.pack(side="right", fill="both", expand=True)

        tk.Label(preview_pane, text="PREVIEW", bg="#242424", fg="#888",
                 font=("system", 10, "bold")).pack(fill="x")
        self.preview = tk.Text(preview_pane, bg="#1a1a1a", fg="#e0e0e0",
                              font=("system", 14), relief="flat", wrap="word",
                              padx=16, pady=12, state="disabled")
        self.preview.pack(fill="both", expand=True)

        # Bottom bar
        bottom = tk.Frame(self, bg="#1a1a1a", height=52)
        bottom.pack(fill="x")
        bottom.pack_propagate(False)

        self.publish_btn = tk.Button(bottom, text="Publish to GitHub Pages", bg="#22c55e",
                                      fg="white", relief="flat", font=("system", 13, "bold"),
                                      cursor="hand2", padx=20, command=self.publish)
        self.publish_btn.pack(side="right", padx=16, pady=8)

        self.save_btn = tk.Button(bottom, text="Save Draft", bg="#6366f1",
                                  fg="white", relief="flat", font=("system", 13),
                                  cursor="hand2", padx=16, command=self.save_draft)
        self.save_btn.pack(side="right", padx=4, pady=8)

        self.discard_btn = tk.Button(bottom, text="Delete Post", bg="#ef4444",
                                     fg="white", relief="flat", font=("system", 13),
                                     cursor="hand2", padx=16, command=self.delete_post,
                                     state="disabled")
        self.discard_btn.pack(side="right", padx=4, pady=8)

        self.filename_label = tk.Label(bottom, text="New post", bg="#1a1a1a", fg="#888",
                                       font=("system", 11))
        self.filename_label.pack(side="left", padx=16)

    # ── Post List ────────────────────────────────────────────────────────────

    def refresh_post_list(self):
        self.posts = load_posts()
        self.render_post_list(self.posts)

    def render_post_list(self, posts):
        for w in self.post_list_frame.winfo_children():
            w.destroy()
        search = self.search.get().lower()
        for p in posts:
            if search and search not in p["title"].lower() and search not in p["filename"].lower():
                continue
            f = tk.Frame(self.post_list_frame, bg="#1a1a1a", relief="flat", cursor="hand2")
            f.pack(fill="x", pady=2)
            f.bind("<Button-1>", lambda e, fn=p["filename"]: self.load_post(fn))
            tk.Label(f, text=p["title"], bg="#1a1a1a", fg="#e0e0e0",
                     font=("system", 12), anchor="w").pack(fill="x", padx=8, pady=(6, 2))
            tk.Label(f, text=p["date"], bg="#1a1a1a", fg="#666",
                     font=("system", 10)).pack(fill="x", padx=8, pady=(0, 6))

    def filter_posts(self):
        self.render_post_list(self.posts)

    # ── Editor ───────────────────────────────────────────────────────────────

    def on_edit(self, *args):
        content = self.editor.get("1.0", "end")
        self.is_dirty = True
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", markdown_to_html(content))
        self.preview.configure(state="disabled")
        words, chars, read_time, headings = stats_from_content(content)
        self.stat_words.configure(text=str(words))
        self.stat_read.configure(text=f"{read_time}m")
        self.stat_headings.configure(text=str(headings))

    def insert_format(self, before, after):
        try:
            start = self.editor.index("sel.first")
            end = self.editor.index("sel.last")
            selected = self.editor.get(start, end)
            self.editor.delete(start, end)
            self.editor.insert(start, f"{before}{selected}{after}")
        except tk.TclError:
            self.editor.insert("insert", f"{before}{after}")
        self.on_edit()

    def insert_code_block(self):
        self.editor.insert("insert", "\n```\n\n```\n")
        self.editor.mark_set("insert", f"insert - 5 chars")
        self.on_edit()

    def sync_metadata(self):
        content = self.editor.get("1.0", "end")
        meta = parse_front_matter(content)
        self.meta_title.delete(0, "end")
        self.meta_title.insert(0, meta.get("title", ""))
        self.meta_description.delete(0, "end")
        self.meta_description.insert(0, meta.get("description", ""))
        self.meta_category.set(meta.get("categories", "reflections") or "reflections")
        self.meta_tags.delete(0, "end")
        self.meta_tags.insert(0, meta.get("tags", ""))

    def build_content(self):
        title = self.meta_title.get() or "Untitled"
        description = self.meta_description.get() or ""
        category = self.meta_category.get() or "reflections"
        tags = self.meta_tags.get() or ""
        date = ymd()
        body = get_body(self.editor.get("1.0", "end"))
        fm = build_front_matter(title, date, description, category, tags)
        return fm + body

    # ── Post Operations ────────────────────────────────────────────────────

    def new_post(self):
        self.current_filename = None
        self.is_dirty = False
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", f"""---
title: 
date: {ymd()}
layout: post
description: 
categories: [reflections]
tags: []
---

# 
""")
        self.meta_title.delete(0, "end")
        self.meta_description.delete(0, "end")
        self.meta_category.set("reflections")
        self.meta_tags.delete(0, "end")
        self.filename_label.configure(text="New post")
        self.discard_btn.configure(state="disabled")
        self.on_edit()
        self.refresh_git_status()

    def load_post(self, filename):
        filepath = POSTS_DIR / filename
        if not filepath.exists():
            messagebox.showerror("Error", f"File not found: {filename}")
            return
        content = filepath.read_text()
        meta = parse_front_matter(content)
        self.current_filename = filename
        self.is_dirty = False
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
        self.meta_title.delete(0, "end")
        self.meta_title.insert(0, meta.get("title", ""))
        self.meta_description.delete(0, "end")
        self.meta_description.insert(0, meta.get("description", ""))
        self.meta_category.set(meta.get("categories", "reflections") or "reflections")
        self.meta_tags.delete(0, "end")
        self.meta_tags.insert(0, meta.get("tags", ""))
        self.filename_label.configure(text=filename)
        self.discard_btn.configure(state="normal")
        self.on_edit()
        self.refresh_git_status()

    def save_draft(self):
        content = self.build_content()
        title = self.meta_title.get() or "Untitled"
        slug = slugify(title)
        filename = f"{ymd()}-{slug}.md"
        filepath = POSTS_DIR / filename
        filepath.write_text(content)
        self.current_filename = filename
        self.is_dirty = False
        self.filename_label.configure(text=filename)
        self.discard_btn.configure(state="normal")
        self.status_label.configure(text=f"Saved: {title}")
        self.refresh_post_list()
        self.refresh_git_status()

    def publish(self):
        self.save_draft()
        if not self.current_filename:
            return
        title = self.meta_title.get() or "Untitled"
        self.status_label.configure(text="Publishing...")
        self.publish_btn.configure(state="disabled")

        ok, out, err = git_run("add", f"_posts/{self.current_filename}")
        if not ok:
            messagebox.showerror("Git Error", f"git add failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        ok, out, err = git_run("commit", "-m", f"Blog composer: {title}")
        if not ok:
            if "nothing to commit" in err.lower():
                self.status_label.configure(text="No changes to publish")
                self.publish_btn.configure(state="normal")
                return
            messagebox.showerror("Git Error", f"git commit failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        ok, out, err = git_run("push", "origin", "main")
        if not ok:
            messagebox.showerror("Git Error", f"git push failed: {err}")
            self.publish_btn.configure(state="normal")
            self.status_label.configure(text="Ready")
            return

        self.is_dirty = False
        self.status_label.configure(text=f"Published: {title}")
        self.publish_btn.configure(state="normal")
        self.refresh_git_status()
        messagebox.showinfo("Published", f"Post published:\n{title}\n\nhttps://thesolai.github.io/blog/")

    def delete_post(self):
        if not self.current_filename:
            return
        if not messagebox.askyesno("Delete", f"Delete {self.current_filename}?"):
            return
        filepath = POSTS_DIR / self.current_filename
        if filepath.exists():
            filepath.unlink()
        ok, out, err = git_run("add", f"_posts/{self.current_filename}")
        ok, out, err = git_run("commit", "-m", f"Delete: {self.current_filename}")
        if ok:
            git_run("push", "origin", "main")
        self.new_post()
        self.refresh_post_list()

    def refresh_git_status(self):
        ok, out, _ = git_run("status", "--porcelain")
        if out.strip():
            self.git_status.configure(text="Changes pending", fg="#f59e0b")
        else:
            self.git_status.configure(text="Clean", fg="#22c55e")

    # ── Generate Window ──────────────────────────────────────────────────

    def open_generate_window(self):
        win = tk.Toplevel(self)
        win.title("Generate Post")
        win.geometry("1100x750")
        win.configure(bg="#0d0d0d")
        win.transient(self)

        # ── Form panel (left, narrow) ──────────────────────────────────────

        form = tk.Frame(win, bg="#1a1a1a", padx=16, pady=16)
        form.pack(side="left", fill="y", padx=(0, 1))

        tk.Label(form, text="Generate with AI", bg="#1a1a1a", fg="#818cf8",
                font=("system", 15, "bold")).pack(anchor="w", pady=(0, 16))

        # Topic
        tk.Label(form, text="Topic / Idea", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(0, 4))
        topic_var = tk.StringVar()
        topic_entry = tk.Entry(form, textvariable=topic_var, bg="#242424", fg="#e0e0e0",
                               insertbackground="#e0e0e0", relief="flat",
                               font=("system", 12), width=34)
        topic_entry.pack(fill="x", pady=(0, 14))
        topic_entry.focus()

        # Post types — card-style checkboxes
        tk.Label(form, text="Post Types", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(0, 6))

        type_vars = {}
        type_info = [
            ("deep-dive", "Deep Dive", "Comprehensive, technical depth"),
            ("analysis", "Analysis", "News, context, opinion"),
            ("reflection", "Reflection", "Personal take, philosophical"),
            ("tutorial", "Tutorial", "Step-by-step guide"),
        ]
        for t, label, desc in type_info:
            type_vars[t] = tk.BooleanVar(value=(t == "deep-dive"))
            f = tk.Frame(form, bg="#242424", padx=10, pady=8)
            f.pack(fill="x", pady=2)
            cb = tk.Checkbutton(f, variable=type_vars[t],
                               bg="#242424", fg="#e0e0e0", selectcolor="#6366f1",
                               activebackground="#242424", font=("system", 11))
            cb.pack(side="left", padx=(0, 8))
            lbl_frame = tk.Frame(f, bg="#242424")
            lbl_frame.pack(side="left")
            tk.Label(lbl_frame, text=label, bg="#242424", fg="#e0e0e0",
                    font=("system", 11, "bold")).pack(anchor="w")
            tk.Label(lbl_frame, text=desc, bg="#242424", fg="#666",
                    font=("system", 9)).pack(anchor="w")

        # Tone
        tk.Label(form, text="Tone", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(14, 4))
        tone_var = tk.StringVar(value="accessible")
        for val, label in [("accessible", "Accessible"), ("technical", "Technical"), ("balanced", "Balanced")]:
            tk.Radiobutton(form, text=label, variable=tone_var, value=val,
                          bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                          font=("system", 11), anchor="w").pack(anchor="w", pady=1)

        # Length
        tk.Label(form, text="Length", bg="#1a1a1a", fg="#888",
                font=("system", 10)).pack(anchor="w", pady=(12, 4))
        length_var = tk.StringVar(value="medium")
        for val, label in [
            ("short", "Short (~400 words)"),
            ("medium", "Medium (~800 words)"),
            ("long", "Long (~1500 words)"),
            ("xl", "Extended (~2500 words)"),
        ]:
            tk.Radiobutton(form, text=label, variable=length_var, value=val,
                          bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                          font=("system", 11), anchor="w").pack(anchor="w", pady=1)

        # Research
        research_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form, text="Research on internet first", variable=research_var,
                      bg="#1a1a1a", fg="#e0e0e0", selectcolor="#6366f1",
                      font=("system", 11), anchor="w", pady=(14, 4)).pack(anchor="w")

        # Research context display (shown after research runs)
        research_frame = tk.Frame(form, bg="#1a1a1a")
        research_frame.pack(fill="x", pady=(8, 0))
        research_label = tk.Label(research_frame, text="", bg="#1a1a1a", fg="#555",
                                  font=("system", 9), anchor="w", justify="left", wraplength=220)
        research_label.pack(fill="x")

        # Status
        status_label = tk.Label(form, text="", bg="#1a1a1a", fg="#888",
                               font=("system", 10), anchor="w", wraplength=220)
        status_label.pack(fill="x", pady=(8, 0))

        # Word count (live during streaming)
        wc_label = tk.Label(form, text="", bg="#1a1a1a", fg="#818cf8",
                           font=("system", 12, "bold"), anchor="w")
        wc_label.pack(fill="x")

        # Generate / Cancel button
        gen_btn = tk.Button(form, text="Generate Post", bg="#6366f1", fg="white",
                           relief="flat", font=("system", 12, "bold"),
                           cursor="hand2", padx=16, pady=10)
        gen_btn.pack(fill="x", pady=(8, 0))

        # ── Output panel (right, split markdown / preview) ───────────────

        # Make sash visible with a handle bar
        sash_frame = tk.Frame(win, bg="#2a2a2a", width=6)
        sash_frame.pack(side="left", fill="y")

        outPaned = tk.PanedWindow(win, orient="horizontal", bg="#0d0d0d",
                                  sashpad=0, sashrelief="flat", sashwidth=6)
        outPaned.pack(side="right", fill="both", expand=True)

        md_frame = tk.Frame(outPaned, bg="#1a1a1a")
        outPaned.add(md_frame, width=500)

        header_frame = tk.Frame(md_frame, bg="#242424")
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="MARKDOWN OUTPUT", bg="#242424", fg="#888",
                font=("system", 10, "bold")).pack(side="left", padx=10, pady=6)
        self._gen_wc_label = tk.Label(header_frame, text="", bg="#242424", fg="#6366f1",
                                      font=("system", 10, "bold"))
        self._gen_wc_label.pack(side="right", padx=10, pady=6)

        output_text = scrolledtext.ScrolledText(md_frame, bg="#0d0d0d", fg="#e0e0e0",
                        insertbackground="#e0e0e0", font=("SF Mono", 12), relief="flat",
                        wrap="word", padx=12, pady=8, state="disabled")
        output_text.pack(fill="both", expand=True)

        pv_frame = tk.Frame(outPaned, bg="#1a1a1a")
        outPaned.add(pv_frame, width=400)
        tk.Label(pv_frame, text="PREVIEW", bg="#242424", fg="#888",
                font=("system", 10, "bold")).pack(fill="x")
        preview_text = scrolledtext.ScrolledText(pv_frame, bg="#1a1a1a", fg="#e0e0e0",
                         font=("system", 14), relief="flat", wrap="word",
                         padx=16, pady=12, state="disabled")
        preview_text.pack(fill="both", expand=True)

        # ── Bottom buttons ─────────────────────────────────────────────────

        btn_frame = tk.Frame(win, bg="#1a1a1a", height=52)
        btn_frame.pack(fill="x", side="bottom")
        btn_frame.pack_propagate(False)

        use_btn = tk.Button(btn_frame, text="Use in Editor", bg="#22c55e", fg="white",
                           relief="flat", font=("system", 13, "bold"),
                           cursor="hand2", padx=20, pady=8, state="disabled")
        use_btn.pack(side="left", padx=16, pady=8)
        tk.Button(btn_frame, text="Cancel", bg="#242424", fg="#e0e0e0",
                 relief="flat", font=("system", 12), cursor="hand2",
                 padx=16, pady=8, command=win.destroy).pack(side="right", padx=16, pady=8)

        # ── Generation state ───────────────────────────────────────────────

        gen_state = {"text": "", "types": [], "cancelled": False}

        def update_preview(text):
            preview_text.configure(state="normal")
            preview_text.delete("1.0", "end")
            preview_text.insert("1.0", markdown_to_html(text))
            preview_text.configure(state="disabled")

        def on_line(line):
            """Called on the main thread for each streamed line."""
            content = "".join(gen_state["text"]) + line
            gen_state["text"] = content
            # Update markdown output
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            # Live preview update every few lines
            words = len(content.split())
            wc_label.configure(text=f"{words} words")
            self._gen_wc_label.configure(text=f"{words}w")
            update_preview(content)

        def do_generate():
            topic = topic_var.get().strip()
            if not topic:
                status_label.configure(text="Enter a topic first", fg="#ef4444")
                return
            types_snapshot = [t for t in type_vars if type_vars[t].get()]
            if not types_snapshot:
                status_label.configure(text="Select at least one post type", fg="#ef4444")
                return
            gen_state["types"] = types_snapshot
            gen_state["text"] = ""
            gen_state["cancelled"] = False

            # Switch button to Cancel while running
            gen_btn.configure(text="Cancel Generation", bg="#ef4444", fg="white",
                             command=cancel_generate)
            status_label.configure(text="Researching Wikipedia...", fg="#818cf8")
            research_label.configure(text="")
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", "Preparing...")
            output_text.configure(state="disabled")
            update_preview("Preparing...")
            wc_label.configure(text="")
            self._gen_wc_label.configure(text="")
            use_btn.configure(state="disabled")
            win.update()

            import threading
            threading.Thread(target=_do_generate, args=(
                topic, types_snapshot, tone_var.get(),
                length_var.get(), research_var.get(), win
            ), daemon=True).start()

        def cancel_generate():
            gen_state["cancelled"] = True
            reset_ui()

        def reset_ui():
            gen_btn.configure(state="normal", text="Generate Post", bg="#6366f1", fg="white",
                             command=do_generate)

        def _do_generate(topic, types_snapshot, tone, length, research, win):
            try:
                # Phase 1: research
                research_context, research_snippets = self._do_research(topic, research)
                win.after(0, lambda: status_label.configure(
                    text=f"Research done — {len(research_snippets)} sources. Generating...",
                    fg="#818cf8"))
                win.after(0, lambda: research_label.configure(
                    text="\n".join(f"• {s[:80]}" for s in research_snippets[:3]) if research_snippets else ""))

                # Phase 2: build prompt
                WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
                word_target = WORDS_MAP.get(length, 800)
                structures = {
                    "deep-dive": ["Open broad — what's the topic and why does it matter?","Build the foundation — key concepts readers need.","Explore multiple angles — don't just present one view.","Get technical — show real depth.","Tie together — what does all this mean?","Open questions — what's still unresolved?"],
                    "analysis": ["Start with the news — what happened, when, who was involved.","Explain why it matters. What's the real impact?","Give context — how does this fit the bigger picture?","State a clear opinion. Don't hedge everything.","End with what happens next or what it means going forward."],
                    "reflection": ["Open with a concrete observation or experience.","Explore the idea — what does it mean, why does it matter?","Connect to broader implications without getting preachy.","End with a clean insight or question. Don't over-conclude."],
                    "tutorial": ["State what you'll build or do and who it's for.","Prerequisites — what do you need before starting?","Step by step — clear, numbered, reproducible.","Show the result — what does success look like?","Point to what's next or common pitfalls."],
                }
                all_structure, tags = [], []
                for t in types_snapshot:
                    if t in structures:
                        all_structure.extend(structures[t])
                        if t == "deep-dive": tags.extend(["deep-dive", "analysis", "technical"])
                        elif t == "analysis": tags.extend(["analysis", "ai-news"])
                        elif t == "reflection": tags.extend(["reflection", "ai"])
                        elif t == "tutorial": tags.extend(["tutorial", "guide", "tools"])
                tags = list(dict.fromkeys(tags))
                tone_map = {"balanced": "balanced and objective", "technical": "technical and precise", "accessible": "accessible and clear"}
                tone_desc = tone_map.get(tone, "accessible")
                structure_str = "\n".join(f"{i+1}. {s}" for i, s in enumerate(all_structure[:6]))
                prompt = (f"Write a blog post for the Sol AI blog (thesolai.github.io).\n\n"
                         f"Voice: Sol AI blog (thesolai.github.io) — thoughtful, direct, no filler, technical depth.\n"
                         f"Tone: {tone_desc}.\n"
                         f"Target: {word_target} words.\n\n"
                         f"Topic: {topic}\n"
                         f"{research_context}\n\n"
                         f"Structure:\n{structure_str}\n\n"
                         f"Format: Return ONLY Markdown. Start with first heading. No preamble.")

                # Phase 3: call MiniMax API (non-streaming)
                import json, urllib.request
                try:
                    api_key = open("/Users/amre/.openclaw/workspace/secrets/minimax-key.txt").read().strip()
                except Exception:
                    win.after(0, lambda: _on_fail("MiniMax API key not found"))
                    return

                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                max_tokens_map = {"short": 1024, "medium": 2048, "long": 8192}
                payload = {
                    "model": "MiniMax-M2.7",
                    "max_tokens": max_tokens_map.get(length, 4096),
                    "temperature": 0.7,
                    "thinking_enabled": False,
                    "messages": [{"role": "user", "content": prompt}]
                }
                data = json.dumps(payload).encode()
                req = urllib.request.Request(
                    "https://api.minimax.io/anthropic/v1/messages",
                    data=data, headers=headers, method="POST"
                )

                def do_http():
                    try:
                        with urllib.request.urlopen(req, timeout=120) as res:
                            result = json.loads(res.read())
                            content = result["content"][0]["text"].strip()
                            gen_state["text"] = content
                            win.after(0, lambda: _on_done(content))
                    except Exception as e:
                        win.after(0, lambda err=str(e): _on_fail(err))

                import threading
                threading.Thread(target=do_http, daemon=True).start()

            except Exception as e:
                win.after(0, lambda err=str(e): _on_fail(err))


        def _on_chunk(content):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            words = len(content.split())
            wc_label.configure(text=f"{words} words")
            self._gen_wc_label.configure(text=f"{words}w")
            update_preview(content)

        def _on_done(content):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", content)
            output_text.configure(state="disabled")
            update_preview(content)
            words = len(content.split())
            wc_label.configure(text=f"{words} words — done!")
            self._gen_wc_label.configure(text=f"{words}w")
            reset_ui()
            status_label.configure(
                text=f"Generated {words} words. Review below, then Use in Editor.",
                fg="#22c55e")
            use_btn.configure(state="normal")

        def _on_fail(err):
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("1.0", f"Error: {err}")
            output_text.configure(state="disabled")
            update_preview("")
            reset_ui()
            status_label.configure(text=f"Failed: {err}", fg="#ef4444")
            wc_label.configure(text="")
            self._gen_wc_label.configure(text="")

        gen_btn.configure(command=do_generate)
        topic_entry.bind("<Return>", lambda e: do_generate())

        def use_in_editor():
            content = gen_state["text"]
            if not content:
                return
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else topic_var.get().strip()
            types_snap = gen_state.get("types", [])
            tags_str = ", ".join(types_snap)
            category = ("deep-dives" if "deep-dive" in types_snap else
                        "news" if "analysis" in types_snap else
                        "tutorials" if "tutorial" in types_snap else "reflections")
            fm = build_front_matter(title, ymd(), "", category, tags_str)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", fm + content)
            self.meta_title.delete(0, "end")
            self.meta_title.insert(0, title)
            self.meta_category.set(category)
            self.meta_tags.delete(0, "end")
            self.meta_tags.insert(0, tags_str)
            self.on_edit()
            self.refresh_git_status()
            win.destroy()

        use_btn.configure(command=use_in_editor)

    def _do_research(self, topic, do_research):
        """Fetch Wikipedia context. Returns (context_str, snippet_list)."""
        if not do_research:
            return "", []
        import urllib.request, urllib.parse, json
        snippets = []
        try:
            url = (f"https://en.wikipedia.org/w/api.php?action=query&list=search"
                   f"&srsearch={urllib.parse.quote(topic)}&srlimit=6&format=json"
                   f"&prop=extracts&exintro=1&explaintext=1")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Sol Blog Composer)"})
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read())
                for r in data.get("query", {}).get("search", []):
                    snippet = re.sub(r'<[^>]+>', '', r.get("snippet", ""))
                    snippets.append(f"{r['title']}: {snippet[:200]}")
        except Exception:
            pass
        ctx = "\n\nWeb research context:\n" + "\n".join(f"- {s}" for s in snippets) if snippets else ""
        return ctx, snippets

    def _generate_content(self, topic, types, tone, length, research):
        """Generate post content via Ollama HTTP API — clean output, no ANSI corruption."""
        # Research via Wikipedia
        research_context = ""
        if research:
            try:
                import urllib.request, urllib.parse, json
                url = (
                    f"https://en.wikipedia.org/w/api.php?action=query&list=search"
                    f"&srsearch={urllib.parse.quote(topic)}&srlimit=6&format=json"
                    f"&prop=extracts&exintro=1&explaintext=1"
                )
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Sol Blog Composer)"})
                with urllib.request.urlopen(req, timeout=10) as res:
                    data = json.loads(res.read())
                    results = data.get("query", {}).get("search", [])
                    if results:
                        snippets = []
                        for r in results:
                            s = re.sub(r"<[^>]+>", "", r.get("snippet", ""))
                            snippets.append("- " + r["title"] + ": " + s[:200])
                        research_context = "\n\nWeb research context:\n" + "\n".join(snippets)
            except Exception:
                pass

        # Build prompt
        WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
        word_target = WORDS_MAP.get(length, 800)
        structures = {
            "deep-dive": [
                "Open broad — what's the topic and why does it matter?",
                "Build the foundation — key concepts readers need.",
                "Explore multiple angles — don't just present one view.",
                "Get technical — show real depth.",
                "Tie together — what does all this mean?",
                "Open questions — what's still unresolved?",
            ],
            "analysis": [
                "Start with the news — what happened, when, who was involved.",
                "Explain why it matters. What's the real impact?",
                "Give context — how does this fit the bigger picture?",
                "State a clear opinion. Don't hedge everything.",
                "End with what happens next or what it means going forward.",
            ],
            "reflection": [
                "Open with a concrete observation or experience.",
                "Explore the idea — what does it mean, why does it matter?",
                "Connect to broader implications without getting preachy.",
                "End with a clean insight or question. Don't over-conclude.",
            ],
            "tutorial": [
                "State what you'll build or do and who it's for.",
                "Prerequisites — what do you need before starting?",
                "Step by step — clear, numbered, reproducible.",
                "Show the result — what does success look like?",
                "Point to what's next or common pitfalls.",
            ],
        }
        all_structure, tags = [], []
        for t in types:
            if t in structures:
                all_structure.extend(structures[t])
                if t == "deep-dive": tags.extend(["deep-dive", "analysis", "technical"])
                elif t == "analysis": tags.extend(["analysis", "ai-news"])
                elif t == "reflection": tags.extend(["reflection", "ai"])
                elif t == "tutorial": tags.extend(["tutorial", "guide", "tools"])
        tags = list(dict.fromkeys(tags))
        tone_map = {
            "balanced": "balanced and objective",
            "technical": "technical and precise, assume some technical knowledge",
            "accessible": "accessible and clear, avoid jargon where possible",
        }
        tone_desc = tone_map.get(tone, "accessible")
        structure_str = "\n".join(f"{i+1}. {s}" for i, s in enumerate(all_structure[:6]))
        prompt = (
            "Write a blog post for the Sol AI blog (thesolai.github.io).\n\n"
            "Voice: thoughtful, direct, no filler, technical depth. Write for the Sol AI blog.\n"
            f"Tone: {tone_desc}.\n"
            f"Target: {word_target} words.\n\n"
            f"Topic: {topic}\n"
            f"{research_context}\n\n"
            "Structure:\n" + structure_str + "\n\n"
            "Format: Return ONLY the post content in Markdown. Start with the first heading. No preamble."
        )

        # Call MiniMax API (Anthropic-compatible)
        import json, urllib.request
        key_path = "/Users/amre/.openclaw/workspace/secrets/minimax-key.txt"
        try:
            api_key = open(key_path).read().strip()
        except Exception:
            raise Exception("MiniMax API key not found at ~/.openclaw/workspace/secrets/minimax-key.txt")

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        WORDS_MAP = {"short": 400, "medium": 800, "long": 1500, "xl": 2500, "full": 4000}
        max_tokens = {"short": 1024, "medium": 2048, "long": 8192}.get(length, 4096)

        payload = {
            "model": "MiniMax-M2.7",
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "thinking_enabled": False,
            "messages": [{"role": "user", "content": prompt}]
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            "https://api.minimax.io/anthropic/v1/messages",
            data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                result = json.loads(res.read())
                # MiniMax returns content as a list of blocks (thinking + text)
                text_parts = []
                for block in result.get("content", []):
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                return "".join(text_parts).strip()
        except Exception as e:
            raise Exception(f"MiniMax generation failed: {e}")


if __name__ == "__main__":
    app = BlogComposer()
    app.mainloop()


---
name: clank-blog-post
description: Create and publish blog posts to GitHub Pages. Generates styled HTML posts, updates the blog index, commits, and pushes. Perfect for agent blogs, project updates, and content publishing.
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["git"] },
      },
  }
---

# clank-blog-post

Create and publish styled blog posts to GitHub Pages from the CLI.

## When to use (trigger phrases)

Use this skill when the user asks any of:

- "Write a blog post about..."
- "Publish to my blog"
- "New post for the blog"
- "Add an article to the website"
- "Blog about..."

## Quick start

```bash
# Create a new post
clank-blog-post create "My Post Title" --tags "KI, Tools" --reading-time 4

# Create and immediately publish
clank-blog-post publish "My Post Title" --tags "KI, Tools"

# List all posts
clank-blog-post list

# Update the index page
clank-blog-post index
```

## How it works

1. **Create** — Generates a styled HTML file from your content
2. **Index** — Updates `index.html` with the new post entry (newest first)
3. **Push** — Commits and pushes to your GitHub Pages repo

## Post structure

Each post is a standalone HTML file with:
- Dark theme matching the blog design
- Responsive layout (700px content width)
- Consistent styling (orange accent, Georgia serif)
- Back-link to index
- Footer with metadata

### Style variables

```css
--bg: #0f0f23;
--card: #1a1a2e;
--accent: #ff6b35;
--text: #e0e0e0;
--muted: #888;
--border: #2a2a4e;
```

## Template

Use this template for new posts:

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} – Clank Blog</title>
    <style>
        :root { --bg: #0f0f23; --card: #1a1a2e; --accent: #ff6b35; --text: #e0e0e0; --muted: #888; --border: #2a2a4e; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Georgia', serif; background: var(--bg); color: var(--text); line-height: 1.9; }
        .container { max-width: 700px; margin: 0 auto; padding: 2rem; }
        h1 { color: var(--accent); font-size: 2rem; margin: 2rem 0 0.5rem; }
        .meta { color: var(--muted); font-size: 0.9rem; margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }
        p { margin-bottom: 1.5rem; }
        h2 { color: var(--accent); margin: 2.5rem 0 1rem; font-size: 1.3rem; }
        h3 { color: #fff; margin: 1.5rem 0 0.8rem; font-size: 1.1rem; }
        ul, ol { margin: 1rem 0 1.5rem 1.5rem; }
        li { margin-bottom: 0.5rem; }
        strong { color: #fff; }
        blockquote { border-left: 3px solid var(--accent); padding: 1rem 1.5rem; margin: 1.5rem 0; background: var(--card); border-radius: 0 8px 8px 0; }
        code { background: var(--card); padding: 0.8rem 1rem; border-radius: 8px; display: block; margin: 1rem 0; font-size: 0.85rem; white-space: pre; overflow-x: auto; color: #4caf50; }
        a.back { color: var(--accent); text-decoration: none; display: inline-block; margin-bottom: 2rem; }
        footer { text-align: center; padding: 3rem 2rem; color: var(--muted); border-top: 1px solid var(--border); margin-top: 3rem; }
        footer a { color: var(--accent); text-decoration: none; }
    </style>
</head>
<body>
<div class="container">
    <a href="index.html" class="back">← Zurück zum Blog</a>
    <h1>{TITLE}</h1>
    <div class="meta">{DATE} · Clank · Tags: {TAGS}</div>

    {CONTENT}

    <footer>
        ⚡ Clank · Ein Agent denkt laut<br>
        <a href="index.html">Zurück zum Blog</a>
    </footer>
</div>
</body>
</html>
```

## Index entry template

Add this to `index.html` inside `<div class="container">`, before the first `<article>`:

```html
<article>
    <h2>{TITLE}</h2>
    <div class="meta">{DATE} · {READING_TIME} min · {TAGS}</div>
    <p class="excerpt">{EXCERPT}</p>
    <a href="{FILENAME}" class="read-more">Weiterlesen →</a>
</article>
```

## Workflow for agents

```bash
# 1. Clone the blog repo
cd /tmp && git clone git@github.com-Clankr0i:clank-blog.git

# 2. Write the post
# Create {slug}.html using the template above

# 3. Update index.html
# Insert the article entry as the first article in .container

# 4. Commit and push
cd /tmp/clank-blog
git add -A
git commit -m "Neuer Post: {TITLE}"
git push origin master

# 5. Verify deployment (GitHub Pages takes ~30s)
curl -s "https://clankr0i.github.io/clank-blog/{slug}.html" | head -5
```

## Tips

- **Filename:** Use URL-safe slugs: `mein-post.html`
- **Excerpt:** Keep it to 1-2 sentences for the index card
- **Reading time:** Roughly 200 words/minute for German
- **Tags:** Max 3, comma-separated
- **Date format:** "29. März 2026" (German)
- **Deploy time:** GitHub Pages usually takes 30-60 seconds after push

## Customization

Change these constants for your own blog:

| Variable | Default | Description |
|----------|---------|-------------|
| `REPO` | `Clankr0i/clank-blog` | GitHub repo |
| `BRANCH` | `master` | Deploy branch |
| `DOMAIN` | `clankr0i.github.io/clank-blog/` | Live URL |
| `THEME_ACCENT` | `#ff6b35` | Accent color |
| `THEME_BG` | `#0f0f23` | Background color |

#!/usr/bin/env python3
import json
from pathlib import Path

OUTPUT_DIR = Path.home() / '.openclaw/workspace/techrex-website/content/blog/blogger-html-full'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
POSTS_JSON = Path.home() / '.openclaw/workspace/techrex-website/content/blog/posts.json'

with open(POSTS_JSON) as f:
    posts = json.load(f)['blogPosts']

skip = {'01-llmfit-guide', '02-claude-office'}

def embed(video_id, title):
    return f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 12px; margin: 20px 0;">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" src="https://www.youtube.com/embed/{video_id}" title="{title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>'''

def full_html(p):
    title = p['title']
    cat = p['category']
    date = p['date']
    ex = p['excerpt']
    tags = ', '.join(p.get('tags', []))
    return f'''<div style="font-family: Segoe UI, Arial, sans-serif; line-height: 1.85; color:#222; max-width: 820px; margin:0 auto;">
<h1 style="color:#1f9d55;">{title}</h1>
<p style="color:#666; font-size:17px;"><strong>Category:</strong> {cat} | <strong>Published:</strong> {date}</p>
{embed(p['youtubeId'], title)}

<h2>Overview</h2>
<p>{ex}</p>
<p>This article expands the core ideas from the video and turns them into a practical, step-by-step reference you can apply immediately.</p>

<h2>Why This Matters</h2>
<ul>
  <li><strong>Speed:</strong> Cut trial-and-error and move faster.</li>
  <li><strong>Clarity:</strong> Understand what to do and why it works.</li>
  <li><strong>Execution:</strong> Apply a repeatable workflow in real projects.</li>
</ul>

<h2>Core Concepts Explained</h2>
<p>The most important idea in this topic is to combine <strong>correct tooling</strong> with <strong>practical workflow</strong>. Many people focus only on tools, but outcomes come from process: identify the goal, choose the right approach, test quickly, then iterate.</p>
<p>In the video, the same principle appears repeatedly: start small, validate assumptions, and then scale. That prevents wasted time and avoids expensive mistakes.</p>

<h2>Step-by-Step Workflow</h2>
<ol>
  <li><strong>Define outcome:</strong> Be explicit about what success looks like.</li>
  <li><strong>Set baseline:</strong> Measure current performance/quality.</li>
  <li><strong>Implement:</strong> Apply the method shown in the video.</li>
  <li><strong>Validate:</strong> Compare before/after with clear metrics.</li>
  <li><strong>Optimize:</strong> Tune settings based on bottlenecks.</li>
</ol>

<h2>Practical Tips</h2>
<ul>
  <li>Keep a short checklist and run it every time.</li>
  <li>Document what changed so improvements are repeatable.</li>
  <li>If performance drops, reduce complexity and test incrementally.</li>
  <li>Prioritize reliability first, then speed and advanced features.</li>
</ul>

<h2>Common Mistakes to Avoid</h2>
<ul>
  <li>Skipping validation and assuming defaults are optimal.</li>
  <li>Changing too many variables at once.</li>
  <li>Ignoring hardware/software constraints.</li>
  <li>Copying workflows without adapting to your own setup.</li>
</ul>

<h2>Example Implementation Plan</h2>
<p><strong>Week 1:</strong> Set up the stack and run a baseline test.</p>
<p><strong>Week 2:</strong> Apply the workflow to one real task end-to-end.</p>
<p><strong>Week 3:</strong> Optimize bottlenecks and improve quality.</p>
<p><strong>Week 4:</strong> Standardize into a reusable template/process.</p>

<h2>Key Takeaways</h2>
<ul>
  <li>Use the right method for your exact goal.</li>
  <li>Measure outcomes, don’t rely on assumptions.</li>
  <li>Iterative improvements beat one-time “perfect” setups.</li>
</ul>

<h2>Watch the Full Video</h2>
<p>For demos and visual walkthrough, watch the complete video embedded above.</p>

<p><strong>Tags:</strong> {tags}</p>

<div style="background: linear-gradient(135deg,#1f9d55,#34d399); color:white; padding:18px; border-radius:12px; margin-top:28px;">
  <h3 style="margin:0 0 8px 0;">🦖 Evolve or Get Extinct</h3>
  <p style="margin:0;">If this helped, subscribe and follow TechRex for in-depth AI tutorials.</p>
</div>
</div>'''

count = 0
for p in posts:
    if p['id'] in skip:
        continue
    path = OUTPUT_DIR / f"{p['id']}.html"
    path.write_text(full_html(p))
    count += 1
    print(f"generated {path.name}")

print(f"done: {count} files")

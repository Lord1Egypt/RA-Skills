#!/usr/bin/env python3
"""
Generate all 19 full-length blog posts
"""

import json
from pathlib import Path

OUTPUT_DIR = Path.home() / ".openclaw/workspace/techrex-website/content/blog/blogger-html-full"
OUTPUT_DIR.mkdir(exist_ok=True)

POSTS_JSON = Path.home() / ".openclaw/workspace/techrex-website/content/blog/posts.json"
with open(POSTS_JSON) as f:
    POSTS_DATA = json.load(f)['blogPosts']

def get_post(post_id):
    for p in POSTS_DATA:
        if p['id'] == post_id:
            return p
    return None

def embed(video_id, title):
    return f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 12px; margin: 20px 0;">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;" 
    src="https://www.youtube.com/embed/{video_id}" title="{title}" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
</div>'''

def wrap(title, date, category, embed_code, body):
    return f'''<div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto;">

<h1 style="color: #27ae60;">{title}</h1>

<p style="font-size: 18px; color: #666;"><strong>Category:</strong> {category} | <strong>Published:</strong> {date}</p>

{embed_code}

{body}

<div style="background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 20px; border-radius: 12px; margin-top: 30px;">
<h3 style="margin: 0 0 10px 0;">🦖 Evolve or Get Extinct</h3>
<p style="margin: 0;">Learn, Build, Launch — Without The Struggle. Subscribe for more AI tutorials!</p>
<a href="https://www.youtube.com/@The_TechRex?sub_confirmation=1" style="display: inline-block; background: #ff0000; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-top: 15px; font-weight: bold;">Subscribe on YouTube →</a>
</div>

</div>'''

posts_content = {}

# Post 01: LLMfit Guide
p = get_post("01-llmfit-guide")
posts_content["01-llmfit-guide"] = wrap(p['title'], p['date'], p['category'], embed(p['youtubeId'], p['title']), """
<h2>The Problem: Downloading AI Models That Don't Work</h2>
<p>Have you ever spent hours downloading a 7GB AI model, only to find out your laptop can't run it? You're not alone. This happens to thousands of people every day. The AI revolution is here, but most people don't know if their hardware can actually handle it.</p>

<h2>The Solution: LLMfit</h2>
<p>Enter <strong>LLMfit</strong> — a free, open-source tool that analyzes your hardware and tells you <em>exactly</em> which Large Language Models will work on your specific machine.</p>

<h2>Understanding Model Sizes</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
<tr style="background: #27ae60; color: white;"><th style="padding: 12px;">Model Size</th><th style="padding: 12px;">RAM Needed</th><th style="padding: 12px;">Hardware Required</th></tr>
<tr style="background: #f9f9f9;"><td style="padding: 12px;">1B-3B (Tiny)</td><td style="padding: 12px;">4-8 GB</td><td style="padding: 12px;">Any modern laptop</td></tr>
<tr><td style="padding: 12px;">7B-8B (Small)</td><td style="padding: 12px;">8-16 GB</td><td style="padding: 12px;">Laptop with 16GB RAM</td></tr>
<tr style="background: #f9f9f9;"><td style="padding: 12px;">13B-14B (Medium)</td><td style="padding: 12px;">16-32 GB</td><td style="padding: 12px;">Gaming PC / Workstation</td></tr>
<tr><td style="padding: 12px;">35B-40B (Large)</td><td style="padding: 12px;">24-48 GB VRAM</td><td style="padding: 12px;">RTX 3090/4090 or M3 Max</td></tr>
<tr style="background: #f9f9f9;"><td style="padding: 12px;">70B+ (Massive)</td><td style="padding: 12px;">40-80 GB VRAM</td><td style="padding: 12px;">Multiple GPUs / Cloud</td></tr>
</table>

<h2>Understanding Quantization</h2>
<p><strong>Q4 (4-bit):</strong> The most compressed. Model size is ~25% of original. Fast inference but some quality loss. Great for testing.</p>
<p><strong>Q5-Q6 (5-6 bit):</strong> Good balance. ~40% of original size. Most quality preserved.</p>
<p><strong>Q8 (8-bit):</strong> Near-original quality. ~50% of original size. Recommended for production.</p>
<p><strong>FP16 (16-bit):</strong> Full quality. 100% of original size. Best results but requires most resources.</p>

<h2>How to Use LLMfit</h2>
<h3>Step 1: Installation</h3>
<pre style="background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px;">git clone https://github.com/yourusername/llmfit.git
cd llmfit
pip install -r requirements.txt</pre>

<h3>Step 2: Run Analysis</h3>
<pre style="background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px;">python llmfit.py --analyze</pre>

<h3>Step 3: Get Recommendations</h3>
<pre style="background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px;">python llmfit.py --recommend --format table</pre>

<h2>Popular Models by Hardware</h2>
<h3>For Most Laptops (8-16GB RAM)</h3>
<ul>
<li><strong>Llama 3 8B:</strong> Meta's latest, excellent reasoning</li>
<li><strong>Mistral 7B:</strong> Fast, efficient, great for coding</li>
<li><strong>Gemma 2 9B:</strong> Google's model, very capable</li>
<li><strong>Phi-3 Mini:</strong> Microsoft's compact powerhouse</li>
</ul>

<h3>For Gaming PCs (16-32GB RAM, 8GB+ VRAM)</h3>
<ul>
<li><strong>Llama 3 70B (Q4):</strong> Nearly GPT-4 quality</li>
<li><strong>Qwen 2.5 32B:</strong> Best coding model</li>
<li><strong>Mixtral 8x7B:</strong> MoE architecture, very efficient</li>
</ul>

<h2>Performance Optimization Tips</h2>
<ol>
<li><strong>Use GPU layers:</strong> Offload as many layers as possible to GPU</li>
<li><strong>Reduce context length:</strong> 4096 → 2048 tokens saves significant memory</li>
<li><strong>Enable CPU offloading:</strong> For very large models</li>
<li><strong>Close background apps:</strong> Free up RAM before loading models</li>
</ol>

<h2>Troubleshooting Common Issues</h2>
<p><strong>"CUDA out of memory":</strong> Use a more quantized version (Q4 instead of Q8) or reduce context length.</p>
<p><strong>Slow generation:</strong> Ensure GPU acceleration is enabled. Check that layers are being offloaded to GPU.</p>
<p><strong>Model won't load:</strong> Check available RAM. Close other applications. Consider using a smaller model.</p>

<h2>Conclusion</h2>
<p>Don't waste time downloading models that won't work. LLMfit takes the guesswork out of local AI setup. Whether you have a basic laptop or a high-end workstation, there's an AI model that will run great on your hardware.</p>

<h3>Related Resources</h3>
<ul>
<li><a href="https://huggingface.co/models">Hugging Face Model Hub</a> — Thousands of free AI models</li>
<li><a href="https://github.com/ggerganov/llama.cpp">llama.cpp</a> — Fast LLM inference engine</li>
<li><a href="https://ollama.ai">Ollama</a> — Easiest way to run local LLMs</li>
</ul>
""")

# Post 02: Claude Office
p = get_post("02-claude-office")
posts_content["02-claude-office"] = wrap(p['title'], p['date'], p['category'], embed(p['youtubeId'], p['title']), """
<h2>The Game-Changer: Claude Cowork</h2>
<p>Anthropic just dropped <strong>Claude Cowork</strong> and it's going to change how we use Microsoft Office forever. Imagine having an AI assistant that can actually <em>see</em> your spreadsheets, analyze your data, and help you build presentations.</p>

<h2>What Makes Claude Cowork Different</h2>
<ul>
<li><strong>Reads your documents:</strong> It can see your Excel data, PowerPoint slides, and Word documents</li>
<li><strong>Understands context:</strong> It knows what you're working on without you explaining everything</li>
<li><strong>Acts on your behalf:</strong> Create formulas, generate charts, suggest slide layouts</li>
<li><strong>Remembers:</strong> It maintains context across your entire workflow</li>
</ul>

<h2>Excel Integration Deep Dive</h2>

<h3>Natural Language Data Analysis</h3>
<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p><strong>You:</strong> "What's the average sales for Q3 in the West region?"</p>
<p><strong>Claude:</strong> "The average sales for Q3 in the West region is $47,320. This represents a 15% increase over Q2 ($41,180)."</p>
</div>

<h3>Formula Generation</h3>
<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p><strong>You:</strong> "Create a formula that calculates commission: 5% for sales under $10k, 7% for $10k-$50k, and 10% for over $50k"</p>
<pre style="background: #fff; padding: 10px;">=IF(B2<10000, B2*0.05, IF(B2<=50000, B2*0.07, B2*0.1))</pre>
</div>

<h2>PowerPoint Integration</h2>

<h3>Slide Generation</h3>
<p>Turn a Word document or data summary into a presentation:</p>
<ol>
<li>Title: Q1 2026 Performance Overview</li>
<li>Key Metrics: Revenue, Growth, Customer Acquisition</li>
<li>Challenges Faced & Solutions</li>
<li>Looking Ahead: Q2 Goals & Strategy</li>
<li>Thank You & Questions</li>
</ol>

<h3>Design Suggestions</h3>
<ul>
<li>"This slide has too much text — suggest a better layout"</li>
<li>"What chart type works best for comparing quarterly performance?"</li>
<li>"Suggest a color scheme that matches our brand"</li>
</ul>

<h2>Real-World Use Cases</h2>

<h3>For Financial Analysts</h3>
<ul>
<li>Analyze quarterly earnings data across multiple spreadsheets</li>
<li>Create executive summaries with key metrics highlighted</li>
<li>Build financial models with AI-assisted formulas</li>
</ul>

<h3>For Marketing Teams</h3>
<ul>
<li>Generate campaign performance reports</li>
<li>Create presentation decks from campaign data</li>
<li>Compare metrics across different channels</li>
</ul>

<h3>For Students</h3>
<ul>
<li>Analyze research data for projects</li>
<li>Create presentation slides from papers</li>
<li>Get help with statistics and formulas</li>
</ul>

<h2>How to Set Up Claude Cowork</h2>

<h3>Step 1: Download Claude Desktop</h3>
<ol>
<li>Go to claude.ai/download</li>
<li>Download for Windows or macOS</li>
<li>Install and sign in</li>
</ol>

<h3>Step 2: Enable Office Integration</h3>
<ol>
<li>Open Claude Desktop</li>
<li>Go to Settings → Extensions</li>
<li>Toggle "Microsoft Office" to ON</li>
<li>Grant permissions when prompted</li>
</ol>

<h3>Step 3: Start Using</h3>
<ol>
<li>Open Excel or PowerPoint</li>
<li>Press Ctrl+Shift+C (default shortcut)</li>
<li>Start chatting with Claude about your document</li>
</ol>

<h2>Privacy & Security</h2>

<p>Anthropic has implemented several safeguards:</p>
<ul>
<li><strong>Local processing:</strong> Document analysis happens on your machine</li>
<li><strong>No cloud storage:</strong> Your files aren't uploaded to Anthropic's servers</li>
<li><strong>Opt-in only:</strong> Integration is disabled by default</li>
</ul>

<h2>The Future of Office Work</h2>

<p>Claude Cowork represents a fundamental shift in how we interact with productivity software. Instead of learning complex formulas or spending hours on data analysis, you can simply <em>ask</em> for what you need.</p>

<p>The AI that actually does things isn't coming — it's here.</p>
""")

# Generate files
for post_id, content in posts_content.items():
    filepath = OUTPUT_DIR / f"{post_id}.html"
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ Generated: {post_id}.html")

print(f"\n📁 All posts saved to: {OUTPUT_DIR}")
print(f"\nNext: Run update-blogger-full.py to update Blogger posts")

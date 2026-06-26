#!/usr/bin/env python3
"""
Generate proper blog posts by understanding transcripts (not inserting them)
Uses oracle CLI to process content
"""

import json
import subprocess
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

OUTPUT_DIR = Path.home() / ".openclaw/workspace/techrex-website/content/blog/blogger-html-full"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POSTS_JSON = Path.home() / ".openclaw/workspace/techrex-website/content/blog/posts.json"
with open(POSTS_JSON) as f:
    POSTS_DATA = json.load(f)['blogPosts']

YT_API = YouTubeTranscriptApi()

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

def wrap(title, date, category, embed_code, body, tags):
    tags_html = ', '.join([f'#{t}' for t in tags])
    return f'''<div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto;">

<h1 style="color: #27ae60;">{title}</h1>

<p style="font-size: 18px; color: #666;"><strong>Category:</strong> {category} | <strong>Published:</strong> {date}</p>

{embed_code}

{body}

<p><strong>Tags:</strong> {tags_html}</p>

<div style="background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 20px; border-radius: 12px; margin-top: 30px;">
<h3 style="margin: 0 0 10px 0;">🦖 Evolve or Get Extinct</h3>
<p style="margin: 0;">Learn, Build, Launch — Without The Struggle. Subscribe for more AI tutorials!</p>
<a href="https://www.youtube.com/@The_TechRex?sub_confirmation=1" style="display: inline-block; background: #ff0000; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin-top: 15px; font-weight: bold;">Subscribe on YouTube →</a>
</div>

</div>'''

def get_transcript(video_id):
    try:
        transcript = YT_API.fetch(video_id)
        return ' '.join([item.text for item in transcript])
    except Exception as e:
        print(f"  Error: {e}")
        return None

def generate_blog_with_oracle(post, transcript):
    """Use oracle CLI to generate blog from transcript understanding"""
    
    is_tutorial = any(word in post['title'].lower() for word in ['how to', 'install', 'setup', 'guide', 'tutorial', 'use'])
    
    if is_tutorial:
        prompt = f"""You are a tech blogger writing for TechRex. Based on the following YouTube video transcript, write a comprehensive tutorial blog post.

Video Title: {post['title']}
Category: {post['category']}
Video Transcript: {transcript[:4000]}

Write a detailed tutorial blog post that includes:
1. An engaging introduction explaining what this tutorial covers and why it matters
2. Prerequisites (what the reader needs before starting)
3. Step-by-step instructions based on what the video teaches
4. Common issues and troubleshooting tips mentioned
5. Real-world use cases
6. A conclusion with key takeaways

Format the output in HTML with proper h2, h3, p, ul/ol, and pre tags for code blocks.
Write in a friendly, helpful tone. Do NOT copy the transcript verbatim - instead, explain the concepts and steps in your own words based on your understanding of the content.
Make it around 800-1200 words."""
    else:
        prompt = f"""You are a tech blogger writing for TechRex. Based on the following YouTube video transcript, write an informative blog post.

Video Title: {post['title']}
Category: {post['category']}
Video Transcript: {transcript[:4000]}

Write a detailed informational blog post that includes:
1. An engaging introduction explaining the topic
2. Key facts and concepts explained clearly
3. Context and background information
4. Practical implications and why this matters
5. Key takeaways
6. Related topics or resources

Format the output in HTML with proper h2, h3, p, ul/ol tags.
Write in an engaging, informative tone. Do NOT copy the transcript verbatim - instead, explain the concepts in your own words based on your understanding of the content.
Make it around 800-1200 words."""
    
    # Use oracle CLI
    try:
        result = subprocess.run(
            ['oracle', '-q', prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout
    except Exception as e:
        print(f"  Oracle error: {e}")
        return None

def main():
    print("🦖 Generating blogs from transcript understanding...\n")
    
    success = 0
    failed = 0
    
    for i, post in enumerate(POSTS_DATA, 1):
        print(f"[{i}/19] {post['title'][:50]}...")
        
        # Get transcript
        transcript = get_transcript(post['youtubeId'])
        if not transcript:
            print("  ✗ No transcript")
            failed += 1
            continue
        
        # Generate blog using oracle
        blog_body = generate_blog_with_oracle(post, transcript)
        if not blog_body:
            print("  ✗ Failed to generate")
            failed += 1
            continue
        
        # Create full HTML
        html = wrap(
            post['title'],
            post['date'],
            post['category'],
            embed(post['youtubeId'], post['title']),
            blog_body,
            post['tags']
        )
        
        # Save
        filepath = OUTPUT_DIR / f"{post['id']}.html"
        with open(filepath, 'w') as f:
            f.write(html)
        
        print(f"  ✓ Generated ({len(blog_body)} chars)")
        success += 1
    
    print(f"\n{'='*60}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

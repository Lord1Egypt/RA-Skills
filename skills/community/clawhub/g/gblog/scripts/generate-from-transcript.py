#!/usr/bin/env python3
"""
Generate blog posts from YouTube transcripts
"""

import json
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
    """Get transcript for a YouTube video"""
    try:
        transcript = YT_API.fetch(video_id)
        full_text = ' '.join([item.text for item in transcript])
        return full_text
    except Exception as e:
        print(f"  Error: {e}")
        return None

def generate_blog_from_transcript(post, transcript):
    """Generate blog content based on transcript"""
    
    title = post['title']
    excerpt = post['excerpt']
    category = post['category']
    
    # Get first 2000 chars of transcript for summary
    transcript_summary = transcript[:2000] if len(transcript) > 2000 else transcript
    
    # Detect if this is a tutorial/installation video
    is_tutorial = any(word in title.lower() for word in ['how to', 'install', 'setup', 'guide', 'tutorial'])
    
    if is_tutorial:
        body = generate_tutorial_blog(post, transcript_summary)
    else:
        body = generate_info_blog(post, transcript_summary)
    
    return body

def generate_tutorial_blog(post, transcript_summary):
    """Generate tutorial-style blog"""
    return f"""
<h2>Introduction</h2>
<p>{post['excerpt']}</p>

<h2>What You'll Learn</h2>
<ul>
<li>Understand the core concepts and why they matter</li>
<li>Step-by-step installation and setup instructions</li>
<li>Practical use cases and real-world applications</li>
<li>Tips, tricks, and common pitfalls to avoid</li>
</ul>

<h2>Prerequisites</h2>
<p>Before starting, make sure you have:</p>
<ul>
<li>A computer with adequate specifications</li>
<li>Basic familiarity with the command line (helpful but not required)</li>
<li>An internet connection for downloading necessary files</li>
</ul>

<h2>Step-by-Step Guide</h2>

<h3>Step 1: Understanding the Problem</h3>
<p>Based on the video, the first step is understanding what we're trying to achieve. Here's what the video explains:</p>
<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[:500]}...</p>
</div>

<h3>Step 2: Installation</h3>
<p>Follow along with the video for the installation process. The key steps covered include:</p>
<ol>
<li>Download the necessary software/tools</li>
<li>Run the installer or setup script</li>
<li>Configure initial settings</li>
<li>Verify the installation worked</li>
</ol>

<h3>Step 3: Configuration</h3>
<p>Proper configuration is crucial for optimal performance:</p>
<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[500:1000]}...</p>
</div>

<h3>Step 4: Testing and Verification</h3>
<p>Always test your setup before using it for important tasks:</p>
<ul>
<li>Run a basic test to confirm everything works</li>
<li>Check for any error messages or warnings</li>
<li>Verify performance meets expectations</li>
</ul>

<h2>Common Use Cases</h2>
<p>Here are some practical ways to use what you've learned:</p>
<ul>
<li><strong>Personal Projects:</strong> Apply this to your own work and hobbies</li>
<li><strong>Professional Work:</strong> Use it to improve productivity and efficiency</li>
<li><strong>Learning:</strong> Deepen your understanding of related technologies</li>
</ul>

<h2>Troubleshooting</h2>
<p>If you run into issues, here are common solutions from the video:</p>
<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[1000:1500]}...</p>
</div>

<h2>Advanced Tips</h2>
<p>Once you have the basics working, consider these optimizations:</p>
<ul>
<li>Fine-tune settings for your specific use case</li>
<li>Integrate with other tools in your workflow</li>
<li>Automate repetitive tasks</li>
<li>Monitor performance and adjust as needed</li>
</ul>

<h2>Conclusion</h2>
<p>You've now learned how to set up and use this technology. Remember:</p>
<ul>
<li>Start with the basics and build up gradually</li>
<li>Practice regularly to build confidence</li>
<li>Stay updated with new features and improvements</li>
</ul>

<h2>Watch the Full Video</h2>
<p>For the complete visual walkthrough with all details, watch the video embedded above. The video includes demonstrations that complement this written guide.</p>

<h2>Additional Resources</h2>
<ul>
<li>Check the video description for links to tools and resources mentioned</li>
<li>Subscribe to TechRex for more tutorials like this</li>
<li>Leave questions in the comments — we read and respond to all of them</li>
</ul>
"""

def generate_info_blog(post, transcript_summary):
    """Generate informational/fact-based blog"""
    return f"""
<h2>Introduction</h2>
<p>{post['excerpt']}</p>

<h2>Key Facts and Concepts</h2>
<p>In this video, we explore important information about {post['category']}. Here are the main points:</p>

<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[:800]}...</p>
</div>

<h2>Understanding the Context</h2>
<p>To fully appreciate this topic, it's important to understand:</p>
<ul>
<li>The historical background and why this matters now</li>
<li>How this impacts current technology and practices</li>
<li>What the future might hold based on these developments</li>
</ul>

<h2>Detailed Explanation</h2>
<p>Here's a deeper dive into the concepts discussed:</p>

<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[800:1600]}...</p>
</div>

<h2>Practical Implications</h2>
<p>What does this mean for you? Here are the practical takeaways:</p>
<ul>
<li>How this affects your current tools and workflows</li>
<li>What changes you might need to make</li>
<li>Opportunities this creates</li>
</ul>

<h2>Expert Insights</h2>
<p>The video shares expert perspectives on this topic:</p>

<div style="background: #f5f5f5; padding: 20px; border-left: 4px solid #27ae60; margin: 20px 0;">
<p>{transcript_summary[1600:]}...</p>
</div>

<h2>Key Takeaways</h2>
<ul>
<li>Understanding the fundamentals is crucial for making informed decisions</li>
<li>This technology/topic is evolving rapidly — staying updated is important</li>
<li>The implications extend beyond just technical aspects to practical applications</li>
<li>Consider how this fits into your broader strategy or interests</li>
</ul>

<h2>Why This Matters</h2>
<p>The significance of this topic goes beyond just technical knowledge:</p>
<ul>
<li><strong>Impact on Industry:</strong> How this shapes the broader landscape</li>
<li><strong>Personal Relevance:</strong> Why you should care about this development</li>
<li><strong>Future Outlook:</strong> What to expect going forward</li>
</ul>

<h2>Watch the Full Video</h2>
<p>For the complete discussion with all details and visual explanations, watch the video embedded above.</p>

<h2>Related Topics</h2>
<p>If you found this interesting, you might also want to explore:</p>
<ul>
<li>Other videos in our {post['category']} series</li>
<li>Related technologies and concepts</li>
<li>Deeper dives into specific aspects mentioned</li>
</ul>

<h2>Conclusion</h2>
<p>Staying informed about developments in {post['category']} helps you make better decisions and stay ahead of the curve. Subscribe to TechRex for more insights like this.</p>
"""

def main():
    print("🦖 Generating blog posts from YouTube transcripts...\n")
    
    success_count = 0
    fail_count = 0
    
    for post in POSTS_DATA:
        print(f"Processing: {post['title'][:50]}...")
        
        # Get transcript
        transcript = get_transcript(post['youtubeId'])
        
        if transcript:
            # Generate blog content
            body = generate_blog_from_transcript(post, transcript)
            
            # Create full HTML
            html = wrap(
                post['title'],
                post['date'],
                post['category'],
                embed(post['youtubeId'], post['title']),
                body,
                post['tags']
            )
            
            # Save
            filepath = OUTPUT_DIR / f"{post['id']}.html"
            with open(filepath, 'w') as f:
                f.write(html)
            print(f"  ✓ Saved ({len(transcript)} chars transcript)")
            success_count += 1
        else:
            print(f"  ✗ Failed to get transcript")
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"{'='*60}")
    print(f"\n📁 Posts saved to: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()

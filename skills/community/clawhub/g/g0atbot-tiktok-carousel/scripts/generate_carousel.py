#!/usr/bin/env python3
"""
TikTok Carousel Generator
Generates viral 6-slide carousels using the proven formula
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Config
DATA_DIR = Path("/Users/g0atface/clawd/skills/tiktok-carousel/data")
CAROUSELS_FILE = DATA_DIR / "carousels.json"
METRICS_FILE = DATA_DIR / "metrics.json"
PROMPTS_FILE = DATA_DIR / "prompts.json"

DATA_DIR.mkdir(exist_ok=True)

# Initialize OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Prompt templates
PROMPT_TEMPLATES = {
    "fitness": {
        "scene": "Kitchen counter, iphone photo, realistic lighting, warm ambient light from window, 45 degree angle, granite countertop, white subway tile backsplash",
        "hooks": [
            "my trainer asked me to log everything i eat for a week. she wasn't ready for what came next",
            "showed my girlfriend how many calories are in her 'healthy' smoothie. she hasn't spoken to me since",
            "my doctor told me to track my food for 30 days. here's what happened by day 12",
        ]
    },
    "finance": {
        "scene": "Home office desk, iphone photo, realistic lighting, natural light from window, overhead can lighting, mahogany desk, laptop in background",
        "hooks": [
            "my accountant looked at my spending for one month. he went silent",
            "showed my wife our joint expenses for january. we didn't speak for 3 days",
            "my bank sent me a notification about my spending habits. it was embarrassing",
        ]
    },
    "productivity": {
        "scene": "Minimalist desk setup, iphone photo, realistic lighting, ring light from above, clean white surface, airpods case, coffee cup",
        "hooks": [
            "my boss asked me about my productivity system. i showed him and he hired 3 more people",
            "my therapist recommended i try time blocking. here's what changed in 2 weeks",
            "i used to drown in notifications. now i complete deep work sessions daily",
        ]
    },
    "dating": {
        "scene": "Cozy bedroom with string lights, iphone photo, realistic warm lighting, 35mm film aesthetic, messy but aesthetic bed sheets",
        "hooks": [
            "showed my hinge date my screen time statistics. she never texted back",
            "my dating coach asked me to track every interaction. here's the breakdown",
            "matched with someone on bumble. showed her my notification summary. unmatched immediately",
        ]
    }
}

def generate_hook(niche, custom_hook=None):
    """Generate or use custom hook"""
    if custom_hook:
        return custom_hook
    
    if niche in PROMPT_TEMPLATES:
        hooks = PROMPT_TEMPLATES[niche]["hooks"]
        return hooks[datetime.now().second % len(hooks)]
    
    # Generic hook
    hooks = [
        "my {profession} asked me to try this for 30 days. here's what happened",
        "showed my {partner} the data. they couldn't believe it",
        "i tracked everything for a week. the results shocked everyone",
    ]
    return hooks[datetime.now().second % len(hooks)]

def generate_image_prompt(niche, slide_num, hook, product):
    """Generate image prompt for a specific slide"""
    
    scene = PROMPT_TEMPLATES.get(niche, PROMPT_TEMPLATES["fitness"])["scene"]
    
    slide_prompts = {
        1: f"iPhone photo, person looking shocked at phone screen, {scene}, realistic lighting, candid moment, slight camera shake, natural expression, surprised reaction",
        2: f"Messy kitchen counter with takeout containers and snack wrappers scattered around, {scene}, realistic lighting, cluttered but believable, iphone photo quality",
        3: f"Person's hand scanning food with smartphone camera, close up on phone screen showing food recognition, {scene}, realistic indoor lighting, focused composition",
        4: f"Clean organized meal prep containers lined up on counter, calories visible on containers, {scene}, realistic lighting, neat and organized, aesthetic food presentation",
        5: f"Weekly progress chart or graph on tablet screen showing improvement, person smiling at results, {scene}, realistic lighting, celebratory mood, iphone photo style",
        6: f"Happy person holding phone showing the app/dashboard, confident expression, {scene}, realistic lighting, satisfied customer, natural smile, iphone photography"
    }
    
    return slide_prompts.get(slide_num, scene)

def generate_carousel(niche, product, custom_hook=None, num_slides=6):
    """Generate a complete carousel"""
    
    print(f"🎠 Generating TikTok carousel...")
    print(f"   Niche: {niche}")
    print(f"   Product: {product}")
    
    # Get hook
    hook = generate_hook(niche, custom_hook)
    print(f"   Hook: {hook[:60]}...")
    
    # Generate prompts for each slide
    carousel = {
        "id": f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "niche": niche,
        "product": product,
        "hook": hook,
        "slides": []
    }
    
    for slide_num in range(1, num_slides + 1):
        prompt = generate_image_prompt(niche, slide_num, hook, product)
        
        slide = {
            "slide_num": slide_num,
            "prompt": prompt,
            "status": "pending"
        }
        carousel["slides"].append(slide)
        
        print(f"   Slide {slide_num}: {prompt[:60]}...")
    
    # Save carousel
    carousels = []
    if CAROUSELS_FILE.exists():
        carousels = json.loads(CAROUSELS_FILE.read_text())
    carousels.append(carousel)
    CAROUSELS_FILE.write_text(json.dumps(carousels, indent=2))
    
    print(f"✅ Carousel saved: {carousel['id']}")
    
    return carousel

def generate_images(carousel_id, model="dall-e-3"):
    """Generate images using DALL-E"""
    
    carousels = json.loads(CAROUSELS_FILE.read_text())
    carousel = next((c for c in carousels if c["id"] == carousel_id), None)
    
    if not carousel:
        print(f"❌ Carousel not found: {carousel_id}")
        return
    
    print(f"🎨 Generating images for {carousel_id}...")
    
    for i, slide in enumerate(carousel["slides"]):
        if slide["status"] == "generated":
            continue
            
        print(f"   Slide {i+1}/6...")
        
        try:
            response = client.images.generate(
                model=model,
                prompt=slide["prompt"],
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            slide["image_url"] = response.data[0].url
            slide["status"] = "generated"
            
            # Save progress
            CAROUSELS_FILE.write_text(json.dumps(carousels, indent=2))
            
            print(f"   ✅ Generated: {response.data[0].url[:50]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            slide["status"] = "error"
            slide["error"] = str(e)
    
    print(f"🎉 Images generated for {carousel_id}")

def create_post_text(carousel):
    """Create TikTok post text from carousel"""
    hook = carousel["hook"]
    
    # Extract first person and conflict for hashtag strategy
    hashtags = f"\n\n#viral #fyp #trending #{carousel['niche']} #lifechange"
    
    post = f"{hook}\n\nSwipe for the transformation 👆{hashtags}"
    
    return post

def main():
    """Main CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TikTok Carousel Generator")
    parser.add_argument("--niche", "-n", default="fitness", help="Content niche (fitness, finance, productivity, dating)")
    parser.add_argument("--product", "-p", required=True, help="Product/app being promoted")
    parser.add_argument("--hook", "-H", help="Custom hook (optional)")
    parser.add_argument("--slides", "-s", type=int, default=6, help="Number of slides (default: 6)")
    parser.add_argument("--generate-images", "-g", help="Generate images for carousel ID")
    parser.add_argument("--list", "-l", action="store_true", help="List all carousels")
    
    args = parser.parse_args()
    
    if args.list:
        if CAROUSELS_FILE.exists():
            carousels = json.loads(CAROUSELS_FILE.read_text())
            for c in carousels[-10:]:
                print(f"  {c['id']} - {c['niche']} - {c['hook'][:50]}...")
        else:
            print("No carousels yet")
        return
    
    if args.generate_images:
        generate_images(args.generate_images)
        return
    
    # Generate new carousel
    carousel = generate_carousel(args.niche, args.product, args.hook, args.slides)
    
    print()
    print("📝 Post text:")
    print(create_post_text(carousel))
    
    print()
    print("💰 To generate images:")
    print(f"   python3 {sys.argv[0]} -g {carousel['id']}")

if __name__ == "__main__":
    main()

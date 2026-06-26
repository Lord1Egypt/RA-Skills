#!/usr/bin/env python3
"""
AI Fitness Recipe Channel - Main Orchestrator
==============================================
Ties together: fal.ai → ElevenLabs → Shotstack → TikTok

Usage:
    python3 run_pipeline.py              # Generate 1 video
    python3 run_pipeline.py --batch 10  # Generate 10 videos
"""

import argparse
import sys
import os
from pathlib import Path

# Add bot directory to path
BOT_DIR = Path.home() / "clawd/bots/fitness-recipes-ai"
sys.path.insert(0, str(BOT_DIR))

from fal_client import generate_food_image, FOOD_PROMPTS
from elevenlabs_client import generate_voiceover
from shotstack_client import assemble_video


# Recipe templates with macros
RECIPES = [
    {"name": "Protein Shake", "calories": 350, "protein": 40, "category": "smoothie"},
    {"name": "Chicken Meal Prep", "calories": 450, "protein": 45, "category": "mealprep"},
    {"name": "Avocado Toast", "calories": 380, "protein": 18, "category": "breakfast"},
    {"name": "Protein Pancakes", "calories": 420, "protein": 35, "category": "breakfast"},
    {"name": "Greek Yogurt Parfait", "calories": 280, "protein": 22, "category": "snack"},
    {"name": "Salmon Dinner", "calories": 480, "protein": 42, "category": "dinner"},
    {"name": "Quinoa Salad", "calories": 350, "protein": 15, "category": "lunch"},
    {"name": "Turkey Stir Fry", "calories": 400, "protein": 38, "category": "dinner"},
    {"name": "Overnight Oats", "calories": 320, "protein": 18, "category": "breakfast"},
    {"name": "Egg White Omelette", "calories": 250, "protein": 28, "category": "breakfast"},
]


def create_script(recipe: dict) -> str:
    """Create TTS script for a recipe."""
    return f"""
    Looking for a high protein meal that's actually delicious?
    
    This {recipe['name']} has only {recipe['calories']} calories but packs {recipe['protein']} grams of protein.
    
    It's perfect for {recipe['category']} and will keep you full for hours.
    
    Save this for your next meal prep!
    
    Your fitness goals just got easier to reach.
    """


def generate_one_video(recipe: dict, index: int = 0) -> dict:
    """Generate one complete video."""
    result = {
        "recipe": recipe["name"],
        "status": "pending",
        "paths": {}
    }
    
    output_dir = Path.home() / "clawd/bots/fitness-recipes-ai/output"
    (output_dir / "images").mkdir(parents=True, exist_ok=True)
    (output_dir / "audio").mkdir(parents=True, exist_ok=True)
    (output_dir / "videos").mkdir(parents=True, exist_ok=True)
    
    # Step 1: Generate food image
    prompt = FOOD_PROMPTS.get(recipe["category"], recipe["name"])
    image_path = str(output_dir / "images" / f"{recipe['name'].replace(' ', '_')}_{index}.jpg")
    result["paths"]["image"] = generate_food_image(prompt, image_path)
    
    # Step 2: Generate voiceover
    script = create_script(recipe)
    audio_path = str(output_dir / "audio" / f"{recipe['name'].replace(' ', '_')}_{index}.mp3")
    result["paths"]["audio"] = generate_voiceover(script, output_path=audio_path)
    
    # Step 3: Assemble video
    video_path = str(output_dir / "videos" / f"{recipe['name'].replace(' ', '_')}_{index}.mp4")
    result["paths"]["video"] = assemble_video(
        result["paths"]["image"],
        result["paths"]["audio"],
        recipe["name"]
    )
    
    result["status"] = "complete" if result["paths"]["video"] else "failed"
    
    return result


def generate_batch(count: int = 10) -> list:
    """Generate a batch of videos."""
    results = []
    
    for i in range(count):
        recipe = RECIPES[i % len(RECIPES)]
        print(f"\n{'='*50}")
        print(f"🎬 Video {i+1}/{count}: {recipe['name']}")
        print(f"{'='*50}")
        
        result = generate_one_video(recipe, i)
        results.append(result)
        
        status = "✅" if result["status"] == "complete" else "❌"
        print(f"{status} {recipe['name']}: {result['status']}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="AI Fitness Recipe Video Generator")
    parser.add_argument("--batch", type=int, default=1, help="Number of videos to generate")
    parser.add_argument("--test", action="store_true", help="Use placeholder images/audio")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🏋️ AI FITNESS RECIPE CHANNEL - VIDEO GENERATOR")
    print("="*60)
    print(f"📦 Batch size: {args.batch}")
    print("="*60 + "\n")
    
    results = generate_batch(args.batch)
    
    # Summary
    complete = sum(1 for r in results if r["status"] == "complete")
    print(f"\n{'='*60}")
    print(f"✅ Complete: {complete}/{len(results)}")
    print(f"❌ Failed: {len(results) - complete}/{len(results)}")
    print("="*60)
    
    # Print video paths
    for r in results:
        if r["status"] == "complete":
            print(f"📹 {r['recipe']}: {r['paths']['video']}")


if __name__ == "__main__":
    main()

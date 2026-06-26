#!/usr/bin/env python3
"""
Fitness Recipe Automation - Daily Cron Job
=====================================
Runs at 8 AM daily to generate 10 fitness recipe videos.

Add to cron:
0 8 * * * cd /root/clawd/bots/fitness-recipes-ai && source venv/bin/activate && python3 daily_batch.py
"""

import sys
import os
from pathlib import Path

# Add to path
BOT_DIR = Path.home() / "clawd/bots/fitness-recipes-ai"
sys.path.insert(0, str(BOT_DIR))

from run_pipeline import generate_batch

# Daily configuration
VIDEOS_PER_DAY = 10


def main():
    """Generate daily batch of fitness recipe videos."""
    print("="*60)
    print("🏋️ DAILY FITNESS RECIPE GENERATION")
    print("="*60)
    print(f"📅 Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}")
    print(f"🎬 Videos: {VIDEOS_PER_DAY}")
    print("="*60)
    
    # Generate batch
    videos = generate_batch(VIDEOS_PER_DAY)
    
    print("\n" + "="*60)
    print(f"✅ Generated {len(videos)} videos")
    print(f"📁 Output: {BOT_DIR}/output/videos/")
    print("="*60)
    
    # Return count for monitoring
    return len(videos)


if __name__ == "__main__":
    main()

"""
Daily Geopolitical TikTok Reporter - Main Script
Generates daily TikTok scripts about geopolitical news
"""

import sys
import os
from datetime import datetime

# Add skill modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_gathering.fetch_news import GeoNewsGatherer
from content_gen.tiktok_generator import TikTokGeoScriptGenerator
import json

def generate_daily_geopolitical_tiktok(
    hours_back: int = 24,
    num_scripts: int = 3,
    region_filter: str = None,
    topic_filter: str = None
):
    """Generate daily geopolitical TikTok scripts
    
    Args:
        hours_back: How many hours back to gather news
        num_scripts: Number of individual scripts to generate
        region_filter: Filter by geographic region (optional)
        topic_filter: Filter by topic category (optional)
    """
    
    print("🌍 Daily Geopolitical TikTok Reporter")
    print(f"⏰ Gathering news from last {hours_back} hours...")
    print(f"�Filtering: Region={region_filter}, Topic={topic_filter}")
    print("-" * 50)
    
    # Step 1: Gather news
    gatherer = GeoNewsGatherer(hours_back=hours_back)
    articles = gatherer.fetch_all_sources()
    
    print(f"📰 Found {len(articles)} geopolitical articles")
    
    if len(articles) == 0:
        print("❌ No geopolitical news found in the specified time period")
        return None
    
    # Apply filters if specified
    if region_filter:
        articles = gatherer.filter_by_region(region_filter)
        print(f"🔍 Filtered to {len(articles)} articles in region: {region_filter}")
    
    if topic_filter:
        articles = gatherer.filter_by_topic(topic_filter)
        print(f"🔍 Filtered to {len(articles)} articles on topic: {topic_filter}")
    
    if len(articles) == 0:
        print("❌ No articles match the specified filters")
        return None
    
    # Get top stories
    top_stories = gatherer.get_top_stories(num_scripts)
    
    print(f"🔥 Selected top {len(top_stories)} stories:")
    for i, story in enumerate(top_stories, 1):
        print(f"   {i}. {story['title'][:60]}...")
        print(f"      Importance: {story['importance_score']}/10")
    
    # Step 2: Generate TikTok scripts
    print("\n🎬 Generating TikTok scripts...")
    generator = TikTokGeoScriptGenerator()
    
    # Generate individual story scripts
    scripts = []
    for i, story in enumerate(top_stories, 1):
        print(f"\n📝 Script {i}: {story['title'][:50]}...")
        script = generator.generate_single_story_script(story)
        scripts.append(script)
        print(f"   ⏱️ Duration: ~{script['estimated_duration']} seconds")
        print(f"   🏷️ Hashtags: {', '.join(script['hashtags'][:4])}...")
    
    # Generate daily report script
    print(f"\n📊 Generating daily report script...")
    daily_report = generator.generate_daily_report_script(top_stories)
    
    if daily_report:
        scripts.append(daily_report)
        print(f"   📋 Daily report covering {daily_report['stories_count']} stories")
    
    # Step 3: Save scripts
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_dir = f"generated_scripts_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n💾 Saving scripts to {output_dir}/...")
    
    for i, script in enumerate(scripts, 1):
        script_type = script.get('type', 'single_story')
        script_title = script.get('title', f'script_{i}')
        script_title = ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in script_title)
        
        # Save individual script
        filename = f"{output_dir}/{i}_{script_title}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script['full_script'])
        
        print(f"   ✅ {filename}")
    
    # Save metadata JSON
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'total_scripts': len(scripts),
        'articles_analyzed': len(articles),
        'time_period_hours': hours_back,
        'filters': {
            'region': region_filter,
            'topic': topic_filter
        },
        'scripts': [
            {
                'type': script.get('type', 'single_story'),
                'title': script.get('title', 'N/A'),
                'duration': script.get('estimated_duration', 'N/A'),
                'hashtags': script.get('hashtags', [])
            }
            for script in scripts
        ]
    }
    
    metadata_file = f"{output_dir}/metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"   ✅ {metadata_file}")
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 SUCCESS! Generated TikTok scripts")
    print("=" * 50)
    print(f"📝 Total scripts: {len(scripts)}")
    print(f"📰 Articles analyzed: {len(articles)}")
    print(f"📁 Output directory: {output_dir}/")
    print("\n📖 Next steps:")
    print("1. Review the generated scripts in the output directory")
    print("2. Customize scripts as needed (add personal style, adjustments)")
    print("3. Use TikTok's text-to-speech or record voiceover")
    print("4. Add visuals (stock footage, news clips, maps)")
    print("5. Post during peak hours for maximum engagement")
    print("\n💡 Pro tip: Schedule this script to run daily for consistent content!")
    
    return {
        'scripts': scripts,
        'metadata': metadata,
        'output_dir': output_dir
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate daily geopolitical TikTok scripts')
    parser.add_argument('--hours', type=int, default=24, 
                       help='Hours back to gather news (default: 24)')
    parser.add_argument('--scripts', type=int, default=3,
                       help='Number of scripts to generate (default: 3)')
    parser.add_argument('--region', type=str, default=None,
                       help='Filter by geographic region (e.g., middle_east, europe, asia)')
    parser.add_argument('--topic', type=str, default=None,
                       help='Filter by topic (e.g., conflicts, diplomacy, elections)')
    
    args = parser.parse_args()
    
    result = generate_daily_geopolitical_tiktok(
        hours_back=args.hours,
        num_scripts=args.scripts,
        region_filter=args.region,
        topic_filter=args.topic
    )
    
    if not result:
        sys.exit(1)
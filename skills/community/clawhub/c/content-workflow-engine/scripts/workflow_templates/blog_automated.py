#!/usr/bin/env python3
"""
Automated Blog Pipeline Template

This template creates a complete blog content pipeline that:
1. Generates ideas based on topics
2. Creates outlines
3. Writes full articles
4. Optimizes for SEO
5. Publishes to WordPress
6. Distributes on social media
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

def create_blog_pipeline(name, topic, frequency, output_dir="workflows"):
    """Create an automated blog pipeline workflow."""
    
    # Calculate schedule based on frequency
    schedule = calculate_schedule(frequency)
    
    workflow = {
        "name": f"Automated Blog: {name}",
        "id": f"blog_{name.lower().replace(' ', '_')}",
        "type": "blog",
        "description": f"Automated blog content pipeline for {topic}",
        "topic": topic,
        "frequency": frequency,
        "created": datetime.now().isoformat(),
        "enabled": True,
        "version": "1.0",
        
        "schedule": schedule,
        
        "stages": [
            {
                "name": "ideation",
                "tool": "ai-brainstorm",
                "config": {
                    "topic": topic,
                    "count": 5,
                    "content_type": "blog",
                    "difficulty_filter": "medium"
                },
                "schedule": "weekly",
                "output_to": ["outline"]
            },
            {
                "name": "outline",
                "tool": "ai-outliner",
                "config": {
                    "depth": 3,
                    "include_examples": True,
                    "target_word_count": 1500,
                    "sections": ["introduction", "problem", "solution", "examples", "conclusion"]
                },
                "depends_on": ["ideation"],
                "output_to": ["writing"]
            },
            {
                "name": "writing",
                "tool": "ai-writer",
                "config": {
                    "tone": "professional",
                    "reading_level": "grade_10",
                    "include_statistics": True,
                    "citation_style": "APA"
                },
                "depends_on": ["outline"],
                "output_to": ["editing"]
            },
            {
                "name": "editing",
                "tool": "grammar-check",
                "config": {
                    "check_grammar": True,
                    "check_spelling": True,
                    "suggest_improvements": True
                },
                "depends_on": ["writing"],
                "output_to": ["seo"]
            },
            {
                "name": "seo",
                "tool": "seo-optimizer",
                "config": {
                    "target_score": 85,
                    "keyword_density": "1.5-2.5%",
                    "add_meta_tags": True,
                    "internal_links": 3,
                    "external_links": 2
                },
                "depends_on": ["editing"],
                "output_to": ["visuals"]
            },
            {
                "name": "visuals",
                "tool": "image-generator",
                "config": {
                    "style": "modern_flat",
                    "sizes": ["1200x630", "800x400"],
                    "brand_colors": True
                },
                "depends_on": ["seo"],
                "output_to": ["publishing"]
            },
            {
                "name": "publishing",
                "tool": "wordpress",
                "config": {
                    "status": "scheduled",
                    "categories": [topic],
                    "tags": ["automated", "ai", "content"],
                    "author": "Content Team"
                },
                "depends_on": ["visuals"],
                "output_to": ["distribution"]
            },
            {
                "name": "distribution",
                "tool": "social-media",
                "config": {
                    "platforms": ["twitter", "linkedin", "facebook"],
                    "schedule_stagger": "2_hours",
                    "variations": 3
                },
                "depends_on": ["publishing"],
                "output_to": ["analytics"]
            },
            {
                "name": "analytics",
                "tool": "analytics",
                "config": {
                    "tracking_period": "30_days",
                    "metrics": ["views", "engagement", "conversions"],
                    "report_frequency": "weekly"
                },
                "depends_on": ["distribution"]
            }
        ],
        
        "quality_checks": {
            "minimum_word_count": 1000,
            "maximum_word_count": 2500,
            "readability_score": 60,
            "seo_score": 80,
            "grammar_score": 95
        },
        
        "notifications": {
            "on_success": ["slack", "email"],
            "on_failure": ["slack", "email", "sms"],
            "on_publish": ["slack"]
        },
        
        "backup": {
            "content_backup": True,
            "image_backup": True,
            "backup_location": "./backups/",
            "retention_days": 30
        }
    }
    
    return workflow

def calculate_schedule(frequency):
    """Calculate publishing schedule based on frequency."""
    base_time = "09:00:00"
    
    if frequency == "daily":
        return {
            "cron": f"0 9 * * *",
            "human_readable": "Every day at 9:00 AM",
            "timezone": "America/New_York"
        }
    elif frequency == "weekly":
        return {
            "cron": f"0 9 * * 1",  # Every Monday at 9:00 AM
            "human_readable": "Every Monday at 9:00 AM",
            "timezone": "America/New_York"
        }
    elif frequency == "biweekly":
        return {
            "cron": f"0 9 1,15 * *",  # 1st and 15th of each month at 9:00 AM
            "human_readable": "1st and 15th of each month at 9:00 AM",
            "timezone": "America/New_York"
        }
    elif frequency == "monthly":
        return {
            "cron": f"0 9 1 * *",  # 1st of each month at 9:00 AM
            "human_readable": "1st of each month at 9:00 AM",
            "timezone": "America/New_York"
        }
    else:
        # Custom frequency
        return {
            "cron": "0 9 * * 1",  # Default to Monday
            "human_readable": "Every Monday at 9:00 AM",
            "timezone": "America/New_York"
        }

def save_workflow(workflow, output_dir):
    """Save workflow to file."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    workflow_file = output_path / f"{workflow['id']}.json"
    
    with open(workflow_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    return workflow_file

def main():
    parser = argparse.ArgumentParser(description="Create automated blog pipeline")
    parser.add_argument("--name", required=True, help="Name for the blog pipeline")
    parser.add_argument("--topic", required=True, help="Main topic for blog content")
    parser.add_argument("--frequency", choices=["daily", "weekly", "biweekly", "monthly"],
                       default="weekly", help="Publishing frequency")
    parser.add_argument("--output", default="workflows", help="Output directory")
    parser.add_argument("--test", action="store_true", help="Test the workflow after creation")
    
    args = parser.parse_args()
    
    print(f"📝 Creating automated blog pipeline...")
    print(f"   Name: {args.name}")
    print(f"   Topic: {args.topic}")
    print(f"   Frequency: {args.frequency}")
    
    try:
        # Create workflow
        workflow = create_blog_pipeline(args.name, args.topic, args.frequency)
        
        # Save workflow
        workflow_file = save_workflow(workflow, args.output)
        
        print(f"✅ Created workflow: {workflow['name']}")
        print(f"   ID: {workflow['id']}")
        print(f"   Stages: {len(workflow['stages'])}")
        print(f"   Schedule: {workflow['schedule']['human_readable']}")
        print(f"   File: {workflow_file}")
        
        # Print workflow summary
        print(f"\n📋 Workflow Summary:")
        print(f"{'='*50}")
        for i, stage in enumerate(workflow['stages'], 1):
            depends = ', '.join(stage.get('depends_on', ['none']))
            print(f"{i:2}. {stage['name']:12} → {stage['tool']:20} (depends: {depends})")
        
        print(f"\n🎯 Quality Checks:")
        for check, value in workflow['quality_checks'].items():
            print(f"   {check}: {value}")
        
        print(f"\n🔔 Notifications:")
        for event, channels in workflow['notifications'].items():
            print(f"   {event}: {', '.join(channels)}")
        
        # Test if requested
        if args.test:
            print(f"\n🧪 Testing workflow...")
            test_workflow(workflow_file)
        
        print(f"\n🚀 Next steps:")
        print(f"1. Configure API keys in api_config.json")
        print(f"2. Test workflow: python3 run_workflow.py --workflow {workflow['id']}")
        print(f"3. Schedule with cron: {workflow['schedule']['cron']}")
        print(f"4. Monitor logs: tail -f logs/{workflow['id']}.log")
        
    except Exception as e:
        print(f"❌ Error creating workflow: {e}", file=sys.stderr)
        sys.exit(1)

def test_workflow(workflow_file):
    """Test the workflow by running it with test data."""
    try:
        # Import the run_workflow module
        import subprocess
        
        print(f"   Running test execution...")
        
        # Create test input
        test_input = {
            "topic": "content automation",
            "test_mode": True,
            "generate_count": 1
        }
        
        # Save test input
        test_file = Path("test_input.json")
        with open(test_file, 'w') as f:
            json.dump(test_input, f, indent=2)
        
        # Run workflow
        result = subprocess.run([
            "python3", "run_workflow.py",
            "--workflow", str(workflow_file),
            "--input-file", "test_input.json",
            "--continue-on-error"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Test completed successfully")
            print(f"   Output: {result.stdout[-500:]}")  # Last 500 chars
        else:
            print(f"   ⚠️  Test completed with errors")
            print(f"   Error: {result.stderr[:500]}")
        
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

if __name__ == "__main__":
    main()
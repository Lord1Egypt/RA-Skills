#!/usr/bin/env python3
"""
Create a new content workflow definition.

This script creates a workflow configuration file that defines
the stages, tools, and connections for a content pipeline.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Default workflow templates
WORKFLOW_TEMPLATES = {
    "blog": {
        "name": "Blog Content Pipeline",
        "description": "Automated blog post creation and publishing",
        "stages": [
            {"name": "ideation", "tool": "ai-brainstorm", "config": {"count": 5}},
            {"name": "outline", "tool": "ai-outliner", "config": {"depth": 3}},
            {"name": "writing", "tool": "ai-writer", "config": {"tone": "professional"}},
            {"name": "editing", "tool": "grammar-check", "config": {}},
            {"name": "seo", "tool": "seo-optimizer", "config": {"keywords": []}},
            {"name": "publishing", "tool": "wordpress", "config": {"status": "draft"}},
            {"name": "distribution", "tool": "social-media", "config": {"platforms": ["twitter", "linkedin"]}}
        ]
    },
    "social": {
        "name": "Social Media Pipeline",
        "description": "Batch creation and scheduling of social media content",
        "stages": [
            {"name": "planning", "tool": "content-calendar", "config": {"days": 7}},
            {"name": "creation", "tool": "ai-content", "config": {"formats": ["text", "image"]}},
            {"name": "scheduling", "tool": "social-scheduler", "config": {"platforms": ["twitter", "linkedin", "facebook"]}},
            {"name": "monitoring", "tool": "analytics", "config": {"metrics": ["engagement", "reach"]}}
        ]
    },
    "newsletter": {
        "name": "Newsletter Pipeline",
        "description": "Automated newsletter creation and distribution",
        "stages": [
            {"name": "collection", "tool": "content-aggregator", "config": {"sources": ["blog", "news"]}},
            {"name": "curation", "tool": "ai-curator", "config": {"max_items": 10}},
            {"name": "writing", "tool": "ai-writer", "config": {"tone": "conversational"}},
            {"name": "formatting", "tool": "template-filler", "config": {"template": "weekly_roundup"}},
            {"name": "sending", "tool": "email-service", "config": {"service": "mailchimp"}},
            {"name": "tracking", "tool": "email-analytics", "config": {"track_opens": True}}
        ]
    },
    "video": {
        "name": "Video Content Pipeline",
        "description": "Script-to-video creation workflow",
        "stages": [
            {"name": "scripting", "tool": "ai-scriptwriter", "config": {"format": "youtube"}},
            {"name": "voiceover", "tool": "tts", "config": {"voice": "professional"}},
            {"name": "editing", "tool": "video-editor", "config": {"template": "standard"}},
            {"name": "upload", "tool": "youtube-upload", "config": {"privacy": "unlisted"}},
            {"name": "optimization", "tool": "seo-optimizer", "config": {"platform": "youtube"}}
        ]
    }
}

def create_workflow(name, workflow_type, output_dir="workflows"):
    """Create a new workflow configuration."""
    
    # Get template or create empty workflow
    if workflow_type in WORKFLOW_TEMPLATES:
        workflow = WORKFLOW_TEMPLATES[workflow_type].copy()
        workflow["type"] = workflow_type
    else:
        workflow = {
            "name": name,
            "type": "custom",
            "description": f"Custom workflow: {name}",
            "stages": []
        }
    
    # Set workflow metadata
    workflow["id"] = name.lower().replace(" ", "-")
    workflow["created"] = datetime.now().isoformat()
    workflow["version"] = "1.0"
    workflow["enabled"] = True
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save workflow file
    workflow_file = output_path / f"{workflow['id']}.json"
    with open(workflow_file, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"✅ Created workflow: {workflow['name']}")
    print(f"   ID: {workflow['id']}")
    print(f"   Type: {workflow['type']}")
    print(f"   Stages: {len(workflow['stages'])}")
    print(f"   File: {workflow_file}")
    
    return workflow_file

def list_templates():
    """List available workflow templates."""
    print("Available workflow templates:")
    for template_id, template in WORKFLOW_TEMPLATES.items():
        print(f"  {template_id}: {template['name']}")
        print(f"     {template['description']}")
        print(f"     Stages: {len(template['stages'])}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Create a new content workflow")
    parser.add_argument("--name", required=True, help="Name of the workflow")
    parser.add_argument("--type", choices=list(WORKFLOW_TEMPLATES.keys()) + ["custom"], 
                       default="blog", help="Type of workflow template to use")
    parser.add_argument("--output", default="workflows", help="Output directory for workflow files")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    # Create the workflow
    try:
        workflow_file = create_workflow(args.name, args.type, args.output)
        print(f"\nNext steps:")
        print(f"1. Review workflow: cat {workflow_file}")
        print(f"2. Edit stages if needed")
        print(f"3. Run workflow: python3 run_workflow.py --workflow {args.name.lower().replace(' ', '-')}")
    except Exception as e:
        print(f"❌ Error creating workflow: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
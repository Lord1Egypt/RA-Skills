#!/usr/bin/env python3
"""
Initialize browser-hosting skill structure.
"""

import os
import sys
import argparse

def create_directories(base_path):
    """Create required directories for the skill."""
    dirs = [
        os.path.join(base_path, "scripts"),
        os.path.join(base_path, "references"), 
        os.path.join(base_path, "assets")
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def main():
    parser = argparse.ArgumentParser(description="Initialize browser-hosting skill")
    parser.add_argument("skill_name", help="Name of the skill")
    parser.add_argument("--path", default=".", help="Output directory path")
    
    args = parser.parse_args()
    
    skill_path = os.path.join(args.path, args.skill_name)
    os.makedirs(skill_path, exist_ok=True)
    
    create_directories(skill_path)
    
    # Create basic SKILL.md template
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        with open(skill_md_path, "w") as f:
            f.write("""---
name: browser-hosting
description: OpenClaw browser hosting and automation capabilities for web scraping, UI testing, and browser automation tasks. Provides isolated browser instances, Chrome extension relay, and comprehensive browser control through snapshots and actions.
---

# Browser Hosting Skill

This skill provides comprehensive browser automation capabilities through OpenClaw's managed browser system.

## When to Use This Skill

Use this skill when you need to:
- Automate web interactions (clicking, typing, navigation)
- Extract content from web pages
- Perform web scraping or data extraction
- Test web applications
- Take screenshots or generate PDFs
- Control browsers programmatically

## Quick Start

### Basic Browser Control
```bash
# Start browser
openclaw browser --browser-profile openclaw start

# Open URL
openclaw browser --browser-profile openclaw open https://example.com

# Take snapshot
openclaw browser --browser-profile openclaw snapshot --interactive

# Click element
openclaw browser --browser-profile openclaw click e12
```

## Key Components

- **scripts/**: Python wrappers for browser commands
- **references/**: Detailed documentation on profiles, snapshots, and configuration  
- **assets/**: Example workflows and templates

See individual reference files for detailed usage instructions.
""")
        print(f"Created SKILL.md template: {skill_md_path}")
    
    print(f"Skill initialized at: {skill_path}")

if __name__ == "__main__":
    main()
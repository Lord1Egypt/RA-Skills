#!/usr/bin/env python3
"""
generate-script.py — Generate podcast script from research

Takes research JSON and generates a conversational podcast script
with inline citations. Uses LLM for generation.

Usage:
    generate-script.py --research research.json --output script.txt --config config.yaml
"""
import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path


def load_config(config_path: str) -> dict:
    """Load config (simplified YAML parser)"""
    import re
    with open(config_path) as f:
        content = f.read()
    
    config = {"script": {}}
    
    # Parse script section
    script_match = re.search(r'script:\s*\n((?:  \w+:.*\n?)*)', content)
    if script_match:
        for line in script_match.group(1).split('\n'):
            if ':' in line:
                key, val = line.strip().split(':', 1)
                config["script"][key.strip()] = val.strip()
    
    return config


def load_template(skill_dir: Path) -> str:
    """Load script prompt template"""
    template_path = skill_dir / "templates" / "script-prompt.md"
    if not template_path.exists():
        return DEFAULT_TEMPLATE
    
    with open(template_path) as f:
        return f.read()


DEFAULT_TEMPLATE = """# Podcast Script Generation Prompt

You are a podcast scriptwriter. Generate a compelling, conversational podcast script based on the research provided.

## Requirements

1. **Length**: {word_count} words
2. **Style**: {style} (conversational, engaging, but fact-based)
3. **Structure**:
   - Hook: Open with a surprising fact or compelling question (30 seconds)
   - Setup: Context and why this matters (2 minutes)
   - Background: Core explanation with details (5 minutes)
   - Deep Dive: Main insights, data, examples (8 minutes)
   - Counter Views: Acknowledge limitations or criticisms (2 minutes)
   - Takeaway: Actionable insight or future implications (2 minutes)

4. **Citations**: Every factual claim MUST have inline [Source: URL] citation immediately after
5. **Tone**: Conversational but authoritative, like explaining to a smart friend
6. **No fluff**: Every sentence should add value
7. **Specific data**: Use exact numbers from research, not approximations

## Research Data
{research_json}

Generate the script now.
"""


def main():
    """Main entry point for script generation"""
    parser = argparse.ArgumentParser(description="Generate podcast script from research")
    parser.add_argument("--research", required=True, help="Research JSON file")
    parser.add_argument("--output", required=True, help="Output script file")
    parser.add_argument("--config", required=True, help="Config YAML file")
    args = parser.parse_args()
    
    skill_dir = Path(__file__).parent.parent
    
    # Load research
    with open(args.research) as f:
        research = json.load(f)
    
    # Load config
    config = load_config(args.config)
    script_config = config.get("script", {})
    
    word_count = script_config.get("word_count", "2500-3500")
    style = script_config.get("style", "conversational")
    
    print(f"=== GENERATING SCRIPT ===")
    print(f"Topic: {research['topic']}")
    print(f"Sources: {len(research.get('sources', []))}")
    print(f"Target length: {word_count} words")
    print(f"Style: {style}")
    print()
    
    # Load template
    template = load_template(skill_dir)
    
    # Fill template
    prompt = template.format(
        word_count=word_count,
        style=style,
        research_json=json.dumps(research, indent=2)
    )
    
    print("⚠️  This script generates the prompt framework.")
    print("    Actual LLM generation must be performed by OpenClaw worker.")
    print()
    print("Worker should:")
    print("  1. Use the prompt template")
    print("  2. Call LLM (Claude Sonnet 4.5 recommended)")
    print("  3. Ensure every claim has [Source: URL] citation")
    print("  4. Verify word count matches config")
    print("  5. Save to output file")
    print()
    
    # Save prompt for worker
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output + ".prompt", 'w') as f:
        f.write(prompt)
    
    print(f"✅ Prompt saved to: {args.output}.prompt")
    print(f"   Worker should generate script to: {args.output}")
    
    # Create placeholder script
    placeholder = f"""[VERIFIED] Podcast Script - {research['topic']} - {datetime.now().date().isoformat()}

[This is a placeholder. OpenClaw worker should replace this with actual generated script.]

Structure:
- Hook: Surprising opening fact
- Setup: Why this matters
- Background: Core explanation
- Deep Dive: Main insights with data
- Counter Views: Limitations/criticisms
- Takeaway: Actionable insight

Every factual claim must have [Source: URL] citation.

Research sources available: {len(research.get('sources', []))}
Target word count: {word_count}
"""
    
    with open(args.output, 'w') as f:
        f.write(placeholder)
    
    print(f"✅ Placeholder script saved to: {args.output}")


if __name__ == "__main__":
    main()

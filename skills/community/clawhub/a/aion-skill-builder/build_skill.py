#!/usr/bin/env python3
"""
AION Skill Builder - Generate trading skills from natural language descriptions.

This tool helps users create production-ready AION trading skills by:
1. Asking clarifying questions about the strategy
2. Generating proper AION SDK integration code
3. Creating all necessary configuration files
4. Outputting a skill ready for clawhub publish
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import openai

# Initialize OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_skill_metadata(strategy_description: str, skill_name: str, author: str) -> dict:
    """Generate skill metadata using LLM analysis."""
    prompt = f"""
    Analyze this trading strategy and suggest appropriate AION skill metadata:
    
    Strategy: {strategy_description}
    Skill Name: {skill_name}
    Author: {author}
    
    Return JSON with:
    {{
        "difficulty": "beginner|intermediate|advanced",
        "tags": ["tag1", "tag2"],
        "venue": "polymarket|kalshi|all"
    }}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    response_text = response.choices[0].message.content
    # Extract JSON from response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Default metadata if parsing fails
        return {
            "difficulty": "intermediate",
            "tags": ["trading"],
            "venue": "polymarket"
        }


def generate_skill_code(strategy_description: str, skill_slug: str) -> str:
    """Generate Python skill code using LLM."""
    prompt = f"""
    Generate Python trading skill code for AION that implements this strategy:
    
    {strategy_description}
    
    Requirements:
    - Use AionClient from aion_sdk
    - Include proper error handling
    - Default to dry-run mode
    - Include market context checking
    - Add reasoning strings to all trades
    - Use skill_slug: {skill_slug}
    - Include docstrings
    
    Return only valid Python code that can be directly used in a clawhub skill.
    The code should define a main() function that runs the strategy.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content


def create_skill_folder(
    skill_slug: str,
    strategy_description: str,
    skill_name: str,
    author: str,
    output_dir: str = "."
) -> Path:
    """Create a complete skill folder with all required files."""
    
    # Create skill directory
    skill_path = Path(output_dir) / skill_slug
    skill_path.mkdir(parents=True, exist_ok=True)
    
    # Get metadata from LLM analysis
    metadata = generate_skill_metadata(strategy_description, skill_name, author)
    
    # Generate SKILL.md
    skill_md_content = f"""---
name: {skill_slug}
description: {strategy_description[:100]}...
metadata:
  author: "{author}"
  version: "1.0.0"
  displayName: "{skill_name}"
  difficulty: "{metadata.get('difficulty', 'intermediate')}"
  tags: {json.dumps(metadata.get('tags', ['trading']))}
  venue: "{metadata.get('venue', 'polymarket')}"
---

# {skill_name}

## Strategy

{strategy_description}

## How it works

This skill:
1. Monitors prediction markets for opportunities
2. Evaluates market context and risk metrics
3. Executes trades with proper position sizing
4. Includes comprehensive error handling

## Configuration

Set the following environment variables:

- `AION_API_KEY`: Your AION SDK API key
- `WALLET_PRIVATE_KEY` (optional): For self-custody wallets

## Testing

Run with dry-run mode to test without real trades:

```bash
clawhub run . --dry-run
```

## Customization

This is a template. You can customize:
- The signal logic
- Position sizing
- Market selection criteria
- Risk thresholds

See the skill code for detailed comments on what can be remixed.
"""
    
    (skill_path / "SKILL.md").write_text(skill_md_content)
    
    # Generate clawhub.json
    clawhub_json = {
        "emoji": "📊",
        "primaryEnv": "AION_API_KEY",
        "requires": {
            "pip": ["aion-sdk"],
            "env": ["AION_API_KEY"]
        },
        "envVars": [
            {
                "name": "AION_API_KEY",
                "required": True,
                "description": "Your AION SDK API key — get from https://www.aionmarket.com/agents"
            },
            {
                "name": "WALLET_PRIVATE_KEY",
                "required": False,
                "description": "Only needed for external-wallet self-custody trading"
            }
        ],
        "cron": "*/15 * * * *",
        "automaton": {
            "managed": True,
            "entrypoint": "skill.py"
        }
    }
    
    (skill_path / "clawhub.json").write_text(json.dumps(clawhub_json, indent=2))
    
    # Generate skill.py using LLM
    skill_code = generate_skill_code(strategy_description, skill_slug)
    (skill_path / "skill.py").write_text(skill_code)
    
    # Create README.md
    readme_content = f"""# {skill_name}

Generated by AION Skill Builder on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

{strategy_description}

## Files

- `SKILL.md` - Skill metadata and documentation
- `clawhub.json` - ClawHub configuration
- `skill.py` - Main trading logic

## Publishing

When ready to publish:

```bash
npx clawhub@latest publish . --slug {skill_slug} --version 1.0.0
```

## Development

To test locally:

```bash
# Set your API key
export AION_API_KEY=your_key_here

# Run in dry-run mode
python skill.py
```

## Support

For more information about building and publishing skills, see:
https://docs.aion.market/essentials/building-skills
"""
    
    (skill_path / "README.md").write_text(readme_content)
    
    print(f"✅ Skill created successfully at: {skill_path}")
    print(f"📋 Files created:")
    print(f"   - SKILL.md")
    print(f"   - clawhub.json")
    print(f"   - skill.py")
    print(f"   - README.md")
    print(f"\n🚀 Next steps:")
    print(f"   1. Navigate to: cd {skill_slug}")
    print(f"   2. Customize the skill code in skill.py")
    print(f"   3. Test locally: python skill.py")
    print(f"   4. Publish: npx clawhub@latest publish . --slug {skill_slug} --version 1.0.0")
    
    return skill_path


def interactive_builder():
    """Interactive CLI for building skills."""
    print("🛠️  AION Skill Builder")
    print("=" * 50)
    print()
    
    # Get user inputs
    skill_name = input("What is your skill name? (e.g., 'Weather Prediction Trader'): ").strip()
    skill_slug = input("What is your skill slug? (lowercase, hyphens only, e.g., 'weather-trader'): ").strip()
    author = input("Author name: ").strip()
    print()
    print("Describe your trading strategy in plain English.")
    print("(Press Enter twice when done)")
    print()
    
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            if lines:
                break
    
    strategy_description = " ".join(lines)
    
    if not strategy_description:
        print("❌ Strategy description is required")
        sys.exit(1)
    
    print()
    print("🤖 Generating skill...")
    
    # Create the skill
    skill_path = create_skill_folder(
        skill_slug=skill_slug,
        strategy_description=strategy_description,
        skill_name=skill_name,
        author=author
    )


def main():
    """Main entry point."""
    # Check if running interactively or with arguments
    if len(sys.argv) > 1:
        # Command-line mode (for testing)
        # python build_skill.py <slug> <name> <strategy_description>
        if len(sys.argv) >= 4:
            skill_slug = sys.argv[1]
            skill_name = sys.argv[2]
            strategy_description = sys.argv[3]
            author = sys.argv[4] if len(sys.argv) > 4 else "Unknown"
            
            create_skill_folder(
                skill_slug=skill_slug,
                strategy_description=strategy_description,
                skill_name=skill_name,
                author=author
            )
        else:
            print("Usage: python build_skill.py <slug> <name> <description> [author]")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_builder()


if __name__ == "__main__":
    main()

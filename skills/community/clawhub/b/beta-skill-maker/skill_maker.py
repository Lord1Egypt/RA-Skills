#!/usr/bin/env python3
"""Skill Maker — generates SKILL.md files for OpenClaw AI agents"""
import argparse
import os
import sys

TEMPLATE = """---
name: {name}
description: {desc}
metadata:
  openclaw:
    emoji: "{emoji}"
    requires:
      bins: [{bins}]
      env: [{env}]
    always: false
---

# {name}

{body}

## Usage

```bash
{name_lower} {args_str}
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Examples

### Example 1

```bash
{name_lower} example1
```

### Example 2

```bash
{name_lower} example2
```

## Notes

- Requires: {bins}
- MIT-0 License
"""

README_TEMPLATE = """# {name}

> {desc}

## Quick Start

```bash
python3 {name_lower}.py --help
```

## Installation

```bash
# Clone or download
# No external dependencies required
```

## License

MIT-0
"""

def main():
    parser = argparse.ArgumentParser(description='Create a SKILL.md for OpenClaw')
    parser.add_argument('--name', required=True, help='Skill name')
    parser.add_argument('--desc', required=True, help='Short description (<50 chars)')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--category', default='productivity', help='Category')
    parser.add_argument('--emoji', default='🛠️', help='Emoji icon')
    parser.add_argument('--bins', default='', help='Required binaries (comma-separated)')
    parser.add_argument('--env', default='', help='Required env vars (comma-separated)')
    args = parser.parse_args()

    name_lower = args.name.lower().replace(' ', '-')
    os.makedirs(args.output, exist_ok=True)

    skill_md = TEMPLATE.format(
        name=args.name,
        name_lower=name_lower,
        desc=args.desc,
        emoji=args.emoji,
        bins=args.bins or 'python3',
        env=args.env or '',
        body=f'Generated skill: {args.name}',
        args_str='--input <file>'
    )

    with open(os.path.join(args.output, 'SKILL.md'), 'w') as f:
        f.write(skill_md)

    readme = README_TEMPLATE.format(name=args.name, name_lower=name_lower, desc=args.desc)
    with open(os.path.join(args.output, 'README.md'), 'w') as f:
        f.write(readme)

    os.makedirs(os.path.join(args.output, 'references'), exist_ok=True)
    with open(os.path.join(args.output, 'references', 'overview.md'), 'w') as f:
        f.write(f'# {args.name} — Overview\n\n{args.desc}\n')

    print(f'✅ Skill created at {args.output}/')
    print(f'  - SKILL.md')
    print(f'  - README.md')
    print(f'  - references/')

if __name__ == '__main__':
    main()

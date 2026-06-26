#!/usr/bin/env python3
"""Quick Skill Maker"""
import argparse, os
TEMPLATE = """---
name: {name}
description: {desc}
metadata:
  openclaw:
    emoji: "{emoji}"
    requires:
      bins: [python3]
    always: false
---

# {name}

{desc}

## Usage

```bash
{name_lower} [command]
```

## Features

- Feature 1
- Feature 2

## Examples

```bash
{name_lower} --example
```

## Notes

MIT-0 License
"""
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    p.add_argument('--desc', required=True)
    p.add_argument('--emoji', default='🛠️')
    args = p.parse_args()
    n = args.name.lower().replace(' ', '-')
    c = TEMPLATE.format(name=args.name, name_lower=n, desc=args.desc, emoji=args.emoji)
    with open('SKILL.md', 'w') as f: f.write(c)
    print(f'Created SKILL.md → {os.getcwd()}/SKILL.md')
if __name__ == '__main__': main()

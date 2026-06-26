#!/usr/bin/env python3
from pathlib import Path
import argparse

STRUCTURE = [
    'launch-assets',
    'launch-assets/posters',
    'launch-assets/videos',
    'launch-assets/campaign-videos',
    'launch-assets/campaign-videos-polished',
    'launch-assets/campaign-videos-sales',
    'launch-assets/people-holding-book-style-pack',
    'launch-assets/people-holding-book-mockups',
    'openclaw-launch-pack',
    'en',
]

FILES = {
    'openclaw-launch-pack/launch-copy.md': '# Launch Copy\n',
    'openclaw-launch-pack/platform-posts.md': '# Platform Posts\n',
    'openclaw-launch-pack/asset-index.md': '# Asset Index\n',
    'openclaw-launch-pack/launch-checklist.md': '# Launch Checklist\n',
    'openclaw-launch-pack/amazon-kindle-conversion-pack.md': '# Amazon Kindle Conversion Pack\n',
    'openclaw-launch-pack/amazon-ready-to-publish-pack.md': '# Amazon Ready-to-Publish Pack\n',
}


def main():
    parser = argparse.ArgumentParser(description='Scaffold a book launch project structure')
    parser.add_argument('target', help='Target project directory')
    args = parser.parse_args()

    root = Path(args.target)
    root.mkdir(parents=True, exist_ok=True)

    for rel in STRUCTURE:
        (root / rel).mkdir(parents=True, exist_ok=True)

    for rel, content in FILES.items():
        p = root / rel
        if not p.exists():
            p.write_text(content, encoding='utf-8')

    print(f'Created launch structure in: {root}')

if __name__ == '__main__':
    main()

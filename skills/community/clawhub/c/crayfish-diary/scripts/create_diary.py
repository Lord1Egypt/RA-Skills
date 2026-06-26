#!/usr/bin/env python3
"""
Crayfish Diary Creation Script
Creates diary entries organized by year/month/day directory structure
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing or replacing illegal characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Replace illegal characters with underscores
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '_', filename)


def update_daily_summary(diary_dir: Path, date_str: str) -> None:
    """
    Update daily summary README.md
    
    Args:
        diary_dir: Path to the day's diary directory
        date_str: Date string in YYYY-MM-DD format
    """
    readme_path = diary_dir / 'README.md'
    
    # Get all markdown files except README.md
    md_files = sorted([f for f in diary_dir.glob('*.md') if f.name != 'README.md'])
    
    if not md_files:
        return
    
    # Build summary content
    summary_lines = [
        f'# {date_str} 日记摘要\n',
        '## 记录列表\n'
    ]
    
    for idx, md_file in enumerate(md_files, 1):
        # Read file content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title (first # heading)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else md_file.stem
        
        # Extract time
        time_match = re.search(r'\*\*时间\*\*: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})', content)
        time = time_match.group(1).split()[1] if time_match else ''
        
        # Extract content summary (first 50 chars of actual content)
        # Skip metadata and get the actual content
        content_lines = content.split('\n')
        actual_content = []
        in_content = False
        for line in content_lines:
            if line.strip() == '---':
                in_content = not in_content
                continue
            if in_content and line.strip() and not line.startswith('#') and not line.startswith('**'):
                actual_content.append(line.strip())
        
        content_text = ' '.join(actual_content)
        summary = content_text[:50] + '...' if len(content_text) > 50 else content_text
        
        summary_lines.append(f'{idx}. **{time} {title}**: {summary}\n')
    
    summary_lines.extend([
        '\n---',
        f'*共 {len(md_files)} 条记录*\n'
    ])
    
    # Write README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.writelines(summary_lines)


def create_diary(base_path: str, content: str, title: str = None, tags: list = None) -> str:
    """
    Create a diary file
    
    Args:
        base_path: Base storage path
        content: Diary content
        title: Diary title (optional)
        tags: List of tags (optional)
        
    Returns:
        Created file path
    """
    now = datetime.now()
    
    # Build directory path: year/month/day
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    
    diary_dir = Path(base_path) / '龙虾日记' / year / month / day
    diary_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine filename
    if not title:
        # Extract title from content (first 20 characters)
        title = content[:20].strip()
        if len(content) > 20:
            title += '...'
    
    # Sanitize filename
    safe_title = sanitize_filename(title)
    time_str = now.strftime('%H-%M')
    filename = f'{time_str}-{safe_title}.md'
    
    # Build complete file path
    file_path = diary_dir / filename
    
    # If file exists, add counter
    counter = 1
    while file_path.exists():
        filename = f'{time_str}-{safe_title}-{counter}.md'
        file_path = diary_dir / filename
        counter += 1
    
    # Build markdown content
    time_formatted = now.strftime('%Y-%m-%d %H:%M')
    
    md_content = f'''# {title}

**时间**: {time_formatted}
'''

    if tags:
        tags_str = '、'.join(tags)
        md_content += f'**标签**: {tags_str}\n'
    
    md_content += f'''
---

{content}

---

*由龙虾日记自动记录*
'''
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Update daily summary
    date_str = now.strftime('%Y-%m-%d')
    update_daily_summary(diary_dir, date_str)
    
    return str(file_path)


def main():
    """Command line entry point"""
    if len(sys.argv) < 3:
        print('Usage: python create_diary.py <base_path> <content> [title] [tag1,tag2,...]')
        sys.exit(1)
    
    base_path = sys.argv[1]
    content = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else None
    tags = sys.argv[4].split(',') if len(sys.argv) > 4 else None
    
    file_path = create_diary(base_path, content, title, tags)
    print(f'Diary created: {file_path}')


if __name__ == '__main__':
    main()

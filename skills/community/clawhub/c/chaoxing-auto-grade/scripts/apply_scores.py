#!/usr/bin/env python3
"""apply_scores.py — Write AI-graded scores back to original HTML files.

Reads subj_graded.json (from grade_subj.py) and updates the
value attributes of <input class="inputBranch questionScore"> tags.

Usage:
    python apply_scores.py --config config.json
"""

import json, re, os, sys

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    for i, a in enumerate(sys.argv):
        if a == '--config' and i + 1 < len(sys.argv):
            cfg_path = sys.argv[i+1]
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    raise FileNotFoundError(f'config.json not found')

CONFIG = load_config()
INPUT_DIR = CONFIG['paths']['input_dir']
WORK_DIR = CONFIG['paths']['work_dir']

GRADED_FILE = os.path.join(WORK_DIR, 'subj_graded.json')

SCORE_PATTERNS = [
    r'<input[^>]*class="[^"]*questionScore[^"]*"[^>]*name="score(\d+)"[^>]*value="([^"]*)"',
    r'<input[^>]*name="score(\d+)"[^>]*class="[^"]*questionScore[^"]*"[^>]*value="([^"]*)"',
    r'<input[^>]*name="score(\d+)"[^>]*class="[^"]*inputBranch[^"]*"[^>]*value="([^"]*)"',
    r'<input[^>]*value="([^"]*)"[^>]*name="score(\d+)"[^>]*class="[^"]*questionScore[^"]*"',
    r'<input[^>]*value="([^"]*)"[^>]*name="score(\d+)"[^>]*class="[^"]*inputBranch[^"]*"',
    r'<input[^>]*name="score(\d+)"[^>]*value="([^"]*)"',
]

def main():
    if not os.path.exists(GRADED_FILE):
        print(f'ERROR: {GRADED_FILE} not found. Run grade_subj.py first.')
        return
    
    with open(GRADED_FILE, 'r', encoding='utf-8') as f:
        graded = json.load(f)
    
    score_map = {}
    for key, score in graded.items():
        if score is None: continue
        parts = key.split('|')
        score_map[(parts[0], parts[1], parts[2])] = score
    
    print(f'Score entries: {len(score_map)}')
    
    updated = 0
    total_changes = 0
    
    for d in os.listdir(INPUT_DIR):
        dp = os.path.join(INPUT_DIR, d)
        if not os.path.isdir(dp): continue
        
        for fname in os.listdir(dp):
            if not fname.endswith('.html'): continue
            fp = os.path.join(dp, fname)
            work_name = fname.replace('.html', '')
            
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            file_modified = False
            changes = 0
            
            matches = []
            for pat in SCORE_PATTERNS:
                for m in re.finditer(pat, content):
                    if pat.startswith('<input[^>]*value="'):
                        qid, old_val = m.group(2), m.group(1)
                    else:
                        qid, old_val = m.group(1), m.group(2)
                    matches.append((m.start(), qid, old_val))
            
            # Deduplicate by position
            seen = set()
            unique = []
            for pos, qid, old_val in matches:
                if pos not in seen:
                    seen.add(pos)
                    unique.append((pos, qid, old_val))
            
            unique.sort(key=lambda x: x[0], reverse=True)
            
            for pos, qid, old_val in unique:
                key = (d, work_name, qid)
                if key in score_map:
                    new_val = str(score_map[key])
                    if old_val != new_val:
                        # Find the exact tag and replace value
                        tag_start = content.rfind('<input', 0, pos)
                        tag_end = content.find('>', pos) + 1
                        tag = content[tag_start:tag_end]
                        new_tag = tag.replace(f'value="{old_val}"', f'value="{new_val}"')
                        
                        if new_tag != tag:
                            content = content[:tag_start] + new_tag + content[tag_end:]
                            changes += 1
                            file_modified = True
            
            if file_modified:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                updated += 1
                total_changes += changes
                print(f'  {d}/{fname}: {changes} updated')
    
    print(f'\nFiles updated: {updated}, Score changes: {total_changes}')

if __name__ == '__main__':
    main()
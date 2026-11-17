#!/usr/bin/env python3
"""extract_subj.py — Extract subjective (essay/fill-in) questions from 超星 HTML to JSON.

Usage:
    python extract_subj.py --config config.json

Output: {work_dir}/subj_questions.json
"""

import json, os, re, sys

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    # Fallback: look for --config arg
    for i, a in enumerate(sys.argv):
        if a == '--config' and i + 1 < len(sys.argv):
            with open(sys.argv[i+1], 'r') as f:
                return json.load(f)
    raise FileNotFoundError('config.json not found. Pass --config <path>')

CONFIG = load_config()
INPUT_DIR = CONFIG['paths']['input_dir']
WORK_DIR = CONFIG['paths']['work_dir']

def strip_tags(s):
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    return s.strip()

def extract():
    questions = []
    
    for root, dirs, files in os.walk(INPUT_DIR):
        for fname in sorted(files):
            if not fname.endswith('.html'): continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as fh:
                c = fh.read()
            
            c2 = re.sub(r'<script[\s\S]*?</script>', '', c)
            c2 = re.sub(r'<style[\s\S]*?</style>', '', c2)
            
            # Find work/student name
            stu_m = re.search(r'id="stuRealName"\s+value="([^"]*)"', c)
            stu_name = stu_m.group(1) if stu_m else ''
            work_name = fname.replace('.html', '')
            
            # Find non-objective (subjective) mark_item1 blocks
            for m in re.finditer(r'<div class="mark_item1(?!\s*objective)', c2):
                s = m.start()
                prev_obj = c2[:s].rfind('<div class="mark_item1 objective')
                next_m = re.search(r'<div class="mark_item1[^"]*"', c2[s+1:])
                e = (next_m.start() + s + 1) if next_m else s + 8000
                block = c2[s:e]
                
                # Title
                title_m = re.search(r'class="mark_name[^"]*"[^>]*>(.*?)</h3>', block, re.DOTALL)
                q_title = title_m.group(1).strip() if title_m else ''
                
                # Skip objective blocks (already scored, not for AI grading)
                if '客观题' in q_title or 'objective' in block[:100]:
                    continue
                
                # Get question stem and answer from bbsContainer
                stem = ''
                bbs_m = re.search(r'bbsContainer[^>]*content="([^"]*)"', block)
                if bbs_m:
                    stem = strip_tags(bbs_m.group(1))
                
                student_ans = ''
                ans_m = re.search(r'bbsContainer[^>]*answer="([^"]*)"', block)
                if ans_m:
                    student_ans = strip_tags(ans_m.group(1))
                
                if not stem and not student_ans:
                    continue
                
                # Full score
                full = '?'
                place_m = re.search(r'placeholder="0-(\d+\.?\d*)"', block)
                if place_m:
                    full = place_m.group(1)
                else:
                    hscore_m = re.search(r'name="qscore\d+".*?value="([^"]*)"', block)
                    if hscore_m:
                        full = hscore_m.group(1)
                
                # QID
                qid_m = re.search(r'questionStem_(\d+)', block)
                qid = qid_m.group(1) if qid_m else str(hash(block[:200]))
                
                questions.append({
                    'file': fpath,
                    'student': stu_name,
                    'work': work_name,
                    'title': q_title,
                    'question': stem,
                    'answer': student_ans,
                    'full_score': float(full) if full != '?' else 0,
                    'qid': qid
                })
    
    outpath = os.path.join(WORK_DIR, 'subj_questions.json')
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f'Extracted {len(questions)} subjective questions → {outpath}')
    return questions

if __name__ == '__main__':
    extract()
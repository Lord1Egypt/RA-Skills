#!/usr/bin/env python3
"""clean_html.py — Clean 超星 review HTML, keep only questions/answers/scores.

Supports: objective (选择题/判断题), fill-in-blank (填空题), subjective (简答题).
Outputs readable HTML with total score display.

Usage:
    python clean_html.py --config config.json
"""

import os, re, sys, json

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    for i, a in enumerate(sys.argv):
        if a == '--config' and i + 1 < len(sys.argv):
            cfg_path = sys.argv[i+1]
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)
    raise FileNotFoundError('config.json not found')

CONFIG = load_config()
ROOT = CONFIG['paths']['input_dir']
OUT = CONFIG['paths']['output_dir']

CSS = '''<style>
body{font-family:"Microsoft YaHei",sans-serif;font-size:14px;color:#333;max-width:900px;margin:20px auto;padding:0 15px;}
.header{margin-bottom:20px;}
.title{font-size:20px;font-weight:bold;color:#4472c4;border-bottom:2px solid #4472c4;padding-bottom:8px;}
.meta{color:#888;font-size:13px;margin-top:4px;}
.section-title{font-size:16px;font-weight:bold;color:#555;margin:24px 0 12px 0;padding-left:8px;border-left:4px solid #4472c4;}
.q-block{border:1px solid #e0e0e0;border-radius:6px;padding:12px 16px;margin-bottom:12px;background:#fafafa;}
.q-title{font-size:15px;font-weight:bold;color:#222;margin-bottom:6px;}
.q-stem{margin-bottom:8px;color:#555;line-height:1.6;}
.answer-row{padding:4px 0;color:#333;}
.answer-row .stu{color:#c00;}
.answer-row .corr{color:#2a7d2a;}
.score-row{padding:2px 0 2px 16px;color:#555;}
.score-row input{width:60px;text-align:center;border:1px solid #ccc;border-radius:3px;padding:2px;background:#fff;}
.score-row .label{font-weight:bold;}
.correct-badge{color:#2a7d2a;font-size:16px;}
.wrong-badge{color:#c00;font-size:16px;}
.subj-answer{background:#f9f9f9;border:1px solid #eee;border-radius:4px;padding:12px 16px;min-height:40px;line-height:1.6;margin-top:8px;}
.subj-answer img{max-width:100%;}
</style>'''

def decode_html(s):
    s = s.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return s

def strip_tags(s):
    s = decode_html(s)
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\n\s*\n\s*\n+', '\n\n', s)
    return s.strip()

def extract_objective_question(block, i, results):
    """Extract multiple-choice / true-false / fill-in-blank question"""
    # Title
    title_m = re.search(r'<h3[^>]*class="mark_name[^"]*"[^>]*>(.*?)</h3>', block, re.DOTALL)
    if not title_m:
        title_m = re.search(r'<h3[^>]*>(.*?)</h3>', block, re.DOTALL)
    q_title = title_m.group(1).strip() if title_m else f'题{i+1}'
    q_title = re.sub(r'<div[^>]*>.*?</div>', '', q_title)
    q_title = re.sub(r'<[^>]+>', '', q_title)
    
    # Question text
    qtext_m = re.search(r'workTextWrap[^>]*>(.*?)</div>', block, re.DOTALL)
    q_text = qtext_m.group(1).strip() if qtext_m else ''
    q_text = re.sub(r'<[^>]+>', '', q_text)[:200]
    
    # Detect question type
    is_fillblank = 'name="填空题"' in block or '填空题' in q_title
    
    # Student answer
    if is_fillblank:
        blank_answers = []
        for fb in re.findall(r'<dd class="fillBox">(.*?)</dd>', block, re.DOTALL):
            p_m = re.search(r'<p>(.*?)</p>', fb, re.DOTALL)
            ans = strip_tags(p_m.group(1)) if p_m else ''
            blank_answers.append(ans)
        student = ' | '.join(blank_answers) if blank_answers else '未作答'
    else:
        stu_m = re.search(r'学生答案[^<]*</i>\s*([A-Za-z]+)', block)
        if not stu_m:
            stu_m = re.search(r'学生答案[^<]*</i>\s*\n?\s*([对错])', block, re.DOTALL)
        student = stu_m.group(1).strip() if stu_m else '未作答'
    
    # Correct answer
    if is_fillblank:
        corr_dds = re.findall(r'<dd>\([^)]*\)\s*([^<]*)</dd>', block)
        correct = ' | '.join(c.strip() for c in corr_dds) if corr_dds else '?'
    else:
        corr_m = re.search(r'正确答案[^<]*</i>\s*([A-Za-z]+)', block)
        if not corr_m:
            corr_m = re.search(r'正确答案[^<]*</i>\s*[\s\r\n]*<i[^>]*>\s*([对错])\s*</i>', block, re.DOTALL)
        if not corr_m:
            corr_m = re.search(r'正确答案[^<]*</i>\s*\n?\s*([对错])', block, re.DOTALL)
        correct = corr_m.group(1).strip() if corr_m else '?'
    
    # Score
    score_m = re.search(r'class="inputBranch"[^>]*?value="([^"]*)"', block)
    score = score_m.group(1) if score_m else '0'
    full_m = re.search(r'\([^)]*?(\d+\.?\d*)\s*分\)', block)
    full = full_m.group(1) if full_m else '0'
    
    results.append((float(score), float(full)))
    
    # Mark correct/wrong
    is_correct = ('✓' if str(score) == str(full) or float(score) >= float(full) * 0.99 else '✗')
    badge = f'<span class="correct-badge">{is_correct}</span>' if '✓' in is_correct else f'<span class="wrong-badge">{is_correct}</span>'
    
    correct_str = f'<span class="corr">正确答案:</span> {correct}' if correct else ''
    
    if student == '未作答':
        ans_html = f'<div class="answer-row">{correct_str}</div>'
    else:
        ans_html = f'''<div class="answer-row"><span class="stu">学生答案:</span> {student}</div>
<div class="answer-row"><span class="corr">{correct_str}</span></div>'''
    
    return f'''<div class="q-block">
        <div class="q-title">{badge} {q_title}</div>
        <div class="q-stem">{q_text}</div>
        {ans_html}
        <div class="score-row"><span class="label">得分:</span> <input type="text" value="{score}" readonly> / {full} 分</div>
    </div>'''

def extract_subjective_question(block, i, results):
    """Extract a single subjective (essay) question"""
    title_m = re.search(r'class="mark_name[^"]*"[^>]*>(.*?)</h3>', block, re.DOTALL)
    if not title_m:
        title_m = re.search(r'<h3[^>]*>(.*?)</h3>', block, re.DOTALL)
    q_title = title_m.group(1).strip() if title_m else f'题{i+1}'
    q_title = re.sub(r'<[^>]+>', '', q_title)
    
    # Question stem
    stem = ''
    bbs_m = re.search(r'bbsContainer[^>]*content="([^"]*)"', block)
    if bbs_m:
        stem = strip_tags(bbs_m.group(1))
    
    # Student answer
    student_ans = ''
    ans_m = re.search(r'bbsContainer[^>]*answer="([^"]*)"', block)
    if ans_m:
        student_ans = strip_tags(ans_m.group(1))
    
    # Score
    score_m = re.search(r'class="inputBranch questionScore"[^>]*value="([^"]*)"', block)
    if not score_m:
        score_m = re.search(r'class="inputBranch"[^>]*value="([^"]*)"', block)
    score = score_m.group(1) if score_m else '0'
    
    # Full score
    full = '?'
    place_m = re.search(r'placeholder="0-(\d+\.?\d*)"', block)
    if place_m:
        full = place_m.group(1)
    else:
        hscore_m = re.search(r'name="qscore\d+".*?value="([^"]*)"', block)
        if hscore_m:
            full = hscore_m.group(1)
    
    results.append((float(score), float(full)))
    
    return f'''<div class="q-block">
        <div class="q-title">✏ {i+1}. {q_title}</div>
        <div class="q-stem">{stem}</div>
        <div class="subj-answer"><strong>学生答案:</strong><br>{student_ans or '(无文字作答)'}</div>
        <div class="score-row"><span class="label">得分:</span> <input type="text" value="{score}" readonly> / {full} 分</div>
    </div>'''

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Student name
    stu_m = re.search(r'id="stuRealName"\s+value="([^"]*)"', content)
    stu_name = stu_m.group(1) if stu_m else ''
    
    # Work name from filename
    fname = os.path.basename(filepath)
    work_name = ''
    wn_m = re.search(r'_(作业[^\.]+)\.html', fname)
    if wn_m:
        work_name = wn_m.group(1)
    
    # Remove script and style
    clean = re.sub(r'<script[\s\S]*?</script>', '', content)
    clean = re.sub(r'<style[\s\S]*?</style>', '', clean)
    
    # Find all mark_item1 blocks
    objective_blocks = []
    subjective_blocks = []
    
    all_starts = [(m.start(), m.group()) for m in re.finditer(r'<div class="mark_item1[^"]*"', clean)]
    
    for idx, (start, tag) in enumerate(all_starts):
        if idx + 1 < len(all_starts):
            end = all_starts[idx + 1][0]
        else:
            end = min(start + 8000, len(clean))
        
        block = clean[start:end]
        
        if 'objective' in tag:
            objective_blocks.append((start, block))
        else:
            subjective_blocks.append((start, block))
    
    sections = []
    results = []
    
    total_obj = len(objective_blocks)
    total_subj = len(subjective_blocks)
    
    if total_obj > 0:
        sections.append(f'<div class="section-title">客观题 ({total_obj}题)</div>')
        for i, (_, block) in enumerate(objective_blocks):
            sections.append(extract_objective_question(block, i + 1, results))
    
    if total_subj > 0:
        sections.append(f'<div class="section-title">主观题 ({total_subj}题)</div>')
        for i, (_, block) in enumerate(subjective_blocks):
            sections.append(extract_subjective_question(block, i + 1, results))
    
    if not sections:
        return None
    
    q_body = '\n'.join(sections)
    total = total_obj + total_subj
    
    total_score = sum(r[0] for r in results)
    total_full = sum(r[1] for r in results)
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{stu_name}_{work_name}</title>
{CSS}
</head>
<body>
<div class="header">
    <div class="title">{stu_name} — {work_name}</div>
    <div class="meta">共 {total} 题（客观题 {total_obj} + 主观题 {total_subj}）</div>
    <div class="meta" style="color:#4472c4;font-size:18px;font-weight:bold;">总分: {total_score:.1f} / {total_full:.1f} 分</div>
</div>

{q_body}

</body>
</html>'''

def main():
    os.makedirs(OUT, exist_ok=True)
    total_before = 0
    total_after = 0
    count = 0
    empty = []
    
    for student_dir in sorted(os.listdir(ROOT)):
        spath = os.path.join(ROOT, student_dir)
        if not os.path.isdir(spath): continue
        
        out_dir = os.path.join(OUT, student_dir)
        os.makedirs(out_dir, exist_ok=True)
        
        for fname in sorted(os.listdir(spath)):
            if not fname.endswith('.html'): continue
            fpath = os.path.join(spath, fname)
            
            before = os.path.getsize(fpath)
            html = clean_file(fpath)
            
            if html:
                outpath = os.path.join(out_dir, fname)
                with open(outpath, 'w', encoding='utf-8') as f:
                    f.write(html)
                after = os.path.getsize(outpath)
                
                total_before += before
                total_after += after
                count += 1
            else:
                empty.append(f'{student_dir}/{fname}')
    
    reduction = (1 - total_after / total_before) * 100 if total_before > 0 else 0
    print(f'Files: {count}')
    print(f'Before: {total_before/1024:.0f} KB')
    print(f'After: {total_after/1024:.0f} KB')
    print(f'Reduction: {reduction:.1f}%')
    
    if empty:
        print(f'\nEmpty (no questions found): {len(empty)}')
        for e in empty:
            print(f'  {e}')
    
    print(f'\nOutput: {OUT}')

if __name__ == '__main__':
    main()
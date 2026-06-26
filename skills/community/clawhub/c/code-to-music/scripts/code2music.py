"""
Code to Music - 代码交响曲生成器
用法: python code2music.py <代码文件路径> [输出MP3路径]
"""

import sys
import re
import json
import requests
import os

API_KEY = os.environ.get('MINIMAX_API_KEY', '')
API_URL = 'https://api.minimaxi.com/v1/music_generation'

if not API_KEY:
    print('[ERROR] MINIMAX_API_KEY not set')
    sys.exit(1)

def analyze_code(code: str) -> dict:
    """分析代码结构特征"""
    lines = code.split('\n')
    total_lines = len(lines)
    non_empty = [l for l in lines if l.strip()]
    code_lines = [l for l in non_empty if not l.strip().startswith('//') and not l.strip().startswith('/*') and not l.strip().startswith('*')]
    
    indent_depths = []
    for line in lines:
        if line.strip():
            indent_depths.append(len(line) - len(line.lstrip()))
    max_indent = max(indent_depths) if indent_depths else 0
    
    # 函数检测（支持多语言）
    functions = re.findall(
        r'(?:function|const|let|var|def|public|private|protected)\s+\w+\s*\([^)]*\)',
        code
    )
    func_count = len(functions)
    
    keywords = ['if', 'else', 'for', 'while', 'return', 'switch', 'case', 'try', 'catch', 'throw', 'import', 'package']
    kw_total = sum(len(re.findall(r'\b' + k + r'\b', code)) for k in keywords)
    
    comment_lines = [l for l in lines if l.strip().startswith('//') or l.strip().startswith('/*') or l.strip().startswith('*')]
    comment_ratio = len(comment_lines) / total_lines if total_lines else 0
    
    strings = re.findall(r'"[^"]*"', code)
    string_count = len(strings)
    
    open_b, close_b = code.count('{'), code.count('}')
    brace = min(open_b, close_b) / max(open_b, close_b) if max(open_b, close_b) else 1
    
    return {
        'total_lines': total_lines,
        'func_count': func_count,
        'max_indent': max_indent,
        'kw_total': kw_total,
        'comment_ratio': comment_ratio,
        'string_count': string_count,
        'brace': brace,
    }

def code_to_music_params(features: dict) -> dict:
    """映射到音乐参数"""
    lines = features['total_lines']
    bpm = min(180, max(60, 60 + lines // 5))
    
    indent = features['max_indent']
    if indent > 32:
        key = "C minor - deep, dark, mysterious"
    elif indent > 16:
        key = "A minor - melancholic, thoughtful"
    elif indent > 8:
        key = "G major - bright, balanced"
    else:
        key = "D major - uplifting, energetic"
    
    func_count = features['func_count']
    if func_count > 20:
        instrument = "piano, strings, brass ensemble"
    elif func_count > 10:
        instrument = "piano, guitar"
    elif func_count > 3:
        instrument = "piano, soft synth"
    else:
        instrument = "solo piano"
    
    kw = features['kw_total']
    if kw > 100:
        rhythm = "fast arpeggios, complex polyrhythms"
        texture = "dense, layered"
    elif kw > 50:
        rhythm = "moderate syncopation"
        texture = "medium"
    else:
        rhythm = "steady, clean"
        texture = "sparse, airy"
    
    comment = features['comment_ratio']
    vocal_style = "soft choir hums" if comment > 0.2 else "whispers" if comment > 0.1 else "instrumental only"
    
    strings = features['string_count']
    if strings > 50:
        mood = "dramatic, emotional crescendo"
    elif strings > 20:
        mood = "expressive, dynamic"
    else:
        mood = "calm, meditative"
    
    return {
        'bpm': bpm,
        'key': key,
        'instrument': instrument,
        'rhythm': rhythm,
        'texture': texture,
        'vocal_style': vocal_style,
        'mood': mood,
    }

def generate_prompt_and_lyrics(features: dict, params: dict) -> tuple:
    """生成 prompt 和歌词"""
    funcs = features['func_count']
    kws = features['kw_total']
    
    extra = "Conditions branching, decisions made\nReturn the answer, never afraid\n" if kws > 50 else ""
    
    lyrics = f"""[Intro - ethereal whispers]
In the code we trust, in the logic we trust
Functions rise and fall, like echoes in the halls

[Verse 1]
{funcs} functions waiting in the dark
Each one called with purpose, each one plays its part
{extra}[Chorus]
Compile the dream, run the test
Syntax errors fade, we have done our best
From zeros and ones, we build the sound
The machine awakens, profound

[Bridge]
{params['mood']}, that's what we feel
Every bracket balanced, every line is real
In the rhythm of the stack, we find our way
Software symphony, playing every day

[Outro]
The program ends, but the music stays
In the memory banks, for endless days"""
    
    prompt = (
        f"A {params['mood']} code symphony. "
        f"{params['bpm']} BPM in {params['key']}. "
        f"Features {funcs} functions, "
        f"{kws} control statements. "
        f"Instruments: {params['instrument']}. "
        f"Rhythm: {params['rhythm']}. "
        f"Think: algorithmic music, computational beauty."
    )
    
    return prompt, lyrics

def main():
    if len(sys.argv) < 2:
        print('Usage: python code2music.py <code_file> [output_mp3]')
        sys.exit(1)
    
    code_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'code_symphony.mp3'
    
    if not os.path.exists(code_file):
        print(f'[ERROR] File not found: {code_file}')
        sys.exit(1)
    
    print(f'[READING] {code_file}')
    with open(code_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print('[ANALYZING] code structure...')
    features = analyze_code(code)
    print(f'  Lines: {features["total_lines"]}, Functions: {features["func_count"]}, '
          f'Keywords: {features["kw_total"]}, Max indent: {features["max_indent"]}')
    
    print('[MAPPING] to music parameters...')
    params = code_to_music_params(features)
    print(f'  BPM: {params["bpm"]}, Key: {params["key"]}')
    print(f'  Instruments: {params["instrument"]}')
    print(f'  Mood: {params["mood"]}')
    
    prompt, lyrics = generate_prompt_and_lyrics(features, params)
    
    print('[GENERATING] music (this may take 1-2 minutes)...')
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'music-2.6',
        'prompt': prompt,
        'lyrics': lyrics,
        'output_format': 'url',
        'aigc_watermark': False,
        'audio_setting': {
            'sample_rate': 44100,
            'bitrate': 128000,
            'format': 'mp3'
        }
    }
    
    r = requests.post(API_URL, headers=headers, json=payload, timeout=300)
    resp = r.json()
    status = resp.get('base_resp', {}).get('status_code', 'N/A')
    msg = resp.get('base_resp', {}).get('status_msg', 'N/A')
    print(f'[API] Status: {status} - {msg}')
    
    if resp.get('data', {}).get('audio'):
        audio_url = resp['data']['audio']
        print(f'[DOWNLOADING] {audio_url}')
        ar = requests.get(audio_url, timeout=60)
        with open(output_file, 'wb') as f:
            f.write(ar.content)
        size_kb = len(ar.content) // 1024
        print(f'[DONE] {output_file} ({size_kb} KB)')
    else:
        print(f'[ERROR] {json.dumps(resp, ensure_ascii=False)[:500]}')
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
🚀 douyin — 全能抖音处理
ASR: qwen-asr(优先) → whisper-medium(本地降级) → tencentcloud(备选)

用法:
  python3 douyin.py stats                    # 能力统计
  python3 douyin.py video <URL或ID>          # 完整流程
  python3 douyin.py video <URL> --no-asr     # 下载不识别
  python3 douyin.py audio <文件>             # 语音识别
  python3 douyin.py audio <文件> --engine qwen|whisper|tencent
"""

import os, sys, re, subprocess
from pathlib import Path

# ==================== 常量 ====================
WHISPER_PATHS = {
    'small': os.path.expanduser('~/.cache/whisper/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120'),
    'medium': os.path.expanduser('~/.cache/whisper/models--Systran--faster-whisper-medium/snapshots/08e178d48790749d25932bbc082711ddcfdfbc4f'),
    'large-v3': os.path.expanduser('~/.cache/whisper/models--Systran--faster-whisper-large-v3/snapshots/edaa852ec7e145841d8ffdb056a99866b5f0a478'),
}
QWEN_ASR_SCRIPT = os.path.expanduser('~/.openclaw/skills/qwen-asr/scripts/main.py')
MEMORY_CORE = os.path.expanduser('~/.openclaw/skills/memory-manager/scripts/memory_core.py')
OUTPUT_DIR = os.path.expanduser('~/Desktop/douyin-super-agent/')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def log(msg):
    print(f"  {msg}", file=sys.stderr)


def memory_add(content, cat='knowledge'):
    try:
        subprocess.run(
            ['python3', MEMORY_CORE, 'add', content[:200], cat],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        pass


def run_cmd(cmd, timeout=60):
    """执行命令，返回 (returncode, stdout, stderr)"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return -1, '', str(e)


# ==================== 🎙️ ASR 引擎 ====================
def _qwen_asr(path):
    """qwen-asr 远程"""
    if not os.path.isfile(QWEN_ASR_SCRIPT):
        return None, None
    rc, *_ = run_cmd(['which', 'uv'], timeout=5)
    if rc:
        return None, None
    rc, out, err = run_cmd(
        ['uv', 'run', QWEN_ASR_SCRIPT, '-f', path],
        timeout=600,
    )
    out = out.strip()
    if out and len(out) > 10 and 'error' not in out.lower() and 'invalid' not in err.lower():
        return out, 'qwen-asr'
    return None, None


def _whisper_local(path, model='medium'):
    """faster_whisper 本地，首次运行自动下载模型"""
    # 优先用预定义快照路径（速度最快）
    mdl = WHISPER_PATHS.get(model, WHISPER_PATHS.get('small'))
    # 路径不存在 → 让 faster_whisper 自动下载
    if not mdl or not os.path.isdir(mdl) or not os.path.isfile(os.path.join(mdl, 'model.bin')):
        log(f'⏳ whisper-{model} 模型未找到，首次自动下载（约 1-3 GB）...')
        mdl = model
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(mdl, compute_type='int8', cpu_threads=4)
        segs, _info = m.transcribe(
            path, language='zh', beam_size=5, vad_filter=True,
        )
        text = ' '.join(s.text.strip() for s in segs)
        if text:
            return text, f'whisper-{model}'
        return None, None
    except Exception as e:
        log(f'本地 whisper 失败: {e}')
        return None, None


def _tencent_asr(path):
    """腾讯云 ASR（备选）"""
    s = os.path.expanduser(
        '~/.openclaw/skills/tencentcloud-asr/scripts/cli_transcribe.py'
    )
    if not os.path.isfile(s):
        return None, None
    rc, out, _ = run_cmd(['python3', s, path], timeout=600)
    if rc == 0 and out.strip() and len(out.strip()) > 10:
        return out.strip(), 'tencent-asr'
    return None, None


def transcribe(path, prefer='qwen'):
    """三级降级: qwen-asr → whisper-medium → tencentcloud"""
    if prefer == 'qwen':
        text, eng = _qwen_asr(path)
        if text:
            log(f'✅ ASR: {eng}')
            return text, eng
        log('⬇️ qwen-asr 失败，降级到本地 whisper')
        text, eng = _whisper_local(path, 'medium')
        if text:
            log(f'✅ ASR: {eng}')
            return text, eng
        log('⬇️ 降级到腾讯云')
        return _tencent_asr(path)
    elif prefer == 'whisper':
        text, eng = _whisper_local(path, 'medium')
        if text:
            log(f'✅ ASR: {eng}')
            return text, eng
        return _qwen_asr(path) or _tencent_asr(path)
    else:
        text, eng = _whisper_local(path, prefer)
        if text:
            return text, eng
        return _qwen_asr(path) or _tencent_asr(path)


# ==================== 📥 抖音处理 ====================
def douyin_parse(url):
    """MCP 解析抖音链接，返回 (video_id, title, download_url)"""
    vid, title, dl_url = None, '', None

    rc, out, _ = run_cmd(
        ['mcporter', 'call', 'douyin-mcp.parse_douyin_video_info',
         f'share_link={url}'],
        timeout=60,
    )
    if rc == 0:
        # 提取 ID
        m = re.search(r'ID:\s*(\d{15,})', out)
        if m:
            vid = m.group(1)
        # 提取标题
        m = re.search(r'标题:\s*(.+)', out)
        if m:
            t = m.group(1).strip()
            # 过滤 "douyin_ID" 格式的无效标题
            if not re.match(r'^douyin_\d+$', t):
                title = t
        # 提取下载链接
        m = re.search(r'链接:\s*(https?://.+)', out)
        if m:
            d = m.group(1).strip()
            try:
                d = d.encode().decode('unicode_escape')
            except Exception:
                pass
            # 只接受内部 video_id 格式的链接
            if re.search(r'v[0-9a-f]{8,}', d):
                dl_url = d

    return vid, title, dl_url


def douyin_download(url, video_id, save_path):
    """
    MCP 下载抖音视频（含路径修复）
    方案 A: douyin-mcp.download_douyin_video
    方案 B: 直链 curl
    """
    # A. MCP 下载
    rc, out, _ = run_cmd(
        ['mcporter', 'call', 'douyin-mcp.download_douyin_video',
         f'share_link={url}'],
        timeout=300,
    )
    if rc == 0:
        m = re.search(r'文件路径:\s*(.+)', out)
        if m:
            p = m.group(1).strip()
            # 修复相对路径
            if not os.path.isabs(p):
                p = os.path.abspath(p)
            if os.path.isfile(p) and os.path.getsize(p) > 1000:
                return p

    # B. 直链下载（仅当有内部 video_id 时）
    vid, title, dl_url = douyin_parse(url)
    if dl_url:
        log('直链下载...')
        rc = subprocess.run([
            'curl', '-sL', '-o', save_path,
            '-H', 'User-Agent: Mozilla/5.0',
            '-H', 'Referer: https://www.douyin.com/',
            dl_url,
        ], capture_output=True, timeout=180)
        if os.path.isfile(save_path) and os.path.getsize(save_path) > 1000:
            return save_path

    return None


def _extract_audio(video_path):
    """ffmpeg 提取音频"""
    base = Path(video_path).stem
    audio_path = os.path.join(OUTPUT_DIR, f'{base}.mp3')
    rc = subprocess.run([
        'ffmpeg', '-y', '-i', video_path, '-vn',
        '-acodec', 'libmp3lame', '-ab', '128k',
        '-ar', '16000', '-ac', '1', audio_path,
    ], capture_output=True, text=True, timeout=120)
    if rc.returncode == 0 and os.path.isfile(audio_path):
        sz = os.path.getsize(audio_path) // 1024
        log(f'音频已提取: {sz}KB')
        return audio_path
    return None


# ==================== ✍️ 文案处理 + 自动纠错 ====================
def simplify_text(text):
    """去口语化 + 常见错别字自动修正"""
    fixes = {
        '晴天柱': '擎天柱',
        '铁哥': '铁疙瘩',
        '住进': '注入',
        '注进': '注入',
        '这特曼': '这特么',
        'AI减4': 'AI-FSD',
        'AI加4': 'AI-FSD',
        '零言池': '零延迟',
        'Grogg': 'Grok',
        '几倍发凉': '脊背发凉',
        '这几倍发粮': '这脊背发凉',
    }
    for k, v in fixes.items():
        text = text.replace(k, v)
    t = re.sub(r'\b(嗯|啊|呢|呃|哦|哈|呀|嘛)\b', '', text)
    t = re.sub(r'[.。]{2,}', '。', t)
    t = re.sub(r'[！？]{2,}', '！', t)
    t = re.sub(r' {2,}', ' ', t)
    t = re.sub(r'\n{2,}', '\n', t)
    return t.strip()


# ==================== 📄 报告生成 ====================
def format_video(result):
    lines = ['# 📊 抖音视频分析', '']
    title = result.get('title', '未知')
    lines.append(f'## 🎬 {title}')
    if result.get('video_id'):
        lines.append(f"- ID: {result['video_id']}")
    if result.get('asr_engine'):
        lines.append(f"- ASR: {result['asr_engine']}")
    vp = result.get('video_path', '')
    if vp and os.path.exists(vp):
        sz = os.path.getsize(vp) // (1024 * 1024)
        lines.append(f"- 📥 视频: {vp} ({sz}MB)")
    ap = result.get('audio_path', '')
    if ap and os.path.exists(ap):
        sz = os.path.getsize(ap) // 1024
        lines.append(f"- 🎵 音频: {ap} ({sz}KB)")
    if result.get('transcript'):
        lines.append('\n## 📝 语音识别\n')
        t = result['transcript']
        lines.append(t[:800])
        if len(t) > 800:
            lines.append(f'\n...(完整 {len(t)} 字)')
    if result.get('simplified'):
        lines.append('\n## ✍️ 精简文案')
        lines.append(f"```\n{result['simplified'][:800]}\n```")
    if result.get('error'):
        lines.append(f"\n❌ 错误: {result['error']}")
    return '\n'.join(lines)


def save_output(result, fmt='txt'):
    """保存结果文件"""
    vid = result.get('video_id', 'unknown')
    if fmt == 'txt':
        path = os.path.join(OUTPUT_DIR, f'transcript_{vid}.txt')
        text = result.get('simplified') or result.get('transcript', '')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    elif fmt == 'md':
        path = os.path.join(OUTPUT_DIR, f'report_{vid}.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(format_video(result))
    else:
        import json
        path = os.path.join(OUTPUT_DIR, f'result_{vid}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    return path


# ==================== 🔧 主流程 ====================
def process_video(url, asr=True):
    """完整流程: 解析 → 下载 → 音频提取 → ASR → 精简"""
    # 1. 解析
    video_id, title, _ = douyin_parse(url)
    if not video_id:
        return {'error': '无法识别视频，请检查链接'}

    result = {
        'video_id': video_id,
        'title': title or f'抖音视频 {video_id[-6:]}',
    }
    log(f'开始处理: {video_id} 标题: {result["title"]}')

    # 2. 下载
    save_path = os.path.join(OUTPUT_DIR, f'dy_{video_id}.mp4')
    vpath = douyin_download(url, video_id, save_path)
    if not vpath:
        result['error'] = '视频下载失败'
        return result
    result['video_path'] = vpath
    log(f'✅ 视频下载: {os.path.getsize(vpath) // (1024*1024)}MB')

    # 3. 音频提取 + ASR
    if not asr:
        return result

    apath = _extract_audio(vpath)
    if not apath:
        result['error'] = '音频提取失败'
        return result
    result['audio_path'] = apath

    text, engine = transcribe(apath, prefer='qwen')
    if not text:
        result['error'] = '所有 ASR 引擎均失败'
        return result

    result['transcript'] = text
    result['asr_engine'] = engine
    result['simplified'] = simplify_text(text)
    log(f'✅ 完成 ({engine})')
    memory_add(f'视频{video_id[:10]}...({engine}): {text[:100]}...', 'knowledge')
    return result


def process_audio(path, engine='auto'):
    """纯音频处理"""
    if not os.path.isfile(path):
        return {'error': f'文件不存在: {path}'}
    if engine == 'qwen':
        text, eng = transcribe(path, prefer='qwen')
    elif engine == 'whisper':
        text, eng = transcribe(path, prefer='whisper')
    elif engine == 'tencent':
        text, eng = transcribe(path, prefer='tencent')
    else:
        text, eng = transcribe(path, prefer='qwen')
    if text:
        memory_add(f'音频转写({eng}): {text[:80]}...', 'knowledge')
        return {
            'text': text,
            'engine': eng,
            'simplified': simplify_text(text),
        }
    return {'error': '所有 ASR 引擎均失败'}


# ==================== 🖥️ CLI 入口 ====================
def main():
    if len(sys.argv) < 2:
        print('用法: python3 douyin.py <命令> [参数]')
        print('  video  <URL或ID>              抖音视频处理')
        print('  audio  <文件>                  ASR 语音识别')
        print('  stats                           能力统计')
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'stats':
        print('📊 douyin 能力:')
        print()
        for name, desc in [
            ('qwen-asr', '远程 Gradio（优先）'),
            ('whisper-medium', '本地 1.5GB（降级）'),
            ('whisper-small', '本地 500MB（快速）'),
            ('whisper-large-v3', '本地 3GB（精准）'),
            ('tencentcloud-asr', '云端（备选）'),
            ('douyin-mcp', '视频解析 + 下载'),
            ('ffmpeg', '音频提取'),
            ('edge-tts', '文字转语音'),
            ('memory-manager', '自动存储'),
        ]:
            print(f'  ✅ {name:20s}{desc}')

    elif cmd == 'video':
        if len(sys.argv) < 3:
            print('用法: python3 douyin.py video <URL或ID>')
            sys.exit(1)
        url = sys.argv[2]
        no_asr = '--no-asr' in sys.argv
        r = process_video(url, asr=not no_asr)
        print(format_video(r))
        save_output(r, 'txt')
        save_output(r, 'json')
        txt = os.path.join(OUTPUT_DIR, f"transcript_{r.get('video_id', '')}.txt")
        if os.path.exists(txt):
            print(f'\n✅ 文件已保存: {txt}')

    elif cmd == 'audio':
        if len(sys.argv) < 3:
            print('用法: python3 douyin.py audio <文件>')
            sys.exit(1)
        path = sys.argv[2]
        engine = 'qwen'
        if '--engine' in sys.argv:
            idx = sys.argv.index('--engine')
            engine = sys.argv[idx + 1]
        r = process_audio(path, engine)
        if 'error' not in r:
            print(f"🎙️ ASR: {r['engine']}")
            print(f"\n## 📝 识别结果\n{r['text'][:500]}")
            print(f"\n## ✍️ 精简文案\n{r['simplified'][:500]}")
            out = os.path.join(OUTPUT_DIR, f"transcript_{Path(path).stem}.txt")
            with open(out, 'w', encoding='utf-8') as f:
                f.write(r['simplified'])
            print(f'\n✅ 已保存: {out}')
        else:
            print(f"❌ {r['error']}")

    else:
        print(f'❌ 未知命令: {cmd}')


if __name__ == '__main__':
    main()

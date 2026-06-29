#!/usr/bin/env python3
"""
Batch transcribe videos: download → extract audio → Whisper → .md.

Supports both Bilibili collections and YouTube playlists.

Usage:
    python3 transcribe_collection.py collection.json --output ./transcripts --model small
    python3 transcribe_collection.py collection.json --output ./transcripts --model large-v3 --device cpu
"""
import sys, os, json, argparse, subprocess, re, glob

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


def find_latest_mp4(temp_dir):
    files = [f for f in os.listdir(temp_dir)
             if f.endswith('.mp4') and not f.endswith('.download')]
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(temp_dir, f)), reverse=True)
    return os.path.join(temp_dir, files[0])


def run_cmd(args, timeout=300):
    try:
        result = subprocess.run(args, capture_output=True, timeout=timeout)
        stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ''
        stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ''
        return result.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'timeout'
    except FileNotFoundError as e:
        return -1, '', str(e)


def download_bilibili(bvid, temp_dir):
    """Download Bilibili video via you-get, fallback yt-dlp"""
    url = f'https://www.bilibili.com/video/{bvid}'

    # Try you-get first
    rc, _, _ = run_cmd(['you-get', '-o', temp_dir, url], timeout=600)
    if rc != 0:
        rc, _, _ = run_cmd([
            'you-get', '-o', temp_dir, '--format=dash-flv360-AVC', url
        ], timeout=600)
    if rc == 0:
        mp4 = find_latest_mp4(temp_dir)
        if mp4:
            renamed = os.path.join(temp_dir, f'{bvid}.mp4')
            if mp4 != renamed:
                if os.path.exists(renamed):
                    os.remove(mp4)
                else:
                    os.rename(mp4, renamed)
            return True

    # Fallback to yt-dlp
    print('  you-get failed, trying yt-dlp...')
    out_path = os.path.join(temp_dir, f'{bvid}.mp4')
    rc, _, _ = run_cmd([
        'yt-dlp', '-o', out_path, '-f', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        '--merge-output-format', 'mp4', url
    ], timeout=600)
    return rc == 0


def download_youtube(vid, temp_dir):
    """Download YouTube video via yt-dlp"""
    out_path = os.path.join(temp_dir, f'{vid}.%(ext)s')
    url = f'https://www.youtube.com/watch?v={vid}'

    rc, _, err = run_cmd([
        'yt-dlp', '-o', out_path, '-f', 'bestaudio/best',
        '--extract-audio', '--audio-format', 'wav',
        '--audio-quality', '0',
        url
    ], timeout=600)

    if rc != 0:
        print(f'  yt-dlp failed: {err[:200]}')

    # Find the downloaded wav
    wav_path = os.path.join(temp_dir, f'{vid}.wav')
    if os.path.exists(wav_path):
        return True

    # Find any .wav in temp dir
    wavs = glob.glob(os.path.join(temp_dir, f'{vid}.*.wav'))
    if wavs:
        os.rename(wavs[0], wav_path)
        return True

    return False


def extract_wav(video_path, wav_path, timeout=300):
    """Extract 16kHz mono WAV from video"""
    rc, _, _ = run_cmd([
        'ffmpeg', '-y', '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le',
        '-ar', '16000', '-ac', '1',
        wav_path
    ], timeout=timeout)
    return rc == 0


def transcribe_audio(wav_path, txt_path, model, device, timeout=3600):
    """Transcribe audio with faster-whisper"""
    rc, stdout, stderr = run_cmd([
        sys.executable, '-c', f'''
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from faster_whisper import WhisperModel
model = WhisperModel("{model}", device="{device}",
    compute_type="float16" if "{device}"=="cuda" else "int8")
segments, info = model.transcribe(r"{wav_path}", beam_size=5, vad_filter=True)
for seg in segments:
    print(seg.text)
''', timeout=timeout)

    text = stdout.strip() or stderr.strip()
    if text:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return text
    return ''


def process_video(v, output_dir, model, device, downloader, skip_download, temp_dir):
    """Process one video"""
    bvid = v.get('bvid') or v.get('id', '')
    title = v.get('title', bvid)
    duration = v.get('duration', 0)
    platform = v.get('platform', 'bilibili')
    duration_str = f'{duration // 60}分{duration % 60}秒' if duration else ''

    print(f'\n  [{bvid}] {title[:50]} ({duration_str}, {platform})')

    vid_key = bvid
    wav_path = os.path.join(temp_dir, f'{vid_key}.wav')
    txt_path = os.path.join(temp_dir, f'{vid_key}.txt')

    # --- 1. Download & extract audio ---
    if not skip_download:
        if platform == 'youtube':
            if not download_youtube(bvid, temp_dir):
                print(f'  [FAIL] YouTube download failed')
                return False
            # yt-dlp may have already extracted the wav
        else:
            if not download_bilibili(bvid, temp_dir):
                print(f'  [FAIL] Bilibili download failed')
                return False

            mp4_path = os.path.join(temp_dir, f'{vid_key}.mp4')
            if os.path.exists(mp4_path) and not os.path.exists(wav_path):
                if not extract_wav(mp4_path, wav_path):
                    print(f'  [FAIL] ffmpeg failed')
                    return False

    # --- 2. Transcribe ---
    text = ''
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f'  [OK] Already transcribed: {len(text)} chars')
    elif os.path.exists(wav_path) or any(f.startswith(vid_key) and f.endswith('.wav') for f in os.listdir(temp_dir)):
        # Find actual wav path
        actual_wav = wav_path
        if not os.path.exists(actual_wav):
            wavs = glob.glob(os.path.join(temp_dir, f'{vid_key}.*.wav'))
            if wavs:
                actual_wav = wavs[0]
        if os.path.exists(actual_wav):
            text = transcribe_audio(actual_wav, txt_path, model, device)
            if text:
                print(f'  [OK] Transcribed: {len(text)} chars')
            else:
                print(f'  [FAIL] Transcription empty')
                return False
        else:
            print(f'  [FAIL] No audio file found')
            return False
    else:
        print(f'  [FAIL] No audio to transcribe')
        return False

    # --- 3. Save as .md ---
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title[:60]).strip()
    if not safe_title:
        safe_title = vid_key

    md_file = os.path.join(output_dir, f'{safe_title}.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n')
        f.write(f'> ID: {vid_key} | Platform: {platform}')
        if duration:
            f.write(f' | 时长: {duration_str}')
        f.write('\n\n')
        if text:
            f.write(text)

    print(f'  [OK] Saved: {os.path.basename(md_file)}')

    # --- 4. Cleanup ---
    for pattern in [f'{vid_key}.mp4', f'{vid_key}.wav', f'{vid_key}.*.mp4', f'{vid_key}.*.wav']:
        for f in glob.glob(os.path.join(temp_dir, pattern)):
            try:
                os.remove(f)
            except:
                pass

    return True


def main():
    parser = argparse.ArgumentParser(description='Batch transcribe videos from Bilibili or YouTube')
    parser.add_argument('videos_json', help='Video list JSON from fetch_collection.py')
    parser.add_argument('--output', '-o', default='./transcripts', help='Output directory')
    parser.add_argument('--model', default='small',
                        choices=['tiny', 'base', 'small', 'medium', 'large-v3'],
                        help='Whisper model size')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'],
                        help='Compute device')
    parser.add_argument('--temp-dir', default='./.temp', help='Temp directory')
    parser.add_argument('--progress', default='progress.json', help='Progress JSON')
    parser.add_argument('--skip-download', action='store_true', help='Skip download')
    parser.add_argument('--limit', type=int, default=0, help='Max videos to process')
    args = parser.parse_args()

    with open(args.videos_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    videos = data.get('videos', [])
    if not videos:
        print('No videos in JSON')
        sys.exit(1)

    coll_name = data.get('collection', {}).get('name', 'unknown')
    platform = data.get('collection', {}).get('platform', 'unknown')
    print(f'Loaded {len(videos)} videos from {coll_name} ({platform})')
    total_s = sum(v.get('duration', 0) for v in videos)
    print(f'Total duration: {total_s//3600}h{total_s%3600//60}m')

    os.makedirs(args.output, exist_ok=True)
    os.makedirs(args.temp_dir, exist_ok=True)

    done = {}
    if os.path.exists(args.progress):
        with open(args.progress, 'r') as f:
            done = json.load(f)
    done_set = set(done.get('done', []))

    processed = 0
    for i, v in enumerate(videos):
        if args.limit and processed >= args.limit:
            break

        bvid = v.get('bvid') or v.get('id', '')
        if bvid in done_set:
            print(f'[{i+1}/{len(videos)}] {bvid} skipped')
            continue

        ok = process_video(v, args.output, args.model, args.device,
                           args.downloader if hasattr(args, 'downloader') else 'auto',
                           args.skip_download, args.temp_dir)
        if ok:
            done_set.add(bvid)
            done['done'] = list(done_set)
            done['last'] = bvid
            with open(args.progress, 'w') as f:
                json.dump(done, f)
            processed += 1
        else:
            print(f'[WARN] {bvid} failed')

    print(f'\nDone: {len(done_set)}/{len(videos)}')
    print(f'Output: {args.output}')


if __name__ == '__main__':
    main()

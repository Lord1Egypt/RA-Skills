#!/usr/bin/env python3
import json, shutil, subprocess, sys
from pathlib import Path

USAGE = "Usage: audio_to_article_pipeline.py <source.(txt|md|m4a|mp3|ogg|wav)> <output-prefix> [coverImage] [qrImage]"
BASE = Path('/Users/meizi/.openclaw/workspace/skills/audio-to-wechat-article/scripts')
WHISPER = Path('/Users/meizi/.openclaw/workspace/skills/meeting-minutes-whisper/scripts/transcribe_and_minutes.py')


def run(cmd):
    subprocess.run(cmd, check=True)


def ensure_text_source(src: Path, prefix: Path) -> Path:
    if src.suffix.lower() in ['.txt', '.md']:
        return src
    out_dir = prefix.parent / (prefix.name + '-transcribe')
    out_dir.mkdir(parents=True, exist_ok=True)
    model = 'tiny'
    if src.stat().st_size > 25 * 1024 * 1024:
        model = 'base'
    run(['/usr/bin/python3', str(WHISPER), str(src), '--language', 'Chinese', '--model', model, '--title', prefix.name, '--output-dir', str(out_dir)])
    candidates = sorted(out_dir.glob('*.txt'))
    if not candidates:
        raise RuntimeError('No transcript txt produced')
    return candidates[0]


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    src = Path(sys.argv[1])
    prefix = Path(sys.argv[2])
    cover = sys.argv[3] if len(sys.argv) > 3 else ''
    qr = sys.argv[4] if len(sys.argv) > 4 else ''

    text_src = ensure_text_source(src, prefix)
    brief_path = prefix.with_suffix('.brief.json')
    article_json = prefix.with_suffix('.article.json')
    markdown_path = prefix.with_suffix('.md')

    run(['/usr/bin/python3', str(BASE / 'build_article_brief.py'), str(text_src), str(brief_path)])
    run(['/usr/bin/python3', str(BASE / 'draft_article_json.py'), str(text_src), str(article_json)])
    run(['/usr/bin/python3', str(BASE / 'compose_wechat_markdown.py'), str(article_json), str(markdown_path), cover])

    result = {
        'source_input': str(src),
        'text_source': str(text_src),
        'brief_json': str(brief_path),
        'article_json': str(article_json),
        'markdown': str(markdown_path),
        'qr_image': qr,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

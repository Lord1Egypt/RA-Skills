#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CFG_PATH = Path.home() / '.openclaw' / 'openclaw.json'


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def load_audio_cli_config():
    if not CFG_PATH.exists():
        fail(f'Missing config file: {CFG_PATH}', 2)
    cfg = json.loads(CFG_PATH.read_text())
    models = cfg.get('tools', {}).get('media', {}).get('audio', {}).get('models', [])
    if not models:
        fail('No audio transcription model configured under tools.media.audio.models', 3)
    model = models[0]
    if model.get('type') != 'cli':
        fail('First configured audio model is not type=cli', 4)
    return model


def main():
    ap = argparse.ArgumentParser(description='Transcribe local audio with the Whisper CLI configured in ~/.openclaw/openclaw.json')
    ap.add_argument('media_path', help='Path to local audio file')
    args = ap.parse_args()

    media_path = Path(args.media_path).expanduser().resolve()
    if not media_path.exists():
        fail(f'Audio file not found: {media_path}', 5)

    model = load_audio_cli_config()
    cmd = [model['command']]
    with tempfile.TemporaryDirectory(prefix='openclaw-stt-') as outdir:
        rendered = []
        for token in model.get('args', []):
            rendered.append(token.replace('{{OutputDir}}', outdir).replace('{{MediaPath}}', str(media_path)))
        cmd.extend(rendered)
        subprocess.run(cmd, check=True)
        txt_path = Path(outdir) / f'{media_path.stem}.txt'
        if not txt_path.exists():
            candidates = list(Path(outdir).glob('*.txt'))
            if not candidates:
                fail('Transcription finished but no .txt output was found', 6)
            txt_path = candidates[0]
        text = txt_path.read_text().strip()
        print(json.dumps({
            'ok': True,
            'mediaPath': str(media_path),
            'text': text,
            'transcriptPath': str(txt_path),
        }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

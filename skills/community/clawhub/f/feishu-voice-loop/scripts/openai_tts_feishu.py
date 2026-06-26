#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = 'gpt-4o-mini-tts'
DEFAULT_VOICE = 'alloy'
DEFAULT_STYLE = (
    'Speak in Chinese like a young Japanese-style male actor vibe in a private conversation, '
    'centered on tenderness with a hint of flirtation. Warm, soft, intimate, slightly husky, '
    'youthful, close to the listener, with gentle affection and just a subtle teasing pull. '
    'Natural human delivery, smooth and quiet, not announcer-like, not formal, not exaggerated.'
)


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def post_json(url, data, headers=None, timeout=60):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={**(headers or {}), 'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        fail(f'HTTP {e.code} calling {url}\n{body}', 10)


def post_multipart_file(url, fields, file_field, file_path, mime, headers=None, timeout=120):
    boundary = '----OpenClawBoundary7MA4YWxkTrZu0gW'
    body = bytearray()
    for k, v in fields.items():
        body.extend(f'--{boundary}\r\n'.encode())
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    body.extend(f'--{boundary}\r\n'.encode())
    body.extend(f'Content-Disposition: form-data; name="{file_field}"; filename="{Path(file_path).name}"\r\n'.encode())
    body.extend(f'Content-Type: {mime}\r\n\r\n'.encode())
    body.extend(Path(file_path).read_bytes())
    body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode())
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={**(headers or {}), 'Content-Type': f'multipart/form-data; boundary={boundary}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        fail(f'HTTP {e.code} calling {url}\n{body}', 11)


def build_parser():
    ap = argparse.ArgumentParser(description='Generate OpenAI TTS audio and send it as a Feishu audio message.')
    ap.add_argument('--to', required=True, help='Feishu open_id of the recipient')
    ap.add_argument('--text', required=True, help='Text to synthesize')
    ap.add_argument('--voice', default=DEFAULT_VOICE)
    ap.add_argument('--model', default=DEFAULT_MODEL)
    ap.add_argument('--instructions', default=DEFAULT_STYLE)
    ap.add_argument('--app-id', default=None, help='Optional Feishu app id override')
    ap.add_argument('--app-secret', default=None, help='Optional Feishu app secret override')
    ap.add_argument('--keep', action='store_true', help='Keep temp wav/ogg files and print their paths')
    return ap


def load_feishu_credentials(args):
    if args.app_id and args.app_secret:
        return args.app_id, args.app_secret
    cfg_path = Path.home() / '.openclaw' / 'openclaw.json'
    if not cfg_path.exists():
        fail(f'Missing config file: {cfg_path}', 2)
    cfg = json.loads(cfg_path.read_text())
    feishu = cfg.get('channels', {}).get('feishu', {})
    app_id = args.app_id or feishu.get('appId')
    app_secret = args.app_secret or feishu.get('appSecret')
    if not app_id or not app_secret:
        fail('Missing Feishu appId/appSecret. Set them in ~/.openclaw/openclaw.json or pass --app-id/--app-secret.', 3)
    return app_id, app_secret


def main():
    args = build_parser().parse_args()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        fail('Missing OPENAI_API_KEY', 1)
    app_id, app_secret = load_feishu_credentials(args)

    temp_ctx = tempfile.TemporaryDirectory(prefix='openai-feishu-voice-')
    tmp = Path(temp_ctx.name)
    wav_path = tmp / 'speech.wav'
    ogg_path = tmp / 'speech.ogg'

    try:
        req = urllib.request.Request(
            'https://api.openai.com/v1/audio/speech',
            data=json.dumps({
                'model': args.model,
                'voice': args.voice,
                'input': args.text,
                'format': 'wav',
                'instructions': args.instructions,
            }).encode(),
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                wav_path.write_bytes(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')
            fail(f'HTTP {e.code} calling OpenAI audio/speech\n{body}', 12)

        subprocess.run([
            '/opt/homebrew/bin/ffmpeg', '-y', '-i', str(wav_path),
            '-ac', '1', '-ar', '16000', '-c:a', 'libopus', '-b:a', '24k', str(ogg_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        duration_sec = subprocess.check_output([
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(ogg_path)
        ], text=True).strip()
        duration_ms = round(float(duration_sec) * 1000)

        token_raw, _ = post_json(
            'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
            {'app_id': app_id, 'app_secret': app_secret},
        )
        token_json = json.loads(token_raw)
        tenant_token = token_json.get('tenant_access_token')
        if not tenant_token:
            fail(json.dumps(token_json, ensure_ascii=False, indent=2), 13)

        upload_raw, _ = post_multipart_file(
            'https://open.feishu.cn/open-apis/im/v1/files',
            {'file_type': 'opus', 'file_name': 'speech.ogg', 'duration': str(duration_ms)},
            'file', str(ogg_path), 'audio/ogg',
            headers={'Authorization': f'Bearer {tenant_token}'},
        )
        upload_json = json.loads(upload_raw)
        file_key = upload_json.get('data', {}).get('file_key')
        if not file_key:
            fail(json.dumps(upload_json, ensure_ascii=False, indent=2), 14)

        send_raw, _ = post_json(
            'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
            {
                'receive_id': args.to,
                'msg_type': 'audio',
                'content': json.dumps({'file_key': file_key}, ensure_ascii=False),
            },
            headers={'Authorization': f'Bearer {tenant_token}'},
        )
        send_json = json.loads(send_raw)
        result = {
            'ok': True,
            'model': args.model,
            'voice': args.voice,
            'durationMs': duration_ms,
            'to': args.to,
            'send': send_json,
        }
        if args.keep:
            result['wavPath'] = str(wav_path)
            result['oggPath'] = str(ogg_path)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            temp_ctx = None
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        if temp_ctx is not None:
            temp_ctx.cleanup()


if __name__ == '__main__':
    main()

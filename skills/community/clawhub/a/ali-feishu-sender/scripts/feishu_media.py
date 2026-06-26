# -*- coding: utf-8 -*-
"""
飞书多媒体发送工具 - Send multimedia content to Feishu (Lark)
Supports: image, audio (voice bubble), video (inline player), rich text with media, card
"""
import urllib.request, json, uuid, os, subprocess, sys, argparse

DEFAULT_APP_ID = os.environ.get('FEISHU_APP_ID', '')
DEFAULT_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')
DEFAULT_OPEN_ID = os.environ.get('FEISHU_OPEN_ID', '')
DEFAULT_FFMPEG = r'D:\ffmpeg\bin\ffmpeg.exe'
DEFAULT_FFPROBE = r'D:\ffmpeg\bin\ffprobe.exe'
UPLOAD_API = 'https://open.feishu.cn/open-apis/im/v1/files'
IMAGE_UPLOAD_API = 'https://open.feishu.cn/open-apis/im/v1/images'
MSG_API = 'https://open.feishu.cn/open-apis/im/v1/messages'
TOKEN_API = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'


def get_token(app_id=None, app_secret=None):
    data = json.dumps({'app_id': app_id or DEFAULT_APP_ID, 'app_secret': app_secret or DEFAULT_APP_SECRET}).encode()
    req = urllib.request.Request(TOKEN_API, data=data, headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['tenant_access_token']


def _safe_response(resp_or_error):
    """Normalize API response"""
    if isinstance(resp_or_error, dict) and 'code' in resp_or_error:
        return resp_or_error
    return {'code': -1, 'msg': str(resp_or_error)}


def _multipart_upload(url, form_fields, file_field, token):
    """
    Upload multipart form data.
    form_fields: dict of {name: string_value}
    file_field: tuple of (field_name, file_path)
    """
    boundary = uuid.uuid4().hex
    lines = []
    for k, v in form_fields.items():
        lines.append('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v))
    fname = os.path.basename(file_field[1])
    lines.append('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n' % (boundary, file_field[0], fname))
    header = ''.join(lines).encode()
    with open(file_field[1], 'rb') as f:
        file_data = f.read()
    footer = ('\r\n--%s--\r\n' % boundary).encode()
    body = header + file_data + footer
    req = urllib.request.Request(url, data=body, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'multipart/form-data; boundary=' + boundary
    })
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return json.loads(raw)
        except:
            return {'code': -1, 'msg': 'HTTP %d: %s' % (e.code, raw[:300])}


def _send_msg(token, open_id, msg_type, content, receive_type='open_id'):
    url = MSG_API + '?' + urllib.parse.urlencode({'receive_id_type': receive_type})
    body = json.dumps({'receive_id': open_id, 'msg_type': msg_type, 'content': json.dumps(content)}).encode()
    req = urllib.request.Request(url, data=body, headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return json.loads(raw)
        except:
            return {'code': -1, 'msg': 'HTTP %d: %s' % (e.code, raw[:300])}


def _get_duration_ms(filepath, ffprobe=None):
    ffprobe = ffprobe or DEFAULT_FFPROBE
    r = subprocess.run([ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_format', filepath],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return int(float(json.loads(r.stdout)['format']['duration']) * 1000)


def _to_opus(src, dst, ffmpeg=None):
    ffmpeg = ffmpeg or DEFAULT_FFMPEG
    r = subprocess.run([ffmpeg, '-y', '-i', src, '-c:a', 'libopus', '-b:a', '32k', dst], capture_output=True)
    return r.returncode == 0 and os.path.exists(dst)


def _faststart_mp4(src, dst, ffmpeg=None):
    ffmpeg = ffmpeg or DEFAULT_FFMPEG
    r = subprocess.run([ffmpeg, '-y', '-i', src, '-c', 'copy', '-movflags', '+faststart', dst], capture_output=True)
    return r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 0


def _upload_image(filepath, token):
    boundary = uuid.uuid4().hex
    ext = os.path.splitext(filepath)[1].lower()
    mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}.get(ext, 'image/png')
    header = (
        '--%s\r\nContent-Disposition: form-data; name="image_type"\r\n\r\nmessage\r\n'
        '--%s\r\nContent-Disposition: form-data; name="image"; filename="%s"\r\nContent-Type: %s\r\n\r\n'
    ) % (boundary, boundary, os.path.basename(filepath), mime)
    with open(filepath, 'rb') as f:
        file_data = f.read()
    body = header.encode() + file_data + ('\r\n--%s--\r\n' % boundary).encode()
    req = urllib.request.Request(IMAGE_UPLOAD_API, data=body, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'multipart/form-data; boundary=' + boundary
    })
    return json.loads(urllib.request.urlopen(req).read())['data']['image_key']


# ============ PUBLIC API ============

def send_text(text, open_id=None, token=None, **kwargs):
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'text', {'text': text})


def send_image(filepath, open_id=None, token=None, **kwargs):
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    image_key = _upload_image(filepath, token)
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'image', {'image_key': image_key})


def send_audio(filepath, open_id=None, token=None, **kwargs):
    """Send audio as native voice bubble. Auto-converts to opus, always includes duration."""
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    ffmpeg = kwargs.get('ffmpeg')
    ffprobe = kwargs.get('ffprobe')

    # Convert to opus if needed
    if not filepath.lower().endswith('.opus'):
        opus_path = os.path.splitext(filepath)[0] + '.opus'
        if not _to_opus(filepath, opus_path, ffmpeg):
            return {'code': -1, 'msg': 'Failed to convert to opus'}
        filepath = opus_path

    duration = _get_duration_ms(filepath, ffprobe) or 0
    r = _multipart_upload(UPLOAD_API,
        {'file_type': 'opus', 'file_name': os.path.basename(filepath), 'duration': str(duration)},
        ('file', filepath), token)
    if r['code'] != 0:
        return r
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'audio', {'file_key': r['data']['file_key']})


def send_video(filepath, cover_image=None, open_id=None, token=None, **kwargs):
    """Send video as inline player. Auto-applies faststart, always includes duration."""
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    ffmpeg = kwargs.get('ffmpeg')
    ffprobe = kwargs.get('ffprobe')

    # Ensure mp4 + faststart
    if not filepath.lower().endswith('.mp4'):
        mp4_path = os.path.splitext(filepath)[0] + '.mp4'
        subprocess.run([ffmpeg or DEFAULT_FFMPEG, '-y', '-i', filepath, '-c', 'copy', '-movflags', '+faststart', mp4_path], capture_output=True)
        if os.path.exists(mp4_path):
            filepath = mp4_path
    else:
        fixed = os.path.splitext(filepath)[0] + '_fs.mp4'
        if _faststart_mp4(filepath, fixed, ffmpeg):
            filepath = fixed

    duration = _get_duration_ms(filepath, ffprobe) or 0
    r = _multipart_upload(UPLOAD_API,
        {'file_type': 'mp4', 'file_name': os.path.basename(filepath), 'duration': str(duration)},
        ('file', filepath), token)
    if r['code'] != 0:
        return r

    image_key = _upload_image(cover_image, token) if cover_image and os.path.exists(cover_image) else None
    content = {'file_key': r['data']['file_key']}
    if image_key:
        content['image_key'] = image_key
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'media', content)


def send_rich_text(title, elements, open_id=None, token=None, **kwargs):
    """
    Send rich text (post) message.
    elements: list of paragraphs, each paragraph is list of tag dicts.
    Tags: text, a (link), at, img, media, hr, emotion
    Media tag: {'tag': 'media', 'file_key': '...', 'image_key': '...'}
    """
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'post',
                     {'zh_cn': {'title': title, 'content': elements}})


def send_card(title, elements, header_color='orange', open_id=None, token=None, **kwargs):
    """Send interactive card message."""
    token = token or get_token(kwargs.get('app_id'), kwargs.get('app_secret'))
    return _send_msg(token, open_id or DEFAULT_OPEN_ID, 'interactive', {
        'config': {'wide_screen_mode': True},
        'header': {'title': {'tag': 'plain_text', 'content': title}, 'template': header_color},
        'elements': elements
    })


def main():
    parser = argparse.ArgumentParser(description='Feishu media sender')
    sub = parser.add_subparsers(dest='cmd')
    p = sub.add_parser('text'); p.add_argument('message')
    p = sub.add_parser('image'); p.add_argument('file')
    p = sub.add_parser('audio'); p.add_argument('file')
    p = sub.add_parser('video'); p.add_argument('file'); p.add_argument('--cover', default=None)
    args = parser.parse_args()
    funcs = {'text': lambda: send_text(args.message), 'image': lambda: send_image(args.file),
             'audio': lambda: send_audio(args.file), 'video': lambda: send_video(args.file, args.cover)}
    if args.cmd in funcs:
        print(json.dumps(funcs[args.cmd](), ensure_ascii=False, indent=2))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

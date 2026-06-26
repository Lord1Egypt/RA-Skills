#!/usr/bin/env python3
import argparse
import html
import json
import mimetypes
import os
import random
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

AUDIO_EXTS = {'.mp3', '.m4a', '.aac', '.wav', '.flac', '.aiff', '.ogg'}
STATE_DIR = Path.home() / '.openclaw' / 'state'
STATE_FILE = STATE_DIR / 'denon-dlna-push.json'
DEFAULT_BASE = 'http://{host}:60006'


def state_load():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def state_save(data):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def is_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()


def scan_audio(root: Path):
    files = []
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in AUDIO_EXTS:
            files.append(p)
    return sorted(files, key=lambda p: str(p).lower())


def choose(files, mode, query=None, count=1):
    if mode == 'random':
        if not files:
            return []
        return random.sample(files, max(1, min(count, len(files))))
    if mode == 'match':
        q = (query or '').strip().lower()
        return [f for f in files if q in f.name.lower() or q in str(f).lower()]
    raise ValueError(f'unsupported mode: {mode}')


def content_type_for(path: Path) -> str:
    t, _ = mimetypes.guess_type(str(path))
    if t:
        return t
    return 'application/octet-stream'


def didl_for(url: str, path: Path) -> str:
    title = escape(path.stem)
    ctype = content_type_for(path)
    protocol_info = f'http-get:*:{ctype}:*'
    return (
        '<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/">'
        '<item id="0" parentID="0" restricted="1">'
        f'<dc:title>{title}</dc:title>'
        '<upnp:class>object.item.audioItem.musicTrack</upnp:class>'
        f'<res protocolInfo="{escape(protocol_info)}">{escape(url)}</res>'
        '</item>'
        '</DIDL-Lite>'
    )


def soap_envelope(service, action, args):
    body = ''.join(f'<{k}>{html.escape(str(v))}</{k}>' for k, v in args.items())
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
        's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
        '<s:Body>'
        f'<u:{action} xmlns:u="{service}">{body}</u:{action}>'
        '</s:Body>'
        '</s:Envelope>'
    ).encode('utf-8')


def soap_post(base_url, control_url, service, action, args, timeout=8):
    data = soap_envelope(service, action, args)
    req = urllib.request.Request(
        base_url + control_url,
        data=data,
        method='POST',
        headers={
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': f'"{service}#{action}"',
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', 'ignore')


def start_http_server(root_dir: Path, host: str, port: int):
    cmd = [sys.executable, '-m', 'http.server', str(port), '--bind', host, '--directory', str(root_dir)]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    if proc.poll() is not None:
        raise RuntimeError('HTTP server exited immediately')
    return proc


def print_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def cmd_scan(args):
    root = Path(os.path.expanduser(args.root)).resolve()
    files = scan_audio(root)
    print_json({'root': str(root), 'count': len(files), 'sample': [str(p) for p in files[:args.limit]]})
    return 0


def cmd_list(args):
    root = Path(os.path.expanduser(args.root)).resolve()
    files = scan_audio(root)
    q = (args.query or '').strip().lower()
    if q:
        files = [f for f in files if q in f.name.lower() or q in str(f).lower()]
    print_json({'root': str(root), 'count': len(files), 'matches': [str(p) for p in files[:args.limit]]})
    return 0


def resolve_selection(args):
    if args.file:
        p = Path(os.path.expanduser(args.file)).resolve()
        if not p.exists():
            raise FileNotFoundError(p)
        return [p]
    root = Path(os.path.expanduser(args.root)).resolve()
    files = scan_audio(root)
    return choose(files, args.mode, args.query, args.count)


def cmd_push(args):
    tracks = resolve_selection(args)
    if not tracks:
        print('error: no tracks selected', file=sys.stderr)
        return 1
    track = tracks[0]
    serve_ip = args.serve_host or local_ip()
    serve_port = args.serve_port
    denon = args.denon_host
    if not denon and not args.base_url:
        raise ValueError('Provide --denon-host or --base-url')
    base = args.base_url or DEFAULT_BASE.format(host=denon)

    http_root = track.parent
    server = start_http_server(http_root, serve_ip, serve_port)
    file_url = f'http://{serve_ip}:{serve_port}/{urllib.request.pathname2url(track.name)}'
    metadata = didl_for(file_url, track)

    state = {
        'httpPid': server.pid,
        'httpRoot': str(http_root),
        'file': str(track),
        'fileUrl': file_url,
        'denonHost': denon,
        'baseUrl': base,
        'updatedAt': int(time.time()),
    }
    state_save(state)

    try:
        set_resp = soap_post(base, '/upnp/control/renderer_dvc/AVTransport', 'urn:schemas-upnp-org:service:AVTransport:1', 'SetAVTransportURI', {
            'InstanceID': 0,
            'CurrentURI': file_url,
            'CurrentURIMetaData': metadata,
        })
        play_resp = soap_post(base, '/upnp/control/renderer_dvc/AVTransport', 'urn:schemas-upnp-org:service:AVTransport:1', 'Play', {
            'InstanceID': 0,
            'Speed': 1,
        })
    except Exception:
        try:
            os.kill(server.pid, signal.SIGTERM)
        except Exception:
            pass
        raise

    print_json({
        'selected': [str(t) for t in tracks],
        'pushed': str(track),
        'fileUrl': file_url,
        'httpPid': server.pid,
        'setResponse': set_resp[:800],
        'playResponse': play_resp[:800],
        'note': 'HTTP server stays running so the Denon can fetch the file. Use stop to terminate it.',
    })
    return 0


def cmd_stop(args):
    st = state_load()
    base = st.get('baseUrl')
    if not base:
        denon = st.get('denonHost')
        if not denon:
            print_json({'error': 'No saved baseUrl or denonHost. Nothing to stop.'})
            return 1
        base = DEFAULT_BASE.format(host=denon)
    try:
        resp = soap_post(base, '/upnp/control/renderer_dvc/AVTransport', 'urn:schemas-upnp-org:service:AVTransport:1', 'Stop', {
            'InstanceID': 0,
        })
    except Exception as e:
        resp = f'stop rpc failed: {e}'
    pid = st.get('httpPid')
    killed = False
    if pid and is_running(pid):
        try:
            os.kill(pid, signal.SIGTERM)
            killed = True
        except Exception:
            pass
    st['updatedAt'] = int(time.time())
    st['stopped'] = True
    state_save(st)
    print_json({'transportStop': resp[:800] if isinstance(resp, str) else resp, 'httpPid': pid, 'serverKilled': killed})
    return 0


def cmd_status(args):
    st = state_load()
    if not st:
        print_json({'state': 'empty'})
        return 0
    pid = st.get('httpPid')
    st['httpRunning'] = bool(pid and is_running(pid))
    print_json(st)
    return 0


def main():
    parser = argparse.ArgumentParser(description='Experimental DLNA push of local audio files to a Denon MediaRenderer.')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p = sub.add_parser('scan')
    p.add_argument('--root', required=True)
    p.add_argument('--limit', type=int, default=100)
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser('list')
    p.add_argument('--root', required=True)
    p.add_argument('--query')
    p.add_argument('--limit', type=int, default=50)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser('push')
    p.add_argument('--root')
    p.add_argument('--file')
    p.add_argument('--mode', choices=['random', 'match'], default='match')
    p.add_argument('--query')
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--denon-host', help='Denon receiver IP or hostname')
    p.add_argument('--base-url')
    p.add_argument('--serve-host', help='Local IP address to expose the HTTP file server on; auto-detected by default')
    p.add_argument('--serve-port', type=int, default=8123)
    p.set_defaults(func=cmd_push)

    p = sub.add_parser('stop')
    p.set_defaults(func=cmd_stop)

    p = sub.add_parser('status')
    p.set_defaults(func=cmd_status)

    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(f'error: {e}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

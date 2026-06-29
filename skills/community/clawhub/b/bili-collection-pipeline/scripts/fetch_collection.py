#!/usr/bin/env python3
"""
Fetch video list from a Bilibili collection or YouTube playlist.

Usage:
    # Bilibili
    python3 fetch_collection.py "https://www.bilibili.com/video/BVxxxxxx" -o collection.json
    python3 fetch_collection.py BV1GeDSYhEVZ -o collection.json

    # YouTube
    python3 fetch_collection.py "https://youtube.com/playlist?list=PLxxxxx" -o collection.json
    python3 fetch_collection.py "https://youtu.be/xxxxx" -o collection.json
"""
import sys, os, json, argparse, subprocess, urllib.request, re, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

BAPI = 'https://api.bilibili.com'


# ── Helpers ──

def run_cmd(args, timeout=30):
    result = subprocess.run(args, capture_output=True, timeout=timeout)
    try:
        return (result.returncode,
                result.stdout.decode('utf-8', errors='replace'),
                result.stderr.decode('utf-8', errors='replace'))
    except:
        return (result.returncode, '', '')


def extract_bvid(url_or_bvid):
    s = url_or_bvid.strip()
    if s.startswith('http'):
        m = re.search(r'(BV[a-zA-Z0-9]+)', s)
        return m.group(1) if m else None
    return s if s.startswith('BV') else None


def is_youtube_url(url):
    url = url.strip()
    patterns = [
        r'youtube\.com/playlist',
        r'youtube\.com/watch',
        r'youtu\.be/',
        r'youtube\.com/@',
        r'youtube\.com/channel/',
    ]
    return any(re.search(p, url) for p in patterns)


# ── Bilibili ──

def bili_api_get(url, retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Referer': 'https://www.bilibili.com/',
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise


def fetch_bilibili(bvid):
    """Fetch Bilibili collection by a video BVID"""
    view = bili_api_get(f'{BAPI}/x/web-interface/view?bvid={bvid}')
    data = view.get('data', {})
    ugc_season = data.get('ugc_season', {})
    season_id = ugc_season.get('id') or data.get('season_id')

    if not season_id:
        print('Error: video is not part of any collection')
        sys.exit(1)

    season_info = bili_api_get(f'{BAPI}/x/web-interface/season?season_id={season_id}')
    season_data = season_info.get('data', {})

    episodes = []
    for ep in season_data.get('episodes', []):
        episodes.append({
            'bvid': ep['bvid'],
            'title': ep.get('title', ''),
            'duration': ep.get('duration', 0),
            'url': f'https://www.bilibili.com/video/{ep["bvid"]}',
            'platform': 'bilibili',
        })

    # Fallback: paginated archives
    if not episodes:
        page = 1
        while True:
            arch = bili_api_get(f'{BAPI}/x/web-interface/season/archive?season_id={season_id}&page={page}')
            arch_data = arch.get('data', {})
            arch_list = arch_data.get('archives', [])
            if not arch_list:
                break
            for a in arch_list:
                episodes.append({
                    'bvid': a['bvid'],
                    'title': a.get('title', ''),
                    'duration': a.get('duration', 0),
                    'url': f'https://www.bilibili.com/video/{a["bvid"]}',
                    'platform': 'bilibili',
                })
            if page >= arch_data.get('page', {}).get('count', 1):
                break
            page += 1
            time.sleep(1)

    up_name = season_data.get('up_name', data.get('owner', {}).get('name', ''))
    up_mid = season_data.get('up_mid', data.get('owner', {}).get('mid', ''))

    return {
        'collection': {
            'id': str(season_id),
            'name': ugc_season.get('title') or season_data.get('name', ''),
            'up_name': up_name,
            'up_mid': up_mid,
            'platform': 'bilibili',
        },
        'videos': episodes,
        'total': len(episodes),
        'total_seconds': sum(e['duration'] for e in episodes),
    }


# ── YouTube ──

def fetch_youtube(url):
    """Fetch YouTube playlist or channel videos using yt-dlp"""
    rc, stdout, stderr = run_cmd([
        'yt-dlp', '--flat-playlist', '--dump-json',
        '--no-warnings', url
    ], timeout=60)

    if rc != 0:
        print(f'yt-dlp error: {stderr[:300]}')
        print('Make sure yt-dlp is installed: pip install yt-dlp')
        sys.exit(1)

    episodes = []
    playlist_title = ''
    uploader = ''

    for line in stdout.strip().split('\n'):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except:
            continue

        # First item has playlist metadata
        if not playlist_title:
            playlist_title = item.get('playlist_title', item.get('playlist', ''))
            uploader = item.get('uploader', item.get('channel', ''))

        vid = item.get('id', '')
        title = item.get('title', '')
        duration = item.get('duration', 0) or 0
        webpage_url = item.get('webpage_url', item.get('url', f'https://youtube.com/watch?v={vid}'))

        episodes.append({
            'bvid': vid,  # Reuse bvid field for compatibility
            'title': title,
            'duration': duration,
            'url': webpage_url,
            'platform': 'youtube',
        })

    return {
        'collection': {
            'id': playlist_title or url,
            'name': playlist_title or 'YouTube Playlist',
            'up_name': uploader or '',
            'up_mid': '',
            'platform': 'youtube',
        },
        'videos': episodes,
        'total': len(episodes),
        'total_seconds': sum(e['duration'] for e in episodes),
    }


# ── Main ──

def main():
    parser = argparse.ArgumentParser(description='Fetch video list from Bilibili collection or YouTube playlist')
    parser.add_argument('input', help='B站视频/合集URL / BVID / YouTube播放列表/视频URL')
    parser.add_argument('-o', '--output', default='collection.json', help='Output JSON file')
    args = parser.parse_args()

    url = args.input.strip()

    if is_youtube_url(url):
        print('Detected YouTube URL. Fetching playlist with yt-dlp...')
        info = fetch_youtube(url)
    else:
        bvid = extract_bvid(url)
        if not bvid:
            print('Error: could not parse BVID from input')
            sys.exit(1)
        print(f'Detected Bilibili URL. Fetching collection for {bvid}...')
        info = fetch_bilibili(bvid)

    c = info['collection']
    total_s = info['total_seconds']
    total_h = total_s // 3600
    total_m = (total_s % 3600) // 60

    print(f'\nCollection: {c["name"]}')
    print(f'Platform:   {c["platform"]}')
    if c.get('up_name'):
        print(f'Creator:    {c["up_name"]}')
    print(f'Videos:     {info["total"]}')
    print(f'Duration:   {total_h}h{total_m}m')
    print()

    for i, v in enumerate(info['videos'], 1):
        m = v['duration'] // 60
        s = v['duration'] % 60
        vid_label = v['bvid'] or v['url'][:20]
        print(f'  [{i:3d}] {vid_label:20s}  {v["title"][:50]:50s}  {m}:{s:02d}')

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f'\nSaved: {args.output}')


if __name__ == '__main__':
    main()

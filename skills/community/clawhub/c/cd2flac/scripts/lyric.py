#!/usr/bin/env python3
"""
Lyric provider for FLAC files using Netease Cloud Music (primary) and Kugou (fallback).

Usage:
    python3 lyric.py "/path/to/album"           # Inject lyrics into all FLACs
    python3 lyric.py "/path/to/song.flac"       # Inject lyrics into one FLAC
    python3 lyric.py "/path/to/album" --dry-run # Preview only
"""

import os, sys, re, json, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib.request, urllib.parse

# ── Netease Cloud Music (linuxapi) ──────────────────────────────────

LINUXAPI_KEY = b'rFgB&h#%2?^eDg:Q'
ANON_TOKEN = ("bf8bfeabb1aa84f9c8c3906c04a04fb864322804c83f5d607e91a04eae463c9436"
              "bd1a17ec353cf780b396507a3f7464e8a60f4bbc019437993166e004087dd32d14"
              "90298caf655c2353e58daa0bc13cc7d5c198250968580b12c1b8817e3f5c807e65"
              "0dd04abd3fb8130b7ae43fcc5b")

def _linuxapi_encrypt(params):
    text = json.dumps(params, separators=(',', ':')).encode('utf-8')
    cipher = AES.new(LINUXAPI_KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(text, AES.block_size)).hex().upper()

def _linuxapi_req(params):
    data = urllib.parse.urlencode({"eparams": _linuxapi_encrypt(params)}).encode()
    req = urllib.request.Request(
        "https://music.163.com/api/linux/forward", data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Cookie": f"MUSIC_A={ANON_TOKEN}",
            "Referer": "https://music.163.com",
            "Content-Type": "application/x-www-form-urlencoded",
        })
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))

def netease_search(title, artist):
    """Search Netease, return list of {id, name, artist, album}"""
    result = _linuxapi_req({
        "method": "POST",
        "url": "http://music.163.com/api/search/get",
        "params": {"s": f"{title} {artist}", "type": 1, "limit": 10, "offset": 0}
    })
    if result.get('code') != 200:
        return []
    return [{
        'id': s['id'],
        'name': s['name'],
        'artist': s.get('artists', [{}])[0].get('name', '') if s.get('artists') else '',
        'album': s.get('album', {}).get('name', ''),
    } for s in result.get('result', {}).get('songs', [])]

def netease_lyric(song_id):
    """Get LRC from Netease by song ID. Returns (lrc_text, translation_text)"""
    result = _linuxapi_req({
        "method": "POST",
        "url": "http://music.163.com/api/song/lyric",
        "params": {"id": song_id, "lv": -1, "kv": -1, "tv": -1}
    })
    lrc = result.get('lrc', {}).get('lyric', '')
    tlrc = result.get('tlyric', {}).get('lyric', '')
    return lrc, tlrc

# ── Kugou (fallback) ───────────────────────────────────────────────

KUGOU_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15"

def kugou_search(title, artist):
    """Search Kugou, return list of {hash, name, artist}"""
    encoded = urllib.parse.quote(f"{artist} {title}")
    req = urllib.request.Request(
        f"http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={encoded}&page=1&pagesize=5",
        headers={"User-Agent": KUGOU_UA})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    songs = []
    if data.get('status') == 1 and data.get('data', {}).get('info'):
        for s in data['data']['info']:
            songs.append({
                'hash': s['hash'],
                'name': s['songname'],
                'artist': s.get('singername', ''),
            })
    return songs

def kugou_lyric(song_hash):
    """Get LRC from Kugou"""
    req = urllib.request.Request(
        f"http://m.kugou.com/app/i/krc.php?cmd=100&hash={song_hash}&timelength=999999",
        headers={"User-Agent": KUGOU_UA})
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read().decode('utf-8', errors='replace')
    lines = [l for l in raw.split('\n') if re.match(r'^\[\d{2}:\d{2}\.\d{2}', l)]
    return '\n'.join(lines)

# ── Lyric matching ─────────────────────────────────────────────────

def _normalize(s):
    """Normalize for matching: lowercase, remove punctuation, extras"""
    if not s:
        return ''
    s = s.lower()
    s = re.sub(r'[\(\)\[\]\{\}（）【】「」,.《》「」『』、：；！？…·\-\s]', '', s)
    return s.strip()

def _pick_best_match(songs, target_title, target_artist):
    """Pick the best matching song from a list"""
    t_title = _normalize(target_title)
    t_artist = _normalize(target_artist) if target_artist else ''
    
    if not songs:
        return None
    
    # Pass 1: exact title + artist match
    for s in songs:
        if _normalize(s['name']) == t_title:
            if t_artist and _normalize(s['artist']) and _normalize(s['artist']) in t_artist:
                return s
    
    # Pass 2: title contains target or vice versa
    for s in songs:
        s_name = _normalize(s['name'])
        if s_name == t_title:
            return s
    
    # Pass 3: any match
    for s in songs:
        if t_title in _normalize(s['name']) or _normalize(s['name']) in t_title:
            return s
    
    return songs[0]  # last resort

# ── Main API ───────────────────────────────────────────────────────

def clean_lrc(lrc_text):
    """Extract only timestamped lines from LRC text"""
    lines = []
    for l in lrc_text.strip().split('\n'):
        l = l.strip().rstrip('\r')
        if re.match(r'^\[\d{2}:\d{2}\.\d{2}', l):
            lines.append(l)
    return '\n'.join(lines)

def _infer_artist_from_dir(filepath):
    """Try to infer artist name from directory path"""
    dirname = os.path.basename(os.path.dirname(os.path.abspath(filepath)))
    # Common patterns: "Artist - Album", "Artist/Album"
    # Check if dirname has Chinese characters that look like an artist name
    parts = dirname.split(' - ')
    if len(parts) >= 2:
        return parts[0].strip()
    # Extract known artists from common patterns (艺名 in brackets before year)
    m = re.match(r'^\d{4}-(.+?)\[', dirname)
    if m:
        candidate = m.group(1).strip()
        # If it's not too long, likely an artist name
        if len(candidate) < 20:
            return candidate
    return dirname

def _try_search(title, artist):
    """Try Netease then Kugou with given title+artist"""
    if not title:
        return None, None, None
    
    # Netease
    songs = netease_search(title, artist)
    best = _pick_best_match(songs, title, artist)
    if best:
        lrc, tlrc = netease_lyric(best['id'])
        cleaned = clean_lrc(lrc)
        if cleaned.strip():
            return cleaned, "netease", clean_lrc(tlrc)
    
    # Kugou fallback
    songs = kugou_search(title, artist)
    best = _pick_best_match(songs, title, artist)
    if best:
        lrc = kugou_lyric(best['hash'])
        if lrc.strip():
            return lrc, "kugou", ""
    
    return None, None, None

def get_lyrics(title, artist, album=None, flac_path=None):
    """
    Get lyrics for a song with multi-strategy search.
    Returns (lrc_text, source_name, translation_text) or (None, None, None).
    """
    # Normalize empty artist
    artist = (artist or '').strip()
    if artist in ('', '?', 'unknown', 'Unknown'):
        artist = ''
    
    # Strategy 1: title + artist (most precise)
    if artist:
        result = _try_search(title, artist)
        if result[0]:
            return result
    
    # Strategy 2: title + inferred artist from directory
    if not artist and flac_path:
        inferred = _infer_artist_from_dir(flac_path)
        if inferred:
            result = _try_search(title, inferred)
            if result[0]:
                return result
    
    # Strategy 3: title only (broad search, works for popular songs)
    result = _try_search(title, '')
    if result[0]:
        return result
    
    return None, None, None

def inject_to_flac(flac_path, lrc_text, translation_text=''):
    """
    Inject lyrics into a FLAC/DSF file.
    FLAC: Vorbis comment LYRICS tag.
    DSF: ID3 USLT frame.
    """
    from mutagen.flac import FLAC
    from mutagen.dsf import DSF
    from mutagen.id3 import USLT, ID3
    if flac_path.endswith('.dsf'):
        # DSF 只生成 .lrc 文件，不修改文件本体（避免损坏 DSF 头）
        lrc_path = os.path.splitext(flac_path)[0] + '.lrc'
        with open(lrc_path, 'w', encoding='utf-8') as f:
            f.write(lrc_text)
        # 验证歌词文件
        print(f"  写入 .lrc: {os.path.basename(lrc_path)} ({len(lrc_text)}字符)")
    else:
        audio = FLAC(flac_path)
        audio['LYRICS'] = lrc_text
        if translation_text and translation_text.strip():
            audio['LYRICS_TRANSLATIONS'] = translation_text
        audio.save()

# ── CLI entry point ────────────────────────────────────────────────

def process_file(flac_path, dry_run=False):
    """Process one FLAC/DSF file: read tags, fetch lyrics, inject"""
    from mutagen.flac import FLAC
    from mutagen.dsf import DSF
    audio = DSF(flac_path) if flac_path.endswith('.dsf') else FLAC(flac_path)
    title = audio.get('title', [''])[0]
    artist = audio.get('artist', [''])[0]
    album = audio.get('album', [''])[0]
    
    if not title:
        title = os.path.splitext(os.path.basename(flac_path))[0]
        m = re.match(r'\d+\s*-\s*(.*)', title)
        if m:
            title = m.group(1).strip()
    
    print(f"🎵 {os.path.basename(flac_path)}")
    print(f"   标签: '{artist}' - '{title}' [{album}]")
    
    lrc, src, tlrc = get_lyrics(title, artist, album, flac_path)
    if not lrc:
        print("   ❌ 未找到歌词")
        return False
    
    line_count = len([l for l in lrc.split('\n') if l.strip()])
    has_tlrc = f" +翻译({len(tlrc.split())}行)" if tlrc.strip() else ''
    print(f"   ✅ [{src}] {line_count}行歌词{has_tlrc}")
    
    if not dry_run:
        inject_to_flac(flac_path, lrc, tlrc)
    
    return True

def process_directory(directory, dry_run=False):
    """Process all FLAC files in a directory"""
    audio_files = sorted([f for f in os.listdir(directory) if f.endswith(('.flac','.dsf'))])
    if not audio_files:
        print(f"ℹ️  没有音频文件在: {directory}")
        return
    
    if dry_run:
        print("🔍 DRY RUN - 仅预览\n")
    
    success = 0
    for f in audio_files:
        if process_file(os.path.join(directory, f), dry_run):
            success += 1
        print()
    
    print(f"{'='*50}")
    print(f"✅ {success}/{len(audio_files)} 增加歌词成功")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    path = os.path.abspath(sys.argv[1])
    dry_run = '--dry-run' in sys.argv
    
    if not os.path.exists(path):
        print(f"❌ 路径不存在: {path}")
        sys.exit(1)
    
    if os.path.isfile(path) and path.endswith('.flac'):
        lang = process_file(path, dry_run)
    elif os.path.isdir(path):
        process_directory(path, dry_run)
    else:
        print(f"❌ 不支持的文件类型")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Bootleg-Link Download Daemon — standalone background process.
Survives Claude exit. Listens on http://127.0.0.1:8765
"""
import sys, json, os, sqlite3, time, uuid, threading, re, socket, signal
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from collections import deque
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
import traceback, subprocess, urllib.request, urllib.parse

# ── Config ──────────────────────────────────────────────
PORT = 8765
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".bootleg-link-mcp", "config.json")
PID_FILE = os.path.join(os.path.dirname(CONFIG_FILE), "daemon.pid")

def load_config():
    d = {"paths":{"outputDir": os.path.join(os.path.expanduser("~"), "Downloads", "bootleg-link"),
                   "dbPath": os.path.join(os.path.expanduser("~"), ".bootleg-link-mcp", "bootleg-link.db")},
         "proxy": {}, "download": {"maxConcurrent": 32, "quality": "320", "pageSize": 100}}
    try:
        with open(CONFIG_FILE) as f: c = json.load(f)
        for k,v in d.items(): c.setdefault(k, v)
        return c
    except: return d

cfg = load_config()
MAX_WORKERS = min((os.cpu_count() or 32), cfg.get("download",{}).get("maxConcurrent", 4))
PAGE_SIZE = cfg.get("download",{}).get("pageSize", 100)
HTTPS_PROXY = cfg.get("proxy",{}).get("https", cfg.get("proxy",{}).get("http",""))
DB_PATH = cfg.get("paths",{}).get("dbPath","")
DEF_OUT = cfg.get("paths",{}).get("outputDir","")
COOKIES_PATH = cfg.get("cookies", os.path.join(os.path.dirname(DB_PATH), "youtube-cookies.txt"))

# ── DB (WAL mode — optimistic concurrency) ─────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY, url TEXT NOT NULL,
  outputDir TEXT DEFAULT '', quality TEXT DEFAULT '320',
  status TEXT DEFAULT 'pending', progress INTEGER DEFAULT 0, message TEXT DEFAULT '',
  createdAt TEXT, updatedAt TEXT, error TEXT,
  songsCompleted INTEGER DEFAULT 0, songsTotal INTEGER DEFAULT 0, lastSong TEXT,
  pageStart INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS downloaded_videos (
  task_id TEXT NOT NULL, video_id TEXT NOT NULL, video_url TEXT NOT NULL,
  fetched_at TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (task_id, video_id)
);
"""
db = sqlite3.connect(DB_PATH, check_same_thread=False)
db.execute("PRAGMA journal_mode=WAL")
for s in SCHEMA.split(";"):
    if s.strip(): db.execute(s.strip())
db.commit()
db_read = sqlite3.connect(DB_PATH, check_same_thread=False)
db_read.execute("PRAGMA query_only=ON")

tasks_lock = threading.Lock()
tasks: dict[str, dict] = {}

def _load_tasks():
    cols = [c[1] for c in db.execute("PRAGMA table_info(tasks)")]
    for row in db.execute("SELECT * FROM tasks"): tasks[row[0]] = dict(zip(cols, row))
_load_tasks()

def _safe_commit():
    """Commit with retry on WAL mode transient failures."""
    for attempt in range(3):
        try:
            db.commit()
            return
        except sqlite3.OperationalError:
            if attempt < 2:
                time.sleep(0.1)
                try: db.rollback()
                except: pass
            else:
                raise

def persist(t: dict):
    db.execute("""INSERT OR REPLACE INTO tasks
      (id, url, outputDir, quality, status, progress, message, createdAt, updatedAt, error,
       songsCompleted, songsTotal, lastSong, pageStart)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
      (t["id"], t["url"], t.get("outputDir",""), t.get("quality","320"),
       t["status"], t.get("progress",0), t.get("message",""),
       t.get("createdAt",""), t.get("updatedAt",""), t.get("error"),
       t.get("songsCompleted",0), t.get("songsTotal",0), t.get("lastSong"),
       t.get("pageStart",1)))
    _safe_commit()

def persist_video(task_id, video_id, video_url):
    db.execute("INSERT OR IGNORE INTO downloaded_videos (task_id, video_id, video_url) VALUES (?,?,?)",
               (task_id, video_id, video_url))
    _safe_commit()

def count_downloaded(task_id):
    return db_read.execute("SELECT COUNT(*) FROM downloaded_videos WHERE task_id=?", (task_id,)).fetchone()[0]

def load_video_set(task_id):
    return db_read.execute("SELECT video_id, video_url FROM downloaded_videos WHERE task_id=?", (task_id,)).fetchall()

def gen_id():
    return f"task_{int(time.time()*1000)}_{uuid.uuid4().hex[:9]}"

def vid_of(entry): return entry.get("id") or entry.get("display_id") or ""
def url_of(vid): return f"https://www.youtube.com/watch?v={vid}" if vid else ""

# ── YT-DLP ──────────────────────────────────────────────
def _get_ytdlp():
    import yt_dlp
    return yt_dlp

_NODE_PATH = os.path.expanduser("~/.nvm/versions/node/v24.16.0/bin/node")
if not os.path.isfile(_NODE_PATH): _NODE_PATH = "node"

from yt_dlp.networking.impersonate import ImpersonateTarget
_IMPERSONATE = ImpersonateTarget(client='chrome')
_JS_RUNTIMES = {'node': {'path': _NODE_PATH}}

# ── Orphan Cleanup ───────────────────────────────────────
def _cleanup_orphans(output_dir):
    """Remove orphaned temp/thumbnail files and deduplicate MP3s."""
    if not os.path.isdir(output_dir):
        return
    cleaned = 0; ghosts = 0; dupes = 0
    all_files = {}
    for f in os.listdir(output_dir):
        path = os.path.join(output_dir, f)
        # Skip ghost files (CIFS dir cache shows deleted files)
        try:
            fd = os.open(path, os.O_RDONLY); os.close(fd)
        except (FileNotFoundError, OSError):
            ghosts += 1; continue
        if not os.path.isfile(path):
            continue
        all_files[f] = path
        if f.endswith('.part') or f.endswith('.ytdl'):
            try: os.remove(path); cleaned += 1
            except: pass
        elif f.endswith('.temp.mp3'):
            final = os.path.join(output_dir, f[:-9] + '.mp3')
            if not os.path.exists(final):
                try: os.rename(path, final)
                except: pass
            else:
                try: os.remove(path); cleaned += 1
                except: pass
        elif any(f.endswith(ext) for ext in ('.webp', '.webm', '.jpg')):
            stem = os.path.splitext(f)[0]
            mp3 = os.path.join(output_dir, stem + '.mp3')
            # Check if mp3 already has embedded cover before trying to embed
            if os.path.exists(mp3):
                has_cover = False
                try:
                    import subprocess as _sp
                    r = _sp.run(['ffprobe', '-v', 'quiet', '-select_streams', 'v',
                                 '-show_entries', 'stream=codec_type', mp3],
                                capture_output=True, text=True)
                    has_cover = 'codec_type=video' in r.stdout
                except: pass
                if not has_cover:
                    _try_embed_cover(mp3, path)
            try: os.remove(path); cleaned += 1
            except: pass
    # Deduplicate: strip common channel prefixes, keep larger file
    mp3s = {f: p for f, p in all_files.items() if f.endswith('.mp3') and os.path.exists(p)}
    by_stem = {}
    for f in mp3s:
        stem = f
        for prefix in ('PureHouseMusic 2024 - ',):
            if stem.startswith(prefix): stem = stem[len(prefix):]
        by_stem.setdefault(stem, []).append(f)
    for stem, files in by_stem.items():
        if len(files) <= 1: continue
        files.sort(key=lambda f: os.path.getsize(os.path.join(output_dir, f)), reverse=True)
        for f in files[1:]:
            try:
                os.remove(os.path.join(output_dir, f)); dupes += 1
            except: pass
    if cleaned or ghosts or dupes:
        print(f"[daemon] cleanup: {cleaned} removed, {dupes} dupes, {ghosts} ghosts in {output_dir}", file=sys.stderr, flush=True)

def _try_embed_cover(mp3_path, thumb_path):
    """Fallback: embed thumbnail into MP3 if it has no cover art. Uses pure mutagen APIC only."""
    try:
        from mutagen.id3 import ID3, APIC, error as ID3Err
        try: audio = ID3(mp3_path)
        except ID3Err: audio = ID3()
        if any(k.startswith("APIC") for k in audio):
            return  # already has cover
        jpg_path = thumb_path
        if thumb_path.endswith(('.webp', '.webm')):
            jpg_path = os.path.splitext(thumb_path)[0] + '.jpg'
            r = subprocess.run(["ffmpeg","-y","-nostdin","-loglevel","error",
                "-i", thumb_path, jpg_path], capture_output=True, timeout=15)
            if r.returncode != 0 or not os.path.exists(jpg_path):
                return
        with open(jpg_path, "rb") as pf:
            audio["APIC"] = APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=pf.read())
        audio.save(mp3_path, v2_version=3)
        if jpg_path != thumb_path:
            try: os.remove(jpg_path)
            except: pass
    except Exception as e:
        print(f"[daemon] fallback embed: {os.path.basename(mp3_path)[:50]}: {e}", file=sys.stderr, flush=True)


def _convert_webm_to_mp3(output_dir, base_name, webm_path, thumb_path):
    """Convert webm→mp3 with NO ID3 tags, embed ONLY cover.jpg.
    Returns mp3_path or None on failure.
    All work happens on local /tmp to avoid CIFS rename/replace issues."""
    if not webm_path or not os.path.exists(webm_path):
        return None

    import tempfile, shutil
    mp3_final = os.path.join(output_dir, base_name + '.mp3')

    # Convert thumb to jpg FIRST (into /tmp to avoid CIFS issues)
    jpg_tmp = None
    if thumb_path and os.path.exists(thumb_path):
        if thumb_path.endswith(('.webp', '.webm')):
            jpg_tmp = os.path.join(tempfile.gettempdir(), base_name + '.cover.jpg')
            subprocess.run(["ffmpeg","-y","-nostdin","-loglevel","error",
                "-i", thumb_path, jpg_tmp], capture_output=True, timeout=30)
            try: os.remove(thumb_path)
            except: pass
        elif thumb_path.endswith('.jpg'):
            jpg_tmp = thumb_path

    # Convert webm to mp3 (output to /tmp)
    mp3_tmp = os.path.join(tempfile.gettempdir(), base_name + '.mp3')
    cmd = [
        "ffmpeg","-y","-nostdin","-loglevel","error",
        "-i", webm_path,
    ]
    if jpg_tmp and os.path.exists(jpg_tmp):
        cmd += ["-i", jpg_tmp, "-map", "0:a", "-map", "1:0"]
    else:
        cmd += ["-vn"]

    cmd += [
        "-c:a", "libmp3lame", "-b:a", "320k", "-ar", "48000",
        "-map_metadata", "-1",
        "-id3v2_version", "3", "-write_id3v1", "0",
    ]
    if jpg_tmp and os.path.exists(jpg_tmp):
        cmd += ["-metadata:s:v", "title=Album cover",
                "-metadata:s:v", "comment=Cover (front)"]
    cmd.append(mp3_tmp)

    r = subprocess.run(cmd, capture_output=True, timeout=120)

    if r.returncode != 0 or not os.path.exists(mp3_tmp):
        # Fallback: check if yt-dlp auto-extracted mp3 (when no webm downloaded)
        alt = os.path.join(output_dir, base_name + '.mp3')
        if os.path.exists(alt) and os.path.getsize(alt) > 0:
            try: os.remove(webm_path)
            except: pass
            return alt
        print(f"[daemon] ffmpeg failed for {base_name[:50]}: {r.stderr[-200:] if r.stderr else 'no stderr'}", file=sys.stderr, flush=True)
        return None

    # Copy from /tmp to CIFS (shutil.copy2, then delete source)
    try:
        shutil.copy2(mp3_tmp, mp3_final)
        os.remove(mp3_tmp)
    except Exception as e:
        # If copy fails due to CIFS ghost, try rename
        try:
            os.rename(mp3_tmp, mp3_final)
        except:
            print(f"[daemon] unable to move mp3: {e}", file=sys.stderr, flush=True)
            return None

    # Cleanup source webm
    try: os.remove(webm_path)
    except: pass

    # Cleanup cover temp
    if jpg_tmp and os.path.exists(jpg_tmp):
        try: os.remove(jpg_tmp)
        except: pass

    # Delete any leftover thumbs/webm for this track
    for ext in ['.webm', '.webp', '.jpg']:
        leftover = os.path.join(output_dir, base_name + ext)
        if os.path.exists(leftover):
            try: os.remove(leftover)
            except: pass

    return mp3_final

def _verify_download(mp3_path, vid=None):
    """Post-download check: file exists, non-empty, has cover, no extra tags."""
    ok = True
    try:
        if not mp3_path or not os.path.exists(mp3_path):
            return "missing_file"
        sz = os.path.getsize(mp3_path)
        if sz < 10000:  # smaller than 10KB — truncated
            ok = False
        r = subprocess.run(['ffprobe','-v','quiet','-show_format','-show_streams',
                            '-select_streams','v', mp3_path],
                           capture_output=True, timeout=15, text=True)
        if 'codec_type=video' not in r.stdout:
            ok = False  # no cover
        # Count non-encoder tags
        tags = [l for l in r.stdout.split('\n') if l.startswith('TAG:') and 'encoder' not in l.lower()]
        if tags:
            ok = False  # unwanted ID3 tags present
    except Exception as e:
        return f"verify_error:{e}"
    return "ok" if ok else "bad_cover_or_tags"

# ── Queue & Workers ─────────────────────────────────────
dl_queue = deque()
futures: dict[str, Future] = {}
pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

def run_download(task_id: str):
    with tasks_lock:
        t = tasks.get(task_id)
    if not t: return

    db.execute("UPDATE tasks SET status='downloading', message=? WHERE id=? AND status='pending'",
               (socket.gethostname()+":"+str(os.getpid()), task_id))
    db.commit()
    with tasks_lock:
        t["status"] = "downloading"

    output_dir = t.get("outputDir") or DEF_OUT
    proxy = HTTPS_PROXY
    skipped_premiere = 0; last_title = ""

    existing = load_video_set(task_id)
    completed_ids = {vid: url for vid, url in existing}
    seen_ids = set(completed_ids.keys())
    completed = len(completed_ids)
    total_items = completed; restored = 0

    if os.path.isdir(output_dir):
        existing_mp3s = {f for f in os.listdir(output_dir) if f.endswith('.mp3')}
        # Only count files we already tracked in DB — don't count files from other tasks
        if existing_mp3s and completed > 0 and len(existing_mp3s) > completed:
            restored = len(existing_mp3s) - completed
            completed = len(existing_mp3s)

    with tasks_lock:
        t["songsCompleted"] = completed
        t["songsTotal"] = total_items
        persist(t)

    def progress_hook(d):
        nonlocal completed, last_title
        status = d.get("status",""); info = d.get("info_dict") or {}
        if status == "downloading":
            pct_s = d.get("_percent_str","0%").replace("%","").strip()
            try: pct_n = int(float(pct_s))
            except: pct_n = 0
            with tasks_lock:
                t["progress"] = pct_n
                t["message"] = f"Downloading... {pct_n}%"
                t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                persist(t)
        elif status in ("finished", "downloaded"):
            fn = info.get("title","") or os.path.basename(d.get("filename",""))
            completed += 1; last_title = fn
            vid = info.get("id","")
            vid_url = info.get("webpage_url") or info.get("original_url") or ""
            if vid and vid not in completed_ids:
                completed_ids[vid] = vid_url
                persist_video(task_id, vid, vid_url)
            with tasks_lock:
                current_total = t.get("songsTotal", total_items)
                pct = int(completed / max(current_total, 1) * 100)
                t["songsCompleted"] = completed
                t["lastSong"] = fn; t["progress"] = pct
                prefix = f"[{skipped_premiere} skipped] " if skipped_premiere else ""
                pg = t.get("pageStart", 1)
                t["message"] = f"P{pg} {completed}/{current_total} ({pct}%): {fn}"
                t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                persist(t)

    try:
        yt_dlp = _get_ytdlp()
        _yt_extractor_args = {"fetch_pot": ["always"]}
        flat_opts = {"quiet":True,"no_warnings":True,"extract_flat":True,
                     "proxy":proxy or None,"socket_timeout":30,"ignoreerrors":True,
                     "impersonate":_IMPERSONATE,"js_runtimes":_JS_RUNTIMES,
                     "extractor_args":{"youtube": _yt_extractor_args}}
        dl_opts = {"quiet":True,"no_warnings":True,"format":"bestaudio/best",
                   "socket_timeout":60,"ignoreerrors":True,
                   "postprocessors": [],
                   "retries":3,"fragment_retries":3,"retry_sleep":5,
                   "extract_flat":"in_playlist","writethumbnail":True,
                   "continuedl":False,"noprogress":True,
                   "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
                   "progress_hooks":[progress_hook],"proxy":proxy or None,
                   "impersonate":_IMPERSONATE,"js_runtimes":_JS_RUNTIMES,
                   "extractor_args":{"youtube": _yt_extractor_args}}
        _auto_cookies = COOKIES_PATH if os.path.isfile(COOKIES_PATH) else ""
        _use_cookies = cfg.get("cookies", "") or _auto_cookies
        if _use_cookies and os.path.isfile(_use_cookies):
            dl_opts["cookiefile"] = _use_cookies
            flat_opts["cookiefile"] = _use_cookies

        page_num = 0
        while True:
            page_num += 1
            flat_opts["playliststart"] = (page_num-1)*PAGE_SIZE + 1
            flat_opts["playlistend"] = page_num*PAGE_SIZE
            with tasks_lock:
                t["message"] = f"Fetching page {page_num}..."; t["pageStart"] = page_num; persist(t)
            try:
                with yt_dlp.YoutubeDL(flat_opts) as ydl:
                    info = ydl.extract_info(t["url"], download=False)
            except Exception as e:
                print(f"[daemon] PAGE_ERR:{task_id}:{page_num}:{str(e)[:150]}", file=sys.stderr, flush=True)
                break
            if info is None: break
            entries = info.get("entries") or []
            # Single video (no entries) — treat as one-item list
            _is_single = False
            if not entries and info.get("id") and info.get("_type", "video") != "playlist":
                entries = [info]
                _is_single = True
            if not entries: break
            batch = []
            for e in entries:
                if not e: continue
                vid = vid_of(e)
                if not vid or vid in seen_ids: continue
                u = url_of(vid)
                if not u: continue
                seen_ids.add(vid); batch.append((vid, u))
            if not batch:
                # Single video with nothing new — done
                if _is_single: break
                continue
            total_items += len(batch)
            with tasks_lock:
                t["songsTotal"] = total_items
                t["pageStart"] = page_num
                t["message"] = f"P{page_num} +{len(batch)} → {completed}/{total_items} ({int(completed/max(total_items,1)*100)}%)"
                persist(t)
            inner_pool = ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(batch)))
            dl_futures = []
            for vid, u in batch:
                def _dl_one(vid=vid, url=u, _retries=[0]):
                    try:
                        yt_dlp_local = _get_ytdlp()
                        # Clean stale .part files to prevent HTTP 416 errors
                        for f in os.listdir(output_dir):
                            if f.endswith('.webm.part'):
                                try: os.remove(os.path.join(output_dir, f))
                                except: pass
                        # Record files before download
                        before = set(f for f in os.listdir(output_dir)
                                     if os.path.isfile(os.path.join(output_dir, f)))
                        with yt_dlp_local.YoutubeDL(dict(dl_opts)) as ydl: ydl.download([url])
                        # Find new files created by this download
                        after = set(f for f in os.listdir(output_dir)
                                    if os.path.isfile(os.path.join(output_dir, f)))
                        new_files = after - before

                        # Find webm and matching webp from new files
                        webm = None; webp = None
                        for fname in new_files:
                            if fname.endswith('.webm') and not fname.endswith('.webm.part'):
                                webm = os.path.join(output_dir, fname)
                            elif fname.endswith('.webp'):
                                webp = os.path.join(output_dir, fname)

                        if webm:
                            base = os.path.splitext(os.path.basename(webm))[0]
                            # If webp not found, try to find one with same base name
                            if not webp:
                                candidate = os.path.join(output_dir, base + '.webp')
                                if os.path.exists(candidate):
                                    webp = candidate
                            mp3_path = None
                            try:
                                mp3_path = _convert_webm_to_mp3(output_dir, base, webm, webp)
                            except Exception as conv_err:
                                print(f"[daemon] convert error for {base[:50]}: {conv_err}", file=sys.stderr, flush=True)
                            # Verify the result
                            if mp3_path:
                                vresult = _verify_download(mp3_path, vid)
                                if vresult != "ok":
                                    print(f"[daemon] verify FAIL ({vresult}) for {base[:50]}", file=sys.stderr, flush=True)
                                    # Retry once: delete bad mp3 and webm leftover, redownload
                                    try: os.remove(mp3_path)
                                    except: pass
                                    raise Exception(f"Download verification failed: {vresult}")
                        return (vid, None)
                    except Exception as e:
                        err = str(e)[:80]
                        nonlocal skipped_premiere
                        if "premiere" in err.lower(): skipped_premiere += 1
                        return (vid, err)
                dl_futures.append(inner_pool.submit(_dl_one))
            for f in as_completed(dl_futures): f.result()
            # NOTE: do NOT call _cleanup_orphans here during concurrent downloads.
            # It races with yt-dlp's EmbedThumbnail postprocessor — the orphan cleanup
            # can delete thumbnail files before they are embedded into the mp3.

        _cleanup_orphans(output_dir)
        with tasks_lock:
            # Final completeness check: count actual mp3 files on disk
            actual_mp3s = 0
            if os.path.isdir(output_dir):
                actual_mp3s = len([f for f in os.listdir(output_dir) if f.endswith('.mp3')])
            t["songsCompleted"] = actual_mp3s
            t["progress"] = 100
            if completed != actual_mp3s:
                t["message"] = f"Done! {actual_mp3s} mp3 on disk ({completed} downloads attempted)"
            else:
                t["message"] = f"Done! {completed} songs" + (f" ({skipped_premiere} skipped)" if skipped_premiere else "")
            t["status"] = "completed"
            t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            persist(t)
    except Exception as e:
        _cleanup_orphans(output_dir)
        with tasks_lock:
            t["status"] = "failed"; t["error"] = str(e)[:200]
            t["message"] = f"Error: {str(e)[:100]}"
            t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            persist(t)

def _auto_submit():
    # Recover tasks stuck in 'downloading' from a previous crash
    to_recover = []
    with tasks_lock:
        for tid, t in list(tasks.items()):
            if t["status"] == "downloading":
                to_recover.append((tid, t))
    for tid, t in to_recover:
        print(f"[daemon] Recovering stuck task: {tid} ({t.get('url','')[:80]})", file=sys.stderr, flush=True)
        with tasks_lock:
            t["status"] = "pending"; t["message"] = "Recovered — waiting to retry"
            t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        persist(t)
    # Submit pending tasks
    with tasks_lock:
        for tid, t in list(tasks.items()):
            if t["status"] == "pending" and tid not in futures:
                dl_queue.append(tid)
    while dl_queue:
        act = len([f for f in futures.values() if not f.done()])
        if act >= MAX_WORKERS: break
        tid = dl_queue.popleft()
        f = pool.submit(run_download, tid)
        futures[tid] = f
        t = tasks.get(tid)
        if t:
            with tasks_lock:
                t["message"] = "Queued"; t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            persist(t)

# ── Self-watchdog ───────────────────────────────────────
_last_health = time.time()
def health_ping(): global _last_health; _last_health = time.time()

def watchdog_loop():
    while True:
        time.sleep(30)
        active = len([f for f in futures.values() if not f.done()])
        if active > 0 and time.time() - _last_health > 120:
            print("[daemon] Watchdog: active tasks with no progress for 120s, exiting...", file=sys.stderr, flush=True)
            os._exit(1)  # hard exit, MCP framework restarts

# ── HTTP API ────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass  # quiet

    def _send(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        health_ping()
        path = self.path.split("?")[0]
        qs = urllib.parse.parse_qs(self.path.split("?")[1] if "?" in self.path else "")

        if path == "/health":
            self._send({"ok": True})

        elif path == "/queue":
            active = len([f for f in futures.values() if not f.done()])
            self._send({"maxConcurrent":MAX_WORKERS,"activeCount":active,
                        "queueLength":len(dl_queue),"totalTasks":len(tasks),
                        "proxy":HTTPS_PROXY or "system","engine":"yt-dlp"})

        elif path == "/tasks":
            st = qs.get("status",["all"])[0]; lim = int(qs.get("limit",["50"])[0])
            with tasks_lock: lst = [dict(v) for v in tasks.values()]
            if st != "all": lst = [t for t in lst if t.get("status")==st]
            lst = sorted(lst, key=lambda x:x.get("createdAt") or "", reverse=True)[:lim]
            self._send({"count":len(lst),"total":len(tasks),
                        "tasks":[{"taskId":t["id"],"url":t["url"],"status":t["status"],
                                  "progress":t["progress"],"message":t["message"],
                                  "songsCompleted":t.get("songsCompleted",0),
                                  "songsTotal":t.get("songsTotal",0),
                                  "lastSong":t.get("lastSong"),"outputDir":t.get("outputDir",""),
                                  "downloadedInDb": count_downloaded(t["id"])} for t in lst]})

        elif path == "/progress":
            tid = qs.get("taskId",[""])[0]
            if not tid: self._send({"error":"Missing taskId"}, 400); return
            with tasks_lock: t = tasks.get(tid)
            if not t: self._send({"error":"Not found"}, 404); return
            self._send({"taskId":t["id"],"url":t["url"],"status":t["status"],
                        "progress":t["progress"],"message":t["message"],
                        "songsCompleted":t.get("songsCompleted",0),
                        "songsTotal":t.get("songsTotal",0),
                        "lastSong":t.get("lastSong"),"outputDir":t.get("outputDir",""),
                        "createdAt":t["createdAt"],"updatedAt":t["updatedAt"],
                        "error":t.get("error"),"downloadedInDb": count_downloaded(tid)})

        elif path == "/auth":
            if os.path.isfile(COOKIES_PATH):
                with open(COOKIES_PATH) as f:
                    lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
                names = set()
                for line in lines:
                    parts = line.split("\t")
                    if len(parts) >= 7: names.add(parts[5])
                self._send({"authenticated": bool(names & {"SID","HSID","SSID","APISID","SAPISID"}),
                            "cookieCount": len(lines), "cookieFile": COOKIES_PATH})
            else:
                self._send({"authenticated": False, "cookieCount": 0, "cookieFile": COOKIES_PATH})

        else:
            self._send({"error":"Not found"}, 404)

    def do_POST(self):
        health_ping()
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}

        if path == "/submit":
            url = body.get("url",""); quality = body.get("quality","320")
            output_dir = body.get("outputDir","")

            # If no outputDir specified, try to reuse existing task's outputDir for sync
            if not output_dir:
                with tasks_lock:
                    for tid, t in tasks.items():
                        if t["url"] == url and t.get("outputDir"):
                            output_dir = t["outputDir"]
                            break
                # Fallback: auto-generate from URL
                if not output_dir:
                    parsed = urllib.parse.urlparse(url)
                    qs = urllib.parse.parse_qs(parsed.query)
                    search = qs.get("search_query", qs.get("query", [""]))[0]
                    if search: sub = search.strip("[] \t")
                    else:
                        m = re.search(r'/@([^/]+)', url); sub = m.group(1) if m else "downloads"
                    sub = re.sub(r'[\\/*?:"<>|]', '', sub).strip()
                    output_dir = os.path.join(DEF_OUT, sub)

            # Deduplicate / sync
            norm_dir = os.path.normpath(output_dir) if output_dir else ""
            with tasks_lock:
                for tid, t in tasks.items():
                    t_dir = os.path.normpath(t.get("outputDir","")) if t.get("outputDir","") else ""
                    if t["url"] == url and t_dir == norm_dir:
                        if t["status"] in ("pending", "downloading"):
                            if tid not in dl_queue:
                                dl_queue.append(tid); _auto_submit()
                        elif t["status"] in ("completed", "failed", "cancelled"):
                            # Sync: reset to pending so run_download re-scans for new videos
                            t["status"] = "pending"; t["progress"] = 0
                            t["message"] = "Sync — checking for new videos"
                            t["error"] = None; t["pageStart"] = 1
                            t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                            persist(t)
                            dl_queue.append(tid); _auto_submit()
                            self._send({"success":True,"taskId":tid,"status":"syncing","url":url,
                                        "quality":quality,"outputDir":output_dir,"maxConcurrent":MAX_WORKERS,
                                        "message":"Sync — checking for new videos",
                                        "songsCompleted":t.get("songsCompleted",0),
                                        "songsTotal":t.get("songsTotal",0)})
                            return
                        self._send({"success":True,"taskId":tid,"status":t["status"],"url":url,
                                    "quality":quality,"outputDir":output_dir,"maxConcurrent":MAX_WORKERS,
                                    "message":f"Existing task ({t['status']})",
                                    "songsCompleted":t.get("songsCompleted",0),
                                    "songsTotal":t.get("songsTotal",0)})
                        return

            tid = gen_id()
            now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            with tasks_lock:
                tasks[tid] = {"id":tid,"url":url,"outputDir":output_dir,"quality":quality,
                              "status":"pending","progress":0,"message":"Queued",
                              "createdAt":now,"updatedAt":now,"error":None,
                              "songsCompleted":0,"songsTotal":0,"lastSong":"","pageStart":1}
                persist(tasks[tid])
            dl_queue.append(tid); _auto_submit()
            self._send({"success":True,"taskId":tid,"status":"pending","url":url,
                        "quality":quality,"outputDir":output_dir,"maxConcurrent":MAX_WORKERS})

        elif path == "/cancel":
            tid = body.get("taskId","")
            with tasks_lock: t = tasks.get(tid)
            if not t: self._send({"success":False,"error":"Not found"}, 404); return
            st = t["status"]
            if st in ("pending","downloading"):
                t["status"] = "cancelled"; t["message"] = "Cancelled"
                t["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
                persist(t)
            self._send({"success":True,"taskId":tid,"message":t["message"]})

        elif path == "/clear":
            before = len(tasks)
            with tasks_lock:
                for k,v in list(tasks.items()):
                    if v["status"] in ("completed","failed","cancelled"):
                        db.execute("DELETE FROM tasks WHERE id=?", (k,))
                        db.execute("DELETE FROM downloaded_videos WHERE task_id=?", (k,))
                        db.commit()
                        del tasks[k]
            self._send({"success":True,"cleared":before-len(tasks),"remaining":len(tasks)})

        elif path == "/clear-all":
            with tasks_lock:
                for k in list(tasks.keys()):
                    db.execute("DELETE FROM downloaded_videos WHERE task_id=?", (k,))
                    db.execute("DELETE FROM tasks WHERE id=?", (k,))
                    db.commit()
                    del tasks[k]
            dl_queue.clear()
            self._send({"success":True,"message":"Database cleared"})

        else:
            self._send({"error":"Not found"}, 404)

def daemonize():
    """Cross-platform backgrounding."""
    if os.name == 'nt':  # Windows
        # On Windows, just detach from console if possible
        try:
            import ctypes
            ctypes.windll.kernel32.FreeConsole()
        except: pass
        # Write PID
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        with open(PID_FILE, "w") as f: f.write(str(os.getpid()))
    else:  # Linux / macOS
        if os.fork():  # parent exits
            os._exit(0)
        os.setsid()
        # Second fork to fully detach
        if os.fork():
            os._exit(0)
        # Redirect stdio
        sys.stdout = open(os.devnull, 'w')
        sys.stdin = open(os.devnull, 'r')
        # Write PID
        os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
        with open(PID_FILE, "w") as f: f.write(str(os.getpid()))


def main():
    # Allow --no-daemon for systemd (skip fork)
    if "--no-daemon" not in sys.argv:
        daemonize()

    # Kill stale daemon from old PID file
    try:
        with open(PID_FILE) as f:
            old = int(f.read().strip())
        if old != os.getpid():
            try: os.kill(old, signal.SIGTERM)
            except: pass
    except: pass

    # Update PID
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Start watchdog
    threading.Thread(target=watchdog_loop, daemon=True).start()

    # Auto-submit pending tasks (don't crash on startup)
    try:
        _auto_submit()
    except Exception as e:
        print(f"[daemon] startup _auto_submit error (non-fatal): {e}", file=sys.stderr, flush=True)

    # Start HTTP server with crash-resistant handler
    class SafeHandler(Handler):
        def handle_one_request(self):
            try:
                super().handle_one_request()
            except Exception as e:
                print(f"[daemon] HTTP handler error: {e}", file=sys.stderr, flush=True)

    server = ThreadingHTTPServer(("127.0.0.1", PORT), SafeHandler)
    print(f"[daemon] Bootleg-Link Daemon on port {PORT} (PID {os.getpid()})", file=sys.stderr, flush=True)
    while True:
        try:
            server.serve_forever()
        except Exception as e:
            print(f"[daemon] serve_forever crashed, restarting in 3s: {e}", file=sys.stderr, flush=True)
            time.sleep(3)

if __name__ == "__main__":
    main()

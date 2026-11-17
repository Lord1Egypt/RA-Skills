#!/usr/bin/env python3
"""New episodes for a client: from the show's RSS feed, a local or synced folder, or a file or link the
client sends. Each one goes into the client's queue once.

    python3 scripts/sources.py check <client-id>                # every source in client.json; new ones queued
    python3 scripts/sources.py check --all                      # every active client
    python3 scripts/sources.py add <client-id> <file or link> [--title "..."] [--published 2026-11-14]
    python3 scripts/sources.py queue <client-id>                # what's queued and what's started
    python3 scripts/sources.py start <client-id> <item id> [--episode ep-112] [--download]
                                  # the episode folder and a batch.json to fill in; --download fetches
                                  # a feed's enclosure into it

Sources in client.json:
  {"type": "rss", "url": "https://feeds.example.com/show.xml"}   the show's own feed: every <item> with
                                                                  an audio or video enclosure
  {"type": "folder", "path": "~/Shared/Clients/Orbit"}          new video or audio files in a folder the
                                                                  client syncs or drops files into
Files: clients/<id>/queue.json (one entry per episode found) and clients/<id>/sources-seen.json (what was
already seen, so nothing is queued twice). Only the client's own material: a YouTube link is queued
with a note and never downloaded by this skill; get the file from the client, or download it yourself
only when the client owns it and has given you the right to use it.
"""
import argparse, datetime, email.utils, os, re, shutil, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (client_dir, client_ids, die, guard, iso, now_utc, parse_time, read_json, rel, slug,  # noqa: E402
                       valid_id, workspace_of, write_json)

MEDIA_EXT = (".mp4", ".mov", ".m4v", ".mkv", ".webm", ".mp3", ".m4a", ".wav", ".aac")
VIDEO_EXT = (".mp4", ".mov", ".m4v", ".mkv", ".webm")
UA = "clipping-agency-skill (podcast feed reader)"


def load_client(ws, cid):
    path = os.path.join(client_dir(ws, cid), "client.json")
    if not os.path.isfile(path):
        die(f"no client \"{cid}\" (clients/{cid}/client.json)")
    c = read_json(path, "the client file")
    if not isinstance(c, dict):
        die(f"clients/{cid}/client.json must hold one JSON object")
    return c


def load_list(path, what):
    if not os.path.exists(path):
        return []
    data = read_json(path, what)
    if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
        die(f"{rel(path)} is damaged (it should be a list). It was left as it is")
    return data


def fetch(url, timeout=60):
    """The bytes at a link or a local file (file:// or a path)."""
    if re.match(r"(?i)^https?://", url):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:   # one plain line, whatever went wrong on the network
            die(f"couldn't read {url}: {getattr(e, 'reason', None) or e}")
    path = urllib.parse.urlparse(url).path if url.lower().startswith("file://") else os.path.expanduser(url)
    path = urllib.request.url2pathname(path) if url.lower().startswith("file://") else path
    if not os.path.isfile(path):
        die(f"{url} not found")
    with open(path, "rb") as fh:
        return fh.read()


def rss_items(data, url):
    """Episodes in an RSS feed: (guid, title, published, enclosure link, type, bytes)."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        die(f"{url} isn't a readable RSS feed ({e})")
    out = []
    for item in root.iter("item"):
        enc = item.find("enclosure")
        if enc is None or not enc.get("url"):
            continue
        link = enc.get("url").strip()
        kind = (enc.get("type") or "").lower()
        if kind and not kind.startswith(("audio/", "video/")):
            continue
        guid = (item.findtext("guid") or link).strip()
        title = " ".join((item.findtext("title") or "").split()) or os.path.basename(urllib.parse.urlparse(link).path)
        pub = None
        raw = item.findtext("pubDate")
        if raw:
            try:
                pub = iso(email.utils.parsedate_to_datetime(raw))
            except (TypeError, ValueError):
                pub = None
        try:
            size = int(enc.get("length") or 0)
        except ValueError:
            size = 0
        out.append({"guid": guid, "title": title, "published": pub, "url": link, "type": kind, "bytes": size})
    return out


def folder_items(path):
    p = os.path.expanduser(path)
    if not os.path.isdir(p):
        die(f"the source folder {path} isn't there (is the synced folder on this computer?)")
    out = []
    for name in sorted(os.listdir(p)):
        full = os.path.join(p, name)
        if name.startswith(".") or not name.lower().endswith(MEDIA_EXT) or not os.path.isfile(full):
            continue
        st = os.stat(full)
        out.append({"guid": f"file:{name}:{st.st_size}", "title": os.path.splitext(name)[0], "path": os.path.abspath(full),
                    "published": iso(datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc)), "bytes": st.st_size,
                    "type": "video" if name.lower().endswith(VIDEO_EXT) else "audio"})
    return out


def is_youtube(url):
    host = (urllib.parse.urlparse(url if "://" in url else "https://" + url).hostname or "").lower()
    return host.endswith(("youtube.com", "youtu.be"))


def queue_item(queue, seen, cid, src_label, it):
    """Add one found episode to the queue unless it was seen before. Returns the new entry or None."""
    if it["guid"] in seen:
        return None
    seen.add(it["guid"])
    n = len(queue) + 1
    entry = {"id": f"q{n:03d}", "source": src_label, "guid": it["guid"], "title": it.get("title"),
             "published": it.get("published"), "found": iso(now_utc()), "status": "new"}
    for k in ("url", "path", "type", "bytes"):
        if it.get(k):
            entry[k] = it[k]
    if entry.get("type", "").startswith("audio") or entry.get("type") == "audio":
        entry["note"] = ("audio only: clips need a picture. Ask the client for the video file, or make audiogram "
                         "clips by hand")
    queue.append(entry)
    return entry


def paths(ws, cid):
    d = client_dir(ws, cid)
    return os.path.join(d, "queue.json"), os.path.join(d, "sources-seen.json")


def check(ws, cid):
    c = load_client(ws, cid)
    if c.get("status") in ("offboarding", "offboarded", "paused"):
        print(f"{cid}: {c.get('status')}, not checked")
        return []
    qp, sp = paths(ws, cid)
    queue = load_list(qp, "the episode queue")
    seen_list = load_list(sp, "the seen list")
    seen = {s.get("guid") for s in seen_list}
    new = []
    sources = c.get("sources") if isinstance(c.get("sources"), list) else []
    if not sources:
        print(f"{cid}: no sources in client.json; the client sends files (sources.py add)")
    for s in sources:
        if not isinstance(s, dict) or s.get("type") not in ("rss", "folder"):
            die(f"clients/{cid}/client.json: each source is {{\"type\": \"rss\", \"url\": ...}} or "
                "{\"type\": \"folder\", \"path\": ...}")
        if s["type"] == "rss":
            if not isinstance(s.get("url"), str):
                die(f"clients/{cid}/client.json: an rss source needs its \"url\"")
            items = rss_items(fetch(s["url"]), s["url"])
            label = "rss"
        else:
            if not isinstance(s.get("path"), str):
                die(f"clients/{cid}/client.json: a folder source needs its \"path\"")
            items = folder_items(s["path"])
            label = "folder"
        first_run = not seen_list and not queue
        for it in items:
            if first_run and s.get("backfill") is not True and s["type"] == "rss" and it is not items[0]:
                seen.add(it["guid"])   # first look at a feed: only the newest episode, not the whole back catalogue
                continue
            e = queue_item(queue, seen, cid, label, it)
            if e:
                new.append(e)
    write_json(qp, queue)
    write_json(sp, [{"guid": g} for g in sorted(x for x in seen if x)])
    for e in new:
        print(f"{cid}: new {e['id']} \"{e.get('title')}\" ({e['source']}" + (f", {e['published'][:10]}" if e.get("published") else "")
              + ")" + (f". {e['note']}" if e.get("note") else ""))
    if not new:
        print(f"{cid}: nothing new")
    return new


def add(ws, cid, what, title=None, published=None):
    load_client(ws, cid)
    qp, sp = paths(ws, cid)
    queue = load_list(qp, "the episode queue")
    seen = {s.get("guid") for s in load_list(sp, "the seen list")}
    it = {"title": title}
    if published:
        t = parse_time(published if "T" in published else published + "T12:00:00Z")
        if not t:
            die("--published is a date like 2026-11-14")
        it["published"] = iso(t)
    if re.match(r"(?i)^(https?://|www\.)", what):
        it.update(guid="url:" + what, url=what)
        if is_youtube(what):
            it["type"] = "youtube"
    else:
        p = os.path.expanduser(what)
        if not os.path.isfile(p):
            die(f"{what} not found")
        st = os.stat(p)
        it.update(guid=f"file:{os.path.basename(p)}:{st.st_size}", path=os.path.abspath(p), bytes=st.st_size,
                  type="video" if p.lower().endswith(VIDEO_EXT) else "audio")
        it["title"] = it["title"] or os.path.splitext(os.path.basename(p))[0]
    e = queue_item(queue, seen, cid, "added", it)
    if not e:
        die(f"{what} is already in {cid}'s queue")
    if it.get("type") == "youtube":
        e["note"] = ("a YouTube link: this skill doesn't download it. Ask the client for the file (better quality than "
                     "YouTube's copy), or download it yourself only when the client owns it and has given you the right")
    write_json(qp, queue)
    write_json(sp, [{"guid": g} for g in sorted(x for x in seen if x)])
    print(f"{cid}: queued {e['id']} \"{e.get('title')}\"" + (f". {e['note']}" if e.get("note") else ""))


def show(ws, cid):
    qp, _ = paths(ws, cid)
    queue = load_list(qp, "the episode queue")
    if not queue:
        print(f"{cid}: queue empty")
    for e in queue:
        print(f"{e['id']}  {e.get('status'):8} {str(e.get('published') or '')[:10]:10}  {e.get('title')}"
              + (f"  -> episodes/{e['episode']}" if e.get("episode") else ""))


def start(ws, cid, item, episode=None, download=False):
    load_client(ws, cid)
    qp, _ = paths(ws, cid)
    queue = load_list(qp, "the episode queue")
    e = next((x for x in queue if x.get("id") == item), None)
    if not e:
        die(f"no queue item {item} for {cid} (sources.py queue {cid} lists them)")
    if e.get("episode"):
        die(f"{item} was already started as episodes/{e['episode']}")
    ep = episode or slug(e.get("title") or item)[:40]
    if not valid_id(ep):
        die(f"--episode {ep}: lowercase letters, digits and single dashes")
    edir = os.path.join(client_dir(ws, cid), "episodes", ep)
    if os.path.exists(os.path.join(edir, "batch.json")):
        die(f"episodes/{ep} already has a batch.json; give --episode another id")
    os.makedirs(edir, exist_ok=True)
    source = None
    if e.get("path"):
        source = e["path"]
    elif e.get("url") and e.get("type") == "youtube":
        print(f"note: {e.get('note')}")
    elif e.get("url"):
        ext = os.path.splitext(urllib.parse.urlparse(e["url"]).path)[1].lower() or ".mp4"
        if download:
            dest = os.path.join(edir, "source" + ext)
            print(f"downloading the episode from the client's feed into {rel(dest)} ...", flush=True)
            if re.match(r"(?i)^https?://", e["url"]):
                req = urllib.request.Request(e["url"], headers={"User-Agent": UA})
                try:
                    with urllib.request.urlopen(req, timeout=120) as r, open(dest + ".part", "wb") as fh:
                        shutil.copyfileobj(r, fh, 1 << 20)
                except Exception as err:
                    die(f"the download stopped: {getattr(err, 'reason', None) or err}. Run the same command again")
                os.replace(dest + ".part", dest)
            else:
                with open(dest, "wb") as fh:
                    fh.write(fetch(e["url"]))
            source = "source" + ext
        else:
            print(f"the episode is at {e['url']}; run again with --download to save it in the episode folder")
    batch = {"client": cid,
             "episode": {"id": ep, "title": e.get("title"), "published": e.get("published"), "queue_item": item,
                         "source": source, "transcript": "work/transcript.json",
                         "guests": [], "guest_release": "unknown", "sponsor_segments": [], "music": []},
             "clips": []}
    write_json(os.path.join(edir, "batch.json"), batch)
    e["status"] = "started"
    e["episode"] = ep
    write_json(qp, queue)
    print(f"{cid}: episodes/{ep}/batch.json written. Next: transcribe.py <source> --out work (in that folder), then "
          "pick the moments")


def main():
    ap = argparse.ArgumentParser(description="New episodes per client, from feeds, folders or files.")
    ap.add_argument("command", choices=["check", "add", "queue", "start"])
    ap.add_argument("client", nargs="?")
    ap.add_argument("what", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--title")
    ap.add_argument("--published")
    ap.add_argument("--episode")
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--workspace")
    a = ap.parse_args()
    ws = os.path.abspath(a.workspace) if a.workspace else (workspace_of(os.getcwd()) or os.getcwd())
    if a.command == "check":
        ids = client_ids(ws) if a.all else [a.client] if a.client else None
        if not ids:
            die("sources.py check <client-id>, or --all")
        for cid in ids:
            check(ws, cid)
        return
    if not a.client:
        die(f"sources.py {a.command} needs the client id")
    if a.command == "add":
        if not a.what:
            die("sources.py add <client-id> <file or link>")
        return add(ws, a.client, a.what, a.title, a.published)
    if a.command == "queue":
        return show(ws, a.client)
    if not a.what:
        die("sources.py start <client-id> <queue item id>")
    start(ws, a.client, a.what, a.episode, a.download)


if __name__ == "__main__":
    guard(main)

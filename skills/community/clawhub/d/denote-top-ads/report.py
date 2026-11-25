"""Generate a local Denote weekly report using the installed Skill client."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Event

from urllib.parse import urlsplit
from urllib.request import build_opener

from scripts.top_ads import NoRedirect, media_destination

ROOT = Path(__file__).resolve().parent
CHARTS = ("trending", "rising", "new")


def call(*arguments):
    result = subprocess.run([sys.executable, str(ROOT / "scripts/top_ads.py"), *arguments],
                            capture_output=True, text=True)
    if not result.returncode:
        return json.loads(result.stdout)["data"], None
    try:
        reason = json.loads(result.stderr)["error"]["reason_code"]
    except (KeyError, TypeError, ValueError):
        reason = "SOURCE_UNAVAILABLE"
    return {}, reason


def clean_url(value):
    return value if media_destination(value) else None


def block(detail, key):
    section = detail.get(key) or {}
    if section.get("locked") or section.get("entitled") is False:
        return None, "locked"
    if section.get("available"):
        return section.get("data") or {}, "empty"
    return {}, "unavailable"


def summarize(chart, item, detail, error, start, end):
    basic = detail.get("basic") or {}
    creative = basic.get("creative") or {}
    performance = detail.get("performance") or {}
    trend, trend_state = block(detail, "trend")
    related, related_state = block(detail, "related_ads")
    audience, audience_state = block(detail, "audience")
    denied = error in ("UPGRADE_REQUIRED", "SCOPE_DENIED")
    return dict(rank=item.get("rank"), key=item["creative_key"], title=item.get("title"),
                advertiser=item.get("advertiser"), platforms=item.get("platforms") or [],
                format=item.get("format"), preview=clean_url(item.get("preview_image_url")),
                video=clean_url(creative.get("video_url")), score=performance.get("weekly_score"),
                increment=performance.get("wow_growth"), rate=performance.get("wow_growth_rate"),
                days=(basic.get("duration") or {}).get("active_days"),
                states=["locked" if denied else ("ok" if basic else "unavailable"),
                        *([ "locked" ] * 3 if denied else [trend_state, related_state, audience_state])],
                trend=[[t.get("date_str"), t.get("value")] for t in (trend or {}).get("days", [])
                       if start <= str(t.get("date_str")) <= end],
                related=[[t.get("title") or t.get("brand_name"), t.get("platform")]
                         for t in (related or {}).get("same_material", [])[:10]],
                audience=[[t.get("code"), t.get("count")]
                          for t in (audience or {}).get("location_detail", [])[:10]])


def collect(category):
    ranking, error = call("rankings", "--app-type", category)
    if error:
        raise SystemExit("Rankings unavailable: " + error)
    start, end = ranking["week_start"], ranking["week_end"]
    jobs = [(chart, item) for chart in CHARTS for item in ranking["charts"][chart]["items"][:10]]
    stop = Event()
    stopped = []

    def read(job):
        chart, item = job
        if stop.is_set():
            detail, reason = {}, stopped[0]
        else:
            args = ("detail", "--app-type", category, "--chart", chart,
                    "--week-start", start, "--creative-key", item["creative_key"])
            detail, reason = call(*args)
            if reason == "SOURCE_UNAVAILABLE" and not stop.is_set():
                detail, reason = call(*args)
            if reason in ("UPGRADE_REQUIRED", "SCOPE_DENIED", "LOGIN_REQUIRED", "RATE_LIMITED"):
                stopped.append(reason)
                stop.set()
        return chart, summarize(chart, item, detail, reason, start, end)

    charts = {chart: [] for chart in CHARTS}
    if jobs:
        chart, row = read(jobs[0])
        charts[chart].append(row)
        with ThreadPoolExecutor(max_workers=3) as pool:
            for chart, row in pool.map(read, jobs[1:]):
                charts[chart].append(row)
    return dict(category=category, start=start, end=end, charts=charts)


def local_cover(url):
    """Embed public Denote JPEG/PNG/WebP covers; retain the API URL on failure."""
    if not url or urlsplit(url).scheme != "https" or urlsplit(url).netloc != "sp.dataideaglobal.com":
        return url
    limit = 2 * 1024 * 1024
    try:
        with build_opener(NoRedirect()).open(url, timeout=10) as response:
            raw = response.read(limit + 1)
    except (OSError, ValueError):
        return url
    if len(raw) > limit:
        return url
    if raw.startswith(bytes.fromhex("ffd8ff")):
        mime = "image/jpeg"
    elif raw.startswith(bytes.fromhex("89504e470d0a1a0a")):
        mime = "image/png"
    elif raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        return url
    return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")


def write_report(data, language, directory):
    directory.mkdir(parents=True, exist_ok=True)
    urls = list(dict.fromkeys(row["preview"] for rows in data["charts"].values() for row in rows))
    with ThreadPoolExecutor(max_workers=4) as pool:
        covers = dict(zip(urls, pool.map(local_cover, urls)))
    charts = {k: [dict(row, preview=covers[row["preview"]]) for row in rows]
              for k, rows in data["charts"].items()}
    payload = json.dumps(dict(data, charts=charts, language=language), ensure_ascii=False, allow_nan=False)
    html = (ROOT / "report.html").read_text(encoding="utf-8").replace(
        "__REPORT_JSON__", payload.replace("<", "\\u003c"))
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, delete=False,
                                     prefix=f"denote-{data['category']}-{data['start']}-",
                                     suffix=".html") as out:
        out.write(html)
    return Path(out.name).resolve()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-type", choices=("game", "app"), default="game")
    parser.add_argument("--language", choices="en zh ja ko es nl de fr".split(), default="en")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()
    data = collect(args.app_type)
    path = write_report(data, args.language, args.output_dir)
    print(json.dumps(dict(report_path=str(path), week_start=data["start"], week_end=data["end"],
                          charts={k: [{f:v for f,v in a.items() if f not in
                                  ("trend","related","audience","states")} for a in rows]
                                  for k,rows in data["charts"].items()}), ensure_ascii=False))

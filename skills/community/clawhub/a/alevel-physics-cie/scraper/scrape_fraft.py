#!/usr/bin/env python3
"""
Scrape all available 9702 files from cie.fraft.org using the site's real backend.

The FRANK CIE search UI submits:
  POST obj/Common/Fetch/renum
with form fields:
  subject=9702, year=<YYYY>, season=<Mar|Jun|Nov>

PDF downloads are served directly at:
  GET obj/Common/Fetch/redir/<filename>
"""

import json
import re
import time
from pathlib import Path
from typing import Optional

import requests
import yaml
from tqdm import tqdm

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

SEASONS = ["Mar", "Jun", "Nov"]
DEFAULT_YEARS = list(range(2001, time.localtime().tm_year + 1))
FILENAME_RE = re.compile(
    r"^(?P<subject>\d{4})_(?P<season>[smwn])(?P<year>\d{2})_(?P<kind>[a-z]{2})_(?P<variant>\d{2})\.pdf$",
    re.IGNORECASE,
)
TEXT_BASED_PAPERS = {"2", "4", "5"}


def load_config() -> dict:
    cfg_path = PROJECT_ROOT / "config.yaml"
    if not cfg_path.exists():
        return {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_config() -> dict:
    cfg = load_config()
    scraper = cfg.get("scraper", {})
    return {
        "base_url": scraper.get("base_url", "https://cie.fraft.org").rstrip("/"),
        "subject_code": scraper.get("subject_code", "9702"),
        "output_dir": PROJECT_ROOT / scraper.get("output_dir", "data/raw"),
        "request_delay_sec": scraper.get("request_delay_sec", 1.2),
        "user_agent": scraper.get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        ),
        "years": scraper.get("years", DEFAULT_YEARS),
        "max_retries": scraper.get("max_retries", 5),
    }


def parse_filename(filename: str) -> dict:
    match = FILENAME_RE.match(filename)
    if not match:
        return {
            "filename": filename,
            "kind": None,
            "paper": None,
            "variant": None,
            "is_text_based": False,
        }
    groups = match.groupdict()
    paper = groups["variant"][0]
    return {
        "filename": filename,
        "subject": groups["subject"],
        "season_code": groups["season"],
        "year_short": groups["year"],
        "kind": groups["kind"],
        "variant": groups["variant"],
        "paper": paper,
        "is_text_based": paper in TEXT_BASED_PAPERS and groups["kind"] == "qp",
    }


def create_session(config: dict) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": config["user_agent"],
            "Referer": f"{config['base_url']}/",
            "Accept": "application/json,text/html,application/pdf,*/*",
        }
    )
    session.get(config["base_url"], timeout=30)
    return session


def fetch_subjects(session: requests.Session, config: dict) -> set[str]:
    url = f"{config['base_url']}/obj/Common/Subject/combo"
    response = session.post(url, data={}, timeout=30)
    response.raise_for_status()
    rows = response.json()
    return {str(item.get("value")) for item in rows}


def fetch_listing(session: requests.Session, config: dict, year: int, season: str) -> list[dict]:
    url = f"{config['base_url']}/obj/Common/Fetch/renum"
    response = session.post(
        url,
        data={"subject": config["subject_code"], "year": str(year), "season": season},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("rows", [])
    results = []
    for row in rows:
        filename = row.get("file")
        if not filename or not str(filename).lower().endswith(".pdf"):
            continue
        meta = parse_filename(filename)
        meta.update(
            {
                "year": year,
                "season": season,
                "lessons": row.get("lessons"),
                "download_url": f"{config['base_url']}/obj/Common/Fetch/redir/{filename}",
            }
        )
        results.append(meta)
    return results


def download_file(session: requests.Session, item: dict, output_dir: Path, config: dict) -> Optional[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / item["filename"]
    if path.exists() and path.stat().st_size > 1024:
        return path

    backoff = max(config["request_delay_sec"], 1.0)
    for attempt in range(1, config["max_retries"] + 1):
        response = session.get(item["download_url"], timeout=60)
        if response.status_code == 429:
            wait_s = min(60, backoff * (2 ** (attempt - 1)))
            print(f"[WARN] 429 for {item['filename']}, retrying in {wait_s:.1f}s (attempt {attempt})")
            time.sleep(wait_s)
            continue
        response.raise_for_status()
        if "application/pdf" not in response.headers.get("Content-Type", "") and len(response.content) < 1024:
            return None

        with open(path, "wb") as f:
            f.write(response.content)
        return path

    return None


def main():
    config = get_config()
    out_dir = config["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    session = create_session(config)
    subjects = fetch_subjects(session, config)
    if config["subject_code"] not in subjects:
        raise RuntimeError(f"Subject {config['subject_code']} is not available on cie.fraft.org.")

    discovered = {}
    for year in tqdm(config["years"], desc="Years"):
        for season in SEASONS:
            try:
                rows = fetch_listing(session, config, year, season)
            except Exception as exc:
                print(f"[WARN] listing failed for {year} {season}: {exc}")
                continue
            for row in rows:
                discovered[row["filename"]] = row
            time.sleep(config["request_delay_sec"])

    items = [discovered[name] for name in sorted(discovered)]
    print(f"Discovered {len(items)} unique files for subject {config['subject_code']}.")

    downloaded = []
    for item in tqdm(items, desc="Downloading PDFs"):
        try:
            local_path = download_file(session, item, out_dir, config)
        except Exception as exc:
            print(f"[WARN] download failed for {item['filename']}: {exc}")
            continue
        if not local_path:
            continue
        record = dict(item)
        record["local_path"] = str(local_path)
        downloaded.append(record)
        time.sleep(config["request_delay_sec"])

    manifest = {
        "base_url": config["base_url"],
        "source": "cie.fraft.org",
        "subject": config["subject_code"],
        "items": downloaded,
    }
    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(downloaded)} PDFs to {out_dir}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

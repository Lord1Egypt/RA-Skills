"""Fetch hot short reviews from Douban Rexxar API."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_ENV_FILE = _ROOT / ".env"
if _ENV_FILE.exists():
    for _line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

sys.path.insert(0, str(Path(__file__).parent))
from monitor import rexxar_get

DATA_DIR = _ROOT / "data"
RESULT_FILE = DATA_DIR / "douban-monitor-result.json"
FAVORITES_FILE = DATA_DIR / "douban-monitor-favorites-result.json"
REVIEWS_FILE = DATA_DIR / "douban-monitor-reviews.json"


def _fetch_reviews(douban_id: str) -> list[dict]:
    """Fetch up to 6 hot short reviews for a subject."""
    for ep in (f"/movie/{douban_id}/interests", f"/tv/{douban_id}/interests"):
        try:
            data = rexxar_get(ep, params={
                "count": 6,
                "order_by": "hot",
                "status": "done",
            })
            interests = data.get("interests") or []
            reviews: list[dict] = []
            for it in interests:
                comment = (it.get("comment") or "").strip()
                if not comment:
                    continue
                user_info = it.get("user") or {}
                rating_obj = it.get("rating") or {}
                reviews.append({
                    "user": user_info.get("name", ""),
                    "rating": int(rating_obj["value"]) if rating_obj.get("value") else None,
                    "comment": comment,
                    "date": (it.get("create_time") or "")[:10],
                })
            if reviews:
                return reviews
        except Exception:
            continue
    return []


def main() -> None:
    # Collect all items from both result.json and favorites-result.json
    all_items: list[dict] = []
    seen_ids: set[str] = set()

    # From result.json (qualified)
    text = RESULT_FILE.read_text(encoding="utf-8").strip() if RESULT_FILE.exists() else ""
    if text:
        try:
            result = json.loads(text)
            for item in result.get("qualified", []):
                did = item.get("douban_id")
                if did and did not in seen_ids:
                    seen_ids.add(did)
                    all_items.append(item)
        except json.JSONDecodeError:
            pass

    # From favorites-result.json
    fav_text = FAVORITES_FILE.read_text(encoding="utf-8").strip() if FAVORITES_FILE.exists() else ""
    if fav_text:
        try:
            fav_data = json.loads(fav_text)
            for item in fav_data.get("qualified", []):
                did = item.get("douban_id")
                if did and did not in seen_ids:
                    seen_ids.add(did)
                    all_items.append(item)
        except json.JSONDecodeError:
            pass

    if not all_items:
        print("无作品需要抓取短评，跳过")
        return

    # Load existing reviews
    reviews: dict[str, list] = {}
    if REVIEWS_FILE.exists():
        text = REVIEWS_FILE.read_text(encoding="utf-8").strip()
        if text:
            try:
                reviews = json.loads(text)
            except (json.JSONDecodeError, ValueError):
                reviews = {}

    total = len(all_items)
    for i, item in enumerate(all_items):
        did = item["douban_id"]
        title = item["title"]
        prefix = f"[{i+1}/{total}]"

        if did in reviews and reviews[did]:
            print(f"{prefix} skip [OK] {title}")
            continue

        print(f"{prefix} {title}", end="  ", flush=True)
        revs = _fetch_reviews(did)
        reviews[did] = revs
        time.sleep(0.5)
        print(f"{len(revs)} 条短评" if revs else "(无短评)")

    REVIEWS_FILE.write_text(
        json.dumps(reviews, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    found = sum(1 for v in reviews.values() if v)
    print(f"\n完成：{found}/{len(reviews)} 条有短评，保存至 {REVIEWS_FILE}")


if __name__ == "__main__":
    main()

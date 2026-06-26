from __future__ import annotations

import argparse
from pathlib import Path

from deviantart_common import DeviantArtError, api_post_form, api_post_multipart, normalize_bool, sanitize_tags


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Upload and publish artwork to DeviantArt via Sta.sh")
    p.add_argument("--file", required=True, help="Path to the file to upload")
    p.add_argument("--title", required=True, help="Submission title")
    p.add_argument("--artist-comments", default="", help="Artist comments / description")
    p.add_argument("--tags", nargs="*", default=[], help="Tags")
    p.add_argument("--is-mature", required=True, help="true/false")
    p.add_argument("--mature-level", choices=["strict", "moderate"])
    p.add_argument("--mature-classification", nargs="*", default=[])
    p.add_argument("--allow-comments", default="true")
    p.add_argument("--allow-free-download", default=None)
    p.add_argument("--display-resolution", type=int, choices=list(range(0, 9)), default=None)
    p.add_argument("--add-watermark", default=None)
    p.add_argument("--is-ai-generated", default=None)
    p.add_argument("--noai", default=None)
    p.add_argument("--galleryid", action="append", default=[])
    p.add_argument("--subject-tags", nargs="*", default=[])
    p.add_argument("--subject-tag-types", nargs="*", default=[])
    p.add_argument("--location-tag", default=None)
    return p


def main() -> int:
    args = build_parser().parse_args()
    file_path = Path(args.file)
    if not file_path.exists() or not file_path.is_file():
        raise DeviantArtError(f"File not found: {file_path}")

    is_mature = normalize_bool(args.is_mature)
    if is_mature == "true" and not args.mature_level:
        raise DeviantArtError("--mature-level is required when --is-mature is true")

    add_watermark = normalize_bool(args.add_watermark) if args.add_watermark is not None else None
    if add_watermark == "true" and args.display_resolution is None:
        raise DeviantArtError("--display-resolution is required when --add-watermark is true")

    tags = sanitize_tags(args.tags)
    gallery_ids = list(args.galleryid or [])
    if args.gallery_name:
        gallery_ids.extend(resolve_gallery_names(args.gallery_name))

    publish_payload = {
        "is_mature": is_mature,
        "mature_level": args.mature_level,
        "mature_classification": args.mature_classification or None,
        "allow_comments": normalize_bool(args.allow_comments),
        "allow_free_download": normalize_bool(args.allow_free_download) if args.allow_free_download is not None else None,
        "display_resolution": args.display_resolution,
        "add_watermark": add_watermark,
        "galleryids": gallery_ids or None,
        "tags": tags or None,
        "subject_tags": args.subject_tags or None,
        "subject_tag_types": args.subject_tag_types or None,
        "location_tag": args.location_tag,
        "is_ai_generated": normalize_bool(args.is_ai_generated) if args.is_ai_generated is not None else None,
        "noai": normalize_bool(args.noai) if args.noai is not None else None,
    }

    if args.dry_run:
        print("Dry run only. No upload or publish call was made.")
        print(f"File: {file_path}")
        print(f"Title: {args.title}")
        print(f"Artist comments: {args.artist_comments}")
        print(f"Tags: {tags}")
        print(f"Resolved gallery IDs: {gallery_ids}")
        print(f"Publish payload: {publish_payload}")
        return 0

    submit_payload = {
        "title": args.title,
        "artist_comments": args.artist_comments,
        "tags": tags,
    }
    submit_resp = api_post_multipart("stash/submit", submit_payload, [("file", file_path)])
    itemid = submit_resp.get("itemid")
    if not itemid:
        raise DeviantArtError(f"Upload succeeded without itemid: {submit_resp}")

    publish_payload = {
        "itemid": itemid,
        "is_mature": is_mature,
        "mature_level": args.mature_level,
        "mature_classification": args.mature_classification or None,
        "allow_comments": normalize_bool(args.allow_comments),
        "allow_free_download": normalize_bool(args.allow_free_download) if args.allow_free_download is not None else None,
        "display_resolution": args.display_resolution,
        "add_watermark": add_watermark,
        "galleryids": args.galleryid or None,
        "tags": tags or None,
        "subject_tags": args.subject_tags or None,
        "subject_tag_types": args.subject_tag_types or None,
        "location_tag": args.location_tag,
        "is_ai_generated": normalize_bool(args.is_ai_generated) if args.is_ai_generated is not None else None,
        "noai": normalize_bool(args.noai) if args.noai is not None else None,
    }
    publish_resp = api_post_form("stash/publish", publish_payload)
    url = publish_resp.get("url")
    deviationid = publish_resp.get("deviationid")

    print("Publish successful.")
    print(f"Item ID: {itemid}")
    print(f"Deviation ID: {deviationid}")
    print(f"URL: {url}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeviantArtError as e:
        message = f"ERROR: {e}"
        try:
            print(message)
        except UnicodeEncodeError:
            safe = message.encode("ascii", errors="backslashreplace").decode("ascii")
            print(safe)
        raise SystemExit(1)

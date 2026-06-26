import argparse
import json

from api_utils import get_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Freesound.")
    parser.add_argument("query")
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--filter", action="append", default=[], help="Raw Freesound filter expression; may be repeated.")
    parser.add_argument("--tag", action="append", default=[], help="Tag to require; may be repeated.")
    parser.add_argument("--license", choices=["all", "cc0", "by", "by-nc"], default="all")
    parser.add_argument("--duration-min", type=float)
    parser.add_argument("--duration-max", type=float)
    args = parser.parse_args()

    filters = list(args.filter)
    for tag in args.tag:
        filters.append(f"tag:{tag}")
    if args.license == "cc0":
        filters.append('license:"Creative Commons 0"')
    elif args.license == "by":
        filters.append('license:"Attribution"')
    elif args.license == "by-nc":
        filters.append('license:"Attribution Noncommercial"')
    if args.duration_min is not None:
        filters.append(f"duration:[{args.duration_min} TO *]")
    if args.duration_max is not None:
        filters.append(f"duration:[* TO {args.duration_max}]")

    params = {
        "query": args.query,
        "page_size": args.page_size,
        "fields": "id,name,username,license,duration,url,previews,tags,type,filesize",
    }
    if filters:
        params["filter"] = " ".join(filters)

    data = get_json("/search/text/", params)

    slim = []
    for item in data.get("results", []):
        previews = item.get("previews") or {}
        slim.append(
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "username": item.get("username"),
                "license": item.get("license"),
                "duration": item.get("duration"),
                "type": item.get("type"),
                "filesize": item.get("filesize"),
                "url": item.get("url"),
                "preview_mp3": previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3"),
                "tags": item.get("tags") or [],
            }
        )
    print(json.dumps({"count": data.get("count"), "results": slim}, indent=2))


if __name__ == "__main__":
    main()

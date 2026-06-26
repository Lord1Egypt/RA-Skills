#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BUILDER_URL = "https://scraperapi.dataify.com/builder?platform=1"
DASHBOARD_URL = "https://dashboard.dataify.com?utm_source=skill"
LOGIN_URL = "https://dashboard.dataify.com/login?utm_source=skill"
MIN_PYTHON = (3, 6)

MODE_URL = "url"
MODE_CID = "cid"
MODE_LOCATION = "location"
MODE_PLACEID = "placeid"
SPIDER_IDS = {
    MODE_URL: "google_map-details_by-url",
    MODE_CID: "google_map-details_by-cid",
    MODE_LOCATION: "google_map-details_by-location",
    MODE_PLACEID: "google_map-details_by-placeid",
}
DEFAULT_URL = "https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1"
DEFAULT_CID = "2476046430038551731"
DEFAULT_KEYWORD = "pizza"
DEFAULT_COUNTRY = "us"
DEFAULT_LAT = "38"
DEFAULT_LONG = "77"
DEFAULT_ZOOM_LEVEL = "20"
DEFAULT_PLACE_ID = "ChIJ3S-JXmauEmsRUcIaWtf4MzE"
DEFAULT_FILE_NAME = "{{TasksID}}"
COUNTRY_VALUES = {
    "gb","af","al","dz","ax","as","ad","ao","ai","aq","ag","ar","am","aw","au","at","az","bs","bh","je","bd","bb","by","be","bz","bj","bm","bt","bo","bq","ba","bw","br","bn","bg","bf","bi","kh","cm","ca","cv","ky","cf","td","cl","cn","cx","cc","co","km","cg","ck","cr","ci","hr","cu","cw","cy","cz","cd","dk","dj","dm","do","ec","eg","sv","gq","er","eu","ee","et","fk","fo","fj","fi","fr","gf","pf","tf","ga","gm","ge","de","gh","gi","gr","gl","gd","gu","gp","gt","gg","gn","gw","gy","ht","hn","hk","hu","is","in","id","io","ir","iq","ie","im","il","it","jm","jp","jo","kz","ke","ki","xk","kw","kg","la","lv","lb","ls","lr","ly","li","lt","lu","mo","mk","mg","mw","my","mv","ml","mt","mh","mq","mr","mu","yt","mx","fm","md","mc","mn","me","ms","ma","mz","mm","na","nr","np","nl","an","nc","nz","ni","ne","ng","nu","nf","kp","mp","no","om","pk","pw","ps","pa","pg","py","pe","ph","pn","pl","pm","pt","pr","qa","re","ro","ru","rw","bl","sh","kn","lc","mf","vc","sm","st","sa","sn","rs","sc","sl","sg","sx","sk","si","sb","so","za","gs","kr","ss","es","lk","sd","sr","se","ch","sy","tw","tj","tz","th","tl","tg","tk","to","tt","tn","tr","tm","tc","tv","ug","ua","ae","uk","us","uz","vu","va","ve","vn","vg","vi","wf","eh","ws","ye","zm","zw","bv","hm"
}


def ensure_python_version():
    if sys.version_info < MIN_PYTHON:
        print(
            "Python {}.{} or newer is required. Run this script with a Python 3 interpreter, for example: python3 scripts/submit_dataify_google_map_details.py --mode location --keyword \"{}\"".format(
                MIN_PYTHON[0], MIN_PYTHON[1], DEFAULT_KEYWORD
            ),
            file=sys.stderr,
        )
        return False
    return True


def normalize_mode(value):
    clean = str(value).strip().lower()
    if clean not in SPIDER_IDS:
        raise ValueError("Unsupported mode: {}. Use url, cid, location, or placeid.".format(value))
    return clean


def normalize_text(value, field_name):
    clean = str(value).strip()
    if not clean:
        raise ValueError("{} cannot be empty".format(field_name))
    return clean


def normalize_url(value):
    clean = normalize_text(value, "url")
    if not clean.startswith("https://www.google.com/maps/"):
        raise ValueError("url must start with https://www.google.com/maps/")
    return clean


def normalize_country(value):
    clean = str(value).strip().lower()
    if clean not in COUNTRY_VALUES:
        raise ValueError("country must be one of the allowed Google country values")
    return clean


def normalize_number(value, field_name):
    clean = str(value).strip()
    try:
        float(clean)
    except ValueError:
        raise ValueError("{} must be numeric".format(field_name))
    return clean


def normalize_non_negative_integer(value, field_name):
    clean = str(value).strip()
    if not clean or not clean.isdigit():
        raise ValueError("{} must be an integer greater than or equal to 0".format(field_name))
    return clean


def normalize_file_name(value):
    if value is None:
        return DEFAULT_FILE_NAME
    clean = str(value).strip()
    if not clean:
        raise ValueError("File name cannot be empty")
    return clean


def normalize_group(group, mode):
    if mode == MODE_URL:
        return {"url": normalize_url(group.get("url", DEFAULT_URL))}
    if mode == MODE_CID:
        return {"CID": normalize_text(group.get("CID", DEFAULT_CID), "CID")}
    if mode == MODE_LOCATION:
        return {
            "keyword": normalize_text(group.get("keyword", DEFAULT_KEYWORD), "keyword"),
            "country": normalize_country(group.get("country", DEFAULT_COUNTRY)),
            "lat": normalize_number(group.get("lat", DEFAULT_LAT), "lat"),
            "long": normalize_number(group.get("long", DEFAULT_LONG), "long"),
            "zoom_level": normalize_non_negative_integer(group.get("zoom_level", DEFAULT_ZOOM_LEVEL), "zoom_level"),
        }
    return {"place_id": normalize_text(group.get("place_id", DEFAULT_PLACE_ID), "place_id")}


def load_groups_from_json(raw, mode):
    try:
        payload = json.loads(raw)
    except ValueError as exc:
        raise ValueError("params-json must be valid JSON: {}".format(exc))
    if not isinstance(payload, list) or not payload:
        raise ValueError("params-json must be a non-empty JSON array")
    groups = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("Each params-json item must be an object")
        groups.append(normalize_group(item, mode))
    return groups


def build_groups(args, mode):
    if args.params_json:
        return load_groups_from_json(args.params_json, mode)
    if mode == MODE_URL:
        return [normalize_group({"url": url}, mode) for url in (args.url or [DEFAULT_URL])]
    if mode == MODE_CID:
        return [normalize_group({"CID": cid}, mode) for cid in (args.cid or [DEFAULT_CID])]
    if mode == MODE_LOCATION:
        keywords = args.keyword or [DEFAULT_KEYWORD]
        return [
            normalize_group(
                {
                    "keyword": keyword,
                    "country": args.country,
                    "lat": args.lat,
                    "long": args.long,
                    "zoom_level": args.zoom_level,
                },
                mode,
            )
            for keyword in keywords
        ]
    return [normalize_group({"place_id": place_id}, mode) for place_id in (args.place_id or [DEFAULT_PLACE_ID])]


def submit_builder(api_token, mode, groups, file_name):
    spider_id = SPIDER_IDS[mode]
    form = {
        "spider_name": "google.com",
        "spider_id": spider_id,
        "spider_parameters": json.dumps(groups, ensure_ascii=False, separators=(",", ":")),
        "spider_errors": "true",
        "file_name": file_name,
    }
    body = urllib.parse.urlencode(form).encode("utf-8")
    request = urllib.request.Request(
        BUILDER_URL,
        data=body,
        headers={"Authorization": "Bearer {}".format(api_token), "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError("Builder request failed with HTTP {}: {}".format(exc.code, detail))
    except urllib.error.URLError as exc:
        raise RuntimeError("Builder request failed: {}".format(exc.reason))
    try:
        payload = json.loads(raw)
    except ValueError:
        raise RuntimeError("Builder returned non-JSON response: {}".format(raw))
    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}
    task_id = data.get("task_id")
    if not task_id:
        raise RuntimeError("Builder did not return task_id. Response: {}".format(json.dumps(payload, ensure_ascii=False)))
    status = data.get("status") or payload.get("status") or payload.get("message") or "submitted"
    return spider_id, task_id, status


def main():
    if not ensure_python_version():
        return 2
    parser = argparse.ArgumentParser(description="Submit a guided Dataify Google Map Details Builder task.")
    parser.add_argument("--mode", required=True, help="Collection mode. Allowed values: url, cid, location, placeid.")
    parser.add_argument("--url", action="append", help="URL mode only. Repeat for multiple URLs.")
    parser.add_argument("--cid", action="append", help="CID mode only. Repeat for multiple CIDs.")
    parser.add_argument("--keyword", action="append", help="Location mode only. Repeat for multiple keywords.")
    parser.add_argument("--country", default=DEFAULT_COUNTRY, help="Location mode only. Default: us.")
    parser.add_argument("--lat", default=DEFAULT_LAT, help="Location mode only. Default: 38.")
    parser.add_argument("--long", default=DEFAULT_LONG, help="Location mode only. Default: 77.")
    parser.add_argument("--zoom-level", default=DEFAULT_ZOOM_LEVEL, help="Location mode only. Default: 20.")
    parser.add_argument("--place-id", action="append", help="Place ID mode only. Repeat for multiple place IDs.")
    parser.add_argument("--file-name", default=DEFAULT_FILE_NAME, help="Builder file_name field. Default: {{TasksID}}.")
    parser.add_argument("--params-json", help="JSON array of parameter objects for the selected mode.")
    parser.add_argument("--api-token", default=os.environ.get("DATAIFY_API_TOKEN"), help="Dataify token. Defaults to DATAIFY_API_TOKEN.")
    args = parser.parse_args()

    if not args.api_token:
        print(
            "Missing Dataify API TOKEN. Enter your Dataify API TOKEN to continue. If you want to reuse it later, save it as DATAIFY_API_TOKEN. If you do not have one, log in at {} to get one.".format(LOGIN_URL),
            file=sys.stderr,
        )
        return 2
    try:
        mode = normalize_mode(args.mode)
        groups = build_groups(args, mode)
        file_name = normalize_file_name(args.file_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        spider_id, task_id, status = submit_builder(args.api_token, mode, groups, file_name)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps({"mode": mode, "spider_id": spider_id, "task_id": task_id, "status": status, "parameters": groups, "file_name": file_name, "dashboard_url": DASHBOARD_URL, "message": "Task submitted. Visit {} to view results.".format(DASHBOARD_URL)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

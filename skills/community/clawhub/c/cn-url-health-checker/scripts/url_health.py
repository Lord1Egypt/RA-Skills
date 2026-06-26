#!/usr/bin/env python3

import argparse, json, sys, urllib.request, urllib.error

def check_url(url):
    result = {"url": url, "status": None, "redirects": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        result["status"] = resp.status
        result["final_url"] = resp.url
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    print(json.dumps(check_url(args.url), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

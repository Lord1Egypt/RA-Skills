#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error

def print_help():
    print("""
Bing Webmaster Tools URL Submission Script (Zero-Dependency)

Usage:
  python3 submit_urls.py --site-url <SITE_URL> --urls <URL1,URL2,...> [--api-key <API_KEY>]
  python3 submit_urls.py --site-url <SITE_URL> --file <PATH_TO_URLS_FILE> [--api-key <API_KEY>]

Environment Variable:
  BING_WEBMASTER_API_KEY: Will be used if --api-key is not provided.
""")

def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args or not args:
        print_help()
        sys.exit(0)

    site_url = None
    urls_str = None
    file_path = None
    api_key = os.environ.get("BING_WEBMASTER_API_KEY")

    # Simple argument parsing
    i = 0
    while i < len(args):
        if args[i] == "--site-url":
            site_url = args[i+1]
            i += 2
        elif args[i] == "--urls":
            urls_str = args[i+1]
            i += 2
        elif args[i] == "--file":
            file_path = args[i+1]
            i += 2
        elif args[i] == "--api-key":
            api_key = args[i+1]
            i += 2
        else:
            print(f"Unknown argument: {args[i]}")
            print_help()
            sys.exit(1)

    if not site_url:
        print("Error: --site-url is required.")
        sys.exit(1)

    if not api_key:
        print("Error: Bing Webmaster API Key is missing. Provide it via --api-key or set BING_WEBMASTER_API_KEY env variable.")
        sys.exit(1)

    url_list = []
    if urls_str:
        url_list = [u.strip() for u in urls_str.split(",") if u.strip()]
    elif file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                url_list = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            sys.exit(1)
    else:
        print("Error: Either --urls or --file must be provided.")
        sys.exit(1)

    if not url_list:
        print("Error: No URLs to submit.")
        sys.exit(1)

    # If only 1 URL, we can use SubmitUrl, but SubmitUrlbatch works for 1 or more URLs as well.
    # Let's use SubmitUrlbatch for all submissions to keep it clean and robust, or route based on count.
    is_batch = len(url_list) > 1

    if not is_batch:
        # Single URL submission
        endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrl?apikey={api_key}"
        payload = {
            "siteUrl": site_url,
            "url": url_list[0]
        }
    else:
        # Batch URL submission
        endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={api_key}"
        payload = {
            "siteUrl": site_url,
            "urlList": url_list
        }

    print(f"Submitting {len(url_list)} URL(s) for site '{site_url}'...")
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=req_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            res_body = response.read().decode("utf-8")
            
            # Bing Webmaster API returns {"d": null} on success
            if status_code == 200:
                print("🎉 Submission successful!")
                print(f"Response: {res_body}")
                for u in url_list:
                    print(f"  [SUBMITTED] {u}")
            else:
                print(f"⚠️ Submission received non-200 status code: {status_code}")
                print(f"Response: {res_body}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            print(f"Details: {error_body}")
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"❌ General Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

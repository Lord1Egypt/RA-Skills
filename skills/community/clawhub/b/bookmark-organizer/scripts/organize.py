
#!/usr/bin/env python3
import sys
import re
import json
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse, urlunparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_with_regex(html_content):
    links = []
    link_pattern = re.compile(r'<A HREF="(.*?)" ADD_DATE="(\d+)"[^>]*?>(.*?)</A>', re.IGNORECASE | re.DOTALL)
    for match in link_pattern.finditer(html_content):
        url, add_date_str, title_html = match.groups()
        title = re.sub('<.*?>', '', title_html).strip()
        if url.startswith('http'):
            links.append({
                'title': title,
                'url': url,
                'add_date': int(add_date_str)
            })
    return links

def classify_link(link, rules):
    search_text = (link['title'] + ' ' + link['url']).lower()
    for category, keywords in rules.items():
        if any(keyword in search_text for keyword in keywords):
            return category
    return 'misc'

def check_url(url):
    command = ['curl', '-L', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-m', '15', url]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            return (url, None, f"curl exit code {result.returncode}")
        status_code = int(result.stdout.strip())
        if status_code >= 400:
            return (url, status_code, None)
    except Exception as e:
        return (url, None, str(e))
    return None

def main():
    parser = argparse.ArgumentParser(description="Organize browser bookmarks into a curated knowledge base.")
    parser.add_argument('input_file', type=str, help="Path to the bookmarks.html file.")
    parser.add_argument('output_dir', type=str, help="Directory to save the organized markdown files.")
    parser.add_argument('--check-links', action='store_true', help="Check for dead links (can be slow).")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    out_path = Path(args.output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    rules_path = Path(__file__).parent / 'rules.json'
    print(f"Loading rules from {rules_path}...")
    with rules_path.open('r', encoding='utf-8') as f:
        rules = json.load(f)

    print(f"Reading bookmarks from {in_path}...")
    html_content = in_path.read_text(encoding='utf-8', errors='ignore')
    all_links = parse_with_regex(html_content)
    print(f"Found {len(all_links)} total links.")

    # Deduplicate by URL
    unique_links = []
    seen_urls = set()
    for link in all_links:
        if link['url'] not in seen_urls:
            unique_links.append(link)
            seen_urls.add(link['url'])
    print(f"Found {len(unique_links)} unique links after deduplication.")

    # Classify
    buckets = defaultdict(list)
    for link in unique_links:
        category = classify_link(link, rules)
        buckets[category].append(link)

    # Optional: Check for dead links
    dead_links_report = []
    if args.check_links:
        urls_to_check = [link['url'] for link in unique_links]
        print(f"Checking {len(urls_to_check)} links for availability (this may take several minutes)...")
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(check_url, url): url for url in urls_to_check}
            for i, future in enumerate(as_completed(future_to_url)):
                print(f"Progress: {i + 1}/{len(urls_to_check)}", end='\r', file=sys.stderr)
                result = future.result()
                if result:
                    dead_links_report.append(result)
        print("\nLink check complete.")
        
        dead_link_urls = {res[0] for res in dead_links_report}
        # Filter dead links out of buckets
        for category, cat_links in buckets.items():
            buckets[category] = [link for link in cat_links if link['url'] not in dead_link_urls]

        # Write dead link report
        report_path = out_path / '_dead_links_report.md'
        with report_path.open('w', encoding='utf-8') as f:
            f.write(f"# Dead Links Report\n\nFound {len(dead_links_report)} problematic links.\n\n")
            for url, status, error in sorted(dead_links_report):
                if status:
                    f.write(f"- [Status {status}] {url}\n")
                else:
                    f.write(f"- [Error] {url} ({error})\n")
        print(f"Dead links report saved to {report_path}")

    # Write out categorized files
    for category, cat_links in buckets.items():
        file_path = out_path / f"{category}.md"
        with file_path.open('w', encoding='utf-8') as f:
            f.write(f"# Category: {category}\n\nTotal: {len(cat_links)} links\n\n")
            for link in sorted(cat_links, key=lambda x: x['add_date'], reverse=True):
                date_str = datetime.fromtimestamp(link['add_date']).strftime("%Y-%m-%d")
                f.write(f"- **[{date_str}]** [{link['title']}]({link['url']})\n")
    print(f"Wrote {len(buckets)} category files to {out_path}")

    # Create a final summary/index file
    summary_path = out_path / '_SUMMARY.md'
    with summary_path.open('w', encoding='utf-8') as f:
        f.write('# Bookmark Library Summary\n\n')
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total unique links: {len(unique_links)}\n")
        if args.check_links:
            f.write(f"Problematic links found: {len(dead_links_report)}\n")
        f.write('\n## Categories\n\n')
        for category, cat_links in sorted(buckets.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"- `{category}.md` - {len(cat_links)} links\n")
    print(f"Summary written to {summary_path}")

if __name__ == "__main__":
    main()

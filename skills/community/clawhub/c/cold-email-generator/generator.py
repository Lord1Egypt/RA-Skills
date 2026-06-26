#!/usr/bin/env python3
"""
Cold Email Auto-Generator — Gracie AI Receptionist
Scrapes a business website and generates a personalized cold email via Ollama.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRAPE_SCRIPT = "/Users/wlc-studio/StudioBrain/00_SYSTEM/skills/scrapling/scrape.py"
LEADS_FILE = Path.home() / "StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md"
OUTREACH_DIR = Path.home() / "StudioBrain/30_INTERNAL/WLC-Services/OUTREACH"


def scrape_url(url: str) -> str:
    """Scrape a URL and return its text content."""
    try:
        r = subprocess.run(
            ["python3", SCRAPE_SCRIPT, "web", url],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0 or not r.stdout.strip():
            return ""
        d = json.loads(r.stdout)
        content = d.get("content", [])
        if isinstance(content, list):
            return " ".join(c for c in content if c).strip()
        return str(content).strip()
    except Exception as e:
        print(f"  [scrape error] {url}: {e}", file=sys.stderr)
        return ""


def scrape_business(url: str) -> str:
    """Scrape homepage and try to also grab about/contact subpages."""
    base = url.rstrip("/")
    texts = []

    # Homepage
    print(f"  Scraping: {base}", file=sys.stderr)
    home_text = scrape_url(base)
    if home_text:
        texts.append(home_text)

    # Try common subpages
    for path in ["/about", "/about-us", "/contact", "/services"]:
        sub_url = base + path
        print(f"  Scraping: {sub_url}", file=sys.stderr)
        sub_text = scrape_url(sub_url)
        if sub_text and len(sub_text) > 100:
            texts.append(sub_text)

    combined = " ".join(texts)
    # Trim to ~2000 chars to keep Ollama prompt manageable
    return combined[:2000] if combined else ""


def generate_email(business_name: str, scraped_content: str) -> str:
    """Use Ollama llama3.2 to generate a cold email."""
    if scraped_content:
        context_section = f"Here's what their website says: {scraped_content}"
    else:
        context_section = "No website content was available, but use what you know about businesses in their industry."

    prompt = (
        f"Write a cold email FROM Jay Jimenez at White Lighter Club Studios "
        f"TO the owner of {business_name}. "
        f"You are pitching Gracie, an AI receptionist service ($299 setup + $399/mo). "
        f"{context_section} "
        f"IMPORTANT: Address the email to 'Hi [their business name] team,' or 'Hi there,' — NOT to Jay. Jay is the SENDER not the recipient. "
        f"Write 3 short paragraphs: "
        f"(1) Open with one specific detail about their business that shows you did your homework. "
        f"(2) Mention the missed call problem — every unanswered call is a lost customer. "
        f"(3) Introduce Gracie: AI receptionist, $299 setup + $399/mo flat, no contracts. "
        f"End with: 'Call (347) 851-1505 right now — hear her answer live.' "
        f"Keep it under 150 words total. No fluff. Sound like a real human, not a salesman. "
        f"Sign off: Jay Jimenez, White Lighter Club Studios."
    )

    print(f"  Generating email via Ollama...", file=sys.stderr)
    try:
        r = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True, text=True, timeout=120
        )
        email = r.stdout.strip()
        if not email:
            return f"[ERROR] Ollama returned no output. stderr: {r.stderr[:200]}"
        return email
    except subprocess.TimeoutExpired:
        return "[ERROR] Ollama timed out after 120 seconds."
    except Exception as e:
        return f"[ERROR] Ollama failed: {e}"


def save_email(business_name: str, email: str, phone: str = "") -> Path:
    """Save email to OUTREACH dir."""
    OUTREACH_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "-", business_name.lower()).strip("-")
    out_path = OUTREACH_DIR / f"{safe_name}.txt"

    header = f"Business: {business_name}\n"
    if phone:
        header += f"Phone: {phone}\n"
    header += "---\n\n"

    out_path.write_text(header + email + "\n")
    return out_path


def process_business(name: str, url: str, phone: str = "", save: bool = False):
    """Full pipeline for one business."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Business: {name}", file=sys.stderr)
    print(f"URL: {url}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    content = scrape_business(url)
    if not content:
        print(f"  [warn] No content scraped — proceeding with name only.", file=sys.stderr)

    email = generate_email(name, content)

    print(f"\n--- EMAIL FOR: {name} ---")
    print(email)
    print()

    if save:
        path = save_email(name, email, phone)
        print(f"[saved] {path}")

    return email


def parse_leads_file() -> list[dict]:
    """
    Parse MASTER_LEAD_LIST.md for leads with URLs.
    Expects markdown table rows or lines with a URL pattern.
    Returns list of dicts with keys: name, url, phone
    """
    if not LEADS_FILE.exists():
        print(f"[error] Leads file not found: {LEADS_FILE}", file=sys.stderr)
        return []

    content = LEADS_FILE.read_text()
    leads = []

    # Match markdown table rows: | Name | Phone | URL | ...
    # Try to find rows containing http links
    url_pattern = re.compile(r'https?://[^\s|)>\]"]+')
    
    for line in content.splitlines():
        # Skip header/separator lines
        if line.strip().startswith("|---") or line.strip() == "":
            continue

        urls = url_pattern.findall(line)
        if not urls:
            continue

        # Extract columns from table row
        cols = [c.strip() for c in line.split("|") if c.strip()]
        name = cols[0] if cols else "Unknown"
        
        # Try to find phone number in line
        phone_match = re.search(r'\(?\d{3}\)?[\s\-]\d{3}[\s\-]\d{4}', line)
        phone = phone_match.group(0) if phone_match else ""

        for url in urls:
            # Clean trailing punctuation
            url = url.rstrip(".,;)")
            leads.append({"name": name, "url": url, "phone": phone})
            break  # One URL per lead

    return leads


def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized cold emails pitching Gracie AI Receptionist."
    )
    parser.add_argument("--name", help="Business name")
    parser.add_argument("--url", help="Business website URL")
    parser.add_argument("--phone", default="", help="Business phone number")
    parser.add_argument("--save", action="store_true", help="Save email to OUTREACH dir")
    parser.add_argument("--list", action="store_true", help="Process all leads from MASTER_LEAD_LIST.md")

    args = parser.parse_args()

    if args.list:
        leads = parse_leads_file()
        if not leads:
            print("[error] No leads with URLs found in MASTER_LEAD_LIST.md")
            sys.exit(1)
        print(f"Found {len(leads)} leads with URLs.")
        for lead in leads:
            process_business(lead["name"], lead["url"], lead.get("phone", ""), args.save)
    elif args.name and args.url:
        process_business(args.name, args.url, args.phone, args.save)
    else:
        parser.print_help()
        print("\n[error] Provide --name and --url, or use --list")
        sys.exit(1)


if __name__ == "__main__":
    main()

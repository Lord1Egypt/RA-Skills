#!/usr/bin/env python3
"""
AEGIS Scanner — Core scanning engine for the AEGIS OpenClaw skill.
Location-aware, multi-source OSINT aggregation with threat classification.

Usage:
  python3 aegis_scanner.py                  # Interactive scan, prints results
  python3 aegis_scanner.py --cron           # Cron mode, outputs JSON for OpenClaw
  python3 aegis_scanner.py --config /path   # Custom config path
  python3 aegis_scanner.py --sources        # List active sources for location
"""

import json, os, sys, re, hashlib, time, subprocess, argparse, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ------- Configuration -------

DEFAULT_CONFIG_PATHS = [
    os.path.expanduser("~/.openclaw/aegis-config.json"),
    os.path.join(os.path.dirname(__file__), "..", "aegis-config.json"),
]

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
DATA_DIR = Path(os.environ.get("AEGIS_DATA_DIR", os.path.expanduser("~/.openclaw/aegis-data")))
SEEN_FILE = DATA_DIR / "seen_hashes.json"
ALERTS_FILE = DATA_DIR / "pending_alerts.json"
SCAN_LOG = DATA_DIR / "scan_log.json"

# ------- Helpers -------

def load_config(config_path=None):
    """Load AEGIS configuration."""
    paths = [config_path] if config_path else DEFAULT_CONFIG_PATHS
    for p in paths:
        if p and os.path.exists(p):
            with open(p) as f:
                return json.load(f)
    print("[AEGIS] No config found. Run aegis_onboard.py first.", file=sys.stderr)
    sys.exit(1)

def load_source_registry():
    """Load the source registry."""
    reg_file = REFERENCES_DIR / "source-registry.json"
    if not reg_file.exists():
        print(f"[AEGIS] Source registry not found: {reg_file}", file=sys.stderr)
        sys.exit(1)
    with open(reg_file) as f:
        return json.load(f)

def load_threat_keywords():
    """Load threat keyword patterns."""
    kw_file = REFERENCES_DIR / "threat-keywords.json"
    if not kw_file.exists():
        return {"critical": {"patterns": {"en": []}}, "high": {"patterns": {"en": []}}, "medium": {"patterns": {"en": []}}}
    with open(kw_file) as f:
        return json.load(f)

def load_country_profile(country_code):
    """Load country-specific profile."""
    profile_file = REFERENCES_DIR / "country-profiles" / f"{country_code.lower()}.json"
    # Try slug-based names too
    if not profile_file.exists():
        for f in (REFERENCES_DIR / "country-profiles").glob("*.json"):
            if f.stem.startswith("_"):
                continue
            try:
                data = json.loads(f.read_text())
                if data.get("country_code", "").upper() == country_code.upper():
                    return data
            except:
                continue
    if profile_file.exists():
        with open(profile_file) as f:
            return json.load(f)
    return None

def load_seen():
    """Load seen content hashes."""
    try:
        with open(SEEN_FILE) as f:
            data = json.load(f)
        # Prune entries older than 48h
        cutoff = time.time() - 48 * 3600
        return {k: v for k, v in data.items() if v > cutoff}
    except:
        return {}

def save_seen(seen):
    """Save seen content hashes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, 'w') as f:
        json.dump(seen, f)

def content_hash(text):
    """Generate hash for content deduplication."""
    normalized = re.sub(r'\s+', ' ', text.strip().lower())
    return hashlib.sha256(normalized[:2000].encode()).hexdigest()[:16]

def get_sources_for_location(registry, config):
    """Filter sources relevant to user's location."""
    country = config.get("location", {}).get("country", "").upper()
    sources = []
    for src in registry.get("sources", []):
        countries = [c.upper() for c in src.get("countries", [])]
        if "GLOBAL" in countries or country in countries:
            # Skip API sources that require keys we don't have
            if src.get("requires_key"):
                key_name = src.get("key_name", "")
                api_keys = config.get("api_keys", {})
                if not api_keys.get(key_name):
                    continue
            sources.append(src)
    return sources

# ------- Fetchers -------

def fetch_rss(url, max_items=20):
    """Fetch and parse RSS/XML feed. Returns list of items."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "--compressed",
             "-H", "User-Agent: AEGIS/1.0 (OpenClaw Emergency Intelligence)",
             url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return []
        
        items = []
        try:
            root = ET.fromstring(result.stdout)
            # Handle RSS 2.0
            for item in root.findall('.//item')[:max_items]:
                title = item.findtext('title', '').strip()
                desc = item.findtext('description', '').strip()
                link = item.findtext('link', '').strip()
                pubdate = item.findtext('pubDate', '').strip()
                # Strip CDATA and HTML from description
                desc = re.sub(r'<!\[CDATA\[|\]\]>', '', desc)
                desc = re.sub(r'<[^>]+>', ' ', desc)
                desc = re.sub(r'\s+', ' ', desc).strip()
                if title:
                    items.append({
                        "title": title,
                        "description": desc[:500],
                        "url": link,
                        "published": pubdate,
                        "raw": f"{title}. {desc}"
                    })
            # Handle Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('.//atom:entry', ns)[:max_items]:
                title = entry.findtext('atom:title', '', ns).strip()
                summary = entry.findtext('atom:summary', '', ns).strip()
                link_el = entry.find('atom:link', ns)
                link = link_el.get('href', '') if link_el is not None else ''
                if title:
                    items.append({
                        "title": title,
                        "description": re.sub(r'<[^>]+>', ' ', summary)[:500],
                        "url": link,
                        "raw": f"{title}. {summary}"
                    })
        except ET.ParseError:
            pass
        return items
    except Exception as e:
        return []

def fetch_web(url, max_chars=8000, ssl_verify=True):
    """Fetch web page and extract text.

    Security: TLS verification is ALWAYS enforced.
    If a source requires disabling verification, it is skipped (risk: MITM injection).
    """
    try:
        cmd = ["curl", "-sL", "--max-time", "15", "--compressed",
             "-H", "User-Agent: Mozilla/5.0 (compatible; AEGIS/1.0)"]
        if not ssl_verify:
            # Never disable TLS verification.
            # Return empty so the scanner continues safely.
            return []
        cmd.append(url)
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return []
        
        html = result.stdout
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        page_title = title_match.group(1).strip() if title_match else ""
        
        # Extract article-like content
        # Look for headline patterns in h1-h3 and article text
        items = []
        
        # Find headlines with links
        headline_pattern = r'<(?:h[1-3]|a)[^>]*>([^<]{15,200})</(?:h[1-3]|a)>'
        headlines = re.findall(headline_pattern, html, re.IGNORECASE)
        
        # Also find article/card patterns
        article_pattern = r'<article[^>]*>(.*?)</article>'
        articles = re.findall(article_pattern, html, re.DOTALL | re.IGNORECASE)[:10]
        
        for article_html in articles:
            a_title = ""
            a_link = ""
            a_desc = ""
            
            t_match = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', article_html, re.DOTALL | re.IGNORECASE)
            if t_match:
                a_title = re.sub(r'<[^>]+>', '', t_match.group(1)).strip()
            
            l_match = re.search(r'href="([^"]+)"', article_html)
            if l_match:
                a_link = l_match.group(1)
                if a_link.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    a_link = f"{parsed.scheme}://{parsed.netloc}{a_link}"
            
            p_match = re.search(r'<p[^>]*>(.*?)</p>', article_html, re.DOTALL | re.IGNORECASE)
            if p_match:
                a_desc = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            
            if a_title and len(a_title) > 10:
                items.append({
                    "title": a_title[:200],
                    "description": a_desc[:500],
                    "url": a_link,
                    "raw": f"{a_title}. {a_desc}"
                })
        
        # Fallback: if no articles found, extract raw text
        if not items:
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()[:max_chars]
            if text:
                items.append({
                    "title": page_title or url,
                    "description": text[:500],
                    "url": url,
                    "raw": text
                })
        
        return items
    except Exception as e:
        return []

def fetch_liveuamap(url, max_items=25):
    """Fetch events from LiveUAMap pages (structured HTML with data-* attributes)."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "--compressed",
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
             "-H", "Accept: text/html,application/xhtml+xml",
             url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return []
        
        html = result.stdout
        items = []
        
        # Extract structured events from data-link and title attributes
        # Pattern: <div ... data-link="URL" ... class="event ..." ...>
        #   <a ... title="HEADLINE" ...>LOCATION</a>
        #   <span class="date_add">TIME AGO</span>
        event_blocks = re.findall(
            r'data-link="([^"]+)"[^>]*data-id="(\d+)"[^>]*class="event[^"]*".*?'
            r'title="([^"]*)"[^>]*>([^<]*)<.*?'
            r'class="date_add">([^<]*)<',
            html, re.DOTALL
        )
        
        for link, evt_id, title, location, time_ago in event_blocks[:max_items]:
            title = title.replace('&#039;', "'").replace('&amp;', '&').replace('&quot;', '"').strip()
            location = location.strip()
            if not title or len(title) < 10:
                continue
            
            items.append({
                "title": title,
                "description": f"{location} — {time_ago.strip()}",
                "url": link,
                "published": time_ago.strip(),
                "raw": f"{title}. {location}"
            })
        
        return items
    except Exception as e:
        return []

def fetch_world_monitor(url="https://world-monitor.com/api/signal-markers", config=None, max_items=30):
    """Fetch conflict location data from World Monitor's public API.
    Returns geolocated conflict zones with AI-synthesized summaries and key points."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15",
             "-H", "User-Agent: Mozilla/5.0 (compatible; AEGIS/1.0)",
             url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return []
        
        data = json.loads(result.stdout)
        locations = data.get("locations", [])
        
        # Filter by country if configured
        target_countries = set()
        if config:
            cc = config.get("location", {}).get("country_code", "").upper()
            profile_path = REFERENCES_DIR / "country-profiles" / f"{cc.lower()}.json"
            if profile_path.exists():
                with open(profile_path) as f:
                    profile = json.load(f)
                # Include the country itself + neighboring/relevant countries
                target_countries.add(profile.get("country", ""))
                for n in profile.get("neighbors", []):
                    target_countries.add(n)
                # Also add "global" relevant regions
                for r in profile.get("regions_of_interest", []):
                    target_countries.add(r)
        
        items = []
        for loc in locations[:max_items * 2]:  # Over-fetch for filtering
            country = loc.get("country", "")
            name = loc.get("location_name", "")
            summary = loc.get("summary", "")
            analysis = loc.get("analysis", "")
            key_points = loc.get("key_points", [])
            lat = loc.get("lat", 0)
            lng = loc.get("lng", 0)
            
            # Filter: if we have target countries, only include relevant ones
            if target_countries and country not in target_countries:
                # Check broader region match (Middle East for UAE)
                if not any(tc.lower() in country.lower() for tc in target_countries):
                    continue
            
            # Emit one item PER key_point (not per location) so each event gets its own hash
            if key_points:
                # Only emit key_points from the last 24 hours (recent events)
                for kp in key_points[-10:]:  # Last 10 key_points per location
                    point_text = kp.get("point", "")
                    date_str = kp.get("date", "")
                    if not point_text:
                        continue
                    items.append({
                        "title": f"[{country}] {point_text[:150]}",
                        "description": f"{name} — {point_text}",
                        "url": f"https://world-monitor.com/",
                        "published": date_str,
                        "raw": f"{name} {country}. {date_str}. {point_text}",
                        "metadata": {
                            "lat": lat, "lng": lng,
                            "location": name,
                            "country": country,
                            "key_points_count": len(key_points)
                        }
                    })
            else:
                items.append({
                    "title": f"[{country}] {summary[:150]}",
                    "description": f"{name} — {summary[:300]}",
                    "url": f"https://world-monitor.com/",
                    "published": "",
                    "raw": f"{name} {country}. {summary}. {analysis[:300]}",
                    "metadata": {
                        "lat": lat, "lng": lng,
                        "location": name,
                        "country": country,
                        "key_points_count": 0
                    }
                })
            
            if len(items) >= max_items:
                break
        
        return items
    except Exception as e:
        return []

def fetch_json_api(url_template, config, source):
    """Fetch from JSON API endpoint."""
    try:
        country = config.get("location", {}).get("country", "")
        city = config.get("location", {}).get("city", "")
        lang = config.get("language", "en")
        
        query = f"{city} {country} conflict security"
        api_keys = config.get("api_keys", {})
        key = api_keys.get(source.get("key_name", ""), "")
        
        url = url_template.format(query=query, lang=lang, key=key, country=country, city=city)
        
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15",
             "-H", "User-Agent: AEGIS/1.0",
             url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            return []
        
        data = json.loads(result.stdout)
        items = []
        
        # Handle NewsAPI format
        if "articles" in data:
            for art in data["articles"][:15]:
                items.append({
                    "title": art.get("title", ""),
                    "description": art.get("description", ""),
                    "url": art.get("url", ""),
                    "published": art.get("publishedAt", ""),
                    "source_name": art.get("source", {}).get("name", ""),
                    "raw": f"{art.get('title', '')}. {art.get('description', '')}"
                })
        # Handle GDELT format
        elif "articles" in data:
            for art in data["articles"][:15]:
                items.append({
                    "title": art.get("title", ""),
                    "description": "",
                    "url": art.get("url", ""),
                    "raw": art.get("title", "")
                })
        
        return items
    except Exception:
        return []

def fetch_source(source, config):
    """Fetch items from a source based on its type."""
    src_type = source.get("type", "web")
    url = source.get("url", source.get("url_template", ""))
    ssl_verify = source.get("ssl_verify", True)
    
    if src_type == "rss":
        return fetch_rss(url)
    elif src_type == "web":
        return fetch_web(url, ssl_verify=ssl_verify)
    elif src_type == "liveuamap":
        return fetch_liveuamap(url)
    elif src_type == "world_monitor":
        return fetch_world_monitor(url, config)
    elif src_type == "api":
        return fetch_json_api(url, config, source)
    return []

# ------- Threat Classification -------

def _check_negative_patterns(text, keywords):
    """Check if text matches any negative (disqualifying) patterns for CRITICAL."""
    neg_patterns = keywords.get("critical", {}).get("negative_patterns", [])
    for pattern in neg_patterns:
        try:
            if re.search(pattern, text, re.IGNORECASE):
                return True, pattern
        except re.error:
            continue
    return False, None


def _load_llm_config(config):
    """Load LLM verification settings from AEGIS config.

    Returns dict with keys: enabled, provider, endpoint, model, api_key, timeout.
    Defaults to Ollama at localhost:11434 if no config specified.
    """
    llm = config.get("llm", {})
    enabled = llm.get("enabled", True)  # Default: enabled (fail-open if unavailable)
    provider = llm.get("provider", "ollama")  # ollama | openai | none
    if provider == "none":
        enabled = False

    return {
        "enabled": enabled,
        "provider": provider,
        "endpoint": llm.get("endpoint", "http://localhost:11434"),
        "model": llm.get("model", "qwen3:8b"),
        "api_key": llm.get("api_key", ""),
        "timeout": llm.get("timeout", 30),
    }


def _llm_verify_critical(item, config, timeout=30):
    """Use LLM to verify CRITICAL classification.

    Supports three modes (configured in aegis-config.json under "llm"):
    - ollama: Local Ollama instance (default, zero cost)
    - openai: Any OpenAI-compatible API (OpenRouter, Together, local vLLM, etc.)
    - none/disabled: Skip LLM verification, rely on regex + negative patterns only

    Returns True only if LLM confirms this is an ACTIVE, ONGOING emergency.
    Returns True on LLM failure (fail-open for safety — better a false positive than missing real danger).
    """
    llm_cfg = _load_llm_config(config)
    if not llm_cfg["enabled"]:
        print(f"  [LLM] Disabled — skipping verification (regex-only mode)", file=sys.stderr)
        return True  # No LLM = fail open

    title = item.get("title", "")
    desc = item.get("description", "")[:300]
    source = item.get("source_name", "unknown")
    country = config.get("location", {}).get("country_name", "the affected area")
    timeout = llm_cfg["timeout"]

    user_msg = f"""Is this news item about an ACTIVE, ONGOING military emergency or attack that poses IMMEDIATE physical danger to civilians in {country} RIGHT NOW?

Title: {title}
Description: {desc}
Source: {source}

Rules:
- YES = breaking news about an active attack, missiles, sirens, shelter orders happening NOW in {country}
- NO = past events, analysis, sports cancellations, economics, speculation, events in other countries, opinion pieces

Start your answer with YES or NO."""

    try:
        import subprocess as sp

        if llm_cfg["provider"] == "ollama":
            # Ollama native chat API
            payload = json.dumps({
                "model": llm_cfg["model"],
                "messages": [{"role": "user", "content": f"/no_think\n{user_msg}"}],
                "stream": False,
                "options": {"temperature": 0.0, "num_predict": 500}
            })
            cmd = [
                "curl", "-s", "--max-time", str(timeout),
                f"{llm_cfg['endpoint']}/api/chat",
                "-d", payload
            ]
            result = sp.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                response = data.get("message", {}).get("content", "").strip()
        elif llm_cfg["provider"] == "openai":
            # OpenAI-compatible chat completions API
            payload = json.dumps({
                "model": llm_cfg["model"],
                "messages": [{"role": "user", "content": user_msg}],
                "max_tokens": 50,
                "temperature": 0.0
            })
            headers = ["-H", "Content-Type: application/json"]
            if llm_cfg["api_key"]:
                headers += ["-H", f"Authorization: Bearer {llm_cfg['api_key']}"]
            cmd = [
                "curl", "-s", "--max-time", str(timeout),
                f"{llm_cfg['endpoint']}/v1/chat/completions",
                *headers, "-d", payload
            ]
            result = sp.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                choices = data.get("choices", [])
                response = choices[0]["message"]["content"].strip() if choices else ""
        else:
            print(f"  [LLM] Unknown provider '{llm_cfg['provider']}' — fail-open", file=sys.stderr)
            return True

        # Parse YES/NO response
        if response:
            first_word = response.split()[0].upper().rstrip(".,!:") if response else ""
            if first_word == "NO" or response.upper().startswith("NO"):
                print(f"  [LLM] Rejected CRITICAL: {title[:80]}", file=sys.stderr)
                return False
            if first_word == "YES" or response.upper().startswith("YES"):
                print(f"  [LLM] Confirmed CRITICAL: {title[:80]}", file=sys.stderr)
                return True
            # Ambiguous response — fail open
            print(f"  [LLM] Ambiguous '{response[:50]}' — fail-open: {title[:80]}", file=sys.stderr)
            return True
        else:
            print(f"  [LLM] Empty response — fail-open: {title[:80]}", file=sys.stderr)
            return True
    except Exception as e:
        print(f"  [LLM] Verification failed ({e}) — fail-open: {title[:80]}", file=sys.stderr)
    return True  # Fail open — if LLM is down, let CRITICAL through


def classify_items(items, keywords, config, country_profile):
    """Classify items by threat level using keyword patterns + LLM verification for CRITICAL.

    Pipeline:
    1. Regex pre-filter: match against CRITICAL/HIGH/MEDIUM patterns
    2. Negative pattern filter: disqualify false-positive CRITICAL candidates
    3. LLM verification: CRITICAL candidates verified by local qwen3:8b (zero cost)
    4. Items failing CRITICAL verification get downgraded to HIGH
    """
    local_keywords = []
    if country_profile:
        local_keywords = country_profile.get("threat_keywords_local", [])

    classified = []

    for item in items:
        title = item.get("title", "").lower()
        description = item.get("description", "").lower()

        # Skip homepage/nav-soup items — they have no meaningful title
        if not title or len(title) < 15:
            continue

        # For web-scraped whole-page items (description looks like nav soup),
        # only use the title for threat matching, not full-page body
        is_nav_soup = any(nav in description[:200] for nav in [
            "sign in", "register", "search", "skip to", "main content", "cookie", "subscribe"
        ])

        # Use title + description (but not nav soup as raw)
        raw = f"{title} {description if not is_nav_soup else ''}"

        if not raw.strip() or len(raw.strip()) < 15:
            continue

        level = None
        matched_patterns = []

        # For nav soup items, only title can trigger (stricter)
        scan_text = title if is_nav_soup else raw.lower()

        # Check each severity level
        for severity in ["critical", "high", "medium"]:
            patterns = keywords.get(severity, {}).get("patterns", {})
            for pattern_lang, pattern_list in patterns.items():
                for pattern in pattern_list:
                    try:
                        if re.search(pattern, scan_text, re.IGNORECASE):
                            location_relevant = any(kw.lower() in scan_text for kw in local_keywords)
                            if severity == "medium" or location_relevant:
                                level = severity
                                matched_patterns.append(pattern)
                                break
                    except re.error:
                        continue
                if level:
                    break
            if level:
                break

        if not level:
            continue

        # --- CRITICAL validation pipeline ---
        if level == "critical":
            # Step 1: Check negative patterns (fast regex disqualification)
            is_negative, neg_pattern = _check_negative_patterns(scan_text, keywords)
            if is_negative:
                print(f"  [NEG] Downgraded CRITICAL→HIGH (matched: {neg_pattern[:50]}): {title[:80]}", file=sys.stderr)
                level = "high"
            else:
                # Step 2: Source tier check — non-government single sources need LLM verification
                source_tier = item.get("source_tier", 9)
                if source_tier <= 0:
                    # Government source (Tier 0) — trust directly
                    print(f"  [GOV] CRITICAL from Tier 0 source — trusted: {title[:80]}", file=sys.stderr)
                else:
                    # Step 3: LLM verification for non-government CRITICAL
                    if not _llm_verify_critical(item, config):
                        level = "high"

        item["threat_level"] = level
        item["matched_patterns"] = matched_patterns[:3]
        classified.append(item)

    return classified

# ------- Main Scanner -------

def scan(config, cron_mode=False):
    """Execute a full scan cycle."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    registry = load_source_registry()
    keywords = load_threat_keywords()
    country = config.get("location", {}).get("country", "")
    country_profile = load_country_profile(country)
    
    sources = get_sources_for_location(registry, config)
    seen = load_seen()
    
    scan_time = datetime.now(timezone.utc).isoformat()
    all_items = []
    source_stats = {}
    
    print(f"[AEGIS] Scan started at {scan_time}", file=sys.stderr)
    print(f"[AEGIS] Location: {config.get('location', {}).get('city', '?')}, {country}", file=sys.stderr)
    print(f"[AEGIS] Scanning {len(sources)} sources...", file=sys.stderr)
    
    for source in sources:
        src_id = source.get("id", "unknown")
        try:
            items = fetch_source(source, config)
            new_items = []
            for item in items:
                h = content_hash(item.get("raw", item.get("title", "")))
                if h not in seen:
                    seen[h] = time.time()
                    item["source_id"] = src_id
                    item["source_name"] = source.get("name", src_id)
                    item["source_tier"] = source.get("tier", 9)
                    item["fetched_at"] = scan_time
                    new_items.append(item)
            all_items.extend(new_items)
            source_stats[src_id] = {"fetched": len(items), "new": len(new_items)}
            if new_items:
                print(f"  [{src_id}] {len(new_items)} new items", file=sys.stderr)
        except Exception as e:
            source_stats[src_id] = {"error": str(e)}
            print(f"  [{src_id}] ERROR: {e}", file=sys.stderr)
    
    save_seen(seen)
    
    # Classify threats
    threats = classify_items(all_items, keywords, config, country_profile)
    
    # Separate by level
    critical = [t for t in threats if t.get("threat_level") == "critical"]
    high = [t for t in threats if t.get("threat_level") == "high"]
    medium = [t for t in threats if t.get("threat_level") == "medium"]
    
    result = {
        "scan_time": scan_time,
        "location": config.get("location", {}),
        "sources_scanned": len(sources),
        "total_items": len(all_items),
        "threats": {
            "critical": critical,
            "high": high,
            "medium": medium
        },
        "threat_counts": {
            "critical": len(critical),
            "high": len(high),
            "medium": len(medium)
        },
        "source_stats": source_stats
    }
    
    # Save scan log
    try:
        log_entries = []
        if SCAN_LOG.exists():
            log_entries = json.loads(SCAN_LOG.read_text())
        log_entries.append({
            "time": scan_time,
            "threats": result["threat_counts"],
            "sources": len(sources),
            "items": len(all_items)
        })
        # Keep last 200 entries
        SCAN_LOG.write_text(json.dumps(log_entries[-200:], indent=2))
    except:
        pass
    
    if cron_mode:
        # Output structured result for OpenClaw agent to process
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"AEGIS SCAN COMPLETE — {scan_time}", file=sys.stderr)
        print(f"Sources: {len(sources)} | Items: {len(all_items)} | Threats: {len(threats)}", file=sys.stderr)
        print(f"  🔴 CRITICAL: {len(critical)}", file=sys.stderr)
        print(f"  🟠 HIGH: {len(high)}", file=sys.stderr)
        print(f"  ℹ️  MEDIUM: {len(medium)}", file=sys.stderr)
        
        for t in critical:
            print(f"\n🔴 CRITICAL: {t.get('title', 'Unknown')}", file=sys.stderr)
            print(f"   Source: {t.get('source_name')} (Tier {t.get('source_tier')})", file=sys.stderr)
            print(f"   URL: {t.get('url', 'N/A')}", file=sys.stderr)
        
        for t in high:
            print(f"\n🟠 HIGH: {t.get('title', 'Unknown')}", file=sys.stderr)
            print(f"   Source: {t.get('source_name')} (Tier {t.get('source_tier')})", file=sys.stderr)
        
        print(f"{'='*60}", file=sys.stderr)
        
        # Still output JSON for piping
        print(json.dumps(result, indent=2))
    
    return result

def list_sources(config):
    """List all active sources for user's location."""
    registry = load_source_registry()
    sources = get_sources_for_location(registry, config)
    print(f"\nAEGIS Sources for {config.get('location', {}).get('city', '?')}, {config.get('location', {}).get('country', '?')}:\n")
    for s in sources:
        tier_emoji = {0: "🏛️", 1: "📰", 2: "✈️", 3: "🔍", 4: "🔑"}.get(s.get("tier", 9), "❓")
        print(f"  {tier_emoji} [{s['id']}] {s['name']} (Tier {s.get('tier', '?')})")
        print(f"     {s.get('url', s.get('url_template', 'N/A'))}")
    print(f"\nTotal: {len(sources)} sources active")

# ------- CLI -------

def main():
    parser = argparse.ArgumentParser(description="AEGIS Scanner — Emergency Intelligence System")
    parser.add_argument("--cron", action="store_true", help="Cron mode (JSON output only)")
    parser.add_argument("--config", type=str, help="Path to aegis-config.json")
    parser.add_argument("--sources", action="store_true", help="List active sources")
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.sources:
        list_sources(config)
        return
    
    scan(config, cron_mode=args.cron)

if __name__ == "__main__":
    main()

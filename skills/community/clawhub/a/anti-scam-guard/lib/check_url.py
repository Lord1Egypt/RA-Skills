#!/usr/bin/env python3
"""Phishguard URL checker - checks URLs against blocklist shards and heuristic rules."""

import json
import os
import re
import sys
import time
import unicodedata
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
SHARDS_DIR = os.path.join(SKILL_DIR, "data", "blocklist-shards")

# GitHub raw URL for latest blocklist shards
GITHUB_SHARDS_BASE = "https://raw.githubusercontent.com/phishguard-niki/blocklist-data/main"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "phishguard")
CACHE_MAX_AGE = 3600  # 1 hour

# Known safe domains (whitelist)
WHITELIST = {
    "google.com", "google.com.tw", "youtube.com", "facebook.com", "instagram.com",
    "twitter.com", "x.com", "linkedin.com", "github.com", "apple.com",
    "microsoft.com", "amazon.com", "netflix.com", "yahoo.com", "wikipedia.org",
    "reddit.com", "line.me", "telegram.org", "whatsapp.com",
    "crypto.com", "coinbase.com", "binance.com", "kraken.com",
    "blockchain.com", "ledger.com", "trezor.io", "trust.com",
    "shopee.tw", "pchome.com.tw", "paypal.com", "bing.com",
    "gov.tw", "edu.tw", "com.tw", "org.tw",
    "npa.gov.tw", "moda.gov.tw", "ey.gov.tw",
    # Taiwan financial / brokerage / news sites (often false-positive flagged)
    "moneydj.com", "cnyes.com", "tw.stock.yahoo.com", "histock.tw",
    "wantgoo.com", "moneylink.com.tw", "sinotrade.com.tw",
    "esunsec.com.tw", "fubon.com", "yuanta.com.tw", "cathaysec.com.tw",
    "ctbcsec.com", "kgieworld.com", "capital.com.tw",
}

# Homograph attack detection - Cyrillic confusables
CONFUSABLE_CHARS = {
    '\u0430': 'a', '\u0435': 'e', '\u043e': 'o', '\u0440': 'p',
    '\u0441': 'c', '\u0443': 'y', '\u0445': 'x', '\u0456': 'i',
    '\u0501': 'd', '\u051b': 'q', '\u051d': 'w',
    '\u0261': 'g', '\u014b': 'n', '\u0196': 'I',
    '\u0d20': 'o', '\u0d21': 'o',
}

# Digit-letter homograph map (e.g., paypa1.com, g00gle.com)
DIGIT_HOMOGRAPH_MAP = {'0': 'o', '1': 'l', '3': 'e', '@': 'a', '$': 's'}
FAMOUS_BRANDS = ['paypal', 'apple', 'google', 'microsoft', 'binance', 'metamask', 'bankofamerica']

SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "secure", "account", "update", "confirm",
    "banking", "wallet", "crypto", "invest", "bonus", "reward", "prize",
    "lucky", "winner", "free", "gift", "claim",
]

RISKY_TLDS = {
    ".xyz", ".top", ".club", ".buzz", ".tk", ".ml", ".ga", ".cf", ".gq",
    ".pw", ".cc", ".icu", ".cam", ".bid", ".win", ".loan", ".racing",
    ".date", ".review", ".stream", ".click", ".link", ".surf",
    ".pages.dev", ".workers.dev", ".web.app", ".firebaseapp.com",
    ".netlify.app", ".vercel.app", ".herokuapp.com", ".weebly.com",
    ".wixsite.com", ".blogspot.com",
}


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        parsed = urlparse(url)
        return parsed.hostname.lower() if parsed.hostname else ""
    except Exception:
        return ""


def get_root_domain(domain: str) -> str:
    """Get root domain (e.g., sub.example.com -> example.com)."""
    parts = domain.split(".")
    if len(parts) >= 2:
        # Handle .com.tw, .gov.tw, .edu.tw etc.
        if len(parts) >= 3 and parts[-2] in ("com", "gov", "edu", "org", "net", "co"):
            return ".".join(parts[-3:])
        return ".".join(parts[-2:])
    return domain


def is_whitelisted(domain: str) -> bool:
    """Check if domain is in whitelist."""
    root = get_root_domain(domain)
    for w in WHITELIST:
        if domain == w or domain.endswith("." + w) or root == w:
            return True
    return False


def _fetch_shard_from_github(shard_file: str):
    """Try to fetch a shard from GitHub, with local caching."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, shard_file)

    # Use cache if fresh enough
    if os.path.isfile(cache_path):
        age = time.time() - os.path.getmtime(cache_path)
        if age < CACHE_MAX_AGE:
            try:
                with open(cache_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass

    # Fetch from GitHub
    url = f"{GITHUB_SHARDS_BASE}/{shard_file}"
    try:
        req = Request(url, headers={"User-Agent": "PhishGuard/0.4.4"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Cache it
            with open(cache_path, "w") as f:
                json.dump(data, f)
            return data
    except Exception:
        # Fall back to stale cache if available
        if os.path.isfile(cache_path):
            try:
                with open(cache_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return None


def check_blocklist(domain: str):
    """Check domain against blocklist shards (GitHub first, local fallback)."""
    first_char = domain[0].lower() if domain else ""
    if first_char.isalpha():
        shard_file = f"shard-{first_char}.json"
    else:
        shard_file = "shard-other.json"

    # Try GitHub (with cache) first
    data = _fetch_shard_from_github(shard_file)

    # Fallback to local bundled shards
    if data is None and os.path.isdir(SHARDS_DIR):
        shard_path = os.path.join(SHARDS_DIR, shard_file)
        if os.path.isfile(shard_path):
            try:
                with open(shard_path, "r") as f:
                    data = json.load(f)
            except Exception:
                pass

    if data is None:
        return None

    domains = set(data.get("domains", []))

    # Check exact match
    if domain in domains:
        return {"matched": True, "source": "黑名單", "domain": domain}

    # Check root domain
    root = get_root_domain(domain)
    if root != domain and root in domains:
        return {"matched": True, "source": "黑名單", "domain": root}

    return None


def check_heuristics(domain: str, url: str) -> list:
    """Check URL for suspicious heuristic patterns."""
    reasons = []

    # 1. Cyrillic homograph attack
    for char in domain:
        if char in CONFUSABLE_CHARS:
            reasons.append(f"同形字攻擊：包含偽造字元 '{char}' (偽裝成 '{CONFUSABLE_CHARS[char]}')")
            break

    # 2. Digit-letter homograph attack (e.g., paypa1.com, g00gle.com)
    normalized = ''.join(DIGIT_HOMOGRAPH_MAP.get(c, c) for c in domain.lower())
    for brand in FAMOUS_BRANDS:
        if brand in normalized and brand not in domain.lower():
            reasons.append(f"數字偽裝攻擊：疑似仿冒 {brand}（使用數字替代字母）")
            break

    # 3. Non-ASCII characters
    try:
        domain.encode("ascii")
    except UnicodeEncodeError:
        if not any(c in CONFUSABLE_CHARS for c in domain):
            reasons.append("網域包含非 ASCII 字元")

    # 4. Deep subdomain (4+ levels)
    parts = domain.split(".")
    if len(parts) >= 5:
        reasons.append(f"深層子網域（{len(parts)} 層），常見於釣魚網站")

    # 5. Suspicious keywords in domain
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in domain:
            reasons.append(f"網域包含可疑關鍵字：'{kw}'")
            break

    # 6. Brand impersonation
    brands = {"paypal", "apple", "google", "microsoft", "amazon", "netflix",
              "facebook", "instagram", "line", "whatsapp", "telegram"}
    root = get_root_domain(domain)
    for brand in brands:
        if brand in domain and brand not in root:
            reasons.append(f"疑似仿冒 {brand.capitalize()} 品牌")
            break

    # 7. Risky TLD
    for tld in RISKY_TLDS:
        if domain.endswith(tld):
            reasons.append(f"使用高風險網域後綴：{tld}")
            break

    # 8. IP address as domain
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
        reasons.append("使用 IP 位址而非網域名稱")

    # 9. Very long domain
    if len(domain) > 50:
        reasons.append(f"網域名稱異常長（{len(domain)} 字元）")

    return reasons


def check_url(url: str) -> dict:
    """Main check function - returns risk assessment."""
    domain = extract_domain(url)
    if not domain:
        return {
            "url": url,
            "domain": "",
            "risk_level": "unknown",
            "risk_level_zh": "無法解析",
            "message": "無法解析此網址",
        }

    # Whitelist check
    if is_whitelisted(domain):
        return {
            "url": url,
            "domain": domain,
            "risk_level": "low",
            "risk_level_zh": "安全",
            "matched_source": None,
            "reasons": [],
            "message": f"{domain} 未發現已知風險。",
        }

    # Blocklist check
    blocklist_result = check_blocklist(domain)
    if blocklist_result:
        return {
            "url": url,
            "domain": domain,
            "risk_level": "critical",
            "risk_level_zh": "極高風險",
            "matched_source": blocklist_result["source"],
            "reasons": ["已被列入詐騙/釣魚黑名單"],
            "message": f"{domain} 是已知的詐騙/釣魚網站！",
        }

    # Heuristic check
    reasons = check_heuristics(domain, url)
    if len(reasons) >= 2:
        return {
            "url": url,
            "domain": domain,
            "risk_level": "high",
            "risk_level_zh": "高風險",
            "matched_source": "啟發式偵測",
            "reasons": reasons,
            "message": f"{domain} 具有多項可疑特徵。",
        }
    elif len(reasons) == 1:
        return {
            "url": url,
            "domain": domain,
            "risk_level": "medium",
            "risk_level_zh": "中風險",
            "matched_source": "啟發式偵測",
            "reasons": reasons,
            "message": f"{domain} 有可疑特徵。",
        }

    # No match
    return {
        "url": url,
        "domain": domain,
        "risk_level": "low",
        "risk_level_zh": "未發現風險",
        "matched_source": None,
        "reasons": [],
        "message": f"{domain} 未發現已知風險。",
    }


def extract_urls(text: str) -> list:
    """Extract all URLs from text."""
    url_pattern = re.compile(
        r'https?://[^\s<>\"\'\)\]]+|'
        r'(?<!\w)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|tw|io|xyz|top|cc|club|dev|app|me|info|biz|co|uk|jp|cn|kr|hk|sg)[^\s<>\"\'\)\]]*'
    )
    return url_pattern.findall(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: check_url.py <url_or_text>"}, ensure_ascii=False))
        sys.exit(1)

    input_text = " ".join(sys.argv[1:])
    urls = extract_urls(input_text)

    if not urls:
        # Treat the whole input as a domain/URL
        urls = [input_text.strip()]

    results = []
    for url in urls:
        result = check_url(url)
        results.append(result)

    if len(results) == 1:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"results": results, "total": len(results)}, ensure_ascii=False, indent=2))

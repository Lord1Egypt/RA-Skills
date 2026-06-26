#!/usr/bin/env python3
"""
从公司域名提取邮箱地址
支持多种方式：官网爬取、WHOIS查询
支持代理设置
"""

import argparse
import json
import os
import re
import sys
import time
import random
import warnings
from urllib.parse import urljoin, urlparse

warnings.filterwarnings('ignore')

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Please install: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False
    print("python-whois not installed, WHOIS lookup disabled", file=sys.stderr)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

PROXIES = None

def init_proxies():
    global PROXIES
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    all_proxy = os.environ.get('ALL_PROXY') or os.environ.get('all_proxy')
    
    if https_proxy:
        PROXIES = {'http': https_proxy, 'https': https_proxy}
    elif http_proxy:
        PROXIES = {'http': http_proxy, 'https': http_proxy}
    elif all_proxy:
        PROXIES = {'http': all_proxy, 'https': all_proxy}
    
    return PROXIES

EXCLUDE_EMAIL_PATTERNS = [
    'example.com', 'test.com', 'sample.com', 'domain.com', 'email.com',
    'yourcompany.com', 'yourdomain.com', 'company.com', 'user@',
    'sentry.io', 'wixpress.com', 'wordpress.com', 'github.com',
    'noreply@', 'no-reply@', 'donotreply@',
    '.png', '.jpg', '.gif', '.svg', '.webp',
]

COMMON_PAGES = [
    '/',
    '/contact',
    '/contact-us',
    '/about',
    '/about-us',
    '/team',
    '/connect',
    '/reach-us',
]


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }


def is_valid_email(email, domain=None):
    if not email or '@' not in email:
        return False
    
    email = email.lower().strip()
    
    for pattern in EXCLUDE_EMAIL_PATTERNS:
        if pattern in email:
            return False
    
    if email.startswith('<'):
        email = email[1:]
    if email.endswith('>'):
        email = email[:-1]
    if email.endswith('.'):
        email = email[:-1]
    
    local, email_domain = email.split('@')
    
    if len(local) < 2:
        return False
    
    if domain and domain in email_domain:
        return True
    
    common_providers = ['gmail', 'yahoo', 'hotmail', 'outlook', 'qq', '163', '126', 'sina', 'foxmail']
    if any(p in email_domain for p in common_providers):
        return False
    
    return True


def extract_emails_from_page(url, domain):
    emails = set()
    
    try:
        response = requests.get(
            url,
            headers=get_random_headers(),
            timeout=10,
            verify=False,
            allow_redirects=True,
            proxies=PROXIES
        )
        
        if response.status_code != 200:
            return emails
        
        text = response.text
        
        found = EMAIL_PATTERN.findall(text)
        
        for email in found:
            email = email.lower().strip()
            if is_valid_email(email, domain):
                emails.add(email)
        
        soup = BeautifulSoup(text, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:'):
                email = href[7:].split('?')[0]
                if is_valid_email(email, domain):
                    emails.add(email.lower())
        
        for elem in soup.find_all(['a', 'span', 'p', 'div', 'li']):
            text = elem.get_text()
            found = EMAIL_PATTERN.findall(text)
            for email in found:
                if is_valid_email(email, domain):
                    emails.add(email.lower())
        
    except Exception as e:
        pass
    
    return emails


def extract_from_website(domain):
    emails = set()
    
    if not domain.startswith('http'):
        domain = f"https://{domain}"
    
    parsed = urlparse(domain)
    base_domain = parsed.netloc.replace('www.', '')
    
    for page in COMMON_PAGES:
        url = f"{domain.rstrip('/')}{page}"
        found = extract_emails_from_page(url, base_domain)
        emails.update(found)
        time.sleep(random.uniform(0.3, 0.8))
    
    return emails


def extract_from_whois(domain):
    emails = set()
    
    if not HAS_WHOIS:
        return emails
    
    try:
        clean_domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        clean_domain = clean_domain.replace('www.', '')
        
        w = whois.whois(clean_domain)
        
        if w.emails:
            email_list = w.emails if isinstance(w.emails, list) else [w.emails]
            for email in email_list:
                email = str(email).lower().strip()
                if '@' in email and is_valid_email(email, clean_domain):
                    emails.add(email)
                    
    except Exception as e:
        pass
    
    return emails


def prioritize_emails(emails, domain):
    if not emails:
        return []
    
    email_list = list(emails)
    
    priority_prefixes = [
        ('sales', 100),
        ('contact', 90),
        ('info', 80),
        ('business', 70),
        ('support', 60),
        ('hello', 50),
        ('team', 40),
    ]
    
    def get_score(email):
        local = email.split('@')[0].lower()
        
        for prefix, score in priority_prefixes:
            if local.startswith(prefix) or local == prefix:
                return score
        
        if domain and domain in email:
            return 30
        
        return 0
    
    email_list.sort(key=get_score, reverse=True)
    
    return email_list


def extract_emails(domain, use_whois=True):
    init_proxies()
    all_emails = set()
    
    print(f"Extracting emails from {domain}...", file=sys.stderr)
    
    website_emails = extract_from_website(domain)
    all_emails.update(website_emails)
    print(f"  Website: found {len(website_emails)} emails", file=sys.stderr)
    
    if use_whois and HAS_WHOIS:
        whois_emails = extract_from_whois(domain)
        all_emails.update(whois_emails)
        print(f"  WHOIS: found {len(whois_emails)} emails", file=sys.stderr)
    
    clean_domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
    clean_domain = clean_domain.replace('www.', '')
    
    prioritized = prioritize_emails(all_emails, clean_domain)
    
    return prioritized


def main():
    parser = argparse.ArgumentParser(description='Extract email addresses from a domain')
    parser.add_argument('domain', help='Domain name (e.g., example.com)')
    parser.add_argument('--no-whois', action='store_true', help='Skip WHOIS lookup')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    parser.add_argument('--proxy', '-p', help='Proxy URL (e.g., http://127.0.0.1:7890)')
    
    args = parser.parse_args()
    
    if args.proxy:
        os.environ['HTTPS_PROXY'] = args.proxy
        os.environ['HTTP_PROXY'] = args.proxy
    
    emails = extract_emails(args.domain, use_whois=not args.no_whois)
    
    result = {
        'domain': args.domain,
        'emails': emails,
        'count': len(emails)
    }
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

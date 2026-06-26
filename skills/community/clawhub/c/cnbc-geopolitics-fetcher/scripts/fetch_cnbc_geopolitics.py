#!/usr/bin/env python3
"""
CNBC Geopolitics Fetcher - COMPLETE UPDATED VERSION
Format: No '### Article' header, keep title and all other fields

FEATURES:
- Scrapes latest CNBC geopolitical articles
- Extracts COMPLETE sentences - NO truncation
- Posts ONE BY ONE to Discord (1-by-1, not batched)
- Tracks sent URLs to avoid duplicates
- NEW FORMAT: No '### Article' header at top

USAGE:
  python fetch_cnbc_geopolitics.py --webhook "DISCORD_WEBHOOK_URL" --verbose
"""

import argparse
import json
import os
import re
import sys
from html import unescape
from bs4 import BeautifulSoup

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--webhook', type=str)
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--config', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()


def load_webhook_from_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            match = re.search(r'https://discord\.com/api/webhooks/\S+', f.read())
            return match.group(0) if match else None
    except FileNotFoundError:
        return None


def http_get(url, headers=None):
    headers = headers or {'User-Agent': 'Mozilla/5.0'}
    if HAS_REQUESTS:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    else:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8')


def http_post_json(url, data):
    json_data = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if HAS_REQUESTS:
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        if resp.status_code >= 400:
            raise Exception(f"Discord error {resp.status_code}")
        if resp.status_code == 204:
            return {'status': 'ok'}
        try:
            return resp.json()
        except json.JSONDecodeError:
            return {'status': 'ok'}
    else:
        req = urllib.request.Request(url, data=json_data, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8')
            return json.loads(body) if body else {'status': 'ok'}


def extract_articles_from_html(html):
    articles = []
    pattern = r'href="(https://www\.cnbc\.com/(\d{4})/[^"]+)"'
    matches = re.findall(pattern, html, re.IGNORECASE)
    
    for m in matches:
        url = m[0]
        if any(x in url.lower() for x in ['/video/', '/premium/', '/pro/', 'tag/', 'section/', 'live']):
            continue
        articles.append({'url': url, 'title': 'pending', 'year': m[1]})
    
    seen = set()
    unique = []
    for a in articles:
        if a['url'] not in seen:
            seen.add(a['url'])
            unique.append(a)
    
    return unique[:25]


def fetch_article_details(url):
    try:
        html = http_get(url)
        return extract_true_complete_facts(html, url)
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def extract_true_complete_facts(html, url):
    """Extract TRUE complete facts - NO TRUNCATION."""
    metadata = {'url': url, 'title': '', 'market_impact': '', 'hard_facts': [], 'summary': ''}
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        return extract_facts_regex(html, url)
    
    # Title
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        metadata['title'] = clean_title(unescape(og_title['content']))
    
    # Article body
    article_body = soup.find('div', class_='ArticleBody-wrapper') or soup.find('div', class_='article-body') or soup.find('article')
    
    if not article_body:
        paragraphs = soup.find_all('p')
        full_text = ' '.join(p.get_text() for p in paragraphs[:25])
    else:
        full_text = article_body.get_text(separator=' ', strip=True)
    
    # Description
    og_desc = soup.find('meta', property='og:description')
    description = unescape(og_desc['content']) if og_desc and og_desc.get('content') else ''
    
    # Extract TRUE complete facts
    metadata['hard_facts'] = extract_true_complete_facts_from_text(full_text, description)
    metadata['market_impact'] = extract_market_impact(full_text)
    metadata['summary'] = generate_summary(full_text, description)
    
    if not metadata['title']:
        metadata['title'] = url.split('/')[-1].replace('-', ' ').title()
    
    return metadata


def extract_true_complete_facts_from_text(text, description=''):
    """Extract TRUE complete facts - ABSOLUTELY NO TRUNCATION."""
    facts = []
    combined = (description + ' ' + text) if description else text
    
    # Normalize whitespace
    combined = re.sub(r'\s+', ' ', combined)
    
    # Split into sentences properly
    sentences = re.split(r'(?<=[.!?])\s+', combined)
    
    # Track which sentences we've used to avoid duplicates
    used_sents = set()
    
    # 1. Find quoted statements (complete sentence with quote) - NO upper length limit
    for sent in sentences:
        if '"' in sent and len(sent) > 40:
            if any(x in sent.lower() for x in ['said', 'says', 'stated', 'announced', 'told', 'warned']):
                if sent not in used_sents:
                    facts.append(f"Official: {sent}")
                    used_sents.add(sent)
                    break
    
    # 2. Find action sentences (military, diplomatic, economic) - NO upper length limit
    action_words = ['fired', 'launched', 'deployed', 'sanctions', 'troops', 'missile', 
                    'summit', 'talks', 'strike', 'attack', 'agreement', 'deal', 'obliterated',
                    'target', 'military', 'defense', 'war', 'conflict']
    
    for sent in sentences:
        sent_lower = sent.lower()
        if any(word in sent_lower for word in action_words):
            if len(sent) > 30 and sent not in used_sents:
                facts.append(f"Action: {sent}")
                used_sents.add(sent)
                break
    
    # 3. Find data/numbers sentences - NO upper length limit
    for sent in sentences:
        # Look for sentences with numbers + units
        if re.search(r'\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|percent|%|thousand|barrel|\$)', sent, re.IGNORECASE):
            if len(sent) > 30 and sent not in used_sents:
                facts.append(f"Data: {sent}")
                used_sents.add(sent)
                break
    
    # 4. Find timeline sentences - NO upper length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['by ', 'before ', 'after ', 'until ', 'deadline', 'within ', 'expected']):
            if len(sent) > 30 and sent not in used_sents:
                facts.append(f"Timeline: {sent}")
                used_sents.add(sent)
                break
    
    # 5. Find analyst/forecast sentences (for Polymarket relevance) - NO upper length limit
    analyst_words = ['analyst', 'forecast', 'predict', 'expect', 'project', 'estimate', 
                     'consensus', 'outlook', 'guidance', 'probability', 'odds',
                     'likely', 'unlikely', 'scenario', 'risk', 'recession', 'stagflation']
    for sent in sentences:
        sent_lower = sent.lower()
        if any(word in sent_lower for word in analyst_words):
            if len(sent) > 30 and sent not in used_sents:
                facts.append(f"Analyst: {sent}")
                used_sents.add(sent)
                break
    
    # 6. Find Polymarket/prediction market relevant sentences - NO upper length limit
    polymarket_words = ['polymarket', 'prediction market', 'betting', 'wager', 'odds', 
                        'probability', 'chance', 'likelihood', 'market implies', 'pricing in']
    for sent in sentences:
        sent_lower = sent.lower()
        if any(word in sent_lower for word in polymarket_words):
            if len(sent) > 30 and sent not in used_sents:
                facts.append(f"Market: {sent}")
                used_sents.add(sent)
                break
    
    # 7. If still need facts, take first meaningful sentences from description
    while len(facts) < 5:
        if description:
            desc_sents = re.split(r'(?<=[.!?])\s+', description)
            for sent in desc_sents:
                if len(sent) > 40 and sent not in used_sents:
                    if not any(x in sent.lower() for x in ['copyright', 'terms', 'privacy']):
                        facts.append(f"Context: {sent}")
                        used_sents.add(sent)
                        break
        else:
            for sent in sentences[:5]:
                if len(sent) > 40 and sent not in used_sents:
                    if not any(x in sent.lower() for x in ['copyright', 'subscribe', 'cookie']):
                        facts.append(f"Info: {sent}")
                        used_sents.add(sent)
                        break
        break
    
    return facts[:5]


def extract_facts_regex(html, url):
    """Fallback without BeautifulSoup."""
    metadata = {'url': url, 'title': '', 'market_impact': '', 'hard_facts': [], 'summary': ''}
    
    title_match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html, re.IGNORECASE)
    if title_match:
        metadata['title'] = clean_title(unescape(title_match.group(1)))
    
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    metadata['hard_facts'] = extract_true_complete_facts_from_text(text)
    metadata['market_impact'] = extract_market_impact(text)
    
    return metadata


def extract_market_impact(text):
    """Extract complete market impact - full sentences with analyst context. NO TRUNCATION."""
    impacts = []
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Find oil/energy sentences - NO length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['oil', 'crude', 'WTI', 'Brent', 'barrel', 'energy']):
            if len(sent) > 20:  # Only minimum length check
                impacts.append(f"Energy: {sent}")
                break
    
    # Find stock sentences - NO length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['S&P', 'NASDAQ', 'Dow', 'Stoxx', 'stock', 'market']):
            if len(sent) > 20:
                impacts.append(f"Stocks: {sent}")
                break
    
    # Find currency sentences - NO length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['dollar', 'EUR', 'USD', 'currency', 'exchange']):
            if len(sent) > 20:
                impacts.append(f"Currency: {sent}")
                break
    
    # Find analyst/economic forecast sentences - NO length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['analyst', 'economist', 'forecast', 'gdp', 'inflation', 'fed', 'interest rate', 'recession']):
            if len(sent) > 20:
                impacts.append(f"Analyst: {sent}")
                break
    
    # Find Polymarket/prediction market sentences - NO length limit
    for sent in sentences:
        if any(x in sent.lower() for x in ['polymarket', 'prediction', 'odds', 'probability', 'betting', 'market pricing']):
            if len(sent) > 20:
                impacts.append(f"Polymarket: {sent}")
                break
    
    return '; '.join(impacts[:5]) if impacts else 'Market impact detailed in article'


def generate_summary(text, description=''):
    combined = (description + ' ' + text) if description else text
    sentences = re.split(r'(?<=[.!?])\s+', combined)
    
    summary_sents = []
    for sent in sentences[:5]:
        sent = sent.strip()
        if 40 < len(sent) < 250:
            if not any(x in sent.lower() for x in ['copyright', 'terms', 'privacy', 'cookie', 'subscribe']):
                summary_sents.append(sent)
                if len(summary_sents) >= 2:
                    break
    
    return '. '.join(summary_sents) + '.' if summary_sents else ''


def clean_title(title):
    editorial = ['stunning', 'grim', 'worrisome', 'shocking', 'breaking', 'major', 'huge', 'massive', 'critical', 'urgent', 'dramatic', 'surprising']
    for word in editorial:
        title = re.sub(rf'\b{word}\b', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'&x27;', "'", title)
    title = re.sub(r'&quot;', '"', title)
    title = re.sub(r'&amp;', '&', title)
    return title


def format_single_article(article):
    """Format a SINGLE article for Discord posting (one at a time) - NO TRUNCATION.
    NEW FORMAT: No '### Article' header at the top."""
    if not article.get('title'):
        return None
    
    # Title: use full title (Discord handles long titles)
    title = article['title']
    
    # Market: use complete market impact string
    market = article.get('market_impact', 'See article')
    
    # Facts: use complete sentences as-is (NO truncation)
    facts = article.get('hard_facts', ['No facts extracted'])[:5]
    facts_text = ''
    for f in facts:
        # No truncation - use complete sentence as extracted
        facts_text += f"  - {f}\n"
    
    # NEW FORMAT: Remove '### Article' and keep everything else
    entry = f"**{title}**\n\n**URL:** {article['url']}\n\n**Market Impact:** {market}\n\n**Hard Facts:**\n{facts_text.strip()}\n\n*(Raw data - no editorial analysis)*"
    
    return entry


def post_single_article(article, num, webhook_url):
    """Post ONE article as a single Discord message - split if exceeds 2000 chars."""
    content = format_single_article(article)
    if not content:
        return False
    
    # Discord limit: 2000 characters per message
    DISCORD_LIMIT = 2000
    
    try:
        if len(content) <= DISCORD_LIMIT:
            # Send as single message
            payload = {'content': content, 'username': 'CNBC Geopolitics'}
            http_post_json(webhook_url, payload)
            print(f"[POSTED] Article {num}: {article['title'][:60]}...", file=sys.stderr)
            return True
        else:
            # Split into parts: Title+URL+Market first, then Facts+disclaimer
            title = article['title']
            url = article['url']
            market = article.get('market_impact', 'See article')
            facts = article.get('hard_facts', ['No facts extracted'])[:5]
            
            part1 = f"\"\"\"**{title}**"
            
            parts.append(part1)
            
            # Part 2: Hard Facts + Disclaimer
            facts_text = f"**Hard Facts:**\n  - "
            for f in facts:
                facts_text += f"{f}\n"
            parts.append(facts_text)
            parts.append("*(Raw data - no editorial analysis)*")
            
            # Send each part separately
            for i, part in enumerate(parts):
                if len(part) <= DISCORD_LIMIT:
                    payload = {'content': part, 'username': 'CNBC Geopolitics'}
                    http_post_json(webhook_url, payload)
                    import time
                    time.sleep(0.3)  # Small delay between parts
            
            print(f"[POSTED] Article {num} (split): {article['title'][:60]}...", file=sys.stderr)
            return True
    except Exception as e:
        print(f"Error posting article {num}: {e}", file=sys.stderr)
        return False


def load_sent_urls(history_path):
    """Load previously sent URLs from history file."""
    try:
        with open(history_path, 'r', encoding='utf-8') as f:
            urls = set()
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.add(line)
            return urls
    except FileNotFoundError:
        return set()


def save_sent_url(history_path, url):
    """Append a new URL to the history file."""
    try:
        with open(history_path, 'a', encoding='utf-8') as f:
            f.write(f'{url}\n')
        return True
    except Exception as e:
        print(f'Error saving URL to history: {e}', file=sys.stderr)
        return False


def main():
    args = parse_args()
    
    webhook_url = args.webhook or load_webhook_from_config(args.config)
    if not webhook_url:
        print('Error: No webhook URL', file=sys.stderr)
        sys.exit(1)
    
    # Determine history file path (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    history_path = os.path.join(script_dir, '..', 'references', 'sent_urls.txt')
    
    # Load previously sent URLs
    sent_urls = load_sent_urls(history_path)
    print(f'Loaded {len(sent_urls)} previously sent URLs from history', file=sys.stderr)
    
    print('Fetching CNBC geopolitical news...', file=sys.stderr)
    
    sections = [
        'https://www.cnbc.com/world/',
        'https://www.cnbc.com/',
        'https://www.cnbc.com/finance/',
    ]
    
    all_candidates = []
    for section in sections:
        try:
            html = http_get(section)
            candidates = extract_articles_from_html(html)
            all_candidates.extend(candidates)
        except Exception as e:
            print(f'Section error: {e}', file=sys.stderr)
    
    geo_keywords = ['iran', 'china', 'russia', 'north korea', 'ukraine', 'israel', 
                    'middle east', 'tariff', 'sanctions', 'defense', 'military',
                    'foreign policy', 'trade', 'oil', 'energy', 'nato', 'putin', 'trump']
    
    geo_articles = []
    for c in all_candidates:
        title_lower = c.get('title', '').lower()
        url_lower = c.get('url', '').lower()
        if any(kw in title_lower or kw in url_lower for kw in geo_keywords):
            geo_articles.append(c)
    
    print(f'Found {len(geo_articles)} geopolitical articles', file=sys.stderr)
    
    articles = []
    skipped_count = 0
    for candidate in geo_articles[:15]:
        if len(articles) >= args.count:
            break
        
        # Skip if URL already sent before
        if candidate['url'] in sent_urls:
            if args.verbose:
                print(f'SKIP (already sent): {candidate["url"]}', file=sys.stderr)
            skipped_count += 1
            continue
        
        details = fetch_article_details(candidate['url'])
        if details and details.get('title'):
            articles.append(details)
            if args.verbose:
                print(f'Extracted: {details["title"][:60]}', file=sys.stderr)
    
    # Print briefing (unchanged - for reference)
    briefing = format_briefing(articles)
    print('\n' + briefing, file=sys.stdout)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(briefing)
    
    # Post articles ONE BY ONE (not batched)
    posted_count = 0
    for i, article in enumerate(articles[:5], 1):
        success = post_single_article(article, i, webhook_url)
        if success:
            # Save URL to history after successful post
            save_sent_url(history_path, article['url'])
            posted_count += 1
        # Small delay between posts to avoid rate limiting
        import time
        time.sleep(0.5)
    
    if posted_count > 0:
        print(f'Discord: Posted {posted_count} new article(s)', file=sys.stderr)
    else:
        print('No new articles to post (all already sent before)', file=sys.stderr)
        # Notify via stdout that no new content was found
        print('NOTIFY_CHAT: No new CNBC articles found - all URLs already in history', file=sys.stdout)
    
    return 0 if posted_count > 0 else 1


def format_briefing(articles):
    """Format briefing - combine all articles into single message (for reference)."""
    if not articles:
        return 'No articles found'
    
    output = []
    for i, article in enumerate(articles[:5], 1):
        output.append(f"---\n### Article {i}\n")
        output.append(f"**{article['title'][:100]}**\n\n")
        url = article.get('url', 'N/A')
        market = article.get('market_impact', 'See article')[:200] if article.get('market_impact') else 'Market impact in article'
        facts = (article.get('hard_facts', []) or ['N/A'])[:3]
        output.append(f"URL: {url}\n")
        output.append(f"Market: {market}\n")
        facts_text = '\n'.join([f"  - {f}" for f in facts])
        output.append(f"Facts:\n{facts_text}")
        output.append("---\n")
    
    return '\n'.join(output) if output else 'No articles found'


if __name__ == '__main__':
    sys.exit(main())
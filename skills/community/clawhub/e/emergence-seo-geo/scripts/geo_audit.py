#!/usr/bin/env python3
"""
GEO/SEO Automated Auditor Script
Inspects a target website for conversational search engine readiness.
Calculates a baseline score based on technical access, schemas, and AI metadata.
Supports E2E verification using Brave and Tavily CLIs, and Google/Bing search fallback checks.
"""

import sys
import urllib.request
import urllib.parse
import re
import json
import subprocess
import shutil
import argparse
from html.parser import HTMLParser

class MetaPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headers = {"h1": 0, "h2": 0, "h3": 0}
        self.ld_json_count = 0
        self.in_script = False
        self.script_type = ""
        self.p_tag_count = 0
        self.first_p_content = ""
        self.in_p = False

    def handle_starttag(self, tag, attrs):
        if tag in self.headers:
            self.headers[tag] += 1
        if tag == "script":
            self.in_script = True
            for name, val in attrs:
                if name == "type" and "application/ld+json" in val:
                    self.script_type = "ld-json"
        elif tag == "p":
            self.p_tag_count += 1
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
            self.script_type = ""
        elif tag == "p":
            self.in_p = False

    def handle_data(self, data):
        if self.in_script and self.script_type == "ld-json":
            if "@context" in data and "schema.org" in data:
                self.ld_json_count += 1
        if self.in_p and self.p_tag_count == 1:
            self.first_p_content += data.strip()

def fetch_url(url, timeout=8):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        import ssl
        try:
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
                return response.status, response.read().decode("utf-8", errors="ignore")
        except Exception as e2:
            return 0, str(e2)

def check_e2e_indexing(domain, prompt=None):
    e2e_results = {}
    
    bx_path = shutil.which("bx") or "/Users/julian/.local/bin/bx"
    tvly_path = shutil.which("tvly") or "/Users/julian/.local/bin/tvly"
    
    # 1. Brave Search Index Check
    brave_indexed = False
    brave_details = "Brave Search CLI not available."
    brave_rankings = {}
    
    if bx_path:
        # Check domain indexation
        cmd_index = [bx_path, "web", f"site:{domain}"]
        try:
            res = subprocess.run(cmd_index, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                results = data.get("web", {}).get("results", [])
                if results:
                    brave_indexed = True
                    brave_details = f"Indexed: Found {len(results)} pages in Brave Search index."
                else:
                    brave_details = "Not found in Brave Search index."
            else:
                brave_details = f"Brave CLI returned error: {res.stderr.strip()}"
        except Exception as e:
            brave_details = f"Error running Brave CLI: {str(e)}"
            
        # Check keyword/prompt rank
        if prompt:
            cmd_rank = [bx_path, "web", prompt]
            try:
                res = subprocess.run(cmd_rank, capture_output=True, text=True, timeout=15)
                rank = -1
                found_url = None
                if res.returncode == 0:
                    data = json.loads(res.stdout)
                    results = data.get("web", {}).get("results", [])
                    for i, r in enumerate(results):
                        url = r.get("url", "")
                        if domain in url:
                            rank = i + 1
                            found_url = url
                            break
                brave_rankings[prompt] = {"found": rank != -1, "rank": rank, "url": found_url}
            except Exception:
                brave_rankings[prompt] = {"found": False, "rank": -1, "url": None}
    
    e2e_results["brave"] = {
        "indexed": brave_indexed,
        "details": brave_details,
        "rankings": brave_rankings
    }

    # 2. Tavily Search Index Check
    tavily_indexed = False
    tavily_details = "Tavily CLI not available."
    tavily_rankings = {}
    
    if tvly_path:
        # Check domain indexation (Tavily doesn't support site: queries, so search for domain)
        cmd_index = [tvly_path, "search", domain, "--json"]
        try:
            res = subprocess.run(cmd_index, capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                results = data.get("results", [])
                matching_results = [r for r in results if domain in r.get("url", "")]
                if matching_results:
                    tavily_indexed = True
                    tavily_details = f"Indexed: Found footprint matches in Tavily Search."
                else:
                    tavily_details = "No matching footprint found in Tavily search results."
            else:
                tavily_details = f"Tavily CLI returned error: {res.stderr.strip()}"
        except Exception as e:
            tavily_details = f"Error running Tavily CLI: {str(e)}"
            
        # Check keyword/prompt rank
        if prompt:
            cmd_rank = [tvly_path, "search", prompt, "--json"]
            try:
                res = subprocess.run(cmd_rank, capture_output=True, text=True, timeout=15)
                rank = -1
                found_url = None
                if res.returncode == 0:
                    data = json.loads(res.stdout)
                    results = data.get("results", [])
                    for i, r in enumerate(results):
                        url = r.get("url", "")
                        if domain in url:
                            rank = i + 1
                            found_url = url
                            break
                tavily_rankings[prompt] = {"found": rank != -1, "rank": rank, "url": found_url}
            except Exception:
                tavily_rankings[prompt] = {"found": False, "rank": -1, "url": None}
                
    e2e_results["tavily"] = {
        "indexed": tavily_indexed,
        "details": tavily_details,
        "rankings": tavily_rankings
    }

    # 3. Google Index Check (Lightweight HTTP Check)
    google_indexed = False
    google_details = "Google direct check not executed."
    google_url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}"
    
    g_status, g_html = fetch_url(google_url)
    if g_status == 200:
        if "did not match any documents" in g_html or "未找到符合" in g_html:
            google_indexed = False
            google_details = "No documents matched domain in Google Search."
        else:
            google_indexed = domain in g_html
            google_details = "Footprint detected in Google search page HTML." if google_indexed else "Domain not clearly identified in Google search page HTML."
    elif g_status == 0:
        google_details = f"Google block / request failed: {g_html}"
    else:
        google_details = f"Google rate-limited or blocked (HTTP Status: {g_status}). Check manually in Search Console."

    e2e_results["google"] = {
        "indexed": google_indexed,
        "details": google_details
    }

    # 4. Bing Index Check (Lightweight HTTP Check)
    bing_indexed = False
    bing_details = "Bing direct check not executed."
    bing_url = f"https://www.bing.com/search?q=site:{urllib.parse.quote(domain)}"
    
    b_status, b_html = fetch_url(bing_url)
    if b_status == 200:
        if "No results found for" in b_html or "没有找到与" in b_html:
            bing_indexed = False
            bing_details = "No pages found in Bing Search."
        else:
            bing_indexed = domain in b_html
            bing_details = "Footprint detected in Bing search page HTML." if bing_indexed else "Domain not clearly identified in Bing search page HTML."
    elif b_status == 0:
        bing_details = f"Bing block / request failed: {b_html}"
    else:
        bing_details = f"Bing rate-limited or blocked (HTTP Status: {b_status}). Check manually in Webmaster Tools."

    e2e_results["bing"] = {
        "indexed": bing_indexed,
        "details": bing_details
    }

    return e2e_results

def audit_url(url, domain_type="human", prompt=None, run_e2e=False):
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    domain = parsed_url.netloc
    
    # 1. Fetch main page
    status, html_content = fetch_url(url)
    if status != 200:
        return {"error": f"Failed to fetch {url}. Status: {status}, Detail: {html_content}"}

    parser = MetaPageParser()
    parser.feed(html_content)

    # 2. Check robots.txt
    robots_url = f"{base_url}/robots.txt"
    robots_status, robots_txt = fetch_url(robots_url)
    
    robots_active = False
    if robots_status == 200:
        robots_active = True

    # 3. Fetch machine-readable metadata files
    llms_url = f"{base_url}/llms.txt"
    pricing_url = f"{base_url}/pricing.md"
    skill_url = f"{base_url}/skill.md"
    sitemap_url = f"{base_url}/sitemap.xml"
    
    llms_status, llms_content = fetch_url(llms_url)
    pricing_status, _ = fetch_url(pricing_url)
    skill_status, _ = fetch_url(skill_url)
    
    # Check sitemap
    sitemap_found = False
    if robots_status == 200 and "sitemap:" in robots_txt.lower():
        sitemap_found = True
    else:
        sitemap_status, _ = fetch_url(sitemap_url)
        if sitemap_status == 200:
            sitemap_found = True

    # 4. Scoring logic
    score_breakdown = {}
    
    # Accessibility Score (Max 15 pts)
    if domain_type == "agent":
        ai_bots = ["GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended", "Bingbot"]
        blocked_bots = []
        if robots_status == 200:
            for bot in ai_bots:
                pattern = rf"(?i)User-agent:\s*(\*|{bot}).*?Disallow:\s*/(\s|$)"
                if re.search(pattern, robots_txt, re.DOTALL):
                    blocked_bots.append(bot)
        access_score = 15 - (len(blocked_bots) * 3)
        detail_accessibility = f"Blocked AI bots: {blocked_bots if blocked_bots else 'None'}. Robots.txt active: {robots_active}"
    else:
        human_bots = ["Googlebot", "Bingbot"]
        blocked_bots = []
        if robots_status == 200:
            for bot in human_bots:
                pattern = rf"(?i)User-agent:\s*(\*|{bot}).*?Disallow:\s*/(\s|$)"
                if re.search(pattern, robots_txt, re.DOTALL):
                    blocked_bots.append(bot)
        access_score = 15 - (len(blocked_bots) * 7.5)
        detail_accessibility = f"Blocked search bots: {blocked_bots if blocked_bots else 'None'}. Robots.txt active: {robots_active}"

    score_breakdown["Technical Accessibility"] = {
        "score": max(0, int(access_score)),
        "max": 15,
        "detail": detail_accessibility
    }

    # Schema Score (Max 10 pts)
    schema_score = 10 if parser.ld_json_count > 0 else 0
    score_breakdown["Structured Schema Quality"] = {
        "score": schema_score,
        "max": 10,
        "detail": f"Found {parser.ld_json_count} schema definitions in JSON-LD format."
    }

    # Header and Structure Score (Max 15 pts)
    h1_score = 5 if parser.headers["h1"] == 1 else (2 if parser.headers["h1"] > 1 else 0)
    h2_h3_score = 10 if (parser.headers["h2"] > 0 or parser.headers["h3"] > 0) else 0
    score_breakdown["Content Extractability & Layout"] = {
        "score": h1_score + h2_h3_score,
        "max": 15,
        "detail": f"H1 counts: {parser.headers['h1']}. H2/H3 counts: H2={parser.headers['h2']}, H3={parser.headers['h3']}"
    }

    # BLUF/Paragraph formatting (Max 10 pts)
    words = parser.first_p_content.split()
    word_count = len(words)
    bluf_score = 0
    if 25 <= word_count <= 70:
        bluf_score = 10
    elif 1 <= word_count < 25:
        bluf_score = 5
    score_breakdown["Answer Density (BLUF)"] = {
        "score": bluf_score,
        "max": 10,
        "detail": f"First paragraph word count: {word_count} words. Content snippet: '{parser.first_p_content[:60]}...'"
    }

    # Machine-Readable Discovery (Max 10 pts)
    metadata_score = 0
    detail_msg = ""
    if domain_type == "agent":
        llms_score = 5 if llms_status == 200 else 0
        skill_score = 5 if (skill_status == 200 or pricing_status == 200) else 0
        
        has_pricing_in_llms = False
        if llms_status == 200:
            pricing_keywords = ["price", "pricing", "cost", "fee", "credits", "资费", "价格", "收费"]
            for kw in pricing_keywords:
                if kw in llms_content.lower():
                    has_pricing_in_llms = True
                    break
        
        if has_pricing_in_llms and llms_status == 200:
            metadata_score = 10
            detail_msg = "llms.txt HTTP status: 200 (Pricing details detected inside llms.txt)."
        else:
            metadata_score = llms_score + skill_score
            detail_msg = f"llms.txt status: {llms_status}. skill.md/pricing.md status: {skill_status if skill_status == 200 else pricing_status}"
    else:
        # Human-first
        sitemap_score = 5 if sitemap_found else 0
        social_meta = False
        if "og:" in html_content or "twitter:" in html_content:
            social_meta = True
        social_score = 5 if social_meta else 0
        metadata_score = sitemap_score + social_score
        detail_msg = f"Sitemap found: {sitemap_found}. OpenGraph/Twitter social meta tags present: {social_meta}."

    score_breakdown["Machine-Readable Discovery"] = {
        "score": metadata_score,
        "max": 10,
        "detail": detail_msg
    }

    # Heuristic-based Automated Metrics
    # Citations & Empirical Data (Max 15 pts)
    has_numbers = len(re.findall(r'\b\d+\b', html_content)) > 10
    has_percentages = '%' in html_content or 'percent' in html_content.lower()
    all_links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html_content)
    external_links = [l for l in all_links if parsed_url.netloc not in l]
    has_external_links = len(external_links) > 2
    
    citation_score = 0
    citation_details = []
    if has_numbers:
        citation_score += 5
        citation_details.append("Contains numeric metrics")
    if has_percentages:
        citation_score += 5
        citation_details.append("Contains percentages")
    if has_external_links:
        citation_score += 5
        citation_details.append("Contains external references")
        
    score_breakdown["Citations & Empirical Data"] = {
        "score": citation_score,
        "max": 15,
        "detail": ", ".join(citation_details) if citation_details else "No empirical data or external citations found."
    }

    # Expertise & Attribution (EEAT) (Max 10 pts)
    eeat_score = 0
    eeat_details = []
    has_author_signals = any(w in html_content.lower() for w in ["author", "written by", "reviewed by", "founder", "team of", "creator", "roaster", "expert"])
    has_contact_signals = any(w in html_content.lower() for w in ["about us", "contact us", "our team", "about-us", "contact-us"]) or any("about" in l or "team" in l or "contact" in l for l in all_links)
    
    if has_author_signals:
        eeat_score += 5
        eeat_details.append("Expert/author signals detected")
    if has_contact_signals:
        eeat_score += 5
        eeat_details.append("Team/contact/transparency pages detected")
        
    score_breakdown["Expertise & Attribution (EEAT)"] = {
        "score": eeat_score,
        "max": 10,
        "detail": ", ".join(eeat_details) if eeat_details else "No clear authorship or brand transparency indicators found."
    }

    # Off-Page Entity Footprint (Max 15 pts)
    e2e_data = None
    footprint_score = 0
    footprint_details = ""
    
    # Check social links
    social_domains = ["github.com", "twitter.com", "x.com", "reddit.com", "linkedin.com", "facebook.com", "youtube.com", "medium.com"]
    social_links_found = [l for l in all_links if any(sd in l for sd in social_domains)]
    
    if run_e2e:
        print("Running E2E search engine indexation checks...")
        e2e_data = check_e2e_indexing(domain, prompt)
        
        # Count hits
        hits = 0
        if e2e_data.get("brave", {}).get("indexed"):
            hits += 2
        if e2e_data.get("tavily", {}).get("indexed"):
            hits += 2
        if e2e_data.get("google", {}).get("indexed"):
            hits += 2
        if e2e_data.get("bing", {}).get("indexed"):
            hits += 2
            
        if hits >= 6:
            footprint_score = 15
            footprint_details = f"Strong off-page index coverage detected across major engines."
        elif hits >= 4:
            footprint_score = 10
            footprint_details = f"Moderate off-page coverage detected across engines."
        elif hits >= 2:
            footprint_score = 5
            footprint_details = f"Sparse index cover detected. Only minor search footprints found."
        else:
            footprint_score = 0
            footprint_details = "Critical exclusion: Site not indexed in search engine indices."
    else:
        if len(social_links_found) > 2:
            footprint_score = 15
            footprint_details = f"Strong off-page reference nodes found in HTML (found {len(social_links_found)} social links)."
        elif len(social_links_found) > 0:
            footprint_score = 10
            footprint_details = f"Moderate off-page reference nodes found in HTML (found {len(social_links_found)} social links)."
        else:
            footprint_score = 5
            footprint_details = "Default score. Run with --e2e for a live search index footprint audit."

    score_breakdown["Off-Page Entity Footprint"] = {
        "score": footprint_score,
        "max": 15,
        "detail": footprint_details
    }

    # Summarize crawler scores
    crawler_score = sum(val["score"] for val in score_breakdown.values())
    max_crawler_score = sum(val["max"] for val in score_breakdown.values())

    response = {
        "url": url,
        "domain_type": domain_type,
        "total_score_crawler_only": crawler_score,
        "max_crawler_score": max_crawler_score,
        "breakdown": score_breakdown
    }
    
    if prompt:
        response["prompt"] = prompt
    if e2e_data:
        response["e2e_verification"] = e2e_data

    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated GEO/SEO Auditor Script")
    parser.add_argument("url", help="Target URL to inspect")
    parser.add_argument("--type", choices=["agent", "human"], default="human", help="Site type (agent-first or human-first)")
    parser.add_argument("--prompt", help="Semantic Search Prompt to verify indexing/rankings for")
    parser.add_argument("--keywords", help="Legacy comma-separated keywords parameter (mapped to prompt)")
    parser.add_argument("--e2e", action="store_true", help="Run E2E indexing checks on Brave, Tavily, Google, Bing")
    
    # Handle legacy argument style if argv contains no flags and just 1 argument
    if len(sys.argv) == 2:
        args = parser.parse_args()
    else:
        args = parser.parse_args()

    url = args.url
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Map legacy keywords to prompt if prompt is not explicitly passed
    prompt_query = args.prompt
    if not prompt_query and args.keywords:
        # Use first keyword as prompt
        prompt_query = args.keywords.split(",")[0].strip()

    result = audit_url(url, domain_type=args.type, prompt=prompt_query, run_e2e=args.e2e)
    print(json.dumps(result, indent=2))

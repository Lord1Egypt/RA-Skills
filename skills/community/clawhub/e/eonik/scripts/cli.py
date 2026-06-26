#!/usr/bin/env python3
import sys
import os
import json
import urllib.request
import urllib.parse
import argparse

API_URL = os.environ.get("EONIK_API_URL", "https://api.eonik.ai")
API_KEY = os.environ.get("EONIK_API_KEY")

if not API_KEY:
    print(json.dumps({"error": "EONIK_API_KEY environment variable is required"}))
    sys.exit(1)

# Route definitions: Tool Name -> (Method, Endpoint)
ROUTES = {
    # Analyze
    "run_budget_audit": ("POST", "/api/budget-agent/run-audit"),
    "get_creative_autopsy": ("GET", "/api/autopsy/command-center"),
    
    # Ideate
    "discover_trends": ("POST", "/api/trends/discover"),
    "get_brand_context": ("GET", "/api/brand-context"),
    "search_ad_library": ("GET", "/api/library/ads"),
    "get_insights_feed": ("GET", "/api/insights/feed"),
    "get_experimentation_gaps": ("GET", "/api/insights/experimentation-gaps"),
    
    # Produce
    "create_ad_creation_run": ("POST", "/api/ad-creation/runs"),
    "compile_seed_spec": ("POST", "/api/ad-creation/runs/{run_id}/compile-seed-spec"),
    "generate_creative_brief": ("POST", "/api/autopsy/generate-brief"),
    
    # Deploy
    "launch_ad_run": ("POST", "/api/ad-creation/runs/{run_id}/launch"),
    
    # Competitive Intel
    "get_my_competitor_ads": ("GET", "/api/autopsy/command-center/competitor-ads"),
    "search_competitor_ads": ("GET", "/api/library/ads"),
    
    # Genome
    "get_genome_matrix": ("GET", "/api/insights/{platform}/genome-matrix"),
    "get_fatigue_signals": ("GET", "/api/insights/{platform}/fatigue-trends"),
    "get_budget_leaks": ("GET", "/api/autopsy/budget-leaks"),
    "get_early_winners": ("GET", "/api/autopsy/early-winners"),
    
    # Experiments
    "list_experiments": ("GET", "/api/experiments"),
    "get_hypothesis_queue": ("GET", "/api/experiments/hypothesis-queue"),
    
    # Cross Platform
    "get_tiktok_performance": ("GET", "/api/tiktok-analytics/overview"),
    "get_google_performance": ("GET", "/api/google-analytics/overview"),
    
    # Status
    "get_shopify_status": ("GET", "/api/shopify/status"),
    "get_slack_status": ("GET", "/api/slack/status"),
}

def parse_args():
    parser = argparse.ArgumentParser(description="Eonik Agent Universal CLI Wrapper")
    parser.add_argument("tool", help="The name of the tool to run")
    parser.add_argument("--json", help="Pass all arguments as a JSON string", default="{}")
    return parser.parse_known_args()

def main():
    args, unknown = parse_args()
    tool = args.tool
    
    if tool not in ROUTES:
        print(json.dumps({"error": f"Unknown tool: {tool}"}))
        sys.exit(1)
        
    method, path = ROUTES[tool]
    
    # Parse generic kwargs
    payload = json.loads(args.json)
    
    # Parse dynamic key-value pairs (e.g. --days 30 --platform tiktok)
    for i in range(0, len(unknown), 2):
        if unknown[i].startswith("--") and i+1 < len(unknown):
            key = unknown[i][2:]
            val = unknown[i+1]
            # Try typecasting
            if val.isdigit(): val = int(val)
            elif val.lower() == 'true': val = True
            elif val.lower() == 'false': val = False
            payload[key] = val
            
    # Handle path formatting
    if "{run_id}" in path and "run_id" in payload:
        path = path.replace("{run_id}", str(payload.pop("run_id")))
    if "{platform}" in path:
        platform = payload.pop("platform", "meta")
        path = path.replace("{platform}", str(platform))
        
    url = f"{API_URL}{path}"
    
    # Construct Request
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Content-Type", "application/json")
    
    data = None
    if method == "GET" and payload:
        url += "?" + urllib.parse.urlencode(payload)
        req.full_url = url
    elif method == "POST" and payload:
        data = json.dumps(payload).encode('utf-8')
        
    try:
        with urllib.request.urlopen(req, data=data) as response:
            result = response.read().decode('utf-8')
            # Just print the raw JSON out for the agent
            print(result)
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        print(json.dumps({"error": f"API Error ({e.code})", "details": error_msg}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": "Failed to connect to Eonik API", "details": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()

import json
import concurrent.futures
import sys
import os
from fetch_news import (
    fetch_hackernews, fetch_github, fetch_producthunt, 
    fetch_weibo, fetch_36kr, fetch_tencent, fetch_v2ex, fetch_wallstreetcn,
    fetch_huggingface_papers, fetch_ai_newsletters, fetch_podcasts, fetch_essays,
    enrich_items_with_content
)

import argparse

# --- Profile Configurations ---

PROFILES = {
    # 1. 综合早报 (General Morning Routine)
    "general": {
        "global_scan": {
            "sources": [
                (fetch_hackernews, 5, None),
                (fetch_producthunt, 5, None),
                (fetch_github, 5, None),
                (fetch_weibo, 5, None),
                (fetch_36kr, 5, None),
                (fetch_tencent, 5, None),
                (fetch_wallstreetcn, 5, None),
                (fetch_v2ex, 5, None)
            ],
            "enrich": True
        },
        "hn_ai": {
            "sources": [(fetch_hackernews, 20, "AI,LLM,GPT,DeepSeek,Github Copilot,Claude,OpenAI")],
            "enrich": True
        },
        "github_trending": {
            "sources": [(fetch_github, 15, None)],
            "enrich": True
        }
    },

    # 2. 财经早报 (Finance)
    "finance": {
        "market_overview": {
            "sources": [
                (fetch_wallstreetcn, 30, None),
                (fetch_hackernews, 10, "Economy,Inflation,Fed,Stock,Finance")
            ],
            "enrich": True
        },
        "china_finance": {
            "sources": [
                (fetch_36kr, 20, "财报,营收,上市,IPO,基金,投资"),
                (fetch_tencent, 15, "财经,股票,基金")
            ],
            "enrich": True
        },
        "crypto": {
            "sources": [
                (fetch_hackernews, 15, "Bitcoin,Crypto,Ethereum,Blockchain,Web3,DeFi"),
                (fetch_wallstreetcn, 10, "比特币,加密货币")
            ],
            "enrich": True
        }
    },

    # 3. 科技早报 (Tech)
    "tech": {
        "ai_frontier": {
            "sources": [
                (fetch_hackernews, 25, "AI,LLM,Transformer,Diffusion,Model,RAG"),
                (fetch_github, 10, "AI,LLM,GPT")
            ],
            "enrich": True
        },
        "dev_tools": {
            "sources": [
                (fetch_producthunt, 20, "Developer Tools,Coding,API"),
                (fetch_github, 15, None)
            ],
            "enrich": True
        },
        "startups": {
            "sources": [(fetch_36kr, 20, "融资,首发,独角兽,创投"), (fetch_producthunt, 10, None)],
            "enrich": True
        }
    },

    # 4. 吃瓜早报 (Social/Gossip)
    "social": {
        "weibo_hot": {
            "sources": [(fetch_weibo, 40, None)],
            "enrich": False # No need for deep verify, just title/heat
        },
        "v2ex_hot": {
            "sources": [(fetch_v2ex, 30, None)],
            "enrich": True # Content is fun
        }
    },

    # 5. GitHub Trending (Github Only)
    "github": {
        "github_trending": {
            "sources": [(fetch_github, 20, None)],
            "enrich": True
        }
    },


    # 6. AI Daily (AI Deep Dive)
    "ai_daily": {
        "newsletter_picks": {
            "sources": [(fetch_ai_newsletters, 100, None)], # Capture all (approx 30-40)
            "enrich": True
        },
        "huggingface_papers": {
            "sources": [(fetch_huggingface_papers, 20, None)], 
            "enrich": True
        }
    },

    # 7. Reading List (Podcasts & Essays)
    "reading_list": {
        "essays": {
            "sources": [(fetch_essays, 50, None)], # Capture all
            "enrich": True
        },
        "podcasts": {
            "sources": [(fetch_podcasts, 50, None)],
            "enrich": False 
        },
        "hn_deep": {
            "sources": [(fetch_hackernews, 20, "blog,essay,philosophy,book")],
            "enrich": True
        }
    }
}


def fetch_section(section_name, config):
    print(f"[{section_name}] Starting fetch...", file=sys.stderr)
    results = []
    
    # Run source fetchers for this section in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_map = {}
        for func, limit, kw in config["sources"]:
            future = executor.submit(func, limit, kw)
            future_map[future] = f"{func.__name__}"
            
        for future in concurrent.futures.as_completed(future_map):
            fname = future_map[future]
            try:
                items = future.result()
                results.extend(items)
                print(f"[{section_name}] {fname} returned {len(items)} items", file=sys.stderr)
            except Exception as e:
                print(f"[{section_name}] {fname} failed: {e}", file=sys.stderr)

    # Enrich if requested
    if config["enrich"] and results:
        print(f"[{section_name}] Enriching content for {len(results)} items...", file=sys.stderr)
        results = enrich_items_with_content(results, max_workers=10)
        
    return results

def save_individual_sources(data, base_dir):
    """
    Splits the aggregated data by 'source' and saves individual JSON files.
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    source_map = {}
    total_count = 0
    
    # Flatten and grouping
    for section, items in data.items():
        for item in items:
            src = item.get('source', 'Unknown')
            # Sanitize filename
            safe_name = "".join([c if c.isalnum() else "_" for c in src])
            if safe_name not in source_map:
                source_map[safe_name] = []
            source_map[safe_name].append(item)
            total_count += 1
            
    # Save
    print(f"Saving {len(source_map)} individual source files to {base_dir}...", file=sys.stderr)
    for src, items in source_map.items():
        fpath = os.path.join(base_dir, f"{src}.json")
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    return list(source_map.keys())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='general', choices=PROFILES.keys(), help='Briefing Profile')
    parser.add_argument('--outdir', help='Optional output directory for individual files')
    parser.add_argument('--no-save', action='store_true', help='Skip saving JSON files to disk (only output to stdout)')
    args = parser.parse_args()
    
    config = PROFILES.get(args.profile, PROFILES['general'])
    
    final_data = {}
    
    # Fetch all sections
    for section, sec_config in config.items():
        final_data[section] = fetch_section(section, sec_config)
    
    # Determine Output Directory
    # Default to reports/YYYY-MM-DD
    if args.outdir:
        out_dir = args.outdir
    else:
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', today)
        
    # Validating existence or creating is handled in save logic, but let's be explicitly safe
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Output result to stdout (for agent to read)
    print(json.dumps(final_data, indent=2, ensure_ascii=False))
    
    if not args.no_save:
        # Save Unified JSON
        unified_path = os.path.join(out_dir, f"{args.profile}_briefing_unified.json")
        with open(unified_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
            
        # Save Individual Sources
        sources_saved = save_individual_sources(final_data, out_dir)
        print(f"Saved unified report and {len(sources_saved)} individual source files to {out_dir}", file=sys.stderr)
    else:
        print(f"JSON output sent to stdout only (--no-save mode)", file=sys.stderr)

if __name__ == "__main__":
    main()

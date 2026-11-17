#!/usr/bin/env python3
"""
TikTok Learning Loop
Tracks post performance and optimizes strategy
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Config
DATA_DIR = Path("/Users/g0atface/clawd/skills/tiktok-carousel/data")
METRICS_FILE = DATA_DIR / "metrics.json"
PERFORMANCE_FILE = DATA_DIR / "performance.json"

DATA_DIR.mkdir(exist_ok=True)

def log_metrics(carousel_id, views, likes, shares, comments, downloads=None):
    """Log metrics for a posted carousel"""
    
    metrics = {}
    if METRICS_FILE.exists():
        metrics = json.loads(METRICS_FILE.read_text())
    
    metrics[carousel_id] = {
        "posted_at": datetime.now().isoformat(),
        "views": views,
        "likes": likes,
        "shares": shares,
        "comments": comments,
        "downloads": downloads,
        "engagement_rate": (likes + shares + comments) / max(views, 1) * 100
    }
    
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))
    print(f"📊 Logged metrics for {carousel_id}")
    print(f"   Views: {views:,} | Engagement: {metrics[carousel_id]['engagement_rate']:.2f}%")

def analyze_performance():
    """Analyze performance and find best/worst performers"""
    
    if not METRICS_FILE.exists():
        print("❌ No metrics available")
        return
    
    metrics = json.loads(METRICS_FILE.read_text())
    
    if not metrics:
        print("📊 No posts logged yet")
        return
    
    # Calculate averages
    views = [m["views"] for m in metrics.values()]
    engagement = [m["engagement_rate"] for m in metrics.values()]
    
    avg_views = sum(views) / len(views)
    avg_engagement = sum(engagement) / len(engagement)
    
    # Find best and worst
    best = max(metrics.items(), key=lambda x: x[1]["views"])
    worst = min(metrics.items(), key=lambda x: x[1]["views"])
    
    print("📊 Performance Analysis")
    print(f"   Total posts: {len(metrics)}")
    print(f"   Avg views: {avg_views:,.0f}")
    print(f"   Avg engagement: {avg_engagement:.2f}%")
    print()
    print(f"🏆 Best: {best[0]}")
    print(f"   Views: {best[1]['views']:,} | Eng: {best[1]['engagement_rate']:.2f}%")
    print(f"   Hook: {best[1].get('hook', 'N/A')[:60]}...")
    print()
    print(f"💀 Worst: {worst[0]}")
    print(f"   Views: {worst[1]['views']:,} | Eng: {worst[1]['engagement_rate']:.2f}%")
    
    return metrics

def generate_insights():
    """Generate optimization insights"""
    
    metrics = analyze_performance()
    if not metrics:
        return
    
    insights = []
    
    # Analyze by engagement rate
    high_engagement = {k: v for k, v in metrics.items() if v["engagement_rate"] > 5}
    low_engagement = {k: v for k, v in metrics.items() if v["engagement_rate"] < 2}
    
    if high_engagement:
        insights.append(f"✅ High engagement posts (>5%): {len(high_engagement)}")
    
    if low_engagement:
        insights.append(f"⚠️ Low engagement posts (<2%): {len(low_engagement)}")
    
    # Check for viral patterns
    viral = {k: v for k, v in metrics.items() if v["views"] > 10000}
    if viral:
        insights.append(f"🚀 Viral posts (>10K views): {len(viral)}")
    
    # Output insights
    if insights:
        print()
        print("💡 Insights:")
        for insight in insights:
            print(f"   {insight}")
    
    return insights

def update_strategy():
    """Update strategy based on performance"""
    
    insights = generate_insights()
    
    if not insights:
        return
    
    strategy_file = DATA_DIR / "strategy.json"
    strategy = {}
    
    if strategy_file.exists():
        strategy = json.loads(strategy_file.read_text())
    
    # Update based on insights
    strategy["last_updated"] = datetime.now().isoformat()
    strategy["insights"] = insights
    
    strategy_file.write_text(json.dumps(strategy, indent=2))
    print(f"✅ Strategy updated")

def track_hook_performance(hook, views):
    """Track which hooks perform best"""
    
    hook_file = DATA_DIR / "hook_performance.json"
    hooks = {}
    
    if hook_file.exists():
        hooks = json.loads(hook_file.read_text())
    
    if hook not in hooks:
        hooks[hook] = {"count": 0, "total_views": 0}
    
    hooks[hook]["count"] += 1
    hooks[hook]["total_views"] += views
    
    hook_file.write_text(json.dumps(hooks, indent=2))
    
    # Print average
    avg = hooks[hook]["total_views"] / hooks[hook]["count"]
    print(f"📊 Hook: {hook[:50]}...")
    print(f"   Avg views: {avg:,.0f}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TikTok Learning Loop")
    parser.add_argument("--log", "-l", nargs=5, metavar=("ID", "VIEWS", "LIKES", "SHARES", "COMMENTS"),
                        help="Log metrics: ID VIEWS LIKES SHARES COMMENTS")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze performance")
    parser.add_argument("--insights", "-i", action="store_true", help="Generate insights")
    parser.add_argument("--update", "-u", action="store_true", help="Update strategy")
    parser.add_argument("--track-hook", "-t", nargs=2, metavar=("HOOK", "VIEWS"),
                        help="Track hook performance")
    
    args = parser.parse_args()
    
    if args.log:
        log_metrics(*args.log)
    
    if args.analyze:
        analyze_performance()
    
    if args.insights:
        generate_insights()
    
    if args.update:
        update_strategy()
    
    if args.track_hook:
        track_hook_performance(args.track_hook[0], int(args.track_hook[1]))
    
    if not any([args.log, args.analyze, args.insights, args.update, args.track_hook]):
        analyze_performance()

if __name__ == "__main__":
    main()

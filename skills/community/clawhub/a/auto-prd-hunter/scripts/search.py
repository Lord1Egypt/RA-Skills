#!/usr/bin/env python3
"""
auto-prd-hunter: Search for user pain points and generate PRD JSON

Usage:
    python3 search.py search-pain-points --keyword "<keyword>" --max-results 8

Environment Variables:
    BRAVE_API_KEY: Brave Search API key (optional, but recommended for better results)
    BAIDU_API_KEY: Baidu Search API key (optional, for Chinese content)

Network Requests:
    - api.search.brave.com (Brave Search API)
    - hn.algolia.com (Hacker News Algolia API)

Privacy Notice:
    Your search keywords will be sent to external API services.
    Do not include sensitive or confidential information in keywords.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import List, Dict, Any, Optional


def search_brave_api(keyword: str, max_results: int = 10) -> List[Dict]:
    """
    Search using Brave Search API
    
    Args:
        keyword: Search keyword
        max_results: Maximum number of results
    
    Returns:
        List of search results with platform, title, url, snippet
    """
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        print("INFO: BRAVE_API_KEY not set, skipping Brave Search", file=sys.stderr)
        return []
    
    results = []
    try:
        url = f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(keyword)}&count={max_results}"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("X-Subscription-Token", api_key)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            for item in data.get("web", {}).get("results", []):
                results.append({
                    "platform": "Brave Search",
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", "")
                })
        print(f"INFO: Found {len(results)} results from Brave Search", file=sys.stderr)
    except urllib.error.HTTPError as e:
        print(f"ERROR: Brave API HTTP error {e.code}: {e.reason}", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"ERROR: Brave API network error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Brave API error: {e}", file=sys.stderr)
    
    return results


def search_hackernews(keyword: str, max_results: int = 10) -> List[Dict]:
    """
    Search Hacker News via Algolia API (no API key required)
    
    Args:
        keyword: Search keyword
        max_results: Maximum number of results
    
    Returns:
        List of search results with platform, title, url, snippet, points, num_comments
    """
    results = []
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(keyword)}&tags=story&hitsPerPage={max_results}"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            for hit in data.get("hits", []):
                title = hit.get("title", "")
                # Check for pain point indicators in title
                pain_indicators = ["problem", "issue", "why", "how to", "struggle", "help", "advice", "tips"]
                if any(indicator in title.lower() for indicator in pain_indicators):
                    results.append({
                        "platform": "Hacker News",
                        "title": title,
                        "url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                        "snippet": title,
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0)
                    })
        print(f"INFO: Found {len(results)} relevant results from Hacker News", file=sys.stderr)
    except urllib.error.URLError as e:
        print(f"ERROR: Hacker News API network error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Hacker News API error: {e}", file=sys.stderr)
    
    return results


def extract_pain_points(results: List[Dict], max_points: int = 5) -> List[Dict]:
    """
    Extract pain points from search results
    
    Args:
        results: List of search results
        max_points: Maximum number of pain points to extract
    
    Returns:
        List of pain point dictionaries
    """
    pain_points = []
    
    for i, result in enumerate(results[:max_points]):
        # Assign severity based on position and engagement
        severity = "high" if i < 2 else "medium" if i < 4 else "low"
        
        pain_point = {
            "id": f"PP-{i+1:03d}",
            "title": result.get("title", "Unknown pain point"),
            "severity": severity,
            "context": result.get("snippet", result.get("title", "")),
            "sources": [{
                "platform": result.get("platform", "Web"),
                "url": result.get("url", ""),
                "quote": result.get("snippet", result.get("title", ""))
            }]
        }
        
        # Add engagement metrics if available
        if "points" in result:
            pain_point["engagement"] = {
                "points": result["points"],
                "comments": result.get("num_comments", 0)
            }
        
        pain_points.append(pain_point)
    
    return pain_points


def generate_product_name(keyword: str) -> str:
    """Generate a creative product name based on keyword"""
    import random
    
    prefixes = ["Smart", "Easy", "Quick", "Pro", "Auto", "Mind", "Flow", "Hub", "Pal", "Go"]
    suffixes = ["Hub", "Pro", "Go", "Now", "Plus", "X", "AI", "App", "Tool", "Mate"]
    
    keyword_clean = keyword.split()[0].title() if ' ' in keyword else keyword.title()
    
    name_templates = [
        f"{random.choice(prefixes)}{keyword_clean}",
        f"{keyword_clean}{random.choice(suffixes)}",
        f"{random.choice(prefixes)}{random.choice(suffixes)}"
    ]
    
    return random.choice(name_templates)


def generate_user_stories(pain_points: List[Dict]) -> List[Dict]:
    """Generate user stories from pain points"""
    stories = []
    
    for i, pp in enumerate(pain_points):
        title = pp.get("title", "")
        
        # Extract key action from title
        story = {
            "id": f"US-{i+1:03d}",
            "as_a": "用户",
            "i_want_to": f"解决{title}的问题",
            "so_that": "我可以更好地完成目标",
            "acceptance_criteria": [
                f"能够识别并记录{title}",
                f"提供针对{title}的解决方案",
                "用户满意度>80%"
            ],
            "priority": "P0" if pp.get("severity") == "high" else "P1" if pp.get("severity") == "medium" else "P2",
            "pain_point_ids": [pp["id"]]
        }
        
        stories.append(story)
    
    return stories


def generate_mvp_features(user_stories: List[Dict], pain_points: List[Dict]) -> List[Dict]:
    """Generate MVP features from user stories"""
    features = []
    
    for i, story in enumerate(user_stories[:5]):
        # Extract feature name from user story
        feature_name = story["i_want_to"].replace("获得", "").replace("解决", "").replace("的问题", "")
        
        feature = {
            "id": f"F-{i+1:03d}",
            "title": f"{feature_name}功能",
            "description": f"实现用户{story['i_want_to']}的核心功能",
            "priority": story["priority"],
            "user_story_ids": [story["id"]],
            "pain_point_ids": story["pain_point_ids"]
        }
        
        features.append(feature)
    
    return features


def generate_openclaw_tasks(features: List[Dict]) -> List[Dict]:
    """Generate OpenClaw development tasks from features"""
    tasks = []
    
    task_templates = [
        ("前端开发", "开发前端界面和交互逻辑"),
        ("后端API", "设计和实现后端API接口"),
        ("数据库设计", "设计数据模型和数据库表结构")
    ]
    
    task_id = 1
    for feature in features[:3]:  # Limit to 3 features for MVP
        for template_name, template_desc in task_templates:
            task = {
                "task_id": f"TASK-{task_id:03d}",
                "title": f"{feature['title']}-{template_name}",
                "description": f"{template_desc}，支持{feature['title']}",
                "priority": feature["priority"],
                "acceptance_criteria": [
                    "代码通过Code Review",
                    "测试覆盖率>80%",
                    "性能指标达标"
                ],
                "feature_id": feature["id"]
            }
            tasks.append(task)
            task_id += 1
    
    return tasks


def search_pain_points(keyword: str, max_results: int = 8) -> Dict[str, Any]:
    """
    Main function to search for pain points and generate PRD
    
    Args:
        keyword: Search keyword
        max_results: Maximum number of results per API
    
    Returns:
        PRD JSON dictionary or error dictionary
    """
    print(f"INFO: Searching for pain points with keyword: '{keyword}'", file=sys.stderr)
    
    # Try to fetch real data from multiple sources
    all_results = []
    
    # Try Brave API (if key available)
    brave_results = search_brave_api(keyword, max_results)
    all_results.extend(brave_results)
    
    # Try Hacker News (always available)
    hn_results = search_hackernews(keyword, max_results)
    all_results.extend(hn_results)
    
    # Check if we got any results
    if not all_results:
        print("ERROR: No API results found", file=sys.stderr)
        return {
            "status": "no_results",
            "keyword": keyword,
            "error": "No API results found. Try providing API keys (BRAVE_API_KEY) or using a different keyword.",
            "suggestions": [
                "Set BRAVE_API_KEY environment variable for broader search",
                "Try a broader or different keyword",
                "Check network connectivity",
                "Hacker News may not have results for non-tech topics"
            ]
        }
    
    # Extract pain points from results
    print(f"INFO: Extracting pain points from {len(all_results)} results", file=sys.stderr)
    pain_points = extract_pain_points(all_results, max_points=5)
    
    # Generate PRD components
    user_stories = generate_user_stories(pain_points)
    mvp_features = generate_mvp_features(user_stories, pain_points)
    openclaw_tasks = generate_openclaw_tasks(mvp_features)
    
    # Determine data source
    data_sources = []
    if brave_results:
        data_sources.append("Brave Search")
    if hn_results:
        data_sources.append("Hacker News")
    
    # Assemble final PRD
    prd = {
        "status": "success",
        "keyword": keyword,
        "project_name": generate_product_name(keyword),
        "summary": f"一站式解决{keyword}相关痛点，提供智能化解决方案",
        "pain_points": pain_points,
        "user_stories": user_stories,
        "mvp_features": mvp_features,
        "openclaw_tasks": openclaw_tasks,
        "generated_at": datetime.now().isoformat(),
        "data_source": ", ".join(data_sources),
        "total_results_found": len(all_results)
    }
    
    print(f"INFO: Successfully generated PRD with {len(pain_points)} pain points", file=sys.stderr)
    return prd


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Search for user pain points and generate PRD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 search.py search-pain-points --keyword "remote work"
  BRAVE_API_KEY=xxx python3 search.py search-pain-points --keyword "AI tools"
  
Environment Variables:
  BRAVE_API_KEY    Brave Search API key (optional but recommended)
  BAIDU_API_KEY    Baidu Search API key (optional, for Chinese content)

Network Requests:
  - api.search.brave.com (Brave Search API)
  - hn.algolia.com (Hacker News Algolia API)
  
Privacy Notice:
  Your search keywords will be sent to external API services.
  Do not include sensitive or confidential information.
        """
    )
    
    parser.add_argument(
        "command",
        choices=["search-pain-points"],
        help="Command to execute"
    )
    parser.add_argument(
        "--keyword",
        required=True,
        help="Keyword to search for pain points"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=8,
        help="Maximum number of results per API (default: 8)"
    )
    
    args = parser.parse_args()
    
    if args.command == "search-pain-points":
        result = search_pain_points(args.keyword, args.max_results)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        error_result = {
            "status": "error",
            "error": f"Unknown command: {args.command}"
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

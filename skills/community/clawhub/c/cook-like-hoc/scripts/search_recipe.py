import sys
import json
import urllib.request
import urllib.parse
from difflib import get_close_matches

import os
import time

TREE_API_URL = "https://api.github.com/repos/Gar-b-age/CookLikeHOC/git/trees/main?recursive=1"
# 使用 jsDelivr 官方 CDN 替换原版 raw.githubusercontent.com 
# 以保障中国大陆等网络较差情况的直连获取速度稳定
RAW_BASE_URL = "https://fastly.jsdelivr.net/gh/Gar-b-age/CookLikeHOC@main/"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "recipe_tree_cache.json")

def fetch_file_list():
    try:
        # Check cache first (valid for 24 hours)
        if os.path.exists(CACHE_FILE):
            if time.time() - os.path.getmtime(CACHE_FILE) < 86400:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
                    
        req = urllib.request.Request(TREE_API_URL)
        req.add_header('User-Agent', 'Mozilla/5.0')
        # Add optional Github token if available in env to increase limits
        if os.environ.get('GITHUB_TOKEN'):
            req.add_header('Authorization', f"token {os.environ.get('GITHUB_TOKEN')}")
            
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        recipes = {}
        for item in data.get('tree', []):
            path = item.get('path', '')
            if path.endswith('.md') and '/' in path and 'README.md' not in path:
                filename = path.split('/')[-1]
                recipe_name = filename.replace('.md', '')
                recipes[recipe_name] = path
                
        # Save to cache
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False)
            
        return recipes
    except Exception as e:
        # If API fails and we have a stale cache, use it anyway
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        print(f"Error fetching recipe list: {e}")
        return {}

def fetch_recipe_content(path):
    url = RAW_BASE_URL + urllib.parse.quote(path)
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching recipe content: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_recipe.py <recipe_name>")
        sys.exit(1)
        
    query = sys.argv[1].strip()
    
    # 1. Fetch available recipes
    recipes = fetch_file_list()
    if not recipes:
        print("Failed to retrieve the recipe database or it is empty.")
        sys.exit(1)
        
    recipe_names = list(recipes.keys())
    
    # 2. Match the query
    if query in recipes:
        best_match = query
    else:
        # Fuzzy match
        matches = get_close_matches(query, recipe_names, n=1, cutoff=0.3)
        if matches:
            best_match = matches[0]
            print(f"[{query}] not found, but found a similar recipe: [{best_match}]\n")
        else:
            print(f"Could not find any recipe matching '{query}'.")
            
            # Print a few examples
            print("Available examples:")
            for i, name in enumerate(recipe_names[:10]):
                print(f" - {name}")
            sys.exit(1)
            
    # 3. Fetch content
    path = recipes[best_match]
    print(f"=== {best_match} ===")
    content = fetch_recipe_content(path)
    print(content)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Supplement Chinese game names from Xiaoheihe (小黑盒) web API.
Uses the public share page endpoint: https://api.xiaoheihe.cn/game/share_game_detail
No API key required - this is a public web endpoint.
"""

import json, subprocess, re, time, sys, os

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cn_names_cache.json")

def get_xhh_cn_name(appid):
    """Get Chinese name from xiaoheihe share page (no auth needed)"""
    try:
        result = subprocess.run(
            ["curl", "-sL", 
             f"https://api.xiaoheihe.cn/game/share_game_detail?appid={appid}&game_type=pc",
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"],
            capture_output=True, text=True, timeout=10
        )
        html = result.stdout
        title_match = re.findall(r'<title>(.*?)</title>', html)
        if title_match:
            cn_name = title_match[0].replace(' - 小黑盒', '').strip()
            return cn_name
    except Exception as e:
        print(f"  ⚠️ Error fetching {appid}: {e}")
    return None

def is_different_cn(cn_name, en_name):
    """Check if the CN name is actually different from EN name"""
    if not cn_name:
        return False
    # Normalize for comparison
    cn_norm = cn_name.lower().replace(' ', '').replace('®', '').replace('™', '')
    en_norm = en_name.lower().replace(' ', '').replace('®', '').replace('™', '')
    return cn_norm != en_norm

def main():
    # Load cache
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    
    # Find games without CN names (where cn == en)
    no_cn = []
    for appid, info in cache.items():
        cn = info.get('cn', '')
        en = info.get('en', '')
        if cn == en or not cn:
            no_cn.append((appid, en))
    
    total = len(no_cn)
    print(f"🎮 小黑盒中文名补充 — 待查: {total} 款\n")
    
    updated = 0
    skipped = 0
    
    for i, (appid, en_name) in enumerate(no_cn, 1):
        cn_name = get_xhh_cn_name(int(appid))
        
        if cn_name and is_different_cn(cn_name, en_name):
            cache[appid]['cn'] = cn_name
            cache[appid]['source'] = 'xiaoheihe'
            updated += 1
            print(f"[{i}/{total}] ✅ {en_name} → {cn_name}")
        else:
            skipped += 1
            print(f"[{i}/{total}] ⏭ {en_name}")
        
        # Rate limit - be polite to xiaoheihe
        time.sleep(0.3)
    
    # Save updated cache
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！Updated: {updated}, Skipped: {skipped}")

if __name__ == "__main__":
    main()

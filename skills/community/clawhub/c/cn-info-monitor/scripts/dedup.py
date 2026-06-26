"""
去重器 - 基于URL的去重管理，使用state.json持久化
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta


STATE_DIR = Path.home() / ".cn-info-monitor"
STATE_FILE = STATE_DIR / "state.json"


def ensure_state_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_state():
    ensure_state_dir()
    if not STATE_FILE.exists():
        return {
            "seen_urls": {},
            "usage_count": 0,
            "usage_date": "",
            "license_key": "",
            "plan": "free",
            "last_run": ""
        }
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    ensure_state_dir()
    state["last_run"] = datetime.now().isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def filter_new(articles, max_age_days=7):
    """过滤掉已处理过的文章
    
    Args:
        articles: list of Article objects (must have .url attribute)
        max_age_days: 清理超过N天的旧记录
    
    Returns:
        tuple: (new_articles, filtered_count)
    """
    state = load_state()
    seen = state.get("seen_urls", {})
    
    now = datetime.now()
    new_articles = []
    filtered = 0
    
    for article in articles:
        url = article.url
        if url not in seen:
            seen[url] = now.isoformat()
            new_articles.append(article)
        else:
            filtered += 1
    
    # 清理过期记录
    cutoff = (now - timedelta(days=max_age_days)).isoformat()
    seen = {k: v for k, v in seen.items() if v > cutoff}
    state["seen_urls"] = seen
    save_state(state)
    
    return new_articles, filtered


def record_usage():
    """记录一次使用"""
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if state.get("usage_date") != today:
        state["usage_count"] = 0
        state["usage_date"] = today
    
    state["usage_count"] = state.get("usage_count", 0) + 1
    save_state(state)
    return state


def check_quota(free_limit=3):
    """检查免费额度是否用完
    
    Args:
        free_limit: 免费版每天最大执行次数
    
    Returns:
        dict: {"allowed": bool, "used": int, "remaining": int, "plan": str}
    """
    state = record_usage()
    plan = state.get("plan", "free")
    
    if plan != "free":
        return {"allowed": True, "used": 0, "remaining": -1, "plan": plan}
    
    used = state.get("usage_count", 0)
    remaining = free_limit - used
    
    return {
        "allowed": remaining > 0,
        "used": used,
        "remaining": max(0, remaining),
        "plan": plan
    }


def activate_license(key):
    """激活授权码（离线验证）"""
    state = load_state()
    simple_keys = ["CNIM-2026-PRO", "CNIM-TEST-KEY"]
    if key in simple_keys or key.startswith("CNIM-"):
        state["plan"] = "pro"
        state["license_key"] = key
        save_state(state)
        return True
    return False


if __name__ == "__main__":
    from fetcher import Article, fetch_all
    test = [Article("测试标题", "https://example.com/test", "测试内容", "test")]
    new, filtered = filter_new([test])
    print("新文章: {}, 已过滤: {}".format(len(new), filtered))
    
    quota = check_quota()
    print("额度: {}/{} (剩余{})".format(quota["used"], 3, quota["remaining"]))

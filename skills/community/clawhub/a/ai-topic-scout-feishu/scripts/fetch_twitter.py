#!/usr/bin/env python3
"""
AI Topic Scout - Twitter 内容抓取工具
使用 nitter 公开接口抓取推文（无需 API key）
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
import re

def fetch_twitter_tweets(username: str, days: int = 7, max_items: int = 20):
    """
    抓取 Twitter 用户最新推文
    
    Args:
        username: Twitter 用户名 (不含 @)
        days: 抓取最近 N 天的推文
        max_items: 最多抓取数量
    
    Returns:
        List of tweet dicts with: text, url, likes, retweets, replies, published_date
    """
    
    # 使用 nitter.net 镜像站
    nitter_instances = [
        "nitter.net",
        "nitter.poast.org",
        "nitter.privacydev.net"
    ]
    
    tweets = []
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for instance in nitter_instances:
        try:
            url = f"https://{instance}/{username}"
            
            # 使用 curl 抓取 HTML
            result = subprocess.run(
                ["curl", "-sL", "-A", "Mozilla/5.0", url],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            html = result.stdout
            
            # 简单的 HTML 解析（生产环境建议用 BeautifulSoup）
            # 匹配推文块
            tweet_pattern = r'<div class="tweet-content.*?>(.*?)</div>.*?<span class="tweet-date">.*?title="(.*?)".*?<div class="tweet-stats">.*?<span class="icon-comment.*?</span>(.*?)</span>.*?<span class="icon-retweet.*?</span>(.*?)</span>.*?<span class="icon-heart.*?</span>(.*?)</span>'
            
            matches = re.finditer(tweet_pattern, html, re.DOTALL)
            
            for match in matches:
                if len(tweets) >= max_items:
                    break
                
                text = match.group(1)
                date_str = match.group(2)
                replies = match.group(3).strip()
                retweets = match.group(4).strip()
                likes = match.group(5).strip()
                
                # 清理 HTML 标签
                text = re.sub(r'<[^>]+>', '', text).strip()
                
                # 解析日期
                try:
                    pub_date = datetime.strptime(date_str, "%b %d, %Y · %I:%M %p %Z")
                    if pub_date < cutoff_date:
                        continue
                except:
                    pub_date = datetime.now()
                
                tweets.append({
                    "text": text,
                    "url": f"https://twitter.com/{username}/status/...",  # 需要进一步解析
                    "likes": int(likes.replace(",", "")) if likes.isdigit() or likes.replace(",", "").isdigit() else 0,
                    "retweets": int(retweets.replace(",", "")) if retweets.isdigit() or retweets.replace(",", "").isdigit() else 0,
                    "replies": int(replies.replace(",", "")) if replies.isdigit() or replies.replace(",", "").isdigit() else 0,
                    "published_date": pub_date.strftime("%Y-%m-%d")
                })
            
            if tweets:
                break  # 成功获取，退出循环
        
        except subprocess.TimeoutExpired:
            continue
        except subprocess.CalledProcessError:
            continue
        except Exception as e:
            print(f"Error with {instance}: {e}", file=sys.stderr)
            continue
    
    return tweets

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fetch_twitter.py <username> [days] [max_items]")
        sys.exit(1)
    
    username = sys.argv[1].lstrip("@")
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    max_items = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    
    tweets = fetch_twitter_tweets(username, days, max_items)
    print(json.dumps(tweets, ensure_ascii=False, indent=2))

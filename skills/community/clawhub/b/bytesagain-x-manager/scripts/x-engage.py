#!/usr/bin/env python3
"""
x-engage.py — X 自动互动
功能:
  1. 自动点赞 AI/skill 相关推文
  2. 监控 @bytesagain 提及，拟好回复发 Telegram 给 Kelly 确认
  3. Kelly 回复"发"后，实际发出回复

用法:
  python3 x-engage.py --like       # 自动点赞
  python3 x-engage.py --monitor    # 监控提及，发 Telegram 待确认
  python3 x-engage.py --send <tweet_id> <reply_text>  # 实际发回复（Kelly确认后触发）
"""
import os, sys, json, requests, argparse
from datetime import datetime, timezone
from requests_oauthlib import OAuth1

TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT  = os.environ.get("TG_CHAT", "")
PENDING_FILE = os.path.expanduser("~/.local/share/x-manager/pending-replies.json")
os.makedirs(os.path.dirname(PENDING_FILE), exist_ok=True)

# ── 初始化 ──────────────────────────────────────────────────────────────────
def load_env():
    pass  # All credentials must be set as environment variables

def get_auth():
    return OAuth1(
        os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"]
    )

def tg_send(msg):
    try:
        payload = {"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown"}
        req_data = json.dumps(payload).encode()
        import urllib.request
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            data=req_data,
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"TG发送失败: {e}")

# ── 1. 自动点赞 ──────────────────────────────────────────────────────────────
LIKE_KEYWORDS = [
    "AI agent skills", "agent skill", "SKILL.md",
    "clawhub", "openclaw", "AI automation skill",
    "AI agent workflow", "agentic AI"
]
LIKED_FILE = "/tmp/x-liked-ids.json"

def load_liked():
    try:
        return set(json.load(open(LIKED_FILE)))
    except:
        return set()

def save_liked(liked_set):
    with open(LIKED_FILE, "w") as f:
        json.dump(list(liked_set)[-500:], f)  # 只保留最近500条

def run_like():
    auth = get_auth()
    liked = load_liked()
    total_liked = 0
    skipped = 0

    for kw in LIKE_KEYWORDS[:4]:  # 每次搜4个关键词，控制API消耗
        try:
            resp = requests.get(
                "https://api.twitter.com/2/tweets/search/recent",
                auth=auth,
                params={
                    "query": f'"{kw}" -is:retweet lang:en',
                    "max_results": 10,
                    "tweet.fields": "author_id,public_metrics,created_at"
                },
                timeout=15
            )
            if resp.status_code != 200:
                print(f"搜索失败 [{kw}]: {resp.status_code}")
                continue

            tweets = resp.json().get("data", [])
            for tweet in tweets:
                tid = tweet["id"]
                if tid in liked:
                    skipped += 1
                    continue
                # 过滤：不点赞自己的推文
                if tweet.get("author_id") == os.environ.get("X_USER_ID", ""):
                    continue
                # 过滤：互动太低的（可能是垃圾）
                metrics = tweet.get("public_metrics", {})
                if metrics.get("like_count", 0) < 1 and metrics.get("retweet_count", 0) < 1:
                    continue

                like_resp = requests.post(
                    f"https://api.twitter.com/2/users/{os.environ.get('X_USER_ID', '')}/likes",
                    auth=auth,
                    json={"tweet_id": tid},
                    timeout=10
                )
                if like_resp.status_code == 200:
                    liked.add(tid)
                    total_liked += 1
                    print(f"✅ 点赞: {tid} [{kw}]")
                else:
                    print(f"点赞失败: {like_resp.status_code} {like_resp.text[:100]}")

        except Exception as e:
            print(f"关键词 [{kw}] 处理失败: {e}")

    save_liked(liked)
    print(f"\n点赞完成: +{total_liked} 新点赞，{skipped} 跳过（已点过）")
    return total_liked

# ── 2. 监控提及，发 Telegram 待确认 ─────────────────────────────────────────
SEEN_FILE = "/tmp/x-seen-mentions.json"

def load_seen():
    try:
        return set(json.load(open(SEEN_FILE)))
    except:
        return set()

def save_seen(seen_set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_set)[-200:], f)

def is_worth_replying(tweet_text, author_metrics):
    """判断是否值得回复"""
    text_lower = tweet_text.lower()
    # 垃圾/spam 特征
    spam_signals = ['follow back', 'giveaway', 'airdrop', 'free crypto', 'dm me']
    if any(s in text_lower for s in spam_signals):
        return False, "疑似spam"
    # 粉丝太少的跳过
    if author_metrics.get("followers_count", 0) < 10:
        return False, "粉丝数<10"
    return True, "正常互动"

def draft_reply(mention_text, author_name, xai_key):
    """用 xAI 生成回复草稿"""
    try:
        payload = {
            "model": "grok-3-mini",
            "messages": [
                {"role": "system", "content": (
                    "You are @bytesagain, an AI agent skills platform. "
                    "Write a short, friendly reply (max 200 chars) to this mention. "
                    "Be genuine, helpful, not salesy. No hashtags. No links."
                )},
                {"role": "user", "content": f"@{author_name} said: {mention_text}"}
            ],
            "max_tokens": 100
        }
        import urllib.request
        req = urllib.request.Request(
            "https://api.x.ai/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {xai_key}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Thanks for the mention, @{author_name}! 🙌"

def run_monitor():
    auth = get_auth()
    xai_key = os.environ.get("XAI_API_KEY", "")
    seen = load_seen()

    # 搜索最近提及 @bytesagain 的推文
    resp = requests.get(
        "https://api.twitter.com/2/tweets/search/recent",
        auth=auth,
        params={
            "query": "@bytesagain -from:bytesagain -is:retweet",
            "max_results": 20,
            "tweet.fields": "author_id,created_at,text,conversation_id",
            "expansions": "author_id",
            "user.fields": "name,username,public_metrics"
        },
        timeout=15
    )

    if resp.status_code != 200:
        print(f"监控失败: {resp.status_code} {resp.text[:200]}")
        return

    data = resp.json()
    tweets = data.get("data", [])
    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}

    new_mentions = 0
    pending = []

    for tweet in tweets:
        tid = tweet["id"]
        if tid in seen:
            continue

        author = users.get(tweet["author_id"], {})
        author_name = author.get("username", "unknown")
        metrics = author.get("public_metrics", {})

        worth, reason = is_worth_replying(tweet["text"], metrics)
        seen.add(tid)

        if not worth:
            print(f"跳过 @{author_name}: {reason}")
            continue

        # 生成回复草稿
        draft = draft_reply(tweet["text"], author_name, xai_key)
        new_mentions += 1

        pending.append({
            "tweet_id": tid,
            "author": author_name,
            "followers": metrics.get("followers_count", 0),
            "original": tweet["text"],
            "draft_reply": f"@{author_name} {draft}",
            "timestamp": tweet.get("created_at", "")
        })

    save_seen(seen)

    if not pending:
        print(f"无新提及（已检查 {len(tweets)} 条）")
        return

    # 保存待确认队列
    existing = []
    try:
        existing = json.load(open(PENDING_FILE))
    except:
        pass
    existing.extend(pending)
    with open(PENDING_FILE, "w") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    # 发 Telegram 通知 Kelly 确认
    for p in pending:
        msg = (
            f"📨 *新提及需确认回复*\n\n"
            f"👤 @{p['author']} ({p['followers']:,} 粉丝)\n"
            f"📝 原文: {p['original'][:200]}\n\n"
            f"💬 *拟回复:*\n`{p['draft_reply']}`\n\n"
            f"回复【发 {p['tweet_id']}】确认发出\n"
            f"回复【跳过 {p['tweet_id']}】忽略"
        )
        tg_send(msg)

    print(f"✅ {new_mentions} 条新提及已发 Telegram 待确认")

# ── 3. 实际发出回复（Kelly确认后） ────────────────────────────────────────────
def run_send(tweet_id, reply_text=None, delay=0):
    import time
    if delay > 0:
        print(f"⏳ 等待 {delay}s...")
        time.sleep(delay)
    auth = get_auth()

    # 从待确认队列找回复内容
    if not reply_text:
        try:
            pending = json.load(open(PENDING_FILE))
            for p in pending:
                if p["tweet_id"] == tweet_id:
                    reply_text = p["draft_reply"]
                    break
        except:
            pass

    if not reply_text:
        print(f"找不到 {tweet_id} 的回复内容")
        return

    resp = requests.post(
        "https://api.twitter.com/2/tweets",
        auth=auth,
        json={
            "text": reply_text,
            "reply": {"in_reply_to_tweet_id": tweet_id}
        },
        timeout=15
    )

    if resp.status_code == 201:
        tid = resp.json()["data"]["id"]
        print(f"✅ 已回复: https://x.com/bytesagain/status/{tid}")
        tg_send(f"✅ *回复已发出*\nhttps://x.com/bytesagain/status/{tid}\n\n内容: {reply_text}")
        # 从待确认队列移除
        try:
            pending = json.load(open(PENDING_FILE))
            pending = [p for p in pending if p["tweet_id"] != tweet_id]
            json.dump(pending, open(PENDING_FILE, "w"), ensure_ascii=False)
        except:
            pass
    else:
        print(f"❌ 发送失败: {resp.status_code} {resp.text}")

# ── 主程序 ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--like", action="store_true", help="自动点赞")
    parser.add_argument("--monitor", action="store_true", help="监控提及，发Telegram待确认")
    parser.add_argument("--send", metavar="TWEET_ID", nargs="+", help="发出确认的回复（支持多个id）")
    parser.add_argument("--reply-text", help="回复内容（可选，不填则用草稿）")
    parser.add_argument("--no-tg", action="store_true")
    args = parser.parse_args()

    load_env()

    if args.like:
        run_like()
    elif args.monitor:
        run_monitor()
    elif args.send:
        import random, time
        ids = args.send
        for i, tid in enumerate(ids):
            delay = random.randint(30, 90) if i > 0 else 0  # 第一条不延迟，后续每条闰30-90秒
            run_send(tid, args.reply_text, delay=delay)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

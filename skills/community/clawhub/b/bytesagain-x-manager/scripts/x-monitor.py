#!/usr/bin/env python3
"""
x-monitor.py — X (Twitter) 热点监控 + 宣传草稿生成
功能:
  1. 搜索 AI agent skills 热点话题
  2. 监控 BytesAgain 品牌提及 + 竞品动态
  3. 追踪 @openclaw 账号最新帖子 + 评论反馈分析
  4. 生成推文草稿供 Kelly 手动发布
  5. 发 Telegram 汇报

用法:
  python3 x-monitor.py              # 完整运行
  python3 x-monitor.py --draft-only # 只生成推文草稿
  python3 x-monitor.py --monitor-only # 只做品牌监控
  python3 x-monitor.py --openclaw-only # 只追踪 openclaw
"""
import urllib.request, json, os, sys, argparse
from datetime import datetime

# ── 配置 ─────────────────────────────────────────────────────────────────────
TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT  = os.environ.get("TG_CHAT", "")
XAI_MODEL = "grok-4"
XAI_URL   = "https://api.x.ai/v1/responses"

def load_env():
    pass  # All credentials must be set as environment variables

def xai_search(prompt):
    """调用 xAI Responses API 搜索 X"""
    key = os.environ.get("XAI_API_KEY", "")
    payload = {
        "model": XAI_MODEL,
        "input": prompt,
        "tools": [{"type": "x_search"}]
    }
    req = urllib.request.Request(
        XAI_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read())
    text = ""
    for item in result.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text += c["text"]
    usage = result.get("usage", {})
    tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
    return text, tokens

def translate_to_cn(text):
    """将英文内容翻译成中文，失败则返回原文"""
    key = os.environ.get("XAI_API_KEY", "")
    if not key:
        return ""
    # 只翻译英文段落（超过30%英文字符才翻译）
    en_chars = sum(1 for c in text if ord('a') <= ord(c.lower()) <= ord('z'))
    if len(text) == 0 or en_chars / len(text) < 0.3:
        return ""  # 主要是中文，不需要翻译
    try:
        payload = {
            "model": "grok-3-mini",
            "messages": [
                {"role": "system", "content": "你是翻译助手。将以下英文内容翻译成简洁的中文摘要，保留关键信息，去掉引用编号如[1][2]。"},
                {"role": "user", "content": text[:2000]}
            ],
            "max_tokens": 800
        }
        req = urllib.request.Request(
            "https://api.x.ai/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return ""

def tg_send(msg):
    payload = {"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown"}
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=10)

# ── 1. 热点监控 ───────────────────────────────────────────────────────────────
def run_monitor():
    print("🔍 搜索品牌提及 + 竞品动态...")
    text, tokens = xai_search(
        "Search X for TODAY's posts about: "
        "1) 'BytesAgain' OR 'bytesagain.com' "
        "2) 'ClawHub' OR 'clawhub.ai' OR 'OpenClaw' "
        "3) 'SKILL.md' OR 'AI agent skills marketplace'. "
        "For each result show: username, post time, key content (1-2 sentences). "
        "Separate results by category. Max 3 posts per category."
    )
    print(f"  → {tokens} tokens")
    return text, tokens

# ── 2. 热点选题 ───────────────────────────────────────────────────────────────
def run_trends():
    print("📈 获取 AI agent 热点话题...")
    text, tokens = xai_search(
        "Search X for the TOP 5 trending topics about AI agents or AI skills posted TODAY. "
        "For each topic: "
        "1. Topic name (2-4 words) "
        "2. Why it's trending (1 sentence) "
        "3. Best angle for a blog article about bytesagain.com (1 sentence) "
        "Format as numbered list. Focus on practical AI tools, not hype."
    )
    print(f"  → {tokens} tokens")
    return text, tokens

# ── 3. 推文草稿生成 ───────────────────────────────────────────────────────────
def run_drafts(trends_text):
    print("✍️  生成推文草稿...")
    # 固定可用的真实页面
    REAL_PAGES = (
        "ONLY use these real pages for 'Reply with' — do NOT invent URLs:\n"
        "  bytesagain.com/skills  (browse all AI agent skills)\n"
        "  bytesagain.com/use-case  (use cases by role)\n"
        "  bytesagain.com/install  (install bytesagain skill)\n"
        "  bytesagain.com  (homepage)\n"
        "Pick the most relevant one. If unsure, use bytesagain.com/skills\n\n"
    )
    text, tokens = xai_search(
        f"Based on these trending topics on X today:\n{trends_text[:800]}\n\n"
        "Write 3 tweet drafts for @bytesagain (bytesagain.com - AI agent skills discovery site). "
        "STRICT Rules (based on 2026 X algorithm): "
        "- Each tweet max 280 chars, NO external links in the main tweet body "
        "- Links MUST go in a separate reply (show as 'Reply with: <link>') "
        "- Max 1-2 hashtags per tweet (more than 2 = 40% penalty) "
        "- Tone: helpful, knowledgeable, not salesy "
        "- Pure text performs 30% better than media on X "
        "- Reference the trending topic naturally "
        "- End with a question or call to discuss to trigger replies "
        + REAL_PAGES +
        "Format for each: "
        "Tweet N: <tweet text (no link)> "
        "Reply with: <one of the real pages above>"
    )
    print(f"  → {tokens} tokens")
    return text, tokens

# ── 4. @openclaw 账号追踪 ─────────────────────────────────────────────────────
def run_openclaw_tracker():
    print("🔭 追踪 @openclaw 最新帖子 + 评论反馈...")
    text, tokens = xai_search(
        "Search X for posts from @openclaw today. "
        "Show me their latest 3 posts: full text, time, likes/replies count. "
        "For each post, summarize the top 2 replies from other users. "
        "What topics are they pushing today? Any notable community reactions?"
    )
    print(f"  → {tokens} tokens")
    return text, tokens

FALLBACK_TWEETS = [
    "Most people use AI as a search engine. Power users use it as an agent that takes action.\n\nWhat's the biggest difference you've noticed? 👇 #AIagents",
    "The best AI skill isn't the most powerful one — it's the one that fits your exact workflow.\n\nWhat's your most-used AI tool right now?",
    "AI agent skills are like apps — but they run inside your AI assistant instead of your phone.\n\nWhich task would you automate first if you could? 🤖",
    "Most productivity advice ignores AI entirely. Most AI advice ignores actual productivity.\n\nWhat's the gap you wish someone would fill? 👇",
    "The future of work isn't AI replacing humans — it's humans who use AI agents replacing those who don't.\n\nAre you building your AI toolkit? 🧰",
]

import random as _random
_fallback_index = [0]

def get_fallback_tweet():
    tweet = FALLBACK_TWEETS[_fallback_index[0] % len(FALLBACK_TWEETS)]
    _fallback_index[0] += 1
    return tweet

# ── 6. 发推前校验 ────────────────────────────────────────────────────────────
def validate_tweet(text):
    """
    发推前检查，返回 (passed, reasons)
    passed=True 才允许发推
    """
    import re
    issues = []
    warnings = []

    # 1. 长度检查
    if len(text) > 280:
        issues.append(f"超长 {len(text)} 字符（最多280）")

    # 2. 链接不能在正文（X算法降权）
    if re.search(r'https?://', text):
        issues.append("正文含链接（X算法降权40%，链接应放Reply中）")

    # 3. hashtag 不超过2个
    tags = re.findall(r'#\w+', text)
    if len(tags) > 2:
        issues.append(f"hashtag过多：{len(tags)}个（最多2个）")

    # 4. 数字检查 - 不能出现我们不确定的具体数字
    # 允许的数字：不含任何数字，或只含模糊表达
    suspicious_numbers = re.findall(r'\b(\d{4,}|\d+[KkMm]\+?)\b', text)
    if suspicious_numbers:
        issues.append(f"含具体数字 {suspicious_numbers}（可能不准确，请用模糊表达如 'thousands of' / 'hundreds'）")

    # 5. 不允许的词汇
    banned = ['guaranteed', 'make money', 'get rich', 'free money', '100%']
    for b in banned:
        if b.lower() in text.lower():
            issues.append(f"含违规词: '{b}'")

    # 6. 空内容
    if not text.strip():
        issues.append("推文内容为空")

    # 7. 警告项（不阻止发推，但记录）
    if '?' not in text and '？' not in text:
        warnings.append("建议加问句（提高互动率）")
    if len(text) < 50:
        warnings.append("推文过短（建议100字符以上）")

    passed = len(issues) == 0
    return passed, issues, warnings


def post_tweet(text):
    """用 OAuth 1.0a 发推，返回 (success, tweet_id or error)"""
    try:
        from requests_oauthlib import OAuth1
        import requests as req_lib
        auth = OAuth1(
            os.environ.get("X_API_KEY", ""),
            os.environ.get("X_API_SECRET", ""),
            os.environ.get("X_ACCESS_TOKEN", ""),
            os.environ.get("X_ACCESS_TOKEN_SECRET", "")
        )
        resp = req_lib.post(
            "https://api.twitter.com/2/tweets",
            auth=auth,
            json={"text": text},
            timeout=15
        )
        data = resp.json()
        if resp.status_code == 201:
            return True, data["data"]["id"]
        else:
            return False, str(data)
    except Exception as e:
        return False, str(e)

def extract_tweets_from_drafts(drafts_text):
    """从草稿文本里提取推文正文（不含 Reply with 部分）"""
    import re
    tweets = []
    for m in re.finditer(r'Tweet \d+:\s*(.+?)(?=\nReply with:|\nTweet \d+:|$)', drafts_text, re.DOTALL):
        tweet = m.group(1).strip()
        # 清理多余空行
        tweet = re.sub(r'\n{2,}', '\n', tweet).strip()
        if tweet and len(tweet) <= 280:
            tweets.append(tweet)
    return tweets

# ── 主程序 ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft-only", action="store_true")
    parser.add_argument("--monitor-only", action="store_true")
    parser.add_argument("--openclaw-only", action="store_true")
    parser.add_argument("--auto-post", action="store_true", help="自动发推（读取草稿文件，按时段发第1/2/3条）")
    parser.add_argument("--post-index", type=int, default=0, help="发第几条草稿（0=第1条，1=第2条，2=第3条）")
    parser.add_argument("--no-tg", action="store_true", help="不发 Telegram")
    args = parser.parse_args()

    load_env()
    total_tokens = 0
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = [f"🐦 *X Monitor Report* — {today}\n"]

    # @openclaw 追踪（每次都跑，除非 draft-only）
    if not args.draft_only:
        try:
            openclaw_text, t = run_openclaw_tracker()
            total_tokens += t
            report.append("*🔭 @openclaw 动态追踪*")
            report.append(openclaw_text[:1500])
        except Exception as e:
            report.append(f"OpenClaw追踪失败: {e}")

    # 品牌监控
    if not args.draft_only and not args.openclaw_only:
        try:
            monitor_text, t = run_monitor()
            total_tokens += t
            report.append("\n*📡 品牌 & 竞品监控*")
            report.append(monitor_text[:1200])
        except Exception as e:
            report.append(f"监控失败: {e}")

    DRAFT_FILE = f"/tmp/x-drafts-{datetime.now().strftime('%Y-%m-%d')}.json"

    # ── auto-post 模式：直接读草稿文件发推，不调xAI ──
    if args.auto_post:
        report[0] = f"🚀 *X Auto Post* — {today}\n"
        try:
            import json as _json
            if os.path.exists(DRAFT_FILE):
                with open(DRAFT_FILE) as f:
                    saved = _json.load(f)
                tweets = saved.get("tweets", [])
                idx = args.post_index
                if idx < len(tweets):
                    tweet = tweets[idx]
                    source = f"草稿第{idx+1}条"
                else:
                    tweet = get_fallback_tweet()
                    source = "预设模板（草稿不足）"
            else:
                tweet = get_fallback_tweet()
                source = "预设模板（无草稿文件）"

            # 发推前校验
            passed, issues, warnings = validate_tweet(tweet)
            if not passed:
                report.append(f"❌ 校验未通过，未发推：")
                for issue in issues:
                    report.append(f"  • {issue}")
                report.append(f"\n原始内容: {tweet}")
            else:
                if warnings:
                    report.append("⚠️ 警告: " + " | ".join(warnings))
                ok, result = post_tweet(tweet)
                if ok:
                    report.append(f"✅ 已发推（{source}）")
                    report.append(f"https://x.com/bytesagain/status/{result}")
                    report.append(f"\n内容: {tweet}")
                else:
                    report.append(f"❌ 发推失败: {result}")
        except Exception as e:
            report.append(f"❌ 异常: {e}")

        full_report = "\n".join(report)
        print("\n" + "="*50)
        print(full_report)
        if not args.no_tg:
            tg_send(full_report[:3500])
        return

    # ── 正常模式：监控 + 生成草稿 ──
    # 热点 + 草稿
    if not args.monitor_only and not args.openclaw_only:
        try:
            trends_text, t = run_trends()
            total_tokens += t
            report.append("\n*📈 今日热点话题*")
            report.append(trends_text[:800])

            drafts_text, t = run_drafts(trends_text)
            total_tokens += t

            # 解析并存储草稿
            import json as _json
            tweets_list = extract_tweets_from_drafts(drafts_text)
            if tweets_list:
                with open(DRAFT_FILE, 'w') as f:
                    _json.dump({"tweets": tweets_list, "generated": today}, f, ensure_ascii=False)
                print(f"✅ 已存储3条草稿到 {DRAFT_FILE}")

            # 自动 audit 每条草稿
            audit_lines = []
            for line in drafts_text.split('\n'):
                stripped = line.strip()
                if stripped.startswith('Tweet') and ':' in stripped:
                    tweet_text = stripped.split(':', 1)[1].strip()
                    if tweet_text:
                        score = 100
                        flags = []
                        import re
                        if re.search(r'https?://', tweet_text):
                            score -= 40; flags.append('链接在正文(-40)')
                        tag_count = len(re.findall(r'#\w+', tweet_text))
                        if tag_count > 2:
                            score -= 20; flags.append(f'hashtag{tag_count}个(-20)')
                        if len(tweet_text) > 280:
                            score -= 30; flags.append(f'{len(tweet_text)}字(-30)')
                        if '?' not in tweet_text and '？' not in tweet_text:
                            flags.append('建议加问句')
                        flag_str = ' | '.join(flags) if flags else '✅ 合规'
                        audit_lines.append(f"  [{score}分] {flag_str}")

            report.append(f"\n*✍️  推文草稿（将于 10:05/15:05/20:05 自动发布）*")
            report.append(drafts_text[:1000])
            if audit_lines:
                report.append("\n*📊 算法评分*")
                report.extend(audit_lines)
        except Exception as e:
            report.append(f"热点/草稿失败: {e}")

    report.append(f"\n💰 总用量: {total_tokens:,} tokens (~${total_tokens/1000000*15:.3f})")

    full_report = "\n".join(report)
    print("\n" + "="*50)
    print(full_report)

    if not args.no_tg:
        # 尝试翻译英文内容
        cn_translation = translate_to_cn(full_report)
        if cn_translation:
            send_text = full_report + "\n\n" + "—" * 20 + "\n🇨🇳 *中文摘要*\n" + cn_translation
        else:
            send_text = full_report
        # Telegram 限制 4096 字符，分段发
        chunks = [send_text[i:i+3500] for i in range(0, len(send_text), 3500)]
        for chunk in chunks:
            tg_send(chunk)
        print("\n✅ Telegram 已发送")

if __name__ == "__main__":
    main()

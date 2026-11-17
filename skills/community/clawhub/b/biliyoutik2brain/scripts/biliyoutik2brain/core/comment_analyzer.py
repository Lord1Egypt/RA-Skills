"""
BiliYouTik2Brain — 评论语义分析引擎

语义级评论分析，解决：
1. 联系对话上下文的互动链分析（不能只看单条评论）
2. UP主/楼主评论和回复的特别关注
3. 营销推广/互喷/恶意评论的剔除
4. LLM 驱动的语义理解
"""

from typing import List, Dict, Optional, Any
import re, json

from .schemas import CommentResult


# ══════════════════════════════════════════════════════════
# 垃圾评论检测（规则层，降低LLM调用量）
# ══════════════════════════════════════════════════════════

# 营销推广模式
SPAM_PATTERNS = [
    # 推广链接
    r'(?:加|添加|联系)(?:微|v|V|微信|QQ|威|🛰)\s*[:：]?\s*[a-zA-Z0-9_@]+',
    r'(?:私信|私聊|点头像|点主页)\s*(?:领|看|发|获取|拿)',
    r'[vV信wxWX]{2,}[\s:：]*[a-zA-Z0-9]{4,}',
    r'(?:扫码|扫二维码|二维码|扫一扫)',
    r'(?:https?|htp)[:：]\/\/[^\s，。！；,\.]+',
    r'(?:tg|telegram|飞机|纸飞机|油管)[\s:：]*[a-zA-Z0-9_@]+',
    r'(?:看主页|关注我|点关注|主页有|简介有|签名有)',
    # 硬广话术
    r'(?:精准|免费|限时|秒杀).{0,5}(?:名额|领取|赠送|福利)',
    r'(?:小白|新手|零基础).{0,5}(?:月入|日赚|日入|月赚|年入)[0-9\u4e00-\u9fff]+',
    r'(?:稳定收益|稳赚|保证盈利|包赚|包赔)',
    r'(?:Q群|裙号|群号|Q群号|社群)[\s:：]*[0-9]{5,}',
    r'(?:关注|关注我).{0,10}(?:看公告|看置顶|看个人主页)',
]

# 互喷模式
FLAME_PATTERNS = [
    r'(?:你.*?(?:懂|会|能|配|算|行|有|是)).{0,10}(?:个|个.*?[屁jb蛋]|尼玛|毛线)',
    r'(?:垃圾|废物|弱智|SB|傻逼|煞笔|脑残|智障|2B|二逼)',
    r'(?:滚蛋|滚粗|爬|去死|吃屎|si全家|死全家)',
    r'(?:菜鸡|菜逼|菜狗|小学生|低能)',
    r'(?:喷子|杠精|键盘侠|水军)',
    r'(?:你.{0,3}(?:媽|妈|娘|大爷|祖宗))',
    r'(?:笑死|笑喷|呵呵.{0,5}垃圾|就这.{0,5}水平)',
]

# 恶意评论模式
MALICIOUS_PATTERNS = [
    r'(?:举报|投诉|律师函|起诉|报警)',
    r'(?:人肉|开盒|曝光.{0,5}信息|扒皮|挂人)',
    r'(?:刷赞|刷粉|刷量|刷数据|买粉)',
    r'(?:传销|庞氏|割韭菜|杀猪盘)',
]


def _detect_spam(content: str) -> Optional[str]:
    """
    检测评论是否为垃圾/营销/互喷/恶意

    Returns:
        "spam" | "flame" | "malicious" | None
    """
    for pat in SPAM_PATTERNS:
        if re.search(pat, content):
            return "spam"
    for pat in FLAME_PATTERNS:
        if re.search(pat, content):
            return "flame"
    for pat in MALICIOUS_PATTERNS:
        if re.search(pat, content):
            return "malicious"
    return None


def _is_probably_short_spam(content: str) -> bool:
    """极短评论（<10字）如果完全由emoji/标点/重复词构成，视为spam"""
    stripped = re.sub(r'[\U0001F000-\U0010FFFF\u2000-\u206F\u3000-\u303F\s]', '', content)
    if len(stripped) < 3:
        return True
    # 纯重复（如"好好好好好好"）
    if len(set(stripped)) <= 2 and len(stripped) >= 5:
        return True
    return False


# ══════════════════════════════════════════════════════════
# 评论交互树构建
# ══════════════════════════════════════════════════════════

def _extract_threads(comments: List[Dict],
                     up_author_id: str = "") -> Dict:
    """
    将扁平评论列表组织为互动树

    Args:
        comments: 评论列表（含reply_to等字段）
        up_author_id: UP主用户ID

    Returns:
        {threads: [{root, replies[], interaction_score, has_up_reply}],
         up_author_comments: [{content, reply_to, likes, time, ...}],
         orphan_replies: []  # 找不到父评论的回复}
    """
    # 区分根评论和回复
    roots = []
    reply_map: Dict[str, List] = {}  # parent_id → [comments]
    up_replies = []  # UP主发出的回复

    for c in comments:
        parent_id = c.get("reply_to", "") or c.get("parent_id", "")
        author_id = c.get("author_id", "")
        author = c.get("author", "")

        if not parent_id:
            roots.append(c)
        else:
            reply_map.setdefault(parent_id, []).append(c)

        # 标记UP主发言
        if author_id and up_author_id and author_id == up_author_id:
            up_replies.append(c)
        elif author and "up" in author.lower():
            up_replies.append(c)

    # 构建互动树 + 收集UP主所有发言
    threads = []
    up_author_comments = []
    orphan_replies = []

    # UP主的所有发言（主贴+回复）
    seen_up_ids = set()

    for root in roots:
        author_id = root.get("author_id", "")
        author = root.get("author", "")
        root_id = root.get("id", "") or root.get("comment_id", "")

        # UP主自己发的根评论
        if (author_id and up_author_id and author_id == up_author_id) or \
           (author and "up" in author.lower()):
            if root_id and root_id not in seen_up_ids:
                up_author_comments.append({**root, "_type": "root"})
                seen_up_ids.add(root_id)

        # 找子回复
        replies = reply_map.pop(root_id, [])
        has_up_reply = False
        for r in replies:
            r_author = r.get("author_id", "")
            r_author_name = r.get("author", "")
            if (r_author and up_author_id and r_author == up_author_id) or \
               (r_author_name and "up" in r_author_name.lower()):
                up_author_comments.append({**r, "_type": "reply_to_comment"})
                has_up_reply = True
                seen_up_ids.add(r.get("id", "") or r.get("comment_id", ""))

        # 互动得分 = 点赞 + 回复数*2 + 子回复点赞*0.5
        interaction_score = root.get("likes", 0) + root.get("reply_count", 0) * 2
        interaction_score += sum(
            sr.get("likes", 0) * 0.5 for sr in replies
        )
        if has_up_reply:
            interaction_score *= 1.5  # UP主参与的互动更有价值

        threads.append({
            "root": root,
            "replies": replies,
            "reply_count": len(replies),
            "interaction_score": round(interaction_score, 1),
            "has_up_reply": has_up_reply,
        })

    # 剩余的回复（无父评论）
    for parent_id, orphans in reply_map.items():
        for o in orphans:
            o_author = o.get("author_id", "")
            o_author_name = o.get("author", "")
            if (o_author and up_author_id and o_author == up_author_id) or \
               (o_author_name and "up" in o_author_name.lower()):
                up_author_comments.append({**o, "_type": "orphan"})
            orphan_replies.append(o)

    return {
        "threads": sorted(threads, key=lambda t: t["interaction_score"], reverse=True),
        "up_author_comments": up_author_comments,
        "orphan_replies": orphan_replies,
    }


# ══════════════════════════════════════════════════════════
# LLM语义分析（prompt模板——让提示词做不确定的事）
# ══════════════════════════════════════════════════════════

COMMENT_SEMANTIC_PROMPT = """你是一个视频评论区分析助手。分析以下评论数据，输出JSON格式结果。

## 视频信息
标题: {video_title}
UP主: {uploader}

## 评论概况
- 总评论数: {total_comments}
- 采样分析: {sample_count}条
- 互动话题数: {thread_count}

## 原始评论（部分）
{sample_comments}

## UP主发言（如果有）
{up_comments}

## 要求
请从以下维度分析并返回JSON（严格保持结构）：

1. topics: 评论中讨论的主要话题（3-5个），每个带出现频率(high/medium/low)
2. overall_sentiment: 整体情感倾向 positive/negative/mixed/neutral
3. audience_needs: 观众最关注/最想解决的问题（2-3个）
4. up_author_engagement: UP主与观众的互动情况描述（如果无则填null）
5. key_opinions: 值得关注的观众观点（2-3个），每个带 sentiment 和 representative_comment
6. spam_indicators: LLM额外发现的可能的垃圾/恶意评论特征（如有）
7. brief_summary: 对整个评论区的一句话总结

返回JSON格式示例:
{{
  "topics": [{{"topic": "xxx", "frequency": "high"}}],
  "overall_sentiment": "positive",
  "audience_needs": ["xxx"],
  "up_author_engagement": "UP主在评论中回复了XXX",
  "key_opinions": [{{"point": "xxx", "sentiment": "positive", "representative_comment": "xxx"}}],
  "spam_indicators": null,
  "brief_summary": "xxx"
}}
"""


def _call_llm_via_local(messages: List[Dict], timeout: int = 60) -> str:
    """使用本地 LLM 模块进行 API 调用（替代 ZIP 的 call_llm）

    适配：原版依赖 `biliyoutik2brain.core.corrector_engine.utils.call_llm`，
    本地化后使用 `core/llm.py` 的统一接口。
    """
    from .llm import _get_config, _call_openai_compatible

    config = _get_config("auto")
    config.timeout = timeout
    result = _call_openai_compatible(messages, config, max_tokens=2048, temperature=0.3)
    choice = result.get("choices", [{}])[0]
    return choice.get("message", {}).get("content", "")


def _build_comment_sample(comments: List[Dict], max_chars: int = 3000) -> str:
    """构建LLM的采样评论（加权取代表性的评论）"""
    # 按点赞排序，取前20条代表性评论
    sorted_c = sorted(comments, key=lambda c: c.get("likes", 0), reverse=True)
    sample = []
    total = 0
    for c in sorted_c:
        content = c.get("content", "")[:200]  # 每条截断到200字
        author = c.get("author", "匿名")
        likes = c.get("likes", 0)
        entry = f"[👍{likes}] {author}: {content}"
        if total + len(entry) > max_chars:
            break
        sample.append(entry)
        total += len(entry)
    return "\n".join(sample)


def _build_up_comments_str(up_comments: List[Dict], max_chars: int = 1500) -> str:
    """构建UP主发言文本"""
    if not up_comments:
        return "（无）"
    parts = []
    total = 0
    for c in up_comments:
        content = c.get("content", "")[:300]
        entry = f"[{c.get('_type', '')}] {content}"
        if total + len(entry) > max_chars:
            break
        parts.append(entry)
        total += len(entry)
    return "\n".join(parts)


def _semantic_analysis(comments: List[Dict], up_comments: List[Dict],
                       video_title: str, uploader: str,
                       total_comments: int, threads: List) -> Dict:
    """
    LLM 驱动的评论区语义分析

    由LLM执行语义理解：
    - 话题聚类（非关键词匹配）
    - 情感倾向（基于语义而非关键词计数）
    - 观众需求提取
    - UP主互动评估
    """

    sample_str = _build_comment_sample(comments)
    up_str = _build_up_comments_str(up_comments)

    prompt = COMMENT_SEMANTIC_PROMPT.format(
        video_title=video_title or "(未知)",
        uploader=uploader or "(未知)",
        total_comments=total_comments,
        sample_count=len(comments),
        thread_count=len(threads),
        sample_comments=sample_str,
        up_comments=up_str,
    )

    messages = [{"role": "user", "content": prompt}]

    try:
        result_text = _call_llm_via_local(messages, timeout=60)
        # 提取JSON
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception as e:
        pass

    # LLM分析失败时降级返回简单统计
    return {
        "error": f"LLM分析失败，使用基础统计",
        "overall_sentiment": "unknown",
        "brief_summary": "评论分析失败",
    }


# ══════════════════════════════════════════════════════════
# 主要分析入口
# ══════════════════════════════════════════════════════════

def analyze_comments(comment_result: CommentResult,
                     platform: str,
                     up_author_id: str = "") -> Dict:
    """
    完整评论分析管线

    Args:
        comment_result: 评论采集结果（包含全部评论数据）
        platform: 平台名称
        up_author_id: 视频UP主的用户ID（用于识别UP主评论）

    Returns:
        {
            "success": bool,
            "platform": str,
            "stats": {统计信息},
            "filtered": {过滤统计+移除列表},
            "threads": [互动树],
            "up_author_comments": [UP主发言],
            "semantic_analysis": {LLM语义分析结果},
            "top_comments": [互动得分最高的评论TOP10],
            "insights": [分析结论（下行文本）],
            "error": str (optional)
        }
    """

    if not comment_result.success:
        return {"success": False, "error": comment_result.error or "无评论数据"}

    all_comments = list(comment_result.hot) + list(comment_result.new)
    if not all_comments:
        return {"success": False, "error": "无评论数据"}

    # 1. 过滤垃圾/营销/互喷/恶意评论
    filtered_out = []
    clean_comments = []
    for c in all_comments:
        content = c.get("content", "")
        # 规则级过滤
        spam_type = _detect_spam(content)
        if spam_type:
            filtered_out.append({**c, "_filter_reason": spam_type})
            continue
        if _is_probably_short_spam(content):
            filtered_out.append({**c, "_filter_reason": "short_spam"})
            continue
        clean_comments.append(c)

    spam_count = sum(1 for f in filtered_out if f.get("_filter_reason") == "spam")
    flame_count = sum(1 for f in filtered_out if f.get("_filter_reason") == "flame")
    malicious_count = sum(1 for f in filtered_out if f.get("_filter_reason") == "malicious")
    short_spam_count = sum(1 for f in filtered_out if f.get("_filter_reason") == "short_spam")

    # 2. 构建互动树
    tree_data = _extract_threads(clean_comments, up_author_id)
    threads = tree_data["threads"]
    up_author_comments = tree_data["up_author_comments"]
    orphan_replies = tree_data["orphan_replies"]

    # 3. LLM语义分析
    semantic = _semantic_analysis(
        clean_comments, up_author_comments,
        video_title="", uploader="",
        total_comments=len(all_comments),
        threads=threads,
    )

    # 4. 按互动得分排序取TOP评论
    top_comments = sorted(
        threads, key=lambda t: t["interaction_score"], reverse=True
    )[:10]
    top_comments_clean = []
    for t in top_comments:
        root = t["root"]
        top_comments_clean.append({
            "author": root.get("author", "匿名"),
            "content": root.get("content", ""),
            "likes": root.get("likes", 0),
            "reply_count": t["reply_count"],
            "interaction_score": t["interaction_score"],
            "has_up_reply": t["has_up_reply"],
            "top_repiles": [
                {"author": r.get("author", ""), "content": r.get("content", "")[:100]}
                for r in t["replies"][:3]
            ],
        })

    # 5. 基础统计
    stats = {
        "total_raw": len(all_comments),
        "after_filter": len(clean_comments),
        "filtered_out": len(filtered_out),
        "thread_count": len(threads),
        "up_author_comment_count": len(up_author_comments),
        "avg_likes": sum(c.get("likes", 0) for c in clean_comments) / max(1, len(clean_comments)),
        "avg_interaction_score": round(
            sum(t["interaction_score"] for t in threads) / max(1, len(threads)), 1
        ),
    }

    # 6. 生成洞察
    insights = []

    if stats["filtered_out"] > 0:
        insights.append(
            f"已过滤{stats['filtered_out']}条异常评论"
            f"（营销{spam_count}条、互喷{flame_count}条"
            f"、恶意{malicious_count}条、短垃圾{short_spam_count}条）"
        )

    if stats["up_author_comment_count"] > 0:
        insights.append(f"UP主在评论区参与了互动（共{stats['up_author_comment_count']}条发言）")

    if semantic.get("overall_sentiment"):
        sentiment_map = {
            "positive": "评论区整体以正面为主",
            "negative": "评论区整体以负面为主",
            "mixed": "评论区存在争议，正负面观点并存",
            "neutral": "评论区以理性讨论为主",
        }
        insights.append(sentiment_map.get(semantic["overall_sentiment"], semantic["overall_sentiment"]))

    topics = semantic.get("topics", [])
    if topics:
        topic_names = [t.get("topic", "") for t in topics[:3]]
        insights.append(f"讨论热点：{'、'.join(topic_names)}")

    audience_needs = semantic.get("audience_needs", [])
    if audience_needs:
        needs_str = "；".join(audience_needs[:2])
        insights.append(f"观众关注点：{needs_str}")

    if semantic.get("brief_summary"):
        insights.append(semantic["brief_summary"])

    return {
        "success": True,
        "platform": platform,
        "stats": stats,
        "filtered": {
            "count": len(filtered_out),
            "spam": spam_count,
            "flame": flame_count,
            "malicious": malicious_count,
            "short_spam": short_spam_count,
            "removed": [
                {
                    "author": f.get("author", ""),
                    "content": f.get("content", "")[:80],
                    "reason": f.get("_filter_reason", ""),
                }
                for f in filtered_out[:20]
            ],
        },
        "threads": threads[:20],  # 只保留前20个最有价值的互动树
        "up_author_comments": [
            {
                "content": c.get("content", ""),
                "type": c.get("_type", ""),
                "likes": c.get("likes", 0),
            }
            for c in up_author_comments
        ],
        "semantic_analysis": semantic,
        "top_comments": top_comments_clean,
        "insights": insights[:8],  # 最多8条洞察
    }


def format_comments_report(analysis: Dict) -> str:
    """
    格式化评论分析报告

    Args:
        analysis: analyze_comments() 的返回
    Returns:
        markdown报告文本
    """
    if not analysis.get("success"):
        return f"❌ 评论分析失败：{analysis.get('error', '未知错误')}"

    lines = [
        "# 💬 评论语义分析",
        "",
        f"**平台**: {analysis.get('platform', 'unknown')}",
        "",
        "## 📊 统计概览",
        "",
        f"- 原始评论：{analysis['stats']['total_raw']}条",
        f"- 过滤后保留：{analysis['stats']['after_filter']}条",
        f"- 异常评论移除：{analysis['stats']['filtered_out']}条",
        f"  - 营销推广：{analysis['filtered']['spam']}条",
        f"  - 互喷：{analysis['filtered']['flame']}条",
        f"  - 恶意：{analysis['filtered']['malicious']}条",
        f"  - 短垃圾：{analysis['filtered']['short_spam']}条",
        f"- 互动话题：{analysis['stats']['thread_count']}个",
        f"- UP主参与：{'是(' + str(analysis['stats']['up_author_comment_count']) + '条发言)' if analysis['stats']['up_author_comment_count'] > 0 else '否'}",
        f"- 平均点赞：{analysis['stats']['avg_likes']:.1f}",
        f"- 平均互动得分：{analysis['stats']['avg_interaction_score']}",
        "",
    ]

    # UP主发言
    if analysis.get("up_author_comments"):
        lines.extend([
            "## 🎙️ UP主发言",
            "",
        ])
        for c in analysis["up_author_comments"]:
            lines.append(f"- [{c.get('type', '评论')}] {c.get('content', '')}")
            if c.get("likes", 0) > 0:
                lines[-1] += f" (👍{c['likes']})"
        lines.append("")

    # 情感
    sem = analysis.get("semantic_analysis", {})
    if sem.get("overall_sentiment"):
        sentiment_icons = {"positive": "😊", "negative": "😡", "mixed": "🤔", "neutral": "😐"}
        lines.extend([
            "## 😊 情感倾向",
            "",
            f"**{sentiment_icons.get(sem['overall_sentiment'], '')} {sem['overall_sentiment']}**",
            "",
        ])

    # 话题
    topics = sem.get("topics", [])
    if topics:
        lines.extend([
            "## 🔥 热门话题",
            "",
        ])
        for t in topics:
            freq_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            lines.append(f"- {freq_icon.get(t.get('frequency', ''), '')} {t.get('topic', '')}")
        lines.append("")

    # 观众需求
    needs = sem.get("audience_needs", [])
    if needs:
        lines.extend([
            "## 🎯 观众关注点",
            "",
        ])
        for n in needs:
            lines.append(f"- {n}")
        lines.append("")

    # 热门评论TOP10
    if analysis.get("top_comments"):
        lines.extend([
            "## 🔥 高互动评论 TOP10",
            "",
        ])
        for i, c in enumerate(analysis["top_comments"], 1):
            flag = " (UP已回复) " if c.get("has_up_reply") else ""
            lines.append(f"**{i}. {c.get('author', '匿名')}** 👍{c.get('likes', 0)} | 📨{c.get('reply_count', 0)}条回复 | 互动分{c.get('interaction_score', 0)}{flag}")
            lines.append(f"> {c.get('content', '')}")
            if c.get("top_repiles"):
                for reply in c["top_repiles"]:
                    lines.append(f">  ↳ {reply.get('author', '')}: {reply.get('content', '')}")
            lines.append("")

    # 关键观点
    opinions = sem.get("key_opinions", [])
    if opinions:
        sent_icon = {"positive": "👍", "negative": "👎", "mixed": "🤷", "neutral": "📌"}
        lines.extend([
            "## 💡 值得关注的观众观点",
            "",
        ])
        for o in opinions:
            icon = sent_icon.get(o.get("sentiment", ""), "")
            lines.append(f"- {icon} {o.get('point', '')}")
            if o.get("representative_comment"):
                lines.append(f"  > \"{o['representative_comment'][:120]}\"")
        lines.append("")

    # 洞察总结
    if analysis.get("insights"):
        lines.extend([
            "## 📌 分析总结",
            "",
        ])
        for insight in analysis["insights"]:
            lines.append(f"- {insight}")
        lines.append("")

    if analysis.get("filtered", {}).get("removed"):
        lines.extend([
            "## 🗑️ 移除的异常评论（部分）",
            "",
        ])
        for r in analysis["filtered"]["removed"][:5]:
            reason_icons = {
                "spam": "📢", "flame": "🔥", "malicious": "☣️", "short_spam": "🗑️"
            }
            lines.append(f"{reason_icons.get(r.get('reason', ''), '')} {r.get('author', '')}: {r.get('content', '')}")
        lines.append("")

    return "\n".join(lines)

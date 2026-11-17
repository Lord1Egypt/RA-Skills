"""
BiliYouTik2Brain — 评论质量过滤器 (v4.0)

增强版评论过滤，解决：
1. 重复评论检测（相同/相似内容跨用户重复）
2. 低俗/不健康内容过滤
3. 违法/诈骗/赌博/传销内容过滤
4. 有益评论提取（UP主深度讨论 + 高质量用户观点）

原则：规则层做确定过滤，LLM 做语义判断。
"""

import re
import json
import hashlib
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
#  重复评论检测
# ═══════════════════════════════════════════════════════════════

def _normalize_text(text: str) -> str:
    """标准化文本用于相似度比较"""
    # 去标点、去空格、转小写
    text = re.sub(r'[^\w\u4e00-\u9fff]', '', text.lower())
    # 去连续重复字（"好好好好好" → "好"）
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text


def _jaccard_similarity(s1: str, s2: str) -> float:
    """Jaccard 相似度（字符级 ngram）"""
    if not s1 or not s2:
        return 0.0
    n = 2  # bigram
    set1 = set(s1[i:i+n] for i in range(len(s1)-n+1))
    set2 = set(s2[i:i+n] for i in range(len(s2)-n+1))
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)


def detect_duplicates(comments: List[Dict], threshold: float = 0.7) -> List[Dict]:
    """
    检测重复/相似评论

    Args:
        comments: 评论列表（含 content 字段）
        threshold: 相似度阈值（0-1），>threshold 视为重复

    Returns:
        被标记为重复的评论列表（含 _dup_reason 字段）
    """
    duplicates = []
    seen: Dict[str, Dict] = {}  # normalized_text → first comment

    for c in comments:
        content = c.get("content", "")
        if len(content) < 5:
            continue  # 太短的跳过

        normalized = _normalize_text(content)
        content_hash = hashlib.md5(normalized.encode()).hexdigest()

        # 完全匹配
        if content_hash in {hashlib.md5(_normalize_text(s.get("content", "")).encode()).hexdigest()
                           for s in seen.values()}:
            duplicates.append({**c, "_dup_reason": "exact_match"})
            continue

        # 相似度匹配
        is_dup = False
        for norm_text, orig in seen.items():
            if _jaccard_similarity(normalized, norm_text) > threshold:
                duplicates.append({**c, "_dup_reason": f"similar_to_{orig.get('author', '匿名')}"})
                is_dup = True
                break

        if not is_dup:
            seen[normalized] = c

    return duplicates


# ═══════════════════════════════════════════════════════════════
#  低俗/不健康内容过滤
# ═══════════════════════════════════════════════════════════════

VULGAR_PATTERNS = [
    # 色情/擦边
    r'(?:约炮|援交|包养|小姐|上门服务|裸聊|色情|黄片|AV)',
    r'(?:嫩模|网红.{0,3}上门|外围|伴游)',
    r'(?:资源|种子|网盘|百度云).{0,5}(?:福利|合集|全套|完整版|无码)',
    r'(?:看片|看A|看黄|开车|飙车|车速快)',
    r'(?:白丝|黑丝|蕾丝|情趣|性感写真)',
    # 低俗用语
    r'(?:屌丝|废柴|loser|low逼|low货|土味)',
    r'(?:脑残粉|智障粉|水军|托儿)',
]

ILLEGAL_PATTERNS = [
    # 诈骗
    r'(?:兼职|刷单|打字员|客服).{0,5}(?:日赚|月入|轻松|高佣金)',
    r'(?:投资理财|荐股|带单|喊单|内幕消息).{0,5}(?:稳赚|保本|高收益)',
    r'(?:跑分|洗钱|套现|套现码|收款码).{0,5}(?:佣金|提成)',
    r'(?:杀猪盘|庞氏骗局|资金盘|传销)',
    # 赌博
    r'(?:博彩|赌博|赌球|赌码|六合彩|时时彩|百家乐)',
    r'(?:网赌|线上赌|澳门.{0,3}线上|真人荷官)',
    r'(?:投注|下注|赔率|盘口|水位)',
    # 违禁品
    r'(?:迷药|伟哥|春药|催情)',
    r'(?:代孕|性别鉴定|堕胎药)',
    r'(?:枪支|弹药|管制刀具)',
    # 违法信息
    r'(?:翻墙|vpn.{0,3}购买|科学上网.{0,3}购买)',
    r'(?:代写论文|代考|替考|作弊)',
    r'(?:发票|假证|假章|假文凭)',
]

# 引战模式（比互喷更宽泛）
FLAME_BAIT_PATTERNS = [
    # 地域攻击
    r'(?:XX人|XX省|XX市|XX地).{0,5}(?:都|全|就是).{0,5}(?:low|穷|土|傻|笨|骗子)',
    r'(?:南方人|北方人|农村人|城里人).{0,5}(?:就是|都|果然)',
    # 性别对立
    r'(?:女.{0,2}权|男.{0,2}权|田园女权|直男癌)',
    r'(?:普信.{0,2}男|小仙.{0,2}女|打拳)',
    # 饭圈/粉圈
    r'(?:粉丝.{0,3}洗地|脑残粉|饭圈.{0,3}文化|控评|带节奏)',
    # 引战句式
    r'(?:只有.{0,3}人才|不会.{0,3}只有|不懂的.{0,3}都是|.{0,3}的都是.{0,3}没文化)',
    r'(?:建议.{0,3}去.{0,3}看看|.{0,3}没.{0,3}别.{0,3}说话|.{0,3}还好意思)',
]


def detect_vulgar_illegal(content: str) -> Optional[str]:
    """
    检测低俗/违法/引战评论

    Returns:
        "vulgar" | "illegal" | "flame_bait" | None
    """
    for pat in VULGAR_PATTERNS:
        if re.search(pat, content):
            return "vulgar"
    for pat in ILLEGAL_PATTERNS:
        if re.search(pat, content):
            return "illegal"
    for pat in FLAME_BAIT_PATTERNS:
        if re.search(pat, content):
            return "flame_bait"
    return None


# ═══════════════════════════════════════════════════════════════
#  有益评论提取
# ═══════════════════════════════════════════════════════════════

# 高质量评论特征词
HIGH_QUALITY_SIGNALS = [
    # 提问/讨论
    r'(?:请问|为什么|怎么|如何|能(.{0,3}不)|.{0,3}(?:什么|哪个|哪里|怎么).{0,3}(?:理解|解释|说明))',
    # 分享经验
    r'(?:我.{0,5}(?:觉得|认为|尝试|实测|验证|总结|分享|经验|建议|推荐|补充))',
    # 技术讨论
    r'(?:参数|配置|方法|策略|指标|数据|测试|对比|分析|逻辑)',
    # 深度内容（长评论）
    r'^.{50,}$',
]

# UP 主深度讨论特征
UP_DISCUSSION_SIGNALS = [
    r'(?:回复.{0,3}的评论|谢谢大家|感谢|补充一下|纠正一下)',
    r'(?:统一回复|集中回答|这里统一说明)',
    r'(?:下一期|后面会|下期讲|后续)',
    r'(?:这个视频|本期内容|上面说的)',
]


def _score_comment_quality(content: str, is_up: bool = False) -> float:
    """
    给评论质量打分（0-1）

    Args:
        content: 评论内容
        is_up: 是否UP主发言

    Returns:
        质量分（越高越好）
    """
    score = 0.0
    length = len(content)

    # 基础分：长度（太短扣分，适中加分）
    if length < 5:
        score -= 0.3
    elif length < 20:
        score += 0.1
    elif length < 100:
        score += 0.3
    elif length < 300:
        score += 0.4
    else:
        score += 0.3  # 太长可能灌水

    # 高质量信号
    for sig in HIGH_QUALITY_SIGNALS:
        if re.search(sig, content):
            score += 0.15

    # UP 主发言加分
    if is_up:
        score += 0.3
        for sig in UP_DISCUSSION_SIGNALS:
            if re.search(sig, content):
                score += 0.1

    # 包含具体数据/案例加分
    if re.search(r'\d+\.?\d*[%℃元个次秒分]', content):
        score += 0.1

    # 有问有答加分（含问号）
    if '？' in content or '?' in content:
        score += 0.05

    return max(0.0, min(1.0, score))


def extract_valuable_comments(
    comments: List[Dict],
    up_author_id: str = "",
    top_n: int = 20,
    quality_threshold: float = 0.3,
) -> Dict:
    """
    提取有价值的评论

    Args:
        comments: 已过滤的评论列表
        up_author_id: UP主用户ID
        top_n: 返回数量
        quality_threshold: 最低质量分

    Returns:
        {
            "up_discussions": [...],       # UP主深度讨论
            "high_quality": [...],         # 高质量用户观点
            "discussion_chains": [...],    # 讨论链（UP参与的）
            "stats": {...}
        }
    """
    up_discussions = []
    high_quality = []
    discussion_chains = []

    for c in comments:
        content = c.get("content", "")
        author_id = c.get("author_id", "")
        author = c.get("author", "")
        is_up = bool(author_id and up_author_id and author_id == up_author_id)

        quality_score = _score_comment_quality(content, is_up)
        c["_quality_score"] = round(quality_score, 3)

        if quality_score < quality_threshold:
            continue

        # UP主深度讨论
        if is_up and quality_score > 0.4:
            up_discussions.append(c)

        # 高质量用户观点
        if not is_up and quality_score > quality_threshold:
            high_quality.append(c)

    # 讨论链：UP主参与的互动树
    reply_map: Dict[str, List] = {}
    for c in comments:
        parent_id = c.get("reply_to", "") or c.get("parent_id", "")
        if parent_id:
            reply_map.setdefault(parent_id, []).append(c)

    for c in comments:
        cid = c.get("id", "") or c.get("comment_id", "")
        author_id = c.get("author_id", "")
        replies = reply_map.get(cid, [])

        has_up = False
        for r in replies:
            r_author = r.get("author_id", "")
            if r_author and up_author_id and r_author == up_author_id:
                has_up = True
                break

        if has_up and (author_id == up_author_id or any(
            r.get("author_id", "") == up_author_id for r in replies
        )):
            discussion_chains.append({
                "root": c,
                "replies": [r for r in replies if r.get("author_id", "") == up_author_id],
                "total_replies": len(replies),
            })

    # 排序
    up_discussions.sort(key=lambda x: x.get("_quality_score", 0), reverse=True)
    high_quality.sort(key=lambda x: x.get("_quality_score", 0), reverse=True)
    discussion_chains.sort(key=lambda x: x.get("total_replies", 0), reverse=True)

    return {
        "up_discussions": up_discussions[:top_n],
        "high_quality": high_quality[:top_n],
        "discussion_chains": discussion_chains[:top_n],
        "stats": {
            "up_discussion_count": len(up_discussions),
            "high_quality_count": len(high_quality),
            "discussion_chain_count": len(discussion_chains),
            "avg_quality_score": round(
                sum(c.get("_quality_score", 0) for c in comments) / max(1, len(comments)),
                3,
            ),
        },
    }


# ═══════════════════════════════════════════════════════════════
#  LLM 辅助：有益评论总结 Prompt
# ═══════════════════════════════════════════════════════════════

VALUABLE_COMMENTS_SUMMARY_PROMPT = """你是一个视频评论区分析助手。基于已过滤和评分的评论，提取有价值的内容。

## 视频信息
标题: {video_title}
UP主: {uploader}
平台: {platform}

## UP主深度讨论（质量分从高到低）
{up_discussions}

## 高质量用户观点（质量分从高到低）
{high_quality_comments}

## 讨论链（UP主参与的互动）
{discussion_chains}

## 过滤统计
- 原始评论: {total_raw} 条
- 营销推广移除: {spam_count} 条
- 互喷移除: {flame_count} 条
- 恶意移除: {malicious_count} 条
- 低俗移除: {vulgar_count} 条
- 违法移除: {illegal_count} 条
- 引战移除: {flame_bait_count} 条
- 重复移除: {dup_count} 条
- 短垃圾移除: {short_spam_count} 条
- 最终保留: {kept_count} 条

## 要求
请从以下维度分析并返回JSON（严格保持结构）：

1. up_summary: UP主在评论区的核心观点总结（3-5条），每条含观点和代表性回复原文
2. key_insights: 从高质量评论中提炼的关键洞察（3-5条），每条含洞察+代表评论
3. audience_questions: 观众最想解决的问题（2-3个），按关注度排序
4. valuable_discussions: 最有价值的讨论链TOP3（UP与用户深度交流的）
5. brief_summary: 评论区价值的一句话总结

返回JSON格式:
{{
  "up_summary": [{{"point": "xxx", "quote": "原文"}}],
  "key_insights": [{{"insight": "xxx", "evidence": "代表评论原文"}}],
  "audience_questions": ["问题1", "问题2"],
  "valuable_discussions": [{{"topic": "xxx", "participants": ["UP主", "用户A"], "summary": "讨论总结"}}],
  "brief_summary": "xxx"
}}
"""


def build_valuable_comments_summary(
    valuable: Dict,
    filter_stats: Dict,
    video_title: str = "",
    uploader: str = "",
    platform: str = "",
) -> str:
    """构建有益评论总结文本（供 LLM 进一步分析）"""

    def format_comments(comments: List[Dict], prefix: str = "") -> str:
        parts = []
        for c in comments[:10]:
            q = c.get("_quality_score", 0)
            author = c.get("author", "匿名")
            content = c.get("content", "")[:200]
            parts.append(f"{prefix}[质量分{q}] {author}: {content}")
        return "\n".join(parts) or "（无）"

    up_str = format_comments(valuable.get("up_discussions", []), "🎙️ ")
    hq_str = format_comments(valuable.get("high_quality", []), "💡 ")

    chains = valuable.get("discussion_chains", [])
    chain_str = ""
    for ch in chains[:5]:
        root = ch.get("root", {})
        root_author = root.get("author", "匿名")
        root_content = root.get("content", "")[:100]
        replies = ch.get("replies", [])
        chain_str += f"🔗 {root_author}: {root_content}\n"
        for r in replies[:3]:
            chain_str += f"  ↳ {r.get('author', '匿名')}: {r.get('content', '')[:80]}\n"
    if not chain_str:
        chain_str = "（无）"

    return VALUABLE_COMMENTS_SUMMARY_PROMPT.format(
        video_title=video_title or "(未知)",
        uploader=uploader or "(未知)",
        platform=platform or "(未知)",
        up_discussions=up_str,
        high_quality_comments=hq_str,
        discussion_chains=chain_str,
        total_raw=filter_stats.get("total_raw", 0),
        spam_count=filter_stats.get("spam", 0),
        flame_count=filter_stats.get("flame", 0),
        malicious_count=filter_stats.get("malicious", 0),
        vulgar_count=filter_stats.get("vulgar", 0),
        illegal_count=filter_stats.get("illegal", 0),
        flame_bait_count=filter_stats.get("flame_bait", 0),
        dup_count=filter_stats.get("duplicate", 0),
        short_spam_count=filter_stats.get("short_spam", 0),
        kept_count=filter_stats.get("kept", 0),
    )


def format_valuable_comments_report(valuable: Dict, filter_stats: Dict) -> str:
    """格式化有益评论报告（不依赖 LLM，直接输出）"""
    lines = [
        "# 💬 评论质量报告",
        "",
        "## 📊 过滤统计",
        "",
        f"- 原始评论: {filter_stats.get('total_raw', 0)} 条",
        f"- 最终保留: {filter_stats.get('kept', 0)} 条",
        f"- 移除明细:",
        f"  - 📢 营销推广: {filter_stats.get('spam', 0)} 条",
        f"  - 🔥 互喷: {filter_stats.get('flame', 0)} 条",
        f"  - ☣️ 恶意: {filter_stats.get('malicious', 0)} 条",
        f"  - 🟡 低俗: {filter_stats.get('vulgar', 0)} 条",
        f"  - 🔴 违法: {filter_stats.get('illegal', 0)} 条",
        f"  - ⚔️ 引战: {filter_stats.get('flame_bait', 0)} 条",
        f"  - 🔄 重复: {filter_stats.get('duplicate', 0)} 条",
        f"  - 🗑️ 短垃圾: {filter_stats.get('short_spam', 0)} 条",
        "",
    ]

    stats = valuable.get("stats", {})
    lines.extend([
        "## 📈 质量统计",
        "",
        f"- UP主深度讨论: {stats.get('up_discussion_count', 0)} 条",
        f"- 高质量用户观点: {stats.get('high_quality_count', 0)} 条",
        f"- 有价值讨论链: {stats.get('discussion_chain_count', 0)} 条",
        f"- 平均质量分: {stats.get('avg_quality_score', 0):.3f}",
        "",
    ])

    # UP主讨论
    up_discussions = valuable.get("up_discussions", [])
    if up_discussions:
        lines.extend([
            "## 🎙️ UP主深度讨论",
            "",
        ])
        for c in up_discussions[:5]:
            q = c.get("_quality_score", 0)
            content = c.get("content", "")
            lines.append(f"**[质量分 {q}]** {content[:200]}")
            lines.append("")

    # 高质量观点
    high_quality = valuable.get("high_quality", [])
    if high_quality:
        lines.extend([
            "## 💡 高质量用户观点",
            "",
        ])
        for c in high_quality[:10]:
            q = c.get("_quality_score", 0)
            author = c.get("author", "匿名")
            content = c.get("content", "")
            lines.append(f"**{author}** [质量分 {q}]")
            lines.append(f"> {content[:200]}")
            lines.append("")

    # 讨论链
    chains = valuable.get("discussion_chains", [])
    if chains:
        lines.extend([
            "## 🔗 有价值讨论链（UP主参与）",
            "",
        ])
        for ch in chains[:5]:
            root = ch.get("root", {})
            root_author = root.get("author", "匿名")
            root_content = root.get("content", "")
            lines.append(f"**{root_author}**: {root_content[:150]}")
            replies = ch.get("replies", [])
            for r in replies[:3]:
                r_author = r.get("author", "匿名")
                r_content = r.get("content", "")
                lines.append(f"  ↳ **{r_author}**: {r_content[:100]}")
            lines.append("")

    return "\n".join(lines)

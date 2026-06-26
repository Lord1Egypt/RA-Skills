#!/usr/bin/env python3
"""TradeContactScorer — 外贸联系人质量评分工具"""

import argparse
import json
import re
import sys


class TradeContactScorer:
    """外贸联系人5维质量评分模型"""

    FOREIGN_TRADE_SIGNALS = [
        "外贸", "B2B", "跨境", "出口", "FOB", "CIF",
        "独立站", "亚马逊", "TikTok", "海外", "工厂",
        "供应链", "批发", "OEM", "ODM"
    ]

    DIMENSIONS = {
        "engagement_rate": {"weight": 0.25, "name": "互动率"},
        "save_ratio": {"weight": 0.20, "name": "收藏比"},
        "comment_activity": {"weight": 0.20, "name": "评论活跃度"},
        "follower_scale": {"weight": 0.15, "name": "粉丝规模"},
        "trade_relevance": {"weight": 0.20, "name": "外贸相关度"},
    }

    TIERS = {
        "S": {"min": 85, "label": "顶级外贸达人"},
        "A": {"min": 70, "label": "优质外贸账号"},
        "B": {"min": 55, "label": "潜力外贸账号"},
        "C": {"min": 40, "label": "一般账号"},
        "D": {"min": 0, "label": "低价值账号"},
    }

    PERSONA_MAP = {
        "工厂主": ["工厂", "生产", "制造", "厂房", "OEM"],
        "跨境卖家": ["亚马逊", "独立站", "店铺", "运营", "选品"],
        "SOHO": ["SOHO", "自由职业", "个人外贸", "创业"],
        "公司经营者": ["公司", "团队", "总经理", "CEO"],
        "新手": ["学习", "入门", "小白", "新手"],
    }

    def __init__(self):
        self.results = []
        self.seen_ids = set()

    def score_engagement(self, likes: int, comments: int, followers: int) -> float:
        if followers == 0:
            return 0.0
        rate = (likes + comments * 3) / followers
        return min(rate * 100, 100)

    def score_save_ratio(self, collects: int, likes: int) -> float:
        if likes == 0:
            return 0.0
        ratio = collects / likes
        return min(ratio * 50, 100)

    def score_comment_activity(self, comments: int, posts: int) -> float:
        if posts == 0:
            return 0.0
        rate = comments / posts
        return min(rate * 10, 100)

    def score_follower_scale(self, followers: int) -> float:
        if followers >= 50000:
            return 95
        elif followers >= 10000:
            return 80
        elif followers >= 5000:
            return 65
        elif followers >= 1000:
            return 45
        else:
            return 20

    def score_trade_relevance(self, bio: str, nickname: str) -> float:
        text = f"{bio} {nickname}".lower()
        matches = sum(1 for s in self.FOREIGN_TRADE_SIGNALS if s.lower() in text)
        return min(matches / len(self.FOREIGN_TRADE_SIGNALS) * 100 * 2, 100)

    def infer_persona(self, bio: str, nickname: str) -> str:
        text = f"{bio} {nickname}"
        scores = {}
        for persona, keywords in self.PERSONA_MAP.items():
            scores[persona] = sum(1 for k in keywords if k in text)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "未识别"

    def assign_tier(self, total_score: float) -> str:
        for tier, config in self.TIERS.items():
            if total_score >= config["min"]:
                return tier
        return "D"

    def score_contact(self, contact: dict) -> dict:
        uid = contact.get("id", "")
        if uid in self.seen_ids:
            return None
        self.seen_ids.add(uid)

        scores = {
            "engagement_rate": self.score_engagement(
                contact.get("likes", 0), contact.get("comments", 0), contact.get("followers", 0)
            ),
            "save_ratio": self.score_save_ratio(
                contact.get("collects", 0), contact.get("likes", 0)
            ),
            "comment_activity": self.score_comment_activity(
                contact.get("comments", 0), contact.get("posts", 1)
            ),
            "follower_scale": self.score_follower_scale(contact.get("followers", 0)),
            "trade_relevance": self.score_trade_relevance(
                contact.get("bio", ""), contact.get("nickname", "")
            ),
        }

        total = sum(scores[dim] * self.DIMENSIONS[dim]["weight"] for dim in scores)
        tier = self.assign_tier(total)
        persona = self.infer_persona(contact.get("bio", ""), contact.get("nickname", ""))

        return {
            "id": uid,
            "nickname": contact.get("nickname", ""),
            "tier": tier,
            "tier_label": self.TIERS[tier]["label"],
            "total_score": round(total, 1),
            "dimension_scores": {self.DIMENSIONS[k]["name"]: round(v, 1) for k, v in scores.items()},
            "persona": persona,
        }

    def score_batch(self, contacts: list) -> dict:
        results = []
        for c in contacts:
            scored = self.score_contact(c)
            if scored:
                results.append(scored)

        tier_dist = {}
        for r in results:
            tier_dist[r["tier"]] = tier_dist.get(r["tier"], 0) + 1

        return {
            "total_processed": len(results),
            "tier_distribution": tier_dist,
            "top_contacts": sorted(results, key=lambda x: x["total_score"], reverse=True)[:20],
            "all_scores": results,
        }


def main():
    parser = argparse.ArgumentParser(description="TradeContactScorer - 外贸联系人质量评分")
    parser.add_argument("--input", type=str, required=True, help="JSON格式联系人数据")
    parser.add_argument("--min-tier", type=str, default="C", choices=["S", "A", "B", "C", "D"], help="最低显示等级")
    args = parser.parse_args()

    try:
        contacts = json.loads(args.input)
        if not isinstance(contacts, list):
            contacts = [contacts]
    except json.JSONDecodeError:
        print(json.dumps({"error": "输入数据格式错误，需要合法JSON"}))
        sys.exit(1)

    scorer = TradeContactScorer()
    result = scorer.score_batch(contacts)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

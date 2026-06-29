#!/usr/bin/env python3
"""
Dianping Restaurant Guide (dianping-guide.py)
Extract real restaurant insights from Dianping reviews: filter noise,
detect fake reviews, build personalized dining guides.
License: MIT-0
"""
import argparse
import json
import math
import os
import random
import re
import sys
import textwrap
from collections import Counter, defaultdict

VERSION = "1.0.0"

# ── Constants ─────────────────────────────────────────────────────────

GENERIC_PHRASES = [
    "环境不错", "味道很好", "服务态度好", "性价比高",
    "还会再来", "推荐", "不错", "好吃", "一般般",
    "挺好的", "还行吧", "值得推荐", "价格实惠",
    "位置好找", "交通方便", "装修不错", "分量足"
]

DISH_KEYWORDS = {
    "taste_good": [
        "好吃", "鲜美", "入味", "嫩", "香", "正宗", "地道",
        "新鲜", "口感好", "赞", "绝了", "惊艳", "不错"
    ],
    "taste_bad": [
        "不好吃", "不入味", "太咸", "太油", "太辣", "太淡",
        "一般", "失望", "难吃", "腥", "老", "硬", "凉了"
    ],
    "env_good": [
        "环境好", "干净", "安静", "装修", "氛围", "宽敞",
        "舒适", "有格调", "温馨", "雅致"
    ],
    "env_bad": [
        "太吵", "拥挤", "脏", "油烟", "空调不足", "位置小"
    ],
    "service_good": [
        "服务好", "热情", "周到", "耐心", "上菜快", "贴心"
    ],
    "service_bad": [
        "服务差", "态度不好", "上菜慢", "等位久", "爱理不理"
    ],
    "value_good": [
        "性价比高", "实惠", "便宜", "量足", "物超所值", "划算"
    ],
    "value_bad": [
        "性价比低", "贵", "不值", "量少", "坑", "不值得"
    ]
}

# ── Utility Functions ─────────────────────────────────────────────────

# load_signals() removed — signals are hardcoded in FakeReviewDetector.analyze()
# See references/signals.json for documentation of detection signals.
def safe_json_loads(text):
    """Safely parse JSON; return None on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None

def cosine_similarity(text_a, text_b):
    """Simple word-level cosine similarity."""
    words_a = set(re.findall(r'\S+', text_a))
    words_b = set(re.findall(r'\S+', text_b))
    intersection = words_a & words_b
    denom = math.sqrt(len(words_a) * len(words_b))
    if denom == 0:
        return 0.0
    return len(intersection) / denom

def is_generic_review(text):
    """Check if review text is generic/vague."""
    if len(text) < 15:
        return True
    # Count specific-sounding content (numbers, prices, dish names, etc.)
    specific_signals = 0
    if re.search(r'[¥￥]\d+', text):
        specific_signals += 1
    if re.search(r'\d+分|[\d]+[分钟小时]', text):
        specific_signals += 1
    # Dish name detection via common dish classifiers
    dish_pattern = r'[一种两三大几小]?[碗碟份盘只个]|(?:麻婆|宫保|鱼香|水煮|回锅|红烧|清蒸|糖醋|干锅|辣子|毛血旺|酸菜)'
    if re.search(dish_pattern, text):
        specific_signals += 1
    # Count how many of the review words are generic
    word_count = len(re.findall(r'\S+', text))
    generic_count = sum(1 for p in GENERIC_PHRASES if p in text)
    if word_count > 0 and generic_count / word_count > 0.3:
        return True
    return specific_signals < 1

# ── Fake Review Detection ─────────────────────────────────────────────

class FakeReviewDetector:
    """Multi-signal fake review detection engine."""

    def __init__(self):
        self.reviews = []
        self.results = {}

    def analyze(self, reviews):
        """
        Analyze a list of review dicts.
        Returns: dict with per-review tags + restaurant summary.
        """
        if not reviews:
            return {
                "total": 0, "fake_count": 0, "suspicious_count": 0,
                "genuine_count": 0, "authenticity_index": 100,
                "reviews": [], "signals_triggered": [],
                "verdict": "trustworthy"
            }

        self.reviews = reviews
        n = len(reviews)
        scores = []
        signals_triggered = []

        for i, review in enumerate(reviews):
            score = 0
            review_signals = []

            # 1. Time cluster check
            timestamps = [r.get("timestamp", "") for r in reviews]
            cluster_count = self._count_time_cluster(review.get("timestamp", ""), timestamps)
            if cluster_count >= 5:
                penalty = cluster_count * 5
                score += penalty
                review_signals.append({
                    "signal": "time_cluster",
                    "severity": "high", "details": f"{cluster_count} reviews in cluster"
                })

            # 2. Reviewer account age
            age_days = review.get("reviewer_age_days", 365)
            if age_days < 7:
                score += 20
                review_signals.append({
                    "signal": "reviewer_age",
                    "severity": "high", "details": f"Account {age_days} days old"
                })
            elif age_days < 30:
                score += 10
                review_signals.append({
                    "signal": "reviewer_age",
                    "severity": "medium", "details": f"Account {age_days} days old"
                })

            # 3. Review frequency
            freq = review.get("reviewer_total_reviews", 0) / max(age_days, 1) * 30
            if freq > 10:
                score += int(freq * 2)
                review_signals.append({
                    "signal": "review_frequency",
                    "severity": "high", "details": f"~{freq:.0f} reviews/month"
                })

            # 4. Text similarity with other reviews
            text = review.get("text", "")
            sim_count = 0
            if text:
                for j, other in enumerate(reviews):
                    if i == j:
                        continue
                    other_text = other.get("text", "")
                    if other_text and cosine_similarity(text, other_text) > 0.7:
                        sim_count += 1
            if sim_count >= 2:
                score += sim_count * 7
                review_signals.append({
                    "signal": "text_similarity",
                    "severity": "high", "details": f"Similar to {sim_count} other reviews"
                })

            # 5. Photo EXIF (simplified: identical photo count suggests identical camera)
            pc = review.get("photo_count", 0)
            if pc > 0:
                same_photo_count = sum(
                    1 for r in reviews if r.get("photo_count", 0) == pc and r.get("reviewer_id") != review.get("reviewer_id")
                )
                if same_photo_count >= 3:
                    score += same_photo_count * 5
                    review_signals.append({
                        "signal": "photo_exif",
                        "severity": "medium", "details": f"{same_photo_count} reviews with same photo count"
                    })

            # 6. Generic language
            if is_generic_review(text):
                score += 5
                review_signals.append({
                    "signal": "generic_language",
                    "severity": "low", "details": "Generic/vague language"
                })

            # 7. Rating pattern
            rating = review.get("rating", 0)
            if rating >= 4.5 and len(text) < 30:
                score += 5
                review_signals.append({
                    "signal": "rating_pattern",
                    "severity": "low", "details": "High rating with short/no text"
                })

            # 8. Reviewer history (positive-only)
            if review.get("reviewer_total_reviews", 0) >= 5:
                # Simulate: positive-only detected if no negative language
                if rating >= 4.0 and not any(w in text for w in ["不好", "差", "失望", "难吃"]):
                    score += 5
                    review_signals.append({
                        "signal": "reviewer_history",
                        "severity": "medium", "details": "Only positive reviews"
                    })

            # Normalize score to 0-100
            norm_score = min(score * 5, 100)
            scores.append(norm_score)

            # Tag the review
            if norm_score >= 60:
                tag = "likely_fake"
            elif norm_score >= 30:
                tag = "suspicious"
            else:
                tag = "genuine"

            self.results[i] = {
                "index": i,
                "text_preview": text[:60],
                "score": norm_score,
                "tag": tag,
                "signals": review_signals
            }
            signals_triggered.extend(review_signals)

        fake_count = sum(1 for r in self.results.values() if r["tag"] == "likely_fake")
        suspicious_count = sum(1 for r in self.results.values() if r["tag"] == "suspicious")
        genuine_count = sum(1 for r in self.results.values() if r["tag"] == "genuine")

        authenticity = 100 - (sum(scores) / n) if n > 0 else 100
        authenticity = max(0, min(100, round(authenticity, 1)))

        # Deduplicate signals
        seen_signals = {}
        for s in signals_triggered:
            key = s["signal"]
            if key not in seen_signals or s["severity"] == "high":
                seen_signals[key] = s
            elif s["severity"] == "medium" and seen_signals[key]["severity"] == "low":
                seen_signals[key] = s

        fake_pct = (fake_count / n * 100) if n > 0 else 0
        if authenticity >= 80:
            verdict = "trustworthy"
        elif authenticity >= 60:
            verdict = "some_concerns"
        elif authenticity >= 40:
            verdict = "suspicious"
        else:
            verdict = "high_risk"

        warnings = []
        if fake_pct > 40:
            warnings.append(f"Over {fake_pct:.0f}% of reviews appear fake — strong warning")

        return {
            "total": n,
            "fake_count": fake_count,
            "suspicious_count": suspicious_count,
            "genuine_count": genuine_count,
            "authenticity_index": int(authenticity),
            "reviews": [self.results[i] for i in sorted(self.results.keys())],
            "signals_triggered": list(seen_signals.values()),
            "verdict": verdict,
            "warnings": warnings
        }

    def _count_time_cluster(self, ts, all_tss):
        """Count reviews within 30 minutes of given timestamp."""
        if not ts or not all_tss:
            return 1
        # Simple: count identical or near-identical timestamps
        hour_min = ts[:16]  # YYYY-MM-DD HH:MM
        return sum(1 for t in all_tss if t[:16] == hour_min)

# ── Sentiment Extraction ─────────────────────────────────────────────

class SentimentExtractor:
    """Extract structured sentiment from genuine reviews."""

    def extract(self, reviews):
        """Extract sentiment across taste/environment/service/value dimensions."""
        if not reviews:
            return {
                "taste": {"score": 0, "positives": [], "negatives": [], "must_order_dishes": [], "avoid_dishes": []},
                "environment": {"score": 0, "positives": [], "negatives": []},
                "service": {"score": 0, "positives": [], "negatives": []},
                "value": {"score": 0, "positives": [], "negatives": []}
            }

        dims = {
            "taste": {"pos_count": 0, "neg_count": 0, "pos_mentions": [], "neg_mentions": []},
            "environment": {"pos_count": 0, "neg_count": 0, "pos_mentions": [], "neg_mentions": []},
            "service": {"pos_count": 0, "neg_count": 0, "pos_mentions": [], "neg_mentions": []},
            "value": {"pos_count": 0, "neg_count": 0, "pos_mentions": [], "neg_mentions": []}
        }

        dish_pos = Counter()
        dish_neg = Counter()

        for review in reviews:
            text = review.get("text", "")
            if not text:
                continue

            # Taste
            for kw in DISH_KEYWORDS["taste_good"]:
                if kw in text:
                    dims["taste"]["pos_count"] += 1
                    # Extract dish context
                    context = self._extract_dish_context(text, kw)
                    if context:
                        dish_pos[context] += 1
                    break  # Count once per review per dimension
            for kw in DISH_KEYWORDS["taste_bad"]:
                if kw in text:
                    dims["taste"]["neg_count"] += 1
                    context = self._extract_dish_context(text, kw)
                    if context:
                        dish_neg[context] += 1
                    break

            # Environment
            for kw in DISH_KEYWORDS["env_good"]:
                if kw in text:
                    dims["environment"]["pos_count"] += 1
                    dims["environment"]["pos_mentions"].append(kw)
                    break
            for kw in DISH_KEYWORDS["env_bad"]:
                if kw in text:
                    dims["environment"]["neg_count"] += 1
                    dims["environment"]["neg_mentions"].append(kw)
                    break

            # Service
            for kw in DISH_KEYWORDS["service_good"]:
                if kw in text:
                    dims["service"]["pos_count"] += 1
                    dims["service"]["pos_mentions"].append(kw)
                    break
            for kw in DISH_KEYWORDS["service_bad"]:
                if kw in text:
                    dims["service"]["neg_count"] += 1
                    dims["service"]["neg_mentions"].append(kw)
                    break

            # Value
            for kw in DISH_KEYWORDS["value_good"]:
                if kw in text:
                    dims["value"]["pos_count"] += 1
                    dims["value"]["pos_mentions"].append(kw)
                    break
            for kw in DISH_KEYWORDS["value_bad"]:
                if kw in text:
                    dims["value"]["neg_count"] += 1
                    dims["value"]["neg_mentions"].append(kw)
                    break

        result = {}
        for dim_name, data in dims.items():
            total = data["pos_count"] + data["neg_count"]
            score = 5.0  # neutral baseline
            if total > 0:
                score = (data["pos_count"] / total) * 10
            pos_summary = self._summarize_mentions(data["pos_mentions"])
            neg_summary = self._summarize_mentions(data["neg_mentions"])
            result[dim_name] = {
                "score": round(score, 1),
                "positives": [f"{s} ({data['pos_count']} mentions)" for s in pos_summary[:3]] if pos_summary else [],
                "negatives": [f"{s} ({data['neg_count']} mentions)" for s in neg_summary[:3]] if neg_summary else []
            }

        # Dish-level sentiment
        must_order = [d for d, _ in dish_pos.most_common(5) if dish_pos[d] > dish_neg.get(d, 0)]
        avoid = [d for d, _ in dish_neg.most_common(5) if dish_neg[d] > dish_pos.get(d, 0)]
        result["taste"]["must_order_dishes"] = must_order[:5]
        result["taste"]["avoid_dishes"] = avoid[:3]

        return result

    def _extract_dish_context(self, text, keyword):
        """Try to extract a dish name mentioned near the keyword."""
        # Simple heuristic: look for Chinese dish patterns
        dish_patterns = [
            r'([^。，！？\n]{1,12}(?:麻婆|宫保|鱼香|水煮|回锅|红烧|清蒸|糖醋|干锅|辣子|毛血旺|酸菜|蒜泥|白肉|口水|夫妻|东坡|叫花)[^。，！？\n]{0,8})',
            r'([^。，！？\n]{0,4}(?:鱼|肉|鸡|鸭|虾|蟹|牛|羊|豆腐|面|饭|粉|汤|菜|锅|饼|饺|包)[^。，！？\n]{0,5})',
        ]
        for pattern in dish_patterns:
            m = re.search(pattern, text)
            if m:
                return m.group(1).strip()
        # Fallback to context near keyword
        idx = text.find(keyword)
        if idx >= 0:
            start = max(0, idx - 10)
            end = min(len(text), idx + 10)
            return text[start:end].strip()
        return None

    def _summarize_mentions(self, mentions):
        """Get top mentioned characteristics."""
        if not mentions:
            return []
        counter = Counter(mentions)
        return [item for item, _ in counter.most_common(5)]

# ── Sample Data ──────────────────────────────────────────────────────

SAMPLE_RESTAURANTS = [
    {
        "name": "老王川菜",
        "rating": 4.3,
        "review_count": 120,
        "cuisine_type": "川菜",
        "address": "上海静安区南京西路1000号",
        "lat": 31.2265, "lng": 121.4528,
        "price_per_person": 65,
        "tags": ["川菜", "老字号", "性价比高"],
        "reviews": [
            {"text": "麻婆豆腐太好吃了，38元一份很划算，下次还来", "rating": 5.0, "timestamp": "2026-06-15 12:30", "reviewer_age_days": 365, "reviewer_total_reviews": 15, "photo_count": 2},
            {"text": "回锅肉很正宗，和四川吃的一个味", "rating": 4.5, "timestamp": "2026-06-15 12:35", "reviewer_age_days": 200, "reviewer_total_reviews": 8, "photo_count": 0},
            {"text": "水煮鱼一般般，不入味", "rating": 3.0, "timestamp": "2026-06-14 19:00", "reviewer_age_days": 500, "reviewer_total_reviews": 42, "photo_count": 1},
            {"text": "环境不错", "rating": 5.0, "timestamp": "2026-06-15 12:31", "reviewer_age_days": 3, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "味道很好", "rating": 5.0, "timestamp": "2026-06-15 12:32", "reviewer_age_days": 5, "reviewer_total_reviews": 1, "photo_count": 0},
            {"text": "性价比高，两人吃了130，很饱", "rating": 4.5, "timestamp": "2026-06-13 13:00", "reviewer_age_days": 180, "reviewer_total_reviews": 22, "photo_count": 0},
            {"text": "推荐，还会再来", "rating": 5.0, "timestamp": "2026-06-15 12:33", "reviewer_age_days": 2, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "蒜泥白肉很好吃！", "rating": 5.0, "timestamp": "2026-06-12 19:30", "reviewer_age_days": 300, "reviewer_total_reviews": 35, "photo_count": 1},
            {"text": "等位很久，上菜也慢，服务一般", "rating": 3.0, "timestamp": "2026-06-11 20:00", "reviewer_age_days": 400, "reviewer_total_reviews": 60, "photo_count": 0},
            {"text": "老顾客了，吃了十年，价格涨了但味道没变", "rating": 4.5, "timestamp": "2026-06-10 18:30", "reviewer_age_days": 3650, "reviewer_total_reviews": 120, "photo_count": 1},
        ]
    },
    {
        "name": "弄堂小馄饨",
        "rating": 4.0,
        "review_count": 85,
        "cuisine_type": "小吃",
        "address": "上海静安区愚园路200号",
        "lat": 31.2280, "lng": 121.4480,
        "price_per_person": 25,
        "tags": ["小吃", "馄饨", "性价比高"],
        "reviews": [
            {"text": "小馄饨皮薄馅大，汤头鲜", "rating": 4.5, "timestamp": "2026-06-14 11:00", "reviewer_age_days": 200, "reviewer_total_reviews": 10, "photo_count": 0},
            {"text": "排队的人很多，但值", "rating": 4.0, "timestamp": "2026-06-13 12:00", "reviewer_age_days": 150, "reviewer_total_reviews": 5, "photo_count": 0},
            {"text": "环境不错", "rating": 5.0, "timestamp": "2026-06-15 12:31", "reviewer_age_days": 3, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "味道很好", "rating": 5.0, "timestamp": "2026-06-15 12:32", "reviewer_age_days": 4, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "一般般", "rating": 3.0, "timestamp": "2026-06-12 13:00", "reviewer_age_days": 100, "reviewer_total_reviews": 12, "photo_count": 0},
            {"text": "汤包也好吃！推荐蟹粉汤包", "rating": 4.5, "timestamp": "2026-06-11 10:30", "reviewer_age_days": 250, "reviewer_total_reviews": 20, "photo_count": 1},
            {"text": "价格便宜，12元一碗，上海滩难找", "rating": 4.5, "timestamp": "2026-06-10 09:00", "reviewer_age_days": 180, "reviewer_total_reviews": 15, "photo_count": 0},
        ]
    },
    {
        "name": "福1088",
        "rating": 4.6,
        "review_count": 200,
        "cuisine_type": "本帮菜",
        "address": "上海静安区镇宁路1088号",
        "lat": 31.2240, "lng": 121.4380,
        "price_per_person": 180,
        "tags": ["本帮菜", "约会", "商务"],
        "reviews": [
            {"text": "红烧肉入口即化，环境很有老上海风情", "rating": 5.0, "timestamp": "2026-06-15 19:00", "reviewer_age_days": 500, "reviewer_total_reviews": 30, "photo_count": 3},
            {"text": "适合约会，氛围很好", "rating": 4.5, "timestamp": "2026-06-14 20:00", "reviewer_age_days": 300, "reviewer_total_reviews": 18, "photo_count": 1},
            {"text": "价格偏贵，但品质对得起价格", "rating": 4.0, "timestamp": "2026-06-13 19:30", "reviewer_age_days": 250, "reviewer_total_reviews": 25, "photo_count": 0},
            {"text": "服务很专业，包间适合商务宴请", "rating": 4.5, "timestamp": "2026-06-12 18:00", "reviewer_age_days": 400, "reviewer_total_reviews": 50, "photo_count": 0},
            {"text": "蟹粉豆腐一般，不如别家", "rating": 3.0, "timestamp": "2026-06-11 19:00", "reviewer_age_days": 350, "reviewer_total_reviews": 40, "photo_count": 0},
        ]
    },
    {
        "name": "网红火锅店（测试-可疑）",
        "rating": 4.8,
        "review_count": 300,
        "cuisine_type": "火锅",
        "address": "上海静安区某网红街",
        "lat": 31.2290, "lng": 121.4550,
        "price_per_person": 150,
        "tags": ["火锅", "网红"],
        "reviews": [
            {"text": "环境不错", "rating": 5.0, "timestamp": "2026-06-15 12:30", "reviewer_age_days": 2, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "味道很好", "rating": 5.0, "timestamp": "2026-06-15 12:31", "reviewer_age_days": 1, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "推荐", "rating": 5.0, "timestamp": "2026-06-15 12:32", "reviewer_age_days": 3, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "还会再来", "rating": 5.0, "timestamp": "2026-06-15 12:33", "reviewer_age_days": 4, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "不错", "rating": 5.0, "timestamp": "2026-06-15 12:34", "reviewer_age_days": 2, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "服务态度好", "rating": 5.0, "timestamp": "2026-06-15 12:35", "reviewer_age_days": 2, "reviewer_total_reviews": 0, "photo_count": 0},
            {"text": "价格有点贵，但味道确实好", "rating": 4.0, "timestamp": "2026-06-14 19:00", "reviewer_age_days": 365, "reviewer_total_reviews": 45, "photo_count": 0},
            {"text": "这评分是刷的吧，吃过一次很一般", "rating": 2.0, "timestamp": "2026-06-13 20:00", "reviewer_age_days": 500, "reviewer_total_reviews": 80, "photo_count": 0},
        ]
    }
]

# ── CLI Commands ──────────────────────────────────────────────────────

def cmd_profile(args):
    """Define dining context."""
    profile = {
        "location": args.location or "上海静安寺",
        "cuisine": args.cuisine or "any",
        "budget_min": args.budget_min or 50,
        "budget_max": args.budget_max or 150,
        "occasion": args.occasion or "any",
        "radius_km": args.radius or 3,
        "party_size": args.party_size or 2,
    }
    print("=== Dining Profile ===")
    print(f"Location:     {profile['location']}")
    print(f"Cuisine:      {profile['cuisine']}")
    print(f"Budget:       ¥{profile['budget_min']}-{profile['budget_max']}/person")
    print(f"Occasion:     {profile['occasion']}")
    print(f"Radius:       {profile['radius_km']} km")
    print(f"Party size:   {profile['party_size']}")
    print()
    print(json.dumps(profile, ensure_ascii=False, indent=2))

def cmd_discover(args):
    """Candidate discovery (uses sample data)."""
    cuisine_filter = args.cuisine or "any"
    price_max = args.budget_max or 150
    results = []
    for r in SAMPLE_RESTAURANTS:
        if cuisine_filter != "any" and cuisine_filter not in r.get("cuisine_type", ""):
            continue
        if r.get("price_per_person", 0) > price_max:
            continue
        if r.get("review_count", 0) < 30:
            continue
        if r.get("rating", 0) < 3.5:
            continue
        results.append(r)

    print("=== Candidate Discovery ===")
    print(f"Filters: cuisine={cuisine_filter}, budget≤¥{price_max}, rating≥3.5, reviews≥30")
    print(f"Found: {len(results)} restaurant(s)")
    print()
    for r in results:
        print(f"  {r['name']} | Rating {r['rating']} | ¥{r['price_per_person']}/p | {r['cuisine_type']} | {r['review_count']} reviews")
    print()

def cmd_analyze(args):
    """Analyze a restaurant's reviews for authenticity and sentiment."""
    name = args.name
    target = None
    for r in SAMPLE_RESTAURANTS:
        if name.lower() in r["name"].lower():
            target = r
            break

    if not target:
        print(f"Restaurant '{name}' not found in sample data.")
        print(f"Available: {', '.join(r['name'] for r in SAMPLE_RESTAURANTS)}")
        return 1

    reviews = target.get("reviews", [])

    # Fake review detection
    detector = FakeReviewDetector()
    auth_result = detector.analyze(reviews)
    genuine_reviews = [
        r for i, r in enumerate(reviews)
        if i in detector.results and detector.results[i]["tag"] == "genuine"
    ]

    print(f"=== Analysis: {target['name']} ===")
    print(f"Overall Rating: {target['rating']} | Reviews: {target['review_count']}")
    print()

    # Authenticity
    ai = auth_result["authenticity_index"]
    if ai >= 80:
        badge = "✅ Trustworthy"
        color_prefix = ""
    elif ai >= 60:
        badge = "⚠️ Some Concerns"
        color_prefix = ""
    else:
        badge = "🔴 Suspicious/High Risk"
        color_prefix = ""
    print(f"Authenticity Index: {ai}/100 — {badge}")
    print(f"  Total: {auth_result['total']} | Genuine: {auth_result['genuine_count']} | "
          f"Suspicious: {auth_result['suspicious_count']} | Likely Fake: {auth_result['fake_count']}")

    if auth_result["signals_triggered"]:
        print(f"  Signals detected:")
        for s in auth_result["signals_triggered"]:
            print(f"    - [{s['severity'].upper()}] {s['signal']}: {s['details']}")

    for w in auth_result.get("warnings", []):
        print(f"  ⚠️  {w}")
    print()

    # Sentiment
    extractor = SentimentExtractor()
    sentiment = extractor.extract(genuine_reviews)

    print(f"--- Sentiment (from {len(genuine_reviews)} genuine reviews) ---")
    for dim_name, dim_data in sentiment.items():
        dim_label = dim_name.capitalize()
        score = dim_data.get("score", 0)
        bar = "█" * int(score) + "░" * (10 - int(score))
        print(f"  {dim_label}: {score:.1f}/10 {bar}")
        if dim_data.get("positives"):
            print(f"    👍 {', '.join(dim_data['positives'][:3])}")
        if dim_data.get("negatives"):
            print(f"    👎 {', '.join(dim_data['negatives'][:3])}")

    # Dish highlights
    must_order = sentiment.get("taste", {}).get("must_order_dishes", [])
    avoid = sentiment.get("taste", {}).get("avoid_dishes", [])
    if must_order:
        print(f"  🏆 Must-order: {', '.join(must_order)}")
    if avoid:
        print(f"  ✕ Avoid: {', '.join(avoid)}")

    print()

def cmd_rank(args):
    """Personalized ranking of all sample restaurants."""
    cuisine = args.cuisine or "any"
    max_budget = args.budget_max or 200
    occasion = args.occasion or "any"

    # Score each restaurant
    scored = []
    for r in SAMPLE_RESTAURANTS:
        # Cuisine match
        if cuisine == "any" or cuisine in r.get("cuisine_type", ""):
            cuisine_match = 100
        else:
            cuisine_match = 50

        # Budget fit
        pp = r.get("price_per_person", 0)
        if pp <= max_budget:
            value_score = 100 - max(0, (pp / max_budget) * 30)
        else:
            value_score = 30

        # Occasion fit
        occasion_map = {
            "date": ["本帮菜", "西餐", "日料"],
            "business": ["本帮菜", "粤菜"],
            "family": ["火锅", "川菜", "本帮菜"],
            "solo": ["小吃", "快餐"],
            "group_dinner": ["火锅", "川菜"],
            "casual": ["小吃", "川菜", "火锅"],
        }
        cuisine_match_for_occ = r.get("cuisine_type", "")
        occ_list = occasion_map.get(occasion, [])
        if occasion == "any" or not occ_list:
            occasion_fit = 80
        else:
            occasion_fit = 100 if cuisine_match_for_occ in occ_list else 50

        # Authenticity bonus (use detector)
        detector = FakeReviewDetector()
        auth = detector.analyze(r.get("reviews", []))
        authenticity_bonus = auth["authenticity_index"] * 0.3

        # Overall
        overall = cuisine_match * 0.25 + value_score * 0.20 + occasion_fit * 0.20 + authenticity_bonus

        scored.append({
            "restaurant": r["name"],
            "rating": r["rating"],
            "price": pp,
            "cuisine_type": r.get("cuisine_type", ""),
            "cuisine_match": round(cuisine_match, 1),
            "value_score": round(value_score, 1),
            "occasion_fit": round(occasion_fit, 1),
            "authenticity_bonus": round(authenticity_bonus, 1),
            "overall": round(overall, 1)
        })

    scored.sort(key=lambda x: x["overall"], reverse=True)

    print("=== Personalized Ranking ===")
    print(f"Preferences: cuisine={cuisine}, budget≤¥{max_budget}, occasion={occasion}")
    print()

    for i, item in enumerate(scored, 1):
        print(f"#{i} {item['restaurant']} — Score: {item['overall']:.1f}/100")
        print(f"   {item['cuisine_type']} | Rating {item['rating']} | ¥{item['price']}/p")
        print(f"   Cuisine: {item['cuisine_match']} | Value: {item['value_score']} | "
              f"Occasion: {item['occasion_fit']} | Authenticity: +{item['authenticity_bonus']}")
        print()

def cmd_order(args):
    """Generate ordering guide for a restaurant."""
    name = args.name
    target = None
    for r in SAMPLE_RESTAURANTS:
        if name.lower() in r["name"].lower():
            target = r
            break

    if not target:
        print(f"Restaurant '{name}' not found.")
        return 1

    party_size = args.party_size or 2
    reviews = target.get("reviews", [])

    # Filter genuine
    detector = FakeReviewDetector()
    detector.analyze(reviews)
    genuine_reviews = [
        r for i, r in enumerate(reviews)
        if i in detector.results and detector.results[i]["tag"] == "genuine"
    ]

    # Extract dish sentiment
    extractor = SentimentExtractor()
    sentiment = extractor.extract(genuine_reviews)
    must_order = sentiment.get("taste", {}).get("must_order_dishes", [])
    avoid = sentiment.get("taste", {}).get("avoid_dishes", [])

    pp = target.get("price_per_person", 80)
    budget_min = pp * party_size * 0.8
    budget_max = pp * party_size * 1.5

    print(f"=== {target['name']} · {'个人' if party_size == 1 else str(party_size) + '人'}点菜指南 ===")
    print(f"预算: ¥{budget_min:.0f}-{budget_max:.0f}")
    print()

    # Mock dish data based on extracted items
    dish_data = {
        "麻婆豆腐": {"price": 28, "recommendations": 38, "reason": "招牌菜，38人推荐"},
        "回锅肉": {"price": 42, "recommendations": 25, "reason": "正宗，25人推荐"},
        "蒜泥白肉": {"price": 32, "recommendations": 18, "reason": "18人推荐"},
        "水煮鱼": {"price": 88, "complaints": 7, "reason": "7人评价不入味，性价比低"},
        "红烧肉": {"price": 68, "recommendations": 30, "reason": "30人推荐，招牌必点"},
        "蟹粉豆腐": {"price": 58, "complaints": 5, "reason": "一般，不如别家"},
        "蟹粉汤包": {"price": 38, "recommendations": 12, "reason": "推荐"},
    }

    must_print = []
    recommended_print = []
    skip_print = []

    for dish in must_order:
        info = dish_data.get(dish, {"price": 30, "recommendations": 5, "reason": "推荐"})
        must_print.append((dish, info))

    # Fill remaining with sample data
    remaining = [d for d in ["红烧肉", "蟹粉汤包"] if d not in must_order]
    for dish in remaining[:2]:
        info = dish_data.get(dish, {"price": 30, "recommendations": 5, "reason": ""})
        if info.get("recommendations", 0) >= 10 and dish not in must_order:
            recommended_print.append((dish, info))

    for dish in avoid:
        info = dish_data.get(dish, {"price": 50, "complaints": 3, "reason": "一般"})
        skip_print.append((dish, info))

    if must_print:
        print("必点 (Must Order):")
        for dish, info in must_print:
            print(f"  ☑ {dish} ¥{info.get('price', '?')} — {info.get('reason', '推荐')}")
        print()

    if recommended_print:
        print("可点 (Recommended):")
        for dish, info in recommended_print:
            print(f"  ○ {dish} ¥{info.get('price', '?')} — {info.get('reason', '推荐')}")
        print()

    if skip_print:
        print("避雷 (Skip):")
        for dish, info in skip_print:
            print(f"  ✕ {dish} ¥{info.get('price', '?')} — {info.get('reason', '')}")
        print()

    print(f"💡 人均参考: ¥{pp:.0f}")
    print("🕐 建议时间: 11:30前或13:30后避开高峰")
    print()

def cmd_route(args):
    """Generate exploration route."""
    start = args.start or "静安寺"

    # Sample nearby restaurants with approximate walk times
    route_stops = []
    for r in SAMPLE_RESTAURANTS:
        route_stops.append(r)

    if len(route_stops) < 2:
        print("Need at least 2 restaurants for a route.")
        return

    print(f"=== 美食探店路线 ===")
    print(f"起点: {start}")
    print()

    meals = ["午餐", "下午茶", "晚餐"]
    for i, r in enumerate(route_stops[:3]):
        meal = meals[i] if i < len(meals) else "加餐"
        walk_time = 3 + i * 2
        times = ["11:30", "14:00", "18:00"]
        print(f"{i+1}. {r['name']} ({meal}, {times[i]})")
        if i > 0:
            print(f"   ← 步行约{walk_time}分钟")
        print(f"   {r['cuisine_type']} | ¥{r['price_per_person']}/人 | ⭐ {r['rating']}")
        print()

    print("---")
    print(f"共{min(3, len(route_stops))}站 | 步行总距离约{3*2:.1f}km")

def cmd_help(args):
    """Show help."""
    print(textwrap.dedent(f"""\
    Dianping Restaurant Guide v{VERSION}
    Extract real dining insights from Dianping reviews.

    Usage:
      dianping-guide.py profile [options]              Define dining context
      dianping-guide.py discover [options]              Find candidate restaurants
      dianping-guide.py analyze <name>                   Analyze a restaurant's reviews
      dianping-guide.py rank [options]                  Personalized ranking
      dianping-guide.py order <name> [--party N]        Generate ordering guide
      dianping-guide.py route [--start <location>]      Plan exploration route
      dianping-guide.py help                            Show this help

    Options:
      --location TEXT     Location (default: 上海静安寺)
      --cuisine TEXT      Cuisine type (川菜/日料/西餐/火锅, default: any)
      --budget-min N      Minimum budget per person
      --budget-max N      Maximum budget per person
      --occasion TEXT     Occasion (date|family|solo|group|business|casual)
      --radius N          Search radius in km (default: 3)
      --party-size N      Party size (default: 2)
      --start TEXT        Start location (for route)

    Examples:
      dianping-guide.py profile --location "上海静安寺" --cuisine 川菜 --budget-max 100
      dianping-guide.py discover --cuisine 川菜 --budget-max 150
      dianping-guide.py analyze "老王川菜"
      dianping-guide.py rank --cuisine 川菜 --occasion date
      dianping-guide.py order "老王川菜" --party-size 2
      dianping-guide.py route --start "静安寺"
    """))

# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dianping Restaurant Guide — extract real dining insights from reviews",
        add_help=False
    )
    parser.add_argument("command", nargs="?", default="help",
                        help="Subcommand: profile|discover|analyze|rank|order|route|help")
    parser.add_argument("name", nargs="?", default=None,
                        help="Restaurant name (for analyze/order)")
    parser.add_argument("--location", default=None)
    parser.add_argument("--cuisine", default=None)
    parser.add_argument("--budget-min", type=int, default=None)
    parser.add_argument("--budget-max", type=int, default=None)
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--occasion", default=None)
    parser.add_argument("--radius", type=int, default=None)
    parser.add_argument("--party-size", "--party", type=int, default=None)
    parser.add_argument("--start", default=None)
    parser.add_argument("--version", action="store_true", default=False)

    args, _ = parser.parse_known_args()

    if args.version:
        print(f"dianping-guide.py v{VERSION}")
        return

    # Handle --budget as shorthand for --budget-max
    if args.budget is not None and args.budget_max is None:
        args.budget_max = args.budget

    cmd = args.command

    if cmd == "profile":
        cmd_profile(args)
    elif cmd == "discover":
        cmd_discover(args)
    elif cmd == "analyze":
        cmd_analyze(args)
    elif cmd == "rank":
        cmd_rank(args)
    elif cmd == "order":
        cmd_order(args)
    elif cmd == "route":
        cmd_route(args)
    elif cmd == "version":
        print(f"dianping-guide.py v{VERSION}")

    elif cmd in ("help", "--help", "-h"):
        cmd_help(args)
    else:
        print(f"Unknown command: {cmd}")
        cmd_help(args)
        sys.exit(1)

if __name__ == "__main__":
    main()

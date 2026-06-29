#!/usr/bin/env python3
"""
同质化检测 — 检测Agent输出是否趋于同质

用法:
  python3 homogeneity_check.py --text "雨丝落在铝制窗框上" --history expressions.jsonl
  python3 homogeneity_check.py --file expressions.jsonl --field raw --stats
"""

import json
import re
import sys
import argparse
from collections import Counter
from pathlib import Path
from difflib import SequenceMatcher

DEFAULT_BANNED = {"雨丝", "窗棂", "霓虹", "灯火阑珊", "城市潜意识"}

TEMPLATE_PATTERNS = [
    (r'是.{1,6}的.{1,6}', "X是Y的Z"),
    (r'un-\w+ \w+', "un-X Y"),
    (r'.+—.+—', "X——Y——Z"),
    (r'不是.{1,10}而是.{1,10}', "不是X而是Y"),
]

def extract_imagery(text):
    images = set()
    for p in [r'[\u4e00-\u9fff]{2,4}(?:的|了|着|在|是)', r'[\u4e00-\u9fff]{2,4}(?:上|下|里|中|间)']:
        for m in re.findall(p, text):
            clean = re.sub(r'[的了着在是上下里中间]$', '', m)
            if len(clean) >= 2:
                images.add(clean)
    return images

def check_banned(text, banned=None):
    banned = banned or DEFAULT_BANNED
    return [w for w in banned if w in text]

def check_templates(text):
    return [name for pattern, name in TEMPLATE_PATTERNS if re.search(pattern, text)]

def check_similarity(text, history_texts, threshold=0.8):
    return [(SequenceMatcher(None, text, old).ratio(), old[:80]) for old in history_texts if SequenceMatcher(None, text, old).ratio() > threshold]

def check_imagery_overlap(text, history_texts, threshold=0.5):
    new_images = extract_imagery(text)
    if not new_images:
        return []
    overlaps = []
    for old in history_texts:
        old_images = extract_imagery(old)
        if not old_images:
            continue
        overlap = len(new_images & old_images) / max(len(new_images), 1)
        if overlap > threshold:
            overlaps.append((overlap, new_images & old_images))
    return overlaps

def compute_homogeneity(texts):
    if len(texts) < 2:
        return 0.0, {}
    all_words = Counter()
    for t in texts:
        all_words.update(re.findall(r'[\u4e00-\u9fff]{2,4}', t))
    total_words = sum(all_words.values())
    if total_words == 0:
        return 0.0, {}
    top10 = all_words.most_common(10)
    top10_ratio = sum(c for _, c in top10) / total_words
    all_images = set()
    for t in texts:
        all_images |= extract_imagery(t)
    diversity = len(all_images) / max(len(texts), 1)
    import random
    sample = random.sample(texts, min(100, len(texts)))
    sim_sum = 0
    sim_count = 0
    for i in range(len(sample)):
        for j in range(i+1, min(i+10, len(sample))):
            sim = SequenceMatcher(None, sample[i], sample[j]).ratio()
            sim_sum += sim
            sim_count += 1
    avg_sim = sim_sum / max(sim_count, 1)
    return avg_sim, {
        "total_texts": len(texts),
        "unique_words": len(all_words),
        "top10_words": top10,
        "top10_ratio": round(top10_ratio, 3),
        "image_diversity": round(diversity, 3),
        "avg_similarity": round(avg_sim, 3),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Output Homogeneity Checker")
    parser.add_argument("--text", help="Text to check")
    parser.add_argument("--file", help="JSONL file to analyze")
    parser.add_argument("--field", default="content", help="Field name in JSONL")
    parser.add_argument("--history", help="History JSONL file for single-text check")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args()

    if args.text and args.history:
        with open(args.history, "r") as f:
            history = [json.loads(l).get(args.field, "") for l in f if l.strip()]
        print("=== Banned Words ===")
        banned = check_banned(args.text)
        print(f"  Found: {banned}" if banned else "  Clean")
        print("\n=== Template Patterns ===")
        templates = check_templates(args.text)
        print(f"  Found: {templates}" if templates else "  Clean")
        print("\n=== Imagery Overlap ===")
        overlaps = check_imagery_overlap(args.text, history[-100:])
        for ratio, images in overlaps[:5]:
            print(f"  {ratio:.2f}: {images}")
    elif args.file:
        with open(args.file, "r") as f:
            texts = [json.loads(l).get(args.field, "") for l in f if l.strip()]
        if args.stats:
            score, stats = compute_homogeneity(texts)
            print(f"Homogeneity Score: {score:.3f} (0=diverse, 1=identical)")
            for k, v in stats.items():
                print(f"  {k}: {v}")
        else:
            for i, text in enumerate(texts[-20:]):
                banned = check_banned(text)
                templates = check_templates(text)
                if banned or templates:
                    print(f"[{i}] Issues: banned={banned} templates={templates}")
                    print(f"    {text[:80]}...")
    else:
        parser.print_help()

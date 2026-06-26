#!/usr/bin/env python3
"""
讲师文案风格定量分析器

分析结果直接写入SQLite，支持增量合并。
--save-sample 同时将输入文本保存到讲师样本目录（Write-Through: DB+文件系统）。

用法:
  python scripts/lecturer_analyzer.py --input sample.txt --lecturer 讲师A --data-dir ./控制台
  python scripts/lecturer_analyzer.py --input sample.txt --lecturer 讲师A --data-dir ./控制台 --save-sample
  python scripts/lecturer_analyzer.py --text "口播文案内容..." --lecturer 讲师A --data-dir ./控制台 --save-sample
  python scripts/lecturer_analyzer.py --input s1.txt s2.txt --lecturer 讲师A --merge --save-sample
  echo "口播文案内容..." | python scripts/lecturer_analyzer.py --lecturer 讲师A --stdin --data-dir ./控制台 --save-sample
"""

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.core.text_utils import count_chinese_chars, split_sentences, chunk_text, extract_keywords
from scripts.core.db_manager import DatabaseManager, resolve_db_path
from scripts.core.lecturer_service import LecturerService

STOP_WORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
    "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有",
    "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些", "什么",
    "怎么", "如何", "为什么", "可以", "能", "得", "地", "把", "被", "让",
])

_seg_mode = "jieba"


def load_text(file_path: str) -> str:
    p = Path(file_path)
    if not p.exists():
        print(f"错误: 文件不存在 - {file_path}", file=sys.stderr)
        sys.exit(1)
    try:
        return p.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        return p.read_text(encoding="gbk").strip()


def segment_chinese(text: str) -> list:
    global _seg_mode
    try:
        import jieba
        _seg_mode = "jieba"
        return [w for w in jieba.cut(text) if w.strip()]
    except ImportError:
        _seg_mode = "fallback"
        print("WARNING: jieba未安装，使用单字分词模式", file=sys.stderr)
        return re.findall(r'[\u4e00-\u9fff]', text)


def analyze_word_frequency(text: str, top_n: int = 30) -> list:
    words = segment_chinese(text)
    if _seg_mode == "fallback":
        filtered = [w for w in words if w not in STOP_WORDS]
    else:
        filtered = [w for w in words if w not in STOP_WORDS and len(w) >= 2]
    return [{"word": w, "count": c} for w, c in Counter(filtered).most_common(top_n)]


def analyze_bigrams(text: str, top_n: int = 20) -> list:
    words = segment_chinese(text)
    if _seg_mode == "fallback":
        filtered = [w for w in words if w not in STOP_WORDS]
    else:
        filtered = [w for w in words if w not in STOP_WORDS and len(w.strip()) > 0]
    bc = Counter()
    for i in range(len(filtered) - 1):
        bg = filtered[i] + filtered[i + 1]
        min_len = 2 if _seg_mode == "fallback" else 3
        if len(bg) >= min_len:
            bc[bg] += 1
    return [{"phrase": p, "count": c} for p, c in bc.most_common(top_n)]


def analyze_punctuation(text: str) -> dict:
    punct_map = {
        "comma": r'[，,]', "period": r'[。.]', "question": r'[？?]',
        "exclamation": r'[！!]', "ellipsis": r'[………]', "dash": r'[——–—]',
    }
    counts = {}
    total = 0
    for name, pat in punct_map.items():
        c = len(re.findall(pat, text))
        counts[name] = c
        total += c
    ratios = {k: round(v / total, 4) for k, v in counts.items()} if total > 0 else {}
    return {"counts": counts, "ratios": ratios, "total": total,
            "question_ratio": ratios.get("question", 0),
            "exclamation_ratio": ratios.get("exclamation", 0)}


def analyze_rhetorical(sentences: list) -> dict:
    if not sentences:
        return {"question_ratio": 0, "exclamation_ratio": 0, "statement_ratio": 1, "total": 0}
    q = sum(1 for s in sentences if re.search(r'[？?]', s))
    e = sum(1 for s in sentences if re.search(r'[！!]', s))
    t = len(sentences)
    return {"question_count": q, "question_ratio": round(q / t, 4),
            "exclamation_count": e, "exclamation_ratio": round(e / t, 4),
            "statement_ratio": round((t - q - e) / t, 4), "total": t}


def analyze_sentence_length(sentences: list) -> dict:
    lengths = [count_chinese_chars(s) for s in sentences if count_chinese_chars(s) > 0]
    if not lengths:
        return {"avg": 0, "median": 0, "min": 0, "max": 0, "stdev": 0}
    dist = {"short_1_10": 0, "medium_11_20": 0, "long_21_35": 0, "very_long_36_plus": 0}
    for l in lengths:
        if l <= 10: dist["short_1_10"] += 1
        elif l <= 20: dist["medium_11_20"] += 1
        elif l <= 35: dist["long_21_35"] += 1
        else: dist["very_long_36_plus"] += 1
    total = len(lengths)
    return {"avg": round(statistics.mean(lengths), 2),
            "median": round(statistics.median(lengths), 2),
            "min": min(lengths), "max": max(lengths),
            "stdev": round(statistics.stdev(lengths), 2) if len(lengths) > 1 else 0,
            "distribution_counts": dist,
            "distribution_ratios": {k: round(v / total, 4) for k, v in dist.items()}}


def analyze_connectors(text: str) -> dict:
    groups = {
        "causal": ["因为", "所以", "因此", "导致"],
        "transitional": ["然后", "接着", "接下来", "其次", "另外"],
        "contrastive": ["但是", "然而", "不过", "可是"],
        "exemplification": ["比如", "例如", "像", "比如说"],
        "summative": ["总之", "总的来说", "综上", "总结一下"],
    }
    result = {}
    for cat, words in groups.items():
        result[cat] = {"count": sum(text.count(w) for w in words),
                        "connectors_used": [w for w in words if text.count(w) > 0]}
    return result


def analyze_vocabulary(text: str) -> dict:
    words = segment_chinese(text)
    filtered = [w for w in words if w not in STOP_WORDS and len(w.strip()) > 0]
    if not filtered:
        return {"ttr": 0, "total_tokens": 0, "unique_types": 0}
    return {"ttr": round(len(set(filtered)) / len(filtered), 4),
            "total_tokens": len(filtered), "unique_types": len(set(filtered))}


def analyze_texts(texts: list) -> dict:
    combined = "\n".join(texts)
    total_chinese = count_chinese_chars(combined)
    if total_chinese == 0:
        print("WARNING: 输入文本不含中文字符", file=sys.stderr)

    all_sents = []
    for t in texts:
        all_sents.extend(split_sentences(t))

    return {
        "metadata": {"analysis_version": "2.0", "segmentation_mode": _seg_mode,
                      "source_count": len(texts)},
        "basic_stats": {"total_chinese_chars": total_chinese,
                         "total_chars": len(re.sub(r'\s', '', combined)),
                         "total_sentences": len(all_sents)},
        "sentence_length": analyze_sentence_length(all_sents),
        "word_frequency": analyze_word_frequency(combined),
        "bigrams": analyze_bigrams(combined),
        "punctuation": analyze_punctuation(combined),
        "vocabulary_diversity": analyze_vocabulary(combined),
        "rhetorical_patterns": analyze_rhetorical(all_sents),
        "connector_patterns": analyze_connectors(combined),
        "opening_patterns": all_sents[:3] if len(all_sents) >= 3 else all_sents,
        "closing_patterns": all_sents[-3:] if len(all_sents) >= 3 else all_sents,
    }


def main():
    parser = argparse.ArgumentParser(description="讲师风格分析器")
    parser.add_argument("--input", nargs="+", help="样本文件路径（支持多文件）")
    parser.add_argument("--text", help="直接传入文本")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取文本（适用于长文本）")
    parser.add_argument("--lecturer", required=True, help="讲师ID")
    parser.add_argument("--data-dir", default=None, help="控制台目录路径（推导数据库路径用）")
    parser.add_argument("--merge", action="store_true", help="增量合并到已有画像")
    parser.add_argument("--save-sample", action="store_true",
                        help="同时将输入文本保存为样本（Write-Through: DB+文件系统）")
    parser.add_argument("--output", default=None, help="同时输出到JSON文件")
    args = parser.parse_args()

    if sum([bool(args.input), bool(args.text), args.stdin]) != 1:
        parser.error("需要且仅需要 --input、--text 或 --stdin 之一")

    # 收集文本
    texts = []
    source_labels = []
    if args.input:
        for f in args.input:
            texts.append(load_text(f))
            source_labels.append(Path(f).name)
    if args.text:
        texts.append(args.text.strip())
        source_labels.append("direct_input")
    if args.stdin:
        stdin_text = sys.stdin.read().strip()
        if not stdin_text:
            parser.error("--stdin 读取到空文本")
        texts.append(stdin_text)
        source_labels.append("stdin")

    # 字数校验
    total_cn = sum(count_chinese_chars(t) for t in texts)
    if total_cn == 0:
        print("WARNING: 文本不含中文字符", file=sys.stderr)
    elif total_cn < 200:
        print(f"WARNING: 文本较少（{total_cn}字），建议200字以上", file=sys.stderr)

    # 分析
    result = analyze_texts(texts)

    # 输出到文件
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # 写入数据库
    try:
        resolved_db = resolve_db_path(None, args.data_dir)
    except ValueError as e:
        result["db_status"] = {"status": "error", "message": str(e)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    db = DatabaseManager(resolved_db)
    svc = LecturerService(db, data_dir=args.data_dir)

    # --save-sample: 将输入文本保存为样本（Write-Through: DB+文件系统）
    was_placeholder = False
    if args.save_sample and args.data_dir:
        existing_check = svc.get_profile(args.lecturer)
        if not existing_check:
            # 创建占位讲师记录以满足外键约束，Step 3 的 add_lecturer 会覆盖此占位
            svc.add_lecturer(args.lecturer, {"lecturer_name": args.lecturer, "_placeholder": True})
            was_placeholder = True
        saved = []
        samples_dir = Path(args.data_dir) / "讲师列表" / args.lecturer / "样本"
        for i, (text, label) in enumerate(zip(texts, source_labels)):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            sample_name = f"sample_{ts}_{i+1}.txt" if len(texts) > 1 else f"sample_{ts}.txt"
            # 如果输入文件已在样本目录内，rename 而非重新创建
            if args.input and i < len(args.input):
                input_path = Path(args.input[i]).resolve()
                if samples_dir.exists() and str(input_path).startswith(str(samples_dir.resolve())):
                    dest = samples_dir / sample_name
                    input_path.rename(dest)
                    # 仅注册 DB，不再写文件
                    now = datetime.now().isoformat(timespec="seconds")
                    svc.db.execute(
                        "INSERT INTO lecturer_samples (lecturer_id, sample_name, content, is_reference, added_at) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (args.lecturer, sample_name, text, 0, now),
                    )
                    svc.db.commit()
                    saved.append({"sample_name": sample_name, "chars": len(text), "source": label, "method": "renamed"})
                    continue
            svc.add_sample(args.lecturer, sample_name, text)
            saved.append({"sample_name": sample_name, "chars": len(text), "source": label, "method": "created"})
        result["sample_saved"] = saved
    elif args.save_sample and not args.data_dir:
        result["sample_saved"] = {"status": "skipped", "reason": "需要 --data-dir 才能保存样本"}

    existing = svc.get_profile(args.lecturer)

    # 合并逻辑：占位讲师视为"不存在"，不干扰 merge_status 判断
    real_existing = existing and not existing.get("_placeholder")
    if real_existing and args.merge:
        # 增量合并
        merge_result = svc.weighted_merge(args.lecturer, result, len(texts))
        result["merge_status"] = merge_result
    elif real_existing:
        result["merge_status"] = {"status": "skipped", "reason": "已有画像，使用--merge进行增量合并"}
    else:
        # 首次创建：智能体负责构建完整profile并写入
        result["merge_status"] = {"status": "new", "lecturer_id": args.lecturer,
                                   "hint": "首次分析，智能体需构建完整profile后调用db_query写入"}

    db.close()

    result["lecturer_id"] = args.lecturer
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()

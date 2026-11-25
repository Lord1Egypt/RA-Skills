#!/usr/bin/env python3
"""
自动进化特征规则脚本

用途：
- 在每次挖掘完成后运行
- 分析信号覆盖缺口（signal-poor 对话）
- 从未覆盖的对话中提取新关键词/模式
- 自动更新 scenes/{scene}.yaml 的 feature_rules
- 记录进化历史

设计原则：
- Layer 1: 统计缺口检测（无 LLM，纯统计，速度快）
- Layer 2: 模式发现（可选 LLM，深度分析）
- Layer 3: 自动更新 YAML + 记录历史
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def load_scene_config(scene: str) -> Dict[str, Any]:
    import yaml
    skill_dir = os.path.dirname(SCRIPT_DIR)
    # Check both pe-self-improving and dialog-discovery for the scenes dir
    for parent in [os.path.join(skill_dir, "..", "pe-self-improving"), skill_dir]:
        path = os.path.join(parent, "scenes", f"{scene}.yaml")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    raise FileNotFoundError(f"Scene config not found: {scene}")


def save_scene_config(config: Dict[str, Any], scene: str) -> str:
    import yaml
    skill_dir = os.path.dirname(SCRIPT_DIR)
    for parent in [os.path.join(skill_dir, "..", "pe-self-improving"), skill_dir]:
        path = os.path.join(parent, "scenes", f"{scene}.yaml")
        if os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            return path
    raise FileNotFoundError(f"Scene config not found: {scene}")


def get_all_existing_keywords(feature_rules: Dict[str, Any]) -> Set[str]:
    """提取所有现有关键词"""
    all_kw = set()
    for rule_name, rule_cfg in feature_rules.items():
        if isinstance(rule_cfg, dict) and "keywords" in rule_cfg:
            for kw in rule_cfg["keywords"]:
                all_kw.add(kw)
        # Also handle nested dicts (stage_keywords, compliance_keywords, etc.)
        if isinstance(rule_cfg, dict):
            for sub_name, sub_cfg in rule_cfg.items():
                if isinstance(sub_cfg, dict) and "keywords" in sub_cfg:
                    for kw in sub_cfg["keywords"]:
                        all_kw.add(kw)
    return all_kw


def extract_meaningful_phrases(text: str) -> List[str]:
    """
    提取有意义的多字短语（非简单 ngram 切分）
    
    策略：基于标点和角色标记的断句，提取完整语义片段
    """
    # Split on punctuation, role markers, and common delimiters
    segments = re.split(r'[，。！？；：、,\.!?;:\s]+', text)
    phrases = []
    for seg in segments:
        seg = seg.strip()
        # Filter: 2-8 chars, not pure filler, not ASR artifact
        if 2 <= len(seg) <= 8:
            # Skip if it's mostly single-char particles
            if not re.match(r'^[嗯啊哦呃诶额了着过的得]+$', seg):
                # Skip ASR artifacts
                if not any(w in seg for w in ['用户', '未说话', '机器人', '客服']):
                    phrases.append(seg)
    return phrases


def extract_ngrams(text: str, n: int = 2) -> List[str]:
    """提取中文 bigrams"""
    # Remove punctuation and whitespace
    text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    if len(text) < n:
        return []
    return [text[i:i+n] for i in range(len(text) - n + 1)]


def extract_trigrams(text: str) -> List[str]:
    """提取中文 trigrams"""
    text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    if len(text) < 3:
        return []
    return [text[i:i+3] for i in range(len(text) - 2)]


def classify_dialog_signal_strength(result: Dict[str, Any]) -> str:
    """评估对话的信号强度"""
    signals = result.get("signals", {})
    pos = len(signals.get("positive", []))
    neg = len(signals.get("negative", []))
    risk = len(signals.get("risk", []))
    total = pos + neg + risk

    if total == 0:
        return "signal_empty"
    if total <= 1:
        return "signal_sparse"
    if total <= 3:
        return "signal_moderate"
    return "signal_rich"


def find_signal_poor_dialogs(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """找出信号稀疏的对话（Layer 1 输入）"""
    poor = []
    for r in results:
        strength = classify_dialog_signal_strength(r)
        if strength in ("signal_empty", "signal_sparse"):
            poor.append(r)
    return poor


def find_uncovered_dialogs(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """找出特征未覆盖的对话 - 更宽泛的策略
    
    策略：从 bad_seed 中找用户有实质内容但现有规则没匹配到的对话
    这些是优化 ROI 最高的对象
    """
    uncovered = []
    for r in results:
        dialog = r.get("dialog", {})
        user_text = dialog.get("user_text", "")
        features = r.get("features", {})
        signals = r.get("signals", {})
        
        # Count substantial user content (exclude filler and ASR artifacts)
        clean_user = re.sub(r'[嗯啊哦呃诶额，。！？\s：；、]+', '', user_text)
        clean_user = re.sub(r'用户未说话', '', clean_user)
        user_substantial = len(clean_user)
        
        # Only look at dialogs where user has real content
        if user_substantial < 10:
            continue
        
        # Check which existing features didn't fire
        user_features_fired = 0
        for feat_name in ["explicit_rejection", "conversation_rejection", "product_objection", 
                          "busy_hits", "question_hits", "explicit_interest", 
                          "explicit_acceptance", "negative_emotion", "terminal_hits"]:
            val = features.get(feat_name, [])
            if isinstance(val, list) and len(val) > 0:
                user_features_fired += 1
            elif isinstance(val, bool) and val:
                user_features_fired += 1
        
        # User has content but few features fired = uncovered
        if user_features_fired <= 1:
            uncovered.append(r)
    
    return uncovered


def find_gray_dialogs(results: List[Dict], min_confidence: float = 0.7) -> List[Dict[str, Any]]:
    """找出灰区对话（Layer 2 输入）"""
    return [
        r for r in results
        if r.get("seed_label", "").startswith("gray")
        and r.get("scores", {}).get("confidence", 0) < min_confidence
    ]


def extract_candidate_keywords_from_texts(
    texts: List[str],
    existing_keywords: Set[str],
    min_freq: int = 3,
    min_len: int = 2,
    max_len: int = 6,
    scene_config: Dict[str, Any] = None,
) -> List[Tuple[str, int]]:
    """
    从文本中提取候选关键词（不在现有词表中的高频词）
    
    策略：优先用语义短语（按标点断句），ngram 作为补充
    """
    # Common filler/stop words to exclude
    stop_words = {
        "的话", "那个", "就是", "然后", "可以", "一下", "一个", "没有",
        "这个", "什么", "因为", "所以", "如果", "但是", "而且", "或者",
        "已经", "时候", "现在", "这样", "那样", "怎么", "为什么",
        "他们", "我们", "你们", "自己", "不是", "也是", "还有",
        "可能", "应该", "需要", "知道", "觉得", "认为", "表示",
        "的时候", "的话", "的一", "的是", "的就", "的就是",
    }

    scene_config = scene_config or {}
    # ASR artifact patterns to exclude (not real conversation signals)
    asr_artifacts = {
        "用户", "客服", "机器人", "未说", "说话", "用户未", "户未说",
        "未说话", "用户未说", "户未说话", "话用", "未说话",
        "户未", "说话用", "话用户", "说话用户", "话用户未",
        "嗯嗯", "嗯我", "话嗯", "说话嗯",
    }

    # Common business words that aren't useful as discriminative features
    # 场景无关的通用停用词
    business_stop_words = {
        "咱们", "这边", "打扰", "您了", "我这", "工号", "客户经理",
        "的时候", "平时", "一下您", "是咱们",
    }
    # 场景特定停用词从场景配置读取
    scene_stop_words = set(scene_config.get("feature_extraction", {}).get("stop_words", []))
    business_stop_words.update(scene_stop_words)

    # === Strategy 1: Extract meaningful short phrases from user utterances ===
    phrase_counter = Counter()
    for utt in texts:
        utt = utt.strip()
        # Clean role markers
        utt = re.sub(r'^(用户|客户)[:：]?\s*', '', utt)
        utt = re.sub(r'(用户未说话|用户未说话)', '', utt)
        utt = utt.strip()
        # Take short meaningful utterances (2-12 chars)
        if 2 <= len(utt) <= 12 and utt not in existing_keywords:
            # Filter: must have Chinese chars
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', utt))
            if cn_chars >= 2:
                # Filter: not pure filler
                if not re.match(r'^[嗯啊哦呃诶额了着过的得]+$', utt):
                    # Filter: not ASR artifact
                    if not any(a in utt for a in ['用户', '未说话', '机器人', '客服', 'dialed', 'busy', 'hold']):
                        phrase_counter[utt] += 1
    
    # === Strategy 2: Extract keyword phrases from agent text (for new signal detection) ===
    agent_phrase_counter = Counter()
    for utt in texts:
        utt = utt.strip()
        utt = re.sub(r'^(机器人|客服|坐席)[:：]?\s*', '', utt)
        utt = utt.strip()
        if 3 <= len(utt) <= 15 and utt not in existing_keywords:
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', utt))
            if cn_chars >= 3:
                agent_phrase_counter[utt] += 1

    # Merge phrases (user phrases have priority)
    candidates = Counter()
    for phrase, freq in phrase_counter.items():
        if freq >= min_freq and phrase not in stop_words and phrase not in asr_artifacts and phrase not in business_stop_words:
            candidates[phrase] = freq

    # Deduplicate: if longer phrase exists, remove shorter substrings
    sorted_candidates = sorted(candidates.items(), key=lambda x: (-len(x[0]), -x[1]))
    final = []
    seen_substrings = set()
    for phrase, freq in sorted_candidates:
        is_substring = any(phrase in s for s in seen_substrings if len(s) > len(phrase))
        if not is_substring:
            final.append((phrase, freq))
            seen_substrings.add(phrase)

    # Also add top agent phrases separately
    agent_final = []
    for phrase, freq in agent_phrase_counter.most_common(20):
        if freq >= min_freq and phrase not in stop_words and phrase not in asr_artifacts and phrase not in business_stop_words:
            agent_final.append((phrase, freq))

    return final[:50], agent_final[:20]

    bigram_counter = Counter()
    trigram_counter = Counter()
    fourgram_counter = Counter()
    phrase_counter = Counter()  # New: semantic phrase counter

    for text in texts:
        # Extract meaningful phrases (preferred over ngrams)
        phrase_counter.update(extract_meaningful_phrases(text))
        
        # Also extract ngrams as fallback
        bigram_counter.update(extract_ngrams(text, 2))
        trigram_counter.update(extract_trigrams(text))
        text_clean = re.sub(r'[^\u4e00-\u9fff]', '', text)
        if len(text_clean) >= 4:
            fourgram_counter.update([text_clean[i:i+4] for i in range(len(text_clean) - 3)])

    # Merge and filter - phrases get priority
    candidates = Counter()
    
    # Add phrases first (they're higher quality)
    for phrase, freq in phrase_counter.items():
        if freq >= min_freq and len(phrase) >= min_len and phrase not in existing_keywords and phrase not in stop_words and phrase not in asr_artifacts and phrase not in business_stop_words:
            candidates[phrase] = freq
    
    # Add ngrams only if not already covered by a phrase
    existing_phrase_strs = set(candidates.keys()) | existing_keywords
    for ngram, freq in bigram_counter.items():
        if freq >= min_freq and len(ngram) >= min_len and ngram not in existing_phrase_strs and ngram not in stop_words and ngram not in asr_artifacts and ngram not in business_stop_words:
            # Skip if this ngram is a substring of an existing phrase
            if not any(ngram in p for p in existing_phrase_strs if len(p) > len(ngram)):
                candidates[ngram] = freq
    for ngram, freq in trigram_counter.items():
        if freq >= min_freq and ngram not in existing_phrase_strs and ngram not in stop_words and ngram not in asr_artifacts and ngram not in business_stop_words:
            if not any(ngram in p for p in existing_phrase_strs if len(p) > len(ngram)):
                candidates[ngram] = freq
    for ngram, freq in fourgram_counter.items():
        if freq >= min_freq and ngram not in existing_phrase_strs and ngram not in stop_words and ngram not in asr_artifacts and ngram not in business_stop_words:
            if not any(ngram in p for p in existing_phrase_strs if len(p) > len(ngram)):
                candidates[ngram] = freq

    # Deduplicate: if "还款方式" exists, remove "还款" and "款方" if they're substrings
    sorted_candidates = sorted(candidates.items(), key=lambda x: -x[1])
    final = []
    seen_substrings = set()
    for ngram, freq in sorted_candidates:
        # Skip if it's a substring of an already accepted longer candidate
        is_substring = any(ngram in s for s in seen_substrings if len(s) > len(ngram))
        if not is_substring:
            final.append((ngram, freq))
            seen_substrings.add(ngram)

    return final[:50]  # Top 50 candidates


def categorize_keyword(keyword: str, feature_rules: Dict[str, Any]) -> str:
    """尝试将关键词归入现有类别"""
    # Define category matching heuristics
    category_hints = {
        "user_refusal": ["不用", "不要", "不需要", "算了", "不借", "不弄"],
        "user_busy": ["忙", "开会", "没空", "不方便", "上班"],
        "user_interest": ["额度", "利息", "借", "还款", "怎么看", "怎么借"],
        "user_negative_emotion": ["烦", "骚扰", "骗", "挂了", "别打"],
        "user_terminal": ["挂了", "再见", "就这样", "别打了"],
        "agent_forbidden": ["保证", "一定", "肯定", "绝对"],
    }

    for category, hint_words in category_hints.items():
        if any(h in keyword for h in hint_words):
            return category
    return ""


def suggest_new_category(keyword: str, freq: int) -> Dict[str, Any]:
    """为无法归入现有类别的关键词建议新类别"""
    # Heuristic category suggestions based on content
    if any(w in keyword for w in ["还款", "还钱", "提前还", "违约", "逾期"]):
        return {"category": "user_question_repayment", "description": "还款相关提问/顾虑"}
    if any(w in keyword for w in ["征信", "信用", "上征信", "影响"]):
        return {"category": "user_question_credit", "description": "征信/信用相关顾虑"}
    if any(w in keyword for w in ["安全", "骗子", "诈骗", "正规", "靠谱"]):
        return {"category": "user_question_safety", "description": "安全/正规性顾虑"}
    if any(w in keyword for w in ["提额", "降息", "涨额度", "调额度"]):
        return {"category": "user_interest_upgrade", "description": "提额降息相关"}
    if any(w in keyword for w in ["操作", "怎么弄", "不会", "找不到", "搜不到"]):
        return {"category": "user_operation_difficulty", "description": "操作困难/不会用"}
    if any(w in keyword for w in ["学生", "老人", "退休", "小孩"]):
        return {"category": "user_special_identity", "description": "特殊身份声明"}
    return {"category": "uncategorized", "description": f"未分类高频词({keyword})"}


def auto_evolve_layer1(
    results: List[Dict[str, Any]],
    feature_rules: Dict[str, Any],
    scene: str,
    scene_config: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Layer 1: 统计缺口检测
    - 找信号稀疏的对话
    - 提取新关键词
    - 自动补入现有类别或建议新类别
    """
    existing_keywords = get_all_existing_keywords(feature_rules)

    # 1. Find signal-poor dialogs AND uncovered dialogs
    poor_dialogs = find_signal_poor_dialogs(results)
    gray_dialogs = find_gray_dialogs(results)
    uncovered_dialogs = find_uncovered_dialogs(results)
    
    target_dialogs = poor_dialogs + gray_dialogs + uncovered_dialogs

    # Deduplicate by dialog_id
    seen_ids = set()
    unique_dialogs = []
    for d in target_dialogs:
        did = d.get("dialog_id", "")
        if did not in seen_ids:
            seen_ids.add(did)
            unique_dialogs.append(d)

    if not unique_dialogs:
        return {
            "layer": 1,
            "status": "no_signal_poor_dialogs",
            "additions": [],
            "new_categories": [],
        }

    # 2. Extract texts from these dialogs - use turn-level data for better quality
    user_utterances = []
    agent_utterances = []
    for d in unique_dialogs:
        dialog = d.get("dialog", {})
        turns = dialog.get("turns", [])
        for t in turns:
            text = t.get("text", "").strip()
            role = t.get("role", "")
            # Filter out ASR artifacts and fillers
            if '用户未说话' in text or '未说话' in text:
                continue
            if re.match(r'^[嗯啊哦呃诶额]+$', text):
                continue
            if role == "user" and len(text) >= 2:
                user_utterances.append(text)
            elif role == "agent" and len(text) >= 3:
                agent_utterances.append(text)

    # 3. Extract candidate keywords
    user_candidates, agent_candidates = extract_candidate_keywords_from_texts(user_utterances, existing_keywords, min_freq=2, scene_config=scene_config)

    # 4. Categorize and build additions
    additions = []  # Keywords to add to existing categories
    new_categories = []  # Suggestions for new categories

    for keyword, freq in user_candidates:
        existing_cat = categorize_keyword(keyword, feature_rules)
        if existing_cat:
            additions.append({
                "keyword": keyword,
                "frequency": freq,
                "target_category": existing_cat,
                "type": "user",
                "action": "add_to_existing",
            })
        else:
            new_cat = suggest_new_category(keyword, freq)
            new_categories.append({
                "keyword": keyword,
                "frequency": freq,
                "suggested_category": new_cat["category"],
                "description": new_cat["description"],
                "type": "user",
                "action": "suggest_new_category",
            })

    for keyword, freq in agent_candidates:
        existing_cat = categorize_keyword(keyword, feature_rules)
        if existing_cat:
            additions.append({
                "keyword": keyword,
                "frequency": freq,
                "target_category": existing_cat,
                "type": "agent",
                "action": "add_to_existing",
            })

    return {
        "layer": 1,
        "status": "completed",
        "signal_poor_count": len(poor_dialogs),
        "gray_count": len(gray_dialogs),
        "uncovered_count": len(uncovered_dialogs),
        "analyzed_count": len(unique_dialogs),
        "additions": additions,
        "new_categories": new_categories,
        "user_candidates_top10": user_candidates[:10],
        "agent_candidates_top10": agent_candidates[:10],
    }


def apply_additions_to_config(
    config: Dict[str, Any],
    additions: List[Dict[str, Any]],
    new_categories: List[Dict[str, Any]],
    auto_apply: bool = True,
) -> Dict[str, Any]:
    """将提取的关键词应用到场景配置"""
    feature_rules = config.setdefault("feature_rules", {})
    applied = []
    skipped = []

    # Apply additions to existing categories
    for add in additions:
        cat = add["target_category"]
        kw = add["keyword"]

        if cat in feature_rules and isinstance(feature_rules[cat], dict):
            keywords = feature_rules[cat].setdefault("keywords", [])
            if kw not in keywords:
                if auto_apply:
                    keywords.append(kw)
                    applied.append(add)
                else:
                    skipped.append(add)

    # Apply new categories (only if auto_apply)
    for nc in new_categories:
        cat_name = nc["suggested_category"]
        kw = nc["keyword"]

        if cat_name not in feature_rules:
            if auto_apply:
                feature_rules[cat_name] = {
                    "keywords": [kw],
                    "description": nc["description"],
                }
                applied.append(nc)
            else:
                skipped.append(nc)
        else:
            keywords = feature_rules[cat_name].setdefault("keywords", [])
            if kw not in keywords:
                if auto_apply:
                    keywords.append(kw)
                    applied.append(nc)
                else:
                    skipped.append(nc)

    return {
        "applied": applied,
        "skipped": skipped,
        "applied_count": len(applied),
        "skipped_count": len(skipped),
    }


def write_evolution_log(
    scene: str,
    layer1_result: Dict[str, Any],
    apply_result: Dict[str, Any],
    output_dir: str,
) -> str:
    """记录进化历史"""
    os.makedirs(output_dir, exist_ok=True)
    log_path = os.path.join(output_dir, f"evolution-log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
    log = {
        "scene": scene,
        "timestamp": datetime.now().isoformat(),
        "layer1": layer1_result,
        "apply_result": apply_result,
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return log_path


def main():
    parser = argparse.ArgumentParser(description="自动进化特征规则")
    parser.add_argument("--input", required=True, help="挖掘结果 JSON")
    parser.add_argument("--scene", required=True, help="场景")
    parser.add_argument("--auto-apply", action="store_true", default=True, help="自动应用变更（默认开启）")
    parser.add_argument("--dry-run", action="store_true", help="只分析不写入")
    parser.add_argument("--log-dir", default=None, help="进化日志目录")
    args = parser.parse_args()

    # Load match results
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data.get("results", [])

    # Load scene config
    config = load_scene_config(args.scene)
    feature_rules = config.get("feature_rules", {})

    # Layer 1: Statistical gap detection
    print("🔍 Layer 1: 统计缺口检测...")
    layer1 = auto_evolve_layer1(results, feature_rules, args.scene, scene_config=config)

    print(f"   信号稀疏对话: {layer1.get('signal_poor_count', 0)} 条")
    print(f"   灰区对话: {layer1.get('gray_count', 0)} 条")
    print(f"   特征未覆盖对话: {layer1.get('uncovered_count', 0)} 条")
    print(f"   可补入现有类别: {len(layer1.get('additions', []))} 个关键词")
    print(f"   建议新类别: {len(layer1.get('new_categories', []))} 个")

    if layer1.get("user_candidates_top10"):
        print(f"\n   用户侧 TOP10 候选短语:")
        for kw, freq in layer1["user_candidates_top10"]:
            # Only show phrases with Chinese chars >= 2 (skip ngram fragments)
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', kw))
            if cn_chars >= 2:
                print(f"     '{kw}' ({freq}次)")

    if layer1.get("agent_candidates_top10"):
        print(f"\n   机器人侧 TOP10 候选短语:")
        for kw, freq in layer1["agent_candidates_top10"]:
            cn_chars = len(re.findall(r'[\u4e00-\u9fff]', kw))
            if cn_chars >= 2:
                print(f"     '{kw}' ({freq}次)")

    # Apply changes
    if not args.dry_run and (layer1.get("additions") or layer1.get("new_categories")):
        print("\n✏️ 应用变更到场景配置...")
        apply_result = apply_additions_to_config(
            config,
            layer1.get("additions", []),
            layer1.get("new_categories", []),
            auto_apply=args.auto_apply,
        )
        print(f"   已应用: {apply_result['applied_count']} 项")
        print(f"   已跳过: {apply_result['skipped_count']} 项")

        # Save updated config
        config_path = save_scene_config(config, args.scene)
        print(f"   配置已更新: {config_path}")

        # Write evolution log
        log_dir = args.log_dir or os.path.expanduser(f"~/pe-self-improving/memory/{args.scene}/warm/evidence")
        log_path = write_evolution_log(args.scene, layer1, apply_result, log_dir)
        print(f"   进化日志: {log_path}")
    else:
        apply_result = {"applied_count": 0, "skipped_count": 0, "applied": [], "skipped": []}
        if args.dry_run:
            print("\n⚠️ Dry run 模式，未写入变更")

    # Summary
    print(f"\n✅ 自动进化完成")
    print(f"   Layer 1: 发现 {len(layer1.get('additions', []))} 个可补充关键词 + {len(layer1.get('new_categories', []))} 个新类别建议")
    print(f"   已应用: {apply_result['applied_count']} 项变更")


if __name__ == "__main__":
    main()

"""
BiliYouTik2Brain — 模糊音混淆矩阵 (Phase 4.1)

三級记录：实例级 → 规律级 → 领域通用级
核心原则：记"题型"不记"题目"。从实例提炼规律，举一反三。

存储位置：~/.biliyoutik2brain_fuzzy.json

数据模型：
  {
    "instances": [            // 实例级：具体的 whiper 误认案例
      {wrong, right, speaker, domain, video_title, timestamp, context_before, context_after}
    ],
    "rules": [                // 规律级：从实例提炼的规律
      {pattern, domain, confidence, tags, source_instances, rules_derived_from}
    ],
    "domain_stats": {         // 领域通用：按领域的统计规律
      "trading": {
        "common_mistakes": ["错→对", ...],
        "syllable_groups": {"入声": ["入声→入市", "入声→入参"], ...},
        "tone_patterns": [...]
      }
    }
  }
"""

import os, json, time, re, math
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

STORAGE_FILE = os.path.expanduser("~/.biliyoutik2brain_fuzzy.json")

_INSTANCE_MAX = 500      # 最大实例数
_RULE_MAX = 100           # 最大规律数


# ═══════════════════════════════════════════════════════════════
# 存储
# ═══════════════════════════════════════════════════════════════

def _load() -> Dict:
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return _empty_db()
    return _empty_db()


def _empty_db() -> Dict:
    return {
        "instances": [],
        "rules": [],
        "domain_stats": {},
        "last_consolidated": "",
    }


def _save(db: Dict):
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# 1. 实例级：记录具体误认
# ═══════════════════════════════════════════════════════════════

def add_instance(
    wrong: str,
    right: str,
    speaker: str = "",
    domain: str = "",
    video_title: str = "",
    context_before: str = "",
    context_after: str = "",
):
    """记录一条 whisper 误认实例
    
    记"题型"不记"题目"：实例会后续被提炼为规律，
    真正起作用的是规律，实例只是素材。
    """
    if not wrong or not right or wrong == right:
        return
    
    db = _load()
    
    instance = {
        "wrong": wrong,
        "right": right,
        "speaker": speaker,
        "domain": domain,
        "video_title": video_title,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "context_before": context_before[:60] if context_before else "",
        "context_after": context_after[:60] if context_after else "",
    }
    
    # 去重：同一 wrong→right 在同一领域不重复记
    for inst in db["instances"]:
        if (inst["wrong"] == wrong and inst["right"] == right
                and inst["domain"] == domain):
            return
    
    db["instances"].append(instance)
    
    # 保留上限
    if len(db["instances"]) > _INSTANCE_MAX:
        db["instances"] = db["instances"][-_INSTANCE_MAX:]
    
    _save(db)
    print(f"  [混淆矩阵] 📝 记录实例: {wrong}→{right} ({domain})")


def get_instances(domain: str = "",
                  speaker: str = "",
                  limit: int = 20) -> List[Dict]:
    """获取最近实例（按时间倒序），可筛选领域/说话人"""
    db = _load()
    instances = db.get("instances", [])
    
    if domain:
        instances = [i for i in instances if i.get("domain") == domain]
    if speaker:
        instances = [i for i in instances if i.get("speaker") == speaker]
    
    return instances[-limit:]


# ═══════════════════════════════════════════════════════════════
# 2. 规律提炼
# ═══════════════════════════════════════════════════════════════

def _is_cjk(char: str) -> bool:
    return '\u4e00' <= char <= '\u9fff'


def _phonetic_features(wrong: str, right: str) -> Dict:
    """提取一对(wrong→right)的语音学特征
    
    Returns:
        {
            "edit_type": "substitution"|"insertion"|"deletion",
            "syllables_diff": int,       # 音节数差异
            "tone_similar": bool,        # 声调是否相似
            "initial_same": bool,        # 声母是否相同
            "final_same": bool,          # 韵母是否相同
        }
    """
    # 简化版：对比首个汉字的拼音特征
    # 真正的实现需要pypinyin或类似库
    w_first = wrong[0] if wrong else ""
    r_first = right[0] if right else ""
    
    features = {
        "edit_type": "substitution",  # 默认替代
        "syllables_diff": abs(len(wrong) - len(right)),
        "tone_similar": _is_cjk(w_first) and _is_cjk(r_first),
        "initial_same": False,
        "final_same": False,
    }
    
    # 粗略判断编辑类型
    if len(wrong) < len(right):
        features["edit_type"] = "insertion"
    elif len(wrong) > len(right):
        features["edit_type"] = "deletion"
    
    return features


def _extract_pattern_from_instance(instance: Dict) -> Optional[Dict]:
    """从一条实例提炼规律
    
    提炼层次：
      1. wrong→right 的编辑类型
      2. 上下文关键词（从 video_title/domain 抽取）
      3. 适用的场景类型（语速快？背景噪音？领域术语？）
    
    Returns:
        pattern dict or None
    """
    wrong = instance.get("wrong", "")
    right = instance.get("right", "")
    domain = instance.get("domain", "")
    
    if not wrong or not right:
        return None
    
    features = _phonetic_features(wrong, right)
    
    # 生成可读的规律描述
    pattern_desc = f""
    if wrong and right:
        if domain in ("trading",):
            pattern_desc = f"交易视频中,'{wrong}'可能被误听为'{right}'"
        elif features["edit_type"] == "substitution":
            pattern_desc = f"领域'{domain}'中,'{wrong}'→'{right}'属常见替代"
        else:
            pattern_desc = f"领域'{domain}'中,'{wrong}'→'{right}'属{features['edit_type']}误差"
    
    tags = [domain] if domain else []
    if features["tone_similar"]:
        tags.append("tone_similar")
    tags.append(f"type:{features['edit_type']}")
    
    return {
        "pattern": pattern_desc,
        "domain": domain or "general",
        "confidence": 0.3,  # 单条实例 → 低置信度
        "tags": tags,
        "source_instances": 1,
        "created_at": instance.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S")),
    }


def consolidate(force: bool = False) -> int:
    """将实例提炼为规律（增量）
    
    流程：
    1. 检查已有实例数量，没有新实例就跳过
    2. 对新实例逐一调用 _extract_pattern_from_instance
    3. 相似规律合并（同领域+同编辑类型）
    4. 去重、去低质量
    
    Returns:
        新生成的规律数
    """
    db = _load()
    instances = db.get("instances", [])
    
    if not instances:
        return 0
    
    existing_rules = db.get("rules", [])
    existing_patterns = {(r.get("pattern", ""), r.get("domain", "")) for r in existing_rules}
    
    new_count = 0
    
    for inst in instances[-50:]:  # 只看最近50条
        pattern = _extract_pattern_from_instance(inst)
        if pattern and (pattern["pattern"], pattern["domain"]) not in existing_patterns:
            existing_rules.insert(0, pattern)
            new_count += 1
            existing_patterns.add((pattern["pattern"], pattern["domain"]))
    
    # 相似规律合并（同领域+同类编辑）
    merged_rules = _merge_similar_rules(existing_rules)
    
    # 保留上限
    if len(merged_rules) > _RULE_MAX:
        merged_rules = merged_rules[:_RULE_MAX]
    
    db["rules"] = merged_rules
    db["last_consolidated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save(db)
    
    if new_count > 0:
        print(f"  [混淆矩阵] 🔄 提炼出{new_count}条新规律（共{len(merged_rules)}条）")
    
    return new_count


def _merge_similar_rules(rules: List[Dict]) -> List[Dict]:
    """合并相似规律（同领域+同标签交集）
    
    相似判定：同 domain，且标签交集 ≥1
    """
    groups = defaultdict(list)
    for r in rules:
        key = (r.get("domain", "general"),)
        groups[key].append(r)
    
    merged = []
    for key, group in groups.items():
        seen_patterns = set()
        for r in group:
            p = r.get("pattern", "").strip()
            if p and p not in seen_patterns:
                seen_patterns.add(p)
                merged.append(r)
    
    return merged


# ═══════════════════════════════════════════════════════════════
# 3. 适配 correction 层：为纠错引擎提供上下文
# ═══════════════════════════════════════════════════════════════

def get_relevant_rules(domain: str = "", speaker: str = "", top_n: int = 5) -> List[Dict]:
    """获取与当前视频最相关的规律
    
    排序依据：
      - 同领域 + 同说话人 > 同领域 > 同说话人 > 通用
      - 置信度越高越靠前
    
    Returns:
        规律 dict 列表
    """
    db = _load()
    rules = db.get("rules", [])
    
    def _score(r):
        score = 0
        r_domain = r.get("domain", "")
        if domain and r_domain == domain:
            score += 10
        if r_domain == "general":
            score += 1
        score += r.get("confidence", 0) * 10
        return score
    
    scored = [(r, _score(r)) for r in rules]
    scored.sort(key=lambda x: -x[1])
    
    return [r for r, s in scored[:top_n]]


def format_rules_for_prompt(domain: str = "", speaker: str = "", top_n: int = 5) -> str:
    """格式化规律文本，供注入 LLM prompt
    
    按照"记题型不记题目"原则，只输出规律描述，不带具体实例。
    """
    rules = get_relevant_rules(domain=domain, speaker=speaker, top_n=top_n)
    if not rules:
        return ""
    
    lines = ["## 该领域已知 whisper 误认规律（混淆矩阵）"]
    lines.append("（以下是从历史实例提炼的规律，用于指导修正方向，不用于逐词替换）")
    lines.append("")
    
    for i, rule in enumerate(rules):
        pattern = rule.get("pattern", "")
        conf = rule.get("confidence", 0.3)
        tags = rule.get("tags", [])
        tag_str = ", ".join(t for t in tags if not t.startswith("type:")) if tags else ""
        lines.append(f"  {i+1}. [{rule.get('domain', '通用')}] {pattern}")
        if tag_str:
            lines.append(f"     ({tag_str}, 置信度={conf:.1f})")
        lines.append("")
    
    lines.append("提示：以上规律由代码自动提炼，仅供参考决策，不直接替换文本。")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 4. 集成接口：使 correction_engine 可调用
# ═══════════════════════════════════════════════════════════════

def get_fuzzy_corrections(text: str, domain: str = "") -> List[Dict]:
    """基于混淆矩阵规律，生成可能的修正候选
    
    Returns:
        [{"original": str, "candidates": [{"text": str, "source": str, "confidence": float}], ...}]
    
    规则：
    - 不直接替换，仅提供候选
    - 每个候选标注来源（是哪个规律推导的）
    - 只有置信度≥0.3的规律才产出候选
    """
    rules = get_relevant_rules(domain=domain, top_n=10)
    if not rules or not text:
        return []
    
    corrections = []
    processed_words = set()
    
    for rule in rules:
        pattern = rule.get("pattern", "")
        if not pattern:
            continue
        
        # 从规律描述中提取关键映射
        # 规律格式："交易视频中,'{wrong}'可能被误听为'{right}'"
        import re as _re
        m = _re.search(r"'([^']+)'[^']*'([^']+)'", pattern)
        if not m:
            continue
        wrong, right = m.group(1), m.group(2)
        
        if wrong in processed_words:
            continue
        processed_words.add(wrong)
        
        # 检查文本中是否包含这个错误模式
        if wrong in text:
            corrections.append({
                "original": wrong,
                "candidates": [{
                    "text": right,
                    "source": f"fuzzy_confusion:{rule.get('domain', 'general')}",
                    "confidence": rule.get("confidence", 0.3),
                }],
                "rule_source": pattern,
            })
    
    return corrections


# ═══════════════════════════════════════════════════════════════
# CLI 工具
# ═══════════════════════════════════════════════════════════════

def show_stats() -> str:
    """显示混淆矩阵统计"""
    db = _load()
    instances = db.get("instances", [])
    rules = db.get("rules", [])
    
    lines = [
        "模糊音混淆矩阵统计:",
        f"  实例数: {len(instances)}",
        f"  规律数: {len(rules)}",
        f"  最后合并: {db.get('last_consolidated', '从未')}",
    ]
    
    # 按领域统计
    domain_counts = defaultdict(int)
    for i in instances:
        domain_counts[i.get("domain", "unknown")] += 1
    if domain_counts:
        lines.append("  按领域分布:")
        for d, c in sorted(domain_counts.items(), key=lambda x: -x[1]):
            lines.append(f"    {d}: {c}条")
    
    return "\n".join(lines)

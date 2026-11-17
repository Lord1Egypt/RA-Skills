"""
BiliYouTik2Brain — Corrector Engine L5: 全段降级重处理

最后手段。对所有残留低置信词打包做全段LLM分析。
返回unresolved词直通P2决策，不再尝试覆盖最终文本。

v1.9: L5的全段修正改为仅回传 unresolved 词供P2使用,
      不再覆盖最终文本，防止长文本后半段被截断。
"""

from typing import List, Tuple, Optional
from .utils import call_llm, extract_json, safe_float
from ..corrector_dictionary import DOMAIN_CORRECTIONS


def level5_full_degradation(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    bvid: str = "",
    max_retries: int = 3,
) -> List[dict]:
    """L5: 全段降级重处理 — 残留词兜底
    
    Args:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        bvid: 视频ID
        max_retries: 最大重试次数（应对API限流）
    
    Returns:
        修正候选列表（含l5_unresolved_words直通字段）
    """
    if not low_conf_words:
        return []
    
    candidates = []
    
    # 只处理L1~L4都没解决的低置信词（置信度<0.5 + 长度>=3）
    unresolved = [(w, c) for w, c in low_conf_words if c < 0.5 and len(w) >= 3]
    if not unresolved:
        return []
    
    word_list = "\n".join([f"- {w}" for w, c in unresolved])
    
    messages = [
        {
            "role": "system",
            "content": "你是转录文本修正专家。分析全段文本中的错误，只修正有把握的词。\n\n"
                       "输出JSON: {\"corrections\": [{\"original\": \"词\", \"corrected\": \"修正\", "
                       "\"confidence\": 0.95, \"evidence\": \"根因\"}], "
                       "\"unresolved\": [\"仍然无法确定的词\"]}\n"
                       "corrections: 有把握的修正\n"
                       "unresolved: 不确定的词（直通上级决策）\n"
                       "confidence: 0~1浮点数。"
        },
        {
            "role": "user",
            "content": f"全文:\n{full_text[:3000]}\n\n"
                       f"以下词可能转录错误，请全段判断修正:\n{word_list}\n\n"
                       f"注意: 不确定的词请放入unresolved列表"
        }
    ]
    
    # 重试机制
    for attempt in range(max_retries):
        response = call_llm(messages, timeout=120 * (attempt + 1))
        if not response:
            if attempt < max_retries - 1:
                print(f"  [L5] 第{attempt+1}次LLM无响应, 重试({attempt+2}/{max_retries})...")
                continue
            break
        
        parsed = extract_json(response)
        if parsed:
            # 提取修正
            corrections_list = parsed.get("corrections", [])
            for corr in corrections_list:
                if corr.get("original") and corr.get("corrected") and corr["original"] != corr["corrected"]:
                    candidates.append({
                        "original": corr["original"],
                        "corrected": corr["corrected"],
                        "source": "L5_full_degradation",
                        "confidence": safe_float(corr.get("confidence", 0.5)),
                        "evidence": corr.get("evidence", ""),
                        "context_snippet": full_text[:200],
                    })
            
            # 提取 unresolved 词的直通字段（仅用于标记，不参与修正）
            unresolved_list = parsed.get("unresolved", [])
            if unresolved_list:
                for uw in unresolved_list:
                    candidates.append({
                        "original": uw,
                        "corrected": uw,  # 不修正
                        "source": "L5_full_degradation",
                        "confidence": 0.3,  # 低置信标记
                        "evidence": "L5无法修复（直通P2决策）",
                        "context_snippet": full_text[:200],
                        "_l5_unresolved": True,  # 标记供P2使用
                    })
            
            return candidates
    
    # 所有重试都失败
    # 标记所有unresolved词为L5无法修复
    for w, c in unresolved:
        candidates.append({
            "original": w,
            "corrected": w,
            "source": "L5_full_degradation",
            "confidence": 0.3,
            "evidence": "L5重试失败（直通P2决策）",
            "context_snippet": full_text[:200],
            "_l5_unresolved": True,
        })
    
    return candidates

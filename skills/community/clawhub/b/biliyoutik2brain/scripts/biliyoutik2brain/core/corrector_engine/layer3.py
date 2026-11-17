"""
BiliYouTik2Brain — Corrector Engine L3: 段落级上下文

比L2/L2.5更大上下文（完整段落+说话人知识+OCR帧文字）。
更多token，更高准确性。保留但极少触发（L2.5应该覆盖了所有领域词）。
"""

from typing import List, Tuple, Optional
from .utils import call_llm, extract_json, safe_float


def level3_paragraph_context(
    low_conf_words: List[Tuple[str, float]],
    full_text: str,
    bvid: str = "",
    speaker_knowledge: str = "",
    ocr_text: str = "",
) -> List[dict]:
    """L3: 段落级上下文修复
    
    适用场景:
      1. L2/L2.5无法解决的专业术语（需要完整段落理解）
      2. 需要说话人知识库辅助的领域专用词
      3. OCR帧文字能提供额外线索的专有名词
    
    Args:
        low_conf_words: [(word, confidence), ...]
        full_text: 全量转录文本
        bvid: 视频ID
        speaker_knowledge: 说话人知识库文本
        ocr_text: OCR帧文字参考
    
    Returns:
        修正候选列表
    """
    if not low_conf_words:
        return []
    
    candidates = []
    
    # 只处理L2没覆盖的高价值词（置信度低+长度>=4）
    target_words = [(w, c) for w, c in low_conf_words if c < 0.5 and len(w) >= 4]
    if not target_words:
        return []
    
    # 批量处理: 把所有未解决词打包到一次LLM调用
    word_list_str = "\n".join([f"- {w} (当前置信度={c:.3f})" for w, c in target_words])
    
    messages = [
        {
            "role": "system",
            "content": "你是专业转录文本修正助手，擅长使用段落上下文和领域知识校正语音识别错误。\n\n"
                       "输出JSON: {\"corrections\": [{\"original\": \"词\", \"corrected\": \"修正\", "
                       "\"confidence\": 0.95, \"evidence\": \"凭据\"}]}\n"
                       "confidence必须是0~1浮点数。不做确定性猜测，不确定返回confidence<0.6。"
        },
        {
            "role": "user",
            "content": f"全文段落:\n{full_text[:3000]}\n\n"
                       f"以下词可能转录错误，请根据段落上下文修正:\n{word_list_str}\n\n"
                       f"{'说话人知识: ' + speaker_knowledge[:500] if speaker_knowledge else ''}"
                       f"{'OCR提示: ' + ocr_text[:500] if ocr_text else ''}"
        }
    ]
    
    response = call_llm(messages, timeout=120)
    if not response:
        return []
    
    parsed = extract_json(response)
    if parsed and "corrections" in parsed:
        for corr in parsed["corrections"]:
            candidates.append({
                "original": corr.get("original"),
                "corrected": corr.get("corrected", corr.get("original")),
                "source": "L3_paragraph_ctx",
                "confidence": safe_float(corr.get("confidence", 0.5)),
                "evidence": corr.get("evidence", ""),
                "context_snippet": full_text[:200],
            })
    
    return candidates

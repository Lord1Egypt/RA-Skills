"""
BiliYouTik2Brain — Corrector Engine

v3 重构: extra/transcription_corrector.py (1871行) → 此目录分层

层:
  L1 — 源交叉验证 (成本≈0)
  L2 — LLM局部修复 (小token)
  L2.5 — 句级上下文 (中token)
  L3 — 段落上下文 (大token)
  L4 — OCR帧验证 (下载/GPU成本)
  L5 — 全段降级重处理 (最后手段)

辅助模块:
  utils — 共享工具函数 (JSON提取/LLM调用/排序)
  exit — 退出条件 + 置信度过滤 + 回归检查 + Gotchas
  feedback — 反馈闭环 (题型模式)

使用方式:
    from .corrector_engine import correct_transcription
    result = correct_transcription(text, low_conf_words, ...)
"""

from typing import List, Dict, Tuple, Optional
from .utils import safe_float, sort_low_conf_words
from .layer1 import level1_cross_validate
from .layer2 import level2_llm_local_repair, level2_5_sentence_context
from .layer3 import level3_paragraph_context
from .layer4 import level4_ocr_frame
from .layer5 import level5_full_degradation
from .exit import (
    HARD_THRESHOLD, LAYER_EXIT_THRESHOLD,
    handle_gotchas, check_exit, get_remaining_words,
    filter_by_confidence, regression_check, needs_regression_check,
)
from .feedback import feedback_loop, workflow_recorder
from ..corrector_dictionary import fast_domain_correct, DOMAIN_CORRECTIONS


def correct_transcription(
    text: str,
    segments: List[Dict] = None,
    low_conf_words: List[Tuple[str, float]] = None,
    bvid: str = "",
    bleep_text: str = "",
    subtitle_segments: Optional[List[Dict]] = None,
    video_path: str = "",
    speaker_knowledge: str = "",
    ocr_context: str = "",
    enable_ocr: bool = False,
    l2_max_words: int = 50,
    skip_l3: bool = False,
    skip_l5: bool = False,
) -> dict:
    """层次化修正主入口 — 返回dict兼容旧CorrectionResult
    
    逐层执行，每层修复上一层的残留低置信词。
    错题库记录改为题型模式（classify_by_type=True）。
    
    Args:
        text: 原始whisper转录文本
        segments: 时间分段
        low_conf_words: 低置信词列表 [(word, confidence), ...]
        bvid: 视频ID
        bleep_text: BLEEP检测结果
        subtitle_segments: 官方字幕分段
        video_path: 视频文件路径 (L4 OCR用)
        speaker_knowledge: 说话人知识库文本
        ocr_context: OCR帧文字参考
        enable_ocr: 是否启用L4 OCR
        l2_max_words: L2单次处理的最大词数
        skip_l3: 跳过L3
        skip_l5: 跳过L5
    
    Returns:
        dict: 包含 corrected_text, corrections, final_confidence,
              layers_used, regression_passed, l5_unresolved_words
    """
    result = {
        "bvid": bvid,
        "original_text": text,
        "corrected_text": text,
        "corrections": [],
        "final_confidence": 0.0,
        "layers_used": [],
        "regression_passed": True,
        "total_tokens_saved": 0,
        "l5_full_correction": "",
        "l5_unresolved_words": [],
    }
    
    segments = segments or []
    low_conf_words = low_conf_words or []
    
    if not low_conf_words:
        print(f"  [矫正器] 无低置信词, 跳过")
        result["final_confidence"] = 0.95
        return result
    
    # 按优先级排序
    sorted_words = sort_low_conf_words(low_conf_words)
    print(f"  [矫正器] {len(low_conf_words)}个低置信词, 按优先级排序完成")
    for w, c, p in sorted_words[:5]:
        print(f"    {w} (conf={c:.3f}, pri={p})")
    if len(sorted_words) > 5:
        print(f"    ... +{len(sorted_words)-5}个")
    
    # 逐层执行
    all_candidates = []
    applied_corrections = {}  # word -> {corrected, confidence, source, ...}
    
    layers = {
        "L1_cross_validate": lambda: level1_cross_validate(
            low_conf_words, text, bvid, bleep_text, subtitle_segments
        ),
        "L2_llm_local": lambda: level2_llm_local_repair(
            low_conf_words, text, bvid, bleep_text,
            ocr_text=ocr_context, max_words=l2_max_words
        ),
        "L2_5_sentence_ctx": lambda: level2_5_sentence_context(
            [(w, c) for w, c in sorted(low_conf_words, key=lambda x: x[1])],
            text, bvid
        ),
        "L3_paragraph_ctx": lambda: level3_paragraph_context(
            [(w, c) for w, c in sorted(low_conf_words, key=lambda x: x[1])],
            text, bvid, speaker_knowledge, ocr_text=ocr_context
        ),
    "L4_ocr_frame": lambda: level4_ocr_frame(
        [(w, c) for w, c in sorted(low_conf_words, key=lambda x: x[1])],
        text, segments, bvid, video_path,
        ocr_text=ocr_context,
    ),
        "L5_full_degradation": lambda: level5_full_degradation(
            [(w, c) for w, c in sorted(low_conf_words, key=lambda x: x[1])],
            text, bvid
        ),
    }
    
    # 自动启用L4：明确开启 或 有预计算OCR数据时
    if not enable_ocr and not ocr_context:
        del layers["L4_ocr_frame"]
    elif ocr_context:
        print(f"  [L4] 自动启用(ocr_context={len(ocr_context)}字)")
    if skip_l3:
        del layers["L3_paragraph_ctx"]
    if skip_l5:
        del layers["L5_full_degradation"]
    
    for layer_name, layer_fn in layers.items():
        print(f"  [{layer_name}] 开始...", flush=True)
        
        remaining = get_remaining_words(low_conf_words, applied_corrections)
        if not remaining:
            print(f"    [{layer_name}] 所有低置信词已高置信修正, 跳过")
            continue
        
        new_candidates = layer_fn()
        if not new_candidates:
            print(f"    [{layer_name}] 无修正结果")
            continue
        
        # Gotcha确定性检查
        gotcha_handled = []
        for c in new_candidates:
            gh = handle_gotchas(
                c.get("original", ""),
                c.get("corrected", ""),
                c.get("confidence", 0.0),
                c.get("context_snippet", ""),
            )
            gotcha_handled.append({**c, **gh})
        
        # 硬关阈值过滤
        filtered = filter_by_confidence(gotcha_handled)
        if len(filtered) < len(new_candidates):
            skipped = len(new_candidates) - len(filtered)
            print(f"    [{layer_name}] {skipped}个修正置信度过低(<{HARD_THRESHOLD}), 不应用")
        
        for c in filtered:
            key = c.get("original", "")
            if key in applied_corrections:
                if c.get("confidence", 0) > applied_corrections[key].get("confidence", 0):
                    applied_corrections[key] = c
            else:
                applied_corrections[key] = c
        
        all_candidates.extend(filtered)
        print(f"    [{layer_name}] 新增{len(filtered)}个修正")
        
        # Exit check
        if check_exit(low_conf_words, applied_corrections):
            print(f"    [{layer_name}] ✅ 所有词高置信覆盖, 跳过后续层")
            break
    
    # 应用修正（以原始文本为基底，长文本不替换，只做确定性替换）
    corrected_text = text
    # 先确定性域词典
    corrected_text = fast_domain_correct(corrected_text)
    # 再应用来自LLM各层的高置信修正
    for w, c_info in sorted(applied_corrections.items(), key=lambda x: len(x[0]), reverse=True):
        corrected_w = c_info.get("corrected", w)
        if corrected_w and corrected_w != w and c_info.get("confidence", 0) >= HARD_THRESHOLD:
            # 跳过L5的unresolved标记
            if c_info.get("_l5_unresolved"):
                continue
            corrected_text = corrected_text.replace(w, corrected_w, 1)
    
    result["corrected_text"] = corrected_text
    result["corrections"] = all_candidates
    
    # 最终确定性域词典再跑一次（修正后可能新出现匹配模式）
    result["corrected_text"] = fast_domain_correct(result["corrected_text"])
    
    # 最终置信度
    if applied_corrections:
        confs = [c.get("confidence", 0) for c in applied_corrections.values()]
        result["final_confidence"] = sum(confs) / len(confs)
    else:
        result["final_confidence"] = 0.95
    
    # 记录使用过的层
    layers_used_set = set()
    for c in all_candidates:
        src = c.get("source", "")
        if "_" in src:
            layers_used_set.add(src.split("_")[0])
        else:
            layers_used_set.add(src)
    result["layers_used"] = sorted(layers_used_set) if layers_used_set else ["none"]
    
    # 提取L5 unresolved词（直通P2）
    l5_unresolved = [c.get("original", "") for c in all_candidates
                     if c.get("_l5_unresolved") and c.get("original")]
    result["l5_unresolved_words"] = l5_unresolved
    
    # 回归检查
    if result["corrected_text"] != text:
        if needs_regression_check(len([c for c in all_candidates if c.get("original") != c.get("corrected")]), len(text)):
            passed, issues = regression_check(text, result["corrected_text"])
            result["regression_passed"] = passed
            if not passed:
                print(f"  [回归检查] ⚠️ 回归失败: {issues[:3]}")
                print(f"  [回归检查] 保留原始文本(仅应用确定性域词典)")
                result["corrected_text"] = fast_domain_correct(text)
                result["final_confidence"] *= 0.8
            else:
                print(f"  [回归检查] ✅ 通过")
        else:
            print(f"  [回归检查] 🔹 少量修正, 跳过检查")
            result["regression_passed"] = True
    else:
        result["regression_passed"] = True
    
    # 反馈闭环（题型模式）
    feedback_loop(all_candidates, bvid)
    
    # 工作流数据记录
    app_count = len([c for c in all_candidates if c.get("original") != c.get("corrected")])
    workflow_recorder(
        bvid=bvid,
        text=text,
        low_conf_words=low_conf_words,
        layer_used=result["layers_used"],
        correction_count=len(all_candidates),
        applied_count=app_count,
        final_confidence=result["final_confidence"],
        text_changed=result["corrected_text"] != text,
        regression_passed=result["regression_passed"],
        unresolved_words=l5_unresolved,
        corrections=all_candidates,
    )
    
    print(f"  [矫正器] ✅ 完成: {len(all_candidates)}修正, "
          f"置信度={result['final_confidence']:.2f}, "
          f"层={result['layers_used']}")
    
    return result


__all__ = [
    "correct_transcription",
    "level1_cross_validate", "level2_llm_local_repair",
    "level2_5_sentence_context", "level3_paragraph_context",
    "level4_ocr_frame", "level5_full_degradation",
]

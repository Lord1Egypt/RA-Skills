"""
OCR 引擎适配层 — RapidOCR 主力 + PaddleOCR PPStructure 辅助
=============================================================
v2.0: 更换主力引擎为 RapidOCR (ONNX Runtime，<0.3s 初始化)
      保留 PaddleOCR PPStructure 做版面分析（首次处理某UP主的视频时用）
"""

import os
import time
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

# 尝试导入 OCR 引擎
_RAPIDOCR_AVAILABLE = False
_PADDLEOCR_AVAILABLE = False
_PPSTRUCTURE_AVAILABLE = False

try:
    from rapidocr import RapidOCR
    from rapidocr.utils.typings import LangRec
    _RAPIDOCR_AVAILABLE = True
except ImportError:
    pass

try:
    from paddleocr import PaddleOCR, PPStructure
    _PADDLEOCR_AVAILABLE = True
    try:
        _ = PPStructure(show_log=False)
        _PPSTRUCTURE_AVAILABLE = True
    except Exception:
        pass
except ImportError:
    pass


# ─── OCR 结果类型 ──────────────────────────────────────────

try:
    from .ocr_cross_validator import OCRBlock
except ImportError:
    from ocr_cross_validator import OCRBlock


def create_ocr_engine(
    prefer_engine: str = "rapidocr",
    lang: str = "ch",
    use_server_model: bool = False,
) -> Tuple[Optional[object], str]:
    """
    创建 OCR 引擎，自动选择可用的引擎
    
    Args:
        prefer_engine: 首选引擎 "rapidocr" / "paddleocr"
        lang: 识别语言
        use_server_model: RapidOCR 是否用 server 级模型（更准但更慢）
    
    Returns:
        (engine, engine_name) — 引擎实例和名称，engine 可能为 None
    """
    # 策略 1: RapidOCR (ONNX Runtime)
    if prefer_engine == "rapidocr" and _RAPIDOCR_AVAILABLE:
        try:
            params = {'Rec.lang_type': LangRec(lang)}
            engine = RapidOCR(params=params)
            return engine, "rapidocr"
        except Exception as e:
            logger.warning(f"RapidOCR 初始化失败: {e}")
    
    # 策略 2: PaddleOCR (PaddlePaddle)
    if _PADDLEOCR_AVAILABLE:
        try:
            engine = PaddleOCR(lang=lang, show_log=False)
            return engine, "paddleocr"
        except Exception as e:
            logger.warning(f"PaddleOCR 初始化失败: {e}")
    
    return None, "none"


def run_ocr(
    engine: object,
    engine_name: str,
    image_path: str,
    min_confidence: float = 0.5,
) -> List[OCRBlock]:
    """
    对单张图片跑 OCR
    
    Args:
        engine: OCR 引擎实例
        engine_name: "rapidocr" / "paddleocr"
        image_path: 图片路径
        min_confidence: 最低置信度阈值
    
    Returns:
        OCRBlock 列表
    """
    blocks = []
    
    if engine_name == "rapidocr":
        result = engine(image_path)
        if result is None:
            return blocks
        
        for i in range(len(result.boxes)):
            score = float(result.scores[i]) if hasattr(result, 'scores') else 0.0
            if score < min_confidence:
                continue
            
            text = result.txts[i] if hasattr(result, 'txts') else ''
            box = result.boxes[i].tolist() if hasattr(result.boxes[i], 'tolist') else result.boxes[i]
            
            blocks.append(OCRBlock(
                text=text.strip(),
                score=score,
                box=box,
            ))
    
    elif engine_name == "paddleocr":
        result = engine.ocr(image_path)
        if not result or not result[0]:
            return blocks
        
        for line in result[0]:
            box = line[0]
            text = line[1][0]
            score = line[1][1]
            
            if score < min_confidence:
                continue
            
            blocks.append(OCRBlock(
                text=text.strip(),
                score=score,
                box=box,
            ))
    
    return blocks


def run_layout_analysis(
    image_path: str,
) -> Optional[List[Dict]]:
    """
    PaddleOCR PPStructure 版面分析（仅首次使用）
    
    分析画面布局：区分标题/正文/表格/图片区域
    结果缓存到 speaker_knowledge 的 teaching_patterns.visual_layout
    
    Returns:
        [{'type': 'text'|'table'|'figure'|'title', 'bbox': [x,y,w,h], 'text': str}, ...]
    """
    if not _PPSTRUCTURE_AVAILABLE:
        return None
    
    try:
        engine = PPStructure(show_log=False)
        result = engine(image_path)
        
        layout = []
        for item in result:
            layout.append({
                'type': item.get('type', 'text'),
                'bbox': item.get('bbox', [0, 0, 0, 0]),
                'text': item.get('res', ''),
            })
        return layout
    except Exception as e:
        logger.warning(f"版面分析失败: {e}")
        return None


def precheck_subtitle_region(
    ocr_blocks: List[OCRBlock],
    transcript_text: str,
    image_height: int = 720,
) -> Optional[Dict]:
    """
    预检：通过交叉验证定位字幕区域
    
    对首帧做 OCR + 音频交叉验证，找到字幕文字块的位置
    这个位置缓存在 speaker_knowledge 里，后续处理同一 UP 主的视频时直接复用
    
    Returns:
        {'region_y_range': (y_min, y_max), 'region_x_range': (x_min, x_max)} 或 None
    """
    try:
        from .ocr_cross_validator import classify_ocr_blocks
    except ImportError:
        from ocr_cross_validator import classify_ocr_blocks
    
    if not ocr_blocks or not transcript_text:
        return None
    
    subtitle_blocks, _ = classify_ocr_blocks(ocr_blocks, transcript_text)
    
    if not subtitle_blocks:
        return None
    
    # 计算字幕块的位置范围
    ys = [b.center_y for b in subtitle_blocks]
    xs = [b.center_x for b in subtitle_blocks]
    
    region = {
        'region_y_range': (min(ys) - 20, max(ys) + 20),
        'region_x_range': (min(xs) - 50, max(xs) + 50),
        'detected_height_ratio': min(ys) / image_height,
    }
    
    return region


# ─── 便捷函数：一键 OCR + 分类 + 焦点 ──────────────────────

def process_frame_full(
    ocr_engine, engine_name: str,
    image_path: str,
    transcript_at_timestamp: str,
    min_confidence: float = 0.5,
) -> Dict:
    """
    对一帧做完整的处理：OCR → 分类 → 教学焦点
    
    Returns:
        {
            'image_path': str,
            'all_blocks': List[OCRBlock],
            'subtitle_blocks': List[OCRBlock],
            'teaching_blocks': List[OCRBlock],
            'teaching_focus_score': float,
            'teaching_focus_region': Optional[Dict],
            'is_keyframe': bool,
        }
    """
    try:
        from .ocr_cross_validator import (
            OCRTimelineFrame, classify_ocr_blocks,
            compute_teaching_focus_score, is_keyframe_worthy,
        )
    except ImportError:
        from ocr_cross_validator import (
            OCRTimelineFrame, classify_ocr_blocks,
            compute_teaching_focus_score, is_keyframe_worthy,
        )
    
    # 1. OCR
    blocks = run_ocr(ocr_engine, engine_name, image_path, min_confidence)
    
    # 2. 交叉验证分类
    sub_blocks, teach_blocks = classify_ocr_blocks(blocks, transcript_at_timestamp)
    
    # 3. 教学焦点
    focus_score, focus_region = compute_teaching_focus_score(teach_blocks)
    
    # 4. 构建帧结果
    frame = OCRTimelineFrame(
        timestamp_sec=0,  # 调用方填充
        image_path=image_path,
        blocks=blocks,
        subtitle_blocks=sub_blocks,
        teaching_blocks=teach_blocks,
        teaching_focus_score=focus_score,
        teaching_focus_region=focus_region,
    )
    
    worthy = is_keyframe_worthy(frame)
    
    return {
        'image_path': image_path,
        'all_blocks': blocks,
        'subtitle_blocks': sub_blocks,
        'teaching_blocks': teach_blocks,
        'teaching_focus_score': focus_score,
        'teaching_focus_region': focus_region,
        'is_keyframe': worthy,
    }

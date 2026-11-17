"""
BiliYouTik2Brain — 关键帧 OCR 节点 (v4.0)

转录完成后触发：
1. LLM 语义分析 → 关键帧需求
2. 混合触发决策 → 是否需要 OCR
3. 精准抽帧 → OCR → 交叉验证
4. 合并到最终产物（图文并茂）

这是一个异步节点，不阻塞主转录管线。
"""

import os
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


def node_keyframe_ocr(
    transcript: str = "",
    segments: Optional[List[Dict]] = None,
    video_path: str = "",
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    duration_min: float = 0,
    llm_call_fn: Optional[callable] = None,
    enable_ocr: bool = True,
    enable_clip: bool = True,
    screenshot_dir: str = "",
    **kw,
) -> Dict:
    """关键帧 OCR 节点入口

    Args:
        transcript: 完整转录文本
        segments: 分段列表 [{start, end, text, tokens}]
        video_path: 视频文件路径（用于抽帧）
        video_title: 视频标题
        uploader: UP主
        domain: 领域
        duration_min: 视频时长
        llm_call_fn: LLM 调用函数
        enable_ocr: 是否启用 OCR
        enable_clip: 是否启用 CLIP 视觉确认
        screenshot_dir: 截图保存目录

    Returns:
        {
            "success": bool,
            "keyframe_requests": [...],      # 关键帧需求
            "keyframe_decisions": [...],     # 关键帧决策
            "ocr_results": [...],            # OCR 结果
            "screenshots": [...],            # 截图路径列表
            "report": str,                   # 格式化报告
            "elapsed_ms": float,
        }
    """
    start_time = time.time()
    segments = segments or []

    if not transcript or not segments:
        return {
            "success": False,
            "error": "无转录内容，跳过关键帧分析",
            "keyframe_requests": [],
            "keyframe_decisions": [],
            "ocr_results": [],
            "screenshots": [],
            "report": "📷 关键帧分析：无转录内容",
            "elapsed_ms": 0,
        }

    # 1. 确保截图目录存在
    if not screenshot_dir:
        screenshot_dir = os.path.expanduser("~/.biliyoutik2brain/screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    # 2. 关键帧语义分析 + 触发决策
    from .keyframe_trigger import make_keyframe_decisions, format_decision_report

    decisions = make_keyframe_decisions(
        transcript=transcript,
        segments=segments,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
        duration_min=duration_min,
        llm_call_fn=llm_call_fn,
        enable_clip=enable_clip,
    )

    # 3. 对需要 OCR 的决策点执行 OCR
    ocr_results = []
    screenshots = []

    if enable_ocr and video_path and os.path.exists(video_path):
        for decision in decisions:
            if not decision.should_ocr:
                # 只需截图
                if decision.should_screenshot:
                    ss_path = _capture_screenshot(
                        video_path, decision.timestamp, screenshot_dir
                    )
                    if ss_path:
                        screenshots.append({
                            "timestamp": decision.timestamp,
                            "path": ss_path,
                            "trigger": decision.trigger,
                            "reason": decision.reason,
                        })
                continue

            # 需要 OCR：抽帧 → OCR → 交叉验证
            ocr_result = _process_keyframe_ocr(
                video_path=video_path,
                timestamp=decision.timestamp,
                screenshot_dir=screenshot_dir,
                transcript_segments=segments,
                decision=decision,
            )
            if ocr_result:
                ocr_results.append(ocr_result)
                if ocr_result.get("screenshot_path"):
                    screenshots.append({
                        "timestamp": decision.timestamp,
                        "path": ocr_result["screenshot_path"],
                        "trigger": decision.trigger,
                        "reason": decision.reason,
                        "ocr_text": ocr_result.get("text", "")[:100],
                    })

    # 4. 生成报告
    report = format_decision_report(decisions)
    if ocr_results:
        report += "\n## 📷 OCR 结果\n\n"
        for i, ocr in enumerate(ocr_results, 1):
            ts = ocr.get("timestamp", 0)
            ts_min = int(ts // 60)
            ts_sec = int(ts % 60)
            text = ocr.get("text", "")[:150]
            report += f"{i}. [{ts_min:02d}:{ts_sec:02d}]\n"
            report += f"   OCR: {text}\n"
            if ocr.get("cross_validation"):
                report += f"   交叉验证: {ocr['cross_validation']}\n"
            report += "\n"

    elapsed_ms = (time.time() - start_time) * 1000

    return {
        "success": True,
        "keyframe_decisions": [
            {
                "timestamp": d.timestamp,
                "trigger": d.trigger,
                "priority": d.priority,
                "should_ocr": d.should_ocr,
                "reason": d.reason,
            }
            for d in decisions
        ],
        "ocr_results": ocr_results,
        "screenshots": screenshots,
        "report": report,
        "elapsed_ms": elapsed_ms,
    }


def _capture_screenshot(video_path: str, timestamp: float, output_dir: str) -> Optional[str]:
    """截取视频帧

    Args:
        video_path: 视频路径
        timestamp: 时间戳（秒）
        output_dir: 输出目录

    Returns:
        截图路径或 None
    """
    import subprocess
    ts_min = int(timestamp // 60)
    ts_sec = int(timestamp % 60)
    filename = f"frame_{ts_min:02d}m{ts_sec:02d}s.jpg"
    output_path = os.path.join(output_dir, filename)

    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-ss", str(timestamp),
                "-i", video_path, "-vframes", "1",
                "-q:v", "2", output_path,
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
    except Exception:
        pass

    return None


def _process_keyframe_ocr(
    video_path: str,
    timestamp: float,
    screenshot_dir: str,
    transcript_segments: List[Dict],
    decision,
) -> Optional[Dict]:
    """处理单个关键帧的 OCR

    1. 抽帧（±2 秒抽 3 帧）
    2. 选信息量最大帧
    3. OCR 提取文字
    4. 与转录交叉验证
    """
    # 抽 3 帧
    frames = []
    for offset in [-2, 0, 2]:
        ts = max(0, timestamp + offset)
        path = _capture_screenshot(video_path, ts, screenshot_dir)
        if path:
            frames.append({"path": path, "timestamp": ts})

    if not frames:
        return None

    # 选最佳帧（这里简化为选中间的，实际可用 CLIP 判断信息量）
    best_frame = frames[len(frames) // 2]

    # OCR 提取文字
    ocr_text = _run_ocr_on_image(best_frame["path"])

    # 交叉验证
    cross_val = _cross_validate(ocr_text, transcript_segments, timestamp)

    return {
        "timestamp": timestamp,
        "screenshot_path": best_frame["path"],
        "text": ocr_text,
        "cross_validation": cross_val,
        "trigger": decision.trigger,
        "expected_content": decision.expected_content,
    }


def _run_ocr_on_image(image_path: str) -> str:
    """对单张图片执行 OCR

    优先用 PaddleOCR，降级到 RapidOCR，再降级到空字符串。
    """
    # 尝试 PaddleOCR
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        result = ocr.ocr(image_path, cls=True)
        if result and result[0]:
            texts = [line[1][0] for line in result[0] if line[1][1] > 0.5]
            return " ".join(texts)
    except ImportError:
        pass
    except Exception:
        pass

    # 尝试 RapidOCR
    try:
        from rapidocr_onnxruntime import RapidOCR
        ocr = RapidOCR()
        result, _ = ocr(image_path)
        if result:
            texts = [line[1] for line in result]
            return " ".join(texts)
    except ImportError:
        pass
    except Exception:
        pass

    return ""


def _cross_validate(
    ocr_text: str,
    transcript_segments: List[Dict],
    timestamp: float,
) -> str:
    """交叉验证：OCR 文字 vs 转录文本

    比较时间戳附近的转录内容，判断一致性。
    """
    if not ocr_text:
        return "无 OCR 文字，无法验证"

    # 找时间戳附近的转录段
    nearby_text = ""
    for seg in transcript_segments:
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        if abs(start - timestamp) < 5 or abs(end - timestamp) < 5:
            nearby_text += seg.get("text", "")

    if not nearby_text:
        return "附近无转录内容，无法交叉验证"

    # 提取数字/价格/指标进行比较
    ocr_numbers = _extract_numbers(ocr_text)
    transcript_numbers = _extract_numbers(nearby_text)

    if ocr_numbers and transcript_numbers:
        common = ocr_numbers & transcript_numbers
        if common:
            return f"✅ 一致（共同数字: {', '.join(str(n) for n in sorted(common)[:5])})"
        else:
            return f"⚠️ 数字不一致（OCR: {ocr_numbers}, 转录: {transcript_numbers}）"

    # 简单文本重叠检查
    from difflib import SequenceMatcher
    ratio = SequenceMatcher(None, ocr_text[:200], nearby_text[:200]).ratio()
    if ratio > 0.3:
        return f"✅ 部分一致（相似度 {ratio:.0%}）"
    else:
        return f"⚠️ 内容不同（OCR 提取画面文字，转录是语音，可能互补）"


def _extract_numbers(text: str) -> set:
    """提取文本中的数字"""
    import re
    # 匹配整数和浮点数
    numbers = re.findall(r'\b\d+\.?\d*\b', text)
    return set(float(n) for n in numbers if n)

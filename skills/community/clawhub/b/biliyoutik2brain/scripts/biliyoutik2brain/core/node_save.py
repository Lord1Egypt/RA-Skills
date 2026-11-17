"""
BiliYouTik2Brain — 保存节点

职责：
  1. 保存转录结果到文件（markdown）
  2. 更新说话人知识库
  3. 知识归档（knowledge/ + Karpathy wiki同步）
  4. 记录任务指标
"""

import os, json, time, re, base64
from typing import Dict, List, Tuple

from .schemas import TranscriptionResult
from .config import record_task, PlatformRegistry
from .speaker_knowledge import update_after_video
from .wiki_bridge import wiki_ingest


# ── 存储路径 ──
from .paths import TRANSCRIPTS_DIR as STORAGE_DIR  # 统一路径管理
os.makedirs(STORAGE_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# 保存结果
# ═══════════════════════════════════════════════════════════════

def save_result(result: TranscriptionResult, output_format: str = "note",
                keyframe_data: Dict = None, comments_data: Dict = None) -> str:
    """保存转录结果到文件（支持多格式输出）

    Args:
        result: 转录结果
        output_format: 输出格式（note/rich/data/obsidian）
        keyframe_data: 关键帧 OCR 数据（可选）
        comments_data: 评论分析数据（可选）

    Returns:
        保存的文件路径
    """
    from .output_selector import render_template, OutputContext, auto_select_format, OutputFormat

    bvid = result.video.video_id
    uploader = result.video.uploader
    date = time.strftime("%Y%m%d")
    safe_name = uploader.replace(" ", "_").replace("/", "_")

    url = result.video.url or ""
    m_page = re.search(r'\?p=(\d+)', url)
    page_suffix = f"_p{m_page.group(1)}" if m_page else ""

    # 自动选择格式（如果用户没指定）
    if not output_format:
        ctx = OutputContext(
            duration_min=result.video.duration / 60 if result.video.duration else 0,
            has_keyframes=bool(keyframe_data and keyframe_data.get("screenshots")),
            has_comments=bool(comments_data and comments_data.get("success")),
            has_ocr=bool(keyframe_data and keyframe_data.get("ocr_results")),
        )
        output_format = auto_select_format(ctx)

    # 准备模板数据
    template_data = {
        "title": result.video.title or "无标题",
        "uploader": uploader,
        "platform": result.video.platform.value if hasattr(result.video.platform, 'value') else str(result.video.platform),
        "video_id": bvid,
        "duration_min": f"{result.video.duration / 60:.0f}" if result.video.duration else "0",
        "domain": getattr(result, 'domain', ''),
        "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "transcript": result.corrected_text or result.raw_text or "",
        "summary": (result.analysis or {}).get("summary", ""),
        "keywords": (result.analysis or {}).get("keywords", []),
        "chapters": (result.analysis or {}).get("chapters", []),
        "knowledge_items": (result.analysis or {}).get("knowledge_items", []),
        "segments_json": json.dumps(getattr(result, 'segments', []), ensure_ascii=False),
        "overall_confidence": getattr(result, 'confidence', 0.8),
        "keyframe_decisions_json": json.dumps((keyframe_data or {}).get("keyframe_decisions", []), ensure_ascii=False),
        "ocr_results_json": json.dumps((keyframe_data or {}).get("ocr_results", []), ensure_ascii=False),
        "screenshots_json": json.dumps((keyframe_data or {}).get("screenshots", []), ensure_ascii=False),
        "comments_analysis_json": json.dumps((comments_data or {}).get("semantic_analysis", {}), ensure_ascii=False),
        "valuable_comments_json": json.dumps((comments_data or {}).get("valuable_comments", []), ensure_ascii=False),
        "keyframe_report": (keyframe_data or {}).get("report", ""),
        "comments_report": (comments_data or {}).get("report", ""),
        "sections": _build_sections(result, keyframe_data),
        "tags": [getattr(result, 'domain', 'general'), uploader],
        "asr_engine": getattr(result, 'model_used', 'unknown'),
        "llm_backend": "deepseek",
        "estimated_cost_cny": 0.0,
        "processing_time_ms": getattr(result, 'pipeline_time_s', 0) * 1000,
        "output_format": output_format,
    }

    # 渲染模板
    output_text = render_template(output_format, template_data)

    # 确定文件扩展名
    ext_map = {
        OutputFormat.NOTE: ".md",
        OutputFormat.RICH: ".md",
        OutputFormat.DATA: ".json",
        OutputFormat.OBSIDIAN: ".md",
    }
    ext = ext_map.get(output_format, ".md")

    # 文件名
    filename = f"{safe_name}_{bvid}{page_suffix}_{date}{ext}"
    filepath = os.path.join(STORAGE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output_text)

    result.file_path = filepath
    print(f"  ✅ 已保存 ({output_format}): {os.path.basename(filepath)}")
    return filepath


def _build_sections(result, keyframe_data) -> list:
    """构建图文模板的 sections（带关键帧的转录分段）

    截图自动转为 base64 data URI 嵌入，实现 MD 文件自包含图文并茂。
    """
    sections = []
    segments = getattr(result, 'segments', []) or []
    screenshots = (keyframe_data or {}).get("screenshots", [])
    ocr_results = (keyframe_data or {}).get("ocr_results", [])

    for seg in segments[:20]:  # 最多 20 段
        text = seg.get("text", "") if isinstance(seg, dict) else getattr(seg, 'text', '')
        start = seg.get("start", 0) if isinstance(seg, dict) else getattr(seg, 'start', 0)
        title = text[:50] + ("..." if len(text) > 50 else "")

        # 找对应时间戳的截图和 OCR
        screenshot_uri = ""
        ocr_text = ""
        for ss in screenshots:
            ss_path = ss.get("path", "")
            ss_ts = ss.get("timestamp", 0)
            if abs(ss_ts - start) < 5 and os.path.isfile(ss_path):
                try:
                    with open(ss_path, "rb") as f:
                        img_b64 = base64.b64encode(f.read()).decode()
                    screenshot_uri = f"data:image/png;base64,{img_b64}"
                except (OSError, IOError):
                    screenshot_uri = ""
                break

        for ocr in ocr_results:
            if abs(ocr.get("timestamp", 0) - start) < 5:
                ocr_text = ocr.get("text", "")[:150]
                break

        sections.append({
            "title": title,
            "text": text[:500],
            "screenshot": screenshot_uri,
            "ocr_text": ocr_text,
            "timestamp": start,
        })

    return sections


# ═══════════════════════════════════════════════════════════════
# 节点函数
# ═══════════════════════════════════════════════════════════════

def _node_save_result(**kw) -> TranscriptionResult:
    """节点：保存结果"""
    collect_result = kw.get("collect")
    enhance_result = kw.get("enhance", {})
    transcribe_result = kw.get("transcribe", {})
    assess_result = kw.get("assess", {})
    
    if collect_result is None:
        raise RuntimeError("缺少 video 信息，无法保存")
    
    video = collect_result.video
    corrected_text = (enhance_result.get("corrected_text", "") if isinstance(enhance_result, dict) else "")
    raw_text = (transcribe_result.get("text", "") if isinstance(transcribe_result, dict) else "")
    analysis = (enhance_result.get("analysis", {}) if isinstance(enhance_result, dict) else {})
    
    route = assess_result.get("route") if isinstance(assess_result, dict) else None
    model_used = f"faster-whisper-{route.model}" if route else "faster-whisper-base"
    
    result = TranscriptionResult(video=video)
    result.raw_text = raw_text
    result.corrected_text = corrected_text
    result.analysis = analysis
    result.model_used = model_used
    result.duration_s = video.duration
    result.pipeline_time_s = kw.get("pipeline_time_s", 0)
    
    filepath = save_result(result)
    result.file_path = filepath
    print(f"  ✅ 已保存: {os.path.basename(filepath)}")
    return result


def _node_update_knowledge(**kw) -> None:
    """节点：更新说话人知识库（含自动特征学习）"""
    collect_result = kw.get("collect")
    enhance_result = kw.get("enhance", {})
    corrected_text = (enhance_result.get("corrected_text", "") if isinstance(enhance_result, dict) else "")
    analysis = (enhance_result.get("analysis", {}) if isinstance(enhance_result, dict) else {})
    
    if collect_result and corrected_text and analysis:
        video = collect_result.video
        corrections = enhance_result.get("corrections", []) if isinstance(enhance_result, dict) else []
        # v2.0: 自动提取平台信息
        platform = ""
        if hasattr(video, 'platform'):
            pv = video.platform
            platform = pv.value if hasattr(pv, 'value') else str(pv)
        update_after_video(
            speaker=video.uploader,
            video_title=video.title,
            bvid=video.video_id,
            video_duration=video.duration,
            analysis=analysis,
            corrected_text=corrected_text,
            corrections=corrections if corrections else None,
            platform=platform,
        )


def _node_auto_archive(**kw) -> None:
    """节点：知识自动归档"""
    enhance_result = kw.get("enhance", {})
    collect_result = kw.get("collect")
    
    if not enhance_result or not collect_result:
        return
    
    analysis = enhance_result.get("analysis", {}) if isinstance(enhance_result, dict) else {}
    video = collect_result.video if collect_result else None
    corrected_text = enhance_result.get("corrected_text", "") if isinstance(enhance_result, dict) else ""
    
    if not analysis or not video or not corrected_text:
        return
    
    summary = analysis.get("summary", "")
    keywords = analysis.get("keywords", [])
    domain = analysis.get("domain", "") or enhance_result.get("domain", "")
    
    if not summary or not keywords:
        return
    
    # 按领域创建/追加知识文件
    speaker = video.uploader
    sanitized = re.sub(r'[^\w\u4e00-\u9fff]', '_', speaker)
    from .paths import KNOWLEDGE_DIR
    knowledge_dir = KNOWLEDGE_DIR
    os.makedirs(knowledge_dir, exist_ok=True)
    target_file = os.path.join(knowledge_dir, f"{sanitized}.md")
    
    existing = ""
    if os.path.exists(target_file):
        with open(target_file) as f:
            existing = f.read()
    
    if summary and summary[:60] in existing:
        print(f"  [知识归档] 摘要已存在，跳过")
        return
    
    today = time.strftime("%Y-%m-%d")
    entry = f"""

## {video.title[:60]}
> 来源: {video.url} | 处理日期: {today} | 领域: {domain}

**摘要**: {summary}

**关键词**: {', '.join(keywords[:10]) if keywords else ''}
"""
    
    with open(target_file, 'a') as f:
        f.write(entry)
    print(f"  [知识归档] ✅ {len(entry)}字 → knowledge/{os.path.basename(target_file)}")
    
    # ── 同步到 Karpathy wiki（karpathy-wiki格式） ──
    print(f"  [Wiki入库] ⏳ 准备写入 (speaker={speaker})")
    try:
        wiki_ingest(
            speaker=speaker, summary=summary, keywords=keywords,
            domain=domain, video_title=video.title,
            video_url=video.url, analysis=analysis,
        )
    except Exception as e:
        import traceback
        print(f"  [Wiki入库] ❌ 错误: {e}")
        traceback.print_exc()


def _node_record_task(duration_s: int = 0, model: str = "base",
                       pipeline_time_s: float = 0, **kw) -> None:
    """节点：记录任务指标"""
    record_task(duration_s, model.replace("faster-whisper-", ""), pipeline_time_s, 1.0)


# ================================================================
# 移植自 ZIP v1.x: node_save.py 扩展内容
# ================================================================

def _export_to_bus(result: TranscriptionResult) -> str:
    """将转录+分析结果以结构化 JSON 写入三技能文件总线
    
    产物位置：storage/3skill/bili_video/<video_id>.json
    供 WETALK / schoolmate-jiang / BG吴江 / 其他技能复用。
    """
    bvid = result.video.video_id
    if not bvid:
        return ""
    
    bus_dir = paths.storage_path("3skill", "bili_video")
    os.makedirs(bus_dir, exist_ok=True)
    
    analysis = result.analysis or {}
    
    # 只输出可复用的结构化信息，不 dump 完整转录文本（太大）
    bus_payload = {
        "protocol": "biliyoutik2brain.video_analysis.v2",
        "video_id": bvid,
        "video_title": result.video.title or "",
        "uploader": result.video.uploader or "",
        "url": result.video.url or "",
        "duration_s": result.video.duration or 0,
        "processed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        # 结构化分析（核心可复用内容）
        "analysis": {
            "summary": analysis.get("summary", ""),
            "keywords": analysis.get("keywords", []),
            "chapters": analysis.get("chapters", []),
            "topics": analysis.get("topics", []),
            "key_persons": analysis.get("key_persons", []),
            "essence": analysis.get("essence", ""),
            "usages": analysis.get("usages", []),
            "relations": analysis.get("relations", []),
        },
        # 转录元信息（不含全文）
        "transcript_meta": {
            "char_count": len(result.corrected_text or result.raw_text or ""),
            "model_used": result.model_used or "",
        },
        # 评论洞察
        "comments": {
            "insights": getattr(result.comments, "insights", []),
        },
        # 🆕 v2: OCR v2 两条腿交叉验证产物（画面文字，技能可直接消费）
        "ocr_v2": {
            "engine": getattr(result, "ocr_v2_engine", "") or "",
            "stats": getattr(result, "ocr_v2_stats", {}) or {},
            "frames": getattr(result, "ocr_frames", []) or [],
            "timeline_visual": getattr(result, "timeline_visual", []) or [],
            "teaching_keyframes": getattr(result, "teaching_keyframes", []) or [],
        },
    }
    
    out_path = os.path.join(bus_dir, f"{bvid}.json")
    with open(out_path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(bus_payload, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(out_path + ".tmp", out_path)
    
    return out_path


# ═══════════════════════════════════════════════════════════════
# 节点函数
# ═══════════════════════════════════════════════════════════════



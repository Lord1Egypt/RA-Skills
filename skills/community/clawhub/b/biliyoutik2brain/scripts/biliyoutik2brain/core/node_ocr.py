"""
BiliYouTik2Brain — OCR节点

职责：
  1. 在 assess 完成后与转录并行执行
  2. 只做全视频持久文字提取（≤30帧采样）
  3. 精确定位在 enhance 中完成
"""

import os
from typing import Dict, Tuple, Callable, Optional, List  # 移植自 ZIP


def _node_ocr(**kw) -> Dict:
    """节点：并行OCR提取（与转录同步执行）
    
    在 assess 完成后启动，与 transcribe 并行。
    只做快速初始采样（min_frames=8基线），
    详细自适应抽帧由 enhance 阶段的 Tier 1 回退链负责。
    """
    collect_result = kw.get("collect")
    if not collect_result:
        return {"timeline": [], "persistent_text": ""}
    
    video_path = getattr(collect_result, "video_file", "")
    if not video_path or not os.path.exists(video_path):
        print(f"  [OCR] ⏭️ 无视频文件，跳过")
        return {"timeline": [], "persistent_text": ""}
    
    print(f"  [OCR] 🔄 初始采样(快速基线)...", end="", flush=True)
    try:
        import subprocess
        # 获取视频时长
        dur_result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, timeout=15
        )
        duration_s = float(dur_result.stdout.strip() or 0)
        if duration_s <= 0:
            duration_s = 600
        
        from biliyoutik2brain.extra.ocr_video import ocr_video_targeted, cleanup
        from biliyoutik2brain.extra.transcription_enhancer import get_persistent_text
        
        # 初始快速采样：min_frames=8帧均匀分布（Tier 1 会自动补充更多帧）
        initial_frames = 8
        interval = max(duration_s / initial_frames, 15)
        timestamps = [i * interval for i in range(initial_frames) if i * interval < duration_s]
        
        ocr_data = ocr_video_targeted(video_path, timestamps=timestamps, window_pad=1.0)
        persistent_text = get_persistent_text(ocr_data)
        timeline = ocr_data.get("timeline", [])
        cleanup()
        
        result = {"persistent_text": persistent_text, "timeline": timeline, "video_path": video_path, "duration_s": duration_s}
        print(f" ✅ {len(persistent_text.split(chr(10)) if persistent_text else [])}条文字, {len(timeline)}帧 (基线, 可迭代补充)")
        return result
    except Exception as e:
        print(f" ⚠️ {e}")
        return {"timeline": [], "persistent_text": ""}


# ================================================================
# 移植自 ZIP v1.x: node_ocr.py 扩展内容
# ================================================================

def _fallback_uniform_sample(video_path: str) -> Dict:
    """均匀采样回退（无低置信数据时）"""
    try:
        import subprocess
        dur = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, timeout=15
        )
        duration_s = float(dur.stdout.strip() or 0)
        if duration_s <= 0:
            duration_s = 600
        
        # 均匀采样 ≤ 20帧
        interval = max(duration_s / 20, 30)
        timestamps = [i * interval for i in range(20)]
        timestamps = [t for t in timestamps if t < duration_s]
        
        print(f"  [OCR] 🎯 均匀采样 {len(timestamps)} 帧...")
        engine_name, engine_fn = pick_ocr_engine()
        
        texts = []
        for i, ts in enumerate(timestamps):
            frame_path = f"/tmp/ocr_fallback_{i}.png"
            subprocess.run([
                'ffmpeg', '-y', '-ss', str(ts), '-i', video_path,
                '-frames:v', '1', '-q:v', '2', frame_path
            ], capture_output=True, timeout=15)
            
            if os.path.exists(frame_path):
                try:
                    txt = engine_fn(frame_path)
                    if txt:
                        texts.append(txt)
                except Exception:
                    pass
                try: os.remove(frame_path)
                except: pass
        
        persistent_text = '\n'.join(texts) if texts else ""
        print(f"  [OCR] ✅ {len(texts)}帧有效文字")
        
        return {
            "ocr_applied": True, "has_hard_subs": bool(texts),
            "corrections": [], "corrected_text": persistent_text,
            "corrected_segments": [], "engine": engine_name,
            "stats": {"frames_sampled": len(timestamps), "frames_with_text": len(texts)},
        }
    except Exception as e:
        return {
            "ocr_applied": False, "has_hard_subs": False,
            "corrections": [], "corrected_text": "",
            "corrected_segments": [], "engine": "error",
            "stats": {"reason": str(e)},
        }


# ========= OCR 引擎选择 =========


def has_paddleocr() -> bool:
    """检查 PaddleOCR 是否可用"""
    try:
        import paddleocr
        return True
    except ImportError:
        return False



def ocr_frame_paddle(image_path: str, lang: str = "ch") -> str:
    """PaddleOCR 识别单帧"""
    from paddleocr import PaddleOCR
    if not hasattr(ocr_frame_paddle, '_ocr'):
        ocr_frame_paddle._ocr = PaddleOCR(lang=lang, use_angle_cls=True, show_log=False)
    
    result = ocr_frame_paddle._ocr.ocr(image_path)
    if not result or not result[0]:
        return ""
    
    return " ".join(line[1][0] for line in result[0])



def ocr_frame_qwen_vl(image_path: str) -> str:
    """百炼 qwen-vl-plus 识别单帧"""
    import base64
    with open(image_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    resp = subprocess.run([
        'curl', '-s', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {api_key}',
        '-d', json.dumps({
            "model": "qwen-vl-plus",
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                {"type": "text", "text": "识别图中所有中文文字，只输出文字内容"}
            ]}],
            "max_tokens": 200,
        })
    ], capture_output=True, text=True, timeout=30)
    
    try:
        return json.loads(resp.stdout)['choices'][0]['message']['content'].strip()
    except Exception:
        return ""



def pick_ocr_engine() -> Tuple[str, callable]:
    """按优先级选择 OCR 引擎"""
    if has_paddleocr():
        return "paddleocr_v4", ocr_frame_paddle
    return "qwen_vl", ocr_frame_qwen_vl


# ========= 低置信词反哺 =========


def extract_low_conf_segments(
    transcription_result: Dict,
    confidence_threshold: float = 0.6,
) -> List[Dict]:
    """从转录结果提取低置信segment"""
    segments = transcription_result.get('segments', [])
    low_conf_words = transcription_result.get('low_conf_words', [])
    
    if not low_conf_words or not segments:
        return []
    
    low_conf_set = {w for w, _ in low_conf_words}
    
    result = []
    for seg in segments:
        seg_text = seg.get('text', '')
        found = [w for w in low_conf_set if w in seg_text]
        if found:
            seg_conf = min(
                (prob for w, prob in low_conf_words if w in seg_text),
                default=0.5
            )
            result.append({
                'start': seg['start'],
                'end': seg['end'],
                'confidence': seg_conf,
                'text': seg_text,
                'words': ' '.join(found),
            })
    
    return result



def ocr_correct(
    transcription_result: Dict,
    video_path: str,
    max_frames: int = 20,
    gap_threshold: float = 2.0,
    confidence_threshold: float = 0.6,
) -> Dict:
    """OCR反哺主函数 — 科学抽帧 + 对齐修正"""
    start_time = time.time()

    # 1. 低置信segment提取
    low_segs = extract_low_conf_segments(transcription_result, confidence_threshold)
    if not low_segs:
        return _empty_result(transcription_result, start_time, 'no_low_confidence')

    # 2. 科学抽帧计划
    plan = ocr_sample_plan(low_segs, max_frames, gap_threshold, confidence_threshold)
    pstats = plan_stats(plan, len(low_segs))
    if not plan:
        return _empty_result(transcription_result, start_time, 'empty_plan')

    # 3. 引擎选择
    engine_name, engine_fn = pick_ocr_engine()

    # 4. 逐帧OCR
    segments = transcription_result.get('segments', [])
    corrections = []
    empty_count = 0

    for i, frame in enumerate(plan):
        frame_path = f"/tmp/ocr_correct_{i}.png"
        subprocess.run([
            'ffmpeg', '-y', '-ss', str(frame['time']), '-i', video_path,
            '-frames:v', '1', '-q:v', '2', frame_path
        ], capture_output=True, timeout=15)
        
        if not os.path.exists(frame_path):
            continue
        
        try:
            ocr_text = engine_fn(frame_path)
        except Exception:
            ocr_text = ""
        
        if not ocr_text or len(ocr_text.strip()) < 2:
            empty_count += 1
            try: os.remove(frame_path)
            except: pass
            if empty_count >= 3:
                break
            continue
        
        empty_count = 0
        
        # 对齐
        for seg in segments:
            overlap_start = max(seg['start'], frame['time'] - 1)
            overlap_end = min(seg['end'], frame['time'] + 1)
            if overlap_end > overlap_start:
                seg_text = seg.get('text', '')
                seg_set = set(seg_text)
                ocr_set = set(ocr_text)
                union = seg_set | ocr_set
                sim = len(seg_set & ocr_set) / max(len(union), 1)
                if sim < 0.6:
                    corrections.append({
                        'time': round(frame['time'], 1),
                        'segment_range': f"{seg['start']:.0f}s-{seg['end']:.0f}s",
                        'whisper_text': seg_text[:60],
                        'ocr_text': ocr_text[:100],
                        'similarity': round(sim, 2),
                        'confidence': frame['confidence'],
                    })
        
        try: os.remove(frame_path)
        except: pass

    if not corrections:
        return {
            'corrected': True, 'ocr_applied': True, 'has_hard_subs': False,
            'corrections': [], 'corrected_text': transcription_result.get('full_text', ''),
            'corrected_segments': segments, 'engine': engine_name,
            'stats': {**pstats, 'ocr_results': 0},
            'elapsed_s': round(time.time() - start_time, 1),
        }

    # 应用修正
    corrected_segments = []
    for seg in segments:
        sc = dict(seg)
        for c in corrections:
            if f"{seg['start']:.0f}s" in c['segment_range']:
                sc['text'] = c['ocr_text']
                sc['ocr_corrected'] = True
        corrected_segments.append(sc)
    
    corrected_text = ' '.join(s['text'] for s in corrected_segments)

    return {
        'corrected': True, 'ocr_applied': True, 'has_hard_subs': True,
        'corrections': corrections, 'corrected_text': corrected_text,
        'corrected_segments': corrected_segments, 'engine': engine_name,
        'stats': {**pstats, 'ocr_results': len(corrections)},
        'elapsed_s': round(time.time() - start_time, 1),
    }



def _empty_result(tr, start_time, reason):
    return {
        'corrected': True, 'ocr_applied': False, 'has_hard_subs': False,
        'corrections': [], 'corrected_text': tr.get('full_text', ''),
        'corrected_segments': tr.get('segments', []), 'engine': 'none',
        'stats': {'reason': reason},
        'elapsed_s': round(time.time() - start_time, 1),
    }


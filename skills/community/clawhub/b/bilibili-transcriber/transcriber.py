"""
Bilibili Transcriber - 音频转录模块
使用 faster-whisper 或原始 whisper 实现高效的语音识别，支持模型缓存
支持优先使用B站官方字幕
"""

import os
import functools
import threading
import json
import urllib.request
from typing import Optional, List, Dict, Tuple, Union
from pathlib import Path

# 全局模型缓存
_model_cache = {}
_model_lock = threading.Lock()

# 后端类型
_backend = None  # 'faster_whisper' 或 'whisper'

# ModelScope 模型映射（国内镜像，下载更快）
# faster-whisper 使用 HuggingFace 格式的 CTranslate2 模型
MODELSCOPE_MODELS = {
    "tiny": "pengzhendong/faster-whisper-tiny",
    "base": "pengzhendong/faster-whisper-base",
    "small": "pengzhendong/faster-whisper-small",
    "medium": "pengzhendong/faster-whisper-medium",
    "large": "pengzhendong/faster-whisper-large",
    "large-v2": "pengzhendong/faster-whisper-large-v2",
    "large-v3": "pengzhendong/faster-whisper-large-v3",
    "large-v3-turbo": "pengzhendong/faster-whisper-large-v3-turbo",
}


def _setup_modelscope_for_faster_whisper():
    """
    设置 ModelScope 作为 faster-whisper 的模型源
    这样在国内可以更快下载模型，且只下载一次
    """
    try:
        # 尝试导入 modelscope 并设置环境变量
        import modelscope
        # 设置 ModelScope 作为 HuggingFace 的镜像
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        print("[Transcriber] 已设置 ModelScope/HF-Mirror 作为模型下载源")
        return True
    except ImportError:
        # 如果没有 modelscope，尝试使用 hf-mirror
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        return False


def _detect_backend():
    """检测可用的后端"""
    global _backend
    if _backend is not None:
        return _backend

    # 优先尝试 faster-whisper
    try:
        import faster_whisper
        _backend = 'faster_whisper'
        return _backend
    except ImportError:
        pass

    # 回退到原始 whisper
    try:
        import whisper
        _backend = 'whisper'
        return _backend
    except ImportError:
        pass

    raise ImportError("未找到可用的 whisper 后端，请安装: pip install faster-whisper 或 pip install openai-whisper")


def _get_model_from_modelscope(model_size: str, cache_dir: str) -> str:
    """
    从 ModelScope 获取 faster-whisper 模型
    只下载一次，后续从本地缓存加载
    """
    try:
        from modelscope import snapshot_download

        model_id = MODELSCOPE_MODELS.get(model_size)
        if not model_id:
            raise ValueError(f"不支持的模型大小: {model_size}")

        # 检查本地是否已有模型（ModelScope 使用子目录结构）
        local_model_path = os.path.join(cache_dir, model_id)

        # 如果模型已存在，直接返回路径
        if os.path.exists(local_model_path) and os.path.isdir(local_model_path):
            # 检查是否有模型文件
            model_bin_path = os.path.join(local_model_path, "model.bin")
            if os.path.exists(model_bin_path):
                print(f"[Transcriber] 使用本地缓存模型: {local_model_path}")
                return local_model_path

        # 本地没有，从 ModelScope 下载
        print(f"[Transcriber] 从 ModelScope 下载模型: {model_id}")
        model_dir = snapshot_download(model_id, cache_dir=cache_dir)
        print(f"[Transcriber] 模型下载完成: {model_dir}")
        return model_dir
    except Exception as e:
        print(f"[Transcriber] ModelScope 获取失败: {e}")
        raise


def get_model(model_size: str = "small", device: Optional[str] = None, compute_type: str = "int8",
              use_modelscope: bool = True):
    """
    获取 Whisper 模型实例（带缓存）

    首次调用会加载模型（约2-5秒），后续调用直接返回缓存实例
    模型文件只下载一次，保存在本地缓存目录

    Args:
        model_size: 模型大小 (tiny, base, small, medium, large)
        device: 计算设备 (cuda, cpu)，None 则自动检测
        compute_type: 计算类型 (int8, int8_float16, float16, float32) - 仅 faster-whisper 有效
        use_modelscope: 是否使用 ModelScope 下载模型（国内推荐）

    Returns:
        WhisperModel 实例
    """
    backend = _detect_backend()

    # 简化缓存键，只按模型大小和后端缓存，避免 device/compute_type 变化导致重复加载
    cache_key = f"{backend}_{model_size}"

    if cache_key not in _model_cache:
        with _model_lock:
            # 双重检查，防止多线程重复加载
            if cache_key not in _model_cache:

                # 自动检测设备
                if device is None:
                    try:
                        import torch
                        device = "cuda" if torch.cuda.is_available() else "cpu"
                    except ImportError:
                        device = "cpu"

                if backend == 'faster_whisper':
                    from faster_whisper import WhisperModel
                    print(f"[Transcriber] 正在加载 faster-whisper 模型: {model_size} (设备: {device}, 类型: {compute_type})...")

                    try:
                        # 设置模型下载源
                        if use_modelscope:
                            _setup_modelscope_for_faster_whisper()

                        # 优先检查本地缓存目录
                        cache_dir = os.path.expanduser("~/.cache/modelscope")
                        model_id = MODELSCOPE_MODELS.get(model_size)
                        local_model_path = None

                        if model_id:
                            # ModelScope 使用子目录结构: pengzhendong/faster-whisper-small
                            local_model_path = os.path.join(cache_dir, model_id)

                        # 检查本地是否已有完整模型
                        model_loaded = False
                        if local_model_path and os.path.exists(local_model_path):
                            model_bin = os.path.join(local_model_path, "model.bin")
                            if os.path.exists(model_bin):
                                print(f"[Transcriber] 使用本地缓存模型: {local_model_path}")
                                model = WhisperModel(
                                    local_model_path,
                                    device=device,
                                    compute_type=compute_type,
                                )
                                model_loaded = True

                        # 本地没有完整模型，才需要下载
                        if not model_loaded:
                            if use_modelscope and model_id:
                                try:
                                    print(f"[Transcriber] 本地无缓存，从 ModelScope 下载模型: {model_id}")
                                    from modelscope import snapshot_download
                                    model_dir = snapshot_download(model_id, cache_dir=cache_dir)
                                    print(f"[Transcriber] 模型下载完成: {model_dir}")
                                    model = WhisperModel(
                                        model_dir,
                                        device=device,
                                        compute_type=compute_type,
                                    )
                                except Exception as ms_e:
                                    print(f"[Transcriber] ModelScope 加载失败，使用默认方式: {ms_e}")
                                    model = WhisperModel(
                                        model_size,
                                        device=device,
                                        compute_type=compute_type,
                                    )
                            else:
                                model = WhisperModel(
                                    model_size,
                                    device=device,
                                    compute_type=compute_type,
                                )

                        _model_cache[cache_key] = (backend, model)
                        print(f"[Transcriber] faster-whisper 模型加载完成，已缓存")
                    except Exception as e:
                        print(f"[Transcriber] faster-whisper 加载失败: {e}")
                        print(f"[Transcriber] 尝试回退到原始 whisper...")
                        # 尝试回退到原始 whisper
                        backend = 'whisper'

                if backend == 'whisper':
                    import whisper
                    print(f"[Transcriber] 正在加载 whisper 模型: {model_size}...")
                    model = whisper.load_model(model_size)
                    _model_cache[cache_key] = (backend, model)
                    print(f"[Transcriber] whisper 模型加载完成，已缓存")

    else:
        print(f"[Transcriber] 使用缓存模型: {model_size}")

    return _model_cache[cache_key]


def transcribe_audio(
    audio_path: str,
    language: str = "zh",
    model_size: str = "small",
    device: Optional[str] = None,
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
    use_modelscope: bool = True,
    **kwargs
) -> str:
    """
    转录音频文件为文字

    Args:
        audio_path: 音频文件路径
        language: 语言代码 (zh, en, ja, ko 等)
        model_size: 模型大小
        device: 计算设备
        compute_type: 计算类型
        beam_size: 束搜索宽度
        vad_filter: 是否启用语音活动检测过滤静音
        **kwargs: 其他参数

    Returns:
        转录文本
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    backend, model = get_model(model_size, device, compute_type, use_modelscope)

    if backend == 'faster_whisper':
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            vad_filter=vad_filter,
            **kwargs
        )

        # 合并所有片段文本
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text)

        return "".join(text_parts).strip()
    else:  # whisper
        result = model.transcribe(audio_path, language=language, **kwargs)
        return result["text"].strip()


def transcribe_audio_bytes(
    audio_data: bytes,
    language: str = "zh",
    model_size: str = "small",
    device: Optional[str] = None,
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
    use_modelscope: bool = True,
    **kwargs
) -> str:
    """
    从内存字节数据转录音频（流式处理，无磁盘I/O）

    Args:
        audio_data: 音频文件字节数据
        language: 语言代码
        model_size: 模型大小
        device: 计算设备
        compute_type: 计算类型
        beam_size: 束搜索宽度
        vad_filter: 是否启用 VAD
        **kwargs: 其他参数

    Returns:
        转录文本
    """
    import tempfile
    import os

    # faster-whisper 需要文件路径，使用临时文件
    with tempfile.NamedTemporaryFile(suffix='.m4a', delete=False) as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name

    try:
        result = transcribe_audio(
            tmp_path,
            language=language,
            model_size=model_size,
            device=device,
            compute_type=compute_type,
            beam_size=beam_size,
            vad_filter=vad_filter,
            use_modelscope=use_modelscope,
            **kwargs
        )
        return result
    finally:
        # 清理临时文件
        try:
            os.unlink(tmp_path)
        except:
            pass


def transcribe_with_timestamps_bytes(
    audio_data: bytes,
    language: str = "zh",
    model_size: str = "small",
    device: Optional[str] = None,
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
    use_modelscope: bool = True,
    **kwargs
) -> List[Dict]:
    """
    从内存字节数据转录并返回带时间戳的结果（流式处理）

    Args:
        audio_data: 音频文件字节数据
        language: 语言代码
        model_size: 模型大小
        device: 计算设备
        compute_type: 计算类型
        beam_size: 束搜索宽度
        vad_filter: 是否启用 VAD
        **kwargs: 其他参数

    Returns:
        包含时间戳的片段列表
    """
    import tempfile
    import os

    # faster-whisper 需要文件路径，使用临时文件
    with tempfile.NamedTemporaryFile(suffix='.m4a', delete=False) as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name

    try:
        result = transcribe_with_timestamps(
            tmp_path,
            language=language,
            model_size=model_size,
            device=device,
            compute_type=compute_type,
            beam_size=beam_size,
            vad_filter=vad_filter,
            use_modelscope=use_modelscope,
            **kwargs
        )
        return result
    finally:
        # 清理临时文件
        try:
            os.unlink(tmp_path)
        except:
            pass


def transcribe_with_timestamps(
    audio_path: str,
    language: str = "zh",
    model_size: str = "small",
    device: Optional[str] = None,
    compute_type: str = "int8",
    beam_size: int = 5,
    vad_filter: bool = True,
    use_modelscope: bool = True,
    **kwargs
) -> List[Dict]:
    """
    转录音频并返回带时间戳的结果

    Args:
        audio_path: 音频文件路径
        language: 语言代码
        model_size: 模型大小
        device: 计算设备
        compute_type: 计算类型
        beam_size: 束搜索宽度
        vad_filter: 是否启用 VAD
        **kwargs: 其他参数

    Returns:
        包含时间戳的片段列表，每项为 {"start": float, "end": float, "text": str}
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    backend, model = get_model(model_size, device, compute_type, use_modelscope)

    if backend == 'faster_whisper':
        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            vad_filter=vad_filter,
            **kwargs
        )

        results = []
        for segment in segments:
            results.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })

        return results
    else:  # whisper
        result = model.transcribe(audio_path, language=language, **kwargs)
        # whisper 返回的 segments 格式不同，需要转换
        results = []
        for seg in result.get("segments", []):
            results.append({
                "start": seg.get("start", 0),
                "end": seg.get("end", 0),
                "text": seg.get("text", "").strip()
            })
        return results


def batch_transcribe(
    audio_paths: List[str],
    language: str = "zh",
    model_size: str = "small",
    device: Optional[str] = None,
    compute_type: str = "int8",
    show_progress: bool = True,
    use_modelscope: bool = True,
    **kwargs
) -> Dict[str, str]:
    """
    批量转录多个音频文件（共享模型实例）

    Args:
        audio_paths: 音频文件路径列表
        language: 语言代码
        model_size: 模型大小
        device: 计算设备
        compute_type: 计算类型
        show_progress: 是否显示进度
        use_modelscope: 是否使用 ModelScope 下载模型
        **kwargs: 其他参数

    Returns:
        字典 {音频路径: 转录文本}
    """
    # 预加载模型
    _ = get_model(model_size, device, compute_type, use_modelscope)

    results = {}
    total = len(audio_paths)

    for i, path in enumerate(audio_paths, 1):
        if show_progress:
            print(f"[Transcriber] 处理中 ({i}/{total}): {path}")

        try:
            text = transcribe_audio(
                path,
                language=language,
                model_size=model_size,
                device=device,
                compute_type=compute_type,
                use_modelscope=use_modelscope,
                **kwargs
            )
            results[path] = text
        except Exception as e:
            print(f"[Transcriber] 处理失败 {path}: {e}")
            results[path] = f"[ERROR: {e}]"

    return results


def get_model_info() -> Dict:
    """
    获取当前缓存的模型信息

    Returns:
        模型信息字典
    """
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        cuda_device_count = torch.cuda.device_count() if cuda_available else 0
        cuda_device_name = torch.cuda.get_device_name(0) if cuda_available else None
    except ImportError:
        cuda_available = False
        cuda_device_count = 0
        cuda_device_name = None

    # 检测当前后端
    backend = _detect_backend() if _backend is None else _backend

    info = {
        "backend": backend,
        "cached_models": list(_model_cache.keys()),
        "cuda_available": cuda_available,
        "cuda_device_count": cuda_device_count,
        "cuda_device_name": cuda_device_name,
    }

    return info


def clear_model_cache():
    """清理模型缓存，释放内存"""
    global _model_cache
    _model_cache.clear()
    import gc
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except ImportError:
        pass
    print("[Transcriber] 模型缓存已清理")


# ==================== B站官方字幕功能 ====================

def get_bilibili_subtitle(bvid: str, cid: str, prefer_ai: bool = True) -> Optional[List[Dict]]:
    """
    获取B站视频的官方字幕（CC字幕）

    Args:
        bvid: BV号，如 "BV1GJ411x7h7"
        cid: 视频CID
        prefer_ai: 是否优先使用AI生成字幕

    Returns:
        字幕列表 [{"start": float, "end": float, "text": str}] 或 None
    """
    try:
        # 1. 调用B站API获取字幕列表
        api_url = f'https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}'
        req = urllib.request.Request(api_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'https://www.bilibili.com/video/{bvid}'
        })

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))

        if data.get('code') != 0:
            return None

        subtitle_info = data['data'].get('subtitle', {})
        subtitles = subtitle_info.get('subtitles', [])

        if not subtitles:
            return None

        # 2. 筛选字幕类型
        ai_subtitles = [s for s in subtitles if 'ai' in s.get('lan_doc', '').lower()]
        human_subtitles = [s for s in subtitles if 'ai' not in s.get('lan_doc', '').lower()]

        # 3. 选择优先级
        if prefer_ai and ai_subtitles:
            selected = ai_subtitles[0]
        elif human_subtitles:
            selected = human_subtitles[0]
        elif ai_subtitles:
            selected = ai_subtitles[0]
        else:
            selected = subtitles[0]

        subtitle_url = selected.get('subtitle_url')
        if not subtitle_url:
            return None

        # 4. 下载字幕内容
        if subtitle_url.startswith('//'):
            subtitle_url = 'https:' + subtitle_url

        req = urllib.request.Request(subtitle_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.bilibili.com'
        })

        with urllib.request.urlopen(req, timeout=30) as response:
            subtitle_data = json.loads(response.read().decode('utf-8'))

        # 5. 解析字幕
        results = []
        for item in subtitle_data.get('body', []):
            results.append({
                "start": float(item.get('from', 0)),
                "end": float(item.get('to', 0)),
                "text": item.get('content', '').strip()
            })

        return results

    except Exception as e:
        print(f"[Transcriber] 获取官方字幕失败: {e}")
        return None


def transcribe_bilibili_video(
    bvid: str,
    cid: str,
    audio_path: Optional[str] = None,
    language: str = "zh",
    prefer_subtitle: bool = True,
    **kwargs
) -> Dict:
    """
    转录B站视频（优先使用官方字幕，其次音频转录）

    Args:
        bvid: BV号
        cid: 视频CID
        audio_path: 音频文件路径（无字幕时使用）
        language: 语言代码
        prefer_subtitle: 是否优先使用官方字幕
        **kwargs: 转录参数

    Returns:
        {
            "text": str,           # 完整文本
            "segments": list,      # 带时间戳的片段
            "source": str,         # "subtitle" 或 "transcription"
            "subtitle_type": str   # 字幕类型描述（如果是字幕）
        }
    """
    # 1. 尝试获取官方字幕
    if prefer_subtitle:
        subtitle_data = get_bilibili_subtitle(bvid, cid)
        if subtitle_data:
            full_text = " ".join([s['text'] for s in subtitle_data])
            return {
                "text": full_text,
                "segments": subtitle_data,
                "source": "subtitle",
                "subtitle_type": "官方CC字幕"
            }

    # 2. 无字幕，使用音频转录
    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError(f"无官方字幕且音频文件不存在: {audio_path}")

    segments = transcribe_with_timestamps(audio_path, language=language, **kwargs)
    full_text = " ".join([s['text'] for s in segments])

    return {
        "text": full_text,
        "segments": segments,
        "source": "transcription",
        "subtitle_type": None
    }


# 便捷函数：直接转录
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python transcriber.py <音频文件路径> [语言]")
        print("示例: python transcriber.py audio.wav zh")
        sys.exit(1)

    audio_file = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "zh"

    print(f"转录文件: {audio_file}")
    print(f"语言: {lang}")
    print("-" * 50)

    try:
        text = transcribe_audio(audio_file, language=lang)
        print(text)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

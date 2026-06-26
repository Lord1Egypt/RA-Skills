"""FunASR Paraformer 字幕时间轴对齐 — ASR 精确逐句字幕

分句策略：使用原始文稿（script_text）的标点来确定句子边界，
仅按 逗号/句号/问号/感叹号（，。？！）分句。
FunASR 不加载 PUNC 模型（避免 OOM），因此 ASR 输出无标点，
必须用原文标点对齐。

字幕展示：去掉句尾的逗号和句号（rstrip '，。'），保留问号和感叹号。
"""
import os
import json
import subprocess
import re

# 分句标点：仅这4种
SPLIT_PUNCTS = set("，。？！")
# 展示时去掉的句尾标点（保留 ？和 ！）
STRIP_PUNCTS = "，。"


def _convert_to_wav(audio_path, wav_path):
    """mp3 → 16kHz mono PCM wav（FunASR 要求）"""
    subprocess.run([
        "ffmpeg", "-y", "-i", audio_path,
        "-ar", "16000", "-ac", "1", "-f", "wav",
        wav_path
    ], capture_output=True, check=True)


def _split_by_script_punctuation(script_text):
    """用原始文稿的标点分句，仅按 ，。？！ 分割。

    Returns:
        list[str]: 带标点的句子列表，如 ["你有安排。", "三个字。"]
    """
    # 去掉空白，保留标点
    clean = re.sub(r'\s+', '', script_text)
    sentences = []
    buf = ""
    for ch in clean:
        buf += ch
        if ch in SPLIT_PUNCTS:
            s = buf.strip()
            if s:
                sentences.append(s)
            buf = ""
    if buf.strip():
        sentences.append(buf.strip())
    return sentences


def align_subtitles(audio_path, script_text, work_dir, verbose=True):
    """用 FunASR 对 TTS 音频做 ASR，返回逐句精确字幕时间轴

    Args:
        audio_path: TTS 生成的音频文件 (mp3)
        script_text: 原始文稿文本（带标点，用于分句）
        work_dir: 工作目录（缓存目录）
        verbose: 打印日志

    Returns:
        list[dict]: [{"text": "...", "start": 0.0, "end": 1.5}, ...]
    """
    os.makedirs(work_dir, exist_ok=True)
    cache_path = os.path.join(work_dir, "subs_asr.json")
    wav_path = os.path.join(work_dir, "asr_input.wav")

    # 缓存检查：音频未变则直接返回
    audio_stat = os.path.getsize(audio_path), os.path.getmtime(audio_path)
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("_audio_stat") == list(audio_stat) and cached.get("subs"):
                if verbose:
                    print(f"  ⏭️ 跳过 ASR (缓存): {len(cached['subs'])}句")
                return cached["subs"]
        except (json.JSONDecodeError, KeyError):
            pass

    try:
        from funasr import AutoModel
    except ImportError:
        if verbose:
            print("  ⚠️ FunASR 未安装，使用 TTS 原始字幕")
        return None

    # mp3 → wav
    if verbose:
        print("  🔊 音频转 16kHz wav...")
    _convert_to_wav(audio_path, wav_path)

    # 加载模型（只加载 paraformer-zh，不加载 VAD/PUNC 避免 OOM）
    if verbose:
        print("  🧠 加载 FunASR Paraformer...")
    import time
    t0 = time.time()
    try:
        model = AutoModel(model="paraformer-zh", disable_update=True)
    except Exception as e:
        if verbose:
            print(f"  ⚠️ FunASR 模型加载失败: {e}")
        return None

    if verbose:
        print(f"  模型加载: {time.time()-t0:.1f}s")

    # 推理
    if verbose:
        print("  🎯 ASR 推理中...")
    t1 = time.time()
    res = model.generate(input=wav_path, batch_size_s=300)
    if verbose:
        print(f"  推理耗时: {time.time()-t1:.1f}s")

    if not res or len(res) == 0:
        if verbose:
            print("  ⚠️ FunASR 推理无结果，使用 TTS 原始字幕")
        return None

    item = res[0]
    asr_text = item.get("text", "").replace(" ", "")  # FunASR 输出字符间有空格，去掉
    timestamps = item.get("timestamp", [])

    if not timestamps:
        if verbose:
            print("  ⚠️ FunASR 无时间戳，使用 TTS 原始字幕")
        return None

    # 构建字符→时间戳映射（ASR 无标点，所有字符都有时间戳）
    char_times = []  # [(char, start_ms, end_ms)]
    for ts in timestamps:
        start_ms = ts[0] if isinstance(ts[0], (int, float)) else 0
        end_ms = ts[-1] if isinstance(ts[-1], (int, float)) else start_ms
        # FunASR timestamp 对应 asr_text 中的字符，与 asr_text 1:1
        char_times.append((start_ms, end_ms))

    # 用原始文稿的标点分句
    sentences = _split_by_script_punctuation(script_text)

    # 将句子映射到 ASR 时间戳
    # 原理：文稿去掉标点后的字符序列应与 asr_text 一致，
    # 按顺序消费 char_times，每个非标点字符消费一个时间戳
    subs = []
    ct_idx = 0  # 当前消费到 char_times 的位置

    for sent in sentences:
        start_ms = None
        end_ms = None

        for ch in sent:
            if ch in SPLIT_PUNCTS:
                continue  # 标点无 ASR 对应，跳过

            # 消费下一个 ASR 时间戳
            if ct_idx < len(char_times):
                s, e = char_times[ct_idx]
                ct_idx += 1
                if start_ms is None:
                    start_ms = s
                end_ms = e

        if start_ms is not None and end_ms is not None:
            # 去掉句尾逗号和句号用于展示，保留 ？和 ！
            display_text = sent.rstrip(STRIP_PUNCTS)
            if display_text:
                subs.append({
                    "text": display_text,
                    "start": round(start_ms / 1000.0, 3),
                    "end": round(end_ms / 1000.0, 3),
                })

    # 后处理：确保时间连续（句子间不应有太大间隔）
    if len(subs) > 1:
        for i in range(1, len(subs)):
            gap = subs[i]["start"] - subs[i - 1]["end"]
            if gap > 0.5:
                subs[i]["start"] = round(subs[i - 1]["end"] + 0.3, 3)

    # 验证：ASR 字符数与原文（去标点）字符数应接近
    asr_chars = len(asr_text)
    script_no_punct = re.sub(r'[，。？！；、…—\n\s]+', '', script_text)
    orig_chars = len(script_no_punct)
    if orig_chars > 0 and abs(asr_chars - orig_chars) / orig_chars > 0.2:
        print(f"  ⚠️ ASR 字符数 ({asr_chars}) 与原文去标点 ({orig_chars}) 差距 >20%，时间戳可能不够准确")

    if verbose:
        total_dur = subs[-1]["end"] - subs[0]["start"] if subs else 0
        print(f"  ✅ ASR 对齐完成: {len(subs)}句, 时长 {total_dur:.1f}s")

    # 写缓存
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"_audio_stat": list(audio_stat), "subs": subs}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return subs

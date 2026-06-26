"""BGM 选择 + MiniMax 生成 + ffmpeg 混音

优先级：
  1. 本地 bgm/ 目录已有 MP3（按风格关键词匹配）
  2. 无匹配 → 调用 MiniMax music-2.5+ 生成纯音乐 → 存入 bgm/ 供复用
"""
import os, subprocess, time, requests, json, hashlib

BGM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bgm")

# MiniMax API
MINIMAX_API_URL = "https://api.minimaxi.com/v1/music_generation"
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# 代理配置（MiniMax API 需要代理访问）
PROXY = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY") or None
PROXIES = {"https": PROXY, "http": PROXY} if PROXY else None


# 风格关键词映射（用于本地匹配 + prompt 生成）
STYLE_KEYWORDS = {
    "calm":       ["calm", "quiet", "沉思", "安静", "平静"],
    "uplifting":  ["uplift", "激励", "励志", "轻快", "spring"],
    "lofi":       ["lofi", "lo-fi", "chill", "chillhop", "电子"],
    "dark":       ["dark", "暗调", "深沉", "紧张", "suspense"],
    "piano":      ["piano", "钢琴", "pianist"],
    "corporate":  ["corporate", "商务", "科技", "tech"],
}

def pick_bgm(style=None, verbose=True):
    """从 bgm/ 目录选择 BGM。

    Args:
        style: 风格关键词 (如 "lofi", "dark", "calm")，None=取第一个

    Returns:
        文件路径 or None
    """
    if not os.path.isdir(BGM_DIR):
        if verbose: print("  ⚠️ bgm/ 目录不存在，跳过 BGM")
        return None
    tracks = [f for f in os.listdir(BGM_DIR) if f.endswith(".mp3") and not f.startswith(".")]
    if not tracks:
        if verbose: print("  ⚠️ bgm/ 目录无 MP3 文件，跳过 BGM")
        return None

    if style:
        # 匹配风格关键词
        keywords = STYLE_KEYWORDS.get(style, [style.lower()])
        matched = []
        for t in tracks:
            name_lower = t.lower()
            if any(kw in name_lower for kw in keywords):
                matched.append(t)
        if matched:
            pick = matched[0]
            if verbose: print(f"  🎵 BGM (style={style}): {pick}")
            return os.path.join(BGM_DIR, pick)
        if verbose: print(f"  ⚠️ bgm/ 无匹配 '{style}' 风格，将尝试生成")

    pick = tracks[0]
    if verbose: print(f"  🎵 BGM: {pick}")
    return os.path.join(BGM_DIR, pick)


def generate_bgm(prompt, style_tag="lofi", output_name=None, verbose=True):
    """调用 MiniMax music-2.5+ 生成纯音乐 BGM。

    Args:
        prompt: 音乐描述 prompt（如 "lo-fi chill, 咖啡馆, 沉稳, 中等节奏"）
        style_tag: 风格标签，用于文件命名
        output_name: 输出文件名 (None=自动生成)
        verbose: 是否打印日志

    Returns:
        文件路径 or None
    """
    if not MINIMAX_API_KEY:
        if verbose: print("  ⚠️ MINIMAX_API_KEY 未设置，跳过 BGM 生成")
        return None

    os.makedirs(BGM_DIR, exist_ok=True)

    if verbose:
        print(f"  🎵 MiniMax 生成 BGM 中... (prompt: {prompt[:60]}...)")

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "music-2.5+",
        "prompt": prompt,
        "is_instrumental": True,
        "output_format": "url",
        "audio_setting": {
            "sample_rate": 44100,
            "bitrate": 128000,
            "format": "mp3",
        },
    }

    try:
        resp = requests.post(MINIMAX_API_URL, json=payload, headers=headers, timeout=500, proxies=PROXIES)
        data = resp.json()

        if data.get("base_resp", {}).get("status_code") != 0:
            msg = data.get("base_resp", {}).get("status_msg", "unknown")
            if verbose: print(f"  ⚠️ MiniMax API 错误: {msg}")
            return None

        audio_url = data.get("data", {}).get("audio")
        if not audio_url:
            # 可能是 hex 格式（不应该，我们请求了 url）
            hex_data = data.get("data", {}).get("audio_hex") or data.get("data", {}).get("audio")
            if hex_data and len(hex_data) > 1000:
                # hex 降级处理
                return _save_hex_bgm(hex_data, style_tag, output_name, verbose)
            if verbose: print(f"  ⚠️ MiniMax 未返回音频数据")
            return None

        # 下载音频
        if verbose: print(f"  📥 下载 BGM...")
        dl_resp = requests.get(audio_url, timeout=60, proxies=PROXIES)
        if dl_resp.status_code != 200:
            if verbose: print(f"  ⚠️ 下载失败: HTTP {dl_resp.status_code}")
            return None

        # 保存
        if output_name is None:
            short_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            output_name = f"minimax_{style_tag}_{short_hash}.mp3"
        output_path = os.path.join(BGM_DIR, output_name)
        with open(output_path, "wb") as f:
            f.write(dl_resp.content)

        size_kb = os.path.getsize(output_path) // 1024
        if verbose: print(f"  ✅ BGM 已生成: {output_name} ({size_kb}KB)")
        return output_path

    except requests.Timeout:
        if verbose: print("  ⚠️ MiniMax API 超时")
        return None
    except Exception as e:
        if verbose: print(f"  ⚠️ MiniMax 生成失败: {e}")
        return None


def _save_hex_bgm(hex_data, style_tag, output_name, verbose):
    """将 hex 格式音频数据保存为 MP3"""
    try:
        audio_bytes = bytes.fromhex(hex_data)
        if output_name is None:
            short_hash = hashlib.md5(hex_data.encode()).hexdigest()[:8]
            output_name = f"minimax_{style_tag}_{short_hash}.mp3"
        output_path = os.path.join(BGM_DIR, output_name)
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        size_kb = os.path.getsize(output_path) // 1024
        if verbose: print(f"  ✅ BGM 已生成 (hex): {output_name} ({size_kb}KB)")
        return output_path
    except Exception as e:
        if verbose: print(f"  ⚠️ hex 解码失败: {e}")
        return None


def pick_or_generate_bgm(style="lofi", prompt=None, verbose=True):
    """优先本地，无匹配则 MiniMax 生成。

    Args:
        style: 风格标签 (用于本地匹配)
        prompt: 生成用 prompt (None=根据 style 自动构建)
        verbose: 日志

    Returns:
        BGM 文件路径 or None
    """
    # 1. 尝试本地匹配
    local = pick_bgm(style=style, verbose=verbose)
    if local:
        return local

    # 2. 构建默认 prompt
    if prompt is None:
        prompt = _default_prompt(style)

    # 3. MiniMax 生成
    return generate_bgm(prompt, style_tag=style, verbose=verbose)


def _default_prompt(style):
    """根据风格标签生成默认 prompt"""
    prompts = {
        "lofi": "lo-fi instrumental, chillhop beat, 咖啡馆氛围, 中等节奏, 克制, 无人声",
        "calm": "calm instrumental, 安静, 轻柔, 沉思, 简单钢琴+轻鼓点, 无人声",
        "dark": "dark ambient instrumental, 暗调, 深沉, 紧张感, 电影氛围, 无人声",
        "uplifting": "uplifting instrumental, 轻快, 阳光, 正能量, 节奏明快, 无人声",
        "piano": "minimal piano instrumental, 简洁, 干净, 留白, 沉稳, 无人声",
        "corporate": "corporate tech instrumental, 商务, 科技感, 简洁现代, 无人声",
    }
    return prompts.get(style, f"instrumental background music, {style} style, 无人声")


def mix_audio_with_bgm(voice_path, output_path, bgm_path, volume=0.35,
                       fade_in=2.0, fade_out=2.0, verbose=True):
    """用 ffmpeg 将语音和 BGM 混音（循环+淡入淡出），输出到 output_path。

    替代 MoviePy 的 CompositeAudioClip 方案，单次 ffmpeg 调用完成，
    避免 AudioFileClip 循环引用导致的 reader GC 问题。
    """
    total_dur = _get_duration(voice_path)
    if total_dur is None:
        if verbose: print("  ⚠️ 无法获取语音时长，跳过 BGM")
        return False

    fade_out_start = max(0, total_dur - fade_out)
    cmd = [
        "ffmpeg", "-y",
        "-i", voice_path,
        "-stream_loop", "-1", "-i", bgm_path,
        "-filter_complex",
        f"[1:a]volume={volume},afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={fade_out_start:.1f}:d={fade_out}[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-c:a", "mp3", "-b:a", "192k",
        output_path,
    ]

    if verbose:
        print(f"  🎵 BGM 混音中 ({int(volume*100)}%)...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=500)
        if result.returncode != 0:
            if verbose:
                print(f"  ⚠️ ffmpeg 混音失败: {result.stderr[-200:]}")
            return False
        size_kb = os.path.getsize(output_path) // 1024
        if verbose:
            print(f"  ✅ 混音完成: {output_path} ({size_kb}KB)")
        return True
    except subprocess.TimeoutExpired:
        if verbose: print("  ⚠️ ffmpeg 混音超时")
        return False


def _get_duration(path):
    """用 ffprobe 获取音频时长"""
    try:
        r = subprocess.run(
            ["ffprobe", "-i", path, "-show_entries", "format=duration",
             "-v", "quiet", "-of", "csv=p=0"],
            capture_output=True, text=True, timeout=10)
        return float(r.stdout.strip())
    except:
        return None

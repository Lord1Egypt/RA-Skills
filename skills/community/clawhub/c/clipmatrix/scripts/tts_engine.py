"""
TTS引擎 — ChatTTS → Kokoro → edge-tts 降级链
- 2个固定音色: 男声 spk_52, 女声 spk_heart
- ChatTTS speed_4
- 文字清洗: em dash→逗号, 弯引号→直引号, emoji移除, 数字转英文
"""
import re
import json
import os
import subprocess
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# 可用音色
VOICE_PROFILES = {
    "spk_52": {"gender": "male", "desc": "deep authoritative"},
    "spk_heart": {"gender": "female", "desc": "warm emotional"},
}

TTS_DIR = Path(__file__).parent / "output" / "tts"

def clean_text(text: str) -> str:
    """清洗TTS文本：移除/替换会截断或出错的字符"""
    # em dash → 逗号
    text = text.replace("\u2014", ",").replace("\u2013", ",")
    # 弯引号 → 直引号
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    # 中文→英文映射（常见词汇）
    cn_to_en = {
        "祖母屋": "grandmother's house",
        "摩梭": "Moso",
        "泸沽湖": "Lugu Lake",
        "九寨沟": "Jiuzhaigou",
        "黄龙": "Huanglong",
        "康定": "Kangding",
        "稻城亚丁": "Daocheng Yading",
        "新都桥": "Xinduqiao",
        "西昌": "Xichang",
        "邛海": "Qionghai",
        "松潘": "Songpan",
        "成都": "Chengdu",
        "重庆": "Chongqing",
    }
    for cn, en in cn_to_en.items():
        text = text.replace(cn, en)
    # 移除剩余中文字符
    text = re.sub(r'[\u4e00-\u9fff]+', '', text)
    # 移除 emoji
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF"
        "\U0000FE00-\U0000FE0F"
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    # 多余空格
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_audio_duration(filepath: str) -> float:
    """用ffprobe获取音频实际时长（秒）"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath],
            capture_output=True, text=True, timeout=30
        )
        return float(result.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        logger.warning(f"ffprobe failed for {filepath}: {e}")
        return 0.0


def generate_tts(text: str, voice: str = "spk_heart", output_path: str = None) -> dict:
    """
    生成TTS音频，返回 {path, duration_sec}
    降级链: ChatTTS → Kokoro → edge-tts
    """
    text = clean_text(text)
    if not text.strip():
        return {"path": "", "duration_sec": 0.0}

    TTS_DIR.mkdir(parents=True, exist_ok=True)

    if output_path:
        out_path = output_path
    else:
        # 临时文件名
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()[:12]
        out_path = str(TTS_DIR / f"tts_{h}_{voice}.wav")

    engines = []

    # 1. Kokoro（主引擎，6音色可用）
    try:
        import kokoro_onnx
        engines.append(("kokoro", _try_kokoro, 2))
    except ImportError:
        logger.warning("Kokoro not available")
        pass

    # 2. ChatTTS (v0.2.5, 需模型文件)
    try:
        import ChatTTS
        engines.append(("chattts", _try_chattts, 2))
    except ImportError:
        logger.warning("ChatTTS not available")
        pass

    # 3. edge-tts (always available if installed)
    try:
        import edge_tts
        engines.append(("edge-tts", _try_edge_tts, 1))
    except ImportError:
        logger.warning("edge-tts not available")
        pass

    for name, func, priority in engines:
        try:
            logger.info(f"Trying TTS engine: {name} with voice {voice}")
            func(text, voice, out_path)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                duration = get_audio_duration(out_path)
                if duration > 1.0:
                    logger.info(f"TTS {name} OK: {out_path} ({duration:.1f}s)")
                    return {"path": out_path, "duration_sec": duration, "engine": name}
        except Exception as e:
            logger.warning(f"TTS engine {name} failed: {e}")
            continue

    logger.error("All TTS engines failed")
    return {"path": "", "duration_sec": 0.0}


def _try_chattts(text: str, voice: str, out_path: str):
    """ChatTTS生成 (v0.2.5 API)"""
    import ChatTTS
    import torch
    import soundfile as sf

    spk_id = voice.replace("spk_", "")
    # 不同seed产生不同音色
    seed_map = {"52": 512, "heart": 42}
    seed = seed_map.get(spk_id, 42)

    tts = ChatTTS.Chat()
    # v0.2.5: load() 替代 load_models()
    tts.load()
    torch.manual_seed(seed)

    # 推理参数 - 控制情绪和变化
    # temperature高=更有情绪起伏
    params_infer = ChatTTS.Chat.InferCodeParams(
        temperature=0.5,      # 提高一点，让语调有变化
        top_P=0.7,
        top_K=20,
        prompt="[speed_4]",   # 语速4
    )
    # 精调参数（控制口语自然度）
    params_refine = ChatTTS.Chat.RefineTextParams(
        prompt="[oral_2][laugh_0][break_4]",
    )

    # v0.2.5: skip_refine → skip_refine_text
    wavs = tts.infer(
        [text],
        skip_refine_text=False,
        params_infer=params_infer,
        params_refine=params_refine,
    )
    wav = wavs[0]

    sf.write(out_path, wav, 24000)

    if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
        raise RuntimeError("ChatTTS output too small")


def _try_kokoro(text: str, voice: str, out_path: str):
    """Kokoro TTS生成"""
    from kokoro_onnx import Kokoro
    import soundfile as sf

    # Kokoro voice mapping
    voice_map = {
        "spk_52": "am_adam", "spk_heart": "af_heart",
    }
    kokoro_voice = voice_map.get(voice, "af_bella")

    # Kokoro v0.4.x 需要显式传模型路径
    model_path = os.path.expanduser(
        "~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx")
    voices_path = os.path.expanduser(
        "~/.cache/hyperframes/tts/voices/voices-v1.0.bin")

    kokoro = Kokoro(model_path, voices_path)
    samples, sample_rate = kokoro.create(text, voice=kokoro_voice, speed=1.0)

    sf.write(out_path, samples, sample_rate)

    if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
        raise RuntimeError("Kokoro output too small")


async def _try_edge_tts_async(text: str, voice: str, out_path: str):
    """edge-tts异步生成"""
    import edge_tts

    voice_map = {
        "spk_52": "en-US-GuyNeural",
        "spk_heart": "en-US-JennyNeural",
    }
    edge_voice = voice_map.get(voice, "en-US-JennyNeural")

    communicate = edge_tts.Communicate(text, edge_voice)
    await communicate.save(out_path)


def _try_edge_tts(text: str, voice: str, out_path: str):
    """edge-tts生成（同步封装）"""
    import asyncio
    asyncio.run(_try_edge_tts_async(text, voice, out_path))

    if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
        raise RuntimeError("edge-tts output too small")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Test
    result = generate_tts("Hello, this is a test of the TTS engine.", "spk_heart")
    print(f"Result: {result}")

"""CyberHorn 环境与配置管理。"""
import os
import shutil
import sys
from pathlib import Path

def load_env():
    """从 .env 加载环境变量（若存在）。"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass


def get_env(key: str, default: str | None = None) -> str:
    val = os.environ.get(key, default or "")
    return val.strip() if isinstance(val, str) else ""


def check_env() -> None:
    """检查必需环境与依赖，缺失则报错退出。"""
    load_env()
    missing = []
    provider = get_env("TTS_PROVIDER", "EDGE").upper()

    # 根据 TTS 提供方检查不同的必需项
    if provider == "ELEVEN" or provider == "ELEVENLABS":
        if not get_env("ELEVEN_API_KEY"):
            missing.append("ELEVEN_API_KEY")
        if not get_env("VOICE_ID"):
            missing.append("VOICE_ID")
    elif provider == "EDGE":
        # Edge 在线 TTS 目前只依赖网络，不强制检查额外环境变量
        pass
    else:
        print(f"[CyberHorn] 不支持的 TTS_PROVIDER: {provider}，请在 .env 中设置为 EDGE 或 ELEVEN。", file=sys.stderr)
        sys.exit(1)

    if not get_env("FEISHU_APP_ID"):
        missing.append("FEISHU_APP_ID")
    if not get_env("FEISHU_APP_SECRET"):
        missing.append("FEISHU_APP_SECRET")
    if missing:
        print(f"[CyberHorn] 缺少环境变量: {', '.join(missing)}", file=sys.stderr)
        print("请在 .env 或环境中设置后重试。", file=sys.stderr)
        sys.exit(1)

    # ffmpeg = shutil.which("ffmpeg")
    # if not ffmpeg:
    #     print("[CyberHorn] 未检测到 ffmpeg，请先安装并加入 PATH。", file=sys.stderr)
    #     sys.exit(1)


# 供 OpenClaw/CLI 使用的便捷配置
def get_eleven_config():
    return {
        "api_key": get_env("ELEVEN_API_KEY"),
        "voice_id": get_env("VOICE_ID"),
    }


def get_feishu_config():
    return {
        "app_id": get_env("FEISHU_APP_ID"),
        "app_secret": get_env("FEISHU_APP_SECRET"),
    }


def get_ffmpeg_path() -> str:
    """优先用系统 PATH 中的 ffmpeg，否则用 .env 的 FFMPEG_PATH（可为目录或可执行文件路径）。"""
    load_env()
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    path = get_env("FFMPEG_PATH")
    if not path:
        return "ffmpeg"
    p = Path(path)
    if p.is_dir():
        return str(p / ("ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"))
    return path


def get_tts_provider() -> str:
    """
    返回当前 TTS 提供方标识。
    默认使用 EDGE，可通过 TTS_PROVIDER 覆盖为 EDGE 或 ELEVEN。
    """
    return get_env("TTS_PROVIDER", "EDGE").upper()


def get_edge_config() -> dict:
    """
    Edge TTS 相关配置。
    目前仅支持通过 EDGE_VOICE 指定语音，未设置时使用一个中文女声默认值。
    """
    voice = get_env("EDGE_VOICE") or "zh-CN-XiaoxiaoNeural"
    return {
        "voice": voice,
    }

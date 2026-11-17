"""应用配置"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # 路径
    DATA_DIR: Path = Path(__file__).parent.parent / "data"
    DOWNLOAD_DIR: Path = DATA_DIR / "downloads"
    AUDIO_DIR: Path = DATA_DIR / "audio"
    TRANSCRIPT_DIR: Path = DATA_DIR / "transcripts"
    REWRITE_DIR: Path = DATA_DIR / "rewrites"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    TEMP_DIR: Path = DATA_DIR / "temp"
    FRONTEND_DIR: Path = Path(__file__).parent.parent / "frontend"
    DEFAULT_AVATAR: Path = Path(__file__).parent / "assets" / "default_avatar.png"

    # LLM
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # ASR
    WHISPER_MODEL: str = "base"

    # TTS
    TTS_ENGINE: str = "edge"  # edge | melotts | cosyvoice

    # 数字人
    DIGITAL_HUMAN_MODE: str = "sadtalker"  # sadtalker | wav2lip | api
    SADTALKER_REF_IMAGE: str = ""

    # 下载代理（绕过平台反爬，如 http://127.0.0.1:7890）
    DOWNLOAD_PROXY: str = ""

    # 超时
    DOWNLOAD_TIMEOUT: int = 120
    PROCESS_TIMEOUT: int = 400

    # 任务清理（秒）
    TASK_CLEANUP_AFTER: int = 7200

    # 端口
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# 确保目录存在
for d in [settings.DOWNLOAD_DIR, settings.AUDIO_DIR,
          settings.TRANSCRIPT_DIR, settings.REWRITE_DIR,
          settings.OUTPUT_DIR, settings.TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

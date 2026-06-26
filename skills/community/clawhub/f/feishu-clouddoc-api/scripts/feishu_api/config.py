from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from .token_store import read_env_file, seed_shared_user_token, user_token_env


def resolve_env_file() -> Path | None:
    custom = os.getenv("FEISHU_ENV_FILE", "").strip()
    if custom:
        return Path(custom).expanduser()
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        return cwd_env
    package_env = Path(__file__).resolve().parents[1] / ".env"
    if package_env.exists():
        return package_env
    return None


@dataclass(slots=True)
class Settings:
    app_id: str
    app_secret: str
    base_url: str = "https://open.feishu.cn"
    log_level: str = "INFO"
    user_access_token: str = ""
    user_refresh_token: str = ""
    user_open_id: str = ""
    user_access_token_expires_at: str = ""
    user_refresh_token_expires_at: str = ""
    env_file: str = ""
    user_token_file: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        env_file = resolve_env_file()
        if env_file:
            load_dotenv(env_file, override=False)
        file_env = read_env_file(env_file)

        def env_value(name: str, default: str = "") -> str:
            return os.getenv(name, "").strip() or file_env.get(name, "").strip() or default

        app_id = env_value("FEISHU_APP_ID")
        app_secret = env_value("FEISHU_APP_SECRET")
        base_url = env_value("FEISHU_BASE_URL", "https://open.feishu.cn")
        log_level = env_value("FEISHU_LOG_LEVEL", "INFO") or "INFO"

        if not app_id:
            raise ValueError("Missing FEISHU_APP_ID")
        if not app_secret:
            raise ValueError("Missing FEISHU_APP_SECRET")

        seed_shared_user_token(app_id, env_file)
        token_file, token_env = user_token_env(app_id, env_file)

        def token_value(name: str) -> str:
            return token_env.get(name, "").strip() or os.getenv(name, "").strip() or file_env.get(name, "").strip()

        return cls(
            app_id=app_id,
            app_secret=app_secret,
            base_url=base_url,
            log_level=log_level,
            user_access_token=token_value("FEISHU_USER_ACCESS_TOKEN"),
            user_refresh_token=token_value("FEISHU_USER_REFRESH_TOKEN"),
            user_open_id=token_value("FEISHU_USER_OPEN_ID"),
            user_access_token_expires_at=token_value("FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT"),
            user_refresh_token_expires_at=token_value("FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT"),
            env_file=str(env_file or ""),
            user_token_file=str(token_file),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()

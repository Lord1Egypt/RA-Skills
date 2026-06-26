from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AMATH_",
        extra="ignore",
    )

    server_name: str = "amath-skill"
    base_url: str = "https://amath.socthink.cn"
    api_prefix: str = "/api"
    timeout_seconds: float = 30.0
    verify_ssl: bool = True
    user_agent: str = "amath-skill/0.1.0"
    default_system_name: str = "奥数探险课"
    auto_persist_token: bool = True
    access_token: str | None = Field(default=None, description="Optional default bearer token")

    @property
    def api_base(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.api_prefix}"


settings = Settings()

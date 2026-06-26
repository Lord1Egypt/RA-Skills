"""Configuration settings for geminipdfocr."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Geminipdfocr configuration settings. Credentials from system env only."""

    google_api_key: str = ""
    ocr_max_concurrent: int = 4
    ocr_model: str = "gemini-2.0-flash"

    model_config = SettingsConfigDict(
        extra="ignore",
    )


settings = Settings()

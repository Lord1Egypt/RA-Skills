from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from pathlib import Path
from typing import Optional
import os
from urllib.parse import quote, urlparse


class Settings(BaseSettings):
    # Calibre OpenClaw Server
    CALIBRE_DB_PATH: str = Field(default="")
    CALIBRE_LIBRARY_PATH: str = Field(default="")
    SERVER_PORT: int = Field(default=6180)
    SERVER_HOST: str = Field(default="127.0.0.1")

    # API security
    API_KEY: Optional[SecretStr] = Field(default=None)
    ALLOW_UNAUTHENTICATED: bool = Field(default=False)
    # When true, GET /health is reachable without an API key (useful for
    # external monitoring/load balancers). Deny by default; the endpoint still
    # works with a valid API key when this is false.
    PUBLIC_HEALTHCHECK: bool = Field(default=False)
    CORS_ALLOW_ORIGINS: str = Field(default="http://127.0.0.1:6180,http://localhost:6180")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=False)
    ALLOW_BOOK_CONTENT_DOWNLOADS: bool = Field(default=False)
    ENABLE_NETWORK_BINDINGS_ENDPOINT: bool = Field(default=False)
    ENABLE_NETWORK_BINDINGS_MONITOR: bool = Field(default=False)
    ALLOW_GET_AUTO_SYNC: bool = Field(default=False)
    
    # Ollama
    OLLAMA_HOST: str = Field(default="http://localhost:11434")
    OLLAMA_MODEL: str = Field(default="nomic-embed-text-v2-moe:latest")
    ALLOW_REMOTE_OLLAMA: bool = Field(default=False)
    
    # Embeddings
    CHUNK_SIZE: int = Field(default=500)
    CHUNK_OVERLAP: int = Field(default=50)
    SIMILARITY_THRESHOLD: float = Field(default=0.3)
    RAG_STOP_AT_LOCAL: str = Field(default="")
    RAG_IDLE_SLEEP_SECONDS: int = Field(default=60)
    RAG_TIMER_ON_CALENDAR: str = Field(default="")
    RAG_RUNTIME_MAX_SEC: str = Field(default="")
    RAG_PREFETCH_RANDOM_BOOKS: bool = Field(default=False)
    RAG_RECONCILE_ON_START: bool = Field(default=False)
    INSTALL_NIGHTLY_EMBEDDINGS: bool = Field(default=False)
    # Manual version counter for the embedding pipeline. Bump this (or change
    # OLLAMA_MODEL / chunk settings) to force every stored embedding to be
    # invalidated and regenerated with the new configuration.
    EMBEDDING_VERSION: int = Field(default=1)
    
    # PostgreSQL
    POSTGRESQL_DB_USER: str = Field(default="")
    POSTGRESQL_DB_PASSWD: SecretStr = Field(default=SecretStr(""))
    POSTGRESQL_DB_DATABASE: str = Field(default="")
    POSTGRESQL_DB_HOST: str = Field(default="localhost")
    POSTGRESQL_DB_PORT: int = Field(default=5432)
    
    # Logs
    LOG_DIR: str = Field(default="/mnt/Backup_2/Biblioteca/logs")
    LOG_LEVEL: str = Field(default="INFO")
    LOG_RETENTION_DAYS: int = Field(default=30)
    LOG_COMPRESS: bool = Field(default=True)
    
    # VirusTotal
    VT_API_KEY: Optional[SecretStr] = Field(default=None)
    
    # OpenLibrary
    OPENLIBRARY_ENABLED: bool = Field(default=True)
    OPENLIBRARY_BASE_URL: str = Field(default="https://openlibrary.org")
    OPENLIBRARY_ACCESS_KEY: Optional[SecretStr] = Field(default=None)
    OPENLIBRARY_SECRET_KEY: Optional[SecretStr] = Field(default=None)
    
    # Download Queue
    DOWNLOAD_DIR: str = Field(default="")
    DOWNLOAD_QUEUE_ENABLED: bool = Field(default=True)
    DOWNLOAD_AUTO_PROCESS: bool = Field(default=True)
    DOWNLOAD_IDLE_SLEEP_SECONDS: int = Field(default=60)
    DOWNLOAD_MAX_CONCURRENT: int = Field(default=3)
    
    @property
    def postgres_dsn(self) -> str:
        user = quote(self.POSTGRESQL_DB_USER, safe="")
        password = quote(self.POSTGRESQL_DB_PASSWD.get_secret_value(), safe="")
        host = self.POSTGRESQL_DB_HOST
        port = self.POSTGRESQL_DB_PORT
        database = quote(self.POSTGRESQL_DB_DATABASE, safe="")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    @property
    def api_key_value(self) -> Optional[str]:
        if self.API_KEY is None:
            return None
        value = self.API_KEY.get_secret_value().strip()
        return value or None

    @property
    def cors_allow_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ALLOW_ORIGINS.split(",")
            if origin.strip()
        ]
    
    @property
    def log_dir_path(self) -> Path:
        return Path(self.LOG_DIR)

    def validate_security(self) -> None:
        weak_passwords = {"", "password", "your_password", "your_password_here", "changeme", "change-me"}
        if not self.CALIBRE_DB_PATH:
            raise RuntimeError("CALIBRE_DB_PATH must be configured in .env")
        if not self.CALIBRE_LIBRARY_PATH:
            raise RuntimeError("CALIBRE_LIBRARY_PATH must be configured in .env")
        if not self.POSTGRESQL_DB_USER or not self.POSTGRESQL_DB_DATABASE:
            raise RuntimeError("PostgreSQL user and database must be configured in .env")
        if self.POSTGRESQL_DB_PASSWD.get_secret_value().strip().lower() in weak_passwords:
            raise RuntimeError("POSTGRESQL_DB_PASSWD must be set to a non-default strong password")
        if not self.ALLOW_UNAUTHENTICATED and not self.api_key_value:
            raise RuntimeError("API_KEY must be set, or ALLOW_UNAUTHENTICATED=true must be explicitly configured")
        if "*" in self.cors_allow_origins_list and self.CORS_ALLOW_CREDENTIALS:
            raise RuntimeError("CORS_ALLOW_CREDENTIALS=true cannot be used with wildcard CORS origins")
        ollama_host = urlparse(self.OLLAMA_HOST).hostname
        if not self.ALLOW_REMOTE_OLLAMA and ollama_host not in {"localhost", "127.0.0.1", "::1"}:
            raise RuntimeError("OLLAMA_HOST must be local unless ALLOW_REMOTE_OLLAMA=true is explicitly configured")
    
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


def load_settings() -> Settings:
    """Load settings from .env file in multiple locations."""
    env_dir = os.environ.get("ENV_DIR")
    env_file = None
    
    if env_dir:
        env_file = Path(env_dir) / ".env"
        if not env_file.exists():
            env_file = None
    
    if not env_file:
        # Try current directory
        if Path(".env").exists():
            env_file = Path(".env")
    
    if env_file:
        return Settings(_env_file=str(env_file), _env_file_encoding="utf-8")
    return Settings()


settings = load_settings()

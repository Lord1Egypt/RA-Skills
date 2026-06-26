from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Settings:
    """
    全局配置读取器。
    相对路径一律按 config.yaml 所在目录解析。
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        self.config_path = Path(config_path).resolve()
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        self.base_dir = self.config_path.parent

        with self.config_path.open("r", encoding="utf-8") as f:
            self._data: Dict[str, Any] = yaml.safe_load(f) or {}

        self._normalize_paths()
        self._ensure_directories()

    def get(self, *keys: str, default: Optional[Any] = None) -> Any:
        data: Any = self._data
        for key in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(key)
            if data is None:
                return default
        return data

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def _normalize_paths(self) -> None:
        """
        将 config.yaml 中的相对路径统一转换为绝对路径。
        """
        path_fields = [
            "company_file",
            "source_file",
            "output_excel_dir",
            "output_word_dir",
            "log_dir",
            "db_file",
            "cache_dir",
            "temp_dir",
            "excel_template",
            "word_template",
        ]

        paths = self._data.get("paths", {})
        if not isinstance(paths, dict):
            return

        for field in path_fields:
            value = paths.get(field)
            if not value:
                continue

            p = Path(value)
            if not p.is_absolute():
                paths[field] = str((self.base_dir / p).resolve())
            else:
                paths[field] = str(p.resolve())

    def _ensure_directories(self) -> None:
        path_keys = [
            ("paths", "output_excel_dir"),
            ("paths", "output_word_dir"),
            ("paths", "log_dir"),
            ("paths", "cache_dir"),
            ("paths", "temp_dir"),
        ]

        for keys in path_keys:
            path_value = self.get(*keys)
            if path_value:
                Path(path_value).mkdir(parents=True, exist_ok=True)

        db_file = self.get("paths", "db_file")
        if db_file:
            Path(db_file).parent.mkdir(parents=True, exist_ok=True)


_settings_instance: Optional[Settings] = None


def get_settings(config_path: str = "config.yaml") -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings(config_path=config_path)
    return _settings_instance
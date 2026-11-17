import json
import os
import shutil
from pathlib import Path
from typing import Any


class BaselineManager:
    def __init__(self, baseline_root: str | Path, project_name: str, config: dict):
        self.project_name = project_name
        explicit_dir = config.get("baseline_dir")
        self.baseline_dir = Path(explicit_dir) if explicit_dir else Path(baseline_root) / project_name
        self.config = config
        self.atomic = config.get("atomic_write", True)
        self.full_index_file = config.get("full_index_file", "full_index.json")
        self.vector_cache_file = config.get("vector_cache_file", "vector_cache.json")
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.baseline_dir / name

    def _atomic_write(self, path: Path, data: Any) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        if isinstance(data, (dict, list)):
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            tmp.write_text(str(data), encoding="utf-8")
        if self.atomic:
            os.replace(tmp, path)
        else:
            shutil.move(tmp, path)

    def write_json(self, name: str, data: dict | list) -> None:
        self._atomic_write(self._path(name), data)

    def read_json(self, name: str) -> dict | list:
        path = self._path(name)
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def write_text(self, name: str, content: str) -> None:
        self._atomic_write(self._path(name), content)

    def read_text(self, name: str) -> str:
        path = self._path(name)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def exists(self, name: str) -> bool:
        return self._path(name).exists()

    def delete(self, name: str) -> None:
        self._path(name).unlink(missing_ok=True)

    def list_files(self) -> list[str]:
        return [p.name for p in self.baseline_dir.iterdir() if p.is_file()]

    def get_baseline(self) -> dict:
        return self.read_json(self.full_index_file)

    def save_baseline(self, data: dict) -> None:
        self.write_json(self.full_index_file, data)

    def get_vector_cache(self) -> dict:
        return self.read_json(self.vector_cache_file)

    def save_vector_cache(self, data: dict) -> None:
        self.write_json(self.vector_cache_file, data)

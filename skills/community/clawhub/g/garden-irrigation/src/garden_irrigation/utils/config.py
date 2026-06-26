from __future__ import annotations

from pathlib import Path
import json
import shutil


class Config:
    def __init__(self, root: Path):
        self.root = root
        self.config_dir = root / 'config'
        self._sync_parent_config()
        self.system = self._load_json('system.json')
        self.zones = self._load_json('zones.json').get('zones', [])

    def _sync_parent_config(self):
        """Overwrite local config files with any matching files from ../config/."""
        parent_config = self.root.parent / 'config'
        if not parent_config.is_dir():
            return
        for src in parent_config.iterdir():
            if src.is_file():
                shutil.copy2(src, self.config_dir / src.name)

    @property
    def data_dir(self) -> Path:
        """Always use ../data/, creating it if needed."""
        parent_data = self.root.parent / 'data'
        parent_data.mkdir(parents=True, exist_ok=True)
        return parent_data

    def _load_json(self, name: str):
        with open(self.config_dir / name, 'r', encoding='utf-8') as f:
            return json.load(f)
